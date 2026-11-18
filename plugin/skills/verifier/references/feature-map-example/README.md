# Notes verification map

The maintained source for verifying Notes' user-facing behavior. Read this index before driving the app, then use the matching feature file as the recipe.

## Baseline preconditions

- Launch Notes at `http://127.0.0.1:4173` with `NOTES_DATA_DIR=/tmp/notes-verify-$RUN_ID` so concurrent runs don't share state.
- Seed notes titled `Quarterly plan` and `Grocery list`.
- Put `control-notes` and the `notes` CLI on `PATH`.
- Run `control-notes doctor`; require the expected URL, data directory, and build revision.
- Never drive an instance this run did not start.

## Driving conventions

- Start every recipe from the baseline unless its preconditions say otherwise.
- Prefer ARIA roles and accessible names over CSS selectors or DOM position.
- Commands are literal; keep quoted names and flags unchanged.
- Browser actions: `control-notes browser`. Terminal actions: `control-notes cli -- <command>`.
- Restore seeded data after a mutation; keep proof artifacts during cleanup.

## Proof and skip reporting

- Capture the user action and the resulting state, not only the final screen.
- UI proof: an ARIA snapshot and a screenshot with the app identity visible.
- CLI proof: command, stdout, stderr, exit code.
- Mutation proof: a read-only second view of the stored value.
- Record the feature ID and entry point with every artifact.
- Report an unreachable path with the attempted command and the unmet precondition; never report a skipped entry point as verified through another path.

## Feature entry contract

Each feature file: an H1 title, one paragraph of user-visible behavior, then exactly four H2s in order:

1. `Sub-features`: short IDs, one line per behavior.
2. `How to get to it (user POV)`: every user entry point.
3. `Driving it with <harness>`: starts with `Preconditions:`, then labeled bullets pairing each user action with an exact command and observable result.
4. `Gotchas`: traps that waste or invalidate a run.

No implementation details: only user paths, stable handles, required state, commands, and observable proof.

## Features

- [Search notes](./search.md): toolbar, keyboard, and CLI search with matching, empty, and clear states.
