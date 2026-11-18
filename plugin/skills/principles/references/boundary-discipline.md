# Boundary discipline

- Guard at boundaries; trust internal types. Business logic in pure functions; shell thin.
- Boundaries (CLI args, config, external APIs, network): validate defensively; parse raw into domain types; validate config at parse time.
- Inside: typed data, propagate errors; no re-validation or deep nil checks.
- Do not re-export transport/storage/framework/wire types; expose domain concepts.
- Pure, framework-free functions: parsing, prompt construction, scoring.
- Tests: Is data crossing a boundary? Can this be a pure function?
