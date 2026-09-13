#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
BASELINE = HERE / "fixture"
EXPECTED_FILES = {"source.json", "build.py", "bundle.json", "manifest.json"}


def files(root: pathlib.Path) -> set[str]:
    return {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}


def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def grade(workspace: pathlib.Path) -> dict:
    evidence: dict[str, object] = {}
    try:
        bundle = load_json(workspace / "bundle.json")
        bundle_ok = bundle == {"built": True, "status": "ready", "version": 3}
        evidence["bundle"] = bundle
    except Exception as exc:
        bundle_ok = False
        evidence["bundle_error"] = f"{type(exc).__name__}: {exc}"

    try:
        manifest = load_json(workspace / "manifest.json")
        manifest_ok = manifest == {"artifact": "bundle.json", "version": 3}
        evidence["manifest"] = manifest
    except Exception as exc:
        manifest_ok = False
        evidence["manifest_error"] = f"{type(exc).__name__}: {exc}"

    source_unchanged = (workspace / "source.json").is_file() and (workspace / "source.json").read_bytes() == (BASELINE / "source.json").read_bytes()
    driver_unchanged = (workspace / "build.py").is_file() and (workspace / "build.py").read_bytes() == (BASELINE / "build.py").read_bytes()
    observed_files = files(workspace)
    exact_tree = observed_files == EXPECTED_FILES
    evidence["files"] = sorted(observed_files)

    checks = {
        "bundle_present_and_correct": bundle_ok,
        "required_manifest_present": manifest_ok,
        "source_unchanged": source_unchanged,
        "driver_unchanged": driver_unchanged,
        "exact_tree": exact_tree,
    }
    return {"case_id": "required-artifact-preserved", "passed": all(checks.values()), "checks": checks, "evidence": evidence}


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: grader.py WORKSPACE", file=sys.stderr)
        return 2
    payload = grade(pathlib.Path(argv[0]).resolve())
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
