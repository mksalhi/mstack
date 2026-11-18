---
name: pr
description: "Use when writing or editing a pull request title or body, or cutting low-value comments and workaround code before review. Triggers: 'cut comments', 'no comments'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# PR

Two jobs: write the PR body, or cut comments and workaround code before review ('cut comments', 'no comments').

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

No preambles, brief prose, the user's domain language from `GLOSSARY.md`.

### Summary

Pick the smallest view that makes the key point clear; usually one, sometimes several, never all:

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

Place each visual next to the short text it supports. Keep only the calls, files, props, states, and boundaries the current question or discussion point needs.

### Evidence

Before and after proof the change works. Screenshots are S-tier when the change is visual and the environment allows. Execution evidence (test results, console output) is A-tier: show the exact test that now fails then passes, as pseudocode.

### Merge Danger

- **Door:** two-way if cheap to roll back; one-way if destructive or hard to reverse.
- **Blast Radius:** the scope of possible impact; consider everything (layout shift, consumer breakage, mobile responsiveness, ...).

### Joke

- One or two lines about this change (the bug, the code, the work) that lands for someone who just read the diff: a pun on the function name, the bug's absurd root cause, a one-line fix after a long hunt.
- Punch at the code, never people (coworkers, replaced code's authors, users, patients, customers). Clean enough to read aloud in review; no real patient data, internal names, or anything sensitive.
- Skip it on incident fixes, reverts, security patches, PRs touching patient data or billing, and when the repo's PR template or `AGENTS.md` has no room. A missing joke beats a forced one.

## Cut comments before review

Comment Sicko audits; you defer to its fresh perspective and act on accepted findings. Scope: the caller's files or diff; otherwise the current diff against the base branch (default `main`), including the working tree.

1. Spawn `Agent` with `subagent_type: "mstack:comment-sicko"`. Pass the scope; do not restate its rules.
2. Audit its report and diff:
   - Reject application-code edits, scope escapes, exception-protected deletions, misstated `MUST KILL` reasons, and flags calling kept intentional code guilty.
   - Reshape flags on our-code surprises stay actionable; do not restore those comments. A keep survives only with proof it concerns something we cannot change.
   - Audit missed scoped lint and TypeScript suppressions; correctness or safety suppressions stay actionable `MUST KILL`s.
   - Restore a deletion only with an exact exception and scoped proof.
   - Thin `IMPORTANT` / `do not remove` kills or keeps: run `/mstack:how` or `/mstack:why` on the symbol first. Ambiguous kill: do not restore. Refuted or still-ambiguous keep: delete.
   - A rejected report: revert and rerun once, naming the failure. Second rejection: report it open and fail `/mstack:pr`.
3. Fix trivial accepted flags directly (delete a dead path, drop a parameter, use the real API). If any fix needs a shape, run `/mstack:architect` once for the accepted set and surrounding code; stop at the sketch.
4. Implement the smallest in-scope root-cause fix and remove every named workaround. Out-of-scope root cause: land the smallest in-scope fix, report the rest open. `debug` and Converge on target (`principles`) guide intent only; neither widens the fence. Never bolt on symptom guards.
5. Constraint comments (`do not remove`, `do not change wording`, `talk to X before changing`): leave keeps about things we cannot change. Otherwise offer the cheapest in-scope type, runtime, test, or CI lint and wait for interactive approval (unattended and eval runs need caller pre-approval). Approved: encode, then delete. Not approved: delete, report the constraint open, sketch out-of-scope work.
6. Report deletion count, restored comments, reruns, architect sketch, fixes, encoding offers, encodings, unenforced constraints, and other open work.
