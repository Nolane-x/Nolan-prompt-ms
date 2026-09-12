import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "behavioral-u0-u1.yml"


class CopilotFreshRunnerWorkflowTests(unittest.TestCase):
    def test_workflow_is_manual_and_least_privilege(self):
        self.assertTrue(WORKFLOW.is_file(), "behavioral U0/U1 workflow must exist")
        text = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("workflow_dispatch:", text)
        self.assertNotIn("\n  push:", text)
        self.assertNotIn("\n  pull_request:", text)
        self.assertIn("contents: read", text)
        self.assertIn("copilot-requests: write", text)


if __name__ == "__main__":
    unittest.main()
