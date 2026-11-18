# Color formats

Every other rule in this area is perceptual and holds in any notation.

## Choosing a notation

| Notation | Good for | Weakness |
| --- | --- | --- |
| Hex | Universal support, compact, what design tools hand you | Opaque. No channel is readable or editable by hand |
| `rgb()` | Same reach as hex, readable alpha | Channels do not correspond to anything a designer thinks about |
| `hsl()` | Channels look like design controls | Its lightness is not perceptual and its hue drifts; a ramp built by varying lightness bunches at one end and shifts hue |
| `oklch()` | Perceptually uniform lightness, stable hue, predictable ramps | Baseline 2023, so very old browser matrices need a fallback |

**Match the project's notation**; it is not a defect. **For a new color system, default to `oklch()`** ([palette-generation.md](palette-generation.md)).

```css
oklch(L C H)          /* lightness 0–1, chroma 0–~0.4, hue 0–360 */
oklch(L C H / alpha)  /* alpha uses a slash, never a comma */
```

## Converting

Convert only when the user asks, an agreed migration is in scope, or the project is standardizing and this value is the straggler. Never convert an isolated value in a project that deliberately uses another notation. Bulk conversion is a migration and must be the task, not a side effect.

When converting, change values only:

- Leave keywords: `currentColor`, `inherit`, `transparent`, `initial`, `unset`.
- In gradients, convert the stops, not the interpolation method.
- Leave colors in third-party configs that expect a specific format.
- Preserve comments and formatting.

```css
color: #3b82f6;                         /* before */
border: 1px solid rgba(0, 0, 0, 0.1);
color: oklch(0.623 0.188 259.815);      /* after */
border: 1px solid oklch(0 0 0 / 0.1);
```

## Gamut

P3 covers roughly 50% more colors than sRGB, only at high vividness. Out-of-gamut colors clip, flattening neighbouring steps into one; maximum vividness varies by hue and lightness (cyans top out far below reds and purples). Fix by reducing vividness while holding hue and lightness. Generate ramps against sRGB unless the product is display-restricted, and add P3 as an enhancement, sRGB first:

```css
.accent { background: #3b82f6; }
@media (color-gamut: p3) {
  .accent { background: oklch(0.62 0.24 259); }
}
```

A P3 color with no fallback is a `HIGH` finding.

For browser matrices predating `oklch()`, layer with `@supports (color: oklch(0 0 0))` the same way. Check the project's browser matrix first; on a modern baseline it is dead weight.

## Modern CSS worth knowing

- **`color-mix()`**: `color-mix(in oklab, var(--color-accent-solid) 15%, white)` for a tinted state. Keep generated values out of the token layer.
- **Relative color syntax**: `oklch(from var(--color-accent-solid) calc(l - 0.1) c h)`. Never chain derivations into a token.
- **`light-dark()`**: see [palette-generation.md](palette-generation.md).

All three compute at render time; measure the rendered result for contrast.
