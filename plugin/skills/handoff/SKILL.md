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

Read [references/resume.md](references/resume.md) and follow it: route, lock scope, fan out over chat history, sweep the shared record, verify, reply to its output contract.

## Catch up

For 'ketchup', 'what did I miss', 'what needs me': this chat only. Read [references/catch-up.md](references/catch-up.md) and follow it: gather read-only, then reply with what waits on the user first.
