# Animation recipes

Start from the recipe and adapt. Values come from [index.md](index.md) (**Easing and duration**); a recipe that departs names the exemption.

## Button press

```css
.button { transition: transform 160ms var(--ease-out); }
.button:active { transform: scale(0.97); }
```

`scale()` carries the label and icons, which reads as a physical press. `:active` needs no hover gating; gate any `:hover` styling separately. Give the component a `static` prop to switch it off where motion distracts:

```tsx
const tapScale = "active:not-disabled:scale-[0.97]";
<button className={cn("transition-transform duration-150 ease-out", !isStatic && tapScale, className)} />
```

Motion: `<motion.button whileTap={{ scale: 0.97 }} />`.

## Dropdown, popover, menu, select

Scale out of the trigger:

```css
.popover {
  transform-origin: var(--transform-origin); /* Base UI supplies this */
  transition: opacity 200ms var(--ease-out), transform 200ms var(--ease-out);
}
.popover[data-starting-style], .popover[data-ending-style] { opacity: 0; transform: scale(0.95); }
```

## Tooltip

Popover shape, 125ms, `scale(0.97)` start. Once one tooltip is open, neighbours open with no delay and no animation:

```css
.tooltip[data-instant] { transition-duration: 0ms; }
```

## Modal

Stays centered (`transform-origin: center`, exempt). 250ms `var(--ease-out)`, start `opacity: 0; scale(0.96)`. Animate the backdrop's opacity on the same 250ms so they read as one surface.

## Drawer / sheet

```css
.drawer { transform: translateY(0); transition: transform 300ms var(--ease-drawer); }
.drawer[data-closed] { transform: translateY(100%); }
```

With drag, see **Drag to dismiss**.

## Toast

```css
.toast {
  transition: opacity 400ms ease, transform 400ms ease;
  @starting-style { opacity: 0; transform: translateY(100%); }
}
```

400ms `ease` is the named toast exemption (Sonner). Without `@starting-style`, set a mount flag in `useEffect` and style `data-mounted`. When stacked toasts reflow, tune opacity against height by feel and recheck the next day.

## Accordion / collapse

```css
.content { overflow: hidden; transition: height 200ms var(--ease-out), opacity 200ms var(--ease-out); }
```

Keep it short (layout cost every frame). Measure content height in JS or use a headless primitive; don't animate to `auto`.

## Stagger a group entrance

For occasionally seen lists, never ones scrolled past all day. Never block interaction.

```css
.item { opacity: 0; transform: translateY(8px); animation: fadeIn 300ms var(--ease-out) forwards; }
.item:nth-child(2) { animation-delay: 50ms; } /* +50ms per item */
@keyframes fadeIn { to { opacity: 1; transform: translateY(0); } }
```

Staged entrance where sequence carries hierarchy (hero, success, empty state): stagger semantic groups (title, description, actions) at 100ms with `opacity`, `translateY` and `blur(4px)` → `0`; a title may split into words at 80ms. Motion: `staggerChildren: 0.1` on the parent, shared `hidden`/`visible` variants.

Exit softer and shorter: `opacity: 0; translateY(-12px)` over 150ms `var(--ease-out)`. Slide fully out (`translateX(-100%)`, 200ms) only when spatial context matters (card returning to its list). No exit when motion adds no information, the interaction repeats often, or reduced motion is on.

## Hold to confirm

For destructive actions.

```css
.overlay { clip-path: inset(0 100% 0 0); transition: clip-path 200ms var(--ease-out); } /* release */
.button:active .overlay { clip-path: inset(0 0 0 0); transition: clip-path 2s linear; } /* press */
.button:active { transform: scale(0.97); }
```

`linear` because the fill is progress.

## Tab indicator with a color transition

Duplicate the tab list, style the copy as active (background and text), clip it to the active tab, animate the clip:

```css
.tabs-active-copy { clip-path: inset(0 60% 0 20%); transition: clip-path 250ms var(--ease-in-out); }
```

## Scroll reveal

Marketing surfaces only.

```css
.reveal { clip-path: inset(0 0 100% 0); transition: clip-path 600ms var(--ease-in-out); }
.reveal[data-visible] { clip-path: inset(0 0 0 0); }
```

Trigger with `IntersectionObserver` or Motion `useInView` with `{ once: true, margin: "-100px" }`. Fire once.

## Drag to dismiss

Springs, not durations.

```js
const velocity = Math.abs(swipeAmount) / (Date.now() - dragStartTime.current);
if (Math.abs(swipeAmount) >= SWIPE_THRESHOLD || velocity > 0.11) dismiss();
element.style.transform = `translateY(${distance}px)`; // on the element, not a parent CSS var
```

