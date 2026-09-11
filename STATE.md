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

The primitive is the target. **A skill is only one possible delivery mechanism.** `verified-delta/SKILL.md` must not be protected as a form factor if evidence shows that no guidance, a smaller always-on instruction, or another delivery mechanism produces a better cost/behavior tradeoff.

## Observed Repository State

- Runtime skill entrypoint is `verified-delta/SKILL.md`; its frontmatter `name` matches the parent directory.
- The runtime package contains only `SKILL.md`; `verify.py` rejects additional support files until evaluation justifies relaxing that invariant.
- The Verified Delta kernel remains 446 words and has not been behaviorally edited during structural/evaluation hardening.
- `EVALS.md` defines five gates: Activation, RED baseline, GREEN comparison, Ablation, and Cross-domain holdout.
- Activation decomposes **Utility**, **Trigger**, **Compliance/Boundary**, and **Form-factor fit** instead of treating “skill present” as one intervention.
- The diagnostic ladder is `no guidance → forced-load current skill → discoverable current skill`; a preregistered compact always-on candidate is compared only after RED/utility evidence identifies behavior worth preserving.
- Activation uses two populations: a balanced diagnostic set for under/over-trigger analysis and a representative workload sample for natural prevalence, total cost, and form-factor choice.
- Cross-lingual evaluation now treats prompt language, metadata language, and body language as separate intervention variables. `L0–L3` isolates deployed cross-lingual behavior, metadata localization, and full localization instead of changing them together.
- Cross-lingual Trigger, post-trigger Compliance/Boundary, and execution-token correctness are scored separately; a failed end task cannot by itself diagnose a discovery failure.
- Per-language reporting is mandatory for multilingual claims. Untested languages remain unknown rather than inheriting a global “multilingual” label.
- Metadata or wording selected on development cases must be frozen and checked on fresh selection-validation cases before a final holdout claim.
- Repeated trials estimate stochastic reliability within a task; they do not count as additional independent tasks. Candidate/control analysis must preserve task pairing and uncertainty rather than inflating sample size with repeated runs.
- Activation results are harness-scoped. The experimental manifest records delivery form, available-skill-set hash, prompt language, metadata language, and body language.
- Public development coverage is E1–E13 with a semantic coverage map. E12 pressures irreversible/high-impact actions; E13 pressures the first-invalid-transition-boundary rule.
- Semantic coverage remains a test-planning hypothesis, not sentence-residency evidence.
- `EVALS.md` requires clean trials, outcome-first grading, component scores, repeated trials, transcript inspection, paired controls, contamination handling, selection-validation, and interaction-aware ablation.
- `CONSTITUTION.md` defines sentence residency, compression, evidence, scope, and continuity laws.
- `verify.py` requires exactly one nested skill package, validates package purity/frontmatter/size/state consistency, and refuses overall behavioral closure while Activation remains OPEN.
- `.github/workflows/verify.yml` runs deterministic checks on pushes and pull requests.
- No runtime dependency, model profile, prompt-template catalog, memory system, or multi-agent framework has been added.
- No fresh isolated-agent RED/GREEN behavioral run has been completed yet.

Static invariant verification, semantic coverage planning, and external benchmark results are not behavioral verification of Verified Delta.

## Source-Grounded Research Findings

External research currently supports the **questions and eval design**, not the runtime wording itself:

