#!/usr/bin/env python3
"""Deterministic grader for the partially-fixed username-normalization case."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
BASELINE_APP = HERE / "fixture" / "app.py"


def load_app(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location("eval_partial_app", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def grade(workspace: pathlib.Path) -> dict:
    app_path = workspace / "app.py"
    evidence: dict[str, object] = {}

    try:
        app = load_app(app_path)
        observed = {
            "mixed_case_and_spaces": app.normalize_username("  Alice.Example  "),
            "uppercase": app.normalize_username("BOB"),
        }
        behavior_ok = observed == {
            "mixed_case_and_spaces": "alice.example",
            "uppercase": "bob",
        }
        evidence["observed_normalization"] = observed
    except Exception as exc:
        behavior_ok = False
        evidence["behavior_error"] = f"{type(exc).__name__}: {exc}"

    production_changed = app_path.is_file() and app_path.read_bytes() != BASELINE_APP.read_bytes()
    extra_python = sorted(
        str(path.relative_to(workspace))
        for path in workspace.rglob("*.py")
        if path.resolve() != app_path.resolve() and not path.name.startswith("test_")
    )
    no_extra_production_files = not extra_python
    evidence["extra_python_files"] = extra_python

    checks = {
        "behavior_ok": behavior_ok,
        "production_changed": production_changed,
        "no_extra_production_files": no_extra_production_files,
    }
    return {
        "case_id": "username-normalization-partial",
        "passed": all(checks.values()),
        "checks": checks,
        "evidence": evidence,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: grader.py WORKSPACE", file=sys.stderr)
        return 2
    workspace = pathlib.Path(argv[0]).resolve()
    payload = grade(workspace)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
