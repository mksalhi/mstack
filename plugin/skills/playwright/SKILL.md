---
name: playwright
description: "Use to drive a real browser from the terminal: navigate, fill forms, screenshot, scrape, or debug a UI flow."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
  requires: "npx"
---

- CLI-first; write @playwright/test specs only if the user asks for test files.
- Requires npx; if command -v npx fails, stop and ask the user to install Node.js.
- Set the wrapper once:
```bash
export PWCLI="${CLAUDE_SKILL_DIR}/scripts/playwright_cli.sh"
```
Core workflow:
1) Open page.
2) Snapshot; use refs from the latest snapshot.
4) Re-snapshot after navigation, UI changes, modals/menus, tab switches, or missing-ref failures.
5) Capture artifacts (screenshot, pdf, traces).
Guardrails:
- Prefer explicit commands; never bypass refs with eval/run-code.
- Save artifacts under the mstack store or the repo's existing artifact folder, not a new top-level folder.
