# STATE — Nolane Prompt MS

**Status:** alpha / research-active  
**Behavioral verification gate:** OPEN  
**Core skill word count:** 446  
**Runtime dependencies:** none

## Boot Sequence

A fresh session that will modify this repository must:

1. read `CONSTITUTION.md`;
2. read `STATE.md`;
3. inspect the current repository and recent changes;
4. re-check every stored claim that could have gone stale;
5. continue from the next evidence-producing action, not from old prose momentum.

Past-self state is a recovery aid, never authority.

## Current Invariant

The repository exists to maximize **behavioral leverage per token** through one primitive:

> current truth → desired truth, preserving invariants, using the smallest sufficient verified delta.

`SKILL.md` must remain broadly applicable, model-agnostic, and small enough to load cheaply.

## Observed Repository State

- `EVALS.md` exists and defines seven pressure scenarios plus the comparison protocol.
- `SKILL.md` exists as the first 446-word Verified Delta kernel.
- `CONSTITUTION.md` defines sentence residency, compression, evidence, scope, and continuity laws.
- No scripts, dependencies, model profiles, prompt templates, or runtime framework have been added.
- No fresh isolated-agent RED/GREEN run has been completed in this repository yet.

## Source-Grounded Design Inputs

The current kernel was distilled from two supplied research documents, not copied wholesale. The retained mechanisms are:

- semantic precision and preservation of exact constraints;
- objective/value invariance while policy may change;
- fact/inference/assumption/unknown separation;
- competing hypotheses only when uncertainty is material;
- cheap high-information probes over prolonged speculation;
- verification distinct from generation;
- externalized continuation state with stale-state checks;
- stopping and compute allocation based on actual decision value.

These mechanisms are inputs to research, not proof that this implementation improves agents.

## Explicit Non-Goals

Do not expand this repository into:

- Prompt Master clone or tool-specific prompt router;
- QX-AI implementation;
- model/version catalog;
- multi-agent orchestration framework;
- memory platform;
- large template/rule collection.

## Open Debts

1. **RED baseline missing.** E1–E7 need fresh no-skill runs.
2. **GREEN comparison missing.** The same scenarios need runs with `SKILL.md`.
3. **Wording micro-tests missing.** Competing phrasings have not been tested with repeated fresh contexts.
4. **Ablation missing.** No core sentence has yet demonstrated behavioral necessity by removal.
5. **Cross-domain holdout missing.** Coding, research, writing, and simple-task cases need unseen tests.

These debts block claims of behavioral verification or convergence.

## Rejected Directions

- Bigger is stronger.
- More rules imply more intelligence.
- Literal “one million reviews” claims without recorded runs.
- Deep reasoning on every task.
- Multi-agent by default.
- Preserving old state without checking current reality.

## Next Best Action

Run the **RED baseline** from `EVALS.md` in isolated fresh contexts without loading `SKILL.md`. Record exact failures and rationalizations.

Only then alter the kernel. The first edit should target a demonstrated failure; if no scenario fails, do not add guidance merely to make the skill look more complete.

## Update Rule

After meaningful work, replace stale state here. Keep this file short. Preserve only current invariants, observed state, open debts, rejected paths that prevent repetition, and the next evidence-producing action.
