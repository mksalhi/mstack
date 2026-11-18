# Token naming

Which ramps exist and what each step does: [palette-structure.md](palette-structure.md).

## Two tiers

**Primitives** name a value by hue and step (`--blue-500`, `--neutral-200`), never change meaning between themes, and are never applied in a component.

**Semantics** name a role (`--color-text-secondary`, `--color-border-subtle`), point at a primitive, and are the only tier components reference.

```css
:root {
  --blue-500: #3b82f6;          /* primitive: never used directly */
  --neutral-200: #e5e7eb;
  --color-accent-solid: var(--blue-500);  /* semantic: what components use */
  --color-border: var(--neutral-200);
}
```

Dark mode, white-label themes and increased-contrast variants repoint only the semantic tier.

Add a component tier (`--color-button-danger-bg`) only where a component intentionally diverges. Many component tokens mean the semantic tier is missing roles.

## The role inventory

The system is complete when every role has a token; build against this list, not screen by screen.

| Group | Roles |
| --- | --- |
| Surfaces | page background, surface, raised (menus, popovers), sunken (inputs, wells), overlay scrim |
| Text | primary, secondary, disabled, inverse, on-accent |
| Borders | subtle, default, strong, focus ring, separator |
| Accent | subtle background, border, solid, solid hover, text |
| Status | per status shipped: subtle background, border, solid, text |

Separator and border are separate roles even when they share a value today.

## Naming grammar

One shape: `--color-{role}-{variant}-{state}` (`--color-bg-surface`, `--color-text-secondary`, `--color-border-strong`, `--color-accent-solid-hover`).

One word per concept:

| Concept | Pick one | Never mix in |
| --- | --- | --- |
| Foreground | `text` | `fg`, `foreground`, `content`, `ink` |
| Background | `bg` | `background`, `surface` as a synonym, `fill` |
| Edge | `border` | `stroke`, `outline`, `line` |
| Brand color | `accent` | `primary`, `brand`, `theme` used interchangeably |

Reserve `primary` for "the most prominent of its group"; the brand is `accent`.

## Anti-patterns

| Name | Problem | Instead |
| --- | --- | --- |
| `--color-blue-button` | Appearance at the semantic tier; lies the moment the brand changes | `--color-accent-solid` |
| `--color-sidebar-gray` | Named for where it was used first; the second usage makes it nonsense | `--color-bg-surface` |
| `--color-light-gray` | Lies in dark mode, where it is the dark one | `--neutral-200` as a primitive |
| `--color-text-2` | Numbered semantics carry no meaning; nobody can guess what `3` would be | `--color-text-secondary` |
| `--color-gray-hover` | Mixes a hue with a state and belongs to no tier | `--color-bg-surface-hover` |
| `--blue-500` used in a component | Skips the semantic tier and removes the theming seam | Point a semantic token at it |

See also **Use a token only in its role** and [color-usage.md](color-usage.md).

## In Tailwind projects

Tailwind v4 generates `bg-*`, `text-*` and `border-*` from `--color-*` in `@theme`. Declare both tiers there:

```css
@theme {
  --color-brand-500: #3b82f6;
  --color-accent-solid: var(--color-brand-500);
  --color-text-secondary: var(--color-neutral-700);
}
```

Templates use semantic utilities (`bg-accent-solid`); flag a raw `bg-brand-500` in a component. Opacity modifiers (`bg-accent-solid/50`) can't be contrast-checked against a static background; use solid tokens for anything with text on it.
