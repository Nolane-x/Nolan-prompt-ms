# Selection Validation Boundary Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a preregistered, future-seeded R1-vs-R1A selection-validation harness whose exact cross-domain cases do not materialize until a manual GitHub Actions run starts.

**Architecture:** `selection_validation.py` owns deterministic selection, materialization, grading, receipt recording, pair summarization, and the frozen decision rule. A manual-only GitHub Actions workflow creates one future-seeded selected manifest, uploads it, fans out eight selected cases × two arms into fresh isolated jobs, attests actual Copilot runtime context, and fails closed when summarizing. The existing runtime skill and frozen candidate are inputs only and are not edited.

**Tech Stack:** Python 3.12 stdlib, unittest, GitHub Actions YAML, existing `eval_harness.py`, `semantic_ablation.py`, and `copilot_event_parser.py` conventions.

**Spec:** `docs/superpowers/specs/2026-09-12-selection-validation-design.md`

## Global Constraints

- Do not edit `verified-delta/SKILL.md`.
- Do not edit `evals/candidates/r1-target-authority.md`.
- Exact selected cases must be materialized only after `workflow_dispatch` starts.
- Select exactly four distinct families from a six-family catalog; materialize both `noop` and `partial` variants for each selected family.
- No-op and partial variants of one family use byte-identical prompt text.
- Every pair must compare R1 vs R1A under attested matched model, reasoning effort, tool set, harness, tool policy, and limits.
- Paid Copilot trials remain manual-only and are not dispatched by implementation CI.
- Decision-bearing run size is exactly 16 Copilot trials.
- The first complete comparable run is decision-bearing; behavioral failure is never rerun for a better seed.

---

### Task 1: Freeze the machine-readable selection contract

**Files:**
- Create: `evals/selection-validation-plan.json`
- Create: `tests/test_selection_validation_plan.py`

**Interfaces:**
- Consumes: design spec above.
- Produces: immutable experiment id `target-authority-selection-v1`, catalog names, selected-family count `4`, variants `noop/partial`, and decision thresholds consumed by `selection_validation.py`.

- [ ] **Step 1: Write the failing plan-contract test**

```python
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLAN = ROOT / "evals" / "selection-validation-plan.json"

class SelectionValidationPlanTests(unittest.TestCase):
    def test_plan_freezes_catalog_sampling_and_decision_rule(self):
        data = json.loads(PLAN.read_text(encoding="utf-8"))
        self.assertEqual(data["experiment"], "target-authority-selection-v1")
        self.assertEqual(data["selected_family_count"], 4)
        self.assertEqual(data["variants"], ["noop", "partial"])
        self.assertEqual(len(data["family_catalog"]), 6)
        self.assertEqual(data["decision_rule"]["max_candidate_harm"], 0)
        self.assertEqual(data["decision_rule"]["required_partial_passes"], 4)
        self.assertEqual(data["decision_rule"]["minimum_noop_passes"], 3)
        self.assertEqual(data["decision_rule"]["minimum_noop_candidate_gains"], 1)
        self.assertEqual(data["maximum_infrastructure_replacements"], 1)
```

- [ ] **Step 2: Run the test and verify RED**

Run: `python -m unittest tests.test_selection_validation_plan -v`

Expected: ERROR because `evals/selection-validation-plan.json` does not exist.

- [ ] **Step 3: Create the exact preregistration JSON**

It must contain the six family ids `retry-cap`, `stable-dedupe`, `export-suffix`, `boolean-flag`, `port-fallback`, `config-precedence`; selected count `4`; variants `["noop", "partial"]`; seed formula version `selection-v1`; manual-only cost boundary `16`; the decision thresholds above; and the invalid-run/stopping rules from the spec.

- [ ] **Step 4: Run test + full verifier**

Run: `python -m unittest tests.test_selection_validation_plan -v && python verify.py`

Expected: PASS.

- [ ] **Step 5: Commit**

Commit message: `eval: preregister selection-validation boundary`

---

### Task 2: Build future-seeded selection and materialization

**Files:**
- Create: `selection_validation.py`
- Create: `tests/test_selection_validation_factory.py`

**Interfaces:**
- Consumes: `evals/selection-validation-plan.json`.
- Produces:
  - `derive_seed(run_id: str, run_attempt: str, workflow_sha: str, candidate_sha256: str) -> str`
  - `select_families(seed_hex: str) -> list[str]`
  - `materialize(seed_hex: str, output_root: pathlib.Path) -> dict`
  - CLI `materialize --run-id ... --run-attempt ... --workflow-sha ... --output-root ... --json`
