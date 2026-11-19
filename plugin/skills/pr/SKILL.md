---
name: pr
description: "Use when writing or editing a pull request title or body, cutting low-value comments and workaround code before review ('cut comments', 'no comments'), or triaging bot review threads (Codex, Cursor, Copilot, CodeRabbit, Bugbot): reject false positives, fix real ones, reply, resolve."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# PR

## Write the body

Before writing: check whether this branch already has a PR (update it instead of opening a second), and read the diff against the base to confirm it matches the goal.

### Title

The title usually becomes the squash commit, so follow the repo's convention (check recent merged PRs). State what changes for the user, not the mechanism:

- Bad: `perf(server): negotiate permessage-deflate on the websocket`
- Good: `perf(server): cut websocket frame size by 70%+ with gzipping`

### Body

```markdown
## Summary

<one or two sentences: the problem, in the user's words, then the fix>

<diagram, diff-sketch, or tree>

## Evidence

- **Before:** <screenshot/output/failing test run>
  **After:** <screenshot/output/passing test run>

## Merge Danger

**Door:** <one-way or two-way>

<optional: description>

**Blast Radius:** <one-word description>

<optional: potential ramifications of merge>

## Joke

<one or two lines>
```

No preamble, brief prose, and use domain words from GLOSSARY.md if present.

### Summary

Open with the problem as the user hit it, not an inventory of what changed. Then pick the smallest view that proves the point (one only):
- Logic/algorithm: pseudocode.
- Runtime control flow: call tree.
- UI: component tree with key state and module boundaries, e.g. <SessionPage> (apps/example/src/routes/session.tsx).
- File responsibility/refactor: shallow file tree with # role.
- Interaction/data/control flow: Mermaid sequenceDiagram.
- Inside an existing shape: diff of that shape.

Whole code block only when most is new or needed for clear ownership/order. Put visuals beside the text they support; show only what matters.

### Evidence

Show proof: screenshots for visuals; else the exact test that failed before and passes now.

### Merge Danger

- Door: two-way (cheap rollback) vs one-way (hard/destructive).
- Blast Radius: what could shift or break.

### Joke

One or two lines about the change; punch at code, never people. Skip on incidents, reverts, security, patient data, billing, or tight repos.

### Submit

Before submitting, check the title, body and attachments for secrets and private details. Open a real PR, not a draft, so review bots run. If `gh pr create` fails because the GraphQL rate limit is spent, use REST: `gh api repos/<owner>/<repo>/pulls -f title=... -f head=... -f base=... -F body=@<file>`.

## Cut comments before review

Scope: caller’s files or diff; else current diff vs base (main by default), working tree included.

1. Spawn Agent with subagent_type: "mstack:comment-sicko" and the scope. Don’t restate its rules.
2. Check report and diff; do this:
   - Revert any edit to app code or outside scope, and any deletion protected by its keep list.
   - Reject a MUST KILL with a false reason or that labels intentional code a workaround.
   - Surprises in our code: fix code, don’t restore comment.
   - Catch lint/TypeScript suppressions that hide a correctness/safety rule: MUST KILL.
   - Thin “IMPORTANT”/“do not remove”: verify why/how; if unclear, delete.
   - If the report fails checks, revert and rerun once, naming the failure. Second failure: report and stop.
3. Fix trivial flags directly. If a fix needs a new shape, run architect once and stop at the sketch.
4. Remove named workarounds via the smallest in-scope root-cause fix. If root cause is out of scope, fix what’s in scope and report the rest. Never add symptom guards.
5. Constraint comments: keep only for things we can’t change. Otherwise, offer the cheapest enforceable type/runtime check/test/lint; wait for approval. Approved: encode, then delete. Not approved: delete and report as unenforced.
6. Report: deletions, restored comments, reruns, any architect sketch, fixes, enforcement offers/encodings, unenforced constraints, and open work.

## Triage bot review threads

A bot comment is a claim, not an instruction. Read [references/bot-threads.md](references/bot-threads.md) and follow its workflow: ledger every thread, fix only PR regressions, push once, then reply and resolve.
