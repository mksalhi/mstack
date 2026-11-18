# Review rubric

Use only the lenses the change touches. Every finding needs evidence: the call chain to trigger it or the input path to the sink. “This could be nil” is not a finding.

## Correctness
- Edge cases, errors, races, happy/sad paths.
- Idempotency: safe twice and after mid-crash; else require reconciliation.
- Shared mutable state serialized by structure (locks/phases/exclusive ownership), not convention.

## Root cause vs symptom
Fix at the right layer; read callers/callees/types/siblings. Flag guards hiding broken invariants; retries hiding broken contracts; casts silencing modeling errors; fixes in A that belong in B’s contract; “don’t do X” that should be a type/lint/runtime check.

## Structure and simplicity
Prefer deletions and smaller diffs. Seek “code judo” that removes branches/helpers/modes/layers via existing architecture.
Presumptive blockers unless justified:
- Complexity a code‑judo move would delete; files >1,000 lines.
- Ad‑hoc feature checks scattered in shared flow (centralize).
- Wrong layer logic; duplicated utilities; new API while old persists unused.
- Validation at boundaries; prefer typed models over optionality/any/unknown/casts.

## Verification
Tests assert behavior; include a test that fails without the fix; read real values, not proxies.

## Security
Trace user input to sinks (SQL/shell/eval/innerHTML); authn/authz on new endpoints; no secret leakage; avoid TOCTOU.

## Tone
Be direct and demanding.
