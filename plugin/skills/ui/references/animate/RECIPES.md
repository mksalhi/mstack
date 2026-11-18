# Animation recipes

Values come from [index.md](index.md). A recipe that departs from them names its exemption.

- Dropdown, popover, menu. Use `transform-origin: var(--transform-origin)`, 200ms opacity+transform from `scale(.95)`, using Base UI’s `data-starting-style` and `data-ending-style`.
- Tooltip. 125ms from `scale(.97)`. Once one tooltip is open, neighbours open instantly: `[data-instant] { transition-duration: 0ms }`.
- Toast. 400ms `ease` with `@starting-style { opacity: 0; transform: translateY(100%) }` (Sonner exemption). Without `@starting-style`, set a `data-mounted` flag in `useEffect`.
- Accordion. Animate height+opacity over 200ms. Measure content height or use a headless primitive; never animate to `auto`.
- Stagger.
  - Items: `opacity` + `translateY(8px)` over 300ms, 50ms between.
  - Exit: `opacity: 0; translateY(-12px)` over 150ms.
  - Skip for frequently seen UIs.
- Drag to dismiss.
  - Dismiss when distance passes threshold or speed > 0.11px/ms.
  - Call `setPointerCapture` on drag start; ignore extra touch points while dragging.
  - Add friction that rises past the boundary (no hard wall).
  - Set transform on the element itself; settle with the default spring.
- Crossfade that won’t settle. Blur the seam: `filter: blur(2px); opacity: .7` during the transition.
- Icon swap. Only for stateful icons (play/pause, like). Animate scale .25→1, opacity 0→1, blur 4px→0 together.
  - With Motion: `AnimatePresence mode="popLayout" initial={false}`, a keyed `motion.span`, and the icon-swap spring. Never add a library just for this.
  - Without one: keep both icons mounted, one absolutely over the other, and toggle `transition-[opacity,filter,scale] duration-300 ease-[cubic-bezier(0.2,0,0,1)]`.
- Skip the first-render animation. `initial={false}` on `AnimatePresence` suits toggles/tabs, not first-time entrances. Verify after a full refresh.
- Theme switch. Inject `*{transition:none!important}`, apply the theme, force a reflow (`document.body.offsetHeight`), then remove after two `requestAnimationFrame`s. Run on `matchMedia` changes. With `next-themes`, use `disableTransitionOnChange`.
- Tab indicator that changes color. Duplicate the tab list; style the copy as active; clip it to the active tab; animate `clip-path` over 250ms `ease-in-out`.
