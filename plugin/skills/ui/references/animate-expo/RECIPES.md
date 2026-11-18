# Expo animation recipes

Start from the recipe, then adapt.

## Setup the recipes assume

```bash
npx expo install react-native-reanimated react-native-worklets react-native-gesture-handler expo-haptics
```

(`react-native-keyboard-controller` only for the keyboard recipe.) `babel-preset-expo` configures the worklets plugin. Wrap the root `_layout` once:

```jsx
<GestureHandlerRootView style={{ flex: 1 }}><Stack /></GestureHandlerRootView>
```

Shared imports and constants:

```js
import { useState, useEffect, useMemo } from 'react';
import Animated, {
  useSharedValue, useAnimatedStyle, useAnimatedScrollHandler, useAnimatedReaction,
  withSpring, withTiming, interpolate, Extrapolation, Easing,
  FadeInDown, FadeOutDown, LinearTransition,
} from 'react-native-reanimated';
import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import { scheduleOnRN } from 'react-native-worklets';
import * as Haptics from 'expo-haptics';

const EASE_OUT = Easing.bezier(0.23, 1, 0.32, 1);
const EASE_IN_OUT = Easing.bezier(0.77, 0, 0.175, 1);
const EASE_SHEET = Easing.bezier(0.32, 0.72, 0, 1);
```

Conventions: shared values via `.get()` / `.set()`; `scheduleOnRN(fn, ...args)` instead of deprecated `runOnJS(fn)(...args)`; gestures wrapped in `useMemo` (rebuilding can drop a mid-flight drag).

**Gesture Handler v3** (Expo installs v2; recipes use `Gesture.Pan()`): on v3 each gesture is a hook with one config object, `onStart` → `onActivate`, `onEnd` → `onDeactivate`, `success` replaced by inverted `event.canceled`, no `useMemo`:

```jsx
const pan = usePanGesture({
  activeOffsetY: [-10, 10],
  onActivate: () => { context.set(translateY.get()); },
  onUpdate: (e) => { translateY.set(context.get() + e.translationY); },
  onDeactivate: (e) => { /* settle with withSpring */ },
});
```

## Two worklets you'll need everywhere

```js
// Where a flick would come to rest (Apple's exponential decay, not v²/2a).
function project(velocity, decelerationRate = 0.998) {
  'worklet';
  return ((velocity / 1000) * decelerationRate) / (1 - decelerationRate);
}
// Past the edge, the element follows less.
function rubberband(overshoot, dimension, constant = 0.55) {
  'worklet';
  return (overshoot * dimension * constant) / (dimension + constant * Math.abs(overshoot));
}
```

## Press feedback

120ms and 3% scale is the ceiling for something touched this often. CSS transition, no shared value; `setState` is fine (twice per press).

```jsx
<Pressable onPress={onPress} onPressIn={() => setPressed(true)} onPressOut={() => setPressed(false)}
  hitSlop={12} pressRetentionOffset={16}>
  <Animated.View style={[styles.box, pressed && styles.pressed]}>{children}</Animated.View>
</Pressable>

const styles = StyleSheet.create({
  box: {
    transform: [{ scale: 1 }],
    transitionProperty: 'transform',
    transitionDuration: '120ms',
    transitionTimingFunction: 'cubic-bezier(0.23, 1, 0.32, 1)',
  },
  pressed: { transform: [{ scale: 0.97 }] },
});
```

## Bottom sheet you can drag to dismiss

If the sheet is its own destination, use `presentation: 'formSheet'` instead. Build this only for a sheet inside an existing screen.

```jsx
const translateY = useSharedValue(0);
const context = useSharedValue(0);

const pan = useMemo(() => Gesture.Pan()
  .activeOffsetY([-10, 10])
  .onStart(() => { context.set(translateY.get()); })   // continue from current value
  .onUpdate((e) => {
    const next = context.get() + e.translationY;
    translateY.set(next >= 0 ? next : rubberband(next, HEIGHT));
  })
  .onEnd((e) => {
    const projected = translateY.get() + project(e.velocityY);
    if (projected > HEIGHT * 0.4) {
      translateY.set(withSpring(HEIGHT, {
        duration: 300, dampingRatio: 1, velocity: e.velocityY, overshootClamping: true,
      }, (finished) => { if (finished) scheduleOnRN(onClose); }));
    } else {
      translateY.set(withSpring(0, { duration: 300, dampingRatio: 0.8, velocity: e.velocityY }));
      scheduleOnRN(Haptics.impactAsync, Haptics.ImpactFeedbackStyle.Light);
    }
  }), [onClose]);

const sheetStyle = useAnimatedStyle(() => ({ transform: [{ translateY: translateY.get() }] }));
const backdropStyle = useAnimatedStyle(() => ({
  opacity: interpolate(translateY.get(), [0, HEIGHT], [1, 0], Extrapolation.CLAMP),
}));
```

Must-haves: `onStart` captures the current value (no teleport when grabbed mid-animation); projected velocity decides, not raw distance; velocity is handed to the spring; `overshootClamping` on dismissal (no gap flash).

## Swipe to delete a row

For swipe-to-reveal action buttons use gesture-handler's [`ReanimatedSwipeable`](https://docs.swmansion.com/react-native-gesture-handler/docs/components/reanimated_swipeable/). Build this only for swipe-to-commit with momentum.

