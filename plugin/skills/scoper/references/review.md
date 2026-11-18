Review diffs for unnecessary complexity. One line per finding: location, what to cut, what replaces it.

## Format

`L<line>: <tag> <what>. <replacement>.`, or `<file>:L<line>: ...` for multi-file diffs.

Tags:

- `delete:` dead code, unused flexibility, speculative feature. Replacement: nothing.
- `stdlib:` hand-rolled thing the standard library ships. Name the function.
- `native:` dependency or code doing what the platform already does. Name the feature.
- `yagni:` abstraction with one implementation, config nobody sets, layer with one caller.
- `shrink:` same logic, fewer lines. Show the shorter form.

## Examples

❌ "This EmailValidator class might be more complex than necessary, have you considered whether all these validation rules are needed at this stage?"

✅ `L12-38: stdlib: 27-line validator class. "@" in email, 1 line, real validation is the confirmation mail.`

## Scoring

End with `net: -<N> lines possible.` Nothing to cut: `Lean already. Ship.` and stop.

## Boundaries

- Over-engineering only. Route correctness bugs, security holes, and performance to a normal review pass.
- A test that passes the `test-audit` gate is not bloat; route test-value questions to `test-audit`.
- Lists fixes, applies none. One-shot. "normal mode" reverts.

## Repository audit

Scan the whole tree instead of a diff, same tags, same boundaries. Rank findings biggest cut first.

### Hunt

Deps the stdlib or platform already ships, single-implementation interfaces, one-product factories, delegate-only wrappers, one-export files, dead flags and config, hand-rolled stdlib.

### Output

`<tag> <what to cut>. <replacement>. [path]`, ranked. End with `net: -<N> lines, -<M> deps possible.` Nothing to cut: `Lean already. Ship.`
