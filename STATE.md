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
- The runtime package contains only `SKILL.md`; `verify.py` rejects additional support files until evaluation justifies relaxing that invariant.
- The Verified Delta kernel remains 446 words and has not been behaviorally edited during structural/evaluation hardening.
- `EVALS.md` separates public development probes from hidden holdouts and defines five gates: Activation, RED baseline, GREEN comparison, Ablation, and Cross-domain holdout.
- Public development coverage is now E1–E13. E12 directly pressures the high-impact/irreversible branch of the Effort Gate; E13 directly pressures the final “return to the first invalid transition boundary” rule.
- `EVALS.md` contains a semantic coverage map linking each independently meaningful runtime unit to pressure cases. This map is a coverage hypothesis only; it is not evidence that the unit changes behavior or deserves residency.
- E3 now contains an explicit-vs-inferable authorization-boundary validity pair so the eval can detect declaration matching instead of genuine scope inference.
- E4 now tests whether internal tuple notation stays internal when exposing it adds no value.
- E10 now grades both final correctness and clarification efficiency rather than rewarding questions unconditionally.
- `EVALS.md` requires matched experimental manifests, clean trials, outcome-first grading, component scores, repeated trials, transcript inspection, paired controls, and contamination handling.
- `CONSTITUTION.md` defines sentence residency, compression, evidence, scope, and continuity laws.
- `verify.py` requires exactly one nested skill package, validates package purity/frontmatter/size/state consistency, and refuses overall behavioral closure while Activation remains OPEN.
- Remote TDD evidence exists for the Activation-gate verifier change: the test-only commit failed before the verifier knew about Activation, then the minimal verifier change passed.
- `.github/workflows/verify.yml` runs deterministic checks on pushes and pull requests.
- No runtime dependency, model profile, prompt-template catalog, memory system, or multi-agent framework has been added.
- No fresh isolated-agent RED/GREEN behavioral run has been completed yet.

Static invariant verification and semantic coverage planning are not behavioral verification.

## Source-Grounded Research Findings

External research currently supports the **questions and eval design**, not the runtime wording itself:

- agent evals need isolated trials, multiple attempts, explicit graders, outcome checks, transcript review, and matched harness configuration;
- infrastructure and resource configuration can move agentic benchmark scores enough to confound small deltas;
- public benchmarks can be contaminated or recognized by capable tool-using agents, so final holdouts must stay unseen;
- line-level prompt ablation can expose regressions that static review misses;
- prompt-attribution research shows that semantic prompt units can have joint/combinatorial effects, so leave-one-out removal alone is insufficient when two units may substitute for or interact with one another;
- prompt formulation can materially change performance even when semantic intent appears similar;
- coding agents show strong action bias on tasks where the correct delta is no code change;
- scope evaluations can become artificially easy when authorization boundaries are explicitly declared instead of inferred;
- clarification quality includes deciding when a question is decision-relevant, not merely generating more questions;
- complex-instruction benchmarks support grading individual constraints instead of hiding tradeoffs in one scalar;
- overthinking research supports scaling deliberation to task difficulty rather than maximizing reasoning by default;
- instruction-hierarchy research motivates testing retrieved/tool content as evidence with a trust level rather than assuming all text has equal authority.

These findings do not prove Verified Delta works; they define failures and attribution traps it must survive.

## Explicit Non-Goals

Do not expand this repository into:

- Prompt Master clone or tool-specific prompt router;
- model/version catalog;
- multi-agent orchestration framework;
- memory platform;
- large template/rule collection;
- public benchmark-answer repository.

## Open Debts

1. **Activation behavior unmeasured.** The current trigger-only description needs balanced should-load/should-not-load tests and comparison against genuinely different metadata forms.
2. **RED behavioral baseline missing.** E1–E13 need fresh no-skill trials; public probes are development tasks, not final holdouts.
3. **GREEN behavioral comparison missing.** Matched runs with the unchanged 446-word kernel are required.
4. **Wording micro-tests missing.** Competing phrasings need no-guidance controls, repeated fresh contexts, and manual transcript review.
5. **Semantic ablation unexecuted.** Runtime units now have planned pressure coverage, but no unit has proved residency by removal/compression. Use single-unit ablation first, then test suspected overlapping pairs/groups before declaring independently silent units redundant; two units can each look unnecessary when the other substitutes for it. If a mapped probe does not discriminate the unit during RED/ablation, revise the coverage claim rather than counting success.
6. **Hidden cross-domain holdout missing.** Final holdout prompts must remain outside the public repository until evaluation is complete.
7. **Compression hypothesis unresolved.** Because activation may be broad, test whether materially shorter kernels preserve behavior; do not assume 446 words are necessary or that an arbitrary smaller target is better.
8. **Frontmatter policy is partly project-specific.** Agent Skills permits descriptions up to 1024 characters and recommends describing what+when; this repo currently enforces ≤500 and `Use when...`. Resolve by activation evidence before changing either policy.
9. **Runtime distribution behavior is unmeasured.** Generic Agent Skills packaging and product-specific auto-discovery layouts are distinct; do not duplicate vendor directories until an intended deployment path requires it.
10. **Coverage adequacy is unvalidated.** E1–E13 are hypotheses about causal failure families. A scenario that cannot distinguish the semantic unit it is mapped to must be split, replaced, or removed.

These debts block claims of behavioral verification or convergence.

## Rejected Directions

- Bigger is stronger.
- More rules imply more intelligence.
- Literal “one million reviews” claims without recorded runs.
- Deep reasoning on every task.
- Multi-agent by default.
- Preserving old state without checking current reality.
- Adding prose for constraints a deterministic verifier can enforce.
- Adding runtime support files before evaluation proves progressive disclosure is needed.
- Treating public E1–E13 as an unseen holdout.
- Treating a semantic coverage table as proof that a sentence works.
- Treating two individually silent ablations as proof both units are useless without checking interaction/redundancy.
- Changing the runtime because external research merely sounds compatible with it.

## Next Best Action

Obtain a **fresh isolated-agent harness** and run the Activation study plus RED baselines before changing `verified-delta/SKILL.md`.

Start RED with paired cases that can falsify both directions of each rule: act/no-op, narrow/wider scope, infer/clarify, low/high effort, continue/restart. Then use those failures to decide which semantic units actually deserve ablation priority.

If an isolated harness is unavailable, stop at the evidence boundary. Do not substitute this already-exposed session for a clean control, because it has read the skill, its evals, and the research hypotheses.

## Update Rule

After meaningful work, replace stale state here. Keep only current invariants, observed state, open debts, rejected paths that prevent repetition, and the next evidence-producing action.
