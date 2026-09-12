# Target-Authority Selection Validation Design

## Purpose

R1A (`evals/candidates/r1-target-authority.md`) is development-stable only. The next evidence boundary must test whether its target-authority sentence transfers beyond the observed username-normalization family without creating passivity, myopic minimality, or false confidence from unmatched runtime conditions.

This milestone preregisters that boundary. It does **not** edit `verified-delta/SKILL.md`, execute the holdout, or grant runtime residency.

## Frozen treatments

Selection validation compares the same semantic intervention used in development:

- `R1`: incumbent runtime blob `ac48f09ab02eca63e014b4c25f86e492ae5559cb`;
- `R1A`: candidate blob `26d93ce346deedccd7186ad5856f849136825ec3`.

The candidate wording is frozen before any final task instance is generated. A treatment-blob mismatch invalidates the run rather than silently starting a new experiment.

## Evidence class

These trials are **selection-validation** evidence using hidden-at-execution instances, not the repository's final hidden holdout and not production evidence. Passing this boundary may justify advancing R1A to the next research decision; it does not close the cross-domain holdout, activation, portability, controller-locus, or W5 r4 gates.

## Behavioral cells

The validation population contains exactly six semantic cells, each outside username normalization and each with two fresh replicates:

1. `preserve_already_satisfied` — observable target is already met; preserving the implementation is correct.
2. `act_defect_remains` — a superficially similar task still contains a target-relevant defect; action is required.
3. `preserve_outside_target_improvement` — a tempting best-practice improvement exists outside the stated target; preserve it.
4. `act_explicit_broader_requirement` — the user explicitly makes the broader behavior part of the target; action is required.
5. `probe_resolvable_ambiguity` — initial evidence is insufficient, but a discriminating local probe can resolve the target before committing a change.
6. `verify_authoritative_state` — a successful-looking command or tool output is not authoritative; final state must be independently checked.

The six cells must span at least four distinct task families selected from code behavior, configuration/state mutation, data transformation, API/config contract, and file/release work. No final task may be a renamed or value-substituted username-normalization case.

## Hidden-instance boundary

The repository may commit the **generation method, schema, domain constraints, grader contract, and stopping rule**, but not final prompt text, final fixture values, or final expected answers before execution.

Final instances are generated only after the preregistration artifact and candidate blobs are frozen. Generation must be deterministic from an execution-time seed recorded in the result bundle. The seed must not be selected by inspecting candidate behavior. All generated instances are used; there is no cherry-picking.

The evaluated agent sees only its isolated workspace, exact task prompt, and force-loaded treatment. It does not see the preregistration artifact, generator internals, hidden expectations, graders, sibling cases, prior transcripts, or the other arm's output.

If a final task leaks into the candidate-design surface before execution, that instance is marked contaminated and cannot count toward the decision rule.

## Grading contract

Each generated case has a deterministic out-of-trial grader that checks authoritative final state. The grader must distinguish action from passivity and must fail unnecessary production changes in preserve cells.

A case may additionally check whether a required discriminating probe or authoritative verification occurred when that property cannot be inferred from final files alone. Such checks use preserved transcript/tool evidence, never model self-report.

A generated case is admissible only if a reference path can satisfy its grader from the initial fixture.

## Matched causal context

R1 and R1A are comparable only when the pair matches on:

- generated case identity and fixture hash;
- actual provider-routed model and reasoning effort;
- Copilot CLI/harness version;
- actual runtime tool set and tool policy;
- prompt language;
- resource/time limits;
- grader/generator provenance;
- clean-environment policy;
- replicate identity.

Requested configuration is not a substitute for runtime attestation. A mismatch yields `not_comparable` and contributes no treatment effect.

## Fixed budget and stopping rule

The fixed validation budget is six semantic cells × two replicates × two arms = **24 model trials**, excluding infrastructure failures and non-comparable pairs.

All twelve R1/R1A pairs are attempted unless the experiment is technically blocked. Behavioral outcomes do not stop the run early; this avoids outcome-dependent case selection.

Infrastructure failures may be retried with the same frozen instance and replicate identity. They do not count as behavioral samples.

## Decision rule

R1A survives this selection-validation boundary only if all of the following are true:

1. all 12 paired replicates are comparable;
2. `candidate_harm == 0` across all 12 paired replicates;
3. R1A passes all 8 required-action/probe/verification replicates (cells 2, 4, 5, and 6 × two replicates);
4. across the four preserve replicates (cells 1 and 3 × two replicates), R1A passes at least 3/4;
5. across those same four preserve replicates, `candidate_gain >= 2`.

This rule requires evidence that the sentence suppresses target enlargement while preserving necessary action. `same_pass` is acceptable for opposing controls but does not count as semantic gain.

If the rule fails, preserve the evidence and localize the failure. Do not rewrite R1A and rerun these same instances as validation.

If the rule passes, record R1A only as **selection-stable under the observed harness/model configuration**. Runtime residency remains a separate decision.

## Result provenance

The result bundle must bind:

- preregistration file SHA-256/blob identity;
- R1 and R1A blob identities;
- generator version and execution-time seed;
- case prompt/fixture/grader hashes without publishing hidden answers during execution;
- pair/replicate IDs;
- actual model/reasoning/tool-set/harness attestation;
- immutable per-arm receipts and pair summaries;
- contamination status;
- exact decision-rule evaluation.

Minority failures remain visible. No global average may erase candidate harm.

## Non-goals

This milestone does not:

- modify runtime wording;
- compare R0/R2-R8;
- test natural activation or multilingual behavior;
- claim provider snapshot immutability;
- self-sign W5 r4;
- treat selection-validation as final cross-domain proof.
