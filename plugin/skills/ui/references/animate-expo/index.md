# Animation in Expo and React Native

Mobile differs from web in three ways:

1. **There's no hover.**
2. **There are two runtimes.** Motion has to stay on the UI runtime (worklets), or it stutters whenever JS is busy.
3. **The finger is on the element**, so interruption and handing off velocity are the baseline.

Use Reanimated 4, never core `Animated`. Judge feel only on a release build on the slowest supported device. For press feedback, draggable sheets, swipe rows, collapsing headers, list entrances, keyboard-following UI, tab indicators, screen transitions, toasts or threshold haptics, start from [RECIPES.md](RECIPES.md).

**The worst failure is animating something that shouldn't move; the next is running it on the wrong thread.**

## 1. Should it animate?

| How often | Decision |
|---|---|
| 100+ times a day: tab switches, the keyboard, scrolling, toggles | The platform default or nothing. Tabs never slide (`animation: 'none'`). |
| Tens of times a day: press, selection | Under 150ms, or nothing |
| Occasionally: sheets, modals, toasts | Standard |
| Rarely: success, empty states | This is where delight goes |

If you can't name a purpose (feedback, orientation, state, explanation), don't build it.

## 2. Tool

| Need | Tool |
|---|---|
| A state change with no gesture | Reanimated CSS transition (`transitionProperty`) |
| A loop, or plays on mount | Reanimated CSS animation (`animationName`) |
| Mount, unmount, list reflow | `entering`, `exiting`, `itemLayoutAnimation` |
| A finger or scroll drives it | `useSharedValue` with `Gesture` and `useAnimatedStyle` |
| Moving between screens, or a sheet that is its own screen | Expo Router native stack options, or `presentation: 'formSheet'`. Never rebuild these in JS. |
| Tab bar, context menu, large-title header | `NativeTabs`, `Link.Menu` / `Link.Preview`, `headerLargeTitleEnabled` |
| Pull to refresh | `RefreshControl` |
| UI that follows the keyboard | `react-native-keyboard-controller` |
| Illustration | Lottie, never for UI state |
| A huge scene or custom drawing | Skia |

Install with `npx expo install`.

## 3. Properties and timing

- **Only `transform` and `opacity` are cheap.** Layout properties re-run Yoga on the node and its siblings every frame. An absolutely positioned element with no children (a tab pill, a progress fill) may animate `width`, because `scaleX` smears its corners.
- **No `scale(0)`. Keep `translate` before `scale` in the transform array.** Don't animate `BlurView` intensity or Android `elevation`; crossfade a static layer instead.
- **If a finger was involved, use a spring; otherwise use timing.** Write springs in the duration/dampingRatio form:
  - Settle: `{ duration: 400, dampingRatio: 1 }`.
  - Snap back after a drag: `0.8` plus the gesture's `velocity`.
  - Sheet: `{ duration: 300, dampingRatio: 0.8, velocity }`.
  - At a hard edge, add `overshootClamping`.
- **Curves** are the same as on web: `Easing.bezier(0.23, 1, 0.32, 1)` for UI, `(0.77, 0, 0.175, 1)` for movement on screen, `(0.32, 0.72, 0, 1)` for sheets. Never `Easing.in`.
- **Durations.** Press: 100 to 150ms. Toggle: 150 to 200ms. Keep UI under 300ms, and leave screen transitions at the platform default.

## 4. Threads

- Never `setState` from a gesture or scroll handler.
- Never call `scheduleOnRN` (which replaces the deprecated `runOnJS`) per frame. Call it in `onEnd`, or in a `useAnimatedReaction` that fires on a threshold crossing.
- Never read or write a shared value during render. Use `.get()` and `.set()`, not `.value`.
- Any function a worklet calls needs `'worklet'` as its first line. Without it, it works in the debugger and throws on device.
- Build gestures inside `useMemo`, because rebuilding drops a drag in flight.
- In Gesture Handler v3, gestures are hooks (`usePanGesture({...})`), `onStart` becomes `onActivate` and `onEnd` becomes `onDeactivate`.

## 5. Press, haptics, accessibility

- **Press.** Give feedback on press-in and commit on press-out, with `scale(0.97)`. Use `hitSlop` to reach 44pt (48dp on Android) and `pressRetentionOffset` so a drifting finger doesn't cancel. Use the Android ripple only in a Material app.
- **Haptics.** Fire one per user action, in the same frame as the cause, never as the only feedback:
  - `selectionAsync` for stepping through values.
  - `impactAsync(Light)` for a snap or commit.
  - `impactAsync(Medium)` for a destructive action.
  - `notificationAsync` for success or failure.
- **Reduced motion.** Check `useReducedMotion()` or pass `reduceMotion: ReduceMotion.System`. Drop translation, scale and overshoot, but keep opacity, and use `animation: 'fade'` for screens.
- **Text scaling.** Text scales with the system setting, so never animate to a hardcoded height.

## When nothing animates

- The worklets Babel plugin is missing. `babel-preset-expo` adds it; in bare React Native it must be the last plugin.
- `GestureHandlerRootView` doesn't wrap the app, so gestures silently do nothing.
- The New Architecture is off; Reanimated 4 requires it.
- On ProMotion iPhones, motion is capped at 60fps unless `CADisableMinimumFrameDurationOnPhone` is `true` in `ios.infoPlist`.

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
- Dismissing on distance alone, rather than velocity or distance
- A hard stop at a boundary instead of rubber-banding
- A haptic per frame
- Judging feel in Expo Go

Write the code, then at most three lines: the frequency tier and purpose, the ingredients and which thread they run on, and a device feel check (flick it, interrupt it, reverse it, try it on a slow Android phone).
