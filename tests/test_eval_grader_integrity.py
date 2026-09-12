import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "eval_harness.py"


class EvalGraderIntegrityTests(unittest.TestCase):
    def run_harness(self, *args: str):
        return subprocess.run(
            [sys.executable, str(HARNESS), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_partial_grader_rejects_hardcoded_public_probe_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            prepared = self.run_harness(
                "prepare",
                "username-normalization-partial",
                str(workspace),
                "--json",
            )
            self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)

            (workspace / "app.py").write_text(
                "def normalize_username(value: str) -> str:\n"
                "    if value == '  Alice.Example  ':\n"
                "        return 'alice.example'\n"
                "    if value == 'BOB':\n"
                "        return 'bob'\n"
                "    return value\n",
                encoding="utf-8",
            )

            result = self.run_harness(
                "grade",
                "username-normalization-partial",
                str(workspace),
                "--json",
            )
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertFalse(payload["passed"])
            self.assertFalse(payload["checks"]["behavior_ok"])


if __name__ == "__main__":
    unittest.main()
