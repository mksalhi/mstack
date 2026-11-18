# Sonner

Docs: https://sonner.emilkowal.ski. Calls made with `toast()` override the Toaster's `toastOptions`.

## Setup

- **Mount one `<Toaster />` near the root** (in Next.js, `layout.tsx`). Never one per page, and never conditionally.
- **Call `toast()` only from client code.** A server action returns its result, and the client shows the toast.
- **`theme` defaults to `'light'` and ignores the OS.** Pass `theme="system"`, or `resolvedTheme` from `next-themes`.

## Calls

- **Variants:** `toast('Title', { description })`, `toast.success`, `.error`, `.info`, `.warning`.
- **Update:** call `toast.loading('Uploading…')`, then `toast.success('Uploaded', { id })`. Reusing an `id` updates that toast.
- **Promises:** `toast.promise(p, { loading, success, error })`, where `success` and `error` can be functions of the result. The first argument must be a promise that settles.
- **Buttons:** `{ action: { label, onClick } }` closes the toast unless `onClick` calls `event.preventDefault()`. `cancel` is the secondary button.
- **Links in the text:** pass a function: `toast(() => <a …/>)`. For JSX without the default shell, use `toast.custom((t) => …)`.
- **Dismissing:** `toast.dismiss(id)` dismisses one, or all without an id. Read active toasts with `useSonner()` or `toast.getActiveToasts()`. `onDismiss` fires on the close button or a swipe, and `onAutoClose` on timeout; there's no single "closed" callback.
- **Several toasters:** give each an `id` and target it with `{ toasterId }`. An untargeted toast renders in every toaster.
- **Duration:** the default 4000ms is too short. Set `toastOptions={{ duration: 5000 }}`, and use `Infinity` for toasts holding an action or an error.

## Styling ladder

Climb only as far as you need:

1. `richColors` or `invert`.
2. `style`.
3. `classNames: { toast, title, description, actionButton, cancelButton, closeButton }`. Every class needs `!important`; if you need more than a few, go headless.
4. Headless: `toast.custom()` wrapped in your own `toast()`, which beats `unstyled: true` for a design system.

Icons: set `icons` on the Toaster or `icon` per toast; `null` removes one.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Never appears | No Toaster is mounted, or it unmounted, or `toast()` was called on the server |
| Appears twice | There are two Toasters, or an effect double-fired under StrictMode. Fire from the handler, or pass a stable `id`. |
| Completely unstyled (Astro, view transitions) | `import 'sonner/dist/styles.css'` |
| Unstyled inside Shadow DOM | Copy the `[data-sonner-toaster]` style tag into the shadow root |
| Behind a modal, or clipped | An ancestor creates a stacking context (`transform`, `filter`, `overflow`). Move the Toaster to the document root, outside any portal. |
| Never closes | `duration: Infinity`, `dismissible: false`, or a promise that never settles |
| Swipes the wrong way | Set `swipeDirections` |
| Too close to the edge on mobile | `mobileOffset`, which applies below 600px wide and defaults to 16px |
