# Interface writing

Clear and brief beats clever; consistent beats varied. The best error message is the interaction redesigned so the error cannot happen.

Rendering (capitalization via `text-transform`, truncation, smart punctuation) belongs to the [typography area](typography/index.md); error markup and announcements to the [accessibility area](accessibility/index.md); room for translated strings to the [layout area](layout/index.md).

## Recon the existing voice

Read nearby copy first: terminology, localization conventions, any voice or content style guide. A deliberate brand voice is not a defect; flag a departure from plain language only when it creates inconsistency, ambiguity, translation risk, or a tone the stakes don't support.

## One voice, flexible tone

Existing copy sets the voice; a local edit doesn't invent a new one. Keep terms consistent ("Archive" in the menu is not "Move to storage" in the toast). Tone flexes with stakes:

| Context | Tone |
| --- | --- |
| Success, onboarding, empty states | Warm, can be light |
| Routine actions, settings | Neutral, minimal |
| Errors, destructive confirmations | Calm, plain, zero playfulness |
| Data loss, security | Serious, explicit |

## Address the reader directly

"You", not "the user". In errors avoid "we": "Unable to load content", not "We're having trouble loading this content" (an established first-person voice may stay in low-stakes copy). Possessives sparingly: "Favorites", not "Your Favorites". Hold one perspective per flow.

## Plain words over clever ones

Words a tired reader gets on the first pass; delete words that do no work. No idioms, colloquialisms or humor that won't translate. No unnecessary gender ("Subscribers can post recipes"). Match the device: "tap" on touch, "click" with a pointer, "select" when both apply.

Never build a sentence from fragments around a variable (`"You have " + n + " new messages"`); use a full templated string with proper pluralization.

## Verb-first buttons

Labels start with a verb: "Send", "Save draft", "Delete project". Never "OK!", "Let's go!", or bare "Yes"/"No" on a consequential action. A confirmation button repeats the consequence: "Delete this project?" offers `Delete project` and `Cancel`.

## Consistent flow vocabulary

One vocabulary per flow: "Get started" to enter, "Continue" or "Next" (pick one) to advance, "Done" to finish.

## Links describe their destination

Link text makes sense out of context: "Read the billing docs", never "Click here". Suffix every "Learn more": "Learn more about exports".

## One capitalization policy

Sentence case by default; title case only where the project already uses it consistently. Hold one policy across every instance of an element type.

## Settings describe the ON state

Label a toggle for what happens when on: "Send read receipts", not "Don't send read receipts". Link straight to a referenced setting ("Notification settings") rather than describing the path.

## Errors say how to fix, next to where it broke

Place the error beside the failing field and make it an instruction:

| Bad | Good |
| --- | --- |
| That password is too short | Choose a password with at least 8 characters |

No blame, no "oops", no exclamation marks. Phrase hints positively ("Use only letters") and show them before the mistake. When the same error keeps firing, redesign the interaction.

## Empty states point forward

Say what this place is, how to fill it, and offer one next action ("No projects yet" / "Projects keep your tasks and files together." / `Create a project`), never a bare "No results." A search or filter empty state names the query and offers an exit: "No results for 'quarterly'. Clear filters". Never park persistent information in an empty state.

## Placeholders are examples, not labels

A placeholder shows the expected format (`name@example.com`, `DD/MM/YYYY`); every field keeps a visible label.

## Reporting

**Severity.** `HIGH` misleads the user or hides how to recover from an error. `MEDIUM` breaks voice, terminology or capitalization consistency. `LOW` is isolated wording polish.

**Verification.** Source alone suffices: every label against the action it invokes, every error for a stated fix, terminology against surrounding copy.

**Format.** Use the standalone format in the review area's [review format](review/review-format.md#standalone-domain-reports), with "No actionable writing findings" as the empty result.
