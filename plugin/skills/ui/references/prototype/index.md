# Prototyping variants

Build several genuinely different versions of one piece of UI ("the pricing card", "a hold-to-delete button") behind a live picker, then hand the choice back. **Never pick the winner yourself.**

## Rules

1. **Production doesn't import the harness**, and the harness doesn't touch production, until a variant is promoted.
2. **Variants differ along one named axis**, stated in a phrase before you build:

   | Axis | What varies |
   |---|---|
   | Structure | Grouping, order, columns, what collapses |
   | Density | Spacing, hit areas, how much fits |
   | Emphasis | Where color fills and what recedes |
   | Type | Scale steps, weight contrast, measure |
   | Voice | Labels, tone, amount of copy |
   | Personality | Quiet to playful: shadows, radii, ornament |
   | Motion or interaction | The entrance story, or the gesture |

   Secondary choices follow from the axis. Two variants that differ only in accent color or copy count as one.
3. **Every variant fully works**, with real interactions, product-shaped copy and realistic data. No lorem ipsum and no dead buttons.
4. **Every variant clears the same floor:**
   - The [review](../review/index.md) "Always HIGH" list.
   - The [animate](../animate/index.md) never-ship list.

   A direction that only works by breaking the floor gets dropped, and you say so.
5. **Copy the picker from [PICKER.md](PICKER.md) verbatim.**

## Steps

1. **Scope one piece per run.** If the brief is "the dashboard", name the component the rest hang off and offer the others as later runs.
2. **Recon:** the stack, tokens, the product's personality (which bounds the boldest variant), and where the piece renders. With no project, use neutral grays, one accent and the system font, and say so.
3. **Directions.** Three by default, at most five. Name each one by its direction ("Quiet", "Editorial", "Dense"), never "Option A".
4. **Pick a host,** taking the first that fits:
   - The existing page, behind `?v=`.
   - Otherwise a `/prototypes/<slug>` route.
   - Otherwise one self-contained HTML file.

   Render one variant at a time, full size, in realistic context: a toast needs a page behind it, a card needs siblings.
5. **Verify:** flip through every variant yourself. Each one renders, its interactions work, the console is clean, and it clears the floor. Then present the variants and stop:

   | # | Variant | Axis position | Right when | Costs |
   |---|---|---|---|---|

   Give the picker URL or path, the keys, and the width you judged at. Cut any variant that converged with another, and say so.
6. **Promote on request.** Build the chosen variant properly, following project conventions, then delete the harness unless asked to keep it.

Invocations:

- `x5` builds that many variants.
- `riff <variant>` builds a new set around that one.
- `keep <variant>` promotes it.
- `keep <variant>, leave the picker` promotes it and keeps the harness.
