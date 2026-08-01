# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this repo is

A curated collection of **agent skills** (reusable Claude/Copilot capabilities). It is not an
application — there is no app to build or run. Each skill lives in its own folder under
`.github/skills/<name>/` and is self-contained. The unit of work is a **single skill**, so scope
changes to one skill folder unless asked otherwise.

This checkout currently contains a single skill — [github-repo-setup](.github/skills/github-repo-setup/SKILL.md) —
alongside its evaluation workspace, [github-repo-setup-workspace/](.github/skills/github-repo-setup-workspace/).
Use that skill's `SKILL.md` as the worked example of the conventions below; the point-of-edit
checklist for frontmatter is [.github/instructions/skill-authoring.instructions.md](.github/instructions/skill-authoring.instructions.md).

## Skill anatomy

```
.github/skills/<name>/
├── SKILL.md        # required: YAML frontmatter + Markdown instructions
├── LICENSE.txt     # required: per-skill license
├── scripts/        # optional: executable helpers
├── references/     # optional: docs loaded on demand (large detail lives here)
├── assets/         # optional: templates, fonts, icons used in output
└── examples/ | templates/ | evals/   # optional, skill-specific
```

## SKILL.md frontmatter rules

Frontmatter is YAML between `---` markers. These rules are the source of truth. Only these keys are
allowed:

`name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`

- `name` (required): kebab-case (`^[a-z0-9-]+$`), ≤64 chars, and **must equal the folder name**.
- `description` (required): ≤1024 chars, **no angle brackets** (`<` or `>`).
- `compatibility` (optional): string ≤500 chars.
- `license` (convention): `Complete terms in LICENSE.txt` (or `Proprietary. LICENSE.txt has complete terms`).

## The `description` field is the trigger surface

An agent decides whether to load a skill from its `description` alone, so put every "when to use"
signal there. Follow the house style: state the capability, then `Use when…` with concrete triggers
(keywords, file extensions, scenarios), then `Do NOT use for…` exclusions.
[github-repo-setup](.github/skills/github-repo-setup/SKILL.md) is the model in this repo — its
`description` does exactly this.

## Validating and packaging a skill

The frontmatter rules above are enforced by
[quick_validate.py](.github/skills/skill-creator/scripts/quick_validate.py) (needs `pyyaml`). Run it
before committing:

`python3 .github/skills/skill-creator/scripts/quick_validate.py .github/skills/<name>`

CI ([.github/workflows/validate-skills.yml](.github/workflows/validate-skills.yml)) runs it over
every skill on push and pull request, and a `PostToolUse` hook
([.github/hooks/validate-skill.sh](.github/hooks/validate-skill.sh)) re-checks a `SKILL.md` right
after it's edited (the hook fails open if `pyyaml` is missing).

To produce a distributable `<name>.skill` archive (a zip of the skill folder, minus `evals/`), run
[package_skill.py](.github/skills/skill-creator/scripts/package_skill.py) as a module from the
`skill-creator` folder — it validates first and refuses to package on failure:

`cd .github/skills/skill-creator && python3 -m scripts.package_skill ../<name> [output-dir]`

These validator and packager scripts live in the `skill-creator/` skill, which isn't part of every
checkout. The hook fails open when it's absent (so a `SKILL.md` edit is never blocked), but the
`quick_validate.py` and `package_skill.py` commands above only work when
`.github/skills/skill-creator/` is present. When it's missing, check frontmatter by hand against
[skill-authoring.instructions.md](.github/instructions/skill-authoring.instructions.md), or run the
`/review-skill` prompt.

## Helper prompts

Three repo prompts (in [.github/prompts/](.github/prompts/)) speed up skill work:

- `/create-skill` — scaffold a new `.github/skills/<name>/` (SKILL.md + `LICENSE.txt`) that follows
  the rules above.
- `/review-skill` — audit an existing `SKILL.md` against those rules and report fixes (read-only).
- `/run-skill-evals` — run a skill's `*-workspace/` A/B eval harness and grade it with `grade.py`
  (see [.github/instructions/eval-harness.instructions.md](.github/instructions/eval-harness.instructions.md)).

## Conventions and gotchas

- Keep `SKILL.md` under ~500 lines. Push long detail into `references/` and link to it from
  `SKILL.md` (progressive disclosure).
- Every skill ships its own `LICENSE.txt`; keep it when adding or copying a skill.
- A skill can carry an evaluation workspace at `<name>-workspace/` (see
  [github-repo-setup-workspace/](.github/skills/github-repo-setup-workspace/)); running and grading
  those evals is covered in
  [.github/instructions/eval-harness.instructions.md](.github/instructions/eval-harness.instructions.md).
