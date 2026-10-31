import tempfile
import unittest
from pathlib import Path
from openfx.research_team import ResearchTeam, Role, Status, WorkItem

def sample(**updates):
    values = dict(work_id="audit-001", title="Audit source", question="Does source support claim?",
        producer_role=Role.SOURCE_RESEARCHER.value,
        acceptance_criteria=["locator recorded", "quote checked"],
        expected_outputs=["source-record.json"])
    values.update(updates)
    return WorkItem(**values)

class ResearchTeamTests(unittest.TestCase):
    def test_handoff_requires_independent_review(self):
        team = ResearchTeam()
        task = team.create(sample(), Role.ORCHESTRATOR.value)
        team.transition(task.work_id, Status.READY, Role.ORCHESTRATOR.value)
        team.transition(task.work_id, Status.RUNNING, Role.SOURCE_RESEARCHER.value)
        team.submit(task.work_id, Role.SOURCE_RESEARCHER.value,
            [{"kind":"source","reference":"fixture://synthetic/001"}])
        with self.assertRaises(PermissionError):
            team.review(task.work_id, Role.SOURCE_RESEARCHER.value, True, ["self review"])
        team.review(task.work_id, Role.CRITICAL_REVIEWER.value, True, ["evidence checked"])
        self.assertEqual(task.status, Status.COMPLETED.value)

    def test_paid_resource_requires_approval(self):
        team = ResearchTeam()
        task = team.create(sample(requires_paid_resource=True), Role.ORCHESTRATOR.value)
        team.transition(task.work_id, Status.READY, Role.ORCHESTRATOR.value)
        with self.assertRaises(PermissionError):
            team.transition(task.work_id, Status.RUNNING, Role.SOURCE_RESEARCHER.value)

    def test_permissions_and_duplicate_ids(self):
        team = ResearchTeam()
        with self.assertRaises(PermissionError):
            team.create(sample(), Role.SOURCE_RESEARCHER.value)
        team.create(sample(), Role.ORCHESTRATOR.value)
        with self.assertRaises(ValueError):
            team.create(sample(), Role.ORCHESTRATOR.value)

    def test_evidence_required(self):
        team = ResearchTeam()
        task = team.create(sample(), Role.ORCHESTRATOR.value)
        team.transition(task.work_id, Status.READY, Role.ORCHESTRATOR.value)
        team.transition(task.work_id, Status.RUNNING, Role.SOURCE_RESEARCHER.value)
        with self.assertRaises(ValueError):
            team.submit(task.work_id, Role.SOURCE_RESEARCHER.value, [])

    def test_queue_round_trip(self):
        team = ResearchTeam()
        team.create(sample(), Role.ORCHESTRATOR.value)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "queue.json"
            team.save(path)
            loaded = ResearchTeam.load(path)
        self.assertEqual(list(loaded.items), ["audit-001"])

    def test_illegal_transition(self):
        team = ResearchTeam()
        task = team.create(sample(), Role.ORCHESTRATOR.value)
        with self.assertRaises(ValueError):
            team.transition(task.work_id, Status.COMPLETED, Role.ORCHESTRATOR.value)

if __name__ == "__main__":
    unittest.main()
