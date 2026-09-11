#!/usr/bin/env python3
"""Deterministic repository invariant checks for Nolane Prompt MS."""

from __future__ import annotations

import pathlib
import re
import sys

REQUIRED = ("SKILL.md", "CONSTITUTION.md", "EVALS.md", "STATE.md", "README.md")
MAX_SKILL_WORDS = 500


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def gate(text: str, label: str) -> str:
    match = re.search(rf"\*\*{re.escape(label)}(?: gate)?(?::\*\*|\*\*:)[ \t]*(OPEN|CLOSED)", text, re.I)
    return match.group(1).upper() if match else "OPEN"


def valid_skill_name(name: str) -> bool:
    return (
        1 <= len(name) <= 64
        and re.fullmatch(r"[a-z0-9-]+", name) is not None
        and name[0] != "-"
        and name[-1] != "-"
        and "--" not in name
    )


def verify(root: pathlib.Path) -> list[str]:
    errors: list[str] = []

    for required_name in REQUIRED:
        if not (root / required_name).is_file():
            fail(errors, f"missing required file: {required_name}")
    if errors:
        return errors

    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    state = (root / "STATE.md").read_text(encoding="utf-8")
    evals = (root / "EVALS.md").read_text(encoding="utf-8")

    fm = frontmatter(skill)
    if fm is None:
        fail(errors, "SKILL.md frontmatter is missing or malformed")
    else:
        name = fm.get("name", "")
        description = fm.get("description", "")
        if not valid_skill_name(name):
            fail(errors, "SKILL.md frontmatter name violates Agent Skills naming constraints")
        if not description.startswith("Use when"):
            fail(errors, "SKILL.md frontmatter description must start with 'Use when'")
        if len(description) > 500:
            fail(errors, "SKILL.md frontmatter description exceeds 500 characters")

    words = len(skill.split())
    if words > MAX_SKILL_WORDS:
        fail(errors, f"SKILL.md has {words} words; limit is {MAX_SKILL_WORDS}")

    count_match = re.search(r"\*\*Core skill word count:\*\*\s*(\d+)", state)
    if not count_match:
        fail(errors, "STATE.md is missing Core skill word count")
    elif int(count_match.group(1)) != words:
        fail(errors, f"STATE.md word count is {count_match.group(1)} but SKILL.md has {words}")

    state_gate = gate(state, "Behavioral verification")
    eval_gates = {
        "RED baseline": gate(evals, "RED baseline"),
        "GREEN comparison": gate(evals, "GREEN comparison"),
        "Ablation": gate(evals, "Ablation"),
        "Cross-domain holdout": gate(evals, "Cross-domain holdout"),
    }
    if state_gate == "CLOSED" and any(value != "CLOSED" for value in eval_gates.values()):
        open_gates = ", ".join(label for label, value in eval_gates.items() if value != "CLOSED")
        fail(errors, f"Behavioral verification gate is CLOSED while eval gates remain OPEN: {open_gates}")

    return errors


def main(argv: list[str]) -> int:
    root = pathlib.Path(argv[1] if len(argv) > 1 else ".").resolve()
    errors = verify(root)
    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS")
    print(f"- SKILL.md words: {len((root / 'SKILL.md').read_text(encoding='utf-8').split())}/{MAX_SKILL_WORDS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
