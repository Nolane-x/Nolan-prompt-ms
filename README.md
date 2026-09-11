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
| `verified-delta/SKILL.md` | Runtime skill package loaded by an agent |
| `EVALS.md` | RED/GREEN pressure scenarios, gates, and scoring |
| `CONSTITUTION.md` | Laws for editing, compressing, and validating the skill |
| `STATE.md` | Minimal cross-session boot state and open research debt |
| `verify.py` | Deterministic invariant checker; Python stdlib only |
| `tests/test_verify.py` | Regression tests for the deterministic checker |
| `.github/workflows/verify.yml` | Runs static checks on push and pull request |

No source document is copied into runtime context. Research is distilled only when a mechanism survives the repository's residency rules.

## Current Status

**Alpha. Behavioral verification is still open.**

The runtime kernel remains 446 words with no runtime dependencies, model profiles, or tool-specific templates. It is packaged under `verified-delta/` so the skill name and parent directory agree. A deterministic verification layer guards mechanical invariants, but it does **not** substitute for isolated-agent RED/GREEN behavioral evaluation.

Do not describe this version as proven, best, converged, or behaviorally verified.

## Development Rule

Before changing the skill:

1. read `CONSTITUTION.md` and `STATE.md`;
2. inspect current repository reality;
3. run `python verify.py`;
4. identify one demonstrated behavioral failure;
5. test a minimal wording change;
6. ablate it;
7. keep it only if behavior worsens without it;
8. update `STATE.md` and rerun the verifier;
9. stop.

“Research a million times for one word” is treated as a **quality standard**, never as a fabricated iteration count.

## Non-Goals

This is not a prompt-template library, model catalog, QX runtime, multi-agent framework, memory platform, or general best-practices encyclopedia.

If an idea cannot be compressed into the Verified Delta primitive and justified by evaluation, it does not belong in the core.
