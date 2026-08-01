---
description: 'Audit an existing SKILL.md against the repository conventions and report pass or fail with concrete fixes, without changing files. Use when the user wants to review, audit, lint, or check a skill or SKILL.md, or verify one before committing. Do NOT use to create a new skill or to run evals.'
name: 'Review Skill'
argument-hint: 'path to a skill folder or SKILL.md'
agent: 'agent'
---

Review a skill for compliance with the repo conventions in [AGENTS.md](../../AGENTS.md) and
[skill-authoring.instructions.md](../instructions/skill-authoring.instructions.md). This is a
**read-only audit**: report findings and fixes, but do not modify any files.

Target the skill folder or `SKILL.md` given in the argument. If none is provided, ask which skill to
review, or infer it from the current context.

## Checklist

Report each item as pass or fail, and for every failure give the specific fix.

**Frontmatter**
- Only the allowed keys are present: `name`, `description`, `license`, `allowed-tools`, `metadata`,
  `compatibility`. Any other key fails.
- `name` is kebab-case (`^[a-z0-9-]+$`), 64 characters or fewer, and **equals the folder name**.
- `description` is present, 1024 characters or fewer, contains **no angle brackets**, and is quoted
  when it contains a colon.
- `license` is present (convention: `Complete terms in LICENSE.txt`).

**Files**
- `LICENSE.txt` exists in the skill folder.
- Any `scripts/`, `references/`, or `assets/` referenced by `SKILL.md` exist, and are referenced with
  relative paths (`./…`).

**Description quality (house style)**
- Reads capability first, then `Use when…` with concrete triggers, then `Do NOT use for…`
  exclusions. Flag vague, trigger-less descriptions.

**Body**
- Under ~500 lines, with long detail pushed into `references/` rather than inline.
- Imperative, step-oriented instructions.

## Output

1. A one-line verdict (pass, or fails with N issues).
2. A checklist table of each item marked pass or fail.
3. An ordered list of concrete fixes for the failures.
4. If `.github/skills/skill-creator/scripts/quick_validate.py` exists, note that
   `python3 .github/skills/skill-creator/scripts/quick_validate.py <skill-dir>` runs the automated
   subset of these checks.

Do not edit files; produce the report only.
