import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "selection_validation.py"
PLAN = ROOT / "evals" / "target-authority-selection-plan.json"


class SelectionValidationHarnessTests(unittest.TestCase):
    def run_harness(self, *args):
        return subprocess.run(
            [sys.executable, str(HARNESS), *map(str, args)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def test_execution_harness_exists(self):
        self.assertTrue(HARNESS.is_file(), "selection_validation.py must exist")

    def test_seeded_generation_matches_frozen_plan(self):
        if not HARNESS.is_file():
            self.skipTest("execution harness not implemented")
        with tempfile.TemporaryDirectory() as tmp:
            bundle = pathlib.Path(tmp) / "bundle"
            result = self.run_harness(
                "generate", "--seed", "fixed-seed-42", "--output", bundle, "--json"
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            manifest = json.loads((bundle / "bundle.json").read_text(encoding="utf-8"))
            plan = json.loads(PLAN.read_text(encoding="utf-8"))
            expected_cells = {cell["id"] for cell in plan["semantic_cells"]}
            cells = [case["cell_id"] for case in manifest["cases"]]
            self.assertEqual(payload["case_count"], 12)
            self.assertEqual(set(cells), expected_cells)
            self.assertTrue(all(cells.count(cell) == 2 for cell in expected_cells))
            self.assertGreaterEqual(len({case["family"] for case in manifest["cases"]}), 4)
            self.assertEqual(len(payload["matrix"]["include"]), 24)


if __name__ == "__main__":
    unittest.main()
