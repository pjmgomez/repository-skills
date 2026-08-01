---
description: "Use when creating or editing a skill's SKILL.md under .github/skills/. Covers the allowed frontmatter fields, the name/description rules, the description trigger-writing style, and how to validate."
applyTo: ".github/skills/**/SKILL.md"
---
# Authoring a SKILL.md

Repo-wide context is in [AGENTS.md](../../AGENTS.md); [github-repo-setup](../skills/github-repo-setup/SKILL.md)
is the worked example. This file is the point-of-edit checklist.

## Frontmatter (YAML between `---`)

Only these keys are allowed (any other key is rejected):
`name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`.

- `name`: required; kebab-case (`^[a-z0-9-]+$`); ≤64 chars; **must equal the folder name**.
- `description`: required; ≤1024 chars; **no angle brackets** (`<` or `>`). Quote the value if it contains a colon.
- `license`: keep the convention `Complete terms in LICENSE.txt` and ship a `LICENSE.txt` in the folder.

## Write `description` as the trigger surface

An agent decides whether to load the skill from its `description` alone, so pack the triggers in.
House style: capability first, then `Use when…` with concrete keywords/file extensions/scenarios,
then `Do NOT use for…` exclusions. [github-repo-setup](../skills/github-repo-setup/SKILL.md) is the
model to copy.

## Body

- Keep it under ~500 lines; move long detail into a `references/` folder and link to it (progressive disclosure).
- Prefer imperative instructions.

## Before committing

Validate this skill (needs `pyyaml`):
`python3 .github/skills/skill-creator/scripts/quick_validate.py .github/skills/<name>`

CI and the `PostToolUse` hook run the same check automatically — CI on every push and pull request,
the hook right after a `SKILL.md` edit.
