# Palette structure

Values: [palette-generation.md](palette-generation.md). Names: [token-naming.md](token-naming.md).

## What a system needs

| Ramp | How many | Notes |
| --- | --- | --- |
| Neutral | 1 | Carries 80–90% of the interface: backgrounds, borders, body text |
| Accent | 1 | The brand hue. Interactive and selected states |
| Status | 0–4 | `danger`, `warning`, `success`, `info`. Add one only when the product shows that state |

A second accent hue never sits adjacent to the first; there, use the accent ramp's own steps.

## Every step has a job

Generate the steps these roles call for and skip the rest.

| Role | Tailwind | Radix |
| --- | --- | --- |
| Page background | `50` | `1` |
| Subtle background | `50` | `2` |
| Component background | `100` | `3` |
| Component hover | `200` | `4` |
| Component active / selected | `200` | `5` |
| Subtle border | `200` | `6` |
| Border, separator | `300` | `7` |
| Strong border, focus ring | `400` | `8` |
| Solid fill | `500` | `9` |
| Solid fill hover | `600` | `10` |
| Low-contrast text | `700` | `11` |
| High-contrast text | `900` | `12` |

- **Radix steps are roles.** Step 9 is the solid fill in every ramp and appearance; the dark scale reuses the numbers, so component CSS never changes.
- **Tailwind steps are lightness.** The mapping holds in light mode and inverts in dark (page background `950`, high-contrast text `50`). Components swap step numbers per appearance or read a semantic token.

Match the project's convention. For a new system prefer Radix's model; on Tailwind, keep `50`–`950` and put the role mapping in the semantic tier. Where the table repeats a Tailwind step, the collision is real: a design needing subtle border and component hover distinguishable needs a 12-step ramp.

## Neutrals

Pure gray is a good default. Tinting toward the accent (a few percent of its vividness, enough to measure, not to name) is a stylistic option, not a correction. Warm neutrals read approachable and editorial, cool ones technical. Whatever you pick, including none, hold it across the whole ramp. Never generate fewer neutral steps than accent steps.

## Status colors

Red reads as danger, amber warning, green success; cultural exceptions in [color-usage.md](color-usage.md).

- **Keep every status hue distinct from the accent.** A red brand moves danger toward deeper crimson; check the two side by side.
- **Status ramps need fewer steps.** Most render four roles: background, border, solid fill, text. Generate a full ramp only where status components span the range.

Pair status color with an icon or text (the accessibility area owns this).

## Auditing an existing palette

1. **Collect every literal.** Grep for hex, `rgb(`, `hsl(`, `oklch(` and the project's utility-class prefixes, including SVG `fill`/`stroke`, chart configs and email templates.
2. **Sort by perceived lightness within each hue family.**
3. **Collapse near-duplicates.** Colors closer than about one ramp step are one color: keep the most-used, retire the others, never average.
4. **Assign each survivor a role** from the table. A color matching no role is a missing token or a mistake; say which in the finding.
5. **Count what is left.** More than one ramp per role means the palette outgrew its structure.

Report the inventory before changing anything; consolidation stays a proposal until the user accepts it.
