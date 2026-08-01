# Run result

## Files (tree)

```
repo/
  .gitignore
  CHANGELOG.md
  CONTRIBUTING.md
  LICENSE
  README.md
  SECURITY.md
  pyproject.toml
  .github/
    PULL_REQUEST_TEMPLATE.md
    ISSUE_TEMPLATE/
      bug_report.md
      config.yml
      feature_request.md
  docs/
    index.md
  src/
    packmule/
      __init__.py
      __main__.py
      cli.py
      __pycache__/
        __init__.cpython-314.pyc
        __main__.cpython-314.pyc
        cli.cpython-314.pyc
  tests/
    __init__.py
    test_cli.py
```

## README.md

```markdown
# packmule

> A lightweight command-line tool for packing and hauling your files around.

`packmule` is an open-source Python CLI. This repository is scaffolded and ready
for development — replace the placeholder command logic in
[`src/packmule/cli.py`](src/packmule/cli.py) with your real features.

## Requirements

- Python 3.9 or newer

## Installation

Install from source while the project is under development:

```bash
git clone https://github.com/your-org/packmule.git
cd packmule
python -m pip install -e .
```

## Usage

```bash
packmule --help
packmule --version
```

You can also run it as a module:

```bash
python -m packmule --help
```

## Development

Set up a local environment with the development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

Run the test suite:

```bash
pytest
```

Lint the code:

```bash
ruff check .
```

## Project layout

```
packmule/
├── src/packmule/      # Application package (src layout)
├── tests/             # Test suite
├── docs/              # Documentation
└── pyproject.toml     # Packaging & tooling configuration
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before
opening an issue or pull request.

## Security

Found a vulnerability? Please follow the process in [SECURITY.md](SECURITY.md).

## License

`packmule` is released under the MIT License. See [LICENSE](LICENSE) for details.
```

## CONTRIBUTING.md

```markdown
# Contributing to packmule

Thanks for your interest in improving `packmule`! This document explains how to
get set up and the conventions we follow.

## Code of Conduct

By participating in this project you agree to be respectful and constructive.
Please be kind to other contributors.

## Getting started

1. Fork the repository and clone your fork.
2. Create a virtual environment and install the development dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # On Windows: .venv\Scripts\activate
   python -m pip install -e ".[dev]"
   ```

3. Create a branch for your change:

   ```bash
   git checkout -b my-feature
   ```

## Making changes

- Keep changes focused; open separate pull requests for unrelated work.
- Add or update tests for any behavior you change.
- Update documentation (including the README) when relevant.

## Before you open a pull request

Run the checks locally and make sure they pass:

```bash
pytest
ruff check .
```

## Commit messages

Write clear, descriptive commit messages. A short summary line (50 characters
or fewer) followed by an optional body explaining the "why" works well.

## Submitting a pull request

1. Push your branch to your fork.
2. Open a pull request against the `main` branch.
3. Fill out the pull request template and link any related issues.

A maintainer will review your contribution as soon as possible. Thank you for
helping make `packmule` better!
```

## SECURITY.md

```markdown
# Security Policy

## Supported Versions

`packmule` is in early development. Security fixes are applied to the latest
release on the `main` branch.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of `packmule` seriously. If you believe you have found a
security vulnerability, please report it privately so we can address it before
it is publicly disclosed.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, use one of the following channels:

- Use GitHub's [private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)
  ("Report a vulnerability" under the repository's **Security** tab), or
- Email the maintainers at `security@example.com`.

Please include as much of the following as you can:

- A description of the vulnerability and its impact.
- Steps to reproduce or a proof of concept.
- The affected version(s) and environment details.

## What to expect

- We will acknowledge your report within **3 business days**.
- We will investigate and keep you informed of our progress.
- Once a fix is available, we will coordinate a disclosure timeline with you and
  credit you for the discovery (unless you prefer to remain anonymous).

Thank you for helping keep `packmule` and its users safe.
```

## .gitignore

```markdown
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Type checkers / linters
.mypy_cache/
.dmypy.json
dmypy.json
.pyre/
.pytype/
.ruff_cache/

# Jupyter Notebook
.ipynb_checkpoints

# IDEs and editors
.idea/
.vscode/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Documentation builds
docs/_build/
site/
```
