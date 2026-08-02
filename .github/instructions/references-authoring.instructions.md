---
description: "Use when creating or editing an on-demand reference doc under a skill's references/ folder (.github/skills/<name>/references/). Covers what belongs there versus in SKILL.md, one-topic-per-file, and linking every doc from SKILL.md."
applyTo: ".github/skills/**/references/**"
---
# Authoring a skill's `references/` docs

Repo-wide context is in [AGENTS.md](../../AGENTS.md); frontmatter rules for the parent skill are in
[skill-authoring.instructions.md](./skill-authoring.instructions.md). A `references/` folder holds
detail an agent loads **on demand**, so `SKILL.md` stays short (progressive disclosure).

## What belongs here

- Long or rarely-needed detail that would bloat `SKILL.md`: full option tables, edge cases, worked
  examples, background.
- Move such detail here to keep `SKILL.md` itself under ~500 lines.

## Rules

- One topic per file; name the file after that topic (kebab-case `.md`).
- Every reference doc must be linked from `SKILL.md` (or another reference) with a relative path
  (`./references/<file>.md`). An unlinked doc is dead weight — `/review-skill` flags it.
- Write imperative, reference-style prose; do not repeat what `SKILL.md` already says.
- No frontmatter is required on a reference doc; it is plain Markdown.
