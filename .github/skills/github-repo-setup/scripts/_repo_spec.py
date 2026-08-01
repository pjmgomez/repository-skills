"""Shared definition of the recommended repository structure.

Single source of truth for audit_repo.py and scaffold_repo.py so the two never drift apart. Scope is
deliberately limited to folder structure plus a fixed set of template files (README, CONTRIBUTING,
SECURITY, a pull request template, issue templates, and .gitignore).
"""
import os

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(SKILL_ROOT, "assets", "templates")

# (name, purpose) -- the mainstream baseline almost every project benefits from.
CORE_DIRS = [
    ("src", "Application or library source code."),
    ("test", "Unit and integration tests."),
    ("docs", "Project documentation."),
    ("tools", "Scripts that automate project tasks (build, release, lint)."),
]

# Opt-in via --extended. Straight from the repo-structure article; useful for larger projects.
EXTENDED_DIRS = [
    (".config", "Configuration for local/machine setup."),
    (".build", "Build-process scripts (Docker Compose, packaging helpers)."),
    ("dep", "Vendored third-party dependencies."),
    ("res", "Static resources such as images."),
    ("samples", "Runnable 'hello world' samples that support the docs."),
]

# Each entry:
#   key        -- stable id
#   label      -- what the audit prints
#   recognized -- paths that count as "already present" (a trailing "/" means a directory with >=1 .md)
#   create     -- [(path_to_write, template_filename)] used by scaffold_repo.py
#   why        -- one-line rationale shown by the audit for missing items
FILES = [
    {
        "key": "readme",
        "label": "README",
        "recognized": ["README.md", "README", "README.txt", "README.rst",
                       ".github/README.md", "docs/README.md"],
        "create": [("README.md", "README.md")],
        "why": "Explains what/why/how; GitHub surfaces it on the repo home page.",
    },
    {
        "key": "contributing",
        "label": "CONTRIBUTING",
        "recognized": ["CONTRIBUTING.md", "CONTRIBUTING",
                       ".github/CONTRIBUTING.md", "docs/CONTRIBUTING.md"],
        "create": [("CONTRIBUTING.md", "CONTRIBUTING.md")],
        "why": "Tells contributors how to propose changes; linked from new issues and pull requests.",
    },
    {
        "key": "security",
        "label": "SECURITY",
        "recognized": ["SECURITY.md", ".github/SECURITY.md", "docs/SECURITY.md"],
        "create": [("SECURITY.md", "SECURITY.md")],
        "why": "Documents how to report vulnerabilities privately and responsibly.",
    },
    {
        "key": "pr_template",
        "label": "Pull request template",
        "recognized": ["PULL_REQUEST_TEMPLATE.md", ".github/PULL_REQUEST_TEMPLATE.md",
                       "docs/PULL_REQUEST_TEMPLATE.md", ".github/PULL_REQUEST_TEMPLATE/"],
        "create": [(".github/PULL_REQUEST_TEMPLATE.md", "PULL_REQUEST_TEMPLATE.md")],
        "why": "Standardizes what contributors include in a pull request.",
    },
    {
        "key": "issue_templates",
        "label": "Issue templates",
        "recognized": [".github/ISSUE_TEMPLATE/", ".github/ISSUE_TEMPLATE.md",
                       "docs/ISSUE_TEMPLATE.md"],
        "create": [(".github/ISSUE_TEMPLATE/bug_report.md", "ISSUE_TEMPLATE/bug_report.md"),
                   (".github/ISSUE_TEMPLATE/feature_request.md", "ISSUE_TEMPLATE/feature_request.md")],
        "why": "Prefills issue bodies so bug reports and feature requests stay consistent.",
    },
    {
        "key": "gitignore",
        "label": ".gitignore",
        "recognized": [".gitignore"],
        "create": [(".gitignore", "gitignore")],
        "why": "Keeps build output, secrets, and OS/editor cruft out of version control.",
    },
]


def dir_present(repo, name):
    return os.path.isdir(os.path.join(repo, name))


def _recognized_hit(repo, rel):
    if rel.endswith("/"):
        directory = os.path.join(repo, rel.rstrip("/"))
        return os.path.isdir(directory) and any(f.endswith(".md") for f in os.listdir(directory))
    return os.path.exists(os.path.join(repo, rel))


def file_present(repo, entry):
    return any(_recognized_hit(repo, rel) for rel in entry["recognized"])
