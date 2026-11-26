import numpy as np, wave, sys
from scipy.signal import butter, sosfilt
AD = sys.argv[2]; T = {'a': 6, 'b': 15, 'c': 10}[AD]; SR = 48000; n = int(SR * T); rng = np.random.default_rng(7); mix = np.zeros((n, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def put(s, at, g=1.0, pan=0.0):
    i = int(at * SR); m = min(len(s), n - i)
    if m <= 0 or i < 0: return
    mix[i:i+m, 0] += s[:m] * g * (1 - max(0, pan)); mix[i:i+m, 1] += s[:m] * g * (1 + min(0, pan))
kick = lambda: (lambda y: np.sin(2 * np.pi * np.cumsum(45 + 140 * np.exp(-y * 35)) / SR) * np.exp(-y * 7))(tt(0.45))
clap = lambda: (lambda y: bp(rng.normal(0, 1, len(y)), 900, 5000) * (np.exp(-y * 40) + 0.6 * np.exp(-np.maximum(0, y - 0.012) * 40) * (y > 0.012)))(tt(0.25))
hat = lambda o=False: (lambda y: hp(rng.normal(0, 1, len(y)), 7000) * np.exp(-y * (18 if o else 70)))(tt(0.2 if o else 0.05))
def hit(): y = tt(1.2); return np.sin(2 * np.pi * np.cumsum(38 * (1 + 2 * np.exp(-y * 25))) / SR) * np.exp(-y * 3) + bp(rng.normal(0, 1, len(y)), 300, 4000) * np.exp(-y * 18) * 0.6
def whoosh(d=0.3): y = tt(d); return bp(rng.normal(0, 1, len(y)), 700, 7000) * np.sin(np.pi * y / d) ** 2
def click(): y = tt(0.04); return bp(rng.normal(0, 1, len(y)), 2500, 9000) * np.exp(-y * 150) + np.sin(2 * np.pi * 2000 * y) * np.exp(-y * 200) * 0.5
def ding(f=1760): y = tt(0.9); return (np.sin(2 * np.pi * f * y) + 0.4 * np.sin(2 * np.pi * f * 2.4 * y)) * np.exp(-y * 5)
def pop(): y = tt(0.1); return np.sin(2 * np.pi * np.cumsum(500 * (1 + 3 * np.exp(-y * 50))) / SR) * np.exp(-y * 35)
def riser(d): y = tt(d); return bp(rng.normal(0, 1, len(y)), 600, 9000) * (y / d) ** 2.4 + np.sin(2 * np.pi * np.cumsum(200 + 600 * (y / d) ** 2) / SR) * (y / d) ** 2 * 0.3
B = 0.5; start = {'a': 0.55, 'b': 0.0, 'c': 0.25}[AD]
for k in range(int((T - start) / (B / 2))):  # 120 BPM groove
    at = start + k * B / 2
    if k % 2 == 0: put(kick(), at, 0.8)
    if k % 4 == 2: put(clap(), at, 0.45)
    put(hat(k % 4 == 3), at + B / 4, 0.12, 0.3)
    if k % 2 == 0: put(lp(np.tanh(3 * np.sin(2 * np.pi * [55, 55, 49, 62][(k // 8) % 4] * tt(0.22))) * np.exp(-tt(0.22) * 6), 300), at, 0.35)
if AD == 'a':
    put(hit(), 0.25, 0.8); put(whoosh(0.35), 0.2, 0.6); put(hit(), 0.55, 0.6)
    for i in range(8): put(click(), 1.9 + i * 0.2, 0.5)
    put(riser(0.6), 3.4, 0.6); put(hit(), 4.0, 0.9); put(pop(), 4.3, 0.5)
if AD == 'b':
    for i in range(3): put(hit(), 0.05 + i * 0.18, 0.4 + 0.1 * i)
    for t0 in (1.8, 5.2, 8.6): put(whoosh(0.4), t0, 0.5); put(ding(1568 + (t0 > 5) * 200), t0 + 0.6, 0.25)
    put(riser(0.8), 11.2, 0.5); put(hit(), 12.0, 0.9); put(pop(), 12.5, 0.6)
if AD == 'c':
    put(hit(), 0.25, 1.0); put(lp(rng.normal(0, 1, int(0.8 * SR)), 120) * np.exp(-tt(0.8) * 4), 0.25, 0.8)
    put(whoosh(0.4), 2.2, 0.6); put(ding(2093), 2.6, 0.4); put(ding(2637), 2.65, 0.25)
    for s in range(4, 10): put(click(), 3.5 + (s - 4), 0.6)
    put(hit(), 7.0, 0.9); put(pop(), 7.4, 0.5)
mix /= np.max(np.abs(mix)); mix = np.tanh(mix * 1.4); mix /= np.max(np.abs(mix)) * 1.08
k = int(0.25 * SR); mix[-k:] *= np.linspace(1, 0, k)[:, None]
w = wave.open(sys.argv[1], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes()); w.close()
