import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENABLER = ROOT / ".github" / "workflows" / "temporal-dispatch-surface-enable-once.yml"


class TemporalDispatchSurfaceEnablerTests(unittest.TestCase):
    def test_enabler_creates_exact_verified_branch_patch_without_dispatching(self):
        self.assertTrue(ENABLER.is_file(), "temporary dispatch-surface enabler is missing")
        workflow = ENABLER.read_text(encoding="utf-8")

        self.assertIn("push:", workflow)
        self.assertIn("branches: [main]", workflow)
        self.assertIn("temporal-dispatch-surface-enable-once.yml", workflow)
        self.assertIn("contents: write", workflow)
        self.assertNotIn("actions: write", workflow)

        self.assertIn("ops/enable-temporal-dispatch-choice", workflow)
        self.assertIn("temporal-supersession", workflow)
        self.assertIn("temporal-continuity-control", workflow)
        self.assertIn("execution-recovery-development.yml", workflow)

        self.assertIn("python -m unittest discover -s tests -v", workflow)
        self.assertIn("python verify.py", workflow)
        self.assertIn("git diff --check", workflow)
        self.assertIn("git push origin HEAD:refs/heads/ops/enable-temporal-dispatch-choice", workflow)

        lowered = workflow.lower()
        self.assertNotIn("gh workflow run", lowered)
        self.assertNotIn("rerun", lowered)
        self.assertNotIn("retry", lowered)
        self.assertNotIn("--force", lowered)


if __name__ == "__main__":
    unittest.main()
