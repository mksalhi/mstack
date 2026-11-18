# Variable fonts and OpenType

## Static vs variable

- **Static:** one weight and style per file.
- **Variable:** a whole range in one file (`font-weight: 589` works).

At one or two weights, static files can be smaller; at several weights, optical sizes or custom axes, variable usually wins.

## Load intended weights and styles

Load the faces the design uses. `font-synthesis: none` disables weight, style, small-cap, superscript and subscript synthesis together; set it only on an isolated, verified treatment (e.g. `.brand-wordmark`) after checking the fallback stack and every emphasis state. For body and interface text keep synthesis on unless the font setup supplies every form. To drop one mode, use the longhand (`font-synthesis-weight`, `font-synthesis-style`, etc.).

## Axes

A font supports only the axes its designer included.

| Axis | Tag | Controls |
| --- | --- | --- |
| Weight | `wght` | Stroke thickness (like `font-weight`) |
| Optical size | `opsz` | Details and spacing tuned for the display size |
| Width | `wdth` | Glyph width |
| Slant | `slnt` | Slant angle |
| Custom | e.g. `GRAD` (Roboto Flex) | Whatever the designer built |

Inter's variable file exposes only `wght` and `opsz`. Many families ship optical sizes as separate files (Heldane Text for reading sizes, Heldane Display for large).

## Properties over axis tags

`font-variation-settings` silently does nothing on a non-variable fallback; use properties for common axes.

```css
/* Good */
.heading { font-weight: 650; font-optical-sizing: auto; }
.heading-grade { font-variation-settings: "GRAD" 80; } /* custom axis, no property */

/* Bad: breaks on fallback fonts */
.heading { font-variation-settings: "wght" 650; }
```

## OpenType features

Work the same on static and variable fonts; a font ships only the features its designer included.

| Tag | Feature |
| --- | --- |
| `tnum` | Tabular numbers: every digit the same width |
| `zero` | Slashed zero: `0` distinct from `O` |
| `liga` | Ligatures: joins pairs like "fi" into one shape |
| `ss01`–`ss20` | Stylistic sets (numbered slots) |
| `cv01`–`cv99` | Character variants (numbered slots) |

Prefer `font-variant-*` properties; `font-feature-settings` only for tags with no property:

```css
.price { font-variant-numeric: tabular-nums; }
.id { font-variant-numeric: slashed-zero; }
.logo { font-feature-settings: "ss01" 1; }
```

## Small caps, superscripts, subscripts

Real small capitals via `font-variant-caps`; real superscripts (x²) and subscripts (H₂O) via `font-variant-position`. Both require the glyphs in the font.

## Stylistic sets and character variants

Slot meanings differ per font; check its docs. In Inter, `ss01` gives open digits and `cv11` a single-story `a`.
