# Playwright CLI reference

Use the wrapper unless the CLI is installed globally:

```bash
export PWCLI="<this skill's directory>/scripts/playwright_cli.sh"
alias pwcli="$PWCLI"   # optional
pwcli --help
```

```bash
# Core
pwcli open https://example.com
pwcli close
pwcli snapshot
pwcli click e3
pwcli dblclick e7
pwcli type "search terms"
pwcli fill e5 "user@example.com"
pwcli drag e2 e8
pwcli hover e4
pwcli select e9 "option-value"
pwcli upload ./document.pdf
pwcli check e12
pwcli uncheck e12
pwcli eval "document.title"
pwcli eval "el => el.textContent" e5
pwcli dialog-accept
pwcli dialog-accept "confirmation text"
pwcli dialog-dismiss
pwcli resize 1920 1080

# Navigation
pwcli go-back
pwcli go-forward
pwcli reload

# Keyboard
pwcli press Enter
pwcli press ArrowDown
pwcli keydown Shift
pwcli keyup Shift

# Mouse
pwcli mousemove 150 300
pwcli mousedown            # or: mousedown right
pwcli mouseup              # or: mouseup right
pwcli mousewheel 0 100

# Save as
pwcli screenshot
pwcli screenshot e5
pwcli pdf

# Tabs
pwcli tab-list
pwcli tab-new
pwcli tab-new https://example.com/page
pwcli tab-close
pwcli tab-close 2
pwcli tab-select 0

# DevTools
pwcli console
pwcli console warning
pwcli network
pwcli run-code "await page.waitForTimeout(1000)"
pwcli tracing-start
pwcli tracing-stop

# Sessions (isolate work), per command or once via env
pwcli --session todo open https://demo.playwright.dev/todomvc
export PLAYWRIGHT_CLI_SESSION=todo
```
