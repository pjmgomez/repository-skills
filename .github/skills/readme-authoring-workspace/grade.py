#!/usr/bin/env python3
"""Grade the iteration-1 eval runs for readme-authoring and emit viewer + benchmark artifacts.

Grading is deterministic and file-based: it reads only the on-disk outputs (the produced README
text, or the QA reply text) and scores them against each eval's fixed assertions, so results are
objective and repeatable — nothing is model-judged. Mirrors the github-repo-setup-workspace grader.

Per run it writes a grading.json; per eval an eval_metadata.json; a result.md for the author/improve
runs; and a top-level benchmark.json in the schema the eval-viewer expects.

Timing/token metrics aren't surfaced in this environment (subagent notifications don't carry them),
so those fields are recorded as 0 and called out in the benchmark notes.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
ITER = os.path.join(ROOT, "iteration-1")
CONFIGS = ["with_skill", "without_skill"]

# Seed for the "improve" eval: a messy README the agent is asked to rewrite (two H1s, no sections,
# an absolute in-repo link, usage buried in prose). Materialized into each run's repo/ before the run.
WEAK_README = (
    "# lumen\n\n"
    "lumen is a tiny logging library for Node. install it with npm install lumen and require it and "
    "call log. it supports levels and colors and json output and file transports and it is fast and "
    "has no dependencies. to use it you write const log = require('lumen'); log.info('hi'). for "
    "contributing see [CONTRIBUTING](https://github.com/acme/lumen/blob/main/CONTRIBUTING.md) and "
    "there is more on the wiki.\n\n"
    "# Notes\n\n"
    "random notes here.\n"
)

# Seed for the "author" eval: the library source the agent writes a README for.
TINYTOML_SRC = (
    '"""tinytoml: a tiny TOML parser and serializer."""\n\n\n'
    "def parse(text: str) -> dict:\n"
    '    """Parse a TOML string into a Python dict."""\n\n\n'
    "def dumps(data: dict) -> str:\n"
    '    """Serialize a Python dict back to a TOML string."""\n'
)

EVALS = [
    {
        "id": 0, "name": "author-readme-from-scratch", "kind": "author",
        "prompt": ("I just built a small Python library called tinytoml — it parses TOML text into a "
                   "dict and serializes a dict back to TOML. The code is in the repo I gave you "
                   "(tinytoml.py). There's no README yet. Can you write me a proper README for it?"),
        "assertions": [
            "README.md exists at the repository root",
            "The README has exactly one top-level '# ' title heading",
            "The README describes what the project does near the top (summary paragraph or a what/overview section)",
            "The README includes an installation or getting-started section",
            "The README includes a usage or examples section",
            "The README shows a usage example in a fenced code block",
            "The README mentions the project name 'tinytoml'",
            "The README uses at least three '## ' section headings (so GitHub's auto table of contents is useful)",
            "Any in-repo links use relative paths (no absolute github.com blob/tree/raw self-links)",
        ],
    },
    {
        "id": 1, "name": "improve-weak-readme", "kind": "improve",
        "prompt": ("Here's my repo. The README is a mess — it's basically a wall of text with a couple "
                   "of stray headings. It's a small Node logging library called lumen. Can you rewrite "
                   "it into a proper, well-structured README? Keep the actual facts about the project."),
        "assertions": [
            "The rewritten README preserves the project name 'lumen'",
            "The rewritten README has exactly one top-level '# ' title heading",
            "The rewritten README adds at least three standard sections (what/overview, install, usage, contributing, license) as '##' headings",
            "The rewritten README has no skipped heading levels",
            "The rewritten README includes a usage example in a fenced code block",
            "In-repo links are relative (the original absolute github.com link to CONTRIBUTING was relativized)",
            "The rewritten README preserves real project facts (mentions Node and at least one feature such as levels, colors, or json)",
        ],
    },
    {
        "id": 2, "name": "readme-placement-and-links-qa", "kind": "qa",
        "prompt": ("Quick question before I write my README: where in the repo should the README file "
                   "actually go so GitHub picks it up, how do I get that table-of-contents outline "
                   "thing, and how should I link between sections and to other files like CONTRIBUTING? "
                   "Just explain — don't create any files yet."),
        "assertions": [
            "Explains that GitHub surfaces the README from .github/, the repository root, or docs/",
            "Explains the precedence order (.github/ first, then root, then docs/)",
            "Explains that GitHub auto-generates the table of contents / outline from the heading structure",
            "Explains that sections are linkable via anchors generated from their headings",
            "Explains that in-repo links should be relative (or that absolute links break in clones/forks)",
            "No files were created or modified (the response stayed read-only)",
        ],
    },
]


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def strip_fences(text):
    out, in_fence = [], False
    for line in text.splitlines():
        if re.match(r"\s*```", line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def headings(text):
    result = []
    for line in strip_fences(text).splitlines():
        m = re.match(r"(#{1,6})\s+(.*\S)\s*$", line)
        if m:
            result.append((len(m.group(1)), m.group(2)))
    return result


def h_level(text, level):
    return [t for lvl, t in headings(text) if lvl == level]


def has_fenced_code(text):
    return sum(1 for line in text.splitlines() if re.match(r"\s*```", line)) >= 2


def has_abs_inrepo(text):
    return re.search(
        r"\((?:https?://github\.com/[^)\s]+/(?:blob|tree|raw)/|https?://raw\.githubusercontent\.com/)[^)\s]+\)",
        strip_fences(text)) is not None


def has_relative_link_to(text, needle):
    return re.search(r"\]\((?!https?://|#)[^)]*" + needle + r"[^)]*\)", strip_fences(text), re.I) is not None


def no_skipped_levels(text):
    prev = None
    for lvl, _ in headings(text):
        if prev is not None and lvl > prev + 1:
            return False
        prev = lvl
    return True


def section_hits(text, groups):
    heads = " ".join(h.lower() for h in h_level(text, 2))
    return sum(1 for kws in groups if any(k in heads for k in kws))


def rel_entries(repo):
    entries = set()
    for dirpath, dirnames, filenames in os.walk(repo):
        for name in list(dirnames) + filenames:
            entries.add(os.path.relpath(os.path.join(dirpath, name), repo))
    return entries


STANDARD_GROUPS = [
    ("what", "about", "overview", "introduction", "description"),
    ("install", "getting started", "setup", "quick start", "quickstart"),
    ("usage", "example", "how to use"),
    ("contribut",),
    ("licen",),
]


def grade_author(repo):
    path = os.path.join(repo, "README.md")
    text = read(path)
    low = text.lower()
    h1 = h_level(text, 1)
    h2 = h_level(text, 2)
    first_h2 = next((i for i, ln in enumerate(strip_fences(text).splitlines())
                     if re.match(r"##\s+\S", ln)), None)
    lines = strip_fences(text).splitlines()
    summary = any(lines[i].strip() and not lines[i].lstrip().startswith("#")
                  for i in range(0, first_h2 if first_h2 is not None else len(lines)))
    has_what = summary or any(any(k in h.lower() for k in STANDARD_GROUPS[0]) for h in h2)
    has_install = any(any(k in h.lower() for k in STANDARD_GROUPS[1]) for h in h2)
    has_usage = any(any(k in h.lower() for k in STANDARD_GROUPS[2]) for h in h2)
    out = [
        (os.path.isfile(path), "found README.md at root" if os.path.isfile(path) else "no README.md at root"),
        (len(h1) == 1, f"{len(h1)} top-level '#' heading(s)"),
        (has_what, "has a summary/what-it-does up top" if has_what else "no what/summary near the top"),
        (has_install, "has an install/getting-started section" if has_install else "no install/getting-started section"),
        (has_usage, "has a usage/examples section" if has_usage else "no usage/examples section"),
        (has_fenced_code(text), "has a fenced code block" if has_fenced_code(text) else "no fenced code block"),
        ("tinytoml" in low, "mentions 'tinytoml'" if "tinytoml" in low else "'tinytoml' not found"),
        (len(h2) >= 3, f"{len(h2)} '##' section headings"),
        (not has_abs_inrepo(text), "no absolute in-repo links" if not has_abs_inrepo(text) else "absolute in-repo link present"),
    ]
    return out


def grade_improve(repo):
    path = os.path.join(repo, "README.md")
    text = read(path)
    low = text.lower()
    h1 = h_level(text, 1)
    hits = section_hits(text, STANDARD_GROUPS)
    rel_ok = not has_abs_inrepo(text)
    facts = ("node" in low) and any(k in low for k in ("level", "color", "json"))
    out = [
        ("lumen" in low, "mentions 'lumen'" if "lumen" in low else "'lumen' not found"),
        (len(h1) == 1, f"{len(h1)} top-level '#' heading(s)"),
        (hits >= 3, f"{hits} standard sections present"),
        (no_skipped_levels(text), "no skipped heading levels" if no_skipped_levels(text) else "skips a heading level"),
        (has_fenced_code(text), "has a fenced code block" if has_fenced_code(text) else "no fenced code block"),
        (rel_ok, ("absolute link relativized" + (" (relative CONTRIBUTING link present)" if has_relative_link_to(text, "contributing") else ""))
            if rel_ok else "absolute github.com in-repo link remains"),
        (facts, "preserves Node + a feature" if facts else "project facts not clearly preserved"),
    ]
    return out


def grade_qa(repo, report_path):
    r = read(report_path).lower()
    idx_gh, idx_docs = r.find(".github"), r.find("docs")
    locations = (".github" in r) and ("docs" in r) and ("root" in r)
    precedence = (any(w in r for w in ("preceden", "order", "first", "takes precedence"))
                  and idx_gh != -1 and idx_docs != -1 and idx_gh < idx_docs)
    auto_toc = (("table of contents" in r) or ("outline" in r)) and \
               any(w in r for w in ("auto", "automatic", "generate")) and ("head" in r)
    anchors = ("anchor" in r) or ("section link" in r) or ("links to a section" in r) or \
              (("link" in r) and ("section" in r) and ("heading" in r))
    relative = ("relative" in r) and any(w in r for w in ("clone", "fork", "absolute"))
    unchanged = len(rel_entries(repo)) == 0
    out = [
        (locations, "names .github/, root, and docs/" if locations else "doesn't name all three locations"),
        (precedence, "explains precedence (.github first)" if precedence else "precedence order not explained"),
        (auto_toc, "explains auto-generated TOC from headings" if auto_toc else "auto-TOC from headings not explained"),
        (anchors, "explains heading anchors/section links" if anchors else "section-link anchors not explained"),
        (relative, "explains relative vs absolute links" if relative else "relative-link guidance missing"),
        (unchanged, "no files written (read-only)" if unchanged else f"unexpected files written: {sorted(rel_entries(repo))}"),
    ]
    return out


def tree(repo):
    lines = []
    for dirpath, dirnames, filenames in os.walk(repo):
        dirnames.sort()
        rel = os.path.relpath(dirpath, repo)
        depth = 0 if rel == "." else rel.count(os.sep) + 1
        name = os.path.basename(repo) if rel == "." else os.path.basename(dirpath)
        lines.append("  " * depth + name + "/")
        for f in sorted(filenames):
            lines.append("  " * (depth + 1) + f)
    return "\n".join(lines)


def write_result_md(repo, out_dir, key_files):
    parts = ["# Run result\n", "## Files (tree)\n", "```", tree(repo), "```\n"]
    for kf in key_files:
        path = os.path.join(repo, kf)
        if os.path.isfile(path):
            parts += [f"## {kf}\n", "```markdown", read(path).rstrip(), "```\n"]
    with open(os.path.join(out_dir, "result.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))


def main():
    bench_runs = []
    per_config_rates = {c: [] for c in CONFIGS}

    for ev in EVALS:
        eval_dir = os.path.join(ITER, ev["name"])
        with open(os.path.join(eval_dir, "eval_metadata.json"), "w", encoding="utf-8") as fh:
            json.dump({"eval_id": ev["id"], "eval_name": ev["name"],
                       "prompt": ev["prompt"], "assertions": ev["assertions"]}, fh, indent=2)

        for cfg in CONFIGS:
            out_dir = os.path.join(eval_dir, cfg, "outputs")
            repo = os.path.join(out_dir, "repo")
            if ev["kind"] == "author":
                results = grade_author(repo)
                write_result_md(repo, out_dir, ["README.md"])
            elif ev["kind"] == "improve":
                results = grade_improve(repo)
                write_result_md(repo, out_dir, ["README.md"])
            else:
                results = grade_qa(repo, os.path.join(out_dir, "report.md"))

            expectations = [{"text": t, "passed": bool(p), "evidence": e}
                            for t, (p, e) in zip(ev["assertions"], results)]
            passed = sum(1 for x in expectations if x["passed"])
            total = len(expectations)
            rate = round(passed / total, 4) if total else 0.0
            per_config_rates[cfg].append(rate)

            grading = {"expectations": expectations,
                       "summary": {"passed": passed, "failed": total - passed,
                                   "total": total, "pass_rate": rate}}
            with open(os.path.join(eval_dir, cfg, "grading.json"), "w", encoding="utf-8") as fh:
                json.dump(grading, fh, indent=2)

            bench_runs.append({
                "eval_id": ev["id"], "eval_name": ev["name"], "configuration": cfg,
                "run_number": 1,
                "result": {"pass_rate": rate, "passed": passed, "failed": total - passed,
                           "total": total, "time_seconds": 0, "tokens": 0, "tool_calls": 0, "errors": 0},
                "expectations": expectations,
            })

    def stats(vals):
        n = len(vals)
        mean = round(sum(vals) / n, 4) if n else 0.0
        var = sum((x - mean) ** 2 for x in vals) / (n - 1) if n > 1 else 0.0
        return {"mean": mean, "stddev": round(var ** 0.5, 4), "min": min(vals or [0]), "max": max(vals or [0])}

    ws, wo = stats(per_config_rates["with_skill"]), stats(per_config_rates["without_skill"])
    benchmark = {
        "metadata": {"skill_name": "readme-authoring", "evals_run": [e["id"] for e in EVALS],
                     "runs_per_configuration": 1},
        "runs": bench_runs,
        "run_summary": {
            "with_skill": {"pass_rate": ws, "time_seconds": {"mean": 0, "stddev": 0}, "tokens": {"mean": 0, "stddev": 0}},
            "without_skill": {"pass_rate": wo, "time_seconds": {"mean": 0, "stddev": 0}, "tokens": {"mean": 0, "stddev": 0}},
            "delta": {"pass_rate": f"{ws['mean'] - wo['mean']:+.2f}", "time_seconds": "n/a", "tokens": "n/a"},
        },
        "notes": [
            "Grading is deterministic and file-based; see each run's grading.json for per-assertion evidence.",
            "Timing and token metrics were not captured in this environment, so time/token columns read 0.",
            "Runs were produced in-environment (no independent task-executing subagents are available "
            "here), so the without_skill outputs represent a competent but unguided attempt; the delta "
            "illustrates the skill's structural guidance rather than a blind measurement.",
        ],
    }
    with open(os.path.join(ITER, "benchmark.json"), "w", encoding="utf-8") as fh:
        json.dump(benchmark, fh, indent=2)

    print(f"{'eval':30} {'with_skill':>12} {'without_skill':>14}")
    for ev in EVALS:
        w = next(r for r in bench_runs if r["eval_id"] == ev["id"] and r["configuration"] == "with_skill")
        o = next(r for r in bench_runs if r["eval_id"] == ev["id"] and r["configuration"] == "without_skill")
        print(f"{ev['name']:30} {w['result']['passed']}/{w['result']['total']:>10} "
              f"{o['result']['passed']}/{o['result']['total']:>12}")
    print(f"\nmean pass_rate  with_skill={ws['mean']}  without_skill={wo['mean']}  delta={ws['mean']-wo['mean']:+.2f}")
    print(f"benchmark.json -> {os.path.join(ITER, 'benchmark.json')}")


if __name__ == "__main__":
    main()
