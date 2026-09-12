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
- `verified-delta/SKILL.md` remains the single-file runtime package: **446 words**, zero runtime dependencies.
- The runtime kernel has not been edited during eval-lab, run-config, or fresh-runner work.
- Behavioral gates in `EVALS.md` remain OPEN: Activation, RED baseline, GREEN comparison, Ablation, and Cross-domain holdout.
- Static/infrastructure verification is not behavioral verification.
- CI discovers all tests under `tests/` before running `python verify.py`.

## Executable U0/U1 Lab

Three intentionally opposing development cases exist:

1. `username-normalization-noop` — already fixed; unnecessary production change fails.
2. `username-normalization-partial` — same report, real defect remains; passivity fails and focused change is required.
3. `false-completion-state` — apparent command success is insufficient; grader re-executes candidate behavior and checks authoritative final state.

`eval_harness.py` provides researcher-side `list`, agent-safe `prepare`, out-of-trial `grade`, immutable `record`, and replicate-preserving `summarize`.

Receipts bind case/condition/pair/replicate, exact skill identity for U1, workspace/transcript/metrics, deterministic grader output, exact evaluator provenance, and a validated causal run configuration. Existing receipts cannot be overwritten.

`run_config` separates:

- `matched` causal context that must be equal across U0/U1;
- `intervention` fields that intentionally differ by condition;
- `trial` provenance that must be unique and auditable.

Receipt loading rejects missing/tampered run-config evidence and internal identity/intervention contradictions. Summary refuses to manufacture a treatment effect from missing conditions, duplicate receipts, mismatched evaluator provenance, or different matched causal context.

## Manual Fresh Runner

Branch work introduces `.github/workflows/behavioral-u0-u1.yml`, a **manual-only `workflow_dispatch` runner** using GitHub Copilot CLI. It is not triggered by push or pull request and has not been manually dispatched during this work.

The workflow is designed to cross the previous clean-context boundary without using this contaminated chat as a trial:

- validates positive replicate and nonblank model input before any model trial;
- resolves one Copilot CLI package version and pins both U0/U1 to it;
- runs U0 and U1 as separate GitHub-hosted jobs;
- uses clean `$RUNNER_TEMP` workspaces and separate `COPILOT_HOME` directories;
- gives Copilot only the prepared workspace, not the grader/manifest as task context;
- disables built-in MCPs, custom instructions, experimental/remote behavior, interactive questioning, and unrestricted tool approval;
- restricts the available tool set and tool permission policy;
- U0 receives only the task prompt;
- U1 receives the exact current `verified-delta/SKILL.md` followed by the same task prompt;
- successful invocations are recorded through the existing mandatory run-config receipt contract;
- Copilot CLI/infrastructure failure produces infrastructure evidence but no behavioral receipt;
- raw artifacts are uploaded even on failure;
- a final job downloads both artifacts, runs `eval_harness.py summarize`, and fails closed on missing/non-comparable receipts while preserving a pair-summary artifact.

The workflow pins Copilot CLI package version, requested model name, reasoning effort, tool policy, and budget per pair. The model backend snapshot is still declared `provider-managed-unpinned`; initial results therefore remain configuration-scoped development evidence, not portability proof.

Token/tool-call metrics remain explicit `null` when the runner cannot observe reliable values. Never estimate missing metrics.

**Cost boundary:** a manual behavioral dispatch may consume GitHub Copilot requests/credits. Building, testing, merging, or registering the workflow does not itself dispatch a model trial. Do not dispatch it without explicit authorization for that experimental usage.

## Fresh-Runner TDD Evidence

The runner was built in bounded RED→GREEN slices. Relevant GREEN runs:

- manual-only least privilege skeleton: `34674938813`;
- isolated matrix/sandbox/tool boundary: `34675052639`;
- exact U0/U1 treatment + receipt path: `34675192330`;
- pinned pair runtime + fail-closed summary: `34675292121`;
- input preflight before trial: `34675433375`.

Earlier run-config/receipt/grader integrity runs remain valid infrastructure history, including mandatory run-config ingress `34674620716`, anti-forgery false-completion grading `34670974459`, and anti-hardcode normalization grading `34671025273`.

