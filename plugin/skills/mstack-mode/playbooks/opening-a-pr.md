### Opening a PR

**Worktree.** Work from a git worktree off main; subagents inherit it. Parallel `Agent` calls on one branch each get their own worktree, or `git fetch && git reset --hard origin/<branch>` between them. Unrelated work on the branch: patch out, fresh worktree, apply. Snarled worktree: reset from main, redo minimally.

**Commits.** Commit liberally, then rebase into small, ordered, landable commits (each a future PR) before opening PRs. Amend when the fix belongs in the last commit. If AGENTS.md forbids rewriting pushed commits, rebase only before the first push.

**Text.** Deslop and cut comments (SKILL.md Routing). Write titles, bodies, and commit messages with `writing` (all layers except Diátaxis, plus STE vocabulary: one word per action, keep articles, plain verb over `-ing`), ending with its unslop pass.
- Title: Conventional Commits `type(scope): subject`, no trailing period. Types like `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`; scope is the area (`mstack`, `mstack-mode`); imperative subject naming the real symbol, e.g. `fix(mstack): retarget opening-a-pr babysit trigger`.
- Body: the `pr` skill (`<mstack>/skills/pr/SKILL.md`), with Summary visual, before and after Evidence, Merge Danger. Under about 40 lines (it becomes the squash commit). No full SHAs, lane recitals, or file checklists; link an artifact. A commit body does not restate its subject.

**Forge.** Resolve once before the first PR operation and keep it. Default `gh`. If `command -v origin` succeeds and Origin resolves the repo, use `origin pr ...`; otherwise record the `gh` fallback. Never require Graphite (`gt`).

**Stacks.** Prefer five narrow PRs to one large one. Root PR targets trunk; each child rebases onto its parent's exact tip and targets the parent branch (`origin pr create --status open --base <parent-branch>` or `gh pr create --base <parent-branch>`; retarget with `origin pr edit <pr> --base <parent-branch>` or `gh pr edit <pr> --base <parent-branch>`). When a parent merges, move the child per `playbooks/shipping.md` step 4. Branch from trunk only for independent work. Rebase on trunk before substantial stack work.

**Readiness.** Open ready, never draft (Origin `--status open`, `gh` without `--draft`); fix a draft with `origin pr ready <number>` or `gh pr ready <number>`. Run `origin pr view <number>` or `gh pr view <number>` before stating PR status.

**No babysit.** Post the URL and keep building. Babysit only when the user asks, after the whole stack exists. Push back when feedback drifts from intent. A subagent that opens a PR runs `interrogate`, deslop, and `/mstack:pr`, posts the URL, and returns. Exception: an Autopilot-full or Autopilot-stack owner, whose brief is the babysit ask `playbooks/babysit.md` waits for; it starts the loop after its code-ready report, reports merge-ready or STACK-READY, and is exempt from the hold-until-stack-built rule.
