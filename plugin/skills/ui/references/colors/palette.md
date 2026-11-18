# Building or auditing a palette

Do the math with a color library (`culori`, `colorjs.io`, `chroma.js`), never by eye. Write the output in the project's notation. For a new system, use `oklch()`.

## Ramps

- One neutral ramp carries 80 to 90% of the UI.
- One accent ramp (the brand) covers interactive and selected states.
- Add status ramps (`danger`, `warning`, `success`, `info`) only for states the product actually shows.
- A second accent hue never sits next to the first.

A correct ramp:

- Steps evenly in **perceived** lightness, which HSL lightness is not. Interpolate in Lab or OKLCH, never sRGB.
- Holds the hue constant from end to end.
- Peaks in chroma mid-ramp; the ends are nearly neutral.
- Spaces steps more densely at the light end, so `50` and `100` read as two different surfaces.
- Stops short of pure black and pure white.

```js
import { formatHex, interpolate, samples } from 'culori'
const ramp = interpolate(['#eff6ff', '#3b82f6', '#172554'], 'lab')
const steps = samples(11).map((t) => formatHex(ramp(t)))
```

- **Brand color.** It goes on the solid-fill step (Tailwind `500`, Radix `9`). Pin it only if the exact value is contractually fixed; otherwise snap it onto the ramp. If white text on it fails contrast, use a darker step for fills. Never quietly darken the brand itself.
- **Matching across hues.** Match perceived lightness exactly. Match chroma as the same **proportion** of each hue's own maximum, not as a copied number; yellows and cyans peak far lower than reds and blues.
- **Status hues.** Keep them clearly apart from the accent: a red brand pushes danger toward crimson. Most status ramps need only four roles: background, border, fill, text.
- **Dark mode.** Reverse the semantic mapping as a starting point. Then lower the accent's chroma by a step, widen the separation at the dark end, and recheck every pair.

## Step roles

| Role | Tailwind | Radix |
|---|---|---|
| Page background | 50 | 1 |
| Component background | 100 | 3 |
| Hover, selected | 200 | 4–5 |
| Subtle border | 200 | 6 |
| Border, separator | 300 | 7 |
| Strong border, focus ring | 400 | 8 |
| Solid fill | 500 | 9 |
| Fill hover | 600 | 10 |
| Low-contrast text | 700 | 11 |
| High-contrast text | 900 | 12 |

Radix steps name roles and stay the same in dark mode. Tailwind steps name lightness and invert in dark mode, so the mapping lives in the semantic tier. If a design needs hover and subtle border to look different, it needs Radix's 12 steps.

## Tokens

- **Two tiers.**
  - Primitives name a value and never change meaning: `--blue-500`.
  - Semantics name a role and point at a primitive: `--color-text-secondary`. Only semantics are used in components.
  - Themes repoint only the semantic tier.
  - Add a component tier only for a deliberate divergence. Many component tokens means the semantic tier is missing roles.
- **Shape:** `--color-{role}-{variant}-{state}`, with one word per concept: `text`, `bg`, `border`, `accent`. `primary` means "most prominent in its group", not the brand.
- **Roles a complete system has:**
  - Surfaces: page, surface, raised, sunken, scrim.
  - Text: primary, secondary, disabled, inverse, on-accent.
  - Borders: subtle, default, strong, focus, separator.
  - Accent and each status: subtle background, border, solid, text.
- **Bad names:**
  - `--color-blue-button`: names the appearance.
  - `--color-sidebar-gray`: names its first use.
  - `--color-light-gray`: false in dark mode.
  - `--color-text-2`: numbered semantics.
- **Tailwind v4:** declare both tiers in `@theme`. Opacity modifiers like `bg-accent/50` can't be contrast-checked, so use solid tokens under text.

## Auditing an existing palette

1. Grep every color literal: hex, `rgb(`, `hsl(`, `oklch(`, and utility classes, plus SVG `fill` and `stroke`, chart configs and email templates.
2. Within each hue, sort by perceived lightness. Merge colors less than a step apart: keep the most-used one, never average them.
3. Give each survivor a role from the table. A color with no role is either a missing token or a mistake.
4. Report the inventory before changing anything. A consolidation stays a proposal until the user accepts it.
