---
name: verifier
description: "Use to create or maintain a project skill that drives the app like a user to prove changes work. Triggers: 'make a verify skill'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Verification skill

A `create` or `maintain` argument picks the mode. Otherwise use **Create** when the project has no `.claude/skills/verify-*` skill and **Maintain** when it has one, and say which.

## Create

Generate `.claude/skills/verify-<app>/`: launch the real app, drive a feature like a user, capture evidence. Write for an agent who has never seen the app.

### 1. Interview the repo, not the user

Ask the user only what you cannot observe in the codebase:

- **Surface:** what does a user touch (web UI, CLI/TUI, desktop, API, mobile, library)? Pick the primary one; note the rest.
- **Run:** the repo's own documented dev command (package scripts, Makefile, README). Note ports, env vars, seed data, auth.
- **Drive:** existing harnesses first (Playwright/Cypress specs, expect scripts, PTY helpers, curl-able endpoints, a debug port); then a generic recipe: browser/CDP for web and Electron, tmux/PTY for CLI/TUI, plain HTTP for services.
- **Observe:** screenshots, terminal transcripts, response bodies, logs, exit codes, DB state.
- **Isolate:** can two instances run side by side (ports, data dirs, profiles)? If not, the generated skill says so and refuses to double-drive a shared instance.

If the checkout doesn't build or start, fix that (or report it precisely) before generating. If an irrelevant missing asset blocks startup (a static dir the API never serves, a sample config), the generated skill may create it, marked as verification scaffolding, and remove it in cleanup.

### 2. Generate the skill

Write `.claude/skills/verify-<app>/SKILL.md` with YAML frontmatter (`name: verify-<app>` and a `description` naming the app, the surface, and when to reach for it; without frontmatter it never registers) and these sections, grounded in the interview, no placeholders:

- **Launch:** exact start command, readiness signal (log line, port answering, prompt), and teardown. Short-lived CLI/TUI: build (or install deps) once, then start each drive in its own isolated PTY or tmux session.
- **Doctor:** one read-only "worth driving?" check: process up, right version/build, port owned by us, auth valid. Run first whenever anything looks off.
- **Drive:** the harness recipe with this repo's real selectors/commands. Prefer stable handles (ARIA labels, data attributes, prompt strings, route paths) over coordinates and tab order.
- **Evidence:** what to capture and where. Proof standards: real user path, not internal setters or test-only endpoints; capture the action and resulting state, not just the final screen; verify side effects (files written, rows inserted, messages sent); mocks only where a production boundary already isolates the external system. For a dry-run or test mode, observe what it actually skips (files, network, git refs); some still touch the network or open a browser.
- **Cleanup:** kill what you started, never by process name. Remove instances and scratch state, never evidence; proof artifacts survive at a location the skill names.
- **Helpers:** shipped scripts are executable, with invocation shown in the skill body.

### 3. Seed the feature map

Create `.claude/skills/verify-<app>/features/README.md` plus one file per user-facing feature (top 3-5 to start, from routes, commands, menus, or docs). Open [`references/feature-map-example/README.md`](references/feature-map-example/README.md) and its sample feature file [`search.md`](references/feature-map-example/search.md) when writing the map's README and first feature file. Each feature file says, from the user's POV, what the feature is, how to reach it, how to drive it, and what observable end state proves it. The four H2s: `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, `Gotchas`. The map is the verification source of truth: a proof driving one convenient entry point is incomplete when the map lists others.

### 4. Prove the generated skill before handing it over

Run it end to end once: launch, doctor, drive ONE mapped feature, capture evidence, clean up. After cleanup, confirm the evidence still exists at the named location. Fix failures, running the generated cleanup after every failed iteration. A never-executed skill is a draft, not a deliverable.

### 5. Hand over

Point the user at `/mstack:verifier maintain`.

## Maintain

- Edit only the verification skill's directory. Never edit product code. Report a product regression instead of fixing it.
- Cover every feature file from source, then drive every feature live at least once, even when source looks clean. Doctor before the first drive and after any failed drive.
- Evidence survives every cleanup. Call a feature unreachable only with the concrete prerequisite and the route attempted.
- End on one outcome and say which: clean (no branch, no PR), changed (one PR of proven corrections), or blocked (say exactly what blocked it).
- Open [references/maintain.md](references/maintain.md) before starting and follow its pass, steps 0 to 6.
