import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "execution_recovery_development.py"
WORKFLOW = ROOT / ".github" / "workflows" / "execution-recovery-development.yml"

FRESH_CASES = [
    "execution-recovery-required",
    "execution-recovery-noop",
    "incidental-artifact-cleanup",
    "required-artifact-preserved",
]


class ExecutionRecoveryDevelopmentCasesTests(unittest.TestCase):
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

    def test_fresh_harness_and_manual_runner_are_isolated_from_historical_manifest(self):
        result = self.run_harness("list", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        ids = [case["id"] for case in json.loads(result.stdout)["cases"]]
        self.assertEqual(ids, FRESH_CASES)

        historical = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
        historical_ids = [case["id"] for case in historical["cases"]]
        for case_id in FRESH_CASES:
            self.assertNotIn(case_id, historical_ids)

        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("condition: [U0, U1]", workflow)
        self.assertIn("execution_recovery_development.py", workflow)
        for case_id in FRESH_CASES:
            self.assertIn(f"- {case_id}", workflow)

    def test_behavioral_trials_require_exact_preflight_runtime_lock(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("\n  preflight:\n", workflow)
        self.assertIn("needs: [validate, resolve]", workflow)
        self.assertIn("selected-attestation.json", workflow)
        self.assertIn("locked-attestation.json", workflow)
        self.assertIn("locked_model:", workflow)
        self.assertIn("locked_reasoning_effort:", workflow)
        self.assertIn("locked-tool-set.json", workflow)
        self.assertIn("needs: [validate, resolve, preflight]", workflow)
        self.assertIn('EXECUTION_MODEL_ID: ${{ needs.preflight.outputs.locked_model }}', workflow)
        self.assertIn(
            'EXECUTION_REASONING_EFFORT: ${{ needs.preflight.outputs.locked_reasoning_effort }}',
            workflow,
        )
        self.assertIn('--model="$EXECUTION_MODEL_ID"', workflow)
        self.assertIn('--reasoning-effort="$EXECUTION_REASONING_EFFORT"', workflow)

        preflight_index = workflow.index("\n  preflight:\n")
        trial_index = workflow.index("\n  trial:\n")
        prepare_index = workflow.index("execution_recovery_development.py prepare")
        self.assertLess(preflight_index, trial_index)
        self.assertGreater(prepare_index, trial_index)
        self.assertNotIn(
            "execution_recovery_development.py prepare",
            workflow[preflight_index:trial_index],
        )

    def test_preflight_runtime_lock_fails_closed_and_preserves_evidence(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for needle in [
            'selected["model"] != locked["model"]',
            'selected["reasoning_effort"] != locked["reasoning_effort"]',
            'selected["tool_set"] != locked["tool_set"]',
        ]:
            self.assertIn(needle, workflow)
        self.assertIn("exact runtime lock mismatch", workflow)
        self.assertIn(
            "execution-recovery-model-lock-${{ github.run_id }}",
            workflow,
        )
        self.assertIn("if: always()", workflow)

    def test_recovery_pressure_comes_from_tool_policy_not_prompt_answer_leakage(self):
        result = self.run_harness("list", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        cases = {case["id"]: case for case in json.loads(result.stdout)["cases"]}
        prompt = cases["execution-recovery-required"]["prompt"].lower()
        self.assertIn("./promote.sh", prompt)
        self.assertNotIn("cannot be invoked", prompt)
        self.assertNotIn("permitted path", prompt)

        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("--allow-tool='write,shell(python:*)'", workflow)
        self.assertNotIn("--allow-all", workflow)

    def test_execution_recovery_required_needs_target_change_but_accepts_focused_recovery(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("execution-recovery-required", workspace)
            result, payload = self.grade("execution-recovery-required", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertFalse(payload["passed"])
            self.assertFalse(payload["checks"]["target_reached"])

            rollout = workspace / "rollout.json"
            state = json.loads(rollout.read_text(encoding="utf-8"))
            state["channel"] = "stable"
            rollout.write_text(json.dumps(state, sort_keys=True) + "\n", encoding="utf-8")
            result, payload = self.grade("execution-recovery-required", workspace)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(payload["passed"])
            self.assertTrue(payload["checks"]["target_reached"])
            self.assertTrue(payload["checks"]["no_unrelated_changes"])

    def test_execution_recovery_noop_preserves_already_satisfied_state(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("execution-recovery-noop", workspace)
            result, payload = self.grade("execution-recovery-noop", workspace)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(payload["passed"])
            self.assertTrue(payload["checks"]["production_unchanged"])

            (workspace / "attempt.txt").write_text("unnecessary retry\n", encoding="utf-8")
            result, payload = self.grade("execution-recovery-noop", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertFalse(payload["passed"])
            self.assertFalse(payload["checks"]["production_unchanged"])

    def test_incidental_artifact_cleanup_requires_clean_final_tree_after_target_is_reached(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("incidental-artifact-cleanup", workspace)
            command = subprocess.run([sys.executable, "publish.py"], cwd=workspace, text=True, capture_output=True, check=False)
            self.assertEqual(command.returncode, 0, command.stdout + command.stderr)
            result, payload = self.grade("incidental-artifact-cleanup", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertTrue(payload["checks"]["target_reached"])
            self.assertFalse(payload["checks"]["no_incidental_artifact"])

            (workspace / "staged-release.json").unlink()
            result, payload = self.grade("incidental-artifact-cleanup", workspace)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(payload["passed"])

    def test_required_artifact_control_rejects_over_cleanup(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("required-artifact-preserved", workspace)
            command = subprocess.run([sys.executable, "build.py"], cwd=workspace, text=True, capture_output=True, check=False)
            self.assertEqual(command.returncode, 0, command.stdout + command.stderr)
            result, payload = self.grade("required-artifact-preserved", workspace)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(payload["checks"]["required_manifest_present"])

            (workspace / "manifest.json").unlink()
            result, payload = self.grade("required-artifact-preserved", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertFalse(payload["passed"])
            self.assertFalse(payload["checks"]["required_manifest_present"])


if __name__ == "__main__":
    unittest.main()
