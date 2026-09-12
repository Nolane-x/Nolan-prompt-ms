# STATE — Nolane Prompt MS

**Status:** alpha / research-active  
**Behavioral verification gate:** OPEN  
**Core skill word count:** 446  
**Runtime dependencies:** none

## Boot Sequence

A fresh session that will modify this repository must:

1. read `CONSTITUTION.md` and all of `STATE.md`;
2. inspect current `main`, recent commits/PRs, and the files named below;
3. run the full unit suite plus `python verify.py` before changing behavior or infrastructure;
4. re-check every stored claim that could have gone stale;
5. continue from current repository reality and the next evidence-producing action.

Past state is recovery evidence, never authority.

## Current Invariant

Maximize **behavioral leverage per token and per unit of controller complexity**.

Verified Delta is an incumbent hypothesis, not protected architecture. Utility precedes compression. Causality precedes wording. Ablation precedes residency. Verification precedes completion.

## Runtime Reality

- Canonical repository: `Nolane-x/Nolane-prompt-ms`.
- `verified-delta/SKILL.md` remains the single-file runtime package: **446 words**, zero runtime dependencies.
- Runtime git blob remains `ac48f09ab02eca63e014b4c25f86e492ae5559cb`.
- Runtime R1 has not been edited by the target-authority experiments.
- Behavioral verification remains OPEN.
- Provider snapshots remain `provider-managed-unpinned`; runtime attestation, not requested configuration, is authoritative.

## Development Evidence

The original three-case U0/U1 development set produced `u1_gain=0`, `u1_harm=0`, `same_pass=2`, `same_fail=1`. It exposed an intermittent no-op failure in which R1 enlarged a user-stated normalization target and manufactured a production change.

Frozen candidate R1A remains `evals/candidates/r1-target-authority.md`, blob `26d93ce346deedccd7186ad5856f849136825ec3`. It is exact R1 plus one target-authority sentence. On the opposing normalization development pair, three replicates produced:

- no-op: `candidate_gain` 2/3, `same_pass` 1/3;
- partial: `candidate_harm` 0/3, `same_pass` 3/3.

R1A therefore passed its preregistered **development-stability** rule. That evidence did not grant runtime residency.

## Frozen Selection Boundary

`evals/target-authority-selection-plan.json`, blob `1b95c5d3658d56e9aa8f25f699b64c63f3380c2d`, froze:

- R1 blob `ac48f09ab02eca63e014b4c25f86e492ae5559cb`;
- R1A blob `26d93ce346deedccd7186ad5856f849136825ec3`;
- six semantic cells × two paired replicates = 12 pairs / 24 model trials;
- no behavioral early stopping;
- same-identity retry only for infrastructure failures;
- decision rule: all 12 pairs comparable, zero candidate harm, R1A passes all 8 act/probe/verify replicates, R1A passes at least 3/4 preserve replicates, and at least 2 candidate gains among the four preserve pairs.

A pass could have granted only **selection-stable under the observed harness/model configuration; not runtime-resident**.

## Selection Attempt 1 — R1A Does Not Pass

Run `34702008909`, attempt 1, executed from `main@1a87a0eb6ae4f801b1390c4288a419db28371dcc` with requested `model=auto`, `reasoning_effort=default`.

Preflight succeeded and attested `gpt-5.6-luna`, reasoning `medium`, Copilot CLI `1.0.83`. Only after preflight did the workflow generate and admit the hidden bundle. The attempt-1 hidden bundle was mechanically clean, used seed `selection-78804f4808a765efb13a8081b66cd15ff0c47572f4a803d1854b453d6cc3edd6`, and has artifact SHA-256 `5db178141c5fd532a13e9894bbc64bbb5ee27d5a9fd7d5b482c80b1df989c1f6`.

All 24 arm jobs completed and created immutable receipts. The frozen summary then reported:

- 11/12 comparable pairs;
- candidate harm: 0;
- R1A preserve passes: 4/4;
- preserve candidate gains: **0/4** (frozen minimum: 2);
- R1A passes on comparable act/probe/verify pairs: **3/7**, with four preserved behavioral failures;
- `verify_authoritative_state-r2` was `not_comparable` because provider auto-routing sent R1 to `mai-code-1.1-flash` with a different actual tool set while R1A routed to `gpt-5.6-luna`.

