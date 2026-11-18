# Accessibility

Review in two passes: keyboard only (complete every flow without a mouse), then screen reader (every control announces name, role, state). Prefer native elements over ARIA; remove ARIA before adding more. Contrast to [colors](../colors/index.md), text sizing and iOS input zoom to [typography](../typography/index.md), RTL to [layout](../layout/index.md).

## Semantics

- Use <a href> for navigation and <button> for actions. A <div onClick> must be fully polyfilled: role="button", tabindex="0", Enter/Space handlers.
- aria-label on role-less div/span is ignored by most screen readers.
- role="menu" requires arrow-key app behavior; site navigation is <nav> with a list.
- aria-labelledby / aria-describedby must reference existing IDs.
- Label in Name (2.5.3): accessible name includes the visible text.
- Repeated landmarks need labels (e.g., <nav aria-label="Breadcrumbs">).
- Never put aria-hidden or role="presentation" on a focusable element or its ancestor.

## Focus and keyboard

- Style :focus-visible. In forced-colors, use system colors.
- Use tabindex only 0 or -1. Composite widgets: one Tab stop with roving tabindex; arrow keys move inside.
- Follow ARIA APG: Escape closes the last opener; menu buttons open on ArrowDown/Up to first/last item; Home/End jump to ends; in <textarea>, Enter newline, ⌘/Ctrl+Enter submits.
- Modals: prefer <dialog>.showModal(). Custom overlays need aria-modal, a name, inert behind, focus on open (least-destructive in confirms), return focus on close, and overscroll-behavior: contain.
- SPA route change: update document.title, then move focus to the new <h1 tabindex="-1"> or to <main>.
- Put a skip link first when repeated navigation precedes <main>. Targets under sticky headers need scroll-margin-top.

## Hit areas

- Minimum 24×24 CSS px (2.5.8 AA).
- Enlarge targets via ::after on wrapping <label>/<button>, never on <input>; expanded areas must not overlap.
- Decorative overlays swallow clicks: add pointer-events: none and aria-hidden.
- Gate hover styles behind (hover: hover) and (pointer: fine); see [mobile-web](../mobile-web.md).

## Forms

- Every control needs a <label>; placeholders are not labels.
- Add autocomplete for user fields: name, email, tel, street-address, postal-code, cc-number, current-password/new-password, one-time-code.
- Codes/PINs/cards: type="text" inputmode="numeric"; money: inputmode="decimal". Add spellcheck="false" on emails, codes, usernames. Never block paste or filter keystrokes.
- Errors: set aria-invalid="true", reference inline text via aria-describedby, focus the first invalid on submit. Never disable submit until valid; disable only while the request runs, with a spinner beside the original label.
- Disabled: tooltips won’t open on native disabled; put the reason in visible text. Use aria-disabled only if it must stay focusable; never set both.

## Announcements

1. If focus moves to the change, the move is the announcement.
2. If tied to a control, use aria-describedby.
3. Non-urgent: role="status" rendered empty before updates.
4. Urgent and not tied: role="alert".

Never move focus to a toast. Action/error toasts persist; timed toasts get ≥5s and pause on hover/focus. Hidden text: .sr-only uses 1px with clip-path: inset(50%), never display: none.

## Alt text and media

- Decorative: alt="". Functional: name the action. Charts: short alt plus nearby data.
- Decorative SVG: aria-hidden="true" focusable="false".
- Video needs captions; anything moving >5s needs pause.

## Motion and zoom

- Make motion opt-in with @media (prefers-reduced-motion: no-preference); global kill switch uses 0.01ms, not none.
- Under reduced motion: crossfades; drop parallax/autoplay; keep spinners and focus.
- Must work at 200% zoom and reflow at 320px; never cap zoom in viewport meta.

## Reporting

Verify by tabbing flows, checking the accessibility tree, and running an automated audit. Use [review](../review/index.md#output).
