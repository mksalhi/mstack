---
name: handoff
description: "Use to pass work between sessions: 'handoff', 'summarize for the next chat' (write); 'where did I leave off', 'catch me up on my recent work' across past sessions (resume); or 'ketchup', 'what did I miss', 'what needs me' in this chat (catch up)."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Handoff

Run the mode named by the `write`, `resume` or `ketchup` argument; otherwise infer it and say which.

## Write

Leave a summary another session can continue from without rereading the thread: state, not story.

- Anchor on the user's newest intent.
- In a workspace, check `git status --short --branch`, recent commits and PR status.
- Include only durable facts: workspace, branch, PR, latest commit; goal and constraints; what's done; what was validated and how; blockers, risks and pending decisions; the exact next step.
- Flag dirty or unpushed work, branch mismatches, pending migrations, tests not run, and auth or tooling blockers.
- Give exact filenames, branches, PR numbers, commands and counts.
- Keep the user's intent apart from inferred next steps. Leave out speculation, abandoned tasks, and why the handoff exists.
- When the user wants something to paste, output a fenced `text` block. Omit empty sections; use terse bullets.
- End with "Good next step".
- Mention a skill or workflow you created or changed outside the handoff text.

```text
Workspace:
Branch:
PR:
Latest relevant commit:

Goal:

Current state:

Completed:

Validation:

Important constraints:

Known issues / blockers:

Good next step:
```

## Resume

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

### Output contract

Order: capsule, threads, problems, next move. Deeper detail goes below or is cut.

- Capsule. At most 5 bullets: what the work is and where it stands.
- Threads. One line each with exactly one tag: [merged #N], [open PR #N], [in flight <branch>], [verified, uncommitted], [reverted #N], or [planned, not started].
- Problems. At most 5 recurring ones, including user-reported symptoms and shipped-then-reverted fixes.
- Next move. The single most useful concrete action.

Exclude adjacent features or tickets unless they block this one. Past one screen, cut detail before threads. Apply the unslop pass (`<mstack>/skills/writing/unslop.md`). Cite chat findings by UUID and shared-record findings by source (PR #, ticket ID, chat permalink, error-tracker issue). Sanitize private context before public output.

## Catch up

For 'ketchup', 'what did I miss', 'what needs me': this chat only.

### Gather

- Read-only. No code changes, apps, jobs, or posting.
- Collect your work since that message, subagent reports, and others' messages in this chat. Check current state of each PR, CI run or agent this chat touched. Check every number against its source.
- An action item is a call only the user can make. Include ones raised before their last message. Never invent one.

### Write the reply

- Budget: under 100 words for what happened; about 30 words per action item. Never drop items to fit the budget.
- 1) One sentence naming what waits on the user, or that nothing does. If nothing happened and nothing waits, say so and stop.
- 2) What happened. Visuals first; then one bullet per thing the user asked for: result and status (done, running, failed, unchecked). Then at most three lines that change what the user knows or must do, and one line on work left that you can do.
- 3) Action items. State the call (merge, approve, pick) and your pick, with any prerequisite and anything irreversible, and the number or link of each PR, issue or agent.
  - Shared call: the call and pick once, then one bullet per item, riskiest first.
  - Always give the risk, even low. Mention the cost of waiting only beyond delay.

### Visuals

- Draw only when a picture beats sentences. At most six boxes of eight words each, labeled in plain speech.
- Embed screenshots for visible changes; otherwise say "No screenshot yet" plus what changed on screen.
- Never invent a number or show a screen you did not capture. Link only existing artifacts.
