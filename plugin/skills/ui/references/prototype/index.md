# Prototyping variants

Take one described piece of UI ("a toast", "the pricing card", "a hold-to-delete button"), build several genuinely different versions, put them behind a picker so the user can flip through live, and hand the choice back. Reviewing existing UI is the [review area](../review/index.md); planning motion fixes is the animate area's [audit mode](../animate/audit-workflow.md).

The value is divergence: each variant is a direction you could defend shipping alone.

## Hard rules

1. Production never imports the harness, and the harness never changes production code, until Phase 6 promotes the picked variant.
2. Variants diverge on one named axis (see the table below), statable in a phrase before building. Sharing the project's tokens is not convergence.
3. Every variant fully works: real interactions, real motion, product-shaped copy, plausible names and the real item count. No lorem ipsum, dead buttons, or "imagine this part".
4. Every variant clears the same floor, which never trades against the axis:
   - Every control has an accessible name, the keyboard reaches everything a pointer does, focus is visible, nothing clips at 320px, and no meaning rides on color alone (the review area's escalation triggers).
   - Motion meets the craft bar: `ease-out` on entrances (never `ease-in`), UI motion under 300ms, correct `transform-origin`, `transform`/`opacity` only, reduced motion handled.
   - A direction that only works by breaking the floor gets dropped, and you say so.
5. The picker is chrome: copy [PICKER.md](PICKER.md) verbatim; it never adapts to the project.
6. Never pick the winner. The choice is the user's.
7. After promotion, delete the harness unless the user asks to keep it.

## Axes

Each variant answers the same brief from a different position on one primary axis:

| Axis | `ui` area | What varies |
| --- | --- | --- |
| Structure | [layout](../layout/index.md) | Grouping, order, column count, what collapses |
| Density | [layout](../layout/index.md) | Spacing scale, hit areas, how much fits |
| Emphasis | [colors](../colors/index.md) | Where filled color goes, what recedes |
| Type | [typography](../typography/index.md) | Scale steps, weight contrast, measure |
| Voice | [copy](../copy.md) | Labels, tone, how much copy |
| Personality | [polish](../polish/index.md) | Quiet to playful: shadows, radii, ornament |
| Motion or interaction | [animate](../animate/index.md) | Entrance story, gesture, what the user does to act |

Secondary choices follow from the primary position (a dense variant may take a smaller type step) and never vary on their own. Two variants that differ only in accent color or copy are one: move one to a new position or cut it.

## Workflow

### Phase 1: Scope

One piece per run. If the brief spans several components ("the dashboard"), name the one the others hang off, say why, and offer the rest as later runs. Restate the brief in one sentence: what it is, where it renders, what it does.

### Phase 2: Recon

- **Stack:** framework, styling system, component library, motion library.
- **Tokens:** color, spacing, radius, type scale, easing and duration. Variants use them.
- **Personality:** the product's density and voice, from playful consumer to crisp dashboard. It bounds the boldest variant.
- **Context:** background, neighbors and widths where the piece renders.

With no project to read, use neutral grays, one accent and the system font stack, and say so.

### Phase 3: Choose directions

Default to 3 variants; up to 5 when asked or the space is genuinely wide, never more. Before coding, write a name and axis position for each. Names state the direction ("Quiet", "Editorial", "Dense"), never "Option A".

**Done when** no two variants share a position and each one's axis fits in a phrase.

### Phase 4: Build the harness

Pick the host, first match wins:

- **The piece belongs on an existing page:** build the variants into that page, with its real chrome, neighbors and data, behind the picker's dev-only `?v=` param.
- **A project with a dev server but no host page yet:** an isolated route (`/prototypes/<slug>` or equivalent), one file per variant plus a small harness.
- **No project, or a static page:** one self-contained HTML file with inline CSS and JS.

Load [PICKER.md](PICKER.md) now and build exactly that. Render one variant at a time, full size, in realistic context (a toast needs a page behind it, a card needs siblings, a button needs a form); never side-by-side thumbnails. Switching variants is instant, no animation.

### Phase 5: Verify and hand off

Run the harness and flip through every variant yourself: each renders, every interaction responds, the console is clean, and the floor holds. Screenshot each if browser tooling is available. Then present and **stop**:

| # | Variant | Axis position | Right when | Costs |
| --- | --- | --- | --- | --- |
| 1 | Quiet | Lowest visual weight | The page is used daily | Least memorable |
| 2 | Editorial | Largest type, most space | The moment deserves weight | Eats vertical space |

Close with where the picker runs (URL or file path), the keys to flip, and the width you judged at (375px and 1440px can differ). Never mark a favorite. Asked which you'd choose, answer from the product's personality and how often the piece is seen, not aesthetics alone. If two variants converged while building, cut one and say so.

**Done when** every variant is reachable and correct, the console is clean, and the table names each tradeoff honestly.

### Phase 6: Promote on selection

Build the picked variant properly where it belongs, following project conventions (file layout, naming, tokens), then delete the other variants and the harness (Hard rule 7). For another round, keep the harness and rerun Phase 3 with new positions around the preferred direction.

## Invocations

| Invocation | Behavior |
| --- | --- |
| `<description>` | Scope, recon, 3 variants, picker, wait for the choice |
| `<description> x5` | That many variants (capped at 5) |
| `riff <variant>` | Keep the harness; a new set diverging around that variant |
| `keep <variant>` | Promote it and delete the harness |
| `keep <variant>, leave the picker` | Promote it and keep the harness |
