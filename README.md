<div align="center">

# Verified Delta

### A 2.9 KB evidence-driven execution discipline for AI agents

**One tiny skill. One hard rule: an agent does not get to call work done until reality agrees.**

[![Release](https://img.shields.io/badge/release-v1.0.0-2ea44f?style=flat-square)](https://github.com/Nolane-x/Nolane-prompt-ms/releases/tag/v1.0.0)
[![Runtime](https://img.shields.io/badge/runtime-1%20file-111827?style=flat-square)](verified-delta/SKILL.md)
[![Words](https://img.shields.io/badge/words-446-111827?style=flat-square)](verified-delta/SKILL.md)
[![Dependencies](https://img.shields.io/badge/runtime%20dependencies-0-111827?style=flat-square)](verified-delta/SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

[**Read the runtime**](verified-delta/SKILL.md) · [**Open the research lab**](https://github.com/Nolane-x/Nolane-prompt-ms/tree/research/verified-delta-full) · [**v1.0.0 release**](https://github.com/Nolane-x/Nolane-prompt-ms/releases/tag/v1.0.0)

</div>

---

Verified Delta is a compact, model-agnostic Agent Skill for a class of failures that often appear **after** the model has already demonstrated enough raw capability to solve the task: it acts from the wrong state, widens scope, stacks patches, obeys stale context, optimizes a proxy, or declares success before reality verifies it.

It is deliberately **not** a giant prompt, an agent framework, a model router, or a library of hundreds of rules. The complete installed runtime is one file:

```text
verified-delta/
└── SKILL.md
```

**2,925 bytes. 446 words. Zero runtime dependencies.**

> **Core principle**  
> Explore as widely as uncertainty requires; commit only the smallest sufficient delta; call it done only when reality verifies it.

## Why reviewers should care

Most agent guidance grows by accumulation: another rule for every failure, another checklist, another abstraction. Verified Delta was built under the opposite pressure.

| Design choice | Why it matters |
| --- | --- |
| **One 2.9 KB runtime file** | The entire controller is inspectable; there is nowhere for hidden orchestration to hide. |
| **Zero runtime dependencies** | No service, model router, daemon, SDK, database, or research harness is required at use time. |
| **Behavioral residency rule** | New wording does not enter the runtime merely because it sounds reasonable. It must be justified by observed behavior. |
| **Fail-closed paired evidence** | Model/config drift, missing receipts, or mismatched treatment arms are rejected rather than counted as wins. |
| **Opposing controls** | A proposed repair must solve the target failure without breaking the opposite case. |
| **Candidate deletion is a success state** | R1A was frozen and rejected; R1B was never created when evidence did not justify more wording. |
| **Research and product are separated** | `main` stays tiny; the full laboratory lives on [`research/verified-delta-full`](https://github.com/Nolane-x/Nolane-prompt-ms/tree/research/verified-delta-full). |

The project optimizes **behavioral leverage per token**, not rule count.

## The failure mode

Strong agents often fail at transitions between reasoning and action:

- solving before establishing the actual current state;
- turning reported or inferred state into fact;
- optimizing a proxy instead of the user's observable target;
- continuing to obey a stale instruction after its scope has expired;
- stacking fixes without killing the previous causal explanation;
- widening a task because more work is available;
- treating compilation, HTTP 200, generated output, or self-written tests as sufficient proof;
- announcing completion before the intended property is actually true;
- continuing after the target is already verified.

Verified Delta compresses those failure modes into one execution model:

```text
current truth → material uncertainty → smallest causal delta → reality check → stop
```

Or, formally:

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

The notation is optional. **The behavior is the product.**

## The six-move controller

Verified Delta pushes an agent toward six moves:

1. **Ground** — distinguish `observed`, `reported`, `inferred`, `assumed`, and `unknown`.
2. **Lock** — preserve the user's actual objective and hard invariants.
3. **Resolve only material uncertainty** — investigate what can change the action, not everything that can be investigated.
4. **Change minimally** — prefer the smallest causal intervention that can reach the desired state.
5. **Verify reality** — test the intended property and relevant regressions with evidence proportionate to risk.
6. **Stop** — once the target is verified and the invariants still hold, stop adding work.

That last step is intentional. Verified Delta is designed to resist both **under-verification** and **performative overthinking**.

## What “strong” means here

Verified Delta is not trying to make a weak model magically know facts it does not know. Its target is narrower and practical: make an already-capable agent **harder to derail at the execution boundary**.

| Failure pressure | Desired behavioral effect |
| --- | --- |
| Scope drift | Keep the user-visible target and invariants authoritative. |
| Premature assumptions | Probe uncertainty that can change the action before committing. |
| Patch stacking | Prefer discriminating evidence over another speculative patch. |
| Unnecessary change | Avoid modifying reality that already satisfies the target. |
| False completion | Require evidence for the intended property, not a convenient proxy. |
| Stale continuation | Treat prior state as evidence to re-check, not permanent authority. |
| Endless polishing | Stop when the verified target is reached. |

This is why the runtime can stay small: it encodes a **decision discipline**, not a catalog of domain-specific answers.

---

# Evidence, not vibes

The runtime was developed as a behavioral research program. The laboratory used paired U0/U1 trials, immutable evidence, deterministic graders, opposing controls, explicit treatment identity, and fail-closed comparability checks.

Pairs with provider/model/config drift were **not** interpreted as causal wins. A result had to survive the active gate at the time it was produced.

## What the research process actually rejected

The current kernel exists partly because the project refused to protect its own previous work:

- **R1A** — a larger candidate — was frozen and rejected at its selection boundary rather than promoted because it had already cost effort.
- A comparable `u1_harm` in an earlier cleanup pressure replicate was treated as real evidence, but the runtime was **not rewritten immediately** when the harm failed to reproduce on the next comparable replicate.
- Runs whose U0/U1 runtime identity drifted were explicitly classified **not comparable**, even when the raw outcome looked favorable.
- **R1B was never created** because the final targeted matched evidence did not justify adding more instructions.

That is the central research claim of this repository: **more prompt is not automatically more control**.

## Fresh matched temporal r3

The final targeted temporal-authority pressure boundary produced fresh matched pairs. For the supersession pair, both arms attested the same resumed runtime: `gpt-5.6-luna`, reasoning effort `medium`, the same pre-treatment session fork, and the same tool surface.

| Pressure case | U0 | U1 + Verified Delta | Result |
| --- | ---: | ---: | --- |
| `temporal-supersession` | PASS | PASS | `comparable=true` · `same_pass` · 0 issues |
| `temporal-continuity-control` | PASS | PASS | `comparable=true` · `same_pass` · 0 issues |

The targeted residual temporal-authority failure **did not reproduce** under the fresh matched runtime, while the opposing continuity control also remained correct. The evidence therefore said: **keep the smaller runtime unchanged**.

In the single matched supersession replicate, U1 happened to finish with **6 tool calls / 13.2 s**, versus U0 with **13 tool calls / 28.5 s**. That is an observation from one matched replicate — **not** a claim of a general 2× speedup.

### Evidence links

- [`temporal-supersession` r3 — run 34748675736](https://github.com/Nolane-x/Nolane-prompt-ms/actions/runs/34748675736)
- [`temporal-continuity-control` r3 — run 34748676936](https://github.com/Nolane-x/Nolane-prompt-ms/actions/runs/34748676936)
- [Living full research branch](https://github.com/Nolane-x/Nolane-prompt-ms/tree/research/verified-delta-full)
- [Frozen pre-distillation archive](https://github.com/Nolane-x/Nolane-prompt-ms/tree/archive/research-final-2026-09-13)
- [v1.0.0 research-distilled release](https://github.com/Nolane-x/Nolane-prompt-ms/releases/tag/v1.0.0)

> [!IMPORTANT]
> **Proof boundary:** this is not a universal benchmark showing that Verified Delta improves every model and task. The current evidence is substantially stronger about the integrity of the research process, the rejection of unsupported expansion, and the absence of the targeted residual temporal regression in fresh matched pressure cases than it is about universal pass-rate uplift.

Broad cross-model, cross-domain, multilingual, natural-activation, and long-horizon evaluation remain appropriate future research targets.

## Why only 446 words?

Because prompt length is not intelligence.

Every extra instruction consumes context, competes for attention, can create new failure modes, and increases the surface future agents must interpret. Verified Delta therefore uses a harsher residency rule:

> **If a rule cannot earn its place through behavioral evidence, it does not get to live in the runtime.**

The result is a controller small enough to audit in minutes and cheap enough to carry into ordinary agent work.

## Install

### Codex

Ask the built-in skill installer to install the GitHub skill directory:

```text
$skill-installer install https://github.com/Nolane-x/Nolane-prompt-ms/tree/main/verified-delta
```

Restart Codex if a newly installed skill is not discovered in the current session.

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

Claude Code can discover the skill when a task matches its description, or you can invoke `/verified-delta` directly. Restart the session if a newly created skills directory is not discovered immediately.

### Other Agent Skills-compatible agents

Copy the `verified-delta` directory into the agent's skills location. `SKILL.md` is the complete runtime package; no other repository file is required at runtime.

## Research without bloating the product

The repository intentionally has two surfaces:

### `main` — distribution

Small, boring, auditable. It contains the public documentation, MIT license, and the one-file runtime.

### `research/verified-delta-full` — living laboratory

This branch is intentionally retained for future research. It contains the full research machinery: constitution, state, evaluators, fixtures, deterministic graders, tests, workflow infrastructure, candidate history, and research documentation.

Use the research branch when continuing R&D. Do **not** copy the laboratory back into runtime dependencies merely because it exists.

A frozen historical checkpoint is also preserved at `archive/research-final-2026-09-13`.

## Reviewer shortcut

If you are evaluating the project, a useful review path is:

1. Read [`verified-delta/SKILL.md`](verified-delta/SKILL.md). That is the entire runtime.
2. Read **Evidence, not vibes** above.
3. Inspect the two fresh matched r3 runs.
4. Open [`research/verified-delta-full`](https://github.com/Nolane-x/Nolane-prompt-ms/tree/research/verified-delta-full) and inspect the rejected candidate, executable eval machinery, tests, and evidence rules.
5. Compare that laboratory with `main` and notice how much was deliberately **not shipped**.

The interesting part of Verified Delta is not that it contains many rules. It is that a long research process was compressed until **almost everything else could be deleted**.

## Runtime identity

The released kernel is pinned by content identity:

```text
Git blob: ac48f09ab02eca63e014b4c25f86e492ae5559cb
SHA-256: 81f44a454bf00d61a172217864114b71e9792a4247b7f4459633f7b5deb3c5a9
Words:    446
Bytes:    2925
Deps:     0
```

## Release

**v1.0.0 — Research-Distilled Release** is published on GitHub and points to a clean distribution snapshot containing only `README.md`, `LICENSE`, and `verified-delta/`.

[Read the v1.0.0 release notes →](https://github.com/Nolane-x/Nolane-prompt-ms/releases/tag/v1.0.0)

## License

MIT © 2026 Nolane-x. See [`LICENSE`](LICENSE).
