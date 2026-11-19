---
name: council
description: "Use to review a change in rounds with several model families, fixing between rounds until they agree. Triggers: 'council', 'sol loop', 'review until they agree'. One read-only pass is `interrogate`."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Council

Several reviewers from different model families review the change, you fix what holds up, and they re-review only what changed. Stop when they agree or the budget runs out. Unlike `interrogate`, you edit code between rounds. Your job in every round is to keep the change small: push back on anything the goal doesn't need.

## 1. Before round 1

- Fix what you already know: outstanding PR comments, known bugs, failing checks. Reviewers get the updated code, not a list of known issues.
- Scope: `git status --short`. Never stash, discard or include unrelated changes. Find the base with `git fetch origin` then `git merge-base HEAD origin/<base>` (the PR's base, else the default branch). The change is base to working tree, untracked files included. Use the same diff command every round.
- State the intent and what is out of scope in one or two sentences. Run the checks that cover the change; note missing or already-failing ones for the brief.

Done when the diff is fixed, the intent is written, and checks have run.

## 2. Seat the council

- Members: the `council members` line in `~/.claude/rules/mstack-models.md`, else `claude-opus-5-5`, `fable`, `sonnet`. A member the user names wins. `auto` or `inherit-parent` means omit `model`.
- One read-only reviewer per member, all in one message, in the background, `effort: high`. Members never edit, commit, push, comment on the PR or start their own subagents.
- A member the harness can't run is reported, never swapped for another model. Fewer than two distinct families means it is not a council: say so and offer `interrogate`.
- Members get no chat history. Send every member the same filled brief, which demands a `VERDICT`, a `SCORE` and numbered `S1` findings.
- Open `references/reviewer-brief.md` when writing a round's brief, and fill it with the rubric at `<mstack>/skills/interrogate/references/rubric.md`.

## 3. Answer the findings

Don't wait idle. Check each finding against the code as it arrives, while the others run; don't edit files a member is still reviewing.

Judge severity yourself, whatever label it came with:
- **blocker**: the intended case is wrong.
- **should**: a real bug callers will hit, inside the intent.
- **nit**: everything else, including other paths, rare cases, small perf costs and extra compatibility.

Then for each finding:
- **Agree**: the smallest fix. Prefer deleting or narrowing code over a new lock, cache, helper or option. Add one focused test that fails without the fix if the intent needs it.
- **Disagree**: say why with evidence (file:line, test, output).
- **Nit or out of scope**: decline in one line and list it as a follow-up.

Keep a ledger with one row per finding: stable id (`S1`, `S2`...), member, severity, outcome (`fixed`, `disagree`, `declined`), evidence. Record each member's score out of 10 for the round; write `no score` when none was given, never invent one. Re-run checks and `git diff --shortstat <base>`. If review grew the diff, cut first. Never agree just to end the loop.

## 4. Next round

- Budget: 3 rounds. Up to 5 only for security, auth, data loss or concurrency while a blocker or should stays open with evidence, or when the user asks.
- Start another round only if budget remains and a blocker or should is open, or behavior code changed since the last approval. A round that returns only nits ends the loop; doc, comment or format-only fixes need no new round.
- Save the change since last round with `git diff` before each round. A new round uses fresh reviewers with the round 1 brief, the ledger, the same base diff and the change since last round. They check open ids and changed code only, marking each old id `resolved` or `still open: <reason>`.

## 5. Stop

- **Agreed**: every member approves the current behavior diff, no blocker or should is open, and you have no concern of your own.
- **Stuck**: an item stays disputed after two replies, or the budget ran out. Show both sides in two or three lines each; the user decides. Budget end is not approval. A timeout, error or empty reply is not approval either.

Push only if the user asked to push, ship or update the PR. If the work has a PR, put this table in its body (edit the body, never a comment); otherwise put it in the reply:

```markdown
## Council review

Rounds: 2

| Member | Round 1 | Round 2 |
| --- | --- | --- |
| claude-opus-5-5 | 7/10 | 9/10 |
| fable | 8/10 | 10/10 |
```

**Reply:** agreed or stuck; rounds and members; what changed because of review; diff size before and after; fixed, disputed and declined findings with reasons; pushed or not.
