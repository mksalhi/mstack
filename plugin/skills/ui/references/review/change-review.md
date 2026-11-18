# Change review

Report what the change caused. Read the full diff and PR intent (title/body, linked issue, commit subjects). Mention correctness, tests, and security once.

## Scope
- Invocation target: `/mstack:ui review pr 482`. Accepted: `working`, `staged`, `branch`, `pr <n>`, a ref, or `a..b` / `a...b`.
- No target:
  1) If `HEAD` is ahead of `merge-base origin/<default> HEAD`, review that range; also uncommitted; count separately.
  2) Else if dirty: review uncommitted.
  3) Else stop; report branch, last commit SHA/subject, open PR (`gh pr status`); offer the last commit, a named target, or a whole-repo audit.
- Never pick `HEAD~1` yourself. Never `Approve` an empty scope.

## Mechanics
- Default branch: `origin/HEAD`, else `gh repo view --json defaultBranchRef`, else `git remote set-head origin --auto`.
- Diff against the merge base (three dots). Include untracked: add `git ls-files --others --exclude-standard`.
- PRs: `git fetch origin "pull/<n>/head:refs/remotes/pr/<n>"`; read with `git show refs/remotes/pr/<n>:path`; cite against that ref.
- Excludes: lockfiles (list each by name; `*.lock` misses `package-lock.json`), snapshots, build, generated, vendored, binaries. Changed fonts or new images still count; review the code that uses them. Name what you dropped.
- Stop if mid-rebase/merge or no resolvable base. Check `git rev-parse --git-path MERGE_HEAD` and equivalents. For a shallow clone, `--deepen=50` then 200 before giving up.
- Never change the checkout. No `checkout`, `switch`, `stash` or `gh pr checkout`. For a rendered check, use a separate worktree at the PR ref and remove it afterward.

## Expand to the surfaces it renders in
- One hop to direct importers; two only for tokens, theme values, shared primitives.
- Review at most five consumers: route/layout entry points first, then the most importers. Say how many you skipped.
- Run `git grep` against the reviewed ref, not the working tree.

## Read the removed lines
```bash
git diff -U0 "$BASE"...HEAD | grep -E '^-[^-]' | grep -E 'aria-|role=|alt=|<label|for=|focus|outline|tabindex|prefers-|lang=|dir=|text-wrap|tabular-nums'
```
Leads only. A removal is a regression only if nothing equivalent replaced it. Also check: semantic element to `div`, color token to literal/lighter token, string deleted vs moved to translations.

## Status every finding
- Status: Introduced, Regression, Pre-existing (verify with `git blame -L n,n "$BASE" -- file`). Also find incomplete: missing states (hover/focus/disabled/loading), translations, empty/error/narrow states, or inconsistent controls across siblings.

## Output
- Use [index.md](index.md) steps 5–8 and its output, with: a scope block (target; base/head SHAs; commit/uncommitted counts; files in scope; what was excluded; surfaces expanded/skipped); a Status column; count only Introduced and Regression toward cap/verdict. If none: “No actionable interface findings in this change.” List up to three Pre-existing findings separately, marked not this change’s responsibility.
