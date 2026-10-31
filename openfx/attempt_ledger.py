"""Separate append-only ledger for pre-registration execution attempts.

This ledger records request/validation/registration outcomes. It is deliberately
not a trial registry and never consumes or changes a trial-family budget.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GENESIS = "0" * 64
EVENT_TYPES = {
    "started",
    "pre_registration_rejected",
    "registration_failed",
    "trial_registered",
    "reconciliation_required",
}
TERMINAL_TYPES = EVENT_TYPES - {"started"}
ALLOWED_PAYLOAD_KEYS = {
    "started": {"request_sha256", "job_id", "family_id", "trial_id"},
    "pre_registration_rejected": {"error_code", "error_type"},
    "registration_failed": {"error_code", "error_type"},
    "trial_registered": {
        "registry_event_id", "registry_event_sha256", "registry_sequence"
    },
    "reconciliation_required": {"reason_code"},
}


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    ).encode("utf-8")


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _event_hash(event: dict[str, Any]) -> str:
    return _sha256(canonical_json(event))


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


class AttemptLedgerError(ValueError):
    """Raised when an attempt ledger operation or integrity check fails."""


class LocalAttemptLedger:
    """Single-host JSONL event chain for attempts before durable trial admission.

    A started attempt must end in exactly one terminal attempt event. The
    trial registry remains authoritative for accepted trial lifecycle/outcomes.
    """

    def __init__(self, path: str | Path, *, lock_timeout_seconds: float = 3.0):
        self.path = Path(path)
        self.lock_path = self.path.with_suffix(self.path.suffix + ".lock")
        self.lock_timeout_seconds = lock_timeout_seconds

    @staticmethod
    def _validate_payload(event_type: str, payload: dict[str, Any]) -> None:
        if not isinstance(payload, dict):
            raise AttemptLedgerError("payload must be an object")
        allowed = ALLOWED_PAYLOAD_KEYS[event_type]
        if set(payload) - allowed:
            raise AttemptLedgerError("payload contains unsupported or unsafe fields")
        required = {
            "started": {"request_sha256"},
            "pre_registration_rejected": {"error_code"},
            "registration_failed": {"error_code"},
            "trial_registered": {
                "registry_event_id", "registry_event_sha256", "registry_sequence"
            },
            "reconciliation_required": {"reason_code"},
        }[event_type]
        if not required.issubset(payload):
            raise AttemptLedgerError("payload is missing required fields")
        for key in ("request_sha256", "registry_event_sha256"):
            if key in payload and (
                not isinstance(payload[key], str)
                or len(payload[key]) != 64
                or any(char not in "0123456789abcdef" for char in payload[key].lower())
            ):
                raise AttemptLedgerError(f"invalid {key}")
        for key in ("job_id", "family_id", "trial_id", "error_code", "error_type",
                    "registry_event_id", "reason_code"):
            if key in payload and (
                not isinstance(payload[key], str) or not payload[key].strip()
                or len(payload[key]) > 160
            ):
                raise AttemptLedgerError(f"invalid {key}")
        if "registry_sequence" in payload and (
            isinstance(payload["registry_sequence"], bool)
            or not isinstance(payload["registry_sequence"], int)
            or payload["registry_sequence"] < 1
        ):
            raise AttemptLedgerError("invalid registry_sequence")

    def _read_and_verify(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        rows: list[dict[str, Any]] = []
        previous = GENESIS
        seen_event_ids: set[str] = set()
        attempts: dict[str, list[dict[str, Any]]] = {}
        expected_keys = {
            "schema_version", "sequence", "event_id", "attempt_id",
            "event_type", "occurred_at_utc", "payload",
            "previous_event_sha256", "event_sha256",
        }
        for line_number, line in enumerate(
            self.path.read_text(encoding="utf-8").splitlines(), 1
        ):
            if not line.strip():
                raise AttemptLedgerError(f"blank line at ledger line {line_number}")
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise AttemptLedgerError(f"invalid JSON at ledger line {line_number}") from exc
            if not isinstance(row, dict) or set(row) != expected_keys:
                raise AttemptLedgerError(f"unexpected event fields at ledger line {line_number}")
            supplied_hash = row.pop("event_sha256")
            if row["schema_version"] != 1:
                raise AttemptLedgerError("unsupported attempt event schema version")
            if row["previous_event_sha256"] != previous or supplied_hash != _event_hash(row):
                raise AttemptLedgerError(f"hash-chain verification failed at ledger line {line_number}")
            if (
                isinstance(row["sequence"], bool)
                or not isinstance(row["sequence"], int)
                or row["sequence"] != len(rows) + 1
            ):
                raise AttemptLedgerError(f"invalid sequence at ledger line {line_number}")
            if not isinstance(row["event_id"], str) or not row["event_id"].strip():
                raise AttemptLedgerError(f"invalid event_id at ledger line {line_number}")
            if row["event_id"] in seen_event_ids:
                raise AttemptLedgerError(f"duplicate event_id at ledger line {line_number}")
            if not isinstance(row["attempt_id"], str) or not row["attempt_id"].strip():
                raise AttemptLedgerError(f"invalid attempt_id at ledger line {line_number}")
            event_type = row["event_type"]
            if not isinstance(event_type, str) or event_type not in EVENT_TYPES:
                raise AttemptLedgerError(f"invalid event_type at ledger line {line_number}")
            if not isinstance(row["payload"], dict):
                raise AttemptLedgerError(f"invalid payload at ledger line {line_number}")
            self._validate_payload(event_type, row["payload"])
            try:
                datetime.fromisoformat(row["occurred_at_utc"].replace("Z", "+00:00"))
            except (AttributeError, ValueError) as exc:
                raise AttemptLedgerError(f"invalid timestamp at ledger line {line_number}") from exc

            prior = attempts.get(row["attempt_id"], [])
            if not prior and event_type != "started":
                raise AttemptLedgerError("attempt must begin with started")
            if prior and (prior[-1]["event_type"] != "started" or event_type == "started"):
                raise AttemptLedgerError("attempt already has a terminal event")
            row["event_sha256"] = supplied_hash
            rows.append(row)
            attempts.setdefault(row["attempt_id"], []).append(row)
            seen_event_ids.add(row["event_id"])
            previous = supplied_hash
        return rows

    def verify(self) -> dict[str, Any]:
        rows = self._read_and_verify()
        attempts: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            attempts.setdefault(row["attempt_id"], []).append(row)
        return {
            "valid": True,
            "event_count": len(rows),
            "attempt_count": len(attempts),
            "open_attempt_count": sum(
                events[-1]["event_type"] == "started" for events in attempts.values()
            ),
            "last_event_sha256": rows[-1]["event_sha256"] if rows else GENESIS,
        }

    def append(
        self, *, event_id: str, attempt_id: str, event_type: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(event_id, str) or not event_id.strip():
            raise AttemptLedgerError("event_id must be non-empty")
        if not isinstance(attempt_id, str) or not attempt_id.strip():
            raise AttemptLedgerError("attempt_id must be non-empty")
        if not isinstance(event_type, str) or event_type not in EVENT_TYPES:
            raise AttemptLedgerError("unsupported attempt event type")
        self._validate_payload(event_type, payload)

        self.path.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.monotonic() + self.lock_timeout_seconds
        fd = None
        while fd is None:
            try:
                fd = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise AttemptLedgerError("attempt ledger lock timeout; inspect stale lock")
                time.sleep(0.025)
        try:
            rows = self._read_and_verify()
            for old in rows:
                if old["event_id"] == event_id:
                    if (old["attempt_id"], old["event_type"], old["payload"]) != (
                        attempt_id, event_type, payload
                    ):
                        raise AttemptLedgerError("event_id reused with different content")
                    return old

            prior = [row for row in rows if row["attempt_id"] == attempt_id]
            if not prior and event_type != "started":
                raise AttemptLedgerError("attempt must begin with started")
            if prior and (prior[-1]["event_type"] != "started" or event_type == "started"):
                raise AttemptLedgerError("attempt already has a terminal event")

            event = {
                "schema_version": 1,
                "sequence": len(rows) + 1,
                "event_id": event_id,
                "attempt_id": attempt_id,
                "event_type": event_type,
                "occurred_at_utc": _utc_now(),
                "payload": payload,
                "previous_event_sha256": rows[-1]["event_sha256"] if rows else GENESIS,
            }
            event["event_sha256"] = _event_hash(event)
            with self.path.open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(json.dumps(event, sort_keys=True, ensure_ascii=False) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
            return event
        finally:
            os.close(fd)
            try:
                self.lock_path.unlink()
            except FileNotFoundError:
                pass
