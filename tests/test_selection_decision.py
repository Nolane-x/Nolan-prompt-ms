import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOL = ROOT / "selection_receipts.py"


def pair(case_id, mode, effect, r1, r1a):
    return {
        "case_id": case_id,
        "mode": mode,
        "comparable": True,
        "effect": effect,
        "arms": {"R1": {"passed": r1}, "R1A": {"passed": r1a}},
    }


PASSING = [
    pair("config-noop", "noop", "candidate_gain", False, True),
    pair("config-required", "required", "same_pass", True, True),
    pair("writing-noop", "noop", "same_pass", True, True),
    pair("writing-required", "required", "same_pass", True, True),
    pair("data-noop", "noop", "same_pass", True, True),
    pair("data-required", "required", "same_pass", True, True),
]


class SelectionDecisionTests(unittest.TestCase):
    def decide(self, pairs):
        with tempfile.TemporaryDirectory() as tmp:
            source = pathlib.Path(tmp) / "summary.json"
            source.write_text(json.dumps({"schema_version": 1, "pairs": pairs}), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(TOOL), "decide", str(source), "--json"],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

    def test_passing_rule_advances(self):
        result = self.decide(PASSING)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["advance_to_hidden_holdout"])
        self.assertEqual(payload["candidate_pass_count"], 6)
        self.assertEqual(payload["required_action_candidate_harm_count"], 0)
        self.assertEqual(payload["noop_candidate_gain_count"], 1)

    def test_required_action_harm_stops(self):
        pairs = json.loads(json.dumps(PASSING))
        pairs[1] = pair("config-required", "required", "candidate_harm", True, False)
        result = self.decide(pairs)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(json.loads(result.stdout)["advance_to_hidden_holdout"])

    def test_missing_case_is_invalid_not_silently_failed(self):
        result = self.decide(PASSING[:-1])
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
