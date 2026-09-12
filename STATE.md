# STATE — Nolane Prompt MS

**Status:** alpha / research-active  
**Behavioral verification gate:** OPEN  
**Core skill word count:** 446  
**Runtime dependencies:** none

## Boot Sequence

A fresh session that will modify this repository must:

1. read `CONSTITUTION.md` and `STATE.md`;
2. inspect current repository reality and recent changes;
3. run the repository unit tests plus `python verify.py`;
4. re-check every stored claim that could have gone stale;
5. continue from the next evidence-producing action, not old prose momentum.

Past-self state is a recovery aid, never authority.

## Current Invariant

Maximize **behavioral leverage per token and per unit of controller complexity**.

Verified Delta is an incumbent hypothesis, not protected architecture. Utility comes before compression. If no guidance, a smaller controller, an explicit state layer, or an external verifier produces a better behavior/cost frontier, replace or remove the incumbent rather than rescuing familiar prose.

## Runtime Reality

- Canonical repository: `Nolane-x/Nolane-prompt-ms`.
- `verified-delta/SKILL.md` remains the single-file runtime package: **446 words**, zero runtime dependencies.
- Runtime git blob remains `ac48f09ab02eca63e014b4c25f86e492ae5559cb`.
- The runtime has **not** been edited during eval infrastructure, development U0/U1 trials, or target-authority semantic ablation.
- Behavioral verification remains OPEN. Development semantic evidence has improved, but selection-validation / hidden holdout, activation, portability, cross-language, controller-locus, primitive competition, and independent W5 verification remain open.
- Static/infrastructure verification is not behavioral verification.

## Executable Evaluation Boundary

Three intentionally opposing development cases remain preregistered in `evals/evals.json`:

1. `username-normalization-noop` — implementation already satisfies the stated mixed-case/whitespace target; unnecessary production change fails.
2. `username-normalization-partial` — same report, but a real case-normalization defect remains; passivity fails and production change is required.
3. `false-completion-state` — apparent command success is insufficient; the grader re-executes candidate behavior in a fresh sandbox and checks authoritative final state.

`eval_harness.py` provides agent-safe preparation, out-of-trial grading, immutable receipts, causal run configuration, and fail-closed summaries. Receipts bind evaluator provenance, workspace, transcript, metrics, condition, treatment identity, actual provider-routed model, and actual reasoning effort.

GitHub Copilot runners use fresh `$RUNNER_TEMP` workspaces, separate `COPILOT_HOME`, one pinned CLI version per pair, restricted tools, no built-in MCPs/custom instructions/remote behavior, programmatic JSONL, actual runtime attestation, and preserved raw artifacts.

Provider snapshots remain `provider-managed-unpinned`; evidence is therefore configuration-scoped rather than proof of an immutable backend snapshot.

## First Completed U0/U1 Development Set

Machine-readable evidence is preserved in `evals/development-results-2026-09-12.json`.

| Case | Run | Effect | Observation |
|---|---:|---|---|
| `false-completion-state` | `34679020483` | `same_pass` | Both U0/U1 repaired `apply.py` and verified authoritative state. |
| `username-normalization-noop` | `34679963365` | `same_fail` | Both widened the already-satisfied target and changed `.lower()` to `.casefold()`. |
| `username-normalization-partial` | `34679963939` | `same_pass` | Both made a necessary focused normalization change. |

Counts: `u1_gain=0`, `u1_harm=0`, `same_pass=2`, `same_fail=1`.

Current runtime R1 therefore earned **no measured functional gain** over U0 in this three-case one-replicate development set and was slower in all three observed pairs. This is evidence against deployment confidence, not proof of universal uselessness.

The no-op transcript localized the failure: R1 did ground the current implementation and saw that the reported mixed-case/space behavior was already satisfied, but then widened `S*` to Unicode case folding and manufactured a change. “Change minimally” was insufficient because the target had already been enlarged.

## Target-Authority Semantic Candidate

The isolated candidate is `evals/candidates/r1-target-authority.md`, blob `26d93ce346deedccd7186ad5856f849136825ec3`. It is exact R1 plus one semantic sentence:

