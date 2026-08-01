---
name: github-repo-setup
description: "Scaffold and audit a GitHub repository's folder structure and community-health files against common best practices. Use when the user wants to set up or bootstrap a new or bare repo, add standard folders (src, test, docs, tools), create or fill in a README, CONTRIBUTING, SECURITY, pull request template, or issue templates, add a starter .gitignore, or check an existing repository for missing structure and files. Trigger on phrases like 'set up my repo', 'scaffold a repository', 'what folders should my project have', 'add a README/CONTRIBUTING/SECURITY file', 'issue and PR templates', 'repo structure best practices', or 'audit my repo layout', even when the user doesn't name a specific file. Do NOT use for framework-specific project scaffolding such as create-react-app, Vite, or Next.js (that is project setup), for writing CI/CD workflows, or for configuring GitHub security features, branch protection, or Git LFS."
license: Complete terms in LICENSE.txt
---

# GitHub Repo Setup

Set up or tidy a repository so it follows widely used GitHub conventions: a predictable folder layout
plus the community-health files GitHub surfaces (README, CONTRIBUTING, SECURITY, a pull request
template, and issue templates) and a starter `.gitignore`. There are two modes — **audit** an
existing repo to see what's missing, and **scaffold** to create the missing pieces without touching
anything that already exists.

Scope is intentionally narrow: folder structure and that fixed set of template files. This skill does
**not** configure GitHub security features (Dependabot, secret scanning, branch protection) or Git
LFS — mention those as follow-ups, but don't try to set them up here.

## Choosing a mode

- "Is my repo set up right?" / "what am I missing?" -> **audit** first.
- "Bootstrap this repo" / "add the standard files" -> **scaffold**.
- Unsure -> audit first, summarize the gaps, then offer to scaffold them.

Confirm the target repo path up front (the scripts default to the current directory). If the project
looks large or polyglot, ask whether to include the extended folders.

## Helper scripts

Run these as black-box tools and pass `--help` for options. They share one source of truth
(`scripts/_repo_spec.py`), so audit and scaffold always agree on what "recommended" means — you
shouldn't need to read the source to use them.

- `scripts/audit_repo.py [REPO] [--extended] [--json]` — read-only. Prints a checklist of present and
  missing folders and files, annotating each missing item with why it matters. `--json` gives
  machine-readable output; the exit code is non-zero when something is missing.
- `scripts/scaffold_repo.py [REPO] [--extended] [--dry-run] [--name NAME]` — creates missing folders
  (each with a `.gitkeep`) and copies missing templates from `assets/templates/`, filling in the
  `{{PROJECT_NAME}}` and `{{YEAR}}` placeholders. It **never overwrites** an existing file. Always
  show a `--dry-run` first so the user can see exactly what will change.

`REPO` defaults to the current directory; `--extended` includes the optional folders listed below.

## Recommended folder layout

Core (created by default):

| Folder   | Purpose                                                        |
| -------- | ------------------------------------------------------------- |
| `src/`   | Application or library source code.                           |
| `test/`  | Unit and integration tests.                                   |
| `docs/`  | Project documentation.                                        |
| `tools/` | Scripts that automate project tasks (build, release, lint).   |

Extended (`--extended`, for larger projects): `.config/` (local setup config), `.build/` (build
scripts), `dep/` (vendored dependencies), `res/` (static resources), `samples/` (runnable examples).

Treat these as a starting point, not a mandate. When a language or framework has its own strong
convention, follow that instead — for example, a Python package often uses the package name in place
of `src/`, and many JS projects use `tests/` rather than `test/`. The point is a predictable,
documented layout, not these exact names.

## Community-health files

GitHub recognizes these in the repo root, in `docs/`, or in `.github/`. The scaffold writes README,
CONTRIBUTING, and SECURITY to the root and the templates under `.github/`:

| File                               | Why it matters                                            |
| ---------------------------------- | --------------------------------------------------------- |
| `README.md`                        | Explains what/why/how; shown on the repo home page.       |
| `CONTRIBUTING.md`                  | How to propose changes; linked from new issues and PRs.   |
| `SECURITY.md`                      | How to report vulnerabilities privately and responsibly.  |
| `.github/PULL_REQUEST_TEMPLATE.md` | Standardizes pull request descriptions.                   |
| `.github/ISSUE_TEMPLATE/*.md`      | Prefilled bug-report and feature-request forms.           |
| `.gitignore`                       | Keeps build output, secrets, and OS/editor cruft out.     |

The audit counts a file as present if it exists in any location GitHub recognizes, so it won't nag
about a `CONTRIBUTING` that already lives in `.github/`.

## Typical workflow

1. Confirm the repo path and whether to include the extended folders.
2. Run the audit and summarize the gaps in plain language.
3. Preview with `scaffold_repo.py --dry-run`, then run it for real once the user is happy.
4. Re-run the audit to confirm everything is now present.
5. Remind the user to edit the generated templates — they ship with placeholders (the contact email
   in `SECURITY.md`, the supported-versions table, the license statement in `README.md`) and are
   starting points, not finished documents.

## Out of scope (mention as follow-ups)

Call these out so the user isn't surprised by what the skill leaves untouched: choosing and adding a
`LICENSE`, a code of conduct, `CODEOWNERS`, and turning on GitHub's security features (Dependabot,
secret scanning, push protection) and branch protection. They're worthwhile, but they live outside
this skill.
