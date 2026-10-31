import json
import unittest
from pathlib import Path

class SyntheticFixtureManifestTests(unittest.TestCase):
    def test_fixture_ids_are_unique_and_critical_tokens_are_present(self):
        manifest_path = Path(__file__).parents[1] / "fixtures" / "time_openfx" / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 1)
        self.assertIn("Synthetic examples", manifest["rights_basis"])
        fixtures = manifest["fixtures"]
        ids = [item["fixture_id"] for item in fixtures]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(fixtures), 5)
        for item in fixtures:
            self.assertTrue(item["text"])
            self.assertTrue(item["locator"])
            for token in item["critical_tokens"]:
                self.assertIn(token, item["text"], msg=item["fixture_id"])

if __name__ == "__main__":
    unittest.main()
