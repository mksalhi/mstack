### Session pickup

**You own the resume point. The prior trail is authoritative. Don't redo it.**

1. Locate the prior trail: a transcript (location in SKILL.md), a remote session URL, a `handoff` note, or a pushed branch. Read the metadata overview and last messages, then scan back for decision points. Parse a long transcript in a subagent and keep the reduced timeline in the main thread (Guard the context window).
2. Reconstruct operational state: branch and worktree, what landed (`git log`, `git diff` against the base), open todos, decisions made.
3. Diff done vs pending and name the resume point. Do not re-run the prior repro or redo completed work.
4. Route the remaining work to the matching playbook and pick the verdict: continue the execution, ship a finished recommendation, ratify or override a prior conclusion, or postmortem a failed run. The routed playbook owns the rest.
5. Verify the inherited claims against the original goal on the real artifact (Prove it works). A passing prior self-report is not proof.

**Reply:** where the prior agent stopped, what you inherited vs redid (ideally nothing), the resume point, the outcome.
