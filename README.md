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
| `.github/workflows/behavioral-u0-u1.yml` | Manual-only fresh U0/U1 runner using GitHub Copilot CLI |
| `CONSTITUTION.md` | Laws for editing, compressing, and validating the skill |
| `STATE.md` | Minimal cross-session boot state and open research debt |
| `verify.py` | Deterministic repository invariant checker; Python stdlib only |
| `tests/` | Regression tests for the verifier and behavioral-eval infrastructure |
| `.github/workflows/verify.yml` | Runs all repository tests and static verification on push/PR |

No source document is copied into runtime context. Research is distilled only when a mechanism survives the repository's residency rules.

## Current Status

**Alpha. Behavioral verification is still open.**

The runtime kernel remains 446 words with no runtime dependencies, model profiles, or tool-specific templates. It is packaged under `verified-delta/` so the skill name and parent directory agree. A deterministic verification layer guards mechanical invariants, and the repository contains an executable three-case U0/U1 development lab.

A manual fresh-runner workflow now exists, but **no behavioral trial has been dispatched yet**. Merging or pushing the workflow does not invoke Copilot. A manual dispatch can consume GitHub Copilot requests/credits and requires an account/repository policy that permits Copilot CLI in Actions.

Do not describe this version as proven, best, converged, or behaviorally verified.

## Executable Utility Lab

The first development pack intentionally stays small and opposing:

- `username-normalization-noop`: the reported bug is already fixed; unnecessary production change fails.
- `username-normalization-partial`: the same report hides a remaining defect; passivity fails and a focused production change is required.
- `false-completion-state`: a command reports success while authoritative state remains wrong; proxy success fails.

### Orchestrator boundary

Inspect preregistered cases from the **orchestrator/researcher side**:

```bash
python eval_harness.py list --json
```

Do not expose the full repository, manifest, graders, or `list` output to the evaluated agent. The agent-facing handoff is the output of `prepare` plus the copied workspace.

Create a clean agent-visible workspace:

```bash
python eval_harness.py prepare username-normalization-noop /tmp/vd-u0-r1 --json
```

`prepare --json` intentionally returns only `case_id`, `workspace`, and `prompt`; it does not return the research-side `expected_output` field.

Run a **fresh isolated agent/model context** against that prompt and workspace. For `U0`, do not load Verified Delta. For `U1`, force-load the exact current `verified-delta/SKILL.md`.

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

Each canonical value is either a non-negative integer or `null` when the external harness genuinely cannot observe it. Additional provider-specific metrics may be retained. Missing canonical keys, negative values, booleans, or stringified numbers are rejected rather than silently normalized.

Every receipt also requires a structured `run-config.json` with three roles:

- `matched` — causal context held equal across U0/U1: prompt language, provider/model/snapshot, harness/version, tools and tool policy, reasoning/sampling controls, and resource limits;
- `intervention` — delivery metadata expected to differ by condition (`none` for U0, `force-loaded-skill` for U1), plus metadata/body language, description variant, and available-skill-set hash;
- `trial` — per-run provenance such as clean-environment ID, trial ID, and UTC timestamp.

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

`record` validates the run-config schema, cross-checks model/harness identity and delivery form against the receipt condition, and binds both a canonical full-config SHA-256 and a separate `matched` SHA-256. A receipt also binds grader output, final workspace hash, transcript hash, metrics, condition, exact evaluator/fixture/grader/manifest digests, and — for `U1` — the SHA-256 of the runtime skill. Existing receipt paths are never overwritten.

### Summarize without averaging away harm

```bash
python eval_harness.py summarize results/*.json --json
```

The summary groups by `case_id + pair_id`, preserves each replicate, and classifies a matched replicate as one of:

- `u1_gain`: U0 fails and U1 passes;
- `u1_harm`: U0 passes and U1 fails;
- `same_pass`: both pass;
- `same_fail`: both fail.

It deliberately emits no global score. Missing or tampered run-config evidence is rejected. Two individually valid receipts whose matched causal context differs are `not_comparable`, as are missing conditions, evaluator-provenance mismatches, and duplicate receipts for the same condition/replicate.

## Manual Fresh U0/U1 Runner

`.github/workflows/behavioral-u0-u1.yml` is a **manual `workflow_dispatch` workflow only**. It never runs on push or pull request.

Before any model call it validates the replicate/model inputs and resolves one Copilot CLI package version for the whole pair. U0 and U1 then run as separate GitHub-hosted jobs with clean `$RUNNER_TEMP` workspaces and separate `COPILOT_HOME` directories. Both install the exact same resolved CLI version, model name, reasoning effort, tool set, tool policy, and time budget.

The treatment difference is intentionally narrow:

- **U0** receives only the task prompt;
- **U1** receives the exact current `verified-delta/SKILL.md`, followed by the same task prompt.

The runner disables built-in MCPs, custom instructions, remote sessions/export, experimental behavior, interactive questioning, and unrestricted tool approval. It restricts available tools and places the evaluated workspace outside the repository checkout.

Each successful model invocation is converted into the same immutable receipt contract used by the local harness. If Copilot CLI itself exits nonzero, the workflow records an infrastructure error and does **not** create a behavioral receipt. Raw artifacts are retained even on failure. A final job downloads both condition artifacts and runs `eval_harness.py summarize`; missing or non-comparable receipts fail closed while preserving a pair-summary artifact.

Important limitations:

- dispatching can consume Copilot requests/credits and is therefore an explicit experimental action, not part of normal CI;
- the Copilot CLI package version is pinned per pair, but the requested model backend is reported honestly as `provider-managed-unpinned` unless the provider exposes a stronger immutable snapshot identity;
- token and tool-call counts remain `null` when Copilot CLI does not expose reliable values; they are never estimated;
- one clean pair is development evidence, not portability, cross-domain, activation, or final holdout evidence.

The current conversation has seen the skill, cases, and graders, so it must not substitute itself for this fresh runner.

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

If an idea cannot be justified by behavioral evaluation and the repository's controller-residency rules, it does not belong in the core.
