---
name: retro
disable-model-invocation: true
description: "Use for a retrospective on the current coding session. Triggers: 'retro', 'what went wrong', 'lessons from this session'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

Suggest improvements to the coding agent's environment for future runs.

Steps
1) Read <mstack>/skills/writing/agents.md> for style.
2) Read primary sources for the named session (search session logs on this machine if needed); default to the current one.
3) Find candidates:
- Navigation: if info took long due to hidden file dependencies, add a navigation pointer.
- Automated checks: prefer existing repo checks first (package.json or build-tool lint/check scripts, CI workflow). Missing/broken guardrails (no pre-commit, no CI lint/type/test) are findings.
- Coding standards: make mechanical rules deterministic (custom linter rule, pre-commit hook, or CI job; choose cheapest). Default to building the check. Reserve CODING_STANDARDS.md for judgement calls (cross-file consistency, matches surrounding style).
- Global AGENTS.md: move steering into coding standards or automated checks when AGENTS.md (repo or global) is large.
- Tool economy: streamline expensive tool calls; flag token-inefficient custom CLIs/MCPs.
- No-ops: remove steering that doesn’t change behavior.
- Information access: enable essentials (e.g., tee dev server logs, readonly third-party access).
4) Present candidates by severity.

Reference
- Reviewer (diff, least context pressure) imposes coding standards; implementation agent does not.
- CLAUDE.md/AGENTS.md load into every agent; use sparingly, mostly navigation pointers.
- CODING_STANDARDS.md: read during review only; add navigation pointers to docs folders past 1,000 lines.
- Docs: reference files already pointed to; check for existing docs first.
- Skills: per <mstack>/skills/writing/agents.md>.
