# Semantics and ARIA

## The rules of ARIA

1. If a native element with the semantics and behavior you need exists, use it instead of ARIA.
2. Don't change native semantics unless you really have to.
3. Every interactive ARIA control must be keyboard-operable; a role promises the full keyboard model, states and behavior.
4. Never put `role="presentation"` or `aria-hidden="true"` on a focusable element.
5. All interactive elements must have an accessible name.

## Button vs link vs div

| Element | Use for | Why |
| --- | --- | --- |
| `<a href>` | Navigation: anything that goes somewhere or changes the URL | Free Cmd/Ctrl/middle-click, right-click → copy link, Enter activation |
| `<button>` | Actions: submit, toggle, open, delete | Free focus, Enter *and* Space activation, form semantics |
| `<div onClick>` | Nothing | No role, no focus, no keyboard; screen readers see plain text |

A "button" that navigates is a styled `<a>`. Where a native element is truly impossible, the full polyfill is `role="button"` plus `tabindex="0"` plus Enter and Space handlers.

## Landmarks and headings

- One visible primary `<main>`; `<header>`, `<nav>`, `<aside>`, `<footer>` are landmarks.
- Repeated landmark types need labels: `<nav aria-label="Primary">`, `<nav aria-label="Breadcrumbs">`.
- Don't report the one-`<h1>` or no-skipped-levels convention as a standalone WCAG failure without a concrete navigation or comprehension impact. Pick heading tags by structure; style size with CSS.
- `<title>` matches the current context, most specific first: `Billing · Settings · Acme`.

## Accessible names

Precedence: `aria-labelledby` > `aria-label` > native label (`<label>`, text content, `alt`) > `title`.

- Prefer visible text or `aria-labelledby` over `aria-label` (invisible, drifts, mistranslated).
- Icon-only buttons: `<button aria-label="Delete"><TrashIcon aria-hidden="true" /></button>`.
- WCAG 2.5.3 Label in Name: a "Send" button with `aria-label="Submit message"` breaks voice control.
- Names must exist even when the design omits visible labels.
- Add `translate="no"` to brand names, code tokens and identifiers.

## Common ARIA mistakes

| Mistake | Why it fails |
| --- | --- |
| `aria-label` on a plain `<div>` or `<span>` | Most screen readers ignore names on non-interactive, role-less elements |
| `<button role="button">` | Redundant role; adds noise, no benefit |
| `aria-hidden="true"` on or above a focusable element | Creates elements you can Tab to but that don't exist for screen readers |
| `aria-labelledby`/`aria-describedby` pointing at a missing ID | Silently produces no name or description |
| `role="menu"` on a nav list | `menu` promises app-style arrow-key behavior; site navigation is `<nav>` with a list |

## Disabled states

Native `disabled` removes the control from tab order, suppresses activation, applies `:disabled` and excludes it from form submission. `aria-disabled="true"` only announces the state.

- Never disable submit buttons; validate on submit and focus the first error ([forms.md](forms.md)).
- A tooltip on a natively `disabled` control never opens for keyboard or touch. Put the reason in visible text beside it, or use `aria-disabled="true"`, which stays focusable and hoverable.
- Use `aria-disabled="true"` where staying discoverable in tab order is intentional, or a custom control cannot use native `disabled`. Then block pointer and keyboard activation in the handler, prevent form submission where applicable, add explicit styling including forced-colors support, and explain nearby why it is unavailable.
- Never set both `disabled` and `aria-disabled` on one element.
- Disabled controls are exempt from contrast minimums; keep them legible anyway.
