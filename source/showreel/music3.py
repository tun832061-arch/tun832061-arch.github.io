import numpy as np, wave, sys
from scipy.signal import butter, sosfilt
SR = 48000; T = 45.1; n = int(SR * T); rng = np.random.default_rng(4); out = np.zeros((n, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def put(s, at, g=1.0, pan=0.0):
    i = int(at * SR); m = min(len(s), n - i)
    if m <= 0: return
    out[i:i+m, 0] += s[:m] * g * (1 - max(0, pan)); out[i:i+m, 1] += s[:m] * g * (1 + min(0, pan))
kick = lambda: (lambda y: np.sin(2 * np.pi * np.cumsum(48 + 120 * np.exp(-y * 30)) / SR) * np.exp(-y * 8))(tt(0.4))
snare = lambda: (lambda y: (rng.normal(0, 1, len(y)) * 0.6 + np.sin(2 * np.pi * 190 * y) * 0.4) * np.exp(-y * 22))(tt(0.3))
hat = lambda: (lambda y: np.diff(rng.normal(0, 1, len(y)), prepend=0) * np.exp(-y * 60) * 0.25)(tt(0.06))
def bass(f, d): y = tt(d); return np.tanh(2.2 * np.sin(2 * np.pi * f * y)) * 0.5 * np.minimum(1, y / 0.005) * np.exp(-y * 2.5)
def hit(): y = tt(1.6); return (np.sin(2 * np.pi * 55 * y) * 0.9 + rng.normal(0, 1, len(y)) * 0.25 * np.exp(-y * 9)) * np.exp(-y * 2.2)
def riser(d): y = tt(d); return np.diff(rng.normal(0, 1, len(y)), prepend=0) * (y / d) ** 2 * 0.35
def pad(fs, d): y = tt(d); s = sum(np.sin(2 * np.pi * f * y) for f in fs) / len(fs); return s * np.minimum(1, y / 1.0) * np.minimum(1, (d - y) / 1.5) * 0.35
roots = [55, 55, 65.41, 49]; B = 0.5
def groove(a, b):
    k = int(a / B)
    while k * B < b:
        at = k * B; r = roots[(k // 4) % 4]
        put(kick(), at, 1.0); put(hat(), at + B / 2, 0.8, 0.3); put(hat(), at, 0.5, -0.3)
        if k % 4 in (1, 3): put(snare(), at, 0.55)
        put(bass(r, B * 0.9), at, 0.55); put(bass(r * 2, B * 0.4), at + B * 0.5, 0.25); k += 1
for i in range(8): put(hat(), i * 0.25, 0.6)        # collage: panels land on eighth notes
groove(2.0, 20.9); groove(40.1, 42.1)
for c in [5.0, 8.0, 11.0, 13.5, 16.5, 19.5, 40.1]: put(hit(), c, 0.5)
put(riser(1.4), 19.5, 0.8)
mx = np.max(np.abs(out)); out = np.tanh(out / mx * 1.1) / 1.12
# The Last Watch keeps its own score from HOLD THE LINE to its title card
w = wave.open(sys.argv[2]); lw = np.frombuffer(w.readframes(w.getnframes()), '<i2').reshape(-1, 2).astype(float) / 32768
i0 = int(20.95 * SR); m = min(len(lw), n - i0); seg = lw[:m] * 0.95
fi, fo = int(0.5 * SR), int(0.4 * SR); seg[:fi] *= np.linspace(0, 1, fi)[:, None]; seg[-fo:] *= np.linspace(1, 0, fo)[:, None]
duck = np.ones(n); duck[i0:i0 + m] = 0.0; duck[i0:i0 + fi] = np.linspace(1, 0, fi); out *= duck[:, None]; out[i0:i0 + m] += seg
put(hit(), 42.1, 0.9); put(pad([110, 164.81, 220, 277.18], 3.0), 42.1, 0.9)
k = int(1.0 * SR); out[-k:] *= np.linspace(1, 0, k)[:, None]; out /= np.max(np.abs(out)) * 1.05
wv = wave.open(sys.argv[1], 'wb'); wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((out * 32767).astype('<i2').tobytes()); wv.close()
