# Execution-Recovery Model Lock Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent execution-recovery development pairs from reaching behavioral U0/U1 trials unless the provider-selected runtime can first be re-invoked by exact model ID with the same attested reasoning effort and tool set.

**Architecture:** Keep the public fresh cases and shared receipt/grader logic unchanged. Add a preflight job between CLI-version resolution and the behavioral matrix: first run a neutral probe using the dispatch request, attest the provider-selected runtime, then run a second neutral probe using that exact attested model ID and reasoning effort. Only if exact-lock attestation matches the selected model/reasoning/tool-set does the preflight expose locked outputs to both U0/U1 arms; otherwise the workflow fails before case preparation and produces no behavioral receipts.

**Tech Stack:** GitHub Actions YAML, GitHub Copilot CLI 1.0.83+ as resolved by the existing workflow, Python 3.12, `copilot_event_parser.py`, `unittest`.

**Spec:** `STATE.md` sections “Fresh R1 Baseline — 2026-09-13”, “Current Research Boundary”, and “Next Best Action”; exact baseline evidence in `evals/execution-recovery-development/results-2026-09-13.json`.

## Global Constraints

- Runtime `verified-delta/SKILL.md` must remain unchanged at 446 words and git blob `ac48f09ab02eca63e014b4c25f86e492ae5559cb`.
- Frozen R1A and historical evals must remain unchanged.
- `auto` is a dispatch request, never a matched-runtime guarantee.
- No behavioral trial may start if the exact model/reasoning lock cannot be proven before case preparation.
- Actual model, reasoning effort, and tool set remain authoritative and fail-closed.
- Preflight uses a neutral prompt and an empty temporary workspace; it must not read a case fixture or task prompt.
- Existing U0/U1 receipt and grader semantics remain unchanged.
- Full unit suite plus `python verify.py` must pass before merge.

---

### Task 1: Lock the preflight contract with RED tests

**Files:**
- Modify: `tests/test_execution_recovery_development_cases.py`
- Inspect: `.github/workflows/execution-recovery-development.yml`

**Interfaces:**
- Consumes: current workflow text at `WORKFLOW`.
- Produces: structural tests that require a `preflight` job, exact runtime outputs, and behavioral matrix dependency on that job.

- [ ] **Step 1: Add the failing workflow-contract test**

Add a test with these assertions:

```python
def test_behavioral_trials_require_exact_preflight_runtime_lock(self):
    workflow = WORKFLOW.read_text(encoding="utf-8")
    self.assertIn("preflight:", workflow)
    self.assertIn("needs: [validate, resolve]", workflow)
    self.assertIn("selected-model", workflow)
    self.assertIn("locked-model", workflow)
    self.assertIn("locked-reasoning-effort", workflow)
    self.assertIn("locked-tool-set", workflow)
    self.assertIn('needs: [validate, resolve, preflight]', workflow)
    self.assertIn('EXECUTION_MODEL_ID: ${{ needs.preflight.outputs.locked_model }}', workflow)
    self.assertIn('EXECUTION_REASONING_EFFORT: ${{ needs.preflight.outputs.locked_reasoning_effort }}', workflow)
    self.assertIn('--model="$EXECUTION_MODEL_ID"', workflow)
    self.assertNotIn('--model="$MODEL_ID" \\\n            "${REASONING_ARGS[@]}"', workflow)
```

Also require that the preflight block occurs textually before `trial:` and that case preparation (`execution_recovery_development.py prepare`) occurs only under `trial:`.

- [ ] **Step 2: Add a fail-closed attestation test**

Require workflow text to compare the first and second preflight attestations on all three matched dimensions:

```python
for needle in [
    'selected["model"] != locked["model"]',
    'selected["reasoning_effort"] != locked["reasoning_effort"]',
    'selected["tool_set"] != locked["tool_set"]',
]:
    self.assertIn(needle, workflow)
self.assertIn("exact runtime lock mismatch", workflow)
```

Require a preflight artifact name containing `execution-recovery-model-lock-` so failed lock attempts retain infrastructure evidence.

- [ ] **Step 3: Run the full unit suite and confirm RED**

Run through repository CI:

```bash
python -m unittest discover -s tests -v
```

Expected: the new model-lock tests fail because the workflow has no `preflight` job or locked outputs; unrelated tests remain green.

- [ ] **Step 4: Commit the RED state**

Commit only the test/plan changes with a message equivalent to:

```text
test: require exact development runtime lock
```

---

### Task 2: Implement the exact runtime lock minimally

**Files:**
- Modify: `.github/workflows/execution-recovery-development.yml`
- Test: `tests/test_execution_recovery_development_cases.py`

**Interfaces:**
- Consumes: `needs.resolve.outputs.copilot_version`, dispatch `model` and `reasoning_effort`, `copilot_event_parser.py attest-runtime`.
- Produces workflow outputs: `locked_model`, `locked_reasoning_effort`, and a serialized locked tool-set evidence file used for validation/provenance; U0/U1 both consume the same locked model/reasoning pair.

- [ ] **Step 1: Add a `preflight` job after `resolve`**

The job must:

