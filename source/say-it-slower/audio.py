import numpy as np, wave, sys, json
from scipy.signal import butter, sosfilt, fftconvolve
SR = 48000; T = 28.0; OFF = 0.5; n = int(SR * T); rng = np.random.default_rng(21); mus = np.zeros((n, 2))
WD = json.load(open(sys.argv[2])); B = lambda i: WD[i][1] + OFF
def tt(d): return np.arange(int(d * SR)) / SR
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
def put(s, at, g=1.0, pan=0.0):
    i = int(at * SR); m = min(len(s), n - i)
    if m <= 0 or i < 0: return
    mus[i:i+m, 0] += s[:m] * g * (1 - max(0, pan)); mus[i:i+m, 1] += s[:m] * g * (1 + min(0, pan))
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def thud(f=55, d=0.5): y = tt(d); return np.sin(2 * np.pi * np.cumsum(f * (1 + 2 * np.exp(-y * 25))) / SR) * np.exp(-y * 7)
def whoosh(d=0.25): y = tt(d); return bp(rng.normal(0, 1, len(y)), 600, 6000) * np.sin(np.pi * y / d) ** 2
def tick(f=3000): y = tt(0.03); return bp(rng.normal(0, 1, len(y)), f * 0.6, f * 1.6) * np.exp(-y * 180)
def click(): y = tt(0.05); return (np.sin(2 * np.pi * 1800 * y) * np.exp(-y * 120) + bp(rng.normal(0, 1, len(y)), 2000, 8000) * np.exp(-y * 200) * 0.5)
def pluck(f, d=0.5): y = tt(d); return (np.sin(2 * np.pi * f * y) + 0.4 * np.sin(4 * np.pi * f * y) * np.exp(-y * 10)) * np.exp(-y * 8)
def pad(fs, d, att=1.2, rel=1.5):
    y = tt(d); s = sum(np.sin(2 * np.pi * f * y + 0.4 * np.sin(2 * np.pi * 0.2 * y + f)) for f in fs) / len(fs)
    return lp(s, 1500) * np.minimum(1, y / att) * np.minimum(1, (d - y) / rel)
# --- 0–5.85: fast and busy
for k in range(int(5.85 / 0.107)):  # 140 bpm 16ths
    at = 0.25 + k * 0.107
    if at > 5.8: break
    put(tick(6000 if k % 2 else 4000), at, 0.35 if k % 4 == 0 else 0.18, 0.3 * ((k % 2) * 2 - 1))
    if k % 4 == 0: put(thud(60, 0.25), at, 0.35)
for i in range(4): put(whoosh(0.18), B(i) - 0.12, 0.6, [-0.6, 0.6, 0, 0][i]); put(thud(50 if i == 3 else 70), B(i), 0.9 if i == 3 else 0.5)
for i in (4, 6, 8): put(whoosh(0.15), B(i) - 0.1, 0.4); put(click(), B(i), 0.4)
y = tt(1.1); rs = bp(rng.normal(0, 1, len(y)), 800, 9000) * (y / 1.1) ** 2.5; put(rs, 4.76 + OFF - 0.05, 0.6)  # flood riser, hard stop
for k in range(40): at = 4.76 + OFF + 1.05 * (1 - (1 - k / 40) ** 0.5);  put(tick(5000), at, 0.25)
# --- calm from "took time"
put(pad([mtof(m) for m in (45, 52, 57, 60, 64)], T - (7.4 + OFF), 2.5, 2.0), 7.4 + OFF, 0.55)
put(thud(42, 1.5), B(17), 0.35)
for k in range(30): put(tick(2500), 8.68 + OFF + k / 24, 0.18)                 # projector clatter on the film grid
put(whoosh(0.6), B(21), 0.5); put(thud(48, 0.8), 9.95 + OFF, 0.6)
for k in range(26): put(tick(1800), B(25) + k * (11.8 - WD[25][1]) / 26, 0.15)  # playhead through one second
for k in range(24): put(tick(3500), 12.63 + OFF + k * (WD[28][1] + 0.35 - 12.63) / 24, 0.22)   # timecode counting
put(thud(45, 1.2), B(28) + 0.35, 0.6); put(pluck(mtof(84), 1.2), B(28) + 0.35, 0.15)
for i in (34, 36, 37, 38, 40, 41, 42): put(click(), B(i), 0.25)
put(whoosh(0.7), B(42), 0.8)
y = tt(1.2); f = np.linspace(220, 70, len(y)); put(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-y * 2) * 0.25, B(46), 0.6)  # "slow": tape-stop
put(click(), B(51) + 0.35, 0.7); put(thud(70, 0.3), B(51) + 0.35, 0.3)
for nn, m in enumerate([72, 76, 79, 84]): put(pluck(mtof(m)), B(56) + nn * 0.07, 0.3, (nn - 1.5) * 0.3)
put(thud(40, 2.0), 24.4 + OFF, 0.8)
for m in (57, 64, 69, 72, 76): put(pluck(mtof(m), 3.0) * 0.6, 24.4 + OFF, 0.25)
# --- reverb on the music bed, then the voice on top
ir = rng.normal(0, 1, (int(1.4 * SR), 2)) * np.exp(-tt(1.4) * 4)[:, None]
wet = np.stack([fftconvolve(mus[:, c], lp(ir[:, c], 6000))[:n] for c in (0, 1)], 1)
mus = mus / np.max(np.abs(mus)) + 0.15 * wet / np.max(np.abs(wet)); mus = np.tanh(mus) * 0.33
vo = wave.open(sys.argv[3]); v = np.frombuffer(vo.readframes(vo.getnframes()), '<i2').astype(float) / 32768
voice = np.zeros(n); i0 = int(OFF * SR); voice[i0:i0 + len(v)] = v[: n - i0]
vwet = fftconvolve(voice, lp(rng.normal(0, 1, int(0.5 * SR)) * np.exp(-tt(0.5) * 12), 5000))[:n]; voice = voice + 0.04 * vwet / np.max(np.abs(vwet))
out = mus + voice[:, None] * 0.9; out = np.tanh(out * 1.1); out /= np.max(np.abs(out)) * 1.08
k = int(0.5 * SR); fade = np.ones(n); fade[-k:] = np.linspace(1, 0, k); out *= fade[:, None]
w = wave.open(sys.argv[1], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype('<i2').tobytes()); w.close()
