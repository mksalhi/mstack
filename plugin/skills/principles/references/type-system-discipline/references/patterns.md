# TypeScript patterns

Examples for each rule in [index.md](../index.md). See also [Boundary discipline](../../boundary-discipline.md).

## Branded types

Validate once at the boundary; downstream trusts the type. Match the `readonly __brand: 'X'` shape; don't invent a convention.

```ts
type AgentId = string & { readonly __brand: "AgentId" };

function parseAgentId(input: string): AgentId {
  if (!isUUID(input)) throw new Error(`Invalid agent id: ${input}`);
  return input as AgentId;
}
```

## Discriminated unions

Every variant shares the discriminant field with a unique literal value. Pick one name (`kind`, `type`, `tag`) and stick to it.

```ts
// Don't: boolean + optionals allow contradictory states
type DiffState = { loading: boolean; diff?: GitDiff; error?: string };

// Do
type DiffState =
  | { kind: "loading" }
  | { kind: "ready"; diff: GitDiff }
  | { kind: "error"; error: string };
```

## Constructive modeling

Build the type from legal parts instead of runtime checks on a loose type.

```ts
type NonEmpty<T> = [T, ...T[]];           // non-empty: no length check per caller
const isNonEmpty = <T>(arr: T[]): arr is NonEmpty<T> => arr.length > 0; // narrow a plain T[] once
type Pairs<T> = [T, T][];                 // even length

// Don't: type TimeRange = { start: Date; end: Date }; // start <= end in a comment
type TimeRange = { start: Date; durationMs: number }; // negative range unwritable
```

Keep `durationMs` a plain number; brand it only if a raw number could be passed where a duration is expected. Expose the reading you need on top (`pairs.flat()`, a `rangeEnd()` helper).

## Simplest total type

Keep `T[]` when every operation is total (`xs.reduce((a, b) => a + b, 0)` handles `[]`). Strengthen when the loose type forces a lie: `!`, `arr[0] as T`, a "should never happen" throw.

```ts
// Don't
function newestSession(sessions: Session[]): Session { return sessions.at(0)!; }
// Do
function newestSession(sessions: NonEmpty<Session>): Session { return sessions[0]; }
```

Returning `Session | undefined` is the other total signature.

## `unknown` over `any`

External data (RPC payloads, `JSON.parse`, `postMessage`, IPC, file contents, env vars, DB results) is `unknown`; narrow before use.

```ts
function handle(input: unknown) {
  if (typeof input === "object" && input !== null && "foo" in input) { /* narrowed */ }
}
```

## Schemas before hand-rolled guards

Before a property-by-property guard, use the repo's runtime schema library and existing schemas. One schema owns validation; derive the type from it. Never keep a schema, duplicate interface, and guard that can drift.

```ts
const UserSchema = z.object({ id: z.string().uuid(), role: z.enum(["admin", "member"]) });
type User = z.infer<typeof UserSchema>;
const parseUser = (input: unknown): User => UserSchema.parse(input);
```

Use `safeParse` when failure is an expected branch; use the equivalent helper for another library. Don't add a schema dependency for one guard.

## No `as` casts

Cast only after full validation (`return data as User` at the end of a parse function that checked every field). Never `const user = data as User`.

When removing an `as`, find why TS can't infer:
- Missing discriminant: add one, use a discriminated union.
- Overly wide source (e.g. `Record<string, unknown>`): narrow it.
- Untyped boundary: add a parse function or schema.
- Genuinely inexpressible: branded type or `satisfies`.

## Narrowing hierarchy

1. Discriminated union switch / if.
2. `in` operator (`"radius" in s` narrows to variants with that key).
3. `typeof` / `instanceof`.
4. User-defined type guard.
5. `as`, only after validation.

## Type guards

Must verify the claim; a lying guard is worse than `as`. Prefer discriminant narrowing.

```ts
function isCircle(s: Shape): s is Shape & { kind: "circle" } { return s.kind === "circle"; }
```

## Exhaustiveness

```ts
switch (s.kind) {
  case "circle": return Math.PI * s.radius ** 2;
  case "rect": return s.width * s.height;
  default: { const _exhaustive: never = s; return _exhaustive; }
}
```

Return-style in value-returning switches; in void switches use `void _exhaustive;` instead of `return`.

## `satisfies` over `as`

```ts
const config = { theme: "dark", cols: 3 } satisfies Config; // theme stays "dark", not string
```

## Boundary validation

Validate once where data crosses in; trust types inside; don't re-validate deep in call chains.
- Wire formats (proto, JSON-RPC): parse with `ignoreUnknownFields` for forward compatibility.
- Persisted JSON: versioned blob, try/catch around the parse.

## Schema-derived types

When a `.proto`, OpenAPI spec, GraphQL schema, or DB migration defines the shape, derive from generated types.

```ts
import type { ChecksMessage } from "<generated module>";
function renderChecks(s: Pick<ChecksMessage, "totalCount" | "checks">) { /* ... */ }
```

Reach for `Pick`, `Omit`, `Parameters`, `ReturnType`, `Awaited`, `typeof` before a new interface.

## Object args

```ts
// Don't: openFile(uri, { startLineNumber: 10, ... }). Swapped args still compile.
openFile({ uri, selection: { startLineNumber: 10, startColumn: 1, endLineNumber: 10, endColumn: 1 } });
```

Skip on hot paths: per-frame render, tokenizers, parsers, tight loops where allocation matters.