The formal summary therefore has `infrastructure_valid=false`, because the plan requires 12 comparable pairs. Nevertheless, R1A is already unable to satisfy the frozen conjunctive decision rule from the preserved comparable behavior: all four preserve pairs are fixed `same_pass`, so the required two preserve gains cannot be reached; and four comparable act/probe/verify R1A failures are behavioral results that cannot be retried as infrastructure. Even a successful repair of the one non-comparable verify pair could raise act/probe/verify passes only to 4/8, below the required 8/8.

**Result:** R1A does **not** pass the frozen selection-validation boundary and receives **no runtime residency**. Do not retune R1A on these instances. Full machine-readable evidence is in `evals/target-authority-selection-results-2026-09-12.json`.

## Excluded Attempt 2

After attempt-1 outcomes were already observed, a GitHub “rerun one matrix job” request unexpectedly restarted the workflow dependency graph, including `generate`, and created a new hidden bundle under run attempt 2. That is not a same-identity infrastructure retry.

Attempt 2 is therefore **excluded in full** from behavioral evidence, regardless of its outputs. Never combine attempt-2 artifacts with attempt-1 receipts. The workflow must be hardened before another hidden experiment so a rerun cannot silently regenerate the selection bundle.

## Earlier Infrastructure-Only Dispatches

- Run `34699852491`: explicit `gpt-5.6-luna` was rejected by Copilot CLI before valid inference; no behavioral sample.
- Run `34701533638`: explicit `gpt-5.4` failed the new preflight before hidden generation; no behavioral sample.

These failures established that this Copilot environment can auto-route to Luna while rejecting Luna and GPT-5.4 as explicit CLI model identifiers.

## Research Consequence

R1A solved a narrow development target-widening failure but did not generalize into the frozen cross-domain selection boundary. The observed selection cases are no longer hidden. They may be used only as clearly labeled diagnostic/development material and must never be reused as a fresh hidden selection or final holdout.

Current evidence does **not** justify editing R1 from these hidden outcomes. Runtime R1 remains the incumbent only because no replacement has earned residency, not because R1 is proven.

## Open Debts

1. Harden selection rerun orchestration so any rerun reuses an exact admitted bundle or fails before regeneration.
2. Default future Copilot selection dispatches to an actually supported routing contract; avoid assuming a documented model identifier is explicitly selectable.
3. Localize the comparable act/probe/verify failures without rewriting R1A on the consumed selection instances.
4. Formulate any next candidate using fresh development probes, then preregister a new selection boundary before generating new hidden cases.
5. Final cross-domain hidden holdout remains open for any future candidate that first passes selection.
6. Provider snapshot immutability remains unavailable.
7. Independent W5 r4 verification remains missing.
8. Primitive competition R0–R8, controller-locus comparison, natural activation, cross-language activation, portability, umbrella-versus-micro-skill granularity, myopic-minimality, and belief-collapse probes remain open.

## Rejected Directions Worth Preserving

- Bigger is stronger or more rules imply more intelligence.
- Protecting R1/R1A because effort has already been invested.
- Treating CI GREEN as behavioral utility.
- Calling mismatched receipts a treatment effect.
- Averaging away minority failures.
- Retrying behavioral failures as if they were infrastructure failures.
- Reusing consumed selection cases as hidden evidence.
- Rewriting R1A after seeing this selection result and rerunning the same cases as if unseen.
- Treating a GitHub matrix-job rerun as same-identity evidence when its dependency graph regenerated the hidden bundle.
- Promoting development-stable or selection-stable evidence directly to runtime residency.

## W5 Boundary

Nolane World 0.12.0 W5 world `world5_0ad739c41440565a1a83`, task `task_a34eb8be38b6f928`, remains blocked at r4 **Assumption Stress**. It requires a genuinely independent verifier; this controller-development context must not self-sign it.

Unresolved research question:

> What is the minimum sufficient behavioral controller that reduces invalid or unverified task-state transitions without introducing passivity, overthinking, myopic minimality, excess context cost, or hidden harness dependence?

## Next Best Action

Keep runtime R1 and frozen R1A wording unchanged while closing the evidence record.

First harden the rerun boundary with a fail-closed regression test. Then analyze the preserved comparable failures as diagnostic evidence, create any new semantic candidate only through fresh development tasks, and preregister a new fresh selection experiment before hidden generation. The consumed attempt-1 cases must never serve as that new hidden set.

## Update Rule

After each meaningful milestone, replace stale state with current invariants, exact evidence, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action. Do not turn this file back into a chronological diary.
