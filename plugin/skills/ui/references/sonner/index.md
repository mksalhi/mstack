# Sonner

Docs: https://sonner.emilkowal.ski. Calls made with `toast()` override the Toaster’s `toastOptions`.

## Setup
- Mount one `<Toaster />` near the root (in Next.js, `layout.tsx`). Never one per page, never conditionally.
- Call `toast()` only from client code. Server actions return a result; the client shows the toast.

## Calls
- Update: `toast.loading('Uploading…')`, then `toast.success('Uploaded', { id })`. Reusing an `id` updates that toast.
- Promises: `toast.promise(p, { loading, success, error })`. The first arg must be a promise that settles; `success`/`error` can be functions of the result.
- Buttons: `{ action: { label, onClick } }` closes the toast unless `onClick` calls `event.preventDefault()`.
- Links: pass a function (`toast(() => <a …/>)`). For JSX without the default shell, use `toast.custom((t) => …)`.
- Dismiss: `toast.dismiss(id)` dismisses one, or all without an id. `onDismiss` (close/swipe) and `onAutoClose` (timeout) are separate.
- Several toasters: give each an `id` and target with `{ toasterId }`. Untargeted toasts render in every toaster.
- Duration: set `toastOptions={{ duration }}`; use `Infinity` for actionable or error toasts.

## Styling
- `classNames: { toast, title, description, actionButton, cancelButton, closeButton }` require `!important` on every class; otherwise go headless.
- Headless: `toast.custom()` wrapped in your own `toast()`.

## Troubleshooting
- Never appears: no Toaster, it unmounted, or `toast()` called on the server.
- Appears twice: two Toasters, or effect double-fired under StrictMode. Fire from the handler, or pass a stable `id`.
- Completely unstyled (Astro, view transitions): import 'sonner/dist/styles.css'.
- Unstyled inside Shadow DOM: copy the `[data-sonner-toaster]` style tag into the shadow root.
- Behind a modal, or clipped: ancestor creates a stacking context. Move the Toaster to the document root, outside any portal.
- Never closes: `duration: Infinity`, `dismissible: false`, or a promise that never settles.
