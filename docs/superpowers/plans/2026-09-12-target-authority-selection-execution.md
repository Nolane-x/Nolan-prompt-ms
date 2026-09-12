# Target-Authority Selection Execution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify the execution-only selection-validation harness and manual workflow for the frozen R1/R1A target-authority experiment without dispatching behavioral trials.

**Architecture:** A new stdlib-only `selection_validation.py` owns deterministic execution-time instance generation, hidden-surface isolation, reference admission, receipt/provenance validation, matched-pair summarization, and literal decision-rule evaluation. A manual GitHub Actions workflow generates/admit one frozen bundle, fans out the exact 12×2 arm matrix under matched Copilot settings, and summarizes all 24 receipts after execution.

**Tech Stack:** Python 3.12 stdlib, `unittest`, JSON, GitHub Actions, GitHub Copilot CLI.

**Spec:** `docs/superpowers/specs/2026-09-12-target-authority-selection-execution-design.md`

## Global Constraints

- `verified-delta/SKILL.md` remains blob `ac48f09ab02eca63e014b4c25f86e492ae5559cb`.
- `evals/candidates/r1-target-authority.md` remains blob `26d93ce346deedccd7186ad5856f849136825ec3`.
- `evals/target-authority-selection-plan.json` is frozen and must not be weakened or rewritten from observed outcomes.
- No final execution seed, final prompt instances, final fixture values, or final expected answers are committed.
- This branch must not dispatch behavioral Copilot trials.

---

### Task 1: RED — executable hidden-instance boundary

**Files:**
- Create: `tests/test_selection_validation_harness.py`

**Interfaces:**
- Produces expected CLI contracts for `generate`, `admit`, and `prepare`.

- [ ] Write tests asserting deterministic generation from the same seed, exactly 12 instances, exactly two per frozen cell, at least four allowed task families, unique identities, and no username-normalization derivatives.
- [ ] Assert an existing output directory is rejected and no seedless/default generation path exists.
- [ ] Assert `prepare` copies only fixture files and emits the task prompt without copying grader/reference/hidden metadata.
- [ ] Assert every generated reference path passes admission and tampered hidden/reference material fails closed.
- [ ] Run `python -m unittest tests.test_selection_validation_harness -v`; expected RED because `selection_validation.py` does not exist.

### Task 2: GREEN — generator, admission, preparation

**Files:**
- Create: `selection_validation.py`
- Test: `tests/test_selection_validation_harness.py`

**Interfaces:**
- `generate --seed SEED --output DIR --json`
- `admit BUNDLE --json`
- `prepare BUNDLE CASE_ID DEST --json`

- [ ] Implement frozen-plan validation and treatment-blob validation.
- [ ] Implement six domain-distinct generation methods producing two replicates per cell and at least four families overall.
- [ ] Keep final values seed-derived and hidden expectations outside agent-visible fixture/prompt surface.
- [ ] Implement deterministic graders/reference paths and all-instance admission.
- [ ] Implement agent-safe preparation.
- [ ] Re-run focused tests to GREEN.

### Task 3: RED→GREEN — immutable selection receipts and exact decision rule

**Files:**
- Extend: `tests/test_selection_validation_harness.py`
- Extend: `selection_validation.py`

**Interfaces:**
- `record BUNDLE CASE_ID WORKSPACE RECEIPT --arm R1|R1A --model-id ... --harness-id ... --transcript ... --metrics ... --run-config ... --json`
- `summarize BUNDLE RECEIPT... --json`

- [ ] Add failing tests for immutable receipt creation, treatment/provenance binding, seed/case/prompt/fixture/grader identities, and deterministic grading.
- [ ] Add failing tests proving actual matched-context drift yields `not_comparable`.
- [ ] Add failing tests for duplicate/missing receipts and contamination.
- [ ] Add failing tests for exact preregistered pass/fail thresholds, including one minority `candidate_harm` causing failure.
- [ ] Run focused RED.
- [ ] Implement minimum receipt loader/validator, pair classification, complete 12-pair accounting, and literal decision evaluation.
- [ ] Run focused GREEN.

### Task 4: RED→GREEN — manual all-pairs workflow

**Files:**
- Create: `tests/test_selection_validation_workflow.py`
- Create: `.github/workflows/target-authority-selection.yml`

**Interfaces:**
- Manual `workflow_dispatch` inputs include explicit execution seed and model/reasoning selectors.
- Generate/admit job emits dynamic matrix consumed by paired arm jobs.

- [ ] Write failing workflow tests asserting manual-only trigger, explicit seed, pre-trial generation/admission, one pinned CLI version, dynamic 12×2 arm execution, isolated `$RUNNER_TEMP`/`COPILOT_HOME`, restricted tools, runtime attestation, arm-specific frozen prompt loading, immutable receipts, exactly 24 receipt requirement, and final summarize artifact.
- [ ] Run focused RED.
- [ ] Implement the minimum workflow satisfying those boundaries; do not dispatch it.
- [ ] Run focused GREEN.

### Task 5: Repository invariant and state reconciliation

**Files:**
- Modify: `README.md`
- Modify: `STATE.md`
- Optionally modify: `verify.py` and `tests/test_verify.py` only if a deterministic no-hidden-instance invariant is needed beyond focused tests.

- [ ] Document execution infrastructure as verified-but-unexecuted, not behavioral evidence.
- [ ] Record exact RED/GREEN run IDs after CI exists, runtime/candidate blobs, and next action: merge first, verify post-merge CI, then dispatch exactly one frozen 24-trial selection run.
- [ ] Run full unit discovery and `python verify.py`.

### Task 6: Branch audit and PR

**Files:**
- Inspect all branch changes.

- [ ] Confirm no diff to R1, R1A, or preregistered decision rule.
- [ ] Confirm no final seed/prompts/fixture values/expected answers are committed.
- [ ] Confirm focused and full tests plus verifier pass.
- [ ] Open PR describing infrastructure-only scope and RED→GREEN evidence.
- [ ] Merge only with exact expected head SHA after green PR CI, then verify post-merge main CI before any behavioral dispatch.
