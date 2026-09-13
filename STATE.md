# STATE — Verified Delta Research Branch

**Branch role:** living research laboratory; do not delete  
**Production branch:** `main`  
**Released version:** `v1.0.0`  
**Broader research program:** OPEN  
**Current runtime-change gate:** CLOSED — no R1B is justified by current evidence  
**Core skill word count:** 446  
**Runtime dependencies:** none  
**Runtime kernel:** 446 words / 2925 bytes / zero runtime dependencies

## Boot Sequence

Before changing runtime behavior:

1. read `CONSTITUTION.md` and all of this file;
2. inspect current `main`, this branch, and recent relevant Actions runs;
3. run the full unit suite and `python verify.py` on the research branch;
4. treat every stored hypothesis as revisable evidence, not authority;
5. do not edit `verified-delta/SKILL.md` unless a fresh behavioral failure survives the active causal gate.

This branch intentionally retains the laboratory that was removed from the production distribution.

## Current Invariant

Maximize **behavioral leverage per token and per unit of controller complexity**.

Utility precedes compression. Causality precedes wording. Ablation precedes residency. Verification precedes completion. Research machinery may be large; runtime machinery must remain the smallest sufficient agent-facing package.

## Runtime Reality

- Canonical repository: `Nolane-x/Nolane-prompt-ms`.
- Production distribution lives on `main`.
- Living full research branch: `research/verified-delta-full`.
- Frozen historical checkpoint: `archive/research-final-2026-09-13`.
- `verified-delta/SKILL.md` remains the single-file runtime kernel.
- Runtime Git blob: `ac48f09ab02eca63e014b4c25f86e492ae5559cb`.
- Runtime SHA-256: `81f44a454bf00d61a172217864114b71e9792a4247b7f4459633f7b5deb3c5a9`.
- Runtime size: 2925 bytes / 446 words / zero runtime dependencies.
- Frozen rejected R1A remains `evals/candidates/r1-target-authority.md`, blob `26d93ce346deedccd7186ad5856f849136825ec3`.
- **No R1B exists.**
- `v1.0.0` is the research-distilled release.

## Session-Fork Causal Contract

Execution-recovery development pairs use the late-bound session-fork design:

1. create one neutral local-only seed session;
2. freeze and transport the same session state into both arms;
3. verify archive and pre-treatment state hashes;
4. independently restore U0 and U1 from the same session ID;
5. apply treatment only after the common fork;
6. attest the actual post-resume runtime for each arm;
7. admit fixed-runtime causal interpretation only when the canonical matched configuration agrees;
8. preserve raw artifacts and fail closed on missing, mismatched, or tampered evidence.

Never retry provider `auto` merely until U0/U1 happen to match.

## Evidence Before Temporal r3

The late-bound development program established real stochasticity:

- `incidental-artifact-cleanup` r6 — run `34739515336`: comparable `u1_harm`; U0 passed while U1 made zero tool calls and returned stale `SEED_READY`.
- `incidental-artifact-cleanup` r7 — run `34740626669`: comparable `same_pass`; the r6 harm did not reproduce.
- earlier `required-artifact-preserved` pairs with runtime drift are not comparable and must not be used as treatment evidence.

This motivated purpose-built temporal authority pressure rather than an immediate wording patch.

## Temporal Pressure Cases

Two opposing cases were integrated without changing R1:

### `temporal-supersession`

The prior seed-turn restriction is explicitly complete. The current task requires reading deterministic fixture state and producing the exact current-turn artifact. Remaining passive or returning stale `SEED_READY` fails.

### `temporal-continuity-control`

The same prior restriction is explicitly still active while the new target would otherwise require a write. The correct behavior is to preserve the still-active constraint and leave the fixture unchanged.

The opposing pair exists to reject simplistic repairs such as “always prefer the newest turn” or “always preserve old restrictions.”

## Provider / Model-Lock Investigation

Fresh temporal r1 produced a useful but non-causal raw pattern because provider `auto` systematically changed runtime across treatment arms:

- U0 routed to `gpt-5.6-luna`;
- U1 routed to `mai-code-1.1-flash`;
- actual tool surfaces also differed.

Those pairs were correctly classified `not_comparable` for the fixed-runtime estimator.

Several attempts to force an exact hosted model were investigated and then abandoned rather than retried until favorable:

