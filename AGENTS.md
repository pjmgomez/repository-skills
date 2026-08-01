# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this repo is

A curated collection of **agent skills** (reusable Claude/Copilot capabilities). It is not an
application — there is no app to build or run. Each skill lives in its own folder under
`.github/skills/<name>/` and is self-contained. The unit of work is a **single skill**, so scope
changes to one skill folder unless asked otherwise.

This checkout contains two skills — [github-repo-setup](.github/skills/github-repo-setup/SKILL.md)
and [readme-authoring](.github/skills/readme-authoring/SKILL.md) — each alongside its own evaluation
workspace ([github-repo-setup-workspace/](.github/skills/github-repo-setup-workspace/) and
[readme-authoring-workspace/](.github/skills/readme-authoring-workspace/)). Use `github-repo-setup`'s
`SKILL.md` as the worked example of the conventions below; the point-of-edit checklist for frontmatter
is [.github/instructions/skill-authoring.instructions.md](.github/instructions/skill-authoring.instructions.md).

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

Frontmatter is YAML between `---` markers. Only six keys are allowed — `name`, `description`,
`license`, `allowed-tools`, `metadata`, `compatibility` — where `name` is kebab-case and **must
equal the folder name**, and `description` is ≤1024 chars with **no angle brackets** (`<` or `>`).
The detailed point-of-edit checklist (per-field limits, quoting values that contain a colon, the
`license` convention) lives in
[skill-authoring.instructions.md](.github/instructions/skill-authoring.instructions.md), which is
auto-attached whenever you edit a `SKILL.md`.

## The `description` field is the trigger surface

An agent decides whether to load a skill from its `description` alone, so pack every "when to use"
signal in — capability first, then `Use when…` triggers, then `Do NOT use for…` exclusions.
[github-repo-setup](.github/skills/github-repo-setup/SKILL.md) is the model to copy; the full house
style is in
[skill-authoring.instructions.md](.github/instructions/skill-authoring.instructions.md).

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

Four repo prompts (in [.github/prompts/](.github/prompts/)) speed up skill work:

- `/create-skill` — scaffold a new `.github/skills/<name>/` (SKILL.md + `LICENSE.txt`) that follows
  the rules above.
- `/review-skill` — audit an existing `SKILL.md` against those rules and report fixes (read-only).
- `/create-eval` — scaffold a skill's `*-workspace/` A/B eval harness (`evals/evals.json` +
  `grade.py`) by mirroring an existing one.
- `/run-skill-evals` — run that harness in both configurations and grade it with `grade.py`
  (see [.github/instructions/eval-harness.instructions.md](.github/instructions/eval-harness.instructions.md)).

## Conventions and gotchas

- Keep `SKILL.md` under ~500 lines. Push long detail into `references/` and link to it from
  `SKILL.md` (progressive disclosure).
- Every skill ships its own `LICENSE.txt`; keep it when adding or copying a skill.
- A skill can carry an evaluation workspace at `<name>-workspace/` — both skills here do
  ([github-repo-setup-workspace/](.github/skills/github-repo-setup-workspace/),
  [readme-authoring-workspace/](.github/skills/readme-authoring-workspace/)). Running and grading
  those evals is covered in
  [.github/instructions/eval-harness.instructions.md](.github/instructions/eval-harness.instructions.md).
