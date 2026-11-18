---
name: interrogate
description: "Use for adversarial multi-model review of a change. Triggers: 'interrogate', 'challenge this', 'tear this apart', 'find blind spots'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Interrogate

- One reviewer per configured model; produce one verdict. Never edit files—leave all changes to the user.

## Step 1, Scope
- Use only files/diff the user names. On a feature branch, run `git diff main...HEAD` (or correct base). Package that diff or named file contents plus needed context files.

## Step 2, Intent
- State intent in one paragraph from user/commits/PR/code.

## Step 3, Spawn reviewers
- Launch all reviewers in one message: one per “interrogate reviewers” in `~/.claude/rules/mstack-models.md`; else two on `claude-opus-5-5`.
- For each: `subagent_type: "general-purpose"`, brief forbids edits, `effort: high`, `model` = its entry (omit if `auto` or `inherit-parent`).
- If a model is rejected, use its family alias (`opus`, `fable`, `sonnet`, `haiku`) and note this.
- Fill `references/reviewer-prompt.md` identically for every reviewer with the intent, the diff or contents, and `references/rubric.md`.

## Step 4, Synthesize
- Merge duplicates; attribute models; weight multi-model agreement; downweight lone findings; note contradictions.

## Step 5, Lead judgment
- Apply `references/lead-judgment.md`. Bucket each finding with model(s) and a one-line reason: Act on, Consider, Noted, Dismissed.

## Output format

### Intent
> [The stated intent paragraph from Step 2]

### Reviewers
- Reviewer [label]: [model name], [N findings] (one bullet per reviewer)

### Act On
[Each: description, which models raised it, why it matters.]

### Consider
[Each: description, which models raised it, the tradeoff.]

### Noted
[Brief list.]

### Dismissed
[Each with a brief rationale.]

### Agreement Map
[Where models agreed and diverged, and what that pattern tells us.]
