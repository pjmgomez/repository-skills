# Repository best-practices audit

**Repository:** `.../audit-existing-repo/with_skill/outputs/repo`
**Mode:** Read-only audit (nothing was created, modified, or deleted)
**Standard checked:** Common GitHub repo layout + community-health files

## Summary

The repo currently has a `README.md` and a `src/` folder — a good start, but **8 recommended
items are missing**. None are blockers, but adding them brings the project in line with the
conventions GitHub surfaces and that contributors expect.

## Present (acknowledged)

| Item         | Notes                                                              |
| ------------ | ------------------------------------------------------------------ |
| `src/`       | Present, contains `parser.py`. This is where source code belongs.  |
| `README.md`  | Present with real content (`# acme-parser`, one-line description). |

## Missing (8 items)

### Folders

| Folder   | Why it matters                                                |
| -------- | ------------------------------------------------------------- |
| `test/`  | Unit and integration tests. Signals the project is testable.  |
| `docs/`  | Project documentation beyond the README.                      |
| `tools/` | Scripts that automate project tasks (build, release, lint).   |

### Community-health files

| File                                  | Why it matters                                                              |
| ------------------------------------- | --------------------------------------------------------------------------- |
| `CONTRIBUTING.md`                     | Tells contributors how to propose changes; linked from new issues and PRs.  |
| `SECURITY.md`                         | Documents how to report vulnerabilities privately and responsibly.          |
| `.github/PULL_REQUEST_TEMPLATE.md`    | Standardizes what contributors include in a pull request.                   |
| `.github/ISSUE_TEMPLATE/*.md`         | Prefills bug-report and feature-request forms so issues stay consistent.    |
| `.gitignore`                          | Keeps build output, secrets, and OS/editor cruft out of version control.    |

> Note: GitHub also recognizes `CONTRIBUTING`/`SECURITY` in `docs/` or `.github/`, so any of those
> locations would count — none currently exist.

## Notes and scope

- **Folder names are a convention, not a mandate.** Since this is a Python project, the source
  could live in a package folder named after the project instead of `src/`, and tests are often in
  `tests/`. The point is a predictable, documented layout — adapt names to your ecosystem.
- **Extended folders were not flagged.** Optional folders for larger/polyglot projects
  (`.config/`, `.build/`, `dep/`, `res/`, `samples/`) are not counted as missing for a project this
  size. Ask if you'd like an extended audit.
- **Out of scope (worthwhile follow-ups, not part of this audit):** choosing a `LICENSE`, a code of
  conduct, `CODEOWNERS`, enabling GitHub security features (Dependabot, secret scanning, push
  protection), branch protection, and Git LFS.

## Suggested next step

No changes were made, as requested. When you're ready, the missing pieces can be created
non-destructively (existing files are never overwritten) — preview first, then apply. Remember the
generated templates ship with placeholders (e.g. the contact email in `SECURITY.md`) that need
editing.
