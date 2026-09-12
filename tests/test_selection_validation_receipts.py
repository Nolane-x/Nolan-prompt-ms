import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

import selection_validation as selection

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "selection_validation.py"
SKILL = ROOT / "verified-delta" / "SKILL.md"
CANDIDATE = ROOT / "evals" / "candidates" / "r1-target-authority.md"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class SelectionValidationReceiptTests(unittest.TestCase):
    def run_harness(self, *args):
        return subprocess.run(
            [sys.executable, str(HARNESS), *map(str, args)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def generate(self, root: pathlib.Path):
        bundle = root / "bundle"
        result = self.run_harness("generate", "--seed", "receipt-seed", "--output", bundle, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        return bundle, json.loads((bundle / "bundle.json").read_text(encoding="utf-8"))

    def write_metrics(self, root: pathlib.Path, arm: str) -> pathlib.Path:
        path = root / f"{arm}-metrics.json"
        path.write_text(json.dumps({
            "input_tokens": None,
            "output_tokens": None,
            "tool_calls": 1,
            "wall_time_ms": 10,
        }), encoding="utf-8")
        return path

    def write_run_config(self, root: pathlib.Path, arm: str, case_id: str, reasoning: str = "medium") -> pathlib.Path:
        treatment = SKILL if arm == "R1" else CANDIDATE
        path = root / f"{arm}-run-config.json"
        path.write_text(json.dumps({
            "schema_version": 1,
            "matched": {
                "prompt_language": "en",
                "model": {
                    "provider": "github-copilot-cli",
                    "id": "test-model",
                    "requested": "auto",
                    "snapshot": "provider-managed-unpinned",
                },
                "harness": {
                    "id": "github-copilot-selection-v1",
                    "version": "1.0.83",
                    "runner_os": "Linux",
                    "runner_arch": "X64",
                },
                "tool_set": ["bash", "create", "edit", "view", "glob", "grep"],
                "tool_policy": {
                    "allow": "write,shell(python:*)",
                    "builtin_mcps": False,
                    "custom_instructions": False,
                    "agent_cwd": "isolated-runner-temp-workspace",
                },
                "reasoning_effort": reasoning,
                "sampling_controls": None,
                "limits": {"job_timeout_minutes": 10},
            },
            "intervention": {
                "delivery_form": "force-loaded-incumbent" if arm == "R1" else "force-loaded-candidate",
                "metadata_language": "en",
                "body_language": "en",
                "description_variant": "r1" if arm == "R1" else "r1-target-authority",
                "available_skill_set_sha256": sha256(treatment),
            },
            "trial": {
                "clean_environment_id": f"test-{case_id}-{arm}",
                "trial_id": f"test-{case_id}-{arm}",
                "timestamp_utc": "2026-09-12T13:00:00Z",
            },
        }), encoding="utf-8")
        return path

    def record(self, root: pathlib.Path, bundle: pathlib.Path, case: dict, arm: str, reasoning: str = "medium"):
        workspace = root / f"workspace-{arm}"
        prepared = self.run_harness("prepare", bundle, case["id"], workspace, "--json")
        self.assertEqual(prepared.returncode, 0, prepared.stderr)
        transcript = root / f"{arm}-transcript.txt"
        transcript.write_text("inspected current target and verified local state\n", encoding="utf-8")
        receipt = root / f"{arm}-receipt.json"
        result = self.run_harness(
            "record", bundle, case["id"], workspace, receipt,
            "--arm", arm,
            "--model-id", "test-model",
            "--harness-id", "github-copilot-selection-v1",
            "--transcript", transcript,
            "--metrics", self.write_metrics(root, arm),
            "--run-config", self.write_run_config(root, arm, case["id"], reasoning),
            "--json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return receipt

    def test_record_is_immutable_and_binds_generated_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            bundle, manifest = self.generate(root)
            case = next(case for case in manifest["cases"] if case["cell_id"] == "preserve_already_satisfied")
            receipt = self.record(root, bundle, case, "R1")
            payload = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(payload["experiment"], "target-authority-selection-validation-v1")
            self.assertEqual(payload["arm"], "R1")
            self.assertEqual(payload["case"]["id"], case["id"])
            self.assertEqual(payload["case"]["prompt_sha256"], case["prompt_sha256"])
            self.assertEqual(payload["case"]["fixture_sha256"], case["fixture_sha256"])
            self.assertEqual(payload["case"]["grader_sha256"], case["grader_sha256"])
            self.assertEqual(payload["bundle"]["seed"], "receipt-seed")
            self.assertTrue(payload["grade"]["passed"])
            duplicate = self.run_harness(
                "record", bundle, case["id"], root / "workspace-R1", receipt,
                "--arm", "R1", "--model-id", "test-model",
                "--harness-id", "github-copilot-selection-v1",
                "--transcript", root / "R1-transcript.txt",
                "--metrics", root / "R1-metrics.json",
                "--run-config", root / "R1-run-config.json", "--json",
            )
            self.assertNotEqual(duplicate.returncode, 0)
            self.assertIn("already exists", duplicate.stderr)

    def test_pair_summary_marks_actual_matched_context_drift_not_comparable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            bundle, manifest = self.generate(root)
            case = next(case for case in manifest["cases"] if case["cell_id"] == "preserve_already_satisfied")
            r1 = self.record(root, bundle, case, "R1", "medium")
            r1a = self.record(root, bundle, case, "R1A", "high")
            result = self.run_harness("summarize", bundle, r1, r1a, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            pair = next(pair for pair in payload["pairs"] if pair["pair_id"] == case["pair_id"])
            self.assertFalse(pair["comparable"])
            self.assertEqual(pair["effect"], "not_comparable")
            self.assertTrue(any("matched run config mismatch" in issue for issue in pair["issues"]))
            self.assertFalse(payload["infrastructure_valid"])
            self.assertFalse(payload["decision"]["passed"])

    def test_exact_preregistered_decision_rule_rejects_minority_harm(self):
        pairs = []
        roles = ["preserve", "act", "preserve", "act", "probe", "verify"]
        for cell_index, role in enumerate(roles):
            for replicate in (1, 2):
                pairs.append({
                    "pair_id": f"cell-{cell_index}-r{replicate}",
                    "role": role,
                    "comparable": True,
                    "effect": "candidate_gain" if role == "preserve" else "same_pass",
                    "arms": {"R1": {"passed": role != "preserve"}, "R1A": {"passed": True}},
                })
        passed = selection.evaluate_decision(pairs)
        self.assertTrue(passed["passed"])
        harmed = json.loads(json.dumps(pairs))
        harmed[1]["effect"] = "candidate_harm"
        harmed[1]["arms"]["R1A"]["passed"] = False
        self.assertFalse(selection.evaluate_decision(harmed)["passed"])


if __name__ == "__main__":
    unittest.main()
