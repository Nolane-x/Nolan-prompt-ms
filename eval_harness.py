#!/usr/bin/env python3
"""Small, model-agnostic utilities for Verified Delta behavioral evals."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HARNESS = pathlib.Path(__file__).resolve()
MANIFEST = ROOT / "evals" / "evals.json"
CASES = ROOT / "evals" / "cases"
SKILL = ROOT / "verified-delta" / "SKILL.md"
REQUIRED_METRICS = ("input_tokens", "output_tokens", "tool_calls", "wall_time_ms")
EFFECT_NAMES = ("same_fail", "same_pass", "u1_gain", "u1_harm")


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def find_case(case_id: str) -> dict:
    for case in load_manifest()["cases"]:
        if case["id"] == case_id:
            return case
    raise ValueError(f"unknown eval case: {case_id}")


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_tree(root: pathlib.Path) -> str:
    digest = hashlib.sha256()
    files = sorted(path for path in root.rglob("*") if path.is_file())
    for path in files:
        relative = path.relative_to(root).as_posix().encode("utf-8")
        content_digest = hashlib.sha256(path.read_bytes()).digest()
        digest.update(relative)
        digest.update(b"\0")
        digest.update(content_digest)
        digest.update(b"\0")
    return digest.hexdigest()


def validate_metrics(metrics: object) -> dict:
    if not isinstance(metrics, dict):
        raise ValueError("metrics must be a JSON object")
    missing = [name for name in REQUIRED_METRICS if name not in metrics]
    if missing:
        raise ValueError(f"metrics missing required fields: {', '.join(missing)}")
    for name in REQUIRED_METRICS:
        value = metrics[name]
        if value is None:
            continue
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"metrics field {name} must be null or a non-negative integer")
    return metrics


def validate_trial_identity(pair_id: str, replicate: int, model_id: str, harness_id: str) -> None:
    if not pair_id.strip():
        raise ValueError("trial pair_id must be non-empty")
    if replicate < 1:
        raise ValueError("trial replicate must be at least 1")
    if not model_id.strip():
        raise ValueError("trial model_id must be non-empty")
    if not harness_id.strip():
        raise ValueError("trial harness_id must be non-empty")


def load_receipt(path: pathlib.Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"receipt does not exist: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise ValueError(f"unsupported receipt schema: {path}")
    condition = payload.get("condition")
    if condition not in ("U0", "U1"):
        raise ValueError(f"invalid receipt condition in {path}")
    case_id = payload.get("case_id")
    pair_id = payload.get("pair_id")
    replicate = payload.get("replicate")
    model_id = payload.get("model_id")
    harness_id = payload.get("harness_id")
    if not isinstance(case_id, str) or not case_id.strip():
        raise ValueError(f"invalid receipt case_id in {path}")
    if not isinstance(pair_id, str) or isinstance(replicate, bool) or not isinstance(replicate, int):
        raise ValueError(f"invalid receipt trial identity in {path}")
    if not isinstance(model_id, str) or not isinstance(harness_id, str):
        raise ValueError(f"invalid receipt trial identity in {path}")
    validate_trial_identity(pair_id, replicate, model_id, harness_id)
    validate_metrics(payload.get("metrics"))
    grade = payload.get("grade")
    if not isinstance(grade, dict) or not isinstance(grade.get("passed"), bool):
        raise ValueError(f"invalid receipt grade in {path}")
    provenance = payload.get("eval_provenance")
    if not isinstance(provenance, dict):
        raise ValueError(f"invalid receipt eval_provenance in {path}")
    return payload


def classify_effect(u0_passed: bool, u1_passed: bool) -> str:
    if u0_passed and u1_passed:
        return "same_pass"
    if not u0_passed and not u1_passed:
        return "same_fail"
    if not u0_passed and u1_passed:
        return "u1_gain"
    return "u1_harm"


def paired_config_issues(replicate: int, u0: dict, u1: dict) -> list[str]:
    issues = []
    for field in ("model_id", "harness_id", "eval_provenance"):
        if u0[field] != u1[field]:
            issues.append(f"replicate {replicate} {field} mismatch")
    return issues


def run_grader(case_id: str, workspace: pathlib.Path) -> dict:
    find_case(case_id)
    grader = CASES / case_id / "grader.py"
    if not grader.is_file():
        raise FileNotFoundError(f"grader not implemented for case: {case_id}")
    if not workspace.is_dir():
        raise FileNotFoundError(f"workspace does not exist: {workspace}")

    result = subprocess.run(
        [sys.executable, str(grader), str(workspace.resolve())],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode not in (0, 1):
        detail = result.stderr.strip() or result.stdout.strip() or f"exit {result.returncode}"
        raise RuntimeError(f"grader infrastructure failure: {detail}")
    return json.loads(result.stdout)


def command_list(as_json: bool) -> int:
    manifest = load_manifest()
    payload = {
        "skill_name": manifest["skill_name"],
        "protocol": manifest["protocol"],
        "cases": manifest["cases"],
    }
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for case in payload["cases"]:
            print(f"{case['id']}: {case['prompt']}")
    return 0


def command_prepare(case_id: str, destination: pathlib.Path, as_json: bool) -> int:
    case = find_case(case_id)
    fixture = CASES / case_id / "fixture"
    if not fixture.is_dir():
        raise FileNotFoundError(f"fixture not implemented for case: {case_id}")
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")

    shutil.copytree(fixture, destination)
    payload = {
        "case_id": case_id,
        "workspace": str(destination.resolve()),
        "prompt": case["prompt"],
    }
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(case["prompt"])
    return 0


def command_grade(case_id: str, workspace: pathlib.Path, as_json: bool) -> int:
    payload = run_grader(case_id, workspace)
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print("PASS" if payload["passed"] else "FAIL")
        for name, passed in payload["checks"].items():
            print(f"- {name}: {'PASS' if passed else 'FAIL'}")
    return 0 if payload["passed"] else 1


def command_record(
    case_id: str,
    workspace: pathlib.Path,
    receipt_path: pathlib.Path,
    condition: str,
    pair_id: str,
    replicate: int,
    model_id: str,
    harness_id: str,
    transcript_path: pathlib.Path,
    metrics_path: pathlib.Path,
    as_json: bool,
) -> int:
    find_case(case_id)
    if receipt_path.exists():
        raise FileExistsError(f"receipt already exists: {receipt_path}")
    if not workspace.is_dir():
        raise FileNotFoundError(f"workspace does not exist: {workspace}")
    if not transcript_path.is_file():
        raise FileNotFoundError(f"transcript does not exist: {transcript_path}")
    if not metrics_path.is_file():
        raise FileNotFoundError(f"metrics do not exist: {metrics_path}")

    validate_trial_identity(pair_id, replicate, model_id, harness_id)
    if condition == "U0":
        skill = {"loaded": False, "sha256": None}
    elif condition == "U1":
        skill = {"loaded": True, "sha256": sha256_file(SKILL)}
    else:
        raise ValueError(f"unsupported condition: {condition}")

    metrics = validate_metrics(json.loads(metrics_path.read_text(encoding="utf-8")))
    case_root = CASES / case_id
    eval_provenance = {
        "harness_sha256": sha256_file(HARNESS),
        "manifest_sha256": sha256_file(MANIFEST),
        "fixture_sha256": sha256_tree(case_root / "fixture"),
        "grader_sha256": sha256_file(case_root / "grader.py"),
    }
    workspace_sha256 = sha256_tree(workspace)
    grade = run_grader(case_id, workspace)
    transcript_bytes = transcript_path.read_bytes()
    payload = {
        "schema_version": 1,
        "case_id": case_id,
        "condition": condition,
        "pair_id": pair_id,
        "replicate": replicate,
        "model_id": model_id,
        "harness_id": harness_id,
        "skill": skill,
        "eval_provenance": eval_provenance,
        "workspace_sha256": workspace_sha256,
        "transcript": {
            "sha256": hashlib.sha256(transcript_bytes).hexdigest(),
            "bytes": len(transcript_bytes),
        },
        "metrics": metrics,
        "grade": grade,
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(str(receipt_path.resolve()))
    return 0


def command_summarize(receipt_paths: list[pathlib.Path], as_json: bool) -> int:
    groups: dict[tuple[str, str], list[dict]] = {}
    for path in receipt_paths:
        receipt = load_receipt(path)
        key = (receipt["case_id"], receipt["pair_id"])
        groups.setdefault(key, []).append(receipt)

    pairs: list[dict] = []
    for (case_id, pair_id), receipts in sorted(groups.items()):
        by_replicate: dict[int, dict[str, dict]] = {}
        for receipt in receipts:
            by_replicate.setdefault(receipt["replicate"], {})[receipt["condition"]] = receipt

        issues: list[str] = []
        replicates: list[dict] = []
        counts = {name: 0 for name in EFFECT_NAMES}
        for replicate, conditions in sorted(by_replicate.items()):
            missing = [condition for condition in ("U0", "U1") if condition not in conditions]
            replicate_issues: list[str] = []
            if missing:
                replicate_issues.append(f"replicate {replicate} missing {'/'.join(missing)}")
            else:
                replicate_issues.extend(
                    paired_config_issues(replicate, conditions["U0"], conditions["U1"])
                )

            if replicate_issues:
                issues.extend(replicate_issues)
                effect = "not_comparable"
            else:
                effect = classify_effect(
                    conditions["U0"]["grade"]["passed"],
                    conditions["U1"]["grade"]["passed"],
                )
                counts[effect] += 1

            condition_summary = {
                condition: {
                    "passed": receipt["grade"]["passed"],
                    "metrics": receipt["metrics"],
                }
                for condition, receipt in sorted(conditions.items())
            }
            replicates.append(
                {
                    "replicate": replicate,
                    "effect": effect,
                    "conditions": condition_summary,
                }
            )

        pairs.append(
            {
                "case_id": case_id,
                "pair_id": pair_id,
                "comparable": not issues,
                "issues": issues,
                "counts": counts,
                "replicates": replicates,
            }
        )

    payload = {"schema_version": 1, "pairs": pairs}
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        for pair in pairs:
            status = "COMPARABLE" if pair["comparable"] else "NOT COMPARABLE"
            print(f"{pair['case_id']} / {pair['pair_id']}: {status}")
            for replicate in pair["replicates"]:
                print(f"- replicate {replicate['replicate']}: {replicate['effect']}")
            for issue in pair["issues"]:
                print(f"  issue: {issue}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="list preregistered eval cases")
    list_parser.add_argument("--json", action="store_true", dest="as_json")

    prepare_parser = subparsers.add_parser("prepare", help="copy one agent-visible fixture into a clean workspace")
    prepare_parser.add_argument("case_id")
    prepare_parser.add_argument("destination", type=pathlib.Path)
    prepare_parser.add_argument("--json", action="store_true", dest="as_json")

    grade_parser = subparsers.add_parser("grade", help="grade a completed workspace outside the agent context")
    grade_parser.add_argument("case_id")
    grade_parser.add_argument("workspace", type=pathlib.Path)
    grade_parser.add_argument("--json", action="store_true", dest="as_json")

    record_parser = subparsers.add_parser("record", help="write an auditable trial receipt after grading")
    record_parser.add_argument("case_id")
    record_parser.add_argument("workspace", type=pathlib.Path)
    record_parser.add_argument("receipt", type=pathlib.Path)
    record_parser.add_argument("--condition", required=True, choices=("U0", "U1"))
    record_parser.add_argument("--pair-id", required=True)
    record_parser.add_argument("--replicate", required=True, type=int)
    record_parser.add_argument("--model-id", required=True)
    record_parser.add_argument("--harness-id", required=True)
    record_parser.add_argument("--transcript", required=True, type=pathlib.Path)
    record_parser.add_argument("--metrics", required=True, type=pathlib.Path)
    record_parser.add_argument("--json", action="store_true", dest="as_json")

    summarize_parser = subparsers.add_parser(
        "summarize",
        help="summarize paired U0/U1 receipts without collapsing task-level effects",
    )
    summarize_parser.add_argument("receipts", nargs="+", type=pathlib.Path)
    summarize_parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "list":
            return command_list(args.as_json)
        if args.command == "prepare":
            return command_prepare(args.case_id, args.destination, args.as_json)
        if args.command == "grade":
            return command_grade(args.case_id, args.workspace, args.as_json)
        if args.command == "record":
            return command_record(
                args.case_id,
                args.workspace,
                args.receipt,
                args.condition,
                args.pair_id,
                args.replicate,
                args.model_id,
                args.harness_id,
                args.transcript,
                args.metrics,
                args.as_json,
            )
        if args.command == "summarize":
            return command_summarize(args.receipts, args.as_json)
        raise AssertionError(args.command)
    except (FileExistsError, FileNotFoundError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
