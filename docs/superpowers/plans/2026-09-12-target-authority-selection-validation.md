# Target-Authority Selection Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preregister a fail-closed, cross-domain selection-validation boundary for frozen R1 versus R1A without exposing final hidden task content or changing runtime behavior.

**Architecture:** Add one machine-readable preregistration artifact whose contents are guarded by a focused unit test. The artifact freezes treatment blobs, semantic cells, hidden-instance constraints, matched-context requirements, fixed budget, and the decision rule. Documentation/state are then reconciled to the new research boundary; execution infrastructure remains a separate subsequent change.

**Tech Stack:** Python 3.12 stdlib `unittest`, JSON, GitHub Actions verification workflow.

**Spec:** `docs/superpowers/specs/2026-09-12-target-authority-selection-validation-design.md`

## Global Constraints

- `verified-delta/SKILL.md` must remain blob `ac48f09ab02eca63e014b4c25f86e492ae5559cb`.
- `evals/candidates/r1-target-authority.md` must remain blob `26d93ce346deedccd7186ad5856f849136825ec3`.
- Final prompt text, final fixture values, and final expected answers must not be committed before execution.
- Selection validation uses exactly six semantic cells, two replicates per cell, two arms, for 24 model trials excluding infrastructure failures.
- No behavioral result may be observed before the preregistration contract and stopping rule are frozen.

---

### Task 1: Guard the preregistration contract with a failing test

**Files:**
- Create: `tests/test_target_authority_selection_plan.py`

**Interfaces:**
- Consumes: repository files `verified-delta/SKILL.md`, `evals/candidates/r1-target-authority.md`.
- Produces: executable invariants for `evals/target-authority-selection-plan.json`.

- [ ] **Step 1: Write the failing test**

Create a stdlib `unittest` case that loads `evals/target-authority-selection-plan.json` and asserts:

```python
self.assertEqual(plan["schema_version"], 1)
self.assertEqual(plan["experiment"], "target-authority-selection-validation-v1")
self.assertEqual(plan["evidence_class"], "selection-validation")
self.assertEqual(plan["treatments"]["R1"]["git_blob"], "ac48f09ab02eca63e014b4c25f86e492ae5559cb")
self.assertEqual(plan["treatments"]["R1A"]["git_blob"], "26d93ce346deedccd7186ad5856f849136825ec3")
self.assertEqual(len(plan["semantic_cells"]), 6)
self.assertEqual(plan["replicates_per_cell"], 2)
self.assertEqual(plan["arms"], ["R1", "R1A"])
self.assertEqual(plan["fixed_model_trial_budget"], 24)
self.assertFalse(plan["hidden_instance_boundary"]["commit_final_prompts_before_execution"])
self.assertFalse(plan["hidden_instance_boundary"]["commit_final_expected_answers_before_execution"])
self.assertTrue(plan["hidden_instance_boundary"]["use_all_generated_instances"])
self.assertEqual(plan["decision_rule"]["maximum_candidate_harm"], 0)
self.assertEqual(plan["decision_rule"]["minimum_candidate_gain_on_preserve_replicates"], 2)
```

Also assert the six required semantic cell IDs exactly match the design and that the committed runtime/candidate files still resolve to the expected Git blob IDs by invoking `git hash-object` when `.git` is available, with a deterministic Git-blob SHA-1 fallback in pure file environments.

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
python -m unittest tests.test_target_authority_selection_plan -v
```

Expected: FAIL because `evals/target-authority-selection-plan.json` does not exist.

- [ ] **Step 3: Commit only the failing test**

```bash
git add tests/test_target_authority_selection_plan.py
git commit -m "test: preregister target-authority selection boundary"
```

---

### Task 2: Add the frozen machine-readable preregistration

**Files:**
- Create: `evals/target-authority-selection-plan.json`
- Test: `tests/test_target_authority_selection_plan.py`

**Interfaces:**
- Consumes: frozen R1/R1A treatment identities and the design spec.
- Produces: one immutable experiment contract for later selection-validation execution.

- [ ] **Step 1: Add the minimum JSON contract**

The JSON must contain:

```json
{
  "schema_version": 1,
  "experiment": "target-authority-selection-validation-v1",
  "evidence_class": "selection-validation",
  "arms": ["R1", "R1A"],
  "replicates_per_cell": 2,
  "fixed_model_trial_budget": 24
}
```

and fully specify the frozen treatment blobs, six semantic cells, minimum four-domain coverage, username-normalization exclusion, hidden-instance boundary, matched causal dimensions, contamination behavior, infrastructure retry rule, and decision rule from the design.

Do not include final prompts, fixtures, answers, or grader outputs.

- [ ] **Step 2: Run the focused test and verify GREEN**

Run:

```bash
python -m unittest tests.test_target_authority_selection_plan -v
```

Expected: PASS.

- [ ] **Step 3: Run the full unit suite and verifier**

Run:

```bash
python -m unittest discover -s tests -v
python verify.py
```

Expected: both exit 0; `verify.py` reports the unchanged 446-word runtime skill.

- [ ] **Step 4: Commit the preregistration**

```bash
git add evals/target-authority-selection-plan.json
git commit -m "eval: freeze target-authority selection contract"
```

---

### Task 3: Reconcile research documentation without upgrading evidence status

**Files:**
- Modify: `README.md`
- Modify: `STATE.md`

**Interfaces:**
- Consumes: the frozen preregistration artifact.
- Produces: accurate boot/status documentation for the next session.

- [ ] **Step 1: Remove stale README status**

Replace the obsolete statement that no behavioral trial has been dispatched. State instead that development U0/U1 trials and target-authority stability ablation have run, while fresh selection validation remains unexecuted.

- [ ] **Step 2: Update STATE minimally**

Record:

- exact preregistration path;
- the six-cell/two-replicate/24-trial fixed boundary;
- frozen R1/R1A blob identities;
- that final hidden instances remain ungenerated/unseen;
- that runtime is unchanged;
- next evidence-producing action: implement/verify the execution runner, then execute only after the plan is frozen.

Do not call R1A proven or runtime-ready.

- [ ] **Step 3: Re-run full verification**

Run:

```bash
python -m unittest discover -s tests -v
python verify.py
```

Expected: both exit 0 and runtime skill word count remains 446.

- [ ] **Step 4: Commit docs/state**

```bash
git add README.md STATE.md
git commit -m "docs: advance state to selection validation"
```

---

### Task 4: Final branch audit

**Files:**
- Inspect only; no planned runtime edits.

**Interfaces:**
- Consumes: all branch changes.
- Produces: reviewable PR with fresh CI evidence.

- [ ] **Step 1: Audit the diff**

Confirm `verified-delta/SKILL.md` and `evals/candidates/r1-target-authority.md` have zero diff from base, no final hidden prompt/answer text is present, and every changed file belongs to the preregistration milestone.

- [ ] **Step 2: Run full verification again**

```bash
python -m unittest discover -s tests -v
python verify.py
```

Expected: exit 0.

- [ ] **Step 3: Open a PR against `main`**

The PR body must explicitly say this is preregistration/infrastructure evidence only, does not execute Copilot trials, and does not change runtime residency.

- [ ] **Step 4: Merge only after PR CI is green and the expected head SHA still matches**

After merge, verify `main` CI and re-check the runtime blob before any selection-validation execution work starts.
