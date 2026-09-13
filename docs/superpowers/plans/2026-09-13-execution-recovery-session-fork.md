# Execution-Recovery Session-Fork Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove or reject pre-treatment Copilot CLI session forking as a way to obtain matched-runtime development evidence, and migrate the fresh development runner only if the proof passes.

**Architecture:** A neutral `auto` seed session resolves runtime identity before treatment. Its local-only `COPILOT_HOME` is cloned byte-for-byte into isolated U0/U1 homes; both arms resume the same session ID without explicit model or reasoning flags, then actual runtime identity and fork isolation are compared fail-closed. Migration is conditional on a live spike satisfying every frozen feasibility check.

**Tech Stack:** GitHub Actions YAML, Bash, Python 3.12, GitHub Copilot CLI 1.0.83-or-resolved single version, existing `copilot_event_parser.py`, existing unit test suite, `python verify.py`.

**Spec:** `docs/superpowers/specs/2026-09-13-execution-recovery-session-fork-design.md`

## Global Constraints

- Do not edit `verified-delta/SKILL.md`, R1, R1A, consumed hidden evidence, development fixtures, or graders.
- Behavioral verification gate stays OPEN.
- Requested model/reasoning settings are never proof; actual runtime attestation is authoritative.
- No retry-until-match behavior.
- Spike produces infrastructure evidence only, never behavioral evidence.
- Session sync/export must be disabled before seed creation.
- U0 and U1 must use distinct writable `COPILOT_HOME` clones created before treatment.
- Any resume failure, identity drift, ambiguous session state, or cross-fork contamination rejects session-fork architecture.

---

### Task 1: Live Session-Fork Feasibility Spike

**Files:**
- Create: `.github/workflows/execution-recovery-session-fork-spike.yml`
- Create: `tests/test_execution_recovery_session_fork_spike.py`

**Interfaces:**
- Consumes: `verified-delta/SKILL.md`, `copilot_event_parser.py`, GitHub Actions `copilot-requests: write` permission.
- Produces: artifact `execution-recovery-session-fork-spike-<run_id>` containing `verdict.json`, seed/U0/U1 event streams, attestations, session-state hashes, exit codes, and stderr.

- [ ] **Step 1: Write the failing static workflow contract test**

Add `tests/test_execution_recovery_session_fork_spike.py` asserting the spike workflow contains all causal boundaries:

