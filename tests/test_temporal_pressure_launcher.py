import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / ".github" / "workflows" / "temporal-pressure-launch-once.yml"


class TemporalPressureLauncherTests(unittest.TestCase):
    def test_launcher_is_one_shot_exact_and_non_retrying(self):
        self.assertTrue(LAUNCHER.is_file(), "one-shot launcher workflow is missing")
        workflow = LAUNCHER.read_text(encoding="utf-8")

        self.assertIn("push:", workflow)
        self.assertIn("branches: [main]", workflow)
        self.assertIn("temporal-pressure-launch-once.yml", workflow)
        self.assertIn("actions: write", workflow)
        self.assertIn("contents: read", workflow)
        self.assertIn("GH_TOKEN: ${{ github.token }}", workflow)

        self.assertEqual(
            workflow.count("gh workflow run execution-recovery-development.yml"),
            2,
        )
        for case_id in ("temporal-supersession", "temporal-continuity-control"):
            self.assertIn(f"-f case_id={case_id}", workflow)

        self.assertEqual(workflow.count("--ref main"), 2)
        self.assertEqual(workflow.count("-f model=auto"), 2)
        self.assertEqual(workflow.count("-f reasoning_effort=default"), 2)
        self.assertEqual(workflow.count("-f replicate=1"), 2)

        lowered = workflow.lower()
        self.assertNotIn("rerun", lowered)
        self.assertNotIn("retry", lowered)
        self.assertNotIn("while ", lowered)


if __name__ == "__main__":
    unittest.main()
