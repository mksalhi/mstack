# Hit areas

## Target sizes

| Standard | Minimum |
| --- | --- |
| WCAG 2.5.8 (AA) | 24×24px, the hard floor |
| WCAG 2.5.5 (AAA) | 44×44px |
| Apple HIG | 44×44pt |
| Material Design | 48×48dp |

Recommend 44px for primary touch controls and 40px on desktop where density permits. Below 24px is not an automatic failure: check the spacing, equivalent-control, inline, user-agent and essential exceptions first. Spacing exception: an undersized target passes when a 24px circle centered on its bounding box intersects no other target and no other undersized target's circle (20px targets need a 4px gap).

Anything that looks clickable is clickable across its whole visual extent, with no dead zones.

## Expanding the hit area

Extend a small visible element with a pseudo-element on the wrapping `<label>` or `<button>`, never on the `<input>` (replaced elements don't render `::before`/`::after` reliably):

```css
.checkbox-label { position: relative; width: 20px; height: 20px; }
.checkbox-label::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%; /* physical centering: direction-independent */
  transform: translate(-50%, -50%);
  width: 44px;
  height: 44px;
}
```

```tsx
<button className="relative size-5 after:absolute after:top-1/2 after:left-1/2 after:size-11 after:-translate-1/2">
  <CheckIcon />
</button>
```

Where the element can afford real box size, prefer `min-width: 44px; min-height: 44px; display: inline-grid; place-items: center;` over a pseudo-element.

## Collision rule

Two interactive elements never have overlapping hit areas; shrink the pseudo-element to the largest size that does not collide.

## Decorative layers

A scrim, glow, sheen or full-bleed `::after` over interactive content swallows its clicks. Give each `pointer-events: none` (Tailwind `pointer-events-none`) and `aria-hidden="true"`. Keep pointer events on layers meant to be hit, such as a click-to-dismiss modal scrim.

## Touch behavior

- `touch-action: manipulation` on interactive elements removes the double-tap-zoom delay.
- `touch-action: none` only on a surface with its own pan, zoom or drag gestures, never page-wide.
- Set `-webkit-tap-highlight-color` to match the design.
- Put hover-only styling behind the mobile-web area's hover query ([mobile-web.md](../mobile-web.md#1-hover-state-stuck-after-tap)), `(hover: hover) and (pointer: fine)`, including its Tailwind caveat; on touch `:hover` latches after a tap.
- Prefer generous targets over tiny drag handles and precise hover zones.
