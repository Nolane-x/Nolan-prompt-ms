# Verified Delta

> **One tiny skill. One hard rule: an agent does not get to call work done until reality agrees.**

**446 words · ~2.9 KB · 1 runtime file · 0 runtime dependencies**

Verified Delta is a compact, model-agnostic Agent Skill for a failure mode that keeps showing up in agentic work: the model is capable enough to act, but acts from the wrong state, widens scope, stacks patches, obeys stale context, or declares success before reality verifies it.

It is deliberately **not** a giant prompt, an agent framework, a model router, or a bag of hundreds of rules. It is a small behavioral controller distilled around one idea:

> Explore as widely as uncertainty requires; commit only the smallest sufficient delta; call it done only when reality verifies it.

The complete distributed runtime is:

```text
verified-delta/
└── SKILL.md
```

No scripts. No services. No model-specific API. No research harness installed with the skill.

---

## Why this exists

Strong agents often fail at the transitions between reasoning and action:

- solving before establishing the actual current state;
- optimizing a proxy instead of the user's real target;
- treating old notes, prior turns, or previous assumptions as authority;
- stacking fixes without proving the previous explanation;
- changing more than the verified target requires;
- treating compilation, HTTP 200, generated output, or the agent's own confidence as proof;
- continuing after the target is already verified.

Verified Delta turns those failure modes into a compact execution discipline.

It represents work as:

```text
⟨S0, S*, I, U, Δ, V⟩
```

| Symbol | Meaning |
| --- | --- |
| `S0` | current state supported by evidence |
| `S*` | desired observable state |
| `I` | invariants that must remain true |
| `U` | unknowns that could change the action |
| `Δ` | smallest sufficient change |
| `V` | evidence that proves `S*` and preserves `I` |

The notation is optional. The behavior is the product.

## What it changes in an agent

Verified Delta pushes the agent toward six moves:

1. **Ground** — separate what is observed, reported, inferred, assumed, and unknown.
2. **Lock** — preserve the actual objective and hard invariants.
3. **Resolve only material uncertainty** — investigate what can change the action, not everything that can be investigated.
4. **Change minimally** — make the smallest causal intervention that can reach the target.
5. **Verify reality** — test the intended property and relevant regressions with evidence proportionate to risk.
6. **Stop** — once the target is verified and invariants still hold, stop adding work.

That last step matters. Verified Delta is designed to resist both **under-verification** and **performative overthinking**.

---

## Evidence, not vibes

This project was developed as a behavioral research program, not by adding prompt rules until the prose sounded impressive.

The research harness used paired U0/U1 trials with a shared pre-treatment session fork, immutable session-state hashes, post-resume runtime attestation, deterministic workspace graders, opposing controls, and fail-closed comparison. Pairs with model/config drift were excluded rather than interpreted as wins.

The current runtime is the result of a **retain / reject / delete** process:

- a larger candidate, **R1A**, was frozen and rejected rather than protected because effort had already been spent on it;
- an observed comparable `u1_harm` in an earlier cleanup pressure case was taken seriously, then **not promoted into a rewrite** when the harm failed to reproduce on the next comparable replicate;
- provider-drift runs that looked favorable were explicitly marked **not comparable** instead of being used as evidence;
- a proposed **R1B was never created** because fresh targeted matched evidence did not justify adding more runtime wording.

That restraint is part of the design. The target is not “more instructions.” The target is **behavioral leverage per token**.

### Fresh matched temporal r3

The final targeted temporal-authority pressure run used the same resumed runtime on both arms: `gpt-5.6-luna`, reasoning effort `medium`, the same pre-treatment session fork, and the same attested tool set.

| Pressure case | U0 | U1 + Verified Delta | Pair result |
| --- | ---: | ---: | --- |
| `temporal-supersession` | PASS | PASS | `comparable=true`, `same_pass`, 0 issues |
| `temporal-continuity-control` | PASS | PASS | `comparable=true`, `same_pass`, 0 issues |

In the supersession replicate, U1 happened to complete with **6 tool calls / 13.2 s** versus U0 with **13 tool calls / 28.5 s**. That is an observed result from one matched replicate, **not a claim of a general 2× speedup**.

