# Swift performance and lifetime

## Performance: measure, then choose

Four costs: calls (copies, dispatch, blocked optimization), layout (inline vs out-of-line), allocation (global free, stack cheap, heap expensive), copies (retain/release).

Algorithms first:

- `remove(at:)` in a loop is O(n²); `removeAll(where:)` is O(n). Re-slicing `Data` per byte is O(n²); `popFirst()` is O(1).
- Chained `map`/`filter` allocate per stage; in hot loops size output once and write into it.
- Profile a *test* in Instruments (secondary-click its run button → Profile). `platform_memmove` = copying; many transient allocations = intermediate arrays; `swift_beginAccess` = exclusivity checks; `swift_retain`/`swift_release` = refcount traffic.

Levers:

- `final` on non-subclassed classes; whole-module optimization enables specialization.
- Large structs with reference fields cost one retain per field per copy; use copy-on-write if copied a lot.
- `any P` has a 3-word inline buffer; bigger values heap-allocate per copy (fix with indirect COW storage).
- `[MyModel]` over `[any Model]`. `T: AnyObject` gives a known representation.
- `InlineArray<N, T>` (6.2): inline fixed-size storage, no heap/refcount/uniqueness checks. Bad if copied or shared.
- `Span` / `RawSpan` / `OutputSpan` (6.2): non-escapable, replaces `withUnsafeBufferPointer`.
- Moving stored properties from a nested class into the parent struct removes exclusivity checks.
- 6.3, when measured: `@inline(always)` (with `final`), `@specialized(where T == ...)` (SE-0460).
- ⚠ 6.4: `borrow`/`mutate` accessors, `UniqueArray`/`UniqueBox`, `Ref`/`MutableRef` to hoist lookups.
- Don't make functions `async` with nothing to await. Batch main-actor hops (pass arrays instead of hopping per iteration).

## ARC and lifetime

- Lifetime ends at last use, not the closing brace; code depending on `deinit` timing is a bug.
- `weak`/`unowned` only break cycles. Reading `weak` after the owner's last use may give `nil`; optional binding there hides the bug worse than a crash.
- Prefer no cycle: factor shared data into a third type (tree). Next: redesign so the object is only strongly reachable. `withExtendedLifetime` is a patch.
- Keep `deinit` side effects local; use `defer` at the call site.
- **Optimize Object Lifetimes** build setting surfaces these bugs.
