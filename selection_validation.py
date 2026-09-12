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
import semantic_ablation as ablation

ROOT = pathlib.Path(__file__).resolve().parent
HARNESS = pathlib.Path(__file__).resolve()
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
                "probe.py": "from transform import keep_readings\nprint(keep_readings([None, 0, 3]))\n",
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
        transcript_parts.extend([result.stdout, result.stderr])
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
    grader = {"expected_tree_sha256": expected_tree, "transcript_required": blueprint["transcript_required"]}
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
            cases.append({
                "id": stable_case_id(seed, cell_id, replicate),
                "cell_id": cell_id,
                "role": cell["role"],
                "family": FAMILY_BY_CELL[cell_id],
                "replicate": replicate,
                "pair_id": f"{cell_id}-r{replicate}",
            })
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
        "generator_sha256": sha256_file(HARNESS),
        "contamination_status": "mechanically-clean",
        "decision_rule": plan["decision_rule"],
        "treatments": {
            arm: {
                "git_blob": plan["treatments"][arm]["git_blob"],
                "content_sha256": sha256_file(SKILL if arm == "R1" else CANDIDATE),
            }
            for arm in ARMS
        },
        "cases": cases,
    }


def validate_sha256(value: object, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise ValueError(f"{label} must be a lowercase SHA-256 digest")
    return value


def load_bundle(bundle: pathlib.Path, *, require_current: bool = True) -> dict:
    manifest_path = bundle / "bundle.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"bundle manifest does not exist: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("experiment") != EXPERIMENT or manifest.get("schema_version") != 1:
        raise ValueError("invalid selection bundle identity")
    if len(manifest.get("cases", [])) != 12:
        raise ValueError("selection bundle must contain exactly 12 cases")
    validate_sha256(manifest.get("plan_sha256"), "bundle plan_sha256")
    validate_sha256(manifest.get("generator_sha256"), "bundle generator_sha256")
    if manifest.get("contamination_status") != "mechanically-clean":
        raise ValueError("selection bundle contamination boundary is not clean")
    if not isinstance(manifest.get("decision_rule"), dict):
        raise ValueError("selection bundle decision rule is missing")
    if set(manifest.get("treatments", {})) != set(ARMS):
        raise ValueError("selection bundle treatments are invalid")
    for arm in ARMS:
        validate_sha256(manifest["treatments"][arm].get("content_sha256"), f"{arm} content_sha256")
        blob = manifest["treatments"][arm].get("git_blob")
        if not isinstance(blob, str) or len(blob) != 40:
            raise ValueError(f"{arm} git blob is invalid")
    if require_current:
        plan = load_plan()
        if manifest["plan_sha256"] != sha256_file(PLAN_PATH):
            raise ValueError("selection bundle preregistration provenance mismatch")
        expected = {
            arm: {
                "git_blob": plan["treatments"][arm]["git_blob"],
                "content_sha256": sha256_file(SKILL if arm == "R1" else CANDIDATE),
            }
            for arm in ARMS
        }
        if manifest["treatments"] != expected:
            raise ValueError("selection bundle treatment provenance mismatch")
        if manifest["decision_rule"] != plan["decision_rule"]:
            raise ValueError("selection bundle decision rule drifted")
        if manifest["generator_sha256"] != sha256_file(HARNESS):
            raise ValueError("selection bundle generator provenance mismatch")
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


def treatment_set(manifest: dict) -> dict[str, str]:
    return {arm: manifest["treatments"][arm]["content_sha256"] for arm in ARMS}


def validate_run_binding(run_config: dict, manifest: dict, arm: str, model_id: str, harness_id: str) -> None:
    value = run_config["value"]
    if value["matched"]["model"]["id"] != model_id:
        raise ValueError("run config matched.model.id does not match --model-id")
    if value["matched"]["harness"]["id"] != harness_id:
        raise ValueError("run config matched.harness.id does not match --harness-id")
    loaded = manifest["treatments"][arm]["content_sha256"]
    if value["intervention"] != ablation.expected_intervention(arm, loaded):
        raise ValueError(f"run config intervention does not match frozen {arm} treatment")


def classify_effect(r1_passed: bool, r1a_passed: bool) -> str:
    if r1_passed and r1a_passed:
        return "same_pass"
    if not r1_passed and not r1a_passed:
        return "same_fail"
    if not r1_passed and r1a_passed:
        return "candidate_gain"
    return "candidate_harm"


def evaluate_decision(pairs: list[dict], rule: dict | None = None) -> dict:
    if rule is None:
        rule = load_plan()["decision_rule"]
    comparable = sum(bool(pair.get("comparable")) for pair in pairs)
    harm = sum(pair.get("effect") == "candidate_harm" for pair in pairs)
    preserve = [pair for pair in pairs if pair.get("role") == "preserve"]
    act_probe_verify = [pair for pair in pairs if pair.get("role") in {"act", "probe", "verify"}]
    r1a_required_passes = sum(
        bool(pair.get("arms", {}).get("R1A", {}).get("passed")) for pair in act_probe_verify
    )
    r1a_preserve_passes = sum(
        bool(pair.get("arms", {}).get("R1A", {}).get("passed")) for pair in preserve
    )
    preserve_gain = sum(pair.get("effect") == "candidate_gain" for pair in preserve)
    checks = {
        "required_comparable_pairs": comparable == rule["required_comparable_pairs"],
        "maximum_candidate_harm": harm <= rule["maximum_candidate_harm"],
        "required_r1a_passes_on_act_probe_verify": r1a_required_passes >= rule["required_r1a_passes_on_act_probe_verify"],
        "minimum_r1a_passes_on_preserve_replicates": r1a_preserve_passes >= rule["minimum_r1a_passes_on_preserve_replicates"],
        "minimum_candidate_gain_on_preserve_replicates": preserve_gain >= rule["minimum_candidate_gain_on_preserve_replicates"],
    }
    return {
        "passed": len(pairs) == rule["required_comparable_pairs"] and all(checks.values()),
        "checks": checks,
        "observed": {
            "comparable_pairs": comparable,
            "candidate_harm": harm,
            "r1a_passes_on_act_probe_verify": r1a_required_passes,
            "r1a_passes_on_preserve_replicates": r1a_preserve_passes,
            "candidate_gain_on_preserve_replicates": preserve_gain,
        },
        "pass_status": rule["pass_status"],
        "failure_action": rule["failure_action"],
    }


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
    matrix = {"include": [{"case_id": case["id"], "arm": arm} for case in manifest["cases"] for arm in ARMS]}
    payload = {"bundle": str(output.resolve()), "seed": seed, "case_count": 12, "matrix": matrix}
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) if as_json else str(output.resolve()))
    return 0


