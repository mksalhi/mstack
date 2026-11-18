# Plan template

Every animate-area audit plan uses this structure. The executor has zero context and zero taste; never reference "the audit above".

```markdown
# NNN — <Short imperative title>

- **Status**: TODO
- **Commit**: <`git rev-parse --short HEAD` when written>
- **Severity**: HIGH | MEDIUM | LOW
- **Category**: <audit category>
- **Estimated scope**: <n files, rough size>

## Problem

What is wrong, where, and how it hurts feel. Cite every location as
`path/to/file.tsx:123` with the current code verbatim:

​```css
/* src/components/dropdown.css:14 — current */
.dropdown { transition: all 400ms ease-in; }
​```

## Target

Exact end state, every value spelled out (curves, durations, spring configs, media queries):

​```css
.dropdown {
  transition: transform 200ms var(--ease-out), opacity 200ms var(--ease-out);
  transform-origin: var(--transform-origin);
}
​```

## Repo conventions to follow

- Easing tokens live in `src/styles/tokens.css`; add new curves there, e.g. `--ease-out: cubic-bezier(0.23, 1, 0.32, 1);`
- <exemplar file:line that already does this correctly>

## Steps

1. <One concrete edit per step: file, change, resulting code.>

## Boundaries

- Do NOT touch <out-of-scope files/components>.
- Do NOT change markup/structure; motion properties only (unless a step says otherwise).
- Do NOT add dependencies.
- If a step doesn't match the code (drift since the commit stamp), STOP and report.

## Verification

- **Mechanical**: <exact typecheck/lint/build commands and expected outcome>.
- **Feel check**: trigger <interaction> and confirm:
  - <e.g. "the dropdown scales from its trigger, not from center">
  - <e.g. "spamming the toggle never restarts the animation from zero">
  - DevTools Animations panel at 10% playback: <detail>.
  - Toggle `prefers-reduced-motion` (Rendering panel): movement drops, opacity feedback remains.
- **Done when**: <machine- or eye-checkable criteria>.
```

## Notes for the plan author

- One plan per finding; merge two only if they share every file and the same fix pattern.
- Pull every value from [audit-catalog.md](audit-catalog.md), never from memory.
- The feel check is mandatory.
- After writing plans, update `plans/README.md`: table (number, title, severity, status), execution order, dependencies.
