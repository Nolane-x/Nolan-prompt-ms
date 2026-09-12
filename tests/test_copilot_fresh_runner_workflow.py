import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "behavioral-u0-u1.yml"


class CopilotFreshRunnerWorkflowTests(unittest.TestCase):
    def workflow_text(self) -> str:
        self.assertTrue(WORKFLOW.is_file(), "behavioral U0/U1 workflow must exist")
        return WORKFLOW.read_text(encoding="utf-8")

    def test_workflow_is_manual_and_least_privilege(self):
        text = self.workflow_text()
        self.assertIn("workflow_dispatch:", text)
        self.assertNotIn("\n  push:", text)
        self.assertNotIn("\n  pull_request:", text)
        self.assertIn("contents: read", text)
        self.assertIn("copilot-requests: write", text)

    def test_trials_are_fresh_bounded_and_failure_preserving(self):
        text = self.workflow_text()
        self.assertIn("condition: [U0, U1]", text)
        self.assertIn("$RUNNER_TEMP", text)
        self.assertIn("COPILOT_HOME", text)
        self.assertIn("--disable-builtin-mcps", text)
        self.assertIn("--no-ask-user", text)
        self.assertIn("--available-tools", text)
        self.assertNotIn("--allow-all", text)
        self.assertIn("actions/upload-artifact@v4", text)
        self.assertIn("if: always()", text)

    def test_u1_binds_exact_skill_and_every_trial_records_a_receipt(self):
        text = self.workflow_text()
        self.assertIn('if [ "$CONDITION" = "U1" ]; then', text)
        self.assertIn("verified-delta/SKILL.md", text)
        self.assertIn("force-loaded-skill", text)
        self.assertIn("run-config.json", text)
        self.assertIn("metrics.json", text)
        self.assertIn("python eval_harness.py record", text)
        self.assertIn("--run-config", text)
        self.assertIn("receipt.json", text)
        self.assertIn('"input_tokens": None', text)
        self.assertIn('"output_tokens": None', text)
        self.assertIn('"tool_calls": None', text)

    def test_pair_pins_one_cli_version_and_summarizes_both_receipts(self):
        text = self.workflow_text()
        self.assertIn("npm view @github/copilot version", text)
        self.assertIn("needs: [validate, resolve]", text)
        self.assertIn('@github/copilot@${{ needs.resolve.outputs.copilot_version }}', text)
        self.assertIn("actions/download-artifact@v4", text)
        self.assertIn("python eval_harness.py summarize", text)
        self.assertIn("pair-summary", text)
        self.assertIn("not_comparable", text)

    def test_dispatch_inputs_are_validated_before_trial_jobs(self):
        text = self.workflow_text()
        self.assertIn("Validate dispatch inputs before any Copilot trial", text)
        self.assertIn('[[ "$REPLICATE_INPUT" =~ ^[1-9][0-9]*$ ]]', text)
        self.assertIn('[[ -n "${MODEL_INPUT//[[:space:]]/}" ]]', text)
        self.assertIn("needs: [validate, resolve]", text)
        self.assertLess(
            text.index("Validate dispatch inputs before any Copilot trial"),
            text.index("Run isolated Copilot trial"),
        )


if __name__ == "__main__":
    unittest.main()
