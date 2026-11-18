# Playwright CLI workflows

Assume `PWCLI` is set and `pwcli` aliases `"$PWCLI"`. Snapshot often.

## Form submission

```bash
pwcli open https://example.com/form --headed
pwcli snapshot
pwcli fill e1 "user@example.com"
pwcli fill e2 "password123"
pwcli click e3
pwcli snapshot
pwcli screenshot
```

## Data extraction

```bash
pwcli eval "document.title"
pwcli eval "el => el.textContent" e12
```

## Debugging and inspection

After reproducing an issue, capture `pwcli console warning` and `pwcli network`. Wrap a suspicious flow in `pwcli tracing-start` … `pwcli tracing-stop`, then `pwcli screenshot`.

## Sessions

Isolate work across projects with `--session <name>` on each command, or `export PLAYWRIGHT_CLI_SESSION=<name>` once.

## Configuration file

The CLI reads `playwright-cli.json` from the current directory; `--config` points elsewhere.

```json
{
  "browser": {
    "launchOptions": { "headless": false },
    "contextOptions": { "viewport": { "width": 1280, "height": 720 } }
  }
}
```

## Troubleshooting

- Element ref fails: `pwcli snapshot` again and retry.
- Page looks wrong: re-open with `--headed` and resize.
- Flow depends on prior state: use a named `--session`.
