# Guard the context window

- Offload large payloads to subagents; keep only summaries in the main thread.
- Keep frequently used templates inline in the skill file.
- Cap each phase: limit files, set turn budgets, account for mechanism costs.
