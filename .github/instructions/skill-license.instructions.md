---
description: "Use when adding, editing, or removing a skill's LICENSE.txt under .github/skills/<name>/. Covers the per-skill license rule, copying the existing Apache-2.0 text, and the matching SKILL.md license field."
applyTo: ".github/skills/**/LICENSE.txt"
---
# A skill's `LICENSE.txt`

Repo-wide context is in [AGENTS.md](../../AGENTS.md). Every skill ships its **own** `LICENSE.txt` so a
skill folder can be copied into another repository unchanged.

## Rules

- Every skill folder must contain a `LICENSE.txt`; keep it when adding or copying a skill, and do not
  delete it.
- Use the repo's license — Apache License 2.0, matching the root [LICENSE](../../LICENSE). Copy an
  existing skill's file (e.g. [github-repo-setup/LICENSE.txt](../skills/github-repo-setup/LICENSE.txt))
  rather than writing new text, so the terms stay identical across skills.
- Keep the matching `SKILL.md` frontmatter field `license: Complete terms in LICENSE.txt` (see
  [skill-authoring.instructions.md](./skill-authoring.instructions.md)).
