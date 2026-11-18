# mods

Claude Code mods, part of [mstack](../README.md). Each folder is a self-contained plugin: a manifest, a hooks module, and a README.

| Mod | What it does | Use |
| --- | --- | --- |
| [sidebar](sidebar/README.md) | One pane for everything, in tiles: live tokens per second, prompt cache, context, this turn's tool calls, files edited, TODOs, prompt history, agents, second opinions and commits. Also keeps context and cache figures in the status line. | `/sidebar`, `/sidebar <tab>`, `/cache`, `/doubt`, `/quick-commit` |
| [session-journal](session-journal/README.md) | Appends one line per turn to a dated journal file under ~/.claude/journal | Always on. |
| [usage-band](usage-band/README.md) | A band above the prompt graphing each rate-limit window (5 hours, week, per-model week) since its last reset. | Always on. |

## Install

From this `mods/` folder, symlink each mod you want into `~/.claude/mods`, then list those paths in `CLAUDE_CODE_PLUGIN_DIRS`
(colon-separated) in `~/.claude/settings.json` and start a new session:

```sh
for m in */; do ln -s "$PWD/${m%/}" ~/.claude/mods/"${m%/}"; done
```

```json
{ "env": { "CLAUDE_CODE_PLUGIN_DIRS": "~/.claude/mods/sidebar:~/.claude/mods/session-journal:~/.claude/mods/usage-band" } }
```

To turn a mod off, remove its path from that list.

## Checking a mod

```sh
claude plugin validate <mod folder>
```

Use the `claude` build that will load the mod: an older CLI rejects hooks modules a newer engine accepts.

## Notes

- Only one mod can draw the band above the prompt. That slot belongs to `usage-band`, which also covers session cost and rate limits. No other mod draws a band.
- `sidebar` includes what the separate `token-rate` mod draws. Load one or the other.
- Built against Claude Code 2.1.286. The mod API is early access and changes between releases.
