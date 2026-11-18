---
name: ui
description: "Use for any UI work or review: a screen, flow, PR or diff review; accessibility, keyboard, ARIA, hit targets; spacing, layout, RTL; UI copy; type scale and fonts; colors, contrast, dark mode; visual polish; web animation; React Native or Expo motion and gestures; web apps that must feel native on a phone; Sonner toasts; worst-case data ('break this', 'edge cases'); or several UI variants behind a picker ('prototype')."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# UI

Read the file for the area the task touches and follow it; a task can touch several. `/mstack:ui <area>` opens that area directly. Relative paths in an area file resolve against its own folder.

| Area | Use for |
|---|---|
| [review](references/review/index.md) | Full review of a screen, flow, PR or diff. Start here; it pulls in the other areas as it goes. |
| [accessibility](references/accessibility/index.md) | Keyboard, focus, ARIA, labels, screen readers, hit targets, reduced motion, WCAG |
| [layout](references/layout/index.md) | Spacing, grouping, alignment, reading order, breakpoints, RTL, safe areas |
| [copy](references/copy.md) | In-product text: buttons, errors, empty states, labels, capitalization |
| [typography](references/typography/index.md) | Type scale, line-height, measure, font loading, OpenType, wrapping, truncation |
| [colors](references/colors/index.md) | Palettes, tokens, contrast, dark mode, gradients, color formats |
| [polish](references/polish/index.md) | Detail pass on a component: radii, optical alignment, shadows vs borders, icons, states |
| [animate](references/animate/index.md) | Adding, fixing or auditing web animation and transitions (not code-rendered video) |
| [animate-expo](references/animate-expo/index.md) | React Native or Expo motion: gestures, sheets, screen transitions, haptics, jank on device |
| [mobile-web](references/mobile-web.md) | A web app that must feel native on a phone: 100vh, input zoom, tap highlight, notch, sticky hover, PWA |
| [break](references/break/index.md) | Stress-testing with worst-case data: long names, empty, huge counts, RTL, emoji |
| [sonner](references/sonner/index.md) | Sonner toasts in React: missing, doubled, unstyled, behind a modal, wrong theme |
| [prototype](references/prototype/index.md) | Several genuinely different versions of a UI piece behind a live picker. Only when asked. |
