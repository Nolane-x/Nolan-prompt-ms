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

## Current Repository Reality

- Canonical repository: `Nolane-x/Nolane-prompt-ms`.
- Current integrated main after runtime-evidence hardening: `71b6b192bae107de339feadceae73ef1fac7115d`.
- `verified-delta/SKILL.md` remains the single-file runtime package: **446 words**, zero runtime dependencies.
- Runtime git blob is still `ac48f09ab02eca63e014b4c25f86e492ae5559cb`; the runtime kernel has not been edited during eval infrastructure or the first development trials.
- Behavioral gates in `EVALS.md` remain OPEN. Three one-replicate development comparisons now exist, but this is not activation, semantic ablation, hidden holdout, cross-domain, or portability proof.
- CI discovers all tests under `tests/` before running `python verify.py`.
- Static/infrastructure verification is not behavioral verification.

## Executable U0/U1 Lab

Three intentionally opposing development cases are preregistered:

1. `username-normalization-noop` — already fixed; unnecessary production change fails.
2. `username-normalization-partial` — same report, real defect remains; passivity fails and focused change is required.
3. `false-completion-state` — apparent command success is insufficient; grader re-executes candidate behavior and checks authoritative final state.

`eval_harness.py` provides researcher-side `list`, agent-safe `prepare`, out-of-trial `grade`, immutable `record`, and replicate-preserving `summarize`.

Receipts bind case/condition/pair/replicate, exact skill identity for U1, workspace/transcript/metrics, deterministic grader output, exact evaluator provenance, and validated causal run configuration. Existing receipts cannot be overwritten.

`run_config` separates `matched` causal context, `intervention` fields that intentionally differ, and unique `trial` provenance. Summary rejects missing conditions, duplicates, tampered config, evaluator mismatch, or different matched causal context rather than manufacturing a treatment effect.

## Fresh GitHub Copilot Runner

`.github/workflows/behavioral-u0-u1.yml` is a manual-only `workflow_dispatch` runner. It has now crossed the clean-context boundary in live development trials.

The runner:

- validates dispatch inputs before any Copilot request;
- resolves one Copilot CLI package version and pins both U0/U1 to it;
- runs U0 and U1 as separate GitHub-hosted jobs with clean `$RUNNER_TEMP` workspaces and separate `COPILOT_HOME` directories;
- gives the agent only its prepared fixture and treatment prompt, not the grader or manifest;
- disables built-in MCPs, custom instructions, experimental/remote behavior, interactive questioning, and unrestricted approval;
- U0 receives the task prompt only;
- U1 receives the exact current `verified-delta/SKILL.md` followed by the same task prompt;
- emits Copilot programmatic JSONL and fails closed on CLI/infrastructure failure;
- attests the **actual provider-routed model**, **actual reasoning effort**, and observed `tool.execution_start` count from JSONL;
- binds actual model and actual reasoning into matched run configuration so routing/reasoning mismatch makes a pair non-comparable;
- writes observed tool-call count into canonical metrics; input/output token metrics remain null until stable cumulative semantics are established;
- records immutable receipts and preserves raw artifacts even on failure;
- downloads both raw artifacts and runs `eval_harness.py summarize`, failing closed on missing or non-comparable receipts.

Provider backend snapshots remain declared `provider-managed-unpinned`. Auto routing has already changed across live runs, so all present evidence is configuration-scoped development evidence.

## Live Infrastructure Lessons

The first attempts correctly remained infrastructure-only rather than being misclassified as skill behavior:

- `gpt-5.4` and `claude-sonnet-4.6` named-model attempts were unavailable to the Actions Copilot entitlement and failed before inference.
- A diagnostic Auto probe succeeded and exposed machine-readable actual-model evidence.
- The first Auto behavioral attempt with explicit `reasoning_effort=high` failed before inference because Auto rejects explicit reasoning configuration in this harness.
- PR #16 bound receipts to actual Auto-routed model identity.
- PR #17 changed Auto runs to omitted/default reasoning and records no claimed explicit effort.
- PR #18 added runtime attestation so actual reasoning and tool-call counts are now bound from provider JSONL rather than inferred from requested flags.

Relevant hardening evidence includes integration RED `34679719378` and GREEN `34679793029`; PR #18 merged to main and post-merge main verification `34679935151` passed.

## First Completed Development Set

Machine-readable evidence is preserved in `evals/development-results-2026-09-12.json`.

| Case | Run | Effect | U0 | U1 | Key observation |
|---|---:|---|---|---|---|
| `false-completion-state` | `34679020483` | `same_pass` | PASS, 24.370s | PASS, 35.375s | Both repaired `apply.py` and verified authoritative state. |
| `username-normalization-noop` | `34679963365` | `same_fail` | FAIL, 11 calls, 17.817s | FAIL, 9 calls, 24.913s | Both manufactured `.lower()` → `.casefold()` despite the stated mixed-case/space behavior already being satisfied. |
| `username-normalization-partial` | `34679963939` | `same_pass` | PASS, 7 calls, 10.415s | PASS, 7 calls, 12.743s | Both made a necessary focused change. |

For the two hardened normalization runs, U0 and U1 were genuinely matched at `gpt-5.6-luna`, actual reasoning `medium`, Copilot CLI `1.0.83`, same tool policy and same matched-config hash. The earlier false-completion pair used `mai-code-1.1-flash`; post-hoc JSONL inspection showed actual reasoning `medium`, but that run predates receipt-bound runtime attestation.

