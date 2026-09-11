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
4. run `python verify.py`;
5. re-check every stored claim that could have gone stale;
6. continue from the next evidence-producing action, not from old prose momentum.

Past-self state is a recovery aid, never authority.

## Current Invariant

The repository exists to maximize **behavioral leverage per token** through one primitive:

> current truth → desired truth, preserving invariants, using the smallest sufficient verified delta.

`verified-delta/SKILL.md` must remain broadly applicable, model-agnostic, and small enough to load cheaply.

## Observed Repository State

- Runtime skill entrypoint is `verified-delta/SKILL.md`; its frontmatter `name` matches the parent directory.
- The Verified Delta kernel remains 446 words; the structural move did not alter its content.
- `EVALS.md` defines seven pressure scenarios and four explicit behavioral gates.
- `CONSTITUTION.md` defines sentence residency, compression, evidence, scope, and continuity laws.
- `verify.py` discovers a single skill entrypoint, validates nested name/directory agreement, frontmatter, the 500-word ceiling, state/count drift, and false behavioral-gate closure.
- `tests/test_verify.py` includes deterministic coverage for valid nested packaging and name/directory mismatch in addition to the prior static invariants.
- `.github/workflows/verify.yml` runs static checks on pushes and pull requests.
- GitHub Actions previously proved the static verifier on `main`; the current structural branch must obtain its own GREEN run before merge.
- No runtime dependency, model profile, prompt-template catalog, memory system, or multi-agent framework has been added.
- No fresh isolated-agent RED/GREEN behavioral run has been completed yet.

Static invariant verification is not behavioral verification.

## Source-Grounded Design Inputs

The kernel was distilled from the supplied Tề Hạ/QX research, not copied wholesale. Retained mechanisms are:

- semantic precision and exact-constraint preservation;
- objective/value invariance while policy may change;
- fact/inference/assumption/unknown separation;
- competing hypotheses only when uncertainty is material;
- cheap high-information probes over prolonged speculation;
- verification distinct from generation;
- externalized continuation state with stale-state checks;
- stopping and compute allocation based on decision value.

These mechanisms are research inputs, not proof that this implementation improves agents.

## Explicit Non-Goals

Do not expand this repository into:

- Prompt Master clone or tool-specific prompt router;
- QX-AI implementation;
- model/version catalog;
- multi-agent orchestration framework;
- memory platform;
- large template/rule collection.

## Open Debts

1. **RED behavioral baseline missing.** E1–E7 need fresh no-skill runs.
2. **GREEN behavioral comparison missing.** The same scenarios need runs with `verified-delta/SKILL.md`.
3. **Wording micro-tests missing.** Competing phrasings need repeated fresh contexts.
4. **Semantic ablation missing.** No core sentence has demonstrated behavioral necessity by removal.
5. **Cross-domain holdout missing.** Coding, research, writing, and simple-task cases need unseen tests.

These debts block claims of behavioral verification or convergence.

## Rejected Directions

- Bigger is stronger.
- More rules imply more intelligence.
- Literal “one million reviews” claims without recorded runs.
- Deep reasoning on every task.
- Multi-agent by default.
- Preserving old state without checking current reality.
- Adding prose for constraints a deterministic verifier can enforce.

## Next Best Action

After the packaged-structure branch is GREEN and merged, run the **RED behavioral baseline** from `EVALS.md` in isolated fresh contexts without loading `verified-delta/SKILL.md`, recording exact failures and rationalizations.

Only then alter the kernel. The first semantic edit must target a demonstrated failure; if no scenario fails, do not add guidance merely to make the skill look more complete.

## Update Rule

After meaningful work, replace stale state here. Keep only current invariants, observed state, open debts, rejected paths that prevent repetition, and the next evidence-producing action.
