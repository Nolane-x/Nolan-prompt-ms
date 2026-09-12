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


if __name__ == "__main__":
    unittest.main()
