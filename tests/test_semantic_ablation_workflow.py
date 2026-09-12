import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "semantic-ablation.yml"


class SemanticAblationWorkflowTests(unittest.TestCase):
    def workflow_text(self) -> str:
        self.assertTrue(WORKFLOW.is_file(), "semantic ablation workflow must exist")
        return WORKFLOW.read_text(encoding="utf-8")

    def test_workflow_is_manual_and_scoped_to_opposing_normalization_cases(self):
        text = self.workflow_text()
        self.assertIn("workflow_dispatch:", text)
        self.assertNotIn("\n  push:", text)
        self.assertNotIn("\n  pull_request:", text)
        self.assertIn("username-normalization-noop", text)
        self.assertIn("username-normalization-partial", text)
        self.assertNotIn("false-completion-state", text)
        self.assertIn("default: auto", text)
        self.assertIn("default: default", text)

    def test_pair_is_fresh_and_binds_exact_incumbent_vs_candidate_prompts(self):
        text = self.workflow_text()
        self.assertIn("arm: [R1, R1A]", text)
        self.assertIn("$RUNNER_TEMP", text)
        self.assertIn("COPILOT_HOME", text)
        self.assertIn('if [ "$ARM" = "R1" ]; then', text)
        self.assertIn("cat verified-delta/SKILL.md", text)
        self.assertIn("cat evals/candidates/r1-target-authority.md", text)
        self.assertIn("python eval_harness.py prepare", text)
        self.assertIn("--disable-builtin-mcps", text)
        self.assertIn("--no-custom-instructions", text)
        self.assertIn("--no-remote", text)
        self.assertNotIn("--allow-all", text)

    def test_runtime_attestation_and_arm_specific_receipts_are_fail_closed(self):
        text = self.workflow_text()
        self.assertIn("python copilot_event_parser.py attest-runtime", text)
        self.assertIn('"tool_calls": attestation["tool_calls"]', text)
        self.assertIn('reasoning_effort = attestation["reasoning_effort"]', text)
        self.assertIn("force-loaded-incumbent", text)
        self.assertIn("force-loaded-candidate", text)
        self.assertIn("python semantic_ablation.py record", text)
        self.assertIn('--arm "$ARM"', text)
        self.assertIn("actions/upload-artifact@v4", text)
        self.assertIn("if: always()", text)

    def test_matched_tool_set_comes_from_runtime_attestation(self):
        text = self.workflow_text()
        self.assertIn('tool_set = attestation["tool_set"]', text)
        self.assertIn('"tool_set": tool_set', text)
        self.assertIn("--available-tools='bash,create,edit,view,glob,grep'", text)
        self.assertNotIn("--available-tools='bash,apply_patch,create,edit,view,glob,grep'", text)
        self.assertNotIn('"tool_set": ["bash", "apply_patch", "create", "edit", "view", "glob", "grep"]', text)

    def test_pair_pins_one_cli_version_and_summarizes_exactly_two_receipts(self):
        text = self.workflow_text()
        self.assertIn("npm view @github/copilot version", text)
        self.assertIn("needs: [validate, resolve]", text)
        self.assertIn('@github/copilot@${{ needs.resolve.outputs.copilot_version }}', text)
        self.assertIn("actions/download-artifact@v4", text)
        self.assertIn('if [ "${#receipts[@]}" -ne 2 ]; then', text)
        self.assertIn("python semantic_ablation.py summarize", text)
        self.assertIn("not_comparable", text)
        self.assertIn("ablation-summary", text)


if __name__ == "__main__":
    unittest.main()
