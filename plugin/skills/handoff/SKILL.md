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

- Route first. This chat since the user's last message: Catch up. One prior chat: mstack-mode's `session-pickup` playbook. A full state capsule from the user: use it, skip mining.
- Lock scope before searching (default last 7 days, active workspace) and state it back. Never quietly turn "all" into "recent N".
- Reply with capsule (at most 5 bullets), threads (one tagged line each, such as [merged #N] or [in flight <branch>]), problems (at most 5), then the single next move.
- Open [references/resume.md](references/resume.md) before searching, for the fan-out, sweep, verification and tags.

## Catch up

This chat only, read-only.
- Check the current state of every PR, CI run or agent this chat touched, and every number against its source.
- An action item is a call only the user can make, including ones raised before their last message. Never invent one.
- Reply in order. 1) One sentence on what waits on the user, or that nothing does (if nothing happened either, stop). 2) What happened, under 100 words, one bullet per user ask with its status. 3) Action items, about 30 words each, never dropped: the call, your pick, anything irreversible, the risk even if low, and the PR or agent number. Riskiest first.
- Embed screenshots for visible changes, else say "No screenshot yet". Never show a number or screen you did not check.
- Open [references/catch-up.md](references/catch-up.md) when the reply needs a drawing or several action items share one call.
