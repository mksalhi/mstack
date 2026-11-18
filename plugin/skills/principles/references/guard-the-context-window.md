# Guard the context window

**Rule:** Send bulk to subagents, keep summaries. Overflow degrades reasoning and halts progress.

- **Isolate large payloads.** Verbose outputs, screenshots and large documents go to subagents; the main thread gets summaries, not raw data.
- **Keep frequently used content inline.** Templates used on every invocation belong in the skill file, not a separate file that costs a read each time.
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
