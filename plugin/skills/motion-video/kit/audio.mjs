// Synthesizes a sound-effects track from a cue list. No samples, no dependencies, same output every run.
//
//   node audio.mjs cues.json out/sfx.wav [seconds]
//
// cues.json: [{ "t": 0.5, "voice": "click" }, { "t": 2, "voice": "tone", "freq": 660, "dur": 0.4, "gain": 0.8 }]
// Add a voice per film when these are not enough: [default seconds, (t, cue, dur) => sample in -1..1].
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

const RATE = 48000;
const TAU = Math.PI * 2;

let seed = 42;
const noise = () => {
  seed = (seed * 1664525 + 1013904223) >>> 0;
  return seed / 2147483648 - 1;
};

const VOICES = {
  click: [0.05, (t) => Math.sin(TAU * 1900 * t) * Math.exp(-t * 95) * 0.5],
  tick: [0.04, (t) => Math.sin(TAU * 3200 * t) * Math.exp(-t * 140) * 0.3],
  pop: [0.16, (t) => Math.sin(TAU * (520 * t + 480 * t * t)) * Math.exp(-t * 28) * 0.45],
  thump: [0.5, (t) => Math.sin(TAU * (95 * t - 35 * t * t)) * Math.exp(-t * 9) * 0.9],
  whoosh: [0.4, (t, _cue, dur) => noise() * Math.sin((Math.PI * t) / dur) ** 2 * 0.3],
  tone: [0.4, (t, cue) => Math.sin(TAU * (cue.freq ?? 440) * t) * Math.exp(-t * 6) * 0.35],
  chime: [0.9, (t, cue) => {
    const f = cue.freq ?? 880;
    return (Math.sin(TAU * f * t) + 0.5 * Math.sin(TAU * f * 1.5 * t)) * Math.exp(-t * 5) * 0.25;
  }],
};

const [cuesPath, outPath, seconds] = process.argv.slice(2);
if (!cuesPath || !outPath) throw new Error("Usage: node audio.mjs cues.json out/sfx.wav [seconds]");
const cues = JSON.parse(readFileSync(cuesPath, "utf8"));
for (const cue of cues) if (!VOICES[cue.voice]) throw new Error(`Unknown voice "${cue.voice}" at ${cue.t}s`);

const length = Number(seconds) || Math.max(...cues.map((cue) => cue.t + (cue.dur ?? VOICES[cue.voice][0]))) + 0.5;
const mix = new Float32Array(Math.ceil(length * RATE));
for (const cue of cues) {
  const [defaultDur, voice] = VOICES[cue.voice];
  const dur = cue.dur ?? defaultDur;
  const start = Math.floor(cue.t * RATE);
  for (let i = 0; i < dur * RATE && start + i < mix.length; i++) {
    mix[start + i] += voice(i / RATE, cue, dur) * (cue.gain ?? 1);
  }
}

// 16-bit mono WAV
const wav = Buffer.alloc(44 + mix.length * 2);
wav.write("RIFF", 0);
wav.writeUInt32LE(36 + mix.length * 2, 4);
wav.write("WAVEfmt ", 8);
wav.writeUInt32LE(16, 16);
wav.writeUInt16LE(1, 20);
wav.writeUInt16LE(1, 22);
wav.writeUInt32LE(RATE, 24);
wav.writeUInt32LE(RATE * 2, 28);
wav.writeUInt16LE(2, 32);
wav.writeUInt16LE(16, 34);
wav.write("data", 36);
wav.writeUInt32LE(mix.length * 2, 40);
let peak = 0;
for (let i = 0; i < mix.length; i++) {
  peak = Math.max(peak, Math.abs(mix[i]));
  wav.writeInt16LE(Math.round(Math.max(-1, Math.min(1, mix[i])) * 32767), 44 + i * 2);
}
mkdirSync(dirname(resolve(outPath)), { recursive: true });
writeFileSync(outPath, wav);
console.log(`wrote ${outPath} (${cues.length} cues, ${length.toFixed(2)}s, peak ${peak.toFixed(2)}${peak > 1 ? ", CLIPPED: lower the gains" : ""})`);
