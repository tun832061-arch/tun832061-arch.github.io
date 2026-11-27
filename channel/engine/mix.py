# mix.py — original music bed (synthesised here, no licensing) ducked under the voice, plus soft section whooshes.
#   python3 mix.py ../ep01        -> ep01/build/mix.wav
import json, os, sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly

ep = sys.argv[1]; b = os.path.join(ep, "build")
S = json.load(open(os.path.join(ep, "script.json"))); T = json.load(open(os.path.join(b, "timeline.json")))
vo, vsr = sf.read(os.path.join(b, "vo.wav")); SR = 48000
vo = resample_poly(vo, SR, vsr); n = len(vo); rng = np.random.default_rng(3)
tt = lambda d: np.arange(int(d * SR)) / SR
lp = lambda x, f: sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)
bp = lambda x, a, c: sosfilt(butter(2, [a, c], "band", fs=SR, output="sos"), x)
mus = np.zeros((n, 2))

def put(s, at, g=1.0, pan=0.0):
    i = int(at * SR); m = min(len(s), n - i)
    if m <= 0 or i < 0: return
    mus[i:i + m, 0] += s[:m] * g * (1 - max(0, pan)); mus[i:i + m, 1] += s[:m] * g * (1 + min(0, pan))

hz = lambda m: 440 * 2 ** ((m - 69) / 12)
# Fmaj9 - Am7 - Dm9 - Bbmaj7 at 84 BPM, two bars each
CH = [[53, 57, 60, 64, 67], [57, 60, 64, 67, 72], [50, 57, 60, 64, 65], [46, 53, 57, 62, 65]]
BEAT = 60 / 84; BAR = 4 * BEAT
def pad(notes, d):
    y = tt(d); env = np.minimum(1, y / 1.2) * np.minimum(1, (d - y) / 1.0)
    s = sum(np.sin(2 * np.pi * hz(m) * y + np.sin(2 * np.pi * 0.2 * y + m)) * (0.6 if m < 55 else 0.35) for m in notes)
    return lp(s, 1400) * env
def pluck(m, d=0.9):
    y = tt(d); return (np.sin(2 * np.pi * hz(m) * y) + 0.3 * np.sin(4 * np.pi * hz(m) * y)) * np.exp(-y * 6)
def kick():
    y = tt(0.35); return np.sin(2 * np.pi * np.cumsum(48 + 90 * np.exp(-y * 30)) / SR) * np.exp(-y * 9)
def hat():
    y = tt(0.05); return bp(rng.normal(0, 1, len(y)), 6000, 12000) * np.exp(-y * 80)
t, k = 0.0, 0
while t < T["dur"]:
    c = CH[k % 4]
    put(pad(c, 2 * BAR + 0.8), t, 0.16)
    for j in range(8):  # arpeggio, eighth notes on alternating beats
        put(pluck(c[(j * 2) % 5] + 12, 0.7), t + j * BEAT, 0.07, 0.4 if j % 2 else -0.4)
    for j in range(8):
        put(kick(), t + j * BEAT * 1, 0.18 if j % 2 == 0 else 0.0)
        put(hat(), t + j * BEAT + BEAT / 2, 0.035, 0.3)
    put(lp(np.sin(2 * np.pi * hz(c[0] - 12) * tt(2 * BAR)) * np.minimum(1, tt(2 * BAR) / 0.1), 300), t, 0.12)
    t += 2 * BAR; k += 1

# whoosh into each section / title card
lines = S["lines"]
for i, L in enumerate(lines):
    if L.get("scene", {}).get("type") in ("section", "title", "end"):
        at = T["lines"][i]["start"] - 0.45; d = 0.5; y = tt(d)
        put(bp(rng.normal(0, 1, len(y)), 500, 6000) * np.sin(np.pi * y / d) ** 2, max(0, at), 0.10)

# duck the bed under the voice (smoothed envelope)
env = np.abs(vo); w = int(0.25 * SR)
env = np.convolve(env, np.ones(w) / w, "same"); env = env / (env.max() + 1e-9)
duck = 1 - 0.55 * np.clip(env * 6, 0, 1)
duck = np.convolve(duck, np.ones(int(0.3 * SR)) / int(0.3 * SR), "same")
mus *= duck[:, None]
fade = int(1.5 * SR); mus[-fade:] *= np.linspace(1, 0, fade)[:, None]; mus[:int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))[:, None]
mix = mus + np.stack([vo, vo], 1) * 0.9
mix /= np.max(np.abs(mix)) * 1.05
sf.write(os.path.join(b, "mix.wav"), mix.astype(np.float32), SR)
print("mix", round(n / SR, 1), "s")
