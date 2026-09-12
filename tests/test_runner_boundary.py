import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "eval_harness.py"


def write_run_config(
    path: pathlib.Path,
    *,
    model_id: str = "fresh-model",
    harness_id: str = "isolated-harness",
) -> pathlib.Path:
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "matched": {
                    "prompt_language": "en",
                    "model": {
                        "provider": "test-provider",
                        "id": model_id,
                        "snapshot": "snapshot-2026-09-12",
                    },
                    "harness": {"id": harness_id, "version": "1.0.0"},
                    "tool_set": ["python", "shell"],
                    "tool_policy": {"workspace_only": True},
                    "reasoning_effort": "high",
                    "sampling_controls": {"temperature": 0},
                    "limits": {"wall_time_ms": 60000, "max_output_tokens": 4000},
                },
                "intervention": {
                    "delivery_form": "none",
                    "metadata_language": None,
                    "body_language": None,
                    "description_variant": None,
                    "available_skill_set_sha256": None,
                },
                "trial": {
                    "clean_environment_id": "clean-u0-1",
                    "trial_id": "pair-a-u0-1",
                    "timestamp_utc": "2026-09-12T04:20:00Z",
                },
            }
        ),
        encoding="utf-8",
    )
    return path


class RunnerBoundaryTests(unittest.TestCase):
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
        return json.loads(result.stdout)

    def record_result(
        self,
        workspace: pathlib.Path,
        receipt: pathlib.Path,
        transcript: pathlib.Path,
        metrics: pathlib.Path,
        *,
        pair_id: str = "pair-a",
        replicate: int = 1,
        model_id: str = "fresh-model",
        harness_id: str = "isolated-harness",
    ):
        run_config = write_run_config(
            receipt.with_suffix(".run-config.json"),
            model_id=model_id,
            harness_id=harness_id,
        )
        return self.run_harness(
            "record",
            "username-normalization-noop",
            str(workspace),
            str(receipt),
            "--condition",
            "U0",
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
            "--run-config",
            str(run_config),
            "--json",
        )

    def test_prepare_json_exposes_only_agent_run_inputs(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            payload = self.prepare("username-normalization-noop", workspace)
            self.assertEqual(set(payload), {"case_id", "workspace", "prompt"})
            self.assertNotIn("expected_output", payload)
            self.assertTrue(payload["prompt"].strip())

    def test_record_requires_run_config(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            workspace = root / "workspace"
            self.prepare("username-normalization-noop", workspace)
            transcript = root / "transcript.txt"
            transcript.write_text("fresh isolated trial\n", encoding="utf-8")
            metrics = root / "metrics.json"
            metrics.write_text(
                json.dumps(
                    {
                        "input_tokens": 100,
                        "output_tokens": 10,
                        "tool_calls": 1,
                        "wall_time_ms": 100,
                    }
                ),
                encoding="utf-8",
            )
            receipt = root / "receipt.json"
            result = self.run_harness(
                "record",
                "username-normalization-noop",
                str(workspace),
                str(receipt),
                "--condition",
                "U0",
                "--pair-id",
                "pair-a",
                "--replicate",
                "1",
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
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("run-config", result.stderr.lower())
            self.assertFalse(receipt.exists())

    def test_record_rejects_invalid_metrics_without_writing_receipt(self):
        invalid_metrics = [
            {
                "input_tokens": -1,
                "output_tokens": 10,
                "tool_calls": 1,
                "wall_time_ms": 100,
            },
            {
                "input_tokens": "100",
                "output_tokens": 10,
                "tool_calls": 1,
                "wall_time_ms": 100,
            },
            {
                "input_tokens": 100,
                "output_tokens": 10,
                "tool_calls": 1,
            },
        ]
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            workspace = root / "workspace"
            self.prepare("username-normalization-noop", workspace)
            transcript = root / "transcript.txt"
            transcript.write_text("fresh isolated trial\n", encoding="utf-8")

            for index, metrics_payload in enumerate(invalid_metrics, start=1):
                with self.subTest(metrics=metrics_payload):
                    metrics = root / f"metrics-{index}.json"
                    metrics.write_text(json.dumps(metrics_payload), encoding="utf-8")
                    receipt = root / f"receipt-{index}.json"
                    result = self.record_result(workspace, receipt, transcript, metrics)
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertIn("metrics", result.stderr.lower())
                    self.assertFalse(receipt.exists())

    def test_record_rejects_invalid_trial_identity_without_writing_receipt(self):
        invalid_identity = [
            {"pair_id": "", "replicate": 1, "model_id": "fresh-model", "harness_id": "isolated-harness"},
            {"pair_id": "pair-a", "replicate": 0, "model_id": "fresh-model", "harness_id": "isolated-harness"},
            {"pair_id": "pair-a", "replicate": 1, "model_id": "   ", "harness_id": "isolated-harness"},
            {"pair_id": "pair-a", "replicate": 1, "model_id": "fresh-model", "harness_id": "\t"},
        ]
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            workspace = root / "workspace"
            self.prepare("username-normalization-noop", workspace)
            transcript = root / "transcript.txt"
            transcript.write_text("fresh isolated trial\n", encoding="utf-8")
            metrics = root / "metrics.json"
            metrics.write_text(
                json.dumps(
                    {
                        "input_tokens": 100,
                        "output_tokens": 10,
                        "tool_calls": 1,
                        "wall_time_ms": 100,
                    }
                ),
                encoding="utf-8",
            )

            for index, identity in enumerate(invalid_identity, start=1):
                with self.subTest(identity=identity):
                    receipt = root / f"identity-receipt-{index}.json"
                    result = self.record_result(
                        workspace,
                        receipt,
                        transcript,
                        metrics,
                        **identity,
                    )
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertIn("trial", result.stderr.lower())
                    self.assertFalse(receipt.exists())


if __name__ == "__main__":
    unittest.main()
