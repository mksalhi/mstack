"""Measure a supplied music track so the film can cut on it.

    pip install numpy librosa soundfile
    python beats.py audio/track.wav > beats.json

Output: bpm, beats (state changes go here), downbeats (big moments), hits (sound effects).
Assumes 4 beats per bar starting on the first detected beat; check the downbeats by ear.
"""
import json
import sys

import librosa
import numpy as np

samples, rate = librosa.load(sys.argv[1], sr=None, mono=True)
tempo, beat_frames = librosa.beat.beat_track(y=samples, sr=rate)
beats = librosa.frames_to_time(beat_frames, sr=rate)

strength = librosa.onset.onset_strength(y=samples, sr=rate)
hit_frames = librosa.onset.onset_detect(onset_envelope=strength, sr=rate, backtrack=False)
hits = librosa.frames_to_time(hit_frames, sr=rate)

json.dump(
    {
        "bpm": round(float(np.atleast_1d(tempo)[0]), 2),
        "beats": [round(float(t), 3) for t in beats],
        "downbeats": [round(float(t), 3) for t in beats[::4]],
        "hits": [round(float(t), 3) for t in hits],
    },
    sys.stdout,
    indent=1,
)
