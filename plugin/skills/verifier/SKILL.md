---
name: verifier
description: "Use to create or maintain a project skill that drives the app like a user to prove changes work. Triggers: 'make a verify skill'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Verification skill

Mode
- Create

Goal: Generate .claude/skills/verify-<app>/ to launch the real app, drive a real user-visible feature, and capture evidence. Assume the agent has never seen the app.

Interview the repo (not the user)
- Surface: identify the primary user touchpoint (web UI, CLI/TUI, desktop, API, mobile, library). Note the rest.
- Run: use the repo’s documented dev command (package scripts, Makefile, README). Note ports, env vars, seed data, auth.
- Drive: prefer existing harnesses (Playwright/Cypress specs, expect scripts, PTY helpers, curl-able endpoints, a debug port); else generic: browser/CDP for web/Electron, tmux/PTY for CLI/TUI, plain HTTP for services.
- Observe: screenshots, terminal transcripts, response bodies, logs, exit codes, DB state.
- Isolate: if two instances can’t run side-by-side (ports, data dirs, profiles), the skill states this and refuses to double-drive a shared instance.
- If checkout doesn’t build or start, fix it or report precisely before generating. If an irrelevant missing asset blocks startup, you may create it as verification scaffolding and remove it in cleanup.

Generate the skill
- Write .claude/skills/verify-<app>/SKILL.md with YAML frontmatter (name: verify-<app and a description naming the app, the surface, and when to use it). Without frontmatter it never registers.
- Sections:
  - Launch: exact start command, readiness signal (log line, port answering, prompt), and teardown. Short-lived CLI/TUI: build/install deps once, then start each drive in its own isolated PTY or tmux session.
  - Doctor: one read-only “worth driving?” check: process up, right version/build, port owned by us, auth valid. Run first whenever anything looks off.
  - Drive: this repo’s real selectors/commands. Prefer stable handles (ARIA labels, data attributes, prompt strings, route paths).
  - Evidence: what to capture and where. Use a real user path; capture action and resulting state; verify side effects (files written, rows inserted, messages sent). Note what dry-run/test modes actually skip.
  - Cleanup: kill only what you started (never by process name). Remove instances and scratch state, never evidence; artifacts survive at a named location.
  - Helpers: shipped scripts are executable; show their invocation in the skill body.

Seed the feature map
- Create .claude/skills/verify-<app>/features/README.md plus one file per top 3–5 user-facing features (from routes, commands, menus, docs), following [references/feature-map-example/](references/feature-map-example/).
- Each file H2s: Sub-features; How to get to it (user POV); Driving it with <harness>; Gotchas.
- The map is the verification source of truth; a proof via one entry point is incomplete when the map lists others.

Prove the skill
- Run end to end once: launch, doctor, drive ONE mapped feature, capture evidence, clean up.
- After cleanup, confirm evidence exists at the named location.
- Fix failures, running generated cleanup after every failed iteration.
- A never-executed skill is a draft.

Hand over
- Point the user at /mstack:verifier maintain.
