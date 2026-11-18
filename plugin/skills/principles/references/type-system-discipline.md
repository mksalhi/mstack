# Type system discipline

**Rule:** Illegal states unrepresentable, parse at boundaries, no casts.

Make the compiler reject impossible states, mismatched primitives, and unhandled variants. Define errors and special cases out of existence rather than adding handlers. Applies to any typed language.

**Patterns:**

- **Make illegal states unrepresentable.** Model variants as sum types (TS discriminated unions, Rust/Swift/Kotlin enums with payloads, Scala sealed classes, Haskell/OCaml ADTs), not optional-field bags. `{ completed: boolean; completedAt?: Date }` admits `completed: true; completedAt: undefined`; derive the boolean (`completedAt !== null`) or use `{ kind: 'open' } | { kind: 'done'; at: Date }`. A bug that makes you ask "can this combination happen?" means the type is too loose.
- **Types are constructions, not restrictions.** Build the type from the values you want instead of carving a looser type with checks. Non-empty list = head plus rest; valid range = start plus duration. No representation is privileged: pick the shape that cannot build the illegal value and expose the interface callers need on top.
- **Brand semantic primitives.** `UserId` and `OrderId` must not be interchangeable: branded intersection (TS) or newtype. Validate once at creation, trust downstream. Same primitive, different meaning: brand.
- **External data is untyped until parsed.** RPC payloads, JSON, IPC, CLI args, config, env vars, DB rows: a parse function at every boundary into the typed model. See [Boundary discipline](boundary-discipline.md).
- **Don't lie to the type system.** Casts, unsafe coercions, and compiler-bypassing assertion functions are latent crashes. Prove the fact (validate, narrow, refine) or accept the cast as a hazard.
- **Exhaustive matching is the compiler's job.** Adding a variant must fail compilation where unhandled: `never` binding (TS), unannotated `match` (Rust), `-Wincomplete-patterns` (Haskell), sealed-class exhaustiveness (Kotlin).
- **Derive types from authoritative schemas.** Protobuf, OpenAPI, GraphQL, DB migration, design-token file, or any file owning a shape: derive, don't hand-roll. See [Encode lessons in structure](encode-lessons-in-structure.md).
- **Strengthen a type only where partiality appears.** An assertion, null check, or "should never happen" throw marks a too-weak type: push the check into the type, then stop. Types track the cases each use site must handle, not maximal precision. Prefer total functions: `sum` takes a plain list (empty = 0); `head` demands non-empty.

**Tests:**
- Can you write a comment saying when this field combination is valid? Too loose; split into a sum type.
- Where did this `any`/`as`/`assertNotNull` come from? Trace to the boundary and validate there.
- Will the compiler point the next agent to every case when a variant is added? If not, the match isn't exhaustive.
- Does this type duplicate a shape another file owns? Derive.
- Strengthening to keep an operation total, or just for precision? If nothing would panic, keep the plain type.

## TypeScript

Apply when reading or editing `.ts` or `.tsx`.

| Rule | Summary |
|------|---------|
| Discriminated unions | Model variants with a `kind` literal discriminant so impossible states can't be represented. No optional-field bags. |
| Branded types | Brand primitives with `& { readonly __brand: "X" }` so they can't be mixed up. Validate once at the boundary. |
| Constructive modeling | Build the shape so the illegal value can't be constructed. `[T, ...T[]]` for non-empty, `[T, T][]` for even length, `start` plus `duration` for a range. Not a runtime guard, not a wish for refinement types. |
| Simplest total type | Keep `T[]` while every operation on it stays total. Strengthen to `NonEmpty<T>` only where the loose type forces `!`, a cast, or a "should never happen" throw. |
| `unknown` over `any` | External data is `unknown`. |
| Schemas before guards | Before hand-writing a property-by-property type guard, use the repository's runtime schema library and infer the type from the schema, such as `z.infer`. |
| No `as` casts | Every `as` is a runtime crash waiting. Cast only after validation. |
| Narrowing hierarchy | Discriminant switch > `in` operator > `typeof`/`instanceof` > user-defined type guard > `as`. |
| Type guards | Must verify the claim; a lying guard is worse than `as`. Name them `isX` or `hasX`. |
| Exhaustiveness | Inline `const _exhaustive: never = x;` in default arms so the compiler errors when a new variant is added. |
| `satisfies` over `as` | Validates the value without widening literal types. |
| Boundary validation | Parse where data crosses in, into a named domain type. `Record<string, unknown>` (however spelled) stops at that parse. Trust types inside. See [Boundary discipline](boundary-discipline.md). |
| Schema-derived types | Reach for `Pick`/`Omit`/`Parameters`/`ReturnType`/`Awaited`/`typeof` before declaring a new interface. |
| Object args | Pass objects, not positional, so argument order is self-documenting. Skip on hot paths (per-frame render, tokenizers, parsers). |

Examples: [type-system-patterns.md](type-system-patterns.md).
