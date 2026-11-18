# Layout

These numbers are defaults for projects with no density system. If the project has one, use it. Hit areas and focus belong to [accessibility](../accessibility/index.md), radius and shadows to [polish](../polish/index.md), and measure and text spacing to [typography](../typography/index.md).

- **Group with space before lines.** Use background shapes for units such as selectable rows, and separator lines only in dense data. The gap between groups is at least twice the gap inside one (8px inside, 16px or more between). Lines added to a gap that already separates are a finding.
- **Controls look like controls.** A control needs a fill, a border, an underline, or a fixed zone such as a toolbar. A static badge must not be shaped like the buttons beside it.
- **Shared edges.** Use few alignment edges and one spacing step per nesting level. An icon 2px off the text edge is a finding. In tables, numbers align to the trailing edge and text to the leading edge.
- **Logical properties.** Use `margin-inline-start` and `inset-inline-end` (Tailwind `ms-4 pe-6 text-start`). Use physical sides only for physical geometry, such as a notch or a gesture direction. Progressions (steps, ratings, progress bars) mirror in RTL, but hand-positioned elements don't mirror on their own.
- **Importance order.** The number the user came for goes at the top and leading edge. In a row, the identifying content leads and metadata and actions trail. Have one primary action per view, and put secondary actions in a menu once there are more than two or three.
- **Hidden content needs a cue.** Let the next item peek 16 to 32px past a scroll edge, create the peek with container padding, and keep snap points on the content edge. Label disclosure with what it hides: "Show 12 more results", not "More".
- **Spacing between controls.** Leave 12px between bordered or filled controls and 24px around borderless text or icon buttons. Compact tools can go tighter if hit areas don't overlap.
- **Content bleeds, controls float.** Backgrounds and media run to the edges. Text and controls stay inside the layout margins and `env(safe-area-inset-*)`. Full-width buttons sit inside the margins (about 16px on mobile) with a radius; edge-to-edge is only for platform chrome that handles safe areas.
- **Breakpoints come from the content.** Break where the layout stops fitting, not at a device preset. Collapse late. Prefer container queries for components, and test the smallest and largest sizes first.
- **Growth.** Never use fixed widths or heights on text containers; translations grow. Size buttons from their label. Test with pseudo-localization. A primary action must never be clippable: not at the bottom of a resizable pane, and not under a keyboard. In a scrolling modal, the action row doesn't scroll.

**Severity:**

- **HIGH:** content or an action is blocked at a supported viewport.
- **MEDIUM:** hierarchy, reading order or adaptability suffers.
- **LOW:** isolated alignment.

Verify at every supported width, at 200% zoom and in RTL. Use the format in [review](../review/index.md#output).
