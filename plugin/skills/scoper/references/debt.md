Collect every `scoper:` shortcut comment into one ledger so a deferral can't quietly become permanent.

## Scan

Skip `node_modules`, `.git`, and build output. The comment prefix keeps prose that only mentions the convention out:

`grep -rnE '(#|//|/\*|--) ?scoper:' .`

## Output

One row per hit, grouped by file. The convention is `scoper: <ceiling>, <upgrade path>`:

`<file>:<line>, <what was simplified>. ceiling: <the limit named>. upgrade: <the trigger to revisit>.`

- Owner per row on request: `git blame -L<line>,<line>`.
- Tag a marker naming no upgrade path or trigger `no-trigger`.
- End with `<N> markers, <M> with no trigger.` Nothing found: `No scoper: debt. Clean ledger.`

## Boundaries

Reads and reports only. Writes the ledger to a file (e.g. `SCOPER-DEBT.md`) only when asked. One-shot. "normal mode" reverts.
