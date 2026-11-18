---
name: write-swift
description: Use when writing, reviewing, or migrating Swift (Swift 6 concurrency, @concurrent, actors, generics, Swift Testing, macros), or fixing a Swift concurrency error, hang, data race, retain cycle, or performance problem.
metadata:
  harness: "claude codex"
  platform: "darwin"
  scope: universal
---

# Write Swift

## Initial response

When first invoked without a specific question, respond only with:

> I'm ready to help you write modern Swift, the way the language wants to be written.

Say nothing else until the user asks a question.

**Baseline: Swift 6.3** (current as of August 2026). ⚠ marks unreleased Swift 6.4 features: accepted and in main, unsafe to write today; check the toolchain and use the older form on 6.3 or earlier. Concurrency rules assume the Swift 6.2 model; on 6.1 or earlier the `async`/`@concurrent` rules in §3 do not apply.

Start with the simplest, most static, single-threaded thing that works. Move down a row only with a reason you can state:

| Need         | Reach for               | Move down only when                                        |
| ------------ | ----------------------- | ---------------------------------------------------------- |
| Data         | `struct` / `enum`       | you need identity, sharing, or inheritance                 |
| Abstraction  | concrete type           | you have repeated code across types                        |
| Polymorphism | `some P` (generic)      | you need heterogeneous storage → `any P`                   |
| Execution    | main actor, synchronous | profiling shows a hang → `async` → `@concurrent` → `actor` |
| Memory       | `Array`, `String`       | profiling shows the cost → `InlineArray`, `Span`           |
| Safety       | safe API                | C interop or a measured hot path → `Unsafe*`               |

## 1. Value types

- `class` only for identity, shared mutable state, inheritance, or resource lifetime. `let` unless you mutate.
- A struct holding a mutable class property is neither value nor reference: copies share mutations. Keep the class immutable, forward through computed properties, or make it `private` behind copy-on-write.
- Copy-on-write: wrap a final class in a struct; check `isKnownUniquelyReferenced(&storage)` before mutating, copy if false.
- Replace piles of optional flags with one `enum State` so invalid combinations are unrepresentable and state changes are atomic.

```swift
struct Material {
  var roughness: Double
  private var _texture: Texture         // a class
  var color: Color {
    get { _texture.color }
    set {
      if !isKnownUniquelyReferenced(&_texture) { _texture = Texture(copying: _texture) }
      _texture.color = newValue
    }
  }
}
```

**Noncopyable types** (`~Copyable`) for unique ownership (file descriptor, transfer): double use becomes a compile error and struct `deinit` works. Mark the finishing method `consuming`. Parameter ownership: `borrowing` (default, read-only), `consuming`, `inout`/`mutating`.

## 2. Errors and optionals

- Recoverable → `throw`. Programmer mistake → `precondition`/`fatalError`.
- Error types: enums with associated values carrying context (`case duplicateFriend(String)`).
- `guard` for error conditions; `if let` for ordinary unwraps.
- Typed throws (`throws(MyError)`) for internal code, error-forwarding generics, and constrained environments. Public API: untyped `throws`. `throws` = `throws(any Error)`; non-throwing = `throws(Never)`.
- Force-unwrap only with a statable invariant; prefer `#require`/`precondition` with a message.

## 3. Concurrency: single-threaded until profiling says otherwise

Progression, in order, no skipping:

1. Single-threaded on the main actor.
2. `async`/`await` to hide latency; SDK APIs (`URLSession.data(from:)`) offload for you.
3. `@concurrent` to move *your* expensive work off main, only after Instruments shows a hang.
4. `actor` to move *state* off main, only when main-actor state forces constant hops.

**Build settings first:** enable **Approachable Concurrency** everywhere. For app and UI modules set **Default Actor Isolation** = **MainActor** (Xcode 26 default for new apps; package: `swiftSettings: [.defaultIsolation(MainActor.self)]`). Never for a general-purpose library: libraries ship `nonisolated` APIs.

**Swift 6.2: `async` does not leave the caller's actor.**

- `@concurrent`: always runs on the concurrent pool. Use on your CPU-heavy work.
- `nonisolated`: runs wherever called. Default for library APIs. On a type, applies to all members (6.1+).
- Neither: stays on the caller's actor.

