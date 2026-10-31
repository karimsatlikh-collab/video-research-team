"""A bounded deterministic OpenFX research-team workflow kernel.

No network, shell, broker, model API, or paid-service access is provided.
"""
from __future__ import annotations
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

class Role(str, Enum):
    ORCHESTRATOR = "orchestrator"
    SOURCE_RESEARCHER = "source_researcher"
    CRITICAL_REVIEWER = "critical_reviewer"

class Status(str, Enum):
    PROPOSED = "proposed"
    READY = "ready"
    RUNNING = "running"
    REVIEW_PENDING = "review_pending"
    COMPLETED = "completed"
    REJECTED = "rejected"
    BLOCKED = "blocked"
    FAILED = "failed"

_TRANSITIONS = {
    Status.PROPOSED: {Status.READY, Status.BLOCKED, Status.REJECTED},
    Status.READY: {Status.RUNNING, Status.BLOCKED, Status.REJECTED},
    Status.RUNNING: {Status.REVIEW_PENDING, Status.BLOCKED, Status.FAILED},
    Status.REVIEW_PENDING: {Status.COMPLETED, Status.READY, Status.REJECTED},
    Status.BLOCKED: {Status.READY, Status.REJECTED},
    Status.FAILED: {Status.READY, Status.REJECTED},
    Status.COMPLETED: set(), Status.REJECTED: set(),
}

@dataclass
class WorkItem:
    work_id: str
    title: str
    question: str
    producer_role: str
    acceptance_criteria: list[str]
    expected_outputs: list[str]
    risk_class: str = "low"
    inputs: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    requires_paid_resource: bool = False
    paid_resource_approved: bool = False
    status: str = Status.PROPOSED.value
    evidence: list[dict[str, str]] = field(default_factory=list)
    review_findings: list[str] = field(default_factory=list)
    decision: str | None = None
    created_at_utc: str = field(default_factory=_now)
    updated_at_utc: str = field(default_factory=_now)

    def validate(self) -> None:
        if not _ID_RE.fullmatch(self.work_id):
            raise ValueError("invalid work_id")
        for key in ("title", "question"):
            if not getattr(self, key).strip():
                raise ValueError(f"{key} must not be empty")
        if self.producer_role != Role.SOURCE_RESEARCHER.value:
            raise ValueError("producer_role must be source_researcher")
        if self.status not in {x.value for x in Status}:
            raise ValueError("invalid status")
        if not self.acceptance_criteria or any(not x.strip() for x in self.acceptance_criteria):
            raise ValueError("acceptance criteria are required")
        if not self.expected_outputs or any(not x.strip() for x in self.expected_outputs):
            raise ValueError("expected outputs are required")
        if self.risk_class not in {"low", "medium", "high", "critical"}:
            raise ValueError("invalid risk_class")
        if self.paid_resource_approved and not self.requires_paid_resource:
            raise ValueError("approval set without a paid resource requirement")
        if self.status in {Status.REVIEW_PENDING.value, Status.COMPLETED.value} and not self.evidence:
            raise ValueError("review/completion requires evidence")

class ResearchTeam:
    """Single-process queue with role-checked handoffs and independent review."""
    def __init__(self, items: list[WorkItem] | None = None):
        self.items: dict[str, WorkItem] = {}
        for item in items or []:
            item.validate()
            if item.work_id in self.items:
                raise ValueError("duplicate work_id")
            self.items[item.work_id] = item

    def create(self, item: WorkItem, actor: str) -> WorkItem:
        if actor != Role.ORCHESTRATOR.value:
            raise PermissionError("only orchestrator creates work items")
        item.validate()
        if item.work_id in self.items:
            raise ValueError("duplicate work_id")
        self.items[item.work_id] = item
        return item

    def transition(self, work_id: str, target: Status, actor: str) -> WorkItem:
        item = self._get(work_id)
        if target not in _TRANSITIONS[Status(item.status)]:
            raise ValueError(f"illegal transition: {item.status} -> {target.value}")
        if target == Status.READY and actor != Role.ORCHESTRATOR.value:
            raise PermissionError("only orchestrator approves readiness")
        if target == Status.RUNNING:
            if actor != item.producer_role:
                raise PermissionError("only assigned producer may start")
            if item.requires_paid_resource and not item.paid_resource_approved:
                raise PermissionError("paid resource needs explicit approval")
        if target in {Status.BLOCKED, Status.FAILED} and actor not in {Role.ORCHESTRATOR.value, item.producer_role}:
            raise PermissionError("actor cannot change this state")
        if target == Status.REJECTED and actor != Role.ORCHESTRATOR.value:
            raise PermissionError("only orchestrator may reject")
        item.status, item.updated_at_utc = target.value, _now()
        return item

    def submit(self, work_id: str, actor: str, evidence: list[dict[str, str]]) -> WorkItem:
        item = self._get(work_id)
        if actor != item.producer_role:
            raise PermissionError("only assigned producer submits")
        if item.status != Status.RUNNING.value:
            raise ValueError("only running work may be submitted")
        if not evidence:
            raise ValueError("submission requires evidence")
        for record in evidence:
            if not isinstance(record, dict) or not record.get("kind") or not record.get("reference"):
                raise ValueError("each evidence record needs kind and reference")
        item.evidence = [dict(x) for x in evidence]
        item.status, item.updated_at_utc = Status.REVIEW_PENDING.value, _now()
        return item

    def review(self, work_id: str, actor: str, accepted: bool, findings: list[str]) -> WorkItem:
        item = self._get(work_id)
        if actor != Role.CRITICAL_REVIEWER.value or actor == item.producer_role:
            raise PermissionError("only an independent critical reviewer may review")
        if item.status != Status.REVIEW_PENDING.value:
            raise ValueError("item is not awaiting review")
        if not findings:
            raise ValueError("review findings are required")
        item.review_findings = list(findings)
        item.status = Status.COMPLETED.value if accepted else Status.READY.value
        item.decision = "accepted" if accepted else "revise"
        item.updated_at_utc = _now()
        return item

    def _get(self, work_id: str) -> WorkItem:
        if work_id not in self.items:
            raise KeyError(f"unknown work_id: {work_id}")
        return self.items[work_id]

    def save(self, path: str | Path) -> None:
        dest = Path(path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        data = {"schema_version": 1, "items": [asdict(x) for x in self.items.values()]}
        temp = dest.with_suffix(dest.suffix + ".tmp")
        temp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        temp.replace(dest)

    @classmethod
    def load(cls, path: str | Path) -> "ResearchTeam":
        data: dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
        if data.get("schema_version") != 1 or not isinstance(data.get("items"), list):
            raise ValueError("unsupported queue schema")
        return cls([WorkItem(**row) for row in data["items"]])
