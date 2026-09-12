import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

import selection_process_evidence as process

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "selection_validation.py"


class SelectionValidationProcessEvidenceTests(unittest.TestCase):
    def run_harness(self, *args):
        return subprocess.run(
            [sys.executable, str(HARNESS), *map(str, args)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def generate(self, root: pathlib.Path):
        bundle = root / "bundle"
        result = self.run_harness(
            "generate", "--seed", "process-evidence-seed", "--output", bundle, "--json"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads((bundle / "bundle.json").read_text(encoding="utf-8"))
        return bundle, manifest

    def write_events(self, root: pathlib.Path, name: str, events: list[dict]) -> pathlib.Path:
        path = root / f"{name}.jsonl"
        path.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
        return path

    def test_probe_cell_requires_real_bash_probe_event_not_model_self_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            bundle, manifest = self.generate(root)
            case = next(
                case for case in manifest["cases"]
                if case["cell_id"] == "probe_resolvable_ambiguity" and case["replicate"] == 1
            )
            self_report_only = self.write_events(root, "self-report", [
                {"type": "assistant.message", "data": {"content": "I ran python probe.py"}},
            ])
            evidence = process.extract_case_evidence(bundle, case["id"], self_report_only)
            self.assertFalse(evidence["passed"])
            self.assertNotIn("probe.py", evidence["trusted_transcript"])

            executed = self.write_events(root, "executed", [
                {
                    "type": "tool.execution_start",
                    "data": {"toolName": "bash", "arguments": {"command": "python probe.py"}},
                },
            ])
            evidence = process.extract_case_evidence(bundle, case["id"], executed)
            self.assertTrue(evidence["passed"])
            self.assertIn("probe.py", evidence["trusted_transcript"])
            self.assertIn("events_sha256", evidence)
            self.assertIn("extractor_sha256", evidence)

    def test_unrelated_tool_metadata_cannot_satisfy_process_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            bundle, manifest = self.generate(root)
            probe_case = next(
                case for case in manifest["cases"]
                if case["cell_id"] == "probe_resolvable_ambiguity" and case["replicate"] == 1
            )
            probe_events = self.write_events(root, "probe-metadata", [
                {
                    "type": "tool.execution_start",
                    "data": {
                        "toolName": "bash",
                        "arguments": {"language": "python", "target": "probe.py"},
                    },
                },
            ])
            self.assertFalse(process.extract_case_evidence(bundle, probe_case["id"], probe_events)["passed"])

            release_case = next(
                case for case in manifest["cases"] if case["cell_id"] == "verify_authoritative_state"
            )
            release_events = self.write_events(root, "release-metadata", [
                {
                    "type": "tool.execution_start",
                    "data": {
                        "toolName": "bash",
                        "arguments": {"language": "python", "target": "publish.py"},
                    },
                },
                {
                    "type": "tool.execution_start",
                    "data": {
                        "toolName": "bash",
                        "arguments": {"verb": "cat ", "target": "release.json"},
                    },
                },
            ])
            self.assertFalse(process.extract_case_evidence(bundle, release_case["id"], release_events)["passed"])

    def test_authoritative_state_requires_file_read_after_publish_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            bundle, manifest = self.generate(root)
            case = next(case for case in manifest["cases"] if case["cell_id"] == "verify_authoritative_state")

            publish_only = self.write_events(root, "publish-only", [
                {
                    "type": "tool.execution_start",
                    "data": {"toolName": "bash", "arguments": {"command": "python publish.py"}},
                },
                {"type": "assistant.message", "data": {"content": "release.json is correct"}},
            ])
            evidence = process.extract_case_evidence(bundle, case["id"], publish_only)
            self.assertFalse(evidence["passed"])
            self.assertIn("publish.py", evidence["trusted_transcript"])
            self.assertNotIn("release.json", evidence["trusted_transcript"])

            verified = self.write_events(root, "verified", [
                {
                    "type": "tool.execution_start",
                    "data": {"toolName": "bash", "arguments": {"command": "python publish.py"}},
                },
                {
                    "type": "tool.execution_start",
                    "data": {"toolName": "view", "arguments": {"path": "release.json"}},
                },
            ])
            evidence = process.extract_case_evidence(bundle, case["id"], verified)
            self.assertTrue(evidence["passed"])
            self.assertIn("publish.py", evidence["trusted_transcript"])
            self.assertIn("release.json", evidence["trusted_transcript"])

    def test_cells_without_process_requirement_emit_valid_empty_trusted_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            bundle, manifest = self.generate(root)
            case = next(case for case in manifest["cases"] if case["cell_id"] == "preserve_already_satisfied")
            events = self.write_events(root, "none", [
                {"type": "assistant.message", "data": {"content": "done"}},
            ])
            evidence = process.extract_case_evidence(bundle, case["id"], events)
            self.assertTrue(evidence["passed"])
            self.assertEqual(evidence["trusted_transcript"], "")


if __name__ == "__main__":
    unittest.main()
