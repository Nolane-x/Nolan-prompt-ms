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
- Runtime has not been edited by the development U0/U1 trials, target-authority ablation, selection preregistration, or selection execution-infrastructure work.
- Behavioral verification remains OPEN.
- Provider model snapshots remain `provider-managed-unpinned`; requested configuration must never be substituted for runtime attestation.

## Development Evidence Already Observed

The original development set in `evals/development-results-2026-09-12.json` contains three one-replicate U0/U1 cases:

- `false-completion-state`, run `34679020483`: `same_pass`;
- `username-normalization-noop`, run `34679963365`: `same_fail`;
- `username-normalization-partial`, run `34679963939`: `same_pass`.

Counts were `u1_gain=0`, `u1_harm=0`, `same_pass=2`, `same_fail=1`. R1 therefore earned no measured functional gain over U0 in that small development set.

The no-op failure localized an intermittent mechanism: R1 grounded the current implementation but enlarged the user-stated target from mixed-case/whitespace normalization to Unicode case folding, then manufactured a production change.

## Frozen R1A Candidate

`evals/candidates/r1-target-authority.md` remains blob `26d93ce346deedccd7186ad5856f849136825ec3`. It is exact R1 plus:

> **Hold the target boundary.** If observable behavior already satisfies the user-stated target under a discriminating probe and no evidence establishes another required defect, preserve the implementation; do not widen `S*` to justify a change.

R1A is experimental and is not the runtime skill.

The three-replicate target-authority stability result is preserved in `evals/target-authority-stability-results-2026-09-12.json`:

- no-op `candidate_gain`: **2/3**;
- no-op `same_pass`: 1/3;
- partial `candidate_harm`: **0/3**;
- partial `same_pass`: **3/3**.

All six pairs were comparable under the recorded `gpt-5.6-luna` / actual reasoning `medium` / Copilot CLI `1.0.83` development configuration. R1A passed the preregistered **development-stability** rule. This did not grant runtime residency or cross-domain validity.

## Selection-Validation Boundary — Frozen

The next behavioral evidence boundary is preregistered in `evals/target-authority-selection-plan.json`, blob `1b95c5d3658d56e9aa8f25f699b64c63f3380c2d`.

The plan freezes:

- R1 blob `ac48f09ab02eca63e014b4c25f86e492ae5559cb`;
- R1A blob `26d93ce346deedccd7186ad5856f849136825ec3`;
- six semantic cells with two paired replicates each;
- **12 paired replicates / 24 model trials** excluding infrastructure failures and non-comparable evidence;
- matched causal dimensions, contamination rule, no behavioral early stopping, and the literal decision rule.

The semantic cells are: target already satisfied → preserve; target-relevant defect remains → act; tempting outside-target improvement → preserve; explicit broader requirement → act; consequential ambiguity → probe then preserve/act from evidence; successful-looking proxy → verify authoritative state.

Frozen decision rule requires all 12 pairs comparable, `candidate_harm == 0`, all 8 act/probe/verify R1A replicates passing, at least 3/4 preserve R1A replicates passing, and at least 2 `candidate_gain` results among the four preserve pairs.

Infrastructure failures may be retried without becoming behavioral samples. Behavioral failures must be preserved and must not be used to retune R1A on the same hidden instances. Even a pass grants at most **selection-stable under the observed harness/model configuration; not runtime-resident**.

## First Dispatch — Invalid Infrastructure Run, No Behavioral Evidence

Manual run `34699852491` was dispatched from `main@e8a1c1fe6d1e2ba43d643cdde2c5d0be15d2940b` with explicit model `gpt-5.6-luna`, reasoning `medium`, and seed `selection-98cad77b1b9b496186f2fcefc9ffbaff`.

`validate`, `generate`, and `resolve` succeeded, but Copilot CLI `1.0.83` rejected the model before successful inference:

`Error: Model "gpt-5.6-luna" from --model flag is not available.`

Trial jobs therefore failed at the receipt boundary with nonzero Copilot exits. Raw evidence was preserved, but no valid behavioral receipts were produced. This run is **infrastructure failure only**. It does not count toward the frozen behavioral budget and it must not be summarized as R1 or R1A performance.

The failed run also exposed a stronger experiment-integrity issue in the original workflow: the externally supplied seed was present in the trial environment while the repository generator remained checked out during inference. Because the evaluated agent had bounded Python shell access, that surface was unnecessarily reconstructible even though the hidden bundle itself had been deleted.

## Hardened Selection Execution Boundary — Integrated

PR #26 integrated the infrastructure fix into `main` as merge commit `7f57d587c8490ad966e487134c7052a3ad9f9532` without changing R1, R1A, the frozen plan, generator semantics, graders, or decision rule.

The hardened workflow now:

- removes `execution_seed` from `workflow_dispatch` and from every trial environment;
- defaults to named `gpt-5.4` with reasoning `medium`, while runtime attestation remains authoritative;
- resolves one Copilot CLI version and runs a minimal model/reasoning preflight **before** any hidden seed or bundle is generated;
- fails before hidden generation if the requested named model is rejected or attests to a different runtime configuration;
- creates a fresh seed internally with `secrets.token_hex(32)` only after preflight succeeds, records it in researcher-side generation/bundle evidence, and never passes it to the evaluated agent;
- admits all reference paths before behavioral trials;
- prepares the visible workspace and exact arm prompt, deletes the hidden bundle, then scrubs the entire repository checkout before inference;
- runs the evaluated model only against the prepared task workspace;
- sets `PYTHONDONTWRITEBYTECODE=1` to prevent incidental Python bytecode from contaminating workspace hashes;
- restores a trusted checkout and re-downloads the exact hidden bundle only after inference for attestation, process-evidence extraction, grading, and immutable receipt creation;
- still requires exactly 24 valid receipts before the frozen summary can produce a decision.

