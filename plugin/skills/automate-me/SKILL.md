---
name: automate-me
disable-model-invocation: true
description: "Use to capture the user's working style or preferences as a personal -mode skill. Triggers: 'automate me', 'update my mode skill'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Automate me

Create one -mode skill. Mine history with <mstack>/skills/mstack-mode/playbooks/authoring-a-skill.md, then run the Unslop pass in <mstack>/skills/writing/SKILL.md>. Exception: for “how I write commit messages”, skip mining; use <mstack>/skills/writing/agents.md>.

0) Check for an existing skill
- Search: .agents/skills/**/*-mode/SKILL.md, .claude/skills/**/*-mode/SKILL.md, ~/.agents/skills/*-mode/SKILL.md for the user’s handle.
- If found, AskUserQuestion: update (default) or start fresh (unless they already said “update”).
- To update: mine only since its last edit (`git log -1 --format=%cI <path>`), ask what changed, edit in place, add sections only for new rules.

1) Mine their history
- Read this project’s transcripts at `~/.claude/projects/<slug>/<session-uuid>.jsonl`, where the slug is the working directory with `/` and `.` turned into `-`. Never glob `~/.claude/projects/*/`.
- Fan out subagents over time slices (e.g., last 2–4 weeks).
- Keep only patterns in 2+ slices; treat single or contradicted prefs as noise.

2) Ask the user
- 1–2 AskUserQuestion rounds with 4–6 options each; allow_multiple: true. Then one free-form.

3) Cluster
- Sections: Response style, Autonomy, Understand first, Subagents, Prose and code, Review and verify, Process, Skills. Only specific, non-default rules. Skip empty.

4) Draft
- Path: keep existing; else .agents/skills/<handle>-mode/SKILL.md (or handle folder), or ~/.agents/skills/<handle>-mode/ symlinked into .claude/skills.
- description: triggers on their name, /<handle>-mode, “work in their style”. One quoted YAML scalar or >-.
- disable-model-invocation: true unless wanted every turn.
- Point to other skills by path. Say “the user”.

5) Iterate
- Show draft, get feedback, cut hard.

6) Land
- Worktree off main, commit, open a PR. Never push to main.
