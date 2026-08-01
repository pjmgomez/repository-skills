---
name: readme-authoring
description: "Author or improve a repository's README so it clearly tells readers what a project does, why it is useful, and how to use it. Use when the user wants to write a README from scratch, rewrite or restructure an existing one, add missing sections (what/why, installation, usage, getting help, maintainers), fix heading structure so GitHub's auto table of contents works, convert absolute in-repo links to relative links and image paths, decide where the README should live (.github, root, or docs), set up a profile README, or move long content to a wiki. Trigger on phrases like 'write a README', 'improve my README', 'my readme is a mess', 'add a table of contents to my readme', or 'readme best practices', even when the user doesn't say 'README' but clearly means a project's landing page. Do NOT use for scaffolding repo folders or other community-health files like CONTRIBUTING or SECURITY (that is github-repo-setup), for writing full end-user docs or a wiki, or for general Markdown formatting unrelated to a README."
license: Complete terms in LICENSE.txt
---

# README Authoring

A README is usually the first thing a visitor reads, and on GitHub it is rendered automatically on the
repository's home page. This skill helps you produce one that earns that attention: it explains what a
project does, why it is worth using, and how to get started — and it is structured so GitHub's built-in
navigation (the automatic table of contents, heading anchors, relative links) actually works.

There are two modes:

- **Author** — write a README from scratch for a project that has none (or only a stub).
- **Improve** — restructure an existing README: add missing sections, fix a heading hierarchy that
  breaks the auto table of contents, relativize links that break in clones, or move overgrown content
  out to a wiki.

Both modes lean on the same underlying idea: a README is a *landing page*, not a manual. Keep it to
what a newcomer needs to understand and start using the project, and link out to the deeper material.

## Choosing a mode