```swift
nonisolated struct PhotoProcessor {
  @concurrent
  func process(_ data: Data) async -> ProcessedPhoto {
    async let sticker = extractSticker(data)
    async let colors  = extractColors(data)
    return await ProcessedPhoto(sticker: sticker, colors: colors)
  }
}
```

- Profile (Time Profiler, hangs) before offloading; make code faster without concurrency first. No tasks for trivial work.
- One task per end-to-end ordered operation; separate tasks for independent ones.
- `await` breaks atomicity: re-check state after it; never hold a lock or rely on thread-locals across it.

### Actor reentrancy

- Other work runs between `await`s on an actor. Mutate state in synchronous methods (the transaction boundary); keep async methods thin and consistent at every `await`.
- Classic bug: check cache → `await` download → write cache. Re-check after the `await` or dedupe in-flight work.
- Actors are not FIFO (highest priority first). For ordering use one task or an `AsyncStream`.

## 4. Sendable

- Value types are inferred `Sendable` when non-public and their storage is. Public types must declare it.
- Actors and `@MainActor` classes are implicitly `Sendable`.
- Most model classes: neither `@MainActor` nor `Sendable`. To leave main, make them `nonisolated`, not `Sendable`.
- A non-`Sendable` value can be *sent* if the sender stops using it: mutate before handoff.
- `@Sendable` on function types only if they really cross domains.
- `@unchecked Sendable` only for types with real internal sync (`Mutex`, lock). `nonisolated(unsafe)` on a global is a last resort, never a warning silencer.

**Fixing a data-race error, in order:**

1. Don't share: give each concurrent job its own local instance (fixes most).
2. Make it a `Sendable` value type.
3. Isolate it to an actor (main or yours).
4. Then `Mutex`/`Atomic` from `Synchronization` (in `let` properties), or `@unchecked Sendable`.

**Globals/statics** (most common source): `let` → `@MainActor` → `Mutex` → `nonisolated(unsafe)`. Globals init lazily and atomically.

**Callback/delegate APIs:** own the protocol → annotate `@MainActor`. Don't → `nonisolated` method + `MainActor.assumeIsolated { }` (traps instead of racing); `@preconcurrency` on the conformance is shorthand. `@preconcurrency import` silences an unmigrated module temporarily.

## 5. Structured concurrency

Prefer structured tasks; they inherit cancellation, priority, and task-locals.

- `async let`: fixed number of children.
- `withTaskGroup`: dynamic number; iterate results as an `AsyncSequence`. `withDiscardingTaskGroup` when children return nothing (frees each immediately, cancels siblings on first error).
- `Task { }`: only for lifetimes that don't fit a scope (delegate callback, tap, view appear). Inherits isolation and priority; you manage cancellation.
- `Task.detached`: almost never (inherits nothing). If needed, put a task group inside one detached root.
- **Cancellation is cooperative:** check `Task.isCancelled` / `try Task.checkCancellation()` before expensive work, including sync helpers. For suspended work use `withTaskCancellationHandler`; the handler runs immediately and concurrently, so its state needs an atomic or lock, not an actor.
- **Bound fan-out:** start N children, add one as each finishes.
- `@TaskLocal` for request IDs/trace spans; make them optional.
- **Continuations** (`withCheckedContinuation` / `withCheckedThrowingContinuation`): resume exactly once on every path. For delayed delegates, store it and nil it on resume. (⚠ 6.4 `Continuation` type checks this at compile time.)
- `AsyncStream`/`AsyncThrowingStream` to adapt handler APIs: build the source in the closure, `yield` from the handler, clean up in `onTermination`.

## 6. Concurrency in SwiftUI

- `View` and its `@State` are `@MainActor`; don't annotate views or view models (delete annotations under main-actor-by-default).
- `@Sendable` closures (`visualEffect`, `Shape.path(in:)`, `Layout`, `onGeometryChange`) run off main. On an isolation error, capture the value, not `self`:

```swift
.visualEffect { [pulse] effect, proxy in
  effect.blur(radius: pulse ? 2 : 0)
}
```

- Action callbacks are synchronous on purpose: do `withAnimation` state changes in the callback; `Task` only for the long work after.
- Put state on the seam: view starts a task, async layer does a synchronous mutation on finish, UI reacts. Async logic stays testable without SwiftUI.

## 7. Protocols and generics

Start concrete. Concrete types → repeated code → protocol → generic code. Near-identical overloads are the signal.

