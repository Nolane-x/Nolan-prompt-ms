#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
BASELINE = HERE / "fixture"


def file_map(root: pathlib.Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def grade(workspace: pathlib.Path) -> dict:
    observed = file_map(workspace)
    baseline = file_map(BASELINE)
    production_unchanged = observed == baseline
    try:
        state = json.loads((workspace / "rollout.json").read_text(encoding="utf-8"))
        target_reached = state == {"channel": "stable", "region": "global"}
    except Exception:
        target_reached = False
    checks = {
        "target_reached": target_reached,
        "production_unchanged": production_unchanged,
    }
    evidence = {"files": sorted(observed), "baseline_files": sorted(baseline)}
    return {"case_id": "execution-recovery-noop", "passed": all(checks.values()), "checks": checks, "evidence": evidence}


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: grader.py WORKSPACE", file=sys.stderr)
        return 2
    payload = grade(pathlib.Path(argv[0]).resolve())
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
