import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

import selection_validation as selection

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

    def test_probe_cell_requires_real_bash_probe_event_not_transcript_words(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            bundle, manifest = self.generate(root)
            case = next(
                case for case in manifest["cases"]
                if case["cell_id"] == "probe_resolvable_ambiguity" and case["replicate"] == 1
            )
            case_root = bundle / "cases" / case["id"]
            workspace = root / "probe-workspace"
            shutil.copytree(case_root / "visible" / "fixture", workspace)

            self_report_only = self.write_events(root, "self-report", [
                {"type": "assistant.message", "data": {"content": "I ran python probe.py"}},
            ])
            grade = selection.grade_case(
                case_root, workspace, "probe.py", events_path=self_report_only
            )
            self.assertFalse(grade["passed"])
            self.assertFalse(grade["checks"]["required_process_evidence"])

            executed = self.write_events(root, "executed", [
                {
                    "type": "tool.execution_start",
                    "data": {"toolName": "bash", "arguments": {"command": "python probe.py"}},
                },
            ])
            grade = selection.grade_case(case_root, workspace, "probe.py", events_path=executed)
            self.assertTrue(grade["passed"])

    def test_authoritative_state_cell_requires_post_publish_file_read_event(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            bundle, manifest = self.generate(root)
            case = next(case for case in manifest["cases"] if case["cell_id"] == "verify_authoritative_state")
            case_root = bundle / "cases" / case["id"]
            workspace = root / "verify-workspace"
            shutil.copytree(case_root / "visible" / "fixture", workspace)
            selection.run_reference(case_root, workspace)

            publish_only = self.write_events(root, "publish-only", [
                {
                    "type": "tool.execution_start",
                    "data": {"toolName": "bash", "arguments": {"command": "python publish.py"}},
                },
                {"type": "assistant.message", "data": {"content": "release.json is correct"}},
            ])
            grade = selection.grade_case(
                case_root,
                workspace,
                "publish.py release.json",
                events_path=publish_only,
            )
            self.assertFalse(grade["passed"])

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
            grade = selection.grade_case(
                case_root,
                workspace,
                "publish.py release.json",
                events_path=verified,
            )
            self.assertTrue(grade["passed"])


if __name__ == "__main__":
    unittest.main()
