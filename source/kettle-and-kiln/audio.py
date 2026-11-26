import numpy as np, wave, sys
from scipy.signal import butter, sosfilt, fftconvolve
SQ = len(sys.argv) > 3 and sys.argv[3] == 'sq'; T = float(sys.argv[2]); SR = 48000; n = int(SR * T); rng = np.random.default_rng(5); mix = np.zeros((n, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def put(s, at, g=1.0, pan=0.0):
    i = int(at * SR); m = min(len(s), n - i)
    if m <= 0 or i < 0: return
    mix[i:i+m, 0] += s[:m] * g * (1 - max(0, pan)); mix[i:i+m, 1] += s[:m] * g * (1 + min(0, pan))
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def rhodes(f, d):
    y = tt(d); mod = np.sin(2 * np.pi * f * 1.0 * y) * 1.2 * np.exp(-y * 3)
    s = np.sin(2 * np.pi * f * y + mod * 0.5) * (0.35 + 0.65 * np.exp(-y * 0.9)) + 0.15 * np.sin(2 * np.pi * 2 * f * y) * np.exp(-y * 3)
    return s * np.minimum(1, y / 0.06) * np.minimum(1, (d - y) / 0.6)
def plop(f=300): y = tt(0.18); return np.sin(2 * np.pi * np.cumsum(f * (1 + 1.5 * np.exp(-y * 45))) / SR) * np.exp(-y * 28)
def clink(): y = tt(1.2); return sum(a * np.sin(2 * np.pi * f * y) * np.exp(-y * d) for f, a, d in [(1870, 1, 5), (2950, .5, 7), (4410, .3, 9), (5200, .2, 12)])
def tick(): y = tt(0.04); return bp(rng.normal(0, 1, len(y)), 1500, 5000) * np.exp(-y * 120) * 0.5
def liquid(d):  # pour: filtered noise with gurgle
    y = tt(d); x = rng.normal(0, 1, len(y)); g = 0.6 + 0.4 * np.sin(2 * np.pi * (7 + 3 * np.sin(y * 3)) * y)
    return bp(x, 300, 2500) * g * np.sin(np.pi * y / d) ** 0.5
def swoosh(d=0.8): y = tt(d); return bp(rng.normal(0, 1, len(y)), 200, 1800) * np.sin(np.pi * y / d) ** 2 * 0.6
# --- music: Fmaj7  Em7  Dm7  Cmaj7, one chord per 2.4 s, soft bass + shaker
chords = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]; D = 2.4
for i in range(int(T / D) + 1):
    at = i * D; ch = chords[i % 4]
    for j, m in enumerate(ch): put(rhodes(mtof(m), D + 0.6), at + j * 0.03, 0.06, (j - 1.5) * 0.2)
    put(lp(np.sin(2 * np.pi * mtof(ch[0] - 12) * tt(D + 0.3)) * np.minimum(1, tt(D + 0.3) / 0.15) * np.minimum(1, (D + 0.3 - tt(D + 0.3)) / 0.4) * 0.8, 300), at, 0.12)
    if at >= 2.4:
        for k in range(8): x = hp(rng.normal(0, 1, int(0.06 * SR)), 5000) * np.exp(-tt(0.06) * 50); put(x, at + k * D / 8, 0.05 if k % 2 else 0.03, 0.4)
# --- sound design
put(liquid(1.6), 0.15, 0.45); [put(plop(260 + 40 * i), 0.9 + i * 0.22, 0.35) for i in range(5)]
put(clink(), 1.95, 0.25)
for i in range(13): put(tick(), 2.2 + i * 0.07, 0.6)
wipes = [4.6, 9.4, 15.4, 20.6]
for w in wipes: put(swoosh(), w - 0.05, 0.5); put(plop(180), w + 0.55, 0.25)
put(liquid(1.2), 5.8, 0.18)                                # curve drawn as a pour
for i in range(3): put(tick(), 7.0 + i * 0.3, 0.6)
put(plop(420), 8.6, 0.3)
items = [10.2, 12.0, 13.8, 11.1, 12.9, 14.7] if SQ else [10.4, 11.2, 12.0, 13.8, 14.05, 14.3]
for i, w in enumerate(items): put(swoosh(0.5), w, 0.3, (i % 3 - 1) * 0.4); put(plop(300 + 60 * (i % 3)), w + 0.4, 0.22)
put(swoosh(0.5), 16.6, 0.3); put(swoosh(0.6), 17.6, 0.35); put(clink(), 17.95, 0.12)
st = hp(rng.normal(0, 1, int(3.5 * SR)), 3000) * np.sin(np.pi * tt(3.5) / 3.5) * 0.05; put(st, 21.8, 1.0)
put(clink(), 21.3, 0.15)
# --- room + master
ir = rng.normal(0, 1, (int(1.6 * SR), 2)) * np.exp(-tt(1.6) * 3.5)[:, None]
wet = np.stack([fftconvolve(mix[:, c], lp(ir[:, c], 5000))[:n] for c in (0, 1)], 1)
out = mix / np.max(np.abs(mix)) + 0.18 * wet / np.max(np.abs(wet)); out = np.tanh(out * 1.2); out /= np.max(np.abs(out)) * 1.1
k = int(0.8 * SR); f = np.ones(n); f[-k:] = np.linspace(1, 0, k); out *= f[:, None]
w = wave.open(sys.argv[1], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype('<i2').tobytes()); w.close()