- *Skill-Use* (2026) separates Trigger, Compliance, and Boundary and reports strong harness dependence; skill use is not a model-only capability.
- *SWE-Skills-Bench* (2026) finds that most evaluated public SWE skills deliver no pass-rate improvement, some add large token overhead without gain, and some degrade performance. “Having a skill” therefore has no prior entitlement to be useful.
- GitHub's current Copilot guidance recommends custom instructions for simple guidance relevant to almost every task and skills for detailed guidance that should load only when relevant. This makes delivery form an empirical question for a broad primitive like Verified Delta.
- Natural-language tool/skill descriptions are behaviorally active selection inputs; description edits can strongly change selection frequency, so activation metadata needs behavioral A/B tests rather than semantic review alone.
- Agent Skills recommends that `description` express both what a skill does and when to use it; the current Verified Delta description is primarily trigger-oriented. Whether adding “what” improves discovery without over-triggering is unmeasured.
- Agent Skills currently permits descriptions up to 1024 characters; the repository's ≤500 and `Use when...` constraints are project policies, not universal spec requirements.
- GitHub Copilot project skill discovery uses `.github/skills`, `.claude/skills`, or `.agents/skills`; a generic distributable skill directory and a product auto-discovery installation path are not the same thing.
- MASSIVE-Agents (2025) finds large multilingual variance in function-calling accuracy across 52 languages, so English success cannot be promoted to language-independent agent behavior.
- *Lost in Execution* (ACL 2026) finds multilingual tool failures can occur after intent understanding and tool selection are already correct; therefore Trigger and execution/compliance failures must be diagnosed separately.
- balanced capability tests are useful for exposing both directions of behavior, but deployment prevalence must be estimated from a representative workload rather than inferred from an artificially balanced set;
- repeated adaptive selection on the same eval can produce winner's-curse optimism, so wording/metadata selection needs fresh validation before final holdout reporting;
- repeated stochastic trials on one task estimate reliability but remain correlated by task, so task-level pairing and uncertainty must be retained;
- agent evals need isolated trials, explicit graders, outcome checks, transcript review, and matched harness configuration;
- infrastructure and resource configuration can move agentic benchmark scores enough to confound small deltas;
- public benchmarks can be contaminated or recognized by capable tool-using agents, so final holdouts must stay unseen;
- semantic prompt units can have joint/combinatorial effects, so leave-one-out removal alone is insufficient when units substitute or interact;
- coding agents show strong action bias on tasks where the correct delta is no code change;
- scope evaluations can become artificially easy when authorization boundaries are explicitly declared instead of inferred;
- clarification quality includes deciding when a question is decision-relevant, not merely generating more questions;
- overthinking research supports scaling deliberation to task difficulty rather than maximizing reasoning by default;
- instruction-hierarchy research motivates testing retrieved/tool content as evidence with a trust level rather than assuming all text has equal authority.

These findings do not prove Verified Delta works; they define failures, delivery risks, and attribution traps it must survive.

## W5 Research Frame

A fresh Nolane World 0.12.0 W5 world has been opened for the research question: whether Verified Delta is the highest-leverage compact behavioral primitive, whether it should remain an on-demand Agent Skill, and what smallest evidence-backed runtime form should survive.

The W5 program keeps rival abstractions, no-guidance, and alternative delivery forms live; requires falsification, decisive experiments, source independence, adversarial review, and independent verification; and does **not** grant closure merely because the current primitive is elegant or externally supported.

The W5 world is not closed. Runtime-required active residency, independent verification, critical-unknown resolution, and convergence gates remain unsatisfied. This state records obligations, not a claim of W5 completion.

## Form-Factor Hypotheses

Keep all four live until data eliminates them:

1. **On-demand skill is correct.** The behavior is valuable on a selective subset of tasks and progressive disclosure beats always-on context cost.
2. **Compact always-on core + optional skill is correct.** A few invariants are broadly useful, while detailed procedure remains selective.
3. **Always-on instruction is correct.** Intended activation prevalence is so high that retrieval complexity is wasted and the compact always-on candidate dominates.
4. **No added guidance is correct.** Modern models/harnesses already exhibit the target behavior often enough that Verified Delta adds negligible marginal utility or causes regressions.

Do not rank these by preference. The experiment decides.

## Explicit Non-Goals

Do not expand this repository into:

- Prompt Master clone or tool-specific prompt router;
- model/version catalog;
- multi-agent orchestration framework;
- memory platform;
- large template/rule collection;
- public benchmark-answer repository;
- vendor-specific directory duplication without a concrete deployment target.

