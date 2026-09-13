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

Machine-readable evidence is `evals/execution-recovery-development/session-fork-feasibility-2026-09-13.json`.

Throwaway spike run `34731466073`, commit `d94e8f3980b72125f5cc826d27603225145b477b`, artifact `10309745927`, artifact SHA-256 `bf1a6d7ab1405a5d3a3dd43c00d748c7eb3b79489a963ed205aad9295b9d0459` passed its frozen feasibility rule in one attempt.

Observed seed/U0/U1 identity was identical:

- model `gpt-5.6-luna`;
- reasoning `medium`;
- tool set `[bash, glob, rg, view]`;
- all three calls exited 0.

All three pre-treatment session-state hashes were `b7643b6988fde94f49481ac24933c5a153d999fe333e370d1c3675a0e380f5aa`. After resume, U0 and U1 independently mutated and diverged while neither modified the other clone. This proves **infrastructure feasibility only** in the observed provider/CLI configuration, not behavioral utility, general provider stability, or runtime residency.

## Production Session-Fork Migration — Integrated

PR #33 merged the clean production migration into `main` as `7a68919677f2e3b37ece65c7ea1cd380999dc559`. The development workflow now:

1. creates a neutral seed session before any case preparation or treatment;
2. keeps Copilot session state local with remote export disabled;
3. records one unique seed session ID, seed runtime attestation, and seed session-state SHA-256;
4. uploads one immutable seed artifact used by both fresh matrix arms;
5. requires each arm to clone and verify the identical pre-treatment session-state hash before constructing treatment;
6. performs behavioral inference through `--resume=<sessionId>` with **no explicit model or reasoning flags**;
7. requires each arm's post-resume actual model/reasoning/tool set to equal the seed before any behavioral receipt is written;
8. binds `session_fork.session_id` and `session_fork.pre_treatment_state_sha256` into the matched run-config.

Migration verification:

- RED commit `49b0e9da0e1d72896dbc58b4bd66b5cb11033203`, run `34731613939`: **97 tests with exactly 2 intended session-fork contract failures**;
- implementation commit `8a2853270874ddc1cf5ca80170c580e5abf668c5`, run `34731679823`: **97/97 tests PASS + `python verify.py` PASS**;
- state-head run `34731740508`: GREEN;
- exact PR #33 run `34731772462`: GREEN;
- post-merge run `34731792178` on `main@7a68919677f2e3b37ece65c7ea1cd380999dc559`: GREEN.

The migration is therefore **integrated and code-verified**, but production cross-runner resume is not yet behavioral evidence. A new live workflow dispatch must still prove that the seed artifact survives the seed-job → U0/U1 runner boundary with matched post-resume identity.

## Candidate Gate

Keep R1 and R1A unchanged. **Do not create R1B.** A new semantic candidate is allowed only if fresh, matched-runtime, session-fork evidence exposes a reproducible R1/U1 residual failure with interpretable opposing controls. Infrastructure failures, provider drift, session-resume failures, or mismatched receipts do not authorize candidate wording.

## Open Debts

1. Live-validate cross-runner seed-artifact resume with new replicate numbers; preserve all earlier mismatched/infrastructure attempts.
2. Re-evaluate the two previously non-comparable cells only from new matched receipts.
3. If a candidate eventually exists, test fresh opposing development stability and preregister a completely new selection boundary before any new hidden bundle.
4. Design a purpose-built exact-bundle repair path before future hidden experiments require same-identity infrastructure repair.
5. Final cross-domain hidden holdout remains open.
6. Provider snapshot immutability remains unavailable.
7. Independent W5 r4 verification remains missing.
8. Primitive competition R0–R8, controller-locus comparison, natural activation, cross-language activation, portability, umbrella-vs-micro-skill granularity, myopic-minimality, and belief-collapse probes remain open.

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

Require GREEN on this state commit. Then dispatch `incidental-artifact-cleanup` replicate **3** and `required-artifact-preserved` replicate **2** through `.github/workflows/execution-recovery-development.yml` using `model=auto` and `reasoning_effort=default`. For each run inspect seed artifact, U0/U1 actual attestations, common fork hash, receipts, and pair summary before interpreting behavior. Keep candidate design closed unless fresh matched evidence exposes a reproducible R1/U1 failure.

## Update Rule

After each meaningful milestone, replace stale state with current invariants, exact evidence, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action. Do not turn this file into a chronological diary.
