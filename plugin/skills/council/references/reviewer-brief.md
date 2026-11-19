# Council reviewer brief

Fill the brackets and send the same text to every member. Members get no chat history.

## Round 1

```
Review only. Do not edit, commit, push, comment on PRs, or start subagents.
Repo: <absolute path>  Base: <sha>
Intent: <one or two sentences>  Out of scope: <list>
Checks: <commands and results, including missing or already-failing ones>
See: git diff <base> [-- <paths>]; git status --short (read untracked files too).

Read the surrounding code. Find bugs, broken callers, and mismatches with the intent.
Skip style unless it hides a bug. Hold the change to the smallest one that meets the intent:
flag code, tests or guards the intent does not need.
Use this rubric where it applies: <contents of interrogate/references/rubric.md>

Severity:
- blocker = the intended case is wrong.
- should = a real bug callers will hit, inside the intent.
- nit = everything else (other paths, rare cases, small perf, extra compatibility).

Reply in exactly this shape:
VERDICT: APPROVE or CHANGES
SCORE: <n>/10
S1 [blocker|should|nit] <file>:<line> <claim>. Fix: <suggestion>
S2 ...
```

## Later rounds

Send the round 1 brief, then:

```
Ledger from the last round:
fixed: S1 <evidence>, ...
disagree: S3 <evidence>, ...
declined: S4 <reason>, ...

Change since the last round: <patch path or pasted diff; save one with git diff before each round>
Review only the open ids and the changed code. Mark each old id `resolved` or `still open: <reason>`.
New findings continue the numbering.
```
