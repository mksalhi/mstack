# Lead Judgment Framework

## Filtering Principles

- **Nitpick gravity.** Adversarial reviewers inflate nits to fill space. If a reviewer's findings are all nits and style, the code is probably fine; say so.
- **Hypothetical vs. actual.** "What if null is passed?" counts only if a caller can pass null. Trace the call site; dismiss if upstream validation or the type system prevents it.
- **Premature abstraction.** Suggested extractions, interfaces, or abstractions count only if the code must change in a second way. Otherwise simple inline code wins.
- **"I would have done it differently."** The most common false positive. Dismiss, with the reason, unless the reviewer shows a concrete problem with the current approach.
- **Missing context.** Dismiss gracefully findings that touch code the author didn't write or modify, flag patterns consistent with the rest of the codebase, or conflict with constraints you know.

## When Reviewers Are Right

Don't dismiss a finding because it's uncomfortable. Signs it deserves attention:

- Multiple models flag it independently.
- It names a concrete execution path, not a hypothetical.
- It exposes a gap in your mental model of the code ("...yeah, actually").

Scrutinize security findings and correctness bugs harder before dismissing, even from a single model.
