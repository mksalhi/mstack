---
name: grilling
description: "Use to stress-test the user's plan, decision or idea by interviewing them relentlessly, or to play back their goal before work starts. Triggers: 'grill me', 'grill this', 'in your own words', 'what do you think I want'."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

Interview the user relentlessly until you reach a shared understanding. Map it as a **design tree**: each decision branches into the decisions that hang off it.

Work in **rounds**. The **frontier** is every decision whose prerequisites are settled: questions you can ask _now_ without guessing at unheard answers. Ask the whole frontier in one round, each question numbered with your recommended answer, then wait for answers. A question depending on another still open this round belongs to a _later_ round. After each round, recompute the frontier.

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Facts are your job, never the user's: when a question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent; never ask for what you could look up. Don't block on it: only questions downstream of a running exploration wait; ask the rest now. Decisions are the user's: put each to them and wait.

Done when the frontier is empty: every branch visited, nothing silently assumed. Do not act until the user confirms shared understanding.

## Play back only

For 'in your own words' or 'what do you think I want', skip the interview: restate in your own words the user's goals and the problem behind them, then stop.
