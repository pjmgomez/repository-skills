# repository-skills

A curated collection of **agent skills** — reusable capabilities for Claude/Copilot coding agents.
Each skill is self-contained under [.github/skills/](.github/skills/) and is loaded on demand when
its `description` matches the task at hand.

This repo is a skills library, not an application: there is nothing to build or run.

## Skills

| Skill | What it does |
|-------|--------------|
| [github-repo-setup](.github/skills/github-repo-setup/SKILL.md) | Scaffold and audit a repo's folder structure and community-health files. |

A skill can ship an evaluation harness beside it; see
[github-repo-setup-workspace/](.github/skills/github-repo-setup-workspace/) and its
[eval-harness instructions](.github/instructions/eval-harness.instructions.md).

## Anatomy of a skill

Each skill lives in `.github/skills/<name>/` with a required `SKILL.md` (YAML frontmatter + Markdown
instructions) and a `LICENSE.txt`, plus optional `scripts/`, `references/`, and `assets/`. See
[AGENTS.md](AGENTS.md) for the conventions and the point-of-edit checklist in
[.github/instructions/skill-authoring.instructions.md](.github/instructions/skill-authoring.instructions.md).

## Developing skills

Validate a skill's frontmatter before committing (needs `pyyaml`):

```bash
python3 .github/skills/skill-creator/scripts/quick_validate.py .github/skills/<name>
```

It checks the rules in [AGENTS.md](AGENTS.md) — allowed keys only, `name` equal to the folder, a
non-empty `description` with no angle brackets, and a `LICENSE.txt` in the folder. CI
([.github/workflows/validate-skills.yml](.github/workflows/validate-skills.yml)) runs it on every push
and pull request, and a `PostToolUse` hook
([.github/hooks/validate-skill.sh](.github/hooks/validate-skill.sh)) re-checks a `SKILL.md` after it's
edited.

Package a skill into a distributable `.skill` archive (validates first) by running as a module from
the `skill-creator` folder:

```bash
cd .github/skills/skill-creator && python3 -m scripts.package_skill ../<name>
```

Both commands live in the `skill-creator/` skill, which isn't part of every checkout. The CI workflow
and the `PostToolUse` hook both fail open when it's absent — CI skips validation with a notice, and a
`SKILL.md` edit is never blocked — but the `quick_validate.py` and `package_skill.py` commands above
only work when `.github/skills/skill-creator/` is present. When it's missing, check frontmatter by hand
against [skill-authoring.instructions.md](.github/instructions/skill-authoring.instructions.md), or run
the `/review-skill` prompt.
