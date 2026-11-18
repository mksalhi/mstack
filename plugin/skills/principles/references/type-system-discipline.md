# Type system discipline

**Rule:** Illegal states unrepresentable, parse at boundaries, no casts.

- **Sum types, not optional-field bags.** `{ completed: boolean; completedAt?: Date }` admits `completed: true` with no date; use `{ kind: "open" } | { kind: "done"; at: Date }` or derive the boolean. If a bug makes you ask "can this combination happen?", the type is too loose. Pick one discriminant name per codebase (`kind`).
- **Construct, don't restrict.** Build the type from legal parts: non-empty is `[T, ...T[]]`, even length is `[T, T][]`, a range is `start` plus `durationMs` (not `start` and `end` with a comment).
- **Strengthen only where partiality shows.** Keep `T[]` while every operation stays total (`reduce` with a seed handles `[]`). An `!`, `arr[0] as T` or "should never happen" throw marks the spot to strengthen; then stop. `Session | undefined` is the other total signature.
- **Brand semantic primitives** with exactly `string & { readonly __brand: "UserId" }`. The one allowed `as` is at the end of the parse function that validated it.
- **External data is `unknown` until parsed** (RPC, `JSON.parse`, IPC, CLI args, env, DB rows). One parse at the boundary; trust types inside. See [Boundary discipline](boundary-discipline.md).
- **Schema before guard.** Use the repo's schema library and infer the type (`z.infer<typeof S>`, `safeParse` when failure is a branch). Never keep a schema, a duplicate interface and a guard that can drift. Don't add a dependency for one guard.
- **Derive from the owner of the shape** (proto, OpenAPI, GraphQL, migration, token file) with `Pick`, `Omit`, `Parameters`, `ReturnType`, `Awaited`, `typeof` before declaring an interface.
- **No `as`.** To remove one, find why inference fails: missing discriminant, a source too wide (`Record<string, unknown>`), an unparsed boundary, or truly inexpressible (brand or `satisfies`). A type guard must check its claim; a lying guard is worse than `as`. Name guards `isX`.
- **Narrowing order:** discriminant switch, `in`, `typeof`/`instanceof`, checked guard, `as` after validation.
- **Exhaustive by compiler.** Adding a variant must break the build where it is unhandled:

  ```ts
  default: { const _exhaustive: never = s; return _exhaustive; } // void switch: void _exhaustive;
  ```

  Rust: unannotated `match`; Haskell: `-Wincomplete-patterns`; Kotlin: sealed `when`.
- **`satisfies` over `as`** keeps literal types: `{ theme: "dark" } satisfies Config`.
- **Object args** over positional so swapped arguments can't compile, except on hot paths (per-frame render, tokenizers, parsers).
