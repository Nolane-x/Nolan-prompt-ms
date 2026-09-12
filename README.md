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
| `eval_harness.py` | Lists, prepares, grades, records, and summarizes U0/U1 trials; Python stdlib only |
| `CONSTITUTION.md` | Laws for editing, compressing, and validating the skill |
| `STATE.md` | Minimal cross-session boot state and open research debt |
| `verify.py` | Deterministic repository invariant checker; Python stdlib only |
| `tests/` | Regression tests for the verifier and behavioral-eval infrastructure |
| `.github/workflows/verify.yml` | Runs all repository tests and static verification on push/PR |

No source document is copied into runtime context. Research is distilled only when a mechanism survives the repository's residency rules.

## Current Status

**Alpha. Behavioral verification is still open.**

The runtime kernel remains 446 words with no runtime dependencies, model profiles, or tool-specific templates. It is packaged under `verified-delta/` so the skill name and parent directory agree. A deterministic verification layer guards mechanical invariants, and the repository contains an executable three-case U0/U1 development lab, but neither substitutes for fresh isolated-agent behavioral comparison.

Do not describe this version as proven, best, converged, or behaviorally verified.

## Executable Utility Lab

The first development pack intentionally stays small and opposing:

- `username-normalization-noop`: the reported bug is already fixed; unnecessary production change fails.
- `username-normalization-partial`: the same report hides a remaining defect; passivity fails and a focused production change is required.
- `false-completion-state`: a command reports success while authoritative state remains wrong; proxy success fails.

### Orchestrator boundary

Inspect the preregistered cases from the **orchestrator/researcher side**:

```bash
python eval_harness.py list --json
```

Do not expose the full repository, manifest, graders, or `list` output to the evaluated agent merely because the orchestrator can see them. The agent-facing handoff is the output of `prepare` plus the copied workspace.

Create a clean agent-visible workspace:

```bash
python eval_harness.py prepare username-normalization-noop /tmp/vd-u0-r1 --json
```

`prepare --json` intentionally returns only `case_id`, `workspace`, and `prompt`; it does not return the research-side `expected_output` field.

Run a **fresh isolated agent/model context** against that prompt and workspace. For `U0`, do not load Verified Delta. For `U1`, force-load the exact current `verified-delta/SKILL.md`. The harness in this repository does not invoke a model and does not itself prove that external skill injection occurred.

Grade final workspace state outside the agent context:

```bash
python eval_harness.py grade username-normalization-noop /tmp/vd-u0-r1 --json
```

### Record every trial

The metrics file supplied to `record` must contain these four canonical keys:

```json
{
  "input_tokens": 100,
  "output_tokens": 20,
  "tool_calls": 2,
  "wall_time_ms": 500
}
```

Each canonical value must be either a non-negative integer or `null` when the external harness genuinely cannot observe it. Additional provider-specific metrics may be retained. Missing canonical keys, negative values, booleans, or stringified numbers are rejected rather than silently normalized.

Every receipt also requires a structured `run-config.json`. It has three roles:

- `matched` — causal context that must be held equal across U0/U1, including prompt language, provider/model/snapshot, harness/version, tools and tool policy, reasoning/sampling controls, and resource limits;
- `intervention` — delivery-form metadata that is expected to differ by condition (`none` for U0, `force-loaded-skill` for U1), plus metadata/body language, description variant, and available-skill-set hash;
- `trial` — per-run provenance such as clean-environment ID, trial ID, and UTC timestamp.

Example shape:

```json
{
  "schema_version": 1,
  "matched": {
    "prompt_language": "en",
    "model": {"provider": "provider", "id": "model", "snapshot": "snapshot"},
    "harness": {"id": "runner", "version": "1.0.0"},
    "tool_set": ["python", "shell"],
    "tool_policy": {"workspace_only": true},
    "reasoning_effort": "high",
    "sampling_controls": {"temperature": 0},
    "limits": {"wall_time_ms": 60000, "max_output_tokens": 4000}
  },
  "intervention": {
    "delivery_form": "none",
    "metadata_language": null,
    "body_language": null,
    "description_variant": null,
    "available_skill_set_sha256": null
  },
  "trial": {
    "clean_environment_id": "clean-u0-r1",
    "trial_id": "noop-pair-u0-r1",
    "timestamp_utc": "2026-09-12T05:00:00Z"
  }
}
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
  --model-id MODEL_ID \
  --harness-id HARNESS_ID \
  --transcript transcript.txt \
  --metrics metrics.json \
  --run-config run-config.json \
  --json
```

`pair-id`, `model-id`, and `harness-id` must be non-empty, and `replicate` starts at 1. `record` validates the run-config schema, cross-checks model/harness identity and delivery form against the receipt condition, and binds both a canonical full-config SHA-256 and a separate `matched` SHA-256. A receipt also binds grader output, final workspace hash, transcript hash, metrics, condition, exact evaluator/fixture/grader/manifest digests, and — for `U1` — the SHA-256 of the runtime skill. Existing receipt paths are never overwritten.

### Summarize without averaging away harm

Once matched receipts exist, summarize them directly:

```bash
python eval_harness.py summarize results/*.json --json
```

The summary groups by `case_id + pair_id`, preserves each replicate, and classifies a matched replicate as exactly one of:

- `u1_gain`: U0 fails and U1 passes;
- `u1_harm`: U0 passes and U1 fails;
- `same_pass`: both pass;
- `same_fail`: both fail.

It deliberately does **not** emit one global score. Missing or tampered run-config evidence is rejected. Two internally valid receipts whose matched causal context differs are `not_comparable`, as are missing conditions, evaluator-provenance mismatches, and duplicate receipts for the same condition/replicate. This prevents input ordering or configuration drift from manufacturing a treatment effect.

The clean U0/U1 execution itself remains an external evidence boundary until a genuinely fresh model/agent harness performs it. A hardened receipt proves what was recorded; it does **not** prove that an external model invocation or skill injection actually occurred as claimed. Preserve transcripts and independent runner evidence.

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
