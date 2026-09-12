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
| `EVALS.md` | Behavioral gates, pressure scenarios, and scoring contract |
| `evals/evals.json` | Preregistered executable utility cases |
| `evals/cases/` | Agent-visible fixtures plus out-of-trial deterministic graders |
| `eval_harness.py` | Lists, prepares, grades, and records U0/U1 trials; Python stdlib only |
| `CONSTITUTION.md` | Laws for editing, compressing, and validating the skill |
| `STATE.md` | Minimal cross-session boot state and open research debt |
| `verify.py` | Deterministic repository invariant checker; Python stdlib only |
| `tests/` | Regression tests for the verifier and behavioral-eval infrastructure |
| `.github/workflows/verify.yml` | Runs all repository tests and static verification on push/PR |

No source document is copied into runtime context. Research is distilled only when a mechanism survives the repository's residency rules.

## Current Status

**Alpha. Behavioral verification is still open.**

The runtime kernel remains 446 words with no runtime dependencies, model profiles, or tool-specific templates. It is packaged under `verified-delta/` so the skill name and parent directory agree. A deterministic verification layer guards mechanical invariants, and the repository now contains an executable three-case U0/U1 development lab, but neither substitutes for fresh isolated-agent behavioral comparison.

Do not describe this version as proven, best, converged, or behaviorally verified.

## Executable Utility Lab

The first development pack intentionally stays small and opposing:

- `username-normalization-noop`: the reported bug is already fixed; unnecessary production change fails.
- `username-normalization-partial`: the same report hides a remaining defect; passivity fails and a focused production change is required.
- `false-completion-state`: a command reports success while authoritative state remains wrong; proxy success fails.

Inspect the preregistered cases:

```bash
python eval_harness.py list --json
```

Create a clean agent-visible workspace:

```bash
python eval_harness.py prepare username-normalization-noop /tmp/vd-u0-r1 --json
```

Run a **fresh isolated agent/model context** against the returned prompt and workspace. For `U0`, do not load Verified Delta. For `U1`, force-load the exact current `verified-delta/SKILL.md`. The harness in this repository does not invoke a model and does not itself prove that external skill injection occurred.

Grade final workspace state outside the agent context:

```bash
python eval_harness.py grade username-normalization-noop /tmp/vd-u0-r1 --json
```

Then record an immutable trial receipt:

```bash
python eval_harness.py record \
  username-normalization-noop \
  /tmp/vd-u0-r1 \
  results/noop-pair-u0-r1.json \
  --condition U0 \
  --pair-id noop-pair \
  --replicate 1 \
  --model-id MODEL_SNAPSHOT \
  --harness-id HARNESS_VERSION \
  --transcript transcript.txt \
  --metrics metrics.json \
  --json
```

A receipt binds the individual result to its grader output, workspace hash, transcript hash, metrics, condition, model/harness identity, exact evaluator/fixture/grader/manifest digests, and — for `U1` — the SHA-256 of the runtime skill. Existing receipt paths are never overwritten. Keep every replicate, including failures; do not average away minority failures.

The clean U0/U1 execution itself remains an external evidence boundary until a genuinely fresh model/agent harness performs it.

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
