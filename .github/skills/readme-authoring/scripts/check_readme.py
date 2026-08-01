#!/usr/bin/env python3
"""Lint a repository README for the structural issues that quietly break on GitHub.

Read-only: this never edits anything. It checks the things that are easy to miss by eye but that
degrade a rendered README — a missing or duplicated title, skipped heading levels (which muddy the
auto-generated table of contents), link text split across lines (which GitHub silently won't render),
absolute in-repo links (which break in forks and clones), and absent reader-question sections.

Usage:
    python check_readme.py [PATH] [--json]

PATH may be a README file or a directory. For a directory, the README is located the way GitHub does:
the .github/ directory, then the repository root, then docs/. PATH defaults to the current directory.

Exit code is non-zero when a hard structural error is found (missing/duplicate title, skipped heading
level, or multi-line link text); missing sections and absolute in-repo links are reported as warnings.
"""
import argparse
import json
import os
import re
import sys

README_NAMES = ["README.md", "README", "README.rst", "README.txt"]
SEARCH_SUBDIRS = [".github", "", "docs"]  # GitHub's own precedence order.

# Reader-question sections a README is expected to answer, and the heading keywords that satisfy each.
RECOMMENDED_SECTIONS = [
    ("what it does / overview", ("what", "about", "overview", "introduction", "description")),
    ("installation / getting started", ("install", "getting started", "setup", "quick start", "quickstart")),
    ("usage / example", ("usage", "example", "how to use")),
    ("contributing", ("contribut",)),
    ("license", ("licen",)),
]

ABSOLUTE_INREPO = re.compile(
    r"\((https?://github\.com/[^)\s]+/(?:blob|tree|raw)/[^)\s]+|https?://raw\.githubusercontent\.com/[^)\s]+)\)")
MULTILINE_LINK = re.compile(r"\[[^\]\n]*\n[^\]]*\]\(")


def find_readme(path):
    if os.path.isfile(path):
        return path
    for sub in SEARCH_SUBDIRS:
        for name in README_NAMES:
            candidate = os.path.join(path, sub, name)
            if os.path.isfile(candidate):
                return candidate
    return None


def strip_code_fences(lines):
    """Return (visible_lines, in_fence_flags): body with fenced code blocks blanked out."""
    out, in_fence = [], False
    for line in lines:
        if re.match(r"\s*```", line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return out


def headings(visible_lines):
    result = []
    for i, line in enumerate(visible_lines):
        m = re.match(r"(#{1,6})\s+(.*\S)\s*$", line)
        if m:
            result.append((i + 1, len(m.group(1)), m.group(2)))
    return result


def check(readme_path):
    with open(readme_path, encoding="utf-8", errors="replace") as fh:
        raw = fh.read()
    lines = raw.splitlines()
    visible = strip_code_fences(lines)
    visible_text = "\n".join(visible)
    hs = headings(visible)

    errors, warnings = [], []

    # Title: exactly one level-1 heading.
    h1s = [h for h in hs if h[1] == 1]
    if not h1s:
        errors.append("No top-level '# Title' heading; GitHub shows the file name instead.")
    elif len(h1s) > 1:
        errors.append(
            f"{len(h1s)} top-level '#' headings (lines {', '.join(str(h[0]) for h in h1s)}); "
            "use a single title and '##' for sections.")

    # Heading hierarchy: no skipped levels (e.g. '##' jumping to '####').
    prev_level = None
    for line_no, level, text in hs:
        if prev_level is not None and level > prev_level + 1:
            errors.append(
                f"Line {line_no}: heading '{text}' jumps from level {prev_level} to {level}; "
                "don't skip levels or the auto table of contents gets muddled.")
        prev_level = level

    # Multi-line link text won't render on GitHub.
    for m in MULTILINE_LINK.finditer(visible_text):
        line_no = visible_text.count("\n", 0, m.start()) + 1
        errors.append(f"Line {line_no}: link text is split across lines; keep '[text]' on one line.")

    # Absolute in-repo links break in forks/clones; prefer relative paths.
    for i, line in enumerate(visible):
        for m in ABSOLUTE_INREPO.finditer(line):
            warnings.append(
                f"Line {i + 1}: absolute in-repo link {m.group(1)}; use a relative link so it "
                "survives forks, clones, and branches.")

    # Recommended sections (a summary paragraph before the first '##' counts as 'what it does').
    heading_blob = " ".join(t.lower() for _, _, t in hs)
    first_section_line = next((ln for ln, lvl, _ in hs if lvl == 2), len(visible) + 1)
    has_summary = any(
        visible[i].strip() and not visible[i].lstrip().startswith("#")
        for i in range(min(len(visible), first_section_line))
    ) if h1s else False
    for label, keywords in RECOMMENDED_SECTIONS:
        satisfied = any(k in heading_blob for k in keywords)
        if label.startswith("what it does") and has_summary:
            satisfied = True
        if not satisfied:
            warnings.append(f"No '{label}' section — readers may be left with that question.")

    return {"readme": readme_path, "errors": errors, "warnings": warnings}


def main():
    ap = argparse.ArgumentParser(description="Lint a README for structural issues (read-only).")
    ap.add_argument("path", nargs="?", default=".", help="README file or directory (default: .)")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = ap.parse_args()

    readme = find_readme(os.path.abspath(args.path))
    if readme is None:
        msg = f"No README found under {os.path.abspath(args.path)} (.github/, root, or docs/)."
        if args.json:
            print(json.dumps({"readme": None, "errors": [msg], "warnings": []}, indent=2))
        else:
            print(f"error: {msg}", file=sys.stderr)
        return 2

    report = check(readme)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"README lint: {os.path.relpath(readme)}\n")
        if report["errors"]:
            print("Errors:")
            for e in report["errors"]:
                print(f"  [ ] {e}")
        if report["warnings"]:
            print("\nWarnings:")
            for w in report["warnings"]:
                print(f"  [!] {w}")
        if not report["errors"] and not report["warnings"]:
            print("No issues found.")
        elif not report["errors"]:
            print("\nNo hard errors; see warnings above.")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
