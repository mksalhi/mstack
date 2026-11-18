# Search notes

A user finds notes by title or body text, opens a match, and can tell no matches from an unavailable search.

## Sub-features

- `search-open` opens search from each browser entry point.
- `search-match` returns title and body matches without changing note data.
- `search-open-result` opens a result in the editor.
- `search-empty` shows a complete empty state for a query with no matches.
- `search-clear` removes the query and restores the recent-notes view.
- `search-cli` returns the same matches from the terminal.

## How to get to it (user POV)

- Choose `Search` in the browser toolbar.
- Press `/` in the browser with focus outside an editable field.
- Run `notes search <query>`.

## Driving it with control-notes

Preconditions:

- Notes is healthy at `http://127.0.0.1:4173`; `control-notes doctor` reports the expected URL and data directory.
- The data directory contains `Quarterly plan` with body text `Draft budget`.

- **Toolbar entry.** Run `control-notes browser click --role button --name "Search"`. Dialog `Search notes` appears with focus in its searchbox.
- **Keyboard entry.** Close the dialog, then run `control-notes browser press --key "/"`. The same dialog appears; no slash is inserted.
- **Title match.** Run `control-notes browser fill --role searchbox --name "Search notes" --value "quarterly"`. `Search results` contains `Quarterly plan`, not `Grocery list`.
- **Body match.** Fill the searchbox with `budget`. `Quarterly plan` remains with a body-match excerpt.
- **Open result.** Run `control-notes browser click --role link --name "Quarterly plan"`. The dialog closes; the editor heading reads `Quarterly plan`.
- **Empty state.** Reopen search and fill `volcano`. Status `No matching notes` appears after search completes.
- **Clear query.** Run `control-notes browser click --role button --name "Clear search"`. The searchbox empties; `Recent notes` replaces the results.
- **CLI match.** Run `control-notes cli -- notes search "quarterly" --format json`. Exit code `0`; stdout has one object titled `Quarterly plan`. With `"volcano"`, stdout is `[]`.
- **Proof.** Run `control-notes browser snapshot --aria --path artifacts/search/results.aria.txt` and `control-notes browser screenshot --path artifacts/search/results.png`. Both identify Notes, the query, and `Quarterly plan`.

## Gotchas

- Pressing `/` while the editor or searchbox has focus inserts text.
- Results debounce; wait for the results list or empty status, not a fixed sleep.
- Archived notes are excluded unless `Include archived` is on.
- The CLI defaults to human-readable output; use `--format json` for stable assertions.
- Opening a result changes browser state; reopen search before proving another query.
