# Spacing and sizing

## Units

| Unit | Behavior |
| --- | --- |
| `px` | Fixed |
| `em` | Scales with the current font size |
| `rem` | Scales with the root font size |
| `%` on `font-size` | Relative to the parent's font size, behaves like `em` |

## Type scale

Pick an existing scale or define one; Tailwind's (`text-xs` through `text-9xl`, each pairing size with line height) is a solid default.

```css
:root {
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.5rem;
  --text-2xl: 2rem;
}
```

A role-based scale pairs size, line-height and weight. Starting point for a product interface:

| Role | Size | Line-height | Weight |
| --- | --- | --- | --- |
| Display | `2.25rem` (36px) | `1.1` | `600` |
| Title | `1.5rem` (24px) | `1.2` | `600` |
| Heading | `1.125rem` (18px) | `1.3` | `600` |
| Body | `1rem` (16px) | `1.5` | `400` |
| Caption | `0.8125rem` (13px) | `1.4` | `400` |

Emphasis within a role is one weight step up (`400` → `500`), not a size change.

## Heading hierarchy

```css
h1 { font-size: var(--text-2xl); }
h2 { font-size: var(--text-xl); }
h3 { font-size: var(--text-lg); }
```

In Tailwind, centralize the per-level utilities in a component or `@layer base`, not inline.

When reviewing, compare computed heading sizes within each semantic section; a child more prominent than its parent breaks hierarchy. A heading is never smaller than body text unless it is a deliberate label-style overline. Pick the element from document structure, never for its browser-default size.

## Kerning and letter-spacing

Kerning is automatic; disable with `font-kerning: none` only deliberately.

```css
.display-heading { letter-spacing: -0.02em; }
.uppercase-label { text-transform: uppercase; letter-spacing: 0.05em; }
```

## Line-height

| Text | Value |
| --- | --- |
| Headings | ~`1.1` |
| Body copy | `1.5`–`1.6` |

Tailwind `leading-snug`, `leading-normal` and `leading-relaxed` rarely need overriding. Prefer a taller row over a tightly leaded paragraph (a 3-line card description gets `1.4`, not `1.1`).

## Text trimming with text-box

`text-box` trims the font's reserved space above and below letters (text sitting low in buttons and badges). Edges: `trim-both`, `trim-start`, `trim-end`.

| Keyword | Trims at |
| --- | --- |
| `cap` | The cap height (top) |
| `alphabetic` | The baseline (bottom) |
| `text` | The font's own text edge, keeping room for descenders |

```css
.badge { text-box: trim-both cap alphabetic; }
.heading { text-box: trim-start cap; }
.label { text-box: trim-end alphabetic; }
```

Chromium 133+ and Safari 18.2+, not Firefox: progressive enhancement only.
