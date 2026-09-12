import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "target-authority-selection.yml"


class TargetAuthoritySelectionWorkflowTests(unittest.TestCase):
    def workflow_text(self) -> str:
        self.assertTrue(WORKFLOW.is_file(), "selection-validation workflow must exist")
        return WORKFLOW.read_text(encoding="utf-8")

    def test_workflow_is_manual_with_named_model_and_no_external_seed_input(self):
        text = self.workflow_text()
        self.assertIn("workflow_dispatch:", text)
        self.assertNotIn("execution_seed:", text)
        self.assertNotIn("EXECUTION_SEED: ${{ inputs.execution_seed }}", text)
        self.assertNotIn("\n  push:", text)
        self.assertNotIn("\n  pull_request:", text)
        self.assertIn("default: gpt-5.4", text)
        self.assertIn("default: medium", text)

    def test_model_preflight_finishes_before_hidden_bundle_generation(self):
        text = self.workflow_text()
        self.assertIn("preflight:", text)
        self.assertIn("needs: [validate, resolve]", text)
        self.assertIn('@github/copilot@${{ needs.resolve.outputs.copilot_version }}', text)
        self.assertIn('copilot \\', text)
        self.assertIn('--model="$MODEL_ID"', text)
        self.assertIn('python copilot_event_parser.py attest-runtime', text)
        self.assertIn('generate:\n    needs: preflight', text)

    def test_generation_refuses_rerun_before_creating_private_seed(self):
        text = self.workflow_text()
        generate = text.index("\n  generate:\n")
        trial = text.index("\n  trial:\n")
        block = text[generate:trial]
        self.assertIn("GITHUB_RUN_ATTEMPT: ${{ github.run_attempt }}", block)
        guard = 'if [ "$GITHUB_RUN_ATTEMPT" != "1" ]; then'
        self.assertIn(guard, block)
        self.assertIn("Refusing selection rerun before hidden generation", block)
        self.assertLess(block.index(guard), block.index("secrets.token_hex(32)"))

    def test_generation_uses_private_internal_seed_and_reference_admission_before_trials(self):
        text = self.workflow_text()
        self.assertIn("secrets.token_hex(32)", text)
        self.assertIn('seed=$(python - <<\'PY\'', text)
        self.assertIn('python selection_validation.py generate', text)
        self.assertIn('--seed "$seed"', text)
        self.assertIn("python selection_validation.py admit", text)
        self.assertIn("matrix", text)
        self.assertIn("actions/upload-artifact@v4", text)
        self.assertIn("selection-hidden-bundle", text)
        self.assertNotIn("EXECUTION_SEED:", text)
        self.assertIn("needs: [generate, resolve]", text)

    def test_all_24_arms_use_one_pinned_cli_and_isolated_runtime(self):
        text = self.workflow_text()
        self.assertIn("npm view @github/copilot version", text)
        self.assertIn('@github/copilot@${{ needs.resolve.outputs.copilot_version }}', text)
        self.assertIn("fromJson(needs.generate.outputs.matrix)", text)
        self.assertIn("CASE_ID: ${{ matrix.case_id }}", text)
        self.assertIn("ARM: ${{ matrix.arm }}", text)
        self.assertIn("$RUNNER_TEMP", text)
        self.assertIn("COPILOT_HOME", text)
        self.assertIn("PYTHONDONTWRITEBYTECODE: \"1\"", text)
        self.assertIn("python selection_validation.py prepare", text)
        self.assertIn('if [ "$ARM" = "R1" ]; then', text)
        self.assertIn("cat verified-delta/SKILL.md", text)
        self.assertIn("cat evals/candidates/r1-target-authority.md", text)
        self.assertIn('rm -rf "$BUNDLE_ROOT"', text)
        self.assertIn('test ! -e "$RUNNER_TEMP/selection-bundle-before"', text)
        self.assertIn("Scrub repository checkout before inference", text)
        self.assertIn('find "$GITHUB_WORKSPACE" -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +', text)
        self.assertIn("Restore trusted repository checkout after inference", text)
        self.assertIn("--available-tools='bash,create,edit,view,glob,grep'", text)
        self.assertNotIn("--available-tools='bash,apply_patch,create,edit,view,glob,grep'", text)
        self.assertIn("--disable-builtin-mcps", text)
        self.assertIn("--no-custom-instructions", text)
        self.assertIn("--no-remote", text)
        self.assertNotIn("--allow-all", text)

    def test_actual_runtime_and_tool_event_evidence_drive_receipts(self):
        text = self.workflow_text()
        self.assertIn("python copilot_event_parser.py attest-runtime", text)
        self.assertIn('actual_model_id = attestation["model"]', text)
        self.assertIn('reasoning_effort = attestation["reasoning_effort"]', text)
        self.assertIn('tool_set = attestation["tool_set"]', text)
        self.assertIn('"tool_set": tool_set', text)
        self.assertIn("python selection_process_evidence.py extract", text)
        self.assertIn('"$TRIAL_ROOT/copilot-events.jsonl"', text)
        self.assertIn('"$TRIAL_ROOT/grading-evidence.txt"', text)
        self.assertIn("python selection_validation.py record", text)
        self.assertIn('--transcript "$TRIAL_ROOT/grading-evidence.txt"', text)
        self.assertIn('--arm "$ARM"', text)
        self.assertIn("if: always()", text)

    def test_summary_requires_exactly_24_receipts_and_runs_frozen_decision(self):
        text = self.workflow_text()
        self.assertIn("actions/download-artifact@v4", text)
        self.assertIn('if [ "${#receipts[@]}" -ne 24 ]; then', text)
        self.assertIn("python selection_validation.py summarize", text)
        self.assertIn("selection-summary", text)
        self.assertIn("infrastructure_valid", text)
        self.assertIn('decision["passed"]', text)


if __name__ == "__main__":
    unittest.main()
