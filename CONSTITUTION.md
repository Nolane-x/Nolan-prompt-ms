# Nolane Prompt MS Constitution

`verified-delta/SKILL.md` governs task behavior. This file governs every future edit to the skill.

## Mission

Maximize **behavioral leverage per token**.

The core primitive is:

> establish current truth → preserve invariants → resolve material uncertainty → commit the smallest sufficient change → verify reality → stop.

Rule count, prose volume, model coverage, and apparent sophistication are not success metrics.

## Millionfold Standard

“Research a million times for one word” is a quality bar, not a fabricated count. Never claim N reviews, runs, or iterations without recorded evidence.

Every sentence in `verified-delta/SKILL.md` must earn residency through seven tests:

1. **Failure** — it addresses an observed or testable failure.
2. **Delta** — changing or removing it can change behavior.
3. **Uniqueness** — another sentence does not already do the same job.
4. **Transfer** — it generalizes beyond one accidental example.
5. **Falsifiability** — a scenario can show it harmful or insufficient.
6. **Observability** — compliance can be judged from behavior or artifacts.
7. **Compression** — no shorter wording keeps the same operational meaning.

Fail one test: delete, merge, move, or rewrite.

## Incumbent Has No Privilege

`Verified Delta`, its tuple, its headings, and the Agent Skill form are hypotheses, not protected architecture.

Before treating the current kernel as the compression target, keep materially different rivals alive. At minimum, behavioral evaluation may compare:

- no added guidance;
- the current full Verified Delta kernel;
- a materially shorter Verified Delta variant;
- a compact evidence-gated feedback/control loop;
- a goal-and-invariant contract;
- a verification-focused kernel.

Freeze candidate wording before selection-validation. Compare matched tasks, serious-failure behavior, and context/tool/latency cost. Where candidate lengths differ materially, include a token-matched control when practical so semantic benefit is not confused with prompt volume.

A materially shorter rival that is non-inferior on the preregistered behavioral criteria and strictly cheaper defeats the incumbent. Replace or prune the incumbent; do not invent a new reason to preserve familiar prose.

If no-guidance performs equivalently, prefer no added guidance until an observed failure creates a residency claim.

## Controller Locus Discipline

Do not confuse **what the controller says** with **where control is implemented**. Treat these as separate intervention loci:

- prompt / skill semantics;
- explicit state or belief representation;
- context-selection / assembly policy;
- external validation, action gating, or repair feedback in the harness.

Credit an improvement to the layer that causally produced it. A harness-blocked invalid action is not evidence of prompt compliance; a better state estimator is not evidence that longer instructions are better.

When a deterministic or harness-level mechanism can enforce an invariant more reliably and cheaply than prose, prefer that mechanism and shrink runtime guidance to the residual behavior that still needs model judgment.

## Evidence Before Expansion

No rule enters the core because it sounds wise.

For behavior-changing edits:

`control → candidate → comparison → pressure case → ablation → retain/delete`

Ablation is mandatory: if removing the sentence does not worsen the target behavior, it has not earned core residency.

When fresh isolated behavioral evaluation is unavailable, keep the gate **OPEN**. Static review, agreement, and source support are not behavioral proof.

## Word Residency

A content-bearing phrase should do at least one job:

- define a trigger;
- distinguish state;
- constrain action;
- preserve an invariant;
- require evidence;
- define a stop condition.

Delete decorative intensifiers, repeated certainty, motivational prose, and explanations already implied by a sharper rule.

Prefer operational contrasts:
- `observed / inferred / unknown` over “be careful with facts”;
- `smallest sufficient delta` over “make minimal high-quality changes”;
- `verified target reached → stop` over “avoid unnecessary work.”

Compression must not become obscurity.

## Scope Firewall

This repository is not a model catalog, prompt-template library, general cognitive runtime, multi-agent framework, memory database, tool registry, or encyclopedia.

An outside idea may enter only when it compresses into the Verified Delta primitive and passes the residency tests.

A new file requires a distinct loading or maintenance reason. “More organized” is insufficient.

## Utility Before Compression

Compression is an optimization, not an acceptance criterion.

A candidate must first demonstrate useful behavioral effect against a matched no-guidance control. Static word count, elegance, or adherence to a house style cannot substitute for that comparison.

The current **≤ 500 words** target is research pressure, not an Agent Skills requirement and not a deterministic validity gate. A longer candidate may temporarily survive when fresh evidence shows that the added semantics earn their cost; that creates explicit compression debt and must later face ablation. A shorter candidate receives no credit if it loses useful behavior.

Likewise, description wording such as `Use when...` is an activation hypothesis to test, not a static syntax law. Deterministic validation should enforce the external format contract; behavioral evaluation decides which valid wording is useful.

## Size Pressure

- `verified-delta/SKILL.md`: working target **≤ 500 words**, subordinate to demonstrated utility.
- Supporting runtime prose: add only when an eval proves progressive disclosure is needed.
- Examples: one excellent example over a catalog.
- Runtime dependencies: zero unless evaluation demonstrates otherwise.

If an invariant can be checked deterministically, enforce it in `verify.py` instead of spending runtime skill tokens on it.

Crossing a target creates explicit compression debt in `STATE.md`; it does not by itself make a candidate invalid.

## Epistemic Discipline

Use four statuses for project claims:

- **observed** — directly inspected or measured;
- **supported** — backed by evidence but not directly measured here;
- **hypothesis** — plausible and testable;
- **unknown** — unresolved.

Summaries must not upgrade status. Past sessions are evidence, not authority. Current repository state and fresh evidence outrank old plans.

Do not call the skill verified, best, complete, or converged while a relevant gate remains open.

## Change Protocol

Before editing:
1. read `STATE.md`;
2. inspect current repository reality;
3. name the exact failure or research question;
4. locate the smallest responsible file.

During editing:
- change one semantic behavior at a time;
- do not mix cleanup with behavior change;
- do not widen scope to justify a preferred solution.

After editing:
1. run `python verify.py`;
2. run the relevant behavioral eval or leave its gate open;
3. scan for semantic duplication;
4. update `STATE.md`;
5. rerun the verifier, then stop.

## Continuity

`STATE.md` is a bootloader, not a diary. Keep only:
- current invariant;
- latest observed repository state;
- open debts/unknowns;
- rejected approaches worth not repeating;
- next evidence-producing action.

Never replay transcript history into state. A fresh session must re-check the world before obeying a stored next step.
