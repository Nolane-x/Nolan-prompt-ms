# STATE — Nolane Prompt MS

**Status:** alpha / research-active  
**Behavioral verification gate:** OPEN  
**Core skill word count:** 446  
**Runtime dependencies:** none

## Boot Sequence

Before modifying this repository: read `CONSTITUTION.md` and all of this file; inspect current `main` and recent PRs; run the full unit suite plus `python verify.py`; re-check stale external/runtime claims; continue from the next evidence-producing action. Past state is recovery evidence, never authority.

## Current Invariant

Maximize **behavioral leverage per token and per unit of controller complexity**. Utility precedes compression. Causality precedes wording. Ablation precedes residency. Verification precedes completion.

## Runtime Reality

- Canonical repository: `Nolane-x/Nolane-prompt-ms`.
- `verified-delta/SKILL.md` remains the single-file runtime package: **446 words**, zero runtime dependencies.
- Runtime blob remains `ac48f09ab02eca63e014b4c25f86e492ae5559cb`.
- Runtime R1 is unchanged by target-authority and execution-recovery research.
- Frozen rejected R1A remains `evals/candidates/r1-target-authority.md`, blob `26d93ce346deedccd7186ad5856f849136825ec3`.
- **No R1B exists.**
- Behavioral verification remains OPEN.
- Provider snapshots remain `provider-managed-unpinned`; actual runtime attestation is authoritative.

## R1A Selection Boundary

Frozen selection attempt 1, run `34702008909`, produced 11/12 comparable pairs. R1A had zero candidate harm, but **0/4 preserve gains** where at least two were required and only **3/7 comparable act/probe/verify passes**. The one non-comparable verify pair could not repair the frozen conjunctive decision. R1A therefore receives no runtime residency. Consumed selection cases are diagnostic only, never fresh hidden evidence.

Attempt 2 is excluded because GitHub rerun semantics regenerated the hidden bundle. PR #28 hardened hidden reruns; PR #29 moved supported manual defaults to `auto/default` without treating requested configuration as matched identity.

## Fresh Execution-Recovery Development Evidence

PR #30 added four fresh-only cases without changing historical `evals/evals.json`, R1, or R1A:

1. `execution-recovery-required`
2. `execution-recovery-noop`
3. `incidental-artifact-cleanup`
4. `required-artifact-preserved`

Replicate 1 evidence is recorded in `evals/execution-recovery-development/results-2026-09-13.json` and merged through PR #31 (`654dca37c484457503161f2d1106ef41eda535e4`). R1/U1 passed all four observed fresh trials. Two pairs were comparable `same_pass`; two were excluded because `auto` routed U0/U1 to different actual model/tool identities. Therefore **no fresh matched R1 failure justified R1B**.

## Explicit-Model Runtime Lock — Rejected Architecture

PR #32 (`2f00a60ea049077ce6daf69996ff476bedbbb1a9`) code-verified a preflight that selected a runtime under `auto`, then attempted to call the same exact model/reasoning identity before behavior.

Live replicate-2 run `34731153920` rejected that architecture before inference:

- `auto` attested `mai-code-1.1-flash`, reasoning `medium`, tool set `[bash, create, edit, glob, grep, view]`;
- Copilot CLI `1.0.83` then rejected `--model=mai-code-1.1-flash` as unavailable;
- behavioral `trial` was SKIPPED, so the run produced **no behavioral evidence**;
- model-lock artifact `10309765109`, SHA-256 `584e256a17f055f2253ec430631010b9a073d4143793976eb0324f1c000d47f7`.

Conclusion: current provider `auto` may resolve to an internal model identifier that cannot be invoked through public explicit-model selection. Do not repair this with retry-until-match.

## Session-Fork Feasibility — PASS

A throwaway branch tested pre-treatment local session forking instead of explicit model re-invocation. Machine-readable evidence is `evals/execution-recovery-development/session-fork-feasibility-2026-09-13.json`.

Live spike run `34731466073`, commit `d94e8f3980b72125f5cc826d27603225145b477b`, artifact `10309745927`, artifact SHA-256 `bf1a6d7ab1405a5d3a3dd43c00d748c7eb3b79489a963ed205aad9295b9d0459` passed its frozen feasibility rule in one attempt.

Observed seed/U0/U1 identity was identical:

- model `gpt-5.6-luna`;
- reasoning `medium`;
- tool set `[bash, glob, rg, view]`;
- all three calls exited 0.

