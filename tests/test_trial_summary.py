import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "eval_harness.py"


class TrialSummaryTests(unittest.TestCase):
    def run_harness(self, *args: str):
        return subprocess.run(
            [sys.executable, str(HARNESS), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def prepare(self, case_id: str, workspace: pathlib.Path):
        result = self.run_harness("prepare", case_id, str(workspace), "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def record(
        self,
        case_id: str,
        workspace: pathlib.Path,
        receipt: pathlib.Path,
        condition: str,
        transcript: pathlib.Path,
        metrics: pathlib.Path,
        *,
        pair_id: str = "pair-a",
        replicate: int = 1,
        model_id: str = "fresh-model",
        harness_id: str = "isolated-harness",
    ):
        result = self.run_harness(
            "record",
            case_id,
            str(workspace),
            str(receipt),
            "--condition",
            condition,
            "--pair-id",
            pair_id,
            "--replicate",
            str(replicate),
            "--model-id",
            model_id,
            "--harness-id",
            harness_id,
            "--transcript",
            str(transcript),
            "--metrics",
            str(metrics),
            "--json",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def make_common_inputs(self, root: pathlib.Path):
        transcript = root / "transcript.txt"
        transcript.write_text("fresh isolated trial\n", encoding="utf-8")
        metrics = root / "metrics.json"
        metrics.write_text(
            json.dumps(
                {
                    "input_tokens": 100,
                    "output_tokens": 20,
                    "tool_calls": 2,
                    "wall_time_ms": 500,
                }
            ),
            encoding="utf-8",
        )
        return transcript, metrics

    def make_paired_receipts(self, root: pathlib.Path):
        transcript, metrics = self.make_common_inputs(root)
        u0_workspace = root / "u0-workspace"
        self.prepare("username-normalization-noop", u0_workspace)
        u0_receipt = root / "u0.json"
        self.record(
            "username-normalization-noop",
            u0_workspace,
            u0_receipt,
            "U0",
            transcript,
            metrics,
        )

        u1_workspace = root / "u1-workspace"
        self.prepare("username-normalization-noop", u1_workspace)
        app = u1_workspace / "app.py"
        app.write_text(app.read_text(encoding="utf-8") + "\n# unnecessary change\n", encoding="utf-8")
        u1_receipt = root / "u1.json"
        self.record(
            "username-normalization-noop",
            u1_workspace,
            u1_receipt,
            "U1",
            transcript,
            metrics,
        )
        return u0_receipt, u1_receipt

    def test_summarize_preserves_pairing_and_classifies_u1_harm(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            u0_receipt, u1_receipt = self.make_paired_receipts(root)

            result = self.run_harness(
                "summarize",
                str(u0_receipt),
                str(u1_receipt),
                "--json",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["schema_version"], 1)
            self.assertEqual(len(payload["pairs"]), 1)
            pair = payload["pairs"][0]
            self.assertEqual(pair["case_id"], "username-normalization-noop")
            self.assertEqual(pair["pair_id"], "pair-a")
            self.assertTrue(pair["comparable"])
            self.assertEqual(pair["issues"], [])
            self.assertEqual(
                pair["counts"],
                {
                    "same_fail": 0,
                    "same_pass": 0,
                    "u1_gain": 0,
                    "u1_harm": 1,
                },
            )
            self.assertEqual(pair["replicates"][0]["replicate"], 1)
            self.assertEqual(pair["replicates"][0]["effect"], "u1_harm")
            self.assertTrue(pair["replicates"][0]["conditions"]["U0"]["passed"])
            self.assertFalse(pair["replicates"][0]["conditions"]["U1"]["passed"])
            self.assertEqual(
                pair["replicates"][0]["conditions"]["U0"]["metrics"],
                {
                    "input_tokens": 100,
                    "output_tokens": 20,
                    "tool_calls": 2,
                    "wall_time_ms": 500,
                },
            )

    def test_summarize_marks_mismatched_configs_not_comparable(self):
        mutations = {
            "model_id": lambda payload: payload.__setitem__("model_id", "different-model"),
            "harness_id": lambda payload: payload.__setitem__("harness_id", "different-harness"),
            "eval_provenance": lambda payload: payload["eval_provenance"].__setitem__(
                "grader_sha256", "0" * 64
            ),
        }
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            u0_receipt, u1_receipt = self.make_paired_receipts(root)
            original_u1 = json.loads(u1_receipt.read_text(encoding="utf-8"))

            for field, mutate in mutations.items():
                with self.subTest(field=field):
                    changed = json.loads(json.dumps(original_u1))
                    mutate(changed)
                    u1_receipt.write_text(json.dumps(changed), encoding="utf-8")
                    result = self.run_harness(
                        "summarize",
                        str(u0_receipt),
                        str(u1_receipt),
                        "--json",
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    pair = json.loads(result.stdout)["pairs"][0]
                    self.assertFalse(pair["comparable"])
                    self.assertTrue(any(field in issue for issue in pair["issues"]))
                    self.assertEqual(
                        pair["counts"],
                        {
                            "same_fail": 0,
                            "same_pass": 0,
                            "u1_gain": 0,
                            "u1_harm": 0,
                        },
                    )
                    self.assertEqual(pair["replicates"][0]["effect"], "not_comparable")


if __name__ == "__main__":
    unittest.main()
