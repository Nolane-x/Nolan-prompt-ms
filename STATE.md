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

PR #33 merged the production session-fork architecture into `main` as `7a68919677f2e3b37ece65c7ea1cd380999dc559`. The workflow creates a neutral seed before treatment, transfers local session state through an artifact, resumes both treatment arms without explicit model/reasoning flags, attests actual post-resume runtime identity, and binds common session-fork identity into matched run-config receipts.

Migration verification included exact PR run `34731772462`, post-merge run `34731792178`, and final state run `34731834564`, all GREEN.

## First Cross-Runner Production Attempt — Infrastructure-Only TOCTOU Failure

Fresh dispatches from `main@196a861030cc865e371d50742402126324850cc7` were intentionally evaluated before behavioral interpretation:

- `incidental-artifact-cleanup` r3, run `34732880632`;
- `required-artifact-preserved` r2, run `34732882721`.

Both seed jobs succeeded. In all four treatment arms, `Clone and verify pre-treatment session fork before treatment` failed with `session fork state hash mismatch`; treatment prompt construction, Copilot resume/inference, receipt generation, and grading were all skipped. These runs contain **zero behavioral evidence** and have no effect on the candidate gate.

Forensic artifact comparison localized a reproducible TOCTOU bug rather than artifact corruption:

- cleanup r3 stored seed hash `2f1b30f9305b7e0dd3e1185a4230d20bfb4afbbd3fdb989cc37b61a5ca3e41f2`, while transferred seed artifact and U0 clone both had `bf305f25776e9bde4edd043d28ff1de681f5bd3cf816305e8ae231d702add693`;
- required-artifact r2 stored seed hash `3940bbf0731dc0fea9f789880ae8805b365a090c89527fd166994184ecb0e495`, while transferred seed artifact and U0 clone both had `7a0c050e24dca757224e22cf3a52c1d59551a6064347ef50f011841108d59b7f`.

The transferred artifact and downloaded clone were byte-consistent. The stale value originated because `seed-state-hash.txt` was computed from the **live** Copilot home before the seed job ended, while local session state could still flush before artifact upload.

Machine-readable evidence is `evals/execution-recovery-development/session-fork-cross-runner-infrastructure-failures-2026-09-13.json`.

## Frozen-Snapshot Fix — Integrated

PR #34 fixes snapshot authority without weakening any gate. After the seed session and unique session ID exist, the workflow copies the live Copilot home to `frozen-seed-home`, computes `seed-state-hash.txt` from that frozen copy, uploads it, and makes both U0/U1 arms clone only that same frozen copy. Existing pre-treatment hash equality, post-resume runtime attestation, graders, and receipt semantics remain unchanged.

TDD and integration evidence:

- RED commit `11ec4cdd309149a06106719d3402fbcf320c43b8`, run `34733113657`: **98 tests with exactly 1 intended frozen-snapshot contract failure**;
- GREEN commit `453484abb9b812bd38b99a661c7a6d567781625d`, run `34733172015`: **98/98 tests PASS + `python verify.py` PASS**;
- state-head run `34733252691`: GREEN;
- exact PR #34 head `8ba5d908614c46beea6ca76b8f230658344893f4`, PR run `34733275904`: GREEN;
- PR #34 merged as `00afe536fcef49090cb93d1d60651b092ddc06d2`;
- post-merge run `34733316358`: **98/98 tests PASS + `python verify.py` PASS**.

The frozen-snapshot fix is integrated and code-verified. It still requires new live cross-runner behavioral dispatches to establish whether resume remains matched across seed → U0/U1 runner boundaries after the TOCTOU repair.

## Candidate Gate

Keep R1 and R1A unchanged. **Do not create R1B.** A new semantic candidate is allowed only if fresh, matched-runtime, session-fork evidence exposes a reproducible R1/U1 residual failure with interpretable opposing controls. Infrastructure failures, provider drift, session-resume failures, stale snapshot hashes, or mismatched receipts do not authorize candidate wording.

## Open Debts

1. Live-validate the integrated frozen-snapshot workflow with new replicate numbers; preserve cleanup r3 / required-artifact r2 as infrastructure-only evidence.
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
- Dropping or bypassing the pre-treatment state-hash gate after a hash mismatch instead of fixing snapshot authority.
- Creating R1B before a fresh matched residual R1 failure exists.
- Promoting development or selection evidence directly to runtime residency.

## W5 Boundary

Nolane World 0.12.0 W5 world `world5_0ad739c41440565a1a83`, task `task_a34eb8be38b6f928`, remains blocked at r4 **Assumption Stress** and requires a genuinely independent verifier.

Unresolved research question:

> What is the minimum sufficient behavioral controller that reduces invalid or unverified task-state transitions without introducing passivity, overthinking, myopic minimality, excess context cost, or hidden harness dependence?

## Next Best Action

Require GREEN on this state commit. Then dispatch `incidental-artifact-cleanup` replicate **4** and `required-artifact-preserved` replicate **3** through `.github/workflows/execution-recovery-development.yml` with `model=auto` and `reasoning_effort=default`. Interpret behavior only if the frozen artifact hash, both clone hashes, seed/U0/U1 actual runtime attestations, receipts, and pair summary all remain matched.

## Update Rule

After each meaningful milestone, replace stale state with current invariants, exact evidence, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action. Do not turn this file into a chronological diary.
