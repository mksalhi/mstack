# Notes verification map

## Baseline
- Launch at http://127.0.0.1:4173 with NOTES_DATA_DIR=/tmp/notes-verify-$RUN_ID.
- Seed notes titled Quarterly plan and Grocery list.
- Put control-notes and the notes CLI on PATH.
- Run control-notes doctor; require expected URL, data directory, build revision.
- Never drive an instance this run did not start.

## Driving
- Prefer ARIA roles/names over CSS/position.
- Commands are literal; keep quoted names/flags unchanged.
- Browser: control-notes browser. Terminal: control-notes cli -- <command>.
- After mutations, restore seeds; keep proof artifacts.

## Proof/skip
- Capture action and resulting state.
- UI: ARIA snapshot + screenshot.
- CLI: command, stdout, stderr, exit code.
- If unreachable, report attempted command and unmet precondition; never claim a skipped entry point via another path.

## Feature entry contract
- H1, one user-visible paragraph, then exactly four H2s: `Sub-features`; `How to get to it (user POV)`; `Driving it with <harness>` (starts with `Preconditions:`; labeled bullets pairing each user action with an exact command and observable result); `Gotchas`.
- No implementation details: only user paths, stable handles, required state, commands, observable proof.

## Features
- [Search notes](./search.md): toolbar, keyboard, and CLI search with matching, empty, and clear states.
