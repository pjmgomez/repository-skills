---
description: 'Run and grade a skill A/B evaluation harness (the *-workspace/ convention): execute each eval with_skill and without_skill, then score with grade.py. Use when the user wants to run, grade, benchmark, or re-run a skill evaluation, or refresh benchmark.json. Do NOT use to author evals from scratch or to change grading assertions.'
name: 'Run Skill Evals'
argument-hint: 'skill name (defaults to the only *-workspace/ present)'
agent: 'agent'
---

Run and grade a skill's evaluation harness, following
[eval-harness.instructions.md](../instructions/eval-harness.instructions.md) (repo context in
[AGENTS.md](../../AGENTS.md)). The harness A/B-tests a skill by running each eval twice —
`with_skill` and `without_skill` — then grading both against fixed, on-disk assertions.

Target skill: read it from the argument. If omitted, use the only `*-workspace/` present (currently
[github-repo-setup-workspace/](../skills/github-repo-setup-workspace/)).

## Steps

1. **Locate the evals.** Read the target skill's `evals/evals.json` (e.g.
   [github-repo-setup/evals/evals.json](../skills/github-repo-setup/evals/evals.json)) for each
   eval's `id`, `prompt`, seed `files`, and `expectations`.
2. **Create run folders** under
   `<skill>-workspace/iteration-<N>/<eval-name>/{with_skill,without_skill}/outputs/`. Seed each run's
   working tree as the harness specifies — `scaffold` starts from an empty `repo/`; seeded evals
   (audit, add-security) start from their seed.
3. **Run each eval prompt in both configs.** In `with_skill` the target skill is available; in
   `without_skill` it is not. Write the agent's file changes into that run's `repo/`. For an
   **audit** eval, put the reply at `outputs/report.md` and leave `repo/` unchanged.
4. **Grade** with `python3 .github/skills/<skill>-workspace/grade.py` (no arguments; pinned to
   `iteration-1` via the `ITER` constant — change it to grade another iteration). Grading reads only
   on-disk outputs, so it is deterministic.
5. **Summarize** from `iteration-<N>/benchmark.json`: per-eval `pass_rate` for `with_skill` vs
   `without_skill`, and any failed `expectations` with their evidence. Ignore `time_seconds`,
   `tokens`, and `tool_calls` — this environment always reports them as `0`.

Do not edit the skill under test or the grading assertions; this prompt only runs and reports the
evals.
