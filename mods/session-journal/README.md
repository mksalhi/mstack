# session-journal

Appends one line per turn to a dated journal file under ~/.claude/journal. A Claude Code mod (a plugin with a hooks module).

## Use

Always on.

## What it does

Appends one line per turn to `~/.claude/journal/YYYY-MM-DD.md`: time, project folder, the prompt's first 100 characters, tool count and files edited.

## Limits


## Files

- `hooks/register.ts`

## Install

See the [repository README](../README.md).
