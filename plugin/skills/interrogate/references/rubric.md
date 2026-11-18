# Review Rubric

Use only the lenses relevant to the change.

## Correctness

Does the code do what the intent says?

- Edge cases: empty, nil/undefined, boundary values, concurrent access
- Errors caught, propagated, or silently swallowed?
- Off-by-one, type coercion, integer overflow, string encoding
- State: race conditions, stale closures, dangling references
- Happy and sad paths both work?
- Idempotency: safe to run twice or after a halfway crash? "Depends on leftover state" means a reconciliation step is missing.
- Concurrency: shared mutable state (files, branches, data) serialized structurally (locks, sequential phases, exclusive ownership), or by conventions that won't hold?

For a potential bug, show the call chain that triggers it, not "this could be nil".

## Root Causes vs. Symptoms

Fix or symptom patch? Read beyond the diff (callers, callees, types, sibling modules) with Read, Grep, Glob to judge whether the change hits the right layer.

- Guard clauses masking a deeper invariant violation
- Retry logic hiding a broken contract
- Type casts silencing a modeling error
- Workarounds: why needed, what would the proper fix be?
- A fix in module A that belongs in module B's contract
- A "don't do X" comment or convention that could be a type constraint, lint rule, or runtime check

## Structural Integrity

- Boundary discipline: validate once where data enters, trust it internally, not scattered through business logic.
- Abstraction level: high-level orchestration mixed with low-level detail?
- Coupling that makes future changes harder?
- Data structures match access patterns?
- Bolted-on vs. integrated: would the code look like this if the requirement were known from the start?
- Legacy dual-paths: new API with the old one kept alive? With no external consumers, migrate callers and delete the old path in the same wave.

Don't penalize simple code for lacking abstraction; premature abstraction is worse than duplication.

## Verification

- Tests present? Testing behavior or implementation details?
- Assertions/invariants that catch regressions?
- Bug fix: a test for the bug?
- Integration boundary: full path tested?
- Checks the real thing, not a proxy (file mtime or cached state instead of the actual value is a gap).
- Delegated or async work: verifies output artifacts, or trusts self-reports?

## Complexity Budget

Simpler is better unless simpler is wrong. Flag:

- Code simpler without losing correctness or clarity
- Abstractions serving one call site
- Configuration for cases that don't exist
- Dead code, unused imports, vestigial parameters
- "Just in case" paths with no callers
- Compatibility scaffolding after the migration is done
- Features, controls, or options that don't earn their UX cost; half-finished features are worse than missing ones

## Security

Trace and show the input path for each finding.

- User input reaching dangerous sinks (SQL, shell, eval, innerHTML) unsanitized
- Authn/authz gaps in new endpoints
- Secrets in code, logs, or error messages
- TOCTOU in security-critical paths
