import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "eval_harness.py"


class RunnerBoundaryTests(unittest.TestCase):
    def run_harness(self, *args: str):
        return subprocess.run(
            [sys.executable, str(HARNESS), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_prepare_json_exposes_only_agent_run_inputs(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            result = self.run_harness(
                "prepare",
                "username-normalization-noop",
                str(workspace),
                "--json",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(set(payload), {"case_id", "workspace", "prompt"})
            self.assertNotIn("expected_output", payload)
            self.assertTrue(payload["prompt"].strip())


if __name__ == "__main__":
    unittest.main()