def command_prepare(bundle: pathlib.Path, case_id: str, destination: pathlib.Path, as_json: bool) -> int:
    manifest = load_bundle(bundle)
    case = find_case(manifest, case_id)
    case_root = validate_case_provenance(bundle, case)
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")
    shutil.copytree(case_root / "visible" / "fixture", destination)
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


def command_record(
    bundle: pathlib.Path,
    case_id: str,
    workspace: pathlib.Path,
    receipt_path: pathlib.Path,
    arm: str,
    model_id: str,
    harness_id: str,
    transcript_path: pathlib.Path,
    metrics_path: pathlib.Path,
    run_config_path: pathlib.Path,
    as_json: bool,
) -> int:
    if receipt_path.exists():
        raise FileExistsError(f"receipt already exists: {receipt_path}")
    if not workspace.is_dir():
        raise FileNotFoundError(f"workspace does not exist: {workspace}")
    if not transcript_path.is_file():
        raise FileNotFoundError(f"transcript does not exist: {transcript_path}")
    manifest = load_bundle(bundle)
    case = find_case(manifest, case_id)
    case_root = validate_case_provenance(bundle, case)
    metrics = base.validate_metrics(json.loads(metrics_path.read_text(encoding="utf-8")))
    run_config = base.load_run_config(run_config_path)
    validate_run_binding(run_config, manifest, arm, model_id, harness_id)
    transcript_bytes = transcript_path.read_bytes()
    transcript_text = transcript_bytes.decode("utf-8", errors="replace")
    members = treatment_set(manifest)
    payload = {
        "schema_version": 1,
        "experiment": EXPERIMENT,
        "arm": arm,
        "model_id": model_id,
        "harness_id": harness_id,
        "bundle": {
            "seed": manifest["seed"],
            "plan_sha256": manifest["plan_sha256"],
            "generator_sha256": manifest["generator_sha256"],
            "contamination_status": manifest["contamination_status"],
        },
        "case": case,
        "treatment": {
            "loaded_sha256": members[arm],
            "treatment_sha256s": members,
            "treatment_set_sha256": base.canonical_sha256(members),
            "git_blob": manifest["treatments"][arm]["git_blob"],
        },
        "workspace_sha256": base.sha256_tree(workspace),
        "transcript": {"sha256": sha256_bytes(transcript_bytes), "bytes": len(transcript_bytes)},
        "metrics": metrics,
        "grade": grade_case(case_root, workspace, transcript_text),
        "run_config": run_config,
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json_text(payload), encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) if as_json else str(receipt_path.resolve()))
    return 0