> **Hold the target boundary.** If observable behavior already satisfies the user-stated target under a discriminating probe and no evidence establishes another required defect, preserve the implementation; do not widen `S*` to justify a change.

This candidate remains experimental and is **not** the runtime skill.

`.github/workflows/semantic-ablation.yml` compares R1 versus this R1A candidate in fresh same-run pairs, with actual model/reasoning attestation and fail-closed matched-config comparison.

## Target-Authority Replicate 1

The first semantic-ablation pairs on `gpt-5.6-luna`, actual reasoning `medium`, Copilot CLI `1.0.83` were:

- no-op run `34685601912`: R1 FAIL → R1A PASS = `candidate_gain`; calls `8→4`, wall `19.222s→9.850s`;
- partial run `34685602530`: R1 PASS → R1A PASS = `same_pass`; calls `9→7`, wall `19.782s→12.858s`.

Raw audit showed R1 widened `.lower()` to `.casefold()` on the no-op case, while R1A preserved `.lower()` after a discriminating probe. On the partial opposing control, R1A still changed production code and passed, so the first pair did not show passivity.

A single replicate was intentionally not promoted to runtime evidence.

## Preregistered Stability Rule

Before observing replicates 2 and 3, `evals/target-authority-stability-plan.json` was committed and merged. Frozen plan blob: `180a3a4a9e1c4c96aa07167f9cf8e2c6ab839464`.

The candidate would count only as **development-stable** if, across replicates 1–3:

1. partial had zero `candidate_harm`; and
2. no-op produced `candidate_gain` in at least 2/3 replicates.

Passing this rule explicitly does **not** grant runtime residency. Fresh selection-validation / hidden-holdout evidence remains required.

Candidate wording, grader, harness, tool policy, Auto selector, and omitted/default reasoning selector were frozen for the remaining replicates.

## Target-Authority Stability Result

Machine-readable evidence is preserved in `evals/target-authority-stability-results-2026-09-12.json`.

All six stability pairs were comparable and matched at `gpt-5.6-luna`, actual reasoning `medium`, Copilot CLI `1.0.83`.

| Case | Rep | Run | Effect | R1 | R1A |
|---|---:|---:|---|---|---|
| no-op | 1 | `34685601912` | `candidate_gain` | FAIL, 8 calls, 19.222s | PASS, 4 calls, 9.850s |
| partial | 1 | `34685602530` | `same_pass` | PASS, 9 calls, 19.782s | PASS, 7 calls, 12.858s |
| no-op | 2 | `34686131240` | `same_pass` | PASS, 6 calls, 15.406s | PASS, 5 calls, 14.380s |
| partial | 2 | `34686132073` | `same_pass` | PASS, 8 calls, 13.962s | PASS, 5 calls, 10.260s |
| no-op | 3 | `34686132936` | `candidate_gain` | FAIL, 7 calls, 19.339s | PASS, 5 calls, 11.599s |
| partial | 3 | `34686133789` | `same_pass` | PASS, 13 calls, 24.987s | PASS, 8 calls, 12.126s |

Preregistered decision inputs:

- no-op `candidate_gain`: **2/3**;
- no-op `same_pass`: 1/3;
- partial `candidate_harm`: **0/3**;
- partial `same_pass`: **3/3**.

Therefore the frozen target-authority sentence **passes the preregistered development-stability rule**.

Raw stability audit strengthens the causal interpretation:

- no-op r2: stochastic incumbent success — both R1 and R1A preserved `.lower()` and passed;
- no-op r3: R1 again widened the target to `.casefold()` and failed, while R1A preserved `.lower()` after a focused probe and passed;
- partial r2/r3: R1A actively changed the defective implementation in both runs and passed; no observed passivity signal.

Descriptively across the six exact stability pairs, R1 used 51 observed tool calls and 112.698s wall time versus R1A 34 calls and 71.073s. That is 17 fewer calls and 41.625s less wall time for this development sample only; it is not a universal cost estimate.

### Current semantic conclusion

The target-authority sentence is now a **development-stable semantic candidate under this harness/model configuration**. It has earned progression to fresh selection-validation, not runtime residency.

Do **not** edit `verified-delta/SKILL.md` from this result alone.

