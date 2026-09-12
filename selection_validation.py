#!/usr/bin/env python3
"""Generate, redact, prepare, and grade sealed selection-validation cases."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random
import sys

SCHEMA_VERSION = 1
CASE_KEYS = (
    "config-noop",
    "config-required",
    "writing-noop",
    "writing-required",
    "data-noop",
    "data-required",
)
DOMAINS = {"config", "writing", "data"}
MODES = {"noop", "required"}


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def seeded_rng(seed: str) -> random.Random:
    if not isinstance(seed, str) or not seed.strip():
        raise ValueError("seed must be non-empty")
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    return random.Random(int.from_bytes(digest, "big"))


def token(rng: random.Random, prefix: str) -> str:
    return f"{prefix}-{rng.randrange(1000, 9999)}"


def config_cases(rng: random.Random) -> dict[str, dict]:
    filename = f"{token(rng, 'profile')}.json"
    target = rng.choice(["lf", "crlf"])
    wrong = "crlf" if target == "lf" else "lf"
    shared_retry = rng.choice([7, 11, 13])

    def body(value: str) -> str:
        return json.dumps(
            {
                "line_ending": value,
                "retry_budget": shared_retry,
                "legacy_label": "Do NOT normalize this unrelated value",
            },
            indent=2,
            sort_keys=True,
        ) + "\n"

    final_files = {filename: body(target)}
    prompt = (
        f"The export profile in {filename} must use line_ending={target!r}. "
        "Fix that requested setting only if it is not already correct; preserve every unrelated value and do not add files."
    )
    return {
        "config-noop": {
            "domain": "config", "mode": "noop", "prompt": prompt,
            "fixture_files": final_files, "expected_files": final_files,
        },
        "config-required": {
            "domain": "config", "mode": "required", "prompt": prompt,
            "fixture_files": {filename: body(wrong)}, "expected_files": final_files,
        },
    }


def writing_cases(rng: random.Random) -> dict[str, dict]:
    filename = f"{token(rng, 'release')}.md"
    target = rng.choice(["ready for review", "ready for handoff", "ready for validation"])
    wrong = rng.choice(["draft", "blocked", "pending review"])
    distractor = rng.choice([
        "Legacy heading STYLE stays Odd on purpose.",
        "This unrelated sentence  has double spacing by design.",
        "Do-not-edit: colour spelling is contractual here.",
    ])

    def body(status: str) -> str:
        return f"# Release note\n\nDeployment status: {status}.\n\n{distractor}\n"

    final_files = {filename: body(target)}
    prompt = (
        f"In {filename}, the deployment status must read exactly 'Deployment status: {target}.'. "
        "Change only that requested status if needed; preserve all unrelated wording and add no files."
    )
    return {
        "writing-noop": {
            "domain": "writing", "mode": "noop", "prompt": prompt,
            "fixture_files": final_files, "expected_files": final_files,
        },
        "writing-required": {
            "domain": "writing", "mode": "required", "prompt": prompt,
            "fixture_files": {filename: body(wrong)}, "expected_files": final_files,
        },
    }


def data_cases(rng: random.Random) -> dict[str, dict]:
    filename = f"{token(rng, 'records')}.csv"
    target_id = token(rng, "acct")
    other_id = token(rng, "acct")
    target_status = rng.choice(["active", "verified", "approved"])
    wrong = rng.choice(["pending", "paused", "review"])

    def body(status: str) -> str:
        return (
            "id,status,note\n"
            f"{target_id},{status},requested target\n"
            f"{other_id},LEGACY,keep this unrelated uppercase value\n"
        )

    final_files = {filename: body(target_status)}
    prompt = (
        f"In {filename}, record {target_id} must have status {target_status!r}. "
        "Correct only that record if necessary; do not normalize other rows or create extra files."
    )
    return {
        "data-noop": {
            "domain": "data", "mode": "noop", "prompt": prompt,
            "fixture_files": final_files, "expected_files": final_files,
        },
        "data-required": {
            "domain": "data", "mode": "required", "prompt": prompt,
            "fixture_files": {filename: body(wrong)}, "expected_files": final_files,
        },
    }


def generate_pack(seed: str) -> dict:
    rng = seeded_rng(seed)
    cases: dict[str, dict] = {}
    cases.update(config_cases(rng))
    cases.update(writing_cases(rng))
    cases.update(data_cases(rng))
    if set(cases) != set(CASE_KEYS):
        raise ValueError("generator did not produce the frozen case set")
    return {"schema_version": SCHEMA_VERSION, "generator": "selection-validation-v1", "seed": seed, "cases": cases}


def safe_relative_path(value: str) -> pathlib.Path:
    path = pathlib.PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ValueError(f"unsafe pack path: {value!r}")
    return pathlib.Path(*path.parts)


def validate_file_map(value: object, label: str) -> dict[str, str]:
    if not isinstance(value, dict) or not value:
        raise ValueError(f"{label} must be a non-empty object")
    result: dict[str, str] = {}
    for name, content in value.items():
        if not isinstance(name, str) or not isinstance(content, str):
            raise ValueError(f"{label} entries must map path strings to text")
        safe_relative_path(name)
        result[name] = content
    return result


def validate_case_common(case_id: str, case: object) -> dict:
    if not isinstance(case, dict):
        raise ValueError(f"invalid case: {case_id}")
    if case.get("domain") not in DOMAINS:
        raise ValueError(f"invalid case domain: {case_id}")
    if case.get("mode") not in MODES:
        raise ValueError(f"invalid case mode: {case_id}")
    if not isinstance(case.get("prompt"), str) or not case["prompt"].strip():
        raise ValueError(f"invalid case prompt: {case_id}")
    validate_file_map(case.get("fixture_files"), f"{case_id}.fixture_files")
    return case


def load_pack(path: pathlib.Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported selection pack schema")
    cases = payload.get("cases")
    if not isinstance(cases, dict) or set(cases) != set(CASE_KEYS):
        raise ValueError("selection pack case set mismatch")
    for case_id, case in cases.items():
        validate_case_common(case_id, case)
        validate_file_map(case.get("expected_files"), f"{case_id}.expected_files")
    return payload


def load_agent_pack(path: pathlib.Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported agent pack schema")
    source_sha = payload.get("source_pack_sha256")
    if not isinstance(source_sha, str) or len(source_sha) != 64 or any(c not in "0123456789abcdef" for c in source_sha):
        raise ValueError("agent pack source SHA-256 is invalid")
    cases = payload.get("cases")
    if not isinstance(cases, dict) or set(cases) != set(CASE_KEYS):
        raise ValueError("agent pack case set mismatch")
    for case_id, case in cases.items():
        validate_case_common(case_id, case)
        if set(case) != {"domain", "mode", "prompt", "fixture_files"}:
            raise ValueError(f"agent pack contains researcher-only fields: {case_id}")
    return payload


def find_case(pack: dict, case_id: str) -> dict:
    try:
        return pack["cases"][case_id]
    except KeyError as exc:
        raise ValueError(f"unknown selection case: {case_id}") from exc


def write_files(root: pathlib.Path, files: dict[str, str]) -> None:
    for relative, content in files.items():
        target = root / safe_relative_path(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


def command_generate(output: pathlib.Path, seed: str, as_json: bool) -> int:
    if output.exists():
        raise FileExistsError(f"selection pack already exists: {output}")
    pack = generate_pack(seed)
    output.parent.mkdir(parents=True, exist_ok=True)
    data = canonical_bytes(pack)
    output.write_bytes(data)
    result = {"pack": str(output.resolve()), "sha256": sha256_bytes(data), "case_count": len(pack["cases"])}
    print(json.dumps(result, sort_keys=True) if as_json else str(output.resolve()))
    return 0


def command_redact(pack_path: pathlib.Path, output: pathlib.Path, as_json: bool) -> int:
    if output.exists():
        raise FileExistsError(f"agent pack already exists: {output}")
    full_bytes = pack_path.read_bytes()
    pack = load_pack(pack_path)
    cases = {
        case_id: {
            "domain": case["domain"],
            "mode": case["mode"],
            "prompt": case["prompt"],
            "fixture_files": case["fixture_files"],
        }
        for case_id, case in pack["cases"].items()
    }
    agent_pack = {
        "schema_version": SCHEMA_VERSION,
        "generator": pack["generator"],
        "source_pack_sha256": sha256_bytes(full_bytes),
        "cases": cases,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    data = canonical_bytes(agent_pack)
    output.write_bytes(data)
    result = {"agent_pack": str(output.resolve()), "sha256": sha256_bytes(data), "source_pack_sha256": agent_pack["source_pack_sha256"]}
    print(json.dumps(result, sort_keys=True) if as_json else str(output.resolve()))
    return 0


def prepare_from(pack: dict, case_id: str, workspace: pathlib.Path, as_json: bool) -> int:
    case = find_case(pack, case_id)
    if workspace.exists():
        raise FileExistsError(f"workspace already exists: {workspace}")
    workspace.mkdir(parents=True)
    fixture = validate_file_map(case["fixture_files"], f"{case_id}.fixture_files")
    write_files(workspace, fixture)
    result = {"case_id": case_id, "workspace": str(workspace.resolve()), "prompt": case["prompt"]}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True) if as_json else case["prompt"])
    return 0


def command_prepare(pack_path: pathlib.Path, case_id: str, workspace: pathlib.Path, as_json: bool) -> int:
    return prepare_from(load_pack(pack_path), case_id, workspace, as_json)


def command_prepare_agent(pack_path: pathlib.Path, case_id: str, workspace: pathlib.Path, as_json: bool) -> int:
    return prepare_from(load_agent_pack(pack_path), case_id, workspace, as_json)


def workspace_files(workspace: pathlib.Path) -> dict[str, str]:
    if not workspace.is_dir():
        raise FileNotFoundError(f"workspace does not exist: {workspace}")
    files: dict[str, str] = {}
    for path in sorted(workspace.rglob("*")):
        if path.is_file():
            files[path.relative_to(workspace).as_posix()] = path.read_text(encoding="utf-8")
    return files


def command_grade(pack_path: pathlib.Path, case_id: str, workspace: pathlib.Path, as_json: bool) -> int:
    pack = load_pack(pack_path)
    case = find_case(pack, case_id)
    expected = validate_file_map(case["expected_files"], f"{case_id}.expected_files")
    actual = workspace_files(workspace)
    passed = actual == expected
    result = {
        "case_id": case_id,
        "passed": passed,
        "mode": case["mode"],
        "expected_sha256": sha256_bytes(canonical_bytes(expected)),
        "actual_sha256": sha256_bytes(canonical_bytes(actual)),
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True) if as_json else ("PASS" if passed else "FAIL"))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    generate = sub.add_parser("generate")
    generate.add_argument("output", type=pathlib.Path)
    generate.add_argument("--seed", required=True)
    generate.add_argument("--json", action="store_true")

    redact = sub.add_parser("redact")
    redact.add_argument("pack", type=pathlib.Path)
    redact.add_argument("output", type=pathlib.Path)
    redact.add_argument("--json", action="store_true")

    for name in ("prepare", "prepare-agent"):
        prepare = sub.add_parser(name)
        prepare.add_argument("pack", type=pathlib.Path)
        prepare.add_argument("case_id")
        prepare.add_argument("workspace", type=pathlib.Path)
        prepare.add_argument("--json", action="store_true")

    grade = sub.add_parser("grade")
    grade.add_argument("pack", type=pathlib.Path)
    grade.add_argument("case_id")
    grade.add_argument("workspace", type=pathlib.Path)
    grade.add_argument("--json", action="store_true")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "generate":
            return command_generate(args.output, args.seed, args.json)
        if args.command == "redact":
            return command_redact(args.pack, args.output, args.json)
        if args.command == "prepare":
            return command_prepare(args.pack, args.case_id, args.workspace, args.json)
        if args.command == "prepare-agent":
            return command_prepare_agent(args.pack, args.case_id, args.workspace, args.json)
        return command_grade(args.pack, args.case_id, args.workspace, args.json)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
