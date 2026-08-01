#!/usr/bin/env python3
"""Scaffold the recommended repository structure and template files.

Safe by design: existing files are never overwritten. Each missing folder gets a .gitkeep so it can
be committed while empty, and each missing template is copied from assets/templates/ with a few
placeholders filled in ({{PROJECT_NAME}}, {{YEAR}}). Preview with --dry-run before writing.

Usage:
    python scaffold_repo.py [REPO_PATH] [--extended] [--dry-run] [--name PROJECT_NAME]

REPO_PATH defaults to the current directory.
"""
import argparse
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _repo_spec import CORE_DIRS, EXTENDED_DIRS, FILES, TEMPLATES_DIR


def _fill(text, project_name):
    return (text
            .replace("{{PROJECT_NAME}}", project_name)
            .replace("{{YEAR}}", str(datetime.date.today().year)))


def scaffold(repo, extended=False, dry_run=False, project_name=None):
    project_name = project_name or os.path.basename(os.path.abspath(repo)) or "your project"
    created, skipped = [], []

    dirs = list(CORE_DIRS) + (list(EXTENDED_DIRS) if extended else [])
    for name, _purpose in dirs:
        target_dir = os.path.join(repo, name)
        if os.path.isdir(target_dir):
            skipped.append(f"{name}/")
            continue
        if not dry_run:
            os.makedirs(target_dir, exist_ok=True)
            open(os.path.join(target_dir, ".gitkeep"), "w").close()
        created.append(f"{name}/.gitkeep")

    for entry in FILES:
        for rel_path, template_name in entry["create"]:
            target = os.path.join(repo, rel_path)
            if os.path.exists(target):
                skipped.append(rel_path)
                continue
            with open(os.path.join(TEMPLATES_DIR, template_name), encoding="utf-8") as fh:
                content = _fill(fh.read(), project_name)
            if not dry_run:
                os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
                with open(target, "w", encoding="utf-8") as fh:
                    fh.write(content)
            created.append(rel_path)

    return created, skipped


def main():
    ap = argparse.ArgumentParser(
        description="Scaffold a repo's structure and community-health files (never overwrites).")
    ap.add_argument("repo", nargs="?", default=".", help="Path to the repository (default: .)")
    ap.add_argument("--extended", action="store_true",
                    help="Also create the optional folders (.config, .build, dep, res, samples).")
    ap.add_argument("--dry-run", action="store_true",
                    help="Show what would change without writing anything.")
    ap.add_argument("--name", dest="name", default=None,
                    help="Project name for template placeholders (default: repo folder name).")
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        print(f"error: not a directory: {repo}", file=sys.stderr)
        return 2

    created, skipped = scaffold(repo, args.extended, args.dry_run, args.name)

    prefix = "would create" if args.dry_run else "created"
    if created:
        print(f"{prefix} ({len(created)}):")
        for c in created:
            print(f"  + {c}")
    else:
        print("nothing to create")
    if skipped:
        print(f"\nleft untouched ({len(skipped)}):")
        for s in skipped:
            print(f"  = {s}")
    if args.dry_run:
        print("\n(dry run - no files were written)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
