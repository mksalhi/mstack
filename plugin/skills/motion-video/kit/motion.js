// Motion helpers. Every function is a pure function of time, so any frame can be drawn
// without simulating the frames before it. Loaded as a plain script (works from file://).

const clamp = (x, lo = 0, hi = 1) => Math.min(hi, Math.max(lo, x));
const lerp = (a, b, p) => a + (b - a) * p;

// [stiffness, damping] pairs: spread into spring() or track().
const SPRING = {
  snappy: [320, 30], // buttons, toggles, leading edges
  standard: [170, 26], // cards, containers
  heavy: [90, 19], // big type, logo lockups
  playful: [200, 12], // mascots, stickers: visible overshoot
};

// Step response of a unit-mass damped spring: 0 at t <= 0, settles at 1.
function spring(t, stiffness = 170, damping = 26) {
  if (t <= 0) return 0;
  const w0 = Math.sqrt(stiffness);
  const zeta = damping / (2 * w0);
  if (zeta < 1) {
    const wd = w0 * Math.sqrt(1 - zeta * zeta);
    return 1 - Math.exp(-zeta * w0 * t) * (Math.cos(wd * t) + ((zeta * w0) / wd) * Math.sin(wd * t));
  }
  if (zeta === 1) return 1 - Math.exp(-w0 * t) * (1 + w0 * t);
  const root = Math.sqrt(zeta * zeta - 1);
  const r1 = -w0 * (zeta - root);
  const r2 = -w0 * (zeta + root);
  return 1 - (r2 * Math.exp(r1 * t) - r1 * Math.exp(r2 * t)) / (r2 - r1);
}

// A value that changes target several times. keys: [[time, value], ...] sorted by time.
// Each change adds its own spring instead of restarting one, so motion stays continuous.
function track(t, keys, stiffness, damping) {
  let value = keys[0][1];
  for (let i = 1; i < keys.length; i++) {
    value += (keys[i][1] - keys[i - 1][1]) * spring(t - keys[i][0], stiffness, damping);
  }
  return value;
}

// Quintic smootherstep, 0 to 1 over p in [0, 1]: zero velocity and acceleration at both ends.
// Camera and full-frame moves use this instead of a spring, which kicks at the start of the move.
const smoother = (p) => {
  const x = clamp(p);
  return x * x * x * (x * (x * 6 - 15) + 10);
};

// Opacity for content inside a morphing container: appears shortly after the morph at tIn
// starts and is fully gone by tOut, when the next morph begins.
function swapAlpha(t, tIn, tOut, lag = 0.08, fade = 0.12) {
  return clamp(Math.min((t - tIn - lag) / fade, (tOut - t) / fade));
}

// Seeded random numbers (mulberry32). Never use Math.random in a film: renders must repeat exactly.
function rng(seed) {
  return () => {
    seed = (seed + 0x6d2b79f5) | 0;
    let x = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    x = (x + Math.imul(x ^ (x >>> 7), 61 | x)) ^ x;
    return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
  };
}

// Beat times for synthesized music, where the tempo is chosen rather than measured.
function beatGrid(bpm, duration, beatsPerBar = 4) {
  const beats = [];
  for (let i = 0; (i * 60) / bpm < duration; i++) beats.push(Number(((i * 60) / bpm).toFixed(3)));
  return { bpm, beats, downbeats: beats.filter((_, i) => i % beatsPerBar === 0) };
}

// Wrap time for a seamless loop.
const loopT = (t, duration) => ((t % duration) + duration) % duration;

if (typeof module === "object") {
  module.exports = { clamp, lerp, SPRING, spring, track, smoother, swapAlpha, rng, beatGrid, loopT };
  // Self-check: node motion.js
  if (require.main === module) {
    const assert = require("node:assert");
    for (const [name, preset] of Object.entries(SPRING)) {
      assert.equal(spring(0, ...preset), 0, name);
      assert.ok(Math.abs(spring(5, ...preset) - 1) < 1e-3, `${name} settles`);
    }
    assert.ok(Math.abs(spring(5, 100, 40) - 1) < 1e-3, "overdamped settles");
    assert.ok(spring(0.2, 100, 40) > 0 && spring(0.2, 100, 40) < 1, "overdamped never overshoots");
    const keys = [[0, 10], [1, 50], [1.2, 20]];
    assert.equal(track(0.5, keys), 10);
    assert.ok(Math.abs(track(1.2001, keys) - track(1.1999, keys)) < 0.1, "track is continuous across a retarget");
    assert.ok(Math.abs(track(9, keys) - 20) < 1e-3, "track settles on the last value");
    assert.equal(smoother(0), 0);
    assert.equal(smoother(0.5), 0.5);
    assert.equal(smoother(2), 1);
    assert.equal(rng(7)(), rng(7)(), "rng repeats for a seed");
    assert.equal(swapAlpha(0.5, 0, 1), 1);
    assert.equal(swapAlpha(1, 0, 1), 0);
    assert.deepEqual(beatGrid(120, 2).beats, [0, 0.5, 1, 1.5]);
    console.log("motion.js ok");
  }
}
