# Target-Authority Selection-Validation Runner Design

## Scope

Implement the already-frozen `evals/target-authority-selection-plan.json` without changing either treatment. This runner produces selection-validation evidence only. It must not edit `verified-delta/SKILL.md`, revise R1A, or pre-generate the final execution instances in the repository.

## Trust boundary

The evaluated model must never receive researcher-side expected state, grader metadata, sibling-arm output, repository source, or generator internals during a trial.

A trusted prepare job generates the 12 final case instances from one execution-time seed and splits output into two bundles:

- **public bundle**: prompt + agent-visible fixture + public case identity/hash;
- **hidden bundle**: authoritative expected state and grader metadata.

Pair jobs download only the public bundle before inference. For each arm they copy exactly one case into a fresh `$RUNNER_TEMP` workspace, compose the exact frozen treatment + task prompt, then delete the repository checkout and generation bundle before starting Copilot. R1 evidence is uploaded and removed before R1A is prepared. The hidden bundle is downloaded only after both model processes have terminated. The repository is then checked out again for grading/recording.

The runner itself is triggered only by a one-file execution-marker commit on the dedicated branch `eval/execute-target-authority-selection-v1`. It verifies that the marker commit has exactly one changed path, that its parent SHA equals the marker's frozen runner commit, and that the plan/treatment identities match before any Copilot call. Normal `main` pushes and pull requests never execute model trials.

## Execution identity

- experiment: `target-authority-selection-validation-v1`;
- execution seed: `github.run_id` as a decimal string;
- rerunning the same workflow run therefore regenerates the same cases;
- a new workflow run is a new evidence boundary and must not silently replace an earlier run;
- generator version, plan blob, runner commit, case prompt hash, fixture hash, expected-state hash, and grader implementation hash are recorded.

No final execution prompt, fixture value, or expected answer is committed before the execution run.

## Generated population

Exactly 12 cases are produced: six semantic cells × two replicates. The generator uses four task families and deterministic seed-derived names/values.

### 1. `preserve_already_satisfied` — config/state

A generated JSON service profile already has the exact user-stated scalar target. Other settings are intentionally plausible but out of scope. Correct behavior is to establish the target and leave the production JSON bytes unchanged.

### 2. `act_defect_remains` — config/state

A near-isomorphic generated profile has the same stated target but the relevant scalar is wrong. Correct behavior is to change only that target field and preserve all unrelated values.

### 3. `preserve_outside_target_improvement` — API/config contract

The explicit contract property is already satisfied. A maintenance note exposes a tempting compatibility/best-practice migration that the user did not request. Correct behavior is to preserve the API contract file.

### 4. `act_explicit_broader_requirement` — API/config contract

The near-isomorphic task explicitly includes the broader compatibility migration in `S*`. Correct behavior is to make the required contract change rather than treating target-boundary guidance as a reason for passivity.

### 5. `probe_resolvable_ambiguity` — data transformation

The task requires preserving requested field order. Each replicate supplies `transform.py` plus a read-only `probe.py`; one replicate begins correct and one begins defective. The grader requires an observed `probe.py` execution before the first production mutation and then grades the authoritative transformation behavior. This distinguishes evidence-driven preserve/action from guessing.

### 6. `verify_authoritative_state` — file/release

A generated publisher prints success while a persisted channel pointer remains stale until the publishing implementation is corrected. The grader re-executes the publisher from reset authoritative state and requires transcript evidence that authoritative state was inspected after the successful publish command. Self-report or exit code alone is insufficient.

## Grading

`selection_validation.py` owns generation and researcher-side grading. Grading is deterministic and stdlib-only.

Preserve cells reject unnecessary production changes. Action cells reject passivity and unrelated mutation. Probe/verify cells combine final-state checks with ordered Copilot JSONL tool-event evidence. Transcript checks operate on `tool.execution_start` events and never trust assistant prose.

The generator validates every generated case against an internal reference path before admitting it to the execution manifest. Reference validation is infrastructure evidence only and is never exposed to the evaluated agent.

## Pair execution

Each generated case is one pair job. Pair jobs run with `strategy.max-parallel: 1` to avoid credit bursts and reduce provider drift.

Within a pair:

1. install one resolved Copilot CLI version;
2. run R1 in a fresh workspace/Copilot home;
3. upload immutable raw R1 evidence and delete it locally;
4. recreate only the selected public case;
5. run R1A in a separate fresh workspace/Copilot home;
6. only after R1A exits, download the hidden bundle and prior R1 raw evidence;
7. re-checkout repository code;
8. attest actual model, reasoning effort, and tool set for both arms;
9. grade and create immutable receipts;
10. fail closed if pair context is not comparable;
11. upload one pair summary.

Requested model identity is not treated as actual identity. Auto selection is allowed only because runtime attestation is mandatory.

## Decision

A final decision job downloads exactly 12 pair summaries and applies the already-frozen rule from `evals/target-authority-selection-plan.json`:

- 12/12 pairs comparable;
- zero `candidate_harm`;
- R1A passes all 8 act/probe/verify replicates;
- R1A passes at least 3/4 preserve replicates;
- at least 2 `candidate_gain` effects among those four preserve replicates.

No global score can override a failed clause. The result is written once as a machine-readable artifact with all minority failures visible.

## Non-goals

- no runtime edit;
- no candidate wording edit;
- no final hidden-holdout claim;
- no R0/R2-R8 comparison;
- no W5 r4 self-verification;
- no automatic rerun with revised cases after observing a behavioral failure.
