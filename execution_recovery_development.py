#!/usr/bin/env python3
"""Fresh execution-recovery development harness using the shared eval machinery."""

from __future__ import annotations

import pathlib
import sys

import eval_harness as base

ROOT = pathlib.Path(__file__).resolve().parent
MANIFEST = ROOT / "evals" / "execution-recovery-development" / "manifest.json"
CASES = ROOT / "evals" / "execution-recovery-development" / "cases"
HARNESS = pathlib.Path(__file__).resolve()

# Keep the generic receipt/config implementation while binding this experiment's
# own manifest, cases and harness provenance. Historical evals stay immutable.
base.MANIFEST = MANIFEST
base.CASES = CASES
base.HARNESS = HARNESS


if __name__ == "__main__":
    raise SystemExit(base.main(sys.argv[1:]))
