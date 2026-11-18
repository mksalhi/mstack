# Never block on the human

**Rule:** Do it, show the result, let the human correct.

The human supervises asynchronously; stay unblocked. Code changes are reversible and reviewable, so a wrong decision usually costs less than blocking.

- Proceed, then present. Don't ask "should I do X?" Do X, explain why.
- Self-heal: when you notice a problem, log it and fix it next round.
- Irreversible actions still need confirmation: messages to people outside the team and anything on the Always-pause list in the `mstack-mode` skill (force-push to shared branches, deploys, data deletion, customer messages).
- Reversible actions (write code, edit notes, split tasks, post in team chat, update tickets) proceed without blocking.
- Product direction comes from the human; execution does not block.
