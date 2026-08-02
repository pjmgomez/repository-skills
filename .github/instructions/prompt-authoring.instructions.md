---
description: "Use when creating or editing a repo prompt under .github/prompts/ (a *.prompt.md slash command). Covers the frontmatter keys and their order, the description trigger style, and the shared body shape the four shipped prompts follow."
applyTo: ".github/prompts/**"
---
# Authoring a prompt (`.github/prompts/*.prompt.md`)

Repo-wide context is in [AGENTS.md](../../AGENTS.md). The four shipped prompts —
[create-skill](../prompts/create-skill.prompt.md), [review-skill](../prompts/review-skill.prompt.md),
[create-eval](../prompts/create-eval.prompt.md), and
[run-skill-evals](../prompts/run-skill-evals.prompt.md) — are the models to copy. This file is the
point-of-edit checklist.

## Frontmatter (YAML between `---`)

Use these keys, in this order:

- `description`: required; single-quoted. Write it as the trigger surface — capability first, then
  `Use when…` with concrete verbs, then `Do NOT use for…` exclusions that point to the sibling prompt
  which owns that case. Angle brackets are allowed here (unlike a `SKILL.md`).
- `name`: Title Case, single-quoted (e.g. `'Create Skill'`).
- `argument-hint`: single-quoted; one line naming the expected argument. May contain angle brackets
  (e.g. `'<kebab-name>: <one-line purpose>'`).
- `agent`: `'agent'`.

Inside a single-quoted YAML value, escape an apostrophe by doubling it (`''`).

## Body

- Open with one paragraph: what the prompt does, linking [AGENTS.md](../../AGENTS.md), the relevant
  `*.instructions.md`, and a worked example to copy.
- Read the argument next; if it is missing or unclear, ask before creating anything.
- Give a numbered `## Steps` section for a workflow, or a `## Checklist` for a read-only audit. Keep
  each step imperative.
- Cross-link with relative Markdown links (`../skills/…`, `../instructions/…`).
- End with a scope boundary that says what the prompt must not touch; a read-only prompt must state
  that it changes no files.
