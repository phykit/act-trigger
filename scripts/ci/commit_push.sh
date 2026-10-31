#!/usr/bin/env bash
# Commit whatever is staged, then push with retries. Files of 90 MB or more are unstaged (GitHub rejects 100 MB);
# every failure is raised as an Actions annotation so it is readable without the raw log.
# Usage: scripts/ci/commit_push.sh "commit message"
set -u
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
while IFS= read -r f; do
  [ -f "$f" ] || continue
  s=$(stat -c%s "$f")
  if [ "$s" -ge 90000000 ]; then
    git reset -q -- "$f"
    echo "::warning::$f is $s bytes; left out of the commit (GitHub limit 100 MB)"
  fi
done < <(git diff --cached --name-only)
echo "::notice::staged $(git diff --cached --name-only | wc -l) files"
git commit -q -m "$1" || { echo "::notice::nothing to commit"; exit 0; }
for i in 1 2 3 4 5; do
  if out=$( { git pull --rebase --autostash -q origin main && git push -q; } 2>&1 ); then
    echo "::notice::pushed on attempt $i"; exit 0
  fi
  echo "::warning::push attempt $i failed: $(printf '%s' "$out" | tr '\n' ' ' | cut -c1-600)"
  git rebase --abort 2>/dev/null || true
  sleep 10
done
echo "::error::push failed after 5 attempts"
exit 1