```yaml
preflight:
  needs: [validate, resolve]
  runs-on: ubuntu-latest
  permissions:
    contents: read
    copilot-requests: write
  outputs:
    locked_model: ${{ steps.lock.outputs.locked_model }}
    locked_reasoning_effort: ${{ steps.lock.outputs.locked_reasoning_effort }}
```

Checkout the repository, set up Python 3.12, install exactly `needs.resolve.outputs.copilot_version`, and create only `$RUNNER_TEMP/execution-recovery-model-lock/workspace`.

- [ ] **Step 2: Run neutral provider selection**

Use the dispatch request and the same available-tool / allow-tool policy as behavioral trials, but a neutral prompt such as:

```text
Return READY. Do not modify files and do not solve any repository task.
```

Write JSONL to `selected-events.jsonl`, require zero exit status, then run:

```bash
python copilot_event_parser.py attest-runtime \
  "$ROOT/selected-events.jsonl" --json > "$ROOT/selected-attestation.json"
```

Extract non-empty `model` and a concrete `reasoning_effort` from the attestation.

- [ ] **Step 3: Re-invoke the exact attested runtime before behavior**

Run a second neutral Copilot invocation with:

```bash
--model="$SELECTED_MODEL"
--reasoning-effort="$SELECTED_REASONING"
```

and otherwise the same tool exposure/policy. Save `locked-events.jsonl`, require zero exit status, and attest it to `locked-attestation.json`.

- [ ] **Step 4: Fail closed on any identity drift**

Use Python to compare the two attestations exactly:

```python
if selected["model"] != locked["model"]:
    raise SystemExit("exact runtime lock mismatch: model")
if selected["reasoning_effort"] != locked["reasoning_effort"]:
    raise SystemExit("exact runtime lock mismatch: reasoning effort")
if selected["tool_set"] != locked["tool_set"]:
    raise SystemExit("exact runtime lock mismatch: tool set")
```

Only after these checks write `locked_model` and `locked_reasoning_effort` to `$GITHUB_OUTPUT`. If the provider-selected model cannot be invoked explicitly, the job fails here and no behavioral matrix starts.

- [ ] **Step 5: Bind both behavioral arms to locked outputs**

Change the trial dependency to:

```yaml
needs: [validate, resolve, preflight]
```

Keep `MODEL_ID: ${{ inputs.model }}` only for recording the original dispatch request. Add:

```yaml
EXECUTION_MODEL_ID: ${{ needs.preflight.outputs.locked_model }}
EXECUTION_REASONING_EFFORT: ${{ needs.preflight.outputs.locked_reasoning_effort }}
```

Invoke Copilot behavior with exact locked values:

```bash
--model="$EXECUTION_MODEL_ID" \
--reasoning-effort="$EXECUTION_REASONING_EFFORT"
```

The receipt continues to derive actual model/reasoning/tool-set from each arm’s own runtime attestation and remains fail-closed if provider behavior still drifts.

- [ ] **Step 6: Preserve preflight evidence**

Always upload the preflight directory as:

```text
execution-recovery-model-lock-${{ github.run_id }}
```

with 30-day retention. This artifact must include selected/locked JSONL, stderr, exit codes, attestations when available, and Copilot version.

- [ ] **Step 7: Run full verification and confirm GREEN**

Run:

```bash
python -m unittest discover -s tests -v
python verify.py
```

Expected: all tests pass and verifier exits 0. No runtime skill bytes change.

- [ ] **Step 8: Commit implementation**

Commit workflow changes with a message equivalent to:

```text
fix: lock execution recovery runtime before trials
```

---

### Task 3: Merge infrastructure before collecting new behavior

**Files:**
- Modify after successful live preflight if needed: `STATE.md`
- Do not modify: `verified-delta/SKILL.md`, `evals/candidates/r1-target-authority.md`

**Interfaces:**
- Consumes: exact branch/PR CI and a future manual workflow dispatch.
- Produces: a merged infrastructure boundary that can either prove a lockable runtime before behavior or fail without behavioral receipts.

- [ ] **Step 1: Review branch diff**

Confirm only plan/tests/workflow/state-if-required changed; reject any runtime-skill or historical-eval mutation.

- [ ] **Step 2: Require exact PR CI GREEN**

Require full unit suite + `python verify.py` on the exact PR head before merge.

- [ ] **Step 3: Merge with expected head SHA and require post-merge CI GREEN**

Do not collect fresh behavior from an unmerged workflow revision.

- [ ] **Step 4: Run one infrastructure-only live dispatch**

Dispatch one fresh development case with `model=auto`, `reasoning_effort=default`, and a new replicate number. Interpret outcomes as follows:

- preflight exact lock fails: infrastructure result only; no behavioral evidence should exist;
- preflight locks and U0/U1 both attest the same runtime: pair may be interpreted normally;
- any arm still differs from the lock: pair remains fail-closed and the infrastructure hypothesis is rejected.

- [ ] **Step 5: Update STATE only from observed evidence**

Record exact run/artifact identifiers and keep behavioral verification OPEN. Do not create R1B unless a fresh matched R1/U1 behavioral failure is observed.
