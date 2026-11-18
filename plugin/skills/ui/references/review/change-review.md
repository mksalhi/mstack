# Change review

Report what the change caused, not everything it touched. Read the whole diff and its stated intent (PR title and body, linked issue, commit subjects) before judging. Correctness, tests and security belong to general code review; mention them once and move on.

## Scope

The invocation is the target: `/mstack:ui review pr 482`. Accepted targets are `working`, `staged`, `branch`, `pr <n>`, a ref, or `a..b` / `a...b` (keep the user's dots).

With no target:

1. `HEAD` is ahead of `merge-base origin/<default> HEAD`: review that range plus any uncommitted changes, and count the two separately. Check this before the working tree, or one stray edit will hide a twelve-commit branch.
2. Otherwise, if the tree is dirty, review the uncommitted changes.
3. Otherwise stop. Report the branch, the last commit's SHA and subject, and any open PR (`gh pr status`), then offer three options: the last commit, a target they name, or a whole-repo audit. Never pick `HEAD~1` yourself, and never `Approve` an empty scope.

Mechanics:

- **Default branch:** `origin/HEAD`, else `gh repo view --json defaultBranchRef`, else `git remote set-head origin --auto`.
- **Diff a branch against its merge base, with three dots.** `git diff HEAD` misses untracked files, so add `git ls-files --others --exclude-standard`.
- **PRs:** `git fetch origin "pull/<n>/head:refs/remotes/pr/<n>"`, read with `git show refs/remotes/pr/<n>:path`, and cite lines against that ref.
- **Excludes:** drop lockfiles (list each by name, since `*.lock` misses `package-lock.json`), snapshots, build output, generated sources, vendored code and binaries, and name what you dropped. A changed font file or a newly added image still counts: review the code that uses it.
- **If the repo is mid-rebase, mid-merge or has no resolvable base, stop and say so.** Check `git rev-parse --git-path MERGE_HEAD` and the equivalents. For a shallow clone, `--deepen=50` and then 200 before giving up.
- **Never change the checkout.** No `checkout`, `switch`, `stash` or `gh pr checkout`. For a rendered check, use a separate worktree at the PR ref and remove it afterward.

## Expand to the surfaces it renders in

Go one hop, to direct importers. Go two hops only for tokens, theme values and shared primitives. Review at most five consumers: route and layout entry points first, then the ones with the most importers. Say how many you skipped. Run `git grep` against the reviewed ref, not the working tree.

## Read the removed lines

```bash
git diff -U0 "$BASE"...HEAD | grep -E '^-[^-]' | grep -E 'aria-|role=|alt=|<label|for=|focus|outline|tabindex|prefers-|lang=|dir=|text-wrap|tabular-nums'
```

These lines are only leads. A removal is a regression only if nothing replaced it: `aria-labelledby` for `aria-label`, a native `<button>` for `role=button`, a `box-shadow` focus ring for `outline`, a token that measures the same, or a logical property for a physical one. Also check for a semantic element turned into a `div`, a color token turned into a literal or lighter token, and a string deleted rather than moved into the translation catalogue.

## Status every finding

- `Introduced`: the change created it.
- `Regression`: the change weakened something that was correct.
- `Pre-existing`: it's in an untouched line, even one three lines from a hunk. Check with `git blame -L n,n "$BASE" -- file`.

Then look for **incomplete** changes: a new variant missing some states (hover, focus, disabled, loading), a new string missing from the translation catalogue, a new component with no empty, error or narrow state, or a control added to one surface but not its siblings.

## Output

Use [index.md](index.md) steps 5 to 8 and its output, with these changes:

- Open with a scope block: target, base and head refs with SHAs, commit and uncommitted counts, files in scope, what was excluded, and surfaces expanded or skipped.
- Add a `Status` column to the findings table.
- The cap and the verdict count only `Introduced` and `Regression`. If those are empty, write "No actionable interface findings in this change."
- List up to three `Pre-existing` findings separately, marked as not this change's responsibility.
