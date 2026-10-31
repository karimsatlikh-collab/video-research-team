"""Reproducible microbenchmark for the deterministic research-team workflow.

Measures local software overhead only. It is not a manual baseline and does not
measure human research time or prove project-level time savings.
"""
from __future__ import annotations
import json
import statistics
import tempfile
import time
from pathlib import Path

from openfx.research_team import ResearchTeam, Role, Status, WorkItem


def run_benchmark(iterations: int = 100) -> dict[str, object]:
    if not 1 <= iterations <= 10000:
        raise ValueError("iterations must be between 1 and 10000")
    durations_ms: list[float] = []
    with tempfile.TemporaryDirectory() as directory:
        queue_path = Path(directory) / "queue.json"
        team = ResearchTeam()
        for index in range(iterations):
            started = time.perf_counter_ns()
            work_id = f"bench-{index:05d}"
            item = WorkItem(
                work_id=work_id,
                title="Synthetic source audit",
                question="Does this synthetic source support the test claim?",
                producer_role=Role.SOURCE_RESEARCHER.value,
                acceptance_criteria=["fixture locator exists", "critical tokens preserved"],
                expected_outputs=["source-record.json"],
            )
            team.create(item, Role.ORCHESTRATOR.value)
            team.transition(work_id, Status.READY, Role.ORCHESTRATOR.value)
            team.transition(work_id, Status.RUNNING, Role.SOURCE_RESEARCHER.value)
            team.submit(work_id, Role.SOURCE_RESEARCHER.value, [
                {"kind": "fixture", "reference": f"synthetic://fixture/{index}"}
            ])
            team.review(work_id, Role.CRITICAL_REVIEWER.value, True, ["synthetic checks passed"])
            durations_ms.append((time.perf_counter_ns() - started) / 1_000_000)
        save_started = time.perf_counter_ns()
        team.save(queue_path)
        save_ms = (time.perf_counter_ns() - save_started) / 1_000_000
        load_started = time.perf_counter_ns()
        restored = ResearchTeam.load(queue_path)
        load_ms = (time.perf_counter_ns() - load_started) / 1_000_000
        if len(restored.items) != iterations:
            raise RuntimeError("queue round-trip lost work items")
    ordered = sorted(durations_ms)
    p95_index = min(len(ordered) - 1, int(0.95 * len(ordered)))
    return {
        "benchmark": "openfx_research_team_kernel_v1",
        "iterations": iterations,
        "completed_items": iterations,
        "median_item_lifecycle_ms": round(statistics.median(durations_ms), 4),
        "p95_item_lifecycle_ms": round(ordered[p95_index], 4),
        "queue_save_ms": round(save_ms, 4),
        "queue_reload_ms": round(load_ms, 4),
        "note": "Local deterministic software overhead only; no manual baseline or human-time savings measured.",
    }


if __name__ == "__main__":
    print(json.dumps(run_benchmark(), indent=2))
