# Type system discipline

- Use sum types; one discriminant name per codebase: kind.
- Construct, don’t restrict: non-empty [T, ...T[]]; even-length [T, T][]; ranges = start + durationMs.
- Strengthen only at partiality: keep T[] while total; a !, arr[0] as T, or “should never happen” marks refinement (often to Session | undefined).
- Brand semantic primitives exactly: string & { readonly __brand: "UserId" }. Only the brand emitted by the validating parse is allowed as-is.
- External data is unknown until parsed (RPC, JSON.parse, IPC, CLI args, env, DB rows). Parse once at the boundary; trust inside.
- Schema before guard: use repo schema lib; infer (z.infer<typeof S>); safeParse when failure is a branch. Don’t keep schema + interface + guard.
- No as. Fix inference: add discriminants; narrow too-wide sources; parse boundaries; or use brand/satisfies when truly inexpressible. Guards must check claims; name guards isX.
- Narrowing order: discriminant switch, in, typeof/instanceof, checked guard, as after validation.
- Exhaustive by compiler:
  ```ts
  default: { const _exhaustive: never = s; return _exhaustive; } // void switch: void _exhaustive;
  ```
- Prefer satisfies over as to keep literal types.
