`L<line>: <tag> <what>. <replacement>.`
or
`<file>:L<line>: <tag> <what>. <replacement>.`

Tags
- delete: dead code, unused flexibility, speculative feature. Replacement: nothing.
- stdlib: hand-rolled thing stdlib ships. Name the function.
- native: code the platform does. Name the feature.
- yagni: single-impl abstraction/config/layer.
- shrink: same logic, fewer lines. Show the shorter form.

Boundaries
- Over-engineering only; route correctness/security/perf to normal review.
- Tests passing test-audit aren’t bloat; route questions to test-audit.
- List fixes, apply none. One-shot; “normal mode” reverts.

End with `net: -<N> lines possible.` None: `Lean already. Ship.`

Repository audit
Scan whole tree; same tags/boundaries.
Hunt stdlib/native dupes; single-impl interfaces/factories; delegate-only wrappers; one-export files; dead flags/config.
Output: `<tag> <what to cut>. <replacement>. [path]`, ranked. End with `net: -<N> lines, -<M> deps possible.`
