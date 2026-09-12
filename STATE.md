# STATE — Nolane Prompt MS

**Status:** alpha / research-active  
**Behavioral verification gate:** OPEN  
**Core skill word count:** 446  
**Runtime dependencies:** none

## Boot Sequence

A fresh session that will modify this repository must:

1. read `CONSTITUTION.md`;
2. read `STATE.md`;
3. inspect current repository reality and recent changes;
4. run `python verify.py` and the repository unit tests;
5. re-check every stored claim that could have gone stale;
6. continue from the next evidence-producing action, not old prose momentum.

Past-self state is a recovery aid, never authority.

## Current Invariant

Maximize **behavioral leverage per token and per unit of controller complexity**.

Verified Delta is the incumbent, not protected architecture. Its wording, tuple, name, size, skill packaging, and even prompt-level implementation remain hypotheses. Utility comes before compression. If no guidance, a smaller controller, an explicit state layer, or an external verifier produces a better behavior/cost frontier, replace or remove the incumbent rather than rescuing familiar prose.

## Observed Repository Reality

- Canonical repository: `Nolane-x/Nolane-prompt-ms`.
- `verified-delta/SKILL.md` remains the single-file runtime package: **446 words**, zero runtime dependencies.
- The runtime kernel has **not** been edited during the eval-lab, fresh-runner, or causal-config hardening work.
- `EVALS.md` keeps **Activation, RED baseline, GREEN comparison, Ablation, and Cross-domain holdout OPEN**.
- Deterministic repository/eval-infrastructure verification is separate from behavioral verification.
- Agent Skills format validation does not treat the project's `Use when...` wording preference or ≤500-word compression target as syntax laws. The ≤500-word value remains research pressure only.
- CI discovers all tests under `tests/` before running `python verify.py`.

## Executable U0/U1 Development Pack

The first utility pack is deterministic and intentionally opposing:

1. `username-normalization-noop` — the reported defect is already absent; unnecessary production change fails.
2. `username-normalization-partial` — matched report, but a real defect remains; pristine/no-op behavior fails and a focused production change is required.
3. `false-completion-state` — `apply.py` can report success while authoritative state remains wrong; the grader functionally re-executes the candidate command and separately checks final state.

`eval_harness.py` provides:

- `list` — researcher-side preregistered case inspection;
- `prepare` — copy only agent-visible fixture state and return `case_id + workspace + prompt`, without `expected_output`;
- `grade` — run the hidden/out-of-trial deterministic grader;
- `record` — create an immutable per-trial U0/U1 receipt;
- `summarize` — preserve matched replicate effects instead of collapsing U0/U1 into one scalar.

The full repo/manifest/grader/`list` output is researcher-side material. A clean evaluated agent should receive only the intended condition, the `prepare` prompt, and the prepared workspace.

## Causal Run-Configuration Contract

Every new receipt requires `--run-config`. The structured configuration has three roles:

- `matched` — causal context that must match across U0/U1: prompt language, provider/model/snapshot, harness/version, tool set and policy, reasoning effort, sampling controls, and resource limits;
- `intervention` — condition-specific delivery metadata: U0 uses `delivery_form=none`; U1 uses `delivery_form=force-loaded-skill`, with metadata/body language, description variant, and available-skill-set hash retained explicitly;
- `trial` — clean-environment ID, trial ID, and UTC timestamp.

The harness validates schema and required identities, rejects duplicate tools or malformed hashes/timestamps, cross-checks model/harness identity and delivery form against top-level trial fields, and records both canonical full-config SHA-256 and a canonical `matched` SHA-256.

Receipt loading is fail-closed: missing run-config evidence, invalid schema, internal identity/intervention contradiction, or stale/tampered config hashes are rejected. Two individually valid U0/U1 receipts with different `matched` hashes are retained but classified `not_comparable`; they are not allowed to manufacture a treatment effect.

### Receipt contract

Each receipt binds:

- case / condition / pair / replicate;
- model and external harness identity;
- exact U1 runtime-skill SHA-256, or explicit no-skill U0 state;
- validated structured run configuration plus full/matched hashes;
- final workspace SHA-256;
- transcript SHA-256 and byte count;
- canonical cost metrics (`input_tokens`, `output_tokens`, `tool_calls`, `wall_time_ms`), with extra provider metrics allowed;
- deterministic grader result;
- exact eval-harness, manifest, fixture, and grader SHA-256 provenance.

Existing receipt paths are rejected instead of overwritten. Keep every replicate, including failures.

### Summary contract

Summary groups by `case_id + pair_id` and preserves each replicate:

- U0 fail / U1 pass → `u1_gain`;
- U0 pass / U1 fail → `u1_harm`;
- both pass → `same_pass`;
- both fail → `same_fail`.

A valid pair is `not_comparable` when one condition is missing, matched causal context differs, model/harness identity differs, evaluator provenance differs, or duplicate receipts claim the same condition and replicate. Invalid/tampered receipts are rejected before comparison. No universal aggregate score is emitted.

### Test-first evidence

Fresh-runner and causal-config infrastructure was built in isolated RED→GREEN slices. Relevant GREEN runs include:

- agent-safe `prepare` boundary: `34671916622`;
- canonical metrics validation: `34671994103`;
- trial identity validation: `34672058813`;
- paired U0/U1 summary: `34672166288`;
- mismatched-config rejection: `34672244402`;
- duplicate condition/replicate rejection: `34672328794`;
- canonical run-config binding: `34672801141`;
- run-config schema validation: `34673945952`;
- identity/intervention binding: `34674028019`;
- matched causal-context comparison: `34674167891`;
- receipt self-integrity plus valid mismatch semantics: `34674299158`;
- mandatory run-config at record boundary: `34674428856`;
- mandatory run-config at receipt-ingress boundary: `34674620716`.

