#!/usr/bin/env bash
# PostToolUse hook: validate a skill's SKILL.md after it is edited.
# Fails open — if no SKILL.md was touched, or the validator/its deps are unavailable,
# it does nothing and never blocks. It blocks only on a genuine validation failure.
set -uo pipefail

payload="$(cat)"

# Only act when an edited path points at a skill's SKILL.md.
paths="$(printf '%s' "$payload" \
  | grep -oE '"[^"]*\.github/skills/[^"]*/SKILL\.md"' \
  | tr -d '"' \
  | sort -u)"
[ -z "$paths" ] && exit 0

# Fail open when the validator cannot run.
command -v python3 >/dev/null 2>&1 || exit 0
python3 -c 'import yaml' >/dev/null 2>&1 || exit 0

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
validator="$repo_root/.github/skills/skill-creator/scripts/quick_validate.py"
[ -f "$validator" ] || exit 0

failed=0
while IFS= read -r p; do
  [ -z "$p" ] && continue
  case "$p" in
    /*) skill_dir="$(dirname "$p")" ;;
    *)  skill_dir="$repo_root/$(dirname "$p")" ;;
  esac
  [ -f "$skill_dir/SKILL.md" ] || continue
  if ! out="$(python3 "$validator" "$skill_dir" 2>&1)"; then
    failed=1
    echo "SKILL.md validation failed for $p: $out" >&2
  fi
done <<< "$paths"

if [ "$failed" -eq 1 ]; then
  printf '%s\n' '{"decision":"block","reason":"A SKILL.md failed quick_validate.py. See the hook message and fix the frontmatter before continuing."}'
  exit 2
fi
exit 0
