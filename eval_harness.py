#!/usr/bin/env python3
"""Small, model-agnostic utilities for Verified Delta behavioral evals."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
MANIFEST = ROOT / "evals" / "evals.json"


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    list_parser = subparsers.add_parser("list", help="list preregistered eval cases")
    list_parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "list":
        return command_list(args.as_json)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
