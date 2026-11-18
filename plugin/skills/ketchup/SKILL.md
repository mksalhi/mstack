---
name: ketchup
description: "Use when the user returns to this chat and wants what changed since their last message plus every call waiting on them. Triggers: 'ketchup', 'what did I miss', 'what needs me'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# Ketchup

Catch the user up on what changed in this chat since the last message they wrote before `/mstack:ketchup` (notifications and subagent results are not their messages). Help them understand each change, then lay out every call waiting on them so they can decide from your reply alone. Assume they remember their last message and nothing after.

Plain words, short sentences, no jargon. Say what changed for the user, not how you did it ("the tests pass", not "CI is green"). Omit hashes, paths, commands, build numbers, and test counts unless needed to act. Name each PR, branch, or agent as the user knows it, not by an invented label. Give a fact its context or leave it out.

## Gather what changed

- Read-only turn: no code changes, no starting apps or jobs, no posting. Visuals only from what you already have.
- Collect your work since that message, subagent reports, and others' messages in this chat. Check the current state of each PR, CI run, or agent this chat touched. Check every number you show against its source; say so when you correct one.
- An action item is a call only the user can take (product choice, approval, irreversible action, access you lack), including ones raised before their last message. Work you can do yourself is not one. Never invent a call. An unrequested, unneeded step counts only if irreversible and waiting on the user: one line, no visual.
- One call can cover many items (e.g. each PR awaiting merge). Per item collect: link, what it changes for users, evidence for your pick, risk, your pick. Write "unknown" for a needed fact you lack; omit links you don't have.

## Write the reply

Budget: what happened under 100 words (excluding pictures), less when less happened; skip work that changed nothing for the user. About 30 words per item: two items well under 150 words total, thirty far more. Never cut or shrink items to fit a count: no count in place of a list, no link in place of an item.

1. One sentence naming what waits on the user, or that nothing does. If nothing happened and nothing waits, say so and stop.
2. What happened, pictures first: inline screenshots and videos the work produced, then any explanatory diagram. Then one bullet per thing the user asked for: what came of it and whether done, running, failed, or not checked, written as spoken ("Search was slow from a missing index", not "Search review: done"). Name bugs found and fixed. Each line true alone; never mark done what waits on the user; don't repeat action items. Then at most three short lines that change what the user knows or must do, and one line naming work left you can do.
3. Action items. Ask the call (merge, approve, pick) and give your pick, including any step you'd take first, prerequisites, and anything irreversible. Give the number or link of each PR, issue, or agent, also in calls between options.
   - One item: one bullet with the call, pick, user change, evidence, risk; item named once.
   - Shared call: call and pick once, then one bullet per item, riskiest first: link and name, user change, evidence, risk. Name an item's pick only where it differs.
   - Always give risk, even low ("Low risk: only the colors change."). Mention the cost of waiting only beyond delay (deadline, lost data).
   - Between options: weigh every option, each with gain, cost, and current state if any; costs are the risk, no separate risk line. If screenshots show the options, put gain and cost under each.

## Visuals

A visual is a screenshot, video, Mermaid diagram, chart from this session's visualization tool, or generated image; a Markdown table is not.

- Draw when a picture beats sentences: how a design or system works, a PR stack or dependency chain with states, before and after of a fix, options side by side. Never draw a status list, action-item list, or unconnected boxes. Never give a fact twice.
- At most six boxes, eight words each, labels in plain speech (not "Tests: pass"). A fact needing a sentence goes in text or nowhere.
- Embed screenshots and videos inline for visible changes. A visible change without one gets "No screenshot yet," on its summary line plus what changed on screen.
- Mermaid for connections, charts for numbers, only from facts you have. Never invent a number or depict a screen you did not capture. Link only existing artifacts.