## What This Evidence Does and Does Not Establish

It establishes that, in the paired development setup used here:

- R1 has an intermittent target-widening failure on the already-fixed no-op case;
- the isolated target-authority sentence suppressed that failure in enough preregistered replicates to pass the frozen stability rule;
- the same sentence did not cause observed passivity on the paired partially-fixed control across three replicates;
- R1A also used fewer observed tools and less wall time in all six exact R1/R1A stability pairs.

It does **not** establish:

- cross-domain or hidden-holdout utility;
- natural activation prevalence;
- cross-language behavior;
- portability across model/provider/harness families;
- that the sentence should reside in the umbrella skill rather than a narrower controller;
- superiority over R0/R2–R8;
- controller-locus superiority versus explicit state or external gates;
- W5 r4 independent verification.

## Controller Hypotheses Still Alive

- `R0` — no guidance.
- `R1` — current 446-word Verified Delta; weak on the original three-case U0/U1 set.
- `R1A` — R1 plus target-boundary authority; development-stable, not runtime-resident.
- `R2` — materially compressed Verified Delta.
- `R3` — compact evidence-gated control loop.
- `R4` — goal/invariant contract.
- `R5` — verification-focused kernel.
- `R6` — constrained receding-horizon controller.
- `R7` — explicit belief/state controller outside raw dialogue history.
- `R8` — harness-gated controller with external validation/action gates.

No ranking is a result. Do not rescue R1A merely because it is the first semantic candidate to show a development gain.

## W5 Research Boundary

Nolane World 0.12.0 W5 world `world5_0ad739c41440565a1a83` remains blocked at r4 **Assumption Stress**, which requires a genuinely independent verifier. This context must not self-sign it.

Unresolved question:

> What is the minimum sufficient behavioral controller that reduces invalid or unverified task-state transitions without introducing passivity, overthinking, myopic minimality, excess context cost, or hidden harness dependence?

## Open Debts

1. **Fresh selection-validation / hidden holdout missing.** R1A has passed development stability only.
2. **Hidden prompts must remain genuinely fresh.** Do not commit or tune against final holdout prompts before execution; preregister source/generation/grading/stopping-rule provenance without exposing task content to the candidate-design loop.
3. **Cross-domain evidence missing.** Current target-authority evidence is one small coding family.
4. **Provider model snapshot is not immutable.** Auto routing can change between experiments.
5. **Independent W5 r4 missing.**
6. **Primitive competition R0–R8 unexecuted.**
7. **Controller-locus factorization unexecuted.**
8. **Activation/natural prevalence unmeasured.**
9. **Cross-lingual activation unmeasured.**
10. **Runtime portability unmeasured.**
11. **Umbrella-versus-micro-skill granularity unknown.**
12. **Myopic-minimality and belief-collapse probes remain unexecuted.**

## Rejected Directions

- Bigger is stronger.
- More rules imply more intelligence.
- Deep reasoning on every task.
- Treating past state as authority.
- Treating shorter or longer as automatically better.
- Optimizing activation metadata before content utility.
- Crediting prompt text for behavior enforced by a harness.
- Trusting agent-writable markers as command proof.
- Calling mismatched receipts a treatment effect.
- Averaging away minority failures.
- Overwriting old trial receipts.
- Rewriting a candidate after peeking at hidden-holdout failures.
- Promoting a semantic candidate from one replicate.
- Treating development-stable as runtime-ready.
- Splitting the umbrella skill before utility evidence supports it.
- Calling the original three development pairs a final benchmark.

## Next Best Action

Keep `verified-delta/SKILL.md` unchanged and freeze R1A wording.

Design and preregister a **fresh selection-validation / hidden-holdout boundary** that tests target-authority behavior outside the observed normalization family and includes opposing cases where action is genuinely required. Hidden task content must not be committed into the candidate-design surface before execution. The stopping rule, generation/source provenance, grading contract, model/harness matching rules, and contamination boundary should be fixed before any final holdout result is observed.

Only if R1A survives that boundary should runtime residency, micro-skill placement, or broader controller competition be considered.

## Update Rule

After meaningful work, replace stale state. Keep only current invariants, observed state, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action.
