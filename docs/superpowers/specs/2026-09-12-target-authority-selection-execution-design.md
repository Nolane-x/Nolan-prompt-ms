# Target-Authority Selection Execution Design

## Purpose

Implement the execution boundary for the already frozen `evals/target-authority-selection-plan.json` without changing R1, R1A, the preregistered decision rule, or the evidence class. This milestone produces infrastructure only: deterministic hidden-at-execution instance generation, reference-path admission, isolated paired execution plumbing, immutable receipts, fail-closed comparability, and decision evaluation. It does not itself count infrastructure runs as behavioral evidence.

## Frozen inputs

The execution layer must refuse to run unless the preregistration remains `target-authority-selection-validation-v1`, R1 remains git blob `ac48f09ab02eca63e014b4c25f86e492ae5559cb`, and R1A remains git blob `26d93ce346deedccd7186ad5856f849136825ec3`. The six semantic cells, two replicates per cell, fixed 24-trial budget, matched dimensions, contamination rule, and decision rule are read from the frozen plan rather than redefined by the runner.

## Generation boundary

`selection_validation.py` is the researcher-side stdlib-only harness. Its `generate` command accepts an explicit seed because deterministic regeneration and testability require a stable API. The production workflow, however, must not accept that seed from the dispatch surface or expose it to trial jobs. The workflow generates a cryptographically fresh execution seed internally only after model/runtime preflight succeeds, records it inside researcher-side generation/bundle evidence, and never places it in the evaluated agent environment.

From that seed `generate` deterministically creates exactly twelve instances: two for every frozen semantic cell, spanning at least four allowed task families and excluding username-normalization derivatives. The committed source contains generation methods and domain constraints, but no final execution seed, final prompt instances, final fixture values, or final expected answers.

Each generated instance is split into an agent-visible surface and a hidden surface. The agent-visible surface contains only the fixture plus task prompt. The hidden surface contains grader/reference material and instance metadata. `prepare` copies only the fixture into a fresh destination and emits the prompt; it must never expose the hidden surface to the evaluated workspace.

All generated instances are used. Generation is immutable: an existing output directory is rejected rather than overwritten.

## Model/runtime preflight

Model availability is an infrastructure property and must be established before hidden instances exist. The workflow first resolves one Copilot CLI version, installs that exact version in a preflight job, performs a minimal model call using the requested named model/reasoning configuration, and validates the resulting JSONL with `copilot_event_parser.py attest-runtime`.

For named models, actual model identity must equal the requested identifier. For explicit reasoning effort, actual reasoning must equal the requested effort. A CLI rejection, routing mismatch, missing attestation, or nonzero exit fails preflight and therefore prevents hidden seed generation. This avoids consuming a fresh selection bundle merely to discover that a provider-facing model identifier is unusable.

The invalid dispatch `34699852491` demonstrated why this is required: Copilot CLI `1.0.83` rejected explicit model `gpt-5.6-luna` before successful inference. That run is infrastructure evidence only and produces no valid behavioral sample.

## Reference admission

After preflight and generation, `admit` executes the generated reference path against a clean copy of every fixture and then runs the deterministic grader. All twelve cases must pass. Missing, malformed, or failing reference/grader material blocks admission. Admission is infrastructure evidence only.

## Trial filesystem boundary

A trial may briefly receive the hidden bundle only for researcher-side `prepare`. After the visible workspace and exact treatment prompt have been materialized, the hidden bundle is deleted. The repository checkout is then scrubbed from `$GITHUB_WORKSPACE` before the evaluated model starts, preventing the agent from reading the generator, the alternate treatment, repository state, or researcher documentation during inference.

The model runs only against the prepared task workspace and prompt. The workflow sets `PYTHONDONTWRITEBYTECODE=1` so Python probes do not create incidental `__pycache__` state that could contaminate final workspace hashes. After inference ends, a trusted checkout is restored and the exact admitted hidden bundle is re-downloaded for researcher-side attestation, process-evidence extraction, grading, and receipt creation.

## Receipts and provenance

`record` creates one immutable receipt per arm. It binds the preregistration digest, generator digest/version, execution seed, case/cell/family/replicate identity, prompt hash, fixture hash, grader hash, treatment-set identities, workspace hash, transcript hash, metrics, deterministic grade, runtime run-config, and contamination status.

Historical receipts are validated against their recorded immutable provenance, not current harness bytes. R1/R1A pair comparison additionally requires equal generated-case identity, seed, prompt/fixture/grader provenance, actual model, actual reasoning, harness version, actual tool set, tool policy, limits, clean-environment policy, and replicate identity. Any drift yields `not_comparable`.

## Decision evaluation

`summarize` requires exactly one R1 and one R1A receipt for every frozen pair. It preserves `same_fail`, `same_pass`, `candidate_gain`, `candidate_harm`, and `not_comparable` per pair. It evaluates the preregistered rule literally: twelve comparable pairs, zero candidate harm, eight R1A passes across act/probe/verify cells, at least three R1A passes across four preserve pairs, and at least two candidate gains on preserve pairs. No average can hide a minority harm.

A behavioral failure is a valid experiment result and must still produce a summary. Infrastructure/provenance incompleteness is fail-closed and prevents a valid decision.

## Workflow

`.github/workflows/target-authority-selection.yml` is `workflow_dispatch` only. Dispatch selects a model and reasoning configuration; it does not supply the hidden execution seed. Validation and one pinned Copilot CLI resolution occur first, followed by the model/runtime preflight. Only after that preflight passes does the generation/admission job create the hidden bundle and dynamic 24-arm matrix.

The matrix runs all twelve cases under both frozen arms in separate clean runner workspaces with separate `COPILOT_HOME`, restricted tools, no built-in MCPs, no custom instructions, no remote mode, and actual runtime attestation from `copilot_event_parser.py`. Each trial has neither hidden bundle nor repository checkout present during inference.

A final job downloads all arm receipts, requires exactly twenty-four unique receipts, runs `selection_validation.py summarize`, uploads the full evidence bundle, and never performs outcome-dependent early stopping. The workflow must not run on push or pull request.

## Contamination boundary

A generated bundle is mechanically clean only when generation occurs after preregistration freeze and successful runtime preflight, the frozen treatment identities match, no final instance path exists in the repository, the execution seed is not exposed to the evaluated agent, and the same bundle is used unchanged for every arm. If the workflow is explicitly marked contaminated or any identity drifts, execution must fail before evidence can count.

## Verification and non-goals

Development is test-first. Focused tests must cover deterministic generation, hidden-surface isolation, runtime preflight ordering, private workflow seed generation, repository scrubbing during inference, reference admission, immutable receipt/provenance binding, comparability drift, exact decision-rule evaluation, and workflow isolation. Full unit discovery plus `python verify.py` must pass before PR review, and runtime/candidate blobs must remain unchanged.

This milestone does not modify runtime wording, retune R1A, compare R0/R2-R8, claim provider snapshot immutability, close the final hidden holdout, or grant runtime residency. A successful 24-trial selection run can establish at most **selection-stable under the observed harness/model configuration; not runtime-resident**.