- Manifest entries contain `case_id`, `family`, `variant`, `prompt`, `parameters`, `fixture_sha256`, `grader_contract_version`.

- [ ] **Step 1: Write RED tests for determinism, future-context sensitivity, opposing pairs, and isolation**

```python
class SelectionFactoryTests(unittest.TestCase):
    def test_selection_is_deterministic_but_changes_with_future_run_id(self):
        a = sv.derive_seed("100", "1", "abc", "def")
        b = sv.derive_seed("100", "1", "abc", "def")
        c = sv.derive_seed("101", "1", "abc", "def")
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertEqual(len(sv.select_families(a)), 4)
        self.assertEqual(len(set(sv.select_families(a))), 4)

    def test_materialization_has_four_opposing_same_prompt_pairs(self):
        manifest = sv.materialize("0" * 64, self.root)
        self.assertEqual(len(manifest["cases"]), 8)
        by_family = {}
        for case in manifest["cases"]:
            by_family.setdefault(case["family"], []).append(case)
        self.assertEqual(len(by_family), 4)
        for pair in by_family.values():
            self.assertEqual({c["variant"] for c in pair}, {"noop", "partial"})
            self.assertEqual(len({c["prompt"] for c in pair}), 1)
```

Also assert agent-visible case directories contain only fixture files and `prompt.txt`; researcher-only expected data lives in the manifest outside those directories.

- [ ] **Step 2: Run and verify RED**

Run: `python -m unittest tests.test_selection_validation_factory -v`

Expected: import/file failure because `selection_validation.py` does not exist.

- [ ] **Step 3: Implement the six minimal generators**

Use only stdlib. Each generator returns prompt, seeded parameters, pristine fixture text, partial fixture text, and a family grader function. Seed family-specific RNG with `sha256(seed_hex + "|" + family_id)` so parameter generation remains stable if catalog ordering changes.

- [ ] **Step 4: Implement canonical manifest hashing and materialization**

Write `selected-manifest.json` with sorted keys and a top-level `manifest_sha256` computed over the manifest value before adding that field. Case ids are `<family>-<variant>`.

- [ ] **Step 5: Run focused + full tests**

Run: `python -m unittest tests.test_selection_validation_factory -v && python -m unittest discover -s tests -v && python verify.py`

Expected: PASS.

- [ ] **Step 6: Commit**

Commit message: `eval: materialize future-seeded selection cases`

---

### Task 3: Add researcher-side grading and immutable receipts

**Files:**
- Modify: `selection_validation.py`
- Create: `tests/test_selection_validation_harness.py`

**Interfaces:**
- Adds:
  - `grade_case(manifest_path, case_id, workspace) -> dict`
  - CLI `prepare MANIFEST CASE_ID DEST --json`
  - CLI `grade MANIFEST CASE_ID WORKSPACE --json`
  - CLI `record MANIFEST CASE_ID WORKSPACE RECEIPT --arm ... --pair-id ... --replicate ... --model-id ... --harness-id ... --transcript ... --metrics ... --run-config ... --json`
  - CLI `summarize RECEIPT... --json`
- Reuses canonical metrics/run-config validation from `eval_harness.py` and treatment semantics from `semantic_ablation.py` where possible.

- [ ] **Step 1: Write RED grader tests for all six families**

For every family generated with a fixed seed, assert pristine `noop` passes and pristine `partial` fails. Then apply the smallest correct patch to the partial workspace and assert it passes. For a no-op workspace, make an unnecessary but behavior-preserving production edit and assert grading fails.

- [ ] **Step 2: Run RED**

Run: `python -m unittest tests.test_selection_validation_harness -v`

Expected: failures because grading/recording commands are absent.

- [ ] **Step 3: Implement graders and prepare boundary**

No-op requires behavior probes + byte-identical production files + no extras. Partial requires behavior probes + necessary production delta + no extras. Hidden probes derive from manifest parameters and additional deterministic probe values not included in prompt examples.

- [ ] **Step 4: Implement receipt provenance**

Bind selected-manifest digest, selector/harness digest, treatment members/set digest, fixture digest, workspace/transcript/metrics, canonical run config, and grade. Refuse overwrite.

- [ ] **Step 5: Implement pair summarization and decision classification**

Effects remain `same_fail`, `same_pass`, `candidate_gain`, `candidate_harm`. Summary emits `selection_pass`, `selection_fail`, `selection_inconclusive`, or `invalid_infrastructure` by the preregistered rule. Missing/duplicate/non-comparable pairs force invalidation.

