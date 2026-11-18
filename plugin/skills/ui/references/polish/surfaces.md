# Surfaces

## Concentric border radius

```
outerRadius = innerRadius + padding
```

Apply where nested layers share a visible, even inset. Past `24px` of padding, or with deliberately asymmetric padding or independent layers, choose each radius independently and keep established component tokens.

```tsx
// Good: outer radius accounts for padding
<div className="rounded-2xl p-2">   {/* 16px radius, 8px padding */}
  <div className="rounded-lg">      {/* 8px radius = 16 - 8 */}

// Bad: same radius on both
<div className="rounded-xl p-2">
  <div className="rounded-xl">
```

## Optical alignment

### Buttons with text + icon

Starting point: `icon-side padding = text-side padding - 2px`.

```css
.button-with-icon {
  padding-inline-start: 16px;
  padding-inline-end: 14px; /* trailing icon side = text side - 2px */
}
```

Tailwind: `ps-4 pe-3.5`.

### Play button triangles

Shift the glyph slightly right: `.play-button svg { transform: translateX(2px); }` (physical correction to the glyph itself).

### Asymmetric icons (stars, arrows, carets)

Best: fix the SVG's viewBox or path. Fallback: a wrapper nudge such as `translate-x-px`.

## Shadows instead of borders

Replace a border used for depth on **buttons, cards and containers** with a transparent `box-shadow`, which adapts to any background. **Never apply this to dividers** (`border-b`, `border-t`, side borders) or any border for layout separation.

Light mode, three layers (1px ring, lift, ambient):

```css
:root {
  --shadow-border:
    0px 0px 0px 1px oklch(0 0 0 / 0.06),
    0px 1px 2px -1px oklch(0 0 0 / 0.06),
    0px 2px 4px 0px oklch(0 0 0 / 0.04);
  --shadow-border-hover:
    0px 0px 0px 1px oklch(0 0 0 / 0.08),
    0px 1px 2px -1px oklch(0 0 0 / 0.08),
    0px 2px 4px 0px oklch(0 0 0 / 0.06);
}
```

Dark mode, one white ring (via the project's dark-mode mechanism):

```css
--shadow-border: 0 0 0 1px oklch(1 0 0 / 0.08);
--shadow-border-hover: 0 0 0 1px oklch(1 0 0 / 0.13);
```

Apply with `box-shadow: var(--shadow-border)` and transition `box-shadow` on hover (timing and curve from the [animate area](../animate/index.md)).

| Use shadows | Use borders |
| --- | --- |
| Cards, containers with depth | Dividers between list items |
| Buttons with bordered styles | Table cell boundaries |
| Elevated elements (dropdowns, modals) | Form input outlines (for accessibility) |
| Elements on varied backgrounds | Hairline separators in dense UI |
| Hover/focus states for lift effect | |

## Image outlines

Light mode `oklch(0 0 0 / 0.1)`, dark mode `oklch(1 0 0 / 0.1)`. Never a palette near-black or near-white (slate-900, zinc-900, `#0a0a0a`, `#111827`, `#f5f5f7`), and never the accent or ink color.

```css
img {
  outline: 1px solid oklch(0 0 0 / 0.1); /* oklch(1 0 0 / 0.1) in dark */
  outline-offset: -1px;
}
```

```tsx
<img className="outline outline-1 -outline-offset-1 outline-black/10 dark:outline-white/10" src={src} alt={alt} />
```

Use `outline-black/10` and `outline-white/10`, never `outline-slate-*`, `outline-zinc-*`, `outline-neutral-*` or any tinted scale. Use `outline`, not `border`, so layout is unaffected; `-1px` offset hugs the corner radius.
