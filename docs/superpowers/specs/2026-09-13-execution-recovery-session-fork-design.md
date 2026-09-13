# Execution-Recovery Session-Fork Design

## Status

Feasibility-proven infrastructure design for obtaining matched-runtime development evidence when GitHub Copilot CLI `auto` routing selects provider-internal model IDs that cannot be invoked through public `--model`.

This design does **not** change `verified-delta/SKILL.md`, R1, R1A, consumed hidden evidence, fixtures, or graders. Behavioral verification remains open.

## Problem

Fresh execution-recovery development runs showed `auto` can route U0 and U1 to different actual runtimes. The existing pair summarizer correctly rejects those pairs as not comparable.

PR #32 added an exact-runtime preflight: call Copilot with `auto`, attest selected model/reasoning/tool set, then invoke that exact model/reasoning identity before behavioral trials. Live run `34731153920` disproved that architecture for the current provider surface: `auto` selected `mai-code-1.1-flash` / `medium`, while the same CLI rejected `--model=mai-code-1.1-flash` before inference.

The root cause is provider/API asymmetry, not a grader, fixture, or candidate defect.

## Feasibility Result

Throwaway spike run `34731466073` from commit `d94e8f3980b72125f5cc826d27603225145b477b` tested a pre-treatment session fork. Artifact `10309745927`, digest `sha256:bf1a6d7ab1405a5d3a3dd43c00d748c7eb3b79489a963ed205aad9295b9d0459`, passed its frozen feasibility rule in one attempt.

Observed seed/U0/U1 runtime identity was identical:

- model: `gpt-5.6-luna`;
- reasoning: `medium`;
- tool set: `[bash, glob, rg, view]`;
- seed/U0/U1 exit code: `0`.

Pre-treatment session-state hashes were byte-identical across seed/U0/U1. U0 and U1 then independently mutated their own cloned session histories, diverged after different continuation prompts, and did not mutate each other's clone.

This proves only infrastructure feasibility for the observed provider/CLI configuration. It is not behavioral evidence or a residency claim.

## Production Development Architecture

### 1. Neutral seed job

Before case preparation or treatment prompt construction, one seed job runs Copilot under a dedicated local-only `COPILOT_HOME` with the requested pair-level model input (`auto` by default), requested reasoning policy, the same bounded tool surface as trials, and a neutral prompt that cannot inspect or solve any development case.

Session sync/export is disabled. The job extracts exactly one `result.sessionId`, requires `session-state/<sessionId>/`, attests actual runtime identity, and hashes the complete session-state tree.

### 2. Immutable seed artifact

The seed job uploads the local Copilot home plus:

- session ID;
- seed runtime attestation;
- seed session-state SHA-256;
- pinned Copilot CLI version.

No case fixture, grader, treatment prompt, or behavioral outcome is present in the seed artifact.

### 3. Isolated pre-treatment clones

Each matrix arm downloads the exact same seed artifact onto a fresh runner, clones the seed home into its own writable `COPILOT_HOME`, and recomputes the pre-treatment session-state hash. The arm may continue only if that hash equals the seed hash.

Only after the clone is verified does the arm prepare its case workspace and U0/U1 treatment prompt.

### 4. Resume instead of explicit model invocation

Behavioral inference uses `--resume=<sessionId>` from the isolated cloned home and passes neither `--model` nor `--reasoning-effort`. U0 and U1 therefore begin from the same pre-treatment session state while receiving different treatment prompts only after the fork.

### 5. Actual attestation remains authoritative

Each arm independently attests its actual model ID, reasoning effort, and tool set after resume. Before writing a behavioral receipt, the arm must prove its actual identity equals the seed attestation. Any mismatch is infrastructure/causal failure and produces no behavioral receipt.

### 6. Matched run config binds the fork point

Each run-config continues to record actual post-resume model, reasoning, tool set, CLI/harness identity, tool policy, limits, and intervention. It additionally binds a common `session_fork` object containing the seed session ID and pre-treatment session-state hash. Because matched-context SHA includes this object, U0/U1 cannot be compared unless they prove the same fork point.

## Failure Semantics

- Seed failure or ambiguous session ID: infrastructure failure; no behavioral receipt.
- Seed artifact/hash mismatch on an arm: infrastructure failure; no behavioral receipt.
- Resume failure: infrastructure failure; no behavioral receipt.
- Post-resume model/reasoning/tool-set drift from seed: causal comparability failure; no behavioral receipt.
- U0/U1 matched-context mismatch: existing pair summarizer rejects the pair fail-closed.
- A green workflow is not behavioral utility; graders and receipts remain authoritative.

## Migration Constraints

- Keep historical `evals/evals.json`, old U0/U1 evidence, frozen selection evidence, fixtures, graders, R1, and R1A unchanged.
- Preserve prior mismatched development runs; never replace or reinterpret them.
- New evidence must use new replicate numbers.
- Do not create R1B unless new matched fresh R1/U1 evidence demonstrates a reproducible residual failure with interpretable opposing controls.
- Behavioral verification gate remains OPEN.
