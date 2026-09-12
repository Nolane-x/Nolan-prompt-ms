#!/usr/bin/env python3
"""Execution-time utilities for frozen target-authority selection validation."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PLAN_PATH = ROOT / "evals" / "target-authority-selection-plan.json"
SKILL = ROOT / "verified-delta" / "SKILL.md"
CANDIDATE = ROOT / "evals" / "candidates" / "r1-target-authority.md"
EXPERIMENT = "target-authority-selection-validation-v1"
ARMS = ("R1", "R1A")
FAMILY_BY_CELL = {
    "preserve_already_satisfied": "api-config-contract",
    "act_defect_remains": "code-behavior",
    "preserve_outside_target_improvement": "config-state",
    "act_explicit_broader_requirement": "config-state",
    "probe_resolvable_ambiguity": "data-transformation",
    "verify_authoritative_state": "file-release",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: pathlib.Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_blob_sha1(path: pathlib.Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def load_plan() -> dict:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    if plan.get("schema_version") != 1:
        raise ValueError("selection plan schema_version must be 1")
    if plan.get("experiment") != EXPERIMENT:
        raise ValueError("unexpected selection experiment")
    if plan.get("status") != "preregistered-unexecuted":
        raise ValueError("selection plan must remain preregistered-unexecuted before execution")
    if plan.get("arms") != list(ARMS):
        raise ValueError("selection plan arms drifted")
    if plan.get("replicates_per_cell") != 2:
        raise ValueError("selection plan replicate count drifted")
    if plan.get("fixed_model_trial_budget") != 24:
        raise ValueError("selection plan model-trial budget drifted")

    expected_blobs = {
        "R1": git_blob_sha1(SKILL),
        "R1A": git_blob_sha1(CANDIDATE),
    }
    for arm, observed in expected_blobs.items():
        frozen = plan["treatments"][arm]["git_blob"]
        if observed != frozen:
            raise ValueError(f"{arm} treatment blob drifted: expected {frozen}, observed {observed}")

    cell_ids = [cell["id"] for cell in plan["semantic_cells"]]
    if set(cell_ids) != set(FAMILY_BY_CELL) or len(cell_ids) != 6:
        raise ValueError("selection plan semantic cells drifted")
    return plan


def stable_case_id(seed: str, cell_id: str, replicate: int) -> str:
    digest = hashlib.sha256(f"{seed}\0{cell_id}\0{replicate}".encode("utf-8")).hexdigest()[:16]
    return f"{cell_id}-r{replicate}-{digest}"


def build_manifest(seed: str, plan: dict) -> dict:
    cases = []
    for cell in plan["semantic_cells"]:
        cell_id = cell["id"]
        family = FAMILY_BY_CELL[cell_id]
        for replicate in range(1, plan["replicates_per_cell"] + 1):
            case_id = stable_case_id(seed, cell_id, replicate)
            cases.append(
                {
                    "id": case_id,
                    "cell_id": cell_id,
                    "role": cell["role"],
                    "family": family,
                    "replicate": replicate,
                    "pair_id": f"{cell_id}-r{replicate}",
                }
            )

    if len(cases) != 12:
        raise ValueError("generator must create exactly 12 cases")
    families = {case["family"] for case in cases}
    minimum_families = plan["task_family_constraints"]["minimum_distinct_families"]
    if len(families) < minimum_families:
        raise ValueError("generated cases do not satisfy minimum family coverage")
    allowed = set(plan["task_family_constraints"]["allowed_families"])
    if not families.issubset(allowed):
        raise ValueError("generated cases contain a disallowed task family")

    return {
        "schema_version": 1,
        "experiment": EXPERIMENT,
        "evidence_class": plan["evidence_class"],
        "seed": seed,
        "plan_sha256": sha256_file(PLAN_PATH),
        "treatments": {
            arm: {
                "git_blob": plan["treatments"][arm]["git_blob"],
                "content_sha256": sha256_file(SKILL if arm == "R1" else CANDIDATE),
            }
            for arm in ARMS
        },
        "cases": cases,
    }


def command_generate(seed: str, output: pathlib.Path, as_json: bool) -> int:
    if not seed.strip():
        raise ValueError("execution seed must be non-empty")
    if output.exists():
        raise FileExistsError(f"output already exists: {output}")

    plan = load_plan()
    manifest = build_manifest(seed, plan)
    output.mkdir(parents=True)
    (output / "bundle.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    matrix = {
        "include": [
            {"case_id": case["id"], "arm": arm}
            for case in manifest["cases"]
            for arm in ARMS
        ]
    }
    payload = {
        "bundle": str(output.resolve()),
        "seed": seed,
        "case_count": len(manifest["cases"]),
        "matrix": matrix,
    }
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(str(output.resolve()))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate")
    generate.add_argument("--seed", required=True)
    generate.add_argument("--output", type=pathlib.Path, required=True)
    generate.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "generate":
            return command_generate(args.seed, args.output, args.json)
        raise ValueError(f"unsupported command: {args.command}")
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
