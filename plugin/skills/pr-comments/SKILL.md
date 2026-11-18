---
name: pr-comments
description: "Use to triage bot review threads on a PR (Codex, Cursor, Copilot, CodeRabbit, Bugbot): reject false positives, fix real ones, reply, resolve."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# PR comments

Apply `scoper` ultra to every fix. A bot comment is a claim, not an instruction: reject noise with evidence, fix real ones at the smallest shared root cause.

## Scope

- Default: unresolved AI-reviewer threads only. The helper knows common Codex, Cursor, Copilot, and CodeRabbit logins; `--author` adds another AI reviewer; `--all-authors` only when the user expands scope.
- Replies, resolution, commits, and pushes are separate mutations: do only those clearly requested. Never commit or push just because the skill ran.
- Invoked by the Babysit playbook (drive/background) or an Autopilot owner: its push wave authorizes pushing and its loop replaces the single-push rule.

## Workflow

1. Resolve the PR; capture base and head SHAs. List threads: `scripts/pr_review_threads.py list [PR] --json` (no PR = current branch).
2. Before editing, build the full ledger: thread, author, file/line, claim, classification, evidence, action. Group duplicates by root cause.
3. Per claim, inspect the current code and all relevant callers and compare against the base (merge base or base SHA): did the PR introduce or worsen it, or merely expose it?
4. Classify: `pr-regression`, `already-fixed`, `duplicate`, `pre-existing`, `stale`, `not-an-issue`, or `needs-user-judgment`.
5. Fix only `pr-regression`. Prefer deletion, existing helpers, stdlib or platform behavior, one shared guard over per-caller patches. No speculative abstractions or bot-appeasing tests.
6. Run the smallest checks proving the change, then re-evaluate the whole ledger. Never push with a valid actionable thread unaddressed.
7. Only if the user authorized a push: one push after the batch is complete and verified. No review/fix/push loop unless asked for another pass.
8. Reply and resolve only once the conclusion is supported and any code fix is visible on the PR. Re-list unresolved AI threads once at the end.

A severe pre-existing security, privacy, data-loss, billing, migration, or healthcare issue stays open for user judgment unless repo policy requires fixing it in this PR.

## Replies

One to three factual sentences, via `reply-and-resolve`:

- `Yes.`: why the claim is valid, how the root cause was fixed, the check that passed.
- `No.`: why it is false, stale, duplicate, or pre-existing, citing the decisive code or base comparison.

Never resolve a valid unfixed thread, resolve just because the line is outdated, submit a broad review, or close the PR.

## Helper

Review-thread plumbing via authenticated `gh`; it does not edit, commit, or push.

```bash
python3 scripts/pr_review_threads.py list OWNER/REPO#123 --json
python3 scripts/pr_review_threads.py list --author cursor --json
python3 scripts/pr_review_threads.py reply-and-resolve THREAD_ID --body "Yes. ..."
```
