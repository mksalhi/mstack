# Contrast

Measure the **foreground** (text, icon, UI element) against the **background** it actually renders on, usually the nearest ancestor that paints one, not the page background.

**Report, don't repaint.** On failure, report the pair, its measured value and the threshold it misses; change colors only when asked. The accessibility area decides whether a pair must pass.

## APCA thresholds (recommended)

APCA is the better default for design decisions. Simplified from its full size/weight table:

| Content type | Minimum | Preferred |
| --- | --- | --- |
| Body text (columns or blocks of text) | Lc 75 | Lc 90 |
| Non-body text (labels, headlines) | Lc 60 | Lc 75 |
| Large text (≥36px) | Lc 45 | Lc 60 |
| UI components | Lc 30 | n/a |

Lc 30 is also the minimum for disabled and placeholder text; Lc 15 is the floor for a non-text element to be discernible. Lc is signed (positive: dark on light); compare the absolute value.

## WCAG 2 thresholds (for legal compliance)

Required for formal WCAG 2.x conformance claims.

| Content type | AA | AAA |
| --- | --- | --- |
| Normal text (<24px / <18.5px bold) | 4.5:1 | 7:1 |
| Large text (≥24px / ≥18.5px bold) | 3:1 | 4.5:1 |
| UI components and graphical objects | 3:1 | n/a |

18pt ≈ `24px`, 14pt bold ≈ `18.5px`. When a project must claim WCAG conformance, WCAG is the gate and APCA the tiebreaker above it.

## Fixing a failing pair (on request)

**Change lightness first**, holding hue and saturation, then remeasure.

```css
/* Failing (Lc ≈ 50) */
color: #7d93b0; background: #eef2f7;
/* Fixed: darker text, same hue (Lc ≈ 90) */
color: #2b3a4f; background: #eef2f7;
```

- **Mid-lightness backgrounds cap the result.** Near 75% perceived lightness even black reaches only about Lc 60; body text needs a background near one extreme, so change the background.
- **Pushing lightness can leave the gamut.** Reduce saturation to stay renderable ([color-formats.md](color-formats.md)).

Always remeasure after a change.

## Quick approximations

First pass only; measure before reporting. For body text at |Lc| ≥ 75:

- **Light background (above ~90% perceived lightness):** foreground below ~35%.
- **Dark background (below ~25%):** foreground above ~90%.

APCA is polarity-aware, so mirrored pairs score differently. Text polarity crossover is around 73% background lightness: above it dark text, at or below it light text (white still wins between roughly 60% and 73%).

## What to check

- **Every pair, in every appearance.**
- **Translucent surfaces** (`backdrop-filter` headers, overlays): test against the lightest and darkest content behind, or make the surface opaque enough.
- **Computed colors** (`color-mix()`, relative color syntax, opacity modifiers): measure the rendered result.
- **Text over images**: measure the worst region, or guarantee a background with a scrim.
