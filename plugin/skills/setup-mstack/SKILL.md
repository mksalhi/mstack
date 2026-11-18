---
name: setup-mstack
disable-model-invocation: true
description: "Use to choose which Claude model mstack uses per role. Triggers: /setup-mstack, 'mstack models', 'mstack budget'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Setup mstack

Write `~/.claude/rules/mstack-models.md`, a user-level rule loaded every session that sets mstack's model per role.

## Steps

### 1. Know the models

Agent `model` aliases: `opus`, `fable`, `sonnet`, `haiku`, or a full id (e.g. `claude-opus-5-5`). `inherit-parent` and `auto` are mstack aliases meaning omit `model` (role runs on the parent chat model). Confirm a user-named full id with a one-line Agent call using that `model` before writing it.

### 2. Load current state

Defaults are the step 5 file. If the rule exists, its `# budget` line and role values are the current choices; drop any role not in step 5.

### 3. Budget, map, and confirm

**(a) Ask for a budget** with AskUserQuestion, these exact labels, naming the current budget if recorded:

- `opus 5.5 — claude-opus-5-5 everywhere (mstack default)`
- `mixed — an opus/fable/sonnet table`

**(b) Apply it** to the step 5 defaults; on a re-run keep roles the user changed by hand or set to `inherit-parent`/`auto`. `opus 5.5` keeps the table. `mixed`: code roles, `swarm workers`, `how explorer`, `why investigators` become `sonnet`; every other single role `opus`; every panel list `opus, fable, sonnet` (three seats per panel vs two).

**(c) Confirm** with AskUserQuestion: show every role and model plus each line step 2 dropped; accept as-is or change roles, offering `opus`, `fable`, `sonnet`, `haiku`, `inherit-parent`, `auto`. Panel roles (arena runners, architect runners, interrogate reviewers) are lists: one subagent per entry, aliases included, so length sets the count. `arena cross-judge pool` is a list Arena picks one value from, differing from the parent's model when possible. `swarm workers` is every worker's default unless a race or comparison assigns per-arm models.

### 4. Validate

Every value is `opus`, `fable`, `sonnet`, `haiku`, `inherit-parent`, `auto`, or a full id confirmed in step 1. Otherwise stop and ask again.

### 5. Write the rule

Overwrite the whole file (idempotent re-runs): a `# budget` line with the chosen label, one line per role with mstack-mode's labels, no frontmatter (a rule without `paths` loads every session). Shape:

```
# mstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit-parent` or `auto` as a value: the role runs on the parent chat model (omit Agent `model`). Alias entries in a panel list still count toward its fan-out.
# budget: opus 5.5 — claude-opus-5-5 everywhere (mstack default)
feature, refactoring: claude-opus-5-5
bug-fix: claude-opus-5-5
perf-issue: claude-opus-5-5
hillclimb: claude-opus-5-5
judgment and prose: claude-opus-5-5
hardest tasks: claude-opus-5-5
how explorer: claude-opus-5-5
how explainer: claude-opus-5-5
why investigators: claude-opus-5-5
why synthesizer: claude-opus-5-5
arena runners: claude-opus-5-5, claude-opus-5-5
arena cross-judge pool: claude-opus-5-5, claude-opus-5-5
swarm workers: claude-opus-5-5
architect runners: claude-opus-5-5, claude-opus-5-5
interrogate reviewers: claude-opus-5-5, claude-opus-5-5
```

### 6. Confirm

Tell the user the rule applies to new sessions and that re-running updates it.

### 7. Offer a verification skill (optional)

If the project has no way to drive the real app (no `.claude/skills/verify-*` skill or harness), offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /mstack:verifier." On yes, Read `<mstack>/skills/verifier/SKILL.md` and follow its Create mode. On no, move on.
