import copy
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "eval_harness.py"


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def make_run_config(condition: str = "U0") -> dict:
    intervention = {
        "delivery_form": "none" if condition == "U0" else "force-loaded-skill",
        "metadata_language": None if condition == "U0" else "en",
        "body_language": None if condition == "U0" else "en",
        "description_variant": None if condition == "U0" else "current",
        "available_skill_set_sha256": None,
    }
    return {
        "schema_version": 1,
        "matched": {
            "prompt_language": "en",
            "model": {
                "provider": "test-provider",
                "id": "fresh-model",
                "snapshot": "snapshot-2026-09-12",
            },
            "harness": {
                "id": "isolated-harness",
                "version": "1.0.0",
            },
            "tool_set": ["python", "shell"],
            "tool_policy": {"workspace_only": True},
            "reasoning_effort": "high",
            "sampling_controls": {"temperature": 0},
            "limits": {
                "wall_time_ms": 60000,
                "max_output_tokens": 4000,
            },
        },
        "intervention": intervention,
        "trial": {
            "clean_environment_id": "clean-env-u0-r1",
            "trial_id": "pair-a-u0-r1",
            "timestamp_utc": "2026-09-12T04:20:00Z",
        },
    }


class RunConfigTests(unittest.TestCase):
    def run_harness(self, *args: str):
        return subprocess.run(
            [sys.executable, str(HARNESS), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def make_trial_inputs(self, root: pathlib.Path):
        workspace = root / "workspace"
        prepared = self.run_harness(
            "prepare",
            "username-normalization-noop",
            str(workspace),
            "--json",
        )
        self.assertEqual(prepared.returncode, 0, prepared.stdout + prepared.stderr)
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
        return workspace, transcript, metrics

    def record_with_config(
        self,
        workspace: pathlib.Path,
        receipt: pathlib.Path,
        transcript: pathlib.Path,
        metrics: pathlib.Path,
        run_config: pathlib.Path,
        *,
        condition: str = "U0",
        model_id: str = "fresh-model",
        harness_id: str = "isolated-harness",
    ):
        return self.run_harness(
            "record",
            "username-normalization-noop",
            str(workspace),
            str(receipt),
            "--condition",
            condition,
            "--pair-id",
            "pair-a",
            "--replicate",
            "1",
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

    def test_record_binds_canonical_run_config_and_matched_context_hash(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            workspace, transcript, metrics = self.make_trial_inputs(root)
            config_payload = make_run_config("U0")
            run_config = root / "run-config.json"
            run_config.write_text(json.dumps(config_payload, indent=2), encoding="utf-8")
            receipt = root / "receipt.json"

            result = self.record_with_config(
                workspace,
                receipt,
                transcript,
                metrics,
                run_config,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["run_config"]["value"], config_payload)
            self.assertEqual(payload["run_config"]["sha256"], canonical_sha256(config_payload))
            self.assertEqual(
                payload["run_config"]["matched_sha256"],
                canonical_sha256(config_payload["matched"]),
            )

    def test_record_rejects_invalid_run_config_without_writing_receipt(self):
        invalid_configs = []

        wrong_schema = make_run_config()
        wrong_schema["schema_version"] = 2
        invalid_configs.append(("schema_version", wrong_schema))

        missing_prompt_language = make_run_config()
        del missing_prompt_language["matched"]["prompt_language"]
        invalid_configs.append(("prompt_language", missing_prompt_language))

        empty_model_id = make_run_config()
        empty_model_id["matched"]["model"]["id"] = "   "
        invalid_configs.append(("model", empty_model_id))

        duplicate_tools = make_run_config()
        duplicate_tools["matched"]["tool_set"] = ["shell", "shell"]
        invalid_configs.append(("tool_set", duplicate_tools))

        naive_timestamp = make_run_config()
        naive_timestamp["trial"]["timestamp_utc"] = "2026-09-12T04:20:00"
        invalid_configs.append(("timestamp", naive_timestamp))

        invalid_skill_set_hash = make_run_config()
        invalid_skill_set_hash["intervention"]["available_skill_set_sha256"] = "not-a-sha256"
        invalid_configs.append(("sha256", invalid_skill_set_hash))

        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            workspace, transcript, metrics = self.make_trial_inputs(root)
            for index, (label, config_payload) in enumerate(invalid_configs, start=1):
                with self.subTest(label=label):
                    run_config = root / f"run-config-{index}.json"
                    run_config.write_text(json.dumps(config_payload), encoding="utf-8")
                    receipt = root / f"receipt-{index}.json"
                    result = self.record_with_config(
                        workspace,
                        receipt,
                        transcript,
                        metrics,
                        run_config,
                    )
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertIn("run config", result.stderr.lower())
                    self.assertFalse(receipt.exists())

    def test_record_rejects_run_config_identity_or_intervention_mismatch(self):
        cases = []

        model_mismatch = make_run_config("U0")
        model_mismatch["matched"]["model"]["id"] = "different-model"
        cases.append(("model", model_mismatch, "U0"))

        harness_mismatch = make_run_config("U0")
        harness_mismatch["matched"]["harness"]["id"] = "different-harness"
        cases.append(("harness", harness_mismatch, "U0"))

        u0_with_skill = make_run_config("U1")
        cases.append(("u0-intervention", u0_with_skill, "U0"))

        u1_without_skill = make_run_config("U0")
        cases.append(("u1-intervention", u1_without_skill, "U1"))

        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            workspace, transcript, metrics = self.make_trial_inputs(root)
            for index, (label, config_payload, condition) in enumerate(cases, start=1):
                with self.subTest(label=label):
                    run_config = root / f"mismatch-{index}.json"
                    run_config.write_text(json.dumps(config_payload), encoding="utf-8")
                    receipt = root / f"mismatch-receipt-{index}.json"
                    result = self.record_with_config(
                        workspace,
                        receipt,
                        transcript,
                        metrics,
                        run_config,
                        condition=condition,
                    )
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                    self.assertIn("run config", result.stderr.lower())
                    self.assertFalse(receipt.exists())


if __name__ == "__main__":
    unittest.main()