- "Write me a README" / "this project needs a README" -> **author**.
- "My README is a mess" / "add a table of contents" / "clean this up" -> **improve** the existing one.
- Unsure whether one exists -> look for a README in `.github/`, the repo root, then `docs/` (that is
  GitHub's own search order); if you find one, improve it rather than replacing it wholesale, so you
  preserve the author's voice and any project-specific details.

Confirm the target: the repository path (or the README file itself), the project's name, and one line
on what it is. If you cannot tell what the project does from the code or the conversation, ask — a
README written without that understanding is the main failure mode here.

## What a great README contains

Readers arrive with a small set of questions. Answer them in roughly this order, because it mirrors how
someone evaluates a project: *is this for me → do I trust it → how do I run it → where do I go next.*

| Section | The reader's question it answers |
| --- | --- |
| **Title + one-line summary** | "What is this, in a sentence?" |
| **What it does / Overview** | "What problem does it solve, and is it for me?" |
| **Why / Features** | "Why choose this over the alternatives?" |
| **Getting started** (prerequisites, install) | "What do I need, and how do I install it?" |
| **Usage** (a minimal, copy-pasteable example) | "Show me it working." |
| **Getting help / Support** | "I'm stuck — where do I go?" |
| **Contributing** | "How do I propose a change?" |
| **Maintainers / Authors** | "Who is behind this?" |
| **License** | "What am I allowed to do with it?" |

Treat this as a checklist of reader questions, not a rigid template. A tiny library may fold "why" into
the summary and skip "maintainers"; a large project may add "Architecture" or "Roadmap". The goal is
that a newcomer can answer every question above without leaving the page or reading the source.

The single most valuable section is a **working usage example** near the top. A reader who can copy one
block and see the project do something is far more likely to keep going than one who has to assemble it
themselves. Lead with the simplest example that produces a visible result.

## Where the README lives

GitHub automatically surfaces a README that sits in any of three places: the `.github/` directory, the
repository root, or the `docs/` directory. If more than one exists, GitHub picks them in that order
(`.github/` wins, then root, then `docs/`). The root is the conventional home and what contributors
expect, so prefer it unless the user has a specific reason (for example, keeping community files
together in `.github/`).

Two special cases worth knowing:

- **Profile README.** A README in the root of a *public* repository whose name matches the owner's
  username renders on their GitHub profile page. If the user is describing "the thing on my profile",
  that is what they mean — the audience is visitors to their profile, not users of a specific project,
  so lead with who they are and what they work on.
- **Size limit.** When rendered on GitHub, anything past 500 KiB is truncated. That is a lot of prose,
  but it is another reason to link out to long-form docs rather than paste them inline.

## Structure it for navigation

GitHub builds a table of contents automatically from the heading structure — there is an "Outline"
button on every rendered README. You get that navigation for free *if* the headings form a clean
hierarchy, so it is worth getting right:

- Start with a single top-level `#` heading (the title). Use `##` for the main sections and `###` for
  subsections. Do not skip levels (an `##` jumping straight to `####`) — it muddies the generated
  outline and reads as a mistake.
- Write descriptive, stable heading text. Every heading becomes a linkable anchor, so
  `## Getting started` is reachable at `#getting-started`. You can link to any section from elsewhere
  in the file, or from other files, using that anchor.

## Links and images that don't break

Use **relative links** for anything inside the same repository, and reserve absolute URLs for genuinely
external resources. This matters because people read READMEs in places other than the GitHub web UI —
in clones, in forks, on other branches — and an absolute link to `https://github.com/you/proj/blob/...`
breaks the moment someone is looking at a fork or a local checkout. GitHub rewrites relative links to
match whatever branch the reader is on, so they keep working everywhere.

- A link relative to the current file: `[Contributing](CONTRIBUTING.md)` or `[guide](docs/guide.md)`.
- A link from the repository root regardless of the current file: start it with `/`, e.g.
  `[license](/LICENSE)`. You can also use `./` and `../` to walk the tree.
- **Keep the link text on one line.** GitHub will not render a link whose `[text]` is split across a
  line break. This is a common, silent breakage — watch for it when reflowing paragraphs.
- Image paths follow the same rules: prefer a relative path like `docs/images/diagram.png` over an
  absolute `raw.githubusercontent.com` URL so the image survives forks and branches.

## Keep it a landing page, not the whole manual

A README should carry only what a developer needs to understand the project and get started. When a
section is growing into reference material — exhaustive configuration, API docs, tutorials — move it to
a **wiki** or a `docs/` page and link to it. This keeps the README scannable and stays under the
render limit.

For the same reason, do not inline the contents of the other community-health files. Reference them:
point "Contributing" at `CONTRIBUTING.md`, "Security" at `SECURITY.md`, a code of conduct at its file,
and the license at `LICENSE`. Creating those files is out of scope here — `github-repo-setup` handles
`CONTRIBUTING` and `SECURITY` — so just link to whichever ones already exist and let the README tie the
project's front page together.

## Workflow

### Authoring from scratch

1. Establish the essentials: project name, a one-sentence description, language/runtime, and how it is
   installed and run. Pull these from the code or the conversation; ask only for what you genuinely
   cannot infer.
2. Copy `assets/templates/README.md` as a starting point and fill it in. It is a scaffold of the
   reader-question sections above with placeholders — delete any section that does not apply rather than
   leaving it empty.
3. Write a minimal usage example that actually runs. If you can derive it from the code (an entry
   point, a CLI command, an exported function), do; a real example beats a plausible-looking fake one.
4. Link out to the community files and docs that exist (`CONTRIBUTING.md`, `SECURITY.md`, `LICENSE`,
   `docs/`), and drop links to ones that don't.
5. Run `scripts/check_readme.py` on the result and fix what it flags.

### Improving an existing README

1. Read the current README first and keep what is good — the project's name, its voice, any accurate
   specifics. You are restructuring, not ghost-writing a replacement.
2. Map what is there against the reader-question checklist and note the gaps (missing usage example, no
   "getting help", etc.).
3. Fix structure: collapse to a single `#` title, normalize the `##`/`###` hierarchy so the auto table
   of contents is clean, and split any level jumps.
4. Fix links: relativize in-repo links and image paths, and repair any link text that wraps across
   lines.
5. If the file is bloated with reference material, propose moving it to a wiki or `docs/` and leaving a
   link.
6. Run `scripts/check_readme.py` to confirm the structural issues are resolved.

## Helper script

`scripts/check_readme.py [PATH]` is a read-only linter. Point it at a README file or a repository (it
finds the README the way GitHub does) and it reports structural problems that are easy to miss by eye:
missing or duplicate top-level heading, skipped heading levels, absent reader-question sections,
link text split across lines, and absolute in-repo links that should be relative. It exits non-zero
when it finds a hard structural error, so you can use it as a quick gate after editing. Run it with
`--help` for options; treat it as a black box — you should not need to read its source to use it.

## Out of scope

Say so when a request drifts past READMEs, and hand it off:

- Creating repository folders (`src/`, `test/`, `docs/`) or the other community-health files
  (`CONTRIBUTING`, `SECURITY`, issue/PR templates, `.gitignore`) -> that is `github-repo-setup`.
- Writing full end-user documentation, tutorials, or the wiki itself -> a README should *link* to
  those, not contain them.
- Choosing a license, configuring CI, or turning on GitHub security features -> outside this skill.
