---
name: setup-mstack
disable-model-invocation: true
description: "Use to choose which Claude model mstack uses per role. Triggers: /setup-mstack, 'mstack models', 'mstack budget'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Setup mstack (compressed)

1) Models
- Aliases: opus, fable, sonnet, haiku, or a full id (e.g. claude-opus-5-5).
- inherit-parent and auto: omit model (role runs on parent chat model).
- If user enters a full id, confirm it via a one-line Agent call using that model before writing.

2) Load current state
- Defaults are the step 5 file below. If ~/.claude/rules/mstack-models.md exists, its # budget line and role values are current; drop any role not in step 5.

3) Budget, map, confirm
- AskUserQuestion (name current budget if recorded) with exactly:
  - opus 5.5 — claude-opus-5-5 everywhere (mstack default)
  - mixed — an opus/fable/sonnet table
- Apply to step 5 defaults; on re-run keep roles user changed by hand or set to inherit-parent/auto.
- mixed mapping: code roles, swarm workers, how explorer, why investigators → sonnet; every other single role → opus; every panel list → opus, fable, sonnet.
- AskUserQuestion to confirm: show every role and model plus each line dropped in step 2; allow changes to opus, fable, sonnet, haiku, inherit-parent, auto, or confirmed full ids. Panel roles are lists: length sets fan-out. arena cross-judge pool is a list Arena picks one value from, differing from the parent when possible. swarm workers is every worker’s default unless a race or comparison assigns per-arm models.

4) Validate
- Each value must be opus, fable, sonnet, haiku, inherit-parent, auto, or a confirmed full id. Otherwise stop and ask again.

5) Write the rule
- Overwrite ~/.claude/rules/mstack-models.md; no frontmatter. Shape:
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
council members: claude-opus-5-5, fable, sonnet
```

6) Confirm
- Tell the user it applies to new sessions; re-running updates it.
