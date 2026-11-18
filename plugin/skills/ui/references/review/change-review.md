# Change review

Follow this when the request names a branch, pull request, commit range or uncommitted changes. Resolve the scope, expand changed files to the surfaces they affect, read both sides of the diff and classify every finding, then hand back to [index.md](index.md) for severity, consolidation, coverage, the cap and the verdict. Domain rules belong to the domain areas. Correctness, tests, security and performance belong to the project's general code review: name the concern once and move on.

Report what the change caused; stay mostly quiet about what it merely touched. Read the whole change and its stated intent before forming an opinion.

## 1. Resolve the change scope first

The whole invocation is the target, so `/mstack:ui review pr 482` reviews pull request 482. [Scope resolution](scope-resolution.md) holds the accepted targets.

With no target, stop at the first match:

1. `HEAD` is ahead of `git merge-base origin/<default-branch> HEAD`: that range **plus** any uncommitted changes, stating commit count and uncommitted file count separately.
2. The working tree is dirty: the uncommitted changes.
3. Neither: stop and ask, per step 2.

Check the merge base before the working tree, or one stray edit shadows a twelve-commit branch.

Exclude lockfiles, snapshots, generated output, vendored code and binaries, and name what you excluded.

## 2. With no change, ask rather than invent one

Never fall back to `HEAD~1..HEAD` on your own. State the repository facts ([Nothing to review](scope-resolution.md#nothing-to-review) lists them), offer these routes and wait:

- **The last commit**, `HEAD~1..HEAD`, named by short SHA and subject.
- **A target they name**: `pr <n>`, a branch, a ref or a range, resolved per step 1.
- **A whole-repository interface audit**: run it as a repository-scope review, without this file's scope block, statuses or pre-existing section.

Check for an open pull request on the current branch first and offer it first; a branch whose commits already landed still has its pull request.

If the scope emptied after exclusions, name the excluded files and ask the same way. Never report a review of nothing as `Approve`.

## 3. A diff is not a surface

Review the **blast radius**: the surfaces a changed file renders in. Expand one hop (direct importers and callers); a second hop only for design tokens, theme values and shared primitives. Review at most five consumers, ordered by [the rule in Scope resolution](scope-resolution.md#expanding-to-consumers), and state how many you did not expand.

## 4. Read the removed lines

Read the `-` side of every hunk against [Removed signals](removed-signals.md). A signal is a lead: a removal is a regression only when nothing in the change replaces it, and the owning area judges that. Route each unmatched removal to its owner, report only what it confirms, and status it `Regression`.

## 5. Classify every finding

- `Introduced`: the change created it.
- `Regression`: the change weakened something previously correct.
- `Pre-existing`: present in the touched code but not caused by this change.

Status by what the diff touched: an untouched line is `Pre-existing` even three lines from a hunk. Confirm against the base ref when it matters:

```bash
git blame -L <line>,<line> "$BASE" -- path/to/file
```

## 6. Hold the change to its stated intent

Read the pull request title and body, the linked issue and the commit messages, then check the interface delivers what they claim. Look for the **incomplete** change:

- A new variant, size or theme applied to some states but not all: hover, focus, active, disabled, loading, selected.
- A new user-facing string with no entry in the project's translation catalogue.
- A new component with no empty, loading, error, disabled or narrow-width state.
- A control added to one surface but not to siblings that carry its peers.

Do not report scope creep.

## 7. Hand the review back

Continue with [index.md](index.md) steps 3 to 10, carrying the scope block, the affected surfaces and a status on every finding.

## 8. Never mutate the working tree

Read-only, including the checkout. `git fetch` of pull request refs is permitted. `gh pr checkout`, `git checkout`, `git switch` and `git stash` are never permitted.

Mark visual and runtime claims **Not verified** unless the project exposes a cheap preview or the user asks for a rendered review. Then use an isolated worktree under the user's configured worktree root (never `/tmp`), checked out at `refs/remotes/pr/<n>`, and remove it when done.

## Review output format

Open with the scope block:

| Field | Value |
| --- | --- |
| Target | `branch`, `working`, `staged`, `pr 482`, or the range as entered |
| Base ref | `origin/main` at `a1b2c3d` |
| Head ref | `refs/remotes/pr/482` at `e4f5g6h` |
| Commits | 7 committed, 2 files uncommitted |
| Files in scope | 12 after exclusions |
| Excluded | `pnpm-lock.yaml`, `src/__snapshots__/`: lockfile and snapshots |
| Surfaces expanded | `CheckoutPage`, `SettingsPanel`; 3 further `Button` consumers not expanded |

The coverage table follows unchanged; a domain with no evidence in the change scope is `Not reviewed: no evidence in the change scope`.

Then the findings, with a `Status` column:

| Severity | Domain | Status | Location | Before | After | Why |
| --- | --- | --- | --- | --- | --- | --- |
| HIGH | Accessibility | Regression | `src/Dialog.tsx:42` | `aria-label="Close"` removed in this change | Restore `aria-label="Close"` on the icon-only control | The close control had an accessible name before this change and no longer does |

With no `Introduced` or `Regression` findings, omit the table and state "No actionable interface findings in this change."

Then `Pre-existing` findings, at most three, highest severity first, stated as not this change's responsibility. Omit the section when there are none.

| Severity | Domain | Location | Issue |
| --- | --- | --- | --- |
| MEDIUM | Typography | `src/Toolbar.tsx:7` | Numeric badges use proportional figures; predates this change |

The cap and the verdict cover `Introduced` and `Regression` only; a change whose only findings are pre-existing is an `Approve`. End with `Block` when any `HIGH` remains and `Approve` otherwise, leaving remaining findings as work to do.
