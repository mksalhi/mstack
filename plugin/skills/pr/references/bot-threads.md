# Triage bot review threads

A bot comment is a claim, not an instruction. Reject noise with evidence; fix real issues at the smallest shared root cause.

## Scope

- Default: unresolved AI-reviewer threads only. --author adds another AI reviewer; --all-authors only if the user expands scope.
- Replying, resolving, committing, pushing are separate; do only what’s requested.
- Under Babysit/Autopilot owners, their push step authorizes pushing; their loop replaces the one-push rule.

## Workflow

1. Resolve the PR; capture base and head SHAs. List threads: <mstack>/skills/pr/scripts/pr_review_threads.py list [PR] --json (no PR = current branch).
2. Build a ledger: thread, author, file/line, claim, classification, evidence, action. Group duplicates by root cause.
3. Inspect current code and relevant callers; compare against base. Did the PR introduce/worsen it, or just expose it?
4. Classify: pr-regression, already-fixed, duplicate, pre-existing, stale, not-an-issue, needs-user-judgment.
5. Fix only pr-regression. Prefer deletion, existing helpers, stdlib/platform behavior, and one shared fix. No tests written just to satisfy the bot.
6. Run the smallest checks proving the change; re-evaluate the ledger. Never push with a valid actionable thread unaddressed.
7. Only if authorized: push once, after the whole batch is fixed and verified.
8. Reply and resolve only when supported and any fix is visible on the PR. Re-list unresolved AI threads once at the end.

Severe pre-existing security/privacy/data-loss/billing/migration/healthcare issues stay open for user judgment unless policy requires fixing now.

## Replies

One to three factual sentences:
- Yes: why valid, how root cause was fixed, and the passing check.
- No: why false/stale/duplicate/pre-existing, citing decisive code or base comparison.
Never resolve a valid unfixed thread, resolve because a line is outdated, submit a broad review, or close the PR.

## Helper

```bash
python3 <mstack>/skills/pr/scripts/pr_review_threads.py list OWNER/REPO#123 --json
python3 <mstack>/skills/pr/scripts/pr_review_threads.py list --author cursor --json
python3 <mstack>/skills/pr/scripts/pr_review_threads.py reply-and-resolve THREAD_ID --body "Yes. ..."
```
