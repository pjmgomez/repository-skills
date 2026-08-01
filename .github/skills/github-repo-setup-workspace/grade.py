#!/usr/bin/env python3
"""Grade the iteration-1 eval runs for github-repo-setup and emit viewer + benchmark artifacts.

Grading is done programmatically against the on-disk outputs (files present, file contents, and the
audit report text) so it is objective and repeatable. Produces, per run, a grading.json; per eval,
an eval_metadata.json; a viewer-friendly result.md for the non-audit runs; and a top-level
benchmark.json matching the schema the eval-viewer expects.

Timing/token metrics are not available in this environment (subagent notifications don't surface
duration/tokens here), so those fields are recorded as 0 and called out in the benchmark notes.
"""
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
ITER = os.path.join(ROOT, "iteration-1")
CONFIGS = ["with_skill", "without_skill"]

AUDIT_SEED = "# acme-parser\n\nParses ACME log files.\n"
ADDSEC_SEED = "# ledger-sync\n\nSyncs ledgers.\n"

EVALS = [
    {
        "id": 0, "name": "scaffold-new-repo", "kind": "scaffold",
        "prompt": ("I just created an empty folder for a new open-source Python CLI tool called "
                   "packmule. Can you set it up with the standard repository structure and the usual "
                   "GitHub files (readme, contributing, a security policy, issue and PR templates, "
                   "and a gitignore)?"),
        "assertions": [
            "README.md exists at the repository root",
            "CONTRIBUTING.md exists (root, docs/, or .github/)",
            "SECURITY.md exists (root, docs/, or .github/)",
            "A pull request template exists at .github/PULL_REQUEST_TEMPLATE.md",
            "At least one issue template exists under .github/ISSUE_TEMPLATE/",
            "A .gitignore file exists at the repository root",
            "The src/ and test/ folders exist",
            "The generated README or CONTRIBUTING mentions the project name 'packmule'",
        ],
    },
    {
        "id": 1, "name": "audit-existing-repo", "kind": "audit",
        "prompt": ("Here's my repository. Right now it only has a README and a src folder. Can you "
                   "check whether it follows GitHub repo best practices and tell me exactly what's "
                   "missing? Please don't change anything yet, just report."),
        "assertions": [
            "The response reports that CONTRIBUTING is missing",
            "The response reports that SECURITY is missing",
            "The response reports that the .gitignore is missing",
            "The response reports that issue and/or pull request templates are missing",
            "The response acknowledges that README and src/ are already present",
            "No new files or folders were written to the repository (audit stayed read-only)",
        ],
    },
    {
        "id": 2, "name": "add-security", "kind": "addsec",
        "prompt": ("My repository doesn't have a security policy and I keep getting reports opened as "
                   "public issues. Can you add a SECURITY.md that tells people how to report "
                   "vulnerabilities privately? Leave the rest of my files alone."),
        "assertions": [
            "A SECURITY.md file exists after the run (root or .github/)",
            "SECURITY.md describes reporting vulnerabilities privately rather than via public issues",
            "SECURITY.md contains a section about how to report a vulnerability",
            "The pre-existing README.md content was not modified",
        ],
    },
]


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def find_file(repo, names, subdirs=("", ".github", "docs")):
    for sub in subdirs:
        for name in names:
            candidate = os.path.join(repo, sub, name)
            if os.path.isfile(candidate):
                return os.path.relpath(candidate, repo)
    return None


def rel_entries(repo):
    entries = set()
    for dirpath, dirnames, filenames in os.walk(repo):
        for d in dirnames:
            entries.add(os.path.relpath(os.path.join(dirpath, d), repo))
        for f in filenames:
            entries.add(os.path.relpath(os.path.join(dirpath, f), repo))
    return entries


def grade_scaffold(repo):
    out = []
    readme = find_file(repo, ["README.md", "README", "README.rst", "README.txt"], subdirs=("",))
    out.append((readme is not None, f"found {readme}" if readme else "no README at root"))
    contributing = find_file(repo, ["CONTRIBUTING.md", "CONTRIBUTING"])
    out.append((contributing is not None, f"found {contributing}" if contributing else "no CONTRIBUTING"))
    security = find_file(repo, ["SECURITY.md"])
    out.append((security is not None, f"found {security}" if security else "no SECURITY"))
    pr = os.path.isfile(os.path.join(repo, ".github", "PULL_REQUEST_TEMPLATE.md"))
    out.append((pr, "found .github/PULL_REQUEST_TEMPLATE.md" if pr else "no .github/PULL_REQUEST_TEMPLATE.md"))
    it_dir = os.path.join(repo, ".github", "ISSUE_TEMPLATE")
    it = os.path.isdir(it_dir) and any(f.endswith(".md") for f in os.listdir(it_dir))
    out.append((it, f"issue templates: {sorted(os.listdir(it_dir))}" if os.path.isdir(it_dir) else "no .github/ISSUE_TEMPLATE/"))
    gi = os.path.isfile(os.path.join(repo, ".gitignore"))
    out.append((gi, "found .gitignore" if gi else "no .gitignore"))
    has_src = os.path.isdir(os.path.join(repo, "src"))
    has_test = os.path.isdir(os.path.join(repo, "test"))
    alt = [d for d in ("tests", "test") if os.path.isdir(os.path.join(repo, d))]
    out.append((has_src and has_test,
                f"src/={has_src}, test/={has_test} (test-like dirs present: {alt or 'none'})"))
    blob = (read(os.path.join(repo, readme or "README.md")) + read(os.path.join(repo, contributing or "CONTRIBUTING.md"))).lower()
    out.append(("packmule" in blob, "'packmule' present in README/CONTRIBUTING" if "packmule" in blob else "'packmule' not found"))
    return out


