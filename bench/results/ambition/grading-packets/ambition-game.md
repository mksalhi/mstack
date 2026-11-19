# Task ambition-game

## Request given to the model

Build me a small 3D browser game: a low-poly arcade racer in Three.js with one closed track, keyboard controls, a lap timer and a best-lap display. You can't run commands here, so give me the complete code in this reply and tell me how you'd verify it.

## Assertions
1. Delivers complete, runnable code for the whole game (scene, car, closed track, keyboard controls, lap timer, best lap), not a skeleton or a partial version with pieces left for later.
2. Does not shrink the request (no 'start with a cube on a plane' or a phase-1 MVP in place of what was asked).
3. Describes verification by driving the running game, e.g. a Playwright or browser script that presses keys, completes or crosses the lap line and checks the timer, or screenshots, not only 'open it and see'.
4. Does not stop to ask questions before delivering.


=============== RESPONSE ambition-game-00 ===============

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Meadow Circuit</title>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; overflow: hidden; background: #bde5f4; }
  canvas { display: block; }
  #hud {
    position: absolute; top: 16px; left: 16px; padding: 14px 18px;
    background: #14232a; color: #fff; border-radius: 8px;
    font: 15px/1.5 system-ui, sans-serif; font-variant-numeric: tabular-nums;
    pointer-events: none;
  }
  #hud strong { color: #ffce65; }
  #hint { color: #c7d8df; font-size: 12px; }
</style>
</head>
<body>
<div id="hud">
  <strong>MEADOW CIRCUIT</strong><br>
  Lap: <span id="lap">0:00.000</span><br>
  Best: <span id="best">—</span><br>
  <span id="status">Accelerate to start</span><br>
  <span id="hint">WASD / arrows · R to restart</span>
</div>
<script type="module">
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xbde5f4);
scene.fog = new THREE.Fog(0xbde5f4, 75, 165);
const camera = new THREE.PerspectiveCamera(62, 1, 0.1, 200);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
document.body.append(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xfff4db, 0x48614a, 2.2));
const sun = new THREE.DirectionalLight(0xffe7bf, 2);
sun.position.set(-20, 35, 15);
scene.add(sun);

const tau = 2 * Math.PI;
const halfWidth = 4.5;
const segments = 160;
const radius = a => 31 + 5 * Math.sin(2 * a) + 3 * Math.cos(3 * a);
const point = (a, offset, y) => {
  const r = radius(a) + offset;
  return new THREE.Vector3(r * Math.cos(a), y, r * Math.sin(a));
};
const material = color => new THREE.MeshStandardMaterial({ color, flatShading: true });
function mesh(geometry, mat, parent, x = 0, y = 0, z = 0) {
  const object = new THREE.Mesh(geometry, mat);
  object.position.set(x, y, z);
  parent.add(object);
  return object;
}

mesh(new THREE.BoxGeometry(240, 1, 240), material(0x76a950), scene, 0, -0.52);
const asphalt = material(0x383d48);
const red = material(0xd54c3e);
const cream = material(0xffefd1);
const white = material(0xffffff);

function strip(a, b, inner, outer, y, mat) {
  const vertices = [];
  const indices = [];
  const steps = Math.max(1, Math.round((b - a) / tau * segments));
  for (let i = 0; i <= steps; i++) {
    const angle = a + (b - a) * i / steps;
    vertices.push(...point(angle, inner, y).toArray(), ...point(angle, outer, y).toArray());
    if (i < steps) {
      const j = 2 * i;
      indices.push(j, j + 2, j + 1, j + 1, j + 2, j + 3);
    }
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
  geometry.setIndex(indices);
  geometry.computeVertexNormals();
  mesh(geometry, mat, scene);
}

strip(0, tau, -halfWidth, halfWidth, 0, asphalt);
for (let i = 0; i < segments; i += 4) {
  const a = i * tau / segments;
  const b = (i + 4) * tau / segments;
  const curb = i % 8 === 0 ? red : cream;
  strip(a, b, -halfWidth, -halfWidth + 0.35, 0.025, curb);
  strip(a, b, halfWidth - 0.35, halfWidth, 0.025, curb);
  strip(a, a + (b - a) / 2, -0.07, 0.07, 0.025, cream);
}
for (let row = 0; row < 2; row++) {
  for (let i = 0; i < 12; i++) {
    const edge = -halfWidth + i * 0.75;
    strip((row - 1) * 0.023, row * 0.023, edge, edge + 0.75, 0.045,
      (i + row) % 2 ? asphalt : white);
  }
}

const trunk = material(0x795437);
const leaves = material(0x2c7146);
const trunkShape = new THREE.CylinderGeometry(0.18, 0.28, 1.6, 5);
const crownShape = new THREE.ConeGeometry(1.55, 3.8, 5);
for (let i = 0; i < 36; i++) {
  const a = i * tau / 36;
  const p = point(a, (i % 3 === 0 ? -1 : 1) * (9 + i % 5), 0);
  mesh(trunkShape, trunk, scene, p.x, 0.8, p.z);
  mesh(crownShape, leaves, scene, p.x, 2.9, p.z).rotation.y = i;
}

const car = new THREE.Group();
scene.add(car);
const orange = material(0xff8738);
const dark = material(0x20242e);
mesh(new THREE.BoxGeometry(1.65, 0.52, 3), orange, car, 0, 0.57);
mesh(new THREE.BoxGeometry(1.28, 0.48, 1.35), material(0x34556a), car, 0, 1.02, -0.2);
mesh(new THREE.BoxGeometry(1.3, 0.12, 1.38), orange, car, 0, 1.29, -0.2);
const tire = new THREE.CylinderGeometry(0.34, 0.34, 0.27, 10);
for (const x of [-0.84, 0.84]) {
  for (const z of [-0.92, 0.92]) mesh(tire, dark, car, x, 0.34, z).rotation.z = Math.PI / 2;
  mesh(new THREE.BoxGeometry(0.3, 0.16, 0.04), cream, car, x * 0.7, 0.61, 1.51);
  mesh(new THREE.BoxGeometry(0.3, 0.16, 0.04), red, car, x * 0.7, 0.61, -1.51);
}

const lap = document.querySelector('#lap');
const best = document.querySelector('#best');
const status = document.querySelector('#status');
const keys = new Set();
const controls = new Set([
  'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyR'
]);
const held = (a, b) => keys.has(a) || keys.has(b);
const forward = new THREE.Vector3();
const chase = new THREE.Vector3();
let speed, heading, start, nextGate, clean, bestTime = Infinity;

function reset() {
  car.position.copy(point(0, 0, 0));
  const tangent = point(0.001, 0, 0).sub(car.position);
  heading = Math.atan2(tangent.x, tangent.z);
  speed = 0;
  start = null;
  nextGate = 1;
  clean = true;
  car.rotation.y = heading;
  camera.position.set(car.position.x - 9 * Math.sin(heading), 6,
    car.position.z - 9 * Math.cos(heading));
}
reset();

addEventListener('keydown', e => {
  if (!controls.has(e.code)) return;
  e.preventDefault();
  if (e.code === 'KeyR' && !e.repeat) reset();
  keys.add(e.code);
});
addEventListener('keyup', e => keys.delete(e.code));
addEventListener('blur', () => keys.clear());

function resize() {
  renderer.setSize(innerWidth, innerHeight);
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
}
addEventListener('resize', resize);
resize();

function format(ms) {
  const n = Math.floor(ms);
  return `${Math.floor(n / 60000)}:${String(Math.floor(n / 1000) % 60).padStart(2, '0')}.${String(n % 1000).padStart(3, '0')}`;
}

const angle = () => (Math.atan2(car.position.z, car.position.x) + tau) % tau;
const onRoad = a => Math.abs(Math.hypot(car.position.x, car.position.z) - radius(a)) <= halfWidth;
const gates = 8;
let previous = performance.now();

renderer.setAnimationLoop(now => {
  const dt = Math.min((now - previous) / 1000, 0.05);
  previous = now;
  const before = angle();
  const road = onRoad(before);
  const gas = held('ArrowUp', 'KeyW');
  const brake = held('ArrowDown', 'KeyS');
  const steer = Number(held('ArrowLeft', 'KeyA')) - Number(held('ArrowRight', 'KeyD'));

  if (gas && start === null) start = now;
  if (brake && start === null) clean = false;
  speed += (Number(gas) * 16 - Number(brake) * (speed > 0 ? 30 : 10)) * dt;
  speed *= Math.exp(-(road ? 0.45 : 2.5) * dt);
  speed = THREE.MathUtils.clamp(speed, -7, road ? 25 : 8);
  heading += steer * 1.9 * THREE.MathUtils.clamp(speed / 7, -1, 1) * dt;
  car.rotation.y = heading;
  forward.set(Math.sin(heading), 0, Math.cos(heading));
  car.position.addScaledVector(forward, speed * dt);

  const after = angle();
  const stillOnRoad = onRoad(after);
  if (!stillOnRoad) clean = false;

  const travel = (after - before + 1.5 * tau) % tau - tau / 2;
  if (start !== null && travel > 0) {
    const sector = Math.floor(after / tau * gates);
    if (sector !== Math.floor(before / tau * gates)) {
      if (sector === 0) {
        if (clean && nextGate === gates) bestTime = Math.min(bestTime, now - start);
        if (stillOnRoad) {
          start = now;
          nextGate = 1;
          clean = true;
        }
      } else if (sector === nextGate) {
        nextGate++;
      }
    }
  }

  lap.textContent = format(start === null ? 0 : now - start);
  best.textContent = Number.isFinite(bestTime) ? format(bestTime) : '—';
  status.textContent = start === null ? 'Accelerate to start'
    : clean ? 'Follow the center dashes' : 'Lap invalid · cross the line to retry';

  chase.copy(car.position).addScaledVector(forward, -9);
  chase.y = 6;
  camera.position.lerp(chase, 1 - Math.exp(-8 * dt));
  camera.lookAt(chase.copy(car.position).addScaledVector(forward, 4).setY(0.8));
  renderer.render(scene, camera);
});
</script>
</body>
</html>
```

Save as `index.html`, run `python -m http.server 8000` in that folder, and open `http://localhost:8000`. The page needs internet access to load Three.js from the CDN.

### How I’d verify it

1. **Load and drive:** Check that the track, car, and HUD appear without console errors. Try both WASD and arrow keys: up accelerates, down brakes and then reverses, and the camera follows through turns. Resize the window and check that the view doesn’t stretch.
2. **Time two laps:** From the starting line, accelerate in the direction the car faces and stay on the asphalt. The lap timer should start on acceleration. After one full circuit, it should restart and populate **Best**. Drive a slower lap, then a faster one: only the faster one should replace the best.
3. **Check invalid laps and reset:** Cut across the grass and confirm the lap is marked invalid and cannot update **Best**. Cross the finish line forward on the road to start a fresh lap. Reverse across the line and drive forward again without completing the circuit; that should not set a best. Press **R** to return to the line and reset the current timer while keeping the session best.

I haven’t run the game here.


=============== RESPONSE ambition-game-01 ===============

Save this as `index.html`. It’s a complete single-file racer with a closed track, a chase camera, off-road slowdown, and a best lap saved in the browser. It loads Three.js from a CDN, so it needs an internet connection but no build step.

**Controls:** W / ↑ to accelerate, S / ↓ to brake or reverse, A / D or ← / → to steer, and R to reset the car and current lap without clearing your best time.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dust Loop — Arcade Racer</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; overflow: hidden; background: #b5dbef; color: white;
           font: 15px system-ui, sans-serif; }
    canvas { display: block; }
    #hud { position: fixed; top: 16px; left: 16px; padding: 14px 18px;
           border-radius: 12px; background: #14222de8; pointer-events: none;
           font-variant-numeric: tabular-nums; }
    h1 { margin: 0 0 8px; font-size: 20px; color: #ffd274; }
    #hud div + div { margin-top: 4px; }
    #help { margin: 10px 0 0; color: #d2e3ee; font-size: 12px; }
  </style>
</head>
<body>
  <section id="hud" aria-label="Race information">
    <h1>Dust Loop</h1>
    <div>Lap <span id="lap">1</span> · <span id="speed">0</span> km/h</div>
    <div>Current: <span id="current">—</span></div>
    <div>Best: <span id="best">—</span></div>
    <div id="status">Cross the start line to begin</div>
    <p id="help">WASD / arrows to drive · R to reset</p>
  </section>

  <script type="module">
    import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js";

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xb5dbef);
    scene.fog = new THREE.Fog(0xb5dbef, 100, 240);

    const camera = new THREE.PerspectiveCamera(58, innerWidth / innerHeight, 0.1, 350);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setSize(innerWidth, innerHeight);
    document.body.appendChild(renderer.domElement);

    scene.add(new THREE.HemisphereLight(0xfff5dc, 0x7b796f, 2.1));
    const sun = new THREE.DirectionalLight(0xffead1, 2.4);
    sun.position.set(-40, 70, -20);
    scene.add(sun);

    const material = color => new THREE.MeshStandardMaterial({ color, flatShading: true });
    function mesh(geometry, mat, x, y, z, parent = scene) {
      const object = new THREE.Mesh(geometry, mat);
      object.position.set(x, y, z);
      parent.add(object);
      return object;
    }

    const ground = mesh(new THREE.PlaneGeometry(500, 500), material(0x82985b), 0, 0, 0);
    ground.rotation.x = -Math.PI / 2;

    const curve = new THREE.CatmullRomCurve3(
      [[0, -40], [40, -34], [55, -6], [33, 17],
       [28, 42], [-17, 47], [-52, 24], [-48, -17], [-26, -37]]
        .map(([x, z]) => new THREE.Vector3(x, 0, z)),
      true
    );
    const N = 256;
    const halfWidth = 5.8;
    const points = curve.getSpacedPoints(N).slice(0, N);
    const tangents = points.map((_, i) => curve.getTangentAt(i / N));
    const sides = tangents.map(t => new THREE.Vector3(t.z, 0, -t.x));

    function strip(left, right, y, first, count, mat) {
      const vertices = [];
      const indices = [];
      for (let k = 0; k <= count; k++) {
        const i = (first + k) % N;
        const p = points[i], s = sides[i];
        vertices.push(p.x + s.x * left, y, p.z + s.z * left,
                      p.x + s.x * right, y, p.z + s.z * right);
        if (k < count) {
          const j = 2 * k;
          indices.push(j, j + 2, j + 1, j + 1, j + 2, j + 3);
        }
      }
      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute("position", new THREE.Float32BufferAttribute(vertices, 3));
      geometry.setIndex(indices);
      geometry.computeVertexNormals();
      mesh(geometry, mat, 0, 0, 0);
    }

    strip(-halfWidth, halfWidth, 0.035, 0, N, material(0x363d47));
    const curb = [material(0xf1ead8), material(0xd95843)];
    for (let i = 0; i < N; i += 4) {
      const mat = curb[(i / 4) % 2];
      strip(-6.2, -5.55, 0.045, i, 4, mat);
      strip(5.55, 6.2, 0.045, i, 4, mat);
    }

    const gates = [0, 64, 128, 192];
    const finish = [material(0xeef1eb), material(0x171e27)];
    const tile = new THREE.BoxGeometry(1.1, 0.025, 0.55);
    const startAngle = Math.atan2(tangents[0].x, tangents[0].z);
    for (let row = 0; row < 2; row++) {
      for (let col = 0; col < 10; col++) {
        const p = points[0].clone()
          .addScaledVector(sides[0], (col - 4.5) * 1.1)
          .addScaledVector(tangents[0], (row - 0.5) * 0.55);
        mesh(tile, finish[(row + col) % 2], p.x, 0.061, p.z).rotation.y = startAngle;
      }
    }

    function trackDistanceSq(x, z) {
      let best = Infinity;
      for (let i = 0; i < N; i++) {
        const a = points[i], b = points[(i + 1) % N];
        const dx = b.x - a.x, dz = b.z - a.z;
        const u = THREE.MathUtils.clamp(
          ((x - a.x) * dx + (z - a.z) * dz) / (dx * dx + dz * dz), 0, 1
        );
        best = Math.min(best, (x - a.x - u * dx) ** 2 + (z - a.z - u * dz) ** 2);
      }
      return best;
    }

    // Seeded scenery so the same course looks the same on every reload.
    let seed = 2025;
    function random() {
      seed = (1664525 * seed + 1013904223) >>> 0;
      return seed / 4294967296;
    }
    const trunkGeo = new THREE.CylinderGeometry(0.16, 0.26, 1.5, 5);
    const treeGeo = new THREE.ConeGeometry(1.5, 3.6, 5);
    const bark = material(0x70503b), leaves = material(0x366749);
    for (let i = 0; i < 160; i++) {
      const x = (random() - 0.5) * 190;
      const z = (random() - 0.5) * 170;
      if (trackDistanceSq(x, z) < 11 ** 2) continue;
      const tree = new THREE.Group();
      tree.position.set(x, 0, z);
      tree.scale.setScalar(0.7 + random() * 0.8);
      tree.rotation.y = random() * Math.PI * 2;
      scene.add(tree);
      mesh(trunkGeo, bark, 0, 0.75, 0, tree);
      mesh(treeGeo, leaves, 0, 2.45, 0, tree);
    }

    const car = new THREE.Group();
    scene.add(car);
    const red = material(0xf44f36), glass = material(0x28445b);
    const rubber = material(0x1a2028), lamp = material(0xffe6a4);
    mesh(new THREE.BoxGeometry(1.85, 0.53, 3.35), red, 0, 0.66, 0, car);
    mesh(new THREE.BoxGeometry(1.43, 0.52, 1.48), glass, 0, 1.16, -0.28, car);
    mesh(new THREE.BoxGeometry(1.49, 0.12, 1.52), red, 0, 1.47, -0.28, car);
    const wheelGeo = new THREE.CylinderGeometry(0.4, 0.4, 0.30, 10);
    for (const x of [-0.95, 0.95]) {
      for (const z of [-1.08, 1.08]) {
        mesh(wheelGeo, rubber, x, 0.43, z, car).rotation.z = Math.PI / 2;
      }
      mesh(new THREE.BoxGeometry(0.38, 0.18, 0.06), lamp, x * 0.7, 0.73, 1.69, car);
    }
    const shadow = mesh(new THREE.CircleGeometry(1, 16),
      new THREE.MeshBasicMaterial({ color: 0x151d21, transparent: true, opacity: 0.28,
                                   depthWrite: false }), 0, 0.08, 0, car);
    shadow.rotation.x = -Math.PI / 2;
    shadow.scale.set(1.25, 2.1, 1);

    const hud = Object.fromEntries(
      ["lap", "speed", "current", "best", "status"].map(id => [id, document.getElementById(id)])
    );
    const storageKey = "dust-loop-best-v1";
    let best = null;
    try {
      const saved = Number(localStorage.getItem(storageKey));
      if (Number.isFinite(saved) && saved > 0) best = saved;
    } catch {
      // Racing still works if browser storage is disabled.
    }

    function format(ms) {
      if (ms === null) return "—";
      const whole = Math.floor(ms);
      const minutes = Math.floor(whole / 60000);
      const seconds = String(Math.floor(whole / 1000) % 60).padStart(2, "0");
      return `${minutes}:${seconds}.${String(whole % 1000).padStart(3, "0")}`;
    }

    const keys = new Set();
    const controls = new Set(["KeyW", "KeyA", "KeyS", "KeyD", "ArrowUp", "ArrowDown",
                              "ArrowLeft", "ArrowRight", "KeyR"]);
    addEventListener("keydown", e => {
      if (!controls.has(e.code)) return;
      e.preventDefault();
      keys.add(e.code);
      if (e.code === "KeyR" && !e.repeat) reset();
    });
    addEventListener("keyup", e => keys.delete(e.code));
    addEventListener("blur", () => keys.clear());
    const down = (a, b) => keys.has(a) || keys.has(b);

    let speed, heading, lap, lapStart, nextGate;
    const forward = new THREE.Vector3();
    const cameraTarget = new THREE.Vector3();
    const lookTarget = new THREE.Vector3();

    function updateCamera(blend) {
      forward.set(Math.sin(heading), 0, Math.cos(heading));
      cameraTarget.copy(car.position).addScaledVector(forward, -9);
      cameraTarget.y += 5.5;
      camera.position.lerp(cameraTarget, blend);
      lookTarget.copy(car.position).addScaledVector(forward, 4);
      lookTarget.y += 0.7;
      camera.lookAt(lookTarget);
    }

    function reset() {
      car.position.copy(points[0]).addScaledVector(tangents[0], -7);
      heading = startAngle;
      car.rotation.y = heading;
      speed = 0;
      lap = 1;
      lapStart = null;
      nextGate = 0;
      updateCamera(1);
    }

    // Return the fraction of the movement segment that hits a gate,
    // or null if it misses or crosses in the wrong direction.
    function crossing(x0, z0, x1, z1, i) {
      const p = points[i], t = tangents[i], s = sides[i];
      const a = (x0 - p.x) * t.x + (z0 - p.z) * t.z;
      const b = (x1 - p.x) * t.x + (z1 - p.z) * t.z;
      if (!(a < 0 && b >= 0)) return null;
      const u = -a / (b - a);
      const x = x0 + (x1 - x0) * u;
      const z = z0 + (z1 - z0) * u;
      return Math.abs((x - p.x) * s.x + (z - p.z) * s.z) <= halfWidth ? u : null;
    }

    reset();
    let previous = performance.now();
    function frame(now) {
      const dt = Math.min(Math.max((now - previous) / 1000, 0), 0.05);
      previous = now;

      const onRoad = trackDistanceSq(car.position.x, car.position.z) <= halfWidth ** 2;
      const throttle = down("KeyW", "ArrowUp");
      const brake = down("KeyS", "ArrowDown");
      if (brake) {
        speed -= (speed > 0 ? 38 : 10) * dt;
      } else if (throttle) {
        speed += (speed < 0 ? 30 : 18) * dt;
      } else {
        speed = THREE.MathUtils.damp(speed, 0, onRoad ? 0.9 : 3, dt);
      }
      speed = THREE.MathUtils.clamp(speed, -8, 34);
      if (!onRoad && Math.abs(speed) > 9) {
        speed = THREE.MathUtils.damp(speed, Math.sign(speed) * 9, 4, dt);
      }

      const steer = Number(down("KeyD", "ArrowRight")) -
                    Number(down("KeyA", "ArrowLeft"));
      heading += steer * Math.sign(speed) * Math.min(Math.abs(speed) / 5, 1)
                 * (2.25 - 0.025 * Math.abs(speed)) * dt;
      car.rotation.y = heading;

      const { x: x0, z: z0 } = car.position;
      car.position.x += Math.sin(heading) * speed * dt;
      car.position.z += Math.cos(heading) * speed * dt;

      const hit = speed > 0
        ? crossing(x0, z0, car.position.x, car.position.z, gates[nextGate])
        : null;
      if (hit !== null) {
        const crossedAt = now - (1 - hit) * dt * 1000;
        if (nextGate === 0) {
          if (lapStart !== null) {
            const elapsed = crossedAt - lapStart;
            if (best === null || elapsed < best) {
              best = elapsed;
              try { localStorage.setItem(storageKey, String(best)); } catch {}
            }
            lap++;
          }
          lapStart = crossedAt;
        }
        nextGate = (nextGate + 1) % gates.length;
      }

      if (Math.abs(car.position.x) > 110 || Math.abs(car.position.z) > 100) reset();

      hud.lap.textContent = lap;
      hud.speed.textContent = Math.round(Math.abs(speed) * 3.6);
      hud.current.textContent = format(lapStart === null ? null : now - lapStart);
      hud.best.textContent = format(best);
      hud.status.textContent = lapStart === null ? "Cross the start line to begin"
        : nextGate === 0 ? "Checkpoints 3/3 · Head for the finish"
        : `Checkpoints ${nextGate - 1}/3`;
      updateCamera(1 - Math.exp(-8 * dt));
      renderer.render(scene, camera);
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);

    addEventListener("resize", () => {
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(innerWidth, innerHeight);
    });
  </script>
</body>
</html>
```

### How I’d verify it

I can’t run it here. To test locally, run `python -m http.server 8000` from the folder containing `index.html`, then open `http://localhost:8000`. Check the browser console for loading or WebGL errors, then test:

1. **Driving:** Try both key sets. Check that the car brakes before reversing, slows on the grass, and stops responding to held keys when the window loses focus.
2. **Lap timing:** Drive straight across the checkerboard. The timer should start and the HUD should show `0/3` checkpoints. Follow the track; each checkpoint should count once, and the next finish crossing should advance to lap 2, restart the timer, and set a best time.
3. **Invalid laps:** Skip a checkpoint or cross the finish backward. Neither should complete a lap.
4. **Best lap and reset:** Finish a slower lap and confirm the record stays unchanged; then beat it and confirm it updates. Press R and reload the page: the current run should reset, but the best time should remain.
5. **Resize:** Resize the window and confirm the scene fills it without stretching.


=============== RESPONSE ambition-game-02 ===============

Save this as `index.html` to play **Mesa Loop**, a single-track Three.js racer. The code keeps the track, driving rules, and HUD in one file. I reviewed the source but did not run it in a browser.

**Data shape.** An immutable oval defines the road. The car has an unwrapped track angle, a lateral offset, and a speed. The race is either waiting for throttle or timing a lap toward the next full turn. The best lap is a separate duration stored when browser storage is available.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mesa Loop</title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: #191e27;
    color: #fff5e6;
    font: 16px/1.4 system-ui, sans-serif;
  }
  main { width: min(100%, 1100px); margin: auto; padding: 16px; }
  header { display: flex; flex-wrap: wrap; align-items: end; gap: 12px 24px; }
  h1 { margin: 0; font-size: clamp(1.5rem, 5vw, 2.5rem); }
  dl { display: flex; flex-wrap: wrap; gap: 8px 12px; margin: 0; }
  dl div { background: #293241; padding: 6px 12px; border-radius: 8px; }
  dt { font-size: .8rem; color: #e2cbbb; }
  dd { margin: 0; font-weight: 700; font-variant-numeric: tabular-nums; }
  #view {
    margin-top: 12px;
    height: clamp(220px, 66vh, 720px);
    background: #e5a76c;
    border-radius: 12px;
    overflow: hidden;
  }
  canvas { display: block; width: 100%; height: 100%; }
  p { margin: 8px 0 0; }
  #status { color: #ffd38e; }
</style>
</head>
<body>
<main>
  <header>
    <h1>Mesa Loop</h1>
    <dl>
      <div><dt>Current lap</dt><dd id="lap">0.000 s</dd></div>
      <div><dt>Best lap</dt><dd id="best">No time yet</dd></div>
    </dl>
  </header>
  <div id="view"></div>
  <p id="status" role="status">Loading track…</p>
  <p>W / ↑ accelerate · S / ↓ brake and reverse · A / ← and D / → steer · R restart</p>
</main>

<script type="module">
const view = document.querySelector('#view');
const lapText = document.querySelector('#lap');
const bestText = document.querySelector('#best');
const status = document.querySelector('#status');

try {
  const THREE = await import('https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js');
  play(THREE);
} catch (error) {
  status.textContent = 'Could not load the game. Check your connection and try a browser with WebGL 2.';
  console.error(error);
}

function play(T) {
  const turn = 2 * Math.PI;
  const track = { x: 45, z: 29, halfWidth: 5, segments: 128 };
  const car = { angle: 0, offset: 0, speed: 0 };
  let race = { phase: 'ready' };
  const bestKey = 'mesa-loop.best.v1';
  let best = null;
  try {
    const saved = Number(localStorage.getItem(bestKey));
    if (Number.isFinite(saved) && saved > 0) best = saved;
  } catch {}

  const format = seconds => `${seconds.toFixed(3)} s`;
  bestText.textContent = best === null ? 'No time yet' : format(best);

  const scene = new T.Scene();
  scene.background = new T.Color(0xf4c891);
  const camera = new T.PerspectiveCamera(55, 1, .1, 400);
  const renderer = new T.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.domElement.setAttribute('aria-label', '3D view of Mesa Loop');
  view.append(renderer.domElement);

  scene.add(new T.HemisphereLight(0xfff2da, 0xa96348, 2));
  const sun = new T.DirectionalLight(0xffecd2, 2.4);
  sun.position.set(-30, 50, 20);
  scene.add(sun);

  function mesh(geometry, color, parent = scene) {
    const material = new T.MeshStandardMaterial({
      color, flatShading: true, side: T.DoubleSide
    });
    const item = new T.Mesh(geometry, material);
    parent.add(item);
    return item;
  }

  function box(parent, color, w, h, d, x, y, z) {
    const item = mesh(new T.BoxGeometry(w, h, d), color, parent);
    item.position.set(x, y, z);
    return item;
  }

  function point(angle, offset, y = 0) {
    const c = Math.cos(angle), s = Math.sin(angle);
    const nx = track.z * c, nz = track.x * s;
    const length = Math.hypot(nx, nz);
    return new T.Vector3(
      track.x * c + offset * nx / length, y,
      track.z * s + offset * nz / length
    );
  }

  function strip(start, end, inner, outer, y, color, segments) {
    const vertices = [], indices = [];
    for (let i = 0; i <= segments; i++) {
      const angle = T.MathUtils.lerp(start, end, i / segments);
      vertices.push(...point(angle, inner, y).toArray(),
                    ...point(angle, outer, y).toArray());
      const j = 2 * i;
      if (i < segments) indices.push(j, j + 1, j + 2, j + 1, j + 3, j + 2);
    }
    const geometry = new T.BufferGeometry();
    geometry.setAttribute('position', new T.Float32BufferAttribute(vertices, 3));
    geometry.setIndex(indices);
    geometry.computeVertexNormals();
    mesh(geometry, color);
  }

  box(scene, 0xc88855, 340, .2, 340, 0, -.13, 0);
  strip(0, turn, -5, 5, .01, 0x303644, track.segments);
  for (const side of [-1, 1]) {
    for (let i = 0; i < 64; i++) {
      strip(i * turn / 64, (i + 1) * turn / 64,
        side * 4.65, side * 5, .025, i % 2 ? 0xffebcb : 0xc74332, 2);
    }
  }
  for (let i = 0; i < 48; i++) {
    strip((i + .22) * turn / 48, (i + .68) * turn / 48,
      -.07, .07, .022, 0xe5b875, 1);
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 10; col++) {
      strip((row - 1) * .018, row * .018, col - 5, col - 4,
        .035, (row + col) % 2 ? 0xfff4db : 0x151821, 1);
    }
  }

  for (let i = 0; i < 28; i++) {
    const angle = i * 2.39996;
    const radius = i < 12 ? 5 + i : 60 + (i % 6) * 5;
    const h = 2 + (i % 5) * 1.5;
    const rock = mesh(new T.CylinderGeometry(1.2, 3.2, h, 5),
      [0xb65c3d, 0xa44e38, 0xd47a4f][i % 3]);
    rock.position.set(radius * Math.cos(angle), h / 2, radius * Math.sin(angle));
    rock.rotation.y = angle;
  }

  const model = new T.Group();
  scene.add(model);
  box(model, 0x21cad1, 1.65, .5, 3, 0, .58, 0);
  box(model, 0x153547, 1.25, .5, 1.35, 0, 1.03, -.24);
  box(model, 0xeffff7, .2, .015, 2.8, 0, .84, 0);
  for (const side of [-1, 1]) {
    for (const axle of [-1, 1]) {
      const wheel = mesh(new T.CylinderGeometry(.36, .36, .26, 8), 0x171923, model);
      wheel.rotation.z = Math.PI / 2;
      wheel.position.set(side * .83, .36, axle * .92);
    }
    box(model, 0xff4434, .29, .14, .05, side * .53, .61, -1.52);
  }

  const keys = new Set();
  const bindings = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
    'KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyR'];
  const held = (a, b) => keys.has(a) || keys.has(b);

  function reset() {
    Object.assign(car, { angle: 0, offset: 0, speed: 0 });
    race = { phase: 'ready' };
    lapText.textContent = format(0);
    status.textContent = 'Press accelerate to start the clock.';
  }

  window.addEventListener('keydown', event => {
    if (!bindings.includes(event.code) || event.altKey || event.ctrlKey || event.metaKey) return;
    event.preventDefault();
    keys.add(event.code);
    if (event.code === 'KeyR' && !event.repeat) reset();
  });
  window.addEventListener('keyup', event => keys.delete(event.code));
  window.addEventListener('blur', () => keys.clear());
  document.addEventListener('visibilitychange', () => keys.clear());
  reset();

  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const resize = new ResizeObserver(() => {
    const { clientWidth: width, clientHeight: height } = view;
    if (!width || !height) return;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height, false);
  });
  resize.observe(view);

  function drive(dt, start, now) {
    const throttle = held('KeyW', 'ArrowUp');
    const brake = held('KeyS', 'ArrowDown');
    const steer = Number(held('KeyD', 'ArrowRight')) -
                  Number(held('KeyA', 'ArrowLeft'));

    if (race.phase === 'ready') {
      if (!throttle || brake) return;
      race = { phase: 'timing', started: start, finish: turn };
      status.textContent = 'Lap in progress.';
    }

    const shoulder = Math.abs(car.offset) > track.halfWidth - .65;
    const limit = shoulder ? 13 : 34;
    const acceleration = brake ? (car.speed > 0 ? -32 : -12) : throttle ? 19 : 0;
    car.speed = T.MathUtils.clamp(
      car.speed * Math.exp(-(shoulder ? 1.4 : .42) * dt) + acceleration * dt,
      -8, limit
    );
    car.offset = T.MathUtils.clamp(
      car.offset + steer * car.speed * .27 * dt, -5.8, 5.8
    );

    const previous = car.angle;
    const tangent = point(previous + .001, car.offset)
      .distanceTo(point(previous - .001, car.offset)) / .002;
    car.angle += car.speed * dt / tangent;

    if (previous < race.finish && car.angle >= race.finish) {
      const fraction = (race.finish - previous) / (car.angle - previous);
      const crossedAt = T.MathUtils.lerp(start, now, fraction);
      const result = (crossedAt - race.started) / 1000;
      const record = best === null || result < best;
      if (record) {
        best = result;
        bestText.textContent = format(best);
        try { localStorage.setItem(bestKey, String(best)); } catch {}
      }
      status.textContent = `${record ? 'New best' : 'Last lap'} · ${format(result)}`;
      race = { phase: 'timing', started: crossedAt, finish: race.finish + turn };
    }
    lapText.textContent = format((now - race.started) / 1000);
  }

  const up = new T.Vector3(0, 1, 0);
  let previousFrame;
  function frame(now) {
    const start = previousFrame ?? now;
    previousFrame = now;
    const dt = Math.min((now - start) / 1000, .05);
    drive(dt, start, now);

    const position = point(car.angle, car.offset);
    const forward = point(car.angle + .002, car.offset).sub(position).normalize();
    model.position.copy(position);
    model.rotation.y = Math.atan2(forward.x, forward.z);

    if (motion.matches) {
      const height = 1.15 * Math.max(34, 53 / camera.aspect) /
        Math.tan(T.MathUtils.degToRad(camera.fov / 2));
      camera.position.set(0, height, 0);
      camera.up.set(0, 0, -1);
      camera.lookAt(0, 0, 0);
    } else {
      camera.up.copy(up);
      camera.position.copy(position).addScaledVector(forward, -10).addScaledVector(up, 6);
      camera.lookAt(position.clone().addScaledVector(forward, 7).addScaledVector(up, .6));
    }
    renderer.render(scene, camera);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}
</script>
</body>
</html>
```

### Run and verify

Open `index.html` in a modern desktop browser with internet access. If the browser blocks the module from a local file, serve the directory with `python -m http.server 8000` and open `http://localhost:8000`.

I would verify these on the actual page, in this order:

1. **Load.** Confirm the track and car appear, the timer stays at `0.000 s` before throttle, and the console has no errors.
2. **Drive.** Hold W or ↑ for a full lap. Test both steering directions, confirm the shoulder slows the car, and confirm S or ↓ brakes before reversing. Switch tabs while holding throttle, release it, and return. Throttle should not stick.
3. **Score.** Complete a lap. The best time should appear and the current timer should roll into the next lap. Reverse across the stripe and drive back over it. That crossing should not score. Complete a slower lap, then a faster one. Only the faster lap should replace the best.
4. **Restart and persist.** Press R mid-lap. The car and current timer should reset without erasing the best. Reload on the same origin and confirm the best remains.
5. **Check the HUD.** Try a 320 px viewport, 200% zoom, and reduced motion. Check that the timers and controls remain readable and that reduced motion swaps the chase camera for a fixed overhead view. Block the CDN and confirm the page shows a load error.

### Design choices and throughput

| Approach | Decision |
|---|---|
| Free-position driving with checkpoint gates | Not chosen. It gives freer handling but needs off-track recovery, checkpoint geometry, and shortcut rules. |
| Track-relative driving with lateral steering | Chosen. The same oval defines the road and lap progress. Reversing subtracts progress rather than creating another finish. |

- **Blocking first steps.** Settle the track coordinate and finish rule before building the scene or HUD.
- **Independent workstreams.** N/A. The renderer and HUD are small consumers of the same model in one file.
- **Shared mutable state.** The frame loop owns driving and lap updates. Input handlers track held keys and handle restart.
- **Smallest safe decomposition.** One file keeps delivery copyable. Delegation, browser execution, commits, and PR work were unavailable here.

**Principles used.** *Model the domain* led to unwrapped progress and explicit race phases. *Prove it works* led to the browser checks above, especially the reverse-crossing test. Those checks remain unrun. The chase camera provides driving feedback; reduced motion uses a fixed view, and the HUD does not animate. No product decision is needed to try this version.


=============== RESPONSE ambition-game-03 ===============

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Loop Sprint</title>
  <style>
    body { margin: 0; background: #a7d9f4; font: 16px system-ui, sans-serif; }
    canvas { display: block; }
    #hud {
      position: fixed; top: 16px; left: 16px; padding: 14px 18px;
      background: #102032e8; color: white; border-radius: 8px;
      font-variant-numeric: tabular-nums; pointer-events: none;
    }
    h1 { margin: 0 0 8px; font-size: 20px; }
    p { margin: 8px 0 0; color: #c6d8eb; font-size: 13px; }
  </style>
</head>
<body>
  <section id="hud">
    <h1>Loop Sprint</h1>
    Lap <span id="lap">0.00 s</span><br>
    Best <span id="best">—</span>
    <p>↑ / W throttle · ↓ / S brake / reverse<br>← → / A D steer · R restart lap</p>
  </section>

  <script type="module">
    import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js';

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xa7d9f4);
    scene.fog = new THREE.Fog(0xa7d9f4, 85, 180);
    const camera = new THREE.PerspectiveCamera(62, 1, 0.1, 220);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    document.body.append(renderer.domElement);

    scene.add(new THREE.HemisphereLight(0xffffff, 0x52613a, 2));
    const sun = new THREE.DirectionalLight(0xffe5bd, 2);
    sun.position.set(-20, 35, 15);
    scene.add(sun);

    function mesh(geometry, color, x, y, z, parent = scene) {
      const object = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({
        color, flatShading: true, side: THREE.DoubleSide
      }));
      object.position.set(x, y, z);
      parent.add(object);
      return object;
    }

    const box = (w, h, d, color, x, y, z, parent) =>
      mesh(new THREE.BoxGeometry(w, h, d), color, x, y, z, parent);

    const radius = 34, halfWidth = 5, turn = 2 * Math.PI;
    box(400, 1, 400, 0x729a4e, 0, -0.55, 0);

    function ring(inner, outer, color, height) {
      const road = mesh(new THREE.RingGeometry(inner, outer, 128), color, 0, height, 0);
      road.rotation.x = -Math.PI / 2;
    }

    ring(radius - halfWidth, radius + halfWidth, 0x353d49, 0);
    for (const edge of [radius - halfWidth, radius + halfWidth]) {
      ring(edge - 0.13, edge + 0.13, 0xffd588, 0.015);
    }

    for (let i = 1; i < 48; i++) {
      const a = i * turn / 48;
      box(0.14, 0.02, 1.5, 0xc8cbd0, radius * Math.cos(a), 0.02,
        radius * Math.sin(a)).rotation.y = -a;
    }

    for (let i = 0; i < 10; i++) {
      for (let j = 0; j < 2; j++) {
        box(1, 0.025, 0.5, (i + j) % 2 ? 0xf5f5f5 : 0x15191e,
          radius - halfWidth + i + 0.5, 0.025, j * 0.5 - 0.25);
      }
    }

    for (let i = 0; i < 30; i++) {
      const a = i * 2.39996;
      const r = i % 2 ? 15 + i % 9 : 47 + i % 13;
      const x = r * Math.cos(a), z = r * Math.sin(a);
      const h = 2.4 + (i % 5) * 0.45;
      box(0.4, 1.4, 0.4, 0x785136, x, 0.7, z);
      mesh(new THREE.ConeGeometry(h * 0.42, h, 5), 0x286b49, x, 0.9 + h / 2, z);
    }

    const car = new THREE.Group();
    scene.add(car);
    box(1.55, 0.45, 2.65, 0xf14943, 0, 0.49, 0, car);
    box(1.17, 0.42, 1.2, 0x243d59, 0, 0.9, -0.25, car);
    box(1.48, 0.12, 0.36, 0xffb84a, 0, 0.81, -1.13, car);
    for (const x of [-0.78, 0.78]) {
      for (const z of [-0.85, 0.85]) {
        mesh(new THREE.CylinderGeometry(0.31, 0.31, 0.26, 8), 0x171923,
          x, 0.32, z, car).rotation.z = Math.PI / 2;
      }
    }

    const lapLabel = document.querySelector('#lap');
    const bestLabel = document.querySelector('#best');
    const time = ms => `${(ms / 1000).toFixed(2)} s`;
    const keys = new Set();
    const down = (a, b) => keys.has(a) || keys.has(b);
    const controls = new Set(['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
      'KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyR']);
    const desiredCamera = new THREE.Vector3();
    let heading, speed, angle, progress, startedAt, best = Infinity;

    function reset() {
      car.position.set(radius, 0, 0);
      heading = speed = angle = progress = 0;
      startedAt = null;
      camera.position.set(radius, 6, -10);
    }

    reset();
    addEventListener('keydown', event => {
      if (!controls.has(event.code)) return;
      event.preventDefault();
      keys.add(event.code);
      if (event.code === 'KeyR' && !event.repeat) reset();
    });
    addEventListener('keyup', event => keys.delete(event.code));
    addEventListener('blur', () => keys.clear());

    function resize() {
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(innerWidth, innerHeight);
    }
    addEventListener('resize', resize);
    resize();

    let previous = performance.now();
    renderer.setAnimationLoop(now => {
      const dt = Math.min(Math.max((now - previous) / 1000, 0), 0.05);
      previous = now;
      const throttle = Number(down('ArrowUp', 'KeyW')) - Number(down('ArrowDown', 'KeyS'));
      const steer = Number(down('ArrowLeft', 'KeyA')) - Number(down('ArrowRight', 'KeyD'));

      speed += throttle * 19 * dt;
      speed *= Math.exp(-(throttle ? 0.45 : 1.7) * dt);
      speed = THREE.MathUtils.clamp(speed, -8, 24);
      heading += steer * 1.65 * THREE.MathUtils.clamp(speed / 8, -1, 1) * dt;
      const fx = Math.sin(heading), fz = Math.cos(heading);
      let x = car.position.x + fx * speed * dt;
      let z = car.position.z + fz * speed * dt;

      // Soft walls keep the car on the loop and prevent infield shortcuts.
      const distance = Math.hypot(x, z);
      const limit = THREE.MathUtils.clamp(distance, radius - halfWidth + 1,
        radius + halfWidth - 1);
      if (limit !== distance) {
        x *= limit / distance;
        z *= limit / distance;
        speed *= Math.exp(-4 * dt);
      }
      car.position.set(x, 0, z);
      car.rotation.y = heading;

      // Signed angular travel cancels when you backtrack across the line.
      const nextAngle = Math.atan2(z, x);
      const delta = nextAngle - angle;
      const step = Math.atan2(Math.sin(delta), Math.cos(delta));
      angle = nextAngle;
      if (startedAt === null && step !== 0) startedAt = now - dt * 1000;
      progress += step;
      if (progress >= turn) {
        const crossedAt = now - (progress - turn) / step * dt * 1000;
        best = Math.min(best, crossedAt - startedAt);
        bestLabel.textContent = time(best);
        startedAt = crossedAt;
        progress -= turn;
      }
      lapLabel.textContent = time(startedAt === null ? 0 : now - startedAt);

      desiredCamera.set(x - fx * 10, 6, z - fz * 10);
      camera.position.lerp(desiredCamera, 1 - Math.exp(-7 * dt));
      camera.lookAt(x + fx * 4, 0.6, z + fz * 4);
      renderer.render(scene, camera);
    });
  </script>
</body>
</html>
```

Save as `index.html` and open it in a modern browser with WebGL and internet access for the Three.js CDN. No build step is needed.

**How I’d verify it (not run here):**

1. Open the page and check that the track, car, and HUD render without console errors. Resize the window and confirm the view still fills it without stretching.
2. Drive with both WASD and the arrow keys. Confirm the chase camera follows, braking transitions to reverse, and hitting either track edge slows the car without letting it cut across the infield.
3. From the starting grid, accelerate and steer right around the loop. Confirm the timer starts on movement, the first full lap sets **Best**, a slower lap leaves it unchanged, and a faster lap replaces it.
4. Rock back and forth over the start line and confirm it doesn’t register a lap. Press **R** and confirm the car returns to the grid, the lap timer resets, and the session best stays visible.


=============== RESPONSE ambition-game-04 ===============

Save this as `index.html`. It gives you a low-poly Three.js racer with one closed track, keyboard steering, a lap timer, and a best lap saved in your browser. The whole game is in one file. It needs an internet connection to load Three.js.

**Data shape.** One ellipse defines the road, its edges, and the finish line. The car stores position, heading, and speed. The lap state is either idle or an active attempt with a start time and an unwrapped track angle. Leaving the road cancels the attempt.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Copper Loop</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; background: #f3bb8a; color: #fff4de; font: 16px system-ui, sans-serif; }
    canvas { display: block; width: 100%; height: 100dvh; }
    .panel {
      position: fixed; left: 16px; z-index: 1; padding: 12px 16px;
      border: 1px solid #927361; border-radius: 12px; background: #211b19;
      max-width: calc(100% - 32px);
    }
    header { top: 16px; }
    h1 { margin: 0 0 8px; font-size: 1rem; letter-spacing: .15em; text-transform: uppercase; }
    dl { display: flex; gap: 24px; margin: 0; }
    dt { font-size: .75rem; color: #ffca98; }
    dd { margin: 0; font: 1.1rem ui-monospace, monospace; }
    footer { bottom: 16px; font-size: .85rem; }
    #status { margin: 8px 0 0; font-size: .8rem; min-height: 1.2em; }
  </style>
</head>
<body>
  <header class="panel">
    <h1>Copper Loop</h1>
    <dl>
      <div><dt>Lap</dt><dd id="lap">--:--.---</dd></div>
      <div><dt>Best</dt><dd id="best">--:--.---</dd></div>
    </dl>
    <p id="status" role="status">Loading track…</p>
  </header>
  <footer class="panel">WASD / arrows to drive · R to restart</footer>

  <script type="module">
    const status = document.querySelector('#status');

    try {
      const T = await import('https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js');
      start(T);
    } catch (error) {
      status.textContent = 'Could not start. Check your connection and WebGL support.';
      console.error(error);
    }

    function start(T) {
      const track = { x: 46, z: 28, inner: .84, outer: 1.16 };
      const tau = Math.PI * 2;
      const segments = 128;
      const scene = new T.Scene();
      scene.background = new T.Color(0xf3bb8a);
      scene.fog = new T.Fog(0xf3bb8a, 75, 180);

      const renderer = new T.WebGLRenderer({ antialias: true });
      renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
      renderer.domElement.setAttribute('aria-label', 'Copper Loop race track');
      document.body.append(renderer.domElement);
      const camera = new T.PerspectiveCamera(57, 1, .1, 220);

      scene.add(new T.HemisphereLight(0xffead8, 0x9b5b50, 2));
      const sun = new T.DirectionalLight(0xffe0b4, 2.2);
      sun.position.set(-30, 50, 20);
      scene.add(sun);

      function mesh(geometry, color, parent = scene) {
        const object = new T.Mesh(geometry, new T.MeshStandardMaterial({
          color, flatShading: true, side: T.DoubleSide
        }));
        parent.add(object);
        return object;
      }

      function box(w, h, d, color, x, y, z, parent = scene) {
        const object = mesh(new T.BoxGeometry(w, h, d), color, parent);
        object.position.set(x, y, z);
        return object;
      }

      function strip(a, b, inner, outer, y, color, steps = 1) {
        const vertices = [];
        const indices = [];
        for (let i = 0; i <= steps; i++) {
          const angle = a + (b - a) * i / steps;
          for (const r of [inner, outer]) {
            vertices.push(track.x * r * Math.cos(angle), y, track.z * r * Math.sin(angle));
          }
          if (i < steps) {
            const k = i * 2;
            indices.push(k, k + 2, k + 1, k + 1, k + 2, k + 3);
          }
        }
        const geometry = new T.BufferGeometry();
        geometry.setAttribute('position', new T.Float32BufferAttribute(vertices, 3));
        geometry.setIndex(indices);
        geometry.computeVertexNormals();
        mesh(geometry, color);
      }

      box(400, .2, 400, 0xc27b52, 0, -.12, 0);
      strip(0, tau, track.inner, track.outer, 0, 0x343542, segments);
      for (const edge of [track.inner, track.outer]) {
        for (let i = 0; i < 32; i++) {
          strip(i * tau / 32, (i + 1) * tau / 32, edge - .012, edge + .012,
            .025, i % 2 ? 0xffe1ad : 0xe95a36, 4);
        }
      }
      for (let i = 1; i < 32; i++) {
        strip((i - .22) * tau / 32, (i + .22) * tau / 32,
          .995, 1.005, .018, 0xd7c5aa, 2);
      }
      const cell = (track.outer - track.inner) / 12;
      for (let i = 0; i < 12; i++) {
        for (let j = 0; j < 2; j++) {
          box(cell * track.x, .025, 1.1, (i + j) % 2 ? 0x1c1b22 : 0xfff4de,
            (track.inner + (i + .5) * cell) * track.x, .035, (j - .5) * 1.1);
        }
      }

      for (let i = 0; i < 48; i++) {
        const angle = i * 2.399963;
        const r = i < 20 ? .22 + (i % 6) * .082 : 1.36 + (i % 7) * .14;
        const size = 1.3 + (i % 5) * .56;
        const rock = mesh(new T.DodecahedronGeometry(size),
          [0x9c4d43, 0xda895d, 0xf3b478][i % 3]);
        rock.position.set(track.x * r * Math.cos(angle), size * .4,
          track.z * r * Math.sin(angle));
        rock.scale.set(1.25, .65 + (i % 4) * .24, 1);
        rock.rotation.y = angle;
      }

      const model = new T.Group();
      scene.add(model);
      box(2.1, .55, 3.5, 0x16b8aa, 0, .62, 0, model);
      box(1.55, .55, 1.65, 0x213845, 0, 1.1, -.3, model);
      box(1.59, .1, 1.69, 0x71e1cb, 0, 1.43, -.3, model);
      for (const x of [-1.04, 1.04]) {
        for (const z of [-1.05, 1.05]) {
          const tire = mesh(new T.CylinderGeometry(.4, .4, .35, 8), 0x211d24, model);
          tire.rotation.z = Math.PI / 2;
          tire.position.set(x, .4, z);
        }
        box(.35, .17, .05, 0xffe5a6, x * .7, .67, 1.77, model);
      }

      const lapText = document.querySelector('#lap');
      const bestText = document.querySelector('#best');
      const storageKey = 'copper-loop-best-v1';
      let best = Infinity;
      try {
        const saved = Number(localStorage.getItem(storageKey));
        if (Number.isFinite(saved) && saved > 0) best = saved;
      } catch {}

      function format(ms) {
        if (!Number.isFinite(ms)) return '--:--.---';
        const n = Math.floor(ms);
        return `${String(Math.floor(n / 60000)).padStart(2, '0')}:` +
          `${String(Math.floor(n / 1000) % 60).padStart(2, '0')}.` +
          String(n % 1000).padStart(3, '0');
      }

      const car = { x: 0, z: 0, heading: 0, speed: 0 };
      const keys = new Set();
      let lap = null;
      let previousAngle;
      let aimInitialized = false;
      const eye = new T.Vector3();
      const focus = new T.Vector3();

      function reset() {
        previousAngle = -.19;
        car.x = track.x * Math.cos(previousAngle);
        car.z = track.z * Math.sin(previousAngle);
        car.heading = Math.atan2(-track.x * Math.sin(previousAngle),
          track.z * Math.cos(previousAngle));
        car.speed = 0;
        lap = null;
        aimInitialized = false;
        status.textContent = 'Cross the checkerboard to start.';
      }

      const controls = new Set([
        'KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyR',
        'ArrowUp', 'ArrowLeft', 'ArrowDown', 'ArrowRight'
      ]);
      addEventListener('keydown', e => {
        if (!controls.has(e.code)) return;
        e.preventDefault();
        keys.add(e.code);
        if (e.code === 'KeyR' && !e.repeat) reset();
      });
      addEventListener('keyup', e => keys.delete(e.code));
      addEventListener('blur', () => keys.clear());
      document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
          keys.clear();
          reset();
        }
      });

      function resize() {
        renderer.setSize(innerWidth, innerHeight, false);
        camera.aspect = innerWidth / innerHeight;
        camera.updateProjectionMatrix();
      }
      addEventListener('resize', resize);
      resize();
      reset();
      bestText.textContent = format(best);

      function updateLap(now, onRoad) {
        const angle = Math.atan2(car.z / track.z, car.x / track.x);
        const change = angle - previousAngle;
        const delta = Math.atan2(Math.sin(change), Math.cos(change));
        const crossed = previousAngle < 0 && angle >= 0 && delta > 0;
        previousAngle = angle;

        if (!onRoad) {
          if (lap) status.textContent = 'Lap invalid. Cross the line to try again.';
          lap = null;
          return;
        }

        if (lap) lap.angle += delta;
        if (!crossed) return;
        if (!lap) {
          lap = { since: now, angle };
          status.textContent = 'Lap underway. Stay between the curbs.';
        } else if (lap.angle >= tau) {
          const elapsed = now - lap.since;
          const record = elapsed < best;
          if (record) {
            best = elapsed;
            bestText.textContent = format(best);
            try { localStorage.setItem(storageKey, String(best)); } catch {}
          }
          lap = { since: now, angle };
          status.textContent = `${record ? 'New best' : 'Last lap'} ${format(elapsed)}`;
        }
      }

      function radius() {
        return Math.hypot(car.x / track.x, car.z / track.z);
      }

      let previousTime = performance.now();
      function frame(now) {
        const dt = Math.min(Math.max((now - previousTime) / 1000, 0), .05);
        previousTime = now;

        const throttle = keys.has('KeyW') || keys.has('ArrowUp');
        const brake = keys.has('KeyS') || keys.has('ArrowDown');
        const left = keys.has('KeyA') || keys.has('ArrowLeft');
        const right = keys.has('KeyD') || keys.has('ArrowRight');

        const r = radius();
        const grip = r >= track.inner && r <= track.outer;
        if (brake) car.speed -= 28 * dt;
        else if (throttle) car.speed += 17 * dt;
        else car.speed *= Math.exp(-1.5 * dt);
        if (!grip) car.speed *= Math.exp(-2.6 * dt);
        car.speed = T.MathUtils.clamp(car.speed, -8, 34);
        car.heading += (Number(left) - Number(right)) * 1.75 * dt *
          Math.min(Math.abs(car.speed) / 7, 1) * Math.sign(car.speed);

        const dx = Math.sin(car.heading);
        const dz = Math.cos(car.heading);
        car.x = T.MathUtils.clamp(car.x + dx * car.speed * dt, -105, 105);
        car.z = T.MathUtils.clamp(car.z + dz * car.speed * dt, -105, 105);
        const nextRadius = radius();
        updateLap(now, nextRadius >= track.inner && nextRadius <= track.outer);
        lapText.textContent = format(lap ? now - lap.since : Infinity);

        model.position.set(car.x, 0, car.z);
        model.rotation.y = car.heading;
        eye.set(car.x - dx * 10, 6.3, car.z - dz * 10);
        focus.set(car.x + dx * 5, .65, car.z + dz * 5);
        if (!aimInitialized) {
          camera.position.copy(eye);
          aimInitialized = true;
        } else {
          camera.position.lerp(eye, 1 - Math.exp(-8 * dt));
        }
        camera.lookAt(focus);
        renderer.render(scene, camera);
        requestAnimationFrame(frame);
      }
      requestAnimationFrame(frame);
    }
  </script>
</body>
</html>
```

### Run and verify

From the directory containing `index.html`, run `python -m http.server 8000`, then open `http://localhost:8000`. I did not run the game here. These are expected results, not measured results.

| Check | Expected result |
|---|---|
| Load the page and resize the window | The track and car render, the view resizes, and the timer panel stays visible. |
| Drive with WASD, then with the arrows | The car steers relative to the chase camera. Down or S brakes and then reverses. |
| Cross the checkerboard forward and complete a clean lap | The timer starts on the first crossing. A full lap sets Best and starts timing the next lap. |
| Reverse back over the line, then drive forward across it again | The short round trip does not record a lap. |
| Cut across the infield during a timed lap | The attempt is canceled. The next forward crossing starts a fresh attempt without setting Best. |
| Complete a slower lap, press R, then reload | The slower lap does not replace Best. R and reload reset the current attempt but retain Best when browser storage is available. |

### Design and scope

| Approach | Decision |
|---|---|
| Free steering on an ellipse | Chosen. The same geometry defines the visible road and validates laps, while the player still has to steer. |
| Car constrained to a spline | Skipped. It simplifies lap tracking but takes away much of the steering. |

**Throughput checkpoint.** Blocking first step: define the track and lap state. Independent workstreams: none needed for one file. Shared mutable state: the frame loop owns driving and timing updates; reset clears the current attempt. Smallest safe decomposition: one file, with separate scene construction, lap tracking, and frame updates. No open product decisions are required to try it.

**Principles applied.** *Model the domain* put the ellipse and lap state before the rendering and driving logic. *Prove it works* shaped the browser checks around clean laps, reverse crossings, shortcuts, and persistence. Runtime verification remains unperformed.


=============== RESPONSE ambition-game-05 ===============

Save this as `index.html`. It’s a complete single-file Three.js racer with a closed track, a chase camera, keyboard controls, and a best lap that persists in the browser. Three.js loads from a CDN, so you’ll need an internet connection when you open the game.

**Controls:** W or ↑ to accelerate, S or ↓ to brake and reverse, A/D or ←/→ to steer, and R to restart without clearing your best lap.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pine Loop Racer</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      overflow: hidden;
      background: #a8d8ef;
      color: #fff;
      font: 15px system-ui, sans-serif;
    }
    canvas { display: block; }
    #hud {
      position: fixed;
      z-index: 1;
      top: 16px;
      left: 16px;
      padding: 14px 18px;
      min-width: 225px;
      border-radius: 12px;
      background: #152338ee;
      font-variant-numeric: tabular-nums;
    }
    h1 { margin: 0 0 8px; font-size: 20px; }
    .row { display: flex; justify-content: space-between; gap: 24px; }
    #status { margin-top: 8px; color: #ffdc85; }
    #controls {
      position: fixed;
      z-index: 1;
      bottom: 16px;
      left: 50%;
      transform: translateX(-50%);
      width: max-content;
      max-width: calc(100% - 32px);
      padding: 8px 14px;
      border-radius: 8px;
      background: #152338ee;
      text-align: center;
    }
  </style>
</head>
<body>
  <section id="hud" aria-label="Race information">
    <h1>Pine Loop Racer</h1>
    <div class="row"><span>Current lap</span><strong id="lap">0:00.000</strong></div>
    <div class="row"><span>Best lap</span><strong id="best">—</strong></div>
    <div class="row"><span>Checkpoints</span><strong id="gates">0 / 3</strong></div>
    <div id="status">Accelerate to start</div>
  </section>
  <div id="controls">WASD / arrows to drive · R to restart</div>

  <script type="module">
    import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js';

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xa8d8ef);
    scene.fog = new THREE.Fog(0xa8d8ef, 90, 230);

    const camera = new THREE.PerspectiveCamera(62, innerWidth / innerHeight, 0.1, 350);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setSize(innerWidth, innerHeight);
    document.body.appendChild(renderer.domElement);

    scene.add(new THREE.HemisphereLight(0xfff4df, 0x52704c, 2));
    const sun = new THREE.DirectionalLight(0xffebc7, 2);
    sun.position.set(-35, 55, 20);
    scene.add(sun);

    const mat = color => new THREE.MeshStandardMaterial({ color, flatShading: true });
    const grass = new THREE.Mesh(new THREE.PlaneGeometry(500, 500), mat(0x648e4b));
    grass.rotation.x = -Math.PI / 2;
    scene.add(grass);

    // A closed spline sampled into a road mesh and used for road detection.
    const curve = new THREE.CatmullRomCurve3([
      [-39, 19], [-16, 35], [20, 33], [43, 16],
      [37, -13], [17, -26], [-10, -20], [-33, -29], [-47, -8]
    ].map(([x, z]) => new THREE.Vector3(x, 0, z)), true);
    const N = 240;
    const halfWidth = 5;
    const points = curve.getSpacedPoints(N).slice(0, N);
    const tangents = points.map((_, i) =>
      points[(i + 1) % N].clone().sub(points[(i + N - 1) % N]).normalize()
    );
    const sides = tangents.map(t => new THREE.Vector3(-t.z, 0, t.x));

    function ribbon(left, right, height, materials, alternate = false) {
      const coords = [], indices = [];
      const geometry = new THREE.BufferGeometry();
      for (let i = 0; i < N; i++) {
        for (const offset of [left, right]) {
          coords.push(points[i].x + sides[i].x * offset, height,
                      points[i].z + sides[i].z * offset);
        }
        const a = i * 2, b = ((i + 1) % N) * 2;
        indices.push(a, a + 1, b, a + 1, b + 1, b);
        if (alternate) geometry.addGroup(i * 6, 6, Math.floor(i / 3) % 2);
      }
      geometry.setAttribute('position', new THREE.Float32BufferAttribute(coords, 3));
      geometry.setIndex(indices);
      geometry.computeVertexNormals();
      scene.add(new THREE.Mesh(geometry, materials));
    }

    ribbon(-halfWidth, halfWidth, 0.03, mat(0x303641));
    const curb = [mat(0xe84b43), mat(0xf5f0dc)];
    ribbon(-5.4, -5, 0.055, curb, true);
    ribbon(5, 5.4, 0.055, curb, true);

    function box(parent, material, w, h, d, x, y, z) {
      const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
      mesh.position.set(x, y, z);
      parent.add(mesh);
      return mesh;
    }

    const white = mat(0xf5f0dc), black = mat(0x151a20);
    const startLine = new THREE.Group();
    startLine.position.copy(points[0]);
    startLine.rotation.y = Math.atan2(tangents[0].x, tangents[0].z);
    scene.add(startLine);
    for (let row = 0; row < 2; row++) {
      for (let col = 0; col < 10; col++) {
        box(startLine, (row + col) % 2 ? black : white,
            1, 0.02, 0.5, col - 4.5, 0.05, (row - 0.5) * 0.5);
      }
    }

    function roadDistance(x, z) {
      let closest = Infinity;
      for (let i = 0; i < N; i++) {
        const a = points[i], b = points[(i + 1) % N];
        const dx = b.x - a.x, dz = b.z - a.z;
        const t = THREE.MathUtils.clamp(
          ((x - a.x) * dx + (z - a.z) * dz) / (dx * dx + dz * dz), 0, 1
        );
        closest = Math.min(closest, (x - a.x - t * dx) ** 2 + (z - a.z - t * dz) ** 2);
      }
      return Math.sqrt(closest);
    }

    // Seeded scenery: every reload generates the same forest.
    let seed = 427;
    function random() {
      seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
      return seed / 4294967296;
    }
    const trunks = mat(0x795035), leaves = [mat(0x245d3a), mat(0x347847)];
    const trunkGeo = new THREE.CylinderGeometry(0.17, 0.24, 1.5, 5);
    const crownGeo = new THREE.ConeGeometry(1.45, 3.7, 5);
    for (let i = 0; i < 210; i++) {
      const x = (random() - 0.5) * 165;
      const z = (random() - 0.5) * 145;
      if (roadDistance(x, z) < 8) continue;
      const tree = new THREE.Group();
      const trunk = new THREE.Mesh(trunkGeo, trunks);
      trunk.position.y = 0.75;
      const crown = new THREE.Mesh(crownGeo, leaves[i % 2]);
      crown.position.y = 2.65;
      tree.add(trunk, crown);
      tree.position.set(x, 0, z);
      tree.scale.setScalar(0.65 + random() * 0.8);
      tree.rotation.y = random() * Math.PI;
      scene.add(tree);
    }

    // The car's local forward direction is +Z.
    const car = new THREE.Group();
    scene.add(car);
    const red = mat(0xff4938), glass = mat(0x29475f);
    box(car, red, 1.8, 0.48, 3.3, 0, 0.48, 0);
    box(car, glass, 1.35, 0.47, 1.53, 0, 0.91, -0.25);
    box(car, red, 1.39, 0.10, 1.57, 0, 1.19, -0.25);
    for (const x of [-0.93, 0.93]) {
      for (const z of [-1.07, 1.07]) {
        const wheel = new THREE.Mesh(new THREE.CylinderGeometry(0.36, 0.36, 0.3, 10), black);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(x, 0.36, z);
        car.add(wheel);
      }
      box(car, white, 0.36, 0.16, 0.08, x * 0.69, 0.53, 1.67);
    }

    const keys = new Set();
    const drivingKeys = new Set([
      'KeyW', 'KeyA', 'KeyS', 'KeyD', 'ArrowUp', 'ArrowDown',
      'ArrowLeft', 'ArrowRight', 'KeyR'
    ]);
    addEventListener('keydown', event => {
      if (!drivingKeys.has(event.code)) return;
      event.preventDefault();
      keys.add(event.code);
      if (event.code === 'KeyR' && !event.repeat) reset();
    });
    addEventListener('keyup', event => keys.delete(event.code));
    addEventListener('blur', () => keys.clear());
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) keys.clear();
    });
    const held = (a, b) => keys.has(a) || keys.has(b);

    const lapEl = document.querySelector('#lap');
    const bestEl = document.querySelector('#best');
    const gatesEl = document.querySelector('#gates');
    const statusEl = document.querySelector('#status');
    const storageKey = 'pine-loop-best-ms-v1';
    let best = Infinity;
    try {
      const stored = Number(localStorage.getItem(storageKey));
      if (Number.isFinite(stored) && stored > 0) best = stored;
    } catch { /* Keep an in-memory best if storage is blocked. */ }

    function format(ms) {
      const n = Math.floor(ms);
      return `${Math.floor(n / 60000)}:${String(Math.floor(n / 1000) % 60).padStart(2, '0')}.${String(n % 1000).padStart(3, '0')}`;
    }
    function updateBest() {
      bestEl.textContent = Number.isFinite(best) ? format(best) : '—';
    }
    updateBest();

    const checkpoints = [N / 4, N / 2, 3 * N / 4];
    let speed, heading, lapStart, nextGate, lapCount;
    const oldPos = new THREE.Vector3();
    const cameraGoal = new THREE.Vector3();
    const look = new THREE.Vector3();
    const forward = new THREE.Vector3();

    function updateCamera(dt, snap = false) {
      forward.set(Math.sin(heading), 0, Math.cos(heading));
      cameraGoal.copy(car.position).addScaledVector(forward, -9);
      cameraGoal.y += 5;
      camera.position.lerp(cameraGoal, snap ? 1 : 1 - Math.exp(-7 * dt));
      look.copy(car.position).addScaledVector(forward, 5);
      look.y += 0.7;
      camera.lookAt(look);
    }

    function reset() {
      car.position.copy(points[0]).addScaledVector(tangents[0], 1.4);
      car.position.y = 0.05;
      heading = Math.atan2(tangents[0].x, tangents[0].z);
      car.rotation.y = heading;
      speed = 0;
      lapStart = null;
      nextGate = lapCount = 0;
      lapEl.textContent = format(0);
      gatesEl.textContent = '0 / 3';
      statusEl.textContent = 'Accelerate to start';
      updateCamera(0, true);
    }
    reset();

    // A gate counts only when crossed forward and within the road width.
    function crossesGate(index) {
      const p = points[index], t = tangents[index], s = sides[index];
      const ax = oldPos.x - p.x, az = oldPos.z - p.z;
      const bx = car.position.x - p.x, bz = car.position.z - p.z;
      const before = ax * t.x + az * t.z;
      const after = bx * t.x + bz * t.z;
      if (before >= 0 || after < 0) return false;
      const f = -before / (after - before);
      const lateral = (ax + f * (bx - ax)) * s.x + (az + f * (bz - az)) * s.z;
      return Math.abs(lateral) <= halfWidth;
    }

    let previous = performance.now();
    renderer.setAnimationLoop(now => {
      const dt = Math.max(0, Math.min((now - previous) / 1000, 0.05));
      previous = now;

      const gas = held('KeyW', 'ArrowUp'), brake = held('KeyS', 'ArrowDown');
      const steer = Number(held('KeyA', 'ArrowLeft')) - Number(held('KeyD', 'ArrowRight'));
      const offRoad = roadDistance(car.position.x, car.position.z) > halfWidth;

      if (gas && lapStart === null) {
        lapStart = now;
        statusEl.textContent = 'Lap 1';
      }
      if (gas) speed += 21 * dt;
      if (brake) speed -= (speed > 0 ? 33 : 13) * dt;
      speed *= Math.exp(-(offRoad ? 2 : gas || brake ? 0.35 : 0.9) * dt);
      speed = THREE.MathUtils.clamp(speed, -8, offRoad ? 10 : 31);

      heading += steer * 2.1 * THREE.MathUtils.clamp(speed / 7, -0.7, 1) * dt;
      car.rotation.y = heading;
      oldPos.copy(car.position);
      car.position.x += Math.sin(heading) * speed * dt;
      car.position.z += Math.cos(heading) * speed * dt;

      if (lapStart !== null) {
        if (nextGate < checkpoints.length && crossesGate(checkpoints[nextGate])) {
          nextGate++;
          gatesEl.textContent = `${nextGate} / 3`;
        }
        if (crossesGate(0)) {
          if (nextGate === checkpoints.length) {
            const elapsed = now - lapStart;
            const record = elapsed < best;
            if (record) {
              best = elapsed;
              updateBest();
              try { localStorage.setItem(storageKey, String(best)); } catch {}
            }
            lapCount++;
            lapStart = now;
            statusEl.textContent = `Lap ${lapCount + 1} · ${record ? 'New best' : format(elapsed)}`;
          } else {
            statusEl.textContent = 'Lap not counted: missed checkpoint';
            lapStart = now;
          }
          nextGate = 0;
          gatesEl.textContent = '0 / 3';
        }
        lapEl.textContent = format(now - lapStart);
      }

      updateCamera(dt);
      renderer.render(scene, camera);
    });

    addEventListener('resize', () => {
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(innerWidth, innerHeight);
    });
  </script>
</body>
</html>
```

### How I’d verify it

I haven’t run it here. From the directory containing `index.html`, I’d run `python -m http.server 8000` and open `http://localhost:8000/`, then check:

1. **Loading and controls:** The track, trees, car, and HUD appear without console errors. Both key layouts work, the arrow keys don’t scroll the page, and releasing a key stops that input. Grass slows the car.
2. **Valid lap:** The timer starts on acceleration. Follow the track in the direction the car is facing, watch the checkpoints advance to `3 / 3`, and cross the checkered line. The timer restarts and the best lap appears.
3. **Invalid lap:** Cut across the infield to skip a checkpoint, or cross the finish line backward. Neither should award a lap.
4. **Restart and persistence:** Press R to reset the car and timer without clearing the best lap. Reload on the same URL and confirm the best is still there. Resize the window and confirm the view keeps the correct proportions.


=============== RESPONSE ambition-game-06 ===============

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ring Sprint</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; overflow: hidden; background: #a9d9e7; color: white;
           font: 600 16px system-ui, sans-serif; }
    canvas { display: block; }
    #hud { position: fixed; top: 16px; left: 16px; z-index: 1;
           padding: 14px 18px; border-radius: 10px; background: #14212eea;
           line-height: 1.6; font-variant-numeric: tabular-nums; }
    #hud small { display: block; color: #c9d9e5; }
  </style>
</head>
<body>
  <div id="hud">
    <strong>RING SPRINT</strong><br>
    Lap: <span id="lap">0.00 s</span><br>
    Best: <span id="best">—</span>
    <small>↑ / W accelerate · ↓ / S brake<br>
    ← / A and → / D steer · R restart lap</small>
  </div>

  <script type="module">
    import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js';

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xa9d9e7);
    const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 350);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    document.body.append(renderer.domElement);

    function resize() {
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(innerWidth, innerHeight);
    }
    addEventListener('resize', resize);
    resize();

    scene.add(new THREE.HemisphereLight(0xffffff, 0x64724c, 2));
    const sun = new THREE.DirectionalLight(0xffefd0, 2);
    sun.position.set(-25, 40, 15);
    scene.add(sun);

    function mesh(geometry, color, x, y, z, parent = scene) {
      const object = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({ color }));
      object.position.set(x, y, z);
      parent.add(object);
      return object;
    }

    const TAU = 2 * Math.PI;
    const inner = 25, outer = 39, middle = (inner + outer) / 2;
    const segments = 64;
    mesh(new THREE.BoxGeometry(240, 1, 240), 0x719f54, 0, -0.55, 0);
    const road = mesh(new THREE.RingGeometry(inner, outer, segments), 0x343b48, 0, 0, 0);
    road.rotation.x = -Math.PI / 2;

    for (let i = 0; i < segments; i++) {
      const angle = (i + 0.5) * TAU / segments;
      for (const radius of [inner, outer]) {
        const curb = mesh(new THREE.BoxGeometry(0.55, 0.18, radius * TAU / segments),
          i % 2 ? 0xf5f1db : 0xef5147,
          radius * Math.cos(angle), 0.06, radius * Math.sin(angle));
        curb.rotation.y = -angle;
      }
    }

    // The checkerboard spans the road at angle zero.
    const tile = (outer - inner) / 14;
    for (let i = 0; i < 14; i++) {
      for (let row = 0; row < 2; row++) {
        mesh(new THREE.BoxGeometry(tile, 0.02, tile),
          (i + row) % 2 ? 0x171d24 : 0xffffff,
          inner + (i + 0.5) * tile, 0.01, (row - 0.5) * tile);
      }
    }

    for (let i = 0; i < 18; i++) {
      const angle = i * TAU / 18;
      const radius = i % 2 ? 19 : 49;
      const x = radius * Math.cos(angle), z = radius * Math.sin(angle);
      mesh(new THREE.BoxGeometry(0.55, 1.6, 0.55), 0x71513d, x, 0.8, z);
      mesh(new THREE.ConeGeometry(1.8, 4 + i % 3, 5), 0x26724d, x, 2.8, z);
    }

    const car = new THREE.Group();
    scene.add(car);
    mesh(new THREE.BoxGeometry(1.65, 0.55, 3), 0xffb629, 0, 0.52, 0, car);
    mesh(new THREE.BoxGeometry(1.2, 0.48, 1.35), 0x253e55, 0, 1, -0.25, car);
    for (const x of [-0.85, 0.85]) {
      for (const z of [-0.96, 0.96]) {
        const wheel = mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.32, 8),
          0x20232a, x, 0.32, z, car);
        wheel.rotation.z = Math.PI / 2;
      }
    }

    const keys = new Set();
    const controls = new Set([
      'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
      'KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyR'
    ]);
    const lap = document.querySelector('#lap');
    const best = document.querySelector('#best');
    const format = seconds => `${seconds.toFixed(2)} s`;

    let angle = 0, radius = middle, speed = 0;
    let started = null, bestTime = Infinity;

    addEventListener('keydown', event => {
      if (!controls.has(event.code)) return;
      event.preventDefault();
      keys.add(event.code);
      if (event.code === 'KeyR' && !event.repeat) {
        angle = speed = 0;
        radius = middle;
        started = null;
      }
    });
    addEventListener('keyup', event => keys.delete(event.code));
    addEventListener('blur', () => keys.clear());

    let previous = performance.now();
    renderer.setAnimationLoop(now => {
      const frame = Math.max(0, (now - previous) / 1000);
      previous = now;
      const dt = Math.min(frame, 0.05);

      const gas = keys.has('ArrowUp') || keys.has('KeyW');
      const brake = keys.has('ArrowDown') || keys.has('KeyS');
      const left = keys.has('ArrowLeft') || keys.has('KeyA');
      const right = keys.has('ArrowRight') || keys.has('KeyD');
      speed = THREE.MathUtils.clamp(speed + (brake ? -36 : gas ? 19 : -6) * dt, 0, 34);

      // Track-constrained steering: left moves outward, right moves inward.
      // scoper: no free-roaming physics; the curbs bound the driving lanes.
      radius = THREE.MathUtils.clamp(
        radius + (Number(left) - Number(right)) * speed * 0.38 * dt,
        inner + 1.3, outer - 1.3
      );

      const step = speed * dt / radius;
      if (step > 0 && started === null) started = now - frame * 1000;
      if (angle + step >= TAU) {
        const crossing = now - frame * 1000 * (1 - (TAU - angle) / step);
        bestTime = Math.min(bestTime, (crossing - started) / 1000);
        best.textContent = format(bestTime);
        started = crossing;
      }
      angle = (angle + step) % TAU;
      lap.textContent = format(started === null ? 0 : (now - started) / 1000);

      const x = radius * Math.cos(angle), z = radius * Math.sin(angle);
      const forwardX = -Math.sin(angle), forwardZ = Math.cos(angle);
      car.position.set(x, 0, z);
      car.rotation.y = -angle;
      camera.position.set(x - forwardX * 10, 6, z - forwardZ * 10);
      camera.lookAt(x + forwardX * 5, 0.6, z + forwardZ * 5);
      renderer.render(scene, camera);
    });
  </script>
</body>
</html>
```

Save as `index.html` and open it in a WebGL-capable browser with an internet connection for the Three.js import. If your browser blocks module imports from local files, serve the folder with `python -m http.server 8000` and open `http://localhost:8000`.

**How I’d verify it** (not run here):

1. Load the page. Check that the track, car, and HUD render with no console errors, and that resizing keeps the view proportional.
2. Hold **W** to accelerate. Check that the timer starts on movement, **A/D** steer between the curbs, and **S** brakes. Stop mid-lap and confirm the timer keeps running.
3. Complete a circuit. Check that Best stays blank until the checkerboard crossing, then records the lap and the current timer rolls over. Drive a slower lap to confirm Best stays unchanged, then a faster one to confirm it updates.
4. Press **R** mid-lap. Check that the car returns to the line, the current timer resets, and Best is preserved. Refresh to confirm Best is session-only.


=============== RESPONSE ambition-game-07 ===============

Save this as `index.html`. It gives keyboard players a low-poly oval racer with a chase camera, a live lap timer, and a best lap that survives reloads when browser storage is available. The maintainer inherits one file and no build step. I reviewed the code statically but could not run it here.

**Data shape.** The car has an unwrapped angle around the oval, a lateral offset, and a signed speed. The lap has a start timestamp and the angle of the next finish crossing. One track function maps angle and offset to a world position for both the road and the car.

| Design | Decision |
|---|---|
| Track-relative steering | Chosen. The car follows the bend while you steer across the road. This keeps the controls simple and makes a full lap distinguishable from rocking across the finish line. |
| Free steering in world coordinates | Not chosen. It would give more control, but it would also require off-track recovery and separate checkpoint logic. |

**Throughput checkpoint**
- **Blocking first steps.** Define the track coordinates and finish rule before building the scene.
- **Independent workstreams.** The HUD layout and scenery can be designed separately once the track shape is fixed.
- **Shared mutable state.** The animation loop owns driving and lap state. Input handlers only maintain the pressed keys and request a reset.
- **Smallest safe decomposition.** One file is enough. The track function is the shared boundary between drawing and driving.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mesa Sprint</title>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; background: #edb882; color: #fff6e7; font: 16px system-ui, sans-serif; }
  canvas { display: block; }
  #hud, #help {
    position: fixed; z-index: 1; left: 16px; padding: 12px 16px;
    background: #201923; border: 1px solid #765a62; border-radius: 12px;
  }
  #hud { top: 16px; }
  h1 { margin: 0 0 8px; font-size: 18px; letter-spacing: .12em; text-transform: uppercase; }
  dl { display: grid; grid-template-columns: auto auto; gap: 4px 24px; margin: 0; }
  dd { margin: 0; text-align: right; font-variant-numeric: tabular-nums; }
  #help { bottom: 16px; right: 16px; width: fit-content; font-size: 13px; line-height: 1.5; }
  #status { display: block; color: #ffcc83; }
</style>
</head>
<body>
<section id="hud" aria-label="Race times">
  <h1>Mesa Sprint</h1>
  <dl>
    <dt>Lap</dt><dd id="lap">1</dd>
    <dt>Current</dt><dd id="current">0:00.000</dd>
    <dt>Best</dt><dd id="best">--</dd>
  </dl>
</section>
<div id="help">
  W / ↑ Accelerate · S / ↓ Brake or reverse<br>
  A D / ← → Steer · R Restart
  <span id="status" role="status">Loading Three.js…</span>
</div>
<script type="module">
const $ = id => document.getElementById(id);
const status = $('status');

try {
  const THREE = await import('https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js');
  start(THREE);
} catch (error) {
  console.error(error);
  status.textContent = 'Could not start. Check your connection and WebGL support.';
}

function start(T) {
  const TAU = Math.PI * 2, A = 44, B = 28, EDGE = 5.5;
  const scene = new T.Scene();
  scene.background = new T.Color(0xedb882);
  scene.fog = new T.FogExp2(0xedb882, .006);
  const camera = new T.PerspectiveCamera(58, 1, .1, 350);
  const renderer = new T.WebGLRenderer({ antialias: true });
  document.body.append(renderer.domElement);

  const resize = () => {
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setSize(innerWidth, innerHeight);
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
  };
  resize();
  window.addEventListener('resize', resize);

  scene.add(new T.HemisphereLight(0xffecd2, 0x84657b, 2));
  const sun = new T.DirectionalLight(0xffe3b8, 2.4);
  sun.position.set(-30, 60, -20);
  scene.add(sun);

  const material = color => new T.MeshStandardMaterial({
    color, flatShading: true, side: T.DoubleSide
  });
  function mesh(parent, geometry, mat, x = 0, y = 0, z = 0) {
    const object = new T.Mesh(geometry, mat);
    object.position.set(x, y, z);
    parent.add(object);
    return object;
  }
  function point(a, offset = 0, y = 0) {
    const c = Math.cos(a), s = Math.sin(a);
    const length = Math.hypot(B * c, A * s);
    return new T.Vector3(A * c + offset * B * c / length, y,
                         B * s + offset * A * s / length);
  }
  function strip(from, to, left, right, y, mat, steps = 1) {
    const positions = [], indices = [];
    for (let i = 0; i <= steps; i++) {
      const a = from + (to - from) * i / steps;
      positions.push(...point(a, left, y).toArray(), ...point(a, right, y).toArray());
      if (i < steps) {
        const j = 2 * i;
        indices.push(j, j + 2, j + 1, j + 1, j + 2, j + 3);
      }
    }
    const geometry = new T.BufferGeometry();
    geometry.setAttribute('position', new T.Float32BufferAttribute(positions, 3));
    geometry.setIndex(indices);
    geometry.computeVertexNormals();
    mesh(scene, geometry, mat);
  }

  mesh(scene, new T.BoxGeometry(500, 1, 500), material(0xc8895e), 0, -.52, 0);
  strip(0, TAU, -EDGE, EDGE, 0, material(0x34333e), 128);
  const cream = material(0xffe3b6), red = material(0xce473d);
  const ink = material(0x171826);
  for (let i = 0; i < 64; i++) {
    const a = i * TAU / 64, b = (i + 1) * TAU / 64;
    const curb = i % 2 ? cream : red;
    strip(a, b, -5.5, -5.1, .016, curb, 2);
    strip(a, b, 5.1, 5.5, .016, curb, 2);
    if (i) strip(a, a + .034, -.055, .055, .018, cream);
  }
  for (let row = 0; row < 2; row++) {
    for (let i = 0; i < 10; i++) {
      strip((row - 1) * .023, row * .023, -5 + i, -4 + i, .025,
            (i + row) % 2 ? cream : ink);
    }
  }

  const rock = [material(0xb75d4b), material(0xd17d52), material(0x944f52)];
  const boulder = new T.DodecahedronGeometry(1);
  for (let i = 0; i < 36; i++) {
    const outside = i >= 14;
    const p = point(i * 2.399963, outside ? 14 + (i % 6) * 5 : -12 - (i % 4));
    const h = 1.4 + (i % 7) * .7;
    const object = mesh(scene, boulder, rock[i % 3], p.x, h * .45, p.z);
    object.scale.set(1.1 + i % 3, h, 1.2 + i % 2);
    object.rotation.y = i;
  }

  const car = new T.Group();
  scene.add(car);
  const paint = material(0x37d6c1);
  mesh(car, new T.BoxGeometry(1.55, .45, 2.8), paint, 0, .57, 0);
  mesh(car, new T.BoxGeometry(1.1, .42, 1.14), ink, 0, .99, -.15);
  mesh(car, new T.BoxGeometry(1.68, .12, .37), paint, 0, .94, -1.17);
  const wheel = new T.CylinderGeometry(.33, .33, .25, 8);
  for (const x of [-.79, .79]) {
    for (const z of [-.91, .91]) {
      mesh(car, wheel, ink, x, .34, z).rotation.z = Math.PI / 2;
    }
    mesh(car, new T.BoxGeometry(.28, .14, .06), red, x * .7, .62, -1.42);
  }

  const codes = new Set([
    'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyR'
  ]);
  const keys = new Set();
  let restart = false;
  window.addEventListener('keydown', e => {
    if (!codes.has(e.code)) return;
    e.preventDefault();
    keys.add(e.code);
    if (e.code === 'KeyR' && !e.repeat) restart = true;
  });
  window.addEventListener('keyup', e => keys.delete(e.code));
  window.addEventListener('blur', () => keys.clear());
  const held = (a, b) => keys.has(a) || keys.has(b);

  const storageKey = 'mesa-sprint-best-ms-v1';
  let best = Infinity;
  try {
    const saved = Number(localStorage.getItem(storageKey));
    if (Number.isFinite(saved) && saved > 0) best = saved;
  } catch {}

  function format(ms) {
    ms = Math.floor(ms);
    return `${Math.floor(ms / 60000)}:${String(Math.floor(ms / 1000) % 60).padStart(2, '0')}.${String(ms % 1000).padStart(3, '0')}`;
  }

  let angle = 0, offset = 0, speed = 0;
  let started = null, finish = TAU, lap = 1;
  let previous = performance.now();
  $('best').textContent = best < Infinity ? format(best) : '--';
  status.textContent = 'Press accelerate to start the clock.';

  function frame(now) {
    const dt = Math.min(.05, Math.max(0, (now - previous) / 1000));
    previous = now;
    const snap = restart;
    if (restart) {
      angle = offset = speed = 0;
      started = null;
      finish = TAU;
      lap = 1;
      $('lap').textContent = lap;
      status.textContent = 'Press accelerate to start the clock.';
      restart = false;
    }

    const throttle = held('KeyW', 'ArrowUp');
    const brake = held('KeyS', 'ArrowDown');
    if (started === null && throttle && !brake && !snap) {
      started = now;
      status.textContent = 'Lap 1 in progress.';
    }

    const steer = Number(held('KeyA', 'ArrowLeft')) -
                  Number(held('KeyD', 'ArrowRight'));
    if (started !== null) {
      const drive = Number(throttle) - Number(brake);
      if (drive) speed += drive * (drive < 0 && speed > 0 ? 40 : 22) * dt;
      else speed *= Math.exp(-1.35 * dt);
      speed = T.MathUtils.clamp(speed, -10, 38);

      const limit = EDGE - .95;
      const nextOffset = offset + steer * speed * .24 * dt;
      if (Math.abs(nextOffset) > limit) speed *= Math.exp(-2.8 * dt);
      offset = T.MathUtils.clamp(nextOffset, -limit, limit);

      const c = Math.cos(angle), s = Math.sin(angle);
      const tangentLength = Math.hypot(A * s, B * c);
      const laneLength = tangentLength + offset * A * B / (tangentLength ** 2);
      angle += speed * dt / laneLength;

      if (angle >= finish) {
        const time = now - started;
        const record = time < best;
        if (record) {
          best = time;
          $('best').textContent = format(best);
          try { localStorage.setItem(storageKey, String(best)); } catch {}
        }
        status.textContent = `${record ? 'New best' : 'Last lap'} · ${format(time)}`;
        started = now;
        finish += TAU;
        $('lap').textContent = ++lap;
      }
    }
    $('current').textContent = format(started === null ? 0 : now - started);

    const forward = point(angle + .001, offset).sub(point(angle, offset)).normalize();
    car.position.copy(point(angle, offset, .03));
    car.rotation.y = Math.atan2(forward.x, forward.z) - steer * .14 *
                     Math.min(1, Math.abs(speed) / 12);

    const eye = car.position.clone().addScaledVector(forward, -9);
    eye.y += 5.5;
    camera.position.lerp(eye, snap ? 1 : 1 - Math.exp(-8 * dt));
    const look = car.position.clone().addScaledVector(forward, 7);
    look.y += 1;
    camera.lookAt(look);
    renderer.render(scene, camera);
  }

  camera.position.copy(point(0, 0, 5.5));
  camera.position.z -= 9;
  renderer.setAnimationLoop(frame);
}
</script>
</body>
</html>
```

### How I would verify it

Serve `index.html` over HTTP. For example, run `python3 -m http.server 8000` in its directory and open `http://localhost:8000`. The pinned Three.js import requires an internet connection.

1. **Load and resize.** Check that the road, car, and HUD appear without console errors. Resize to a narrow window and check that the HUD and controls stay readable.
2. **Drive a full lap.** Confirm the clock stays at zero until acceleration. Try both key sets, steer into a curb, and brake into reverse. Cross the finish after one full circuit. Expect lap 2, a restarted current timer, and a recorded best.
3. **Test the finish rule.** Reverse across the finish and drive forward over it again. Expect no new lap until you reach the next full-circuit mark.
4. **Test records and reset.** Drive a slower lap and check that the best stays unchanged. Press R and check that the car and current timer reset while the best remains. Reload at the same URL and check that the best returns.
5. **Test focus loss.** Hold accelerate, switch tabs, release the key, and return. Expect no stuck throttle. Elapsed lap time includes time spent away.

**Principles applied.** *Model the domain* led to unwrapped progress and one next-finish threshold. *Boundary discipline* led to validating saved times and keeping storage failures out of the driving loop. *Prove it works* led to browser checks for full laps, false crossings, and reloads rather than treating static review as a pass. Browser verification remains open. No repository, commit, or PR was part of this delivery.


=============== RESPONSE ambition-game-08 ===============

Save the code below as `index.html`. It gives you a keyboard time trial on one closed oval, with a live lap timer and a best lap saved in the browser. Three.js is the only dependency. I reviewed the code by inspection but could not run it here.

**Data shape and design.** The track is an oval with a centerline and a width. The car has an angle around the oval, a lateral offset, and a speed. The clock has a nullable start time, a completed-lap count, and a nullable best time.

| Design considered | Decision by inspection |
|---|---|
| Free steering on an open ground plane | Would give the player more control, but needs off-track recovery and checkpoint validation. |
| Track-relative steering | Chosen. The car follows the oval while the player steers across the road. Gravel slows the car, and completing a forward circuit is the only way to score a lap. |

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mesa Circuit</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: #151b22;
      color: #fff6e5;
      font: 16px system-ui, sans-serif;
    }
    header {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: .8rem 2rem;
      padding: 1rem clamp(.75rem, 4vw, 2rem);
    }
    h1 { margin: 0; font-size: 1.5rem; }
    .eyebrow, dt {
      color: #ffcd87;
      font-size: .75rem;
      letter-spacing: .12em;
      text-transform: uppercase;
    }
    dl { display: flex; flex-wrap: wrap; gap: .5rem 1.4rem; margin: 0; }
    dd { margin: .15rem 0 0; font-variant-numeric: tabular-nums; }
    #view {
      display: grid;
      place-items: center;
      height: clamp(240px, 68vh, 800px);
      background: #a4cecf;
      color: #151b22;
    }
    canvas { display: block; width: 100%; height: 100%; min-height: 0; }
    footer { padding: .8rem clamp(.75rem, 4vw, 2rem); line-height: 1.6; }
    kbd { color: #ffcd87; font: inherit; font-weight: 700; }
  </style>
</head>
<body>
  <header>
    <div><div class="eyebrow">Desert time trial</div><h1>Mesa Circuit</h1></div>
    <dl>
      <div><dt>Lap time</dt><dd id="time">0:00.000</dd></div>
      <div><dt>Best lap</dt><dd id="best">None yet</dd></div>
      <div><dt>Completed</dt><dd id="laps">0</dd></div>
    </dl>
  </header>
  <main id="view" aria-label="Mesa Circuit race view">
    <p id="loading" role="status">Loading circuit…</p>
  </main>
  <footer>
    <kbd>↑ / W</kbd> accelerate · <kbd>↓ / S</kbd> brake ·
    <kbd>← / A</kbd> and <kbd>→ / D</kbd> steer · <kbd>R</kbd> restart
  </footer>

  <script type="module">
    const view = document.querySelector('#view');
    const loading = document.querySelector('#loading');

    try {
      const THREE = await import(
        'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js'
      );
      start(THREE);
    } catch (error) {
      loading.textContent =
        'Could not start the game. Check your connection and WebGL support, then reload.';
      console.error(error);
    }

    function start(T) {
      const tau = Math.PI * 2;
      const track = { x: 41, z: 26, half: 5, segments: 128 };
      const car = { angle: 0, offset: 0, speed: 0 };
      const storeKey = 'mesa-circuit.best.v1';
      const race = { start: null, laps: 0, best: null };
      try {
        const saved = Number(localStorage.getItem(storeKey));
        if (Number.isFinite(saved) && saved > 0) race.best = saved;
      } catch {}

      const time = document.querySelector('#time');
      const best = document.querySelector('#best');
      const laps = document.querySelector('#laps');
      const reduced = matchMedia('(prefers-reduced-motion: reduce)');
      const scene = new T.Scene();
      scene.background = new T.Color(0xa4cecf);
      scene.fog = new T.Fog(0xa4cecf, 110, 235);
      const renderer = new T.WebGLRenderer({ antialias: true });
      renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
      renderer.domElement.setAttribute('aria-label', 'Low-poly race track');
      scene.add(new T.HemisphereLight(0xffefd0, 0x9a5740, 2.1));
      const sun = new T.DirectionalLight(0xffddb3, 2);
      sun.position.set(-35, 60, -20);
      scene.add(sun);

      function mesh(parent, geometry, color, x, y, z) {
        const object = new T.Mesh(geometry, new T.MeshStandardMaterial({
          color, flatShading: true, side: T.DoubleSide
        }));
        object.position.set(x, y, z);
        parent.add(object);
        return object;
      }

      function box(parent, color, x, y, z, w, h, d) {
        return mesh(parent, new T.BoxGeometry(w, h, d), color, x, y, z);
      }

      function point(angle, offset, y) {
        return [(track.x + offset) * Math.cos(angle), y,
                (track.z + offset) * Math.sin(angle)];
      }

      function strip(inner, outer, y, color, from = 0, to = track.segments) {
        const vertices = [];
        for (let i = from; i < to; i++) {
          const a = i * tau / track.segments;
          const b = (i + 1) * tau / track.segments;
          const p = point(a, inner, y), q = point(a, outer, y);
          const r = point(b, inner, y), s = point(b, outer, y);
          vertices.push(...p, ...r, ...q, ...q, ...r, ...s);
        }
        const geometry = new T.BufferGeometry();
        geometry.setAttribute('position', new T.Float32BufferAttribute(vertices, 3));
        geometry.computeVertexNormals();
        mesh(scene, geometry, color, 0, 0, 0);
      }

      box(scene, 0xcf9563, 0, -.52, 0, 400, 1, 400);
      strip(-7, 7, 0, 0xa86b42);
      strip(-track.half, track.half, .02, 0x343942);
      strip(-5, -4.8, .035, 0xffe2a6);
      strip(4.8, 5, .035, 0xffe2a6);
      for (let i = 4; i < track.segments; i += 5) {
        strip(-.08, .08, .035, 0xd3ae72, i, i + 2);
      }
      for (let row = 0; row < 2; row++) {
        for (let col = 0; col < 10; col++) {
          box(scene, (row + col) % 2 ? 0x19212a : 0xfff3db,
              track.x - 4.5 + col, .045, (row - .5) * .65, 1, .025, .65);
        }
      }

      for (let i = 0; i < 27; i++) {
        const angle = i * 2.39996;
        const radius = i < 11 ? 6 + i * .95 : 56 + i % 7 * 4;
        const height = 2 + i % 6;
        const rock = mesh(scene, new T.CylinderGeometry(
          .7 + i % 3, 2 + i % 4, height, 5
        ), i % 2 ? 0xbb6748 : 0xde905c,
        Math.cos(angle) * radius, height / 2 - .02, Math.sin(angle) * radius);
        rock.rotation.y = angle;
      }

      const vehicle = new T.Group();
      scene.add(vehicle);
      box(vehicle, 0xe83f2e, 0, .56, 0, 1.9, .53, 3.4);
      box(vehicle, 0x293e50, 0, 1, -.28, 1.43, .48, 1.55);
      box(vehicle, 0xffdc81, 0, .84, 1.04, .28, .04, 1.05);
      box(vehicle, 0xe83f2e, 0, 1.04, -1.42, 2.05, .14, .37);
      for (const x of [-.96, .96]) {
        for (const z of [-1.04, 1.04]) {
          const wheel = mesh(vehicle, new T.CylinderGeometry(.34, .34, .32, 9),
                             0x171c22, x, .35, z);
          wheel.rotation.z = Math.PI / 2;
        }
      }

      const chase = new T.PerspectiveCamera(58, 1, .1, 300);
      const overview = new T.OrthographicCamera(-1, 1, 1, -1, .1, 300);
      overview.position.set(0, 100, 60);
      overview.lookAt(0, 0, 0);
      const forward = new T.Vector3();

      function draw() {
        vehicle.position.set(...point(car.angle, car.offset, .055));
        forward.set(-(track.x + car.offset) * Math.sin(car.angle), 0,
                      (track.z + car.offset) * Math.cos(car.angle)).normalize();
        vehicle.rotation.y = Math.atan2(forward.x, forward.z);
        chase.position.copy(vehicle.position).addScaledVector(forward, -8);
        chase.position.y += 4.5;
        chase.lookAt(vehicle.position.x + forward.x * 6, .8,
                     vehicle.position.z + forward.z * 6);

        const aspect = view.clientWidth / Math.max(1, view.clientHeight);
        if (chase.aspect !== aspect || renderer.domElement.clientWidth !== view.clientWidth ||
            renderer.domElement.clientHeight !== view.clientHeight) {
          resize();
        }
        renderer.render(scene, reduced.matches ? overview : chase);
      }

      function resize() {
        const w = Math.max(1, view.clientWidth);
        const h = Math.max(1, view.clientHeight);
        const aspect = w / h;
        renderer.setSize(w, h, false);
        chase.aspect = aspect;
        chase.updateProjectionMatrix();
        const halfHeight = Math.max(38, 53 / aspect);
        overview.left = -halfHeight * aspect;
        overview.right = halfHeight * aspect;
        overview.top = halfHeight;
        overview.bottom = -halfHeight;
        overview.updateProjectionMatrix();
      }

      function format(ms) {
        const n = Math.floor(ms);
        const minutes = Math.floor(n / 60000);
        const seconds = String(Math.floor(n / 1000) % 60).padStart(2, '0');
        return `${minutes}:${seconds}.${String(n % 1000).padStart(3, '0')}`;
      }

      function showResults() {
        best.textContent = race.best === null ? 'None yet' : format(race.best);
        laps.textContent = race.laps;
      }

      const keys = new Set();
      const controls = new Set([
        'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
        'KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyR'
      ]);
      const held = (a, b) => Number(keys.has(a) || keys.has(b));
      addEventListener('keydown', event => {
        if (!controls.has(event.code) || event.ctrlKey || event.metaKey || event.altKey) return;
        event.preventDefault();
        keys.add(event.code);
        if (event.code === 'KeyR' && !event.repeat) {
          Object.assign(car, { angle: 0, offset: 0, speed: 0 });
          race.start = null;
          race.laps = 0;
          showResults();
        }
      });
      addEventListener('keyup', event => keys.delete(event.code));
      addEventListener('blur', () => keys.clear());
      document.addEventListener('visibilitychange', () => keys.clear());

      function drive(dt, now) {
        const throttle = held('ArrowUp', 'KeyW');
        const brake = held('ArrowDown', 'KeyS');
        const steer = held('ArrowRight', 'KeyD') - held('ArrowLeft', 'KeyA');
        const gravel = Math.abs(car.offset) > track.half - .65;
        const limit = gravel ? 12 : 34;
        const accel = brake ? -35 : throttle ? 18 : -8;
        car.speed = T.MathUtils.clamp(
          car.speed + (car.speed > limit ? Math.min(accel, -24) : accel) * dt, 0, 34
        );
        if (car.speed <= limit) car.speed = Math.min(car.speed, limit);
        if (car.speed === 0 || dt === 0) return;

        const stepStart = now - dt * 1000;
        race.start ??= stepStart;
        const old = car.angle;
        const radius = Math.hypot(
          (track.x + car.offset) * Math.sin(old),
          (track.z + car.offset) * Math.cos(old)
        );
        const advance = car.speed * dt / radius;
        car.angle += advance;
        car.offset = T.MathUtils.clamp(
          car.offset - steer * Math.min(8, car.speed * .45) * dt, -6.5, 6.5
        );
        if (car.angle < tau) return;

        const crossedAt = stepStart + (tau - old) / advance * dt * 1000;
        const result = crossedAt - race.start;
        car.angle -= tau;
        race.start = crossedAt;
        race.laps++;
        if (race.best === null || result < race.best) {
          race.best = result;
          try { localStorage.setItem(storeKey, String(result)); } catch {}
        }
        showResults();
      }

      let previous = performance.now();
      function frame(now) {
        const dt = Math.min(.05, Math.max(0, (now - previous) / 1000));
        previous = now;
        drive(dt, now);
        const label = format(race.start === null ? 0 : now - race.start);
        if (time.textContent !== label) time.textContent = label;
        draw();
        requestAnimationFrame(frame);
      }

      view.append(renderer.domElement);
      resize();
      draw();
      loading.remove();
      showResults();
      requestAnimationFrame(frame);
    }
  </script>
</body>
</html>
```

## How I would verify it

Serve the directory over HTTP. For example, if Python is installed, run `python -m http.server 8000` there and open `http://localhost:8000`. The browser needs WebGL and internet access to load Three.js.

| Browser check | Expected result, inferred from the code |
|---|---|
| Load the page and open DevTools. | The track and car appear. The timer reads `0:00.000`, and a fresh browser profile shows `None yet`. There are no console errors. |
| Hold Up or W, steer both ways, then brake. | The car accelerates, crosses the road in the expected direction, slows on gravel, and brakes to a stop. The timer starts on movement and keeps counting while stopped. |
| Complete one circuit, then drive a deliberately slower second lap. | The first finish sets the best. The second increments the count but leaves the best unchanged. The live timer rolls over at each finish. |
| Press R mid-lap, then reload. | R resets the car, timer, and session lap count. The best survives both R and reload when browser storage is available. |
| Switch tabs while holding throttle, then return. | The car does not keep accelerating from a stuck key. The lap clock still includes time away. |
| Try a 320 px viewport, 200% zoom, and reduced motion. | HUD text wraps without clipping. Reduced motion uses a fixed overview instead of a moving chase camera. |
| Block the CDN and reload. | The loading message changes to a recovery message instead of staying on “Loading circuit…”. |

**Throughput checkpoint.** Blocking first step: choose the track and lap model. Independent workstreams: none, because the deliverable is one file. Shared mutable state: one animation loop advances the race, and restart runs between frames. Smallest safe decomposition: one HTML file with separate input, simulation, and rendering functions. Subagent review and browser verification were unavailable here.

**Principles used.** *Model the domain* led to track-relative progress and an explicit idle clock. *Prove it works* led to browser checks for controls, lap rollover, and persistence rather than treating source inspection as a pass. No open decisions are required to try the game.


=============== RESPONSE ambition-game-09 ===============

Save this as `index.html`. It gives you a keyboard-controlled time trial on one closed, low-poly circuit, with a chase camera, a live lap timer, and a best lap saved in the browser. The whole game is in one file. I reviewed the code by inspection but did not run it.

**Data shape and design.** The track is a closed curve sampled by distance. The car stores distance around the track, sideways offset, sideways velocity, and speed. The clock stores the current lap's start time and the best completed time.

| Design considered | Decision |
|---|---|
| Free steering on a road mesh | Rejected by inspection. It needs road detection and checkpoint logic to distinguish a valid lap from a shortcut. |
| Steering across a loop indexed by distance | Chosen. It gives the player room to steer and run wide, while a lap requires covering the whole loop. The tradeoff is that the car follows the track's direction rather than turning freely. |

**Throughput checkpoint**
1. **Blocking first steps.** Settle track coordinates and the lap boundary before wiring the car, camera, and HUD.
2. **Independent workstreams.** Rendering and timing can be checked separately against the same track model.
3. **Shared mutable state.** The frame loop owns the race state. The HUD reads it, and storage receives only a new best.
4. **Smallest safe decomposition.** One HTML file is enough. No build step, asset pipeline, or server-side code.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pine Loop | Arcade Time Trial</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      overflow: hidden;
      color: #fff8e8;
      background: #162b31;
      font: 16px system-ui, sans-serif;
    }
    canvas { display: block; }
    #hud {
      position: absolute;
      top: 16px;
      left: 16px;
      max-width: calc(100vw - 32px);
      padding: 12px 16px;
      border: 1px solid #56706e;
      border-radius: 12px;
      background: #14252c;
      pointer-events: none;
    }
    h1 {
      margin: 0 0 8px;
      color: #ffd477;
      font-size: 1rem;
      letter-spacing: .16em;
      text-transform: uppercase;
    }
    dl { display: flex; flex-wrap: wrap; gap: 8px 20px; margin: 0; }
    dt { color: #c4d6d5; font-size: .75rem; }
    dd {
      margin: 0;
      min-width: 4ch;
      font-weight: 700;
      font-variant-numeric: tabular-nums;
    }
    #help { margin: 8px 0 0; color: #c4d6d5; font-size: .75rem; }
    #error { position: absolute; bottom: 16px; left: 16px; right: 16px; }
  </style>
</head>
<body>
  <section id="hud" aria-label="Race dashboard">
    <h1>Pine Loop</h1>
    <dl>
      <div><dt>Lap</dt><dd id="lap">0:00.000</dd></div>
      <div><dt>Best</dt><dd id="best">--:--.---</dd></div>
      <div><dt>Speed</dt><dd id="speed">0 km/h</dd></div>
    </dl>
    <p id="help">W / ↑ accelerate · S / ↓ brake · A D / ← → steer · R restart</p>
  </section>
  <p id="error" role="alert" hidden></p>

  <script type="module">
    async function main() {
      const T = await import("https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js");
      const scene = new T.Scene();
      scene.background = new T.Color(0xb6dce4);
      scene.fog = new T.FogExp2(0xb6dce4, 0.004);
      const camera = new T.PerspectiveCamera(62, 1, 0.1, 500);
      const renderer = new T.WebGLRenderer({ antialias: true });
      renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
      renderer.domElement.setAttribute("aria-label", "Pine Loop race track");
      document.body.prepend(renderer.domElement);

      function resize() {
        camera.aspect = innerWidth / innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(innerWidth, innerHeight);
      }
      window.addEventListener("resize", resize);
      resize();

      scene.add(new T.HemisphereLight(0xfff6dc, 0x62777a, 2));
      const sun = new T.DirectionalLight(0xffe0b1, 2);
      sun.position.set(-50, 75, -30);
      scene.add(sun);

      const material = color => new T.MeshStandardMaterial({
        color, roughness: 0.92, flatShading: true, side: T.DoubleSide
      });

      function mesh(geometry, mat, parent, x, y, z) {
        const object = new T.Mesh(geometry, mat);
        object.position.set(x, y, z);
        parent.add(object);
        return object;
      }

      const ground = mesh(new T.PlaneGeometry(550, 550), material(0x729157),
        scene, 0, -0.08, 0);
      ground.rotation.x = -Math.PI / 2;

      const curve = new T.CatmullRomCurve3([
        [0, 60], [52, 60], [83, 31], [71, -7], [89, -46],
        [39, -69], [-2, -49], [-49, -70], [-83, -37], [-74, 14], [-54, 55]
      ].map(([x, z]) => new T.Vector3(x, 0, z)), true);
      curve.arcLengthDivisions = 2048;
      const length = curve.getLength();
      const halfRoad = 6;
      const wrap = d => ((d % length) + length) % length;

      function frameAt(distance) {
        const u = wrap(distance) / length;
        const center = curve.getPointAt(u);
        const forward = curve.getTangentAt(u);
        const right = new T.Vector3(-forward.z, 0, forward.x);
        return { center, forward, right };
      }

      function strip(from, to, left, right, height, mat, segments) {
        const vertices = [], indices = [];
        for (let i = 0; i <= segments; i++) {
          const f = frameAt(T.MathUtils.lerp(from, to, i / segments));
          for (const offset of [left, right]) {
            const p = f.center.clone().addScaledVector(f.right, offset);
            vertices.push(p.x, height, p.z);
          }
          if (i < segments) {
            const j = i * 2;
            indices.push(j, j + 1, j + 2, j + 1, j + 3, j + 2);
          }
        }
        const geometry = new T.BufferGeometry();
        geometry.setAttribute("position", new T.Float32BufferAttribute(vertices, 3));
        geometry.setIndex(indices);
        geometry.computeVertexNormals();
        mesh(geometry, mat, scene, 0, 0, 0);
      }

      const asphalt = material(0x303c47);
      const gravel = material(0xa89774);
      const cream = material(0xfff1d3);
      const red = material(0xe25544);
      const dark = material(0x19242d);
      const segments = Math.ceil(length / 2);
      strip(0, length, -9, 9, 0, gravel, segments);
      strip(0, length, -halfRoad, halfRoad, 0.02, asphalt, segments);
      for (const side of [-1, 1]) {
        const left = side < 0 ? -6.55 : 6;
        for (let i = 0; i < 120; i++) {
          strip(length * i / 120, length * (i + 1) / 120,
            left, left + 0.55, 0.04, i % 2 ? cream : red, 3);
        }
      }
      for (let row = 0; row < 2; row++) {
        for (let col = 0; col < 12; col++) {
          strip((row - 1) * 0.65, row * 0.65, col - 6, col - 5,
            0.05, (row + col) % 2 ? cream : dark, 1);
        }
      }

      const trunk = new T.CylinderGeometry(0.22, 0.34, 1.8, 5);
      const crown = new T.ConeGeometry(1.65, 4, 5);
      const bark = material(0x674c39);
      const needles = [material(0x285e49), material(0x397451)];
      const samples = Array.from({ length: segments }, (_, i) =>
        frameAt(i * length / segments).center);
      let seed = 42;
      function random() {
        seed = (Math.imul(1664525, seed) + 1013904223) >>> 0;
        return seed / 4294967296;
      }
      for (let i = 0; i < 240; i++) {
        const x = (random() - 0.5) * 245;
        const z = (random() - 0.5) * 220;
        if (samples.some(p => (p.x - x) ** 2 + (p.z - z) ** 2 < 13 ** 2)) continue;
        const scale = 0.75 + random() * 0.9;
        mesh(trunk, bark, scene, x, 0.9 * scale, z).scale.setScalar(scale);
        mesh(crown, needles[i % 2], scene, x, 3.25 * scale, z).scale.setScalar(scale);
      }

      const car = new T.Group();
      scene.add(car);
      mesh(new T.BoxGeometry(1.9, 0.58, 3.6), red, car, 0, 0.65, 0);
      mesh(new T.BoxGeometry(1.38, 0.55, 1.65), dark, car, 0, 1.18, -0.22);
      mesh(new T.BoxGeometry(1.1, 0.10, 1.3), cream, car, 0, 1.49, -0.22);
      mesh(new T.BoxGeometry(1.9, 0.17, 0.28), dark, car, 0, 1.08, -1.58);
      const tire = new T.CylinderGeometry(0.37, 0.37, 0.34, 10);
      for (const x of [-0.97, 0.97]) {
        for (const z of [-1.13, 1.13]) {
          mesh(tire, dark, car, x, 0.37, z).rotation.z = Math.PI / 2;
        }
      }

      const lapEl = document.getElementById("lap");
      const bestEl = document.getElementById("best");
      const speedEl = document.getElementById("speed");
      const bestKey = "pine-loop.best-ms.v1";
      let best = Infinity;
      try {
        const saved = Number(localStorage.getItem(bestKey));
        if (Number.isFinite(saved) && saved > 0) best = saved;
      } catch {}

      function format(ms) {
        if (!Number.isFinite(ms)) return "--:--.---";
        const n = Math.floor(ms);
        return `${Math.floor(n / 60000)}:${String(Math.floor(n / 1000) % 60)
          .padStart(2, "0")}.${String(n % 1000).padStart(3, "0")}`;
      }

      const keys = new Set();
      const controls = new Set([
        "KeyW", "KeyA", "KeyS", "KeyD",
        "ArrowUp", "ArrowLeft", "ArrowDown", "ArrowRight", "KeyR"
      ]);
      const held = (a, b) => keys.has(a) || keys.has(b);
      const freshRace = () => ({ distance: 0, offset: 0, lateral: 0, speed: 0, started: null });
      let race = freshRace();
      let snapCamera = true;

      window.addEventListener("keydown", event => {
        if (!controls.has(event.code)) return;
        event.preventDefault();
        keys.add(event.code);
        if (event.code === "KeyR" && !event.repeat) {
          race = freshRace();
          snapCamera = true;
        }
      });
      window.addEventListener("keyup", event => keys.delete(event.code));
      window.addEventListener("blur", () => keys.clear());
      document.addEventListener("visibilitychange", () => keys.clear());

      function advance(dt, now) {
        const gas = held("KeyW", "ArrowUp");
        const brake = held("KeyS", "ArrowDown");
        const steering = Number(held("KeyD", "ArrowRight")) -
          Number(held("KeyA", "ArrowLeft"));
        const offRoad = Math.abs(race.offset) > halfRoad - 0.7;
        const limit = offRoad ? 15 : 48;
        const acceleration = brake ? -38 : gas ? 19 : -8;
        race.speed = Math.max(0, race.speed + acceleration * dt);
        if (race.speed > limit) race.speed = Math.max(limit, race.speed - 33 * dt);

        const target = steering * 9 * Math.min(1, race.speed / 16);
        race.lateral = T.MathUtils.lerp(race.lateral, target, 1 - Math.exp(-9 * dt));
        race.offset = T.MathUtils.clamp(race.offset + race.lateral * dt, -8, 8);

        const travel = race.speed * dt;
        if (travel <= 0) return;
        race.started ??= now - dt * 1000;
        const remaining = length - race.distance;
        race.distance += travel;
        if (race.distance >= length) {
          const crossed = now - (1 - remaining / travel) * dt * 1000;
          const elapsed = crossed - race.started;
          if (elapsed < best) {
            best = elapsed;
            try { localStorage.setItem(bestKey, String(best)); } catch {}
          }
          race.distance -= length;
          race.started = crossed;
        }
      }

      let previous;
      function tick(now) {
        const dt = Math.min((now - (previous ?? now)) / 1000, 0.05);
        previous = now;
        advance(dt, now);

        const { center, forward, right } = frameAt(race.distance);
        car.position.copy(center).addScaledVector(right, race.offset);
        // The car's nose points along local +Z, so screen-right is local -X.
        car.rotation.y = Math.atan2(forward.x, forward.z) -
          Math.atan2(race.lateral, Math.max(6, race.speed));

        const eye = car.position.clone().addScaledVector(forward, -11);
        eye.y = 5.7;
        camera.position.lerp(eye, snapCamera ? 1 : 1 - Math.exp(-9 * dt));
        snapCamera = false;
        const aim = car.position.clone().addScaledVector(forward, 7);
        aim.y = 0.7;
        camera.lookAt(aim);

        lapEl.textContent = format(race.started === null ? 0 : now - race.started);
        bestEl.textContent = format(best);
        speedEl.textContent = `${Math.round(race.speed * 3.6)} km/h`;
        renderer.render(scene, camera);
        requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    }

    main().catch(error => {
      console.error(error);
      const message = document.getElementById("error");
      message.textContent = "Could not start Pine Loop. Check your connection and WebGL support.";
      message.hidden = false;
    });
  </script>
</body>
</html>
```

## How I'd verify it

From the directory containing `index.html`, run `python3 -m http.server 8000` and visit `http://localhost:8000`. The page needs internet access to load the pinned Three.js module.

| Browser check | Expected result |
|---|---|
| Load with DevTools open, then resize the window | The car, track, and HUD appear with no console errors. The scene keeps its proportions and the HUD stays in view. |
| Drive with both key sets | W or Up accelerates. S or Down brakes. A/D and Left/Right move the car in the corresponding screen direction. The gravel shoulder cuts top speed. |
| Complete the first lap | The timer starts on movement. The best stays blank until the car returns to the checkerboard, then records the lap once and starts timing the next one. |
| Complete a slower lap and then a faster one | The slower lap leaves the best unchanged. The faster lap replaces it. Reloading on the same origin retains it. |
| Press R mid-lap | The car returns to the line and the current timer clears. The best stays intact. Holding a drive key can start the next run immediately. |
| Switch tabs while holding throttle, then release it | The throttle does not stick on return. The clock counts time away, so leaving the tab cannot improve a lap. |

**Principles applied:** **Model the domain** led to distance and lateral offset as the race coordinates. **Boundary discipline** led to validating the stored time and handling unavailable storage without stopping the game. **Prove it works** led to browser checks for controls, the finish line, and persistence rather than treating code inspection as a pass.

**Open decisions:** None required to run it. The track-following steering is an intentional arcade choice. Browser behavior and driving feel are unverified.


=============== RESPONSE ambition-game-10 ===============

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sunset Circuit</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; overflow: hidden; background: #f8c99b; color: #fff; font: 16px system-ui, sans-serif; }
    canvas { display: block; }
    #hud { position: fixed; top: 16px; left: 16px; padding: 14px 18px; background: #172332ee; border-radius: 10px; font-variant-numeric: tabular-nums; }
    h1 { margin: 0 0 8px; font-size: 18px; }
    #hud div { display: flex; justify-content: space-between; gap: 24px; }
    small { display: block; margin-top: 10px; color: #cbd5e1; }
  </style>
</head>
<body>
  <section id="hud" aria-label="Race information">
    <h1>Sunset Circuit</h1>
    <div>Lap time <strong id="lap">0:00.000</strong></div>
    <div>Best lap <strong id="best">—</strong></div>
    <small>↑ ↓ or W S: drive · ← → or A D: steer</small>
  </section>

  <script type="module">
    import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js';

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf8c99b);
    scene.fog = new THREE.Fog(0xf8c99b, 70, 155);
    const camera = new THREE.PerspectiveCamera(58, 1, 0.1, 200);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    document.body.append(renderer.domElement);

    scene.add(new THREE.HemisphereLight(0xfff1d6, 0x556446, 2));
    const sun = new THREE.DirectionalLight(0xffdfb5, 2);
    sun.position.set(20, 35, 10);
    scene.add(sun);

    function mesh(geometry, color, x, y, z, parent = scene) {
      const object = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({
        color, flatShading: true
      }));
      object.position.set(x, y, z);
      parent.add(object);
      return object;
    }

    function box(w, h, d, color, x, y, z, parent) {
      return mesh(new THREE.BoxGeometry(w, h, d), color, x, y, z, parent);
    }

    const inner = 25, outer = 37, radius = (inner + outer) / 2;
    const tau = 2 * Math.PI;
    const ground = mesh(new THREE.PlaneGeometry(400, 400), 0x72894b, 0, -0.04, 0);
    ground.rotation.x = -Math.PI / 2;

    function ring(from, to, color, y) {
      mesh(new THREE.RingGeometry(from, to, 96), color, 0, y, 0).rotation.x = -Math.PI / 2;
    }

    ring(inner, outer, 0x343945, 0);
    ring(inner, inner + 0.32, 0xf9e7b7, 0.01);
    ring(outer - 0.32, outer, 0xf9e7b7, 0.01);

    for (let i = 0; i < 48; i++) {
      const a = (i + 0.5) * tau / 48;
      box(0.12, 0.02, 1.3, 0xe8d69f, radius * Math.cos(a), 0.013,
        radius * Math.sin(a)).rotation.y = -a;
    }

    // The start/finish stripe lies at angle zero, across the full road.
    for (let i = 0; i < 12; i++) {
      for (let j = 0; j < 2; j++) {
        box(1, 0.025, 0.55, (i + j) % 2 ? 0x181b24 : 0xffffff,
          inner + i + 0.5, 0.02, (j - 0.5) * 0.55);
      }
    }

    for (let i = 0; i < 27; i++) {
      const a = i * 2.39996, r = i % 2 ? 45 + i % 7 : 6 + i % 15;
      const x = r * Math.cos(a), z = r * Math.sin(a);
      box(0.5, 1.7, 0.5, 0x684735, x, 0.85, z);
      mesh(new THREE.ConeGeometry(1.5, 3.6, 5), i % 2 ? 0x325f4e : 0x487752,
        x, 2.7, z);
    }

    const car = new THREE.Group();
    scene.add(car);
    car.position.set(radius, 0, 0);
    box(1.6, 0.46, 2.75, 0xff573d, 0, 0.48, 0, car);
    box(1.22, 0.43, 1.28, 0x203c50, 0, 0.88, -0.22, car);
    for (const x of [-0.82, 0.82]) {
      for (const z of [-0.9, 0.9]) {
        mesh(new THREE.CylinderGeometry(0.29, 0.29, 0.22, 8), 0x181b24,
          x, 0.29, z, car).rotation.z = Math.PI / 2;
      }
      box(0.3, 0.15, 0.06, 0xffedbd, x * 0.72, 0.51, 1.39, car);
    }

    const keys = new Set();
    const controls = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'KeyW', 'KeyA', 'KeyS', 'KeyD'];
    for (const type of ['keydown', 'keyup']) {
      addEventListener(type, event => {
        if (!controls.includes(event.code)) return;
        event.preventDefault();
        if (type === 'keydown') keys.add(event.code);
        else keys.delete(event.code);
      });
    }
    addEventListener('blur', () => keys.clear());
    const pressed = (a, b) => Number(keys.has(a) || keys.has(b));

    const lap = document.querySelector('#lap');
    const best = document.querySelector('#best');
    function time(ms) {
      return `${Math.floor(ms / 60000)}:${(Math.floor(ms) % 60000 / 1000)
        .toFixed(3).padStart(6, '0')}`;
    }

    let speed = 0, heading = 0, angle = 0, progress = 0;
    let previous, started, bestTime = Infinity;
    const follow = new THREE.Vector3();

    function resize() {
      renderer.setSize(innerWidth, innerHeight);
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
    }
    addEventListener('resize', resize);
    resize();

    renderer.setAnimationLoop(now => {
      const dt = Math.min((now - (previous ?? now)) / 1000, 0.05);
      const frameStart = previous ?? now;
      previous = now;

      const throttle = pressed('ArrowUp', 'KeyW') - pressed('ArrowDown', 'KeyS');
      const steer = pressed('ArrowRight', 'KeyD') - pressed('ArrowLeft', 'KeyA');
      speed = THREE.MathUtils.clamp((speed + throttle * 22 * dt) * Math.exp(-0.85 * dt), -8, 21);
      if (throttle && dt > 0) started ??= frameStart;
      heading -= steer * 1.8 * THREE.MathUtils.clamp(speed / 6, -1, 1) * dt;

      const dx = Math.sin(heading), dz = Math.cos(heading);
      const x = car.position.x + dx * speed * dt;
      const z = car.position.z + dz * speed * dt;
      const distance = Math.hypot(x, z);
      const bounded = THREE.MathUtils.clamp(distance, inner + 1.1, outer - 1.1);
      car.position.set(x * bounded / distance, 0, z * bounded / distance);
      if (distance !== bounded) speed *= Math.exp(-5 * dt);
      car.rotation.y = heading;

      // Unwrap the angle so reversing subtracts progress instead of granting laps.
      const nextAngle = Math.atan2(z, x);
      const step = Math.atan2(Math.sin(nextAngle - angle), Math.cos(nextAngle - angle));
      angle = nextAngle;
      if (started !== undefined) {
        progress += step;
        if (progress >= tau) {
          const crossing = now - (now - frameStart) * (progress - tau) / step;
          bestTime = Math.min(bestTime, crossing - started);
          best.textContent = time(bestTime);
          started = crossing;
          progress -= tau;
        }
        lap.textContent = time(now - started);
      }

      follow.set(car.position.x - dx * 8, 5, car.position.z - dz * 8);
      if (dt === 0) camera.position.copy(follow);
      else camera.position.lerp(follow, 1 - Math.exp(-8 * dt));
      camera.lookAt(car.position.x + dx * 4, 0.6, car.position.z + dz * 4);
      renderer.render(scene, camera);
    });
  </script>
</body>
</html>
```

Save as `index.html` and open it in a WebGL-capable browser with internet access. Three.js loads from a CDN; no build step is needed. Best lap is kept until you reload.

**How I’d verify it (not run here):**
1. Open the page and check that the track, car, and HUD render without console errors. Resize the window and check that the view stays proportional.
2. Try both control schemes, including braking and reversing. Confirm the chase camera follows, the car slows at the track edges, and switching tabs while holding a key doesn’t leave it stuck.
3. Drive forward with gentle left turns to complete a lap. Confirm the timer starts when you drive, resets at the stripe after a full circuit, and records a best. Run a slower lap, then a faster one; only the faster lap should replace the best.
4. Reload, reverse across the stripe, then drive forward across it. Confirm that crossing back and forth doesn’t register a lap.


=============== RESPONSE ambition-game-11 ===============

# Mesa Circuit

Save the code below as `index.html`. It gives you one low-poly desert circuit, a chase camera, keyboard steering, a current-lap timer, and a best lap saved in the browser when storage is available. The maintainer gets one file, no build step, and no art assets to download.

**Data shape.** The track has two elliptical edges and four ordered gates. The car has a position, heading, and signed speed. The lap record holds a start timestamp, the next expected gate, and a nullable best time. The road mesh and the off-road check use the same ellipse dimensions.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mesa Circuit</title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0; background: #211b19; color: #fff4df;
    font: 1rem system-ui, sans-serif;
  }
  main { max-width: 78rem; margin: auto; padding: .8rem; }
  header { display: flex; flex-wrap: wrap; align-items: center; gap: .5rem 1.5rem; }
  h1 { margin: 0; font-size: clamp(1.4rem, 4vw, 2.2rem); }
  dl { display: flex; flex-wrap: wrap; gap: .5rem 1.5rem; margin: 0; }
  dt { font-size: .8rem; color: #ffcd8c; }
  dd { margin: 0; font: 700 1.15rem ui-monospace, monospace; }
  #view {
    margin-top: .65rem; height: clamp(14rem, 69vh, 48rem);
    background: #694733; border: 1px solid #a78368; border-radius: .45rem;
    overflow: hidden; display: grid; place-items: center;
  }
  canvas { display: block; }
  #message { padding: 1rem; text-align: center; }
  p { margin: .55rem 0; }
</style>
</head>
<body>
<main>
  <header>
    <h1>Mesa Circuit</h1>
    <dl>
      <div><dt>Current lap</dt><dd id="current">0:00.000</dd></div>
      <div><dt>Best lap</dt><dd id="best">None yet</dd></div>
    </dl>
  </header>
  <div id="view"><p id="message" role="status">Loading the track…</p></div>
  <p id="status" role="status">Cross the checkered line to start.</p>
  <p>W / ↑ accelerate · S / ↓ brake or reverse · A D / ← → steer · R reset</p>
</main>

<script type="module">
const view = document.querySelector('#view');
const message = document.querySelector('#message');
const current = document.querySelector('#current');
const best = document.querySelector('#best');
const status = document.querySelector('#status');

try {
  const THREE = await import('https://cdn.jsdelivr.net/npm/three@0.174.0/build/three.module.js');
  boot(THREE);
} catch (error) {
  message.hidden = false;
  if (!message.isConnected) view.append(message);
  message.textContent = 'Could not load the track. Check your connection and WebGL support, then reload.';
  console.error(error);
}

function boot(T) {
  const TAU = 2 * Math.PI;
  const track = { x: 44, z: 29, inner: .84, outer: 1.16, segments: 128 };
  const gates = [0, TAU / 4, TAU / 2, 3 * TAU / 4];
  const keys = new Set();
  const storageKey = 'mesa-circuit-v1-best-ms';
  const car = { x: 0, z: 0, heading: 0, speed: 0 };
  const lap = { started: null, next: 1, valid: true, best: null };
  try {
    const saved = Number(localStorage.getItem(storageKey));
    if (Number.isFinite(saved) && saved > 0) lap.best = saved;
  } catch {}

  const scene = new T.Scene();
  scene.background = new T.Color(0xf4bb87);
  scene.fog = new T.Fog(0xf4bb87, 85, 210);
  const camera = new T.PerspectiveCamera(62, 1, .1, 240);
  const renderer = new T.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.domElement.setAttribute('aria-label', '3D view of Mesa Circuit');
  message.remove();
  view.append(renderer.domElement);

  scene.add(new T.HemisphereLight(0xfff2dc, 0x855443, 2.2));
  const sun = new T.DirectionalLight(0xffdda8, 2.4);
  sun.position.set(-30, 45, 15);
  scene.add(sun);

  const mat = color => new T.MeshStandardMaterial({ color, flatShading: true });
  function mesh(geometry, material, parent, x, y, z) {
    const object = new T.Mesh(geometry, material);
    object.position.set(x, y, z);
    parent.add(object);
    return object;
  }
  function box(parent, material, x, y, z, w, h, d) {
    return mesh(new T.BoxGeometry(w, h, d), material, parent, x, y, z);
  }
  const sand = mat(0xb97047);
  const asphalt = mat(0x34323a);
  const cream = mat(0xffead2);
  const rust = mat(0xb44231);
  const dark = mat(0x171820);
  box(scene, sand, 0, -.52, 0, 420, 1, 420);

  function band(inner, outer, y, material) {
    const positions = [];
    const indices = [];
    for (let i = 0; i <= track.segments; i++) {
      const a = TAU * i / track.segments;
      for (const r of [inner, outer]) {
        positions.push(track.x * r * Math.cos(a), y, track.z * r * Math.sin(a));
      }
      if (i < track.segments) {
        const j = 2 * i;
        indices.push(j, j + 2, j + 1, j + 1, j + 2, j + 3);
      }
    }
    const geometry = new T.BufferGeometry();
    geometry.setAttribute('position', new T.Float32BufferAttribute(positions, 3));
    geometry.setIndex(indices);
    geometry.computeVertexNormals();
    mesh(geometry, material, scene, 0, 0, 0);
  }
  band(track.inner, track.outer, 0, asphalt);
  band(track.inner, track.inner + .018, .015, cream);
  band(track.outer - .018, track.outer, .015, cream);

  for (let i = 0; i < 48; i++) {
    const a = TAU * i / 48;
    const dash = box(scene, cream, track.x * Math.cos(a), .022,
      track.z * Math.sin(a), .14, .025, 1.55);
    dash.rotation.y = Math.atan2(-track.x * Math.sin(a), track.z * Math.cos(a));
  }
  const tile = track.x * (track.outer - track.inner) / 16;
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 16; col++) {
      box(scene, (row + col) % 2 ? dark : cream,
        track.x * track.inner + (col + .5) * tile, .05,
        (row - .5) * tile, tile, .035, tile);
    }
  }

  const rock = new T.DodecahedronGeometry(1);
  for (let i = 0; i < 38; i++) {
    const a = i * 2.39996;
    const r = i < 13 ? .26 + (i % 4) * .09 : 1.45 + (i % 7) * .16;
    const size = 1.2 + (i % 5) * .55;
    const stone = mesh(rock, i % 2 ? sand : rust, scene,
      track.x * r * Math.cos(a), size * .45, track.z * r * Math.sin(a));
    stone.scale.set(size, size * (i < 13 ? 1 : 2.1), size);
    stone.rotation.y = a;
  }

  const kart = new T.Group();
  scene.add(kart);
  box(kart, mat(0x13a69a), 0, .57, 0, 1.65, .55, 2.75);
  box(kart, mat(0x214157), 0, 1, -.18, 1.18, .48, 1.15);
  box(kart, cream, 0, .87, .9, .25, .035, .65);
  const wheel = new T.CylinderGeometry(.35, .35, .3, 10);
  for (const x of [-.87, .87]) {
    for (const z of [-.88, .88]) {
      mesh(wheel, dark, kart, x, .36, z).rotation.z = Math.PI / 2;
    }
  }

  function format(ms) {
    const n = Math.floor(ms);
    return `${Math.floor(n / 60000)}:${String(Math.floor(n / 1000) % 60).padStart(2, '0')}.${String(n % 1000).padStart(3, '0')}`;
  }
  function angle() {
    return (Math.atan2(car.z / track.z, car.x / track.x) + TAU) % TAU;
  }
  function onRoad() {
    const radius = Math.hypot(car.x / track.x, car.z / track.z);
    return radius >= track.inner && radius <= track.outer;
  }
  function reset() {
    const a = -.13;
    car.x = track.x * Math.cos(a);
    car.z = track.z * Math.sin(a);
    car.heading = Math.atan2(-track.x * Math.sin(a), track.z * Math.cos(a));
    car.speed = 0;
    lap.started = null;
    lap.next = 1;
    lap.valid = true;
    status.textContent = 'Cross the checkered line to start.';
  }

  function score(before, after, road, now) {
    if (lap.started !== null && lap.valid && !road) {
      lap.valid = false;
      status.textContent = 'Off track. Cross the line to start a fresh lap.';
    }
    const advance = (after - before + TAU) % TAU;
    if (advance === 0 || advance > Math.PI || !road || car.speed <= 0) return;
    for (let i = 0; i < gates.length; i++) {
      const distance = (gates[i] - before + TAU) % TAU;
      if (distance === 0 || distance > advance) continue;
      if (i === 0) {
        if (lap.started !== null && lap.valid && lap.next === gates.length) {
          const elapsed = now - lap.started;
          const record = lap.best === null || elapsed < lap.best;
          if (record) {
            lap.best = elapsed;
            best.textContent = format(elapsed);
            try { localStorage.setItem(storageKey, String(elapsed)); } catch {}
          }
          status.textContent = `${record ? 'New best' : 'Lap complete'} · ${format(elapsed)}`;
        } else {
          status.textContent = 'Lap started. Stay between the white lines.';
        }
        lap.started = now;
        lap.next = 1;
        lap.valid = true;
      } else if (lap.started !== null && i === lap.next) {
        lap.next++;
      }
    }
  }

  const controls = new Set([
    'KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyR',
    'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'
  ]);
  window.addEventListener('keydown', event => {
    if (!controls.has(event.code) || event.ctrlKey || event.metaKey || event.altKey) return;
    event.preventDefault();
    keys.add(event.code);
    if (event.code === 'KeyR' && !event.repeat) reset();
  });
  window.addEventListener('keyup', event => keys.delete(event.code));
  window.addEventListener('blur', () => keys.clear());

  function resize() {
    const { clientWidth: width, clientHeight: height } = view;
    renderer.setSize(width, height);
    camera.aspect = width / Math.max(height, 1);
    camera.updateProjectionMatrix();
  }
  new ResizeObserver(resize).observe(view);
  resize();
  reset();
  if (lap.best !== null) best.textContent = format(lap.best);

  const down = (a, b) => Number(keys.has(a) || keys.has(b));
  let last = performance.now();
  renderer.setAnimationLoop(now => {
    const dt = Math.min(Math.max((now - last) / 1000, 0), .04);
    last = now;
    const before = angle();
    const road = onRoad();
    const throttle = down('KeyW', 'ArrowUp') - down('KeyS', 'ArrowDown');
    const turn = down('KeyA', 'ArrowLeft') - down('KeyD', 'ArrowRight');
    if (throttle) {
      const braking = throttle * car.speed < 0;
      car.speed += throttle * (braking ? 30 : 15) * dt;
    } else {
      car.speed *= Math.exp(-2 * dt);
    }
    car.speed = T.MathUtils.clamp(car.speed, -8, road ? 30 : 9);
    car.heading += turn * 1.9 * T.MathUtils.clamp(car.speed / 6, -1, 1) * dt;
    const dx = Math.sin(car.heading);
    const dz = Math.cos(car.heading);
    car.x += dx * car.speed * dt;
    car.z += dz * car.speed * dt;
    score(before, angle(), onRoad(), now);

    kart.position.set(car.x, 0, car.z);
    kart.rotation.y = car.heading;
    camera.position.set(car.x - dx * 8.5, 5.5, car.z - dz * 8.5);
    camera.lookAt(car.x + dx * 4, .6, car.z + dz * 4);
    current.textContent = format(lap.started === null ? 0 : now - lap.started);
    renderer.render(scene, camera);
  });
}
</script>
</body>
</html>
```

## Run and verify

Serve the file over HTTP. If you have Python 3, run `python -m http.server 8000` in the file's directory and open `http://localhost:8000`. The browser needs internet access for the pinned Three.js module and WebGL support.

**Not run here.** These are expected results from reading the code, not measured results. I would verify them in the browser:

| Check | Expected result |
|---|---|
| Load the page and open the developer console | The track, car, and HUD appear without console errors. The timer reads `0:00.000`. |
| Accelerate, steer both ways, brake, and reverse | Both key sets work. Arrow keys do not scroll the page. Switching tabs while holding a key does not leave it stuck. |
| Drive two clean clockwise laps in the marked travel direction | The first forward crossing starts timing. Each full lap restarts the current timer. The best display shows the faster lap. |
| Reverse across the line, then drive off the road during a timed lap | A backward crossing does not score. An off-road lap does not update the best. The next forward crossing on the road starts a fresh attempt. |
| Press R, then reload on the same URL | R resets the car and current timer. The best survives both actions when browser storage is available. |
| Resize to 320 px, test 200% zoom, and block the CDN once | The HUD and controls remain readable, the canvas resizes, and a blocked module shows a recovery message. |

## Design and scope

| Approach | Decision |
|---|---|
| Free steering with ordered gates | Chosen. You can miss a corner or cut across the infield, but an off-road lap cannot set a record. |
| Steering constrained to the road | Skipped. It would simplify lap counting at the cost of letting you drive off the racing line. |

**Throughput checkpoint.** Blocking first steps were choosing the track and lap state. Independent workstreams were not needed for one file. The frame loop owns car and lap updates, with input handlers collecting keys and handling reset. One implementation pass keeps the geometry and scoring rules together. Browser verification remains open. No subagents, repo design contract, or PR workflow were available in this chat.

**Principles applied.** *Model the domain* led to a shared ellipse model and an ordered gate index. *Prove it works* led to browser checks for actual driving, invalid laps, and persistence rather than a syntax-only check.


=============== RESPONSE ambition-game-12 ===============

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ring Run</title>
  <style>
    body { margin: 0; overflow: hidden; background: #a4dae8; color: white;
           font: 16px system-ui, sans-serif; font-variant-numeric: tabular-nums; }
    canvas { display: block; }
    #hud { position: fixed; top: 16px; left: 16px; padding: 12px 16px;
           background: #14222aee; border-radius: 8px; pointer-events: none; }
    #hud p { margin: 6px 0 0; }
    #hint { color: #cbdce3; font-size: 13px; }
  </style>
</head>
<body>
  <div id="hud">
    <strong>RING RUN</strong>
    <p>Lap <span id="lap">—</span> · Best <span id="best">—</span></p>
    <p id="status">Cross the stripe to start</p>
    <p id="hint">WASD / arrows to drive · R to reset</p>
  </div>
  <script type="module">
    import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js";

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xa4dae8);
    scene.fog = new THREE.Fog(0xa4dae8, 55, 130);
    const camera = new THREE.PerspectiveCamera(58, 1, 0.1, 160);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    document.body.append(renderer.domElement);

    function resize() {
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(innerWidth, innerHeight);
    }
    addEventListener("resize", resize);
    resize();

    scene.add(new THREE.HemisphereLight(0xfff5dc, 0x526344, 2.3));
    const sun = new THREE.DirectionalLight(0xffeed0, 2);
    sun.position.set(-20, 35, 12);
    scene.add(sun);

    const roadInner = 30, roadOuter = 42;
    const radius = (roadInner + roadOuter) / 2;
    const turn = 2 * Math.PI;

    function ring(inner, outer, height, color) {
      const mesh = new THREE.Mesh(
        new THREE.RingGeometry(inner, outer, 96),
        new THREE.MeshStandardMaterial({ color, roughness: 1 })
      );
      mesh.rotation.x = -Math.PI / 2;
      mesh.position.y = height;
      scene.add(mesh);
    }

    function box(parent, w, h, d, color, x, y, z) {
      const mesh = new THREE.Mesh(
        new THREE.BoxGeometry(w, h, d),
        new THREE.MeshStandardMaterial({ color })
      );
      mesh.position.set(x, y, z);
      parent.add(mesh);
      return mesh;
    }

    box(scene, 300, 0.2, 300, 0x689c53, 0, -0.11, 0);
    ring(roadInner, roadOuter, 0, 0x343b46);
    ring(roadInner, roadInner + 0.35, 0.01, 0xf2cd6e);
    ring(roadOuter - 0.35, roadOuter, 0.01, 0xf2cd6e);

    for (let i = 0; i < 36; i++) {
      const a = i * turn / 36;
      box(scene, 0.14, 0.02, 2, 0xc0c5cb,
          radius * Math.cos(a), 0.012, radius * Math.sin(a)).rotation.y = -a;
    }

    for (let i = 0; i < 12; i++) {
      for (let j = 0; j < 2; j++) {
        box(scene, 1, 0.025, 0.5, (i + j) % 2 ? 0xf6f3de : 0x141721,
            roadInner + i + 0.5, 0.025, (j - 0.5) * 0.5);
      }
    }

    const treeShape = new THREE.ConeGeometry(1.4, 3.8, 5);
    const leaves = new THREE.MeshStandardMaterial({ color: 0x245d43, flatShading: true });
    for (let i = 0; i < 44; i++) {
      const a = i * 2.39996;
      const r = i % 2 ? 47 + i % 10 : 10 + i % 16;
      const x = r * Math.cos(a), z = r * Math.sin(a);
      box(scene, 0.36, 1, 0.36, 0x77523c, x, 0.5, z);
      const tree = new THREE.Mesh(treeShape, leaves);
      tree.position.set(x, 2.4, z);
      tree.rotation.y = a;
      scene.add(tree);
    }

    const car = new THREE.Group();
    scene.add(car);
    box(car, 1.75, 0.43, 3.1, 0xef5341, 0, 0.5, 0);
    box(car, 1.25, 0.48, 1.4, 0x233b50, 0, 0.91, -0.22);
    for (const x of [-0.87, 0.87]) {
      for (const z of [-0.98, 0.98]) {
        box(car, 0.37, 0.55, 0.64, 0x171a20, x, 0.28, z);
      }
    }

    const lap = document.querySelector("#lap");
    const bestDisplay = document.querySelector("#best");
    const status = document.querySelector("#status");
    const keys = new Set();
    const controls = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight",
                      "KeyW", "KeyA", "KeyS", "KeyD", "KeyR"];
    let speed, heading, angle, started, nextGate, clean;
    let best = Infinity;
    const format = ms => `${(ms / 1000).toFixed(2)} s`;

    function reset() {
      angle = -0.16;
      heading = -angle;
      speed = 0;
      car.position.set(radius * Math.cos(angle), 0, radius * Math.sin(angle));
      started = null;
      nextGate = 0;
      clean = true;
      status.textContent = "Cross the stripe to start";
    }

    addEventListener("keydown", event => {
      if (!controls.includes(event.code)) return;
      event.preventDefault();
      keys.add(event.code);
      if (event.code === "KeyR" && !event.repeat) reset();
    });
    addEventListener("keyup", event => keys.delete(event.code));
    addEventListener("blur", () => keys.clear());

    const onRoad = () => {
      const r = Math.hypot(car.position.x, car.position.z);
      return r >= roadInner && r <= roadOuter;
    };

    reset();
    const forward = new THREE.Vector3();
    const eye = new THREE.Vector3();
    const target = new THREE.Vector3();
    let last = performance.now();

    function frame(now) {
      const dt = Math.min((now - last) / 1000, 0.05);
      last = now;
      const throttle = Number(keys.has("KeyW") || keys.has("ArrowUp"))
                     - Number(keys.has("KeyS") || keys.has("ArrowDown"));
      const steer = Number(keys.has("KeyA") || keys.has("ArrowLeft"))
                  - Number(keys.has("KeyD") || keys.has("ArrowRight"));
      const road = onRoad();
      speed += throttle * 18 * dt;
      speed *= Math.exp(-(road ? 0.7 : 2.8) * dt);
      speed = THREE.MathUtils.clamp(speed, road ? -8 : -4, road ? 22 : 7);
      heading += steer * 1.85 * Math.min(Math.abs(speed) / 8, 1) * Math.sign(speed) * dt;
      forward.set(Math.sin(heading), 0, Math.cos(heading));
      car.position.addScaledVector(forward, speed * dt);
      car.rotation.y = heading;

      const raw = Math.atan2(car.position.z, car.position.x);
      const delta = raw - angle;
      const step = Math.atan2(Math.sin(delta), Math.cos(delta));
      // Unwrap this step so crossing the atan2 seam is not a lap event.
      const end = angle + step;
      const crossed = gate =>
        Math.floor((end - gate) / turn) > Math.floor((angle - gate) / turn);

      const stillOnRoad = onRoad();
      if (started !== null && (!road || !stillOnRoad)) clean = false;
      if (stillOnRoad && crossed(0)) {
        if (started !== null && nextGate === 4 && clean) {
          best = Math.min(best, now - started);
          bestDisplay.textContent = format(best);
        }
        started = now;
        nextGate = 1;
        clean = true;
      } else if (started !== null && nextGate < 4 && crossed(nextGate * turn / 4)) {
        nextGate++;
      }
      angle = raw;

      lap.textContent = started === null ? "—" : format(now - started);
      if (started !== null) {
        status.textContent = clean ? `${nextGate - 1}/3 checkpoints` : "Lap invalid · stay on the asphalt";
      }

      eye.copy(car.position).addScaledVector(forward, -9);
      eye.y = 5.5;
      target.copy(car.position).addScaledVector(forward, 5);
      target.y = 0.6;
      camera.position.lerp(eye, 1 - Math.exp(-8 * dt));
      camera.lookAt(target);
      renderer.render(scene, camera);
      requestAnimationFrame(frame);
    }

    camera.position.set(car.position.x, 5.5, car.position.z - 9);
    requestAnimationFrame(frame);
  </script>
</body>
</html>
```

Save as `index.html` and open it in a modern browser with internet access; Three.js loads from a CDN. Use **WASD** or the **arrow keys**; **R** returns you to the start and keeps your best lap. The best time resets on reload.

**How I’d verify it** (not run here):

1. Open the page and check that the track, car, and HUD render without console errors. Resize the window and confirm the view doesn’t stretch.
2. Drive across the stripe in the direction the car faces. Confirm the timer starts, then follow the asphalt around the ring. The checkpoint count should reach `3/3`, and the next stripe crossing should set **Best** and restart the timer.
3. Drive a slower clean lap, then a faster one. Only the faster lap should replace **Best**.
4. Cut across the grass or reverse over the stripe without completing the checkpoints. Neither should set a best time. Press **R** and confirm the timer clears while the best time remains.


=============== RESPONSE ambition-game-13 ===============

Save the code below as `index.html`. It gives keyboard players a low-poly time trial on one closed circuit. The lap clock starts at the checkered line, and the best lap is saved in the browser when storage is available. The project is one file with a pinned Three.js dependency and no build step. I wrote it here but did not run it.

**Data shape.** The track is an elliptical ring with eight ordered gates. The car has a position, heading, and signed speed. The lap is either waiting for the start line or running with a start timestamp and the next required gate. A missing best lap is `null`.

**Design choice.** I chose free steering on a ring over steering constrained to a spline. The ring uses the same coordinates for rendering, road boundaries, and checkpoint detection. The spline alternative would make it easier to add irregular turns, but it would also need a separate way to map the car's position back onto the track.

## Complete `index.html`

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cinder Circuit</title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: #263e43;
    color: #fff7e9;
    font: 1rem system-ui, sans-serif;
  }
  canvas { position: fixed; inset: 0; display: block; }
  .hud {
    position: relative;
    width: fit-content;
    max-width: calc(100% - 1.5rem);
    margin: .75rem;
    padding: .85rem 1rem;
    border: 1px solid #667571;
    border-radius: .75rem;
    background: #172523;
    overflow-wrap: anywhere;
  }
  h1 { margin: 0; font-size: 1.15rem; letter-spacing: .08em; }
  dl { display: flex; flex-wrap: wrap; gap: .5rem 1.4rem; margin: .65rem 0; }
  dt { font-size: .78rem; color: #dfd4bf; }
  dd { margin: 0; color: #ffd38f; font: 700 1.25rem ui-monospace, monospace; }
  p { margin: .35rem 0 0; font-size: .85rem; }
</style>
</head>
<body>
<main class="hud" aria-label="Race information">
  <h1>CINDER CIRCUIT</h1>
  <dl>
    <div><dt>Current lap</dt><dd id="lap">0:00.000</dd></div>
    <div><dt>Best lap</dt><dd id="best">None</dd></div>
  </dl>
  <p id="status" role="status">Loading track…</p>
  <p>Drive with WASD or arrow keys. Press R to reset.</p>
</main>

<script type="module">
const status = document.getElementById('status');

try {
  const THREE = await import(
    'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js'
  );
  start(THREE);
} catch (error) {
  status.textContent = 'Could not start. Check your internet connection and WebGL support, then reload.';
  console.error(error);
}

function start(T) {
  const lapDisplay = document.getElementById('lap');
  const bestDisplay = document.getElementById('best');
  const storageKey = 'cinder-circuit.best-ms.v1';
  const track = { a: 50, b: 34, inner: .81, outer: 1.19, gates: 8 };
  const tau = 2 * Math.PI;
  const gateStep = tau / track.gates;
  const car = { x: 0, z: 0, heading: 0, speed: 0 };
  let lap = { phase: 'waiting' };
  let best = null;

  try {
    const saved = Number(localStorage.getItem(storageKey));
    if (Number.isFinite(saved) && saved > 0) best = saved;
  } catch {}

  const scene = new T.Scene();
  scene.background = new T.Color(0xf5b685);
  scene.fog = new T.FogExp2(0xf5b685, .005);
  const camera = new T.PerspectiveCamera(57, 1, .1, 350);
  const renderer = new T.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.domElement.setAttribute('aria-hidden', 'true');
  document.body.prepend(renderer.domElement);

  scene.add(new T.HemisphereLight(0xffead4, 0x736468, 2));
  const sun = new T.DirectionalLight(0xffe1b0, 2.1);
  sun.position.set(-35, 55, -20);
  scene.add(sun);

  function mesh(geometry, color, parent = scene) {
    const object = new T.Mesh(geometry, new T.MeshStandardMaterial({
      color, flatShading: true, side: T.DoubleSide
    }));
    parent.add(object);
    return object;
  }

  function box(w, h, d, color, x, y, z, parent = scene) {
    const object = mesh(new T.BoxGeometry(w, h, d), color, parent);
    object.position.set(x, y, z);
    return object;
  }

  function strip(inner, outer, from, to, y, color, segments) {
    const vertices = [];
    const faces = [];
    for (let i = 0; i <= segments; i++) {
      const a = from + (to - from) * i / segments;
      for (const r of [inner, outer]) {
        vertices.push(track.a * r * Math.cos(a), y, track.b * r * Math.sin(a));
      }
      const j = i * 2;
      if (i < segments) faces.push(j, j+1, j+2, j+1, j+3, j+2);
    }
    const geometry = new T.BufferGeometry();
    geometry.setAttribute('position', new T.Float32BufferAttribute(vertices, 3));
    geometry.setIndex(faces);
    geometry.computeVertexNormals();
    mesh(geometry, color);
  }

  box(440, 1, 440, 0xb87850, 0, -.52, 0);
  strip(track.inner, track.outer, 0, tau, .01, 0x32383d, 192);
  strip(.81, .836, 0, tau, .025, 0xffd297, 192);
  strip(1.164, 1.19, 0, tau, .025, 0xffd297, 192);
  for (let i = 0; i < 56; i++) {
    const a = tau * (i + .5) / 56;
    strip(.996, 1.004, a - .022, a + .022, .026, 0xa7b2af, 4);
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 12; col++) {
      const r = track.inner + col * (track.outer - track.inner) / 12;
      strip(r, r + (track.outer - track.inner) / 12,
        (row - 1) * .024, row * .024, .04,
        (row + col) % 2 ? 0xfdf4e7 : 0x161b20, 3);
    }
  }

  for (let i = 0; i < 32; i++) {
    const a = i * tau / 32;
    const s = 2 + (i * 7 % 13) * .65;
    const rock = mesh(new T.DodecahedronGeometry(s), i % 2 ? 0x9d543f : 0xd19161);
    const r = i % 2 ? .49 : 1.65;
    rock.position.set(track.a * r * Math.cos(a), s * .27, track.b * r * Math.sin(a));
    rock.scale.set(1, 1.15, .85);
    rock.rotation.y = i * .73;
  }

  const model = new T.Group();
  scene.add(model);
  box(2, .65, 3.7, 0xf85a35, 0, .65, 0, model);
  box(1.48, .62, 1.65, 0x204754, 0, 1.23, -.28, model);
  box(1.8, .16, .45, 0xffc272, 0, 1.09, -1.56, model);
  for (const x of [-1, 1]) {
    for (const z of [-1.21, 1.21]) {
      box(.44, .65, .76, 0x20242a, x, .36, z, model);
    }
    box(.46, .2, .08, 0xffeee0, x * .64, .73, 1.86, model);
  }

  function format(ms) {
    const n = Math.max(0, Math.floor(ms));
    return `${Math.floor(n / 60000)}:${String(Math.floor(n / 1000) % 60).padStart(2, '0')}.${String(n % 1000).padStart(3, '0')}`;
  }

  function reset(message = 'Cross the checkered line to start.') {
    const a = -.13;
    car.x = track.a * Math.cos(a);
    car.z = track.b * Math.sin(a);
    car.heading = Math.atan2(-track.a * Math.sin(a), track.b * Math.cos(a));
    car.speed = 0;
    lap = { phase: 'waiting' };
    status.textContent = message;
  }

  function passGate(gate, now) {
    if (gate === 0) {
      const valid = lap.phase === 'running' && lap.next === track.gates;
      const elapsed = valid ? now - lap.since : 0;
      const record = valid && elapsed > 0 && (best === null || elapsed < best);
      if (record) {
        best = elapsed;
        bestDisplay.textContent = format(best);
        try { localStorage.setItem(storageKey, String(best)); } catch {}
      }
      status.textContent = record ? `New best: ${format(elapsed)}`
        : valid ? `Last lap: ${format(elapsed)}` : 'Lap running.';
      lap = { phase: 'running', since: now, next: 1 };
    } else if (lap.phase === 'running' && gate === lap.next) {
      lap.next++;
    }
  }

  const keys = new Set();
  const controls = new Set([
    'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
    'KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyR'
  ]);
  addEventListener('keydown', event => {
    if (!controls.has(event.code) || event.altKey || event.ctrlKey || event.metaKey) return;
    event.preventDefault();
    keys.add(event.code);
    if (event.code === 'KeyR' && !event.repeat) reset();
  });
  addEventListener('keyup', event => keys.delete(event.code));
  addEventListener('blur', () => keys.clear());
  document.addEventListener('visibilitychange', () => {
    keys.clear();
    if (document.hidden) reset();
  });
  const held = (a, b) => Number(keys.has(a) || keys.has(b));

  function step(dt, now) {
    const throttle = held('ArrowUp', 'KeyW') - held('ArrowDown', 'KeyS');
    const steer = held('ArrowLeft', 'KeyA') - held('ArrowRight', 'KeyD');
    const acceleration = throttle * car.speed < 0 ? 32 : 17;
    car.speed = T.MathUtils.clamp(
      (car.speed + throttle * acceleration * dt) * Math.exp(-.48 * dt), -9, 29
    );
    car.heading += steer * Math.sign(car.speed) * Math.min(Math.abs(car.speed) / 4, 1) * 1.45 * dt;

    const old = Math.atan2(car.z / track.b, car.x / track.a);
    car.x += Math.sin(car.heading) * car.speed * dt;
    car.z += Math.cos(car.heading) * car.speed * dt;
    const x = car.x / track.a, z = car.z / track.b;
    const radius = Math.hypot(x, z);
    if (radius < track.inner || radius > track.outer) {
      reset('Off track. Cross the line to start a new lap.');
      return;
    }

    const angle = Math.atan2(z, x);
    const delta = Math.atan2(Math.sin(angle - old), Math.cos(angle - old));
    if (delta > 0) {
      const from = (old + tau) % tau;
      const next = Math.floor(from / gateStep) + 1;
      if (from + delta >= next * gateStep) passGate(next % track.gates, now);
    } else if (delta < 0 && lap.phase === 'running') {
      const from = (old + tau) % tau;
      const previous = Math.floor(from / gateStep);
      if (from + delta < previous * gateStep) {
        lap = { phase: 'waiting' };
        status.textContent = 'Wrong way. Cross the line forward to start again.';
      }
    }
  }

  function resize() {
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
  }

  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const viewTarget = new T.Vector3();
  const viewPosition = new T.Vector3();
  let previous = performance.now();
  function frame(now) {
    const dt = Math.min(Math.max(0, (now - previous) / 1000), .05);
    previous = now;
    if (!document.hidden) step(dt, now);

    model.position.set(car.x, 0, car.z);
    model.rotation.y = car.heading;
    const dx = Math.sin(car.heading), dz = Math.cos(car.heading);
    if (reducedMotion.matches) {
      camera.position.set(0, 130, -72);
      camera.lookAt(0, 0, 0);
    } else {
      viewPosition.set(car.x - dx * 10, 6.8, car.z - dz * 10);
      viewTarget.set(car.x + dx * 5, .6, car.z + dz * 5);
      camera.position.copy(viewPosition);
      camera.lookAt(viewTarget);
    }
    lapDisplay.textContent = format(lap.phase === 'running' ? now - lap.since : 0);
    renderer.render(scene, camera);
    requestAnimationFrame(frame);
  }

  bestDisplay.textContent = best === null ? 'None' : format(best);
  reset();
  resize();
  addEventListener('resize', resize);
  requestAnimationFrame(frame);
}
</script>
</body>
</html>
```

## How to run and verify

Open `index.html` in a WebGL-capable browser with internet access. If your browser blocks the CDN import from a local file, serve the folder with `python -m http.server 8000` and open `http://localhost:8000`. No package install is required.

These are the checks I would run in the browser. The expected results are inferred from the code, not measured.

| Check | Expected result |
|---|---|
| Load the page and open DevTools | The car, track, and HUD appear without console errors. The clock reads `0:00.000`, and a fresh browser profile shows `None` for the best lap. |
| Drive with both key sets | Up/W accelerates, Down/S brakes and then reverses, and Left/A and Right/D steer. Arrow keys do not scroll the page. |
| Complete a lap | The clock starts at the first forward crossing. Hold Up and tap Right to follow the bend. The next forward crossing after all checkpoints records a best lap and starts the next clock. |
| Run a slower lap, then reload | The slower lap does not replace the best. Reloading at the same address keeps the best when storage is available. |
| Reverse across a checkpoint or cut across the infield | No lap is credited. A backward checkpoint crossing invalidates the attempt. Leaving the road returns the car to the start. |
| Press R or switch tabs mid-lap | The current attempt resets, but the best lap remains. No held key carries over from the other tab. |
| Resize to 320px, zoom to 200%, and enable reduced motion | The HUD text remains readable and wraps. Reduced motion replaces the chase camera with a fixed overview. |
| Block the CDN and reload | The page shows a startup error instead of remaining on “Loading track…” indefinitely. |

The only continuous motion is gameplay. There are no HUD transitions or camera shake. Camera feel and narrow-window layout remain unverified.

## Implementation checkpoint

- **Blocking first steps.** Define the track coordinates and lap rules before wiring the controls and HUD.
- **Independent workstreams.** The scene styling and input mapping do not own lap state.
- **Shared mutable state.** The animation loop advances the car and lap. Reset handles abandoned attempts.
- **Smallest safe decomposition.** One HTML file keeps the render, driving, and lap checks runnable together. Delegation, browser execution, commits, and PR steps were unavailable in this chat.

**Principles applied.** **Model the domain** led to the waiting/running lap state and ordered gates. **Prove it works** led to browser checks for valid laps, invalid attempts, and persistence rather than a syntax-only check. No product decision is needed to use this version.


=============== RESPONSE ambition-game-14 ===============

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dustloop — Three.js Arcade Racer</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; overflow: hidden; background: #bce5f4; color: white;
      font: 16px system-ui, sans-serif; }
    canvas { display: block; }
    #hud { position: fixed; top: 16px; left: 16px; padding: 14px 18px;
      border-radius: 12px; background: #14222bea; pointer-events: none; }
    h1 { margin: 0 0 8px; font-size: 20px; letter-spacing: .16em; color: #ffce70; }
    #times { margin: 0; font: 17px ui-monospace, monospace; white-space: pre; }
    #hint { margin: 8px 0 0; font-size: 13px; color: #c9d8e2; }
  </style>
</head>
<body>
  <div id="hud">
    <h1>DUSTLOOP</h1>
    <p id="times"></p>
    <p id="hint">WASD / arrows · R to restart<br>Cross the stripe to start timing.</p>
  </div>
  <script type="module">
    import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js";

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xbce5f4);
    scene.fog = new THREE.FogExp2(0xbce5f4, 0.005);
    const camera = new THREE.PerspectiveCamera(62, innerWidth / innerHeight, 0.1, 350);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setSize(innerWidth, innerHeight);
    document.body.append(renderer.domElement);

    scene.add(new THREE.HemisphereLight(0xfff4df, 0x79827a, 2));
    const sun = new THREE.DirectionalLight(0xffe4be, 2);
    sun.position.set(-30, 50, 20);
    scene.add(sun);

    function mesh(geometry, color, x, y, z, parent = scene) {
      const object = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({
        color, flatShading: true, side: THREE.DoubleSide
      }));
      object.position.set(x, y, z);
      parent.add(object);
      return object;
    }

    mesh(new THREE.BoxGeometry(400, 1, 400), 0xb69863, 0, -0.51, 0);

    const rx = 48, rz = 34, inner = 0.84, outer = 1.16;
    const turn = Math.PI * 2;
    function strip(lo, hi, start, end, segments, y, color) {
      const vertices = [], indices = [];
      for (let i = 0; i <= segments; i++) {
        const angle = start + (end - start) * i / segments;
        for (const r of [lo, hi]) {
          vertices.push(rx * r * Math.cos(angle), y, rz * r * Math.sin(angle));
        }
        if (i < segments) {
          const j = i * 2;
          indices.push(j, j + 2, j + 1, j + 1, j + 2, j + 3);
        }
      }
      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute("position", new THREE.Float32BufferAttribute(vertices, 3));
      geometry.setIndex(indices);
      geometry.computeVertexNormals();
      mesh(geometry, color, 0, 0, 0);
    }

    strip(inner, outer, 0, turn, 128, 0.01, 0x323943);
    for (let i = 0; i < 64; i++) {
      const a = i * turn / 64, b = (i + 1) * turn / 64;
      const curb = i % 2 ? 0xf5eee0 : 0xde5140;
      strip(inner, inner + 0.025, a, b, 2, 0.025, curb);
      strip(outer - 0.025, outer, a, b, 2, 0.025, curb);
      if (i !== 0 && i !== 63) strip(0.994, 1.006, a, a + (b - a) / 2, 1, 0.024, 0xffda84);
    }
    for (let row = 0; row < 2; row++) {
      for (let col = 0; col < 8; col++) {
        const cell = (outer - inner) / 8;
        strip(inner + col * cell, inner + (col + 1) * cell,
          (row - 1) * 0.022, row * 0.022, 1, 0.035,
          (row + col) % 2 ? 0x20252d : 0xffffff);
      }
    }

    for (let i = 0; i < 42; i++) {
      const angle = i * 2.39996;
      const r = i % 3 ? 1.29 + (i % 7) * 0.055 : 0.25 + (i % 5) * 0.09;
      const x = rx * r * Math.cos(angle), z = rz * r * Math.sin(angle);
      const h = 2.5 + (i % 5) * 0.65;
      mesh(new THREE.CylinderGeometry(0.15, 0.25, h / 2, 5), 0x72503b, x, h / 4, z);
      mesh(new THREE.ConeGeometry(h * 0.39, h, 5), i % 2 ? 0x427458 : 0x578159,
        x, h * 0.76, z);
    }

    // The car's local +Z axis points forward.
    const car = new THREE.Group();
    scene.add(car);
    mesh(new THREE.BoxGeometry(1.9, 0.55, 3.5), 0xe34a32, 0, 0.66, 0, car);
    mesh(new THREE.BoxGeometry(1.4, 0.59, 1.48), 0x273e50, 0, 1.16, -0.25, car);
    for (const x of [-0.96, 0.96]) {
      for (const z of [-1.04, 1.04]) {
        const wheel = mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.34, 10),
          0x21252a, x, 0.4, z, car);
        wheel.rotation.z = Math.PI / 2;
      }
      mesh(new THREE.BoxGeometry(0.33, 0.17, 0.08), 0xffe7a7, x * 0.72, 0.69, 1.75, car);
    }

    const keys = new Set();
    const controls = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight",
      "KeyW", "KeyA", "KeyS", "KeyD", "KeyR"];
    addEventListener("keydown", event => {
      if (!controls.includes(event.code)) return;
      event.preventDefault();
      keys.add(event.code);
      if (event.code === "KeyR" && !event.repeat) reset();
    });
    addEventListener("keyup", event => keys.delete(event.code));
    addEventListener("blur", () => keys.clear());
    addEventListener("resize", () => {
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(innerWidth, innerHeight);
    });

    const times = document.querySelector("#times");
    const storageKey = "dustloop.best.v1";
    let best = Infinity;
    try {
      const saved = Number(localStorage.getItem(storageKey));
      if (saved > 0 && Number.isFinite(saved)) best = saved;
    } catch { /* Timing still works when storage is unavailable. */ }

    let heading, speed, started, gate;
    const view = new THREE.Vector3();
    function reset() {
      car.position.set(rx, 0, -5);
      car.rotation.y = heading = 0;
      speed = 0;
      started = null;
      gate = 0;
      camera.position.set(rx, 6.5, -16);
    }
    reset();

    const pressed = (a, b) => Number(keys.has(a) || keys.has(b));
    const angleAt = (x, z) => Math.atan2(z / rz, x / rx);
    const radiusAt = (x, z) => Math.hypot(x / rx, z / rz);
    const wrap = angle => (angle + Math.PI * 3) % turn - Math.PI;
    const format = seconds => Number.isFinite(seconds) ? `${seconds.toFixed(2)} s` : "—";

    let previous = performance.now();
    renderer.setAnimationLoop(now => {
      const dt = Math.max(0, Math.min((now - previous) / 1000, 0.05));
      previous = now;
      const { x, z } = car.position;
      const r = radiusAt(x, z);
      const onRoad = r >= inner && r <= outer;
      const throttle = pressed("KeyW", "ArrowUp") - pressed("KeyS", "ArrowDown");
      const steer = pressed("KeyA", "ArrowLeft") - pressed("KeyD", "ArrowRight");
      speed += throttle * 23 * dt;
      speed *= Math.exp(-(onRoad ? 0.65 : 2.9) * dt);
      speed = THREE.MathUtils.clamp(speed, -8, 29);
      heading += steer * Math.sign(speed) * Math.min(Math.abs(speed) / 5, 1) * 1.9 * dt;

      const dx = Math.sin(heading), dz = Math.cos(heading);
      car.rotation.y = heading;
      car.position.x += dx * speed * dt;
      car.position.z += dz * speed * dt;

      // Stripe, then three quarter-turn gates, then the stripe again.
      const before = angleAt(x, z);
      const after = angleAt(car.position.x, car.position.z);
      const step = wrap(after - before);
      if (Math.abs(step) > 0.000001 && Math.abs(step) < Math.PI / 2) {
        for (let i = 0; i < 4; i++) {
          const offset = wrap(i * turn / 4 - before);
          const fraction = offset / step;
          if (fraction <= 0 || fraction > 1) continue;
          const crossingRadius = radiusAt(
            THREE.MathUtils.lerp(x, car.position.x, fraction),
            THREE.MathUtils.lerp(z, car.position.z, fraction)
          );
          if (step < 0 || crossingRadius < inner || crossingRadius > outer) {
            started = null;
            gate = 0;
          } else if (i === 0) {
            if (started !== null && gate === 0) {
              const lap = (now - started) / 1000;
              if (lap < best) {
                best = lap;
                try { localStorage.setItem(storageKey, String(best)); } catch {}
              }
            }
            started = now;
            gate = 1;
          } else if (started !== null && i === gate) {
            gate = (gate + 1) % 4;
          }
          break;
        }
      }

      view.set(car.position.x - dx * 11, 6.5, car.position.z - dz * 11);
      camera.position.lerp(view, 1 - Math.exp(-7 * dt));
      camera.lookAt(car.position.x + dx * 4, 0.9, car.position.z + dz * 4);
      times.textContent =
        `Lap   ${format(started === null ? Infinity : (now - started) / 1000)}\n` +
        `Best  ${format(best)}`;
      renderer.render(scene, camera);
    });
  </script>
</body>
</html>
```

Save this as `index.html` and open it in a modern browser. It needs WebGL and an internet connection to load Three.js from the CDN. If your browser blocks the module on a `file:` URL, serve the folder with `python -m http.server 8000` and open `http://localhost:8000`.

**How I’d verify it** — I haven’t run it here:

1. **Load and drive.** Check that the HUD, car, and closed track render without console errors. Test both key layouts, reverse, and resize. Drive onto the dirt and confirm the car slows down.
2. **Time two laps.** Drive forward across the checkered stripe: `Lap` should start and `Best` should stay blank. Complete the loop: `Best` should show the finished time and `Lap` should restart. Drive a slower lap, then a faster one; only the faster time should replace the best.
3. **Try an invalid lap.** After starting, cut across the infield or reverse across the stripe. Neither should set a best time. Cross the stripe forward again and complete a clean lap to confirm timing recovers.
4. **Check restart and persistence.** Press `R`: the car should return behind the stripe and the current timer should clear, while the best stays. Reload from the same localhost URL and confirm the best survives.


=============== RESPONSE ambition-game-15 ===============

Save this as `index.html`. It’s a complete single-file game; Three.js loads from a pinned CDN URL. Use **WASD** or the **arrow keys** to drive, and **R** to reset the car and current lap. Your best lap is saved in the browser when local storage is available.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pine Loop Racer</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      overflow: hidden;
      background: #adcfe0;
      font: 16px system-ui, sans-serif;
    }
    canvas { display: block; }
    #hud, #help {
      position: fixed;
      z-index: 1;
      color: white;
      background: #13202aeb;
      border-radius: 12px;
      padding: 12px 16px;
      pointer-events: none;
    }
    #hud { top: 16px; left: 16px; min-width: 215px; }
    h1 { margin: 0 0 8px; font-size: 18px; }
    #hud div {
      display: flex;
      justify-content: space-between;
      gap: 18px;
      font-variant-numeric: tabular-nums;
    }
    #status { margin: 8px 0 0; color: #fbd47b; font-size: 13px; }
    #help { bottom: 16px; left: 16px; font-size: 13px; }
  </style>
</head>
<body>
  <section id="hud" aria-label="Race information">
    <h1>Pine Loop Racer</h1>
    <div>Lap <strong id="lap">0:00.000</strong></div>
    <div>Best <strong id="best">—</strong></div>
    <div>Speed <strong id="speed">0</strong></div>
    <p id="status">Cross the start line to begin.</p>
  </section>
  <aside id="help">WASD / arrows: drive · R: reset</aside>

  <script type="module">
    import * as THREE from
      'https://cdn.jsdelivr.net/npm/three@0.172.0/build/three.module.js';

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xadcfe0);
    scene.fog = new THREE.Fog(0xadcfe0, 65, 150);

    const camera = new THREE.PerspectiveCamera(58, 1, 0.1, 220);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    document.body.appendChild(renderer.domElement);

    scene.add(new THREE.HemisphereLight(0xf0f8ff, 0x706147, 2.1));
    const sun = new THREE.DirectionalLight(0xffe4b4, 2.3);
    sun.position.set(-35, 55, 20);
    scene.add(sun);

    const mat = color => new THREE.MeshStandardMaterial({
      color, roughness: 0.9, flatShading: true
    });
    function mesh(geometry, material, x = 0, y = 0, z = 0, parent = scene) {
      const object = new THREE.Mesh(geometry, material);
      object.position.set(x, y, z);
      parent.add(object);
      return object;
    }
    function box(w, h, d, material, x, y, z, parent) {
      return mesh(new THREE.BoxGeometry(w, h, d), material, x, y, z, parent);
    }

    box(340, 0.2, 340, mat(0x709455), 0, -0.13, 0);

    // Closed elliptical centerline. All road markings use the same geometry.
    const A = 49, B = 32, HALF = 5, TAU = 2 * Math.PI;
    function track(t, offset = 0, y = 0) {
      const c = Math.cos(t), s = Math.sin(t);
      const nx = c / A, nz = s / B;
      const length = Math.hypot(nx, nz);
      return new THREE.Vector3(
        A * c + offset * nx / length, y,
        B * s + offset * nz / length
      );
    }

    function strip(start, end, inner, outer, y, segments, material) {
      const positions = [], indices = [];
      for (let i = 0; i <= segments; i++) {
        const t = start + (end - start) * i / segments;
        for (const offset of [inner, outer]) {
          const p = track(t, offset, y);
          positions.push(p.x, p.y, p.z);
        }
        if (i < segments) {
          const j = i * 2;
          indices.push(j, j + 2, j + 1, j + 1, j + 2, j + 3);
        }
      }
      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
      geo.setIndex(indices);
      geo.computeVertexNormals();
      mesh(geo, material);
    }

    const asphalt = mat(0x39414a);
    const white = mat(0xf6f1df), red = mat(0xf05a46);
    const dark = mat(0x171c23), yellow = mat(0xf5c86a);
    strip(0, TAU, -HALF, HALF, 0.02, 160, asphalt);
    for (let i = 0; i < 80; i++) {
      const t = i * TAU / 80, end = (i + 1) * TAU / 80;
      const curb = i % 2 ? white : red;
      strip(t, end, -HALF, -HALF + 0.42, 0.035, 2, curb);
      strip(t, end, HALF - 0.42, HALF, 0.035, 2, curb);
      if (i !== 0 && i !== 79) {
        strip(t, t + (end - t) * 0.48, -0.065, 0.065, 0.04, 2, yellow);
      }
    }
    for (let row = 0; row < 2; row++) {
      for (let col = 0; col < 10; col++) {
        strip((row - 1) * 0.018, row * 0.018, col - 5, col - 4,
          0.05, 1, (row + col) % 2 ? white : dark);
      }
    }

    // Deterministic scenery, with a clear shoulder around the road.
    let seed = 1234;
    function random() {
      seed = (Math.imul(1664525, seed) + 1013904223) >>> 0;
      return seed / 4294967296;
    }
    const samples = Array.from({ length: 160 }, (_, i) => track(i * TAU / 160));
    function roadDistance(x, z) {
      let best = Infinity;
      for (const p of samples) {
        best = Math.min(best, (x - p.x) ** 2 + (z - p.z) ** 2);
      }
      return Math.sqrt(best);
    }
    const bark = mat(0x76523b);
    const greens = [mat(0x285d47), mat(0x377b54), mat(0x4c8651)];
    const trunkGeo = new THREE.CylinderGeometry(0.17, 0.24, 1.4, 5);
    const crownGeo = new THREE.ConeGeometry(1.25, 3, 5);
    for (let i = 0; i < 245; i++) {
      const x = (random() - 0.5) * 165, z = (random() - 0.5) * 130;
      if (roadDistance(x, z) < 8.5) continue;
      const scale = 0.65 + random() * 0.85;
      const tree = new THREE.Group();
      tree.position.set(x, 0, z);
      tree.scale.setScalar(scale);
      tree.rotation.y = random() * TAU;
      scene.add(tree);
      mesh(trunkGeo, bark, 0, 0.7, 0, tree);
      const leaves = greens[i % greens.length];
      mesh(crownGeo, leaves, 0, 2.15, 0, tree);
      mesh(crownGeo, leaves, 0, 3.25, 0, tree).scale.setScalar(0.72);
    }

    // Local +Z is the car's forward direction.
    const car = new THREE.Group();
    scene.add(car);
    const paint = mat(0xff7738), glass = mat(0x365466);
    box(1.62, 0.42, 2.85, paint, 0, 0.55, 0, car);
    box(1.26, 0.42, 1.33, glass, 0, 0.96, -0.18, car);
    box(1.30, 0.09, 1.21, paint, 0, 1.20, -0.2, car);
    box(1.46, 0.12, 0.22, dark, 0, 0.82, -1.25, car);
    const tire = new THREE.CylinderGeometry(0.32, 0.32, 0.24, 10);
    for (const x of [-0.82, 0.82]) {
      for (const z of [-0.88, 0.88]) {
        mesh(tire, dark, x, 0.34, z, car).rotation.z = Math.PI / 2;
      }
    }
    for (const x of [-0.56, 0.56]) {
      box(0.31, 0.14, 0.06, white, x, 0.59, 1.44, car);
      box(0.28, 0.13, 0.06, red, x, 0.59, -1.44, car);
    }
    const shadow = mesh(new THREE.CircleGeometry(1, 20),
      new THREE.MeshBasicMaterial({ color: 0x101820, transparent: true,
        opacity: 0.24, depthWrite: false }), 0, 0.065, 0);
    shadow.rotation.x = -Math.PI / 2;
    shadow.scale.set(1.1, 1.65, 1);

    const ui = Object.fromEntries(
      ['lap', 'best', 'speed', 'status'].map(id => [id, document.getElementById(id)])
    );
    const saveKey = 'pine-loop-best-v1';
    let best = Infinity;
    try {
      const saved = Number(localStorage.getItem(saveKey));
      if (Number.isFinite(saved) && saved > 0) best = saved;
    } catch {}

    function format(ms) {
      const n = Math.floor(ms);
      return `${Math.floor(n / 60000)}:${String(Math.floor(n / 1000) % 60)
        .padStart(2, '0')}.${String(n % 1000).padStart(3, '0')}`;
    }
    function showBest() {
      ui.best.textContent = Number.isFinite(best) ? format(best) : '—';
    }
    showBest();

    const keys = new Set();
    const controls = new Set([
      'KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyR',
      'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'
    ]);
    const held = (...codes) => codes.some(code => keys.has(code));
    addEventListener('keydown', e => {
      if (!controls.has(e.code)) return;
      e.preventDefault();
      keys.add(e.code);
      if (e.code === 'KeyR' && !e.repeat) reset();
    });
    addEventListener('keyup', e => keys.delete(e.code));
    addEventListener('blur', () => keys.clear());
    document.addEventListener('visibilitychange', () => keys.clear());

    let speed, heading, lapStart, nextGate;
    // Gates are forward-only and must be crossed in order: 1, 2, 3, 0.
    // Each lies on a cardinal axis and spans the width of the asphalt.
    const gates = [
      { x: A, z: 0, dx: 0, dz: 1 },
      { x: 0, z: B, dx: -1, dz: 0 },
      { x: -A, z: 0, dx: 0, dz: -1 },
      { x: 0, z: -B, dx: 1, dz: 0 }
    ];
    function crossed(g, oldX, oldZ, x, z) {
      const a = (oldX - g.x) * g.dx + (oldZ - g.z) * g.dz;
      const b = (x - g.x) * g.dx + (z - g.z) * g.dz;
      if (!(a < 0 && b >= 0)) return null;
      const f = -a / (b - a);
      const hitX = oldX + (x - oldX) * f - g.x;
      const hitZ = oldZ + (z - oldZ) * f - g.z;
      return Math.abs(hitX * g.dz - hitZ * g.dx) <= HALF ? f : null;
    }

    const target = new THREE.Vector3(), view = new THREE.Vector3();
    function follow(blend) {
      const dx = Math.sin(heading), dz = Math.cos(heading);
      target.set(car.position.x - dx * 10, 6.4, car.position.z - dz * 10);
      camera.position.lerp(target, blend);
      view.set(car.position.x + dx * 5, 0.65, car.position.z + dz * 5);
      camera.lookAt(view);
    }
    function reset() {
      car.position.copy(track(-0.13));
      heading = Math.atan2(-A * Math.sin(-0.13), B * Math.cos(-0.13));
      car.rotation.y = heading;
      speed = 0;
      lapStart = null;
      nextGate = 0;
      ui.lap.textContent = format(0);
      ui.status.textContent = 'Cross the start line to begin.';
      follow(1);
    }
    reset();

    function resize() {
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(innerWidth, innerHeight);
    }
    addEventListener('resize', resize);
    resize();

    let previous = performance.now();
    function frame(now) {
      const dt = Math.max(0, Math.min((now - previous) / 1000, 0.05));
      previous = now;
      const oldX = car.position.x, oldZ = car.position.z;
      const grass = roadDistance(oldX, oldZ) > HALF;
      const throttle = Number(held('KeyW', 'ArrowUp'))
                     - Number(held('KeyS', 'ArrowDown'));
      const steer = Number(held('KeyA', 'ArrowLeft'))
                  - Number(held('KeyD', 'ArrowRight'));

      if (throttle) {
        const braking = speed * throttle < 0;
        speed += throttle * (braking ? 40 : throttle > 0 ? 20 : 12) * dt;
      } else {
        speed *= Math.exp(-2.1 * dt);
      }
      const limit = grass ? 9 : 31;
      if (speed > limit) speed = Math.max(limit, speed - 48 * dt);
      speed = THREE.MathUtils.clamp(speed, grass ? -5 : -9, 31);
      heading += steer * Math.sign(speed) *
        Math.min(Math.abs(speed) / 5, 1) * (grass ? 1.9 : 1.55) * dt;

      car.position.x = THREE.MathUtils.clamp(oldX + Math.sin(heading) * speed * dt, -90, 90);
      car.position.z = THREE.MathUtils.clamp(oldZ + Math.cos(heading) * speed * dt, -74, 74);
      car.rotation.y = heading;
      shadow.position.x = car.position.x;
      shadow.position.z = car.position.z;
      shadow.rotation.z = -heading;

      const fraction = crossed(gates[nextGate], oldX, oldZ, car.position.x, car.position.z);
      if (fraction !== null) {
        if (nextGate === 0) {
          const crossingTime = now - (1 - fraction) * dt * 1000;
          if (lapStart !== null) {
            const elapsed = crossingTime - lapStart;
            const record = elapsed < best;
            if (record) {
              best = elapsed;
              try { localStorage.setItem(saveKey, String(best)); } catch {}
              showBest();
            }
            ui.status.textContent = `${record ? 'New best' : 'Last lap'}: ${format(elapsed)}`;
          } else {
            ui.status.textContent = 'Lap underway — follow the track.';
          }
          lapStart = crossingTime;
        } else if (nextGate === 3) {
          ui.status.textContent = 'All checkpoints cleared. Head to the finish!';
        }
        nextGate = (nextGate + 1) % gates.length;
      }

      if (lapStart !== null) ui.lap.textContent = format(now - lapStart);
      ui.speed.textContent = `${Math.round(Math.abs(speed) * 3.6)} km/h`;
      follow(1 - Math.exp(-7 * dt));
      renderer.render(scene, camera);
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  </script>
</body>
</html>
```

### Run and verify

From the folder containing `index.html`, run `python -m http.server 8000` and open `http://localhost:8000/`. The browser needs internet access to fetch Three.js.

I haven’t run the game here. This is the browser smoke test I’d use:

1. **Load and resize:** Confirm the track, car, and HUD appear with no console errors. Resize the window and check that the view doesn’t stretch.
2. **Drive:** Try both key sets. Check that steering works in forward and reverse, grass slows the car, and releasing the keys lets it coast to a stop.
3. **Time a lap:** Cross the checkered line in the starting direction. The timer should start, but **Best** should remain blank. Follow the track around and cross the line again; **Best** should update and the next lap should start immediately.
4. **Check invalid laps:** Reverse across the line and drive forward over it again without completing the loop. Verify that this doesn’t record a lap. Cutting through the infield and missing a checkpoint should also prevent a lap from counting.
5. **Check persistence:** Complete a slower lap and confirm the best stays unchanged. Press **R**, then reload: both should clear the current lap, while the best time remains.


=============== RESPONSE ambition-game-16 ===============

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mint Circuit</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; overflow: hidden; background: #a9d9de; color: white;
           font: 16px system-ui, sans-serif; }
    canvas { display: block; }
    #hud { position: fixed; top: 16px; left: 16px; z-index: 1;
           padding: 14px 18px; border-radius: 10px; background: #172737ed;
           font-variant-numeric: tabular-nums; }
    h1 { margin: 0 0 8px; font-size: 20px; color: #a5f3cf; }
    #hud small { display: block; margin-top: 8px; color: #d6e5ee; }
  </style>
</head>
<body>
  <div id="hud">
    <h1>Mint Circuit</h1>
    Lap <span id="lap">0.00 s</span> · Best <span id="best">—</span>
    <small>WASD / arrows to drive · R to restart</small>
  </div>

  <script type="module">
    import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js';

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xa9d9de);
    scene.fog = new THREE.Fog(0xa9d9de, 65, 170);

    const camera = new THREE.PerspectiveCamera(58, 1, 0.1, 200);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    document.body.append(renderer.domElement);

    function resize() {
      renderer.setSize(innerWidth, innerHeight);
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
    }
    addEventListener('resize', resize);
    resize();

    scene.add(new THREE.HemisphereLight(0xfff5dd, 0x52695a, 2));
    const sun = new THREE.DirectionalLight(0xffebc1, 2);
    sun.position.set(-20, 35, 10);
    scene.add(sun);

    function box(parent, color, w, h, d, x, y, z) {
      const mesh = new THREE.Mesh(
        new THREE.BoxGeometry(w, h, d),
        new THREE.MeshStandardMaterial({ color, flatShading: true })
      );
      mesh.position.set(x, y, z);
      parent.add(mesh);
    }

    box(scene, 0x68a36b, 240, 1, 240, 0, -0.53, 0);

    const rx = 30, rz = 21, inner = 0.82, outer = 1.18;
    const tau = 2 * Math.PI, segments = 96;

    function strip(lo, hi, color, y, dashed = false) {
      const vertices = [];
      for (let i = 0; i < segments; i++) {
        if (dashed && i % 4 >= 2) continue;
        const a = i * tau / segments, b = (i + 1) * tau / segments;
        const point = (angle, r) =>
          [rx * r * Math.cos(angle), y, rz * r * Math.sin(angle)];
        vertices.push(...point(a, lo), ...point(b, hi), ...point(a, hi),
                      ...point(a, lo), ...point(b, lo), ...point(b, hi));
      }
      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
      geometry.computeVertexNormals();
      scene.add(new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({ color })));
    }

    strip(inner, outer, 0x303844, 0);
    strip(inner, inner + 0.015, 0xf5e8cd, 0.01);
    strip(outer - 0.015, outer, 0xf5e8cd, 0.01);
    strip(0.995, 1.005, 0xe6c768, 0.01, true);

    const tile = rx * (outer - inner) / 12;
    for (let i = 0; i < 12; i++) {
      for (let row = 0; row < 2; row++) {
        box(scene, (i + row) % 2 ? 0x10151e : 0xffffff,
            tile, 0.02, 0.45, rx * inner + (i + 0.5) * tile, 0.015,
            (row - 0.5) * 0.45);
      }
    }

    const treeMaterial = new THREE.MeshStandardMaterial({ color: 0x236e58, flatShading: true });
    const treeShape = new THREE.ConeGeometry(1.4, 3.7, 5);
    for (let i = 0; i < 28; i++) {
      const a = i * tau / 28;
      const r = i % 2 ? 1.42 : 0.62;
      const tree = new THREE.Mesh(treeShape, treeMaterial);
      tree.position.set(rx * r * Math.cos(a), 1.85, rz * r * Math.sin(a));
      tree.rotation.y = a;
      scene.add(tree);
    }

    const car = new THREE.Group();
    scene.add(car);
    box(car, 0xff6056, 1.5, 0.48, 2.7, 0, 0.52, 0);
    box(car, 0x213849, 1.15, 0.46, 1.15, 0, 0.98, -0.22);
    for (const x of [-0.78, 0.78]) {
      for (const z of [-0.85, 0.85]) {
        box(car, 0x171c26, 0.36, 0.52, 0.58, x, 0.27, z);
      }
      box(car, 0xffedb0, 0.34, 0.17, 0.05, x * 0.65, 0.57, 1.36);
    }

    const lapDisplay = document.querySelector('#lap');
    const bestDisplay = document.querySelector('#best');
    const format = ms => `${(ms / 1000).toFixed(2)} s`;
    let heading, speed, angle, progress, lapStart;
    let best = Infinity;

    function reset() {
      car.position.set(rx, 0, 0);
      heading = speed = angle = progress = 0;
      lapStart = null;
    }
    reset();

    const keys = new Set();
    const controls = ['KeyW', 'KeyA', 'KeyS', 'KeyD', 'ArrowUp',
                      'ArrowLeft', 'ArrowDown', 'ArrowRight', 'KeyR'];
    addEventListener('keydown', event => {
      if (!controls.includes(event.code)) return;
      event.preventDefault();
      keys.add(event.code);
      if (event.code === 'KeyR' && !event.repeat) reset();
    });
    addEventListener('keyup', event => keys.delete(event.code));
    addEventListener('blur', () => keys.clear());

    const held = (a, b) => Number(keys.has(a) || keys.has(b));
    const chase = new THREE.Vector3();
    let previous = performance.now();

    renderer.setAnimationLoop(now => {
      const dt = Math.min((now - previous) / 1000, 0.05);
      previous = now;

      const throttle = held('KeyW', 'ArrowUp') - held('KeyS', 'ArrowDown');
      const steer = held('KeyD', 'ArrowRight') - held('KeyA', 'ArrowLeft');
      if (throttle) {
        lapStart ??= now;
        speed += throttle * 22 * dt;
      } else {
        speed *= Math.exp(-2.3 * dt);
      }
      speed = THREE.MathUtils.clamp(speed, -9, 28);
      heading -= steer * Math.sign(speed) * Math.min(Math.abs(speed) / 5, 1) * 2.2 * dt;

      let x = car.position.x + Math.sin(heading) * speed * dt;
      let z = car.position.z + Math.cos(heading) * speed * dt;
      const radius = Math.hypot(x / rx, z / rz);
      // scoper: soft track edges, not a rigid-body collision simulation.
      const limit = THREE.MathUtils.clamp(radius, inner + 0.035, outer - 0.035);
      if (limit !== radius) {
        x *= limit / radius;
        z *= limit / radius;
        speed *= Math.exp(-5 * dt);
      }
      car.position.set(x, 0, z);
      car.rotation.y = heading;

      const nextAngle = Math.atan2(z / rz, x / rx);
      // Signed progress cancels backtracking and unwraps the atan2 seam.
      progress += THREE.MathUtils.euclideanModulo(nextAngle - angle + Math.PI, tau) - Math.PI;
      angle = nextAngle;
      if (lapStart !== null && progress >= tau) {
        best = Math.min(best, now - lapStart);
        bestDisplay.textContent = format(best);
        progress -= tau;
        lapStart = now;
      }
      lapDisplay.textContent = format(lapStart === null ? 0 : now - lapStart);

      chase.set(x - 8 * Math.sin(heading), 5.5, z - 8 * Math.cos(heading));
      camera.position.lerp(chase, 1 - Math.exp(-8 * dt));
      camera.lookAt(x + 3 * Math.sin(heading), 0.65, z + 3 * Math.cos(heading));
      renderer.render(scene, camera);
    });
  </script>
</body>
</html>
```

Save as `index.html` and open it in a modern browser with internet access and WebGL enabled. Three.js loads from a CDN; there’s no build step. If your browser blocks module loading from `file://`, serve the file through a local static server.

**How I’d verify it** (not run here):

1. **Load and drive.** Check that the track, car, and HUD appear without console errors. Try both WASD and the arrow keys. From the starting line, accelerate and steer left to follow the oval. Check that the car slows and stays on the road when pushed into an edge.
2. **Check lap counting.** Drive one full lap in the starting direction. The lap timer should start on the first throttle input, the best time should appear at the finish, and the current timer should restart. Reverse across the line and drive back over it: that should not award another lap.
3. **Check best time and restart.** Drive a deliberately slower lap and confirm the best stays unchanged. Press **R** and confirm the car returns to the start and the current timer resets while the best remains. Reloading the page clears the best.


=============== RESPONSE ambition-game-17 ===============

Save this as `index.html`. It’s a complete single-file racer with one closed track, a chase camera, keyboard controls, and a best lap saved in your browser. It loads Three.js from a CDN, so you’ll need an internet connection.

**Controls:** WASD or arrow keys to drive, Space to brake, R to restart the run without clearing your best lap.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pine Loop — Arcade Racer</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; overflow: hidden; background: #a9d7e8; color: white;
           font: 15px system-ui, sans-serif; }
    canvas { display: block; }
    #hud, #help {
      position: fixed; z-index: 1; pointer-events: none;
      background: #14232ee8; padding: 12px 16px; border-radius: 10px;
    }
    #hud { top: 14px; left: 14px; font-variant-numeric: tabular-nums; }
    #hud strong { color: #ffd86b; }
    #times { display: grid; grid-template-columns: auto auto; gap: 4px 16px;
             margin-top: 8px; }
    #status { margin-top: 8px; color: #c6e4ee; }
    #help { bottom: 14px; left: 14px; right: 14px; width: fit-content; }
  </style>
</head>
<body>
  <div id="hud">
    <strong>PINE LOOP</strong>
    <div id="times">
      <span>Lap</span><span id="lap">—</span>
      <span>Best</span><span id="best">—</span>
      <span>Speed</span><span id="speed">0 km/h</span>
    </div>
    <div id="status">Cross the stripe to start.</div>
  </div>
  <div id="help">WASD / arrows: drive · Space: brake · R: restart</div>

  <script type="module">
    import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js';

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xa9d7e8);
    scene.fog = new THREE.Fog(0xa9d7e8, 95, 210);
    const camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 300);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setSize(innerWidth, innerHeight);
    document.body.appendChild(renderer.domElement);

    scene.add(new THREE.HemisphereLight(0xffffff, 0x526447, 2.1));
    const sun = new THREE.DirectionalLight(0xffe9b9, 2.5);
    sun.position.set(-30, 60, 20);
    scene.add(sun);

    const mat = color => new THREE.MeshStandardMaterial({ color, flatShading: true });
    function mesh(geometry, material, parent = scene) {
      const m = new THREE.Mesh(geometry, material);
      parent.add(m);
      return m;
    }

    const grass = mesh(new THREE.PlaneGeometry(500, 500), mat(0x679057));
    grass.rotation.x = -Math.PI / 2;

    const points = [
      [-36, -24], [0, -37], [38, -26], [51, 0],
      [35, 28], [4, 38], [-31, 29], [-50, 5]
    ].map(([x, z]) => new THREE.Vector3(x, 0, z));
    const track = new THREE.CatmullRomCurve3(points, true, 'centripetal');
    const N = 320, halfWidth = 5.6;
    const samples = Array.from({ length: N }, (_, i) => track.getPointAt(i / N));
    const tangents = Array.from({ length: N }, (_, i) => track.getTangentAt(i / N));
    const mod = (n, m) => ((n % m) + m) % m;

    function strip(left, right, y, materials, choose = () => 0) {
      const positions = [], indices = [];
      const geometry = new THREE.BufferGeometry();
      for (let i = 0; i <= N; i++) {
        const p = samples[i % N], t = tangents[i % N];
        for (const offset of [left, right]) {
          positions.push(p.x + t.z * offset, y, p.z - t.x * offset);
        }
        if (i < N) {
          const j = i * 2;
          geometry.addGroup(indices.length, 6, choose(i));
          indices.push(j, j + 1, j + 2, j + 1, j + 3, j + 2);
        }
      }
      geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
      geometry.setIndex(indices);
      geometry.computeVertexNormals();
      mesh(geometry, materials);
    }
    strip(-halfWidth, halfWidth, 0.035, [mat(0x373d46)]);
    const curb = [mat(0xf4eee0), mat(0xd7473f)];
    strip(-6.1, -halfWidth, 0.045, curb, i => Math.floor(i / 4) % 2);
    strip(halfWidth, 6.1, 0.045, curb, i => Math.floor(i / 4) % 2);

    const stripe = new THREE.Group();
    stripe.position.copy(samples[0]);
    stripe.rotation.y = Math.atan2(tangents[0].x, tangents[0].z);
    scene.add(stripe);
    const checker = [mat(0xffffff), mat(0x171b21)];
    const tileWidth = 2 * halfWidth / 12;
    for (let row = 0; row < 2; row++) {
      for (let col = 0; col < 12; col++) {
        mesh(new THREE.BoxGeometry(tileWidth, 0.02, 0.48),
          checker[(row + col) % 2], stripe)
          .position.set((col + 0.5) * tileWidth - halfWidth, 0.052, (row - 0.5) * 0.48);
      }
    }

    // Closest point on the sampled centerline. The returned index includes
    // the fractional position along the segment, for smooth gate detection.
    function nearest(x, z) {
      let d2 = Infinity, index = 0;
      for (let i = 0; i < N; i++) {
        const a = samples[i], b = samples[(i + 1) % N];
        const dx = b.x - a.x, dz = b.z - a.z;
        const u = THREE.MathUtils.clamp(
          ((x - a.x) * dx + (z - a.z) * dz) / (dx * dx + dz * dz), 0, 1);
        const d = (x - a.x - dx * u) ** 2 + (z - a.z - dz * u) ** 2;
        if (d < d2) { d2 = d; index = (i + u) % N; }
      }
      return { d2, index };
    }

    const bark = mat(0x76513a), pine = mat(0x245e48), tips = mat(0x33765b);
    const trunkGeo = new THREE.CylinderGeometry(0.2, 0.29, 1.5, 5);
    const crownGeo = new THREE.ConeGeometry(1.38, 2.9, 5);
    let seed = 42;
    const random = () => {
      seed = (1664525 * seed + 1013904223) >>> 0;
      return seed / 4294967296;
    };
    for (let i = 0; i < 175; i++) {
      const x = (random() - 0.5) * 175, z = (random() - 0.5) * 150;
      if (nearest(x, z).d2 < 11 ** 2) continue;
      const tree = new THREE.Group();
      scene.add(tree);
      tree.position.set(x, 0, z);
      tree.scale.setScalar(0.65 + random() * 0.85);
      tree.rotation.y = random() * Math.PI;
      mesh(trunkGeo, bark, tree).position.y = 0.75;
      mesh(crownGeo, pine, tree).position.y = 2.1;
      const top = mesh(crownGeo, tips, tree);
      top.position.y = 3.15;
      top.scale.setScalar(0.72);
    }

    const car = new THREE.Group();
    scene.add(car);
    const yellow = mat(0xffb626), glass = mat(0x244b63), rubber = mat(0x20242a);
    function carBox(w, h, l, x, y, z, material) {
      mesh(new THREE.BoxGeometry(w, h, l), material, car).position.set(x, y, z);
    }
    carBox(1.7, 0.5, 3.1, 0, 0.62, 0, yellow);
    carBox(1.28, 0.51, 1.39, 0, 1.08, -0.15, glass);
    carBox(1.31, 0.10, 1.42, 0, 1.37, -0.15, yellow);
    const wheelGeo = new THREE.CylinderGeometry(0.37, 0.37, 0.29, 9);
    for (const x of [-0.87, 0.87]) {
      for (const z of [-1.02, 1.02]) {
        const wheel = mesh(wheelGeo, rubber, car);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(x, 0.39, z);
      }
    }
    const red = mat(0xff4033);
    for (const x of [-0.57, 0.57]) carBox(0.32, 0.15, 0.06, x, 0.67, -1.57, red);

    const keys = new Set();
    const controls = new Set([
      'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
      'KeyW', 'KeyA', 'KeyS', 'KeyD', 'Space', 'KeyR'
    ]);
    addEventListener('keydown', e => {
      if (!controls.has(e.code)) return;
      e.preventDefault();
      keys.add(e.code);
      if (e.code === 'KeyR' && !e.repeat) reset();
    });
    addEventListener('keyup', e => keys.delete(e.code));
    addEventListener('blur', () => keys.clear());
    addEventListener('resize', () => {
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(innerWidth, innerHeight);
    });

    const lapEl = document.querySelector('#lap');
    const bestEl = document.querySelector('#best');
    const speedEl = document.querySelector('#speed');
    const statusEl = document.querySelector('#status');
    const storageKey = 'pine-loop-best-v1';
    let best = Infinity;
    try {
      const saved = Number(localStorage.getItem(storageKey));
      if (Number.isFinite(saved) && saved > 0) best = saved;
    } catch { /* Storage may be blocked; keep the best in memory. */ }

    function format(ms) {
      if (!Number.isFinite(ms)) return '—';
      const total = Math.floor(ms);
      const minutes = Math.floor(total / 60000);
      const seconds = String(Math.floor(total / 1000) % 60).padStart(2, '0');
      return `${minutes}:${seconds}.${String(total % 1000).padStart(3, '0')}`;
    }

    const forward = new THREE.Vector3(), eye = new THREE.Vector3(), look = new THREE.Vector3();
    let yaw, speed, previousIndex, startedAt, nextGate, notice;
    const gates = [N / 4, N / 2, 3 * N / 4];

    function follow(dt, snap = false) {
      forward.set(Math.sin(yaw), 0, Math.cos(yaw));
      eye.copy(car.position).addScaledVector(forward, -9);
      eye.y += 5.5;
      camera.position.lerp(eye, snap ? 1 : 1 - Math.exp(-7 * dt));
      look.copy(car.position).addScaledVector(forward, 4);
      look.y += 0.75;
      camera.lookAt(look);
    }

    function reset() {
      const spawn = N - 10;
      car.position.copy(samples[spawn]);
      car.position.y = 0.04;
      yaw = Math.atan2(tangents[spawn].x, tangents[spawn].z);
      car.rotation.y = yaw;
      speed = 0;
      previousIndex = spawn;
      startedAt = null;
      nextGate = 0;
      notice = 'Cross the stripe to start.';
      follow(0, true);
    }

    function updateLap(hit, now) {
      const delta = mod(hit.index - previousIndex + N / 2, N) - N / 2;
      const crossed = gate => {
        const ahead = mod(gate - previousIndex, N);
        return ahead > 0 && ahead <= delta;
      };
      // Count only forward crossings on the road. Three ordered checkpoints
      // prevent repeated trips across the start stripe from counting as laps.
      if (delta > 0 && hit.d2 <= halfWidth ** 2) {
        if (startedAt !== null && nextGate < gates.length && crossed(gates[nextGate])) {
          nextGate++;
        }
        if (crossed(0)) {
          if (startedAt === null) {
            notice = 'Lap started.';
          } else if (nextGate === gates.length) {
            const lap = now - startedAt;
            if (lap < best) {
              best = lap;
              try { localStorage.setItem(storageKey, String(best)); } catch {}
              notice = `New best: ${format(lap)}`;
            } else {
              notice = `Last lap: ${format(lap)}`;
            }
          } else {
            notice = 'Checkpoint missed. New lap started.';
          }
          startedAt = now;
          nextGate = 0;
        }
      }
      previousIndex = hit.index;
    }

    const down = (a, b) => keys.has(a) || keys.has(b);
    const approach = (value, target, amount) =>
      value < target ? Math.min(target, value + amount) : Math.max(target, value - amount);

    reset();
    let previousFrame = performance.now();
    renderer.setAnimationLoop(now => {
      const dt = Math.min(Math.max(0, (now - previousFrame) / 1000), 0.04);
      previousFrame = now;
      const onRoad = nearest(car.position.x, car.position.z).d2 <= halfWidth ** 2;
      const throttle = Number(down('KeyW', 'ArrowUp')) - Number(down('KeyS', 'ArrowDown'));
      const steer = Number(down('KeyA', 'ArrowLeft')) - Number(down('KeyD', 'ArrowRight'));
      if (keys.has('Space')) {
        speed = approach(speed, 0, 38 * dt);
      } else if (throttle > 0) {
        speed = approach(speed, onRoad ? 30 : 9, (onRoad ? 18 : 25) * dt);
      } else if (throttle < 0) {
        speed = approach(speed, -8, (speed > 0 ? 28 : 12) * dt);
      } else {
        speed = approach(speed, 0, (onRoad ? 5 : 16) * dt);
      }

      yaw += steer * Math.sign(speed) * Math.min(Math.abs(speed) / 5, 1) * 1.9 * dt;
      car.rotation.y = yaw;
      car.position.x += Math.sin(yaw) * speed * dt;
      car.position.z += Math.cos(yaw) * speed * dt;
      updateLap(nearest(car.position.x, car.position.z), now);
      follow(dt);

      lapEl.textContent = startedAt === null ? '—' : format(now - startedAt);
      bestEl.textContent = format(best);
      speedEl.textContent = `${Math.round(Math.abs(speed) * 3.6)} km/h`;
      statusEl.textContent = startedAt === null
        ? notice : `${notice} · Checkpoints ${nextGate}/3`;
      renderer.render(scene, camera);
    });
  </script>
</body>
</html>
```

### How I’d verify it

I haven’t run this here. I’d serve the file locally with `python -m http.server 8000` from its folder, then open `http://localhost:8000`. Serving over HTTP gives the page a consistent origin for saving its best lap.

1. **Load and drive:** Confirm the track, car, and HUD render without console errors. Check both keyboard layouts, Space braking, and that grass slows the car down.
2. **Complete a lap:** Cross the stripe in the starting direction. The timer should start, the checkpoint count should reach `3/3` in order, and the next stripe crossing should set the best lap and start a new timer.
3. **Check invalid laps:** Reverse across the stripe, then drive forward over it again without going around. The best lap should not change. Cutting across the infield and missing a checkpoint should likewise prevent a lap from counting.
4. **Check persistence:** Complete a slower lap and confirm the best stays unchanged. Press R and reload the page; both should reset the run but preserve the best time.


=============== RESPONSE ambition-game-18 ===============

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dust Loop</title>
  <style>
    body { margin: 0; overflow: hidden; background: #a9d9ef; font: 16px system-ui; }
    canvas { display: block; }
    #hud {
      position: fixed; top: 16px; left: 16px; padding: 14px 18px;
      border-radius: 8px; background: #14202a; color: white;
      font-variant-numeric: tabular-nums;
    }
    #hud strong { color: #ffcb67; }
    #status, small { color: #cedae2; }
  </style>
</head>
<body>
  <div id="hud">
    <strong>DUST LOOP</strong><br>
    Lap <span id="lap">—</span> · Best <span id="best">—</span><br>
    <span id="status">Cross the stripe to start</span><br>
    <small>WASD / arrows · R to reset</small>
  </div>

  <script type="module">
    import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js';

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xa9d9ef);
    scene.fog = new THREE.Fog(0xa9d9ef, 85, 180);

    const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 220);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    document.body.append(renderer.domElement);

    function resize() {
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(innerWidth, innerHeight);
    }
    addEventListener('resize', resize);
    resize();

    scene.add(new THREE.HemisphereLight(0xffffff, 0x82623e, 2));
    const sun = new THREE.DirectionalLight(0xffefd2, 2);
    sun.position.set(-25, 40, 15);
    scene.add(sun);

    function mesh(parent, geometry, color, x, y, z) {
      const object = new THREE.Mesh(
        geometry, new THREE.MeshStandardMaterial({ color, flatShading: true })
      );
      object.position.set(x, y, z);
      parent.add(object);
      return object;
    }

    const a = 43, b = 29, inner = 0.83, outer = 1.17;
    const tau = 2 * Math.PI;
    const clamp = THREE.MathUtils.clamp;

    mesh(scene, new THREE.BoxGeometry(360, 1, 360), 0xc5a26d, 0, -0.51, 0);

    function ring(lo, hi, color, y) {
      const road = mesh(scene, new THREE.RingGeometry(lo, hi, 96), color, 0, y, 0);
      road.scale.set(a, b, 1);
      road.rotation.x = -Math.PI / 2;
    }
    ring(inner, outer, 0x343a42, 0.01);
    ring(inner, inner + 0.012, 0xffd27c, 0.02);
    ring(outer - 0.012, outer, 0xffd27c, 0.02);

    // The timing line is z = 0 on the positive-x side of the oval.
    const tile = a * (outer - inner) / 12;
    for (let i = 0; i < 12; i++) {
      for (let j = 0; j < 2; j++) {
        mesh(scene, new THREE.BoxGeometry(tile, 0.025, 0.55),
          (i + j) % 2 ? 0x16191e : 0xffffff,
          a * inner + (i + 0.5) * tile, 0.025, (j - 0.5) * 0.55);
      }
    }

    for (let i = 0; i < 17; i++) {
      const t = i * 2.4;
      const h = 2 + (i % 4) * 0.7;
      mesh(scene, new THREE.ConeGeometry(h * 0.8, h, 5), 0x597044,
        Math.cos(t) * (12 + i % 7), h / 2, Math.sin(t) * (9 + i % 5));
    }

    const car = new THREE.Group();
    scene.add(car);
    mesh(car, new THREE.BoxGeometry(1.65, 0.48, 2.9), 0xed563e, 0, 0.59, 0);
    mesh(car, new THREE.BoxGeometry(1.26, 0.45, 1.35), 0x263d50, 0, 1, -0.15);
    mesh(car, new THREE.BoxGeometry(1.4, 0.13, 0.35), 0xffb34d, 0, 0.68, 1.32);
    for (const x of [-0.86, 0.86]) {
      for (const z of [-0.92, 0.92]) {
        const wheel = mesh(car, new THREE.CylinderGeometry(0.34, 0.34, 0.28, 8),
          0x171a1f, x, 0.35, z);
        wheel.rotation.z = Math.PI / 2;
      }
    }

    const lap = document.querySelector('#lap');
    const best = document.querySelector('#best');
    const status = document.querySelector('#status');
    const format = seconds => `${seconds.toFixed(2)} s`;
    const keys = new Set();
    const controls = new Set([
      'KeyW', 'KeyA', 'KeyS', 'KeyD', 'ArrowUp', 'ArrowLeft', 'ArrowDown', 'ArrowRight', 'KeyR'
    ]);

    addEventListener('keydown', event => {
      if (!controls.has(event.code)) return;
      event.preventDefault();
      keys.add(event.code);
      if (event.code === 'KeyR' && !event.repeat) reset();
    });
    addEventListener('keyup', event => keys.delete(event.code));
    addEventListener('blur', () => keys.clear());

    let heading, speed, angle, started, nextGate, bestTime = Infinity;
    function trackAngle() {
      return (Math.atan2(car.position.z / b, car.position.x / a) + tau) % tau;
    }
    function reset() {
      car.position.set(a * Math.cos(-0.19), 0, b * Math.sin(-0.19));
      heading = 0.28;
      speed = 0;
      angle = trackAngle();
      started = null;
      nextGate = 1;
      status.textContent = 'Cross the stripe to start';
    }
    reset();

    const chase = new THREE.Vector3();
    let previous = performance.now();
    renderer.setAnimationLoop(now => {
      const dt = clamp((now - previous) / 1000, 0, 0.05);
      previous = now;

      const throttle = keys.has('KeyW') || keys.has('ArrowUp');
      const brake = keys.has('KeyS') || keys.has('ArrowDown');
      const left = keys.has('KeyA') || keys.has('ArrowLeft');
      const right = keys.has('KeyD') || keys.has('ArrowRight');
      speed += (Number(throttle) * 24 - Number(brake) * 32) * dt;
      speed *= Math.exp(-dt * (throttle || brake ? 0.55 : 2));
      speed = clamp(speed, -8, 29);

      // +Z is the car's nose; positive yaw steers right.
      heading += (Number(right) - Number(left)) * 2.2 * clamp(speed / 7, -1, 1) * dt;
      const dx = Math.sin(heading), dz = Math.cos(heading);
      car.rotation.y = heading;
      car.position.x += dx * speed * dt;
      car.position.z += dz * speed * dt;

      const radius = Math.hypot(car.position.x / a, car.position.z / b);
      const current = trackAngle();
      const advance = ((current - angle + 3 * Math.PI) % tau) - Math.PI;
      const time = now / 1000;

      if (radius < inner || radius > outer) {
        speed *= Math.exp(-4 * dt);
        started = null;
        nextGate = 1;
        status.textContent = 'Off track · cross the stripe to restart';
      } else if (advance > 0) {
        if (angle + advance >= tau) {
          if (started !== null && nextGate === 4) {
            bestTime = Math.min(bestTime, time - started);
            best.textContent = format(bestTime);
          }
          started = time;
          nextGate = 1;
          status.textContent = 'Lap in progress';
        } else if (started !== null && nextGate < 4) {
          const gate = nextGate * Math.PI / 2;
          if (angle < gate && current >= gate) nextGate++;
        }
      }
      angle = current;
      lap.textContent = started === null ? '—' : format(time - started);

      chase.set(car.position.x - dx * 9, 5.8, car.position.z - dz * 9);
      camera.position.lerp(chase, 1 - Math.exp(-10 * dt));
      camera.lookAt(car.position.x + dx * 4, 0.9, car.position.z + dz * 4);
      renderer.render(scene, camera);
    });
  </script>
</body>
</html>
```

Save as `index.html` and open it in a browser with internet access for the Three.js import. If your browser blocks the module from a local file, serve the folder with `python -m http.server 8000` and open `http://localhost:8000`.

**How I’d verify it** (I haven’t run it here):

1. **Rendering and controls:** Check that the track, car, and HUD appear with no console errors. Try both key sets, confirm the arrow keys don’t scroll the page, and resize the window.
2. **Lap timing:** From spawn, drive forward over the stripe. The timer should start while **Best** stays blank. Complete a clean lap; **Best** should show the finished time and the lap timer should restart. Drive a slower lap, then a faster one, and confirm only the faster time replaces the record.
3. **Invalid laps and reset:** Back over the stripe, then drive forward over it without completing a lap; the record should not change. Cut across the infield and confirm the lap is invalidated. Press **R** to return to spawn: the current lap clears, but the best time stays until you reload the page.


=============== RESPONSE ambition-game-19 ===============

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dustloop — Arcade Racer</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; overflow: hidden; background: #f5c38b; color: white;
           font: 15px system-ui, sans-serif; }
    canvas { display: block; }
    #hud { position: fixed; top: 16px; left: 16px; padding: 12px 16px;
           border-radius: 8px; background: #17202de8; pointer-events: none; }
    h1 { margin: 0 0 8px; font-size: 19px; letter-spacing: .12em; }
    output { font-variant-numeric: tabular-nums; }
    small { display: block; margin-top: 8px; color: #d3deee; }
  </style>
</head>
<body>
  <aside id="hud">
    <h1>DUSTLOOP</h1>
    Lap <output id="lap">0.00 s</output> · Best <output id="best">—</output>
    <small>↑ / W accelerate · ↓ / S brake/reverse · ← → / A D steer</small>
  </aside>

  <script type="module">
    import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js';

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf5c38b);
    scene.fog = new THREE.Fog(0xf5c38b, 65, 150);

    const camera = new THREE.PerspectiveCamera(58, 1, 0.1, 180);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    document.body.append(renderer.domElement);

    function resize() {
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(innerWidth, innerHeight);
    }
    addEventListener('resize', resize);
    resize();

    scene.add(new THREE.HemisphereLight(0xffefd9, 0x6b5962, 2));
    const sun = new THREE.DirectionalLight(0xffe2b3, 2);
    sun.position.set(-20, 30, 15);
    scene.add(sun);

    function mesh(parent, geometry, color, x, y, z) {
      const object = new THREE.Mesh(geometry,
        new THREE.MeshStandardMaterial({ color, flatShading: true }));
      object.position.set(x, y, z);
      parent.add(object);
      return object;
    }

    const ground = mesh(scene, new THREE.PlaneGeometry(400, 400), 0xc68e60, 0, 0, 0);
    ground.rotation.x = -Math.PI / 2;

    const rx = 34, rz = 23, inner = 0.80, outer = 1.20;
    const turn = Math.PI * 2;

    function ring(from, to, color, height) {
      const band = mesh(scene, new THREE.RingGeometry(from, to, 96), color, 0, height, 0);
      band.rotation.x = -Math.PI / 2;
      band.scale.set(rx, rz, 1);
    }

    ring(inner, outer, 0x333b49, 0.02);
    ring(inner, inner + 0.025, 0xe5b55e, 0.03);
    ring(outer - 0.025, outer, 0xe5b55e, 0.03);

    for (let i = 0; i < 32; i++) {
      if (i === 0) continue;
      const a = i * turn / 32;
      const dash = mesh(scene, new THREE.BoxGeometry(0.17, 0.025, 1.35),
        0xcbd0d4, rx * Math.cos(a), 0.04, rz * Math.sin(a));
      dash.rotation.y = Math.atan2(-rx * Math.sin(a), rz * Math.cos(a));
    }

    const tile = (outer - inner) * rx / 16;
    for (let col = 0; col < 16; col++) {
      for (let row = 0; row < 2; row++) {
        mesh(scene, new THREE.BoxGeometry(tile, 0.025, 0.45),
          (col + row) % 2 ? 0x151922 : 0xfff4df,
          rx * inner + (col + 0.5) * tile, 0.05, (row - 0.5) * 0.45);
      }
    }

    for (let i = 0; i < 22; i++) {
      const a = i * turn / 22;
      const h = 2 + (i * 7 % 9) * 0.7;
      const rock = mesh(scene, new THREE.ConeGeometry(2 + i % 3, h, 5),
        i % 2 ? 0xab634e : 0x9b5260, 56 * Math.cos(a), h / 2, 41 * Math.sin(a));
      rock.rotation.y = i;
    }

    const car = new THREE.Group();
    scene.add(car);
    car.position.set(rx, 0, 0);
    mesh(car, new THREE.BoxGeometry(1.55, 0.48, 2.7), 0x17c4bc, 0, 0.52, 0);
    mesh(car, new THREE.BoxGeometry(1.17, 0.43, 1.25), 0x243956, 0, 0.94, -0.19);
    const wheel = new THREE.CylinderGeometry(0.31, 0.31, 0.27, 8);
    for (const x of [-0.81, 0.81]) {
      for (const z of [-0.86, 0.86]) {
        mesh(car, wheel, 0x171920, x, 0.33, z).rotation.z = Math.PI / 2;
      }
      mesh(car, new THREE.BoxGeometry(0.24, 0.13, 0.06),
        0xff4239, x * 0.77, 0.56, -1.36);
    }

    const controls = new Set([
      'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'KeyW', 'KeyA', 'KeyS', 'KeyD'
    ]);
    const keys = new Set();
    addEventListener('keydown', e => {
      if (!controls.has(e.code)) return;
      e.preventDefault();
      keys.add(e.code);
    });
    addEventListener('keyup', e => keys.delete(e.code));
    addEventListener('blur', () => keys.clear());

    const pressed = (arrow, letter) => Number(keys.has(arrow) || keys.has(letter));
    const lapDisplay = document.querySelector('#lap');
    const bestDisplay = document.querySelector('#best');
    const format = ms => `${(ms / 1000).toFixed(2)} s`;
    const follow = new THREE.Vector3();

    let speed = 0, heading = 0, previousAngle = 0, progress = 0;
    let lapStart = null, best = Infinity, lastFrame;

    function frame(now) {
      const dt = lastFrame === undefined ? 0 : Math.min((now - lastFrame) / 1000, 0.05);
      lastFrame = now;

      const throttle = pressed('ArrowUp', 'KeyW') - pressed('ArrowDown', 'KeyS');
      const steer = pressed('ArrowLeft', 'KeyA') - pressed('ArrowRight', 'KeyD');
      speed = THREE.MathUtils.clamp(speed + throttle * 24 * dt, -9, 30);
      if (!throttle) speed *= Math.exp(-1.8 * dt);
      heading += steer * Math.sign(speed) * Math.min(Math.abs(speed) / 5, 1) * 2.2 * dt;

      const p = car.position;
      p.x += Math.sin(heading) * speed * dt;
      p.z += Math.cos(heading) * speed * dt;
      car.rotation.y = heading;

      // Arcade rails: keep the car on the road; no off-road shortcuts.
      const radius = Math.hypot(p.x / rx, p.z / rz);
      const clamped = THREE.MathUtils.clamp(radius, inner + 0.035, outer - 0.035);
      if (radius !== clamped) {
        p.x *= clamped / radius;
        p.z *= clamped / radius;
        speed *= Math.exp(-4 * dt);
      }

      // Signed, unwrapped angle: reversing cancels progress instead of adding to it.
      const angle = Math.atan2(p.z / rz, p.x / rx);
      const delta = THREE.MathUtils.euclideanModulo(angle - previousAngle + Math.PI, turn) - Math.PI;
      previousAngle = angle;
      if (lapStart === null && speed !== 0) lapStart = now;
      progress += delta;
      if (progress >= turn) {
        const finish = now - dt * 1000 * (progress - turn) / delta;
        best = Math.min(best, finish - lapStart);
        bestDisplay.textContent = format(best);
        lapStart = finish;
        progress -= turn;
      }
      lapDisplay.textContent = format(lapStart === null ? 0 : now - lapStart);

      follow.set(p.x - 8 * Math.sin(heading), 5.5, p.z - 8 * Math.cos(heading));
      camera.position.lerp(follow, dt ? 1 - Math.exp(-7 * dt) : 1);
      camera.lookAt(p.x + 3 * Math.sin(heading), 0.6, p.z + 3 * Math.cos(heading));
      renderer.render(scene, camera);
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  </script>
</body>
</html>
```

Save as `index.html` and open it in a WebGL-capable browser with internet access for the Three.js CDN import. If your browser blocks modules from local files, serve the folder with `python -m http.server 8000` and visit `http://localhost:8000`.

**How I’d verify it** — I haven’t run it here:

1. Load the page. Confirm the track, car, and HUD appear with no console errors. The timer should stay at `0.00 s` until the car moves.
2. Drive with both WASD and the arrow keys. At the start, steer right to follow the bend. Check that the camera follows, the car slows at the road edges, and resizing doesn’t stretch the view.
3. Complete a forward lap. The best time should appear and the current timer should roll over. Drive a slower lap, then a faster one: only the faster lap should replace the best.
4. Back across the start line and drive forward across it again. That alone should not count as a lap. Switch tabs while holding a key and confirm it isn’t stuck when you return.

Best lap is session-only; reload to start fresh.


=============== RESPONSE ambition-game-20 ===============

Save this as `index.html` to play **Pine Loop**, a single-track Three.js racer with a chase camera, a lap timer, and a best lap saved in the browser. It needs an internet connection to load Three.js, but no build step or downloaded assets.

**Data shape.** The track is a closed centerline with a fixed road width. The car state holds distance along the loop, lateral offset, and speed. The race state holds the current lap time, completed lap count, and best time.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pine Loop</title>
<style>
  * { box-sizing: border-box }
  html, body { margin: 0; min-height: 100%; background: #142a26; color: #fff }
  body { font: 16px system-ui, sans-serif }
  canvas { position: fixed; inset: 0; display: block; z-index: 0 }
  main { position: relative; z-index: 1; padding: 16px; pointer-events: none }
  .panel {
    width: fit-content; max-width: 100%; padding: 14px 16px;
    background: #10201e; border: 1px solid #56756c; border-radius: 12px;
  }
  h1 { margin: 0; font-size: 1.25rem }
  dl { display: flex; flex-wrap: wrap; gap: 8px 22px; margin: 12px 0 0 }
  dt { color: #b9d9cd; font-size: .8rem }
  dd { margin: 3px 0 0; font-weight: 700; font-variant-numeric: tabular-nums }
  p { margin: 10px 0 0; font-size: .85rem }
  #status { color: #ffe498 }
</style>
</head>
<body>
<main>
  <section class="panel" aria-label="Race dashboard">
    <h1>Pine Loop</h1>
    <dl>
      <div><dt>Lap</dt><dd id="lap">1</dd></div>
      <div><dt>Time</dt><dd id="time">0:00.000</dd></div>
      <div><dt>Best</dt><dd id="best">None yet</dd></div>
    </dl>
    <p>↑ / W accelerate · ↓ / S brake<br>← → / A D steer · R restart</p>
    <p id="status" role="status">Loading Three.js…</p>
  </section>
</main>

<script type="module">
const status = document.getElementById('status');

try {
  const THREE = await import('https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js');
  start(THREE);
} catch (error) {
  status.textContent = 'Could not start. Check your connection and WebGL support, then reload.';
  console.error(error);
}

function start(T) {
  const lapText = document.getElementById('lap');
  const timeText = document.getElementById('time');
  const bestText = document.getElementById('best');
  const scene = new T.Scene();
  scene.background = new T.Color(0xa9d8db);
  scene.fog = new T.Fog(0xa9d8db, 60, 160);
  const camera = new T.PerspectiveCamera(60, 1, 0.1, 240);
  const renderer = new T.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.domElement.setAttribute('aria-hidden', 'true');
  document.body.prepend(renderer.domElement);

  function resize() {
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
  }
  addEventListener('resize', resize);
  resize();

  scene.add(new T.HemisphereLight(0xfff6de, 0x547463, 2));
  const sun = new T.DirectionalLight(0xffe1a3, 2);
  sun.position.set(-30, 45, 20);
  scene.add(sun);

  const centerline = new T.CatmullRomCurve3(
    [[0, 35], [-27, 32], [-43, 11], [-39, -18],
     [-13, -32], [14, -25], [37, -30], [47, -7], [32, 25]]
      .map(([x, z]) => new T.Vector3(x, 0, z)),
    true
  );
  centerline.arcLengthDivisions = 1000;
  const length = centerline.getLength();
  const halfWidth = 4.5;
  const wrap = d => ((d % length) + length) % length;

  function trackFrame(distance) {
    const u = wrap(distance) / length;
    const point = centerline.getPointAt(u);
    const forward = centerline.getTangentAt(u);
    const right = new T.Vector3(-forward.z, 0, forward.x);
    return { point, forward, right };
  }

  function mesh(parent, geometry, color, x, y, z) {
    const object = new T.Mesh(geometry, new T.MeshStandardMaterial({
      color, flatShading: true
    }));
    object.position.set(x, y, z);
    parent.add(object);
    return object;
  }

  function strip(from, to, left, right, height, color, segments) {
    const vertices = [];
    const indices = [];
    for (let i = 0; i <= segments; i++) {
      const frame = trackFrame(from + (to - from) * i / segments);
      for (const offset of [left, right]) {
        const p = frame.point.clone().addScaledVector(frame.right, offset);
        vertices.push(p.x, height, p.z);
      }
      if (i < segments) {
        const a = 2 * i;
        indices.push(a, a + 1, a + 2, a + 1, a + 3, a + 2);
      }
    }
    const geometry = new T.BufferGeometry();
    geometry.setAttribute('position', new T.Float32BufferAttribute(vertices, 3));
    geometry.setIndex(indices);
    geometry.computeVertexNormals();
    return mesh(scene, geometry, color, 0, 0, 0);
  }

  mesh(scene, new T.BoxGeometry(400, 1, 400), 0x57896b, 0, -0.53, 0);
  strip(0, length, -halfWidth, halfWidth, 0, 0x303946, 400);
  for (const side of [-1, 1]) {
    const edge = side * (halfWidth - 0.2);
    strip(0, length, edge - 0.08, edge + 0.08, 0.015, 0xf7edcd, 400);
  }
  for (let d = 5; d < length - 4; d += 6) {
    strip(d, d + 2, -0.065, 0.065, 0.016, 0xf7ce72, 4);
  }
  for (let row = 0; row < 2; row++) {
    for (let column = 0; column < 12; column++) {
      const x = -halfWidth + column * 0.75;
      strip((row - 1) * 0.6, row * 0.6, x, x + 0.75, 0.024,
        (row + column) % 2 ? 0xfaf5e5 : 0x151b22, 3);
    }
  }

  const samples = Array.from({ length: 150 }, (_, i) =>
    trackFrame(i * length / 150).point
  );
  const trunk = new T.CylinderGeometry(0.17, 0.23, 1.5, 5);
  const crown = new T.ConeGeometry(1.3, 3.6, 5);
  let seed = 23;
  function random() {
    seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
    return seed / 4294967296;
  }
  for (let i = 0; i < 145; i++) {
    const x = (random() - 0.5) * 150;
    const z = (random() - 0.5) * 125;
    if (samples.some(p => (p.x - x) ** 2 + (p.z - z) ** 2 < 8 ** 2)) continue;
    mesh(scene, trunk, 0x664935, x, 0.75, z);
    const tree = mesh(scene, crown, i % 2 ? 0x245947 : 0x326d54, x, 2.6, z);
    tree.rotation.y = random() * Math.PI;
  }

  const car = new T.Group();
  scene.add(car);
  mesh(car, new T.BoxGeometry(1.55, 0.42, 2.8), 0xf35539, 0, 0.43, 0);
  mesh(car, new T.BoxGeometry(1.16, 0.46, 1.13), 0x263b52, 0, 0.81, -0.2);
  mesh(car, new T.BoxGeometry(1.7, 0.12, 0.36), 0xf9b74d, 0, 0.77, -1.19);
  const tire = new T.CylinderGeometry(0.32, 0.32, 0.23, 10);
  for (const x of [-0.78, 0.78]) {
    for (const z of [-0.87, 0.87]) {
      mesh(car, tire, 0x172024, x, 0.32, z).rotation.z = Math.PI / 2;
    }
    mesh(car, new T.BoxGeometry(0.29, 0.13, 0.06), 0xffe09a, x * 0.7, 0.47, 1.41);
  }

  const storageKey = 'pine-loop-best-v1';
  let best = null;
  try {
    const saved = Number(localStorage.getItem(storageKey));
    if (Number.isFinite(saved) && saved > 0) best = saved;
  } catch {}

  const drive = { distance: 0, offset: 0, speed: 0, steer: 0 };
  const race = { elapsed: 0, completed: 0, running: false };
  const keys = new Set();
  const controls = new Set([
    'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
    'KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyR'
  ]);
  const held = (a, b) => keys.has(a) || keys.has(b);
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');

  function format(seconds) {
    const ms = Math.floor(seconds * 1000);
    const minutes = Math.floor(ms / 60000);
    const wholeSeconds = String(Math.floor(ms / 1000) % 60).padStart(2, '0');
    return `${minutes}:${wholeSeconds}.${String(ms % 1000).padStart(3, '0')}`;
  }

  function reset() {
    Object.assign(drive, { distance: 0, offset: 0, speed: 0, steer: 0 });
    Object.assign(race, { elapsed: 0, completed: 0, running: false });
    status.textContent = 'Accelerate to start the clock.';
  }
  addEventListener('keydown', event => {
    if (!controls.has(event.code) || event.ctrlKey || event.metaKey || event.altKey) return;
    event.preventDefault();
    if (event.code === 'KeyR' && !event.repeat) {
      keys.clear();
      reset();
    } else if (event.code !== 'KeyR') {
      keys.add(event.code);
    }
  });
  addEventListener('keyup', event => keys.delete(event.code));
  addEventListener('blur', () => keys.clear());
  document.addEventListener('visibilitychange', () => keys.clear());

  function update(dt) {
    const throttle = held('ArrowUp', 'KeyW');
    const brake = held('ArrowDown', 'KeyS');
    const targetSteer = Number(held('ArrowRight', 'KeyD')) -
      Number(held('ArrowLeft', 'KeyA'));
    drive.steer += (targetSteer - drive.steer) * (1 - Math.exp(-10 * dt));

    if (!race.running && throttle && !brake) {
      race.running = true;
      status.textContent = '';
    }

    const edge = Math.abs(drive.offset) > halfWidth - 1;
    const maxSpeed = edge ? 14 : 32;
    const acceleration = brake ? -34 : throttle ? 17 : -7;
    drive.speed = T.MathUtils.clamp(drive.speed + acceleration * dt, 0, maxSpeed);
    drive.offset = T.MathUtils.clamp(
      drive.offset + drive.steer * drive.speed * 0.24 * dt,
      -halfWidth + 0.55, halfWidth - 0.55
    );

    if (!race.running) return;
    const advance = drive.speed * dt * (1 - 0.18 * Math.abs(drive.steer));
    const nextDistance = drive.distance + advance;
    if (nextDistance >= length) {
      const toLine = dt * (length - drive.distance) / advance;
      const result = race.elapsed + toLine;
      race.completed++;
      if (best === null || result < best) {
        best = result;
        try { localStorage.setItem(storageKey, String(best)); } catch {}
        status.textContent = `New best lap · ${format(result)}`;
      } else {
        status.textContent = `Last lap · ${format(result)}`;
      }
      race.elapsed = dt - toLine;
      drive.distance = nextDistance - length;
    } else {
      race.elapsed += dt;
      drive.distance = nextDistance;
    }
  }

  function draw() {
    const frame = trackFrame(drive.distance);
    car.position.copy(frame.point).addScaledVector(frame.right, drive.offset);
    car.rotation.y = Math.atan2(frame.forward.x, frame.forward.z) -
      drive.steer * 0.24 * Math.min(1, drive.speed / 5);
    camera.position.copy(frame.point).addScaledVector(frame.forward, -11);
    camera.position.y = reducedMotion.matches ? 11 : 7.5;
    const target = trackFrame(drive.distance + 9).point;
    camera.lookAt(target.x, 0.7, target.z);
    lapText.textContent = race.completed + 1;
    timeText.textContent = format(race.elapsed);
    bestText.textContent = best === null ? 'None yet' : format(best);
    renderer.render(scene, camera);
  }

  reset();
  let last = performance.now();
  let accumulator = 0;
  const step = 1 / 120;
  renderer.setAnimationLoop(now => {
    const dt = Math.min(0.1, Math.max(0, (now - last) / 1000));
    last = now;
    if (document.hidden || !document.hasFocus()) {
      accumulator = 0;
    } else {
      accumulator += dt;
      while (accumulator >= step) {
        update(step);
        accumulator -= step;
      }
    }
    if (!document.hidden) draw();
  });
}
</script>
</body>
</html>
```

### Run and verify

I did not run the game here. These are the checks I would run in a browser:

1. **Load it.** In the folder with `index.html`, run `python3 -m http.server 8000` and open `http://localhost:8000`. Expect a continuous road, a car at the checkered line, lap 1, a zero timer, and `None yet` on a fresh origin. Check the console for errors.
2. **Drive it.** Test both key sets. Confirm left and right move the car in the expected direction, braking stops it, and the road edge slows it down. Stop mid-lap and confirm the timer keeps counting. Switch tabs and confirm the clock pauses and the keys do not stick on return.
3. **Check lap scoring.** Hold accelerate without steering for a full circuit. Expect the lap count to advance once at the line and the best time to populate. Brake during the next lap to make it slower. Expect the best time to stay unchanged. Press **R** mid-lap, then reload. The current run should reset both times, and the best should survive on the same origin.
4. **Check the dashboard.** Try a 320px viewport, 200% zoom, and reduced-motion mode. Check that labels wrap without clipping and that reduced motion uses the higher chase view. Block the CDN and reload to check that the page gives a recovery message instead of staying on “Loading Three.js…”.

### Design and throughput checkpoint

| Option | Decision |
|---|---|
| Free steering with checkpoint gates | More driving freedom, but it needs collision and shortcut rules. |
| Track-relative steering | Used here. The car follows bends, and the player controls speed and lateral position. A full circuit is the only way to score a lap. |

- **Blocking first steps.** Choose the driving model and define what counts as a lap before drawing the track.
- **Independent workstreams.** The dashboard and scenery can be reviewed separately against the same game state. No subagent tools were available here.
- **Shared mutable state.** One update loop owns race and drive state. Rendering reads it.
- **Smallest safe decomposition.** One HTML file with separate track, update, and draw functions. No build system.

**Principles applied.** *Model the domain* led to track-relative distance and lateral offset. *Boundary discipline* led to validating the saved best time on load and letting the game run if storage is unavailable. *Prove it works* puts lap scoring, persistence, and layout checks in the actual browser. Runtime verification remains open.


=============== RESPONSE ambition-game-21 ===============

Save this as `index.html` to play **Mesa Circuit**, a single-track Three.js racer with keyboard controls, a lap timer, and a best lap saved in your browser. The game uses one file and no art assets. I reviewed the code by inspection but could not run it here.

**Data shape.** The track is a closed curve. The car has a distance along that curve, a sideways offset, and a speed. The timer is either waiting for the first move or running. I chose track-relative steering over free-roaming physics so braking and cornering still matter, but cutting across the infield cannot advance the lap.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mesa Circuit</title>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; background: #21191b; color: #fff4e1; font: 16px system-ui, sans-serif; }
  canvas { display: block; width: 100%; height: 100%; }
  #view { position: fixed; inset: 0; }
  .hud {
    position: relative; width: min(25rem, calc(100% - 2rem)); margin: 1rem;
    background: #21191b; border: 1px solid #8d6559; padding: 1rem;
    border-radius: .75rem; pointer-events: none;
  }
  h1 { margin: 0; font-size: 1.35rem; letter-spacing: .06em; }
  dl { display: flex; flex-wrap: wrap; gap: .5rem 1.25rem; margin: .75rem 0; }
  dt { color: #ffbf89; font-size: .8rem; text-transform: uppercase; }
  dd { margin: 0; font: bold 1.15rem ui-monospace, monospace; overflow-wrap: anywhere; }
  p { margin: .4rem 0 0; font-size: .85rem; }
</style>
</head>
<body>
<div id="view" aria-hidden="true"></div>
<header class="hud">
  <h1>MESA CIRCUIT</h1>
  <dl>
    <div><dt>Lap time</dt><dd id="lap">0.00 s</dd></div>
    <div><dt>Best lap</dt><dd id="best">None</dd></div>
    <div><dt>Speed</dt><dd id="speed">0 km/h</dd></div>
  </dl>
  <p>W / ↑ accelerate · S / ↓ brake</p>
  <p>A / ← and D / → steer · R restart</p>
  <p id="status" role="status">Loading Three.js…</p>
</header>

<script type="module">
const el = id => document.getElementById(id);
const status = el('status');

async function main() {
  const T = await import('https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js');
  const scene = new T.Scene();
  scene.background = new T.Color(0xffcba4);
  scene.fog = new T.FogExp2(0xffcba4, 0.004);
  const camera = new T.PerspectiveCamera(58, 1, 0.1, 650);
  const renderer = new T.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  el('view').append(renderer.domElement);

  const V = (x, y, z) => new T.Vector3(x, y, z);
  const clamp = T.MathUtils.clamp;
  const track = new T.CatmullRomCurve3([
    V(-48,0,36), V(10,0,47), V(55,0,27), V(62,0,-7),
    V(26,0,-17), V(12,0,-46), V(-36,0,-48), V(-65,0,-12)
  ], true);
  track.arcLengthDivisions = 1600;
  const length = track.getLength();
  const halfRoad = 6;
  const wrap = n => ((n % 1) + 1) % 1;
  const rightOf = v => V(-v.z, 0, v.x);
  const point = (fraction, offset, y) => {
    const u = wrap(fraction);
    return track.getPointAt(u).addScaledVector(rightOf(track.getTangentAt(u)), offset)
      .setY(y);
  };

  function strip(lo, hi, y, color, from = 0, to = 1, segments = 320) {
    const vertices = [], indices = [];
    for (let i = 0; i <= segments; i++) {
      const u = from + (to - from) * i / segments;
      vertices.push(...point(u, lo, y).toArray(), ...point(u, hi, y).toArray());
      if (i < segments) {
        const k = 2 * i;
        indices.push(k, k + 1, k + 2, k + 1, k + 3, k + 2);
      }
    }
    const geometry = new T.BufferGeometry();
    geometry.setAttribute('position', new T.Float32BufferAttribute(vertices, 3));
    geometry.setIndex(indices);
    scene.add(new T.Mesh(geometry, new T.MeshBasicMaterial({ color, side: T.DoubleSide })));
  }

  function mesh(parent, geometry, color, x, y, z) {
    const model = new T.Mesh(geometry, new T.MeshStandardMaterial({ color, flatShading: true }));
    model.position.set(x, y, z);
    parent.add(model);
    return model;
  }

  scene.add(new T.HemisphereLight(0xffe5cd, 0xa35c41, 2.1));
  const sun = new T.DirectionalLight(0xffe5c1, 2.4);
  sun.position.set(-45, 70, 30);
  scene.add(sun);
  mesh(scene, new T.BoxGeometry(900, 1, 900), 0xc77b52, 0, -0.55, 0);

  strip(-halfRoad, halfRoad, 0, 0x36333b);
  strip(-5.75, -5.55, .015, 0xffe2aa);
  strip(5.55, 5.75, .015, 0xffe2aa);
  for (let i = 0; i < 48; i++) {
    strip(-.06, .06, .018, 0x9c9291, i / 48, (i + .48) / 48, 2);
  }
  for (let row = 0; row < 2; row++) {
    for (let col = 0; col < 12; col++) {
      strip(col - 6, col - 5, .025, (row + col) % 2 ? 0x221e24 : 0xfff2d8,
        (row - 2) / length, (row - 1) / length, 2);
    }
  }

  const rock = new T.DodecahedronGeometry(1, 0);
  for (let i = 0; i < 58; i++) {
    const a = i * 2.399963;
    const r = 82 + 8 * (i % 7);
    const h = 2 + (i * 13 % 11);
    const boulder = mesh(scene, rock, i % 2 ? 0xb5563b : 0x92472f,
      Math.cos(a) * r, h * .45, Math.sin(a) * r);
    boulder.scale.set(2 + i % 5, h, 2 + i % 4);
    boulder.rotation.y = a;
  }

  const car = new T.Group();
  scene.add(car);
  mesh(car, new T.BoxGeometry(1.75, .55, 3.25), 0xff5338, 0, .62, 0);
  mesh(car, new T.BoxGeometry(1.3, .55, 1.4), 0x253d53, 0, 1.06, -.25);
  mesh(car, new T.BoxGeometry(1.7, .14, .4), 0xffc265, 0, 1, -1.35);
  const wheel = new T.CylinderGeometry(.37, .37, .28, 8);
  for (const x of [-.88, .88]) {
    for (const z of [-1.05, 1.05]) {
      mesh(car, wheel, 0x242129, x, .37, z).rotation.z = Math.PI / 2;
    }
  }

  const storageKey = 'mesa-circuit-v1-best-seconds';
  let best = null;
  try {
    const stored = Number(localStorage.getItem(storageKey));
    if (Number.isFinite(stored) && stored > 0) best = stored;
  } catch {}
  const format = seconds => `${seconds.toFixed(2)} s`;
  const drawBest = () => { el('best').textContent = best === null ? 'None' : format(best); };
  drawBest();

  const keys = new Set();
  const controls = ['KeyW','KeyA','KeyS','KeyD','ArrowUp','ArrowDown','ArrowLeft','ArrowRight','KeyR'];
  const held = (...codes) => codes.some(code => keys.has(code));
  const driver = { distance: 0, offset: 0, speed: 0, startedAt: null };
  function reset() {
    Object.assign(driver, { distance: 0, offset: 0, speed: 0, startedAt: null });
    keys.clear();
    status.textContent = 'Accelerate to start your lap.';
  }
  reset();
  addEventListener('keydown', e => {
    if (e.altKey || e.ctrlKey || e.metaKey || !controls.includes(e.code)) return;
    e.preventDefault();
    if (e.code === 'KeyR' && !e.repeat) reset();
    else keys.add(e.code);
  });
  addEventListener('keyup', e => keys.delete(e.code));
  addEventListener('blur', () => keys.clear());
  document.addEventListener('visibilitychange', () => keys.clear());

  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  function resize() {
    camera.aspect = innerWidth / Math.max(1, innerHeight);
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight, false);
  }
  addEventListener('resize', resize);
  resize();

  function drive(dt, now) {
    const steer = Number(held('KeyD', 'ArrowRight')) - Number(held('KeyA', 'ArrowLeft'));
    const brake = held('KeyS', 'ArrowDown');
    const gas = held('KeyW', 'ArrowUp');
    const gravel = Math.abs(driver.offset) > halfRoad - .7;
    const cap = gravel ? 11 : 34;
    const acceleration = brake ? -37 : gas && driver.speed < cap ? 22 : -5;
    const before = driver.speed;
    driver.speed = clamp(before + acceleration * dt, 0, Math.max(before, cap));
    if (driver.speed > cap) driver.speed = Math.max(cap, driver.speed - 28 * dt);

    if (driver.speed === 0 && before === 0) return;
    if (driver.startedAt === null) {
      driver.startedAt = now - dt;
      status.textContent = 'Stay on the asphalt to keep your speed.';
    }

    const travel = (before + driver.speed) * .5 * dt;
    const u = driver.distance / length;
    const tangent = track.getTangentAt(wrap(u));
    const next = track.getTangentAt(wrap(u + 3 / length));
    const bend = next.dot(rightOf(tangent));
    driver.offset = clamp(driver.offset + (
      steer * driver.speed * .37 - bend * driver.speed ** 2 * .21
    ) * dt, -10, 10);

    driver.distance += travel;
    if (driver.distance >= length) {
      driver.distance -= length;
      const crossing = now - dt * driver.distance / travel;
      const lap = crossing - driver.startedAt;
      driver.startedAt = crossing;
      if (best === null || lap < best) {
        best = lap;
        drawBest();
        try { localStorage.setItem(storageKey, String(best)); } catch {}
        status.textContent = `New best lap: ${format(lap)}`;
      } else {
        status.textContent = `Last lap: ${format(lap)}`;
      }
    }
  }

  let previous = performance.now() / 1000;
  renderer.setAnimationLoop(milliseconds => {
    const now = milliseconds / 1000;
    const dt = clamp(now - previous, 0, .05);
    previous = now;
    drive(dt, now);

    const u = driver.distance / length;
    const tangent = track.getTangentAt(wrap(u));
    car.position.copy(point(u, driver.offset, 0));
    car.rotation.y = Math.atan2(tangent.x, tangent.z);
    if (reducedMotion.matches) {
      camera.position.set(0, 155, 95);
      camera.position.multiplyScalar(Math.max(1, 1.3 / camera.aspect));
      camera.lookAt(0, 0, 0);
    } else {
      camera.position.copy(point(u, driver.offset * .55, 8))
        .addScaledVector(tangent, -12);
      camera.lookAt(point(u + 8 / length, driver.offset * .35, 1));
    }

    el('lap').textContent = format(driver.startedAt === null ? 0 : now - driver.startedAt);
    el('speed').textContent = `${Math.round(driver.speed * 3.6)} km/h`;
    renderer.render(scene, camera);
  });
}

main().catch(error => {
  status.textContent = 'Could not start. Check your internet connection and WebGL support, then reload.';
  console.error(error);
});
</script>
</body>
</html>
```

### Run and verify

From the folder containing `index.html`, run `python -m http.server 8000` and open `http://localhost:8000/`. The page needs internet access to load the pinned Three.js module.

These are expected results, not measured passes:

| Check | Expected result |
|---|---|
| Open the page and check the browser console | The track and car render without errors. The lap timer reads `0.00 s`. |
| Drive using both WASD and the arrow keys | Acceleration starts the clock. Steering moves the car sideways. Braking slows it, and riding the gravel drops the top speed. Arrow keys do not scroll the page. |
| Cross the finish line after a full circuit | The lap timer restarts. The first completed lap sets a best. A slower lap leaves it alone, and a faster one replaces it. |
| Press `R` mid-lap, then reload | `R` resets the current run without recording it or clearing the best. Reload preserves the best when browser storage is available. |
| Switch tabs while holding a key | That key is no longer held on return. An active lap still counts elapsed time. |
| Test at 320 px wide, 200% zoom, and with reduced motion enabled | The HUD text wraps without clipping. Reduced motion uses a fixed overview instead of the moving chase camera. |

**Throughput checkpoint.** The blocking decision was the track and timing model. Independent workstreams were not needed for one file. The animation loop owns mutable race state, with restart handled by the same state model. One implementation keeps the road, crossing, and reset logic together. No delegation or browser runs were available in this chat.

**Principles used.** *Model the domain* led to a single lap distance and a nullable start time rather than separate checkpoint and timer flags. *Prove it works* led to browser checks that exercise complete laps, restart, and reload rather than stopping at a render check.


=============== RESPONSE ambition-game-22 ===============

Save this as `index.html`. It’s a complete single-file racer with a closed track, a chase camera, keyboard controls, and a best lap that persists across reloads. Three.js loads from a CDN, so the game needs an internet connection.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pine Loop Racer</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; overflow: hidden; background: #a9d8ed; font: 16px system-ui, sans-serif; }
    canvas { display: block; }
    #hud {
      position: fixed; top: 16px; left: 16px; z-index: 1;
      padding: 14px 18px; border-radius: 12px;
      background: #10221dec; color: white; font-variant-numeric: tabular-nums;
      pointer-events: none;
    }
    h1 { margin: 0 0 8px; font-size: 18px; color: #b8ffad; }
    #hud div { display: flex; justify-content: space-between; gap: 24px; }
    #status { margin: 10px 0 0; color: #b8ffad; font-size: 13px; }
    #controls {
      position: fixed; bottom: 14px; left: 50%; transform: translateX(-50%);
      width: max-content; max-width: calc(100% - 24px); text-align: center;
      padding: 8px 14px; border-radius: 10px; background: #10221dec; color: white;
      font-size: 13px; z-index: 1; pointer-events: none;
    }
  </style>
</head>
<body>
  <section id="hud" aria-label="Race timing">
    <h1>Pine Loop Racer</h1>
    <div><span>Current lap</span><strong id="lap">0:00.000</strong></div>
    <div><span>Best lap</span><strong id="best">—</strong></div>
    <p id="status">Cross the line to start timing.</p>
  </section>
  <div id="controls">WASD / arrows: drive · Space: brake · R: restart</div>

  <script type="module">
    import * as T from 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js';

    const scene = new T.Scene();
    scene.background = new T.Color(0xa9d8ed);
    scene.fog = new T.Fog(0xa9d8ed, 85, 200);
    const camera = new T.PerspectiveCamera(63, innerWidth / innerHeight, 0.1, 300);
    const renderer = new T.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setSize(innerWidth, innerHeight);
    document.body.appendChild(renderer.domElement);

    scene.add(new T.HemisphereLight(0xfff5db, 0x548055, 2.0));
    const sun = new T.DirectionalLight(0xffe2ac, 2.2);
    sun.position.set(-35, 55, 20);
    scene.add(sun);

    const material = color => new T.MeshStandardMaterial({ color, flatShading: true });
    const mesh = (geometry, mat, parent, x = 0, y = 0, z = 0) => {
      const m = new T.Mesh(geometry, mat);
      m.position.set(x, y, z);
      parent.add(m);
      return m;
    };
    const box = (w, h, d, mat, parent, x, y, z) =>
      mesh(new T.BoxGeometry(w, h, d), mat, parent, x, y, z);
    const ground = mesh(new T.PlaneGeometry(500, 500), material(0x69994f), scene);
    ground.rotation.x = -Math.PI / 2;

    const track = new T.CatmullRomCurve3(
      [[-37, 18], [-15, 31], [17, 30], [43, 13], [41, -14],
       [18, -28], [-7, -20], [-30, -27], [-48, -9]]
        .map(([x, z]) => new T.Vector3(x, 0, z)),
      true
    );
    track.arcLengthDivisions = 1000;
    const N = 320, halfWidth = 5;
    const wrap = i => (i % N + N) % N;
    const samples = Array.from({ length: N }, (_, i) => {
      const p = track.getPointAt(i / N);
      const tangent = track.getTangentAt(i / N);
      return { p, tangent, side: new T.Vector3(-tangent.z, 0, tangent.x) };
    });

    function strip(left, right, y, colors, colorIndex = () => 0, visible = () => true) {
      const vertices = [], rgb = [];
      const palette = colors.map(c => new T.Color(c));
      for (let i = 0; i < N; i++) {
        if (!visible(i)) continue;
        const a = samples[i], b = samples[wrap(i + 1)];
        const color = palette[colorIndex(i)];
        for (const [s, offset] of [[a, left], [b, left], [a, right],
                                  [a, right], [b, left], [b, right]]) {
          vertices.push(s.p.x + s.side.x * offset, y, s.p.z + s.side.z * offset);
          rgb.push(color.r, color.g, color.b);
        }
      }
      const geo = new T.BufferGeometry();
      geo.setAttribute('position', new T.Float32BufferAttribute(vertices, 3));
      geo.setAttribute('color', new T.Float32BufferAttribute(rgb, 3));
      geo.computeVertexNormals();
      mesh(geo, new T.MeshStandardMaterial({ vertexColors: true, side: T.DoubleSide }), scene);
    }
    strip(-5, 5, 0.025, [0x333b46]);
    strip(-5.45, -5, 0.03, [0xf4eee0, 0xda483b], i => (i >> 2) % 2);
    strip(5, 5.45, 0.03, [0xf4eee0, 0xda483b], i => (i >> 2) % 2);
    strip(-0.06, 0.06, 0.035, [0xe3c76e], undefined, i => i % 12 < 5);

    const start = new T.Group();
    scene.add(start);
    start.position.copy(samples[0].p);
    start.rotation.y = Math.atan2(samples[0].tangent.x, samples[0].tangent.z);
    const checker = [material(0xf9f7ed), material(0x171d23)];
    for (let row = 0; row < 2; row++) {
      for (let col = 0; col < 20; col++) {
        box(0.5, 0.02, 0.42, checker[(row + col) % 2], start,
            -4.75 + col * 0.5, 0.045, (row - 0.5) * 0.42);
      }
    }

    function nearest(x, z) {
      let index = 0, distance2 = Infinity;
      for (let i = 0; i < N; i++) {
        const { p } = samples[i];
        const d = (x - p.x) ** 2 + (z - p.z) ** 2;
        if (d < distance2) { index = i; distance2 = d; }
      }
      return { index, distance2 };
    }

    let seed = 913;
    function random() {
      seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
      return seed / 4294967296;
    }
    const trunk = material(0x77503b);
    const leaves = [material(0x246040), material(0x37794b), material(0x4b9051)];
    const trunkGeo = new T.CylinderGeometry(0.2, 0.28, 1.6, 5);
    const leavesGeo = new T.ConeGeometry(1.3, 3.1, 5);
    for (let i = 0; i < 240; i++) {
      const x = (random() - 0.5) * 175, z = (random() - 0.5) * 140;
      if (nearest(x, z).distance2 < 9 ** 2) continue;
      const tree = new T.Group();
      scene.add(tree);
      tree.position.set(x, 0, z);
      tree.rotation.y = random() * Math.PI * 2;
      tree.scale.setScalar(0.6 + random() * 0.9);
      mesh(trunkGeo, trunk, tree, 0, 0.8, 0);
      mesh(leavesGeo, leaves[i % 3], tree, 0, 2.35, 0);
    }

    const car = new T.Group();
    scene.add(car);
    const red = material(0xe64430), glass = material(0x344f67);
    const rubber = material(0x192027), lights = material(0xffecc0);
    box(1.75, 0.46, 3.15, red, car, 0, 0.64, 0);
    box(1.33, 0.49, 1.45, glass, car, 0, 1.06, -0.32);
    box(1.30, 0.10, 1.30, red, car, 0, 1.34, -0.34);
    const tireGeo = new T.CylinderGeometry(0.36, 0.36, 0.31, 10);
    for (const x of [-0.91, 0.91]) {
      for (const z of [-1.05, 1.05]) {
        mesh(tireGeo, rubber, car, x, 0.38, z).rotation.z = Math.PI / 2;
      }
    }
    for (const x of [-0.59, 0.59]) box(0.32, 0.17, 0.05, lights, car, x, 0.69, 1.59);

    const lapEl = document.querySelector('#lap');
    const bestEl = document.querySelector('#best');
    const status = document.querySelector('#status');
    const bestKey = 'pine-loop-best-v1';
    let best = Infinity;
    try {
      const saved = Number(localStorage.getItem(bestKey));
      if (Number.isFinite(saved) && saved > 0) best = saved;
    } catch { /* Timing still works when storage is unavailable. */ }

    function format(seconds) {
      const ms = Math.floor(seconds * 1000);
      return `${Math.floor(ms / 60000)}:${String(Math.floor(ms / 1000) % 60).padStart(2, '0')}.${String(ms % 1000).padStart(3, '0')}`;
    }
    bestEl.textContent = Number.isFinite(best) ? format(best) : '—';

    const keys = new Set();
    const drivingKeys = new Set([
      'KeyW', 'KeyA', 'KeyS', 'KeyD', 'ArrowUp', 'ArrowLeft',
      'ArrowDown', 'ArrowRight', 'Space', 'KeyR'
    ]);
    addEventListener('keydown', e => {
      if (!drivingKeys.has(e.code)) return;
      e.preventDefault();
      keys.add(e.code);
      if (e.code === 'KeyR' && !e.repeat) reset();
    });
    addEventListener('keyup', e => keys.delete(e.code));
    addEventListener('blur', () => keys.clear());
    addEventListener('resize', () => {
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(innerWidth, innerHeight);
    });

    let yaw, speed, lapStart, checkpoint;
    const checkpoints = [N / 4, N / 2, 3 * N / 4, 0];
    const cameraGoal = new T.Vector3(), look = new T.Vector3();

    function updateCamera(dt, snap = false) {
      const x = Math.sin(yaw), z = Math.cos(yaw);
      cameraGoal.set(car.position.x - x * 8.5, 5.6, car.position.z - z * 8.5);
      camera.position.lerp(cameraGoal, snap ? 1 : 1 - Math.exp(-7 * dt));
      look.set(car.position.x + x * 4, 0.9, car.position.z + z * 4);
      camera.lookAt(look);
    }

    function reset() {
      const s = samples[N - 8];
      car.position.copy(s.p);
      yaw = Math.atan2(s.tangent.x, s.tangent.z);
      car.rotation.y = yaw;
      speed = 0;
      lapStart = null;
      checkpoint = 0;
      lapEl.textContent = format(0);
      status.textContent = 'Cross the line to start timing.';
      updateCamera(0, true);
    }

    function crossGate(index, oldX, oldZ, x, z) {
      const { p, tangent, side } = samples[index];
      const a = (oldX - p.x) * tangent.x + (oldZ - p.z) * tangent.z;
      const b = (x - p.x) * tangent.x + (z - p.z) * tangent.z;
      if (!(a < 0 && b >= 0)) return null;
      const t = -a / (b - a);
      const lateral = (oldX + (x - oldX) * t - p.x) * side.x +
                      (oldZ + (z - oldZ) * t - p.z) * side.z;
      return Math.abs(lateral) <= halfWidth ? t : null;
    }

    reset();
    let previous = performance.now() / 1000;
    renderer.setAnimationLoop(() => {
      const now = performance.now() / 1000;
      const dt = Math.min(now - previous, 0.05);
      previous = now;

      const up = keys.has('KeyW') || keys.has('ArrowUp');
      const down = keys.has('KeyS') || keys.has('ArrowDown');
      const left = keys.has('KeyA') || keys.has('ArrowLeft');
      const right = keys.has('KeyD') || keys.has('ArrowRight');
      const oldX = car.position.x, oldZ = car.position.z;
      const offRoad = nearest(oldX, oldZ).distance2 > halfWidth ** 2;

      speed += (Number(up) * (speed < 0 ? 32 : 16) -
                Number(down) * (speed > 0 ? 30 : 10)) * dt;
      if (!up && !down) speed *= Math.exp(-1.15 * dt);
      if (offRoad) speed *= Math.exp(-2.1 * dt);
      if (keys.has('Space')) speed *= Math.exp(-7 * dt);
      speed = T.MathUtils.clamp(speed, -9, 31);

      const steer = Number(left) - Number(right);
      const grip = Math.min(Math.abs(speed) / 5, 1);
      yaw += steer * Math.sign(speed) * grip * (2.05 - Math.abs(speed) * 0.027) * dt;
      car.rotation.y = yaw;
      car.position.x += Math.sin(yaw) * speed * dt;
      car.position.z += Math.cos(yaw) * speed * dt;

      const gate = lapStart === null ? 0 : checkpoints[checkpoint];
      const crossing = crossGate(gate, oldX, oldZ, car.position.x, car.position.z);
      if (crossing !== null) {
        const at = now - dt * (1 - crossing);
        if (lapStart === null) {
          lapStart = at;
          status.textContent = 'Lap in progress · checkpoint 0/3';
        } else if (gate !== 0) {
          checkpoint++;
          status.textContent = `Lap in progress · checkpoint ${checkpoint}/3`;
        } else {
          const elapsed = at - lapStart;
          if (elapsed < best) {
            best = elapsed;
            bestEl.textContent = format(best);
            status.textContent = `New best: ${format(elapsed)}`;
            try { localStorage.setItem(bestKey, String(best)); } catch {}
          } else {
            status.textContent = `Last lap: ${format(elapsed)}`;
          }
          lapStart = at;
          checkpoint = 0;
        }
      }
      if (lapStart !== null) lapEl.textContent = format(now - lapStart);
      updateCamera(dt);
      renderer.render(scene, camera);
    });
  </script>
</body>
</html>
```

### Run and verify

From the folder containing `index.html`, run `python -m http.server 8000` (or `python3 -m http.server 8000`) and open `http://localhost:8000/`. I haven’t run the game here; these are the checks I’d perform:

1. **Startup and handling:** Confirm the car, road, and HUD render without console errors. Drive with both WASD and the arrow keys. Check that Space slows the car and grass reduces speed.
2. **Lap timing:** Drive forward over the checkered line. The timer should start, and the HUD should count three checkpoints in order. Cross the line again to record a best lap and start the next one.
3. **Invalid laps:** Cross the start line backward or turn around and recross it without visiting the checkpoints. Neither should record a lap.
4. **Reset and persistence:** Press R mid-lap. The car should return behind the line and the current timer should clear. Reload the page on the same URL and confirm the best lap remains.


=============== RESPONSE ambition-game-23 ===============

Save this as `index.html`. It gives you a solo time-trial racer with one closed track, keyboard steering, a live lap timer, and a personal best. The whole game lives in one file, with Three.js as its only dependency.

**Data shape.** The track is a closed centerline with a fixed width. The car stores distance along that line, lateral offset, and speed. The lap state stores elapsed driving time and the best completed time. The same centerline drives the road mesh and the car position.

| Design | Decision |
|---|---|
| Free movement with checkpoint gates | Rejected. It would need off-road recovery and rules for missed gates and shortcuts. |
| Track-relative steering | Chosen. You steer across the road and manage speed, while the car follows the loop. A lap ends only after traveling the full track length. |

**Throughput checkpoint**

1. **Blocking first steps.** Define the track coordinates and lap rollover before building the scene.
2. **Independent workstreams.** The HUD and scenery only read game state. They do not change timing or controls.
3. **Shared mutable state.** The game loop owns car and lap updates. Keyboard handlers record input.
4. **Smallest safe decomposition.** One HTML file. Scene construction, simulation, and display each have a distinct job. No repository or subagent tools were available here.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mesa Loop</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: #fff5de;
      background: #211c21;
      font: 1rem system-ui, sans-serif;
    }
    header, footer { padding: .8rem clamp(.75rem, 3vw, 2rem); }
    header { display: flex; flex-wrap: wrap; align-items: center; gap: .8rem 2rem; }
    h1 { margin: 0; font-size: clamp(1.2rem, 4vw, 1.8rem); }
    dl { margin: 0; display: flex; flex-wrap: wrap; gap: .5rem 1.5rem; }
    dt { color: #ffd28c; font-size: .8rem; }
    dd { margin: 0; font-variant-numeric: tabular-nums; }
    #view { position: relative; height: 74vh; min-height: 240px; }
    canvas { display: block; width: 100%; height: 100%; }
    #status { padding: 1rem; margin: 0; }
    footer { line-height: 1.5; }
    kbd { color: #ffd28c; font: inherit; font-weight: bold; }
  </style>
</head>
<body>
  <header>
    <h1>Mesa Loop</h1>
    <dl>
      <div><dt>Current lap</dt><dd id="lap">0:00.000</dd></div>
      <div><dt>Best lap</dt><dd id="best">No lap yet</dd></div>
    </dl>
  </header>
  <main id="view" aria-label="Mesa Loop race view">
    <p id="status" role="status">Loading the track…</p>
  </main>
  <footer>
    <kbd>↑</kbd> / <kbd>W</kbd> accelerate ·
    <kbd>↓</kbd> / <kbd>S</kbd> brake ·
    <kbd>← →</kbd> / <kbd>A D</kbd> steer ·
    <kbd>R</kbd> restart lap
  </footer>
  <noscript>This game needs JavaScript.</noscript>

  <script type="module">
    const view = document.querySelector('#view');
    const status = document.querySelector('#status');

    try {
      const THREE = await import(
        'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js'
      );
      run(THREE);
    } catch (error) {
      status.hidden = false;
      status.textContent =
        'Could not start the game. Check your connection and WebGL support, then reload.';
      console.error(error);
    }

    function run(T) {
      const scene = new T.Scene();
      scene.background = new T.Color(0xffc998);
      scene.fog = new T.FogExp2(0xffc998, 0.006);
      scene.add(new T.HemisphereLight(0xfff0d7, 0xb06c57, 2));
      const sun = new T.DirectionalLight(0xffe2b6, 2);
      sun.position.set(-35, 60, 20);
      scene.add(sun);

      const camera = new T.PerspectiveCamera(58, 1, 0.1, 500);
      const renderer = new T.WebGLRenderer({ antialias: true });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      view.append(renderer.domElement);

      const line = new T.CatmullRomCurve3(
        [[-30, 20], [0, 29], [35, 17], [42, -8],
         [22, -27], [-9, -22], [-38, -17], [-46, 4]]
          .map(([x, z]) => new T.Vector3(x, 0, z)),
        true
      );
      line.arcLengthDivisions = 1024;
      const length = line.getLength();
      const halfWidth = 5;
      const wrap = s => T.MathUtils.euclideanModulo(s, length);

      function pose(s) {
        const u = wrap(s) / length;
        const forward = line.getTangentAt(u);
        return {
          center: line.getPointAt(u),
          forward,
          right: new T.Vector3(-forward.z, 0, forward.x)
        };
      }

      function roadPoint(s, lateral, height) {
        const { center, right } = pose(s);
        return center.addScaledVector(right, lateral).setY(height);
      }

      function patch(s0, s1, left, right, height, vertices) {
        const a = roadPoint(s0, left, height);
        const b = roadPoint(s0, right, height);
        const c = roadPoint(s1, left, height);
        const d = roadPoint(s1, right, height);
        for (const p of [a, b, c, b, d, c]) vertices.push(p.x, p.y, p.z);
      }

      function surface(vertices, color) {
        const geometry = new T.BufferGeometry();
        geometry.setAttribute('position', new T.Float32BufferAttribute(vertices, 3));
        geometry.computeVertexNormals();
        scene.add(new T.Mesh(geometry, new T.MeshStandardMaterial({
          color, side: T.DoubleSide
        })));
      }

      function mesh(parent, geometry, color, x, y, z) {
        const object = new T.Mesh(geometry, new T.MeshStandardMaterial({
          color, flatShading: true
        }));
        object.position.set(x, y, z);
        parent.add(object);
        return object;
      }

      const ground = mesh(scene, new T.PlaneGeometry(450, 450), 0xc78153, 0, -0.1, 0);
      ground.rotation.x = -Math.PI / 2;

      const asphalt = [], cream = [], red = [], marks = [], dark = [];
      for (let i = 0; i < 240; i++) {
        const a = i * length / 240;
        const b = (i + 1) * length / 240;
        patch(a, b, -halfWidth, halfWidth, 0, asphalt);
        const curb = Math.floor(i / 2) % 2 ? cream : red;
        patch(a, b, -halfWidth, -halfWidth + .45, .025, curb);
        patch(a, b, halfWidth - .45, halfWidth, .025, curb);
        if (i % 8 < 3 && i > 2 && i < 237) {
          patch(a, b, -.06, .06, .02, marks);
        }
      }
      for (let row = 0; row < 2; row++) {
        for (let col = 0; col < 10; col++) {
          patch((row - 1) * .55, row * .55, col - 5, col - 4, .04,
            (row + col) % 2 ? dark : cream);
        }
      }
      surface(asphalt, 0x383943);
      surface(red, 0xd74337);
      surface(cream, 0xffedcc);
      surface(marks, 0xcfb58e);
      surface(dark, 0x14151b);

      const trackSamples = Array.from({ length: 120 }, (_, i) => line.getPointAt(i / 120));
      const rock = new T.DodecahedronGeometry(1, 0);
      for (let i = 0; i < 110; i++) {
        const x = Math.sin(i * 73.17) * (12 + i * .63);
        const z = Math.cos(i * 19.31) * (9 + i * .43);
        if (trackSamples.some(p => Math.hypot(x - p.x, z - p.z) < 11)) continue;
        const size = 1 + (i % 7) * .46;
        const stone = mesh(scene, rock, i % 2 ? 0xa7523a : 0xdf9a61, x, size * .35, z);
        stone.scale.set(size * 1.5, size, size * 1.2);
        stone.rotation.y = i;
      }

      const car = new T.Group();
      scene.add(car);
      mesh(car, new T.BoxGeometry(1.65, .48, 3), 0x09aaa6, 0, .52, 0);
      mesh(car, new T.BoxGeometry(1.22, .45, 1.35), 0x183749, 0, .94, -.2);
      mesh(car, new T.BoxGeometry(1.7, .12, .35), 0xffdb79, 0, .98, -1.27);
      const wheel = new T.CylinderGeometry(.34, .34, .27, 10);
      for (const x of [-.83, .83]) {
        for (const z of [-.94, .94]) {
          mesh(car, wheel, 0x191820, x, .34, z).rotation.z = Math.PI / 2;
        }
      }

      const lapDisplay = document.querySelector('#lap');
      const bestDisplay = document.querySelector('#best');
      const recordKey = 'mesa-loop-best-v1';
      let best = Infinity;
      try {
        const saved = Number(localStorage.getItem(recordKey));
        if (Number.isFinite(saved) && saved > 0) best = saved;
      } catch { /* Storage may be blocked. The session record still works. */ }

      const format = seconds => {
        const ms = Math.floor(seconds * 1000);
        return `${Math.floor(ms / 60000)}:${String(Math.floor(ms / 1000) % 60)
          .padStart(2, '0')}.${String(ms % 1000).padStart(3, '0')}`;
      };
      if (Number.isFinite(best)) bestDisplay.textContent = format(best);

      const keys = new Set();
      const controls = new Set([
        'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
        'KeyW', 'KeyA', 'KeyS', 'KeyD', 'KeyR'
      ]);
      const held = (a, b) => Number(keys.has(a) || keys.has(b));
      const restart = () => ({ distance: 0, offset: 0, speed: 0, elapsed: 0 });
      let drive = restart();
      let previous;

      window.addEventListener('keydown', event => {
        if (!controls.has(event.code) || event.ctrlKey || event.metaKey || event.altKey) return;
        event.preventDefault();
        if (event.code === 'KeyR' && !event.repeat) drive = restart();
        keys.add(event.code);
      });
      window.addEventListener('keyup', event => keys.delete(event.code));
      function clearInput() {
        keys.clear();
        previous = undefined;
      }
      window.addEventListener('blur', clearInput);
      document.addEventListener('visibilitychange', clearInput);

      function step(dt) {
        const throttle = held('ArrowUp', 'KeyW');
        const brake = held('ArrowDown', 'KeyS');
        const steer = held('ArrowRight', 'KeyD') - held('ArrowLeft', 'KeyA');
        const limit = 40 - 15 * T.MathUtils.smoothstep(Math.abs(drive.offset), 3, 4.15);
        drive.speed = T.MathUtils.clamp(
          drive.speed + (brake ? -34 : throttle ? 16 : -9) * dt, 0, limit
        );
        drive.offset = T.MathUtils.clamp(
          drive.offset + steer * Math.min(drive.speed * .32, 9) * dt, -4.15, 4.15
        );

        const travel = drive.speed * dt;
        const distance = drive.distance + travel;
        if (distance >= length) {
          const spill = dt * (distance - length) / travel;
          const completed = drive.elapsed + dt - spill;
          if (completed < best) {
            best = completed;
            bestDisplay.textContent = format(best);
            try { localStorage.setItem(recordKey, String(best)); } catch {}
          }
          drive.elapsed = spill;
          drive.distance = distance - length;
        } else {
          if (distance > 0 || drive.elapsed > 0) drive.elapsed += dt;
          drive.distance = distance;
        }
      }

      const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
      new ResizeObserver(() => {
        const width = Math.max(1, view.clientWidth);
        const height = Math.max(1, view.clientHeight);
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height, false);
      }).observe(view);

      function frame(now) {
        if (previous !== undefined && !document.hidden) {
          step(Math.min((now - previous) / 1000, .05));
        }
        previous = now;

        const { center, forward, right } = pose(drive.distance);
        car.position.copy(center).addScaledVector(right, drive.offset);
        car.rotation.y = Math.atan2(forward.x, forward.z);

        if (reducedMotion.matches) {
          camera.position.set(0, 32, 0);
          camera.up.set(0, 0, -1);
          camera.lookAt(0, 0, 0);
          if (!(camera instanceof T.OrthographicCamera)) {
            // Keep the whole loop visible without a moving camera.
            const half = Math.max(42, 57 / camera.aspect);
            camera.fov = T.MathUtils.radToDeg(2 * Math.atan(half / 32));
            camera.updateProjectionMatrix();
          }
        } else {
          camera.up.set(0, 1, 0);
          camera.fov = 58;
          camera.updateProjectionMatrix();
          camera.position.copy(center).addScaledVector(forward, -13);
          camera.position.y = 8;
          const target = center.clone().addScaledVector(forward, 8);
          target.y = .8;
          camera.lookAt(target);
        }

        lapDisplay.textContent = format(drive.elapsed);
        renderer.render(scene, camera);
        requestAnimationFrame(frame);
      }

      status.hidden = true;
      requestAnimationFrame(frame);
    }
  </script>
</body>
</html>
```

### Run and verify

Serve the folder with any static server. For example, run `python -m http.server 8000` and open `http://localhost:8000`. The browser needs internet access to load Three.js from the CDN and WebGL support to render the scene.

**Verification status:** Not run here. These are expected results inferred from the code, not observed browser results.

| Browser check | Expected result |
|---|---|
| Load with DevTools open. | The track and car appear, the console has no startup errors, the timer reads `0:00.000`, and a fresh browser profile shows `No lap yet`. |
| Hold accelerate, steer both ways, then brake. | The car advances, moves across the lane, slows near the curbs, and stops under braking. The timer keeps running after the car has moved. |
| Complete a lap, then complete a slower lap and a faster lap. | The checkerboard crossing rolls the current timer over once per lap. The slower lap leaves the record unchanged. The faster lap replaces it. |
| Press `R` halfway around, then reload on the same origin. | Restart returns the car to the line and clears the current timer without awarding a lap. Reload keeps the best if storage is available. |
| Hold a key while switching tabs, release it, and return. | The key is not stuck, and the timer does not jump by the time spent in the background. |
| Test at 320px and 200% zoom, then emulate reduced motion. | HUD text wraps without clipping. Reduced motion uses a fixed overhead view instead of a chase camera. |

**Timing choice:** Lap times use simulation time. The timer pauses in background tabs and caps each frame's contribution at 50 ms, so sustained low frame rates can produce shorter times than a wall clock would report.

**Principles applied:** *Model the domain* led to track-relative distance and a single lap rollover rule. *Prove it works* led to verification steps that drive the game in a real browser and check the displayed record across laps and reloads.

**Open decisions:** None required. This is a solo keyboard time trial, with no opponents or multiplayer.


=============== RESPONSE ambition-game-24 ===============

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sunset Circuit</title>
<style>
  body { margin: 0; overflow: hidden; background: #ffcb99; color: #fff; font: 16px system-ui, sans-serif; }
  canvas { display: block; }
  #hud { position: fixed; top: 16px; left: 16px; padding: 14px 18px;
         background: #182233; border-radius: 8px; pointer-events: none; }
  h1 { margin: 0 0 8px; font-size: 18px; }
  .time { font-variant-numeric: tabular-nums; }
  small { display: block; margin-top: 8px; color: #c9d8ea; }
</style>
</head>
<body>
<div id="hud">
  <h1>Sunset Circuit</h1>
  <div>Lap <span id="lap">1</span> · <span class="time" id="current">0:00.000</span></div>
  <div>Best · <span class="time" id="best">—</span></div>
  <small>↑ / W throttle · ↓ / S brake &amp; reverse<br>← → / A D steer · R restart</small>
</div>
<script type="module">
import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js";

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffcb99);
scene.fog = new THREE.Fog(0xffcb99, 75, 160);
const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 200);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
document.body.appendChild(renderer.domElement);

function resize() {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
}
addEventListener("resize", resize);
resize();

scene.add(new THREE.HemisphereLight(0xffecd6, 0x827d58, 2));
const sun = new THREE.DirectionalLight(0xffe0b5, 2.3);
sun.position.set(-20, 35, 15);
scene.add(sun);

function mesh(geometry, color, x, y, z, parent = scene) {
  const object = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({ color, flatShading: true }));
  object.position.set(x, y, z);
  parent.add(object);
  return object;
}
function box(w, h, d, color, x, y, z, parent = scene) {
  return mesh(new THREE.BoxGeometry(w, h, d), color, x, y, z, parent);
}
function ring(inner, outer, y, color) {
  mesh(new THREE.RingGeometry(inner, outer, 96), color, 0, y, 0).rotation.x = -Math.PI / 2;
}

const radius = 30, inner = 25, outer = 35, turn = 2 * Math.PI;
box(320, 0.2, 320, 0x78985c, 0, -0.12, 0);
ring(inner, outer, 0, 0x343a48);
ring(inner, inner + 0.25, 0.015, 0xffdf91);
ring(outer - 0.25, outer, 0.015, 0xffdf91);

for (let i = 1; i < 48; i++) {
  const a = i * turn / 48;
  box(0.13, 0.02, 1.1, 0xb9bfca, radius * Math.cos(a), 0.015, radius * Math.sin(a)).rotation.y = -a;
}
for (let i = 0; i < 20; i++) {
  for (let j = 0; j < 2; j++) {
    box(0.5, 0.02, 0.5, (i + j) % 2 ? 0xfafafa : 0x171c25,
        inner + (i + 0.5) * 0.5, 0.022, (j - 0.5) * 0.5);
  }
}
for (let i = 0; i < 28; i++) {
  const a = i * 2.4, r = i % 2 ? 12 + i % 8 : 39 + i % 11;
  const x = r * Math.cos(a), z = r * Math.sin(a);
  box(0.4, 1.4, 0.4, 0x725140, x, 0.7, z);
  mesh(new THREE.ConeGeometry(1.5, 3 + i % 3, 5), 0x315d48, x, 2.5, z);
}

const car = new THREE.Group();
scene.add(car);
box(1.5, 0.48, 2.65, 0xee5035, 0, 0.52, 0, car);
box(1.12, 0.48, 1.2, 0x263c55, 0, 0.95, -0.22, car);
for (const x of [-0.77, 0.77]) {
  for (const z of [-0.83, 0.83]) {
    mesh(new THREE.CylinderGeometry(0.31, 0.31, 0.28, 8), 0x171a21,
         x, 0.31, z, car).rotation.z = Math.PI / 2;
  }
  box(0.32, 0.15, 0.04, 0xffebac, x * 0.7, 0.56, 1.34, car);
  box(0.32, 0.15, 0.04, 0xff9e7c, x * 0.7, 0.56, -1.34, car);
}

const lapLabel = document.querySelector("#lap");
const currentLabel = document.querySelector("#current");
const bestLabel = document.querySelector("#best");
const keys = new Set();
const controls = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "KeyW", "KeyA", "KeyS", "KeyD", "KeyR"];
const pressed = (a, b) => keys.has(a) || keys.has(b);

let speed, heading, angle, progress, started, lap;
let best = Infinity;
function reset() {
  car.position.set(radius, 0, 0);
  speed = heading = angle = progress = 0;
  started = null;
  lap = 1;
  lapLabel.textContent = lap;
  camera.position.set(radius, 5, -8);
}
reset();

addEventListener("keydown", e => {
  if (!controls.includes(e.code)) return;
  e.preventDefault();
  keys.add(e.code);
  if (e.code === "KeyR" && !e.repeat) reset();
});
addEventListener("keyup", e => keys.delete(e.code));
addEventListener("blur", () => keys.clear());

function format(ms) {
  const t = Math.floor(ms);
  return `${Math.floor(t / 60000)}:${String(Math.floor(t / 1000) % 60).padStart(2, "0")}.${String(t % 1000).padStart(3, "0")}`;
}

const clamp = THREE.MathUtils.clamp;
const cameraGoal = new THREE.Vector3();
let previous = performance.now();

renderer.setAnimationLoop(now => {
  const dt = clamp((now - previous) / 1000, 0, 0.05);
  const throttle = Number(pressed("ArrowUp", "KeyW")) - Number(pressed("ArrowDown", "KeyS"));
  const steer = Number(pressed("ArrowLeft", "KeyA")) - Number(pressed("ArrowRight", "KeyD"));
  if (throttle && started === null) started = now;
  speed = throttle
    ? clamp(speed + throttle * (throttle < 0 ? 26 : 18) * dt, -8, 23)
    : speed * Math.exp(-2 * dt);
  heading -= steer * 1.55 * clamp(speed / 8, -1, 1) * dt;
  car.rotation.y = heading;

  const dx = Math.sin(heading), dz = Math.cos(heading);
  const p = car.position;
  p.x += dx * speed * dt;
  p.z += dz * speed * dt;
  const r = Math.hypot(p.x, p.z);
  const edge = clamp(r, inner + 1, outer - 1);
  if (r !== edge) {
    p.multiplyScalar(edge / r);
    speed *= Math.exp(-5 * dt);
  }

  // Signed angular travel: reversing undoes progress instead of counting laps.
  const nextAngle = Math.atan2(p.z, p.x);
  const delta = Math.atan2(Math.sin(nextAngle - angle), Math.cos(nextAngle - angle));
  angle = nextAngle;
  progress += delta;
  if (started !== null && progress >= turn) {
    const crossing = Math.max(started, now - (now - previous) * (progress - turn) / delta);
    best = Math.min(best, crossing - started);
    bestLabel.textContent = format(best);
    started = crossing;
    progress -= turn;
    lapLabel.textContent = ++lap;
  }
  currentLabel.textContent = format(started === null ? 0 : now - started);
  previous = now;

  cameraGoal.set(p.x - dx * 8, 5, p.z - dz * 8);
  camera.position.lerp(cameraGoal, 1 - Math.exp(-7 * dt));
  camera.lookAt(p.x + dx * 3, 0.7, p.z + dz * 3);
  renderer.render(scene, camera);
});
</script>
</body>
</html>
```

Save it as `index.html` and open it in a modern browser with WebGL and internet access. The only dependency is the pinned Three.js CDN import. Best lap is kept for the open page, including across **R** restarts; reloading clears it.

**How I’d verify it** (not run here):

1. Open the page and check that the track, car, and HUD render without console errors. Resize the window and confirm the view doesn’t stretch.
2. Try both key sets. Drive forward from the grid, steer left around the circuit, and check that braking leads into reverse and the track edges keep the car on the road. Switch tabs while holding a key and check that it isn’t stuck on return.
3. Complete two laps. The timer should start at first throttle, then reset at each valid finish crossing. The best display should keep the faster lap. Reverse across the finish line and drive forward over it again without circling the track; the lap count should stay unchanged. Press **R** and confirm the car returns to the grid, the lap timer resets, and the best lap remains.


=============== RESPONSE ambition-game-25 ===============

Save this as `index.html`. It gives players one closed circuit, a low-poly car, keyboard steering, and a best lap that survives reloads when browser storage is available. The maintainer gets one file with no build step or art assets. I reviewed the code statically; I did not run it in a browser.

**Data shape.** The track is an ellipse sampled into a road mesh. The car has signed distance along the track, lateral offset, and speed. The lap timer has a start timestamp, a next finish distance, and an optional best time. Rendering reads that state without changing it.

| Design | Tradeoff |
|---|---|
| Track-relative driving, chosen | Left and right move the car across the road. Signed progress makes lap counting independent of visual finish-line detection. |
| Free steering | Gives players more control over racing lines, but needs off-track recovery and ordered checkpoints to reject shortcuts. |

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Juniper Sprint</title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0; background: #101e21; color: #f7f7ef;
    font: 16px system-ui, sans-serif;
  }
  #view { position: fixed; inset: 0; }
  canvas { display: block; width: 100%; height: 100%; }
  .hud {
    position: relative; margin: 12px; padding: 12px 16px;
    width: fit-content; max-width: calc(100% - 24px);
    background: #101e21; border: 1px solid #577176; border-radius: 12px;
  }
  h1 { margin: 0; font-size: 1.15rem; }
  dl { display: flex; flex-wrap: wrap; gap: 8px 20px; margin: 10px 0; }
  dt { color: #c3d5d3; font-size: .8rem; }
  dd { margin: 0; font: bold 1rem ui-monospace, monospace; }
  p { margin: 6px 0 0; font-size: .8rem; }
  #status { color: #ffde93; }
</style>
</head>
<body>
<div id="view" aria-hidden="true"></div>
<main class="hud">
  <h1>Juniper Sprint</h1>
  <dl>
    <div><dt>Current lap</dt><dd id="lap">0:00.000</dd></div>
    <div><dt>Best lap</dt><dd id="best">None yet</dd></div>
    <div><dt>Speed</dt><dd id="speed">0 km/h</dd></div>
  </dl>
  <p>W / ↑ accelerate · S / ↓ brake and reverse</p>
  <p>A / ← and D / → steer · R restart</p>
  <p id="status" role="status">Loading Three.js…</p>
</main>

<script type="module">
const el = id => document.getElementById(id);

try {
  const THREE = await import(
    'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js'
  );
  start(THREE);
} catch (error) {
  el('status').textContent =
    'Could not start. Check your connection and WebGL support, then reload.';
  console.error(error);
}

function start(T) {
  const scene = new T.Scene();
  scene.background = new T.Color(0xaccad2);
  const renderer = new T.WebGLRenderer({ antialias: true });
  el('view').append(renderer.domElement);
  const chase = new T.PerspectiveCamera(62, 1, 0.2, 300);
  const overhead = new T.OrthographicCamera(-64, 64, 64, -64, 0.2, 300);
  overhead.up.set(0, 0, -1);
  overhead.position.set(0, 110, 0);
  overhead.lookAt(0, 0, 0);
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');

  function resize() {
    const w = innerWidth, h = Math.max(1, innerHeight), aspect = w / h;
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
    renderer.setSize(w, h);
    chase.aspect = aspect;
    chase.updateProjectionMatrix();
    const half = Math.max(45, 62 / aspect);
    Object.assign(overhead, {
      left: -half * aspect, right: half * aspect, top: half, bottom: -half
    });
    overhead.updateProjectionMatrix();
  }
  addEventListener('resize', resize);
  resize();

  scene.add(new T.HemisphereLight(0xfff8df, 0x54604b, 2.0));
  const sun = new T.DirectionalLight(0xffe6c5, 2);
  sun.position.set(-25, 40, 15);
  scene.add(sun);

  const mat = color => new T.MeshStandardMaterial({ color, flatShading: true });
  function mesh(geometry, material, parent, x = 0, y = 0, z = 0) {
    const object = new T.Mesh(geometry, material);
    object.position.set(x, y, z);
    parent.add(object);
    return object;
  }
  function box(w, h, d, material, parent, x, y, z) {
    return mesh(new T.BoxGeometry(w, h, d), material, parent, x, y, z);
  }
  box(440, 1, 440, mat(0x688b56), scene, 0, -.51, 0);

  const a = 43, b = 29, width = 5, count = 256;
  const turn = 2 * Math.PI;
  const lengths = [0];
  function point(angle, offset = 0) {
    const c = Math.cos(angle), s = Math.sin(angle);
    const norm = Math.hypot(c / a, s / b);
    return new T.Vector3(a * c + offset * c / a / norm, 0,
                         b * s + offset * s / b / norm);
  }
  let previous = point(0);
  for (let i = 1; i <= count; i++) {
    const next = point(i * turn / count);
    lengths.push(lengths[i - 1] + previous.distanceTo(next));
    previous = next;
  }
  const length = lengths[count];

  function angleAt(distance) {
    const d = ((distance % length) + length) % length;
    let lo = 0, hi = count;
    while (hi - lo > 1) {
      const mid = (lo + hi) >> 1;
      if (lengths[mid] <= d) lo = mid;
      else hi = mid;
    }
    return (lo + (d - lengths[lo]) / (lengths[hi] - lengths[lo])) * turn / count;
  }

  function strip(inner, outer, y, color) {
    const vertices = [], indices = [];
    for (let i = 0; i <= count; i++) {
      for (const offset of [inner, outer]) {
        const p = point(i * turn / count, offset);
        vertices.push(p.x, y, p.z);
      }
      if (i < count) {
        const j = i * 2;
        indices.push(j, j + 2, j + 1, j + 1, j + 2, j + 3);
      }
    }
    const geometry = new T.BufferGeometry();
    geometry.setAttribute('position', new T.Float32BufferAttribute(vertices, 3));
    geometry.setIndex(indices);
    geometry.computeVertexNormals();
    mesh(geometry, mat(color), scene);
  }
  strip(-width, width, .02, 0x343e45);
  strip(-width, -width + .23, .03, 0xffdf9a);
  strip(width - .23, width, .03, 0xffdf9a);

  const white = mat(0xf4f1df), black = mat(0x242a2e);
  for (let i = 0; i < 10; i++) {
    for (let j = 0; j < 2; j++) {
      box(1, .02, .5, (i + j) % 2 ? black : white,
          scene, a - width + i + .5, .045, (j - .5) * .5);
    }
  }

  const leaves = mat(0x265c48), trunks = mat(0x624832);
  const crown = new T.ConeGeometry(1.7, 4.6, 5);
  const trunk = new T.CylinderGeometry(.23, .3, 1.8, 5);
  for (let i = 0; i < 56; i++) {
    const p = point(i * turn / 56, (i % 2 ? -1 : 1) * (9 + i % 7));
    mesh(trunk, trunks, scene, p.x, .9, p.z);
    const tree = mesh(crown, leaves, scene, p.x, 3, p.z);
    tree.rotation.y = i * 2.4;
    tree.scale.setScalar(.75 + (i % 5) * .13);
  }

  const car = new T.Group();
  scene.add(car);
  const paint = mat(0xf36c43);
  box(1.75, .53, 3.05, paint, car, 0, .56, 0);
  box(1.32, .52, 1.38, mat(0x244653), car, 0, 1.05, -.22);
  box(1.7, .12, .35, paint, car, 0, 1.03, -1.31);
  const tire = new T.CylinderGeometry(.36, .36, .3, 10);
  for (const x of [-.89, .89]) {
    for (const z of [-.98, .98]) {
      mesh(tire, black, car, x, .36, z).rotation.z = Math.PI / 2;
    }
  }

  const recordKey = 'juniper-sprint-best-ms-v1';
  let best = null;
  try {
    const saved = Number(localStorage.getItem(recordKey));
    if (Number.isFinite(saved) && saved > 0) best = saved;
  } catch {}

  const format = ms => {
    const n = Math.max(0, Math.floor(ms));
    return `${Math.floor(n / 60000)}:${String(Math.floor(n / 1000) % 60).padStart(2, '0')}.${String(n % 1000).padStart(3, '0')}`;
  };

  const keys = new Set();
  const bindings = [
    'KeyW', 'ArrowUp', 'KeyS', 'ArrowDown',
    'KeyA', 'ArrowLeft', 'KeyD', 'ArrowRight', 'KeyR'
  ];
  const held = (a, b) => keys.has(a) || keys.has(b);
  let run;
  function reset() {
    run = { distance: 0, offset: 0, speed: 0, start: null, finish: length };
    el('status').textContent = 'Accelerate to start the timer.';
  }

  addEventListener('keydown', event => {
    if (!bindings.includes(event.code) || event.altKey ||
        event.ctrlKey || event.metaKey) return;
    event.preventDefault();
    if (event.code === 'KeyR' && !event.repeat) reset();
    keys.add(event.code);
  });
  addEventListener('keyup', event => keys.delete(event.code));
  addEventListener('blur', () => keys.clear());
  document.addEventListener('visibilitychange', () => keys.clear());

  function update(dt, now) {
    const throttle = held('KeyW', 'ArrowUp');
    const brake = held('KeyS', 'ArrowDown');
    if (run.start === null) {
      if (!throttle || brake) return;
      run.start = now - dt * 1000;
      el('status').textContent = 'Lap in progress';
    }

    const steer = Number(held('KeyD', 'ArrowRight')) -
                  Number(held('KeyA', 'ArrowLeft'));
    run.speed += (brake ? -24 : throttle ? 15 : 0) * dt;
    run.speed *= Math.exp(-(brake || throttle ? .24 : 1.45) * dt);
    run.speed = T.MathUtils.clamp(run.speed, -9, 32);
    run.offset = T.MathUtils.clamp(
      run.offset + steer * Math.min(7, Math.abs(run.speed) * .65) *
                   Math.sign(run.speed) * dt, -width - 2, width + 2
    );
    if (Math.abs(run.offset) > width - .6) {
      run.speed *= Math.exp(-2.8 * dt);
    }

    const before = run.distance;
    run.distance += run.speed * dt;
    if (before < run.finish && run.distance >= run.finish) {
      const fraction = (run.finish - before) / (run.distance - before);
      const crossed = now - (1 - fraction) * dt * 1000;
      const lap = crossed - run.start;
      const record = best === null || lap < best;
      if (record) {
        best = lap;
        try { localStorage.setItem(recordKey, String(best)); } catch {}
      }
      el('status').textContent =
        `${record ? 'New best' : 'Last lap'} ${format(lap)}`;
      run.start = crossed;
      run.finish += length;
    }
  }

  reset();
  let last = performance.now();
  renderer.setAnimationLoop(now => {
    const dt = Math.min(.05, Math.max(0, (now - last) / 1000));
    last = now;
    update(dt, now);

    const angle = angleAt(run.distance);
    const p = point(angle, run.offset);
    const forward = new T.Vector3(-a * Math.sin(angle), 0, b * Math.cos(angle))
      .normalize();
    car.position.copy(p);
    car.rotation.y = Math.atan2(forward.x, forward.z);
    chase.position.copy(p).addScaledVector(forward, -10);
    chase.position.y = 6;
    const target = p.clone().addScaledVector(forward, 7);
    target.y = .8;
    chase.lookAt(target);
    renderer.render(scene, reduced.matches ? overhead : chase);

    el('lap').textContent = format(run.start === null ? 0 : now - run.start);
    el('best').textContent = best === null ? 'None yet' : format(best);
    el('speed').textContent = `${Math.round(Math.abs(run.speed) * 3.6)} km/h`;
  });
}
</script>
</body>
</html>
```

### Run and verify

Serve the folder with `python3 -m http.server 8000`, then open `http://localhost:8000`. Use a desktop browser with WebGL and internet access for the pinned Three.js import.

These are planned browser checks, not results:

1. **Load and drive.** Confirm the road and car render without console errors. Try both key sets. Drive onto the grass and confirm the car slows. Switch windows while accelerating and confirm the throttle clears.
2. **Complete a lap.** Hold accelerate and stay near the center. Confirm the timer starts on acceleration, the first circuit sets a best, and the current timer rolls into the next lap.
3. **Reject a false lap.** Drive a short distance, reverse over the line, and cross it forward again. Confirm neither crossing sets a best.
4. **Keep the record.** Complete a slower second lap, press `R`, then reload. Confirm the slower lap does not replace the best, restart clears the current run, and reload restores the best.
5. **Check the display.** Resize to 320 px and test at 200% zoom. Check that the HUD wraps. Enable reduced motion and confirm the camera switches to a fixed overhead view. Block the CDN and reload to check the startup error.

**Throughput checkpoint.** Blocking first step was choosing the track and lap model. Independent workstreams were n/a because the deliverable is one coupled file. The simulation owns mutable race state and renders after each update. One implementation was the smallest split. Agent delegation, browser verification, commits, and a PR were unavailable in this chat.

**Principles used.** *Model the domain* led to signed progress and a next-finish threshold instead of a finish-line flag. *Prove it works* led to browser checks that exercise driving, lap counting, and storage on the actual page.

The open decision is driving style. This version uses lane steering and a reduced-motion overhead view. Free steering is the next change if you want cornering skill to determine lap times.


=============== RESPONSE ambition-game-26 ===============

Save this as `index.html`. It’s a complete single-file racer: one closed track, a chase camera, keyboard controls, and a best lap saved in your browser. Three.js loads from a CDN, so the page needs an internet connection.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pine Loop Racer</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; overflow: hidden; background: #a9d9ef; color: white;
           font: 16px system-ui, sans-serif; }
    canvas { display: block; }
    #hud { position: fixed; top: 16px; left: 16px; padding: 14px 18px;
           background: #101a26e8; border-radius: 12px; min-width: 230px;
           pointer-events: none; font-variant-numeric: tabular-nums; }
    h1 { margin: 0 0 8px; font-size: 19px; }
    .row { display: flex; justify-content: space-between; gap: 20px; }
    #status { color: #ffe08a; margin: 8px 0 4px; min-height: 1.4em; }
    small { color: #c5d7e4; }
    #error { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
             padding: 16px; background: #101a26; border-radius: 8px; }
  </style>
</head>
<body>
  <section id="hud" aria-label="Race information">
    <h1>Pine Loop Racer</h1>
    <div class="row"><span>Current lap</span><strong id="current">—</strong></div>
    <div class="row"><span>Best lap</span><strong id="best">—</strong></div>
    <div class="row"><span>Laps finished</span><strong id="count">0</strong></div>
    <div id="status"></div>
    <small>WASD / arrows · R to restart</small>
  </section>
  <div id="error" role="alert" hidden></div>

  <script type="module">
    async function main() {
      const THREE = await import(
        "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js"
      );

      const $ = id => document.getElementById(id);
      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0xa9d9ef);
      scene.fog = new THREE.Fog(0xa9d9ef, 115, 240);
      const camera = new THREE.PerspectiveCamera(59, innerWidth / innerHeight, 0.1, 300);
      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
      renderer.setSize(innerWidth, innerHeight);
      document.body.appendChild(renderer.domElement);

      scene.add(new THREE.HemisphereLight(0xf1f8ff, 0x64734c, 2.3));
      const sun = new THREE.DirectionalLight(0xffedcf, 2);
      sun.position.set(-30, 60, 25);
      scene.add(sun);

      const material = color => new THREE.MeshStandardMaterial({
        color, flatShading: true
      });
      function mesh(geometry, mat, parent, x = 0, y = 0, z = 0) {
        const object = new THREE.Mesh(geometry, mat);
        object.position.set(x, y, z);
        parent.add(object);
        return object;
      }

      const ground = mesh(new THREE.PlaneGeometry(600, 600), material(0x668c48), scene);
      ground.rotation.x = -Math.PI / 2;

      const track = new THREE.CatmullRomCurve3([
        [-38, -22], [-10, -34], [24, -31], [48, -13],
        [43, 15], [14, 33], [-17, 25], [-47, 13]
      ].map(([x, z]) => new THREE.Vector3(x, 0, z)), true);
      // Arc-length sampling keeps checkpoints and curb segments evenly spaced.
      track.arcLengthDivisions = 1200;
      const N = 320, HALF = 5.8;
      const points = Array.from({ length: N }, (_, i) => track.getPointAt(i / N));
      const normals = points.map((p, i) => {
        const a = points[(i + N - 1) % N], b = points[(i + 1) % N];
        return new THREE.Vector3(-(b.z - a.z), 0, b.x - a.x).normalize();
      });

      function ribbon(lo, hi, y, colors, segmentColor) {
        const positions = [], indices = [];
        const geometry = new THREE.BufferGeometry();
        for (let i = 0; i < N; i++) {
          const p = points[i], n = normals[i];
          for (const offset of [lo, hi])
            positions.push(p.x + n.x * offset, y, p.z + n.z * offset);
        }
        for (let i = 0; i < N; i++) {
          const a = 2 * i, b = 2 * ((i + 1) % N);
          const color = segmentColor(i);
          if (color < 0) continue;
          geometry.addGroup(indices.length, 6, color);
          indices.push(a, a + 1, b, a + 1, b + 1, b);
        }
        geometry.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
        geometry.setIndex(indices);
        geometry.computeVertexNormals();
        mesh(geometry, colors.map(material), scene);
      }

      // Use one material for the asphalt to avoid a draw call per segment.
      function surface(lo, hi, y, color) {
        const positions = [], indices = [];
        for (let i = 0; i < N; i++) {
          const p = points[i], n = normals[i];
          positions.push(p.x + n.x * lo, y, p.z + n.z * lo,
                         p.x + n.x * hi, y, p.z + n.z * hi);
          const a = 2 * i, b = 2 * ((i + 1) % N);
          indices.push(a, a + 1, b, a + 1, b + 1, b);
        }
        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
        geometry.setIndex(indices);
        geometry.computeVertexNormals();
        mesh(geometry, material(color), scene);
      }

      surface(-HALF, HALF, 0.025, 0x363b46);
      // Each curb color gets its own geometry, for two draw calls per curb.
      for (const side of [-1, 1]) {
        const lo = side * HALF - 0.33, hi = side * HALF + 0.33;
        [0xe75d4e, 0xffeee2].forEach((color, parity) => {
          // Group-free mesh: collect only segments that use this color.
          const positions = [];
          const vertex = (i, offset) => {
            const p = points[i], n = normals[i];
            positions.push(p.x + n.x * offset, 0.042, p.z + n.z * offset);
          };
          for (let i = 0; i < N; i++) {
            if (Math.floor(i / 4) % 2 !== parity) continue;
            const j = (i + 1) % N;
            vertex(i, lo); vertex(i, hi); vertex(j, lo);
            vertex(i, hi); vertex(j, hi); vertex(j, lo);
          }
          const geometry = new THREE.BufferGeometry();
          geometry.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
          geometry.computeVertexNormals();
          mesh(geometry, material(color), scene);
        });
      }

      const start = points[0], tangent = track.getTangentAt(0);
      const startYaw = Math.atan2(tangent.x, tangent.z);
      const grid = new THREE.Group();
      grid.position.copy(start);
      grid.rotation.y = startYaw;
      scene.add(grid);
      const tiles = [material(0xf7f4dc), material(0x1b2030)];
      const tileWidth = 2 * HALF / 12;
      const tile = new THREE.BoxGeometry(tileWidth, 0.02, 0.52);
      for (let row = 0; row < 2; row++)
        for (let col = 0; col < 12; col++)
          mesh(tile, tiles[(row + col) % 2], grid,
               -HALF + (col + 0.5) * tileWidth, 0.055, (row - 0.5) * 0.52);

      function nearest(x, z) {
        let index = 0, distance2 = Infinity;
        for (let i = 0; i < N; i++) {
          const p = points[i], dx = x - p.x, dz = z - p.z;
          const d2 = dx * dx + dz * dz;
          if (d2 < distance2) { index = i; distance2 = d2; }
        }
        return { index, distance2 };
      }

      const trunk = new THREE.CylinderGeometry(0.16, 0.24, 1.4, 5);
      const crown = new THREE.ConeGeometry(1.2, 3.1, 6);
      const bark = material(0x6f4935);
      const greens = [material(0x245f47), material(0x31794e), material(0x438655)];
      let seed = 827;
      const random = () => (seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0)
                           / 4294967296;
      for (let i = 0; i < 170; i++) {
        const x = (random() - 0.5) * 180, z = (random() - 0.5) * 150;
        if (nearest(x, z).distance2 < (HALF + 12) ** 2) continue;
        const s = 0.65 + random() * 0.95;
        mesh(trunk, bark, scene, x, 0.7 * s, z).scale.setScalar(s);
        const top = mesh(crown, greens[i % 3], scene, x, 2.35 * s, z);
        top.scale.setScalar(s);
        top.rotation.y = random() * Math.PI;
      }

      const car = new THREE.Group();
      scene.add(car);
      mesh(new THREE.BoxGeometry(1.65, 0.53, 3.1), material(0xff6439), car, 0, 0.58);
      mesh(new THREE.BoxGeometry(1.24, 0.46, 1.35), material(0x223b58), car, 0, 1.04, -0.28);
      const rubber = material(0x161a20), headlight = material(0xffedb3);
      const tire = new THREE.CylinderGeometry(0.33, 0.33, 0.28, 10);
      const light = new THREE.BoxGeometry(0.35, 0.15, 0.08);
      for (const x of [-0.83, 0.83]) {
        for (const z of [-0.97, 0.97])
          mesh(tire, rubber, car, x, 0.34, z).rotation.z = Math.PI / 2;
        mesh(light, headlight, car, x * 0.73, 0.61, 1.57);
      }

      const keys = new Set();
      const controls = new Set([
        "KeyW", "KeyA", "KeyS", "KeyD", "KeyR",
        "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"
      ]);
      const storageKey = "pine-loop-best-v1";
      let best = Infinity;
      try {
        const stored = Number(localStorage.getItem(storageKey));
        if (stored > 0 && Number.isFinite(stored)) best = stored;
      } catch {} // The game still works if browser storage is unavailable.

      let yaw, speed, previousIndex, laps, lapStart, checkpoint, courseTravel;
      let notice, noticeUntil;
      const look = new THREE.Vector3(), desired = new THREE.Vector3();
      const pressed = (a, b) => keys.has(a) || keys.has(b);
      const format = ms => {
        const t = Math.floor(ms);
        return `${Math.floor(t / 60000)}:${String(Math.floor(t / 1000) % 60)
          .padStart(2, "0")}.${String(t % 1000).padStart(3, "0")}`;
      };

      function follow(dt, snap = false) {
        const x = Math.sin(yaw), z = Math.cos(yaw);
        desired.set(car.position.x - 8.5 * x, 5.4, car.position.z - 8.5 * z);
        camera.position.lerp(desired, snap ? 1 : 1 - Math.exp(-8 * dt));
        look.set(car.position.x + x * 3.5, 0.75, car.position.z + z * 3.5);
        camera.lookAt(look);
      }

      function reset() {
        yaw = startYaw;
        // Spawn just before the stripe so the first forward crossing starts timing.
        car.position.copy(track.getPointAt(1 - 5 / N));
        car.rotation.y = yaw;
        previousIndex = nearest(car.position.x, car.position.z).index;
        speed = laps = checkpoint = courseTravel = noticeUntil = 0;
        lapStart = null;
        follow(0, true);
      }

      addEventListener("keydown", event => {
        if (!controls.has(event.code)) return;
        event.preventDefault();
        keys.add(event.code);
        if (event.code === "KeyR" && !event.repeat) reset();
      });
      addEventListener("keyup", event => keys.delete(event.code));
      addEventListener("blur", () => keys.clear());
      document.addEventListener("visibilitychange", () => keys.clear());
      addEventListener("resize", () => {
        camera.aspect = innerWidth / innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(innerWidth, innerHeight);
      });

      const checkpoints = [N / 4, N / 2, 3 * N / 4];
      function updateLap(sample, now, onRoad) {
        const index = sample.index;
        const delta = (index - previousIndex + N + N / 2) % N - N / 2;
        if (lapStart !== null) courseTravel += delta;

        if (onRoad && delta > 0 && delta <= 8) {
          const crossed = gate => {
            const distance = (gate - previousIndex + N) % N;
            return distance > 0 && distance <= delta;
          };
          if (lapStart !== null && checkpoint < checkpoints.length &&
              crossed(checkpoints[checkpoint])) checkpoint++;

          if (crossed(0)) {
            if (lapStart === null) {
              lapStart = now;
              courseTravel = index;
            } else if (checkpoint === checkpoints.length && courseTravel >= N) {
              const elapsed = now - lapStart;
              laps++;
              const record = elapsed < best;
              if (record) {
                best = elapsed;
                try { localStorage.setItem(storageKey, String(best)); } catch {}
              }
              notice = `${record ? "New best" : "Lap complete"}: ${format(elapsed)}`;
              noticeUntil = now + 2600;
              lapStart = now;
              checkpoint = 0;
              courseTravel = index;
            }
          }
        }
        previousIndex = index;
      }

      reset();
      let last = performance.now();
      let sample = nearest(car.position.x, car.position.z);

      function frame(now) {
        const dt = Math.min(0.05, Math.max(0, (now - last) / 1000));
        last = now;
        sample = nearest(car.position.x, car.position.z);
        const onRoad = sample.distance2 <= HALF ** 2;
        const throttle = Number(pressed("KeyW", "ArrowUp"))
                       - Number(pressed("KeyS", "ArrowDown"));
        const steer = Number(pressed("KeyA", "ArrowLeft"))
                    - Number(pressed("KeyD", "ArrowRight"));

        speed += throttle * (throttle * speed < 0 ? 36 : 19) * dt;
        speed *= Math.exp(-(onRoad ? (throttle ? 0.42 : 1.8) : 3.4) * dt);
        speed = THREE.MathUtils.clamp(speed, -8, onRoad ? 29 : 8);
        yaw += steer * 1.85 * Math.min(Math.abs(speed) / 5, 1) * Math.sign(speed) * dt;
        car.position.x += Math.sin(yaw) * speed * dt;
        car.position.z += Math.cos(yaw) * speed * dt;
        car.rotation.y = yaw;

        sample = nearest(car.position.x, car.position.z);
        updateLap(sample, now, sample.distance2 <= HALF ** 2);
        follow(dt);

        $("current").textContent = lapStart === null ? "—" : format(now - lapStart);
        $("best").textContent = Number.isFinite(best) ? format(best) : "—";
        $("count").textContent = laps;
        $("status").textContent = now < noticeUntil ? notice :
          lapStart === null ? "Cross the stripe to start" :
          sample.distance2 > HALF ** 2 ? "Grass slows you down" :
          `Checkpoints: ${checkpoint} / ${checkpoints.length}`;

        renderer.render(scene, camera);
        requestAnimationFrame(frame);
      }
      requestAnimationFrame(frame);
    }

    main().catch(error => {
      console.error(error);
      const box = document.getElementById("error");
      box.hidden = false;
      box.textContent = "Could not start the game. Check your internet connection, WebGL support, and the browser console.";
    });
  </script>
</body>
</html>
```

### How I’d verify it

I haven’t run it here. Open `index.html` in a modern browser. If opening the file directly blocks the module import, run `python -m http.server 8000` from its folder and visit `http://localhost:8000`.

1. **Rendering and controls:** Confirm the car starts just before the checkered stripe. Test both key layouts, braking and reversing, and verify that driving onto the grass slows the car.
2. **Lap timing:** Cross the stripe forward. The timer should start without counting a completed lap. Follow the road through all three checkpoints and cross again: the lap count should increment, the best lap should appear, and the current timer should restart.
3. **False finishes:** Reverse across the stripe and drive forward over it repeatedly. That should not award a lap. Cutting across the infield without passing the checkpoints on the road should not award one either.
4. **Persistence and reset:** Finish a slower second lap and confirm the best doesn’t change. Press `R` to reset the car, timer, and lap count without clearing the best. Reload at the same URL and confirm the best remains.
5. **Browser behavior:** Resize the window and switch away while holding a driving key. The view should resize without stretching, and the car should not keep accelerating from a stuck key when you return.


=============== RESPONSE ambition-game-27 ===============

Save this as `index.html` to play **Mesa Loop**, a low-poly time trial with one closed track. The game uses a single HTML file and loads a pinned version of Three.js from a CDN. I couldn't run it here, so the browser checks below are a verification plan, not test results.

**Data shape.** The track is an annulus with an inner and outer radius. The car has an X/Z position, heading, and signed speed. The lap state holds elapsed time, net angular progress, and the best completed lap. The simulation updates that state; the renderer and HUD read it.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Mesa Loop</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: #191e25;
      color: #fff5df;
      font: 1rem system-ui, sans-serif;
    }
    #view { position: fixed; inset: 0; }
    canvas { display: block; }
    .hud, footer {
      position: fixed;
      left: 12px;
      max-width: calc(100% - 24px);
      background: #191e25;
      border: 1px solid #68605a;
      border-radius: 12px;
      padding: 10px 14px;
      pointer-events: none;
    }
    .hud { top: 12px; }
    footer { bottom: 12px; font-size: .82rem; }
    h1 { margin: 0 0 6px; font-size: 1.12rem; letter-spacing: .12em; }
    dl { display: flex; flex-wrap: wrap; gap: 6px 20px; margin: 0; }
    dt { font-size: .75rem; color: #e7b77b; }
    dd { margin: 0; font-variant-numeric: tabular-nums; font-weight: 700; }
    #status { margin: 6px 0 0; font-size: .82rem; }
  </style>
</head>
<body>
  <div id="view" aria-hidden="true"></div>
  <header class="hud">
    <h1>MESA LOOP</h1>
    <dl>
      <div><dt>Current lap</dt><dd id="current">0:00.000</dd></div>
      <div><dt>Best lap</dt><dd id="best">---</dd></div>
    </dl>
    <p id="status" role="status">Loading Three.js…</p>
  </header>
  <footer>WASD / arrows to drive · S / ↓ brakes and reverses · R restarts</footer>

  <script type="module">
    const status = document.querySelector('#status');
    try {
      const T = await import('https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js');
      start(T);
    } catch (error) {
      status.textContent = 'Could not start. Check your connection and WebGL support, then reload.';
      console.error(error);
    }

    function start(T) {
      const current = document.querySelector('#current');
      const best = document.querySelector('#best');
      const TAU = Math.PI * 2;
      const track = { inner: 32, outer: 46, center: 39 };
      const clamp = T.MathUtils.clamp;
      const storageKey = 'mesa-loop.best.v1';
      const scene = new T.Scene();
      scene.background = new T.Color(0xeab48a);
      scene.fog = new T.Fog(0xeab48a, 95, 230);

      const renderer = new T.WebGLRenderer({ antialias: true });
      renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
      document.querySelector('#view').append(renderer.domElement);
      const camera = new T.PerspectiveCamera(57, 1, 0.1, 300);
      const overview = new T.OrthographicCamera();
      overview.position.set(0, 115, 0);
      overview.up.set(0, 0, -1);
      overview.lookAt(0, 0, 0);
      overview.near = 0.1;
      overview.far = 200;
      const reduced = matchMedia('(prefers-reduced-motion: reduce)');

      scene.add(new T.HemisphereLight(0xffefdb, 0x806759, 2));
      const sun = new T.DirectionalLight(0xffeed2, 2);
      sun.position.set(-35, 60, 25);
      scene.add(sun);

      function mesh(geometry, color, x, y, z, parent = scene) {
        const material = new T.MeshStandardMaterial({ color, flatShading: true });
        const object = new T.Mesh(geometry, material);
        object.position.set(x, y, z);
        parent.add(object);
        return object;
      }

      function box(w, h, d, color, x, y, z, parent) {
        return mesh(new T.BoxGeometry(w, h, d), color, x, y, z, parent);
      }

      function ring(inner, outer, y, color) {
        const road = mesh(new T.RingGeometry(inner, outer, 96), color, 0, y, 0);
        road.rotation.x = -Math.PI / 2;
      }

      box(500, 1, 500, 0xbe7853, 0, -0.55, 0);
      ring(31.5, 46.5, 0, 0xffd6a0);
      ring(track.inner, track.outer, 0.015, 0x343944);
      for (let i = 0; i < 48; i++) {
        const a = i * TAU / 48;
        box(0.16, 0.025, 1.65, 0xefca79,
          track.center * Math.cos(a), 0.035, track.center * Math.sin(a)).rotation.y = -a;
      }

      for (let row = 0; row < 2; row++) {
        for (let col = 0; col < 14; col++) {
          box(1, 0.024, 0.68, (row + col) % 2 ? 0x222630 : 0xfff5df,
            track.inner + col + 0.5, 0.06, (row - 0.5) * 0.68);
        }
      }

      for (let i = 0; i < 34; i++) {
        const a = i * 2.399963;
        const r = i < 10 ? 8 + (i * 7 % 19) : 53 + (i * 11 % 37);
        const h = 2 + (i * 3 % 11);
        const rock = mesh(new T.CylinderGeometry(1.1, 2.4, h, 5),
          i % 2 ? 0xa3513e : 0xd9905c, r * Math.cos(a), h / 2, r * Math.sin(a));
        rock.rotation.y = a;
      }

      const model = new T.Group();
      scene.add(model);
      box(2.15, 0.58, 3.75, 0x23b8ab, 0, 0.58, 0, model);
      box(1.55, 0.55, 1.6, 0x143e50, 0, 1.1, -0.25, model);
      box(1.7, 0.13, 1.05, 0x69ebd7, 0, 1.43, -0.35, model);
      for (const x of [-1.05, 1.05]) {
        for (const z of [-1.18, 1.18]) {
          const tire = mesh(new T.CylinderGeometry(0.39, 0.39, 0.42, 8),
            0x191e25, x, 0.4, z, model);
          tire.rotation.z = Math.PI / 2;
        }
        box(0.4, 0.18, 0.08, 0xff725b, x * 0.72, 0.66, -1.89, model);
      }

      const car = { x: track.center, z: 0, heading: 0, speed: 0 };
      const lap = { seconds: 0, angle: 0, best: null };
      try {
        const saved = Number(localStorage.getItem(storageKey));
        if (Number.isFinite(saved) && saved > 0) lap.best = saved;
      } catch {
        // The session record still works when storage is blocked.
      }

      function format(seconds) {
        const ms = Math.round(seconds * 1000);
        const min = Math.floor(ms / 60000);
        const sec = String(Math.floor(ms / 1000) % 60).padStart(2, '0');
        return `${min}:${sec}.${String(ms % 1000).padStart(3, '0')}`;
      }

      function showBest() {
        best.textContent = lap.best === null ? '---' : format(lap.best);
      }

      function reset() {
        Object.assign(car, { x: track.center, z: 0, heading: 0, speed: 0 });
        lap.seconds = lap.angle = 0;
        status.textContent = 'Drive past the stripe to start. Follow the loop forward.';
      }

      const keys = new Set();
      const bindings = new Set([
        'KeyW', 'KeyA', 'KeyS', 'KeyD', 'ArrowUp', 'ArrowLeft',
        'ArrowDown', 'ArrowRight', 'KeyR'
      ]);
      const held = (a, b) => Number(keys.has(a) || keys.has(b));
      addEventListener('keydown', event => {
        if (!bindings.has(event.code) || event.altKey || event.ctrlKey || event.metaKey) return;
        event.preventDefault();
        if (event.code === 'KeyR' && !event.repeat) reset();
        keys.add(event.code);
      });
      addEventListener('keyup', event => keys.delete(event.code));
      addEventListener('blur', () => keys.clear());
      document.addEventListener('visibilitychange', () => {
        keys.clear();
        last = performance.now();
      });

      function step(dt) {
        const gas = held('KeyW', 'ArrowUp');
        const brake = held('KeyS', 'ArrowDown');
        const steer = held('KeyA', 'ArrowLeft') - held('KeyD', 'ArrowRight');

        if (brake) car.speed -= (car.speed > 0 ? 52 : 16) * dt;
        else if (gas) car.speed += 24 * dt;
        else car.speed *= Math.exp(-2.1 * dt);
        car.speed = clamp(car.speed, -9, 39);
        if (Math.abs(car.speed) < 0.03) car.speed = 0;

        car.heading += steer * 1.85 * clamp(car.speed / 8, -1, 1) * dt;
        const before = Math.atan2(car.z, car.x);
        car.x += Math.sin(car.heading) * car.speed * dt;
        car.z += Math.cos(car.heading) * car.speed * dt;
        const r = Math.hypot(car.x, car.z);
        const safe = clamp(r, track.inner + 2, track.outer - 2);
        if (safe !== r) {
          car.x *= safe / r;
          car.z *= safe / r;
          car.speed *= Math.exp(-7 * dt);
        }

        const turn = Math.atan2(car.z, car.x) - before;
        const delta = Math.atan2(Math.sin(turn), Math.cos(turn));
        if (lap.seconds === 0 && delta === 0) return;
        if (lap.seconds === 0) status.textContent = 'Time trial active';
        lap.seconds += dt;
        lap.angle += delta;
        if (lap.angle < TAU) return;

        const carry = dt * (lap.angle - TAU) / delta;
        const completed = lap.seconds - carry;
        const record = lap.best === null || completed < lap.best;
        if (record) {
          lap.best = completed;
          showBest();
          try { localStorage.setItem(storageKey, String(completed)); } catch {}
        }
        status.textContent = `${record ? 'New best' : 'Last lap'} · ${format(completed)}`;
        lap.angle -= TAU;
        lap.seconds = carry;
      }

      function resize() {
        const aspect = innerWidth / innerHeight;
        camera.aspect = aspect;
        camera.updateProjectionMatrix();
        const half = 54 / Math.min(1, aspect);
        Object.assign(overview, {
          left: -half * aspect, right: half * aspect, top: half, bottom: -half
        });
        overview.updateProjectionMatrix();
        renderer.setSize(innerWidth, innerHeight);
      }

      function frame(now) {
        const elapsed = Math.max(0, (now - last) / 1000);
        last = now;
        if (!document.hidden) {
          const dt = Math.min(elapsed, 0.1);
          const steps = Math.ceil(dt * 120);
          for (let i = 0; i < steps; i++) step(dt / steps);
          if (lap.seconds > 0) lap.seconds += elapsed - dt;
        }

        model.position.set(car.x, 0, car.z);
        model.rotation.y = car.heading;
        const dx = Math.sin(car.heading);
        const dz = Math.cos(car.heading);
        camera.position.set(car.x - dx * 10, 6.2, car.z - dz * 10);
        camera.lookAt(car.x + dx * 5, 0.8, car.z + dz * 5);
        const text = format(lap.seconds);
        if (current.textContent !== text) current.textContent = text;
        renderer.render(scene, reduced.matches ? overview : camera);
        requestAnimationFrame(frame);
      }

      let last = performance.now();
      addEventListener('resize', resize);
      resize();
      showBest();
      reset();
      requestAnimationFrame(frame);
    }
  </script>
</body>
</html>
```

### Run it

Serve the folder containing `index.html`. For example, if Python is installed, run `python -m http.server 8000` and open `http://localhost:8000`. The browser needs WebGL and an internet connection to load Three.js.

### How I'd verify it

| Check | Expected result |
|---|---|
| Load the page and check DevTools | The car starts on the checkered stripe, the current timer reads `0:00.000`, and there are no console errors. |
| Drive with WASD, then with the arrows | Both layouts steer, accelerate, brake, and reverse. Arrow keys don't scroll the page. The road edges slow the car and keep it on track. From the starting heading, steer left to follow the curve. |
| Complete two forward laps | The first lap sets a best. The current timer rolls into the next lap. A slower lap leaves the best alone; a faster lap replaces it. |
| Reverse over the stripe and drive forward over it again | No lap is awarded. A lap requires a full net turn in the forward direction. |
| Press R halfway through a lap, then reload after setting a record | R resets the car and current timer without erasing the best. Reload restores the record when local storage is available. |
| Switch tabs while holding throttle | The hidden tab pauses the run. Returning does not leave throttle stuck. |
| Try a 320 px viewport, 200% zoom, and reduced motion | The HUD and controls remain readable. Reduced motion uses a fixed overhead camera rather than the moving chase camera. |
| Block the CDN request and reload | The page shows a startup error with recovery instructions instead of leaving the loading message in place. |

**Design choice, inferred from the implementation.** An annulus makes the road boundary and lap rule use the same coordinates. A free-form spline would give more variety, but would need separate road projection and checkpoint logic. The circle also makes the tradeoff visible. There is one long, consistent turn rather than a mix of corners.

**Throughput checkpoint**
1. **Blocking first steps.** Define the track, car, and lap state before wiring input or rendering.
2. **Independent workstreams.** N/A. The deliverable is one inline file and no delegation tool is available.
3. **Shared mutable state.** One animation loop owns driving and lap updates. Keyboard handlers maintain the input set and handle restart.
4. **Smallest safe decomposition.** One file with separate setup, simulation, and rendering functions. The remaining open decision is how the handling feels in a browser.

**Principles that changed the design.** *Model the domain* led to one shared track model and signed lap progress instead of a finish-line trigger alone. *Experience first* led to a chase camera for normal play and a fixed view for reduced motion. *Prove it works* led to browser checks for reverse crossings, record persistence, and tab switching rather than treating source inspection as a pass.


=============== RESPONSE ambition-game-28 ===============

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cinder Circuit</title>
<style>
  body { margin: 0; overflow: hidden; background: #ffc98e; color: #fff; font: 16px system-ui, sans-serif; }
  canvas { display: block; }
  #hud { position: fixed; z-index: 1; top: 16px; left: 16px; padding: 14px 18px;
         border-radius: 10px; background: #19222a; font-variant-numeric: tabular-nums; }
  h1 { margin: 0 0 8px; font-size: 18px; color: #ffd185; }
  small { display: block; margin-top: 8px; color: #d0d8df; }
</style>
</head>
<body>
<div id="hud">
  <h1>Cinder Circuit</h1>
  Lap <span id="lap">1</span> · <span id="time">0.000 s</span><br>
  Best · <span id="best">—</span>
  <small>↑ / W accelerate · ↓ / S brake<br>← → / A D steer · R restart lap</small>
</div>
<script type="module">
import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffc98e);
scene.fog = new THREE.FogExp2(0xffc98e, 0.008);
const camera = new THREE.PerspectiveCamera(62, innerWidth / innerHeight, 0.1, 250);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);
document.body.append(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xfff3db, 0x907057, 2));
const sun = new THREE.DirectionalLight(0xffe0af, 2);
sun.position.set(-30, 50, 20);
scene.add(sun);

const inner = 24, outer = 36, middle = (inner + outer) / 2;
const turn = 2 * Math.PI;

function mesh(geometry, color, x, y, z, parent = scene) {
  const object = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({
    color, flatShading: true
  }));
  object.position.set(x, y, z);
  parent.add(object);
  return object;
}

function box(w, h, d, color, x, y, z, parent) {
  return mesh(new THREE.BoxGeometry(w, h, d), color, x, y, z, parent);
}

function ring(a, b, color, y) {
  mesh(new THREE.RingGeometry(a, b, 96), color, 0, y, 0).rotation.x = -Math.PI / 2;
}

box(360, 1, 360, 0xbd7451, 0, -0.51, 0);
ring(inner, outer, 0x383b43, 0);
ring(inner, inner + 0.35, 0xffc66b, 0.015);
ring(outer - 0.35, outer, 0xffc66b, 0.015);

for (let i = 1; i < 48; i++) {
  const a = i * turn / 48;
  box(0.16, 0.02, 1.65, 0xc9c0ad, Math.sin(a) * middle, 0.02,
      Math.cos(a) * middle).rotation.y = a + Math.PI / 2;
}
for (let row = 0; row < 2; row++) {
  for (let i = 0; i < 12; i++) {
    box(0.5, 0.02, 1, (i + row) % 2 ? 0xf6ead0 : 0x22252b,
        (row - 0.5) * 0.5, 0.025, inner + i + 0.5);
  }
}
for (let i = 0; i < 28; i++) {
  const a = i * 2.39996;
  const r = i % 3 === 0 ? 10 + i % 10 : 44 + i % 17;
  const rock = mesh(new THREE.DodecahedronGeometry(1.1 + (i % 5) * 0.35),
    i % 2 ? 0xd99265 : 0xa65a41, Math.sin(a) * r, 0.65, Math.cos(a) * r);
  rock.rotation.set(i, a, i / 2);
}

const car = new THREE.Group();
scene.add(car);
box(1.65, 0.48, 2.8, 0x26c6be, 0, 0.52, 0, car);
box(1.24, 0.44, 1.2, 0x25424c, 0, 0.92, -0.2, car);
box(1.45, 0.12, 0.35, 0xffda70, 0, 0.84, -1.16, car);
for (const x of [-0.87, 0.87]) {
  for (const z of [-0.92, 0.92]) {
    mesh(new THREE.CylinderGeometry(0.31, 0.31, 0.29, 8),
      0x20242a, x, 0.31, z, car).rotation.z = Math.PI / 2;
  }
}

const lapText = document.querySelector('#lap');
const timeText = document.querySelector('#time');
const bestText = document.querySelector('#best');
const keys = new Set();
const controls = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'w', 'a', 's', 'd', 'r'];
const down = (a, b) => keys.has(a) || keys.has(b);
const format = ms => `${(ms / 1000).toFixed(3)} s`;
const view = new THREE.Vector3();
let heading, speed, progress, started, lap = 1, best = Infinity;

function restart() {
  car.position.set(0, 0, middle);
  heading = Math.PI / 2;
  speed = progress = 0;
  started = null;
}
restart();

addEventListener('keydown', event => {
  const key = event.key.length === 1 ? event.key.toLowerCase() : event.key;
  if (!controls.includes(key)) return;
  event.preventDefault();
  keys.add(key);
  if (key === 'r' && !event.repeat) restart();
});
addEventListener('keyup', event => keys.delete(
  event.key.length === 1 ? event.key.toLowerCase() : event.key
));
addEventListener('blur', () => keys.clear());
addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});

let previous = performance.now();
renderer.setAnimationLoop(now => {
  const dt = Math.min(Math.max((now - previous) / 1000, 0), 0.05);
  previous = now;
  const gas = down('ArrowUp', 'w');
  const brake = down('ArrowDown', 's');
  if (gas && !brake && started === null) started = now;
  speed = THREE.MathUtils.clamp(speed + (brake ? -29 : gas ? 16 : -6) * dt, 0, 27);

  const steer = Number(down('ArrowLeft', 'a')) - Number(down('ArrowRight', 'd'));
  heading += steer * 1.8 * Math.min(speed / 6, 1) * dt;
  car.rotation.y = heading;
  const dx = Math.sin(heading), dz = Math.cos(heading);
  const { x, z } = car.position;
  car.position.x += dx * speed * dt;
  car.position.z += dz * speed * dt;
  const radius = Math.hypot(car.position.x, car.position.z);
  const limit = THREE.MathUtils.clamp(radius, inner + 1, outer - 1);
  if (limit !== radius) {
    car.position.multiplyScalar(limit / radius);
    speed *= Math.exp(-5 * dt);
  }

  // Signed angular travel cancels out backtracking and wraps across ±π.
  const delta = Math.atan2(car.position.x, car.position.z) - Math.atan2(x, z);
  progress += Math.atan2(Math.sin(delta), Math.cos(delta));
  if (progress >= turn && started !== null) {
    // Interpolate the finish crossing within this frame.
    const finish = now - dt * 1000 * (progress - turn) / deltaWrapped(delta);
    best = Math.min(best, finish - started);
    bestText.textContent = format(best);
    lapText.textContent = ++lap;
    progress -= turn;
    started = finish;
  }
  timeText.textContent = format(started === null ? 0 : now - started);

  camera.position.copy(car.position).add(view.set(-dx * 8, 5.5, -dz * 8));
  camera.lookAt(view.set(car.position.x + dx * 5, 0.5, car.position.z + dz * 5));
  renderer.render(scene, camera);
});

function deltaWrapped(angle) {
  return Math.atan2(Math.sin(angle), Math.cos(angle));
}
</script>
</body>
</html>
```

Save as `index.html` and open it in a modern browser with internet access for the pinned Three.js CDN import. The best lap is kept for the current page session.

**How I’d verify it (not run here):**
1. Open DevTools and check that the track, car, and HUD render without console errors. Resize the window and confirm the view still fills it.
2. Hold **W**, steer with **A/D**, and brake with **S**. Repeat with the arrow keys. The car should slow against either track edge instead of leaving the circuit.
3. Follow the track from the starting line in the direction the car faces. A full lap should increment the lap count, record a best time, and start the next timer. Run a slower lap to check that the best stays unchanged, then a faster one to check that it updates.
4. Turn around and cross the line backward, then drive forward over it again. Neither crossing should count as a lap. Press **R** mid-lap and confirm the car returns to the line, the timer resets, and the best time stays visible.


=============== RESPONSE ambition-game-29 ===============

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ridge Run</title>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; overflow: hidden; background: #bde4ef; color: white;
           font: 16px system-ui, sans-serif; }
    canvas { display: block; }
    #hud { position: fixed; top: 16px; left: 16px; padding: 14px 18px;
           background: #15212aee; border-radius: 10px; pointer-events: none;
           font-variant-numeric: tabular-nums; }
    h1 { margin: 0 0 8px; font-size: 20px; }
    p { margin: 4px 0; }
    small { color: #bfd2df; }
  </style>
</head>
<body>
  <section id="hud">
    <h1>Ridge Run</h1>
    <p>Lap <span id="lap">1</span> · <span id="time">0.00 s</span></p>
    <p>Best · <span id="best">—</span></p>
    <small>↑/W accelerate · ↓/S brake · ←/→ or A/D steer</small>
  </section>
  <script type="module">
    import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js';

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xbde4ef);
    scene.fog = new THREE.Fog(0xbde4ef, 75, 175);
    const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 220);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    document.body.appendChild(renderer.domElement);
    function resize() {
      camera.aspect = innerWidth / innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(innerWidth, innerHeight);
    }
    addEventListener('resize', resize);
    resize();

    scene.add(new THREE.HemisphereLight(0xfff4dc, 0x62794e, 1.8));
    const sun = new THREE.DirectionalLight(0xffefcf, 2);
    sun.position.set(-30, 45, 20);
    scene.add(sun);

    function mesh(geometry, color, parent, x, y, z) {
      const object = new THREE.Mesh(geometry,
        new THREE.MeshStandardMaterial({ color, flatShading: true }));
      object.position.set(x, y, z);
      parent.add(object);
      return object;
    }
    function box(parent, color, x, y, z, w, h, d) {
      return mesh(new THREE.BoxGeometry(w, h, d), color, parent, x, y, z);
    }
    box(scene, 0x729c59, 0, -0.52, 0, 360, 1, 360);

    const TAU = 2 * Math.PI;
    const halfWidth = 5;
    function track(angle, lane = 0, y = 0) {
      return new THREE.Vector3((36 + lane) * Math.cos(angle), y,
                               (23 + lane) * Math.sin(angle));
    }
    function strip(inner, outer, y, color) {
      const points = [];
      for (let i = 0; i < 96; i++) {
        const a = i * TAU / 96, b = (i + 1) * TAU / 96;
        const p = track(a, inner, y), q = track(a, outer, y);
        const r = track(b, inner, y), s = track(b, outer, y);
        for (const v of [p, r, q, q, r, s]) points.push(v.x, v.y, v.z);
      }
      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute('position', new THREE.Float32BufferAttribute(points, 3));
      geometry.computeVertexNormals();
      mesh(geometry, color, scene, 0, 0, 0);
    }
    strip(-halfWidth, halfWidth, 0.01, 0x343c47);
    strip(-halfWidth, -halfWidth + 0.22, 0.02, 0xffcd68);
    strip(halfWidth - 0.22, halfWidth, 0.02, 0xffcd68);

    // The finish line is at angle zero, across the full road.
    for (let i = 0; i < 10; i++) {
      for (let j = 0; j < 2; j++) {
        box(scene, (i + j) % 2 ? 0x141820 : 0xffffff,
            track(0, i - halfWidth + 0.5).x, 0.025, (j - 0.5) * 0.45,
            1, 0.02, 0.45);
      }
    }
    for (let i = 0; i < 24; i++) {
      const a = i * TAU / 24;
      const p = track(a, i % 2 ? 10 + i % 5 : -10);
      const h = 3.3 + (i % 4) * 0.7;
      box(scene, 0x694834, p.x, 0.7, p.z, 0.45, 1.4, 0.45);
      mesh(new THREE.ConeGeometry(h * 0.36, h, 5), 0x31644e,
           scene, p.x, 1 + h / 2, p.z);
    }

    const car = new THREE.Group();
    scene.add(car);
    box(car, 0xff5138, 0, 0.57, 0, 1.65, 0.55, 3.05);
    box(car, 0x30475a, 0, 1.02, -0.25, 1.25, 0.45, 1.35);
    for (const x of [-0.86, 0.86]) {
      for (const z of [-0.95, 0.95]) {
        const wheel = mesh(new THREE.CylinderGeometry(0.36, 0.36, 0.32, 8),
                           0x171a20, car, x, 0.36, z);
        wheel.rotation.z = Math.PI / 2;
      }
    }

    const keys = new Set();
    const controls = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
                      'KeyW', 'KeyA', 'KeyS', 'KeyD'];
    addEventListener('keydown', event => {
      if (!controls.includes(event.code)) return;
      event.preventDefault();
      keys.add(event.code);
    });
    addEventListener('keyup', event => keys.delete(event.code));
    addEventListener('blur', () => keys.clear());
    const pressed = (a, b) => keys.has(a) || keys.has(b);

    const lapText = document.querySelector('#lap');
    const timeText = document.querySelector('#time');
    const bestText = document.querySelector('#best');
    const seconds = ms => `${(ms / 1000).toFixed(2)} s`;
    let angle = 0, lane = 0, speed = 0;
    let lap = 1, best = Infinity, lapStart = null, previous = null;

    function frame(now) {
      const dt = previous === null ? 0 : Math.min((now - previous) / 1000, 0.05);
      previous = now;
      const gas = pressed('ArrowUp', 'KeyW');
      const brake = pressed('ArrowDown', 'KeyS');
      const steer = Number(pressed('ArrowRight', 'KeyD')) -
                    Number(pressed('ArrowLeft', 'KeyA'));
      speed = THREE.MathUtils.clamp(speed + (brake ? -30 : gas ? 14 : -5) * dt, 0, 28);

      // Arcade steering moves across the road; its edges keep the car on track.
      lane = THREE.MathUtils.clamp(lane + steer * Math.min(speed * 0.3, 5) * dt,
                                  -halfWidth + 1, halfWidth - 1);
      const tangentX = -(36 + lane) * Math.sin(angle);
      const tangentZ =  (23 + lane) * Math.cos(angle);
      const step = speed * dt / Math.hypot(tangentX, tangentZ);
      if (step > 0 && lapStart === null) lapStart = now - dt * 1000;
      if (angle + step >= TAU) {
        const crossing = now - dt * 1000 * (1 - (TAU - angle) / step);
        best = Math.min(best, crossing - lapStart);
        bestText.textContent = seconds(best);
        lapText.textContent = ++lap;
        lapStart = crossing;
      }
      angle = (angle + step) % TAU;
      timeText.textContent = seconds(lapStart === null ? 0 : now - lapStart);

      car.position.copy(track(angle, lane));
      const yaw = Math.atan2(-(36 + lane) * Math.sin(angle),
                              (23 + lane) * Math.cos(angle));
      car.rotation.y = yaw + steer * Math.min(speed / 25, 0.17);
      camera.position.copy(car.position);
      camera.position.x -= 9 * Math.sin(yaw);
      camera.position.y += 5.5;
      camera.position.z -= 9 * Math.cos(yaw);
      camera.lookAt(track(angle + 0.13, lane, 0.7));

      renderer.render(scene, camera);
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  </script>
</body>
</html>
```

**How I’d verify it**

1. Save it as `index.html` and open it in a modern browser with internet access so it can load Three.js from the CDN. Check that the road, car, and HUD appear and that the browser console has no errors.
2. Try both key sets. Confirm the car starts stationary, accelerates, brakes to a stop, and steers to both road edges without leaving the track. Switch focus while holding the throttle, then return and check that the key isn’t stuck.
3. Drive across the checkered line. Confirm the lap counter advances once, the timer restarts near zero, and Best shows the completed lap. Brake during the next lap to make it slower and confirm Best stays unchanged. Resize the window and check that the scene retains its proportions.

I haven’t run this here. The best lap is session-only; reloading resets it.
