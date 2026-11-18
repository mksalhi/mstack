# Palette generation

Which ramps and steps: [palette-structure.md](palette-structure.md).

## Start from the brand color

**Which step?** A brand color for buttons and links goes on the solid-fill step: `500` in Tailwind, `9` in Radix.

**Pinned or snapped?** Pin a contractually fixed brand color (exact, ramp builds outward, that step spaces slightly unevenly). Otherwise snap it onto the ramp so every step spaces evenly.

A brand color failing contrast behind white text stays the brand color but moves off the solid-fill step; use a darker step for interactive fills. Never quietly darken the brand.

## What a correct ramp looks like

- **Even steps in perceived lightness**, not HSL lightness.
- **Constant hue** end to end.
- **Vividness peaks mid-ramp**; the lightest and darkest steps are nearly neutral.
- **Denser at the light end**: `50` to `200` close, `800` to `950` further apart, so `50` and `100` read as two surfaces.
- **No indistinguishable adjacent steps**; if two look identical on a calibrated screen, drop one.
- **Both ends stop short of pure black and white.**

## Use a color library

Never compute by hand or eye. Use `culori`, `colorjs.io` or `chroma.js`: read the brand color in any format, do the math in a perceptual space, emit the project's notation.

```js
import { formatHex, interpolate, samples } from 'culori'

const ramp = interpolate(['#eff6ff', '#3b82f6', '#172554'], 'lab')
const steps = samples(11).map((t) => formatHex(ramp(t)))
```

The output format is the project's choice; the interpolation space for a ramp is not (sRGB gives muddy mid-steps). Decorative gradients are different ([color-usage.md](color-usage.md)).

## Several hues at once

The same step must read equally bright and vivid across hues (`danger-500` vs `brand-500`).

- **Match perceived lightness exactly.**
- **Match vividness relatively**: the same *proportion* of each hue's own maximum, never a copied saturation number. Yellows and cyans peak much lower than reds and blues.

## Dark mode

Reversal is the starting point, not the output. Swap the semantic roles first:

```css
:root { --color-bg: var(--brand-50); --color-text: var(--brand-950); }
.dark { --color-bg: var(--brand-950); --color-text: var(--brand-50); }
```

Then hand-tune:

- **Lower vividness**: the accent a step or two less vivid.
- **More separation at the dark end.**
- **Recheck contrast** for every foreground against its real background in both appearances ([contrast.md](contrast.md)).

### Choosing the switching mechanism

Pick one and use it throughout:

- **`prefers-color-scheme` alone** when there is no theme toggle.
- **A `.dark` class** once users can override the system setting; the media query sets only the initial value.
- **`light-dark()`** for least code when the project sets `color-scheme`; a class-based toggle must set `color-scheme` too.

```css
:root {
  color-scheme: light dark;
  --color-bg: light-dark(#ffffff, #172554);
}
```
