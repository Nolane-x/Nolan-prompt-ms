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

    def test_behavioral_trials_require_pre_treatment_session_fork(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("\n  seed:\n", workflow)
        self.assertIn("needs: [validate, resolve]", workflow)
        self.assertIn("seed-attestation.json", workflow)
        self.assertIn("seed-state-hash.txt", workflow)
        self.assertIn("session-id.txt", workflow)
        self.assertIn("execution-recovery-seed-${{ github.run_id }}", workflow)
        self.assertIn("needs: [validate, resolve, seed]", workflow)
        self.assertIn("actions/download-artifact@v4", workflow)
        self.assertIn('SEED_ARCHIVE="$SEED_ROOT/frozen-seed-home.tar"', workflow)
        self.assertIn('tar -xf "$SEED_ARCHIVE" -C "$COPILOT_HOME"', workflow)
        self.assertIn('--resume="$SESSION_ID"', workflow)
        self.assertNotIn('--model="$EXECUTION_MODEL_ID"', workflow)
        self.assertNotIn('--reasoning-effort="$EXECUTION_REASONING_EFFORT"', workflow)

        seed_index = workflow.index("\n  seed:\n")
        trial_index = workflow.index("\n  trial:\n")
        prepare_index = workflow.index("execution_recovery_development.py prepare")
        self.assertLess(seed_index, trial_index)
        self.assertGreater(prepare_index, trial_index)
        self.assertNotIn(
            "execution_recovery_development.py prepare",
            workflow[seed_index:trial_index],
        )

    def test_session_fork_fails_closed_and_binds_common_fork(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for needle in [
            '"remoteExport": false',
            'PRE_TREATMENT_STATE_SHA256',
            'seed["model"] != attestation["model"]',
            'seed["reasoning_effort"] != attestation["reasoning_effort"]',
            'seed["tool_set"] != attestation["tool_set"]',
            '"session_fork": {',
            '"session_id": session_id',
            '"pre_treatment_state_sha256": pre_treatment_state_sha256',
        ]:
            self.assertIn(needle, workflow)
        self.assertIn("session fork runtime mismatch", workflow)
        self.assertIn("session fork state hash mismatch", workflow)
        self.assertIn("if: always()", workflow)

    def test_seed_hash_is_bound_to_lossless_transport_archive(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        seed_index = workflow.index("\n  seed:\n")
        trial_index = workflow.index("\n  trial:\n")
        seed_block = workflow[seed_index:trial_index]
        trial_block = workflow[trial_index:]

        self.assertIn('FROZEN_HOME="$ROOT/frozen-seed-home"', seed_block)
        self.assertIn('cp -a "$SEED_HOME/." "$FROZEN_HOME/"', seed_block)
        self.assertIn('ARCHIVE="$ROOT/frozen-seed-home.tar"', seed_block)
        self.assertIn(
            'tar --exclude="./session-state/$SESSION_ID/inuse.*.lock"',
            seed_block,
        )
        self.assertIn('-C "$FROZEN_HOME" -cf "$ARCHIVE" .', seed_block)
        self.assertIn('seed-archive-hash.txt', seed_block)
        self.assertIn('VERIFY_HOME="$ROOT/archive-verification-home"', seed_block)
        self.assertIn(
            'python - "$VERIFIED_SESSION_DIR" "$ROOT/seed-state-hash.txt"',
            seed_block,
        )
        self.assertIn(
            '${{ runner.temp }}/execution-recovery-seed/frozen-seed-home.tar',
            seed_block,
        )
        self.assertIn('include-hidden-files: false', seed_block)

        self.assertIn('SEED_ARCHIVE="$SEED_ROOT/frozen-seed-home.tar"', trial_block)
        self.assertIn('session fork archive hash mismatch', trial_block)
        self.assertIn('tar -xf "$SEED_ARCHIVE" -C "$COPILOT_HOME"', trial_block)
        self.assertIn('copilot-local-session-resume-v2-tar', trial_block)
        self.assertIn(
            '"transport_archive_sha256": transport_archive_sha256',
            trial_block,
        )
        self.assertNotIn('SEED_SOURCE="$SEED_ROOT/frozen-seed-home"', trial_block)

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
