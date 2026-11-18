---
name: automate-me
description: "Use to capture the user's working style or preferences as a personal -mode skill. Triggers: 'automate me', 'update my mode skill'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Automate me

Turn the user's working conventions into one `-mode` skill (e.g. `jay-mode`): mine their history, write it with the Authoring a skill playbook (`<mstack>/skills/mstack-mode/playbooks/authoring-a-skill.md`), then run the unslop pass (`<mstack>/skills/writing/unslop.md`).

For one narrow workflow ("how I write commit messages"), skip mining and use the playbook with `<mstack>/skills/writing/agents.md`.

## 0. Check for an existing skill

Search `.agents/skills/**/*-mode/SKILL.md`, `.claude/skills/**/*-mode/SKILL.md` and `~/.agents/skills/*-mode/SKILL.md` for the user's handle. If one exists, ask with `AskUserQuestion` whether to update it (default) or start fresh, unless they already said "update". To update: mine only history since its last edit (`git log -1 --format=%cI <path>`), ask what changed, and edit in place, adding sections only for new rules.

## 1. Mine their history

Read this project's transcripts per `<mstack>/skills/mstack-mode/references/transcripts.md`; never glob `~/.claude/projects/*/`. Fan out subagents over slices (e.g. the last 2-4 weeks in 3 slices). Each returns patterns with evidence pointers for:

- reply preferences (length, tone, format, "dumb it down" corrections);
- delegation (subagents, models, parallelism);
- what "done" means (tests, live repro, reviewers);
- code and prose style, principles cited, lint and format tools;
- process (worktrees, commits, PRs, review and merge tools);
- meta habits (fixing skills mid-task).

Keep patterns seen in 2+ slices. A preference stated once and contradicted elsewhere is noise.

## 2. Ask the user

One or two `AskUserQuestion` rounds with 4-6 options each (`allow_multiple: true` for categories), then one free-form question.

## 3. Cluster

Group findings into sections that hold a specific non-default rule: Response style, Autonomy, Understand first, Subagents, Prose and code, Review and verify, Process, Skills. Skip empty sections. "Communicate clearly" is not a rule; "Short paragraphs. Tables when comparing options." is.

## 4. Draft

- Path: keep an existing skill's location. New: `.agents/skills/<handle>-mode/SKILL.md` (or under `.agents/skills/<handle>/` if the repo has a folder for that handle), or `~/.agents/skills/<handle>-mode/` for a personal skill, symlinked into the matching `.claude/skills`.
- `description`: triggers on their name, `/<handle>-mode` and "work in their style", not generic keywords. One YAML scalar; quote it or use `>-`.
- `disable-model-invocation: true` unless the user wants it on every turn.
- Point to other skills by path instead of restating them. Say "the user", not their name.

## 5. Iterate

Show the draft, take feedback, cut hard. Ask the user whether it reads like them and what it missed.

## 6. Land it

Worktree off main, commit, open a PR. Never push to main.
