# Animation in Expo and React Native

- No hover. Two runtimes: keep motion on UI runtime (worklets). Finger on element: support interruption and velocity handoff.
- Use Reanimated 4; never core `Animated`. Judge feel on a release build on the slowest supported device.
- Open [RECIPES.md](RECIPES.md) when building a drag-to-dismiss sheet, swipe to delete, collapsing header, list entrance, keyboard-following footer, tab indicator, screen transition, toast or threshold haptic.
- Worst failures: animating what shouldn’t move; running on the wrong thread.

## 1) Should it animate?
- 100+/day: platform default or none. Tabs never slide (`animation: 'none'`).
- Tens/day: ≤150ms or none. Occasional: standard. Rare: only with clear purpose.

## 2) Tool
- State change, no gesture: Reanimated CSS transition (`transitionProperty`).
- Loop/on mount: Reanimated CSS animation (`animationName`).
- Mount/unmount/list reflow: `entering`, `exiting`, `itemLayoutAnimation`.
- Finger/scroll-driven: `useSharedValue` + `Gesture` + `useAnimatedStyle`.
- Screen moves/sheet-as-screen: Expo Router native stack options, or `presentation: 'formSheet'`. Never rebuild these in JS.
- Tab bar, context menu, large-title header: `NativeTabs`, `Link.Menu` / `Link.Preview`, `headerLargeTitleEnabled`.
- Pull to refresh: `RefreshControl`. Keyboard-following UI: `react-native-keyboard-controller`.
- Illustration: Lottie (never for UI state). Huge scene/custom drawing: Skia.

## 3) Properties and timing
- Only `transform` and `opacity` are cheap. Layout props re-run Yoga; only absolutely positioned, no-children may animate `width` (avoid `scaleX` smearing).
- No `scale(0)`. Order transforms: `translate` before `scale`. Don’t animate `BlurView` intensity or Android `elevation`; crossfade a static layer.
- Finger → spring; otherwise timing. Springs use `{ duration, dampingRatio, velocity }`. Defaults: settle `{ duration: 400, dampingRatio: 1 }`; snap-back `{ duration: 300, dampingRatio: 0.8, velocity }`; sheet `{ duration: 300, dampingRatio: 0.8, velocity }`. Add `overshootClamping` at hard edges.
- Curves: `Easing.bezier(0.23, 1, 0.32, 1)` (UI), `(0.77, 0, 0.175, 1)` (movement), `(0.32, 0.72, 0, 1)` (sheets). Never `Easing.in`.
- Durations: press 100–150ms; toggle 150–200ms; keep UI ≤300ms; leave screen transitions at platform default.

## 4) Threads
- Never `setState` from a gesture or scroll handler.
- Never call `scheduleOnRN` per frame; prefer `onEnd` or a `useAnimatedReaction` on threshold crossing.
- Never read or write a shared value during render. Use `.get()`/`.set()`, not `.value`.
- Any function a worklet calls needs `'worklet'` as its first line.
- Build gestures inside `useMemo` (rebuilding drops drags).
- Gesture Handler v3: hooks (`usePanGesture({...})`), `onStart`→`onActivate`, `onEnd`→`onDeactivate`.

## 5) Press, haptics, accessibility
- Press: feedback on press-in; commit on press-out; `scale(0.97)`. Use `hitSlop` (reach 44pt/48dp) and `pressRetentionOffset`. Android ripple only in Material apps.
- Haptics: one per action, same frame. `selectionAsync`; `impactAsync(Light|Medium)`; `notificationAsync`.
- Reduced motion: `useReducedMotion()` or `reduceMotion: ReduceMotion.System`. Drop translation/scale/overshoot; keep opacity; screens use `animation: 'fade'`.
- Text scales with system; never animate to a hardcoded height.

## When nothing animates
- Worklets Babel plugin missing (last in bare RN); `babel-preset-expo` adds it.
- `GestureHandlerRootView` not wrapping the app.
- New Architecture off; Reanimated 4 requires it.
- On ProMotion iPhones, cap at 60fps unless `CADisableMinimumFrameDurationOnPhone` is `true` in `ios.infoPlist`.

## Never ship
- `PanResponder`
- `setState` per frame
- `runOnJS`
- Core `Animated` on anything a finger touches
- Animated layout properties
- `entering` on a virtualized list row
- A screen transition rebuilt in JS
- Tabs that slide
- `Easing.in`
- Dismissing on distance alone
- A hard stop at a boundary
- A haptic per frame
- Judging feel in Expo Go

Write the code, then at most three lines: the frequency tier and purpose; the ingredients and which thread they run on; and a device feel check (flick it, interrupt it, reverse it, try it on a slow Android phone).
