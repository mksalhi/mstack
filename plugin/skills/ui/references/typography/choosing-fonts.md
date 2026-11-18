# Choosing fonts

## Choosing a typeface

| Category | Traits | Use for |
| --- | --- | --- |
| Serif | Small strokes at the ends of letters guide the eye along a line | Long passages, editorial reading |
| Sans-serif | Clean, even shapes that stay crisp at small sizes | Default for most interfaces (Helvetica, Inter, Geist) |
| Monospace | Every glyph the same width so columns line up | Code, tables, tabular data |
| Display | Drawn for large headlines | Marketing headlines, hero text |
| Script | Mimics handwriting | Rare, decorative moments |

CSS keywords `cursive` and `fantasy` cover the last two. Where a family ships `Display` and `Text` variants (SF Pro, Heldane), use the one matching the set size.

### Rules

- Rarely more than three fonts; marketing pages may be more expressive than apps. Same restraint for sizes and weights.
- Pair for contrast, not similarity: serif headline over sans body, never two near-identical sans-serifs.
- Below `18px` stay at weight `400`+. Weights `100`–`300` only for `28px`+ display text, checked against the background.

## Font family scope

Applying or reviewing typography never requires a new typeface. Use the product's type system unless the task asks for a type change; never introduce a paid or proprietary face to satisfy a checklist. Rendering details do not override the project's family.

When a change is asked for: the system stack for a native macOS/iOS feel, or a commercial brand face with a fallback stack.

```css
html { font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
html { font-family: "Helvetica Now", "Helvetica Neue", Arial, sans-serif; }
```

## Formats

| Format | Notes |
| --- | --- |
| `.woff2` | Brotli compression, broadly supported. Use this on the web. |
| `.woff` | Fallback only for very old browsers. |
| `.ttf` / `.otf` | No web compression. Never on the web; desktop apps only. |

## Anatomy of a typeface

| Term | Meaning |
| --- | --- |
| x-height | Height of a lowercase `x` |
| Cap height | Height of uppercase letters |
| Baseline | The invisible line letters sit on |
| Ascender | Part of a letter rising above the x-height |
| Descender | Part dropping below the baseline |

A larger x-height makes a font look bigger at the same `font-size`.
