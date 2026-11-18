# Testing with Swift Testing


XCTest only for UI automation (`XCUIApplication`), `XCTMetric`, and Objective-C tests/exceptions.

- `#expect(a == b)` with plain expressions; `try #require(...)` stops the test and unwraps.
- Suites are `struct`s (fresh instance per test, `init` for setup); `class`/`actor` only for `deinit` teardown.
- `@Test(arguments: [...])` instead of loops/copy-paste. Two collections = cross product; `zip()` for pairs.
- Traits: `.enabled(if:)`, `.disabled("reason")` (never comment tests out), `.bug(url)`, `.tags(...)`, `.timeLimit`, `.serialized`. `@available` over runtime `#available`.
- `withKnownIssue { }` for external failures (over `.disabled`). `confirmation` for N-times callbacks; `withCheckedContinuation` for one-shot callbacks with no async overload.
- Tests run parallel and randomized; fix dependencies instead of `.serialized`.
- Exit tests: `#expect(processExitsWith: .failure) { ... }` for `precondition`/`fatalError` (macOS, Linux, FreeBSD, Windows).
- Migration: frameworks coexist in one target; migrate incrementally, new tests in Swift Testing. Interop (ST-0021; check Xcode availability) lets `XCTFail` helpers run from Swift Testing and vice versa: mode **complete** or **strict**, never **limited** or **none**, so issues stay errors and point to `Issue.record`.
