#!/usr/bin/env python3
"""Audit a repository against the recommended structure and template files.

Read-only: this never creates or modifies anything. It prints a checklist of what is present and what
is missing, with a one-line rationale for each missing item, so you can decide what to add.

Usage:
    python audit_repo.py [REPO_PATH] [--extended] [--json]

REPO_PATH defaults to the current directory.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _repo_spec import CORE_DIRS, EXTENDED_DIRS, FILES, dir_present, file_present


def audit(repo, extended=False):
    dirs = list(CORE_DIRS) + (list(EXTENDED_DIRS) if extended else [])
    dir_results = [
        {"name": name, "purpose": purpose, "present": dir_present(repo, name)}
        for name, purpose in dirs
    ]
    file_results = [
        {"label": e["label"], "why": e["why"], "present": file_present(repo, e)}
        for e in FILES
    ]
    return dir_results, file_results


def main():
    ap = argparse.ArgumentParser(
        description="Audit a repo's folder structure and community-health files (read-only).")
    ap.add_argument("repo", nargs="?", default=".", help="Path to the repository (default: .)")
    ap.add_argument("--extended", action="store_true",
                    help="Also check the optional folders (.config, .build, dep, res, samples).")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of text.")
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        print(f"error: not a directory: {repo}", file=sys.stderr)
        return 2

    dir_results, file_results = audit(repo, args.extended)
    missing_dirs = [d["name"] for d in dir_results if not d["present"]]
    missing_files = [f["label"] for f in file_results if not f["present"]]
    total_missing = len(missing_dirs) + len(missing_files)

    if args.json:
        print(json.dumps(
            {"repo": repo, "directories": dir_results, "files": file_results,
             "missing": missing_dirs + missing_files}, indent=2))
        return 1 if total_missing else 0

    def mark(present):
        return "[x]" if present else "[ ]"

    print(f"Repository audit: {repo}\n")
    print("Folders:")
    for d in dir_results:
        line = f"  {mark(d['present'])} {d['name']}/"
        if not d["present"]:
            line += f"  - {d['purpose']}"
        print(line)

    print("\nCommunity-health files:")
    for f in file_results:
        line = f"  {mark(f['present'])} {f['label']}"
        if not f["present"]:
            line += f"  - {f['why']}"
        print(line)

    print()
    if total_missing == 0:
        print("All recommended items are present.")
    else:
        print(f"Missing {total_missing} item(s): " + ", ".join(missing_dirs + missing_files))
        print("Run scaffold_repo.py to create the missing pieces (it won't overwrite anything).")
    return 1 if total_missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
