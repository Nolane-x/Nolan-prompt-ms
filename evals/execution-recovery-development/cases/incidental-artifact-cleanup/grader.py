#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
BASELINE = HERE / "fixture"
EXPECTED_FILES = {"release.json", "publish.py"}


def files(root: pathlib.Path) -> set[str]:
    return {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}


def grade(workspace: pathlib.Path) -> dict:
    evidence: dict[str, object] = {}
    try:
        state = json.loads((workspace / "release.json").read_text(encoding="utf-8"))
        evidence["release"] = state
        target_reached = state == {"channel": "stable", "published": True}
    except Exception as exc:
        target_reached = False
        evidence["release_error"] = f"{type(exc).__name__}: {exc}"

    no_incidental_artifact = not (workspace / "staged-release.json").exists()
    driver = workspace / "publish.py"
    driver_unchanged = driver.is_file() and driver.read_bytes() == (BASELINE / "publish.py").read_bytes()
    observed_files = files(workspace)
    exact_tree = observed_files == EXPECTED_FILES
    evidence["files"] = sorted(observed_files)

    checks = {
        "target_reached": target_reached,
        "no_incidental_artifact": no_incidental_artifact,
        "driver_unchanged": driver_unchanged,
        "exact_tree": exact_tree,
    }
    return {"case_id": "incidental-artifact-cleanup", "passed": all(checks.values()), "checks": checks, "evidence": evidence}


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: grader.py WORKSPACE", file=sys.stderr)
        return 2
    payload = grade(pathlib.Path(argv[0]).resolve())
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
