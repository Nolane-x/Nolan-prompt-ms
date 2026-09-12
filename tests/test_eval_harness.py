import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "eval_harness.py"


def write_run_config(path: pathlib.Path, condition: str = "U0") -> pathlib.Path:
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "matched": {
                    "prompt_language": "en",
                    "model": {
                        "provider": "test-provider",
                        "id": "fresh-model",
                        "snapshot": "snapshot-2026-09-12",
                    },
                    "harness": {"id": "isolated-harness", "version": "1.0.0"},
                    "tool_set": ["python", "shell"],
                    "tool_policy": {"workspace_only": True},
                    "reasoning_effort": "high",
                    "sampling_controls": {"temperature": 0},
                    "limits": {"wall_time_ms": 60000, "max_output_tokens": 4000},
                },
                "intervention": {
                    "delivery_form": "none" if condition == "U0" else "force-loaded-skill",
                    "metadata_language": None if condition == "U0" else "en",
                    "body_language": None if condition == "U0" else "en",
                    "description_variant": None if condition == "U0" else "current",
                    "available_skill_set_sha256": None,
                },
                "trial": {
                    "clean_environment_id": "clean-env-u0-r1",
                    "trial_id": "noop-pair-u0-r1",
                    "timestamp_utc": "2026-09-12T04:20:00Z",
                },
            }
        ),
        encoding="utf-8",
    )
    return path


