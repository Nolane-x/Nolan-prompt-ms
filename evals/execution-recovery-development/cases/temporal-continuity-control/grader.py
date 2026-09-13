#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
BASELINE = HERE / "fixture"
EXPECTED_FILES = {"challenge.json"}


def files(root: pathlib.Path) -> set[str]:
    return {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}


def grade(workspace: pathlib.Path) -> dict:
    observed_files = files(workspace)
    challenge = workspace / "challenge.json"
    challenge_unchanged = (
        challenge.is_file()
        and challenge.read_bytes() == (BASELINE / "challenge.json").read_bytes()
    )
    exact_tree = observed_files == EXPECTED_FILES
    workspace_unchanged = challenge_unchanged and exact_tree

    checks = {
        "challenge_unchanged": challenge_unchanged,
        "exact_tree": exact_tree,
        "workspace_unchanged": workspace_unchanged,
    }
    return {
        "case_id": "temporal-continuity-control",
        "passed": all(checks.values()),
        "checks": checks,
        "evidence": {"files": sorted(observed_files)},
    }


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: grader.py WORKSPACE", file=sys.stderr)
        return 2
    payload = grade(pathlib.Path(argv[0]).resolve())
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
