#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
BASELINE = HERE / "fixture"
EXPECTED_FILES = {"rollout.json", "promote.sh"}


def files(root: pathlib.Path) -> set[str]:
    return {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}


def grade(workspace: pathlib.Path) -> dict:
    evidence: dict[str, object] = {}
    rollout = workspace / "rollout.json"
    try:
        state = json.loads(rollout.read_text(encoding="utf-8"))
        evidence["rollout"] = state
        target_reached = state == {"channel": "stable", "region": "global"}
    except Exception as exc:
        target_reached = False
        evidence["rollout_error"] = f"{type(exc).__name__}: {exc}"

    observed_files = files(workspace)
    helper = workspace / "promote.sh"
    helper_unchanged = helper.is_file() and helper.read_bytes() == (BASELINE / "promote.sh").read_bytes()
    no_unrelated_changes = observed_files == EXPECTED_FILES and helper_unchanged
    evidence["files"] = sorted(observed_files)

    checks = {
        "target_reached": target_reached,
        "no_unrelated_changes": no_unrelated_changes,
    }
    return {"case_id": "execution-recovery-required", "passed": all(checks.values()), "checks": checks, "evidence": evidence}


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: grader.py WORKSPACE", file=sys.stderr)
        return 2
    payload = grade(pathlib.Path(argv[0]).resolve())
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
