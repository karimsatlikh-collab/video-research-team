"""Adversarial tests for the separate pre-registration attempt ledger."""
import json
import tempfile
import unittest
from pathlib import Path

from openfx.attempt_ledger import AttemptLedgerError, LocalAttemptLedger


HASH = "a" * 64


class LocalAttemptLedgerTests(unittest.TestCase):
    def test_records_rejected_attempt_without_trial_lifecycle_or_budget_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = LocalAttemptLedger(Path(tmp) / "attempts.jsonl")
            started = ledger.append(
                event_id="attempt-1-started", attempt_id="attempt-1",
                event_type="started",
                payload={"request_sha256": HASH, "job_id": "job-1",
                         "family_id": "family-1", "trial_id": "trial-1"},
            )
            rejected = ledger.append(
                event_id="attempt-1-rejected", attempt_id="attempt-1",
                event_type="pre_registration_rejected",
                payload={"error_code": "invalid_contract", "error_type": "ValueError"},
            )
            self.assertEqual(started["sequence"], 1)
            self.assertEqual(rejected["sequence"], 2)
            self.assertEqual(ledger.verify()["attempt_count"], 1)
            self.assertEqual(ledger.verify()["open_attempt_count"], 0)
            self.assertNotIn("trial_index", rejected)
            self.assertNotIn("max_trials", rejected)

    def test_registered_attempt_links_to_trial_registry_without_owning_trial_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = LocalAttemptLedger(Path(tmp) / "attempts.jsonl")
            ledger.append(
                event_id="a-start", attempt_id="a", event_type="started",
                payload={"request_sha256": HASH},
            )
            registered = ledger.append(
                event_id="a-registered", attempt_id="a", event_type="trial_registered",
                payload={"registry_event_id": "trial-pending-1",
                         "registry_event_sha256": HASH, "registry_sequence": 1},
            )
            self.assertEqual(registered["event_type"], "trial_registered")
            self.assertEqual(ledger.verify()["open_attempt_count"], 0)

    def test_interleaved_attempts_are_independently_validated(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = LocalAttemptLedger(Path(tmp) / "attempts.jsonl")
            for attempt in ("a", "b"):
                ledger.append(
                    event_id=f"{attempt}-start", attempt_id=attempt,
                    event_type="started", payload={"request_sha256": HASH},
                )
            ledger.append(
                event_id="a-rejected", attempt_id="a",
                event_type="registration_failed", payload={"error_code": "lock_timeout"},
            )
            ledger.append(
                event_id="b-rejected", attempt_id="b",
                event_type="pre_registration_rejected",
                payload={"error_code": "schema_invalid"},
            )
            self.assertEqual(ledger.verify()["attempt_count"], 2)
            self.assertEqual(ledger.verify()["event_count"], 4)

    def test_idempotent_event_retry_returns_existing_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = LocalAttemptLedger(Path(tmp) / "attempts.jsonl")
            first = ledger.append(
                event_id="a-start", attempt_id="a", event_type="started",
                payload={"request_sha256": HASH},
            )
            again = ledger.append(
                event_id="a-start", attempt_id="a", event_type="started",
                payload={"request_sha256": HASH},
            )
            self.assertEqual(first, again)
            self.assertEqual(ledger.verify()["event_count"], 1)

    def test_rejects_second_start_and_second_terminal_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = LocalAttemptLedger(Path(tmp) / "attempts.jsonl")
            ledger.append(event_id="a-start", attempt_id="a", event_type="started",
                          payload={"request_sha256": HASH})
            with self.assertRaises(AttemptLedgerError):
                ledger.append(event_id="a-start-2", attempt_id="a", event_type="started",
                              payload={"request_sha256": HASH})
            ledger.append(event_id="a-reject", attempt_id="a",
                          event_type="pre_registration_rejected",
                          payload={"error_code": "bad_input"})
            with self.assertRaises(AttemptLedgerError):
                ledger.append(event_id="a-second-terminal", attempt_id="a",
                              event_type="registration_failed",
                              payload={"error_code": "later_error"})

    def test_rejects_terminal_event_without_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = LocalAttemptLedger(Path(tmp) / "attempts.jsonl")
            with self.assertRaises(AttemptLedgerError):
                ledger.append(event_id="orphan", attempt_id="missing",
                              event_type="pre_registration_rejected",
                              payload={"error_code": "bad_input"})

    def test_rejects_raw_exception_message_and_unknown_payload_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = LocalAttemptLedger(Path(tmp) / "attempts.jsonl")
            with self.assertRaises(AttemptLedgerError):
                ledger.append(event_id="unsafe", attempt_id="a", event_type="started",
                              payload={"request_sha256": HASH, "exception_message": "/home/user/token"})
            ledger.append(event_id="a-start", attempt_id="a", event_type="started",
                          payload={"request_sha256": HASH})
            with self.assertRaises(AttemptLedgerError):
                ledger.append(event_id="a-failed", attempt_id="a",
                              event_type="registration_failed",
                              payload={"error_code": "internal", "error": "secret"})

    def test_detects_hash_chain_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "attempts.jsonl"
            ledger = LocalAttemptLedger(path)
            ledger.append(event_id="a-start", attempt_id="a", event_type="started",
                          payload={"request_sha256": HASH})
            row = json.loads(path.read_text(encoding="utf-8"))
            row["payload"]["request_sha256"] = "b" * 64
            path.write_text(json.dumps(row) + "\n", encoding="utf-8")
            with self.assertRaises(AttemptLedgerError):
                ledger.verify()

    def test_reports_unfinished_attempt_as_open_not_as_failed(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = LocalAttemptLedger(Path(tmp) / "attempts.jsonl")
            ledger.append(event_id="a-start", attempt_id="a", event_type="started",
                          payload={"request_sha256": HASH})
            status = ledger.verify()
            self.assertEqual(status["open_attempt_count"], 1)
            self.assertTrue(status["valid"])

    def test_lock_timeout_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = LocalAttemptLedger(Path(tmp) / "attempts.jsonl",
                                        lock_timeout_seconds=0.01)
            ledger.lock_path.parent.mkdir(parents=True, exist_ok=True)
            ledger.lock_path.write_text("stale", encoding="utf-8")
            with self.assertRaisesRegex(AttemptLedgerError, "lock timeout"):
                ledger.append(event_id="a-start", attempt_id="a", event_type="started",
                              payload={"request_sha256": HASH})


if __name__ == "__main__":
    unittest.main()
