# Target-Authority Selection Execution Design

## Purpose

Implement the execution boundary for the already frozen `evals/target-authority-selection-plan.json` without changing R1, R1A, the preregistered decision rule, or the evidence class. This milestone produces infrastructure only: deterministic hidden-at-execution instance generation, reference-path admission, isolated paired execution plumbing, immutable receipts, fail-closed comparability, and decision evaluation. It does not dispatch behavioral model trials.

## Frozen inputs

The execution layer must refuse to run unless the preregistration remains `target-authority-selection-validation-v1`, R1 remains git blob `ac48f09ab02eca63e014b4c25f86e492ae5559cb`, and R1A remains git blob `26d93ce346deedccd7186ad5856f849136825ec3`. The six semantic cells, two replicates per cell, fixed 24-trial budget, matched dimensions, contamination rule, and decision rule are read from the frozen plan rather than redefined by the runner.

## Generation boundary

Add `selection_validation.py` as a researcher-side stdlib-only harness. `generate` accepts an explicit execution seed and a new output directory. It deterministically creates exactly twelve instances: two for every frozen semantic cell, spanning at least four allowed task families and excluding username-normalization derivatives. The committed source contains generation methods and domain constraints, but no execution-time seed, final prompt instances, final fixture values, or final expected answers.

Each generated instance is split into an agent-visible surface and a hidden surface. The agent-visible surface contains only the fixture plus task prompt. The hidden surface contains grader/reference material and instance metadata. `prepare` copies only the fixture into a fresh destination and emits the prompt; it must never expose the hidden surface to the evaluated workspace.

All generated instances are used. Generation is immutable: an existing output directory is rejected rather than overwritten.

## Reference admission

Before any model trial, `admit` executes the generated reference path against a clean copy of every fixture and then runs the deterministic grader. All twelve cases must pass. Missing, malformed, or failing reference/grader material blocks admission. Admission is infrastructure evidence only.

## Receipts and provenance

`record` creates one immutable receipt per arm. It binds the preregistration digest, generator digest/version, execution seed, case/cell/family/replicate identity, prompt hash, fixture hash, grader hash, treatment-set identities, workspace hash, transcript hash, metrics, deterministic grade, runtime run-config, and contamination status.

Historical receipts are validated against their recorded immutable provenance, not current harness bytes. R1/R1A pair comparison additionally requires equal generated-case identity, seed, prompt/fixture/grader provenance, actual model, actual reasoning, harness version, actual tool set, tool policy, limits, clean-environment policy, and replicate identity. Any drift yields `not_comparable`.

## Decision evaluation

`summarize` requires exactly one R1 and one R1A receipt for every frozen pair. It preserves `same_fail`, `same_pass`, `candidate_gain`, `candidate_harm`, and `not_comparable` per pair. It evaluates the preregistered rule literally: twelve comparable pairs, zero candidate harm, eight R1A passes across act/probe/verify cells, at least three R1A passes across four preserve pairs, and at least two candidate gains on preserve pairs. No average can hide a minority harm.

A behavioral failure is a valid experiment result and must still produce a summary. Infrastructure/provenance incompleteness is fail-closed and prevents a valid decision.

## Workflow

Add `.github/workflows/target-authority-selection.yml` as `workflow_dispatch` only. One generation/admission job creates the frozen hidden bundle from the supplied seed, resolves a single Copilot CLI version, and emits a dynamic matrix. The matrix runs all twelve cases under both frozen arms in separate clean runner workspaces with separate `COPILOT_HOME`, restricted tools, no built-in MCPs, no custom instructions, no remote mode, and actual runtime attestation from `copilot_event_parser.py`.

A final job downloads all arm receipts, requires exactly twenty-four unique receipts, runs `selection_validation.py summarize`, uploads the full evidence bundle, and never performs outcome-dependent early stopping. The workflow must not run on push or pull request.

## Contamination boundary

A generated bundle is mechanically clean only when generation occurs after preregistration freeze, the frozen treatment identities match, no final instance path exists in the repository, and the same bundle is used unchanged for every arm. If the workflow is explicitly marked contaminated or any identity drifts, execution must fail before evidence can count.

## Verification and non-goals

Development is test-first. Focused tests must cover deterministic generation, hidden-surface isolation, reference admission, immutable receipt/provenance binding, comparability drift, exact decision-rule evaluation, and workflow isolation. Full unit discovery plus `python verify.py` must pass before PR review, and runtime/candidate blobs must remain unchanged.

This milestone does not dispatch the 24 model trials, modify runtime wording, retune R1A, compare R0/R2-R8, claim provider snapshot immutability, close the final hidden holdout, or grant runtime residency.
