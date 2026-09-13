# One-Skill Final Distillation Design

## Goal

Turn Nolane Prompt MS from an active research laboratory into the smallest practical distribution repository that ships exactly one model-agnostic Agent Skill while preserving research provenance in Git history.

## Runtime invariant

The distributed product is one skill only: `verified-delta/SKILL.md`. It must remain model-agnostic, dependency-free, and operationally focused on moving from current truth to desired truth with the smallest sufficient verified change. No model catalog, prompt-template library, framework router, test harness, evaluator, research state, or historical artifact belongs in the shipped runtime.

## Reference comparison

`nidhinjs/prompt-master` is useful as a packaging and activation reference, especially its explicit activation description and task/constraints/done contract. Its large tool/model routing tables and reference library are intentionally not adopted. Nolane Prompt MS should compress those durable ideas into the existing universal controller rather than accumulate model-specific branches.

## Terminal research boundary

Research ends when the current temporal-authority hypothesis is resolved as far as the existing evidence protocol can justify without inventing new research directions.

1. Run the already-designed opposing pressure pair:
   - `temporal-supersession`
   - `temporal-continuity-control`
2. Admit behavioral evidence only when U0/U1 receipts are comparable under the existing matched-runtime gate.
3. Do not create R1B from infrastructure failures, non-comparable arms, or a one-off failure that does not survive the opposing-control boundary.
4. If a reproducible R1-specific temporal failure is demonstrated, create the smallest semantic candidate that distinguishes expired prior-turn constraints from explicitly still-active constraints, then require matched opposing development evidence and ablation before residency.
5. If no candidate earns residency, retain R1. Lack of evidence for a replacement is not proof of R1, but it is a valid reason not to enlarge the runtime.
6. Do not open unrelated new research programs once this boundary is resolved. Existing open research debts become archived provenance rather than shipment blockers.

## Operational repair boundary

The temporary one-shot launcher failed only because `execution-recovery-development.yml` did not expose the two new temporal case choices. The temporary enabler proved the exact two-line patch with the full unit suite and verifier, but GitHub Actions could not push a workflow-file edit because its token lacked workflow permission. Apply the same exact two-choice patch through the authenticated repository connector, preserving all behavioral semantics.

## Freeze and provenance

Before production purge, preserve a named Git ref/branch at the final research head when possible. Regardless, deleted research files remain recoverable from Git history. Do not rewrite or squash away the research history as part of this distillation.

## Production tree

The desired root is intentionally tiny:

```text
README.md
verified-delta/
  SKILL.md
```

A license may remain only if already present and legally necessary; otherwise no extra runtime/support file is introduced merely for organization. Production must contain no `tests/`, `evals/`, research Python scripts, research docs, state files, experimental workflows, temporary launchers, temporary enablers, or superpowers planning/spec files.

## Installation contract

The README must explain installation without introducing runtime code duplication:

- Claude Code project-local: copy or clone `verified-delta` into `.claude/skills/verified-delta/`.
- Claude Code user-level: copy or clone into `~/.claude/skills/verified-delta/`.
- Codex/Agent Skills: install the `verified-delta` directory through the supported skill installer or place the skill directory in the user's/project's Agent Skills location where supported.
- Generic Agent Skills-compatible agents: install the directory as one skill package containing `SKILL.md`.

The README must not promise support for a product surface unless the installation form is known to accept Agent Skills. Durable filesystem/manual-copy instructions are preferred over brittle model- or UI-specific claims.

## Final optimization rule

Do not shorten or rewrite runtime wording merely to make the file smaller. A runtime semantic change requires evidence earned before the research boundary closes. Production optimization after freeze is structural: remove non-runtime files, sharpen install documentation, and preserve the exact winning skill bytes unless evidence authorizes a candidate replacement.

## Completion criteria

The final repository is complete when:

- exactly one runtime skill package remains;
- no research/test/eval infrastructure remains on production `main`;
- README installation paths are clear for Claude Code and Codex-compatible Agent Skills usage;
- the final skill has valid frontmatter and no runtime dependency;
- research provenance remains reachable from Git history or a named archive branch/ref;
- no claim says the skill is proven, best, or universally validated beyond the evidence actually obtained.
