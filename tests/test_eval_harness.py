import json
import pathlib
import subprocess
import sys
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


if __name__ == "__main__":
    unittest.main()
