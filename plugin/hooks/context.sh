#!/usr/bin/env bash
set -euo pipefail

root="${CLAUDE_PLUGIN_ROOT}"
slug=$(printf '%s' "${CLAUDE_PROJECT_DIR:-$PWD}" | sed 's#[/.]#-#g')
text="mstack is installed at ${root} (written <mstack> in mstack skills). Invoke mstack skills as /mstack:<name> or let them fire from their descriptions. When a mstack skill or playbook routes you to another mstack skill, Read <mstack>/skills/<name>/SKILL.md and follow it, resolving its relative paths against that file's directory. The mstack store for this project is ~/.claude/mstack/${slug}/."

if [ "${1:-session}" = subagent ]; then
	printf '{"hookSpecificOutput":{"hookEventName":"SubagentStart","additionalContext":%s}}\n' "$(printf '%s' "$text" | node -e 'process.stdout.write(JSON.stringify(require("fs").readFileSync(0,"utf8")))')"
else
	printf '%s\n' "$text"
fi
