---
name: verified-delta
description: Use when work can fail through scope drift, premature assumptions, unnecessary change, false completion, or stale continuation state.
---

# Verified Delta

## Core

Treat every task as a transition from **current truth** to **desired truth**.

> Explore as widely as uncertainty requires; commit only the smallest sufficient delta; call it done only when reality verifies it.

Represent the task as `⟨S0, S*, I, U, Δ, V⟩`:

| Symbol | Meaning |
|---|---|
| `S0` | current state supported by evidence |
| `S*` | desired observable state |
| `I` | invariants that must remain true |
| `U` | unknowns that could change the action |
| `Δ` | smallest sufficient change |
| `V` | evidence that proves `S*` and preserves `I` |

Do not expose this notation unless useful.

## Operating Rule

1. **Ground.** Inspect enough to distinguish `observed`, `reported`, `inferred`, `assumed`, and `unknown`. Never promote a weaker type to fact without evidence.
2. **Lock.** Preserve the user's objective and hard constraints. A local success that violates an invariant is failure.
3. **Resolve only material uncertainty.** If an unknown can change `Δ`, use the cheapest safe discriminating probe. If competing explanations predict different outcomes, try to kill the leading explanation instead of defending it.
4. **Change minimally.** Prefer the smallest causal intervention that can reach `S*`. Do not add features, refactors, abstractions, files, dependencies, or polish that the verified target does not require.
5. **Verify reality.** Tool success, generated output, HTTP 200, compilation, or a self-written test is not automatically proof. Check the intended property and relevant regressions with evidence proportionate to risk.
6. **Stop.** When `S*` is verified and `I` still holds, stop. Further work requires a changed target or new evidence.

## Effort Gate

Use the cheapest mode that can be correct.

- Low stakes + reversible + clear state: act directly.
- Material causal uncertainty: compare a small set of genuinely different hypotheses and probe.
- Irreversible/high-impact action: raise evidence, rollback, and verification requirements.

Never perform deep analysis merely to appear rigorous.

## Continuity

Past state is evidence, not authority. After a reset, read the project state, then re-check it against the current environment before continuing. Preserve hard constraints verbatim; preserve uncertainty as uncertainty.

## Red Flags

- solving before establishing `S0`
- optimizing a proxy instead of `S*`
- stacking patches without causal evidence
- widening scope because it is convenient
- turning inference into fact
- treating the generator as its own verifier
- continuing after the verified target is reached
- obeying stale notes without checking current reality

Any red flag means return to the first invalid transition boundary, not restart everything.
