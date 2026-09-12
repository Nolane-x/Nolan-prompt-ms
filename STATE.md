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
4. run `python verify.py`;
5. re-check every stored claim that could have gone stale;
6. continue from the next evidence-producing action, not old prose momentum.

Past-self state is a recovery aid, never authority.

## Current Invariant

Maximize **behavioral leverage per token and per unit of controller complexity**.

The current incumbent is Verified Delta, but its wording, tuple, name, skill packaging, size target, and even prompt-level implementation are hypotheses. Utility comes before compression. A shorter rival, a longer evidence-backed candidate, an explicit state layer, a harness-level controller, or no added guidance may replace the incumbent if controlled evidence shows a better behavior/cost frontier.

## Observed Repository State

- `verified-delta/SKILL.md` remains the single-file runtime package, 446 words, zero runtime dependencies.
- The runtime kernel and its current description have not been behaviorally edited during structural, multilingual, W5, primitive-competition, controller-locus, or utility-first research.
- `EVALS.md` keeps Activation, RED baseline, GREEN comparison, Ablation, and Cross-domain holdout OPEN.
- `CONSTITUTION.md` has **Incumbent Has No Privilege**, **Controller Locus Discipline**, and **Utility Before Compression**.
- Static CI on `main@34a8534d759e1cc4f5f8a27f8de65ac61440c60a` passed unit tests and `python verify.py` after the controller-locus merge.
- A test-first governance correction demonstrated that the old verifier wrongly treated project heuristics as Agent Skills syntax: it rejected valid descriptions that did not start with `Use when`, rejected descriptions above 500 characters even though the standard permits 1024, and rejected bodies above 500 words.
- RED evidence: Actions run `34668529074` failed exactly on those four expectations while unrelated verifier tests passed.
- GREEN evidence: Actions run `34668747588` passed all 13 verifier tests and `python verify.py` after deterministic validation was narrowed to non-empty description + 1024-character maximum and the hard 500-word acceptance gate was removed.
- The **≤500-word** value remains a working compression target in the Constitution, not a deterministic validity rule.
- No fresh isolated-agent U0/U1 behavioral comparison has been completed.

Static checks, literature, W5 reasoning, conceptual coverage, word count, and elegance are not behavioral verification.

## Usefulness Research Frame

A skill earns runtime residency only through **incremental utility**, not by restating good practice.

For a matched task, compare no-guidance `U0` with force-loaded current-skill `U1` and retain the task as the primary paired unit. Record at least:

- target-state success;
- skill-induced functional failure: `U0` succeeds while `U1` fails;
- serious/invariant failure;
- false completion;
- no-op versus necessary-action calibration;
- unnecessary actions or ceremonial verification;
- token/tool/time cost where available;
- transcript evidence explaining the causal difference.

The first utility round should stay deliberately small and discriminating. Start with three executable development cases rather than growing a benchmark before the cases prove useful:

1. **Fully fixed / no-op:** the reported defect is already absent; the correct result is no production change.
2. **Partially fixed opposing control:** surface wording is closely matched, but one real defect remains; the agent must change production state rather than generalizing no-op behavior into passivity.
3. **False completion:** an intermediate tool/command reports success while the intended final state is still wrong; grading checks final state rather than the agent's claim or command exit status.

Run each case in clean contexts with and without the skill. Do not tune the skill after seeing a final holdout. If a development case cannot discriminate the claimed behavior, repair or discard the case instead of optimizing prose against it.

If the incumbent shows no practically meaningful benefit on high-signal failure families, do not rescue it by tuning metadata. Narrow, factor, replace, or remove guidance. If benefit appears only in one or two families, test whether narrower micro-skills beat the umbrella skill before claiming broad utility.

## W5 Research State

A fresh Nolane World 0.12.0 W5 world was opened for the controller-locus question:

`world5_0ad739c41440565a1a83`

Research MicroVM evidence is complete through:

- `r1` Question Certificate;
- `r2` Evidence Map;
- `r3` Counterexample Retrieval.

The cursor is blocked at `r4` **Assumption Stress**, which requires an independent verifier. This context must not self-sign it. W5 closure remains OPEN.

The refined W5 question is:

> What is the minimum sufficient behavioral controller that reduces invalid or unverified task-state transitions without introducing passivity, overthinking, myopic minimality, excess context cost, or hidden harness dependence?

## Representation Shift: Prompt → Closed-Loop Control Stack

Do not model this project as prompt wording alone. Separate five functions:

1. **State estimation** — what current world state or belief is supported by evidence?
2. **Target / constraint representation** — what must become true and what must remain true?
3. **Action selection** — what intervention or probe should happen next?
4. **Commit policy** — how much of a plan should be executed before observing again?
5. **Verification / feedback** — what external evidence accepts, rejects, repairs, or stops execution?

