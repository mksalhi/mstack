Snapshot often.

Debugging: After reproducing an issue, run pwcli console warning and pwcli network. Wrap suspicious flows with pwcli tracing-start … pwcli tracing-stop, then pwcli screenshot.

Sessions: use --session <name> on each command, or export PLAYWRIGHT_CLI_SESSION=<name> once.

Configuration: The CLI reads playwright-cli.json from the current directory; --config points elsewhere.

Troubleshooting:
- Element ref fails: pwcli snapshot and retry.
- Page looks wrong: re-open with --headed and resize.
- Flow depends on prior state: use a named --session.