All of these are **infrastructure/regression evidence only**. They do not show that Verified Delta improves an agent.

## Behavioral Evidence Boundary

No fresh isolated-agent U0/U1 behavioral comparison has yet been completed or accepted.

The current conversation has seen the skill, research state, cases, graders, and expected failure families. It cannot be clean U0 or U1 evidence.

The first real experiment should be deliberately small:

- manually dispatch one preregistered case and one replicate through the fresh runner;
- inspect U0 and U1 raw artifacts, transcripts, receipts, and pair summary before running more;
- treat missing receipt, entitlement/auth failure, CLI failure, or non-comparable pair as infrastructure evidence, not behavioral failure;
- retain `u1_harm` and minority failures as first-class evidence;
- do not alter `SKILL.md` from the result until the evidence boundary and treatment attribution are understood.

A strong first target is `false-completion-state` because it directly probes the incumbent's strongest claimed value, but the matched no-op/partial pair remains necessary to detect skill-induced passivity.

## Controller Hypotheses Still Alive

- `R0` — no guidance.
- `R1` — current 446-word Verified Delta.
- `R2` — materially compressed Verified Delta.
- `R3` — compact evidence-gated control loop.
- `R4` — goal/invariant contract.
- `R5` — verification-focused kernel.
- `R6` — constrained receding-horizon controller.
- `R7` — explicit belief/state controller outside raw dialogue history.
- `R8` — harness-gated controller with external validation/action gates.

No ranking is a result. Primitive competition starts only after U0/U1 establishes that intervention is useful enough to optimize.

## W5 Research Boundary

Nolane World 0.12.0 W5 world `world5_0ad739c41440565a1a83` remains blocked at `r4` **Assumption Stress**, which requires a genuinely independent verifier. This context must not self-sign it.

Unresolved question:

> What is the minimum sufficient behavioral controller that reduces invalid or unverified task-state transitions without introducing passivity, overthinking, myopic minimality, excess context cost, or hidden harness dependence?

## Open Debts

1. **First clean U0/U1 execution missing.** This is the immediate behavioral boundary.
2. **GitHub Copilot entitlement/policy/runtime execution unproven.** Static workflow/CI validation cannot substitute for an actual manual dispatch.
3. **Provider model snapshot is not immutable.** Initial results remain provider/harness scoped.
4. **Independent W5 r4 missing.**
5. **Primitive competition R0–R8 unexecuted.**
6. **Controller-locus factorization unexecuted.**
7. **Semantic ablation unexecuted.** Run only after a behavioral family earns optimization.
8. **Activation/natural prevalence unmeasured.**
9. **Cross-lingual activation unmeasured.**
10. **Hidden cross-domain/language holdout missing.**
11. **Runtime portability unmeasured.**
12. **Umbrella-versus-micro-skill granularity unknown.**
13. **Myopic-minimality and belief-collapse probes remain unexecuted.**

## Rejected Directions

- Bigger is stronger.
- More rules imply more intelligence.
- Literal “million reviews” without recorded evidence.
- Deep reasoning on every task.
- Treating past state as authority.
- Treating shorter or longer as automatically better.
- Optimizing activation metadata before content utility.
- Crediting prompt text for behavior enforced by a harness.
- Trusting agent-writable markers as command proof.
- Calling mismatched U0/U1 receipts a treatment effect.
- Averaging away minority failures.
- Overwriting old trial receipts.
- Writing candidate wording from final holdout failures.
- Splitting the umbrella skill before utility evidence supports it.
- Dispatching paid/credit-consuming behavioral runs silently.

## Next Best Action

Do **not** edit `verified-delta/SKILL.md`.

Finish integration of the manual fresh-runner workflow, verify it registers on the default branch without dispatching it, and preserve the runtime kernel unchanged. After explicit authorization for Copilot experimental usage, run exactly one paired fresh trial first, inspect the full evidence, then decide whether additional replicates/cases are justified.

## Update Rule

After meaningful work, replace stale state. Keep only current invariants, observed state, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action.
