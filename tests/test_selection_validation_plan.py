import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLAN = ROOT / "evals" / "selection-validation-plan.json"


class SelectionValidationPlanTests(unittest.TestCase):
    def test_plan_freezes_catalog_sampling_and_decision_rule(self):
        data = json.loads(PLAN.read_text(encoding="utf-8"))
        self.assertEqual(data["experiment"], "target-authority-selection-v1")
        self.assertEqual(data["selected_family_count"], 4)
        self.assertEqual(data["variants"], ["noop", "partial"])
        self.assertEqual(
            data["family_catalog"],
            [
                "retry-cap",
                "stable-dedupe",
                "export-suffix",
                "boolean-flag",
                "port-fallback",
                "config-precedence",
            ],
        )
        self.assertEqual(data["decision_rule"]["max_candidate_harm"], 0)
        self.assertEqual(data["decision_rule"]["required_partial_passes"], 4)
        self.assertEqual(data["decision_rule"]["minimum_noop_passes"], 3)
        self.assertEqual(data["decision_rule"]["minimum_noop_candidate_gains"], 1)
        self.assertEqual(data["maximum_infrastructure_replacements"], 1)
        self.assertEqual(data["copilot_trial_count"], 16)
        self.assertEqual(data["seed_formula_version"], "selection-v1")
        self.assertTrue(data["manual_dispatch_only"])


if __name__ == "__main__":
    unittest.main()
