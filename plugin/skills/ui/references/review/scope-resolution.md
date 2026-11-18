# Scope resolution

## Default branch

Try `refs/remotes/origin/HEAD`, then `gh repo view --json defaultBranchRef`, then `init.defaultBranch`. If the ref is missing, run `git remote set-head origin --auto` rather than guessing (writes only under `.git`, so permitted; note it in Verification). With no remote, fall back to a local `main` or `master` and state the assumed base.

## Targets

Accepted: `working`, `staged`, `branch`, `pr <n>`, a bare `<ref>`, and an explicit `<a>..<b>` or `<a>...<b>` range. Anything else is a `<ref>`.

Diff a branch against the **merge base**, three dots; two dots counts upstream commits as part of the change. When the user wrote a range, keep their dots: `<a>..<b>` compares endpoints, `<a>...<b>` compares `merge-base(<a>, <b>)` with `<b>`. State the resolved range in the scope block.

`git diff HEAD` reports tracked changes only. Any target with uncommitted work must add `git ls-files --others --exclude-standard`, or new files drop silently. For `branch` with uncommitted work, report the two counts separately.

## Pull requests

Fetch the head into a remote-tracking ref and review it in place (works for forks):

`git fetch origin "pull/<n>/head:refs/remotes/pr/<n>"`

Read files with `git show refs/remotes/pr/<n>:path/to/file`, never the working-tree copy. `gh pr diff <n>` gives patch text only; fetch the ref too for context and consumers.

**Citations.** Cite `path/to/file:line` against the head ref, and declare that ref and its SHA in the scope block.

**Intent.** The `title` and `body` from `gh pr view` are the stated intent; add commit subjects when the body is empty.

## Awkward repository states

Anything not below fails loudly at `merge-base` (no remote, unrelated histories, no commits, moved submodule pointer): say the base is unresolvable and stop. Never review a range you cannot name.

**Detached HEAD.** Use the merge base against the default branch and name the SHA in the scope block.

**Shallow clone** (`merge-base` returns nothing). Fetch `--deepen=50`, retry, then `--deepen=200`, then report the scope unresolvable. Permitted; note it in Verification.

**Mid-rebase or mid-merge.** `git diff` succeeds but returns the wrong thing. Detect with `git rev-parse --git-path` against `rebase-merge`, `rebase-apply`, `MERGE_HEAD` and `CHERRY_PICK_HEAD` (not raw `.git/` paths, which fail in linked worktrees). Stop and say the tree is mid-operation.

## Nothing to review

Clean tree, `HEAD` not ahead of the merge base. Gather: current branch, tree cleanliness, count ahead of base, last commit's SHA and subject, any open pull request from `gh pr status`.

`gh pr status` omits `currentBranch` when no pull request is open; that is an answer, not an error. If it fails (no `gh`, no auth, no GitHub remote), say "no pull request found" and offer the remaining routes.

Report the facts, then offer the three routes in [change-review.md](change-review.md) step 2, with the last commit's SHA and subject inside the offer. A whole-repository audit runs through [index.md](index.md) as a repository-scope review, without scope block, statuses or pre-existing section.

## Renames

`--name-status` reports `R100 old/path new/path`. Use `--find-renames=40% --find-copies-harder` when a file was moved and edited. Review a rename as a move: only genuine edits are in scope.

## Excluded paths

Exclude these and name them in the scope block:

| Category | Patterns |
| --- | --- |
| Lockfiles | `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lock`, `bun.lockb`, `Cargo.lock`, `composer.lock`, `Gemfile.lock`, `poetry.lock`, `uv.lock` |
| Snapshots and fixtures | `__snapshots__/`, `*.snap`, `*.approved.*`, `test-results/`, `playwright-report/` |
| Generated output | `dist/`, `build/`, `out/`, `.next/`, `.turbo/`, `.svelte-kit/`, `coverage/`, `storybook-static/`, `*.min.js`, `*.min.css`, `*.map` |
| Generated sources | `*.gen.ts`, `*.generated.*`, `*.d.ts` emitted by a build, GraphQL and Prisma client output |
| Vendored code | `vendor/`, `third_party/`, `node_modules/` |
| Binaries and media | `*.png`, `*.jpg`, `*.webp`, `*.avif`, `*.woff2`, `*.mp4`, `*.pdf` |

Exceptions: a **font file** added or swapped is a typography change; an **image** added to a component is a polish and accessibility change. Review the code that references them, not the bytes.

Apply exclusions as pathspecs so the scope count is the reviewed count. Cover every lockfile name (`*.lock` misses `package-lock.json` and `pnpm-lock.yaml`). `**` needs `glob` magic, or `**/dist/**` misses a root-level `dist/`. Run the diff with and without the pathspecs and confirm the count dropped by exactly the files you named.

## Expanding to consumers

One hop, two for tokens and primitives. Use the project's resolver where one exists, otherwise import paths.

Pass the reviewed ref to `git grep` after the pattern, or on a pull request you search the wrong revision. Read `<rev>:path/to/file` results with `git show`. Pass `-e` when the pattern starts with a dash (`--color-*`). For a changed token or theme value, search the token name, not the file.

Order consumers reproducibly:

1. **Route and layout entry points first**: `app/**/page.*`, `app/**/layout.*`, `pages/**`, `routes/**`, `src/views/**`, `*.astro` pages, or the framework's equivalent.
2. **Then by importer count**, most first.
3. **Ties by proximity**: same package or feature directory first.

Review the first five, state how many you did not expand, and say if the ordering was arbitrary past a point.
