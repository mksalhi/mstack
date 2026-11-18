# Accessibility

Review in two passes: keyboard only, where every flow must finish without a mouse, then screen reader, where every control must announce its name, role and state. Use native elements before ARIA, and remove ARIA before adding more. Contrast numbers belong to [colors](../colors/index.md), text sizing and iOS input zoom to [typography](../typography/index.md), and RTL to [layout](../layout/index.md). This file lists only the rules agents get wrong.

## Semantics

- Use `<a href>` for anything that navigates and `<button>` for actions. A `<div onClick>` is always a finding; the full polyfill is `role="button"`, `tabindex="0"`, and Enter and Space handlers.
- `aria-label` on a role-less `div` or `span` is ignored by most screen readers.
- `role="menu"` promises arrow-key app behavior. Site navigation is a `<nav>` holding a list.
- An `aria-labelledby` or `aria-describedby` that points at a missing ID fails silently.
- **Label in Name (2.5.3):** the accessible name contains the visible text. A "Send" button with `aria-label="Submit message"` breaks voice control.
- Repeated landmarks need labels (`<nav aria-label="Breadcrumbs">`). A skipped heading level is not a WCAG failure on its own; report it only when it breaks navigation.
- Never put `aria-hidden` or `role="presentation"` on a focusable element or any ancestor of one.

## Focus and keyboard

- Style `:focus-visible`. Adding only `outline-offset` keeps the browser ring, which is the best ring. `outline: 2px solid` with no color renders `currentColor`, which isn't automatically visible, so check a custom ring against every color it crosses. In `forced-colors`, use system colors such as `Highlight`.
- Use `tabindex` 0 or -1 only, never a positive value. Composite widgets (tabs, menus, toolbars, radio groups) take one Tab stop with a roving tabindex, and arrow keys move inside them.
- Follow the ARIA APG keyboard model for every custom widget:
  - Escape closes whatever opened last.
  - A menu button opens on ArrowDown and focuses the first item; ArrowUp opens it on the last item.
  - Home and End jump to the ends.
  - In a `<textarea>`, Enter adds a newline and ⌘/Ctrl+Enter submits.
- **Modals:** prefer `<dialog>.showModal()`. A custom overlay needs `aria-modal`, a name, and `inert` on everything behind it. Focus the first control on open, or the least destructive one in a destructive confirm. Return focus to the trigger on close. Add `overscroll-behavior: contain`.
- **SPA route change:** update `document.title`, then move focus to the new `<h1 tabindex="-1">` or to `<main>`.
- Put a skip link first when repeated navigation comes before `<main>`. Anchor targets under a sticky header need `scroll-margin-top`.

## Hit areas

- **The floor is 24×24 CSS px (WCAG 2.5.8 AA).** A smaller target passes if a 24px circle centered on it hits no other target. Aim for 44px on touch and 40px on desktop.
- **To enlarge a target, use `::after` on the wrapping `<label>` or `<button>`, never on the `<input>`.** Replaced elements don't render pseudo-elements reliably. Expanded areas must not overlap.
- **Decorative overlays (scrim, glow, full-bleed `::after`) swallow clicks.** Give them `pointer-events: none` and `aria-hidden`.
- **Gate hover styles** behind `(hover: hover) and (pointer: fine)`; see [mobile-web](../mobile-web.md).

## Forms

- Every control needs a `<label for>` or a wrapping `<label>`. A placeholder is never a label.
- Fields about the user need `autocomplete` (1.3.5): `name`, `email`, `tel`, `street-address`, `postal-code`, `cc-number`, `current-password` vs `new-password`, `one-time-code`. Add a section prefix where needed (`shipping street-address`).
- Codes, PINs and card numbers use `type="text" inputmode="numeric"`, not `type="number"`. Money uses `inputmode="decimal"`. Add `spellcheck="false"` on emails, codes and usernames. Never block paste or filter keystrokes.
- **Errors:**
  - Mark the field `aria-invalid="true"` and point `aria-describedby` at an inline message that isn't just a red border.
  - On submit, focus the first invalid field.
  - Never disable submit until the form is valid. Disable it only while the request runs, with a spinner beside the original label.
- **Disabled:** a tooltip on a natively `disabled` control never opens on keyboard or touch, so put the reason in visible text. Use `aria-disabled` only when the control must stay focusable, then block activation in code. Never set both.

## Announcements

Stop at the first rule that fits:

1. Focus moves to the change anyway: the focus move is the announcement.
2. The update is tied to a control: use `aria-describedby`.
3. Non-urgent: use `role="status"`, rendered empty before its text changes, or repeats aren't announced.
4. Urgent and not tied to a control: use `role="alert"`. Dynamically inserted alerts behave differently across screen readers, so test them.

Never move focus to a toast. A toast holding an action or an error stays until dismissed; a timed one gets at least 5s and pauses on hover or focus.

**Hidden text:** `.sr-only` uses `1px` with `clip-path: inset(50%)`, not `0`, which some screen readers skip, and never `display: none`.

## Alt text and media

- Decorative: `alt=""`, present but empty, because a missing `alt` gets the filename read aloud.
- Functional: name the action (`alt="Search"`, not "magnifying glass").
- Charts: a short `alt` plus the data nearby.
- Decorative SVG: `aria-hidden="true" focusable="false"`.
- Video needs captions. Anything moving for more than 5s needs a pause control (2.2.2), muted hero videos included.

## Motion and zoom

- Make motion opt-in with `@media (prefers-reduced-motion: no-preference)`. A global kill switch must use `0.01ms`, not `none`, so `transitionend` still fires.
- Under reduced motion, swap slides and scales for crossfades and drop parallax and autoplay. Keep spinners and focus changes.
- The page must work at 200% zoom and reflow at 320px width. Use `min-height` on text containers, and never cap zoom in the viewport meta.

## Reporting

Severity:

- **HIGH:** blocks a task, hides content from assistive tech, or is systemic.
- **MEDIUM:** makes a task meaningfully harder.
- **LOW:** isolated polish.

Verify by tabbing the flow, reading names and roles from the accessibility tree, and running an automated audit. Use the format in [review](../review/index.md#output).
