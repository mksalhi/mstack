# Accessibility

Write every fix in the project's styling system, with the exact values below. Review with two walks: keyboard-only (every flow completes without a mouse), then screen-reader (every control announces name, role and state). When unsure, take the platform default over a custom rebuild, and remove ARIA rather than add it.

Contrast measurement and color fixes belong to the [colors area](../colors/index.md); text sizing and iOS input zoom to the [typography area](../typography/index.md); spatial RTL layout to the [layout area](../layout/index.md).

## Native elements first

Don't use ARIA when a native element exists: `<button>` for actions, `<a href>` for navigation, never `<div onClick>`. A real link supports Cmd/Ctrl/middle-click. No ARIA beats bad ARIA. Landmarks, button-vs-link and disabled states: [semantics-and-aria.md](semantics-and-aria.md).

## Visible focus rings

Style `:focus-visible`, not bare `:focus`; prefer the browser's unmodified indicator. A custom ring needs a project focus token or explicit color, verified against every adjacent color it crosses (`currentColor` included), at least a `2px` solid perimeter or equivalent area. Never `outline: none` without a verified replacement; preserve system colors in forced-colors mode. Recipes: [focus-and-keyboard.md](focus-and-keyboard.md).

## Full keyboard support

Every pointer interaction needs a keyboard path. Follow ARIA APG: Escape closes overlays, arrows move within composite widgets, Tab moves between widgets, Enter and Space activate. Use only `tabindex="0"` (join tab order) and `tabindex="-1"` (programmatic focus), never positive. Composite widgets use roving tabindex: active item `0`, others `-1`.

## Trap and restore focus

Modals set `inert` on the background, move focus inside on open, return it to the trigger on close, and add `overscroll-behavior: contain`.

## Minimum hit area

WCAG 2.5.8 AA: 24×24 CSS px, or one of its spacing, equivalent-control, inline, user-agent and essential exceptions. Aim for 44×44px on touch and 40×40px on desktop where density permits; extend with a pseudo-element to keep the visible element smaller. Never let extended hit areas overlap; give decorative layers `pointer-events: none`. Gate hover styling with the mobile-web area's hover query so it doesn't stick after a tap. Details: [hit-areas.md](hit-areas.md).

## Label and type every control

Every input gets a `<label for>` or wrapping `<label>`; a placeholder is never a label. Label and control share one hit target. Add `autocomplete` with a meaningful `name`, plus the `type` and `inputmode` for the right keyboard. Never block paste. See [forms.md](forms.md).

## Errors that announce

Keep submit enabled until the request starts, then disable with a spinner and the original label. Validate on submit: mark failing fields `aria-invalid="true"`, point `aria-describedby` at the inline error, focus the first invalid field.

Use native `disabled` when a control is unavailable. Use `aria-disabled="true"` only when it must stay focusable, then block pointer, keyboard and form behavior in code and style the state explicitly. A tooltip on a natively `disabled` control never opens: use text beside it, or `aria-disabled`.

## Accessible names everywhere

Icon-only buttons need a descriptive `aria-label`. Visible label text must appear in the accessible name. Decorative elements get `aria-hidden="true"`, never on a focusable element.

## Don't rely on color alone

Status needs a redundant cue: icon, text or underline. Work out which WCAG contrast requirement applies, measure the rendered pair with the colors area, and on failure report the pair and the requirement; leave the colors alone unless asked.

## Honor prefers-reduced-motion

Wrap motion in `@media (prefers-reduced-motion: no-preference)` (the animate area's pattern). Under reduced motion, replace slides and scales with opacity crossfades; kill parallax and autoplay. Regardless of preference: autoplaying media needs a visible pause control, and toasts with an action or error stay until dismissed. See [motion-and-zoom.md](motion-and-zoom.md).

## Announce dynamic content

`aria-describedby` for field validation; polite `role="status"` for non-urgent untied updates (toasts, result counts); `role="alert"` for urgent untied errors only. Repeated polite announcements need a stable empty region rendered before its text updates. Test dynamically inserted alerts on target screen readers. See [screen-readers.md](screen-readers.md).

## Alt text by purpose

Decorative: `alt=""`. Informative: describe the meaning. Functional: describe the action (`alt="Search"`, not `alt="magnifying glass"`).

## Structure is navigation

Descriptive headings forming a coherent outline: one `<h1>`, no skipped levels. One visible primary `<main>`. When repeated navigation precedes it, a "Skip to content" link is the first focusable element. Anchored headings get `scroll-margin-top`.

## Survive zoom and text resize

Work at 200% zoom and reflow at 320px width without horizontal scrolling. Use `min-height`, not fixed `height`, on text containers. Prefer `rem` breakpoints where they fit the codebase; never let the viewport meta cap zoom.

## Reporting

**Severity.** `HIGH` prevents a task, hides content from assistive technology, or is systemic. `MEDIUM` makes an interaction meaningfully harder. `LOW` is isolated polish.

**Verification.** Without a browser: accessible names on every interactive element, keyboard handlers on non-native controls, focus styles, `prefers-reduced-motion` guards, labels bound to inputs. With one: tab the flow in order, read computed names and roles from the accessibility tree, confirm a visible focus indicator at every stop, run an automated audit.

**Format.** Use the standalone format in the review area's [review format](../review/review-format.md#standalone-domain-reports), with "No actionable accessibility findings" as the empty result.
