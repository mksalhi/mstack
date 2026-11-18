---
name: interrogate
description: "Use for adversarial multi-model review of a change. Triggers: 'interrogate', 'challenge this', 'tear this apart', 'find blind spots'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Interrogate

One reviewer per configured model attacks a change; the signal comes from model diversity, not personas. Deliver one verdict and leave every change for the user to apply.

## Step 1, Scope

Use the files or diff the user points at; on a feature branch, `git diff main...HEAD` (or the right base); otherwise gather the files of the recent work they reference. Package the diff or contents with any context files reviewers need.

## Step 2, Intent

State the intent in one paragraph from the user's message, commit messages, PR description, and code. If unsure, ask the user before proceeding.

## Step 3, Spawn reviewers

Launch all reviewers in one message, one per entry on the `interrogate reviewers` line in `~/.claude/rules/mstack-models.md` (else two on `claude-opus-5-5`), labeled Reviewer A, B, and so on. Each gets `subagent_type: "general-purpose"`, a brief that forbids edits, `effort: high`, and its entry as `model`; `auto` or `inherit-parent` means omit `model`. If the Agent tool rejects a model, run that reviewer on its family alias (`opus`, `fable`, `sonnet`, `haiku`) and say so.

Fill `references/reviewer-prompt.md` identically for every reviewer with the intent, the diff or contents, and `references/rubric.md`.

## Step 4, Synthesize

Merge findings that describe the same issue, noting which models raised each. Independent findings from two or more models are the highest signal; weight a lone model's finding accordingly. Note disagreements, especially one model contradicting another.

## Step 5, Lead judgment

You are the lead reviewer, a pragmatic senior engineer, not a neutral aggregator. Apply `references/lead-judgment.md` and bucket every finding with its model(s) and a one-line reason:

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
