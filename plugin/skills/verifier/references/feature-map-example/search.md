# Search notes

Preconditions:
- Notes healthy at http://127.0.0.1:4173; control-notes doctor reports expected URL and data directory.
- Data directory contains “Quarterly plan” with body “Draft budget”.

Open search:
- Toolbar: control-notes browser click --role button --name "Search" (dialog opens focused).
- Keyboard: control-notes browser press --key "/" (close dialog first).

Queries:
- Title: control-notes browser fill --role searchbox --name "Search notes" --value "quarterly" → results contain “Quarterly plan”, not “Grocery list”.
- Body: fill “budget” → “Quarterly plan” remains with a body-match excerpt.
- Empty: query “volcano” → status “No matching notes” after results settle.

Open result:
- control-notes browser click --role link --name "Quarterly plan" → dialog closes; editor heading “Quarterly plan”.

Clear query:
- control-notes browser click --role button --name "Clear search" → searchbox empties; “Recent notes” shows.

CLI:
- control-notes cli -- notes search "quarterly" --format json → exit 0; stdout one object titled “Quarterly plan”. With “volcano”, stdout is [].

Proof:
- control-notes browser snapshot --aria --path artifacts/search/results.aria.txt
- control-notes browser screenshot --path artifacts/search/results.png

Gotchas:
- “/” inserts text if editor/searchbox is focused.
- Results debounce; wait for list or empty status.
- Archived notes excluded unless “Include archived” is on.
- CLI is human-readable by default; use --format json.
- Opening a result changes browser state; reopen search before proving another query.
