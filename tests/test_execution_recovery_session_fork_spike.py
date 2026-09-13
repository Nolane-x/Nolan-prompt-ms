import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "execution-recovery-session-fork-spike.yml"


class ExecutionRecoverySessionForkSpikeTests(unittest.TestCase):
    def test_spike_forks_local_session_before_treatment_and_attests_all_arms(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for needle in [
            'COPILOT_HOME="$SEED_HOME"',
            '"remoteExport": false',
            'session-state/$SESSION_ID',
            'cp -a "$SEED_HOME/." "$U0_HOME/"',
            'cp -a "$SEED_HOME/." "$U1_HOME/"',
            '--resume="$SESSION_ID"',
            'cat verified-delta/SKILL.md',
            'seed-attestation.json',
            'u0-attestation.json',
            'u1-attestation.json',
            'verdict.json',
        ]:
            self.assertIn(needle, workflow)
        self.assertNotIn('--model="$SELECTED_MODEL"', workflow)
        self.assertNotIn("execution_recovery_development.py prepare", workflow)

    def test_spike_requires_identity_and_isolation_checks_before_pass(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for needle in [
            'seed["model"] == u0["model"] == u1["model"]',
            'seed["reasoning_effort"] == u0["reasoning_effort"] == u1["reasoning_effort"]',
            'seed["tool_set"] == u0["tool_set"] == u1["tool_set"]',
            'pre_u0 == pre_u1 == pre_seed',
            'post_u0 != pre_u0',
            'post_u1 != pre_u1',
            'post_u0 != post_u1',
            '"passed": passed',
        ]:
            self.assertIn(needle, workflow)


if __name__ == "__main__":
    unittest.main()
