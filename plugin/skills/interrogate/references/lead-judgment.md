# Lead Judgment Framework

## Filtering Principles
- Hypotheticals: Count only if callers can hit them; trace call sites/types; dismiss if upstream prevents.
- Premature abstraction: Extract/interface only if a second change is expected; prefer simple inline code.
- “I’d do it differently”: Dismiss unless the reviewer shows a concrete problem.
- Missing context: Dismiss items outside changed code, consistent with codebase patterns, or conflicting with known constraints.

## When Reviewers Are Right
- Multiple models agree.
- Concrete execution path named.
- Reveals a gap in your mental model.
- Scrutinize security/correctness harder, even from one model.
