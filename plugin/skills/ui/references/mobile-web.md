# Feeling native on mobile web

Fix the platform tells that make a web app feel like a website on a phone. None of these bugs show up in desktop device emulation, so say which fixes you verified on hardware and which you only checked in code. Prefer CSS or a meta tag over JS. Gate on capability (`hover`, `pointer`, `env()`, `dvh`), never on user agent or width. Never disable zoom.

## Symptoms

### Hover sticks after a tap

This is the hover gate for the whole `ui` skill:

```css
@media (hover: hover) and (pointer: fine) { .button:hover { … } }
```

You need both conditions. Tailwind v4's `hover:` only checks `(hover: hover)`, and v3 needs `future.hoverOnlyWhenSupported`. Where hover drives motion or reveals controls, define `@custom-variant hover-fine { @media (hover: hover) and (pointer: fine) { &:hover { @slot; } } }`.

### Other symptoms

- **Gray flash on tap.** Set `html { -webkit-tap-highlight-color: transparent }`, then give every tappable element its own `:active` style.
- **Wrong height.** `100vh` is the largest viewport, so it overflows under the URL bar. Use `100dvh` for app shells and drawers and `100svh` for heroes, since `dvh` shifts layout mid-scroll.
- **The page zooms into an input.**
  - Apply the 16px rule in [typography](typography/index.md).
  - Set the keyboard type: `inputmode` numeric or decimal, `type` email or tel, and `enterkeyhint` send, search or done.
  - Put `autocapitalize="none" autocorrect="off"` on codes and usernames.
- **Taps feel laggy.** Add `touch-action: manipulation` on controls. Give feedback on `:active` or `pointerdown`, not `click`, using the press values from [animate](animate/index.md).
- **Pull-to-refresh fights the app.** Use `overscroll-behavior: none` on the root and `contain` on inner scrollers. Never `touchmove` with `preventDefault()`.
- **Content stops at the notch.** Without `viewport-fit=cover` in the viewport meta, `env()` is 0. Pad fixed headers, tab bars, toasts and sheets with `env(safe-area-inset-*, 0px)`.
- **Long-press selects button text.** Add `user-select: none; -webkit-user-select: none; -webkit-touch-callout: none` on buttons, tabs, chips and drag handles only, never on `body`.
- **A carousel scrolls vertically.** `touch-action: pan-y` on a horizontal carousel you drive yourself, and `none` only on a surface that handles every axis. A native-scroll carousel with `scroll-snap-type: x mandatory` doesn't need it.
- **The status bar color is wrong.**
  - Add one `theme-color` meta per `prefers-color-scheme`, matching the header color rather than the brand color.
  - Class-based themes update the tag from JS.
  - In Next.js, use the `viewport.themeColor` array.

## Baseline for a mobile-facing app

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, interactive-widget=resizes-content" />
```

```css
html { -webkit-tap-highlight-color: transparent; -webkit-text-size-adjust: 100%; overscroll-behavior: none; }
button, a, [role="button"] { touch-action: manipulation; }
```

`interactive-widget=resizes-content` makes the Android keyboard resize the layout the way iOS does. Drop `overscroll-behavior: none` on documents where pull-to-refresh is welcome.

## Testing on a phone

- Serve on `0.0.0.0` and open the LAN IP on the phone. Inspect through Safari's Develop menu on iOS or `chrome://inspect` on Android.
- Test on an old phone, with the keyboard open, once in landscape, and as an installed PWA if that's a target. The Simulator misses touch feel.

After applying fixes, report the symptom, what changed, and what still needs a phone.
