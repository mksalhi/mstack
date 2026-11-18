---
name: blast-radius
description: "Use before shipping a risky or untrusted diff, to find what it could break outside the diff. Triggers: 'blast radius', 'what could this break', a small diff you don't trust yet."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Blast radius

Find breakage outside the diff. Prove the one or two safety facts by running code.

## Steps
1. Read the change, including non-obvious effects the diff doesn’t show.
2. Find the one safety fact.
3. Go where grep stops: the called library's source at pinned version/local patch; lifecycle timing; API/DB/wire format; other languages; feature flags; downstream code.
4. Cite real `file:line`; an empty search is an answer; never invent a caller or API.
5. Prove it: write a script or test that runs the real code, run it, paste the result.

## Reply
- What it does, including non-obvious parts.
- The safety fact, the list step it reached, and the proof, or "unproven".
- Risks: how each breaks; `file:line`; likelihood, severity; how to check.
- Cleared: what you checked and why it's fine.
- Before merge: the cheapest test/repro that catches the real bug, including your script.

Strip anything private before it goes public.
