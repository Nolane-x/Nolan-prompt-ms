#!/usr/bin/env python3
"""Derive grading evidence only from Copilot tool-execution events.

This module deliberately ignores assistant prose. It converts raw JSONL tool events into
a minimal trusted transcript that the frozen selection grader can consume without
crediting model self-report as evidence of probing or authoritative-state reads.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

import selection_validation as selection

EXTRACTOR = pathlib.Path(__file__).resolve()
READ_TOKENS = ("cat ", "jq ", "grep ", "head ", "tail ", "read_text", "open(", "print(")


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def iter_events(path: pathlib.Path):
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, start=1):
            if not raw.strip():
                continue
            try:
                event = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON on line {line_number}: {exc.msg}") from exc
            if not isinstance(event, dict):
                raise ValueError(f"event on line {line_number} must be an object")
            yield event


def flatten_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, nested in value.items():
            if isinstance(key, str):
                yield key
            yield from flatten_strings(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from flatten_strings(nested)


def tool_events(path: pathlib.Path) -> list[dict]:
    records = []
    for event in iter_events(path):
        if event.get("type") != "tool.execution_start":
            continue
        data = event.get("data")
        if not isinstance(data, dict):
            raise ValueError("tool.execution_start data must be an object")
        tool_name = data.get("toolName")
        if not isinstance(tool_name, str) or not tool_name.strip():
            # Keep the parser fail-closed if the provider changes this event schema.
            raise ValueError("tool.execution_start is missing toolName")
        rendered = " ".join(flatten_strings(data)).lower()
        records.append({"tool_name": tool_name.strip().lower(), "rendered": rendered})
    return records


def has_probe_execution(records: list[dict]) -> bool:
    return any(
        record["tool_name"] == "bash"
        and "probe.py" in record["rendered"]
        and "python" in record["rendered"]
        for record in records
    )


def has_authoritative_release_verification(records: list[dict]) -> tuple[bool, bool]:
    publish_index = None
    for index, record in enumerate(records):
        if (
            record["tool_name"] == "bash"
            and "publish.py" in record["rendered"]
            and "python" in record["rendered"]
        ):
            publish_index = index
            break
    if publish_index is None:
        return False, False

    for record in records[publish_index + 1 :]:
        rendered = record["rendered"]
        if "release.json" not in rendered:
            continue
        if record["tool_name"] == "view":
            return True, True
        if record["tool_name"] == "bash" and any(token in rendered for token in READ_TOKENS):
            return True, True
    return True, False


def extract_case_evidence(bundle: pathlib.Path, case_id: str, events: pathlib.Path) -> dict:
    if not events.is_file():
        raise FileNotFoundError(f"events file does not exist: {events}")
    manifest = selection.load_bundle(bundle)
    case = selection.find_case(manifest, case_id)
    case_root = selection.validate_case_provenance(bundle, case)
    grader = json.loads((case_root / "hidden" / "grader.json").read_text(encoding="utf-8"))
    required = grader.get("transcript_required")
    if not isinstance(required, list) or any(not isinstance(value, str) for value in required):
        raise ValueError("grader transcript_required must be a list of strings")

    records = tool_events(events)
    markers: list[str] = []
    checks: dict[str, bool] = {}

    if required == []:
        passed = True
    elif required == ["probe.py"]:
        observed = has_probe_execution(records)
        checks["probe_executed_by_tool"] = observed
        if observed:
            markers.append("tool-event verified: python probe.py")
        passed = observed
    elif required == ["publish.py", "release.json"]:
        published, verified = has_authoritative_release_verification(records)
        checks["publish_executed_by_tool"] = published
        checks["release_state_read_after_publish"] = verified
        if published:
            markers.append("tool-event verified: python publish.py")
        if verified:
            markers.append("tool-event verified: release.json authoritative read")
        passed = published and verified
    else:
        raise ValueError(f"unsupported frozen process-evidence contract: {required!r}")

    trusted_transcript = ""
    if markers:
        trusted_transcript = "\n".join(
            [
                f"events_sha256={sha256_file(events)}",
                f"extractor_sha256={sha256_file(EXTRACTOR)}",
                *markers,
            ]
        ) + "\n"

    return {
        "schema_version": 1,
        "experiment": manifest["experiment"],
        "case_id": case_id,
        "cell_id": case["cell_id"],
        "required_markers": required,
        "passed": passed,
        "checks": checks,
        "events_sha256": sha256_file(events),
        "extractor_sha256": sha256_file(EXTRACTOR),
        "tool_event_count": len(records),
        "trusted_transcript": trusted_transcript,
    }


def command_extract(
    bundle: pathlib.Path,
    case_id: str,
    events: pathlib.Path,
    output: pathlib.Path,
    as_json: bool,
) -> int:
    if output.exists():
        raise FileExistsError(f"trusted evidence output already exists: {output}")
    evidence = extract_case_evidence(bundle, case_id, events)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(evidence["trusted_transcript"], encoding="utf-8")
    if as_json:
        print(json.dumps(evidence, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(str(output.resolve()))
    # Missing process evidence is a behavioral result, not an infrastructure error.
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    extract = subparsers.add_parser("extract")
    extract.add_argument("bundle", type=pathlib.Path)
    extract.add_argument("case_id")
    extract.add_argument("events", type=pathlib.Path)
    extract.add_argument("output", type=pathlib.Path)
    extract.add_argument("--json", action="store_true")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "extract":
            return command_extract(args.bundle, args.case_id, args.events, args.output, args.json)
        raise ValueError(f"unsupported command: {args.command}")
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
