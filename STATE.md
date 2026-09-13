# STATE — Nolane Prompt MS

**Status:** alpha / research-active  
**Behavioral verification gate:** OPEN  
**Core skill word count:** 446  
**Runtime dependencies:** none

## Boot Sequence

Before modifying this repository: read `CONSTITUTION.md` and all of this file; inspect current `main` and recent PRs/runs; run the full unit suite plus `python verify.py`; treat stored next actions as hypotheses until rechecked against repository/runtime reality.

## Current Invariant

Maximize **behavioral leverage per token and per unit of controller complexity**. Utility precedes compression. Causality precedes wording. Ablation precedes residency. Verification precedes completion.

Research machinery may temporarily be larger than the runtime package. It must not become a runtime dependency. After the research gates actually close, freeze the evidence and distill the installable distribution to the smallest sufficient agent-facing package instead of shipping the laboratory.

## Runtime Reality

- Canonical repository: `Nolane-x/Nolane-prompt-ms`.
- `verified-delta/SKILL.md` remains the single-file runtime kernel: **446 words**, zero runtime dependencies.
- Runtime R1 blob remains `ac48f09ab02eca63e014b4c25f86e492ae5559cb`.
- Frozen rejected R1A remains `evals/candidates/r1-target-authority.md`, blob `26d93ce346deedccd7186ad5856f849136825ec3`.
- **No R1B exists.**
- Behavioral verification remains OPEN.
- Provider snapshots remain `provider-managed-unpinned`; actual post-resume runtime attestation is authoritative for behavioral matching.

## Current Session-Fork Contract

Behavioral development pairs use `copilot-local-session-resume-v3-late-bound-runtime`:

1. create one neutral local-only seed session;
2. freeze and tar the seed home;
3. verify archive SHA-256;
4. derive authoritative transported session-state SHA from the decoded tar;
5. U0/U1 independently restore the same archive and same session ID;
6. verify pre-treatment state equality;
7. resume both arms;
8. attest actual post-resume runtime identity;
9. admit behavioral comparison only when U0/U1 canonical matched config agrees.

Seed runtime is provenance, not a requirement that post-resume runtime equal the seed. Do not retry provider `auto` until arms happen to match. Do not weaken archive/state gates after an infrastructure mismatch.

## Latest Admissible Development Evidence

Fresh late-bound-runtime evidence established both a real signal and unresolved stochasticity:

- `incidental-artifact-cleanup` r6 — run `34739515336`: **comparable `u1_harm`**. U0 passed; U1 used the same matched resumed runtime/config but made zero tool calls and returned `SEED_READY`. This is admissible behavioral evidence.
- `incidental-artifact-cleanup` r7 — run `34740626669`: **comparable `same_pass`**. The r6 harm did not reproduce.
- `required-artifact-preserved` r5/r6 evidence with U0/U1 runtime drift is **not comparable** and must not be interpreted as treatment effect.

Current hypothesis: R1 may intermittently retain a superseded turn-scoped instruction after a new user target arrives. Status remains **unresolved / stochastic**, not reproduced strongly enough to authorize R1B.

## Temporal-Authority Pressure Cases — Integrated

PR #38 integrated two purpose-built development cases at merge commit `cac8de133474bca59bc7185b23c01819b7a5c183` without changing R1, R1A, `eval_harness.py`, receipt schema, or the pair summarizer.

### `temporal-supersession`

The prior seed-turn restriction is explicitly declared complete. The current task requires reading `challenge.json` and creating exactly one deterministic `answer.json`. The workspace-only grader fails if the agent remains passive, emits stale `SEED_READY`, writes the wrong value, mutates the fixture, or creates extra files.

### `temporal-continuity-control`

The same prior seed-turn restriction is explicitly declared still active while the new target would otherwise require a workspace write. The grader requires the fixture workspace to remain unchanged. This opposes a simplistic repair such as “new turn means discard all prior constraints.”

Both cases intentionally reuse the same existing seed architecture, so the causal contrast is temporal authority rather than a different seed construction.

TDD/integration evidence:

- RED commit `eb8d9e34cdabe179fba7abb48a96d67ec0c273f6`, run `34743316136`: **101 tests with exactly the expected 2 failures + 1 error from missing temporal cases**;
- exact PR head `79e55f7a826838f3ca9b5957ea35b62201d70c55`, run `34745155079`: full unittest PASS + `python verify.py` PASS;
- post-merge main run `34745224568`: full unittest PASS + `python verify.py` PASS.

These are code/infrastructure verification only. They are **not** behavioral evidence about R1.

## Candidate Gate

Keep R1 and R1A unchanged. **Do not create R1B yet.**

A semantic candidate becomes admissible only if fresh targeted temporal evidence shows an interpretable, sufficiently reproducible R1/U1 residual failure under comparable U0/U1 resumed runtime/config, while the opposing continuity control shows that a proposed repair can distinguish expired constraints from still-active constraints.

Non-comparable pairs, infrastructure failures, seed/resume provider drift by itself, missing receipts, or a single unreproduced stochastic failure do not authorize wording changes.

If a future candidate exists, keep the semantic delta extremely small and derive it from the observed causal failure. It must then face fresh opposing development tests, ablation, and a newly preregistered selection boundary before runtime residency.

## Rejected Directions Worth Preserving

- Bigger rule count or longer prose as a proxy for intelligence.
- Protecting R1/R1A because effort was invested.
- Treating CI GREEN as behavioral utility.
- Calling mismatched receipts a treatment effect.
- Retrying behavioral/provider outcomes until a desired match appears.
- Treating provider-internal model IDs as guaranteed public `--model` identifiers.
- Requiring resumed runtime to equal neutral seed runtime when the causal comparison is U0 versus U1.
- Sharing one writable resumed session between treatment arms.
- Weakening archive/state-hash gates after mismatch instead of fixing representation authority.
- Retroactively admitting behavior from runs that failed the gate active at the time.
- Reusing consumed hidden/selection evidence as fresh evidence.
- Creating R1B before fresh matched temporal evidence justifies it.
- Shipping research harness/evidence as runtime dependency merely because it exists in the research repository.

## Open Debts

1. Run fresh replicate 1 for `temporal-supersession` and `temporal-continuity-control`; inspect raw receipts, archive/state/session provenance, actual U0/U1 resumed runtime, matched SHA, and pair summary. Use behavior only when the pair is comparable.
2. The current workflow-dispatch UI choice list predates the two temporal cases. Resolve the dispatch surface without changing causal semantics, or dispatch through a supported API/CLI path that can supply the registered case IDs. Do not treat inability to launch a run as behavioral evidence.
3. If targeted temporal harm reproduces, replicate before opening R1B and preserve the continuity opposing control.
4. Build a purpose-made exact-bundle repair path before another hidden experiment requires same-identity infrastructure repair.
5. Final cross-domain hidden holdout remains open.
6. Provider snapshot immutability remains unavailable.
7. Independent W5 r4 verification remains missing.
8. Primitive competition R0–R8, controller-locus comparison, natural activation, cross-language activation, portability, umbrella-vs-micro-skill granularity, myopic-minimality, and belief-collapse probes remain open.
9. Final distribution distillation and broad agent installation documentation occur only after the behavioral research boundary closes; do not delete the laboratory early.

## W5 Boundary

Nolane World 0.12.0 W5 world `world5_0ad739c41440565a1a83`, task `task_a34eb8be38b6f928`, remains blocked at r4 **Assumption Stress** and requires a genuinely independent verifier.

Unresolved research question:

> What is the minimum sufficient behavioral controller that reduces invalid or unverified task-state transitions without introducing passivity, overthinking, myopic minimality, excess context cost, or hidden harness dependence?

## Next Best Action

First require GREEN on this STATE update. Then obtain **fresh replicate 1** behavioral runs for both temporal pressure cases with `model=auto` and `reasoning_effort=default`.

Do not open R1B from code integration alone. Interpret the temporal hypothesis only from fresh comparable paired receipts; if evidence remains unstable, keep R1 unchanged and continue targeted replication.

## Update Rule

After each meaningful milestone, replace stale state with current invariants, exact evidence, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action. `STATE.md` is a bootloader, not a diary.
