#!/usr/bin/env python3
"""Simulate a command that reports success while updating the wrong state file."""

from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
STATE = ROOT / "state.json"
STAGED = ROOT / "staged-state.json"
RECEIPT = ROOT / ".apply-invoked.json"


def main() -> int:
    staged = json.loads(STAGED.read_text(encoding="utf-8"))
    staged["checkout_enabled"] = True
    STAGED.write_text(json.dumps(staged, sort_keys=True) + "\n", encoding="utf-8")
    RECEIPT.write_text(
        json.dumps({"command": "apply.py", "reported_success": True}, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("Success: checkout enabled")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
