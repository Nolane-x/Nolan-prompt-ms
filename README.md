# Verified Delta

A tiny, model-agnostic Agent Skill for reliable task execution.

**Verified Delta** moves work from current truth to desired truth: establish reality, preserve hard constraints, resolve only uncertainty that can change the action, make the smallest sufficient change, verify the intended result, then stop.

The distributed product is one runtime file:

```text
verified-delta/
└── SKILL.md
```

No runtime dependencies. No scripts. No model routing. No test or research payload is installed with the skill.

## Install

### Codex

In Codex, ask the built-in installer to install this GitHub skill directory:

```text
$skill-installer install https://github.com/Nolane-x/Nolane-prompt-ms/tree/main/verified-delta
```

Restart Codex after installation if the new skill is not yet discovered.

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

Claude Code can load the skill automatically when the task matches its description, or you can invoke `/verified-delta` directly. If you create a top-level skills directory during an already-running Claude Code session, restart that session so it is discovered.

### Other Agent Skills-compatible agents

Install the `verified-delta` directory in the agent's skills location. `SKILL.md` is the complete package; no other repository file is required at runtime.

## Use it for

Scope drift, premature assumptions, unnecessary change, false completion, stale continuation state, and other tasks where the agent must distinguish actual state from assumed state before acting.

## Evidence boundary

The runtime was developed against behavioral pressure cases and deliberately rejects unevidenced expansion. This release does **not** claim universal optimality or validation across every model, and it does not replace deterministic validation where deterministic enforcement is possible.

The complete pre-distillation research tree is preserved in Git history at `archive/research-final-2026-09-13`.
