# Create a note

A user saves a titled note from the browser or CLI, cancels an unfinished draft, and confirms the saved note from a second view.

## Sub-features

- `create-open` opens a blank editor from each browser entry point.
- `create-save` persists a title and body.
- `create-cancel` discards an unfinished browser draft.
- `create-cli` creates the same note shape from the terminal.

## How to get to it (user POV)

- Choose `New note` in the browser toolbar.
- Press `n` in the browser with focus outside an editable field.
- Run `notes create --title <title> --body <body>`.

## Driving it with control-notes

Preconditions:

- Notes is healthy at `http://127.0.0.1:4173`; `control-notes doctor` reports the expected URL and disposable data directory.
- No note is titled `Release checklist`.

- **Open editor.** Run `control-notes browser click --role button --name "New note"`. A form named `Note editor` appears with focus in `Title`.
- **Enter content.** Run `control-notes browser fill --role textbox --name "Title" --value "Release checklist"` and `control-notes browser fill --role textbox --name "Body" --value "Tag and publish"`. `Save note` becomes enabled.
- **Save note.** Run `control-notes browser click --role button --name "Save note"`. Status `Note saved` appears; the heading reads `Release checklist`.
- **Confirm persistence.** Run `control-notes browser click --role link --name "All notes"`, then `control-notes browser click --role link --name "Release checklist"`. The editor shows both saved values.
- **Cancel draft.** Open a new note, fill `Title` with `Discard me`, then run `control-notes browser click --role button --name "Cancel"`. The note list returns with no `Discard me` link.
- **CLI entry.** Run `control-notes cli -- notes create --title "CLI note" --body "Created from terminal" --format json`. Exit code `0`; stdout contains the new note ID and title.
- **Proof.** Run `control-notes browser snapshot --aria --path artifacts/create-note/list.aria.txt` and `control-notes browser screenshot --path artifacts/create-note/list.png`. Both show `Release checklist` and `CLI note`.

## Gotchas

- Pressing `n` while a textbox has focus types the character.
- Titles are trimmed on save; assert the rendered title, not the draft input.
- A save status alone is not proof; reopen the note from the list.
- Remove `Release checklist` and `CLI note` in fixture cleanup; keep their proof artifacts.
