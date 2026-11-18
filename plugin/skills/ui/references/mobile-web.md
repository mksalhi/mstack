# Feeling native on mobile

Remove the platform-layer tells (viewport, touch, scroll, safe areas, browser chrome) that make a web app feel like a website on a phone. Motion design is the [animate area](animate/index.md), motion review the [review area](review/index.md), React Native the [animate-expo area](animate-expo/index.md).

## Hard rules

- None of these bugs reproduce in desktop device emulation. Test on hardware before calling it done; if you can't, say which fixes are verified from code and which need a real device.
- CSS or a meta tag over JavaScript (no `useIsTouchDevice()` hook to hide hover).
- Apply each fix where its reason applies, not globally (`user-select: none` on a button is right, on body text a defect).
- Gate by capability (`(hover: hover)`, `(pointer: fine)`, `env()`, `dvh`), never by user agent or screen width. Touch and mouse coexist (iPad with trackpad, touchscreen laptop).
- Never disable zoom (`user-scalable=no`, `maximum-scale=1`). Fix the input font size.

Match the user's symptom to a section below.

## The fixes

### 1. Hover state stuck after tap

The canonical hover gate for every area of the `ui` skill:

```css
@media (hover: hover) and (pointer: fine) {
  .button:hover { background: var(--gray-3); transform: scale(1.02); }
}
```

Both conditions are needed (`pointer: fine` rules out styluses and Android devices that claim hover). Tailwind caveat: v4 `hover:` compiles to `(hover: hover)` alone, and v3 needs `future.hoverOnlyWhenSupported` to gate at all. Where hover drives motion or reveals controls, use this variant instead of `hover:`:

```css
@custom-variant hover-fine {
  @media (hover: hover) and (pointer: fine) { &:hover { @slot; } }
}
```

Touch users get press feedback through `:active` (§5).

### 2. Gray/blue flash on tap

```css
html { -webkit-tap-highlight-color: transparent; }
```

Set once, globally, then give every tappable element its own `:active` state.

### 3. Layout has the wrong height

`100vh` on mobile is the largest viewport, so it overflows under the URL bar.

```css
.app { height: 100dvh; }      /* app shell, drawers: tracks chrome show/hide */
.hero { min-height: 100svh; } /* heroes, first screens: stable, never cut off */
```

`dvh` shifts layout mid-scroll on marketing content; use `svh` there. Avoid `lvh`. Add a `100vh` fallback line only if the support matrix demands it.

### 4. Page zooms into the input