```jsx
const pan = useMemo(() => Gesture.Pan()
  .activeOffsetX([-10, 10])   // declare the axis or it steals vertical scroll
  .onStart(() => { context.set(x.get()); })
  .onUpdate((e) => { x.set(Math.min(0, context.get() + e.translationX)); })
  .onEnd((e) => {
    if (x.get() + project(e.velocityX) < -SWIPE_THRESHOLD) {
      x.set(withTiming(-WIDTH, { duration: 200, easing: EASE_OUT }, (f) => {
        if (f) scheduleOnRN(onDelete, id);
      }));
    } else {
      x.set(withSpring(0, { duration: 300, dampingRatio: 1, velocity: e.velocityX }));
    }
  }), [onDelete, id]);

const ROW_CLOSE = LinearTransition.duration(200);   // module scope
<Animated.FlatList data={items} itemLayoutAnimation={ROW_CLOSE} ... />   // the list closes the gap
```

## Collapsing header on scroll

```jsx
const scrollY = useSharedValue(0);
const onScroll = useAnimatedScrollHandler((e) => { scrollY.set(e.contentOffset.y); });
const titleStyle = useAnimatedStyle(() => ({
  opacity: interpolate(scrollY.get(), [0, 60], [1, 0], Extrapolation.CLAMP),
  transform: [{ translateY: interpolate(scrollY.get(), [0, 60], [0, -12], Extrapolation.CLAMP) }],
}));
<Animated.ScrollView onScroll={onScroll} scrollEventThrottle={16}>
```

Never animate header `height`. Fixed-height container, translate the content, `overflow: 'hidden'`. `Extrapolation.CLAMP` is required.

## List entrances

```jsx
function Row({ item, index }) {
  const entering = useMemo(() => FadeInDown.duration(250).delay(index * 40), [index]);
  return <Animated.View entering={entering}>{/* ... */}</Animated.View>;
}
```

Build layout animations at module scope or in `useMemo`, never inline. Stagger 30–80ms. Never `entering` on a row in `FlatList`, `FlashList` or any virtualized list (re-fires on recycle); animate the container once or use `itemLayoutAnimation` for reflow. Entrances only for content the user is waiting on.

## Keyboard-synced UI

```bash
npx expo install react-native-keyboard-controller
```

Wrap the root `_layout` in `<KeyboardProvider>` next to `GestureHandlerRootView` ([Expo keyboard guide](https://docs.expo.dev/guides/keyboard-handling/)); the hooks do nothing without it.

```jsx
import { useReanimatedKeyboardAnimation } from 'react-native-keyboard-controller';
const { height } = useReanimatedKeyboardAnimation();   // 0 → -keyboardHeight, UI thread
const footerStyle = useAnimatedStyle(() => ({ transform: [{ translateY: height.get() }] }));
```

Never `Keyboard.addListener` plus a timing animation; it lags or leads the keyboard.

## Tab / segmented indicator

Measure with `onLayout` once, then animate:

```jsx
useEffect(() => {
  const l = layouts[active];
  if (!l) return;
  x.set(withTiming(l.x, { duration: 250, easing: EASE_IN_OUT }));
  w.set(withTiming(l.width, { duration: 250, easing: EASE_IN_OUT }));
}, [active, layouts]);
const pillStyle = useAnimatedStyle(() => ({ transform: [{ translateX: x.get() }], width: w.get() }));
```

Sanctioned `width` animation (absolute, childless pill; `scaleX` smears corners). Fire `Haptics.selectionAsync()` on press, not on landing.

## Screen transitions (Expo Router)

Configure the native stack; never rebuild in JS.

```jsx
<Stack screenOptions={{ animation: reduced ? 'fade' : 'default' }}>
  <Stack.Screen name="settings" options={{ animation: 'slide_from_right', animationMatchesGesture: true }} />
  <Stack.Screen name="compose" options={{ presentation: 'modal' }} />
  <Stack.Screen name="filter" options={{
    presentation: 'formSheet', sheetAllowedDetents: 'fitToContents', sheetGrabberVisible: true,
  }} />
</Stack>
```

| Navigation | Option |
| --- | --- |
| Deeper into a hierarchy | `animation: 'default'` |
| Self-contained task the user can abandon | `presentation: 'modal'` |
| Short interruption: picker, filter, share | `presentation: 'formSheet'` with detents |
| Between tabs | `animation: 'none'` |
| Reduced motion | `animation: 'fade'` |

Set `animationMatchesGesture: true` whenever you set a custom `animation`. `formSheet` differences ([Expo modal docs](https://docs.expo.dev/router/advanced/modals/#form-sheet-presentation)):

- Android caps detents at three; design for three.
- `sheetGrabberVisible` is iOS-only; not the only drag affordance.
- Android form sheets can't host native headers or nested stacks; use `presentation: 'modal'` if it needs navigation.
- `fitToContents` needs explicitly sized content (not a `flex: 1` root).

## Toast

```jsx
const TOAST_ENTER = FadeInDown.duration(300).easing(EASE_OUT);   // module scope
const TOAST_EXIT = FadeOutDown.duration(250).easing(EASE_OUT);
<Animated.View entering={TOAST_ENTER} exiting={TOAST_EXIT}
  style={{ position: 'absolute', bottom: insets.bottom + 16, left: 16, right: 16 }} />
```

300ms cap holds (no toast exemption on mobile). Exit the way it entered, ~20% faster. Always use safe-area insets. Stacked toasts: add `itemLayoutAnimation`, tune opacity against reflow by eye, recheck the next day.

## Firing something once at a threshold

For detents, snaps, pull-to-refresh arming:

```jsx
useAnimatedReaction(
  () => pullDistance.get() > REFRESH_THRESHOLD,
  (isArmed, wasArmed) => {
    if (isArmed !== wasArmed) {
      armed.set(isArmed);
      scheduleOnRN(Haptics.impactAsync, Haptics.ImpactFeedbackStyle.Light);
    }
  }
);
```

The comparison runs on the UI thread; the JS call fires only on crossing.
