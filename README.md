# Nolane Prompt MS

A tiny, model-agnostic agent skill built around one idea:

> **Verified Delta:** move from current truth to desired truth with the smallest sufficient change, preserve invariants, verify reality, then stop.

This repository deliberately optimizes **behavioral leverage per token**, not rule count.

## Why

Large skill libraries can become expensive to load, hard to audit, internally repetitive, and easy to turn into checklists that agents perform ceremonially.

Nolane Prompt MS takes the opposite approach: compress research into a small kernel whose sentences must prove they change behavior.

## Files

| File | Responsibility |
|---|---|
| `SKILL.md` | Runtime behavior loaded by an agent |
| `EVALS.md` | RED/GREEN pressure scenarios and scoring |
| `CONSTITUTION.md` | Laws for editing, compressing, and validating the skill |
| `STATE.md` | Minimal cross-session boot state and open research debt |

No source document is copied into runtime context. Research is distilled only when a mechanism survives the repository's residency rules.

## Current Status

**Alpha. Behavioral verification is still open.**

The first kernel is 446 words and has no dependencies, scripts, model profiles, or tool-specific templates. `EVALS.md` defines the required baseline and comparison tests, but fresh isolated RED/GREEN runs have not yet been completed.

Do not describe this version as proven, best, converged, or behaviorally verified.

## Development Rule

Before changing the skill:

1. read `CONSTITUTION.md` and `STATE.md`;
2. inspect current repository reality;
3. identify one demonstrated failure;
4. test a minimal wording change;
5. ablate it;
6. keep it only if behavior worsens without it;
7. update `STATE.md`;
8. stop.

“Research a million times for one word” is treated as a **quality standard**, never as a fabricated iteration count.

## Non-Goals

This is not a prompt-template library, model catalog, QX runtime, multi-agent framework, memory platform, or general best-practices encyclopedia.

If an idea cannot be compressed into the Verified Delta primitive and justified by evaluation, it does not belong in the core.