```python
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "execution-recovery-session-fork-spike.yml"


class ExecutionRecoverySessionForkSpikeTests(unittest.TestCase):
    def test_spike_forks_local_session_before_treatment_and_attests_all_arms(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for needle in [
            "COPILOT_HOME=\"$SEED_HOME\"",
            '"remoteExport": false',
            'session-state/$SESSION_ID',
            'cp -a "$SEED_HOME/." "$U0_HOME/"',
            'cp -a "$SEED_HOME/." "$U1_HOME/"',
            '--resume="$SESSION_ID"',
            'cat verified-delta/SKILL.md',
            'seed-attestation.json',
            'u0-attestation.json',
            'u1-attestation.json',
            'verdict.json',
        ]:
            self.assertIn(needle, workflow)
        self.assertNotIn('--model="$SELECTED_MODEL"', workflow)
        self.assertNotIn("execution_recovery_development.py prepare", workflow)

    def test_spike_requires_identity_and_isolation_checks_before_pass(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        for needle in [
            'seed["model"] == u0["model"] == u1["model"]',
            'seed["reasoning_effort"] == u0["reasoning_effort"] == u1["reasoning_effort"]',
            'seed["tool_set"] == u0["tool_set"] == u1["tool_set"]',
            'pre_u0 == pre_u1 == pre_seed',
            'post_u0 != pre_u0',
            'post_u1 != pre_u1',
            'post_u0 != post_u1',
            '"passed": passed',
        ]:
            self.assertIn(needle, workflow)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the full unit suite to verify RED**

Run:

```bash
python -m unittest discover -s tests -v
```

Expected: only the new spike tests fail because the workflow file does not exist yet; historical tests remain green.

- [ ] **Step 3: Implement the minimal push-triggered spike workflow**

Create `.github/workflows/execution-recovery-session-fork-spike.yml` with these exact phases:

```text
checkout -> setup Python -> resolve/install one Copilot CLI version
-> initialize local-only seed COPILOT_HOME
-> run neutral seed with model=auto
-> parse sessionId from result event
-> require session-state/<sessionId>
-> attest seed
-> hash seed home/session state
-> clone seed home to U0 and U1
-> verify both pre-treatment clone hashes equal seed
-> resume U0 with neutral control continuation
-> resume U1 with verified-delta/SKILL.md + same neutral continuation
-> attest U0 and U1
-> hash post-resume state independently
-> write verdict.json from frozen eight-condition decision rule
-> upload all evidence always
-> fail job if verdict.passed is false
```

Implementation requirements:

```bash
mkdir -p "$SEED_HOME"
printf '%s\n' '{"remoteExport": false}' > "$SEED_HOME/settings.json"
export COPILOT_HOME="$SEED_HOME"
```

Parse the seed session ID only from a unique JSONL `result.sessionId`; reject zero or multiple IDs.

Clone only after seed exit:

```bash
mkdir -p "$U0_HOME" "$U1_HOME"
cp -a "$SEED_HOME/." "$U0_HOME/"
cp -a "$SEED_HOME/." "$U1_HOME/"
```

Resume without `--model` and without `--reasoning-effort`:

```bash
COPILOT_HOME="$U0_HOME" copilot --resume="$SESSION_ID" --prompt="Return CONTROL_READY. Do not inspect or modify files." ...
```

For U1, build the continuation prompt from the exact runtime skill plus the same neutral sentence, but expose no development fixture.

- [ ] **Step 4: Run full static verification GREEN**

Run:

```bash
python -m unittest discover -s tests -v
python verify.py
```

Expected: all tests and verifier PASS; runtime skill remains 446 words.

- [ ] **Step 5: Commit the workflow so its branch `push` trigger executes the live spike**

Commit message:

```text
spike: test pre-treatment Copilot session fork
```

The workflow must restrict its push trigger to `spike/execution-recovery-session-fork` so the experiment runs exactly when this spike implementation is committed.

- [ ] **Step 6: Inspect the live artifact and freeze the feasibility verdict**

Require one artifact containing `verdict.json`. A PASS requires all eight spec conditions in one run. Any failed condition rejects the architecture; do not rerun until matched.

- [ ] **Step 7: Record the spike result in `STATE.md`**

If PASS, state only that session-fork is feasibility-proven for the observed provider/CLI configuration and authorize Task 2. If FAIL, state the exact failed condition and reject Task 2.

---

### Task 2: Migrate Fresh Development Runner — Only After Task 1 PASS

**Files:**
- Modify: `.github/workflows/execution-recovery-development.yml`
- Modify: `tests/test_execution_recovery_development_cases.py`
- Modify: `STATE.md`

**Interfaces:**
- Consumes: Task 1 PASS artifact and frozen session-fork semantics.
- Produces: fresh development U0/U1 receipts where both arms are resumed from byte-identical pre-treatment session state and still independently attested after treatment.

- [ ] **Step 1: Write RED tests replacing exact-model-lock requirements with session-fork requirements**

Update the development workflow tests to require:

```text
neutral seed job before trial
local-only COPILOT_HOME
unique sessionId extraction
pre-treatment U0/U1 clone hashes
--resume=<sessionId> in both arm jobs
no explicit --model in resumed behavioral invocation
actual runtime attestation per arm
post-treatment matched-context comparison
```

Also assert the old exact-model reinvocation path is absent.

- [ ] **Step 2: Run the full unit suite and require only the new migration expectations to fail**

Run:

```bash
python -m unittest discover -s tests -v
```

Expected: RED only on development workflow session-fork expectations.

- [ ] **Step 3: Implement the smallest migration**

Replace the current exact-model preflight with neutral seed/fork evidence. Behavioral U0/U1 must each receive one isolated clone and resume the same seed session ID. Keep existing fixtures, graders, immutable receipt logic, treatment prompts, tool policy, CLI version pinning, and fail-closed pair summarizer unchanged.

Each `run-config.json` must continue to record **actual** post-resume model, reasoning effort, and tool set. Additionally bind a hash of the common pre-treatment seed state so the two arms prove they began from the same fork point.

- [ ] **Step 4: Verify GREEN locally/CI**

Run:

```bash
python -m unittest discover -s tests -v
python verify.py
```

Expected: all tests + verifier PASS; runtime skill still 446 words.

- [ ] **Step 5: Open exact-head PR and require PR-triggered GREEN**

Review the diff to ensure only development infrastructure/tests/state changed. Merge only with exact expected head SHA after PR CI passes.

- [ ] **Step 6: Run post-merge verification**

Require main CI GREEN before generating new development evidence.

- [ ] **Step 7: Generate new fresh replicates without replacing old mismatches**

Use new replicate numbers for `incidental-artifact-cleanup` and `required-artifact-preserved`. Preserve all prior runs. Interpret treatment effect only if post-resume receipts remain matched under actual runtime attestation.

- [ ] **Step 8: Re-evaluate candidate gate**

If matched fresh R1/U1 still passes target cases, do not create R1B. Only a reproducible matched R1/U1 failure with interpretable opposing controls may reopen candidate design.
