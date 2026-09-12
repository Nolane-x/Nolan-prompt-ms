#!/usr/bin/env python3
"""Small, model-agnostic utilities for Verified Delta behavioral evals."""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent
MANIFEST = ROOT / "evals" / "evals.json"
CASES = ROOT / "evals" / "cases"


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def find_case(case_id: str) -> dict:
    for case in load_manifest()["cases"]:
        if case["id"] == case_id:
            return case
    raise ValueError(f"unknown eval case: {case_id}")


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
        "expected_output": case["expected_output"],
    }
    if as_json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(case["prompt"])
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "list":
            return command_list(args.as_json)
        if args.command == "prepare":
            return command_prepare(args.case_id, args.destination, args.as_json)
        raise AssertionError(args.command)
    except (FileExistsError, FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