TDD and integration evidence:

- test-only commit `2e077cdca04cf8b67270ec5fcea93fa24409d669` → run `34700203085` RED with exactly four new workflow-boundary failures while prior tests remained green;
- implementation commit `76fa7741ce6c525b321b72bbbd6c60a822392298` → run `34700371261` GREEN;
- final PR head `ad2b33527368d6b56cb4015dc38e161959d62a81` → push run `34700509229` GREEN with **88/88 tests** plus `python verify.py`;
- exact PR-triggered run `34700561438` GREEN on the same head;
- post-merge `main@7f57d587c8490ad966e487134c7052a3ad9f9532` run `34700580459` GREEN, including the full unit suite and `python verify.py`.

These runs are infrastructure evidence only, not selection behavioral evidence.

## Earlier Selection Infrastructure Evidence

PR #25 merged the original execution boundary into `main` as `e62fde30b6fb722cd122d1041b1179fe7da2f790` after exact-head merge-ref run `34698483551` passed **87/87 tests** plus `python verify.py`. Post-merge run `34698546154` independently passed **87/87 tests** plus `python verify.py`; later state reconciliation landed at `e8a1c1fe6d1e2ba43d643cdde2c5d0be15d2940b`.

Earlier RED→GREEN infrastructure evidence includes `34694922809` → `34694999546` for generator existence, `34695242624` → `34695380305` for immutable receipts/decision evaluation, `34695452037` → `34695562998` for manual workflow contract, and `34695602489` / `34695720095` → `34695877200` for trusted process-evidence plumbing. `34698281819` was GREEN after structured-argument hardening.

## Open Debts

1. **The frozen 24-trial selection-validation experiment still has no valid behavioral run.** Infrastructure is integrated and green; the next evidence-producing action is one manual dispatch using `gpt-5.4` / `medium`, gated by the new preflight.
2. Final hidden instances for the valid run must remain fresh and unseen by the evaluated agent. Do not publish or tune against them before execution.
3. Final cross-domain hidden holdout remains open even if selection validation passes.
4. Provider snapshot immutability remains unavailable.
5. Independent W5 r4 verification remains missing.
6. Primitive competition R0–R8 remains unexecuted.
7. Controller-locus comparison remains unexecuted.
8. Natural activation prevalence remains unmeasured.
9. Cross-language activation remains unmeasured.
10. Portability across provider/model/harness remains unmeasured.
11. Umbrella-versus-micro-skill granularity remains unknown.
12. Myopic-minimality and belief-collapse probes remain unexecuted.

## Rejected Directions Worth Preserving

- Bigger is stronger or more rules imply more intelligence.
- Protecting R1/R1A because effort has already been invested.
- Treating CI GREEN as behavioral utility.
- Treating tool success, model self-report, command-looking metadata, or agent-writable markers as authoritative final-state proof.
- Crediting prompt text for behavior actually enforced by a harness.
- Calling mismatched receipts a treatment effect.
- Averaging away minority failures.
- Overwriting receipts or rewriting history.
- Reusing observed development prompts as a hidden holdout.
- Rewriting a candidate after seeing validation/holdout failures and rerunning the same cases as if still unseen.
- Promoting development-stable or selection-stable evidence directly to runtime residency.
- Exposing a deterministic hidden-case seed or generator checkout to the evaluated agent when the orchestration layer can avoid doing so.

## W5 Boundary

Nolane World 0.12.0 W5 world `world5_0ad739c41440565a1a83`, task `task_a34eb8be38b6f928`, remains blocked at r4 **Assumption Stress**. It requires a genuinely independent verifier; this controller-development context must not self-sign it.

Unresolved research question:

> What is the minimum sufficient behavioral controller that reduces invalid or unverified task-state transitions without introducing passivity, overthinking, myopic minimality, excess context cost, or hidden harness dependence?

## Next Best Action

Keep `verified-delta/SKILL.md`, R1A wording, `selection_validation.py` case-generation semantics, and the frozen decision rule unchanged.

Manually dispatch `.github/workflows/target-authority-selection.yml` exactly once from current `main` with `model=gpt-5.4` and `reasoning_effort=medium`. Do **not** supply an execution seed; the workflow now generates it privately only after model/runtime preflight succeeds. If preflight fails, no final hidden bundle exists and the failure is infrastructure-only.

Preserve the resulting preflight, generation/admission artifacts, all immutable arm receipts, and summary exactly as observed. Retry only infrastructure failures. A behavioral failure is a valid result; a non-comparable or infrastructure-incomplete run is not a treatment result. Do not tune R1A on generated selection instances.

The current ChatGPT GitHub connector can inspect and re-run existing Actions runs but does not expose creation of a new `workflow_dispatch` event. That tooling limitation is external to the repository and is not evidence about R1/R1A.

## Update Rule

After each meaningful milestone, replace stale state with current invariants, exact evidence, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action. Do not turn this file back into a chronological diary.