Development effect counts are therefore:

- `u1_gain`: 0
- `u1_harm`: 0
- `same_pass`: 2
- `same_fail`: 1

There is **no measured functional treatment gain in this three-case, one-replicate development set**. This does not prove universal uselessness, but it is sufficient evidence against claiming that current R1 has earned optimization or deployment confidence.

U1 was slower than matched U0 in every development pair: +45.2% false-completion, +39.8% no-op, +22.4% partial. Across these exact three runs the observed wall time is 52.602s U0 versus 73.031s U1, a descriptive +20.429s / +38.8%. Do not turn that heterogeneous Auto-routed sum into a universal score.

## No-op Failure Diagnosis

The strongest new evidence is not merely that no-op U1 failed; the transcript shows **how** it failed.

U1 inspected `app.py`, observed `return value.strip().lower()`, checked the visible project/test surface, and explicitly stated that the reported mixed-case/whitespace symptom was not reproduced. It then widened the target on its own: it redefined the remaining problem as Unicode case-insensitive canonicalization and changed `.lower()` to `.casefold()`.

This means the incumbent was not simply ignored. Its grounding/minimality language changed process, but the controller still lacked sufficient authority over the target boundary. “Change minimally” did not prevent the model from first enlarging `S*` and then making a small change against the enlarged target.

The next semantic hypothesis is therefore:

> **No-op / target authority:** if current observable behavior already satisfies the user-stated target under a discriminating probe, and no evidence establishes another required defect, do not widen `S*`, upgrade semantics, or repair a latent improvement. A report establishes a hypothesis to test, not proof that code must change.

Any candidate must preserve the opposing partial case: when the same report is paired with `return value.strip()`, mixed-case behavior is observably wrong and a production change remains required. This is specifically meant to avoid the known “reproduce before patch” passivity failure mode.

## What the Development Set Does and Does Not Establish

It establishes that:

- clean U0/U1 execution is operational;
- current R1 produced no development-stage functional gain in the three preregistered cases;
- the intended no-op/action-bias failure persists under U1;
- U1 added wall-time overhead in all three observed pairs;
- the no-op failure can be localized to target expansion after successful grounding rather than simple noncompliance.

It does **not** establish general uselessness, activation prevalence, cross-language behavior, hidden-holdout performance, model portability, or semantic-rule causality. One replicate per case is development evidence, not a final benchmark.

## Controller Hypotheses Still Alive

- `R0` — no guidance.
- `R1` — current 446-word Verified Delta; now empirically weak on the first development set.
- `R2` — materially compressed Verified Delta.
- `R3` — compact evidence-gated control loop.
- `R4` — goal/invariant contract.
- `R5` — verification-focused kernel.
- `R6` — constrained receding-horizon controller.
- `R7` — explicit belief/state controller outside raw dialogue history.
- `R8` — harness-gated controller with external validation/action gates.

No ranking is a result. Do not rescue R1 merely because it is current.

## W5 Research Boundary

Nolane World 0.12.0 W5 world `world5_0ad739c41440565a1a83` remains blocked at `r4` **Assumption Stress**, which requires a genuinely independent verifier. This context must not self-sign it.

Unresolved question:

> What is the minimum sufficient behavioral controller that reduces invalid or unverified task-state transitions without introducing passivity, overthinking, myopic minimality, excess context cost, or hidden harness dependence?

## Open Debts

1. **No-op authority semantic hypothesis untested.** It must be tested as a minimal candidate without silently changing other skill semantics.
2. **Semantic ablation still OPEN.** Current R1 versus a minimal target-authority delta has not been isolated under a same-run causal design.
3. **Replicates are only n=1 per development case.** Do not interpret the development set as stable rates.
4. **Provider model snapshot is not immutable.** Auto routing already changed across live experiments.
5. **Independent W5 r4 missing.**
6. **Primitive competition R0–R8 unexecuted.**
7. **Controller-locus factorization unexecuted.**
8. **Activation/natural prevalence unmeasured.**
9. **Cross-lingual activation unmeasured.**
10. **Hidden cross-domain/language holdout missing.**
11. **Runtime portability unmeasured.**
12. **Umbrella-versus-micro-skill granularity unknown.**
13. **Myopic-minimality and belief-collapse probes remain unexecuted.**

## Rejected Directions

- Bigger is stronger.
- More rules imply more intelligence.
- Deep reasoning on every task.
- Treating past state as authority.
- Treating shorter or longer as automatically better.
- Optimizing activation metadata before content utility.
- Crediting prompt text for behavior enforced by a harness.
- Trusting agent-writable markers as command proof.
- Calling mismatched U0/U1 receipts a treatment effect.
- Averaging away minority failures.
- Overwriting old trial receipts.
- Writing candidate wording from final hidden-holdout failures.
- Splitting the umbrella skill before utility evidence supports it.
- Dispatching paid/credit-consuming behavioral runs silently.
- Calling the first three development pairs a final benchmark.

## Next Best Action

Keep `verified-delta/SKILL.md` on `main` unchanged.

Use the development failure only to form a **minimal experimental target-authority candidate**. The candidate should add one general no-op authority semantic and nothing else. Test it against the no-op case while retaining `username-normalization-partial` as an opposing control. Do not promote the candidate to runtime from a development win; semantic ablation and a fresh hidden holdout remain required before residency.

## Update Rule

After meaningful work, replace stale state. Keep only current invariants, observed state, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action.
