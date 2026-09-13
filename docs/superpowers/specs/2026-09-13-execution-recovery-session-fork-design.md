# Execution-Recovery Session-Fork Design

## Status

Research architecture for obtaining matched-runtime development evidence when GitHub Copilot CLI `auto` routing selects provider-internal model IDs that cannot be invoked through the public `--model` flag.

This design does **not** change `verified-delta/SKILL.md`, R1, R1A, any consumed hidden evidence, or any grader. Behavioral verification remains open.

## Problem

Fresh execution-recovery development runs proved that `auto` can route U0 and U1 to different actual runtimes. The existing pair summarizer correctly marks those pairs not comparable.

PR #32 added an exact-runtime preflight: call Copilot with `auto`, attest the selected model/reasoning/tool set, then invoke the exact model/reasoning identity before any behavioral trial. Live run `34731153920` showed the architecture is incompatible with the current provider surface:

- `auto` selected `mai-code-1.1-flash`, reasoning `medium`;
- runtime events reported that model as the only `availableModels` candidate;
- a subsequent `--model=mai-code-1.1-flash --reasoning-effort=medium` invocation failed before inference with `Model "mai-code-1.1-flash" from --model flag is not available.`;
- behavioral trial jobs were skipped, so the run produced no behavioral evidence.

The root problem is therefore provider/API asymmetry, not a grader, fixture, or candidate defect.

## Goal

Test whether a runtime selected by `auto` can be assigned **before treatment** and then reused by two isolated treatment arms without public explicit-model invocation.

If and only if this is empirically true, replace the impossible exact-model preflight with a session-fork boundary that produces matched runtime evidence while preserving fail-closed causal semantics.

## Proposed Architecture

### 1. Neutral seed session

Create one local Copilot CLI session under a dedicated `COPILOT_HOME` with:

- `model=auto`;
- default reasoning selection;
- the exact same bounded tool surface intended for behavioral trials;
- built-in MCPs, custom instructions, experimental features, remote export, and auto-update disabled;
- a neutral prompt that cannot solve or inspect any development case.

The seed prompt exists only to force `auto` to resolve a runtime before treatment. Its complete conversation history is shared identically by both future arms.

### 2. Local-only persistence

Keep session persistence local. The seed `COPILOT_HOME` must disable remote session export/sync so that two forked copies cannot race through cloud session state.

After the seed call exits, obtain the authoritative `sessionId` from the JSONL `result` event and require a corresponding `session-state/<sessionId>/` directory.

### 3. Pre-treatment fork

Before either arm receives treatment:

- clone the complete seed `COPILOT_HOME` to isolated U0 and U1 homes;
- record hashes of the seed session-state tree and require both clone hashes to match it;
- never share a writable home between the arms.

The fork point is therefore causally upstream of the intervention.

### 4. Resume instead of explicit model selection

Each arm resumes the same seed `sessionId` from its own cloned home using `--resume=<sessionId>` and **does not pass `--model` or `--reasoning-effort`**.

For the feasibility spike:

- U0 receives a short neutral continuation prompt;
- U1 receives the current `verified-delta/SKILL.md` followed by the same neutral continuation prompt.

No development fixture is exposed in the spike. This isolates whether treatment shape itself changes runtime identity on resume.

### 5. Actual attestation remains authoritative

The spike and any future behavioral runner must parse runtime events independently for seed, U0, and U1 and compare at least:

- actual model ID;
- actual reasoning effort;
- actual tool set.

The pair is admissible only when both resumed arms match each other and match the seed identity. Requested settings are never treated as proof.

### 6. Fork isolation checks

The spike must additionally prove:

- both clones start from the same seed session-state hash;
- U0 and U1 mutate only their own cloned session state;
- their post-resume session histories diverge as expected after different continuation prompts;
- neither branch modifies the other branch's home;
- no development case or grader data is present in the neutral seed workspace.

## Feasibility Decision Rule

The session-fork architecture is feasible only if one live spike satisfies all conditions in a single run:

1. seed `auto` invocation succeeds and yields a concrete session ID;
2. local seed session-state exists and can be cloned exactly;
3. both `--resume=<sessionId>` invocations succeed without an explicit model flag;
4. seed, U0, and U1 attest the **same** actual model ID;
5. seed, U0, and U1 attest the **same** concrete reasoning effort;
6. seed, U0, and U1 attest the **same** tool set;
7. U0 and U1 start from byte-identical pre-treatment session state;
8. U0 and U1 post-resume state remains isolated and independently mutated.

Any failure rejects the architecture for causal use. There is no retry-until-match rule and no behavioral evidence is produced by the spike.

## Failure Semantics

- Provider rejection of resume: infrastructure failure; session-fork rejected.
- Runtime identity drift after resume: causal comparability failure; session-fork rejected.
- Missing or ambiguous session ID/state: infrastructure failure; session-fork rejected.
- Shared-state contamination between forks: architecture failure; session-fork rejected.
- A successful spike proves only **feasibility of pre-treatment runtime assignment in this observed provider/CLI configuration**. It does not prove behavioral utility, runtime residency, or general provider stability.

## Behavioral Harness Migration, If Feasible

Only after the spike passes:

1. write TDD tests requiring the session-fork boundary before behavioral trials;
2. replace the exact-model preflight with neutral seed + fork + resume;
3. keep the current immutable receipts, actual-runtime attestation, exact final-tree graders, and fail-closed pair summarizer;
4. run new fresh development replicates; do not reinterpret or overwrite prior mismatched attempts;
5. do not create R1B unless matched fresh R1/U1 evidence exposes a reproducible residual failure.

## Rejected Alternatives

- **Retry `auto` until U0/U1 happen to match:** selection-on-outcome and not causal evidence.
- **Use the provider-internal model ID with `--model`:** empirically rejected by run `34731153920`.
- **Run both behavioral arms independently under `auto` and compare only after the fact:** still permits treatment-dependent routing and loses pairs unpredictably.
- **Share one writable resumed session between U0 and U1:** treatment contamination and order dependence.
- **Treat session resume as model pinning because documentation says history is restored:** documentation does not guarantee runtime identity; live attestation is required.

## Research Boundary

Until the feasibility spike passes, runtime R1 remains unchanged at 446 words, R1A remains rejected, no R1B exists, and the behavioral verification gate remains OPEN.
