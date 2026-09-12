import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "eval_harness.py"
SKILL = ROOT / "verified-delta" / "SKILL.md"


class TrialReceiptTests(unittest.TestCase):
    def run_harness(self, *args: str):
        return subprocess.run(
            [sys.executable, str(HARNESS), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def prepare(self, case_id: str, destination: pathlib.Path):
        result = self.run_harness("prepare", case_id, str(destination), "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def record_args(
        self,
        case_id: str,
        workspace: pathlib.Path,
        receipt: pathlib.Path,
        transcript: pathlib.Path,
        metrics: pathlib.Path,
        condition: str = "U0",
        replicate: int = 1,
    ) -> tuple[str, ...]:
        return (
            "record",
            case_id,
            str(workspace),
            str(receipt),
            "--condition",
            condition,
            "--pair-id",
            "pair-a",
            "--replicate",
            str(replicate),
            "--model-id",
            "fresh-model",
            "--harness-id",
            "isolated-harness",
            "--transcript",
            str(transcript),
            "--metrics",
            str(metrics),
            "--json",
        )

    def test_record_u1_trial_binds_exact_runtime_skill_digest(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            workspace = root / "workspace"
            self.prepare("username-normalization-noop", workspace)
            transcript = root / "transcript.txt"
            transcript.write_text("Checked the current state before acting.\n", encoding="utf-8")
            metrics = root / "metrics.json"
            metrics.write_text(
                json.dumps(
                    {
                        "input_tokens": 580,
                        "output_tokens": 40,
                        "tool_calls": 2,
                        "wall_time_ms": 980,
                    }
                ),
                encoding="utf-8",
            )
            receipt = root / "receipt.json"

            result = self.run_harness(
                *self.record_args(
                    "username-normalization-noop",
                    workspace,
                    receipt,
                    transcript,
                    metrics,
                    condition="U1",
                )
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["condition"], "U1")
            self.assertEqual(
                payload["skill"],
                {
                    "loaded": True,
                    "sha256": hashlib.sha256(SKILL.read_bytes()).hexdigest(),
                },
            )
            self.assertTrue(payload["grade"]["passed"])

    def test_record_refuses_to_overwrite_existing_trial_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            workspace = root / "workspace"
            self.prepare("username-normalization-noop", workspace)
            transcript = root / "transcript.txt"
            transcript.write_text("first run\n", encoding="utf-8")
            metrics = root / "metrics.json"
            metrics.write_text(
                json.dumps(
                    {
                        "input_tokens": 100,
                        "output_tokens": 20,
                        "tool_calls": 1,
                        "wall_time_ms": 500,
                    }
                ),
                encoding="utf-8",
            )
            receipt = root / "receipt.json"

            first = self.run_harness(
                *self.record_args(
                    "username-normalization-noop",
                    workspace,
                    receipt,
                    transcript,
                    metrics,
                    replicate=1,
                )
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            original = receipt.read_bytes()

            transcript.write_text("second run must not replace the first\n", encoding="utf-8")
            second = self.run_harness(
                *self.record_args(
                    "username-normalization-noop",
                    workspace,
                    receipt,
                    transcript,
                    metrics,
                    replicate=2,
                )
            )
            self.assertEqual(second.returncode, 2, second.stdout + second.stderr)
            self.assertIn("already exists", second.stderr.lower())
            self.assertEqual(receipt.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
