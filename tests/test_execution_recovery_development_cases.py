import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "eval_harness.py"
WORKFLOW = ROOT / ".github" / "workflows" / "behavioral-u0-u1.yml"

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

    def test_manifest_and_manual_runner_expose_all_fresh_cases(self):
        result = self.run_harness("list", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        ids = [case["id"] for case in json.loads(result.stdout)["cases"]]
        for case_id in FRESH_CASES:
            self.assertIn(case_id, ids)

        workflow = WORKFLOW.read_text(encoding="utf-8")
        for case_id in FRESH_CASES:
            self.assertIn(f"- {case_id}", workflow)

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
