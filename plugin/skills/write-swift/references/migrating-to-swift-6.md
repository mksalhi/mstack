# Migrating to Swift 6

Enable Approachable Concurrency and (app modules) main-actor-by-default first; use Xcode's migration tooling (swift.org/migration).

1. Build with the new compiler in Swift 5 mode.
2. Per target, enable complete concurrency checking, UI/app layer first.
3. Fix warnings cheapest first (`var` globals → `let`, functions → `@MainActor`, public struct → `: Sendable`).
4. Flip the target to Swift 6 mode.
5. Next target, repeat.
6. Refactor afterwards, separately; never combine with enabling data-race safety.
