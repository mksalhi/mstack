# Prototyping variants

Build several genuinely different versions of one UI piece behind a live picker. Never pick the winner yourself.

Rules
- Production doesn't import the harness, and the harness doesn't touch production, until a variant is promoted.
- State one named axis before building; secondary choices follow. Variants that differ only in accent color or copy count as one.
- Every variant fully works: real interactions, product-shaped copy, realistic data. No lorem ipsum; no dead buttons.
- Each variant clears: the [review](../review/index.md) “Always HIGH” list and the [animate](../animate/index.md) never-ship list.
- Open [PICKER.md](PICKER.md) when building the harness and copy its picker verbatim.

Steps
- Scope one piece per run; if the brief is broad, name the anchor component.
- Recon: stack, tokens, product personality, and where it renders. If no project, use neutral grays, one accent, system font, and say so.
- Directions: 3 by default, max 5; name by direction.
- Host (first that fits): existing page behind `?v=`; otherwise a `/prototypes/<slug>` route; otherwise one self-contained HTML file. Render one at a time in realistic context.
- Verify, present, stop: flip every variant; interactions work; console clean; clears the floor. Provide picker URL/path and keys.
- Promote on request: build the chosen variant properly; delete the harness unless asked to keep it.

Invocations
- `x5` 5 variants.
- `riff <variant>` new set around it.
- `keep <variant>` promote.
- `keep <variant>, leave the picker` promote; keep harness.
