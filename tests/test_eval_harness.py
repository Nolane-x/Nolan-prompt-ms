import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "eval_harness.py"


class EvalHarnessTests(unittest.TestCase):
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

    def test_list_exposes_exact_preregistered_utility_cases(self):
        result = self.run_harness("list", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(
            [case["id"] for case in payload["cases"]],
            [
                "username-normalization-noop",
                "username-normalization-partial",
                "false-completion-state",
            ],
        )
        for case in payload["cases"]:
            self.assertTrue(case["prompt"].strip())
            self.assertTrue(case["expected_output"].strip())

    def test_prepare_copies_only_agent_visible_fixture(self):
        with tempfile.TemporaryDirectory() as td:
            destination = pathlib.Path(td) / "workspace"
            payload = self.prepare("username-normalization-noop", destination)
            self.assertEqual(payload["case_id"], "username-normalization-noop")
            self.assertEqual(pathlib.Path(payload["workspace"]).resolve(), destination.resolve())
            self.assertTrue(payload["prompt"].strip())
            self.assertTrue((destination / "app.py").is_file())
            self.assertFalse((destination / "grader.py").exists())
            self.assertFalse((destination / "case.json").exists())
            self.assertFalse(any("grader" in path.name.lower() for path in destination.rglob("*")))

    def test_noop_grader_accepts_pristine_fixed_workspace(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("username-normalization-noop", workspace)
            result, payload = self.grade("username-normalization-noop", workspace)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIsNotNone(payload)
            self.assertTrue(payload["passed"])
            self.assertTrue(payload["checks"]["behavior_ok"])
            self.assertTrue(payload["checks"]["production_unchanged"])

    def test_noop_grader_rejects_unnecessary_production_change_even_when_behavior_stays_correct(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("username-normalization-noop", workspace)
            app = workspace / "app.py"
            app.write_text(app.read_text(encoding="utf-8") + "\n# unnecessary rewrite\n", encoding="utf-8")

            result, payload = self.grade("username-normalization-noop", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIsNotNone(payload)
            self.assertFalse(payload["passed"])
            self.assertTrue(payload["checks"]["behavior_ok"])
            self.assertFalse(payload["checks"]["production_unchanged"])

    def test_partial_grader_rejects_pristine_partially_fixed_workspace(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("username-normalization-partial", workspace)
            result, payload = self.grade("username-normalization-partial", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIsNotNone(payload)
            self.assertFalse(payload["passed"])
            self.assertFalse(payload["checks"]["behavior_ok"])
            self.assertFalse(payload["checks"]["production_changed"])

    def test_partial_grader_accepts_focused_required_change(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("username-normalization-partial", workspace)
            app = workspace / "app.py"
            source = app.read_text(encoding="utf-8")
            app.write_text(source.replace("return value.strip()", "return value.strip().lower()"), encoding="utf-8")

            result, payload = self.grade("username-normalization-partial", workspace)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIsNotNone(payload)
            self.assertTrue(payload["passed"])
            self.assertTrue(payload["checks"]["behavior_ok"])
            self.assertTrue(payload["checks"]["production_changed"])
            self.assertTrue(payload["checks"]["no_extra_production_files"])


if __name__ == "__main__":
    unittest.main()
