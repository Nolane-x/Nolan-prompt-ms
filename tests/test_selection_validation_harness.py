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

    def generate(self, root: pathlib.Path, seed: str = "fixed-seed-42"):
        bundle = root / "bundle"
        result = self.run_harness("generate", "--seed", seed, "--output", bundle, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        return bundle, json.loads(result.stdout)

    def test_execution_harness_exists(self):
        self.assertTrue(HARNESS.is_file(), "selection_validation.py must exist")

    def test_seeded_generation_matches_frozen_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle, payload = self.generate(pathlib.Path(tmp))
            manifest = json.loads((bundle / "bundle.json").read_text(encoding="utf-8"))
            plan = json.loads(PLAN.read_text(encoding="utf-8"))
            expected_cells = {cell["id"] for cell in plan["semantic_cells"]}
            cells = [case["cell_id"] for case in manifest["cases"]]
            self.assertEqual(payload["case_count"], 12)
            self.assertEqual(set(cells), expected_cells)
            self.assertTrue(all(cells.count(cell) == 2 for cell in expected_cells))
            self.assertGreaterEqual(len({case["family"] for case in manifest["cases"]}), 4)
            self.assertEqual(len(payload["matrix"]["include"]), 24)

    def test_generation_is_deterministic_and_immutable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            first, _ = self.generate(root / "first", "same-seed")
            second, _ = self.generate(root / "second", "same-seed")
            self.assertEqual(
                json.loads((first / "bundle.json").read_text(encoding="utf-8")),
                json.loads((second / "bundle.json").read_text(encoding="utf-8")),
            )
            duplicate = self.run_harness(
                "generate", "--seed", "same-seed", "--output", first, "--json"
            )
            self.assertNotEqual(duplicate.returncode, 0)
            self.assertIn("already exists", duplicate.stderr)

    def test_prepare_exposes_only_prompt_and_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            bundle, _ = self.generate(root)
            manifest = json.loads((bundle / "bundle.json").read_text(encoding="utf-8"))
            case = manifest["cases"][0]
            case_root = bundle / "cases" / case["id"]
            self.assertTrue((case_root / "visible" / "prompt.txt").is_file())
            self.assertTrue((case_root / "visible" / "fixture").is_dir())
            self.assertTrue((case_root / "hidden" / "grader.json").is_file())
            self.assertTrue((case_root / "hidden" / "reference.json").is_file())

            workspace = root / "workspace"
            result = self.run_harness("prepare", bundle, case["id"], workspace, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            prepared = json.loads(result.stdout)
            self.assertEqual(prepared["case_id"], case["id"])
            self.assertTrue(prepared["prompt"].strip())
            self.assertTrue(workspace.is_dir())
            self.assertFalse(any(path.name in {"grader.json", "reference.json"} for path in workspace.rglob("*")))
            self.assertFalse(any("hidden" in path.parts for path in workspace.rglob("*")))

    def test_reference_admission_passes_every_generated_case(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            bundle, _ = self.generate(root)
            result = self.run_harness("admit", bundle, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["passed"])
            self.assertEqual(payload["admitted_cases"], 12)


if __name__ == "__main__":
    unittest.main()
