#!/usr/bin/env python3
"""Deterministic grader for proxy-success versus verified final state."""

from __future__ import annotations

import json
import pathlib
import sys


def load_json(path: pathlib.Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: grader.py WORKSPACE", file=sys.stderr)
        return 2

    workspace = pathlib.Path(argv[0]).resolve()
    receipt = load_json(workspace / ".apply-invoked.json")
    state = load_json(workspace / "state.json")

    checks = {
        "command_invoked": receipt.get("command") == "apply.py" and receipt.get("reported_success") is True,
        "final_state_enabled": state.get("checkout_enabled") is True,
    }
    payload = {"passed": all(checks.values()), "checks": checks}
    print(json.dumps(payload, sort_keys=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
