---
name: grilling
description: "Use to stress-test the user's plan, decision or idea by interviewing them relentlessly, or to play back their goal before work starts. Triggers: 'grill me', 'grill this', 'in your own words', 'what do you think I want'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

Interview in rounds to shared understanding; map a design tree (each decision branches to dependents). Frontier = decisions with settled prerequisites. Each round ask the whole frontier, numbered, with recommended answer; defer any that depend on still-open ones; then wait. Recompute the frontier each round. Facts are yours: use sub-agents for environment info; don’t ask the user. Don’t block; only defer those downstream of exploration. Decisions are the user’s; pose each and wait. Done when the frontier is empty; no assumptions. Do not act until the user confirms understanding. Playback-only: if asked 'in your own words'/'what do you think I want', skip the interview; restate goals and the problem, then stop.
