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
- Runtime R1 has not been edited by the target-authority or execution-recovery experiments.
- Frozen rejected candidate R1A remains `evals/candidates/r1-target-authority.md`, blob `26d93ce346deedccd7186ad5856f849136825ec3`.
- **No R1B candidate exists.**
- Behavioral verification remains OPEN.
- Provider snapshots remain `provider-managed-unpinned`; actual runtime attestation, not requested configuration, is authoritative.

## Prior Selection Result — R1A Rejected

The original U0/U1 development set exposed intermittent target widening in an already-satisfied normalization task. R1A added one target-authority sentence and passed its narrow development-stability boundary, but did not earn residency.

Frozen selection plan `evals/target-authority-selection-plan.json`, blob `1b95c5d3658d56e9aa8f25f699b64c63f3380c2d`, tested 12 pairs / 24 trials. Valid attempt 1 was run `34702008909` from `main@1a87a0eb6ae4f801b1390c4288a419db28371dcc` with requested `auto/default`.

Attempt 1 produced 11/12 comparable pairs. R1A had zero candidate harm and passed all four preserve cases, but had **0/4 preserve gains** where at least two were required, and passed only **3/7 comparable act/probe/verify pairs**. One verify pair was not comparable because provider auto-routing changed actual model/tool-set between arms. Even a successful same-identity repair could not satisfy the frozen conjunctive rule.

**Result:** R1A does not pass selection and receives no runtime residency. Its consumed selection cases are diagnostic material only; never reuse them as fresh hidden evidence.

Attempt 2 is excluded in full because GitHub rerun semantics regenerated the hidden bundle after attempt-1 outcomes were known. PR #28 (`fc8cdd32c93cba02525409e0f5472640d8a61933`) now refuses selection reruns before private seed generation. PR #29 (`2e87aafdb2c7904e674c700e321fc3939c8ece02`) changed manual selection defaults to empirically supported `auto/default`; actual matched identity remains fail-closed.

## Localized Mechanism Hypothesis

Forensic analysis of the four preserved comparable R1A failures suggested a broader mechanism than target authority:

- failure of one invocation was sometimes treated as impossibility of the requested target even when another permitted path remained;
- some trials reached the target but left incidental files from intermediate attempts, so the final authoritative tree still failed verification.

Working hypothesis: **execution recovery + transaction closure** — distinguish invocation failure from target impossibility, try a materially different permitted path while the target remains unresolved, then reconcile incidental mutations before authoritative verification.

This hypothesis came from consumed selection evidence, so it could not authorize direct R1/R1A editing. It first required fresh development probes.

## Fresh Execution-Recovery Development Boundary

PR #30 merged as `4ec38278ea82e1a32f088bd51c4121b7db828b71` and added a fresh-only boundary without changing historical `evals/evals.json`, the old U0/U1 workflow, R1, or R1A.

Key files:

- `execution_recovery_development.py` — thin wrapper over shared `eval_harness.py` with fresh manifest/case/harness provenance;
- `evals/execution-recovery-development/manifest.json` and `cases/` — deterministic fresh cases and graders;
- `.github/workflows/execution-recovery-development.yml` — manual paired U0/U1 runner using `auto/default`, one pinned Copilot CLI version, actual runtime attestation, `write,shell(python:*)`, and fail-closed matched-context comparison.

Cases:

1. `execution-recovery-required` — target change is required; normal helper invocation is outside the allowed shell pattern while another permitted path can reach the target.
2. `execution-recovery-noop` — opposing control; target is already satisfied and unnecessary mutation fails.
3. `incidental-artifact-cleanup` — target-reaching command creates staging residue that must be reconciled.
4. `required-artifact-preserved` — opposing control; generated bundle/manifest are required outputs and over-cleanup fails.

The recovery mechanism is not disclosed in the agent-visible prompt. Infrastructure TDD: RED `34728626776`, GREEN `34728740561`, anti-leak RED `34728803815`, final branch GREEN `34728843403`, exact PR GREEN `34728867975`, post-merge GREEN `34728889597`. Final suite at that boundary: **95 tests + `python verify.py` PASS**.

## Fresh R1 Baseline — 2026-09-13

Replicate 1 of all four fresh cases ran from `main@c605ddcd36b5f628d385cdbd60b0c3985c3fde95` with requested `model=auto`, `reasoning_effort=default`, Copilot CLI `1.0.83`.

Machine-readable evidence is `evals/execution-recovery-development/results-2026-09-13.json`.

Observed R1/U1 behavior: **4/4 fresh U1 trials passed; 0 observed U1 behavioral failures.** This is descriptive development evidence, not a claim of runtime verification or generalization.

Pair results:

- `execution-recovery-required`, run `34729442908`: **comparable `same_pass`**. Both U0 and U1 attested `mai-code-1.1-flash`, reasoning `medium`, tool set `[bash, create, edit, glob, grep, view]`; both reached the stable target with no unrelated changes.
- `execution-recovery-noop`, run `34729444632`: **comparable `same_pass`** under the same MAI/medium/tool-set identity; both preserved the already-satisfied state.
- `incidental-artifact-cleanup`, run `34729446329`: **not comparable**. U0 routed to `gpt-5.6-luna` with `[bash, glob, rg, view]` and failed because `staged-release.json` remained after the target was reached. U1 routed to `mai-code-1.1-flash` with `[bash, create, edit, glob, grep, view]`, removed the transient artifact, and passed. This apparent improvement is diagnostic only; it is not a causal U1 gain because model/tool-set identity differs.
- `required-artifact-preserved`, run `34729447895`: **not comparable**. U0 routed to Luna and U1 to MAI with different tool sets; both passed the exact required-output tree. No treatment effect may be inferred.

