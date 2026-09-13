# Verified Delta

A tiny, model-agnostic Agent Skill for reliable task execution.

**Verified Delta** treats work as a transition from current truth to desired truth: establish reality, preserve hard constraints, resolve only uncertainty that can change the action, make the smallest sufficient change, verify the intended result, then stop.

The distributed product is intentionally one file:

```text
verified-delta/
└── SKILL.md
```

No runtime dependencies. No scripts. No model routing. No test or research payload is installed with the skill.

## Install

### Codex

Ask Codex to install the skill from this repository:

```text
$skill-installer install https://github.com/Nolane-x/Nolane-prompt-ms/tree/main/verified-delta
```

Then restart Codex so the installed skill is discovered.

### Claude Code — personal

Make the skill available across your projects:

```bash
mkdir -p ~/.claude/skills/verified-delta
cp verified-delta/SKILL.md ~/.claude/skills/verified-delta/SKILL.md
```

### Claude Code — project

Install it only for the current project:

```bash
mkdir -p .claude/skills/verified-delta
cp verified-delta/SKILL.md .claude/skills/verified-delta/SKILL.md
```

Claude Code can then load it automatically when the task matches its description, or you can invoke `/verified-delta` directly.

### Other Agent Skills-compatible agents

Install the `verified-delta` directory in the agent's skills location. `SKILL.md` is the complete package; no other repository file is required at runtime.

## What it is for

Use Verified Delta when work can fail through scope drift, premature assumptions, unnecessary change, false completion, or stale continuation state. It is designed to improve execution discipline without turning ordinary work into a heavyweight checklist.

## Evidence boundary

The runtime was developed against behavioral pressure cases and deliberately rejects unevidenced expansion. This release does **not** claim that the skill is universally optimal, behaviorally proven across every model, or a replacement for deterministic validation where deterministic enforcement is possible.

The complete pre-distillation research tree remains preserved in Git history on `archive/research-final-2026-09-13`.