The important confirmatory result is narrower and stronger: the targeted residual temporal-authority failure did **not** reproduce under a fresh matched runtime, while the opposing continuity control also remained correct. The evidence therefore said **keep the smaller runtime unchanged**.

Evidence runs:

- [`temporal-supersession` r3 — run 34748675736](https://github.com/Nolane-x/Nolane-prompt-ms/actions/runs/34748675736)
- [`temporal-continuity-control` r3 — run 34748676936](https://github.com/Nolane-x/Nolane-prompt-ms/actions/runs/34748676936)
- [Frozen pre-distillation research tree](https://github.com/Nolane-x/Nolane-prompt-ms/tree/archive/research-final-2026-09-13)

### What this does **not** prove

Verified Delta does **not** claim universal optimality, universal benchmark gains, or guaranteed improvement on every model and task. Two targeted matched pressure cases are not a universal benchmark.

It also does not claim that the one observed tool/time reduction generalizes. Broad cross-model, cross-domain, multilingual, natural-activation, and long-horizon evaluation would be required for claims at that level.

This repo intentionally makes the evidence boundary visible rather than hiding it behind marketing language.

---

## Why only 446 words?

Because prompt length is not intelligence.

Every extra instruction consumes context, competes for attention, can create new failure modes, and increases the surface that future agents must interpret. Verified Delta therefore follows a harsher residency rule:

> **If a rule cannot earn its place through behavioral evidence, it does not get to live in the runtime.**

The current `SKILL.md` is a single-file kernel with zero runtime dependencies. Its Git blob is intentionally kept stable after the matched behavioral closure.

## When to use it

Use Verified Delta when a task can fail through:

- scope drift;
- stale continuation state;
- premature assumptions;
- unnecessary edits or refactors;
- false completion;
- weak causal debugging;
- verification by proxy instead of verification of the intended property;
- agents that keep working after the actual target is already satisfied.

It is especially useful for coding agents, repository maintenance, debugging, multi-step implementation, migration work, and tasks where “almost correct” state tracking creates expensive downstream errors.

## Install

### Codex

Ask the built-in skill installer to install this GitHub skill directory:

```text
$skill-installer install https://github.com/Nolane-x/Nolane-prompt-ms/tree/main/verified-delta
```

Restart Codex if the new skill is not discovered in the current session.

### Claude Code — personal

```bash
mkdir -p ~/.claude/skills/verified-delta
curl -fsSL https://raw.githubusercontent.com/Nolane-x/Nolane-prompt-ms/main/verified-delta/SKILL.md \
  -o ~/.claude/skills/verified-delta/SKILL.md
```

### Claude Code — project

```bash
mkdir -p .claude/skills/verified-delta
curl -fsSL https://raw.githubusercontent.com/Nolane-x/Nolane-prompt-ms/main/verified-delta/SKILL.md \
  -o .claude/skills/verified-delta/SKILL.md
```

Claude Code can discover the skill when the task matches its description, or you can invoke `/verified-delta` directly. Restart the session if a newly created skills directory is not discovered immediately.

### Other Agent Skills-compatible agents

Copy the `verified-delta` directory into the agent's skills location. `SKILL.md` is the complete runtime package; no other repository file is required.

## Reviewer shortcut

If you are evaluating this project, the fastest path is:

1. Read [`verified-delta/SKILL.md`](verified-delta/SKILL.md) — the entire runtime fits on one screenful of focused prose.
2. Read the **Evidence, not vibes** section above.
3. Inspect the two fresh matched r3 runs and their pair summaries.
4. Inspect the frozen research branch to see the rejected candidates, tests, immutable receipts, and research constraints that were intentionally removed from the production distribution.

The interesting part of Verified Delta is not that it contains many rules. It is that a long research process was distilled down until **almost everything else could be deleted**.

## Runtime identity

Current release kernel:

```text
Git blob: ac48f09ab02eca63e014b4c25f86e492ae5559cb
SHA-256: 81f44a454bf00d61a172217864114b71e9792a4247b7f4459633f7b5deb3c5a9
Words:    446
Bytes:    2925
```

## License

MIT. See [`LICENSE`](LICENSE).
