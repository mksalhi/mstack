# Icons

## Match icon stroke to text weight

| Adjacent text | Icon stroke width (24px grid) |
| --- | --- |
| Regular (400), 14–16px | `1.5px` |
| Medium/Semibold (500–600) | `2px` |
| Bold (700), or emphasized standalone | `2.5px` |

```html
<!-- Good: stroke tuned to the label weight -->
<button class="flex items-center gap-2 font-semibold">
  <PlusIcon stroke-width="2" class="size-4" /> New project
</button>

<!-- Bad: default 1.5px stroke against a bold label -->
<button class="flex items-center gap-2 font-bold">
  <PlusIcon stroke-width="1.5" class="size-4" /> New project
</button>
```

- **One optical strategy per surface.** Never mix icon libraries with incompatible stroke conventions on one toolbar. Without stroke variants, keep the set's native stroke and use size or color for emphasis.
- **Size inline icons to the text**, typically `1em`–`1.25em`.

## One SVG, recolored per state

One SVG with `stroke="currentColor"`; CSS state drives color:

```css
.icon-button { color: oklch(0.552 0.016 285.938); }
.icon-button:hover { color: oklch(0.21 0.006 285.885); }
.icon-button[aria-pressed="true"] { color: oklch(0.623 0.188 259.815); }
.icon-button:disabled { opacity: 0.4; }
```

Tailwind: `text-zinc-500 hover:text-zinc-900 aria-pressed:text-blue-600 disabled:opacity-40`. Strip hardcoded fills (`fill="#666"`) to `currentColor` when importing.

## Outline default, fill active

| Variant | Use for |
| --- | --- |
| Outline | Default state: toolbars, list rows, inline with text |
| Fill | Selected/active state: the active tab, a toggled bookmark, a liked heart |

Never use them interchangeably (`variant={isActive ? "solid" : "outline"}`). Swap values: the animate area's [recipes](../animate/RECIPES.md#icon-swap).

## Design at render size

- Test every icon at its smallest render size, often `16px`; it must stay recognizable.
- Prefer simplified glyphs for small contexts.
- Use the set's native grid sizes (`16`, `20`, `24`), not fractional scales.
- Always SVG, never raster.

## Icons in RTL

| Flip | Don't flip |
| --- | --- |
| Back/forward arrows, chevrons in navigation | Logos and brand marks |
| Text-block glyphs (alignment, lists, indent) | Checkmarks |
| Speaker/volume waves (emanate in reading direction) | Physical objects: clocks, cups, pencils |
| "Send" style directional glyphs | Media playback (play/rewind refer to tape direction, convention keeps them LTR) |

```css
[dir="rtl"] .icon-directional { scale: -1 1; }
```

Tailwind: `rtl:-scale-x-100`. Analyze composite icons part by part; a badge or slash overlay may keep its position when the base flips. Accessible names belong to the [accessibility area](../accessibility/index.md).
