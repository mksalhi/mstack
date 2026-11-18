---
name: interrogate
description: "Use for adversarial multi-model review of a change. Triggers: 'interrogate', 'challenge this', 'tear this apart', 'find blind spots'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Interrogate

One reviewer per configured model adversarially reviews a change; the signal comes from model diversity, not personas. Deliver a synthesized verdict and leave every change for the user to apply.

## Step 1, Scope

Use the files or diff the user points at; on a feature branch, `git diff main...HEAD` (or the right base); otherwise gather the files of the recent work they reference. Package the diff or contents with any context files reviewers need.

## Step 2, Intent

State the intent in one paragraph from the user's message, commit messages, PR description, and code. If unsure, ask the user before proceeding.

## Step 3, Spawn reviewers

Launch all reviewers in one message, one per entry on the `interrogate reviewers` line in `~/.claude/rules/mstack-models.md`, labeled Reviewer A, B, and so on. Missing rule or line: the table defaults. Set each spawn's `effort` per the **Effort** rule in `mstack-mode`'s Subagents section.

| Subagent | Default model |
|----------|---------------|
| Reviewer A | `claude-opus-5-5` |
| Reviewer B | `claude-opus-5-5` |

Each gets `subagent_type: "general-purpose"`, a brief that forbids edits, and `model` set to its entry or table default; omit `model` for `auto`/`inherit-parent` (parent model). Never treat an alias as a rejected slug or apply the fallbacks below to it.

- Agent tool rejects a configured entry: run that reviewer on its family's table default (`opus`, `fable`, `sonnet`, `haiku`, or full `claude-*` ids; no match: Reviewer A's default) and say so.
- Rejects a table default: use the closest valid slug from the error (same family, most capable), open a separate PR updating the table, and don't block the review.

Fill `references/reviewer-prompt.md` identically for every reviewer with the intent, the diff or contents, `references/rubric.md`, and `references/code-quality-review.md`.

## Step 4, Synthesize

Merge findings that describe the same issue, noting which models raised each. Independent findings from two or more models are the highest signal; weight a lone model's finding accordingly. Note disagreements, especially one model contradicting another.

## Step 5, Lead judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator. Apply `references/lead-judgment.md`. Bucket every finding with its model(s) and a one-line rationale:

- **Act on**: real correctness, security, or maintainability issues given the goals; would block a real PR.
- **Consider**: legitimate, but unclear it outweighs the cost now.
- **Noted**: valid but not actionable (context-dependent, premature optimization, low impact).
- **Dismissed**: wrong, nitpicky, or missing context, with a brief reason.

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
