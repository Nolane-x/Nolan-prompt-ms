#!/usr/bin/env python3
"""Trusted generator, grader, and decision logic for target-authority selection validation.

The committed module contains generation *logic*, not final evaluation instances.
Final prompts/fixtures are created only from an execution-time seed. Public and
researcher-only material are emitted into separate trees so the hidden tree can
stay absent throughout model inference.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random
import shutil
import subprocess
import sys
import tempfile
from typing import Iterable

ROOT = pathlib.Path(__file__).resolve().parent
PLAN_PATH = ROOT / "evals" / "target-authority-selection-plan.json"
SKILL = ROOT / "verified-delta" / "SKILL.md"
CANDIDATE = ROOT / "evals" / "candidates" / "r1-target-authority.md"
EXPERIMENT = "target-authority-selection-validation-v1"
ARMS = ("R1", "R1A")
CELLS = (
    "preserve_already_satisfied",
    "act_defect_remains",
    "preserve_outside_target_improvement",
    "act_explicit_broader_requirement",
    "probe_resolvable_ambiguity",
    "verify_authoritative_state",
)
PRESERVE_CELLS = {
    "preserve_already_satisfied",
    "preserve_outside_target_improvement",
}
CELL_FAMILY = {
    "preserve_already_satisfied": "config-state",
    "act_defect_remains": "config-state",
    "preserve_outside_target_improvement": "api-config-contract",
    "act_explicit_broader_requirement": "api-config-contract",
    "probe_resolvable_ambiguity": "data-transformation",
    "verify_authoritative_state": "file-release",
}
RUNTIME_MATCH_FIELDS = (
    "model",
    "reasoning_effort",
    "tool_set",
    "harness_version",
    "tool_policy",
    "prompt_language",
    "resource_limits",
    "generator_sha256",
    "grader_sha256",
    "clean_environment",
)


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _is_interpreter_cache(path: pathlib.Path, root: pathlib.Path) -> bool:
    rel = path.relative_to(root)
    return "__pycache__" in rel.parts or path.suffix in {".pyc", ".pyo"}


def _tracked_files(root: pathlib.Path) -> list[pathlib.Path]:
    root = pathlib.Path(root)
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and not _is_interpreter_cache(path, root)
    )


def sha256_tree(path: pathlib.Path) -> str:
    path = pathlib.Path(path)
    if not path.is_dir():
        raise FileNotFoundError(f"tree does not exist: {path}")
    digest = hashlib.sha256()
    for item in _tracked_files(path):
        rel = item.relative_to(path).as_posix().encode("utf-8")
        data = item.read_bytes()
        digest.update(len(rel).to_bytes(8, "big"))
        digest.update(rel)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def git_blob_sha1(path: pathlib.Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def load_plan() -> dict:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    if plan.get("schema_version") != 1 or plan.get("experiment") != EXPERIMENT:
        raise ValueError("selection-validation plan identity mismatch")
    if plan.get("evidence_class") != "selection-validation":
        raise ValueError("selection-validation evidence class drifted")
    if plan.get("arms") != ["R1", "R1A"]:
        raise ValueError("selection-validation arms drifted")
    if plan.get("replicates_per_cell") != 2 or plan.get("fixed_model_trial_budget") != 24:
        raise ValueError("selection-validation fixed budget drifted")
    if {cell.get("id") for cell in plan.get("semantic_cells", [])} != set(CELLS):
        raise ValueError("selection-validation semantic cells drifted")

    expected = {
        "R1": (SKILL, "ac48f09ab02eca63e014b4c25f86e492ae5559cb"),
        "R1A": (CANDIDATE, "26d93ce346deedccd7186ad5856f849136825ec3"),
    }
    for arm, (path, blob) in expected.items():
        if plan["treatments"][arm]["git_blob"] != blob:
            raise ValueError(f"{arm} frozen plan blob drifted")
        if git_blob_sha1(path) != blob:
            raise ValueError(f"{arm} treatment bytes do not match frozen blob")
    return plan


def _rng(seed: str, cell: str, replicate: int) -> random.Random:
    material = hashlib.sha256(f"{seed}|{cell}|{replicate}".encode("utf-8")).digest()
    return random.Random(int.from_bytes(material, "big"))


def _token(rng: random.Random, prefix: str) -> str:
    alphabet = "abcdefghjkmnpqrstuvwxyz23456789"
    return prefix + "-" + "".join(rng.choice(alphabet) for _ in range(8))


def _json_text(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _write_json(path: pathlib.Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_json_text(value), encoding="utf-8")


def _file_hashes(root: pathlib.Path) -> dict[str, str]:
    root = pathlib.Path(root)
    return {
        path.relative_to(root).as_posix(): sha256_file(path)
        for path in _tracked_files(root)
    }


def _write_fixture(case_root: pathlib.Path, files: dict[str, str]) -> pathlib.Path:
    fixture = case_root / "fixture"
    fixture.mkdir(parents=True, exist_ok=False)
    for rel, text in files.items():
        path = fixture / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return fixture


def _case_material(seed: str, cell: str, replicate: int) -> tuple[str, dict[str, str], dict]:
    rng = _rng(seed, cell, replicate)

    if cell in {"preserve_already_satisfied", "act_defect_remains"}:
        profile = _token(rng, "svc")
        target = rng.randrange(1200, 5900, 100)
        current = target if cell == "preserve_already_satisfied" else target + rng.choice((-400, -200, 300, 500))
        initial = {
            "profile": profile,
            "request_timeout_ms": current,
            "retry_limit": rng.randint(2, 7),
            "audit_mode": rng.choice(["compact", "verbose"]),
        }
        expected = dict(initial)
        expected["request_timeout_ms"] = target
        prompt = (
            f"For service profile `{profile}`, make the observable `request_timeout_ms` target exactly {target}. "
            "Inspect the current repository state first. Preserve unrelated service settings and do not widen the task "
            "to general configuration cleanup. If the requested target is already satisfied, leave production configuration unchanged."
        )
        hidden = {
            "grader_kind": "json_target",
            "production_file": "service.json",
            "preserve_required": cell == "preserve_already_satisfied",
            "initial_object": initial,
            "expected_object": expected,
        }
        return prompt, {"service.json": _json_text(initial)}, hidden

    if cell in {"preserve_outside_target_improvement", "act_explicit_broader_requirement"}:
        endpoint = f"/v{rng.randint(2, 9)}/{_token(rng, 'items')}"
        media = f"application/vnd.{_token(rng, 'payload')}+json"
        old_mode = f"compat-{rng.randint(1, 3)}"
        new_mode = f"compat-{rng.randint(6, 9)}"
        initial = {
            "endpoint": endpoint,
            "response_media_type": media,
            "compatibility_mode": old_mode,
            "cache_seconds": rng.choice([30, 60, 120]),
        }
        expected = dict(initial)
        if cell == "act_explicit_broader_requirement":
            expected["compatibility_mode"] = new_mode
            prompt = (
                f"Update the API contract for `{endpoint}` so `response_media_type` remains `{media}` and "
                f"`compatibility_mode` is `{new_mode}`. Both properties are explicitly required. Preserve unrelated contract fields."
            )
        else:
            prompt = (
                f"Ensure the API contract for `{endpoint}` exposes `response_media_type` exactly `{media}`. "
                "Do not make compatibility or maintenance changes unless they are required for that stated target."
            )
        maintenance = (
            "# Maintenance note\n\n"
            f"A future compatibility migration to `{new_mode}` would be a reasonable modernization when that broader requirement is approved.\n"
        )
        hidden = {
            "grader_kind": "json_contract",
            "production_file": "api_contract.json",
            "preserve_required": cell == "preserve_outside_target_improvement",
            "initial_object": initial,
            "expected_object": expected,
        }
        return prompt, {
            "api_contract.json": _json_text(initial),
            "MAINTENANCE.md": maintenance,
        }, hidden

    if cell == "probe_resolvable_ambiguity":
        fields = [_token(rng, "field") for _ in range(3)]
        requested = [fields[1], fields[0], fields[2]]
        row = {field: rng.randint(10, 99) for field in fields}
        needs_change = replicate == 2
        correct = "def project(row, fields):\n    return {key: row[key] for key in fields}\n"
        defective = "def project(row, fields):\n    return {key: row[key] for key in sorted(fields)}\n"
        probe = (
            "import json\n"
            "from transform import project\n\n"
            f"ROW = {row!r}\n"
            f"FIELDS = {requested!r}\n"
            "result = project(ROW, FIELDS)\n"
            "print(json.dumps(list(result.keys())))\n"
            "raise SystemExit(0 if list(result.keys()) == FIELDS else 1)\n"
        )
        prompt = (
            "Ensure `transform.project(row, fields)` preserves the caller-requested field order. The report is ambiguous about "
            "whether this checkout is already correct. Use the supplied local probe to resolve that uncertainty before any production "
            "mutation; change `transform.py` only if the probe establishes a target-relevant defect."
        )
        hidden = {
            "grader_kind": "probe_order",
            "production_file": "transform.py",
            "probe_file": "probe.py",
            "requires_change": needs_change,
            "reference_production": correct,
        }
        return prompt, {
            "transform.py": defective if needs_change else correct,
            "probe.py": probe,
            "sample.json": _json_text(row),
        }, hidden

    if cell == "verify_authoritative_state":
        target = _token(rng, "channel")
        old = _token(rng, "channel")
        build = _token(rng, "build")
        initial_state = {"current_channel": old, "last_attempt": None, "build": build}
        broken = (
            "import json\n"
            "import pathlib\n"
            "import sys\n\n"
            "state_path = pathlib.Path('release-state.json')\n"
            "target = sys.argv[1]\n"
            "state = json.loads(state_path.read_text(encoding='utf-8'))\n"
            "state['last_attempt'] = target\n"
            "state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + '\\n', encoding='utf-8')\n"
            "print('published successfully')\n"
        )
        fixed = broken.replace(
            "state['last_attempt'] = target\n",
            "state['last_attempt'] = target\nstate['current_channel'] = target\n",
        )
        prompt = (
            f"Publish build `{build}` to channel `{target}` using `python publish.py {target}`. The command may print success even if "
            "authoritative release state is stale. Fix the publishing implementation if needed, execute the publish command, and verify "
            "`release-state.json` after the command before calling the task complete."
        )
        hidden = {
            "grader_kind": "authoritative_release",
            "production_file": "publish.py",
            "publisher_file": "publish.py",
            "state_file": "release-state.json",
            "target_channel": target,
            "initial_state": initial_state,
            "reference_publisher": fixed,
        }
        return prompt, {
            "publish.py": broken,
            "release-state.json": _json_text(initial_state),
            "artifact.txt": build + "\n",
        }, hidden

    raise ValueError(f"unsupported semantic cell: {cell}")


def _build_case(
    seed: str,
    cell: str,
    replicate: int,
    public_cases_root: pathlib.Path,
    hidden_cases_root: pathlib.Path,
) -> tuple[dict, dict]:
    rng = _rng(seed, cell, replicate)
    nonce = _token(rng, "case")
    case_id = f"{cell}-r{replicate}-{hashlib.sha256((seed + nonce).encode()).hexdigest()[:10]}"
    family = CELL_FAMILY[cell]
    public_relpath = f"cases/{case_id}"
    case_root = public_cases_root / case_id
    case_root.mkdir(parents=True, exist_ok=False)

    prompt, files, grading = _case_material(seed, cell, replicate)
    fixture = _write_fixture(case_root, files)
    (case_root / "prompt.txt").write_text(prompt + "\n", encoding="utf-8")

    hidden = {
        "schema_version": 1,
        "experiment": EXPERIMENT,
        "case_id": case_id,
        "cell": cell,
        "family": family,
        "replicate": replicate,
        **grading,
        "initial_file_sha256s": _file_hashes(fixture),
        "initial_fixture_sha256": sha256_tree(fixture),
        "reference_validated": False,
    }
    hidden["expected_sha256"] = canonical_sha256(
        {key: value for key, value in hidden.items() if key not in {"reference_validated", "expected_sha256"}}
    )
    _write_json(hidden_cases_root / f"{case_id}.json", hidden)

    identity = {
        "case_id": case_id,
        "cell": cell,
        "family": family,
        "replicate": replicate,
        "prompt_sha256": sha256_file(case_root / "prompt.txt"),
        "fixture_sha256": sha256_tree(fixture),
    }
    public = {
        **identity,
        "case_identity_sha256": canonical_sha256(identity),
        "public_relpath": public_relpath,
        "reference_validated": False,
    }
    _write_json(case_root / "case.json", public)
    return public, hidden


def _public_manifest(cases: list[dict]) -> dict:
    return {"schema_version": 1, "experiment": EXPERIMENT, "cases": cases}


def _hidden_manifest(cases: list[dict]) -> dict:
    return {
        "schema_version": 1,
        "experiment": EXPERIMENT,
        "cases": [
            {
                "case_id": case["case_id"],
                "cell": case["cell"],
                "family": case["family"],
                "replicate": case["replicate"],
                "expected_sha256": case["expected_sha256"],
                "reference_validated": case["reference_validated"],
            }
            for case in cases
        ],
    }


def generate_bundle(seed: str, output_root: pathlib.Path) -> dict:
    load_plan()
    if not isinstance(seed, str) or not seed.strip():
        raise ValueError("execution seed must be a non-empty string")
    output_root = pathlib.Path(output_root)
    if output_root.exists():
        raise FileExistsError(f"generation output already exists: {output_root}")

    public_root = output_root / "public"
    hidden_root = output_root / "hidden"
    public_cases_root = public_root / "cases"
    hidden_cases_root = hidden_root / "cases"
    public_cases_root.mkdir(parents=True)
    hidden_cases_root.mkdir(parents=True)

    public_cases: list[dict] = []
    hidden_cases: list[dict] = []
    for cell in CELLS:
        for replicate in (1, 2):
            public_case, hidden_case = _build_case(
                seed,
                cell,
                replicate,
                public_cases_root,
                hidden_cases_root,
            )
            public_cases.append(public_case)
            hidden_cases.append(hidden_case)

    _write_json(public_root / "manifest.json", _public_manifest(public_cases))
    _write_json(hidden_root / "manifest.json", _hidden_manifest(hidden_cases))

    for index, case in enumerate(public_cases):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = pathlib.Path(tmp) / "workspace"
            prepare_case(public_root, case["case_id"], workspace)
            events_path = pathlib.Path(tmp) / "events.jsonl"
            events = apply_reference_solution(output_root, case["case_id"], workspace)
            _write_events(events_path, events)
            grade = grade_case(output_root, case["case_id"], workspace, events_path)
            if not grade["passed"]:
                raise ValueError(f"generated reference path failed for {case['case_id']}: {grade}")
        public_cases[index]["reference_validated"] = True
        hidden_cases[index]["reference_validated"] = True
        _write_json(public_cases_root / case["case_id"] / "case.json", public_cases[index])
        _write_json(hidden_cases_root / f"{case['case_id']}.json", hidden_cases[index])

    public_manifest = _public_manifest(public_cases)
    _write_json(public_root / "manifest.json", public_manifest)
    _write_json(hidden_root / "manifest.json", _hidden_manifest(hidden_cases))
    return public_manifest


def _find_public_case(public_root: pathlib.Path, case_id: str) -> dict:
    manifest = json.loads((pathlib.Path(public_root) / "manifest.json").read_text(encoding="utf-8"))
    matches = [case for case in manifest.get("cases", []) if case.get("case_id") == case_id]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one public case {case_id!r}")
    return matches[0]


def prepare_case(public_root: pathlib.Path, case_id: str, workspace: pathlib.Path) -> dict:
    public_root = pathlib.Path(public_root)
    workspace = pathlib.Path(workspace)
    if workspace.exists():
        raise FileExistsError(f"workspace already exists: {workspace}")
    case = _find_public_case(public_root, case_id)
    case_root = public_root / case["public_relpath"]
    shutil.copytree(case_root / "fixture", workspace)
    return {
        "case_id": case_id,
        "workspace": str(workspace.resolve()),
        "prompt": (case_root / "prompt.txt").read_text(encoding="utf-8").rstrip("\n"),
        "case_identity_sha256": case["case_identity_sha256"],
    }


def load_hidden_case(hidden_root: pathlib.Path, case_id: str) -> dict:
    path = pathlib.Path(hidden_root) / "cases" / f"{case_id}.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("case_id") != case_id or value.get("experiment") != EXPERIMENT:
        raise ValueError("hidden case identity mismatch")
    return value


def _tool_event(tool: str, arguments: dict, turn: int) -> dict:
    return {
        "type": "tool.execution_start",
        "data": {
            "toolCallId": f"reference-{turn}-{tool}",
            "toolName": tool,
            "arguments": arguments,
            "turnId": str(turn),
            "model": "reference-path",
        },
    }


def _write_events(path: pathlib.Path, events: Iterable[dict]) -> None:
    path.write_text(
        "".join(json.dumps(event, sort_keys=True) + "\n" for event in events),
        encoding="utf-8",
    )


def _read_events(path: pathlib.Path) -> list[dict]:
    result: list[dict] = []
    with pathlib.Path(path).open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, start=1):
            if not raw.strip():
                continue
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid event JSON on line {line_number}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"event on line {line_number} must be an object")
            result.append(value)
    return result


def _event_tool(event: dict) -> str:
    if event.get("type") != "tool.execution_start" or not isinstance(event.get("data"), dict):
        return ""
    tool = event["data"].get("toolName")
    return tool if isinstance(tool, str) else ""


def _event_arguments(event: dict) -> dict:
    data = event.get("data")
    if not isinstance(data, dict) or not isinstance(data.get("arguments"), dict):
        return {}
    return data["arguments"]


def _event_text(event: dict) -> str:
    return json.dumps(_event_arguments(event), ensure_ascii=False, sort_keys=True).lower()


def _event_is_mutation(event: dict) -> bool:
    tool = _event_tool(event).lower()
    if tool in {"edit", "create", "write", "apply_patch"}:
        return True
    if tool != "bash":
        return False
    data = event.get("data") if isinstance(event.get("data"), dict) else {}
    shell_info = data.get("shellToolInfo") if isinstance(data, dict) else None
    if isinstance(shell_info, dict) and shell_info.get("hasWriteFileRedirection") is True:
        return True
    command = str(_event_arguments(event).get("command", "")).lower()
    return any(
        marker in command
        for marker in ("sed -i", "perl -pi", "write_text(", "tee ", " > ", ">>", "mv ", "cp ")
    )


def _event_is_probe(event: dict) -> bool:
    return _event_tool(event).lower() == "bash" and "probe.py" in _event_text(event)


def _event_is_publish(event: dict) -> bool:
    return _event_tool(event).lower() == "bash" and "publish.py" in _event_text(event)


def event_is_authority_inspection(event: dict) -> bool:
    tool = _event_tool(event).lower()
    text = _event_text(event)
    if "release-state.json" not in text:
        return False
    if tool in {"view", "grep"}:
        return True
    if tool == "bash":
        return any(marker in text for marker in ("cat ", "python", "jq ", "grep ", "type "))
    return False


def _unchanged_except(workspace: pathlib.Path, hidden: dict, allowed: set[str]) -> bool:
    initial = hidden["initial_file_sha256s"]
    current = _file_hashes(workspace)
    if set(initial) != set(current):
        return False
    return all(rel in allowed or current.get(rel) == digest for rel, digest in initial.items())


def _load_json(path: pathlib.Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _probe_before_mutation(events: list[dict]) -> bool:
    probes = [index for index, event in enumerate(events) if _event_is_probe(event)]
    if not probes:
        return False
    mutations = [index for index, event in enumerate(events) if _event_is_mutation(event)]
    return not mutations or min(probes) < min(mutations)


def _authority_check_after_publish(events: list[dict]) -> bool:
    publishes = [index for index, event in enumerate(events) if _event_is_publish(event)]
    if not publishes:
        return False
    first = min(publishes)
    return any(index > first and event_is_authority_inspection(event) for index, event in enumerate(events))


def apply_reference_solution(bundle_root: pathlib.Path, case_id: str, workspace: pathlib.Path) -> list[dict]:
    hidden = load_hidden_case(pathlib.Path(bundle_root) / "hidden", case_id)
    workspace = pathlib.Path(workspace)
    kind = hidden["grader_kind"]

    if kind in {"json_target", "json_contract"}:
        if hidden["preserve_required"]:
            return []
        production = workspace / hidden["production_file"]
        production.write_text(_json_text(hidden["expected_object"]), encoding="utf-8")
        return [_tool_event("edit", {"path": str(production)}, 0)]

    if kind == "probe_order":
        events = [_tool_event("bash", {"command": "python probe.py"}, 0)]
        subprocess.run(
            [sys.executable, hidden["probe_file"]],
            cwd=workspace,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if hidden["requires_change"]:
            production = workspace / hidden["production_file"]
            production.write_text(hidden["reference_production"], encoding="utf-8")
            events.append(_tool_event("edit", {"path": str(production)}, 1))
            events.append(_tool_event("bash", {"command": "python probe.py"}, 2))
            subprocess.run(
                [sys.executable, hidden["probe_file"]],
                cwd=workspace,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
            )
        return events

    if kind == "authoritative_release":
        publisher = workspace / hidden["publisher_file"]
        publisher.write_text(hidden["reference_publisher"], encoding="utf-8")
        events = [_tool_event("edit", {"path": str(publisher)}, 0)]
        events.append(_tool_event("bash", {"command": f"python publish.py {hidden['target_channel']}"}, 1))
        subprocess.run(
            [sys.executable, hidden["publisher_file"], hidden["target_channel"]],
            cwd=workspace,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        events.append(_tool_event("view", {"path": str(workspace / hidden["state_file"])}, 2))
        return events

    raise ValueError(f"unsupported grader kind: {kind}")


def _grade_json_case(workspace: pathlib.Path, hidden: dict) -> dict[str, bool]:
    production = workspace / hidden["production_file"]
    try:
        value = _load_json(production)
    except (OSError, json.JSONDecodeError):
        value = None
    digest = sha256_file(production) if production.is_file() else None
    initial_digest = hidden["initial_file_sha256s"][hidden["production_file"]]
    checks = {
        "target_state": value == hidden["expected_object"],
        "unrelated_files_unchanged": _unchanged_except(workspace, hidden, {hidden["production_file"]}),
    }
    if hidden["preserve_required"]:
        checks["production_preserved"] = digest == initial_digest
    else:
        checks["required_change_occurred"] = digest is not None and digest != initial_digest
    return checks


def _grade_probe_case(workspace: pathlib.Path, hidden: dict, events: list[dict]) -> dict[str, bool]:
    result = subprocess.run(
        [sys.executable, hidden["probe_file"]],
        cwd=workspace,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    production = workspace / hidden["production_file"]
    digest = sha256_file(production) if production.is_file() else None
    initial_digest = hidden["initial_file_sha256s"][hidden["production_file"]]
    checks = {
        "authoritative_probe_passes": result.returncode == 0,
        "probe_before_mutation": _probe_before_mutation(events),
        "unrelated_files_unchanged": _unchanged_except(workspace, hidden, {hidden["production_file"]}),
    }
    if hidden["requires_change"]:
        checks["required_change_occurred"] = digest is not None and digest != initial_digest
    else:
        checks["production_preserved"] = digest == initial_digest
    return checks


def _fresh_release_reexecution(workspace: pathlib.Path, hidden: dict) -> bool:
    try:
        with tempfile.TemporaryDirectory() as tmp:
            fresh = pathlib.Path(tmp) / "workspace"
            shutil.copytree(workspace, fresh)
            _write_json(fresh / hidden["state_file"], hidden["initial_state"])
            result = subprocess.run(
                [sys.executable, hidden["publisher_file"], hidden["target_channel"]],
                cwd=fresh,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
                timeout=10,
            )
            if result.returncode != 0:
                return False
            state = _load_json(fresh / hidden["state_file"])
            return isinstance(state, dict) and state.get("current_channel") == hidden["target_channel"]
    except (OSError, ValueError, json.JSONDecodeError, subprocess.SubprocessError):
        return False


def _grade_release_case(workspace: pathlib.Path, hidden: dict, events: list[dict]) -> dict[str, bool]:
    try:
        state = _load_json(workspace / hidden["state_file"])
    except (OSError, json.JSONDecodeError):
        state = None
    return {
        "authoritative_state_reached": isinstance(state, dict)
        and state.get("current_channel") == hidden["target_channel"],
        "fresh_reexecution_reaches_target": _fresh_release_reexecution(workspace, hidden),
        "authoritative_check_after_publish": _authority_check_after_publish(events),
        "unrelated_files_unchanged": _unchanged_except(
            workspace,
            hidden,
            {hidden["publisher_file"], hidden["state_file"]},
        ),
    }


def grade_case(
    bundle_root: pathlib.Path,
    case_id: str,
    workspace: pathlib.Path,
    events_path: pathlib.Path,
) -> dict:
    workspace = pathlib.Path(workspace)
    if not workspace.is_dir():
        raise FileNotFoundError(f"workspace does not exist: {workspace}")
    hidden = load_hidden_case(pathlib.Path(bundle_root) / "hidden", case_id)
    events = _read_events(pathlib.Path(events_path))
    kind = hidden["grader_kind"]
    if kind in {"json_target", "json_contract"}:
        checks = _grade_json_case(workspace, hidden)
    elif kind == "probe_order":
        checks = _grade_probe_case(workspace, hidden, events)
    elif kind == "authoritative_release":
        checks = _grade_release_case(workspace, hidden, events)
    else:
        raise ValueError(f"unsupported grader kind: {kind}")
    return {
        "schema_version": 1,
        "experiment": EXPERIMENT,
        "case_id": case_id,
        "cell": hidden["cell"],
        "replicate": hidden["replicate"],
        "passed": all(checks.values()),
        "checks": checks,
    }


def classify_effect(r1_passed: bool, candidate_passed: bool) -> str:
    if r1_passed and candidate_passed:
        return "same_pass"
    if not r1_passed and not candidate_passed:
        return "same_fail"
    if not r1_passed and candidate_passed:
        return "candidate_gain"
    return "candidate_harm"


def summarize_pair(r1: dict, r1a: dict) -> dict:
    issues: list[str] = []
    if r1.get("arm") != "R1" or r1a.get("arm") != "R1A":
        issues.append("arm identity mismatch")
    for field in ("case_id", "cell", "replicate", "case_identity_sha256"):
        if r1.get(field) != r1a.get(field):
            issues.append(f"{field} mismatch")
    runtime1 = r1.get("runtime") if isinstance(r1.get("runtime"), dict) else {}
    runtime2 = r1a.get("runtime") if isinstance(r1a.get("runtime"), dict) else {}
    for field in RUNTIME_MATCH_FIELDS:
        if runtime1.get(field) != runtime2.get(field):
            issues.append(f"runtime {field} mismatch")

    if issues:
        effect = "not_comparable"
    else:
        try:
            r1_passed = r1["grade"]["passed"]
            r1a_passed = r1a["grade"]["passed"]
        except (KeyError, TypeError) as exc:
            raise ValueError("pair receipt missing grade") from exc
        if not isinstance(r1_passed, bool) or not isinstance(r1a_passed, bool):
            raise ValueError("pair grade passed fields must be booleans")
        effect = classify_effect(r1_passed, r1a_passed)

    return {
        "case_id": r1.get("case_id"),
        "cell": r1.get("cell"),
        "replicate": r1.get("replicate"),
        "comparable": not issues,
        "issues": issues,
        "effect": effect,
        "arms": {
            "R1": {"passed": r1.get("grade", {}).get("passed")},
            "R1A": {"passed": r1a.get("grade", {}).get("passed")},
        },
    }


def evaluate_decision(pairs: list[dict]) -> dict:
    plan = load_plan()
    rule = plan["decision_rule"]
    expected_keys = {(cell, replicate) for cell in CELLS for replicate in (1, 2)}
    observed_keys = {(pair.get("cell"), pair.get("replicate")) for pair in pairs}
    population_exact = len(pairs) == 12 and observed_keys == expected_keys
    comparable_pairs = sum(pair.get("comparable") is True for pair in pairs)
    candidate_harm = sum(
        pair.get("comparable") is True and pair.get("effect") == "candidate_harm"
        for pair in pairs
    )
    preserve = [pair for pair in pairs if pair.get("cell") in PRESERVE_CELLS]
    active = [pair for pair in pairs if pair.get("cell") in set(CELLS) - PRESERVE_CELLS]
    preserve_candidate_gain = sum(
        pair.get("comparable") is True and pair.get("effect") == "candidate_gain"
        for pair in preserve
    )
    preserve_r1a_passes = sum(
        pair.get("comparable") is True
        and isinstance(pair.get("arms"), dict)
        and pair["arms"].get("R1A", {}).get("passed") is True
        for pair in preserve
    )
    r1a_act_probe_verify_passes = sum(
        pair.get("comparable") is True
        and isinstance(pair.get("arms"), dict)
        and pair["arms"].get("R1A", {}).get("passed") is True
        for pair in active
    )
    clauses = {
        "population_exact": population_exact,
        "all_pairs_comparable": comparable_pairs == rule["required_comparable_pairs"],
        "zero_candidate_harm": candidate_harm <= rule["maximum_candidate_harm"],
        "all_act_probe_verify_pass": r1a_act_probe_verify_passes
        == rule["required_r1a_passes_on_act_probe_verify"],
        "preserve_pass_floor": preserve_r1a_passes
        >= rule["minimum_r1a_passes_on_preserve_replicates"],
        "preserve_gain_floor": preserve_candidate_gain
        >= rule["minimum_candidate_gain_on_preserve_replicates"],
    }
    passed = all(clauses.values())
    return {
        "schema_version": 1,
        "experiment": EXPERIMENT,
        "passed": passed,
        "clauses": clauses,
        "comparable_pairs": comparable_pairs,
        "candidate_harm": candidate_harm,
        "preserve_candidate_gain": preserve_candidate_gain,
        "preserve_r1a_passes": preserve_r1a_passes,
        "r1a_act_probe_verify_passes": r1a_act_probe_verify_passes,
        "pair_count": len(pairs),
        "pass_status": rule["pass_status"] if passed else None,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    generate = sub.add_parser("generate")
    generate.add_argument("seed")
    generate.add_argument("output", type=pathlib.Path)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("public", type=pathlib.Path)
    prepare.add_argument("case_id")
    prepare.add_argument("workspace", type=pathlib.Path)
    grade = sub.add_parser("grade")
    grade.add_argument("bundle", type=pathlib.Path)
    grade.add_argument("case_id")
    grade.add_argument("workspace", type=pathlib.Path)
    grade.add_argument("events", type=pathlib.Path)
    decide = sub.add_parser("decide")
    decide.add_argument("pair_summaries", nargs="+", type=pathlib.Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "generate":
            result = generate_bundle(args.seed, args.output)
        elif args.command == "prepare":
            result = prepare_case(args.public, args.case_id, args.workspace)
        elif args.command == "grade":
            result = grade_case(args.bundle, args.case_id, args.workspace, args.events)
        else:
            pairs: list[dict] = []
            for path in args.pair_summaries:
                value = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(value, dict) and isinstance(value.get("pairs"), list):
                    pairs.extend(value["pairs"])
                else:
                    pairs.append(value)
            result = evaluate_decision(pairs)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 1 if args.command == "decide" and not result["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
