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

The current incumbent is Verified Delta, but its wording, tuple, name, skill packaging, and even prompt-level implementation are hypotheses. A shorter rival, an explicit state layer, a harness-level controller, or no added guidance may replace it if controlled evidence shows a better behavior/cost frontier.

## Observed Repository State

- `verified-delta/SKILL.md` remains the single-file runtime package, 446 words, zero runtime dependencies.
- The runtime kernel has not been behaviorally edited during structural, multilingual, W5, primitive-competition, or controller-locus research.
- `EVALS.md` keeps Activation, RED baseline, GREEN comparison, Ablation, and Cross-domain holdout OPEN.
- `CONSTITUTION.md` now has both **Incumbent Has No Privilege** and **Controller Locus Discipline**.
- Static CI on `main@359499fe2d3a7ff325f2783a88d1c2e97b03d4a7` passed unit tests and `python verify.py` after the previous W5 merge.
- No fresh isolated-agent U0/U1 behavioral comparison has been completed.

Static checks, literature, W5 reasoning, conceptual coverage, and elegance are not behavioral verification.

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

R7 predicts that an explicit belief/state layer will improve:

- calibration under ambiguous observations;
- consistency across sequential evidence;
- resistance to premature commitment;
- recovery after contradictory observations;
- context efficiency when raw history is long.

A September 2026 preprint, *Belief-State Engine*, reports gains from external Bayesian belief tracking over history-conditioned LLM baselines on two POMDP-style domains. Treat this as fresh supporting evidence for the **test**, not as proof of generality or of R7 in this project.

## Why R8 Is Distinct

Several 2026 results point toward architecture-level control:

- *Structured Feedback Improves Repair in an LLM Agent Loop* reports large paired gains when an external harness controls validation and returns failure location, observed value, and admissible alternatives.
- *Stable Agentic Control* shows that deterministic tool/interface constraints can provide stability properties independent of the LLM's raw capability in its tested domain.
- *Procedure-Aware Evaluation* shows that task success alone can conceal policy/integrity violations (“corrupt success”).
- *Context Assembly as the Controlled Variable* treats the outer context policy as a control layer around a frozen model.

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

For every arm, report target success, serious failures, invariant violations, false completion, no-op errors, unnecessary actions, tokens/context, tool calls, latency/resources, and task-level reliability.

Do **not** count behavior prevented by a harness gate as prompt compliance. Do **not** count a better state estimator as evidence that more prompt text helped.

### Decision law

- If `CP ≈ C0`, prompt guidance has no demonstrated marginal utility for that family.
- If `CB > CP` under partial observability, move state tracking out of prose and shrink prompt state-management rules.
- If `CV > CP` on integrity/verification failures, prefer harness enforcement and shrink prompt verification rules to residual judgment.
- If `CP+B` or `CP+V` beats either component alone, retain only the prompt semantics responsible for the interaction.
- If a shorter controller is non-inferior on preregistered success/serious-failure criteria and strictly cheaper, it defeats the longer incumbent.

## Behavioral Program Order

Do not optimize later layers before earlier causal questions are answered:

1. **U0 vs U1** — no guidance vs force-loaded 446-word incumbent.
2. **Primitive competition** — R0–R8 only if U1 demonstrates useful behavior.
3. **Controller-locus factorization** — prompt vs belief/state vs verifier/context layer on failure families where locus matters.
4. **Semantic ablation/compression** — only on the winning primitive/locus family.
5. **Activation and multilingual discovery** — only when on-demand prompt delivery remains relevant.
6. **Form-factor selection** — skill vs always-on vs hybrid vs architecture-only.
7. **Fresh hidden cross-domain/language holdout** — after all adaptive selection is frozen.

## New Discriminating Failure Families

Two new development families are required before primitive selection can be trusted:

### Myopic Minimality

The locally smallest action appears attractive but creates a downstream dead end, invalid dependency, or much larger repair. The correct agent plans beyond the immediate patch while committing only the smallest safe prefix and re-observing before further commitment.

This distinguishes “smallest current patch” from “smallest globally sufficient closed-loop intervention.”

