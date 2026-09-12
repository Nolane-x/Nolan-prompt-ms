# Selection-Validation Design — Frozen Target-Authority Candidate

Date: 2026-09-12

## Purpose

Test whether the frozen R1A target-authority semantic generalizes beyond the public username-normalization development family before any final hidden-holdout or runtime-residency decision.

This stage is **selection-validation**, not the final hidden holdout. It exists to detect adaptive overfitting after semantic wording selection while preserving one later, stricter hidden boundary.

The runtime skill remains unchanged. R1A remains `evals/candidates/r1-target-authority.md`, blob `26d93ce346deedccd7186ad5856f849136825ec3`.

## Non-negotiable contamination boundary

Exact selection instances must not be committed before execution.

The repository may contain:

- generation procedure;
- task-family definitions;
- deterministic grading logic;
- acceptance/stopping rule;
- treatment digests and harness code.

It must not contain the exact runtime-generated prompts, parameter values, case IDs, initial workspaces, or expected outputs before the selection run.

A GitHub Actions `generate` job creates a fresh pack using runtime entropy only after the candidate is frozen. The pack is split into two artifacts:

1. **agent bundle** — opaque case IDs, prompts, initial workspaces, exact R1/R1A treatment files, and non-sensitive runtime attestation tooling;
2. **grader bundle** — hidden case semantics, expected states, generation seed/provenance, and deterministic grading data.

Trial jobs receive only the agent bundle. They do not checkout the repository and therefore cannot inspect generator source, graders, development fixtures, prior receipts, or expected answers. Grading occurs in a separate job after trials finish.

## Selection population

One fresh pack contains six independent paired tasks: three task families, each with an already-satisfied case and an action-required opposing control.

### Family A — coding state transition

A tiny Python module implements a bounded numeric normalization rule with runtime-randomized identifiers and limits.

- already-satisfied: current implementation satisfies the exact reported lower/upper-bound target; byte-changing production edits fail;
- action-required: one material bound is missing; leaving production unchanged fails.

The prompt states only the user-observable defect and asks for a focused fix. The grader uses randomized probes, including values outside the public prompt examples, and checks no-op byte identity where applicable.

### Family B — evidence/research correction

A small source file provides a randomized evidence table and a short conclusion artifact summarizes one requested fact.

- already-satisfied: conclusion already matches the supplied evidence; rewriting it fails the no-op identity requirement;
- action-required: conclusion names the wrong winning item; the artifact must be corrected from the supplied evidence.

No web access or remote tools are available. The target can be solved solely from the visible evidence file. Grading checks the requested conclusion and protects unrelated content.

### Family C — writing/editing target

A short customer-facing notice contains a runtime-randomized policy value and unrelated text.

- already-satisfied: the notice already states the exact requested policy; unnecessary rewriting fails;
- action-required: one policy value is wrong and must be corrected while unrelated wording remains unchanged.

The grader checks the requested fact plus minimal preservation of unrelated bytes/lines, rather than rewarding generic prose quality.

## Why these families

They test the same target-authority semantic without reusing the development surface:

- coding probes whether the candidate prevents semantic upgrades around already-correct code while still repairing a real implementation defect;
- evidence/research probes whether “hold the target boundary” transfers to evidence-backed conclusions rather than code;
- writing/editing probes whether it prevents gratuitous rewriting while still making a necessary factual edit.

The families are deliberately deterministic enough for outcome grading. Open-ended style quality is deferred because a subjective judge would introduce a second uncontrolled model at this stage.

## Runtime generation and commitments

`selection_validation.py generate` receives an output directory and an optional explicit seed for unit tests. Production workflow generation omits the seed, causing the script to create cryptographically strong runtime entropy.

Generation must produce:

- six opaque case IDs that do not encode family or condition;
- `agent/manifest.json` containing only case IDs and agent-visible paths/hashes;
- `agent/cases/<id>/prompt.txt` and `workspace/`;
- `agent/treatments/R1.md` and `R1A.md` copied exactly from the frozen repository files;
- `agent/tools/copilot_event_parser.py`;
- `grader/manifest.json` with family, condition, expected state, initial hashes, seed, generator/treatment provenance, and agent-pack commitment;
- `commitment.json` with SHA-256 commitments, family counts, candidate/runtime digests, generator digest, and a hash of the secret generation seed, but not the seed or exact prompts.

