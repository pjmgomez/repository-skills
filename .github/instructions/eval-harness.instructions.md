---
description: "Use when running, grading, or extending the evaluation harness under github-repo-setup-workspace (the per-skill `*-workspace/` A/B eval convention). Covers where evals are defined, the with_skill vs without_skill run layout, how grade.py scores outputs deterministically, and the benchmark.json the eval viewer reads."
applyTo: ".github/skills/github-repo-setup-workspace/**"
---
# Evaluating a skill (the `*-workspace/` harness)

Repo-wide context is in [AGENTS.md](../../AGENTS.md). A skill's evaluation harness sits beside it in
a `*-workspace/` folder — currently only
[github-repo-setup-workspace/](../skills/github-repo-setup-workspace/). It A/B-tests the skill by
running each eval twice, `with_skill` and `without_skill`, then grades both against fixed assertions.

## Where things live

- Eval definitions: [github-repo-setup/evals/evals.json](../skills/github-repo-setup/evals/evals.json)
  — each has an `id`, `prompt`, `expected_output`, seed `files`, and `expectations`.
  [grade.py](../skills/github-repo-setup-workspace/grade.py) also embeds the same evals plus the
  per-eval `assertions` it scores, so grading is self-contained.
- Runs: `iteration-1/<eval-name>/<config>/outputs/`, where `<config>` is `with_skill` or
  `without_skill`. The agent's working tree for a run is that folder's `repo/`; **audit** runs
  instead put the audit reply at `outputs/report.md` (graded as text — the `repo/` must stay
  unchanged).
- Grader [grade.py](../skills/github-repo-setup-workspace/grade.py); its `iteration-1/benchmark.json`
  and `review-iteration-1.html` feed the viewer. The packaged skill under test is
  `github-repo-setup.skill`.

## Running and grading

1. For each eval in `evals.json`, create the run folders under
   `iteration-1/<eval-name>/{with_skill,without_skill}/outputs/`. `scaffold` starts from an empty
   `repo/`; `audit` and `add-security` start from a seed (`AUDIT_SEED` / `ADDSEC_SEED` in
   `grade.py` — audit seeds a `repo/` of `README.md` + `src/parser.py`).
2. Run each eval prompt in both configs, writing the agent's file changes into that run's `repo/`
   (and, for audit, the reply into `outputs/report.md`).
3. Grade: `python3 .github/skills/github-repo-setup-workspace/grade.py` (takes no arguments). It is
   pinned to `iteration-1` via the `ITER` constant — change that to grade a different iteration.

Grading reads only **on-disk outputs** (files present, file contents, audit report text) against
each eval's assertions, so it is objective and repeatable — nothing is model-judged. It writes a
per-eval `eval_metadata.json`, a per-run `grading.json`, a `result.md` for scaffold/add-security
runs, and the top-level `benchmark.json`.

`benchmark.json`: a `metadata` block (`skill_name`, `evals_run`, `runs_per_configuration`) plus
`runs`, each with `eval_id`, `eval_name`, `configuration`, `run_number`, a `result` block
(`pass_rate`, `passed`, `failed`, `total`, and `time_seconds` / `tokens` / `tool_calls` / `errors`),
and per-`expectations` `{text, passed, evidence}`.

> `time_seconds`, `tokens`, and `tool_calls` are always `0`: this environment doesn't surface
> subagent duration/token metrics. Don't read those zeros as real measurements.
