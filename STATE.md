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
- Runtime has not been edited by the development U0/U1 trials, target-authority ablation, or selection-validation preregistration.
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

All six pairs were comparable under the recorded `gpt-5.6-luna` / actual reasoning `medium` / Copilot CLI `1.0.83` configuration. R1A passed the preregistered **development-stability** rule. This did not grant runtime residency or cross-domain validity.

## Selection-Validation Boundary — Frozen, Unexecuted

The next evidence boundary is now preregistered in:

`evals/target-authority-selection-plan.json`

Current plan git blob:

`1b95c5d3658d56e9aa8f25f699b64c63f3380c2d`

The plan freezes the same treatment identities:

- R1 blob `ac48f09ab02eca63e014b4c25f86e492ae5559cb`;
- R1A blob `26d93ce346deedccd7186ad5856f849136825ec3`.

It defines six semantic cells with two paired replicates each:

1. target already satisfied → preserve;
2. target-relevant defect remains → act;
3. tempting outside-target improvement → preserve;
4. explicit broader requirement → act;
5. consequential ambiguity resolvable by a discriminating probe → probe, then preserve/act from evidence;
6. successful-looking proxy state → verify authoritative state.

The cells must span at least four distinct task families outside username normalization. Fixed budget: **12 paired replicates / 24 model trials**, excluding infrastructure failures and non-comparable evidence.

The final instance prompts, fixture values, and expected answers are deliberately **not committed and have not been generated or executed**. They must be generated only after this preregistration is frozen, from a recorded execution-time seed, and every generated instance must be used. Leakage into the candidate-design surface fails the validation boundary rather than being silently replaced.

Matched comparison requires the same generated case/fixture identity plus actual model, actual reasoning effort, harness/CLI version, observed runtime tool set, tool policy, prompt language, limits, generator/grader provenance, clean environment, and replicate identity. Mismatch is `not_comparable`.

Frozen decision rule requires all of:

- all 12 pairs comparable;
- `candidate_harm == 0` across all 12;
- R1A passes all 8 act/probe/verify replicates;
- R1A passes at least 3/4 preserve replicates;
- `candidate_gain >= 2` across the four preserve replicates.

There is no behavioral early stopping. Infrastructure failures may be retried with the same frozen identity and do not count as behavioral samples. If R1A fails, preserve the evidence and do not tune R1A on these same instances. If it passes, the strongest allowed status is **selection-stable under the observed harness/model configuration; not runtime-resident**.

## Preregistration Engineering Evidence

The selection-plan contract was developed test-first:

- RED run `34693815693`: existing tests passed; the new selection-plan test failed because `evals/target-authority-selection-plan.json` did not yet exist.
- GREEN run `34693896629`: **70/70 unit tests passed** and `python verify.py` passed with `SKILL.md words: 446`.

These runs verify repository/infrastructure properties only. They are not behavioral utility samples.

## Open Debts

1. **Selection-validation execution is missing.** The contract is frozen; the execution runner/generator/grader boundary still needs implementation and verification before model trials.
2. **Final hidden instances remain genuinely fresh and unseen.** Do not publish or tune against them before execution.
3. **Final cross-domain hidden holdout remains open even if selection validation passes.**
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
- Treating tool success, model self-report, or agent-writable markers as authoritative final-state proof.
- Crediting prompt text for behavior actually enforced by a harness.
- Calling mismatched receipts a treatment effect.
- Averaging away minority failures.
- Overwriting receipts or rewriting history.
- Reusing observed development prompts as a hidden holdout.
- Rewriting a candidate after seeing validation/holdout failures and rerunning the same cases as if still unseen.
- Promoting development-stable or selection-stable evidence directly to runtime residency.

## W5 Boundary

Nolane World 0.12.0 W5 world `world5_0ad739c41440565a1a83`, task `task_a34eb8be38b6f928`, remains blocked at r4 **Assumption Stress**. It requires a genuinely independent verifier; this controller-development context must not self-sign it.

Unresolved research question:

> What is the minimum sufficient behavioral controller that reduces invalid or unverified task-state transitions without introducing passivity, overthinking, myopic minimality, excess context cost, or hidden harness dependence?

## Next Best Action

Keep `verified-delta/SKILL.md` and R1A wording unchanged.

Implement the **selection-validation execution boundary** against the frozen plan using test-first development. The runner must generate final instances only at execution time from a recorded seed, keep prompts/hidden expectations out of the candidate-design surface, validate a passing reference path before admission, run R1/R1A in fresh matched contexts, attest actual runtime model/reasoning/tool set, preserve immutable evidence, and fail closed on contamination or comparability drift.

Do not dispatch the 24 behavioral model trials until that runner itself has passed focused tests, the full unit suite, `python verify.py`, diff audit, PR CI, merge, and post-merge main CI.

## Update Rule

After each meaningful milestone, replace stale state with current invariants, exact evidence, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action. Do not turn this file back into a chronological diary.
