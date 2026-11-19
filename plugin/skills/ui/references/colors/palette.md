# Building or auditing a palette

- Use a color library (`culori`, `colorjs.io`, `chroma.js`). Write output in the project’s notation. For new systems, use `oklch()`.

## Ramps
- One neutral ramp carries 80–90% of the UI. One accent ramp (brand) for interactive/selected states. Add status ramps only for visible states. A second accent hue never sits next to the first.
- Interpolate in Lab/OKLCH, never sRGB. Even perceived-lightness steps; constant hue; chroma peaks mid-ramp and ends nearly neutral; denser at the light end; stop short of pure black/white.
- Brand: place on solid-fill step (Tailwind 500, Radix 9). Pin only if contractually fixed; otherwise snap it to the ramp. If white text fails, use a darker fill step; never darken the brand itself.
- Cross-hue: match perceived lightness exactly; match chroma as the same proportion of each hue’s maximum.
- Status hues: keep clearly apart from the accent; provide background, border, fill, text.
- Dark mode: reverse semantic mapping, lower accent chroma by one step, widen separation at the dark end, recheck pairs.

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

Radix steps name roles and stay the same in dark mode. Tailwind steps name lightness and invert in dark mode; mapping lives in the semantic tier. If hover and subtle border must differ, use Radix’s 12 steps.

## Tokens
- Two tiers: primitives (values, e.g. `--blue-500`) and semantics (roles, e.g. `--color-text-secondary`). Themes repoint only semantics. Add a component tier only for deliberate divergence.
- Shape: `--color-{role}-{variant}-{state}`. `primary` means “most prominent”, not the brand.
- Roles: Surfaces (page, surface, raised, sunken, scrim). Text (primary, secondary, disabled, inverse, on-accent). Borders (subtle, default, strong, focus, separator). Accent and each status: subtle background, border, solid, text.
- Tailwind v4: declare both tiers in `@theme`. Avoid opacity utilities (`bg-accent/50`) under text; use solid tokens.

## Auditing
1. Grep every color literal and utility, plus SVG/chart/email uses.
2. Within each hue, sort by perceived lightness. Merge colors less than a step apart; keep the most-used, never average.
3. Assign each survivor a role from the table. No-role = missing token or mistake.
