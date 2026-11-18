# Feeling native on mobile web

Prefer CSS/meta over JS. Gate on capability (`hover`, `pointer`, `env()`, `dvh`), never on user agent or width. Never disable zoom. Say which fixes you verified on hardware vs only checked in code.

## Symptoms

- Hover sticks after a tap: require hover + fine pointer.
```css
@media (hover: hover) and (pointer: fine) { .button:hover { … } }
```
Tailwind: v4 `hover:` only checks `(hover: hover)`; v3 needs `future.hoverOnlyWhenSupported`.
```css
@custom-variant hover-fine {
  @media (hover: hover) and (pointer: fine) { &:hover { @slot; } }
}
```
- Wrong height: `100vh` overflows under URL bar. Use `100dvh` for app shells/drawers; `100svh` for heroes.
- Page zooms into an input:
  - Apply the 16px rule in [typography](typography/index.md).
  - Use `inputmode` numeric/decimal, `type` email/tel, `enterkeyhint` send/search/done.
  - `autocapitalize="none" autocorrect="off"` on codes/usernames.
- Taps feel laggy: `touch-action: manipulation` on controls. Feedback on `:active` or `pointerdown`, not `click` (see [animate](animate/index.md)).
- Pull-to-refresh fights the app: `overscroll-behavior: none` on root; `contain` on inner scrollers. Never `touchmove` with `preventDefault()`.
- Content stops at the notch: need `viewport-fit=cover`. Pad fixed UI with `env(safe-area-inset-*, 0px)`.
- Long-press selects button text: `user-select: none; -webkit-user-select: none; -webkit-touch-callout: none` on buttons/tabs/chips/drag handles only (never on `body`).
- Carousel scrolls vertically: `touch-action: pan-y` on custom horizontal carousels; `none` only if you handle every axis. Native scroll-snap doesn’t need it.
- Status bar color: one `theme-color` meta per `prefers-color-scheme`; class-based themes update it from JS; in Next.js use `viewport.themeColor`.

## Baseline
```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, interactive-widget=resizes-content" />
```
```css
html { -webkit-tap-highlight-color: transparent; -webkit-text-size-adjust: 100%; overscroll-behavior: none; }
button, a, [role="button"] { touch-action: manipulation; }
```
Drop `overscroll-behavior: none` where pull-to-refresh is welcome.

## Testing on a phone
- Serve on `0.0.0.0`, open LAN IP; inspect via Safari Develop on iOS or `chrome://inspect` on Android. Simulators miss touch feel.
- After fixes, report the symptom, what changed, and what still needs a phone.
