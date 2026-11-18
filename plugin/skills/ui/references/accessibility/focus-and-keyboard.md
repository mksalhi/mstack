# Focus and keyboard

## Focus rings

Style `:focus-visible`, not bare `:focus`. Never `outline: none` or `focus:outline-none` without a visible replacement. Prefer the browser's unmodified indicator; adding only `outline-offset` preserves it. `outline: 2px solid` with no color renders `currentColor`, which is not automatically accessible.

```css
/* Best: keep the browser ring */
:focus-visible { outline-offset: 2px; }

/* Custom ring when the design requires one: the project's verified token */
:focus-visible { outline: 2px solid var(--focus-ring); outline-offset: 2px; }
```

```tsx
<button className="focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--focus-ring)]">Save</button>
```

A custom indicator must meet the project or WCAG target for visible area and change of contrast. Check the whole perimeter against every adjacent color it crosses (fills, surfaces, images, gradients, hover and selected states); a token, brand color or `currentColor` passes only on that rendered check.

In `forced-colors: active`, keep the default adjustment or name a system color such as `Highlight`. Use `forced-color-adjust: none` only where you checked the control stays perceivable.

Use `:focus-within` when a wrapper should light up while an inner input has focus.

## Skip link

```css
.skip-link { position: absolute; inset-inline-start: -999px; }
.skip-link:focus { inset-inline-start: 16px; top: 16px; }
```

```html
<a class="skip-link" href="#main">Skip to content</a>
<header>…</header>
<main id="main">…</main>
```

Give in-page anchor targets `scroll-margin-top` (e.g. `80px` under a sticky header).

## tabindex rules

- `tabindex="0"`: only for custom interactive elements that aren't natively focusable.
- `tabindex="-1"`: focus via `el.focus()` only; for headings you move focus to, modal containers, roving-tabindex members.
- Positive `tabindex`: never. Fix the DOM order instead.

### Roving tabindex

Tabs, menus, toolbars and radio groups occupy one Tab stop. Active item `tabindex="0"`, others `-1`; arrow keys move focus and the `0`:

```tsx
<button role="tab" tabIndex={i === activeIndex ? 0 : -1} aria-selected={i === activeIndex}
  onKeyDown={handleArrowKeys} /* ArrowLeft/ArrowRight move activeIndex, wrapping */>
```

## Focus trapping and restoration

Prefer native `<dialog>` with `showModal()` (trap, inert background and Escape for free). A custom overlay needs `role="dialog"`, `aria-modal="true"`, a name via `aria-labelledby`, and `inert` on everything behind it:

```tsx
// On open
document.getElementById("app-content").inert = true;
(dialog.querySelector("[autofocus]") ??
  dialog.querySelector("button, [href], input, select, textarea"))?.focus();
// On close
document.getElementById("app-content").inert = false;
triggerRef.current?.focus();
```

- On open, focus the first focusable element; for destructive confirmations, the least destructive action.
- On close, return focus to the trigger, or the nearest logical container if it is gone.
- `overscroll-behavior: contain` on the dialog.

## Keyboard patterns (ARIA APG)

Custom widgets must implement the full keyboard model their role promises.

| Widget | Keys |
| --- | --- |
| Dialog | Tab/Shift+Tab cycle inside (wrap at ends); Escape closes |
| Tabs | Arrow keys move between tabs (wrapping); Tab exits to the panel; Home/End jump to first/last |
| Menu button | Enter/Space/ArrowDown opens and focuses first item; ArrowUp opens and focuses last; arrows navigate; Escape closes and refocuses the button |
| Disclosure / accordion | Header is a `<button aria-expanded>`; Enter and Space toggle |
| Combobox | ArrowDown opens/moves into the list; Enter accepts; Escape closes and returns to the input; typing filters |
| Listbox / radio group | Arrow keys move selection; one Tab stop for the whole group |

- Escape dismisses whatever opened last: tooltip, then menu, then dialog.
- Arrows move within a composite widget; Tab moves between widgets.
- Tabs activate automatically on arrow focus when panels render instantly, manually (Enter/Space) when switching is expensive.
- Enter submits the focused input's form; in `<textarea>`, Enter is a newline and ⌘/Ctrl+Enter submits.

## SPA route changes

On route change, update `document.title`, then move focus to the new view's `<h1>` (with `tabindex="-1"`) or `<main>`. Restore scroll on back/forward; scroll to top on forward navigation.