def load_receipt(path: pathlib.Path, manifest: dict) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"receipt does not exist: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1 or payload.get("experiment") != EXPERIMENT:
        raise ValueError(f"invalid selection receipt identity: {path}")
    arm = payload.get("arm")
    if arm not in ARMS:
        raise ValueError(f"invalid selection receipt arm: {path}")
    case_raw = payload.get("case")
    if not isinstance(case_raw, dict) or not isinstance(case_raw.get("id"), str):
        raise ValueError(f"invalid selection receipt case: {path}")
    expected_case = find_case(manifest, case_raw["id"])
    if case_raw != expected_case:
        raise ValueError(f"selection receipt case provenance mismatch: {path}")
    expected_bundle = {
        "seed": manifest["seed"],
        "plan_sha256": manifest["plan_sha256"],
        "generator_sha256": manifest["generator_sha256"],
        "contamination_status": manifest["contamination_status"],
    }
    if payload.get("bundle") != expected_bundle:
        raise ValueError(f"selection receipt bundle provenance mismatch: {path}")
    members = treatment_set(manifest)
    treatment = payload.get("treatment")
    expected_treatment = {
        "loaded_sha256": members[arm],
        "treatment_sha256s": members,
        "treatment_set_sha256": base.canonical_sha256(members),
        "git_blob": manifest["treatments"][arm]["git_blob"],
    }
    if treatment != expected_treatment:
        raise ValueError(f"selection receipt treatment provenance mismatch: {path}")
    payload["metrics"] = base.validate_metrics(payload.get("metrics"))
    grade = payload.get("grade")
    if not isinstance(grade, dict) or not isinstance(grade.get("passed"), bool):
        raise ValueError(f"invalid selection receipt grade: {path}")
    run_config_raw = payload.get("run_config")
    if not isinstance(run_config_raw, dict):
        raise ValueError(f"invalid selection receipt run config: {path}")
    value = base.validate_run_config(run_config_raw.get("value"))
    run_config = {
        "value": value,
        "sha256": base.canonical_sha256(value),
        "matched_sha256": base.canonical_sha256(value["matched"]),
    }
    if run_config_raw.get("sha256") != run_config["sha256"] or run_config_raw.get("matched_sha256") != run_config["matched_sha256"]:
        raise ValueError(f"selection receipt run-config hash mismatch: {path}")
    validate_run_binding(run_config, manifest, arm, payload.get("model_id"), payload.get("harness_id"))
    payload["run_config"] = run_config
    return payload


