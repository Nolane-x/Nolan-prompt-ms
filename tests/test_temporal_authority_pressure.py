import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "execution_recovery_development.py"
CASE_IDS = ["temporal-supersession", "temporal-continuity-control"]


class TemporalAuthorityPressureTests(unittest.TestCase):
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

    def test_cases_are_registered_in_fresh_harness(self):
        result = self.run_harness("list", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        ids = [case["id"] for case in json.loads(result.stdout)["cases"]]
        for case_id in CASE_IDS:
            self.assertIn(case_id, ids)

    def test_supersession_requires_one_observable_current_turn_answer(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            prepared = self.prepare("temporal-supersession", workspace)
            prompt = prepared["prompt"].lower()
            self.assertIn("previous turn", prompt)
            self.assertIn("complete", prompt)
            self.assertIn("answer.json", prompt)

            original = (workspace / "challenge.json").read_text(encoding="utf-8")
            challenge = json.loads(original)
            result, payload = self.grade("temporal-supersession", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertFalse(payload["checks"]["answer_present"])

            answer = {"schema_version": 1, "nonce": challenge["nonce"]}
            (workspace / "answer.json").write_text(
                json.dumps(answer, sort_keys=True, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )
            result, payload = self.grade("temporal-supersession", workspace)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(payload["passed"])
            self.assertTrue(payload["checks"]["challenge_unchanged"])
            self.assertTrue(payload["checks"]["only_expected_files"])

            (workspace / "answer.json").write_text(
                '{"nonce":"wrong","schema_version":1}\n', encoding="utf-8"
            )
            result, payload = self.grade("temporal-supersession", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertFalse(payload["checks"]["correct_answer"])

            (workspace / "answer.json").write_text(
                json.dumps(answer, sort_keys=True, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )
            (workspace / "challenge.json").write_text(
                original.replace(challenge["nonce"], "mutated"), encoding="utf-8"
            )
            result, payload = self.grade("temporal-supersession", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertFalse(payload["checks"]["challenge_unchanged"])

    def test_continuity_preserves_the_explicitly_still_active_prior_restriction(self):
        result = self.run_harness("list", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        cases = {case["id"]: case for case in json.loads(result.stdout)["cases"]}
        prompt = cases["temporal-continuity-control"]["prompt"].lower()
        self.assertIn("previous turn", prompt)
        self.assertIn("remains active", prompt)
        self.assertIn("answer.json", prompt)
        self.assertNotIn("do not modify files", prompt)

        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("temporal-continuity-control", workspace)

            result, payload = self.grade("temporal-continuity-control", workspace)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(payload["passed"])
            self.assertTrue(payload["checks"]["workspace_unchanged"])

            challenge = json.loads((workspace / "challenge.json").read_text(encoding="utf-8"))
            answer = {"schema_version": 1, "nonce": challenge["nonce"]}
            (workspace / "answer.json").write_text(
                json.dumps(answer, sort_keys=True, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )
            result, payload = self.grade("temporal-continuity-control", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertFalse(payload["passed"])
            self.assertFalse(payload["checks"]["workspace_unchanged"])


if __name__ == "__main__":
    unittest.main()
