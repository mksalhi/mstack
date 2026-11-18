# Slack Conversations

## How to search it

Inspect the available Slack MCP's tool schema first; it may require `mcp_auth`. Auth fails: stop, invent nothing, report Slack as unsearchable.

1. **Author-bounded search:** the PR author's messages around the merge date. Narrows scope dramatically.
2. **PR URL search:** the PR URL, or just `/pull/<number>`.
3. **Error string search:** if the code handles a specific error, search the string; incident threads surface.

## Common pitfalls

- **Retention cliff:** old messages may be gone; note the date nothing exists before.
- **DMs** are unsearchable; a known limitation.
- **Jokes aren't decisions:** "Lol just do the thing" isn't one, even before the commit. Look for considered discussion.
- **Always fetch the thread:** a lone message reads differently out of context.
