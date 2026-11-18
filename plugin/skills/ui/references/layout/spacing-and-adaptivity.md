# Spacing and adaptivity

## Breathing room between targets

Where the project has no density scale:

| Between | Starting point |
| --- | --- |
| Adjacent bordered/filled controls (buttons, inputs) | `12px` |
| Around borderless controls (text buttons, icon buttons) | `24px` |
| Unrelated control groups | `24px`+ (2× the intra-group gap) |

Compact professional tools may use less where hit areas stay distinct and never overlap; preserve an established, usable density. Target sizes and hit-area expansion belong to the [accessibility area](../accessibility/hit-areas.md); these clearances are additional.

## Inset buttons from the edges

In content layouts, keep buttons inside the layout margins (near `16px` inline on mobile without a layout token); they may still span the content width. Edge-to-edge is valid only for deliberate platform chrome that accounts for safe areas.

```css
/* Good: inset action bar */
.action-bar {
  padding-inline: 16px;
  padding-bottom: calc(16px + env(safe-area-inset-bottom));
}
.action-bar button { width: 100%; border-radius: 12px; }

/* Bad: button glued to all three edges */
.action-bar button { width: 100vw; border-radius: 0; position: fixed; bottom: 0; }
```

## Progressive disclosure needs an affordance

Keep the product's established cue; otherwise:

- **Peeking items.** In a horizontal scroller, size items so the next peeks `16–32px` past the container edge. Container padding creates the peek; snap points stay on the content edge.
- **Disclosure controls.** A chevron or "Show more" labelled with what is hidden: "Show 12 more results", not "More".
- **Truncation cues.** Ellipsis plus a way to expand; mechanics belong to the [typography area](../typography/index.md).

```css
.scroller {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-inline: 24px;
  scroll-padding-inline: 24px;
  scroll-snap-type: x mandatory;
}
.scroller > * {
  flex: 0 0 calc(100% - 48px - 24px); /* container minus margins minus peek */
  scroll-snap-align: start;
}
```

## Content bleeds, controls float

- **Content layer**: backgrounds, hero media and scrollable lists extend to the viewport edges.
- **Control layer**: text and controls stay inside layout margins and safe areas.

```css
.article { display: grid; grid-template-columns: 1fr min(65ch, calc(100% - 48px)) 1fr; }
.article > * { grid-column: 2; }
.article > .full-bleed { grid-column: 1 / -1; }

.fab {
  position: fixed;
  inset-inline-end: calc(16px + env(safe-area-inset-right));
  bottom: calc(16px + env(safe-area-inset-bottom));
}
```

## Hold structure until it breaks

- Break where the layout stops fitting (sidebar squeezes content below its minimum measure, grid columns drop below usable width), not at `768px` because a preset says so.
- Collapse late; keep the expanded structure while it fits.
- Prefer **container queries** for components:

```css
.card-list { container-type: inline-size; }
@container (max-width: 400px) { .card { grid-template-columns: 1fr; } }
```

Test the smallest and largest supported sizes first.

## Plan for growth and clipping

String expansion varies by language and source length; never rely on one percentage.

- No fixed widths sized to English labels: `max-width` plus wrapping.
- No fixed heights on text containers: `min-height` where a floor is needed.
- Buttons size from their label (`padding-inline: 16px; white-space: nowrap;`), never a hardcoded width.
- Test with pseudo-localization or a long-string locale before shipping.

**Clipping.** Never park a critical action at the bottom edge of a resizable pane, below the fold of a fixed-height modal, or behind an expanding keyboard. Keep primary actions in stable chrome: a sticky footer with safe-area padding or the top of the view. When a modal's content scrolls, its action row does not.
