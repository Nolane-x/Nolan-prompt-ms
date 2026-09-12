#!/usr/bin/env python3
"""Researcher-side recorder and summarizer for R1 vs target-authority ablation."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

import eval_harness as base

ROOT = pathlib.Path(__file__).resolve().parent
HARNESS = pathlib.Path(__file__).resolve()
SKILL = ROOT / "verified-delta" / "SKILL.md"
CANDIDATE = ROOT / "evals" / "candidates" / "r1-target-authority.md"
EXPERIMENT = "target-authority-ablation-v1"
ARMS = ("R1", "R1A")
EFFECT_NAMES = ("same_fail", "same_pass", "candidate_gain", "candidate_harm")


def treatment_path(arm: str) -> pathlib.Path:
    if arm == "R1":
        return SKILL
    if arm == "R1A":
        return CANDIDATE
    raise ValueError(f"unsupported ablation arm: {arm}")


def treatment_sha256s() -> dict[str, str]:
    return {arm: base.sha256_file(treatment_path(arm)) for arm in ARMS}


def treatment_set_sha256() -> str:
    return base.canonical_sha256(treatment_sha256s())


def expected_intervention(arm: str) -> dict[str, object]:
    loaded_sha = base.sha256_file(treatment_path(arm))
    return {
        "delivery_form": "force-loaded-incumbent" if arm == "R1" else "force-loaded-candidate",
        "metadata_language": "en",
        "body_language": "en",
        "description_variant": "r1" if arm == "R1" else "r1-target-authority",
        "available_skill_set_sha256": loaded_sha,
    }


def validate_run_config_binding(run_config: dict, arm: str, model_id: str, harness_id: str) -> None:
    value = run_config["value"]
    matched = value["matched"]
    if matched["model"]["id"] != model_id:
        raise ValueError("run config matched.model.id does not match --model-id")
    if matched["harness"]["id"] != harness_id:
        raise ValueError("run config matched.harness.id does not match --harness-id")
    expected = expected_intervention(arm)
    if value["intervention"] != expected:
        raise ValueError(f"run config intervention does not match {arm} treatment")


def eval_provenance(case_id: str) -> dict[str, str]:
    case_root = base.CASES / case_id
    return {
        "semantic_ablation_sha256": base.sha256_file(HARNESS),
        "eval_harness_sha256": base.sha256_file(base.HARNESS),
        "manifest_sha256": base.sha256_file(base.MANIFEST),
        "fixture_sha256": base.sha256_tree(case_root / "fixture"),
        "grader_sha256": base.sha256_file(case_root / "grader.py"),
    }


def command_record(
    case_id: str,
    workspace: pathlib.Path,
    receipt_path: pathlib.Path,
    arm: str,
    pair_id: str,
    replicate: int,
    model_id: str,
    harness_id: str,
    transcript_path: pathlib.Path,
    metrics_path: pathlib.Path,
    run_config_path: pathlib.Path,
    as_json: bool,
) -> int:
    base.find_case(case_id)
    treatment_path(arm)
    if receipt_path.exists():
        raise FileExistsError(f"receipt already exists: {receipt_path}")
    if not workspace.is_dir():
        raise FileNotFoundError(f"workspace does not exist: {workspace}")
    if not transcript_path.is_file():
        raise FileNotFoundError(f"transcript does not exist: {transcript_path}")
    if not metrics_path.is_file():
        raise FileNotFoundError(f"metrics do not exist: {metrics_path}")

    base.validate_trial_identity(pair_id, replicate, model_id, harness_id)
    metrics = base.validate_metrics(json.loads(metrics_path.read_text(encoding="utf-8")))
    run_config = base.load_run_config(run_config_path)
    validate_run_config_binding(run_config, arm, model_id, harness_id)

    treatment_shas = treatment_sha256s()
    transcript_bytes = transcript_path.read_bytes()
    payload = {
        "schema_version": 1,
        "experiment": EXPERIMENT,
        "case_id": case_id,
        "arm": arm,
        "pair_id": pair_id,
        "replicate": replicate,
        "model_id": model_id,
        "harness_id": harness_id,
        "treatment": {
            "loaded_sha256": treatment_shas[arm],
            "treatment_sha256s": treatment_shas,
            "treatment_set_sha256": treatment_set_sha256(),
        },
        "eval_provenance": eval_provenance(case_id),
        "workspace_sha256": base.sha256_tree(workspace),
        "transcript": {
            "sha256": hashlib.sha256(transcript_bytes).hexdigest(),
            "bytes": len(transcript_bytes),
        },
        "metrics": metrics,
        "grade": base.run_grader(case_id, workspace),
        "run_config": run_config,
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


def load_receipt(path: pathlib.Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"receipt does not exist: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise ValueError(f"unsupported receipt schema: {path}")
    if payload.get("experiment") != EXPERIMENT:
        raise ValueError(f"unexpected ablation experiment in {path}")
    arm = payload.get("arm")
    if arm not in ARMS:
        raise ValueError(f"invalid ablation arm in {path}")

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
    base.validate_trial_identity(pair_id, replicate, model_id, harness_id)
    base.validate_metrics(payload.get("metrics"))

    grade = payload.get("grade")
    if not isinstance(grade, dict) or not isinstance(grade.get("passed"), bool):
        raise ValueError(f"invalid receipt grade in {path}")
    if payload.get("eval_provenance") != eval_provenance(case_id):
        raise ValueError(f"eval provenance mismatch in {path}")

    treatment = payload.get("treatment")
    expected_shas = treatment_sha256s()
    if not isinstance(treatment, dict):
        raise ValueError(f"invalid treatment provenance in {path}")
    if treatment.get("loaded_sha256") != expected_shas[arm]:
        raise ValueError(f"loaded treatment SHA-256 mismatch in {path}")
    if treatment.get("treatment_sha256s") != expected_shas:
        raise ValueError(f"treatment-set members mismatch in {path}")
    if treatment.get("treatment_set_sha256") != treatment_set_sha256():
        raise ValueError(f"treatment-set SHA-256 mismatch in {path}")

    run_config_raw = payload.get("run_config")
    if not isinstance(run_config_raw, dict):
        raise ValueError(f"invalid receipt run config in {path}")
    value = base.validate_run_config(run_config_raw.get("value"))
    run_config = {
        "value": value,
        "sha256": base.canonical_sha256(value),
        "matched_sha256": base.canonical_sha256(value["matched"]),
    }
    if run_config_raw.get("sha256") != run_config["sha256"]:
        raise ValueError(f"run config SHA-256 mismatch in receipt: {path}")
    if run_config_raw.get("matched_sha256") != run_config["matched_sha256"]:
        raise ValueError(f"run config matched SHA-256 mismatch in receipt: {path}")
    validate_run_config_binding(run_config, arm, model_id, harness_id)
    payload["run_config"] = run_config
    return payload


def classify_effect(r1_passed: bool, candidate_passed: bool) -> str:
    if r1_passed and candidate_passed:
        return "same_pass"
    if not r1_passed and not candidate_passed:
        return "same_fail"
    if not r1_passed and candidate_passed:
        return "candidate_gain"
    return "candidate_harm"


def paired_issues(replicate: int, r1: dict, r1a: dict) -> list[str]:
    issues = []
    for field in ("model_id", "harness_id", "eval_provenance"):
        if r1[field] != r1a[field]:
            issues.append(f"replicate {replicate} {field} mismatch")
    if r1["treatment"]["treatment_set_sha256"] != r1a["treatment"]["treatment_set_sha256"]:
        issues.append(f"replicate {replicate} treatment set mismatch")
    if r1["run_config"]["matched_sha256"] != r1a["run_config"]["matched_sha256"]:
        issues.append(f"replicate {replicate} matched run config mismatch")
    return issues


def command_summarize(receipt_paths: list[pathlib.Path], as_json: bool) -> int:
    groups: dict[tuple[str, str], list[dict]] = {}
    for path in receipt_paths:
        receipt = load_receipt(path)
        key = (receipt["case_id"], receipt["pair_id"])
        groups.setdefault(key, []).append(receipt)

    pairs = []
    for (case_id, pair_id), receipts in sorted(groups.items()):
        by_replicate: dict[int, dict[str, dict]] = {}
        duplicate_issues: dict[int, list[str]] = {}
        for receipt in receipts:
            replicate = receipt["replicate"]
            arm = receipt["arm"]
            arms = by_replicate.setdefault(replicate, {})
            if arm in arms:
                duplicate_issues.setdefault(replicate, []).append(
                    f"replicate {replicate} duplicate {arm} receipt"
                )
                continue
            arms[arm] = receipt

        issues = []
        replicates = []
        counts = {name: 0 for name in EFFECT_NAMES}
        for replicate, arms in sorted(by_replicate.items()):
            missing = [arm for arm in ARMS if arm not in arms]
            replicate_issues = list(duplicate_issues.get(replicate, []))
            if missing:
                replicate_issues.append(f"replicate {replicate} missing {'/'.join(missing)}")
            else:
                replicate_issues.extend(paired_issues(replicate, arms["R1"], arms["R1A"]))

            if replicate_issues:
                issues.extend(replicate_issues)
                effect = "not_comparable"
            else:
                effect = classify_effect(
                    arms["R1"]["grade"]["passed"],
                    arms["R1A"]["grade"]["passed"],
                )
                counts[effect] += 1

            arm_summary = {
                arm: {
                    "passed": receipt["grade"]["passed"],
                    "metrics": receipt["metrics"],
                }
                for arm, receipt in sorted(arms.items())
            }
            replicates.append(
                {
                    "replicate": replicate,
                    "effect": effect,
                    "arms": arm_summary,
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

    payload = {"schema_version": 1, "experiment": EXPERIMENT, "pairs": pairs}
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

    record = subparsers.add_parser("record")
    record.add_argument("case_id")
    record.add_argument("workspace", type=pathlib.Path)
    record.add_argument("receipt", type=pathlib.Path)
    record.add_argument("--arm", choices=ARMS, required=True)
    record.add_argument("--pair-id", required=True)
    record.add_argument("--replicate", type=int, required=True)
    record.add_argument("--model-id", required=True)
    record.add_argument("--harness-id", required=True)
    record.add_argument("--transcript", type=pathlib.Path, required=True)
    record.add_argument("--metrics", type=pathlib.Path, required=True)
    record.add_argument("--run-config", type=pathlib.Path, required=True)
    record.add_argument("--json", action="store_true", dest="as_json")

    summarize = subparsers.add_parser("summarize")
    summarize.add_argument("receipts", nargs="+", type=pathlib.Path)
    summarize.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "record":
            return command_record(
                args.case_id,
                args.workspace,
                args.receipt,
                args.arm,
                args.pair_id,
                args.replicate,
                args.model_id,
                args.harness_id,
                args.transcript,
                args.metrics,
                args.run_config,
                args.as_json,
            )
        return command_summarize(args.receipts, args.as_json)
    except (FileExistsError, FileNotFoundError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
