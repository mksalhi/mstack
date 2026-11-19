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
5. Constraint comments: keep only for things we can’t change. Otherwise, encode the cheapest enforceable type/runtime check/test/lint, then delete the comment. Nothing enforceable: delete and report as unenforced.
6. Report: deletions, restored comments, reruns, any architect sketch, fixes, enforcement offers/encodings, unenforced constraints, and open work.

## Triage bot review threads

A bot comment is a claim, not an instruction. Reject noise with evidence; fix real issues at the smallest shared root cause.

- Default scope is unresolved AI-reviewer threads. `--author` adds another AI reviewer; `--all-authors` only when the user expands scope.
- Replying, resolving, committing and pushing are separate; do only what was asked. Under Babysit or Autopilot their push step authorizes pushing and their loop replaces the one-push rule.

1. Resolve the PR and capture base and head SHAs. List threads with `python3 <mstack>/skills/pr/scripts/pr_review_threads.py list [OWNER/REPO#123] --json` (no PR means the current branch; `--author cursor` filters).
2. Ledger every thread with author, file and line, claim, classification, evidence and action. Group duplicates by root cause.
3. Read the current code and its callers and compare against base. Did the PR introduce or worsen it, or only expose it?
4. Classify each as pr-regression, already-fixed, duplicate, pre-existing, stale, not-an-issue or needs-user-judgment.
5. Fix only pr-regression. Prefer deletion, existing helpers, stdlib or platform behavior, and one shared fix. Write no test just to satisfy the bot.
6. Run the smallest checks that prove the change and re-check the ledger. Never push with a valid actionable thread unaddressed.
7. Only if authorized, push once, after the whole batch is fixed and verified.
8. Reply and resolve only when the fix is visible on the PR, with `pr_review_threads.py reply-and-resolve THREAD_ID --body "..."`. Re-list unresolved AI threads once at the end.

- Replies are one to three factual sentences. A yes says why it is valid, how the root cause was fixed, and the passing check. A no says why it is false, stale, duplicate or pre-existing, citing the decisive code or base comparison.
- Never resolve a valid unfixed thread, resolve because a line is outdated, submit a broad review, or close the PR.
- Severe pre-existing security, privacy, data-loss, billing, migration or healthcare issues stay open for user judgment unless policy requires fixing now.
