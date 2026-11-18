# Macros, logging and unsafe code

## Macros

Only for code the compiler could derive.

- Freestanding `#foo`; attached `@Foo` roles: member, peer, accessor, member-attribute, conformance (composable).
- Test with `assertMacroExpansion`; breakpoint in `expansion` and `po` the node.
- When it doesn't apply, throw or `context.addDiagnostic` (warnings, fix-its). Never silently emit uncompilable code.

## Logging and debugging

- `Logger` from `os`, one per subsystem/category, never `print`.
- Non-numeric interpolations are redacted; `privacy: .public` only for non-personal data; `.private(mask: .hash)` to correlate.
- Levels: `debug` (not persisted, optimized away), `info`, `notice` (default), `error`, `fault`. Bug-report material at `error`/`fault`.
- Log a correlation ID; `log collect --device --start ...`, filter by subsystem in Console. Use `format:`/`align:`.
- LLDB: steps across `await`; `swift task info`; name tasks for the debugger and Instruments.

## Unsafe code and interop

- Unsafe = precondition violations are undefined behavior. Safe traps are fine.
- `Span` over `Unsafe*Pointer`; raw pointers only for C interop. Then: smallest region, buffer pointers, never escape the closure, run **Address Sanitizer**.
- **Strict memory safety** in security-critical modules (⚠ 6.4 `@diagnose` per function).
- Interop is incremental: C/ObjC/C++ map in (C++ move-only → `~Copyable`); 6.3 `@c` exposes Swift to C (`@implementation` for existing headers). Adopt file by file; don't rewrite.
