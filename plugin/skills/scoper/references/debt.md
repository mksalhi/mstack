Skip `node_modules`, `.git`, and build output.

`grep -rnE '(#|//|/\*|--) ?scoper:' .`

One row per hit, grouped by file. `scoper: <ceiling>, <upgrade path>`.

`<file>:<line>, <what was simplified>. ceiling: <the limit named>. upgrade: <the trigger to revisit>.`

Tag lacking upgrade path/trigger `no-trigger`. End with `<N> markers, <M> with no trigger.` Nothing found: `No scoper: debt. Clean ledger.`

Read-only; write `SCOPER-DEBT.md` only if asked.
