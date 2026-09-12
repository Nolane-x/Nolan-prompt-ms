import hashlib
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLAN = ROOT / "evals" / "target-authority-selection-plan.json"
R1 = ROOT / "verified-delta" / "SKILL.md"
R1A = ROOT / "evals" / "candidates" / "r1-target-authority.md"

EXPECTED_CELLS = {
    "preserve_already_satisfied",
    "act_defect_remains",
    "preserve_outside_target_improvement",
    "act_explicit_broader_requirement",
    "probe_resolvable_ambiguity",
    "verify_authoritative_state",
}


def git_blob_sha1(path: pathlib.Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


class TargetAuthoritySelectionPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = json.loads(PLAN.read_text(encoding="utf-8"))

    def test_freezes_experiment_shape_and_treatments(self):
        plan = self.plan
        self.assertEqual(plan["schema_version"], 1)
        self.assertEqual(plan["experiment"], "target-authority-selection-validation-v1")
        self.assertEqual(plan["evidence_class"], "selection-validation")
        self.assertEqual(plan["arms"], ["R1", "R1A"])
        self.assertEqual(plan["replicates_per_cell"], 2)
        self.assertEqual(plan["fixed_model_trial_budget"], 24)

        treatments = plan["treatments"]
        self.assertEqual(
            treatments["R1"]["git_blob"],
            "ac48f09ab02eca63e014b4c25f86e492ae5559cb",
        )
        self.assertEqual(
            treatments["R1A"]["git_blob"],
            "26d93ce346deedccd7186ad5856f849136825ec3",
        )
        self.assertEqual(git_blob_sha1(R1), treatments["R1"]["git_blob"])
        self.assertEqual(git_blob_sha1(R1A), treatments["R1A"]["git_blob"])

    def test_requires_six_cross_domain_semantic_cells_without_normalization_reuse(self):
        cells = self.plan["semantic_cells"]
        self.assertEqual(len(cells), 6)
        self.assertEqual({cell["id"] for cell in cells}, EXPECTED_CELLS)
        self.assertGreaterEqual(self.plan["task_family_constraints"]["minimum_distinct_families"], 4)
        self.assertIn(
            "username-normalization",
            self.plan["task_family_constraints"]["forbidden_development_family_substrings"],
        )
        for cell in cells:
            self.assertIn(cell["role"], {"preserve", "act", "probe", "verify"})
            self.assertTrue(cell["required_behavior"].strip())

    def test_hidden_instances_are_not_committed_or_cherry_picked(self):
        boundary = self.plan["hidden_instance_boundary"]
        self.assertFalse(boundary["commit_final_prompts_before_execution"])
        self.assertFalse(boundary["commit_final_fixture_values_before_execution"])
        self.assertFalse(boundary["commit_final_expected_answers_before_execution"])
        self.assertTrue(boundary["generate_after_preregistration_freeze"])
        self.assertTrue(boundary["record_execution_seed"])
        self.assertTrue(boundary["use_all_generated_instances"])
        self.assertEqual(boundary["contaminated_instance_action"], "exclude_and_fail_validation_boundary")

    def test_matched_context_and_decision_rule_fail_closed(self):
        matched = set(self.plan["matched_pair_dimensions"])
        self.assertTrue(
            {
                "case_identity",
                "fixture_hash",
                "actual_model",
                "actual_reasoning_effort",
                "harness_version",
                "actual_tool_set",
                "tool_policy",
                "prompt_language",
                "resource_limits",
                "generator_provenance",
                "grader_provenance",
                "replicate_identity",
            }.issubset(matched)
        )

        decision = self.plan["decision_rule"]
        self.assertEqual(decision["required_comparable_pairs"], 12)
        self.assertEqual(decision["maximum_candidate_harm"], 0)
        self.assertEqual(decision["required_r1a_passes_on_act_probe_verify"], 8)
        self.assertEqual(decision["minimum_r1a_passes_on_preserve_replicates"], 3)
        self.assertEqual(decision["minimum_candidate_gain_on_preserve_replicates"], 2)
        self.assertEqual(
            decision["pass_status"],
            "selection-stable under observed harness/model configuration; not runtime-resident",
        )

    def test_budget_does_not_stop_early_on_behavioral_outcomes(self):
        stopping = self.plan["stopping_rule"]
        self.assertEqual(stopping["paired_replicates"], 12)
        self.assertFalse(stopping["behavioral_early_stop"])
        self.assertTrue(stopping["retry_infrastructure_failures_same_identity"])
        self.assertFalse(stopping["count_infrastructure_failures_as_behavioral_samples"])


if __name__ == "__main__":
    unittest.main()
