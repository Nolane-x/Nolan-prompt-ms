import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "execution_recovery_development.py"
WORKFLOW = ROOT / ".github" / "workflows" / "execution-recovery-development.yml"
CASE_IDS = ["temporal-supersession", "temporal-continuity-control"]
STANDING_RULE_MARKER = "standing-rule-alpha"


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

    def test_cases_are_registered_for_harness_and_manual_dispatch(self):
        result = self.run_harness("list", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        ids = [case["id"] for case in json.loads(result.stdout)["cases"]]
        for case_id in CASE_IDS:
            self.assertIn(case_id, ids)

        workflow = WORKFLOW.read_text(encoding="utf-8")
        for case_id in CASE_IDS:
            self.assertIn(f"- {case_id}", workflow)

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

    def test_continuity_requires_standing_rule_from_previous_turn_without_prompt_leakage(self):
        result = self.run_harness("list", "--json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        cases = {case["id"]: case for case in json.loads(result.stdout)["cases"]}
        prompt = cases["temporal-continuity-control"]["prompt"]
        self.assertIn("remains active", prompt.lower())
        self.assertIn("answer.json", prompt)
        self.assertNotIn(STANDING_RULE_MARKER, prompt)

        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn('CASE_ID: ${{ inputs.case_id }}', workflow)
        self.assertIn('if [ "$CASE_ID" = "temporal-continuity-control" ]; then', workflow)
        self.assertIn(STANDING_RULE_MARKER, workflow)

        with tempfile.TemporaryDirectory() as td:
            workspace = pathlib.Path(td) / "workspace"
            self.prepare("temporal-continuity-control", workspace)
            challenge = json.loads((workspace / "challenge.json").read_text(encoding="utf-8"))

            result, payload = self.grade("temporal-continuity-control", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertFalse(payload["checks"]["answer_present"])

            answer = {
                "schema_version": 1,
                "nonce": challenge["nonce"],
                "standing_rule_marker": STANDING_RULE_MARKER,
            }
            (workspace / "answer.json").write_text(
                json.dumps(answer, sort_keys=True, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )
            result, payload = self.grade("temporal-continuity-control", workspace)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(payload["passed"])

            answer["standing_rule_marker"] = "wrong-standing-rule"
            (workspace / "answer.json").write_text(
                json.dumps(answer, sort_keys=True, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )
            result, payload = self.grade("temporal-continuity-control", workspace)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertFalse(payload["checks"]["standing_rule_preserved"])


if __name__ == "__main__":
    unittest.main()
