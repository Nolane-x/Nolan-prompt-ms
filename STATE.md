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
- Behavioral verification remains OPEN.
- Provider snapshots remain `provider-managed-unpinned`; actual runtime attestation is authoritative.

## Prior Evidence That Still Matters

The original U0/U1 development set exposed intermittent target widening in the already-satisfied username-normalization case. R1A added one target-authority rule and passed its narrow opposing development-stability boundary, but that did not grant residency.

Frozen selection plan `evals/target-authority-selection-plan.json`, blob `1b95c5d3658d56e9aa8f25f699b64c63f3380c2d`, then tested 12 pairs / 24 trials. Valid attempt 1 was run `34702008909` from `main@1a87a0eb6ae4f801b1390c4288a419db28371dcc` with requested `auto/default`; preflight attested `gpt-5.6-luna`, reasoning `medium`, Copilot CLI `1.0.83`.

Attempt 1 produced 11/12 comparable pairs. R1A had zero candidate harm and passed all four preserve cases, but had **0/4 preserve gains** where at least two were required, and passed only **3/7 comparable act/probe/verify pairs**. One verify pair was not comparable because provider auto-routing changed actual model/tool-set between arms. Even a successful same-identity repair of that pair could not satisfy the frozen conjunctive rule.

**Result:** R1A does not pass selection and receives no runtime residency. Its consumed selection cases may be used only as diagnostic material, never again as fresh hidden evidence.

Attempt 2 of that run is excluded in full because GitHub rerun semantics regenerated the hidden bundle. PR #28 (`fc8cdd32c93cba02525409e0f5472640d8a61933`) now rejects selection rerun attempts before private seed generation. PR #29 (`2e87aafdb2c7904e674c700e321fc3939c8ece02`) changed manual selection defaults to empirically supported `auto/default`; comparability still uses actual attested runtime identity.

## Localized Mechanism Hypothesis

Forensic analysis of the four preserved comparable R1A failures from attempt 1 found a cross-case pattern broader than target authority:

- a denied invocation was sometimes treated as evidence that the desired state was impossible even though a materially different permitted execution path remained available;
- some trials reached the requested target but left incidental files created by probes or failed/intermediate attempts, so the final authoritative tree still failed verification.

The working hypothesis is therefore **execution recovery + transaction closure**: distinguish failure of one invocation from impossibility of the target state; when the target remains unresolved, try a materially different permitted path; before final verification, reconcile incidental mutations while preserving required outputs.

This is a hypothesis derived from consumed selection evidence. Do **not** edit R1/R1A directly from those cases and do not reuse those cases as hidden evidence.

## Fresh Execution-Recovery Development Boundary

PR #30 merged as `4ec38278ea82e1a32f088bd51c4121b7db828b71` and added a fresh-only development boundary without modifying historical `evals/evals.json`, the old U0/U1 workflow, R1, or R1A.

Key files:

- `execution_recovery_development.py` — thin wrapper that reuses `eval_harness.py` while binding fresh manifest/case/harness provenance;
- `evals/execution-recovery-development/manifest.json` — fresh development manifest;
- `evals/execution-recovery-development/cases/` — deterministic fixtures and graders;
- `.github/workflows/execution-recovery-development.yml` — manual paired U0/U1 Copilot runner using `auto/default`, one pinned CLI version, actual runtime attestation, `write,shell(python:*)`, and fail-closed matched-context comparison.

The four fresh cases are:

1. `execution-recovery-required` — target change is required; the normal helper invocation is outside the allowed shell pattern, while another permitted path can still reach the target.
2. `execution-recovery-noop` — opposing control; target is already satisfied and unnecessary retry/change fails.
3. `incidental-artifact-cleanup` — the required command reaches the target but creates incidental staging residue that must be reconciled.
4. `required-artifact-preserved` — opposing control; generated `bundle.json` and `manifest.json` are required deliverables and over-cleanup fails.

The agent-visible recovery prompt does not disclose the recovery mechanism; pressure comes from the tool policy. TDD evidence: RED run `34728626776`, GREEN `34728740561`, anti-leak RED `34728803815` with exactly one intended failure, final branch GREEN `34728843403`, exact PR GREEN `34728867975`, and post-merge GREEN `34728889597`. Final suite: **95 tests + `python verify.py` PASS**.

## Candidate Gate

**No R1B candidate exists yet.** Do not create one merely because the mechanism sounds plausible.

First run fresh paired behavioral baselines on all four cases with the current R1 as U1 and no guidance as U0. For each pair, preserve actual model/reasoning/tool-set provenance and reject non-comparable pairs rather than interpreting routing drift as treatment effect.

Candidate creation is allowed only if fresh evidence exposes a reproducible residual failure that the current R1 does not solve and the opposing controls remain interpretable. If R1 passes all fresh target cases, the present hypothesis has not earned a new runtime sentence; create new fresh probes or abandon/compress the hypothesis instead of manufacturing R1B.

## Open Debts

1. Run fresh behavioral baseline pairs for all four execution-recovery development cases.
2. If a fresh residual failure exists, formulate the smallest semantic candidate and test it against opposing fresh controls before any selection experiment.
3. Preregister a completely new selection boundary and generate a wholly fresh hidden bundle only after a candidate survives fresh development stability.
4. Design a purpose-built exact-bundle repair path before any future hidden experiment needs same-identity infrastructure retry.
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
- Retrying behavioral failures as infrastructure failures.
- Reusing consumed selection cases as hidden evidence.
- Rewriting R1A after seeing selection outcomes and rerunning those cases as if unseen.
- Treating a GitHub matrix-job rerun as same-identity evidence when its dependency graph regenerated a hidden bundle.
- Treating `auto` routing as a matched-model guarantee.
- Encoding an eval answer in the agent-visible prompt instead of applying pressure through the environment.
- Creating R1B before fresh development evidence demonstrates a residual failure.
- Promoting development-stable or selection-stable evidence directly to runtime residency.

## W5 Boundary

Nolane World 0.12.0 W5 world `world5_0ad739c41440565a1a83`, task `task_a34eb8be38b6f928`, remains blocked at r4 **Assumption Stress**. It requires a genuinely independent verifier; this controller-development context must not self-sign it.

Unresolved research question:

> What is the minimum sufficient behavioral controller that reduces invalid or unverified task-state transitions without introducing passivity, overthinking, myopic minimality, excess context cost, or hidden harness dependence?

## Next Best Action

Keep runtime R1 and frozen R1A unchanged. Dispatch replicate 1 of all four cases through `.github/workflows/execution-recovery-development.yml` with `model=auto` and `reasoning_effort=default`, then inspect immutable receipts and pair summaries. Only fresh behavioral evidence may authorize the next candidate-design step.

## Update Rule

After each meaningful milestone, replace stale state with current invariants, exact evidence, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action. Do not turn this file back into a chronological diary.
