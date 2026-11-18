// Renders a film to a silent MP4 by seeking the page frame by frame and piping screenshots to ffmpeg.
//
//   node render.mjs                          full render of index.html, 9x16, 30 fps
//   node render.mjs --format 16x9 --fps 60 --sub 4     60 fps, 4 blended subframes per frame (motion blur)
//   node render.mjs --fps 2 --out out/draft.mp4        cheap draft for a contact sheet
//   node render.mjs --from 4 --to 6 --out out/fix.mp4  re-render only the seconds you changed
//
// The page either defines window.seek(t) and window.FILM = { width, height, duration } (canvas films),
// or is a CSS-keyframe page: then every animation is paused and seeked, and --size and --to are required.
// Set CHROME_PATH to use an installed Chrome instead of the one Puppeteer downloads.
import { spawn } from "node:child_process";
import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import puppeteer from "puppeteer";

const flag = (name, fallback) => {
  const i = process.argv.indexOf(`--${name}`);
  return i > 0 ? process.argv[i + 1] : fallback;
};
const fps = Number(flag("fps", 30));
const sub = Number(flag("sub", 1));
const out = flag("out", "out/silent.mp4");
const url = pathToFileURL(resolve(flag("page", "index.html")));
url.searchParams.set("render", "1");
url.searchParams.set("format", flag("format", "9x16"));

const browser = await puppeteer.launch({ executablePath: process.env.CHROME_PATH });
const page = await browser.newPage();
await page.goto(url.href);
const film = await page.evaluate(() => window.FILM ?? null);
const [width, height] = film ? [film.width, film.height] : (flag("size", "") || "x").split("x").map(Number);
const from = Number(flag("from", 0));
const to = Number(flag("to", film?.duration));
if (!width || !height || !(to > from)) {
  await browser.close();
  throw new Error("The page has no window.FILM, so pass --size 1920x1080 and --to <seconds>.");
}
await page.setViewport({ width, height, deviceScaleFactor: 1 });
await page.evaluate(() => document.fonts.ready);

mkdirSync(dirname(resolve(out)), { recursive: true });
// tmix averages the last `sub` subframes; select keeps the one frame per group that averages a whole group.
const blur = sub > 1 ? ["-vf", `tmix=frames=${sub},select='not(mod(n+1\\,${sub}))',setpts=N/${fps}/TB`] : [];
const ffmpeg = spawn(
  "ffmpeg",
  ["-y", "-loglevel", "error", "-f", "image2pipe", "-c:v", "png", "-framerate", String(fps * sub), "-i", "-",
    ...blur, "-r", String(fps), "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out],
  { stdio: ["pipe", "inherit", "inherit"] },
);
const encoded = new Promise((done, fail) => {
  ffmpeg.on("close", (code) => (code === 0 ? done() : fail(new Error(`ffmpeg exited with ${code}`))));
});

const total = Math.round((to - from) * fps * sub);
for (let i = 0; i < total; i++) {
  await page.evaluate((t) => {
    if (window.seek) return void window.seek(t);
    for (const animation of document.getAnimations()) {
      animation.pause();
      animation.currentTime = t * 1000;
    }
  }, from + i / (fps * sub));
  const frame = await page.screenshot({ type: "png", optimizeForSpeed: true });
  if (!ffmpeg.stdin.write(frame)) await new Promise((drained) => ffmpeg.stdin.once("drain", drained));
  if (i % (fps * sub * 2) === 0) console.log(`rendering ${(from + i / (fps * sub)).toFixed(1)}s of ${to}s`);
}
ffmpeg.stdin.end();
await encoded;
await browser.close();
console.log(`wrote ${out} (${width}x${height}, ${to - from}s at ${fps} fps)`);
