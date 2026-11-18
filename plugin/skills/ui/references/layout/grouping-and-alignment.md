# Grouping and alignment

## Group with space, not lines

In order of preference:

1. **Negative space**, the default.
2. **Background shapes** (card, filled container) where a group must read as one unit, such as a selectable row or draggable card.
3. **Separator lines**, last resort for dense data (tables, long settings lists). Keep them hairline and low contrast, never added to a gap that already did the job.

Gap between groups ≥ 2× gap within one: `8px` inside needs `16px`+ between.

```css
/* Good: spacing alone communicates the grouping */
.field-group { display: flex; flex-direction: column; gap: 8px; }
.form { display: flex; flex-direction: column; gap: 24px; }

/* Bad: uniform spacing plus lines to compensate */
.form > * { margin-bottom: 12px; border-bottom: 1px solid var(--separator); }
```

## Keep controls distinct from content

Interactive elements need a background, border, underline, or a consistent control zone (toolbar, footer row). Conversely, a non-clickable badge must not be shaped like the buttons beside it.

## Align to shared edges

- Use a small set of alignment edges; an icon 2px off the text edge or a card padded unlike its neighbor is a finding.
- One project spacing step expresses each hierarchy level (`16px` default); deeper nesting repeats it.
- Table numbers align to the trailing edge, text to the leading edge. Tabular figures belong to the typography area.

## Logical properties, not physical

| Physical (avoid) | Logical (use) |
| --- | --- |
| `margin-left` | `margin-inline-start` |
| `padding-right` | `padding-inline-end` |
| `left: 0` | `inset-inline-start: 0` |
| `text-align: left` | `text-align: start` |
| `border-right` | `border-inline-end` |

Tailwind: `ms-4 pe-6 text-start`, not `ml-4 pr-6 text-left`.

Physical properties only for physical screen sides (device notch, gesture direction). Progressions (star ratings, step indicators, progress bars) mirror in RTL; stars fill from the trailing side. Hand-positioned elements don't mirror automatically. Digit order and other bidi rules belong to the typography area.

## Order by importance

- The most important information sits near the top and leading edge; never bury the number the user came for under secondary detail. Push detail into collapsed sections, tabs or detail views.
- Within a row, identifying content leads; metadata and actions trail.

## Don't overload the entry point

- One primary action per view (the colors area owns how color enforces it).
- Group secondary actions behind a menu once they exceed two or three.
- Prefer a short view that links deeper over one that shows everything at level one.
