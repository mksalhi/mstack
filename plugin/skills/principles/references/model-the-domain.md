# Model the domain: structure catalog

Derive the shape from "what must never happen" and "how data is read".

- State machine over booleans or phase flags.
- Discriminated unions over loose optional params.
- Maps, registries and lookups over branching spread across files.
- Reducer, command or event over ad hoc mutation.
- One module owns each domain rule; execution order is not ownership.
- Small boundaries that gather invariants in one place.
- Queues, caches, indexes, graphs, trees or normalized collections when the access pattern demands them.

Prefer boring code when the shape is clear and local. Skip indirection that removes no branch or risk.
