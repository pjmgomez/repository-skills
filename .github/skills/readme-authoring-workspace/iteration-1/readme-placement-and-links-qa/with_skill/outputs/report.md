# Where the README goes, the table of contents, and links

**Where to put the file.** GitHub surfaces a README from any of three locations: the `.github/`
directory, the repository **root**, or the `docs/` directory. If more than one exists, GitHub picks
them in that order of precedence — `.github/` first, then the repository root, then `docs/`. The root
is the conventional home and what contributors expect, so put it there unless you specifically want to
keep community files together in `.github/`.

**The table-of-contents outline.** You don't build it by hand. GitHub automatically generates the
table of contents (the "Outline" button on the rendered page) from your **heading structure**. You get
it for free as long as your headings form a clean hierarchy: one top-level `#` title, `##` for the
main sections, `###` for subsections, without skipping levels.

**Linking between sections.** Every heading automatically becomes a linkable **anchor** derived from
its text — so `## Getting started` is reachable as `#getting-started`. You can link to any section
from elsewhere in the file (or from another file) using that anchor.

**Linking to other files like CONTRIBUTING.** Use a **relative** link, e.g.
`[Contributing](CONTRIBUTING.md)`, rather than an absolute `https://github.com/...` URL. GitHub
rewrites relative links to match whatever branch the reader is on, so they keep working in clones and
forks — absolute in-repo links break the moment someone views a fork or a local checkout. Two
gotchas: start a link with `/` to make it relative to the repo root (`/LICENSE`), and keep the link
text on a single line or GitHub won't render it.
