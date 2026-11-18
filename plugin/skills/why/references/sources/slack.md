# Slack Conversations

- Inspect Slack MCP tool schema first; may require mcp_auth. If auth fails: stop; invent nothing; report Slack unsearchable.

Search:
1) Author-bounded around merge date.
2) PR URL or /pull/<number>.
3) Specific error string.

Pitfalls:
- Retention cliff: note earliest available date.
- DMs unsearchable.
- Jokes aren’t decisions.
- Always fetch full thread for context.
