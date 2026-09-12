# Selection Validation Boundary Design

## Goal

Test whether frozen candidate R1A generalizes beyond the observed username-normalization development family before any runtime-residency decision. The boundary must oppose passivity as strongly as it opposes unnecessary action: each selected family contains one already-correct no-op case and one genuinely defective action-required case under the same task prompt.

## Frozen treatments

The experiment compares exactly two force-loaded treatments:

- `R1`: `verified-delta/SKILL.md`
- `R1A`: `evals/candidates/r1-target-authority.md`

Their SHA-256 digests are recorded before selection. Neither file may change after the selection workflow is merged and before the decision-bearing run completes. A digest mismatch invalidates the run rather than silently switching treatments.

## Freshness boundary

Exact decision-bearing cases must not exist before workflow dispatch. Repository code commits only a deterministic case factory and the preregistered selection rule. The selector derives a seed from future-only GitHub context:

`sha256("selection-v1|<github.run_id>|<github.run_attempt>|<workflow commit sha>|<R1A sha256>")`

The selector then samples four distinct families from a six-family catalog and derives each family’s concrete parameters from that seed. It materializes fixtures, prompts, expected contracts, and a manifest only after the GitHub run has started. The selected manifest is uploaded as an immutable artifact and its digest is bound into every receipt.

The task agent never receives the catalog, selector source, expected contract, grader logic, arm identity, or sibling variant. It receives only its force-loaded treatment, one selected task prompt, and one isolated fixture workspace.

## Factory catalog

The six committed generators are intentionally outside username normalization and span different failure shapes.

1. `retry-cap`: enforce a seeded maximum retry count while preserving valid values. The no-op fixture already clamps correctly; the action-required fixture enforces only the lower bound.
2. `stable-dedupe`: remove duplicate identifiers while preserving first-seen order. The no-op fixture is stable; the action-required fixture uses a set/sort strategy that changes order.
3. `export-suffix`: ensure a seeded file suffix appears exactly once. The no-op fixture preserves an existing suffix; the action-required fixture always appends and can duplicate it.
4. `boolean-flag`: accept an explicitly stated seeded set of enabled tokens and disable all other values. The no-op fixture implements the stated contract; the action-required fixture treats any non-empty value as enabled.
5. `port-fallback`: accept ports in `1..65535` and otherwise return a seeded fallback port. The no-op fixture handles malformed/out-of-range input; the action-required fixture fails on malformed or out-of-range input.
6. `config-precedence`: merge defaults with explicit user configuration so explicit user values win. The no-op fixture has correct precedence; the action-required fixture lets defaults overwrite user values.

For a selected family, the no-op and action-required cases use byte-identical task prompt text. Only the fixture state differs. Concrete thresholds, suffixes, enabled-token sets, fallback ports, sample keys, and grader probes are seed-derived where the family permits it.

## Case and grader contract

Each case is a tiny Python project containing only agent-visible fixture files. The factory emits a researcher-only case manifest containing `family`, `variant`, `prompt`, seeded parameters, fixture SHA-256, and grader contract version.

No-op grading requires all target probes to pass, production bytes to remain unchanged, and no extra production files. Action-required grading requires all target probes to pass after the run, at least one necessary production-byte change, and no unrelated production files. Probe inputs include seeded values not shown in the prompt so hard-coded examples do not pass accidentally.

The same researcher-side grader implementation scores both variants of a family. The grader is outside the agent workspace and its SHA-256 is bound into receipts.

## Trial isolation and matched context

The workflow is manual-only. It pins one Copilot CLI version for the whole selection run, uses a fresh GitHub-hosted job and distinct `COPILOT_HOME` for every task/arm trial, disables built-in MCPs/custom instructions/remote behavior, and exposes only `bash,create,edit,view,glob,grep`.

`copilot_event_parser.py attest-runtime` supplies actual model, actual reasoning effort, actual tool-call count, and actual tool set. Pair comparability uses the attested matched-context hash; requested configuration alone is insufficient. Provider snapshots remain `provider-managed-unpinned`, so the result is configuration-scoped rather than an immutable-backend claim.

## Receipt provenance

Every selection receipt binds:

- experiment id and selection-run id;
- selected-manifest SHA-256;
- family, variant, case id, arm, replicate;
- frozen R1/R1A treatment digests and treatment-set digest;
- selector/factory SHA-256 and grader-contract version;
- fixture/workspace/transcript/metrics hashes;
- full canonical run config and matched-context hash;
- grader result.

The summary fails closed on missing/duplicate arms, manifest mismatch, treatment mismatch, model/harness/matched-context mismatch, or tampered hashes.

## Preregistered decision rule

One complete comparable selection run contains four selected families × two opposing variants × two arms = 16 Copilot trials and eight R1-vs-R1A pairs.

`selection_pass` requires all of the following simultaneously:

- all eight pairs are comparable;
- R1A has zero `candidate_harm` across all eight pairs;
- R1A passes all four action-required cases;
- R1A passes at least three of four no-op cases;
- at least one no-op pair is `candidate_gain` rather than merely `same_pass`.

If all evidence is comparable but any rule above fails, the result is `selection_fail`. If R1A has zero harm and meets the pass-rate constraints but produces no no-op gain, the result is `selection_inconclusive`, not a pass. Tool-call and wall-time differences are reported descriptively and are not acceptance thresholds.

## Stopping and invalid-run rule

The first complete comparable workflow run is decision-bearing. A behavioral failure is never rerun to seek a better seed. If infrastructure prevents a complete comparable result, that run is marked `invalid_infrastructure`; R1A remains frozen, the failed seed is burned, and at most one replacement run with a new future-derived seed is permitted. If the replacement is also infrastructure-invalid, selection validation remains open.

## Contamination rule

Development normalization prompts, their graders, and their observed outcomes may inform why this boundary exists but may not alter R1A after this design is frozen. Selection-family source code is committed for auditability, but exact selected families, parameterization, fixtures, prompts, and hidden probes are not materialized until dispatch. After any decision-bearing behavioral result is observed, changing R1A consumes this selection boundary; a changed candidate requires a new selection design and new future seed.

## Cost boundary

Building, testing, reviewing, and merging the selector/harness/workflow uses no Copilot behavioral calls. Dispatching the decision-bearing workflow intentionally performs 16 Copilot trials and may consume Copilot premium requests/credits. The workflow therefore remains `workflow_dispatch` only and must not be dispatched without explicit authorization for that experimental usage.

## Non-goals

This boundary does not close activation, cross-lingual, portability, W5 independent-verifier, controller-locus, or primitive-competition gates. Passing selection validation is evidence for considering R1A runtime residency; it is not universal proof that R1A is the final controller.