All three pre-treatment session-state hashes were `b7643b6988fde94f49481ac24933c5a153d999fe333e370d1c3675a0e380f5aa`. After resume, U0 and U1 independently mutated and diverged while neither modified the other clone. This proves **infrastructure feasibility only** in the observed provider/CLI configuration, not behavioral utility, general provider stability, or runtime residency.

## Production Session-Fork Migration

Branch `fix/execution-recovery-session-fork` replaces the impossible exact-model preflight in `.github/workflows/execution-recovery-development.yml` with:

1. a neutral seed job before any case preparation or treatment;
2. local-only Copilot session state with remote export disabled;
3. one unique seed session ID, seed runtime attestation, and seed session-state SHA-256;
4. immutable seed artifact shared to both fresh matrix arms;
5. per-arm byte-identical local clone verified before treatment construction;
6. behavioral inference through `--resume=<sessionId>` with **no explicit model or reasoning flags**;
7. post-resume actual model/reasoning/tool-set equality against the seed before any receipt is written;
8. matched run-config binding of `session_fork.session_id` and `session_fork.pre_treatment_state_sha256`.

Migration TDD:

- RED commit `49b0e9da0e1d72896dbc58b4bd66b5cb11033203`, run `34731613939`: **97 tests with exactly 2 intended session-fork contract failures**;
- implementation commit `8a2853270874ddc1cf5ca80170c580e5abf668c5`, run `34731679823`: **97/97 tests PASS + `python verify.py` PASS**.

This migration is currently **code-verified only**. The throwaway spike proved same-run cloning/resume feasibility; production still needs a live workflow dispatch to prove that the seed artifact can cross GitHub runner/job boundaries and resume with matched identity in both behavioral arms.

## Candidate Gate

Keep R1 and R1A unchanged. **Do not create R1B.** A new semantic candidate is allowed only if fresh, matched-runtime, session-fork evidence exposes a reproducible R1/U1 residual failure with interpretable opposing controls. Infrastructure failures, provider drift, session-resume failures, or mismatched receipts do not authorize candidate wording.

## Open Debts

1. Integrate the session-fork migration through exact-head PR + post-merge GREEN.
2. Live-validate cross-runner seed-artifact resume with new replicate numbers; preserve all earlier mismatched/infrastructure attempts.
3. Re-evaluate the two previously non-comparable cells only from new matched receipts.
4. If a candidate eventually exists, test fresh opposing development stability and preregister a completely new selection boundary before any new hidden bundle.
5. Design a purpose-built exact-bundle repair path before future hidden experiments require same-identity infrastructure repair.
6. Final cross-domain hidden holdout remains open.
7. Provider snapshot immutability remains unavailable.
8. Independent W5 r4 verification remains missing.
9. Primitive competition R0–R8, controller-locus comparison, natural activation, cross-language activation, portability, umbrella-vs-micro-skill granularity, myopic-minimality, and belief-collapse probes remain open.

## Rejected Directions Worth Preserving

- Bigger is stronger / more rules imply more intelligence.
- Protecting R1/R1A because effort was invested.
- Treating CI GREEN as behavioral utility.
- Calling mismatched receipts a treatment effect.
- Retrying behavioral failures as infrastructure failures.
- Reusing consumed selection cases as hidden evidence.
- Treating `auto` as a matched-model guarantee.
- Retrying `auto` until arms happen to match.
- Treating provider-internal model IDs as public `--model` identifiers.
- Sharing one writable resumed session between treatment arms.
- Treating session-resume documentation as proof of runtime identity without actual attestation.
- Creating R1B before a fresh matched residual R1 failure exists.
- Promoting development or selection evidence directly to runtime residency.

## W5 Boundary

Nolane World 0.12.0 W5 world `world5_0ad739c41440565a1a83`, task `task_a34eb8be38b6f928`, remains blocked at r4 **Assumption Stress** and requires a genuinely independent verifier.

Unresolved research question:

> What is the minimum sufficient behavioral controller that reduces invalid or unverified task-state transitions without introducing passivity, overthinking, myopic minimality, excess context cost, or hidden harness dependence?

## Next Best Action

Require GREEN on this state commit, review branch diff, open an exact-head PR for the clean production migration, require PR-triggered GREEN, merge with expected head, then require post-merge GREEN. Only then dispatch new fresh replicates for `incidental-artifact-cleanup` and `required-artifact-preserved` and inspect seed + U0/U1 attestations before interpreting behavior.

## Update Rule

After each meaningful milestone, replace stale state with current invariants, exact evidence, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action. Do not turn this file into a chronological diary.
