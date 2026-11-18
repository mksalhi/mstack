# Expo animation recipes

These assume `react-native-reanimated`, `react-native-worklets`, `react-native-gesture-handler` and `expo-haptics`, with `GestureHandlerRootView` at the root `_layout`. They use the `EASE_*` curves from [index.md](index.md).

```js
// Where a flick comes to rest (Apple's exponential decay, not v²/2a)
function project(velocity, rate = 0.998) { 'worklet'; return ((velocity / 1000) * rate) / (1 - rate); }
// Resistance past an edge
function rubberband(over, dim, c = 0.55) { 'worklet'; return (over * dim * c) / (dim + c * Math.abs(over)); }
```

## Press feedback

Use a CSS transition and `setState`, not a shared value; it only changes twice per press.

```jsx
<Pressable onPressIn={() => setPressed(true)} onPressOut={() => setPressed(false)} hitSlop={12} pressRetentionOffset={16}>
  <Animated.View style={[{ transitionProperty: 'transform', transitionDuration: '120ms',
    transitionTimingFunction: 'cubic-bezier(0.23, 1, 0.32, 1)' }, { transform: [{ scale: pressed ? 0.97 : 1 }] }]} />
</Pressable>
```

## Drag-to-dismiss sheet

Build this only for a sheet inside a screen. If the sheet is its own destination, use `presentation: 'formSheet'`.

```jsx
const pan = useMemo(() => Gesture.Pan().activeOffsetY([-10, 10])
  .onStart(() => { context.set(translateY.get()); })              // no teleport when grabbed mid-flight
  .onUpdate((e) => { const n = context.get() + e.translationY; translateY.set(n >= 0 ? n : rubberband(n, HEIGHT)); })
  .onEnd((e) => {
    if (translateY.get() + project(e.velocityY) > HEIGHT * 0.4) {   // projected, not raw distance
      translateY.set(withSpring(HEIGHT, { duration: 300, dampingRatio: 1, velocity: e.velocityY, overshootClamping: true },
        (done) => { if (done) scheduleOnRN(onClose); }));
    } else {
      translateY.set(withSpring(0, { duration: 300, dampingRatio: 0.8, velocity: e.velocityY }));
      scheduleOnRN(Haptics.impactAsync, Haptics.ImpactFeedbackStyle.Light);
    }
  }), [onClose]);
```

Fade the backdrop with `interpolate(translateY, [0, HEIGHT], [1, 0], Extrapolation.CLAMP)`.

## Swipe to delete

For buttons revealed by a swipe, use `ReanimatedSwipeable`. Build this only for swipe-to-commit:

- Set `activeOffsetX([-10, 10])`, or the row steals vertical scroll.
- Clamp the translation to ≤ 0.
- On end, if `x + project(vx)` passes the threshold, run a 200ms `EASE_OUT` timing to `-WIDTH` and then `onDelete`. Otherwise spring back with `dampingRatio: 1`.
- Let the list close the gap with `itemLayoutAnimation={LinearTransition.duration(200)}`, defined at module scope.

## Collapsing header

Use `useAnimatedScrollHandler` to write `scrollY`, then interpolate opacity and `translateY` over 0 to 60 with `Extrapolation.CLAMP`. Set `scrollEventThrottle={16}`. Never animate the header's height: keep a fixed container with `overflow: 'hidden'` and translate its content.

## List entrances

`entering={useMemo(() => FadeInDown.duration(250).delay(index * 40), [index])}`. Build layout animations at module scope or in `useMemo`, never inline. **Never put `entering` on a row of a FlatList, FlashList or any other virtualized list**, because it fires again on recycle. Animate the container once instead.

## Keyboard

Wrap the root in `<KeyboardProvider>`; without it the hooks do nothing. `const { height } = useReanimatedKeyboardAnimation()`, then use `translateY: height.get()` on the footer. Never use `Keyboard.addListener` with a timing animation, because it drifts out of sync with the keyboard.

## Tab indicator

Measure the tabs with `onLayout` once. Then animate `x` and `width` with `withTiming(…, { duration: 250, easing: EASE_IN_OUT })`; animating width is allowed here because the pill is absolute and has no children. Fire `Haptics.selectionAsync()` on press, not when the pill lands.

## Screen transitions

```jsx
<Stack screenOptions={{ animation: reduced ? 'fade' : 'default' }}>
  <Stack.Screen name="compose" options={{ presentation: 'modal' }} />
  <Stack.Screen name="filter" options={{ presentation: 'formSheet', sheetAllowedDetents: 'fitToContents', sheetGrabberVisible: true }} />
</Stack>
```

- Going deeper uses `default`; a task the user can abandon uses `modal`; a short interruption uses `formSheet`; tab switches use `none`.
- Set `animationMatchesGesture: true` whenever you set a custom animation.
- Form sheets on Android allow at most three detents, have no grabber, and can't host a header or a nested stack.
- `fitToContents` needs content with an explicit size.

## Toast

`FadeInDown.duration(300).easing(EASE_OUT)` in, `FadeOutDown.duration(250)` out, both at module scope. Position with `bottom: insets.bottom + 16`. Mobile has no 400ms toast exemption.

## Firing once at a threshold

```jsx
useAnimatedReaction(() => pull.get() > THRESHOLD, (armed, was) => {
  if (armed !== was) scheduleOnRN(Haptics.impactAsync, Haptics.ImpactFeedbackStyle.Light);
});
```
