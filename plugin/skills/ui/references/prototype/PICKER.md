Copy the markup, CSS and wiring below verbatim; only variant names and count change per run. Never restyle it with project tokens, fonts or colors. It is a floating dark-glass pill, bottom-center, deliberately not theme-aware.

## Markup

```html
<nav class="proto-picker" aria-label="Prototype variants">
  <span class="proto-picker-highlight" aria-hidden="true"></span>
  <button class="proto-picker-item" data-active aria-current="true">Quiet</button>
  <button class="proto-picker-item">Editorial</button>
  <button class="proto-picker-item">Playful</button>
  <span class="proto-picker-divider" aria-hidden="true"></span>
  <button class="proto-picker-item proto-picker-replay" aria-label="Replay animation (R)">↻</button>
</nav>
```

In a framework, keep class names and structure.

## Rules

- Verbatim. No project fonts, brand colors, theme switching, or extra shadows or borders.
- The highlight slides (250ms, strong ease-out); the variant swap stays instant. The highlight's width transition is a deliberate exception to the transform/opacity rule (28px tall, absolute, no layout dependents).
- One allowed modification: if a variant occupies bottom-center (toast stack, bottom sheet, dock), set data-position="top".
- Replay is conditional. Render the replay button and its divider only when a variant has an entrance or state animation to re-trigger.

## Behavior contract

- 1–N and ←/→ switch variants; R replays. Ignore keys when focus is in an input, textarea, select or contenteditable, or a modifier is held.
- Click switches; exactly one item has data-active and aria-current="true"; the highlight slides to it.
- Selection persists via ?v=2, falling back to variant 1. Initial highlight position doesn't animate (data-ready added after first paint).
- Switching re-mounts the variant (entrances re-run); replay re-mounts without switching.

## Reference wiring

Verbatim for standalone HTML. In a framework, same behavior idiomatically: state instead of innerHTML, keyed re-mount instead of requestAnimationFrame, refs + a layout effect for highlight measurement.
