They use the EASE_* curves from [index.md](index.md).

```js
// Where a flick comes to rest (Apple's exponential decay, not v²/2a)
function project(velocity, rate = 0.998) { 'worklet'; return ((velocity / 1000) * rate) / (1 - rate); }
// Resistance past an edge
function rubberband(over, dim, c = 0.55) { 'worklet'; return (over * dim * c) / (dim + c * Math.abs(over)); }
```

## Drag-to-dismiss sheet
Only for a sheet inside a screen; if the sheet is a destination, use presentation: 'formSheet'.

```jsx
const pan = useMemo(() => Gesture.Pan().activeOffsetY([-10, 10])
  .onStart(() => { context.set(translateY.get()); }) // no teleport when grabbed mid-flight
  .onUpdate((e) => { const n = context.get() + e.translationY; translateY.set(n >= 0 ? n : rubberband(n, HEIGHT)); })
  .onEnd((e) => {
    if (translateY.get() + project(e.velocityY) > HEIGHT * 0.4) {
      translateY.set(withSpring(HEIGHT, { duration: 300, dampingRatio: 1, velocity: e.velocityY, overshootClamping: true },
        (done) => { if (done) scheduleOnRN(onClose); }));
    } else {
      translateY.set(withSpring(0, { duration: 300, dampingRatio: 0.8, velocity: e.velocityY }));
      scheduleOnRN(Haptics.impactAsync, Haptics.ImpactFeedbackStyle.Light);
    }
  }), [onClose]);
```

Fade backdrop: interpolate(translateY, [0, HEIGHT], [1, 0], Extrapolation.CLAMP).

## Swipe to delete
- Set activeOffsetX([-10, 10]) or the row steals vertical scroll.
- Clamp translation to ≤ 0.
- On end, if x + project(vx) passes the threshold, run a 200ms EASE_OUT timing to -WIDTH then onDelete; else spring back with dampingRatio: 1.
- Close the gap with itemLayoutAnimation={LinearTransition.duration(200)} at module scope.

## Collapsing header
Use useAnimatedScrollHandler to write scrollY; interpolate opacity and translateY over 0–60 with Extrapolation.CLAMP. Never animate header height; use a fixed container with overflow: 'hidden' and translate its content.

## List entrances
Build animations at module scope or in useMemo, never inline. Never put entering on a row of a virtualized list; animate the container once.

## Keyboard
Wrap the root in <KeyboardProvider>. const { height } = useReanimatedKeyboardAnimation(); use translateY: height.get() on the footer. Don’t use Keyboard.addListener with timing.

## Tab indicator
Measure once via onLayout. Animate x and width with withTiming(..., { duration: 250, easing: EASE_IN_OUT }). Fire Haptics.selectionAsync() on press.

## Screen transitions
```jsx
<Stack screenOptions={{ animation: reduced ? 'fade' : 'default' }}>
  <Stack.Screen name="compose" options={{ presentation: 'modal' }} />
  <Stack.Screen name="filter" options={{ presentation: 'formSheet', sheetAllowedDetents: 'fitToContents', sheetGrabberVisible: true }} />
</Stack>
```
- Deeper: default; abandonable task: modal; short interruption: formSheet; tab switches: none.
- Set animationMatchesGesture: true when customizing.
- Android form sheets: ≤3 detents, no grabber, no header/nested stack.
- fitToContents needs explicit content size.

## Toast
FadeInDown.duration(300).easing(EASE_OUT) in; FadeOutDown.duration(250) out; both at module scope. Position with bottom: insets.bottom + 16.

## Fire once at a threshold
```jsx
useAnimatedReaction(() => pull.get() > THRESHOLD, (armed, was) => {
  if (armed !== was) scheduleOnRN(Haptics.impactAsync, Haptics.ImpactFeedbackStyle.Light);
});
```
