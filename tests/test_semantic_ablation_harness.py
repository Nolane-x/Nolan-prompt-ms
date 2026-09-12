import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "semantic_ablation.py"
SKILL = ROOT / "verified-delta" / "SKILL.md"
CANDIDATE = ROOT / "evals" / "candidates" / "r1-target-authority.md"
FIXTURE = ROOT / "evals" / "cases" / "username-normalization-noop" / "fixture"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


class SemanticAblationHarnessTests(unittest.TestCase):
    def run_harness(self, *args):
        return subprocess.run(
            [sys.executable, str(HARNESS), *map(str, args)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def write_metrics(self, root: pathlib.Path, name: str) -> pathlib.Path:
        path = root / f"{name}-metrics.json"
        path.write_text(
            json.dumps(
                {
                    "input_tokens": None,
                    "output_tokens": None,
                    "tool_calls": 1,
                    "wall_time_ms": 10,
                }
            ),
            encoding="utf-8",
        )
        return path

    def write_run_config(
        self,
        root: pathlib.Path,
        arm: str,
        *,
        reasoning_effort: str = "medium",
    ) -> pathlib.Path:
        treatment_path = SKILL if arm == "R1" else CANDIDATE
        delivery = "force-loaded-incumbent" if arm == "R1" else "force-loaded-candidate"
        description_variant = "r1" if arm == "R1" else "r1-target-authority"
        payload = {
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
                    "id": "github-copilot-ablation-v1",
                    "version": "1.0.83",
                    "runner_os": "Linux",
                    "runner_arch": "X64",
                },
                "tool_set": ["bash", "apply_patch", "create", "edit", "view", "glob", "grep"],
                "tool_policy": {
                    "allow": "write,shell(python:*)",
                    "builtin_mcps": False,
                    "custom_instructions": False,
                    "agent_cwd": "isolated-runner-temp-workspace",
                },
                "reasoning_effort": reasoning_effort,
                "sampling_controls": None,
                "limits": {"job_timeout_minutes": 10},
            },
            "intervention": {
                "delivery_form": delivery,
                "metadata_language": "en",
                "body_language": "en",
                "description_variant": description_variant,
                "available_skill_set_sha256": sha256(treatment_path),
            },
            "trial": {
                "clean_environment_id": f"test-{arm}",
                "trial_id": f"test-noop-{arm}-r1",
                "timestamp_utc": "2026-09-12T09:00:00Z",
            },
        }
        path = root / f"{arm}-run-config.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def record(
        self,
        root: pathlib.Path,
        arm: str,
        workspace: pathlib.Path,
        *,
        reasoning_effort: str = "medium",
    ) -> pathlib.Path:
        transcript = root / f"{arm}-transcript.md"
        transcript.write_text(f"# {arm}\n", encoding="utf-8")
        metrics = self.write_metrics(root, arm)
        run_config = self.write_run_config(root, arm, reasoning_effort=reasoning_effort)
        receipt = root / f"{arm}-receipt.json"
        result = self.run_harness(
            "record",
            "username-normalization-noop",
            workspace,
            receipt,
            "--arm",
            arm,
            "--pair-id",
            "target-authority-noop",
            "--replicate",
            "1",
            "--model-id",
            "test-model",
            "--harness-id",
            "github-copilot-ablation-v1",
            "--transcript",
            transcript,
            "--metrics",
            metrics,
            "--run-config",
            run_config,
            "--json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(receipt.is_file())
        return receipt

    def test_real_grader_pair_classifies_candidate_gain(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            r1_workspace = root / "r1-workspace"
            r1a_workspace = root / "r1a-workspace"
            shutil.copytree(FIXTURE, r1_workspace)
            shutil.copytree(FIXTURE, r1a_workspace)

            app = r1_workspace / "app.py"
            app.write_text(
                app.read_text(encoding="utf-8").replace(".lower()", ".casefold()"),
                encoding="utf-8",
            )

            r1_receipt = self.record(root, "R1", r1_workspace)
            r1a_receipt = self.record(root, "R1A", r1a_workspace)

            summary = self.run_harness("summarize", r1_receipt, r1a_receipt, "--json")
            self.assertEqual(summary.returncode, 0, summary.stderr)
            payload = json.loads(summary.stdout)
            self.assertEqual(len(payload["pairs"]), 1)
            pair = payload["pairs"][0]
            self.assertTrue(pair["comparable"])
            self.assertEqual(pair["counts"]["candidate_gain"], 1)
            self.assertEqual(pair["replicates"][0]["effect"], "candidate_gain")
            self.assertFalse(pair["replicates"][0]["arms"]["R1"]["passed"])
            self.assertTrue(pair["replicates"][0]["arms"]["R1A"]["passed"])

    def test_summarize_fails_closed_on_matched_context_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            r1_workspace = root / "r1-workspace"
            r1a_workspace = root / "r1a-workspace"
            shutil.copytree(FIXTURE, r1_workspace)
            shutil.copytree(FIXTURE, r1a_workspace)

            r1_receipt = self.record(root, "R1", r1_workspace, reasoning_effort="medium")
            r1a_receipt = self.record(root, "R1A", r1a_workspace, reasoning_effort="high")

            summary = self.run_harness("summarize", r1_receipt, r1a_receipt, "--json")
            self.assertEqual(summary.returncode, 0, summary.stderr)
            pair = json.loads(summary.stdout)["pairs"][0]
            self.assertFalse(pair["comparable"])
            self.assertEqual(pair["replicates"][0]["effect"], "not_comparable")
            self.assertTrue(any("matched run config mismatch" in issue for issue in pair["issues"]))

    def test_historical_receipts_do_not_depend_on_current_harness_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            r1_workspace = root / "r1-workspace"
            r1a_workspace = root / "r1a-workspace"
            shutil.copytree(FIXTURE, r1_workspace)
            shutil.copytree(FIXTURE, r1a_workspace)
            receipts = [
                self.record(root, "R1", r1_workspace),
                self.record(root, "R1A", r1a_workspace),
            ]
            for receipt in receipts:
                payload = json.loads(receipt.read_text(encoding="utf-8"))
                payload["eval_provenance"]["semantic_ablation_sha256"] = "a" * 64
                receipt.write_text(json.dumps(payload), encoding="utf-8")

            summary = self.run_harness("summarize", *receipts, "--json")
            self.assertEqual(summary.returncode, 0, summary.stderr)
            self.assertTrue(json.loads(summary.stdout)["pairs"][0]["comparable"])

    def test_historical_receipts_bind_recorded_treatments_not_current_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            r1_workspace = root / "r1-workspace"
            r1a_workspace = root / "r1a-workspace"
            shutil.copytree(FIXTURE, r1_workspace)
            shutil.copytree(FIXTURE, r1a_workspace)
            receipts = {
                "R1": self.record(root, "R1", r1_workspace),
                "R1A": self.record(root, "R1A", r1a_workspace),
            }
            historical_shas = {"R1": "1" * 64, "R1A": "2" * 64}
            historical_set = canonical_sha256(historical_shas)
            for arm, receipt in receipts.items():
                payload = json.loads(receipt.read_text(encoding="utf-8"))
                payload["treatment"]["loaded_sha256"] = historical_shas[arm]
                payload["treatment"]["treatment_sha256s"] = historical_shas
                payload["treatment"]["treatment_set_sha256"] = historical_set
                run_config = payload["run_config"]
                run_config["value"]["intervention"]["available_skill_set_sha256"] = historical_shas[arm]
                run_config["sha256"] = canonical_sha256(run_config["value"])
                run_config["matched_sha256"] = canonical_sha256(run_config["value"]["matched"])
                receipt.write_text(json.dumps(payload), encoding="utf-8")

            summary = self.run_harness("summarize", *receipts.values(), "--json")
            self.assertEqual(summary.returncode, 0, summary.stderr)
            self.assertTrue(json.loads(summary.stdout)["pairs"][0]["comparable"])


if __name__ == "__main__":
    unittest.main()