- A protocol where every conformer uses the default is wasted: use a constrained extension. No type zoology.
- Has-a over is-a: if only some operations fit, wrap in a generic struct (`GeometricVector<Storage: SIMD>`, not `GeometricVector: SIMD`). Composition over class inheritance.
- Requirements are dynamically dispatched customization points; extension-only methods are static, so a conformer's version shadows and `any P` calls the extension's. Customizable → make it a requirement.
- A forced downcast is a smell.

### `some` vs `any`

- `some P` by default; `any P` only for heterogeneous storage, optional underlying type, or full hiding. `any` erases associated types and blocks optimization.
- You can't call a method consuming an associated type on `any P`; pass it to a function taking `some P` (implicit opening).
- Constrained opaque/existential types: `some Collection<Element>`. Declare primary associated types (`protocol Container<Item>`) for what callers supply, not `Iterator`.
- Pin cross-protocol relationships with same-type `where` clauses (`where Self.CropType.FeedType == Self`).

## 8. API design: clarity at the point of use

- No type prefixes in Swift-only APIs (keep for ObjC mirrors); avoid overly general names.
- Drop leading `get`: `persistentPosts`.
- Explicit access control at boundaries (`private`, `internal`, `package`, `public`).
- Illegal states unspellable: private setters + validating mutating method, enums, typed `UUID` over `String`.
- Property wrappers for access policies; with `@dynamicMemberLookup` to project through (`$binding.title`). Result builders for DSLs; macros for compiler-derivable boilerplate (§12).

## 9. Performance: measure, then choose

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

## 10. ARC and lifetime

- Lifetime ends at last use, not the closing brace; code depending on `deinit` timing is a bug.
- `weak`/`unowned` only break cycles. Reading `weak` after the owner's last use may give `nil`; optional binding there hides the bug worse than a crash.
- Prefer no cycle: factor shared data into a third type (tree). Next: redesign so the object is only strongly reachable. `withExtendedLifetime` is a patch.
- Keep `deinit` side effects local; use `defer` at the call site.
- **Optimize Object Lifetimes** build setting surfaces these bugs.

## 11. Testing: Swift Testing

XCTest only for UI automation (`XCUIApplication`), `XCTMetric`, and Objective-C tests/exceptions.

- `@Test` on any function (async, throws, actor-isolated). `#expect(a == b)` with plain expressions.
- `try #require(...)` stops the test and unwraps optionals.
- Suites are `struct`s (fresh instance per test, `init` for setup); `class`/`actor` only for `deinit` teardown.
- `@Test(arguments: [...])` instead of loops/copy-paste. Two collections = cross product; `zip()` for pairs.
- Traits: `.enabled(if:)`, `.disabled("reason")` (never comment tests out), `.bug(url)`, `.tags(...)`, `.timeLimit`, `.serialized`. `@available` over runtime `#available`.
- `withKnownIssue { }` for external failures (over `.disabled`). `confirmation` for N-times callbacks; `withCheckedContinuation` for one-shot callbacks with no async overload.
- Tests run parallel and randomized; fix dependencies instead of `.serialized`.
- Exit tests: `#expect(processExitsWith: .failure) { ... }` for `precondition`/`fatalError` (macOS, Linux, FreeBSD, Windows).
- Migration: frameworks coexist in one target; migrate incrementally, new tests in Swift Testing. Interop (ST-0021; check Xcode availability) lets `XCTFail` helpers run from Swift Testing and vice versa: mode **complete** or **strict**, never **limited** or **none**, so issues stay errors and point to `Issue.record`.

## 12. Macros

Only for code the compiler could derive.

- Freestanding `#foo`; attached `@Foo` roles: member, peer, accessor, member-attribute, conformance (composable).
- Test with `assertMacroExpansion`; breakpoint in `expansion` and `po` the node.
- When it doesn't apply, throw or `context.addDiagnostic` (warnings, fix-its). Never silently emit uncompilable code.

## 13. Logging and debugging

- `Logger` from `os`, one per subsystem/category, never `print`.
- Non-numeric interpolations are redacted; `privacy: .public` only for non-personal data; `.private(mask: .hash)` to correlate.
- Levels: `debug` (not persisted, optimized away), `info`, `notice` (default), `error`, `fault`. Bug-report material at `error`/`fault`.
- Log a correlation ID; `log collect --device --start ...`, filter by subsystem in Console. Use `format:`/`align:`.
- LLDB: steps across `await`; `swift task info`; name tasks for the debugger and Instruments.