Earlier anti-forgery false-completion grading (`34670974459`) and anti-hardcode normalization grading (`34671025273`) remain part of the infrastructure history.

All runs above are **infrastructure/regression evidence**, not evidence that Verified Delta improves an agent.

## Behavioral Evidence Boundary

No fresh isolated-agent U0/U1 comparison has been completed.

The current conversation has read the skill, research state, eval design, expected failure families, grader behavior, and run-config contract. It is contaminated and cannot serve as clean U0 or U1 behavioral evidence. Do not manufacture trials from this context.

The next real experiment must use genuinely fresh model/agent contexts under matched configuration:

- `U0`: no Verified Delta guidance;
- `U1`: force-load the exact current `verified-delta/SKILL.md`;
- same case and exact `matched` run configuration;
- clean workspace/environment per trial;
- retain every transcript and replicate, including failures;
- record each trial through the mandatory run-config receipt contract;
- inspect every `not_comparable`, `u1_harm`, minority failure, and surprising grader result directly.

Primary outcomes are final-task success and serious failure. Also retain no-op/action calibration, false completion, unnecessary actions, tool/token/time cost, and transcript evidence. A skill-induced failure (`U0` succeeds while `U1` fails) is first-class evidence, not noise.

A structurally valid receipt still does **not** independently prove that the external model call, clean environment, or skill injection actually occurred. External runner evidence and transcripts remain necessary.

## Controller Hypotheses Still Alive

Do not optimize later layers until U0/U1 shows that intervention is useful.

- `R0` — no guidance.
- `R1` — current 446-word Verified Delta.
- `R2` — materially compressed Verified Delta.
- `R3` — compact evidence-gated control loop.
- `R4` — goal/invariant contract.
- `R5` — verification-focused kernel.
- `R6` — constrained receding-horizon controller: broad enough planning, short commit horizon.
- `R7` — explicit belief/state controller outside raw dialogue history.
- `R8` — harness-gated controller with external validation/action gates.

These are hypotheses only. No ranking is a result.

If prompt guidance earns a signal, later controller-locus work may compare no controller, prompt-only, explicit state/belief, and external verifier/action-gate interventions. Credit improvement to the layer that causally produced it.

## W5 Research Boundary

Nolane World 0.12.0 W5 world `world5_0ad739c41440565a1a83` remains blocked at `r4` **Assumption Stress**, which requires a genuinely independent verifier. This context must not self-sign it.

The unresolved question remains:

> What is the minimum sufficient behavioral controller that reduces invalid or unverified task-state transitions without introducing passivity, overthinking, myopic minimality, excess context cost, or hidden harness dependence?

## Open Debts

1. **Clean U0/U1 execution missing.** This is the immediate behavioral boundary.
2. **External execution attestation remains external.** Structured receipts bind declared configuration but cannot independently prove model invocation, isolation, or skill injection.
3. **Independent W5 r4 missing.** Do not self-sign it from this context.
4. **Primitive competition unexecuted.** R0–R8 remain hypotheses.
5. **Controller-locus factorization unexecuted.** Prompt vs explicit state vs verifier effects are unknown.
6. **Semantic ablation unexecuted.** Run only after a behavior/locus family earns optimization.
7. **Activation and natural prevalence unmeasured.** Trigger, compliance, boundary, distractors, and workload prevalence remain unknown.
8. **Cross-lingual activation unmeasured.** Do not infer language robustness from general model capability.
9. **Hidden cross-domain/language holdout missing.** Final generalization claims remain blocked.
10. **Runtime portability unmeasured.** Any future result is harness/model scoped until replicated.
11. **Umbrella-versus-micro-skill granularity unknown.** Do not split the runtime package because modularity looks cleaner.
12. **Myopic-minimality and belief-collapse probes remain unexecuted.** They matter only if the first utility comparison justifies further controller research.

## Rejected Directions

- Bigger is stronger.
- More rules imply more intelligence.
- Literal “million reviews” without recorded evidence.
- Deep reasoning on every task.
- Multi-agent by default.
- Treating past state as authority.
- Treating shorter or longer as automatically better.
- Treating `Use when...` or ≤500 words as universal Agent Skills syntax.
- Optimizing activation metadata before content utility.
- Crediting prompt text for behavior actually enforced by a harness.
- Trusting an agent-writable marker as proof that a command ran correctly.
- Calling mismatched U0/U1 receipts a treatment effect.
- Letting duplicate receipts resolve by input order.
- Accepting missing or tampered run-config evidence as analyzable trial data.
- Pooling languages, harnesses, tasks, repeated trials, or conflicting metrics into a convenient scalar.
- Averaging away minority failures.
- Overwriting old trial receipts.
- Writing candidate wording from final holdout failures.
- Splitting the umbrella skill before utility evidence supports a narrower boundary.

## Next Best Action

Do **not** edit `verified-delta/SKILL.md`.

Use the hardened executable lab in a genuinely fresh isolated-agent/model harness and collect the first matched U0/U1 receipts for the three development cases. Start small, preserve the exact structured causal configuration, retain independent runner evidence, inspect every transcript, and decide whether the current skill produces any practically meaningful marginal utility without new passivity, ceremonial verification, unnecessary action, or excessive cost.

If U1 does not beat U0 on a target failure family, do not tune metadata to hide the result. Narrow, factor, replace, or remove guidance. If a benefit appears, expand only the failure families justified by that evidence before any wording optimization.

## Update Rule

After meaningful work, replace stale state. Keep only current invariants, observed state, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action.
