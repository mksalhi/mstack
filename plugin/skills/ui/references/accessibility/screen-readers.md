# Screen readers

## Visually hidden content

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}
```

Keep `1px`, not `0` (some screen readers skip zero-sized elements). Never `display: none` or `visibility: hidden` for content meant for assistive tech. Tailwind ships `sr-only`; skip links un-hide with `focus:not-sr-only`. Use it for context sighted users get visually (`<span class="sr-only">Opens in new tab</span>`, table captions, a label where `aria-label` isn't an option).

## Choosing how to announce a change

Stop at the first match:

1. **Focus moves there anyway** (opened modal, first invalid field): the focus move is the announcement.
2. **Tied to a control** (field error, character count): `aria-describedby` on the control.
3. **Non-urgent, untied** (toast, "Saved", result count, loading): polite `role="status"`.
4. **Urgent, untied** (form-level failure, session expiry): `role="alert"`.

## Live regions

| Mechanism | Politeness | Use for |
| --- | --- | --- |
| `role="status"` (= `aria-live="polite"` + `aria-atomic="true"`) | Waits for a pause | Toasts, "Saved", result counts, loading updates |
| `role="alert"` (= `aria-live="assertive"` + `aria-atomic="true"`) | Interrupts immediately | Errors and urgent problems only |

- For repeated polite updates, render a stable empty region before changing its text: `<div role="status" className="sr-only">{statusMessage}</div>`.
- Dynamically inserted `role="alert"` varies by screen reader; test target combinations.
- Default to polite; overusing `assertive` is the most common mistake.
- Keep messages short and self-contained.
- Never move focus to a toast. Give toasts a generous timeout or a dismiss button; never put the only path to an action inside an auto-dismissing one.
- Loading: `aria-busy="true"` on the updating region, announce "Loading…" politely, then the outcome ("Loaded, 12 results").

## aria-hidden

Removes the element and its subtree from assistive tech; use for decorative icons and visually duplicated content. Never on or above a focusable element; hiding something interactive means removing it from tab order too.

## Alt text

| Purpose | Alt | Example |
| --- | --- | --- |
| Decorative, or redundant with adjacent text | `alt=""` (empty, but present) | Logo next to the company name in text |
| Informative | Describe the meaning it adds | `alt="Ticket QR code"` |
| Functional (image is the link/button) | Describe the action or destination | Search icon → `alt="Search"`, not `alt="magnifying glass"` |
| Image of text | The exact text (better: use real text) | `alt="50% off everything"` |
| Complex (chart, diagram) | Short summary in `alt`, full data as a table or text nearby | `alt="Revenue by quarter, described below"` |

Never omit `alt`; screen readers then read the file name.

## SVG

- Decorative: `aria-hidden="true"` and `focusable="false"`.
- Meaningful inline: `role="img"` plus `aria-label="…"`, or a first-child `<title>` referenced by `aria-labelledby`.
- Simple cases: `<img src="icon.svg" alt="…">` is most reliable.

## Video and audio

Captions on prerecorded video; transcripts for audio. Never autoplay with sound; always render controls.
