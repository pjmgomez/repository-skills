---
description: 'Scaffold a new skill''s evaluation harness (the *-workspace/ A/B convention): create the skill''s evals/evals.json and a matching grade.py by mirroring an existing harness. Use when the user wants to add, bootstrap, or scaffold evals, an eval harness, or a *-workspace/ for a skill that has none. Do NOT use to run or grade existing evals (that is /run-skill-evals), or to change a skill''s own behavior.'
name: 'Create Eval Harness'
argument-hint: 'skill name to add an eval harness for'
agent: 'agent'
---

Scaffold an A/B evaluation harness for an existing skill, following
[eval-harness.instructions.md](../instructions/eval-harness.instructions.md) (repo context in
[AGENTS.md](../../AGENTS.md)). Mirror an existing harness —
[github-repo-setup-workspace/](../skills/github-repo-setup-workspace/) or
[readme-authoring-workspace/](../skills/readme-authoring-workspace/) — as the model to copy.

Read the target skill name from the invocation argument (see the argument hint). If it is missing,
or the named skill has no `.github/skills/<name>/SKILL.md`, ask before creating anything. If the
skill already has a `*-workspace/`, stop and point the user at
[/run-skill-evals](./run-skill-evals.prompt.md) rather than scaffolding a second one.

## Steps

1. **Confirm the target.** Verify `.github/skills/<name>/SKILL.md` exists and that no
   `.github/skills/<name>-workspace/` is present yet. Read the skill's `description` and body so the
   evals exercise what it actually claims to do.
2. **Define the evals** in `.github/skills/<name>/evals/evals.json`: an object with `skill_name` and
   an `evals` array. Give each eval an `id`, a kebab-case `name`, a `kind`, a realistic user
   `prompt`, a one-sentence `expected_output`, seed `files` (empty for from-scratch runs), and a list
   of plain-language `expectations`. Cover the skill's main modes and include at least one read-only
   or negative case. Use `github-repo-setup`'s scaffold/audit/add-security or `readme-authoring`'s
   author/improve/qa evals as templates.
3. **Create the grader** `.github/skills/<name>-workspace/grade.py` by copying an existing `grade.py`
   and adapting it: keep the `with_skill` / `without_skill` configs, the `iteration-1/<eval-name>/`
   layout, and the deterministic **on-disk** scoring (files present, file contents, or report text —
   never model-judged). Embed the same evals plus a machine-checkable `assertion` for each
   `expectation`, and emit the per-run `grading.json`, per-eval `eval_metadata.json`, and top-level
   `benchmark.json` in the schema the viewer reads. Seed any starting fixtures as module constants
   (as `AUDIT_SEED` / `WEAK_README` do). Record `time_seconds` / `tokens` / `tool_calls` as `0` —
   this environment doesn't surface them.
4. **(Optional) Add a trigger test.** If the skill's discovery matters, add a
   `.github/skills/<name>-workspace/trigger-eval.json` of `{query, should_trigger}` cases — some that
   should load the skill and some that should not — modelled on
   [readme-authoring-workspace/trigger-eval.json](../skills/readme-authoring-workspace/trigger-eval.json).
5. **Summarize** the files created, and tell the user to run the harness with
   [/run-skill-evals](./run-skill-evals.prompt.md): that command generates `iteration-N/`,
   `benchmark.json`, and the review HTML — this prompt only scaffolds the definitions and grader.

Create only the evals and grader for the target skill. Do not run the evals, and do not change the
skill's own behavior.
