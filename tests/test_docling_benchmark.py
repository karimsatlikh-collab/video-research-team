import unittest
from scripts.benchmark_docling_adapter import score_artifact


class DoclingBenchmarkScoringTests(unittest.TestCase):
    def test_critical_tokens_and_locators_are_scored_separately(self):
        artifact = {
            "markdown": "حد ضرر ۴۵ پوینت است؛ نیست.",
            "structured_document": {"prov": [{"page_no": 2}], "text": "1.25 ATR"},
        }
        score = score_artifact(
            artifact, ["۴۵", "نیست", "۱۰۰"], ['"page_no": 2', '"page_no": 3']
        )
        self.assertEqual(score["critical_token_hits"], 2)
        self.assertAlmostEqual(score["critical_token_recall"], 2 / 3)
        self.assertEqual(score["locator_hits"], 1)
        self.assertAlmostEqual(score["locator_recall"], 0.5)


if __name__ == "__main__":
    unittest.main()
