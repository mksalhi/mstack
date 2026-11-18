### Opening a PR

- Worktree: Work from a git worktree off main. For parallel runs use separate worktrees per branch, or reset between runs: `git fetch && git reset --hard origin/<branch>`. If snarled: reset from main and redo minimally.

- Commits: Commit freely; before first push, rebase into small, ordered commits. Amend only if the fix belongs in the last commit. If AGENTS.md forbids rewriting pushed commits, rebase only before the first push.

- Text: Deslop. Title: Conventional Commits `type(scope): subject`, imperative, no period. PR body per <mstack>/skills/pr/SKILL.md: Summary visual, before/after Evidence, Merge Danger. ~40 lines; no full SHAs or file checklists; link an artifact. A commit body does not restate its subject.

- Forge: Resolve once; default `gh`. If `command -v origin` succeeds and Origin resolves the repo, use `origin pr ...`; else record the `gh` fallback. Never require Graphite (`gt`).

- Stacks: Root targets trunk. Each child rebases onto its parent’s tip and targets the parent branch:
  - `origin pr create --status open --base <parent-branch>` or `gh pr create --base <parent-branch>`
  When a parent merges, move the child per playbooks/shipping.md step 4.

- Readiness: Open ready (Origin `--status open`, `gh` no `--draft`). Fix a draft: `origin pr ready <number>` or `gh pr ready <number>`.

- No babysit: Post the URL and continue. Subagent opening a PR runs `interrogate`, deslop, `/mstack:pr`, posts the URL, and returns. Exception: playbooks/babysit.md.
