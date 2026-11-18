# Color usage

Values: [palette-generation.md](palette-generation.md). Names: [token-naming.md](token-naming.md). Pairs: [contrast.md](contrast.md).

## One color, one meaning

A near-miss hue reads as the same color.

```css
/* Bad: the accent means both "link" and "decorative heading" */
a { color: #3b82f6; }
.section-title { color: #4f8ef7; }

/* Good: interactive elements own the accent; headings stay neutral */
a { color: var(--color-accent-text); }
.section-title { color: var(--color-text-primary); }
```

The rule runs both ways: if the accent means interactive, an interactive element rendered neutral misleads too. Pair color with an icon, label or shape (the accessibility area owns this).

## Use tokens in their role

Apply a semantic token only for the role it names: never `color: var(--color-border)` on a caption or `background: var(--color-text-secondary)` on a tag. Roles: [token-naming.md](token-naming.md).

## One colored action per view

One filled primary action, neutral secondaries. Preserve an established hierarchy that communicates emphasis another way; don't recolor controls just to impose this. Selected states (active tab, checked segment) may use the accent on glyph and label.

## Gradients

```css
background: linear-gradient(#3b82f6, #ec4899);           /* sRGB: midpoint darkens and mutes */
background: linear-gradient(in oklab, #3b82f6, #ec4899); /* even brightness; best default */
background: linear-gradient(in oklch, #3b82f6, #ec4899); /* arcs around the hue wheel, stays vivid */
```

`oklch` is polar, so it passes through intermediate hues (blue-to-pink routes through purple). Opposite hues in a rectangular space go gray in the middle: switch to a polar space, or add a third stop. Control the polar direction with `in oklch shorter hue` (usually wanted) or `longer hue` (sweeps the spectrum).

**Banding** on large low-contrast gradients: widen the stop contrast, shrink the area, or overlay subtle noise.

**Keep text off gradients** where you can; otherwise measure the worst region or add a scrim.

## Color across cultures

Where color is load-bearing in finance, status or alerts, verify the meaning in every shipped locale.

| Color | Common Western reading | Elsewhere |
| --- | --- | --- |
| Red | Danger, loss, errors | Luck, prosperity; **gains** in Chinese financial UIs |
| Green | Success, gains, go | Losses in Chinese financial UIs |
| White | Purity, cleanliness | Mourning in parts of East Asia |
| Gold | Premium, luxury | Religious significance in some regions |

Make gain and loss per-locale tokens where the product ships to such markets.

## Light, dark and increased contrast

Every custom color needs light and dark variants ([palette-generation.md](palette-generation.md)), plus an increased-contrast one:

```css
:root { --color-accent-solid: #3b82f6; }
@media (prefers-color-scheme: dark) { :root { --color-accent-solid: #60a5fa; } }
@media (prefers-contrast: more) { :root { --color-accent-solid: #1d4ed8; } }
```

The increased-contrast variant widens the foreground/background gap by at least 15 points of perceived lightness, then re-verifies against Lc 90 body and Lc 75 non-body.
