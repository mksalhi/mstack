---
name: retro
description: "Use for a retrospective on the current coding session. Triggers: 'retro', 'what went wrong', 'lessons from this session'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

Suggest improvements to the coding agent's **environment** for future runs.

## Steps

1. Read `<mstack>/skills/writing/agents.md` for style.
2. Read the primary sources for the session the user names (search session logs on this machine if needed); default to the current one.
3. Find candidates in these categories:

- **Navigation.** Hidden file dependencies, or a **navigation pointer** that would help. _Use when_ finding information took long.
- **Automated checks.** Linting, typing, tests, filesystem linters that would catch the agent's errors. Read the repo's own check command first (`package.json` or build-tool `lint`/`check` scripts, CI workflow): an existing but unwired or silently broken check is the finding, not a reinvention. No **guardrail** (no pre-commit hook and no CI job running lint, typecheck, or test) is itself a finding. _Use when_ a check could have caught a mistake, or there is no guardrail.
- **Coding standards.** Add, remove, or clarify a **reviewer agent** rule. A **mechanical** violation (syntactic pattern, banned API, import shape, file location) gets a deterministic check: a custom rule in the repo's linter, a pre-commit hook, or a CI job, whichever is cheapest. Default to building the check. Reserve `CODING_STANDARDS.md` for **judgement calls** (cross-file consistency, "matches the surrounding style"). _Use when_ the reviewer missed a mistake.
- **Global AGENTS.md.** Steering instructions that belong in coding standards or automated checks. _Use when_ AGENTS.md (repo or global) is large.
- **Tool economy.** Expensive tool calls to streamline; token-inefficient custom CLIs or MCPs. _Use when_ the agent made an expensive call.
- **No-ops.** Steering instructions that don't change behavior. _Use when_ steering files are large.
- **Information access.** E.g. teeing dev server logs, readonly third-party access. _Use when_ key information was unavailable.

4. Present candidates by severity.

## Reference

- The reviewer (gets a diff, least **context pressure**) imposes coding standards, not the implementation agent (explores, writes, debugs; most pressure).
- `CLAUDE.md`/`AGENTS.md`: loaded into every agent's context; use sparingly, mostly **navigation pointers**.
- `CODING_STANDARDS.md`: read during review only; add **navigation pointers** to docs folders past 1,000 lines.
- Docs: reference files pointed to by other files; check for existing docs first.
- Skills: for docs (descriptions enter context) or user-invoked commands, per `<mstack>/skills/writing/agents.md`.
