# Design red flags

## Shallow module
Large interface hiding little complexity. Judge depth by hidden capability/policy vs surface; a deep module concentrates capability.
- Callers coordinate several methods for one operation.

## Information leakage
Several modules depend on one internal decision. Public re-exports of transport or wire types are leakage: parse external data into domain types; keep storage schemas, framework objects, and protocol details private.

## Temporal decomposition
Organizing by execution order repeats representation and invariants. Group by owned knowledge; keep methods together when they protect the same decisions.

## Pass-through method
Forwards same-shaped calls; delete or move responsibility. Keep only when adding policy, adaptation, or a distinct abstraction.
