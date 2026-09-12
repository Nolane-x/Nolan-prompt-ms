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
| `evals/evals.json` | Preregistered executable development utility cases |
| `evals/target-authority-selection-plan.json` | Frozen, machine-readable cross-domain selection-validation contract; contains no final hidden task content |
| `evals/target-authority-selection-results-2026-09-12.json` | Preserved attempt-1 selection evidence, rejection basis, provenance, and excluded-attempt boundary |
| `evals/cases/` | Agent-visible development fixtures plus out-of-trial deterministic graders |
| `eval_harness.py` | Lists, prepares, grades, records, and summarizes U0/U1 trials; Python stdlib only |
| `semantic_ablation.py` | Records and summarizes matched R1/R1A semantic-ablation trials |
| `selection_validation.py` | Generates fresh seeded selection instances, admits references, prepares agent-safe workspaces, records immutable arm receipts, and evaluates the frozen decision rule |
| `selection_process_evidence.py` | Derives grader-visible process evidence from structured Copilot tool-execution events rather than model prose |
| `.github/workflows/behavioral-u0-u1.yml` | Manual-only fresh U0/U1 runner using GitHub Copilot CLI |
| `.github/workflows/semantic-ablation.yml` | Manual-only R1/R1A development ablation runner |
| `.github/workflows/target-authority-selection.yml` | Manual-only 12-pair / 24-arm frozen selection-validation runner |
| `CONSTITUTION.md` | Laws for editing, compressing, and validating the skill |
| `STATE.md` | Minimal cross-session boot state and open research debt |
| `verify.py` | Deterministic repository invariant checker; Python stdlib only |
| `tests/` | Regression tests for the verifier and behavioral-eval infrastructure |
| `.github/workflows/verify.yml` | Runs all repository tests and static verification on push/PR |

No source document is copied into runtime context. Research is distilled only when a mechanism survives the repository's residency rules.

## Current Status

**Alpha. Behavioral verification is still open.**

The runtime kernel remains **446 words**, has no runtime dependencies, and remains git blob `ac48f09ab02eca63e014b4c25f86e492ae5559cb`. It has not been edited by the evaluation work described below.

The first three-case U0/U1 development set found no measured functional gain for current runtime R1 over no guidance and exposed an intermittent no-op target-widening failure. A frozen R1A candidate — exact R1 plus one target-authority sentence — then passed its preregistered three-replicate development-stability rule on the opposing normalization pair. That was **development evidence only**.

R1A has now reached its frozen cross-domain selection boundary. Run `34702008909`, attempt 1, requested Copilot `auto/default`; preflight attested actual `gpt-5.6-luna` with reasoning `medium`, and the workflow generated the hidden bundle only after that preflight. All 24 arm jobs produced immutable receipts.

The frozen summary found **11/12 comparable pairs**. One verify pair was fail-closed as `not_comparable` because provider auto-routing sent the R1 arm to `mai-code-1.1-flash` while the matched R1A arm routed to `gpt-5.6-luna`, with different actual tool sets. The formal summary is therefore infrastructure-invalid rather than a complete 12-pair causal estimate.

The comparable behavioral evidence is nevertheless sufficient to reject R1A under the preregistered conjunctive rule. All four preserve pairs were `same_pass`, so R1A produced **0/4 preserve candidate gains** against a frozen minimum of 2. Across the seven comparable act/probe/verify pairs, R1A passed only 3 and failed 4; even perfect repair of the one non-comparable verify pair could raise that to at most 4/8, below the required 8/8. Candidate harm was 0 and preserve passes were 4/4, but those checks are not sufficient on their own.

Therefore R1A **does not pass the frozen selection-validation boundary and is not promoted to runtime residency**. The exact result/provenance is recorded in `evals/target-authority-selection-results-2026-09-12.json`. Runtime R1 remains unchanged because no replacement has earned residency, not because R1 has been proven.

A later GitHub rerun attempt unexpectedly restarted the workflow dependency graph and regenerated a new hidden bundle after attempt-1 outcomes had already been observed. That attempt is excluded in full and must never be combined with attempt-1 evidence. The rerun boundary must be hardened before the next hidden experiment.

Do not describe this version as proven, best, converged, behaviorally verified, cross-domain validated, or runtime-ready.

## Executable Utility Lab

The original development pack intentionally stays small and opposing:

- `username-normalization-noop`: the reported bug is already fixed; unnecessary production change fails.
- `username-normalization-partial`: the same report hides a remaining defect; passivity fails and a focused production change is required.
- `false-completion-state`: a command reports success while authoritative state remains wrong; proxy success fails.

### Orchestrator boundary

Inspect preregistered development cases from the **orchestrator/researcher side**:

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