A sixth function, **context assembly**, decides which instructions/state/evidence the model sees at each step.

Prompt text may implement some of these functions, but explicit state machinery or harness code may implement them more reliably. Credit gains to the actual causal layer.

## Rival Controller Ecology

Keep every materially distinct rival live until controlled evidence eliminates it:

1. **R0 — No guidance.** Modern model/harness behavior may already be sufficient.
2. **R1 — Full Verified Delta.** Current 446-word incumbent.
3. **R2 — Compressed Verified Delta.** Same claimed semantics with materially less notation/prose.
4. **R3 — Evidence-Gated Control Loop.** Observe → target/constraints → smallest justified action → act → verify → update/stop.
5. **R4 — Goal/Invariant Contract.** Lock target and invariants; resolve only decision-changing unknowns; act; verify.
6. **R5 — Verification Kernel.** Minimal guidance focused on evidence-backed completion and repair after failed verification.
7. **R6 — Constrained Receding-Horizon Controller.** Plan as far ahead as uncertainty/risk requires, but commit only the smallest safe action or prefix; observe, update, verify, and replan. This explicitly separates **planning horizon** from **commit horizon**.
8. **R7 — Explicit Belief-State Controller.** Maintain a structured belief/current-state representation outside raw dialogue history; update it from observations and expose the policy only to the current belief plus target/constraints.
9. **R8 — Harness-Gated Controller.** The model proposes; external validators/gates control acceptance, irreversible actions, budgets, repair feedback, and completion. Prompt guidance is reduced to residual judgment not enforceable by the harness.

Current conceptual ranking is not a result. R6–R8 were added because they make causally different predictions from prompt-only rivals.

## Why R6 Is Distinct

The phrase “smallest sufficient delta” can become **myopic** if interpreted as the smallest immediate patch. R6 separates:

- **exploration/planning horizon** — may be long enough to expose downstream dependencies;
- **commit horizon** — stays short enough to preserve reversibility and feedback.

Its decisive test is a task where the smallest immediate intervention creates a later dead end or expensive repair, while a slightly broader plan with one-step commitment succeeds.

If R3 and R6 tie on such tasks, the extra receding-horizon concept has no residency claim.

## Why R7 Is Distinct

Partial observability is not only “uncertainty in prose.” A history-conditioned LLM can collapse onto the wrong hidden state even when every individual observation is plausible.

R7 predicts that an explicit belief/state layer will improve calibration under ambiguous observations, consistency across sequential evidence, resistance to premature commitment, recovery after contradictory observations, and context efficiency when raw history is long.

External belief-state research motivates the test but does not prove R7 for this project.

## Why R8 Is Distinct

External research on structured repair feedback, deterministic control, procedure-aware evaluation, evidence-carrying termination, and context assembly motivates testing architecture-level control rather than assuming every invariant belongs in prompt prose.

These results motivate R8 and context-policy experiments. They do not prove that prompt guidance is useless.

## Controller-Locus Experiment

Do not compare only “skill on / skill off.” After U0/U1 establishes that a target failure family is worth intervention, isolate the locus on matched diagnostic tasks.

Core arms:

- `C0` — no added controller;
- `CP` — force-loaded prompt controller only;
- `CB` — explicit state/belief layer only;
- `CV` — external verifier/action gate only.

Only add interaction arms when a main effect justifies the cost:

- `CP+B` — prompt + belief layer;
- `CP+V` — prompt + verifier;
- `CB+V` — belief + verifier;
- full stack only if interactions remain decision-relevant.

Do **not** count behavior prevented by a harness gate as prompt compliance. Do **not** count a better state estimator as evidence that more prompt text helped.

### Decision law

- If `CP ≈ C0`, prompt guidance has no demonstrated marginal utility for that family.
- If `CB > CP` under partial observability, move state tracking out of prose and shrink prompt state-management rules.
- If `CV > CP` on integrity/verification failures, prefer harness enforcement and shrink prompt verification rules to residual judgment.
- If `CP+B` or `CP+V` beats either component alone, retain only the prompt semantics responsible for the interaction.
- If a shorter controller is non-inferior on preregistered success/serious-failure criteria and strictly cheaper, it defeats the longer incumbent.

## Behavioral Program Order

Do not optimize later layers before earlier causal questions are answered:

1. **U0 vs U1** — no guidance vs force-loaded 446-word incumbent, beginning with the three utility cases above.
2. **Primitive competition** — R0–R8 only if U1 demonstrates useful behavior.
3. **Controller-locus factorization** — prompt vs belief/state vs verifier/context layer on failure families where locus matters.
4. **Semantic ablation/compression** — only on the winning primitive/locus family.
5. **Activation and multilingual discovery** — only when on-demand prompt delivery remains relevant.
6. **Form-factor selection** — skill vs always-on vs hybrid vs architecture-only.
7. **Fresh hidden cross-domain/language holdout** — after all adaptive selection is frozen.