The pack commitment uses canonical JSON and deterministic tree hashing so the grader can verify that all raw trials derive from the same generated selection pack.

## Trial isolation

The workflow is manual-only `workflow_dispatch`.

Jobs:

1. `generate`
   - checkout exact main;
   - validate frozen candidate/runtime digests;
   - generate one six-case pack;
   - expose only the opaque case-ID matrix and public commitment as job outputs/artifacts;
   - upload agent and grader artifacts separately.

2. `resolve`
   - resolve one Copilot CLI version for the full selection run.

3. `trial`
   - matrix: six opaque cases × `R1/R1A`;
   - no repository checkout;
   - download only agent bundle;
   - create a clean `$RUNNER_TEMP` workspace per job;
   - install the single resolved CLI version;
   - force-load exact treatment text followed by identical task prompt;
   - use `model=auto`, omitted/default reasoning selector, restricted local tools, no MCPs, no remote behavior, no interactive questioning;
   - preserve JSONL, stderr, transcript, final workspace, runtime attestation, metrics, and trial metadata;
   - fail closed on model/CLI/runtime-attestation failure.

4. `grade`
   - waits for every trial;
   - checkout repository only after agent trials are complete;
   - download raw trial artifacts plus grader bundle;
   - verify pack/treatment/generator commitments;
   - deterministically grade each workspace;
   - compare only matched R1/R1A pairs (actual model, actual reasoning, CLI, tools, limits, pack commitment);
   - preserve per-case receipts and one aggregate summary.

The agent never receives the grader bundle.

## Causal comparison

Every case is a paired unit: R1 versus R1A on the same generated task instance.

Within a pair, any mismatch in actual model, actual reasoning effort, harness version, tool policy, limits, or pack commitment makes that case `not_comparable`.

Do not pool a non-comparable pair into candidate gain/harm counts.

One selection pack is one experiment. No wording changes, candidate changes, grader changes, or generation changes are permitted after generation begins.

## Preregistered acceptance rule

Selection validation passes only if all of the following are true:

1. all six R1/R1A pairs are comparable;
2. R1A passes all six independent tasks (`6/6`);
3. `candidate_harm == 0` across the six pairs;
4. each of the three action-required opposing controls passes under R1A;
5. each of the three already-satisfied cases passes under R1A (no unnecessary mutation);
6. there is no infrastructure failure or grader inconsistency that would make the run incomplete.

`candidate_gain` count is reported but is not a mandatory threshold at this stage. Development ablation has already established a causal gain; selection-validation is primarily a fresh generalization/regression gate. Requiring the fresh control to fail would incorrectly condition acceptance on stochastic incumbent failure.

There is no retry-on-behavior rule. A behavioral R1A failure fails selection validation.

Infrastructure failure before a valid receipt does not count as behavior; rerunning an infrastructure-failed job/run is allowed only if the exact generated pack can be reused and its commitment remains unchanged. If the pack cannot be reused exactly, the run is abandoned and a new experiment receives a new pack identity.

## Cost reporting

Report per-arm tool calls and wall time for every comparable pair, plus descriptive totals. Cost is not collapsed into the pass/fail gate unless it reveals pathological behavior, but a later residency decision must consider behavioral benefit per token/tool/time cost.

Input/output token counts remain null unless Copilot exposes stable cumulative semantics that the parser can attest without inference.

## Result interpretation

If the selection rule passes, R1A becomes **selection-validated under this GitHub Copilot configuration**. That still does not make it universally verified or automatically runtime-resident.

A separate final hidden holdout remains required before a strong runtime-residency claim. That final holdout should expand domain coverage further (for example artifact work and simple direct tasks), remain unseen until the procedure is frozen, and must not be authored from selection-validation failures.

If selection validation fails, do not tune R1A on the selection cases and then reuse them as unbiased evidence. Preserve the failure, classify it, and return to development with a new candidate/version; future validation must use fresh cases.

## Files expected during implementation

- `selection_validation.py` — generation, deterministic grading, pack verification, receipt/summarize logic;
- `.github/workflows/selection-validation.yml` — manual isolated runner;
- `evals/selection-validation-plan.json` — machine-readable frozen acceptance/generation contract, containing no final instance content;
- `tests/test_selection_validation.py` — deterministic generator/grader/commitment tests;
- `tests/test_selection_validation_workflow.py` — workflow isolation and fail-closed contract tests.

Runtime files are not part of this implementation.
