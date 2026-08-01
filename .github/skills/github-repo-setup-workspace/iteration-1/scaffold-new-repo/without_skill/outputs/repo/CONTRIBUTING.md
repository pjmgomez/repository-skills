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
