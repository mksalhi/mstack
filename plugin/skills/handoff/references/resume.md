# Resume

Rebuild the user's recent working context and return a short capsule of where things stand and what to do next. Context lives in chat history and the shared record the `why` skill searches. Read this project's transcripts per `<mstack>/skills/mstack-mode/references/transcripts.md`. Never glob ~/.claude/projects/*/.

1) Route:
- What changed in this chat since the user's last message: Catch up mode.
- One specific prior chat: the `session-pickup` playbook.
- Turning habits into a skill: `automate-me`.
- Summary for the next session: Write mode.
- If the user gave a full state capsule (paths, branch, the change), use it and skip mining.

2) Lock scope before searching: window (default last 7 days), topic if named, workspace (default the active one). State the scope back. Never quietly turn "all" into "recent N".

3) Fan out over chat history: parallel subagents, one slice each. Order candidates by real mtime (`ls -t`), grep the topic first, then read only matching chats and regions; skip the current chat and noise (subagent, eval, test chats). Each returns one block per chat, citing the chat UUID: topic, user's goal, decisions, open threads, struggles and corrections, artifacts (PRs, tickets, branches). For one or two chats, search directly. Raw transcripts stay in subagents.

4) Sweep the shared record whenever the topic names a feature, file, subsystem, area, or bug ("my work on X" is not exempt). Use the `why` skill's source investigators and per-source playbooks with the question "what's the current state, what's been tried and didn't hold, what are users still reporting". Run in parallel with step 3, one investigator per source. Null results are findings; skip an unavailable MCP and say so. Skip the sweep only for pure activity recall with no named target.

5) Verify PRs, branches, and tickets from steps 3-4 with `git` and `gh`. When the answer hinges on what an agent actually did (tools, files, errors), read the full transcript, not a trimmed copy.

6) Reply with the brief to the contract below, grouped by thread, on the named topic.

## Output contract

Order: capsule, threads, problems, next move. Deeper detail goes below or is cut.

- Capsule. At most 5 bullets: what the work is and where it stands.
- Threads. One line each with exactly one tag: [merged #N], [open PR #N], [in flight <branch>], [verified, uncommitted], [reverted #N], or [planned, not started].
- Problems. At most 5 recurring ones, including user-reported symptoms and shipped-then-reverted fixes.
- Next move. The single most useful concrete action.

Exclude adjacent features or tickets unless they block this one. Past one screen, cut detail before threads. Apply the unslop pass (`<mstack>/skills/writing/unslop.md`). Cite chat findings by UUID and shared-record findings by source (PR #, ticket ID, chat permalink, error-tracker issue). Sanitize private context before public output.
