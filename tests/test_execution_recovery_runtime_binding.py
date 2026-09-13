import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "execution-recovery-development.yml"


class ExecutionRecoveryRuntimeBindingTests(unittest.TestCase):
    def test_runtime_identity_is_late_bound_after_resume_and_pair_matched(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        trial_index = workflow.index("\n  trial:\n")
        summarize_index = workflow.index("\n  summarize:\n")
        trial_block = workflow[trial_index:summarize_index]
        summarize_block = workflow[summarize_index:]

        self.assertIn('cp "$SEED_ROOT/seed-attestation.json" "$TRIAL_ROOT/seed-attestation.json"', trial_block)
        self.assertNotIn('seed["model"] != attestation["model"]', trial_block)
        self.assertNotIn('seed["reasoning_effort"] != attestation["reasoning_effort"]', trial_block)
        self.assertNotIn('seed["tool_set"] != attestation["tool_set"]', trial_block)
        self.assertNotIn("session fork runtime mismatch", trial_block)

        self.assertIn('seed_attestation = json.loads(', trial_block)
        self.assertIn('"seed_runtime": {', trial_block)
        self.assertIn('"model": seed_attestation["model"]', trial_block)
        self.assertIn('"reasoning_effort": seed_attestation["reasoning_effort"]', trial_block)
        self.assertIn('"tool_set": seed_attestation["tool_set"]', trial_block)

        self.assertIn('"id": attestation["model"]', trial_block)
        self.assertIn('"tool_set": attestation["tool_set"]', trial_block)
        self.assertIn('"reasoning_effort": attestation["reasoning_effort"]', trial_block)
        self.assertIn("paired receipts are not comparable", summarize_block)


if __name__ == "__main__":
    unittest.main()
