---
name: blast-radius
description: "Use before shipping a risky or untrusted diff, to find what it could break outside the diff. Triggers: 'blast radius', 'what could this break', a small diff you don't trust yet."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Blast radius

Find what a change breaks elsewhere before it ships. `how` covers what code does and `why` why it's shaped so; this skill finds the breakage grep won't show, not a list of callers.

A plausible writeup is worthless. Find the one or two facts the change's safety depends on and prove them by running code.

## How sure are you

Push each fact as far down this list as is cheap; say where it stopped.

1. You said so. Worthless alone.
2. You pointed at the line: a real `file:line`, or the library's own source.
3. You walked the failure step by step and showed it can't be reached.
4. You ran it: a script or test calling the real code that fails loud if you're wrong (usually one small script importing the library the app ships and calling the exact function).
5. You reproduced it in the running app.

## Steps

1. Read the change: diff, symbols added, changed, deleted, and what it now does differently, including what the diff doesn't spell out. Use `why` step 2 to pull the PR and commits.
2. Find the one fact it's safe because of (e.g. "this call only drops already-dead cache entries"). If it holds, most risky cases clear at once. Spend time here, not on a list of maybes.
3. Look where grep stops. Read the called library's source at its pinned version plus any local patch. Work out when things run: microtasks, unmount and teardown, Solid versus React. Follow what symbol search misses: API JSON, a DB column, a wire format, another language reading the same bytes, a feature flag, code three hops downstream.
4. Rate each risk honestly: real likelihood, real cost. Keep confirmed risks; list checked-and-cleared ones separately. Same rules as `why`: cite real `file:line`, an empty search is still an answer, never invent a caller or API.
5. Prove the one fact: write a script or test that runs the real code, run it, paste the result.
6. Big or wide change: run it as an `arena` (several models, same question, merged; different models catch different bugs).

## What to hand back

- **What it does.** What changed, including the non-obvious part.
- **The one fact it's safe because of.** State it, the step reached, and the proof; else write unproven.
- **Risks.** Each: how it breaks, `file:line`, likelihood and severity, how to check. Paste proof for the ones that matter.
- **Cleared.** What you checked and why it's fine.
- **Before you merge.** The cheapest test or repro that catches the real bug, including your script.

Run it through the `writing` skill's unslop pass (`<mstack>/skills/writing/unslop.md`), cite real code, and strip anything private before it goes public.

**Reply:** the writeup above, with the one safety fact proven or marked unproven.
