# Review rubric

Use only the lenses the change touches. Every finding needs evidence: the call chain that triggers a bug, the input path for a security issue. "This could be nil" is not a finding.

## Correctness

- Edge cases, swallowed errors, races, stale closures, both happy and sad paths.
- Idempotency: safe to run twice, or after a crash halfway? "Depends on leftover state" means a reconciliation step is missing.
- Shared mutable state (files, branches, rows) serialized by structure (locks, phases, exclusive ownership), not by convention.

## Root cause or symptom

Read beyond the diff (callers, callees, types, sibling modules) to judge whether the fix is at the right layer. Flag guards masking a broken invariant, retries hiding a broken contract, casts silencing a modeling error, a fix in A that belongs in B's contract, and a "don't do X" comment that could be a type, lint or runtime check.

## Structure and simplicity

Rank deletions and smaller diffs above restructurings. Hunt for code judo: a behavior-preserving reframing that deletes whole branches, helpers, modes or layers by using the existing architecture better.

Presumptive blockers unless justified:

- complexity a code-judo move would delete;
- a file pushed from under 1,000 lines to over;
- ad-hoc branches or feature checks scattered through a shared flow (move them to a helper, state machine or module);
- a thin wrapper, one-call-site abstraction, config for cases that don't exist, or a cast-heavy contract;
- a helper duplicating an existing utility, or logic in the wrong layer when a canonical home exists;
- a new API with the old one kept alive when nothing external uses it;
- validation scattered through business logic instead of once at the boundary;
- needless optionality, `any`, `unknown` or casts where a typed model fits.

Don't penalize simple code for lacking abstraction. Propose an extraction only when it removes code or branches.

## Verification

Tests check behavior, not implementation; a bug fix has a test that fails without it; checks read the real value, not a proxy (mtime, cache, a delegate's self-report).

## Security

User input reaching SQL, shell, eval or `innerHTML`; authn and authz gaps on new endpoints; secrets in code, logs or errors; TOCTOU in security paths.

## Tone

Direct and demanding. Don't soften a structural problem into "maybe rename this".
