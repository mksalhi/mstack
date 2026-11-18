# Sonner API reference

`toast()` options override the same options in the Toaster's `toastOptions`.

## `<Toaster />`

| Prop | Type | Default | Notes |
| --- | --- | --- | --- |
| `theme` | `string` | `'light'` | `'light'`, `'dark'`, `'system'` |
| `richColors` | `boolean` | `false` | Colorful error/success |
| `expand` | `boolean` | `false` | Expanded by default (else on hover) |
| `visibleToasts` | `number` | `3` | |
| `id` | `string` | – | Targeted by `toasterId` |
| `position` | `string` | `'bottom-right'` | `top-left`, `top-center`, `top-right`, `bottom-left`, `bottom-center`, `bottom-right` |
| `closeButton` | `boolean` | `false` | On all toasts |
| `offset` | `string \| number \| object` | `'32px'` | Per-side object: `{ bottom: '24px', right: '16px' }` |
| `mobileOffset` | `string \| number \| object` | `'16px'` | Width < 600px |
| `swipeDirections` | `array` | from position | Swipe-to-dismiss directions |
| `dir` | `string` | `'ltr'` | |
| `hotkey` | `string` | `⌥/alt + T` | Focuses the toaster |
| `invert` | `boolean` | `false` | Dark in light mode and vice versa |
| `toastOptions` | `object` | – | Defaults for every toast |
| `gap` | `number` | `14` | Gap when expanded |
| `icons` | `object` | – | `{ success, info, warning, error, loading }`; `null` removes |

## `toast()` options

`toast(message, options)`: message is a string, JSX, or a function returning JSX. Returns the id.

| Option | Type | Default | Notes |
| --- | --- | --- | --- |
| `description` | `ReactNode` | – | Below the title; accepts a function |
| `closeButton` | `boolean` | `false` | |
| `invert` | `boolean` | `false` | |
| `duration` | `number` | `4000` | ms; `Infinity` persists |
| `position` | `string` | `'bottom-right'` | |
| `dismissible` | `boolean` | `true` | `false` blocks user dismissal |
| `icon` | `ReactNode` | – | `null` removes the default |
| `action` | `ReactNode \| { label, onClick }` | – | Closes unless `onClick` calls `event.preventDefault()` |
| `cancel` | `ReactNode \| { label, onClick }` | – | Closes on click |
| `actionButtonStyle` | `object` | `{}` | |
| `cancelButtonStyle` | `object` | `{}` | |
| `id` | `string` | – | Same id updates the existing toast |
| `testId` | `string` | – | `data-testid` |
| `toasterId` | `string` | – | Target toaster |
| `style` | `object` | – | |
| `classNames` | `object` | – | `{ toast, title, description, actionButton, cancelButton, closeButton }`; needs `!important` unless `unstyled` |
| `unstyled` | `boolean` | `false` | Removes default styles |
| `onDismiss` | `(toast) => void` | – | Close button or swipe |
| `onAutoClose` | `(toast) => void` | – | Timeout close |
| `containerAriaLabel` | `string` | `'Notifications'` | |

## Functions

| Function | Purpose |
| --- | --- |
| `toast(message, opts?)` | Render; returns id |
| `toast.success / .error / .info / .warning(message, opts?)` | Typed toast |
| `toast.loading(message, opts?)` | Spinner; update by id |
| `toast.promise(promise, { loading, success, error })` | `success`/`error`: strings, JSX, functions of the result, or toast-option objects |
| `toast.custom((t) => jsx, opts?)` | Headless |
| `toast.dismiss(id?)` | One, or all without an id |
| `toast.getActiveToasts()` | Outside React |
| `useSonner()` | Hook returning `{ toasts }` |
