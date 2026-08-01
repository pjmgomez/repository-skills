# Run result

## Files (tree)

```
repo/
  .gitignore
  CONTRIBUTING.md
  README.md
  SECURITY.md
  .github/
    PULL_REQUEST_TEMPLATE.md
    ISSUE_TEMPLATE/
      bug_report.md
      feature_request.md
  docs/
    .gitkeep
  src/
    .gitkeep
  test/
    .gitkeep
  tools/
    .gitkeep
```

## README.md

```markdown
# packmule

One-paragraph description of what this project does and who it is for.

## Why

What problem does this solve? Why would someone choose it?

## Getting started

### Prerequisites

- List the tools, runtimes, and versions a user needs.

### Installation

```
# commands to install
```

### Usage

```
# a minimal, copy-pasteable example
```

## Project structure

| Path | Purpose |
| --- | --- |
| `src/` | Source code. |
| `test/` | Tests. |
| `docs/` | Documentation. |
| `tools/` | Automation scripts. |

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or
pull request.

## Security

Found a vulnerability? Please follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

## License

State the project's license here (for example, "Released under the MIT License"). Add a `LICENSE`
file with the full text.
```

## CONTRIBUTING.md

```markdown
# Contributing to packmule

Thanks for taking the time to contribute. This guide explains how to propose changes so they can be
reviewed and merged quickly.

## Ways to contribute

- Report a bug using the bug report issue template.
- Suggest an improvement using the feature request template.
- Improve the documentation.
- Submit code changes through a pull request.

## Development workflow

Regular collaborators work from branches in this repository rather than forks, which keeps
collaboration and review in one place.

1. Create a branch off `main`: `git switch -c short-description`
2. Make your change in small, focused commits.
3. Run the tests and any linters.
4. Open a pull request and fill in the template.

## Commit messages

Write imperative, present-tense summaries (for example, "Add retry to upload"). Keep the subject line
short and use the body to explain *why* when it isn't obvious from the change.

## Pull requests

- Keep each pull request focused on a single change.
- Link the issue it resolves.
- Make sure automated checks pass and respond to review feedback.

## Be respectful

Assume good intent, keep discussion constructive, and help make this a welcoming place to collaborate.
```

## SECURITY.md

```markdown
# Security Policy

## Supported versions

Update this table to reflect which versions currently receive security fixes.

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| older   | :x:                |

## Reporting a vulnerability

Please report security vulnerabilities **privately** — do not open a public issue.

- Preferred: use GitHub's private vulnerability reporting ("Report a vulnerability" under the
  repository's **Security** tab), if it is enabled.
- Otherwise, email the maintainers at security@example.com.

Please include as much of the following as you can:

- A description of the issue and its impact.
- Steps to reproduce, or a proof of concept.
- Affected versions and any known mitigations.

## What to expect

- We will acknowledge your report within a few business days.
- We will keep you updated as we investigate and prepare a fix.
- We will credit you in the release notes unless you would prefer to remain anonymous.
```

## .gitignore

```markdown
# Dependencies
node_modules/

# Build output
dist/
build/
out/

# Logs
*.log
logs/

# Environment and secrets -- never commit these
.env
.env.*
*.pem
*.key

# Python
__pycache__/
*.py[cod]
.venv/
venv/
.pytest_cache/

# OS files
.DS_Store
Thumbs.db

# Editor / IDE
.idea/
*.swp
```
