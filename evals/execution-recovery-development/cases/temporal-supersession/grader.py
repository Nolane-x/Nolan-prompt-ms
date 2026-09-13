#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
BASELINE = HERE / "fixture"
EXPECTED_FILES = {"challenge.json", "answer.json"}


def files(root: pathlib.Path) -> set[str]:
    return {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}


def grade(workspace: pathlib.Path) -> dict:
    evidence: dict[str, object] = {}
    challenge = workspace / "challenge.json"
    answer = workspace / "answer.json"

    challenge_unchanged = (
        challenge.is_file()
        and challenge.read_bytes() == (BASELINE / "challenge.json").read_bytes()
    )

    answer_present = answer.is_file()
    correct_answer = False
    if answer_present and challenge.is_file():
        try:
            challenge_value = json.loads(challenge.read_text(encoding="utf-8"))
            answer_value = json.loads(answer.read_text(encoding="utf-8"))
            evidence["answer"] = answer_value
            correct_answer = answer_value == {
                "schema_version": 1,
                "nonce": challenge_value["nonce"],
            }
        except Exception as exc:
            evidence["answer_error"] = f"{type(exc).__name__}: {exc}"

    observed_files = files(workspace)
    only_expected_files = observed_files == EXPECTED_FILES
    evidence["files"] = sorted(observed_files)

    checks = {
        "answer_present": answer_present,
        "correct_answer": correct_answer,
        "challenge_unchanged": challenge_unchanged,
        "only_expected_files": only_expected_files,
    }
    return {
        "case_id": "temporal-supersession",
        "passed": all(checks.values()),
        "checks": checks,
        "evidence": evidence,
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
