# Interface copy

Match the voice of the copy around it; a deliberate brand voice isn't a defect. Flag copy only for inconsistency, ambiguity, translation risk, or a tone that doesn't fit the stakes: plain and calm for errors and destructive actions, never playful. Rendering belongs to [typography](typography/index.md), error markup to [accessibility](accessibility/index.md), and room for longer strings to [layout](layout/index.md).

- **One term per concept.** "Archive" in the menu is never "Move to storage" in the toast. Use one flow vocabulary: Get started, then Continue or Next (pick one), then Done.
- **Address the reader as "you".** In errors, avoid "we": write "Unable to load content".
- **Buttons start with a verb and repeat the consequence.** "Delete this project?" offers `Delete project` and `Cancel`. Never bare Yes, No or OK on a consequential action.
- **Links read on their own.** Write "Learn more about exports", never "Click here".
- **Toggles describe the ON state.** "Send read receipts", not "Don't send read receipts".
- **Errors sit beside the field and say how to fix it.** "Choose a password with at least 8 characters", not "Too short". No blame, no "oops", no exclamation marks. An error that keeps firing means the interaction needs a redesign.
- **Empty states say what goes here, then give one action.** A filtered empty state names the query and offers a way out: "No results for 'quarterly'. Clear filters".
- **Never concatenate around a variable.** `"You have " + n + " messages"` breaks plurals and translation, so use one templated string with plural rules.
- **Match the device.** Say tap on touch, click with a pointer, and select when it could be either.
- **Use sentence case** unless the project already uses title case consistently.
- **A placeholder is an example**, such as `name@example.com`, never the label.

**Severity:**

- **HIGH:** misleads the user, or hides how to recover.
- **MEDIUM:** inconsistent terms or capitalization.
- **LOW:** wording polish.

Use the format in [review](review/index.md#output).
