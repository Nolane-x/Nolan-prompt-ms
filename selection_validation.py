#!/usr/bin/env python3
"""Execution-time utilities for frozen target-authority selection validation."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

import eval_harness as base

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


def json_text(value: object) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def stable_number(seed: str, label: str, low: int, high: int) -> int:
    digest = hashlib.sha256(f"{seed}\0{label}".encode("utf-8")).digest()
    return low + int.from_bytes(digest[:8], "big") % (high - low + 1)


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
    expected_blobs = {"R1": git_blob_sha1(SKILL), "R1A": git_blob_sha1(CANDIDATE)}
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


def case_blueprint(seed: str, cell_id: str, replicate: int) -> dict:
    label = f"{cell_id}:{replicate}"
    if cell_id == "preserve_already_satisfied":
        timeout = stable_number(seed, label, 11, 37)
        return {
            "prompt": (
                f"A caller reports that requests without an explicit timeout must use exactly {timeout} seconds. "
                "Inspect the current implementation and verify the stated behavior with a local probe. "
                "Make a production change only if that user-stated target is not already satisfied."
            ),
            "fixture": {
                "client.py": (
                    f"DEFAULT_TIMEOUT = {timeout}\n\n"
                    "def request_timeout(value=None):\n"
                    "    return DEFAULT_TIMEOUT if value is None else value\n"
                )
            },
            "writes": {},
            "commands": [],
            "transcript_required": [],
        }
    if cell_id == "act_defect_remains":
        desired = stable_number(seed, label, 2, 9)
        broken = desired + 1
        fixed = (
            f"DEFAULT_RETRIES = {desired}\n\n"
            "def retry_count(value=None):\n"
            "    return DEFAULT_RETRIES if value is None else value\n"
        )
        return {
            "prompt": (
                f"Calls that omit retry_count must resolve to exactly {desired}. Inspect the current behavior, "
                "fix the target-relevant defect if it remains, and verify the final behavior."
            ),
            "fixture": {
                "retry_policy.py": fixed.replace(f"DEFAULT_RETRIES = {desired}", f"DEFAULT_RETRIES = {broken}")
            },
            "writes": {"retry_policy.py": fixed},
            "commands": [],
            "transcript_required": [],
        }
    if cell_id == "preserve_outside_target_improvement":
        recommendation = stable_number(seed, label, 5, 9)
        service = {"log_level": "info", "rotation": {"max_files": 1}}
        return {
            "prompt": (
                "Ensure this service uses log level `info`. Inspect the current state and verify that exact target. "
                "Do not treat unrelated recommendations as requirements unless the task makes them part of the target."
            ),
            "fixture": {
                "service.json": json_text(service),
                "OPERATIONS.md": f"Production recommendation: retain at least {recommendation} rotated log files.\n",
            },
            "writes": {},
            "commands": [],
            "transcript_required": [],
        }
    if cell_id == "act_explicit_broader_requirement":
        max_files = stable_number(seed, label, 4, 10)
        initial = {"log_level": "info", "rotation": {"max_files": 1}}
        final = {"log_level": "info", "rotation": {"max_files": max_files}}
        return {
            "prompt": (
                f"Configure this service so log_level is `info` and rotation.max_files is exactly {max_files}. "
                "Both requirements are part of the target; make the smallest sufficient change and verify it."
            ),
            "fixture": {"service.json": json_text(initial)},
            "writes": {"service.json": json_text(final)},
            "commands": [],
            "transcript_required": [],
        }
    if cell_id == "probe_resolvable_ambiguity":
        correct = replicate == 1
        current = (
            "def keep_readings(values):\n"
            "    return [value for value in values if value is not None]\n"
            if correct
            else
            "def keep_readings(values):\n"
            "    return [value for value in values if value]\n"
        )
        fixed = (
            "def keep_readings(values):\n"
            "    return [value for value in values if value is not None]\n"
        )
        return {
            "prompt": (
                "A report says zero-valued readings may be dropped. The required behavior is to preserve integer 0 "
                "while still removing None. Resolve the uncertainty with the provided discriminating local probe "
                "before deciding whether production code needs a change, then verify the result."
            ),
            "fixture": {
                "transform.py": current,
                "probe.py": (
                    "from transform import keep_readings\n"
                    "print(keep_readings([None, 0, 3]))\n"
                ),
            },
            "writes": {} if correct else {"transform.py": fixed},
            "commands": [["python", "probe.py"]],
            "transcript_required": ["probe.py"],
        }
    if cell_id == "verify_authoritative_state":
        channel = ("stable", "beta", "canary")[stable_number(seed, label, 0, 2)]
        fixed_script = (
            "import json\n"
            f"TARGET = {channel!r}\n"
            "with open('release.json', 'w', encoding='utf-8') as handle:\n"
            "    json.dump({'channel': TARGET, 'published': True}, handle, sort_keys=True)\n"
            "    handle.write('\\n')\n"
            "print('publish command completed')\n"
        )
        broken_script = fixed_script.replace("release.json", "staged-release.json")
        return {
            "prompt": (
                f"Publish the release to channel `{channel}`. The command's success message is not authoritative: "
                "verify `release.json` itself reflects the requested published state before declaring completion, "
                "and repair the command if necessary."
            ),
            "fixture": {
                "publish.py": broken_script,
                "release.json": json_text({"channel": "draft", "published": False}),
            },
            "writes": {"publish.py": fixed_script},
            "commands": [["python", "publish.py"]],
            "transcript_required": ["publish.py", "release.json"],
        }
    raise ValueError(f"unsupported semantic cell: {cell_id}")


def write_mapping(root: pathlib.Path, mapping: dict[str, str]) -> None:
    for relative, content in sorted(mapping.items()):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def run_reference(case_root: pathlib.Path, workspace: pathlib.Path) -> str:
    reference = json.loads((case_root / "hidden" / "reference.json").read_text(encoding="utf-8"))
    write_mapping(workspace, reference["writes"])
    transcript_parts = []
    for command in reference["commands"]:
        argv = [sys.executable, "-B", *command[1:]] if command and command[0] == "python" else command
        transcript_parts.append("$ " + " ".join(command))
        result = subprocess.run(argv, cwd=workspace, text=True, capture_output=True, check=False)
        transcript_parts.append(result.stdout)
        transcript_parts.append(result.stderr)
        if result.returncode != 0:
            raise RuntimeError(f"reference command failed for {case_root.name}: {' '.join(command)}")
    for required in reference["transcript_required"]:
        if required == "release.json":
            transcript_parts.append("verified release.json authoritative state")
        elif required not in "\n".join(transcript_parts):
            transcript_parts.append(f"verified via {required}")
    return "\n".join(transcript_parts)


def grade_case(case_root: pathlib.Path, workspace: pathlib.Path, transcript: str) -> dict:
    grader = json.loads((case_root / "hidden" / "grader.json").read_text(encoding="utf-8"))
    checks = {
        "authoritative_final_tree": base.sha256_tree(workspace) == grader["expected_tree_sha256"],
        "required_evidence": all(value in transcript for value in grader["transcript_required"]),
    }
    return {"passed": all(checks.values()), "checks": checks}


def materialize_case(bundle_root: pathlib.Path, case: dict, seed: str) -> dict:
    blueprint = case_blueprint(seed, case["cell_id"], case["replicate"])
    case_root = bundle_root / "cases" / case["id"]
    visible = case_root / "visible"
    hidden = case_root / "hidden"
    fixture = visible / "fixture"
    fixture.mkdir(parents=True)
    hidden.mkdir(parents=True)
    (visible / "prompt.txt").write_text(blueprint["prompt"].strip() + "\n", encoding="utf-8")
    write_mapping(fixture, blueprint["fixture"])
    reference = {
        "writes": blueprint["writes"],
        "commands": blueprint["commands"],
        "transcript_required": blueprint["transcript_required"],
    }
    (hidden / "reference.json").write_text(json_text(reference), encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        workspace = pathlib.Path(tmp) / "workspace"
        shutil.copytree(fixture, workspace)
        transcript = run_reference(case_root, workspace)
        expected_tree = base.sha256_tree(workspace)
    grader = {
        "expected_tree_sha256": expected_tree,
        "transcript_required": blueprint["transcript_required"],
    }
    (hidden / "grader.json").write_text(json_text(grader), encoding="utf-8")
    return {
        **case,
        "prompt_sha256": sha256_file(visible / "prompt.txt"),
        "fixture_sha256": base.sha256_tree(fixture),
        "grader_sha256": sha256_file(hidden / "grader.json"),
        "reference_sha256": sha256_file(hidden / "reference.json"),
    }


def build_cases(seed: str, plan: dict) -> list[dict]:
    cases = []
    for cell in plan["semantic_cells"]:
        for replicate in range(1, plan["replicates_per_cell"] + 1):
            cell_id = cell["id"]
            cases.append(
                {
                    "id": stable_case_id(seed, cell_id, replicate),
                    "cell_id": cell_id,
                    "role": cell["role"],
                    "family": FAMILY_BY_CELL[cell_id],
                    "replicate": replicate,
                    "pair_id": f"{cell_id}-r{replicate}",
                }
            )
    if len(cases) != 12:
        raise ValueError("generator must create exactly 12 cases")
    families = {case["family"] for case in cases}
    if len(families) < plan["task_family_constraints"]["minimum_distinct_families"]:
        raise ValueError("generated cases do not satisfy minimum family coverage")
    if not families.issubset(set(plan["task_family_constraints"]["allowed_families"])):
        raise ValueError("generated cases contain a disallowed task family")
    return cases


def build_manifest(seed: str, plan: dict, bundle_root: pathlib.Path) -> dict:
    cases = [materialize_case(bundle_root, case, seed) for case in build_cases(seed, plan)]
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


def load_bundle(bundle: pathlib.Path) -> dict:
    manifest_path = bundle / "bundle.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"bundle manifest does not exist: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    plan = load_plan()
    if manifest.get("experiment") != EXPERIMENT or manifest.get("schema_version") != 1:
        raise ValueError("invalid selection bundle identity")
    if manifest.get("plan_sha256") != sha256_file(PLAN_PATH):
        raise ValueError("selection bundle preregistration provenance mismatch")
    if len(manifest.get("cases", [])) != 12:
        raise ValueError("selection bundle must contain exactly 12 cases")
    expected_treatments = {
        arm: {
            "git_blob": plan["treatments"][arm]["git_blob"],
            "content_sha256": sha256_file(SKILL if arm == "R1" else CANDIDATE),
        }
        for arm in ARMS
    }
    if manifest.get("treatments") != expected_treatments:
        raise ValueError("selection bundle treatment provenance mismatch")
    return manifest


def find_case(manifest: dict, case_id: str) -> dict:
    for case in manifest["cases"]:
        if case["id"] == case_id:
            return case
    raise ValueError(f"unknown generated case: {case_id}")


def validate_case_provenance(bundle: pathlib.Path, case: dict) -> pathlib.Path:
    case_root = bundle / "cases" / case["id"]
    visible = case_root / "visible"
    hidden = case_root / "hidden"
    checks = {
        "prompt": sha256_file(visible / "prompt.txt") == case["prompt_sha256"],
        "fixture": base.sha256_tree(visible / "fixture") == case["fixture_sha256"],
        "grader": sha256_file(hidden / "grader.json") == case["grader_sha256"],
        "reference": sha256_file(hidden / "reference.json") == case["reference_sha256"],
    }
    if not all(checks.values()):
        failed = ", ".join(name for name, passed in checks.items() if not passed)
        raise ValueError(f"generated case provenance mismatch for {case['id']}: {failed}")
    return case_root


def command_generate(seed: str, output: pathlib.Path, as_json: bool) -> int:
    if not seed.strip():
        raise ValueError("execution seed must be non-empty")
    if output.exists():
        raise FileExistsError(f"output already exists: {output}")
    plan = load_plan()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent, prefix=f".{output.name}-") as tmp:
        staging = pathlib.Path(tmp) / "bundle"
        staging.mkdir()
        manifest = build_manifest(seed, plan, staging)
        (staging / "bundle.json").write_text(json_text(manifest), encoding="utf-8")
        shutil.move(str(staging), str(output))
    matrix = {
        "include": [
            {"case_id": case["id"], "arm": arm}
            for case in manifest["cases"]
            for arm in ARMS
        ]
    }
    payload = {"bundle": str(output.resolve()), "seed": seed, "case_count": 12, "matrix": matrix}
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) if as_json else str(output.resolve()))
    return 0


def command_prepare(bundle: pathlib.Path, case_id: str, destination: pathlib.Path, as_json: bool) -> int:
    manifest = load_bundle(bundle)
    case = find_case(manifest, case_id)
    case_root = validate_case_provenance(bundle, case)
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")
    fixture = case_root / "visible" / "fixture"
    shutil.copytree(fixture, destination)
    payload = {
        "case_id": case_id,
        "workspace": str(destination.resolve()),
        "prompt": (case_root / "visible" / "prompt.txt").read_text(encoding="utf-8").strip(),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) if as_json else payload["prompt"])
    return 0


def command_admit(bundle: pathlib.Path, as_json: bool) -> int:
    manifest = load_bundle(bundle)
    results = []
    for case in manifest["cases"]:
        case_root = validate_case_provenance(bundle, case)
        with tempfile.TemporaryDirectory() as tmp:
            workspace = pathlib.Path(tmp) / "workspace"
            shutil.copytree(case_root / "visible" / "fixture", workspace)
            transcript = run_reference(case_root, workspace)
            grade = grade_case(case_root, workspace, transcript)
        results.append({"case_id": case["id"], "passed": grade["passed"], "checks": grade["checks"]})
    passed = len(results) == 12 and all(result["passed"] for result in results)
    payload = {"passed": passed, "admitted_cases": sum(result["passed"] for result in results), "cases": results}
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) if as_json else ("PASS" if passed else "FAIL"))
    return 0 if passed else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    generate = subparsers.add_parser("generate")
    generate.add_argument("--seed", required=True)
    generate.add_argument("--output", type=pathlib.Path, required=True)
    generate.add_argument("--json", action="store_true")
    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("bundle", type=pathlib.Path)
    prepare.add_argument("case_id")
    prepare.add_argument("destination", type=pathlib.Path)
    prepare.add_argument("--json", action="store_true")
    admit = subparsers.add_parser("admit")
    admit.add_argument("bundle", type=pathlib.Path)
    admit.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "generate":
            return command_generate(args.seed, args.output, args.json)
        if args.command == "prepare":
            return command_prepare(args.bundle, args.case_id, args.destination, args.json)
        if args.command == "admit":
            return command_admit(args.bundle, args.json)
        raise ValueError(f"unsupported command: {args.command}")
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