- Pointer capture once the drag starts.
- Multi-touch protection: `if (isDragging) return` on new touch points.
- Damping past boundaries: friction that rises with distance, not a wall.
- Settle with `{ type: "spring", duration: 0.5, bounce: 0.2 }`.

## Masking a crossfade that won't settle

When easing and duration tuning can't fix a visible overlap, blur the seam:

```css
.content { transition: filter 200ms ease, opacity 200ms ease; }
.content.transitioning { filter: blur(2px); opacity: 0.7; }
```

Keep blur under 20px (expensive, especially Safari).

## Programmatic, without a library

```js
element.animate(
  [{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }],
  { duration: 1000, fill: 'forwards', easing: 'cubic-bezier(0.77, 0, 0.175, 1)' }
);
```

## Icon swap

For state-changing icons (play/pause, like/liked) or icons appearing on hover. Animate together: scale `0.25` → `1`, opacity `0` → `1`, blur `4px` → `0px`. Static navigation, decorative and always-visible icons don't animate.

With a library, use whichever of `motion/react` or `framer-motion` the project has; never add one for this:

```tsx
<AnimatePresence mode="popLayout" initial={false}>
  <motion.span
    key={isActive ? "active" : "inactive"}
    initial={{ opacity: 0, scale: 0.25, filter: "blur(4px)" }}
    animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
    exit={{ opacity: 0, scale: 0.25, filter: "blur(4px)" }}
    transition={{ type: "spring", duration: 0.3, bounce: 0 }}
  ><Icon /></motion.span>
</AnimatePresence>
```

Without one, keep both icons mounted, one `absolute inset-0` over the other (the non-absolute one sets layout size), and toggle:

```tsx
const swap = "transition-[opacity,filter,scale] duration-300 ease-[cubic-bezier(0.2,0,0,1)]";
const shown = "scale-100 opacity-100 blur-0";
const hidden = "scale-[0.25] opacity-0 blur-[4px]";
```

## Skip the enter animation on first render

`initial={false}` on `AnimatePresence`: right for icon swaps, toggles, tabs, segmented controls. Wrong where `initial` drives a first-time entrance (staggered hero, loading state). Check a full page refresh after applying.

## Suppress transitions on theme switch

```tsx
function suppressTransitions(apply: () => void) {
  const style = document.createElement("style");
  style.append(document.createTextNode("*,*::before,*::after{transition:none !important}"));
  document.head.append(style);
  apply();
  void document.body.offsetHeight; // force style flush
  requestAnimationFrame(() => requestAnimationFrame(() => style.remove()));
}
```

Wrap in-app toggles, and call it from a `matchMedia("(prefers-color-scheme: dark)")` change listener. `next-themes`: `disableTransitionOnChange`.

## Image placeholder

A hero or large image that would otherwise pop in. Inline a tiny SVG version behind it, blurred with an SVG filter, so something shows on first paint with no extra request. Tune the blur `stdDeviation` in code for how much detail shows. When the real image loads, fade it in with `opacity` (200–300ms, `var(--ease-out)`) and remove the SVG from the DOM.

```html
<div class="hero">
  <svg class="hero-placeholder" viewBox="0 0 40 24" aria-hidden="true" preserveAspectRatio="none">
    <filter id="hero-blur"><feGaussianBlur stdDeviation="2" /></filter>
    <g filter="url(#hero-blur)"><!-- a few rects or paths in the image's main colors --></g>
  </svg>
  <img src="hero.jpg" alt="..." onload="this.classList.add('loaded'); this.previousElementSibling.remove()" />
</div>
```

```css
.hero { display: grid; }
.hero > * { grid-area: 1 / 1; width: 100%; height: 100%; }
.hero img { opacity: 0; transition: opacity 250ms var(--ease-out); }
.hero img.loaded { opacity: 1; }
```

## Coded explainer

Marketing or onboarding motion that would otherwise be a video (a product walkthrough, devices, a flow diagram). Build the devices, screens and steps from DOM and SVG, animated with WAAPI or CSS. The result is a few KB instead of megabytes, sharp at any resolution, responsive, and localizable, since the text is real text. Video placeholders work the same way: redraw two or three key stills as inline SVG so the play button shows instantly.

- Real text needs real semantics: label the illustration (`role="img"` with an `aria-label`, or a visible caption), and hide pure decoration with `aria-hidden="true"`.
- It is the explanation tier: it plays when it scrolls into view or on request, never loops in a user's working view, and drops movement under reduced motion while keeping the end state.

