import unittest
from scripts.benchmark_research_team import run_benchmark

class ResearchTeamBenchmarkTests(unittest.TestCase):
    def test_benchmark_runs_and_reports_limitations(self):
        result = run_benchmark(3)
        self.assertEqual(result["completed_items"], 3)
        self.assertGreaterEqual(result["median_item_lifecycle_ms"], 0)
        self.assertIn("no manual baseline", result["note"])

    def test_benchmark_bounds_iterations(self):
        with self.assertRaises(ValueError):
            run_benchmark(0)

if __name__ == "__main__":
    unittest.main()
