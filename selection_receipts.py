#!/usr/bin/env python3
"""Receipt utilities and fail-closed decision rule for selection validation."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PLAN = ROOT / "evals" / "selection-validation-plan.json"
ARMS = ("R1", "R1A")
EFFECTS = {"same_pass", "same_fail", "candidate_gain", "candidate_harm"}


def load_json(path: pathlib.Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def expected_effect(r1_passed: bool, candidate_passed: bool) -> str:
    if r1_passed and candidate_passed:
        return "same_pass"
    if not r1_passed and not candidate_passed:
        return "same_fail"
    if not r1_passed and candidate_passed:
        return "candidate_gain"
    return "candidate_harm"


def expected_mode(case_id: str) -> str:
    if case_id.endswith("-noop"):
        return "noop"
    if case_id.endswith("-required"):
        return "required"
    raise ValueError(f"case id does not encode frozen mode: {case_id}")


def validate_plan() -> dict:
    plan = load_json(PLAN)
    if plan.get("schema_version") != 1:
        raise ValueError("unsupported selection plan schema")
    case_keys = plan.get("case_keys")
    if not isinstance(case_keys, list) or len(case_keys) != len(set(case_keys)) or not case_keys:
        raise ValueError("selection plan case_keys are invalid")
    rule = plan.get("decision_rule")
    if not isinstance(rule, dict):
        raise ValueError("selection plan decision_rule is invalid")
    for field in (
        "required_action_candidate_harm_max",
        "candidate_pass_min",
        "noop_candidate_gain_min",
        "on_failure",
        "on_pass",
    ):
        if field not in rule:
            raise ValueError(f"selection plan decision_rule missing {field}")
    return plan


def validate_pair(pair: object, expected_cases: set[str]) -> dict:
    if not isinstance(pair, dict):
        raise ValueError("selection summary pair must be an object")
    case_id = pair.get("case_id")
    if not isinstance(case_id, str) or case_id not in expected_cases:
        raise ValueError(f"unexpected selection case: {case_id!r}")
    mode = pair.get("mode")
    if mode != expected_mode(case_id):
        raise ValueError(f"selection case mode mismatch: {case_id}")
    if pair.get("comparable") is not True:
        raise ValueError(f"selection pair is not comparable: {case_id}")
    effect = pair.get("effect")
    if effect not in EFFECTS:
        raise ValueError(f"invalid selection effect: {case_id}")
    arms = pair.get("arms")
    if not isinstance(arms, dict) or set(arms) != set(ARMS):
        raise ValueError(f"selection arms mismatch: {case_id}")
    passed = {}
    for arm in ARMS:
        value = arms[arm]
        if not isinstance(value, dict) or not isinstance(value.get("passed"), bool):
            raise ValueError(f"invalid {arm} grade: {case_id}")
        passed[arm] = value["passed"]
    if effect != expected_effect(passed["R1"], passed["R1A"]):
        raise ValueError(f"selection effect contradicts grades: {case_id}")
    return {
        "case_id": case_id,
        "mode": mode,
        "effect": effect,
        "r1_passed": passed["R1"],
        "candidate_passed": passed["R1A"],
    }


def command_decide(summary_path: pathlib.Path, as_json: bool) -> int:
    plan = validate_plan()
    summary = load_json(summary_path)
    if summary.get("schema_version") != 1:
        raise ValueError("unsupported selection summary schema")
    pairs = summary.get("pairs")
    if not isinstance(pairs, list):
        raise ValueError("selection summary pairs must be a list")

    expected_cases = set(plan["case_keys"])
    validated = [validate_pair(pair, expected_cases) for pair in pairs]
    case_ids = [pair["case_id"] for pair in validated]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("selection summary contains duplicate cases")
    if set(case_ids) != expected_cases:
        missing = sorted(expected_cases - set(case_ids))
        extra = sorted(set(case_ids) - expected_cases)
        raise ValueError(f"selection summary case set mismatch; missing={missing}, extra={extra}")

    candidate_pass_count = sum(pair["candidate_passed"] for pair in validated)
    required_harm_count = sum(
        pair["mode"] == "required" and pair["effect"] == "candidate_harm"
        for pair in validated
    )
    noop_gain_count = sum(
        pair["mode"] == "noop" and pair["effect"] == "candidate_gain"
        for pair in validated
    )

    rule = plan["decision_rule"]
    advance = (
        candidate_pass_count >= rule["candidate_pass_min"]
        and required_harm_count <= rule["required_action_candidate_harm_max"]
        and noop_gain_count >= rule["noop_candidate_gain_min"]
    )
    payload = {
        "schema_version": 1,
        "advance_to_hidden_holdout": advance,
        "case_count": len(validated),
        "candidate_pass_count": candidate_pass_count,
        "required_action_candidate_harm_count": required_harm_count,
        "noop_candidate_gain_count": noop_gain_count,
        "disposition": rule["on_pass"] if advance else rule["on_failure"],
    }
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(payload["disposition"])
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    decide = sub.add_parser("decide")
    decide.add_argument("summary", type=pathlib.Path)
    decide.add_argument("--json", action="store_true")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return command_decide(args.summary, args.json)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