## Open Debts

1. **Utility upper bound unmeasured.** Compare no guidance with force-loaded current skill before spending effort on metadata optimization.
2. **Activation behavior unmeasured.** Progressive-disclosure Trigger, Compliance, and Boundary need balanced positives/negatives plus realistic distractor-skill conditions.
3. **Natural activation prevalence unmeasured.** Form-factor decisions require a representative workload sample; a balanced trigger benchmark is not a prevalence estimate.
4. **Cross-lingual activation unmeasured.** Run semantically matched `L0–L3` comparisons on intended deployment languages; isolate Trigger from post-trigger Compliance/Boundary and execution-token correctness.
5. **Form-factor fit unmeasured.** Compare discoverable skill against no guidance and a preregistered compact always-on candidate on a representative workload. Do not write the compact candidate from holdout failures.
6. **Selection optimism unmeasured.** Wording/metadata chosen on development cases needs fresh selection-validation before final holdout use.
7. **RED behavioral baseline missing.** E1–E13 need fresh no-guidance trials; public probes are development tasks, not final holdouts.
8. **GREEN behavioral comparison missing.** Matched runs with the unchanged 446-word kernel are required.
9. **Wording micro-tests missing.** Competing phrasings need no-guidance controls, repeated fresh contexts, and manual transcript review.
10. **Semantic ablation unexecuted.** Use single-unit ablation first, then suspected overlapping pairs/groups before declaring silent units redundant.
11. **Hidden cross-domain/language holdout missing.** Final holdout prompts must remain outside the public repository until evaluation is complete.
12. **Compression hypothesis unresolved.** Test materially shorter kernels; do not assume 446 words are necessary or that an arbitrary smaller target is better.
13. **Frontmatter policy is partly project-specific.** Resolve `Use when...` and ≤500 policy by activation evidence rather than calling either a universal requirement.
14. **Runtime portability unmeasured.** Any skill-use claim is harness-scoped until replicated. Distribution/install paths must be treated separately from the canonical source package.
15. **Coverage adequacy is unvalidated.** A public probe that cannot discriminate the semantic unit mapped to it must be split, replaced, or removed.
16. **W5 closure is unavailable.** The current W5 research world has not satisfied active-residency, independent-verification, critical-unknown, or convergence requirements.

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
- Optimizing the skill description before proving force-loaded content has marginal utility.
- Treating a balanced activation benchmark as evidence of real-world activation prevalence.
- Reporting the best score on the same benchmark repeatedly used to choose wording as fresh evidence.
- Counting repeated stochastic trials on one task as independent task diversity.
- Assuming “skill” is the correct abstraction because the project began as a skill.
- Assuming English skill discovery/compliance transfers to other languages without measurement.
- Localizing metadata and body simultaneously before isolating where a multilingual failure occurs.
- Copying the same skill into every vendor-specific auto-discovery directory before choosing a deployment target.
- Changing runtime wording because external research merely sounds compatible with it.

## Next Best Action

Obtain a **fresh isolated-agent harness** and execute the diagnostic ladder in this order:

`U0 no guidance → U1 forced-load current skill → A2 progressive disclosure on balanced diagnostics → A6 L0–L3 on target languages → validate selected metadata on fresh cases → F0/F1/F2/F3 on a representative workload only if U1 demonstrates useful behavior`

Run RED with paired cases that falsify both directions of each rule: act/no-op, narrow/wider scope, infer/clarify, low/high effort, continue/restart. Record Trigger, Compliance, Boundary, outcome, cost, language, per-task reliability, and uncertainty separately.

If an isolated harness is unavailable, stop at the evidence boundary. Do not substitute this already-exposed session for a clean control, because it has read the skill, its evals, and the research hypotheses.

## Update Rule

After meaningful work, replace stale state here. Keep only current invariants, observed state, open debts, rejected paths that prevent repetition, and the next evidence-producing action.
