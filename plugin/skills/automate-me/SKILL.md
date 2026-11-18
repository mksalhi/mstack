---
name: automate-me
description: "Use to capture the user's working style or preferences as a personal -mode skill. Triggers: 'automate me', 'update my mode skill'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Automate me

Turn the user's working conventions into one `-mode` skill (e.g. `jay-mode`): mine history inline, author with the Authoring a skill playbook (`<mstack>/skills/mstack-mode/playbooks/authoring-a-skill.md`), then apply the unslop pass (`<mstack>/skills/writing/unslop.md`).

For a task-specific skill or one narrow workflow (e.g. "how I write commit messages"), skip mining: use the Authoring a skill playbook with `<mstack>/skills/writing/agents.md` and `<mstack>/skills/writing/SKILL-MECHANICS.md`.

## 0. Check for an existing skill

Search recursively `.agents/skills/**/*-mode/SKILL.md`, `.claude/skills/**/*-mode/SKILL.md`, `~/.agents/skills/*-mode/SKILL.md` for the user's handle (it may sit in a category dir like `.agents/skills/<handle>/`). If found, confirm with `AskUserQuestion` unless they already said "update my skill": update (default) or start fresh (rare; ask why).

Update mode:
- Step 1 mines only history since the last edit (`git log -1 --format=%cI <path>`).
- Step 2 asks what changed or is missing.
- Step 4 edits in place: keep uncontradicted sections, revise ones with new evidence, add sections only for new rules.

## 1. Mine their history

Read this project's transcripts per `<mstack>/skills/mstack-mode/references/transcripts.md`. Never glob ~/.claude/projects/*/.

Fan out parallel subagents over slices of history (e.g. last 2-4 weeks in 3 slices). Each reads from the workspace-scoped path the parent provides and returns a short list of patterns with evidence pointers. Signals:

- Response preferences (length, tone, format, "dumb it down" corrections)
- Delegation habits (subagents, models, workflows, parallelism)
- Verification posture (what "done" means, unit tests vs live repro, reviewers)
- Code and prose discipline (style, principles cited, lint and format tools)
- Process conventions (worktrees, commits, PRs, review and merge tooling)
- Meta preferences (fixing skills mid-task, proposing new ones)

Keep patterns seen in 2+ slices; drop lone signals. A preference stated once and contradicted elsewhere is noise.

## 2. Ask the user directly

Use `AskUserQuestion`: one or two questions, 4-6 options each, `allow_multiple: true` for category questions. Start broad ("Which areas matter most?"), follow up on selected areas, then one free-form chat question. No 20-question dumps.

## 3. Cluster findings

Group into sections, only those with a specific non-default rule: **Response style**, **Autonomy** (asking, MCP use), **Understand first** (skills for scoping and investigating), **Subagents** (default, parallelism, model-to-task, workflows), **Prose / code discipline**, **Review and verify**, **Process** (worktrees, commits, PRs), **Skills** (authoring habits, fix-the-skill-first). Skip empty sections; "Communicate clearly" is not a section, "Short paragraphs. Tables when comparing options." is.

Read `mstack-mode` for granularity only; don't copy its content.

## 4. Draft the skill

Author with the Authoring a skill playbook.

- Path: keep an existing mode skill's location. New: `.agents/skills/<handle>/<handle>-mode/SKILL.md` if the repo has a personal category for that handle, else `.agents/skills/<handle>-mode/SKILL.md` (`.claude/skills` symlinked to `.agents/skills`), or `~/.agents/skills/<handle>-mode/` symlinked into `~/.claude/skills` for a personal skill.
- Handle: first name or chosen identifier.
- `description`: trigger on their name + `/<handle>-mode` + "work in their style", not generic keywords. One YAML scalar per `<mstack>/skills/writing/SKILL-MECHANICS.md`; quote it or use `description: >-` when needed.
- `disable-model-invocation: true` unless the user wants it on every turn.
- Operational prose only: reference other skills and principle docs by path, don't inline or restate them. Say "the user", not the author's name.

## 5. Iterate on prose

Apply the unslop pass and `<mstack>/skills/writing/agents.md` to every line. Show the draft, take feedback, iterate, cut hard. No benchmark loop: vibe-check with the user (reads like them? missed anything?). Run a description-optimization loop only if trigger accuracy is a real problem.

## 6. Land it

Worktree off main, commit, open a PR. Never push to main.