## New Discriminating Failure Families

### Myopic Minimality

The locally smallest action appears attractive but creates a downstream dead end, invalid dependency, or much larger repair. The correct agent plans beyond the immediate patch while committing only the smallest safe prefix and re-observing before further commitment.

### Premature Belief Collapse

Sequential observations remain compatible with multiple hidden states. One vivid observation favors the wrong hypothesis but is not discriminating. The correct controller preserves alternative state hypotheses or a calibrated belief until a decisive observation/probe arrives.

These are development hypotheses, not evidence that new runtime wording is required.

## Current External Evidence Pressure

External evidence supports the **tests**, not the incumbent wording:

- recent Skill-Use results separate Trigger, Compliance, and Boundary and show material harness dependence;
- SWE-Skills-Bench reports that most tested public SWE skills add no pass-rate gain while a small set of specialized skills do, so generic skill utility cannot be presumed;
- SkillsBench reports heterogeneous skill effects, including negative task deltas, and favors focused skill sets over comprehensive documentation on its aggregate results;
- 2026 skill-induced-failure analysis reports both functional failures and efficiency regressions caused by skills; excessive verification is a major excessive-procedure failure mode;
- FixedBench exposes action bias on already-fixed issues and the opposing passivity failure when “reproduce before patch” is overgeneralized to partially fixed issues;
- false-success research motivates grading final environment state rather than accepting agent/tool success claims;
- official Agent Skills guidance recommends starting with a few realistic with-skill/without-skill evals, clean contexts, observable assertions, and cost measurement before expanding the suite.

None of these sources establishes that Verified Delta improves this repository's target behavior.

## Open Debts

1. **Clean U0/U1 missing.** This remains the first behavioral experiment.
2. **Three-case executable utility pack missing.** Build and validate the no-op, partially-fixed, and false-completion cases before expanding benchmark breadth.
3. **Independent W5 r4 missing.** Current W5 world cannot advance honestly without a genuinely independent verifier.
4. **Primitive competition unexecuted.** R0–R8 are hypotheses only.
5. **Rival wording unpreregistered.** Do not write R2–R8 from hidden-holdout failures.
6. **Controller-locus factorization unexecuted.** CP/CB/CV effects and interactions are unknown.
7. **Myopic-minimality probe unexecuted.** R3 vs R6 remains unresolved.
8. **Belief-collapse probe unexecuted.** Prompt uncertainty handling vs explicit belief state remains unresolved.
9. **Activation / natural prevalence unmeasured.** Trigger, compliance, boundary, distractors, and real prevalence remain unknown.
10. **Cross-lingual activation unmeasured.** L0–L3 remains protocol only.
11. **Semantic ablation unexecuted.** Run only after a primitive/locus family earns optimization.
12. **Hidden cross-domain/language holdout missing.** Final claims remain blocked.
13. **Runtime portability unmeasured.** Claims remain harness-scoped until replicated.
14. **Umbrella-versus-micro-skill granularity unknown.** Factorization is a hypothesis only; do not split the runtime package without utility/activation evidence.

## Rejected Directions

- Bigger is stronger.
- More rules imply more intelligence.
- Literal “million reviews” without recorded evidence.
- Deep reasoning on every task.
- Multi-agent by default.
- Treating past state as authority.
- Equating behavioral leverage per token with a hard pre-evaluation word ceiling.
- Treating `Use when...` as syntax rather than an activation wording hypothesis.
- Optimizing metadata before content utility.
- Optimizing incumbent prose before primitive/locus selection.
- Treating shorter as automatically better.
- Treating longer as automatically better.
- Crediting a prompt for behavior actually enforced by a harness.
- Treating explicit state machinery as “just more prompt.”
- Using a balanced activation set as deployment prevalence.
- Pooling languages, harnesses, repeated trials, or conflicting metrics into a convenient scalar.
- Writing rival candidates after observing final holdout failures.
- Splitting the umbrella skill into multiple skills merely because modularity looks cleaner.

## Next Best Action

Build the **three-case executable U0/U1 development pack** without changing `verified-delta/SKILL.md`:

`fully fixed / no-op ↔ partially fixed / action required ↔ false completion / final-state check`.

Each case must have a deterministic or otherwise auditable grader, a clean trial contract, and a paired no-guidance/force-loaded-skill execution record. Run the cases in a genuinely fresh agent/model context when such a harness is available.

If U1 earns a practically meaningful benefit without skill-induced functional or efficiency regressions, expand only the failure families justified by the first results. If it does not, narrow, factor, replace, or remove guidance instead of tuning its trigger.

This session has read the incumbent, rivals, and eval hypotheses and cannot serve as a clean control.

## Update Rule

After meaningful work, replace stale state. Keep only current invariants, observed state, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action.
