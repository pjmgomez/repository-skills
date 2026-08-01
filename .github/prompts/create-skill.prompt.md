---
description: 'Scaffold a new agent skill in this repository: create the skill folder with a conventions-compliant SKILL.md and a LICENSE.txt. Use when the user wants to add, create, bootstrap, or scaffold a new skill, or start a new SKILL.md. Do NOT use to edit an existing skill, or to review, validate, or package one.'
name: 'Create Skill'
argument-hint: '<kebab-name>: <one-line purpose>'
agent: 'agent'
---

Scaffold a new skill under `.github/skills/`, following the repo conventions in
[AGENTS.md](../../AGENTS.md) and the point-of-edit checklist in
[skill-authoring.instructions.md](../instructions/skill-authoring.instructions.md). Use
[github-repo-setup/SKILL.md](../skills/github-repo-setup/SKILL.md) as the model to copy.

Read the kebab-case skill name and one-line purpose from the invocation argument (see the argument
hint). If either is missing or unclear, ask for both before creating anything.

## Steps

1. **Derive and validate the name.** Convert to kebab-case and confirm it matches `^[a-z0-9-]+$`, is
   64 characters or fewer, and is not already taken under `.github/skills/`. The folder name and the
   `name` frontmatter field must be identical.
2. **Create the folder** `.github/skills/<name>/`.
3. **Write `SKILL.md`** using only the allowed frontmatter keys — `name`, `description`, `license`,
   and optionally `allowed-tools`, `metadata`, `compatibility`:
   - `name`: the kebab-case name (equal to the folder).
   - `description`: write it as the trigger surface — capability first, then `Use when…` with
     concrete keywords and scenarios, then `Do NOT use for…` exclusions. Keep it 1024 characters or
     fewer with **no angle brackets**; quote the value if it contains a colon.
   - `license: Complete terms in LICENSE.txt`.

   Then add a Markdown body: a one-paragraph summary, a **When to use** section, a numbered
   **Procedure**, and (only if needed) pointers to `scripts/`, `references/`, or `assets/`. Keep the
   body under ~500 lines and move long detail into a `references/` folder.
4. **Add `LICENSE.txt`** by copying
   [github-repo-setup/LICENSE.txt](../skills/github-repo-setup/LICENSE.txt) into the new folder, so
   the skill ships its own license.
5. **Validate.** The `PostToolUse` hook re-checks the `SKILL.md` automatically after you write it. If
   `.github/skills/skill-creator/scripts/quick_validate.py` exists, also run
   `python3 .github/skills/skill-creator/scripts/quick_validate.py .github/skills/<name>` (needs
   `pyyaml`) and fix anything it flags.
6. **Summarize** the files created, and remind the user to flesh out the body and sharpen the
   `description` triggers.

Create only the new skill's files. Do not modify other skills, and do not start implementing the
skill's own behavior.
