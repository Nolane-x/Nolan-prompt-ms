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

Live run `34731153920` rejected that architecture before inference: `auto` attested `mai-code-1.1-flash` at `medium`, but Copilot CLI `1.0.83` rejected the same provider-internal identifier through explicit `--model`. No behavioral trial ran. Do not repair this with retry-until-match.

## Session-Fork Feasibility and Production Migration

Throwaway feasibility run `34731466073` showed that one local Copilot session could be cloned into isolated U0/U1 homes with identical pre-treatment state and, in that observed run, identical runtime identity. This established infrastructure feasibility only.

PR #33 merged the production session-fork architecture as `7a68919677f2e3b37ece65c7ea1cd380999dc559`: neutral seed before treatment, local-only Copilot home, isolated U0/U1 resumes from a common session ID, actual runtime attestation, and matched run-config receipts.

## Cross-Runner Failure 1 — Live-State TOCTOU

Fresh cleanup r3 (`34732880632`) and required-artifact r2 (`34732882721`) failed before treatment at the pre-treatment state-hash gate. The transferred artifact and downloaded clones were consistent with each other, while the stored seed hash was stale because it had been computed from the live Copilot home before late session flushes completed. These runs contain zero behavioral evidence.

PR #34 fixed snapshot authority by copying the live Copilot home to an immutable frozen seed before hashing/upload. It merged as `00afe536fcef49090cb93d1d60651b092ddc06d2`; post-merge run `34733316358` was GREEN.

## Cross-Runner Failure 2 — Directory Artifact Representation

Fresh cleanup r4 (`34734044025`) and required-artifact r3 (`34734045527`) proved a second infrastructure boundary. In both runs, the hash stored from the frozen directory differed from the tree reconstructed from the uploaded directory artifact, while the downloaded artifact and trial clone agreed exactly. No treatment inference ran and these runs contain zero behavioral evidence.

The supported repair is representation-preserving transport rather than weakening the state-hash gate.

## Lossless Tar Session Transport — Integrated and Live-Validated

PR #36 replaced direct directory transport with one verified tar representation. The seed job freezes the local Copilot home, creates `frozen-seed-home.tar`, records the archive SHA-256, decodes that same tar locally to derive the authoritative transported session-state hash, and uploads the tar plus metadata. Each trial verifies archive SHA-256 before extraction and then verifies the extracted session-state hash. Stale `inuse.<pid>.lock` ownership markers are excluded from the transport representation. `transport_archive_sha256` is bound into matched run-config provenance.

PR #36 exact head CI was GREEN, it merged as `bf4a12888c0421f61b8e3aa579817c4c4c10ff54`, and post-merge run `34736731996` passed the full unit suite plus `python verify.py`.

Fresh live validation from that exact main revision:

- cleanup r5: run `34736843169`;
- required-artifact r4: run `34736845884`.

In all four U0/U1 arms, seed artifact download, archive verification, extraction, and **pre-treatment session-state equality all passed**. This closes the previously observed cross-runner representation/hash failure under the observed harness configuration.

Those runs still do **not** count as behavioral evidence: after successful resume/inference, the old receipt gate rejected all arms because provider `auto` had selected `gpt-5.6-luna` for the neutral seed but re-selected `mai-code-1.1-flash` after resume. Within each pair, U0 and U1 matched each other on actual resumed model/reasoning/tool identity; only seed runtime differed. The runs therefore remain infrastructure diagnostics and are consumed.

## Late-Bound Resumed Runtime Matching — Integrated

The causal authority is now split at the correct boundary:

- seed authority: common session ID, exact transport archive SHA-256, exact decoded pre-treatment state hash, and bound seed-runtime provenance;
- behavioral matched-runtime authority: actual **post-resume U0 versus U1** model, reasoning effort, tool set, harness, and all other `matched` run-config fields.

A resumed arm is no longer rejected merely because its provider-selected runtime differs from the neutral seed runtime. Instead, each arm records its actual resumed runtime in `matched`, while `seed_runtime` remains bound inside `session_fork` provenance. The existing canonical matched-context hash and pair summarizer still fail closed if U0 and U1 differ on resumed runtime identity or any other matched field. This is not retry-until-match and does not weaken archive/state identity.

TDD/integration evidence:

- RED commit `a809eb14e432662a6a99934d5cd3da4522e6d16f`, run `34737221590`: **99 tests with exactly 1 intended late-bound-runtime contract failure**;
- exact GREEN production tree `cc4e63f2a397994544a732dc0766d9e121d5119b`: **99/99 tests PASS + `python verify.py` PASS + `git diff --check` PASS**, with exact unchanged R1/R1A blobs;
- PR #37 exact-head run `34737497541`: GREEN;
- PR #37 merged as `b3ed2097346e01de160984074c0d34dbb8b9f4b3`;
- post-merge run `34737526548`: **full unit suite PASS + `python verify.py` PASS**.

No behavioral result from cleanup r5 or required-artifact r4 is retroactively admitted after this harness change. Fresh replicate identities are required.

## Candidate Gate

Keep R1 and R1A unchanged. **Do not create R1B.** A new semantic candidate is allowed only if fresh, comparable, matched-resumed-runtime session-fork evidence exposes a reproducible R1/U1 residual failure with interpretable opposing controls. Infrastructure failures, provider drift between seed and resume, U0/U1 runtime drift, session-resume failures, stale hashes, missing receipts, or non-comparable summaries do not authorize candidate wording.

## Open Debts

1. Run fresh cleanup r6 and required-artifact r5 under the integrated late-bound-runtime contract; cleanup r5 / required-artifact r4 remain consumed infrastructure diagnostics.
2. Re-evaluate the previously non-comparable execution-recovery cells only from new matched receipts.
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
- Requiring a post-resume runtime to equal the neutral seed runtime when the actual causal comparison is U0 versus U1.
- Sharing one writable resumed session between treatment arms.
- Treating session-resume documentation as proof of runtime identity without actual attestation.
- Dropping or bypassing archive/state-hash gates after mismatch instead of fixing representation authority.
- Retroactively admitting behavior from runs that failed the then-current infrastructure/receipt gate.
- Creating R1B before a fresh matched residual R1 failure exists.
- Promoting development or selection evidence directly to runtime residency.

## W5 Boundary

Nolane World 0.12.0 W5 world `world5_0ad739c41440565a1a83`, task `task_a34eb8be38b6f928`, remains blocked at r4 **Assumption Stress** and requires a genuinely independent verifier.

Unresolved research question:

> What is the minimum sufficient behavioral controller that reduces invalid or unverified task-state transitions without introducing passivity, overthinking, myopic minimality, excess context cost, or hidden harness dependence?

## Next Best Action

Require GREEN on this STATE commit. Then dispatch `incidental-artifact-cleanup` replicate **6** and `required-artifact-preserved` replicate **5** through `.github/workflows/execution-recovery-development.yml` with `model=auto` and `reasoning_effort=default`.

Interpret behavior only if both arms produce receipts and the pair summary is comparable. The transport archive SHA-256, pre-treatment state hash, session ID, seed provenance, and all U0/U1 matched fields must agree where required. Seed runtime may differ from post-resume runtime, but post-resume U0 and U1 actual model/reasoning/tool identity must match each other through the canonical matched-context gate.

## Update Rule

After each meaningful milestone, replace stale state with current invariants, exact evidence, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action. Do not turn this file into a chronological diary.
