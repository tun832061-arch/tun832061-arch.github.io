import numpy as np, wave, sys
from scipy.signal import butter, sosfilt
SR = 48000; T = 38.0; n = int(SR * T); rng = np.random.default_rng(4); out = np.zeros((n, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def put(s, at, g=1.0, pan=0.0):
    i = int(at * SR); m = min(len(s), n - i)
    if m <= 0: return
    out[i:i+m, 0] += s[:m] * g * (1 - max(0, pan)); out[i:i+m, 1] += s[:m] * g * (1 + min(0, pan))
def load(p): w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), '<i2').reshape(-1, 2).astype(float) / 32768
kick = lambda: (lambda y: np.sin(2 * np.pi * np.cumsum(48 + 120 * np.exp(-y * 30)) / SR) * np.exp(-y * 8))(tt(0.4))
snare = lambda: (lambda y: (rng.normal(0, 1, len(y)) * 0.6 + np.sin(2 * np.pi * 190 * y) * 0.4) * np.exp(-y * 22))(tt(0.3))
hat = lambda: (lambda y: np.diff(rng.normal(0, 1, len(y)), prepend=0) * np.exp(-y * 60) * 0.25)(tt(0.06))
def bass(f, d): y = tt(d); return np.tanh(2.2 * np.sin(2 * np.pi * f * y)) * 0.5 * np.minimum(1, y / 0.005) * np.exp(-y * 2.5)
def hit(): y = tt(1.6); return (np.sin(2 * np.pi * 55 * y) * 0.9 + rng.normal(0, 1, len(y)) * 0.25 * np.exp(-y * 9)) * np.exp(-y * 2.2)
def riser(d): y = tt(d); return np.diff(rng.normal(0, 1, len(y)), prepend=0) * (y / d) ** 2 * 0.35
def pad(fs, d): y = tt(d); s = sum(np.sin(2 * np.pi * f * y) for f in fs) / len(fs); return s * np.minimum(1, y / 1.0) * np.minimum(1, (d - y) / 1.5) * 0.35
roots = [55, 55, 65.41, 49]; B = 0.5
def groove(a, b):
    k = int(round(a / B))
    while k * B < b - 1e-6:
        at = k * B; r = roots[(k // 4) % 4]
        put(kick(), at, 1.0); put(hat(), at + B / 2, 0.8, 0.3); put(hat(), at, 0.5, -0.3)
        if k % 4 in (1, 3): put(snare(), at, 0.55)
        put(bass(r, B * 0.9), at, 0.55); put(bass(r * 2, B * 0.4), at + B * 0.5, 0.25); k += 1
groove(8.0, 15.95); groove(28.5, 35.0)
for c in [8.0, 11.0, 14.0, 28.5, 31.0, 33.0]: put(hit(), c, 0.5)
put(riser(1.4), 14.55, 0.8)
out = np.tanh(out / np.max(np.abs(out)) * 1.1) / 1.12
def lay(seg, at, fi=0.05, fo=0.05, g=0.95):
    seg = seg.copy() * g; a, b = int(fi * SR), int(fo * SR)
    if a: seg[:a] *= np.linspace(0, 1, a)[:, None]
    if b: seg[-b:] *= np.linspace(1, 0, b)[:, None]
    i = int(at * SR); m = min(len(seg), n - i); out[i:i+m] += seg[:m]
# Say It Slower's own voice + sound design opens the reel
ss = load(sys.argv[2]); lay(ss[: int(8.15 * SR)], 0.0, 0.0, 0.45, 1.0)
# The Last Watch: HOLD THE LINE cuts, then straight to the embers title (its own score)
lwa, lwb = load(sys.argv[3]), load(sys.argv[4])
i0 = int(15.95 * SR); j = i0 + len(lwa); k2 = j + len(lwb)
out[i0:k2] *= 0.0
lay(lwa, 15.95, 0.3, 0.12); lay(lwb, 15.95 + len(lwa) / SR - 0.1, 0.12, 0.3)
put(hit(), 35.0, 0.9); put(pad([110, 164.81, 220, 277.18], 3.0), 35.0, 0.9)
kk = int(0.8 * SR); out[-kk:] *= np.linspace(1, 0, kk)[:, None]; out /= np.max(np.abs(out)) * 1.05
wv = wave.open(sys.argv[1], 'wb'); wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((out * 32767).astype('<i2').tobytes()); wv.close()
