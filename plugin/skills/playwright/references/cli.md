Use the wrapper unless the CLI is installed globally:

```bash
export PWCLI="<this skill's directory>/scripts/playwright_cli.sh"
alias pwcli="$PWCLI"   # optional
pwcli --help
```

```bash
pwcli select e9 "option-value"
pwcli upload ./document.pdf
pwcli eval "el => el.textContent" e5
pwcli dialog-accept "confirmation text"
pwcli screenshot e5
pwcli run-code "await page.waitForTimeout(1000)"
pwcli tracing-start
pwcli tracing-stop
```

```bash
pwcli --session todo open https://demo.playwright.dev/todomvc
export PLAYWRIGHT_CLI_SESSION=todo
```
