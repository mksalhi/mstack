# Working with Sonner

Answer Sonner ([docs](https://sonner.emilkowal.ski)) tasks from this file first. Exact prop names, types and defaults are in [API.md](API.md).

## Setup

1. One `<Toaster />`, mounted once near the root (Next.js: `layout.tsx`; works in server components). Never per-page or conditional.
2. `toast()` from client code only (handlers, effects, callbacks); no hook or provider. In a server action, return the result and call `toast()` on the client.

```jsx
import { Toaster } from 'sonner'; // once, in layout
import { toast } from 'sonner';   // anywhere client-side
```

## Picking the right call

| You want | Call |
| --- | --- |
| Plain message | `toast('Title')`, `{ description }` for a second line |
| Typed icon | `toast.success('…')`, `toast.error('…')`, etc. |
| Spinner, state managed yourself | `toast.loading('…')`, then update by id |
| Loading → success/error from a promise | `toast.promise(promise, { loading, success, error })`; success/error accept functions of the result/error |
| Button | `{ action: { label, onClick } }`; closes unless `onClick` calls `event.preventDefault()`; `cancel` is secondary |
| Custom JSX in the default shell | `toast(<jsx />)` |
| Custom JSX, no styles | `toast.custom((t) => <jsx />)`; `t` gives the id |

## Recipes

- **Update**: call again with the same `id`; only passed props change. `toast.success(…, { id })` changes the type.

  ```jsx
  const id = toast.loading('Uploading…');
  toast.success('Uploaded', { id });
  ```

- **Durations**: action and error toasts `duration: Infinity`; timed toasts at least 5000ms via `<Toaster toastOptions={{ duration: 5000 }} />` (default 4000ms is too short). Rule source: the accessibility area's [Autoplay and timed UI](../accessibility/motion-and-zoom.md#autoplay-and-timed-ui).
- **Dismiss**: `toast.dismiss(id)`, or `toast.dismiss()` for all. **Active toasts**: `useSonner()` in React, `toast.getActiveToasts()` outside.
- **Links/components in text**: pass a function, `toast(() => <a href="…">View</a>)`.
- **Multiple toasters**: give each an `id`, target with `{ toasterId: 'canvas' }`; untargeted toasts render in every toaster.
- **Close callbacks**: `onDismiss` (close button or swipe) and `onAutoClose` (timeout) are separate; there's no single "closed" callback.

## Styling: the escalation ladder

Climb only as far as needed; jumping straight to headless is fine, lingering mid-ladder is not.

1. Defaults, plus `richColors` (colored success/error; otherwise gray) or `invert`.
2. `toastOptions={{ style: {…} }}` on the Toaster, or `style` per call.
3. `toastOptions={{ classNames: { toast, title, description, actionButton, cancelButton, closeButton } }}`. Every class needs `!important` (Tailwind `!text-red-900`). More than a few? Go headless.
4. Headless: `toast.custom()` wrapped in your own `toast()` abstraction (recommended for design-system toasts; better than `unstyled: true`).

Icons: Toaster `icons` per type, `icon` per toast, `null` removes. Theme defaults to `'light'` and ignores the OS: pass `theme="system"` or `<Toaster theme={resolvedTheme} />` from `next-themes`.

## Troubleshooting

| Symptom | Cause → fix |
| --- | --- |
| Never appears | No `<Toaster />` mounted or it unmounted; mount one at the root. Server action: call `toast()` on the client. |
| Appears twice | Two Toasters (layout and page): keep one. Or an effect under StrictMode double-invoke: fire from the handler or pass a stable `id`. |
| Classes have no effect | Use `!important`, `unstyled`, or headless. |
| Completely unstyled (Astro, view transitions) | `import 'sonner/dist/styles.css'` in a layout. |
| Unstyled inside Shadow DOM | Copy the style tag containing `[data-sonner-toaster]` from `document.head` into the shadow root. |
| Behind a modal or clipped | Ancestor stacking context (`transform`, `filter`, `overflow`) or higher-z overlay. Move `<Toaster />` to the document root, outside dialogs/portals. |
| Never closes | `duration: Infinity`, `dismissible: false`, or a `toast.promise` that never settles. |
| `toast.promise` stuck loading | First argument must be a promise (or function returning one) that resolves/rejects. |
| Swipe goes the wrong way | Directions derive from `position`; set `swipeDirections`. |
| Too close to the edge on mobile | `offset` (default 32px) and `mobileOffset` (<600px, default 16px): number, CSS string, or per-side object. |
