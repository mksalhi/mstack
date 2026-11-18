# Design red flags

Screen every candidate before synthesis. A red flag means revise or reject the shape.

## Shallow module

Large interface hiding little complexity. Judge depth by capability and policy hidden relative to surface size; prefer a simple interface over substantial behavior. A deep module concentrates capability behind one interface; a deep call chain scatters it across layers.

Signs:
- Callers coordinate several methods for one operation.
- Public options expose internal stages or implementation choices.
- Learning the interface doesn't spare the caller learning the implementation.

## Information leakage

Several modules depend on one internal decision (representation, policy, protocol detail), so changing it needs coordinated edits. Public re-exports of transport or wire types are leakage: parse external data into domain types behind the interface; keep storage schemas, framework objects, and protocol details private.

## Temporal decomposition

Modules organized by execution order (load, validate, transform, save) instead of owned knowledge, repeating one representation and its invariants across boundaries. Group by domain knowledge and ownership; methods running at different times belong together when they protect the same decisions.

## Pass-through method

Forwards the same arguments to a same-shaped method, adding a layer without hiding complexity. Remove it or move responsibility to the module that completes the operation. Keep a forwarding boundary only when it adds policy, adaptation, or a distinct abstraction.