iOS zooms on focus when input text is under 16px. Apply the rule from the [typography area](typography/index.md#inputs-at-16px-on-mobile) (**Inputs at 16px on mobile**). Also set the keyboard: `inputmode="numeric"` for codes, `inputmode="decimal"` for amounts, `type="email"` / `type="tel"`, `autocapitalize="none"` and `autocorrect="off"` on usernames and codes, `enterkeyhint="send"` / `"search"` / `"done"`.

### 5. Tap feels laggy

Kill the double-tap-zoom delay:

```css
button, a, [role="button"], .tappable { touch-action: manipulation; }
```

Give feedback on press, not release: style `:active`, and in JS listen to `pointerdown`, not `click`.

```css
.button { transition: transform 100ms var(--ease-out), background 100ms; }
.button:active { transform: scale(0.97); background: var(--gray-4); }
```

Press values come from the animate area (**Easing and duration**); use existing tokens.

### 6. Pull-to-refresh hijacks scroll

For apps with their own scroll containers, draggable drawers or canvases:

```css
html, body { overscroll-behavior: none; }
.sheet-content { overflow-y: auto; overscroll-behavior: contain; } /* inner scrollables */
```

`none` on the root, `contain` on children. Never `touchmove` + `preventDefault()`.

### 7. Content stops at the notch

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
```

```css
.app-header { padding-top: env(safe-area-inset-top); }
.bottom-bar { padding-bottom: env(safe-area-inset-bottom); }
.sheet { padding-bottom: calc(1rem + env(safe-area-inset-bottom)); }
```

Without `viewport-fit=cover`, `env()` is `0px`. Pad fixed headers, bottom tab bars, toasts and sheets. Use a fallback inside `calc` (`env(safe-area-inset-bottom, 0px)`).

### 8. Long-press selects button text

```css
button, [role="button"], .tab, .chip, .drag-handle {
  user-select: none;
  -webkit-user-select: none;   /* Safari needs the prefix */
  -webkit-touch-callout: none; /* links/images used as controls */
}
```

Never on `body`; content text must stay selectable.

### 9. Carousel scrolls vertically

`touch-action` names what the browser may still do:

```css
.carousel { touch-action: pan-y; }              /* you handle horizontal */
.drag-surface { touch-action: none; }           /* custom gesture owns every axis */
.vertical-sheet-handle { touch-action: pan-x; } /* you handle vertical */
```

`none` only on elements that truly handle everything. For native-scroll carousels prefer `scroll-snap-type: x mandatory` on the track and `scroll-snap-align: start` on slides; then `touch-action` is unnecessary.

### 10. Status bar color doesn't match

```html
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#ffffff" />
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0a0a0a" />
<meta name="color-scheme" content="light dark" />
```

Match the color at the top of the page (header background, not brand color). Next.js: `viewport` export `themeColor: [{ media, color }]`. Class-based theme toggles update the tag from JS. Installed PWAs: `apple-mobile-web-app-status-bar-style` and manifest `theme_color`/`background_color` follow the same choice.

### 11. Right in Chrome, wrong on phone

- Run the dev server on `0.0.0.0`, open it by LAN IP on a USB-connected phone.
- iOS: Safari → Develop → the device. Android: `chrome://inspect`.
- Test on a few-years-old phone, with the keyboard open, in landscape once, and as an installed PWA if that's a target.
- The Xcode Simulator misses touch feel.

## Baseline

Ship before the first component of a mobile-facing app:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, interactive-widget=resizes-content" />
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#ffffff" />
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0a0a0a" />
```

```css
html {
  -webkit-tap-highlight-color: transparent;
  -webkit-text-size-adjust: 100%; /* no landscape font inflation */
  overscroll-behavior: none;
}
/* inputs: the 16px rule from the typography area */
button, a, [role="button"] { touch-action: manipulation; }
button, a[role="button"], [role="button"], [role="tab"], .chip, .drag-handle {
  user-select: none;
  -webkit-user-select: none;
}
@media (hover: hover) and (pointer: fine) { /* all :hover rules */ }
```

`interactive-widget=resizes-content` makes the Android keyboard shrink the layout viewport like iOS. Drop `overscroll-behavior: none` for scrolling documents where pull-to-refresh is welcome.

## Never ship

| Never | Instead |
| --- | --- |
| `user-scalable=no` or `maximum-scale=1` | 16px input text (typography area) |
| Ungated `:hover` | `@media (hover: hover) and (pointer: fine)` |
| `100vh` for an app shell or bottom-pinned UI | `100dvh` |
| `100dvh` on a marketing hero | `100svh` |
| Press feedback on `click` only | `:active` / `pointerdown` |
| `touchmove` + `preventDefault()` to stop overscroll | `overscroll-behavior` |
| `user-select: none` on `body` | Only buttons, tabs, chips, drag handles |
| `touch-action: none` on something the user scrolls past | `pan-x` / `pan-y` |
| `env(safe-area-inset-*)` without `viewport-fit=cover` | Add the meta tag |
| One `theme-color` for both schemes | One per `prefers-color-scheme` |
| User-agent sniffing to detect touch | `(hover)` / `(pointer)` media queries |
| Declaring it fixed from device emulation | Real hardware |

## Output

Apply the fixes, then at most a few lines:

- **What was wrong**: matched symptom and one-line why.
- **What changed**: file and declaration, one line each.
- **What needs a phone**: verified from code vs. must confirm on hardware.

No report. When you can't verify without a device, say so instead of claiming it's fixed.
