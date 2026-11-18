# Transcripts

This project's transcripts live in `~/.claude/projects/<slug>/`, where `<slug>` is the absolute working directory with every `/` and `.` turned into `-` (`/Users/you/proj` → `-Users-you-proj`). Each session is `<session-uuid>.jsonl`, one message per line. Its subagents are `<session-uuid>/subagents/*.jsonl`. The current session id is `${CLAUDE_SESSION_ID}`.

Read only this project's directory. Never glob `~/.claude/projects/*/`: it reads private chats from unrelated projects.
