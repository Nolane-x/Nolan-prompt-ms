import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLAN = ROOT / "evals" / "selection-validation-plan.json"


class SelectionValidationPlanTests(unittest.TestCase):
    def test_plan_freezes_cases_budget_and_decision_rule(self):
        payload = json.loads(PLAN.read_text(encoding="utf-8"))
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(
            set(payload["case_keys"]),
            {
                "config-noop",
                "config-required",
                "writing-noop",
                "writing-required",
                "data-noop",
                "data-required",
            },
        )
        self.assertEqual(payload["replicates"], [1])
        self.assertEqual(payload["max_model_trials"], 12)
        self.assertEqual(payload["candidate"], "evals/candidates/r1-target-authority.md")
        rule = payload["decision_rule"]
        self.assertEqual(rule["required_action_candidate_harm_max"], 0)
        self.assertEqual(rule["candidate_pass_min"], 6)
        self.assertEqual(rule["noop_candidate_gain_min"], 1)
        self.assertEqual(rule["on_failure"], "stop_without_rewriting_candidate")


if __name__ == "__main__":
    unittest.main()
