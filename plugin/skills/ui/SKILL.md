---
name: ui
description: "Use for any UI work or review: a screen, flow or UI diff; accessibility; spacing, layout, RTL; UI copy; type; color, contrast, dark mode; polish; web, React Native or Expo animation; web apps that must feel native on a phone; Sonner toasts; worst-case data ('break this'); or UI variants behind a picker ('prototype')."
metadata:
  harness: "claude codex"
  platform: "darwin linux"
  scope: universal
---

# UI

Open the area file for each area the task touches and follow it; `/mstack:ui <area>` opens one directly. Paths in an area file resolve against its folder. Each area's core line below applies even unopened.

- [review](references/review/index.md). Open first for any review; it runs the other areas in order. Cite file:line per finding, one row per root cause, max 15. Block if any HIGH remains, else Approve; read-only unless asked to fix.
- [accessibility](references/accessibility/index.md). Native elements before ARIA. Every control has a name, visible focus and keyboard reach. Never disable submit until valid.
- [layout](references/layout/index.md). Logical properties for RTL. One primary action. Never fix text box sizes.
- [copy](references/copy.md). Match the surrounding voice. Buttons start with a verb. Errors say how to fix. Never concatenate around a variable.
- [typography](references/typography/index.md). Keep the project typeface and scale. Tabular figures on changing numbers. Never disable zoom.
- [colors](references/colors/index.md). Never report contrast you did not measure. Components use semantic tokens only.
- [polish](references/polish/index.md). Concentric radius. Shadows for depth, borders for structure.
- [animate](references/animate/index.md). Never animate keyboard actions or 100+/day UI. Transform and opacity only, UI 300ms or less. Never `transition: all`, `scale(0)` or ease-in. Movement only inside `prefers-reduced-motion: no-preference`.
- [animate-expo](references/animate-expo/index.md). Reanimated 4 on the UI thread; never core `Animated` or `setState` per frame. Screen transitions come from the native stack.
- [mobile-web](references/mobile-web.md). Gate on `hover`, `pointer` and `dvh`, never user agent or width.
- [break](references/break/index.md). Worst-case values from real limits, injected as data. Report, then stop unless asked to fix.
- [sonner](references/sonner/index.md). One `<Toaster />` near the root; `toast()` only from client code.
- [prototype](references/prototype/index.md). Only when asked. Fully working variants behind the verbatim picker; never pick the winner.
