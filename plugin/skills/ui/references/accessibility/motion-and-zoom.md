# Motion and zoom

## prefers-reduced-motion

Make motion opt-in:

```css
@media (prefers-reduced-motion: no-preference) {
  .card { transition: transform 200ms var(--ease-out); /* values from the animate area */ }
}
```

```tsx
<div className="motion-safe:transition-transform motion-safe:hover:-translate-y-1" />
```

Where opt-in isn't feasible in an existing codebase, use the global kill switch. Keep `0.01ms`, not `none`, so `animationend`/`transitionend` still fire:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### What to disable vs reduce

Reduced, not eliminated: target vestibular triggers, keep feedback.

| Disable entirely | Replace | Keep |
| --- | --- | --- |
| Parallax scrolling | Slide/scale/zoom transitions → opacity crossfade | Loading spinners and progress |
| Autoplaying video, GIFs, looping decoration | Smooth scrolling → instant jump | Instant state changes (hover color, focus ring) |
| Spinning, large-scale movement across the screen | Auto-rotating carousels → start paused | Brief functional feedback (button press) |

Animations are interruptible and driven by user input; nothing autoplays or refuses to stop.

## Autoplay and timed UI

- **No autoplaying media without visible controls** (WCAG 2.2.2). Anything moving, blinking or updating on its own for more than 5 seconds needs a visible pause or stop control, muted looping hero videos included.
- **Prefer explicit dismissal over timers.** Auto-dismiss only low-stakes confirmations. A toast with an action, an error or information the user may need stays until dismissed. Where one must time out, 5 seconds is the floor, and hover or focus pauses the timer.
- **Never put critical information only in a timed element** (e.g. the only undo link in a toast).

## Zoom and reflow

- **200% zoom** (WCAG 1.4.4): all content and functionality survives 200% text, and the viewport allows zoom.
- **Reflow at 320px** (WCAG 1.4.10): at 400% zoom on 1280px, the page works with vertical scrolling alone. Tables, maps and code blocks may scroll inside their own container.

Use `min-height`, not fixed heights, on anything containing text.

### rem vs px

Follow the codebase: where it sizes in `px` or an established Tailwind scale, never introduce mixed units. In new code or a `rem` codebase:

| Use `rem` | Use `px` |
| --- | --- |
| `font-size` | Borders and hairlines |
| `max-width` of text containers | Focus outline width and offset |
| Media-query breakpoints (`@media (min-width: 48rem)`) | `box-shadow` details |
| Spacing that should scale with text | Fixed-size decorations |

Breakpoints matter most: an `em`/`rem` query switches layout when a larger base font needs it; a `px` query does not.