def grade_audit(repo, report_path):
    r = read(report_path).lower()
    out = []
    out.append(("contributing" in r, "report mentions CONTRIBUTING" if "contributing" in r else "CONTRIBUTING not in report"))
    out.append(("security" in r, "report mentions SECURITY" if "security" in r else "SECURITY not in report"))
    out.append(("gitignore" in r, "report mentions .gitignore" if "gitignore" in r else ".gitignore not in report"))
    out.append(("template" in r, "report mentions templates" if "template" in r else "templates not in report"))
    ack = ("readme" in r and "src" in r and ("present" in r or "acknowledg" in r))
    out.append((ack, "report acknowledges README and src as present" if ack else "README/src presence not clearly acknowledged"))
    entries = rel_entries(repo)
    expected = {"README.md", "src", os.path.join("src", "parser.py")}
    extras = entries - expected
    out.append((not extras, "repo unchanged (only README.md + src/parser.py)" if not extras else f"unexpected entries written: {sorted(extras)}"))
    return out


def grade_addsec(repo):
    out = []
    sec = find_file(repo, ["SECURITY.md"])
    content = read(os.path.join(repo, sec)) if sec else ""
    low = content.lower()
    out.append((sec is not None, f"found {sec}" if sec else "no SECURITY.md"))
    private = ("privat" in low) and ("public" in low)
    out.append((private, "mentions private reporting and public issues" if private else "does not clearly contrast private vs public reporting"))
    has_report_section = any(line.lstrip().lower().startswith("#") and "report" in line.lower()
                             for line in content.splitlines())
    out.append((has_report_section, "has a 'Reporting a vulnerability' style heading" if has_report_section else "no reporting-section heading"))
    readme = read(os.path.join(repo, "README.md"))
    unchanged = hashlib.sha256(readme.encode()).hexdigest() == hashlib.sha256(ADDSEC_SEED.encode()).hexdigest()
    out.append((unchanged, "README.md byte-identical to seed" if unchanged else "README.md was modified"))
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
            if ev["kind"] == "scaffold":
                results = grade_scaffold(repo)
                write_result_md(repo, out_dir, ["README.md", "CONTRIBUTING.md", "SECURITY.md", ".gitignore"])
            elif ev["kind"] == "audit":
                results = grade_audit(repo, os.path.join(out_dir, "report.md"))
            else:
                results = grade_addsec(repo)
                write_result_md(repo, out_dir, ["SECURITY.md", "README.md"])

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
        "metadata": {"skill_name": "github-repo-setup", "evals_run": [e["id"] for e in EVALS],
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
            "Eval 0 assertion 'src/ and test/ folders exist' is a convention check: the skill emits test/ "
            "(per the recommended layout) while a from-scratch baseline chose the equally valid tests/, so this "
            "assertion is expected to discriminate on naming, not correctness.",
        ],
    }
    with open(os.path.join(ITER, "benchmark.json"), "w", encoding="utf-8") as fh:
        json.dump(benchmark, fh, indent=2)

    print(f"{'eval':22} {'with_skill':>12} {'without_skill':>14}")
    for ev in EVALS:
        w = next(r for r in bench_runs if r["eval_id"] == ev["id"] and r["configuration"] == "with_skill")
        o = next(r for r in bench_runs if r["eval_id"] == ev["id"] and r["configuration"] == "without_skill")
        print(f"{ev['name']:22} {w['result']['passed']}/{w['result']['total']:>10} "
              f"{o['result']['passed']}/{o['result']['total']:>12}")
    print(f"\nmean pass_rate  with_skill={ws['mean']}  without_skill={wo['mean']}  delta={ws['mean']-wo['mean']:+.2f}")
    print(f"benchmark.json -> {os.path.join(ITER, 'benchmark.json')}")


if __name__ == "__main__":
    main()
