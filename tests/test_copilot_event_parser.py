import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PARSER = ROOT / "copilot_event_parser.py"


class CopilotEventParserTests(unittest.TestCase):
    def run_parser(self, events):
        with tempfile.TemporaryDirectory() as tmp:
            source = pathlib.Path(tmp) / "events.jsonl"
            source.write_text(
                "".join(json.dumps(event) + "\n" for event in events),
                encoding="utf-8",
            )
            return subprocess.run(
                [sys.executable, str(PARSER), "resolve-model", str(source), "--json"],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

    def test_resolve_model_binds_auto_choice_to_response_model(self):
        result = self.run_parser(
            [
                {
                    "type": "session.auto_mode_resolved",
                    "data": {"chosenModel": "gpt-5.6-luna"},
                },
                {
                    "type": "assistant.message",
                    "data": {"model": "gpt-5.6-luna", "content": "OK"},
                },
            ]
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"model": "gpt-5.6-luna"})

    def test_resolve_model_rejects_conflicting_model_evidence(self):
        result = self.run_parser(
            [
                {
                    "type": "session.auto_mode_resolved",
                    "data": {"chosenModel": "gpt-5.6-luna"},
                },
                {
                    "type": "assistant.message",
                    "data": {"model": "different-model", "content": "OK"},
                },
            ]
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_resolve_model_accepts_named_model_response_without_auto_event(self):
        result = self.run_parser(
            [
                {
                    "type": "assistant.message",
                    "data": {"model": "named-model", "content": "OK"},
                }
            ]
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"model": "named-model"})


if __name__ == "__main__":
    unittest.main()
