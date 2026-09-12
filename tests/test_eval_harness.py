import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "eval_harness.py"


class EvalHarnessTests(unittest.TestCase):
    def run_harness(self, *args: str):
        return subprocess.run(
            [sys.executable, str(HARNESS), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_list_exposes_exact_preregistered_utility_cases(self):
        result = self.run_harness("list", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(
            [case["id"] for case in payload["cases"]],
            [
                "username-normalization-noop",
                "username-normalization-partial",
                "false-completion-state",
            ],
        )
        for case in payload["cases"]:
            self.assertTrue(case["prompt"].strip())
            self.assertTrue(case["expected_output"].strip())

    def test_prepare_copies_only_agent_visible_fixture(self):
        with tempfile.TemporaryDirectory() as td:
            destination = pathlib.Path(td) / "workspace"
            result = self.run_harness(
                "prepare",
                "username-normalization-noop",
                str(destination),
                "--json",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["case_id"], "username-normalization-noop")
            self.assertEqual(pathlib.Path(payload["workspace"]).resolve(), destination.resolve())
            self.assertTrue(payload["prompt"].strip())
            self.assertTrue((destination / "app.py").is_file())
            self.assertFalse((destination / "grader.py").exists())
            self.assertFalse((destination / "case.json").exists())
            self.assertFalse(any("grader" in path.name.lower() for path in destination.rglob("*")))


if __name__ == "__main__":
    unittest.main()
