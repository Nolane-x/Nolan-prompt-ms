import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PARSER = ROOT / "copilot_event_parser.py"


class CopilotEventParserTests(unittest.TestCase):
    def run_parser(self, events, command="resolve-model"):
        with tempfile.TemporaryDirectory() as tmp:
            source = pathlib.Path(tmp) / "events.jsonl"
            source.write_text(
                "".join(json.dumps(event) + "\n" for event in events),
                encoding="utf-8",
            )
            return subprocess.run(
                [sys.executable, str(PARSER), command, str(source), "--json"],
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

    def test_attest_runtime_reports_actual_effort_and_tool_calls(self):
        result = self.run_parser(
            [
                {
                    "type": "assistant.message",
                    "data": {"model": "mai-code-1.1-flash", "content": ""},
                },
                {"type": "tool.execution_start", "data": {"toolName": "view"}},
                {"type": "tool.execution_start", "data": {"toolName": "bash"}},
                {
                    "type": "session.usage_checkpoint",
                    "data": {
                        "promptCacheBreakState": [
                            {
                                "models": {
                                    "m": {
                                        "model": "mai-code-1.1-flash",
                                        "reasoning_effort": "medium",
                                    }
                                }
                            }
                        ]
                    },
                },
            ],
            command="attest-runtime",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {
                "model": "mai-code-1.1-flash",
                "reasoning_effort": "medium",
                "tool_calls": 2,
            },
        )

    def test_attest_runtime_rejects_conflicting_reasoning_evidence(self):
        result = self.run_parser(
            [
                {"type": "assistant.message", "data": {"model": "named-model", "content": ""}},
                {
                    "type": "session.usage_checkpoint",
                    "data": {
                        "promptCacheBreakState": [
                            {
                                "models": {
                                    "first": {
                                        "model": "named-model",
                                        "reasoning_effort": "medium",
                                    },
                                    "second": {
                                        "model": "named-model",
                                        "reasoning_effort": "high",
                                    },
                                }
                            }
                        ]
                    },
                },
            ],
            command="attest-runtime",
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
