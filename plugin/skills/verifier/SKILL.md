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

Generate a project-local skill (`.claude/skills/verify-<app>/`) that launches the real app, drives a feature like a user, and captures evidence. Write for an agent reading it cold, mid-task, who has never seen the app.

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

Create `.claude/skills/verify-<app>/features/README.md` plus one file per user-facing feature (top 3-5 to start, from routes, commands, menus, or docs), following [`references/feature-map-example/`](references/feature-map-example/). Each file says, from the user's POV, what the feature is, how to reach it, how to drive it, and what observable end state proves it. The four H2s: `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, `Gotchas`. The map is the verification source of truth: a proof driving one convenient entry point is incomplete when the map lists others.

### 4. Prove the generated skill before handing it over

Run it end to end once: launch, doctor, drive ONE mapped feature, capture evidence, clean up. After cleanup, confirm the evidence still exists at the named location. Fix failures, running the generated cleanup after every failed iteration. A never-executed skill is a draft, not a deliverable.

### 5. Offer the maintenance loop

Point the user at `/mstack:verifier maintain`. Suggest a cadence only if asked.

## Maintain

Upkeep for a project-local verification skill with a feature map. Cover every feature file from source and drive every feature live at least once; not every bullet needs its own drive.

### Outcomes

End on one and say which:

- **clean**: every feature got source and live coverage; nothing to ship. No branch, no PR.
- **changed**: one PR ships proven doc, harness, or map corrections.
- **blocked**: coverage couldn't finish or a proven fix couldn't ship safely. Say exactly what blocked it.

### Edit scope

Edit only the verification skill's directory (SKILL.md, features/, its harness scripts). Never edit product code: behavior the map describes that the app no longer does is doc drift (fix the map) or a product regression (report it).

### Pass

0. **Locate the target**: the project-local skill with launch/drive sections and a feature map (usually `.claude/skills/verify-*/`). Several → ask which; none → stop and point at Create mode.
1. **Index hygiene.** Read the feature map README, glob its siblings, fix missing, extra, duplicate, or dead entries. No generated inventory.
2. **Source wave.** One read-only subagent per feature file, concurrently. Each explains how the feature works from source, flags likely drift with citations, and returns one live-verification recipe. Children never drive the app or edit files. Return shape: feature summary / source entry points / likely drift or none / one recipe.
3. **Reconcile.** Every feature file has a summary. Merge recipes into as few app states as practical. Spot-check cited drift; don't re-prove clean claims. Sweep recent churn for user-facing surfaces missing from the map, citing a concrete source path for each.
4. **Live pass**, required even when source looks clean. The coordinator owns all driving, following the skill's own Launch model (one long-lived instance driven serially for servers/UIs, a fresh isolated session per drive for short-lived CLIs). Exercise every feature at least once. Hold three invariants throughout:
   1. Never drive an instance not health-checked since it last surprised you: doctor before first drive, on each fresh session where sessions are the unit, and after any failed drive; where doctor can't see the failure (wedged UI on a healthy process), reset to a known state or relaunch.
   2. Evidence captured so far survives every cleanup, checked at its named location.
   3. Nothing a drive started outlives its usefulness: clean failed-iteration residue whether the session is stuck, exited, or shared (shared: clean the residue, not the instance).

   A doctor failure caused by skill drift is drift: fix it under edit scope and retry once (restart only what the fix invalidated) before calling the pass `blocked`. A feature is `verified-unreachable` only with the concrete prerequisite (auth, entitlement, OS, external state) and the route attempted; a prerequisite the map omits is drift. Re-drive any triage harness fix live before it ships. Final teardown follows the last drive, including re-proofs; evidence stays.
5. **Triage.** Wrong or missing user-POV description → doc drift, fix it. Working behavior the harness can't drive → harness gap, fix it (helpers rule applies). Actually broken app behavior → product gap; record it for the user, keep it out of this PR.
6. **Ship or stop.** Changed: one PR of proven corrections, re-reading every changed file first. Clean or blocked: no PR; report outcome and coverage honestly.

Keep concise run notes (features covered, unreachable prerequisites, confirmed drift, outcome) in a scratch location; don't commit them.
