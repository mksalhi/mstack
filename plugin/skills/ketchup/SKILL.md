---
name: ketchup
description: "Use when the user returns to this chat and wants what changed since their last message plus every call waiting on them. Triggers: 'ketchup', 'what did I miss', 'what needs me'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Ketchup

Catch the user up on what changed in this chat since their last message before `/mstack:ketchup` (notifications and subagent results are not their messages), then lay out every call waiting on them so they can decide from your reply alone. Assume they remember their last message and nothing after.

Use plain words and short sentences. Say what changed for the user, not how ("the tests pass", not "CI is green"). Leave out hashes, paths, commands, build numbers and test counts unless needed to act. Name each PR, branch or agent the way the user knows it.

## Gather

- This turn is read-only: no code changes, no starting apps or jobs, no posting.
- Collect your work since that message, subagent reports, and others' messages in this chat. Check the current state of each PR, CI run or agent this chat touched. Check every number against its source.
- An action item is a call only the user can make: a product choice, an approval, an irreversible action, access you lack. Include ones raised before their last message. Work you can do yourself is not one. Never invent one.
- One call can cover many items (e.g. several PRs awaiting merge). Per item collect: link, what it changes for users, evidence for your pick, risk, your pick. Write "unknown" for a fact you lack.

## Write the reply

Budget: under 100 words for what happened, less when less happened; about 30 words per action item. Never drop items to fit the budget.

1. One sentence naming what waits on the user, or that nothing does. If nothing happened and nothing waits, say so and stop.
2. What happened. Screenshots and videos the work produced come first, then any diagram. Then one bullet per thing the user asked for: what came of it, and whether it is done, running, failed or unchecked, written as spoken ("Search was slow from a missing index"). Each line stands alone; never mark done what waits on the user. Then at most three lines that change what the user knows or must do, and one line on work left that you can do.
3. Action items. State the call (merge, approve, pick) and your pick, with any prerequisite and anything irreversible, and the number or link of each PR, issue or agent.
   - One item: one bullet with the call, pick, user-facing change, evidence and risk.
   - Shared call: the call and pick once, then one bullet per item, riskiest first.
   - Always give the risk, even low ("Low risk: only the colors change."). Mention the cost of waiting only beyond delay (a deadline, lost data).
   - Between options: give each option's gain, cost and current state; the costs are the risk.

## Visuals

A visual is a screenshot, video, Mermaid diagram, chart or generated image; a Markdown table is not.

- Draw only when a picture beats sentences: how a system works, a PR stack with states, before and after, options side by side. Never draw a status list or unconnected boxes.
- At most six boxes of eight words each, labeled in plain speech.
- Embed screenshots for visible changes. A visible change without one gets "No screenshot yet" plus what changed on screen.
- Never invent a number or show a screen you did not capture. Link only existing artifacts.
