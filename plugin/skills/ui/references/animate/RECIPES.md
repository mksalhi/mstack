# Animation recipes

Values come from [index.md](index.md). A recipe that departs from them names its exemption.

- **Button press.** `transition: transform 160ms var(--ease-out); :active { transform: scale(.97) }`. In Tailwind, `active:not-disabled:scale-[0.97]`, with a `static` prop to turn it off. In Motion, `whileTap={{ scale: .97 }}`.
- **Dropdown, popover, menu.** Use `transform-origin: var(--transform-origin)`, 200ms opacity and transform from `scale(.95)`, using Base UI's `data-starting-style` and `data-ending-style`.
- **Tooltip.** 125ms from `scale(.97)`. Once one tooltip is open, its neighbours open instantly (`[data-instant] { transition-duration: 0ms }`).
- **Modal.** Centered, 250ms from `opacity: 0; scale(.96)`, with the backdrop's opacity on the same 250ms.
- **Drawer.** `translateY(100%)` to `0`, 300ms `var(--ease-drawer)`.
- **Toast.** 400ms `ease` transitions with `@starting-style { opacity: 0; transform: translateY(100%) }`; this is the Sonner exemption. Without `@starting-style`, set a `data-mounted` flag in `useEffect`.
- **Accordion.** Height and opacity over 200ms. Measure the content's height or use a headless primitive; never animate to `auto`.
- **Stagger.**
  - Items: `opacity` plus `translateY(8px)` over 300ms, with 50ms between them.
  - Hero, success and empty states: stagger the title, description and actions at 100ms, using `blur(4px)` to `0`.
  - Exit with `opacity: 0; translateY(-12px)` over 150ms.
  - Skip the stagger for anything seen often.
- **Hold to confirm.** An overlay going from `clip-path: inset(0 100% 0 0)` to `inset(0)` over 2s `linear` while pressed, back over 200ms `ease-out` on release, plus press scale on the button.
- **Tab indicator that changes color.** Duplicate the tab list, style the copy as active, clip it to the active tab, and animate `clip-path` over 250ms `ease-in-out`.
- **Scroll reveal.** Marketing only. `clip-path: inset(0 0 100% 0)` to `inset(0)` over 600ms, fired once through `IntersectionObserver` with `margin: -100px`.
- **Drag to dismiss.**
  - Dismiss when the distance passes the threshold or the speed is above 0.11px/ms.
  - Call `setPointerCapture` when the drag starts, and ignore extra touch points while dragging.
  - Add friction that rises past the boundary, not a hard wall.
  - Set the transform on the element itself, and settle with the default spring.
- **Comparison slider.** Two stacked images; the top one has `clip-path: inset(0 X 0 0)` driven by the drag.
- **Crossfade that won't settle.** Blur the seam: `filter: blur(2px); opacity: .7` during the transition.
- **Icon swap.** Only for icons that change state (play/pause, like). Animate scale .25 to 1, opacity 0 to 1 and blur 4px to 0 together.
  - With Motion: `AnimatePresence mode="popLayout" initial={false}`, a keyed `motion.span`, and the icon-swap spring. Never add a library just for this.
  - Without one: keep both icons mounted, one absolutely positioned over the other, and toggle `transition-[opacity,filter,scale] duration-300 ease-[cubic-bezier(0.2,0,0,1)]`.
- **Skip the first-render animation.** `initial={false}` on `AnimatePresence` suits toggles and tabs, but not first-time entrances. Check after a full refresh.
- **Theme switch.** Inject `*{transition:none!important}`, apply the theme, force a reflow (`document.body.offsetHeight`), and remove the style after two `requestAnimationFrame`s. Run the same on `matchMedia` changes. With `next-themes`, use `disableTransitionOnChange`.
- **Image placeholder.** Put a tiny inline SVG of the image's main shapes behind it, blurred with `feGaussianBlur`. Fade the real image in over 250ms on load, then remove the SVG.
- **Coded explainer.** Build the walkthrough from DOM and SVG instead of a video: it's a few KB and the text is real. Label it `role="img"`, play it on view rather than in a loop, and keep the end state under reduced motion.
- **3D.** Use `transform-style: preserve-3d` with `rotateY` and `translateZ` for card flips and orbits.
- **Decorative pointer tracking.** Pass the value through `useSpring` with the default spring. Never do this on data the user reads.
