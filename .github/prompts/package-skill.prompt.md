---
description: 'Package a skill into a distributable .skill archive (the skill folder zipped, minus evals/) using package_skill.py, which validates first and refuses to package on failure. Use when the user wants to package, bundle, zip, or produce a shareable .skill file for a skill. Do NOT use to create, edit, review, or evaluate a skill (see /create-skill, /review-skill, /create-eval, /run-skill-evals).'
name: 'Package Skill'
argument-hint: 'skill name to package'
agent: 'agent'
---

Package one skill under `.github/skills/` into a distributable `<name>.skill` archive, following the
packaging notes in [AGENTS.md](../../AGENTS.md). The packager
([package_skill.py](../skills/skill-creator/scripts/package_skill.py)) validates the skill first and
refuses to package on failure.

Read the skill name from the argument (see the argument hint). If it is missing or unclear, ask which
skill to package before doing anything.

## Steps

1. **Check the packager is present.** It lives in the `skill-creator/` skill, which is not in every
   checkout. If `.github/skills/skill-creator/scripts/package_skill.py` does not exist, stop and tell
   the user to add the `skill-creator/` skill — do not hand-roll an archive.
2. **Confirm the target.** Ensure `.github/skills/<name>/` exists and contains a `SKILL.md`.
3. **Package** by running the module from the `skill-creator` folder (needs `pyyaml`):
   `cd .github/skills/skill-creator && python3 -m scripts.package_skill ../<name> [output-dir]`. It
   validates the frontmatter, then zips the skill folder minus `evals/`. If validation fails it
   refuses to package — fix the reported issues (see [/review-skill](./review-skill.prompt.md)) and
   re-run.
4. **Report** the produced `<name>.skill` archive and where it was written.

Do not modify the skill's files while packaging; this prompt only builds the archive.
