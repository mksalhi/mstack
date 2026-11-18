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

1. Anchor on the user's newest intent.
2. In a workspace, check `git status --short --branch`, recent commits and PR status.
3. Include only durable facts: workspace, branch, PR, latest commit; goal and constraints; what's done; what was validated and how; blockers, risks and pending decisions; the exact next step.
4. Flag dirty or unpushed work, branch mismatches, pending migrations, tests not run, and auth or tooling blockers.
5. End with "Good next step".

When the user wants something to paste, output a fenced `text` block. Omit empty sections; use terse bullets.

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

- Give exact filenames, branches, PR numbers, commands and counts.
- Keep the user's intent apart from inferred next steps.
- Leave out speculation, abandoned tasks, and why the handoff exists.
- Mention a skill or workflow you created or changed outside the handoff text.

## Resume

Rebuild the user's recent working context and return a short capsule of where things stand and what to do next. Context lives in two places: chat history, and the shared record the `why` skill searches (source control, issue tracker, team chat, docs, error tracking), which holds user-reported symptoms, reverted fixes and live errors. Don't rebuild from transcripts alone.

Read this project's transcripts per `<mstack>/skills/mstack-mode/references/transcripts.md`. Never glob ~/.claude/projects/*/.

1. Route. What changed in this chat since the user's last message: Catch up mode. One specific prior chat: the `session-pickup` playbook. Turning habits into a skill: `automate-me`. Summary for the next session: Write mode. If the user gave a full state capsule (paths, branch, the change), use it and skip mining.
2. Lock scope before searching: window (default last 7 days), topic if named, workspace (default the active one; never read another project's transcripts unasked). State the scope back. Never quietly turn "all" into "recent N".
3. Fan out over chat history: parallel subagents on a fast, cheap model, one slice each. Each orders candidates by real mtime (`ls -t`), never UUID name; greps the topic first, then reads only matching chats and regions; skips the current chat and noise (subagent, eval, test chats). Each returns one block per chat, citing the chat UUID: topic, user's goal, decisions, open threads, struggles and corrections, artifacts (PRs, tickets, branches). For one or two chats, search directly. Raw transcripts stay in subagents.
4. Sweep the shared record whenever the topic names a feature, file, subsystem, area, or bug ("my work on X" is not exempt). Use the `why` skill's source investigators and per-source playbooks with the question "what's the current state, what's been tried and didn't hold, what are users still reporting". Run in parallel with step 3, one investigator per source. Null results are findings; skip an unavailable MCP and say so. Skip the sweep only for pure activity recall with no named target ("what did I do this week").
5. Verify PRs, branches, and tickets from steps 3-4 with `git` and `gh`. When the answer hinges on what an agent actually did (tools, files, errors), read the full transcript, not a trimmed copy.
6. Reply with the brief to the contract below, grouped by thread, on the named topic.

### Output contract

Order: capsule, threads, problems, next move. Deeper detail goes below or is cut.

- **Capsule.** At most 5 bullets: what the work is and where it stands.
- **Threads.** One line each with exactly one tag: `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[verified, uncommitted]`, `[reverted #N]`, or `[planned, not started]`. Untagged means not done, so tag it.
- **Problems.** At most 5 recurring ones, including user-reported symptoms and shipped-then-reverted fixes.
- **Next move.** The single most useful concrete action.

Exclude adjacent features or tickets unless they block this one. Past one screen, cut detail before threads. Apply the unslop pass (`<mstack>/skills/writing/unslop.md`). Cite chat findings by UUID and shared-record findings by source (PR #, ticket ID, chat permalink, error-tracker issue). Sanitize private context before public output.

## Catch up

For 'ketchup', 'what did I miss', 'what needs me': this chat only.

Catch the user up on what changed in this chat since their last message before they asked (notifications and subagent results are not their messages), then lay out every call waiting on them so they can decide from your reply alone. Assume they remember their last message and nothing after.

Use plain words and short sentences. Say what changed for the user, not how ("the tests pass", not "CI is green"). Leave out hashes, paths, commands, build numbers and test counts unless needed to act. Name each PR, branch or agent the way the user knows it.

### Gather

- This turn is read-only: no code changes, no starting apps or jobs, no posting.
- Collect your work since that message, subagent reports, and others' messages in this chat. Check the current state of each PR, CI run or agent this chat touched. Check every number against its source.
- An action item is a call only the user can make: a product choice, an approval, an irreversible action, access you lack. Include ones raised before their last message. Work you can do yourself is not one. Never invent one.
- One call can cover many items (e.g. several PRs awaiting merge). Per item collect: link, what it changes for users, evidence for your pick, risk, your pick. Write "unknown" for a fact you lack.

### Write the reply

Budget: under 100 words for what happened, less when less happened; about 30 words per action item. Never drop items to fit the budget.

1. One sentence naming what waits on the user, or that nothing does. If nothing happened and nothing waits, say so and stop.
2. What happened. Screenshots and videos the work produced come first, then any diagram. Then one bullet per thing the user asked for: what came of it, and whether it is done, running, failed or unchecked, written as spoken ("Search was slow from a missing index"). Each line stands alone; never mark done what waits on the user. Then at most three lines that change what the user knows or must do, and one line on work left that you can do.
3. Action items. State the call (merge, approve, pick) and your pick, with any prerequisite and anything irreversible, and the number or link of each PR, issue or agent.
   - One item: one bullet with the call, pick, user-facing change, evidence and risk.
   - Shared call: the call and pick once, then one bullet per item, riskiest first.
   - Always give the risk, even low ("Low risk: only the colors change."). Mention the cost of waiting only beyond delay (a deadline, lost data).
   - Between options: give each option's gain, cost and current state; the costs are the risk.

### Visuals

A visual is a screenshot, video, Mermaid diagram, chart or generated image; a Markdown table is not.

- Draw only when a picture beats sentences: how a system works, a PR stack with states, before and after, options side by side. Never draw a status list or unconnected boxes.
- At most six boxes of eight words each, labeled in plain speech.
- Embed screenshots for visible changes. A visible change without one gets "No screenshot yet" plus what changed on screen.
- Never invent a number or show a screen you did not capture. Link only existing artifacts.