- `matched` — causal context held equal across paired arms: prompt language, provider/model/snapshot, harness/version, tools and tool policy, reasoning/sampling controls, and resource limits;
- `intervention` — delivery metadata expected to differ by condition, plus metadata/body language, description variant, and available-skill-set hash;
- `trial` — per-run provenance such as clean-environment ID, trial ID, and UTC timestamp.

Then record an immutable trial receipt. `record` validates the run-config schema, cross-checks model/harness identity and delivery form against the receipt condition, and binds both a canonical full-config SHA-256 and a separate `matched` SHA-256. A receipt also binds grader output, final workspace hash, transcript hash, metrics, condition, exact evaluator/fixture/grader/manifest digests, and treatment identity. Existing receipt paths are never overwritten.

### Summarize without averaging away harm

```bash
python eval_harness.py summarize results/*.json --json
```

The U0/U1 summary preserves each replicate and classifies a matched replicate as one of:

- `u1_gain`: U0 fails and U1 passes;
- `u1_harm`: U0 passes and U1 fails;
- `same_pass`: both pass;
- `same_fail`: both fail.

The R1/R1A semantic-ablation and selection summaries analogously use `candidate_gain`, `candidate_harm`, `same_pass`, and `same_fail`. Missing or tampered run-config evidence is rejected. Individually valid receipts whose matched causal context differs are `not_comparable`; minority failures are never averaged away.

## Manual Fresh Runners

The Copilot behavioral workflows are **manual `workflow_dispatch` workflows only**. Normal push/PR CI does not invoke model trials.

Before target-authority selection can generate hidden cases, the runner validates the requested model/reasoning configuration, resolves one Copilot CLI package version, installs that exact version in a preflight job, performs a minimal model call, and attests the actual model/reasoning/tool set. A rejected or mismatched runtime configuration stops there, before hidden seed generation.

For target-authority selection, the production workflow generates one private execution seed internally after preflight. `selection_validation.py generate` still accepts an explicit seed as its deterministic researcher/test API, but dispatch does not accept that seed and trial jobs do not receive it. The admitted bundle creates exactly twelve cases and a dynamic 24-arm matrix. Every reference path must pass before behavioral trials.

For each trial, the hidden bundle is used only to prepare the visible workspace and prompt and is then deleted. The repository checkout is also scrubbed before inference, so the evaluated agent cannot inspect the generator, alternate treatment, repository state, or hidden grader material. The model runs only against its prepared task workspace. After inference, a trusted checkout and the exact admitted hidden bundle are restored for runtime attestation, structured process-evidence extraction, deterministic grading, and immutable receipt creation. `PYTHONDONTWRITEBYTECODE=1` prevents incidental Python bytecode files from contaminating workspace hashes.

The runners disable built-in MCPs, custom instructions, remote sessions/export, experimental behavior, interactive questioning, and unrestricted tool approval. They preserve raw artifacts even on failure. A nonzero Copilot CLI exit is infrastructure failure, not a behavioral sample.

Important limitations:

- dispatching can consume Copilot requests/credits and is therefore an explicit experimental action, not normal CI;
- the CLI package version is pinned per matched execution, but the backend snapshot remains `provider-managed-unpinned` unless the provider exposes stronger immutable identity;
- provider `auto` routing can differ across arm jobs, so actual-model and actual-tool-set comparability must remain fail-closed;
- token counts remain `null` when the harness cannot observe them reliably; they are never estimated;
- development stability is not cross-domain validation, portability, activation, or final-holdout evidence;
- consumed selection cases are diagnostic material only and cannot be reused as hidden evidence;
- even a passing future selection run would grant only **selection-stable under the observed harness/model configuration; not runtime-resident**.

The current conversation has seen the development skill/cases/graders and the attempt-1 selection summary, so it must not substitute itself for a fresh evaluated-agent context.

## Development Rule

Before changing runtime behavior:

1. read `CONSTITUTION.md` and `STATE.md`;
2. inspect current repository reality;
3. run the full unit suite and `python verify.py`;
4. identify one demonstrated behavioral failure;
5. test a minimal semantic intervention;
6. ablate it;
7. keep it only if behavior worsens without it under a preregistered comparison;
8. advance through fresh selection/holdout boundaries without tuning on observed holdout failures;
9. update `STATE.md`, rerun verification, and stop at the current evidence boundary.

“Research a million times for one word” is treated as a **quality standard**, never as a fabricated iteration count.

## Non-Goals

This is not a prompt-template library, model catalog, QX runtime, multi-agent framework, memory platform, or general best-practices encyclopedia.

If an idea cannot be justified by behavioral evaluation and the repository's controller-residency rules, it does not belong in the core.
