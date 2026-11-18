# Forms

## Labels

Every control needs `<label for>` pointing at the input's `id`, or a wrapping `<label>` (which also merges the hit target). A placeholder is never a label; use it only alongside one, for an example format: `placeholder="name@company.com"`.

```html
<label for="email">Email</label>
<input id="email" type="email" autocomplete="email" />
```

Mark required fields with native `required` plus a visible indicator explained once per form ("* required").

## Error messaging

```html
<input id="email" type="email" autocomplete="email"
  aria-invalid="true" aria-describedby="email-error" />
<p id="email-error">Enter a valid email address.</p>
```

- `aria-invalid="true"` on the failing field, removed once fixed.
- Errors render inline beside their fields with an icon or text, never a red border alone.
- On submit, focus the first invalid field. Never disable submit until valid.
- Accept free text and validate after; never block typing or filter characters. Trim values before validating.

## Autocomplete and input types

`autocomplete` is required (WCAG 1.3.5) for fields about the user:

| Field | `autocomplete` |
| --- | --- |
| Name | `name` (or `given-name` / `family-name`) |
| Email | `email` |
| Phone | `tel` |
| Address | `street-address`, `address-line1`, `postal-code`, `country` |
| Card | `cc-number`, `cc-exp`, `cc-csc`, `cc-name` |
| Login | `username`, `current-password` |
| Signup / reset | `new-password` |
| 2FA code | `one-time-code` |

Prefix with a section where relevant: `autocomplete="shipping street-address"`.

| Input | Use |
| --- | --- |
| Email, URL, phone | `type="email"`, `type="url"`, `type="tel"` |
| OTP / PIN / card number | `type="text" inputmode="numeric"` (no spinner) |
| Money, decimals | `type="text" inputmode="decimal"` |
| True numeric quantity | `type="number"` |

Set `spellcheck="false"` on emails, codes and usernames. Stay compatible with password managers and 2FA autofill: real `<form>`, correct `autocomplete`, no fake inputs.

## Submit behavior

- Keep submit enabled until the request starts, then disable it and show a spinner *beside the original label* ("Save" with a spinner, never a bare spinner).
- Success goes through a polite live region. On failure, focusing the first invalid field is the announcement. Reserve `role="alert"` for form-level errors not tied to a field ([screen-readers.md](screen-readers.md)).
- Warn on unsaved changes before navigation; never lose typed input to a re-render. Hydration must preserve focus and value.
- Enter submits from any focused input; in `<textarea>`, ⌘/Ctrl+Enter submits.