## 14. Unsafe code and interop

- Unsafe = precondition violations are undefined behavior. Safe traps are fine.
- `Span` over `Unsafe*Pointer`; raw pointers only for C interop. Then: smallest region, buffer pointers, never escape the closure, run **Address Sanitizer**.
- **Strict memory safety** in security-critical modules (⚠ 6.4 `@diagnose` per function).
- Interop is incremental: C/ObjC/C++ map in (C++ move-only → `~Copyable`); 6.3 `@c` exposes Swift to C (`@implementation` for existing headers). Adopt file by file; don't rewrite.

## 15. Modern syntax

| Instead of                                                            | Write                                                                                                    | Since |
| --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ----- |
| Nested ternaries; an immediately-called closure to initialize a `let` | `if`/`switch` **expressions**                                                                            | 5.9   |
| Overloads for 1, 2, 3… arguments                                      | **parameter packs** (`each T`), and `for` over a pack                                                    | 5.9   |
| `ObservableObject` + `@Published` on every property                   | **`@Observable`**                                                                                        | 5.9   |
| Polling an object for changes                                         | **`Observations { ... }`**, an `AsyncSequence` of transactional updates                                | 6.2   |
| `NotificationCenter` with stringly-typed `userInfo`                   | concrete notification types (`MainActorMessage` / `AsyncMessage`)                                        | 6.2   |
| `Process` + pipes for scripting                                       | the **Subprocess** package (`AsyncBufferSequence.strings()` for line-by-line output; 1.0 lands with 6.4) | 6.2+  |
| Hand-rolled string index math                                         | **Swift Regex**: literals for brevity, `RegexBuilder` for structure                                    | 5.7   |
| `[String]` of fixed size in a hot path                                | **`InlineArray<N, T>`**                                                                                  | 6.2   |
| `withUnsafeBufferPointer`                                             | **`.span`** / **`.bytes`** (`RawSpan`) / `OutputSpan`                                                    | 6.2   |
| Manual `Task.isCancelled` juggling to finish a write                  | `Task` **cancellation shield** (SE-0504)                                                                 | 6.4 ⚠ |
| Rebuilding a dictionary by hand to use the key                        | **`mapKeyedValues`**                                                                                     | 6.4 ⚠ |
| `@available(iOS ..., macOS ..., tvOS ..., watchOS ..., visionOS ...)` | **`@available(anyAppleOS ...)`**                                                                         | 6.4 ⚠ |
| `Rocket.SaturnV` when a type shadows a module                         | **module selector** `Rocket::SaturnV`                                                                    | 6.3   |
| Blanket "warnings as errors"                                          | **`@diagnose`** per declaration / warning group                                                          | 6.4 ⚠ |
| `@unchecked Sendable` because of a `weak var`                         | `weak let`; or state non-sendability with **`~Sendable`**                                                | 6.4 ⚠ |
| Manually parsing binary formats with pointers                         | **Swift Binary Parsing** (`ParserSpan`, overflow-checked parsing initializers)                           | 6.2   |
| Awkward test function names                                           | **raw identifiers**: `` @Test func `fruits have a tropical climate`() ``                                 | 6.0   |

Regex: compose Foundation parsers (`.date(...)`, `.currency(...)`), never hand-roll; explicit locale; `NegativeLookahead` or `Local` to stop backtracking.

## 16. Migrating to Swift 6

Enable Approachable Concurrency and (app modules) main-actor-by-default first; use Xcode's migration tooling (swift.org/migration).

1. Build with the new compiler in Swift 5 mode.
2. Per target, enable complete concurrency checking, UI/app layer first.
3. Fix warnings cheapest first (`var` globals → `let`, functions → `@MainActor`, public struct → `: Sendable`).
4. Flip the target to Swift 6 mode.
5. Next target, repeat.
6. Refactor afterwards, separately; never combine with enabling data-race safety.

## Not

- `DispatchSemaphore`/`NSCondition` across `await` (restructure).
- `Task.detached` or `DispatchQueue.global()` to offload (use `@concurrent`).
- Making a UI callback `async` (put a `Task { }` inside it).