### Premature Belief Collapse

Sequential observations remain compatible with multiple hidden states. One vivid observation favors the wrong hypothesis but is not discriminating. The correct controller preserves alternative state hypotheses or a calibrated belief until a decisive observation/probe arrives.

This distinguishes ordinary caution from explicit state-estimation robustness.

These are development hypotheses, not evidence that new runtime wording is required.

## Source-Grounded Findings Added in v6

External evidence currently supports the research questions, not this implementation:

- *Belief-State Engine* (Sep 2026): external belief-state tracking can improve planning consistency/calibration under partial observability in its evaluated domains.
- *Structured Feedback Improves Repair* (Jul 2026): validator-controlled repair feedback materially improves terminal success in paired TextWorld experiments; feedback content matters more than JSON syntax.
- *Procedure-Aware Evaluation* (Mar 2026): reported task success can hide procedural/integrity violations; outcome-only scoring is insufficient.
- *Stable Agentic Control* (May 2026): deterministic tool-mediated constraints can bound agent behavior independently of model capability in a cyber-defense setting.
- *Context Assembly as the Controlled Variable* (Jul 2026): context selection itself can be treated as an outer controller around a frozen model.
- *FixedBench* (May 2026): action bias persists on no-op tasks, and a prompt that reduces over-action can cause the opposite passivity failure on partially fixed tasks.
- *SWE-Skills-Bench* and *Skill-Use* (2026): skill utility, triggering, compliance, and harness dependence must be measured rather than presumed.
- *TextReg* (May 2026): iterative prompt optimization can grow narrow rules and overfit the development distribution.

## Open Debts

1. **Clean U0/U1 missing.** This remains the first behavioral experiment.
2. **Independent W5 r4 missing.** Current W5 world cannot advance honestly without a genuinely independent verifier.
3. **Primitive competition unexecuted.** R0–R8 are hypotheses only.
4. **Rival wording unpreregistered.** Do not write R2–R8 from hidden-holdout failures.
5. **Controller-locus factorization unexecuted.** CP/CB/CV effects and interactions are unknown.
6. **Myopic-minimality probe unexecuted.** R3 vs R6 remains unresolved.
7. **Belief-collapse probe unexecuted.** Prompt uncertainty handling vs explicit belief state remains unresolved.
8. **Activation / natural prevalence unmeasured.** Trigger, compliance, boundary, distractors, and real prevalence remain unknown.
9. **Cross-lingual activation unmeasured.** L0–L3 remains protocol only.
10. **Semantic ablation unexecuted.** Run only after a primitive/locus family earns optimization.
11. **Hidden cross-domain/language holdout missing.** Final claims remain blocked.
12. **Runtime portability unmeasured.** Claims remain harness-scoped until replicated.

## Rejected Directions

- Bigger is stronger.
- More rules imply more intelligence.
- Literal “million reviews” without recorded evidence.
- Deep reasoning on every task.
- Multi-agent by default.
- Treating past state as authority.
- Optimizing metadata before content utility.
- Optimizing incumbent prose before primitive/locus selection.
- Treating shorter as automatically better.
- Treating longer as automatically better.
- Crediting a prompt for behavior actually enforced by a harness.
- Treating explicit state machinery as “just more prompt.”
- Using a balanced activation set as deployment prevalence.
- Pooling languages, harnesses, repeated trials, or conflicting metrics into a convenient scalar.
- Writing rival candidates after observing final holdout failures.

## Next Best Action

Obtain a **fresh isolated-agent harness** and execute `U0 no guidance → U1 force-loaded incumbent` on paired failure/opposing-control tasks.

If U1 earns a practically meaningful benefit, preregister R2–R8 and run primitive competition. Use Myopic Minimality and Premature Belief Collapse to discriminate controller families before sentence-level optimization.

If no isolated harness is available, stop at the evidence boundary. This session has read the incumbent, rivals, and eval hypotheses and cannot serve as a clean control.

## Update Rule

After meaningful work, replace stale state. Keep only current invariants, observed state, unresolved obligations, rejected paths worth preserving, and the next evidence-producing action.
