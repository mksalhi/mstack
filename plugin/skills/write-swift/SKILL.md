---
name: write-swift
description: Use when writing, reviewing, or migrating Swift (Swift 6 concurrency, @concurrent, actors, generics, Swift Testing, macros), or fixing a Swift concurrency error, hang, data race, retain cycle, or performance problem.
metadata:
  harness: "claude codex"
  platform: "darwin"
  scope: universal
---

# Write Swift

**Baseline: Swift 6.3.** ⚠ marks Swift 6.4 features: check the toolchain and use the older form on 6.3 or earlier. Concurrency rules assume the Swift 6.2 model; on 6.1 or earlier the `async`/`@concurrent` rules in §3 do not apply.

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

- A struct holding a mutable class property is neither value nor reference: copies share mutations. Keep the class immutable, forward through computed properties, or make it `private` behind copy-on-write.
- Copy-on-write: wrap a final class in a struct; check `isKnownUniquelyReferenced(&storage)` before mutating, copy if false.

**Noncopyable types** (`~Copyable`) for unique ownership (file descriptor, transfer): double use becomes a compile error and struct `deinit` works. Mark the finishing method `consuming`. Parameter ownership: `borrowing` (default, read-only), `consuming`, `inout`/`mutating`.

## 2. Errors and optionals

- Typed throws (`throws(MyError)`) for internal code, error-forwarding generics, and constrained environments. Public API: untyped `throws`. `throws` = `throws(any Error)`; non-throwing = `throws(Never)`.

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

- Profile (Time Profiler, hangs) before offloading; make code faster without concurrency first. No tasks for trivial work, and no `async` on a function with nothing to await.
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

### `some` vs `any`

- `some P` by default; `any P` only for heterogeneous storage, optional underlying type, or full hiding. `any` erases associated types and blocks optimization.
- You can't call a method consuming an associated type on `any P`; pass it to a function taking `some P` (implicit opening).
- Constrained opaque/existential types: `some Collection<Element>`. Declare primary associated types (`protocol Container<Item>`) for what callers supply, not `Iterator`.
- Pin cross-protocol relationships with same-type `where` clauses (`where Self.CropType.FeedType == Self`).

## 8. Modern syntax

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

Log with `Logger` from `os`, never `print`; `privacy: .public` only for non-personal data.

Regex: compose Foundation parsers (`.date(...)`, `.currency(...)`), never hand-roll; explicit locale; `NegativeLookahead` or `Local` to stop backtracking.

## Tests and migration

- Swift Testing by default (`@Test`, `#expect`, `try #require`); XCTest only for UI automation, `XCTMetric` and Objective-C tests.
- Tests run in parallel and random order; fix shared state instead of adding `.serialized`.
- For a Swift 6 migration, enable Approachable Concurrency (and main-actor-by-default for apps) while still in Swift 5, then per target, UI first, turn on complete checking, fix the warnings and switch to Swift 6.
- Never combine the language-mode switch with refactoring; refactor afterwards.

## More

- Open `references/performance.md` when profiling or fixing allocation, copies, ARC, `deinit` or a retain cycle.
- Open `references/macros-logging-unsafe.md` when writing a macro, adding logging, or touching `Unsafe*` pointers or C/C++ interop.
- Open `references/testing.md` when writing parameterized tests, known issues, confirmations, exit tests or XCTest interop.
