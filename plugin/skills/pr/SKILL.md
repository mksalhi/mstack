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

```markdown
## Summary

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

No preamble, brief prose, and the domain words from `GLOSSARY.md` if the repo has one.

### Summary

Pick the smallest view that makes the point, usually one:

- Logic or algorithm: pseudocode.
- Runtime control flow: call tree.
- UI structure: component tree with the state and module boundaries that matter, e.g. `<SessionPage> (apps/example/src/routes/session.tsx)`.
- File responsibility or broad refactor: shallow file tree with a `# role` comment per entry.
- Component interaction, control, or data flow: Mermaid (`sequenceDiagram`).
- What changes inside an existing shape: `diff` of that shape (component tree, file tree, call tree, or state flow):

```diff
 submitForm
   createSession
     persistPrompt
+    expandSkillMention
     launchAgent
```

- Whole code block: when most of it is new, when omitted context would hide ownership or order, or when the user needs a copyable target shape.

Put each visual next to the text it supports, showing only the calls, files and states that matter.

### Evidence

Before and after proof the change works. For a visual change, screenshots beat everything else. Otherwise show test results or output: the exact test that failed before and passes now.

### Merge Danger

- **Door:** two-way if cheap to roll back; one-way if destructive or hard to reverse.
- **Blast Radius:** what the change could affect (layout shift, consumer breakage, mobile).

### Joke

- One or two lines about this change (the bug, the code, the work) that lands for someone who just read the diff: a pun on the function name, the bug's absurd root cause, a one-line fix after a long hunt.
- Punch at the code, never people (coworkers, replaced code's authors, users, patients, customers). Clean enough to read aloud in review; no real patient data, internal names, or anything sensitive.
- Skip it on incident fixes, reverts, security patches, PRs touching patient data or billing, and when the repo's PR template or `AGENTS.md` has no room. A missing joke beats a forced one.

## Cut comments before review

The `comment-sicko` agent audits and deletes; you check its work and fix what it flags. Scope: the caller's files or diff, else the current diff against the base branch (default `main`), working tree included.

1. Spawn `Agent` with `subagent_type: "mstack:comment-sicko"` and the scope. Don't restate its rules.
2. Check its report and diff:
   - Revert any edit to application code or outside the scope, and any deletion of a comment its keep list protects.
   - Reject a `MUST KILL` flag whose reason is false or that calls intentional code a workaround.
   - A flag on a surprise in our own code stays: fix the code, don't restore the comment. A kept comment needs proof it concerns something we can't change.
   - Catch lint and TypeScript suppressions it missed in scope; one hiding a correctness or safety rule becomes a `MUST KILL`.
   - For a thin `IMPORTANT` or `do not remove` call either way, run `how` or `why` on the symbol first. If still unclear, the comment goes.
   - If the report fails these checks, revert and rerun once, naming the failure. A second failure: report it and stop.
3. Fix trivial flags directly (delete a dead path, drop a parameter, use the real API). If a fix needs a new shape, run `architect` once for all of them and stop at the sketch.
4. Remove every named workaround with the smallest in-scope root-cause fix. If the root cause is out of scope, fix what's in scope and report the rest. Never add symptom guards.
5. Constraint comments (`do not remove`, `do not change wording`, `talk to X first`): keep those about things we can't change. For the rest, offer the cheapest type, runtime check, test or lint that enforces the constraint and wait for approval (unattended runs need it granted up front). Approved: encode it, then delete the comment. Not approved: delete it and report the constraint as unenforced.
6. Report: deletions, restored comments, reruns, any architect sketch, fixes, enforcement offers and encodings, unenforced constraints, and open work.

## Triage bot review threads

A bot comment is a claim, not an instruction: reject noise with evidence, and fix real issues at the smallest shared root cause, with `scoper` at ultra.

### Scope

- Default: unresolved AI-reviewer threads only. The helper knows common Codex, Cursor, Copilot, and CodeRabbit logins; `--author` adds another AI reviewer; `--all-authors` only when the user expands scope.
- Replying, resolving, committing and pushing are separate actions: do only the ones requested. Running this skill authorizes none of them.
- Under the Babysit playbook or an Autopilot owner, their push step authorizes pushing and their loop replaces the one-push rule below.

### Workflow

1. Resolve the PR; capture base and head SHAs. List threads: `scripts/pr_review_threads.py list [PR] --json` (no PR = current branch).
2. Before editing, build the full ledger: thread, author, file/line, claim, classification, evidence, action. Group duplicates by root cause.
3. Per claim, inspect the current code and all relevant callers and compare against the base (merge base or base SHA): did the PR introduce or worsen it, or merely expose it?
4. Classify: `pr-regression`, `already-fixed`, `duplicate`, `pre-existing`, `stale`, `not-an-issue`, or `needs-user-judgment`.
5. Fix only `pr-regression`. Prefer deletion, existing helpers, stdlib or platform behavior, and one shared fix over per-caller patches. No tests written just to satisfy the bot.
6. Run the smallest checks proving the change, then re-evaluate the whole ledger. Never push with a valid actionable thread unaddressed.
7. Only if the user authorized a push: push once, after the whole batch is fixed and verified.
8. Reply and resolve only once the conclusion is supported and any code fix is visible on the PR. Re-list unresolved AI threads once at the end.

A severe pre-existing security, privacy, data-loss, billing, migration, or healthcare issue stays open for user judgment unless repo policy requires fixing it in this PR.

### Replies

One to three factual sentences, via `reply-and-resolve`:

- `Yes.`: why the claim is valid, how the root cause was fixed, the check that passed.
- `No.`: why it is false, stale, duplicate, or pre-existing, citing the decisive code or base comparison.

Never resolve a valid unfixed thread, resolve just because the line is outdated, submit a broad review, or close the PR.

### Helper

Lists, replies to and resolves threads through `gh`; it never edits, commits or pushes.

```bash
python3 scripts/pr_review_threads.py list OWNER/REPO#123 --json
python3 scripts/pr_review_threads.py list --author cursor --json
python3 scripts/pr_review_threads.py reply-and-resolve THREAD_ID --body "Yes. ..."
```
