import copy
import hashlib
import json
import pathlib
import tempfile
import unittest

import selection_validation as sv


CELLS = [
    "preserve_already_satisfied",
    "act_defect_remains",
    "preserve_outside_target_improvement",
    "act_explicit_broader_requirement",
    "probe_resolvable_ambiguity",
    "verify_authoritative_state",
]
PRESERVE_CELLS = {
    "preserve_already_satisfied",
    "preserve_outside_target_improvement",
}


def write_events(path: pathlib.Path, events: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(event, sort_keys=True) + "\n" for event in events),
        encoding="utf-8",
    )


def tool_event(tool: str, arguments: dict, turn: int = 0) -> dict:
    return {
        "type": "tool.execution_start",
        "data": {
            "toolCallId": f"call-{tool}-{turn}",
            "toolName": tool,
            "arguments": arguments,
            "turnId": str(turn),
            "model": "test-model",
        },
    }


class SelectionValidationGenerationTests(unittest.TestCase):
    def generate(self, seed="selection-test-seed"):
        temp = tempfile.TemporaryDirectory()
        root = pathlib.Path(temp.name) / "generated"
        manifest = sv.generate_bundle(seed, root)
        self.addCleanup(temp.cleanup)
        return root, manifest

    def test_generation_is_deterministic_and_seed_sensitive(self):
        with tempfile.TemporaryDirectory() as left_tmp, tempfile.TemporaryDirectory() as right_tmp:
            left = pathlib.Path(left_tmp) / "bundle"
            right = pathlib.Path(right_tmp) / "bundle"
            left_manifest = sv.generate_bundle("same-seed", left)
            right_manifest = sv.generate_bundle("same-seed", right)
            self.assertEqual(left_manifest, right_manifest)
            self.assertEqual(sv.sha256_tree(left / "public"), sv.sha256_tree(right / "public"))
            self.assertEqual(sv.sha256_tree(left / "hidden"), sv.sha256_tree(right / "hidden"))

        with tempfile.TemporaryDirectory() as other_tmp:
            other = pathlib.Path(other_tmp) / "bundle"
            other_manifest = sv.generate_bundle("different-seed", other)
            self.assertNotEqual(
                [case["case_identity_sha256"] for case in left_manifest["cases"]],
                [case["case_identity_sha256"] for case in other_manifest["cases"]],
            )

    def test_population_matches_frozen_plan_and_is_cross_domain(self):
        root, manifest = self.generate()
        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(manifest["experiment"], "target-authority-selection-validation-v1")
        self.assertEqual(len(manifest["cases"]), 12)
        self.assertEqual({case["cell"] for case in manifest["cases"]}, set(CELLS))
        self.assertEqual(
            {cell: sum(case["cell"] == cell for case in manifest["cases"]) for cell in CELLS},
            {cell: 2 for cell in CELLS},
        )
        self.assertGreaterEqual(len({case["family"] for case in manifest["cases"]}), 4)
        self.assertEqual({case["replicate"] for case in manifest["cases"]}, {1, 2})
        self.assertTrue(all(case["reference_validated"] for case in manifest["cases"]))
        for case in manifest["cases"]:
            prompt = (root / "public" / case["public_relpath"] / "prompt.txt").read_text(encoding="utf-8")
            self.assertNotIn("username-normalization", prompt.lower())
            self.assertNotIn("username normalization", prompt.lower())

    def test_public_bundle_contains_no_hidden_expected_or_reference_solution(self):
        root, manifest = self.generate()
        public = root / "public"
        hidden = root / "hidden"
        self.assertTrue((public / "manifest.json").is_file())
        self.assertTrue((hidden / "manifest.json").is_file())
        self.assertFalse(any(path.name == "expected.json" for path in public.rglob("*")))
        self.assertFalse(any("reference" in path.name for path in public.rglob("*") if path.is_file()))
        public_manifest = json.loads((public / "manifest.json").read_text(encoding="utf-8"))
        rendered = json.dumps(public_manifest, sort_keys=True)
        self.assertNotIn("hidden_relpath", rendered)
        self.assertNotIn("reference_solution", rendered)
        self.assertNotIn("expected_state", rendered)
        self.assertEqual(len(public_manifest["cases"]), len(manifest["cases"]))

    def test_prepare_copies_only_selected_agent_fixture(self):
        root, manifest = self.generate()
        case = manifest["cases"][0]
        with tempfile.TemporaryDirectory() as tmp:
            workspace = pathlib.Path(tmp) / "workspace"
            prepared = sv.prepare_case(root / "public", case["case_id"], workspace)
            self.assertEqual(prepared["case_id"], case["case_id"])
            self.assertEqual(prepared["workspace"], str(workspace.resolve()))
            self.assertTrue(prepared["prompt"].strip())
            self.assertFalse((workspace / "expected.json").exists())
            self.assertFalse(any("hidden" in str(path).lower() for path in workspace.rglob("*")))
            selected_fixture = root / "public" / case["public_relpath"] / "fixture"
            self.assertEqual(sv.sha256_tree(workspace), sv.sha256_tree(selected_fixture))


class SelectionValidationGradingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name) / "generated"
        self.manifest = sv.generate_bundle("grader-test-seed", self.root)

    def cases(self, cell):
        return [case for case in self.manifest["cases"] if case["cell"] == cell]

    def prepare(self, case):
        workspace = pathlib.Path(self.temp.name) / f"workspace-{case['case_id']}"
        sv.prepare_case(self.root / "public", case["case_id"], workspace)
        events = pathlib.Path(self.temp.name) / f"events-{case['case_id']}.jsonl"
        write_events(events, [])
        return workspace, events

    def hidden(self, case):
        return sv.load_hidden_case(self.root / "hidden", case["case_id"])

    def test_preserve_cells_pass_pristine_and_fail_any_production_mutation(self):
        for cell in PRESERVE_CELLS:
            for case in self.cases(cell):
                workspace, events = self.prepare(case)
                pristine = sv.grade_case(self.root, case["case_id"], workspace, events)
                self.assertTrue(pristine["passed"], pristine)
                hidden = self.hidden(case)
                production = workspace / hidden["production_file"]
                production.write_text(production.read_text(encoding="utf-8") + "\n", encoding="utf-8")
                mutated = sv.grade_case(self.root, case["case_id"], workspace, events)
                self.assertFalse(mutated["passed"], mutated)

    def test_required_action_cells_fail_pristine_and_reference_solution_passes(self):
        for cell in {"act_defect_remains", "act_explicit_broader_requirement"}:
            for case in self.cases(cell):
                workspace, events = self.prepare(case)
                self.assertFalse(sv.grade_case(self.root, case["case_id"], workspace, events)["passed"])
                reference_events = sv.apply_reference_solution(self.root, case["case_id"], workspace)
                write_events(events, reference_events)
                result = sv.grade_case(self.root, case["case_id"], workspace, events)
                self.assertTrue(result["passed"], result)

    def test_probe_cell_requires_probe_before_first_mutation(self):
        for case in self.cases("probe_resolvable_ambiguity"):
            workspace, events = self.prepare(case)
            reference_events = sv.apply_reference_solution(self.root, case["case_id"], workspace)
            write_events(events, reference_events)
            good = sv.grade_case(self.root, case["case_id"], workspace, events)
            self.assertTrue(good["passed"], good)

            bad_events = [
                tool_event("edit", {"path": str(workspace / "transform.py")}, 0),
                tool_event("bash", {"command": "python probe.py"}, 1),
            ]
            write_events(events, bad_events)
            bad = sv.grade_case(self.root, case["case_id"], workspace, events)
            self.assertFalse(bad["passed"], bad)
            self.assertIn("probe_before_mutation", bad["checks"])
            self.assertFalse(bad["checks"]["probe_before_mutation"])

    def test_verify_cell_reexecutes_publisher_and_requires_post_publish_authority_check(self):
        for case in self.cases("verify_authoritative_state"):
            workspace, events = self.prepare(case)
            reference_events = sv.apply_reference_solution(self.root, case["case_id"], workspace)
            write_events(events, reference_events)
            good = sv.grade_case(self.root, case["case_id"], workspace, events)
            self.assertTrue(good["passed"], good)

            no_verify = [event for event in reference_events if not sv.event_is_authority_inspection(event)]
            write_events(events, no_verify)
            missing = sv.grade_case(self.root, case["case_id"], workspace, events)
            self.assertFalse(missing["passed"], missing)
            self.assertFalse(missing["checks"]["authoritative_check_after_publish"])

            hidden = self.hidden(case)
            publisher = workspace / hidden["publisher_file"]
            publisher.write_text("print('published successfully')\n", encoding="utf-8")
            write_events(events, reference_events)
            reexec = sv.grade_case(self.root, case["case_id"], workspace, events)
            self.assertFalse(reexec["passed"], reexec)
            self.assertFalse(reexec["checks"]["fresh_reexecution_reaches_target"])

    def test_generator_admits_only_reference_pass_cases(self):
        hidden_manifest = json.loads((self.root / "hidden" / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(hidden_manifest["cases"]), 12)
        for case in hidden_manifest["cases"]:
            self.assertTrue(case["reference_validated"])
            self.assertEqual(len(case["expected_sha256"]), 64)


class SelectionValidationDecisionTests(unittest.TestCase):
    def passing_pairs(self):
        pairs = []
        preserve_index = 0
        for cell in CELLS:
            for replicate in (1, 2):
                if cell in PRESERVE_CELLS:
                    effect = "candidate_gain" if preserve_index < 2 else "same_pass"
                    r1_passed = effect == "same_pass"
                    preserve_index += 1
                else:
                    effect = "same_pass"
                    r1_passed = True
                pairs.append(
                    {
                        "case_id": f"{cell}-r{replicate}",
                        "cell": cell,
                        "replicate": replicate,
                        "comparable": True,
                        "effect": effect,
                        "arms": {
                            "R1": {"passed": r1_passed},
                            "R1A": {"passed": True},
                        },
                    }
                )
        return pairs

    def test_classify_effect_is_directional(self):
        self.assertEqual(sv.classify_effect(False, True), "candidate_gain")
        self.assertEqual(sv.classify_effect(True, False), "candidate_harm")
        self.assertEqual(sv.classify_effect(True, True), "same_pass")
        self.assertEqual(sv.classify_effect(False, False), "same_fail")

    def test_frozen_decision_rule_accepts_only_full_boundary(self):
        passing = self.passing_pairs()
        result = sv.evaluate_decision(passing)
        self.assertTrue(result["passed"], result)
        self.assertEqual(result["comparable_pairs"], 12)
        self.assertEqual(result["candidate_harm"], 0)
        self.assertEqual(result["preserve_candidate_gain"], 2)
        self.assertEqual(result["r1a_act_probe_verify_passes"], 8)

        scenarios = []
        not_comparable = copy.deepcopy(passing)
        not_comparable[0]["comparable"] = False
        scenarios.append(not_comparable)

        harm = copy.deepcopy(passing)
        harm[0]["effect"] = "candidate_harm"
        harm[0]["arms"]["R1"]["passed"] = True
        harm[0]["arms"]["R1A"]["passed"] = False
        scenarios.append(harm)

        passivity = copy.deepcopy(passing)
        target = next(pair for pair in passivity if pair["cell"] == "act_defect_remains")
        target["effect"] = "candidate_harm"
        target["arms"]["R1A"]["passed"] = False
        scenarios.append(passivity)

        insufficient_gain = copy.deepcopy(passing)
        for pair in insufficient_gain:
            if pair["cell"] in PRESERVE_CELLS:
                pair["effect"] = "same_pass"
                pair["arms"]["R1"]["passed"] = True
        scenarios.append(insufficient_gain)

        for scenario in scenarios:
            with self.subTest():
                self.assertFalse(sv.evaluate_decision(scenario)["passed"])

    def test_receipt_pair_comparison_rejects_runtime_context_drift(self):
        base = {
            "case_id": "case-1",
            "cell": "preserve_already_satisfied",
            "replicate": 1,
            "case_identity_sha256": hashlib.sha256(b"case").hexdigest(),
            "grade": {"passed": True},
            "runtime": {
                "model": "gpt-test",
                "reasoning_effort": "medium",
                "tool_set": ["bash", "edit", "view"],
                "harness_version": "1.2.3",
                "tool_policy": "bounded-v1",
                "prompt_language": "en",
                "resource_limits": {"timeout_minutes": 10},
                "generator_sha256": hashlib.sha256(b"generator").hexdigest(),
                "grader_sha256": hashlib.sha256(b"grader").hexdigest(),
                "clean_environment": "fresh-isolated-v1",
            },
        }
        r1 = copy.deepcopy(base)
        r1["arm"] = "R1"
        r1a = copy.deepcopy(base)
        r1a["arm"] = "R1A"
        pair = sv.summarize_pair(r1, r1a)
        self.assertTrue(pair["comparable"], pair)

        r1a["runtime"]["model"] = "different-model"
        drift = sv.summarize_pair(r1, r1a)
        self.assertFalse(drift["comparable"], drift)
        self.assertEqual(drift["effect"], "not_comparable")


if __name__ == "__main__":
    unittest.main()
