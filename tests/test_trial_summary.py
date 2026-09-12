import hashlib
import json
import pathlib
import shutil
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


def refresh_run_config_hashes(payload: dict) -> None:
    payload["run_config"]["matched_sha256"] = canonical_sha256(
        payload["run_config"]["value"]["matched"]
    )
    payload["run_config"]["sha256"] = canonical_sha256(payload["run_config"]["value"])


def make_run_config(condition: str, model_id: str, harness_id: str, replicate: int) -> dict:
    return {
        "schema_version": 1,
        "matched": {
            "prompt_language": "en",
            "model": {
                "provider": "test-provider",
                "id": model_id,
                "snapshot": "snapshot-2026-09-12",
            },
            "harness": {
                "id": harness_id,
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
        "intervention": {
            "delivery_form": "none" if condition == "U0" else "force-loaded-skill",
            "metadata_language": None if condition == "U0" else "en",
            "body_language": None if condition == "U0" else "en",
            "description_variant": None if condition == "U0" else "current",
            "available_skill_set_sha256": None,
        },
        "trial": {
            "clean_environment_id": f"clean-{condition.lower()}-{replicate}",
            "trial_id": f"pair-a-{condition.lower()}-{replicate}",
            "timestamp_utc": "2026-09-12T04:20:00Z",
        },
    }


def mutate_model_id(payload: dict) -> None:
    payload["model_id"] = "different-model"
    payload["run_config"]["value"]["matched"]["model"]["id"] = "different-model"
    refresh_run_config_hashes(payload)


def mutate_harness_id(payload: dict) -> None:
    payload["harness_id"] = "different-harness"
    payload["run_config"]["value"]["matched"]["harness"]["id"] = "different-harness"
    refresh_run_config_hashes(payload)


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
        run_config = receipt.with_suffix(".run-config.json")
        run_config.write_text(
            json.dumps(make_run_config(condition, model_id, harness_id, replicate)),
            encoding="utf-8",
        )
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
            "--run-config",
            str(run_config),
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
            "model_id": mutate_model_id,
            "harness_id": mutate_harness_id,
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

    def test_summarize_marks_matched_run_context_mismatch_not_comparable(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            u0_receipt, u1_receipt = self.make_paired_receipts(root)
            changed = json.loads(u1_receipt.read_text(encoding="utf-8"))
            changed["run_config"]["value"]["matched"]["limits"]["max_output_tokens"] = 8000
            refresh_run_config_hashes(changed)
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
            self.assertTrue(any("matched run config" in issue for issue in pair["issues"]))
            self.assertEqual(pair["replicates"][0]["effect"], "not_comparable")

    def test_summarize_rejects_tampered_run_config_hashes(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            u0_receipt, u1_receipt = self.make_paired_receipts(root)
            changed = json.loads(u1_receipt.read_text(encoding="utf-8"))
            changed["run_config"]["value"]["matched"]["limits"]["max_output_tokens"] = 9000
            u1_receipt.write_text(json.dumps(changed), encoding="utf-8")

            result = self.run_harness(
                "summarize",
                str(u0_receipt),
                str(u1_receipt),
                "--json",
            )
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("run config", result.stderr.lower())

    def test_summarize_rejects_duplicate_condition_replicate_without_last_file_wins(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            u0_receipt, u1_receipt = self.make_paired_receipts(root)
            duplicate_u0 = root / "u0-duplicate.json"
            shutil.copyfile(u0_receipt, duplicate_u0)
            duplicate_payload = json.loads(duplicate_u0.read_text(encoding="utf-8"))
            duplicate_payload["grade"]["passed"] = False
            duplicate_u0.write_text(json.dumps(duplicate_payload), encoding="utf-8")

            result = self.run_harness(
                "summarize",
                str(u0_receipt),
                str(duplicate_u0),
                str(u1_receipt),
                "--json",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            pair = json.loads(result.stdout)["pairs"][0]
            self.assertFalse(pair["comparable"])
            self.assertTrue(any("duplicate U0" in issue for issue in pair["issues"]))
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
