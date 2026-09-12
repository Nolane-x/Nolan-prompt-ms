# Target-Authority Selection-Validation Runner Implementation Plan

> Execute test-first. Do not generate final execution instances or invoke Copilot while this implementation branch is under development.

**Goal:** Build and merge a fail-closed execution boundary for the frozen six-cell R1/R1A selection-validation contract.

**Spec:** `docs/superpowers/specs/2026-09-12-target-authority-selection-runner-design.md`

## Task 1 — RED: generated-case and decision semantics

Create `tests/test_selection_validation.py` before `selection_validation.py` exists. Tests must require:

- deterministic 12-case generation from a seed;
- different seeds change final instance identity;
- exactly six frozen cells × two replicates and at least four families;
- public output excludes expected state;
- `prepare` copies only the selected agent fixture;
- preserve cases reject production mutation;
- action cases reject passivity/unrelated mutation;
- probe cell requires `probe.py` execution before first production mutation;
- verify cell re-executes publisher from reset state and requires post-publish authoritative inspection;
- generated reference paths pass before admission;
- pure pair classification is fail-closed;
- frozen decision rule accepts only the exact required outcome shape and rejects harm, non-comparability, passivity, and insufficient preserve gain.

Run focused test and preserve the intended module-missing RED in Actions.

## Task 2 — GREEN: stdlib selection harness

Create `selection_validation.py` implementing:

- frozen plan/treatment identity validation;
- deterministic `generate` with public/hidden split;
- `prepare`;
- deterministic `grade` using Copilot JSONL tool events for ordered probe/verification evidence;
- reference-path admission checks;
- receipt creation with case/treatment/runtime/provenance hashes;
- pair summarization with actual-runtime comparability;
- final decision evaluation from the frozen plan.

Run focused tests, full unit suite, and `python verify.py`.

## Task 3 — RED/GREEN: trusted Actions runner

Create `tests/test_selection_validation_workflow.py` first. It must reject a missing workflow and then guard these properties:

- no `workflow_dispatch`, `pull_request`, or normal `main` push trigger;
- only dedicated execution-branch + marker-path push can start trials;
- marker validates single-file diff and exact parent runner commit before inference;
- plan/treatment identities are checked before inference;
- seed is `github.run_id`;
- one Copilot CLI version is frozen for the execution;
- case-pair matrix is `max-parallel: 1`;
- each pair runs R1 then R1A with separate workspaces/Copilot homes;
- repository/public bundle is removed before each model call;
- R1 raw output is uploaded and removed before R1A starts;
- hidden bundle is downloaded only after both model calls end;
- actual model/reasoning/tool set are attested;
- only model-success trials receive behavioral receipts;
- final job requires exactly 12 pair summaries and runs frozen decision logic.

Then add `.github/workflows/selection-validation.yml` minimally to make the tests pass. Normal CI must never consume Copilot credits.

## Task 4 — Repository reconciliation and PR

Update README/STATE only after runner tests are GREEN. State must say runner is merged/ready but final instances remain ungenerated until an execution marker is created from verified `main`.

Audit that runtime and R1A blobs are unchanged. Open a dedicated PR, verify PR CI, merge with exact expected head, then verify post-merge `main` CI.

## Task 5 — Separate execution boundary

Only after Task 4 is merged and post-merge CI is GREEN:

1. create `eval/execute-target-authority-selection-v1` from exact verified `main`;
2. add only `evals/selection-execution-trigger.json`, binding experiment, plan blob, and exact parent runner commit;
3. confirm branch diff is exactly that marker;
4. let the dedicated push workflow generate final instances from its run ID and execute all 12 sequential pairs;
5. retain every raw artifact and final decision;
6. do not revise R1A or cases after seeing results;
7. update STATE/results in a new evidence-only PR after auditing the artifacts.
