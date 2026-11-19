
# Motion sound

One timeline: the same numbers place the cuts and the sounds. Needs `audio.mjs` and `beats.py` from the kit; if missing, run `engine.md` first.

## Path 1: a track is supplied

Measure before animating.

```bash
pip install numpy librosa soundfile
python beats.py audio/track.wav > beats.json
```

`beats.json` holds `bpm`, `beats`, `downbeats`, `hits`:

- State changes and cuts on `beats`.
- Big moments (hook, reveal, logo) on `downbeats`; start the film on one.
- Effects on `hits` (measured peaks).

Downbeats assume 4/4 from the first detected beat; if cuts feel a beat off, confirm with the user by ear.

## Path 2: nothing is supplied

Pick a tempo (default 120 BPM, a beat per half second); `beatGrid(bpm, duration)` in `motion.js` gives `beats` and `downbeats`.

Write `cues.json` from the shot list, one cue per visible event:

```json
[
  { "t": 0.0, "voice": "thump" },
  { "t": 0.5, "voice": "whoosh", "dur": 0.5 },
  { "t": 2.0, "voice": "pop" },
  { "t": 5.5, "voice": "chime", "freq": 880, "gain": 0.8 }
]
```

```bash
node audio.mjs cues.json out/sfx.wav 15     # last argument: film length in seconds
```

Voices: `click`, `tick`, `pop`, `thump`, `whoosh`, `tone`, `chime`. New textures or melody: add a voice (one function of time) to `VOICES` in `audio.mjs`; keep the seeded noise generator.

- Sparse beats dense.
- No generic synth pads; music is a real phrase with a start, a lift, and a landing on the logo.

## Voice

Narrator or character: call the user's text-to-speech API (key in `.env`, referred to by name). Generate the voice first, measure it, time the shots to it.

## Mix

Target **−16 LUFS** for web, help-center and product demos; **−14 LUFS** for social reels. Other skills cite this rule. Commands use −14; set `I=-16` in `loudnorm` for a demo.

```bash
# effects only
ffmpeg -y -i out/silent.mp4 -i out/sfx.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
  -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest out/final.mp4

# supplied track plus effects
ffmpeg -y -i out/silent.mp4 -i audio/track.wav -i out/sfx.wav \
  -filter_complex "[1:a][2:a]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest out/final.mp4
```

## Check it without ears

- `audio.mjs` prints the peak and warns on clipping.
- Print loudness per 0.1 s from the final file; confirm each burst lines up with a cue.
- Filtered noise (whoosh) measures far quieter than a tone at equal gain: raise noise voices to within about 2x of tonal ones.
- Tell the user timing was verified by measurement and the mix has not been judged by ear.
