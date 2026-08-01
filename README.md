# repository-skills

A curated collection of **agent skills** — reusable capabilities for Claude/Copilot coding agents.
Each skill is self-contained under [.github/skills/](.github/skills/) and is loaded on demand when
its `description` matches the task at hand.

This repo is a skills library, not an application: there is nothing to build or run.

## Skills

| Skill | What it does |
|-------|--------------|
| [github-repo-setup](.github/skills/github-repo-setup/SKILL.md) | Scaffold and audit a repo's folder structure and community-health files. |
| [readme-authoring](.github/skills/readme-authoring/SKILL.md) | Author or improve a repository's README so it works as a clear landing page. |

Each skill can ship an evaluation harness beside it in a `<name>-workspace/` folder — both here do
([github-repo-setup-workspace/](.github/skills/github-repo-setup-workspace/),
[readme-authoring-workspace/](.github/skills/readme-authoring-workspace/)); see the
[eval-harness instructions](.github/instructions/eval-harness.instructions.md).

## Getting started

You don't install these skills directly — an AI coding agent loads one automatically when a request
matches its `description`. Asking an agent to "set up my repo" pulls in
[github-repo-setup](.github/skills/github-repo-setup/SKILL.md); "write me a README" pulls in
[readme-authoring](.github/skills/readme-authoring/SKILL.md). To use a skill in another project,
package it (see [Developing skills](#developing-skills)) and place the resulting `.skill` where your
agent discovers skills.

## Usage

Work on the skills through the repo's slash-command prompts (in [.github/prompts/](.github/prompts/)):

- `/create-skill` — scaffold a new skill folder (`SKILL.md` + `LICENSE.txt`).
- `/review-skill` — audit an existing `SKILL.md` against the conventions (read-only).
- `/create-eval` — scaffold a skill's `<name>-workspace/` A/B evaluation harness.
- `/run-skill-evals` — run and grade that harness.

For example, `/create-skill pdf-export: turn a Markdown file into a PDF` produces a
conventions-compliant starting point you then flesh out.

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

## Contributing

Conventions live in [AGENTS.md](AGENTS.md), with the point-of-edit checklist in
[skill-authoring.instructions.md](.github/instructions/skill-authoring.instructions.md). Keep each
change scoped to one skill folder, validate before committing, and use `/review-skill` to self-check;
CI ([.github/workflows/validate-skills.yml](.github/workflows/validate-skills.yml)) runs the validator
on every push and pull request.

## License

[Apache License 2.0](LICENSE). Each skill also ships its own `LICENSE.txt`.
