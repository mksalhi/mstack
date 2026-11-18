# Swift performance and lifetime

- Profile tests in Instruments; watch platform_memmove, transient allocations, swift_beginAccess, swift_retain/release.
- Avoid O(n²): remove(at:) in loops; re-slicing Data per byte. Prefer removeAll(where:), popFirst().
- Pre-size outputs; avoid chained map/filter in hot loops.

Levers:
- final on non-subclassed classes; whole-module optimization enables specialization.
- Large structs with reference fields retain on copy; use COW if copied often.
- any P has a 3‑word inline buffer; larger values heap‑allocate per copy. Prefer [MyModel] over [any Model].
- InlineArray<N, T> (6.2): inline fixed storage; poor if copied/shared. Span/RawSpan/OutputSpan (6.2): non‑escapable buffer access.
- Move stored properties from nested class into parent struct to remove exclusivity checks.
- 6.3: @inline(always) with final; @specialized(where T == ...). 6.4: borrow/mutate accessors; UniqueArray/UniqueBox; Ref/MutableRef.
- Don’t make functions async with nothing to await; batch main‑actor hops.

ARC/lifetime:
- Lifetime ends at last use; don’t rely on deinit. weak/unowned only break cycles; reading weak after last use may be nil.
- Prefer no cycle (factor shared data); withExtendedLifetime is a patch. Keep deinit side effects local; use defer. Enable Optimize Object Lifetimes.
