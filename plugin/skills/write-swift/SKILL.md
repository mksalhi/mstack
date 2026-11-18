---
name: write-swift
description: Use when writing, reviewing, or migrating Swift (Swift 6 concurrency, @concurrent, actors, generics, Swift Testing, macros), or fixing a Swift concurrency error, hang, data race, retain cycle, or performance problem.
metadata:
  harness: "claude codex"
  platform: "darwin"
  scope: universal
---

# Write Swift

Baseline: Swift 6.3. ⚠ marks Swift 6.4 features. Concurrency rules assume the Swift 6.2 model.

Prefer: structs/enums; concrete types; some P; main-actor synchronous. Move to class/any P/async/@concurrent/actor only with a measured reason (profiling, forced hops).

## 1. Value types

- A struct with a mutable class property shares mutations across copies. Make the class immutable and expose via computed properties, or hide it behind copy-on-write.
- Copy-on-write: wrap a final class; before mutating, `isKnownUniquelyReferenced(&storage)`; copy if not unique.
- Noncopyable types (`~Copyable`) for unique ownership. Use `consuming` for finish methods; parameter ownership: `borrowing` (default), `consuming`, `inout`/`mutating`.

## 2. Errors and optionals

- Use typed throws (`throws(MyError)`) internally, in forwarding generics, or constrained environments. Public API: untyped `throws`.
- `throws` = `throws(any Error)`; non-throwing = `throws(Never)`.

## 3. Concurrency: single-threaded until profiling says otherwise

- Build settings: enable Approachable Concurrency everywhere. For app/UI modules set Default Actor Isolation = MainActor (package: `swiftSettings: [.defaultIsolation(MainActor.self)]`). Not for general-purpose libraries; libraries ship `nonisolated` APIs.

Swift 6.2 model: `async` does not leave the caller’s actor.
- `@concurrent`: always runs on the concurrent pool; use for your CPU-heavy work.
- `nonisolated`: runs wherever called. On a type, applies to all members (6.1+).
- Neither: stays on the caller’s actor.

- Profile (Time Profiler, hangs) before offloading; make code faster without concurrency first.
- `await` breaks atomicity: re-check state after it; never hold a lock or rely on thread-locals across it.

### Actor reentrancy

- Other work runs between `await`s on the same actor. Mutate state in synchronous methods; keep async methods thin and consistent at every `await`.
- Re-check caches/state after `await` or dedupe in-flight work.
- Actors are not FIFO (highest priority first). For ordering, use a single task or an `AsyncStream`.

## 4. Sendable

- Value types are inferred `Sendable` when non-public and their storage is. Public types must declare it.
- Actors and `@MainActor` classes are implicitly `Sendable`.
- Most model classes: neither `@MainActor` nor `Sendable`. To leave main, make them `nonisolated`, not `Sendable`.
- A non-`Sendable` value can be sent if the sender stops using it.
- `@Sendable` on function types only if they really cross domains.
- `@unchecked Sendable` only with real internal synchronization (e.g., `Mutex`). `nonisolated(unsafe)` is a last resort, not a warning silencer.

Fixing a data race, in order:
1) Don’t share: give each job its own instance. 2) Make it a `Sendable` value type. 3) Isolate to an actor. 4) Then `Mutex`/`Atomic` (`Synchronization`), or `@unchecked Sendable`.

Globals/statics: prefer `let` → `@MainActor` → `Mutex` → `nonisolated(unsafe)`. Globals init lazily and atomically.

Callback/delegate APIs: if you own the protocol, annotate `@MainActor`. If not, use a `nonisolated` method and `MainActor.assumeIsolated { }`; `@preconcurrency` on the conformance is shorthand. `@preconcurrency import` can temporarily silence an unmigrated module.

## 5. Structured concurrency

- Prefer structured tasks; they inherit cancellation, priority, and task-locals.
- `async let`: fixed number of children. `withTaskGroup`: dynamic; iterate results; use `withDiscardingTaskGroup` when children return nothing.
- `Task { }`: only for lifetimes that don’t fit a scope (delegate callback, tap, view appear). Inherits isolation/priority; you manage cancellation.
- `Task.detached`: almost never. If needed, put a task group inside one detached root.
- Cancellation is cooperative: check `Task.isCancelled` / `try Task.checkCancellation()` before expensive work (including sync helpers). For suspended work use `withTaskCancellationHandler`; its handler runs immediately and concurrently—protect its state with an atomic/lock, not an actor.
- Continuations (`withCheckedContinuation` / `withCheckedThrowingContinuation`): resume exactly once on every path. For delayed delegates, store it and nil it on resume. (⚠ 6.4 `Continuation` can be type-checked.)
- `AsyncStream`/`AsyncThrowingStream` to adapt handler APIs: build the source in the closure, `yield` from the handler, clean up in `onTermination`.

## 6. Concurrency in SwiftUI

- `View` and its `@State` are `@MainActor`; don’t annotate views or view models under main-actor-by-default.
- `@Sendable` closures (`visualEffect`, `Shape.path(in:)`, `Layout`, `onGeometryChange`) run off main. On an isolation error, capture the value, not `self`.
- Action callbacks are synchronous: do `withAnimation` state changes there; start a `Task` only for long work after. Keep async logic testable outside SwiftUI.

## 7. Protocols and generics

- Start concrete; introduce a protocol only to remove repeated code across types.
- Requirements are dynamically dispatched customization points; extension-only methods are static and get shadowed. Make customizable APIs requirements.
- `some` by default; `any` only for heterogeneous storage, optional underlying type, or full hiding. `any` erases associated types and blocks optimization.
- You can’t call a method consuming an associated type on `any P`; pass it to a function taking `some P` (implicit opening).
- Constrained opaque/existential types: `some Collection<Element>`. Prefer primary associated types (`protocol Container<Item>`). Use same-type `where` clauses to pin cross-protocol relationships.

## More

- performance, allocation, copies, ARC, `deinit` or retain cycles: [references/performance.md](references/performance.md)
- macros, `Logger` and LLDB, `Unsafe*` pointers or C/C++ interop: [references/macros-logging-unsafe.md](references/macros-logging-unsafe.md)
- writing or migrating tests (Swift Testing, XCTest interop): [references/testing.md](references/testing.md)
- moving a target to Swift 6 language mode: [references/migrating-to-swift-6.md](references/migrating-to-swift-6.md)