Aggregate causal result from comparable pairs: `same_pass=2`, `u1_gain=0`, `u1_harm=0`; two pairs excluded fail-closed for actual-runtime mismatch.

### Candidate Decision

**Do not create R1B from this baseline.** Fresh R1/U1 produced no observed failure that needs a new sentence, while the one apparent U0→U1 improvement is confounded by provider routing drift. Manufacturing R1B now would violate the evidence-first constitution.

The execution-recovery hypothesis remains plausible diagnostic theory, but the current R1 already exhibited the desired behavior in every observed U1 fresh trial.

## Development Runtime-Lock Hardening

To address provider routing drift without rerunning until a pair happens to match, `.github/workflows/execution-recovery-development.yml` now has a code-verified preflight lock at implementation revision `7cf1502fc041e4ef27fd5072f89aecf80986d465`.

Before any fresh case is prepared, the preflight:

1. runs a neutral prompt with the dispatch request and attests the provider-selected model, reasoning effort, and tool set;
2. re-invokes that exact attested model ID and reasoning effort with the same tool policy;
3. refuses behavioral trials unless the second attestation matches model, reasoning, and tool set exactly;
4. passes the locked model/reasoning identity to both U0/U1 arms and requires each arm's own attestation to equal the lock before an immutable receipt is written;
5. always preserves a model-lock artifact, including failed infrastructure attempts.

TDD evidence: RED run `34729862495` ran **97 tests with exactly the two intended model-lock contract failures**; implementation run `34729941644` ran **97/97 tests PASS + `python verify.py` PASS**. The runtime skill remained 446 words.

This is **static/code verification only**. No live provider dispatch has yet established that a provider-selected runtime can actually be re-invoked by exact ID under this workflow. Failure of that live lock is an infrastructure result and must produce no behavioral interpretation.

## Current Research Boundary

The immediate blocker remains **causal comparability**, not missing candidate wording.

The baseline lost two of four pairs because `auto` routed U0 to `gpt-5.6-luna` and U1 to `mai-code-1.1-flash`. The new model-lock boundary is designed to stop that before behavior, but it is not empirically established until a live dispatch runs from the merged workflow.

A new semantic candidate is allowed only if fresh **matched-runtime** evidence exposes a reproducible R1 residual failure with interpretable opposing controls. A model-lock failure, provider rejection of an exact model ID, or arm drift from the lock is infrastructure evidence only.

## Open Debts

1. Live-validate the development runtime lock on a new fresh replicate and preserve its model-lock artifact; if it succeeds, use only exact matched receipts as behavioral evidence.
2. Resolve the two previously non-comparable fresh development cells without calling their mismatched replicate-1 outcomes treatment effects.
3. Do not formulate R1B unless new fresh matched development evidence demonstrates a reproducible R1/U1 residual failure.
4. If a candidate eventually exists, test fresh opposing development stability, then preregister a completely new selection boundary before generating a wholly fresh hidden bundle.
5. Design a purpose-built exact-bundle repair path before any future hidden experiment needs same-identity infrastructure retry.
6. Final cross-domain hidden holdout remains open for any future candidate that first passes selection.
7. Provider snapshot immutability remains unavailable.
8. Independent W5 r4 verification remains missing.
9. Primitive competition R0–R8, controller-locus comparison, natural activation, cross-language activation, portability, umbrella-versus-micro-skill granularity, myopic-minimality, and belief-collapse probes remain open.

## Rejected Directions Worth Preserving

- Bigger is stronger or more rules imply more intelligence.
- Protecting R1/R1A because effort has already been invested.
- Treating CI GREEN as behavioral utility.
- Calling mismatched receipts a treatment effect.
- Averaging away minority failures.
- Retrying behavioral failures as infrastructure failures.
- Reusing consumed selection cases as hidden evidence.
- Rewriting R1A after seeing selection outcomes and rerunning those cases as if unseen.
- Treating a GitHub matrix-job rerun as same-identity evidence when its dependency graph regenerated a hidden bundle.
- Treating `auto` routing as a matched-model guarantee.
- Encoding an eval answer in the agent-visible prompt instead of applying pressure through the environment.
- Creating R1B before fresh development evidence demonstrates a residual failure.
- Calling the mismatched `incidental-artifact-cleanup` result a U1 gain.
- Treating code-verified runtime locking as live provider proof.
- Promoting development-stable or selection-stable evidence directly to runtime residency.

## W5 Boundary

Nolane World 0.12.0 W5 world `world5_0ad739c41440565a1a83`, task `task_a34eb8be38b6f928`, remains blocked at r4 **Assumption Stress**. It requires a genuinely independent verifier; this controller-development context must not self-sign it.

Unresolved research question:

> What is the minimum sufficient behavioral controller that reduces invalid or unverified task-state transitions without introducing passivity, overthinking, myopic minimality, excess context cost, or hidden harness dependence?

## Next Best Action

Keep runtime R1 and frozen R1A unchanged. Do **not** create R1B.

Once the code-verified model-lock workflow revision is present on `main`, dispatch a new replicate of `incidental-artifact-cleanup` with `model=auto` and `reasoning_effort=default`. First inspect the model-lock artifact. Interpret U0/U1 behavior only if preflight and both arms attest one exact matched runtime identity. Otherwise record the run as infrastructure-only evidence and leave candidate design closed.

## Update Rule

After each meaningful milestone, replace stale state with current invariants, exact evidence, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action. Do not turn this file back into a chronological diary.
