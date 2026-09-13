# Execution-Recovery Session-Fork Migration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the empirically impossible explicit-model preflight in the fresh execution-recovery development workflow with a pre-treatment local session fork that preserves actual runtime identity across U0/U1.

**Architecture:** A neutral seed job selects the runtime before treatment, stores local-only Copilot session state as an immutable artifact, and exposes the seed session ID/state hash. Each arm downloads the same artifact, clones it locally, verifies the same pre-treatment hash, constructs its treatment only after the fork, resumes the same session without model/reasoning flags, and refuses to write a behavioral receipt unless actual post-resume identity matches the seed attestation.

**Tech Stack:** GitHub Actions YAML, Bash, Python 3.12, existing `copilot_event_parser.py`, `execution_recovery_development.py`, unit tests, `python verify.py`.

**Spec:** `docs/superpowers/specs/2026-09-13-execution-recovery-session-fork-design.md`

## Global Constraints

- Runtime R1 stays byte-identical and 446 words.
- R1A stays frozen/rejected; no R1B is created.
- Historical manifests, fixtures, graders, consumed selection evidence, and prior mismatched attempts remain unchanged.
- Seed occurs before case preparation and treatment prompt construction.
- Seed session sync/export is disabled.
- Every arm starts from the same byte-identical seed session-state hash.
- Resumed behavioral invocations pass neither `--model` nor `--reasoning-effort`.
- Actual model/reasoning/tool set must match seed before receipt creation.
- Existing pair summary remains fail-closed on matched-context mismatch.

---

### Task 1: RED — Require session-fork semantics

**Files:**
- Modify: `tests/test_execution_recovery_development_cases.py`

**Interfaces:**
- Consumes: current development workflow text.
- Produces: static tests that reject the old explicit-model lock and require seed artifact, clone/hash verification, resume, and fork binding.

- [ ] Replace the two exact-model preflight tests with assertions for a `seed` job, seed artifact upload/download, local-only settings, session ID extraction, seed-state hashing, `--resume="$SESSION_ID"`, absence of explicit model/reasoning flags in behavioral invocation, actual runtime attestation, and `session_fork` in run-config.
- [ ] Run `python -m unittest discover -s tests -v`.
- [ ] Require RED only from the new migration expectations; historical tests must remain green.
- [ ] Commit as `test: require session-fork development boundary`.

### Task 2: GREEN — Migrate development workflow

**Files:**
- Modify: `.github/workflows/execution-recovery-development.yml`

**Interfaces:**
- Consumes: dispatch inputs, resolved Copilot CLI version, existing fresh cases/graders.
- Produces: seed artifact plus two independently resumed behavioral receipts sharing the same pre-treatment fork hash.

- [ ] Replace `preflight` with neutral `seed` job after `validate` + `resolve`.
- [ ] In seed job, run neutral Copilot call with dispatch model/reasoning policy, local-only home, bounded tools, no case access, unique `result.sessionId`, actual attestation, and session-state SHA-256.
- [ ] Upload `seed-home`, `session-id.txt`, `seed-attestation.json`, `seed-state-hash.txt`, and CLI version as `execution-recovery-seed-${{ github.run_id }}`.
- [ ] Make `trial` depend on `seed`, download the seed artifact, clone `seed-home` into its arm-local home, verify session-state hash equals seed, then prepare fixture/treatment.
- [ ] Resume the seed session with `--resume="$SESSION_ID"` and no behavioral `--model` or `--reasoning-effort` flags.
- [ ] Compare post-resume actual model/reasoning/tool set to seed attestation before writing metrics/run-config/receipt; mismatch exits as infrastructure failure and preserves raw evidence.
- [ ] Add matched `session_fork` object with seed session ID and seed-state SHA-256 to both run-configs.
- [ ] Keep existing grader, receipt, artifact retention, and pair summarizer behavior unchanged.
- [ ] Run `python -m unittest discover -s tests -v` and `python verify.py`; require GREEN.
- [ ] Commit as `fix: fork matched runtime before development trials`.

### Task 3: Record state and integrate

**Files:**
- Modify: `STATE.md`

**Interfaces:**
- Consumes: feasibility run `34731466073` and GREEN migration CI.
- Produces: boot state that distinguishes feasibility proof from behavioral proof and names the next live replicates.

- [ ] Record the exact-model preflight rejection from `34731153920` and session-fork feasibility PASS from `34731466073` with artifact/digest.
- [ ] State that migration is code-verified only until a live development dispatch proves cross-runner resume identity.
- [ ] Keep candidate gate closed unless matched fresh R1/U1 evidence exposes a residual failure.
- [ ] Run full tests + verifier.
- [ ] Open exact-head PR, require PR-triggered GREEN, merge with expected head, then require post-merge GREEN.
- [ ] Only after post-merge GREEN, run new replicate numbers for previously non-comparable development cells.