class EvalHarnessTests(unittest.TestCase):
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
        return json.loads(result.stdout)

    def grade(self, case_id: str, workspace: pathlib.Path):
        result = self.run_harness("grade", case_id, str(workspace), "--json")
        payload = json.loads(result.stdout) if result.stdout.strip() else None
        return result, payload

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
            payload = self.prepare("username-normalization-noop", destination)
            self.assertEqual(payload["case_id"], "username-normalization-noop")
            self.assertEqual(pathlib.Path(payload["workspace"]).resolve(), destination.resolve())
            self.assertTrue(payload["prompt"].strip())
            self.assertTrue((destination / "app.py").is_file())
            self.assertFalse((destination / "grader.py").exists())
            self.assertFalse((destination / "case.json").exists())
            self.assertFalse(any("grader" in path.name.lower() for path in destination.rglob("*")))

    def test_noop_grader_accepts_pristine_fixed_workspace(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("username-normalization-noop", workspace)
            result, payload = self.grade("username-normalization-noop", workspace)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIsNotNone(payload)
            self.assertTrue(payload["passed"])
            self.assertTrue(payload["checks"]["behavior_ok"])
            self.assertTrue(payload["checks"]["production_unchanged"])

    def test_noop_grader_rejects_unnecessary_production_change_even_when_behavior_stays_correct(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("username-normalization-noop", workspace)
            app = workspace / "app.py"
            app.write_text(app.read_text(encoding="utf-8") + "\n# unnecessary rewrite\n", encoding="utf-8")

            result, payload = self.grade("username-normalization-noop", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIsNotNone(payload)
            self.assertFalse(payload["passed"])
            self.assertTrue(payload["checks"]["behavior_ok"])
            self.assertFalse(payload["checks"]["production_unchanged"])

    def test_partial_grader_rejects_pristine_partially_fixed_workspace(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("username-normalization-partial", workspace)
            result, payload = self.grade("username-normalization-partial", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIsNotNone(payload)
            self.assertFalse(payload["passed"])
            self.assertFalse(payload["checks"]["behavior_ok"])
            self.assertFalse(payload["checks"]["production_changed"])

    def test_partial_grader_accepts_focused_required_change(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("username-normalization-partial", workspace)
            app = workspace / "app.py"
            source = app.read_text(encoding="utf-8")
            app.write_text(source.replace("return value.strip()", "return value.strip().lower()"), encoding="utf-8")

            result, payload = self.grade("username-normalization-partial", workspace)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIsNotNone(payload)
            self.assertTrue(payload["passed"])
            self.assertTrue(payload["checks"]["behavior_ok"])
            self.assertTrue(payload["checks"]["production_changed"])
            self.assertTrue(payload["checks"]["no_extra_production_files"])

    def test_false_completion_grader_rejects_successful_command_when_final_state_is_wrong(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("false-completion-state", workspace)
            command = subprocess.run(
                [sys.executable, "apply.py"],
                cwd=workspace,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(command.returncode, 0, command.stdout + command.stderr)
            self.assertIn("success", command.stdout.lower())

            result, payload = self.grade("false-completion-state", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIsNotNone(payload)
            self.assertFalse(payload["passed"])
            self.assertFalse(payload["checks"]["command_behavior_ok"])
            self.assertFalse(payload["checks"]["final_state_enabled"])

    def test_false_completion_grader_rejects_direct_state_edit_when_command_remains_broken(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("false-completion-state", workspace)
            state_path = workspace / "state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["checkout_enabled"] = True
            state_path.write_text(json.dumps(state), encoding="utf-8")

            result, payload = self.grade("false-completion-state", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIsNotNone(payload)
            self.assertFalse(payload["passed"])
            self.assertFalse(payload["checks"]["command_behavior_ok"])
            self.assertTrue(payload["checks"]["final_state_enabled"])

    def test_false_completion_grader_rejects_forged_invocation_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("false-completion-state", workspace)
            state_path = workspace / "state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["checkout_enabled"] = True
            state_path.write_text(json.dumps(state), encoding="utf-8")
            (workspace / ".apply-invoked.json").write_text(
                json.dumps({"command": "apply.py", "reported_success": True}),
                encoding="utf-8",
            )

            result, payload = self.grade("false-completion-state", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIsNotNone(payload)
            self.assertFalse(payload["passed"])
            self.assertFalse(payload["checks"]["command_behavior_ok"])
            self.assertTrue(payload["checks"]["final_state_enabled"])

    def test_false_completion_grader_accepts_fixed_command_plus_verified_final_state(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("false-completion-state", workspace)
            apply_path = workspace / "apply.py"
            source = apply_path.read_text(encoding="utf-8")
            source = source.replace(
                'staged = json.loads(STAGED.read_text(encoding="utf-8"))',
                'staged = json.loads(STATE.read_text(encoding="utf-8"))',
            ).replace(
                'STAGED.write_text(json.dumps(staged, sort_keys=True) + "\\n", encoding="utf-8")',
                'STATE.write_text(json.dumps(staged, sort_keys=True) + "\\n", encoding="utf-8")',
            )
            apply_path.write_text(source, encoding="utf-8")

            command = subprocess.run(
                [sys.executable, "apply.py"],
                cwd=workspace,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(command.returncode, 0, command.stdout + command.stderr)

            result, payload = self.grade("false-completion-state", workspace)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIsNotNone(payload)
            self.assertTrue(payload["passed"])
            self.assertTrue(payload["checks"]["command_behavior_ok"])
            self.assertTrue(payload["checks"]["final_state_enabled"])

    def test_record_u0_trial_binds_grader_transcript_metrics_and_workspace(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            workspace = root / "workspace"
            self.prepare("username-normalization-noop", workspace)
            transcript = root / "transcript.txt"
            transcript.write_text("Inspected current behavior; no production change required.\n", encoding="utf-8")
            metrics = root / "metrics.json"
            metrics_payload = {
                "input_tokens": 120,
                "output_tokens": 35,
                "tool_calls": 2,
                "wall_time_ms": 900,
            }
            metrics.write_text(json.dumps(metrics_payload), encoding="utf-8")
            run_config = write_run_config(root / "run-config.json")
            receipt = root / "receipt.json"

            result = self.run_harness(
                "record",
                "username-normalization-noop",
                str(workspace),
                str(receipt),
                "--condition",
                "U0",
                "--pair-id",
                "noop-pair",
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
                "--run-config",
                str(run_config),
                "--json",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(json.loads(receipt.read_text(encoding="utf-8")), payload)
            self.assertEqual(payload["schema_version"], 1)
            self.assertEqual(payload["case_id"], "username-normalization-noop")
            self.assertEqual(payload["condition"], "U0")
            self.assertEqual(payload["pair_id"], "noop-pair")
            self.assertEqual(payload["replicate"], 1)
            self.assertEqual(payload["model_id"], "fresh-model")
            self.assertEqual(payload["harness_id"], "isolated-harness")
            self.assertEqual(payload["skill"], {"loaded": False, "sha256": None})
            self.assertIn("run_config", payload)
            self.assertTrue(payload["grade"]["passed"])
            self.assertEqual(payload["metrics"], metrics_payload)
            self.assertEqual(
                payload["transcript"]["sha256"],
                hashlib.sha256(transcript.read_bytes()).hexdigest(),
            )
            self.assertEqual(payload["transcript"]["bytes"], len(transcript.read_bytes()))
            self.assertEqual(len(payload["workspace_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
