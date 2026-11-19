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

Drive a real browser with `playwright-cli` through the bundled wrapper. Stay CLI-first: write `@playwright/test` specs only when the user asks for test files.

The wrapper needs `npx`. If `command -v npx` fails, stop and ask the user to install Node.js. Set the wrapper once:

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

Open `references/cli.md` when you need a command not shown here (keyboard, mouse, dialogs, uploads, pdf, console, network) or a `playwright-cli.json` config.

## Guardrails

- Snapshot before using a ref like `e12`; never bypass refs with `run-code`.
- Prefer explicit commands over `eval` and `run-code`.
- When debugging a flow, reproduce it, then capture `console warning` and `network`; wrap the suspicious steps in `tracing-start` and `tracing-stop`, then screenshot.
- If a ref fails, snapshot again and retry. If the page looks wrong, reopen with `--headed` and `resize`. If the flow depends on prior state or another project, use a named `--session`.
- Save artifacts under the mstack store or the repo's existing artifact folder, not a new top-level folder.