def compare_pair(case: dict, r1: dict | None, r1a: dict | None, duplicate: bool = False) -> dict:
    issues = []
    if duplicate:
        issues.append("duplicate arm receipt")
    if r1 is None:
        issues.append("missing R1 receipt")
    if r1a is None:
        issues.append("missing R1A receipt")
    if r1 is not None and r1a is not None:
        if r1["bundle"] != r1a["bundle"]:
            issues.append("bundle provenance mismatch")
        if r1["treatment"]["treatment_set_sha256"] != r1a["treatment"]["treatment_set_sha256"]:
            issues.append("treatment set mismatch")
        if r1["run_config"]["matched_sha256"] != r1a["run_config"]["matched_sha256"]:
            issues.append("matched run config mismatch")
    comparable = not issues
    effect = classify_effect(r1["grade"]["passed"], r1a["grade"]["passed"]) if comparable else "not_comparable"
    arms = {}
    for arm, receipt in (("R1", r1), ("R1A", r1a)):
        if receipt is not None:
            arms[arm] = {"passed": receipt["grade"]["passed"], "metrics": receipt["metrics"]}
    return {
        "case_id": case["id"],
        "pair_id": case["pair_id"],
        "cell_id": case["cell_id"],
        "role": case["role"],
        "comparable": comparable,
        "issues": issues,
        "effect": effect,
        "arms": arms,
    }


def command_summarize(bundle: pathlib.Path, receipt_paths: list[pathlib.Path], as_json: bool) -> int:
    manifest = load_bundle(bundle, require_current=False)
    grouped: dict[str, dict[str, dict]] = {}
    duplicates: set[str] = set()
    global_issues = []
    expected_ids = {case["id"] for case in manifest["cases"]}
    for path in receipt_paths:
        receipt = load_receipt(path, manifest)
        case_id = receipt["case"]["id"]
        if case_id not in expected_ids:
            global_issues.append(f"unexpected case receipt: {case_id}")
            continue
        arms = grouped.setdefault(case_id, {})
        arm = receipt["arm"]
        if arm in arms:
            duplicates.add(case_id)
        else:
            arms[arm] = receipt
    pairs = []
    for case in manifest["cases"]:
        arms = grouped.get(case["id"], {})
        pairs.append(compare_pair(case, arms.get("R1"), arms.get("R1A"), case["id"] in duplicates))
    decision = evaluate_decision(pairs, manifest["decision_rule"])
    infrastructure_valid = (
        len(receipt_paths) == 24
        and not global_issues
        and all(pair["comparable"] for pair in pairs)
        and manifest["contamination_status"] == "mechanically-clean"
    )
    if not infrastructure_valid:
        decision = {**decision, "passed": False, "infrastructure_valid": False}
    else:
        decision = {**decision, "infrastructure_valid": True}
    payload = {
        "schema_version": 1,
        "experiment": EXPERIMENT,
        "bundle": {
            "seed": manifest["seed"],
            "plan_sha256": manifest["plan_sha256"],
            "generator_sha256": manifest["generator_sha256"],
            "contamination_status": manifest["contamination_status"],
        },
        "infrastructure_valid": infrastructure_valid,
        "issues": global_issues,
        "pairs": pairs,
        "decision": decision,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) if as_json else ("PASS" if decision["passed"] else "FAIL"))
    return 0


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
    record = subparsers.add_parser("record")
    record.add_argument("bundle", type=pathlib.Path)
    record.add_argument("case_id")
    record.add_argument("workspace", type=pathlib.Path)
    record.add_argument("receipt", type=pathlib.Path)
    record.add_argument("--arm", choices=ARMS, required=True)
    record.add_argument("--model-id", required=True)
    record.add_argument("--harness-id", required=True)
    record.add_argument("--transcript", type=pathlib.Path, required=True)
    record.add_argument("--metrics", type=pathlib.Path, required=True)
    record.add_argument("--run-config", type=pathlib.Path, required=True)
    record.add_argument("--json", action="store_true")
    summarize = subparsers.add_parser("summarize")
    summarize.add_argument("bundle", type=pathlib.Path)
    summarize.add_argument("receipts", nargs="+", type=pathlib.Path)
    summarize.add_argument("--json", action="store_true")
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
        if args.command == "record":
            return command_record(
                args.bundle, args.case_id, args.workspace, args.receipt, args.arm,
                args.model_id, args.harness_id, args.transcript, args.metrics, args.run_config, args.json,
            )
        if args.command == "summarize":
            return command_summarize(args.bundle, args.receipts, args.json)
        raise ValueError(f"unsupported command: {args.command}")
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
