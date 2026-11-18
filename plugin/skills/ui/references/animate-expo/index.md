# Building animations in Expo

Turn a React Native motion request into code that survives strict review on a real device. Mobile differs from web in three ways:

1. No hover. Web hover affordances move to press, position, or nothing.
2. Two runtimes (Worklets, Reanimated 4): the React Native runtime (React, app logic) and the UI runtime (worklets, every frame). Motion that touches the RN runtime stutters when the app is busy. Keep motion on the UI runtime.
3. The finger is on the element: interruptibility and velocity handoff are baseline.

## Hard rules

- Animating something that shouldn't animate is the worst failure; zero lines is a valid outcome. Next worst is the wrong thread (`setState` per frame, `PanResponder`, animated `height`).
- Make the call, give the reason in one line, write the code. Never offer a menu of motion options.
- Run the sequence in order. Steps 1 and 2 gate everything.
- Reanimated, not core `Animated` (which can't follow a gesture without the bridge and whose `useNativeDriver` takes only transform and opacity).
- Take curves and spring configs from the tables below. Never approximate.
- Reduced motion ships with the animation.
- Feel is judged only on a release build on the slowest supported device.

## The build sequence

### 1. Should this animate at all?

| Frequency | Decision |
| --- | --- |
| 100+ times/day: tab switches, keyboard open/close, scrolling, settings toggles | No animation. Platform default or nothing. Stop. |
| Tens of times/day: press feedback, list navigation, row selection | Under 150ms, or nothing |
| Occasional: sheets, modals, toasts, onboarding steps | Standard animation |
| Rare / first-time: success, empty-state illustration, celebration | Delight budget lives here |

Tab switches never slide (tabs are peers): `animation: 'none'`. If the request fails the gate, say so and don't write it.

### 2. What is the purpose?

Name one: **feedback**, **spatial consistency**, **state indication**, **preventing a jarring change**, **explanation**, **delight** (rare tier only). Can't name it? Don't build it.

### 3. Pick the tool (stop at the first that fits)

| Need | Tool |
| --- | --- |
| State-driven change, no gesture (press, toggle, color) | Reanimated CSS transition (`transitionProperty`) |
| Loop, multi-stage, or plays on mount | Reanimated CSS animation (`animationName` keyframes) |
| Mount/unmount, list reflow | Layout animations (`entering` / `exiting` / `itemLayoutAnimation`) |
| Anything a finger touches or derived from scroll | `useSharedValue` + `Gesture` + `useAnimatedStyle` |
| Screen to screen | Native stack options in Expo Router. Never hand-roll |
| Bottom sheet that is its own screen | `presentation: 'formSheet'` |
| Tab bar | `NativeTabs` (`expo-router/unstable-native-tabs`) |
| Context menu, press-and-hold preview | `Link.Menu` / `Link.Preview` (Expo Router, iOS-only); never rebuilt in JS |
| Collapsing large-title header | `headerLargeTitleEnabled` on the native stack (iOS-only; `headerLargeTitle` is deprecated), not a scroll worklet |
| Pull to refresh | `RefreshControl`; hand-roll only for a signature interaction (threshold recipe) |
| UI tracking the keyboard | `react-native-keyboard-controller` |
| Illustration, celebration, empty state | Lottie (never for UI state) |
| Huge animated scene, freeform drawing | `@shopify/react-native-skia` (when the view hierarchy is the bottleneck) |

Shared values only for continuous or interruptible values; a press scale or two-state toggle is a CSS transition.

Install with `npx expo install <package>` (matches the SDK):

| Need | Package |
| --- | --- |
| Animation | `react-native-reanimated` + `react-native-worklets` |
| Gestures | `react-native-gesture-handler` |
| Navigation, sheets, native tabs, menus | `expo-router` |
| Haptics | `expo-haptics` |
| Keyboard-following UI | `react-native-keyboard-controller` (`KeyboardProvider` at the root) |
| Illustration | `lottie-react-native` |
| Large scenes, custom drawing | `@shopify/react-native-skia` |

### 4. Pick the properties

- Only `transform` and `opacity` are free. `width`, `height`, `margin`, `padding`, `flex`, `top`, `left`, `gap` re-run Yoga every frame for the node and its siblings.
- Exception: an absolutely positioned element with no children (tab pill, progress fill) may animate `width`, which keeps the corner radius `scaleX` would smear.
- Never `scale(0)`. Start from `scale(0.9–0.97)` + `opacity: 0`.
- `transform` order matters: keep `[{ translateY }, { scale }]` (translate first) unless you want the translate scaled.
- Don't animate Android `elevation` or `BlurView` intensity (re-rendered every frame). Crossfade the opacity of a static pre-shadowed or blurred layer.
- Percentage `translateY('100%')` moves by the element's own height.

### 5. Timing or spring

If a finger was involved, use a spring (carries velocity through interruption); otherwise timing. Use Reanimated's duration/dampingRatio form, not mass/stiffness/damping:

| Interaction | Config |
| --- | --- |
| Default settle, no overshoot | `{ duration: 400, dampingRatio: 1 }` |
| Reposition / snap back after a drag | `{ duration: 400, dampingRatio: 0.8, velocity }` |
| Sheet, drawer | `{ duration: 300, dampingRatio: 0.8, velocity }` |
| Must not pass a hard edge | add `overshootClamping: true` |

Bounce only when the gesture carried momentum.

| Situation | Easing |
| --- | --- |
| Entering or exiting (and default) | `ease-out` |
| Moving / morphing on screen | `ease-in-out` |
| Constant motion (progress, marquee) | `linear` |

Never `ease-in` on UI. Built-ins are too weak; use:

```js
import { Easing } from 'react-native-reanimated';
const EASE_OUT = Easing.bezier(0.23, 1, 0.32, 1);      // UI
const EASE_IN_OUT = Easing.bezier(0.77, 0, 0.175, 1);  // on-screen movement
const EASE_SHEET = Easing.bezier(0.32, 0.72, 0, 1);    // iOS sheet
```

| Element | Duration |
| --- | --- |
| Press feedback | 100–150ms |
| Toggle, chip, small state change | 150–200ms |
| Sheet, modal, drawer | spring, ~300ms perceived |
| Screen transition | platform default; don't override |

UI animations stay under 300ms. Match the platform for navigation (iOS push is 350ms), beat it elsewhere.

### 6. Keep it off the JS thread

- Never `setState` from a gesture or scroll handler. Shared value → `useAnimatedStyle`.
- Never call `scheduleOnRN(fn, ...args)` (from `react-native-worklets`; replaces deprecated `runOnJS(fn)(...args)`) inside `onUpdate` or a scroll handler. Put it in `onEnd` or a `useAnimatedReaction` that fires at a threshold.
- Never read (`translateY.get()` in JSX) or write a shared value during render. Touch shared values only in worklets, handlers and effects.
- Use `.get()` / `.set()`, not `.value` (React Compiler safe). `sv.set((v) => v + 1)` works.
- Functions called from a worklet need `'worklet'` as their first line, or they throw on device while working in the debugger.

### 7. Press, not hover

- Feedback on press-in, commit on press-out.
- `scale: 0.97` in 100–150ms on any pressable (`Pressable` + CSS transition).
- 44×44pt minimum touch target (48dp Android). Add `hitSlop`; don't grow the visual.
- Set `pressRetentionOffset` so a drifting finger doesn't cancel a press.
- Android ripple only in a Material-styled app; otherwise the same scale on both platforms.

### 8. Haptics

| Moment | Call |
| --- | --- |
| Value ticks past a step (picker, slider detent, segmented control) | `Haptics.selectionAsync()` |
| Snap home, sheet detent catches, drag commits | `Haptics.impactAsync(ImpactFeedbackStyle.Light)` |
| Heavy landing, destructive action fires | `Haptics.impactAsync(ImpactFeedbackStyle.Medium)` |
| Operation succeeded or failed | `Haptics.notificationAsync(NotificationFeedbackType.Success / Error)` |

Absolute rules:

- Same frame as the visual, at the causal moment (the detent catching), not when the animation ends.
- One per user action. Never on scroll, per frame, or on an entrance the user didn't cause.
- Never the only feedback (often disabled, silent on most Android hardware).
- From a worklet: `scheduleOnRN(Haptics.selectionAsync)`.

### 9. Reduced motion and accessibility

```jsx
import { useReducedMotion, ReduceMotion, withSpring } from 'react-native-reanimated';
const reduced = useReducedMotion();
const y = useSharedValue(reduced ? 0 : SHEET_HEIGHT);
withSpring(0, { duration: 300, dampingRatio: 0.8, reduceMotion: ReduceMotion.System });
```

Fewer and gentler, not zero: keep opacity and color that explain a state change; drop translation, scale, parallax and overshoot. Screen transitions become `animation: 'fade'`. Text scales (`allowFontScaling` on by default), so never animate to a hardcoded height; measure with `onLayout` or animate a transform.

## Setup that silently breaks motion

Check first when an animation doesn't run:

- `npx expo install react-native-reanimated react-native-worklets`. `babel-preset-expo` adds the worklets Babel plugin; only bare RN without that preset adds it manually, last in the list. Missing or misplaced throws `Failed to create a worklet`.
- `GestureHandlerRootView` must wrap the app, or gestures silently do nothing.
- Reanimated 4 requires the New Architecture.
- Never judge feel in Expo Go or a dev build; use a release build.

## 120fps

ProMotion iPhones cap third-party animation at 60fps unless `CADisableMinimumFrameDurationOnPhone` is set. Recent SDKs set it; confirm, and add if missing:

```json
{ "expo": { "ios": { "infoPlist": { "CADisableMinimumFrameDurationOnPhone": true } } } }
```

Frame budget is then 8ms.

## Recipes

When the request matches press feedback, drag-to-dismiss sheet, swipe-to-delete, collapsing header, list entrances, keyboard-synced UI, tab indicator, or screen transitions, load [RECIPES.md](RECIPES.md) and start from the recipe.

## Never ship

| Never | Instead |
| --- | --- |
| `PanResponder` | `Gesture.Pan()` from gesture-handler |
| `setState` in a gesture or scroll handler | shared value + `useAnimatedStyle` |
| `runOnJS` (deprecated in Reanimated 4) | `scheduleOnRN` from `react-native-worklets` |
| `scheduleOnRN` per frame | `onEnd`, or `useAnimatedReaction` at a threshold |
| Reading or writing a shared value during render | `.get()` / `.set()` in worklets, handlers, effects |
| Core `Animated` for anything a finger touches | Reanimated |
| Animating `height` / `width` / `margin` / `flex` / `top` | `transform` + `opacity` (absolute, childless elements exempt) |
| Animating `BlurView` intensity or Android `elevation` | crossfade a static layer |
| `entering` on a virtualized list row | animate the container, or `itemLayoutAnimation` |
| A screen transition rebuilt in JS | native stack `animation` |
| Sliding between tabs | `animation: 'none'` |
| `Easing.in(...)` on a UI element | `Easing.bezier(0.23, 1, 0.32, 1)` |
| `scale(0)` entrance | `scale(0.95)` + `opacity: 0` |
| Distance-only dismissal threshold | velocity **or** distance |
| Hard stop at a boundary | rubber-band resistance |
| A haptic per frame, or as the only feedback | one per commit, paired with a visual |
| Judging feel in Expo Go or the simulator | release build, slowest supported device |

## Output

Write the code, then at most a few lines:

- **Gate result**: frequency tier and named purpose; what you rejected and why.
- **Ingredients**: tool, properties, spring or curve + duration, thread.
- **Feel-check on device**: flick it, interrupt it mid-flight, reverse it, run it on the slowest Android available. Gestures, velocity handoff and haptic timing can't be judged from code.

No report. When the answer is "this shouldn't animate" or "this needs a real device first", say so.