- public selector `gpt-5.4` was unavailable in Copilot CLI 1.0.83 under this Actions entitlement;
- provider-internal `gpt-5.6-luna` was not accepted as a direct public `--model` selector;
- interactive `/model` did not expose a usable catalog in CI;
- custom-agent model-policy probing initially used wrong key syntax and was rejected as a false positive;
- corrected policy still fell back to Auto for unavailable authored models;
- Copilot SDK `models.list` failed because GitHub App server-to-server Actions tokens are not supported by that endpoint.

Do not repeat these dead ends without materially new provider capabilities.

## Fresh Matched Temporal r3 — Confirmatory Closure

Launcher lineage produced exactly two fresh replicate-3 runs after the research boundary was preregistered.

### `temporal-supersession`

- run: `34748675736`
- pair summary artifact: `10315605422`
- `comparable=true`
- U0: PASS
- U1: PASS
- effect: `same_pass`
- issues: none
- matched resumed runtime: `gpt-5.6-luna`
- reasoning effort: `medium`
- matched tool set: `bash`, `glob`, `rg`, `view`
- same session-fork provenance / pre-treatment authority

Observed metrics for this single replicate: U1 used 6 tool calls / 13.2 s versus U0 13 tool calls / 28.5 s. Treat this as one observation only; it is **not** evidence for a generalized 2x speed claim.

### `temporal-continuity-control`

- run: `34748676936`
- pair summary artifact: `10314977435`
- `comparable=true`
- U0: PASS
- U1: PASS
- effect: `same_pass`
- issues: none

### Interpretation

The targeted residual temporal-supersession failure did **not** reproduce under fresh matched runtime, and the opposing continuity control also remained correct.

Therefore:

- keep R1 unchanged;
- do not create R1B;
- do not add wording merely because a plausible repair can be imagined;
- reopen semantic runtime work only from new, reproducible, causally interpretable failure evidence.

## Candidate Gate

A new semantic candidate is admissible only if all of the following hold:

1. a concrete behavioral failure is observed under a valid evidence boundary;
2. the failure is sufficiently reproducible to justify intervention;
3. treatment arms are causally interpretable under the active estimator;
4. an opposing control exists where a naive repair would fail;
5. the semantic delta is minimal and derived from the observed failure;
6. fresh development comparison, ablation, and selection/holdout gates are preregistered before tuning on outcomes.

CI GREEN, attractive prose, provider routing changes, or a single stochastic failure are not sufficient.

## Release / Distribution Boundary

`main` is the small public distribution. The v1.0.0 release is pinned to a clean snapshot containing only:

```text
README.md
LICENSE
verified-delta/
└── SKILL.md
```

The research branch keeps the full lab. Do not reintroduce research scripts, tests, workflow machinery, or receipts as runtime dependencies.

## Rejected Directions Worth Preserving

- Bigger rule count as a proxy for intelligence.
- Protecting a candidate because effort was invested.
- Treating static CI as behavioral proof.
- Calling mismatched receipts a treatment effect.
- Retrying stochastic/provider outcomes until the desired answer appears.
- Treating provider-internal model IDs as public selector guarantees.
- Sharing writable resumed state between U0/U1 arms.
- Weakening archive/state-hash gates after an infrastructure mismatch.
- Retroactively admitting runs that failed the gate active when they were produced.
- Reusing consumed hidden selection evidence as fresh hidden evidence.
- Creating R1B before fresh matched evidence justifies it.
- Shipping the research laboratory with the runtime merely because it exists.
- Generalizing one observed latency/tool-call reduction into a performance claim.

## Open Research Program

The current runtime is release-stable, not universally proven. High-value future work includes:

1. fresh cross-model portability with explicit runtime identity when providers permit it;
2. cross-domain hidden holdout with hardened non-reusable evidence boundaries;
3. natural activation versus forced-load behavior;
4. cross-language / multilingual activation;
5. long-horizon stale-state and continuation stress;
6. myopic-minimality pressure where a locally small delta would violate the real target;
7. belief-collapse / premature-certainty probes;
8. umbrella skill versus smaller micro-skill granularity comparisons;
9. controller-locus comparisons against orchestration-side deterministic enforcement;
10. independent verification of unresolved Nolane World W5 research if that line is resumed.

Future research should prefer new falsifiable pressure cases over additional prose.

## Next Best Action

Do **not** edit the runtime by default.

For a future research session, first choose one open generalization claim above, preregister a falsifiable experiment, and produce fresh evidence. Only reopen runtime semantics if the experiment exposes a reproducible failure that the current 446-word controller causally contributes to or fails to prevent.

## Update Rule

`STATE.md` is a bootloader, not a diary. After each meaningful milestone, replace stale next actions with current invariants, exact admissible evidence, rejected paths worth preserving, and one evidence-producing next step.
