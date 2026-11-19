# Resume

Rebuild the user's recent working context and return a short capsule of where things stand and what to do next. Context lives in chat history and the shared record the `why` skill searches. Read this project's transcripts at `~/.claude/projects/<slug>/<session-uuid>.jsonl`, where the slug is the working directory with `/` and `.` turned into `-`. Never glob `~/.claude/projects/*/`.

1) Route and lock scope per `SKILL.md` Resume. Also route "turning habits into a skill" to `automate-me` and "summary for the next session" to Write mode. Scope also takes a topic if named.

2) Fan out over chat history: parallel subagents, one slice each. Order candidates by real mtime (`ls -t`), grep the topic first, then read only matching chats and regions; skip the current chat and noise (subagent, eval, test chats). Each returns one block per chat, citing the chat UUID: topic, user's goal, decisions, open threads, struggles and corrections, artifacts (PRs, tickets, branches). For one or two chats, search directly. Raw transcripts stay in subagents.

3) Sweep the shared record whenever the topic names a feature, file, subsystem, area, or bug ("my work on X" is not exempt). Use the `why` skill's source investigators and per-source playbooks with the question "what's the current state, what's been tried and didn't hold, what are users still reporting". Run in parallel with step 2, one investigator per source. Null results are findings; skip an unavailable MCP and say so. Skip the sweep only for pure activity recall with no named target.

4) Verify PRs, branches, and tickets from steps 2-3 with `git` and `gh`. When the answer hinges on what an agent actually did (tools, files, errors), read the full transcript, not a trimmed copy.

5) Reply with the brief to the contract below, grouped by thread, on the named topic.

## Output contract

Order and limits are in `SKILL.md` Resume. Deeper detail goes below or is cut. Thread tags, exactly one per line: [merged #N], [open PR #N], [in flight <branch>], [verified, uncommitted], [reverted #N], or [planned, not started]. Problems include user-reported symptoms and shipped-then-reverted fixes.

Exclude adjacent features or tickets unless they block this one. Past one screen, cut detail before threads. Apply the unslop pass (`<mstack>/skills/writing/unslop.md`). Cite chat findings by UUID and shared-record findings by source (PR #, ticket ID, chat permalink, error-tracker issue). Sanitize private context before public output.