- [ ] **Step 6: Verify RED→GREEN and historical independence**

Run: `python -m unittest tests.test_selection_validation_harness -v && python -m unittest discover -s tests -v && python verify.py`

Expected: PASS. Tests must also prove a stored receipt can be summarized from recorded provenance without requiring current candidate bytes to match a future edited file.

- [ ] **Step 7: Commit**

Commit message: `eval: add selection grading and receipts`

---

### Task 4: Add the manual fresh selection workflow

**Files:**
- Create: `.github/workflows/selection-validation.yml`
- Create: `tests/test_selection_validation_workflow.py`

**Interfaces:**
- Manual inputs: `model` default `auto`, `reasoning_effort` default `default`.
- Jobs: `validate`, `resolve`, `select`, dynamic `trial`, `summarize`.
- `select` outputs a JSON matrix of eight case ids and uploads materialized selection artifact.
- `trial` expands case × arm `[R1, R1A]` into 16 fresh jobs.

- [ ] **Step 1: Write RED workflow contract test**

Assert `workflow_dispatch` only; no push/PR trigger; one pinned CLI version; selector seed includes `${{ github.run_id }}`, `${{ github.run_attempt }}`, `${{ github.sha }}`; selected manifest artifact exists; matrix contains selected cases × arms; fresh `COPILOT_HOME`; only `bash,create,edit,view,glob,grep`; actual runtime attestation drives model/reasoning/tool set/tool calls; exactly 16 expected receipts; summary runs fail-closed; treatments point to exact R1/R1A files.

- [ ] **Step 2: Run RED**

Run: `python -m unittest tests.test_selection_validation_workflow -v`

Expected: failure because workflow does not exist.

- [ ] **Step 3: Implement selector/resolve jobs without model calls**

`select` checks treatment digests, materializes cases under `$RUNNER_TEMP/selection`, emits compact case matrix JSON via `$GITHUB_OUTPUT`, uploads the entire selection directory, and never grants `copilot-requests: write`.

- [ ] **Step 4: Implement trial jobs**

Each trial downloads the selection artifact, prepares exactly one fixture workspace, force-loads R1 or R1A, invokes pinned Copilot CLI with the established isolation flags, records raw JSONL/transcript/stderr, attests runtime context, grades, and writes one immutable receipt.

- [ ] **Step 5: Implement summary job**

Download all raw artifacts, require exactly 16 receipts, call `selection_validation.py summarize`, fail when status is `invalid_infrastructure`, and preserve summary artifact even on failure. A valid `selection_fail` is an experimental result, not workflow infrastructure failure; the job should still upload it clearly without silently rerunning.

- [ ] **Step 6: Full verification**

Run: `python -m unittest discover -s tests -v && python verify.py`

Expected: PASS with zero Copilot behavioral calls because the workflow is manual-only.

- [ ] **Step 7: Commit**

Commit message: `eval: add fresh selection-validation runner`

---

### Task 5: Update bootloader state and merge without running the holdout

**Files:**
- Modify: `STATE.md`

**Interfaces:**
- Records tool-set provenance correction, frozen selection design, workflow existence, 16-call cost boundary, and that selection result is still OPEN because no workflow has been dispatched.

- [ ] **Step 1: Update STATE without changing R1/R1A wording**

Record that historical development/stability effects remain interpretable because same-run arms shared requested tools, but their old `matched.tool_set` represented requested rather than attested availability. State that new runners use actual tool-set attestation and omit unsupported `apply_patch`.

- [ ] **Step 2: Verify repository reality**

Run: `python -m unittest discover -s tests -v && python verify.py`

Also verify `git hash-object verified-delta/SKILL.md` equals the incumbent blob and `git hash-object evals/candidates/r1-target-authority.md` equals the frozen candidate blob recorded before this work.

- [ ] **Step 3: Audit diff and PR**

Diff must contain only selection-validation design/plan/preregistration, selection harness/tests/workflow, the provenance hardening already integrated on main, and STATE documentation. No runtime skill or candidate edits.

- [ ] **Step 4: Merge only after PR CI is green**

Use expected-head SHA. Run post-merge main verification.

- [ ] **Step 5: Stop before paid execution**

Do not dispatch `selection-validation.yml`. Report that the infrastructure is ready and request/confirm explicit authorization for exactly 16 Copilot trial calls before the decision-bearing run.
