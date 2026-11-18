---
name: playwright
description: "Use to drive a real browser from the terminal: navigate, fill forms, screenshot, scrape, or debug a UI flow."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
  requires: "npx"
---

# Playwright CLI

Drive a real browser with `playwright-cli` through the bundled wrapper. Stay CLI-first: no `@playwright/test` specs unless the user explicitly asks for test files.

## Prerequisite check (required)

Before proposing commands, run `command -v npx >/dev/null 2>&1`. If missing, pause and ask the user to install Node.js/npm, giving these steps verbatim:

```bash
# Verify Node/npm are installed
node --version
npm --version

# If missing, install Node.js/npm, then:
npm install -g @playwright/cli@latest
playwright-cli --help
```

Prefer the wrapper (it runs `npx --package @playwright/cli playwright-cli`) over a global install unless the repo standardizes on one. Set it once:

```bash
export PWCLI="${CLAUDE_SKILL_DIR}/scripts/playwright_cli.sh"
```

## Core workflow

1. Open the page.
2. Snapshot to get element refs.
3. Interact using refs from the latest snapshot.
4. Re-snapshot after navigation, UI-changing clicks, modals/menus opening or closing, tab switches, or a missing-ref failure.
5. Capture artifacts (screenshot, pdf, traces) when useful.

```bash
"$PWCLI" open https://example.com --headed
"$PWCLI" snapshot
"$PWCLI" fill e1 "user@example.com"
"$PWCLI" click e3
"$PWCLI" snapshot
"$PWCLI" tracing-start   # ...interactions... then tracing-stop
"$PWCLI" tab-new https://example.com; "$PWCLI" tab-list; "$PWCLI" tab-select 0
```

Open only what you need: the command list in `references/cli.md`, workflows and troubleshooting in `references/workflows.md`.

## Guardrails

- Always snapshot before referencing ids like `e12`.
- Prefer explicit commands over `eval` and `run-code`.
- Without a fresh snapshot, use placeholder refs like `eX` and say why; don't bypass refs with `run-code`.
- Use `--headed` when a visual check helps.
- Save artifacts under the mstack store or the repo's existing artifact dir; no new top-level folder.
