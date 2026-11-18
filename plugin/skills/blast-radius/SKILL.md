---
name: blast-radius
description: "Use before shipping a risky or untrusted diff, to find what it could break outside the diff. Triggers: 'blast radius', 'what could this break', a small diff you don't trust yet."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Blast radius

Find what a change breaks outside its diff before it ships: the breakage grep won't show, not a list of callers. A plausible writeup is worthless. Find the one or two facts the change's safety depends on and prove them by running code.

## How sure are you

Push each fact as far down this list as is cheap, and say where it stopped:

1. You said so. Worthless alone.
2. You pointed at the line: a real `file:line`, or the library's own source.
3. You walked the failure step by step and showed it can't be reached.
4. You ran it: a script or test calling the real code that fails loudly if you're wrong.
5. You reproduced it in the running app.

## Steps

1. Read the change, including what it now does differently that the diff doesn't spell out. Pull the PR and commits as in `why` step 2.
2. Find the one fact it's safe because of (e.g. "this call only drops already-dead cache entries"). If it holds, most risks clear at once. Spend your time here.
3. Look where grep stops: the called library's source at its pinned version and any local patch; when things run (microtasks, teardown, framework lifecycle); API JSON, a DB column, a wire format, another language reading the same bytes, a feature flag, code three hops downstream.
4. Rate each risk by real likelihood and cost. Cite real `file:line`; an empty search is an answer; never invent a caller or API.
5. Prove the one fact: write a script or test that runs the real code, run it, paste the result.
6. For a big or wide change, run it as an `arena`: different models catch different bugs.

## Reply

- **What it does**, including the non-obvious part.
- **The fact it's safe because of**, the list step it reached, and the proof, or "unproven".
- **Risks**: how each breaks, `file:line`, likelihood and severity, how to check.
- **Cleared**: what you checked and why it's fine.
- **Before you merge**: the cheapest test or repro that catches the real bug, including your script.

Strip anything private before it goes public.
