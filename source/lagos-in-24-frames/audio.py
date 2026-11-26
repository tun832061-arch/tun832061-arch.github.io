import numpy as np, wave, sys
from scipy.signal import butter, sosfilt, fftconvolve
SR = 48000; T = 20.0; n = int(SR * T); rng = np.random.default_rng(24); drums = np.zeros((n, 2)); fx = np.zeros((n, 2))
def tt(d): return np.arange(int(d * SR)) / SR
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x, axis=0)
def hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x, axis=0)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x, axis=0)
def put(buf, s, at, g=1.0, pan=0.0):
    i = int(at * SR); m = min(len(s), n - i)
    if m <= 0 or i < 0: return
    buf[i:i+m, 0] += s[:m] * g * (1 - max(0, pan)); buf[i:i+m, 1] += s[:m] * g * (1 + min(0, pan))
kick = lambda: (lambda y: np.sin(2 * np.pi * np.cumsum(48 + 110 * np.exp(-y * 32)) / SR) * np.exp(-y * 9))(tt(0.4))
rim = lambda: (lambda y: (np.sin(2 * np.pi * 1650 * y) * 0.6 + bp(rng.normal(0, 1, len(y)), 1500, 6000)) * np.exp(-y * 70))(tt(0.08))
shk = lambda: (lambda y: hp(rng.normal(0, 1, len(y)), 6500) * np.exp(-y * 55))(tt(0.07))
def bell(f): y = tt(0.35); return (np.sin(2 * np.pi * f * y) + 0.5 * np.sin(2 * np.pi * f * 2.76 * y)) * np.exp(-y * 14)
def tdrum(f0, f1, d=0.28): y = tt(d); f = np.geomspace(f0, f1, len(y)); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-y * 9) * np.minimum(1, y / 0.003)
S = 0.125  # sixteenth at 120 BPM
for bar in range(int(T / 2) + 1):
    b0 = bar * 2.0
    for st in range(16):
        at = b0 + st * S
        if at >= T: break
        if st in (0, 7, 10): put(drums, kick(), at, 0.9)
        if st in (4, 12): put(drums, rim(), at, 0.5, 0.15)
        put(drums, shk(), at, 0.22 if st % 4 == 2 else 0.11, -0.35)
        if st in (0, 6, 8, 14): put(drums, bell(920 if st in (0, 8) else 690), at, 0.16, 0.4)
        if st in (3, 11): put(drums, tdrum(180, 320), at, 0.45, -0.2)
        if st == 14 and bar % 2: put(drums, tdrum(300, 150, 0.35), at, 0.4, -0.2)
# the loop drops back while the sun sets: heavy low-pass from 12 s, opens again at 17 s
env = np.ones(n); y = np.arange(n) / SR
muf = (y >= 12.0) & (y < 17.0)
dl = lp(drums, 350); drums = np.where(muf[:, None], dl * 1.6, drums)
drums[(y >= 12.0) & (y < 12.02)] *= 0
# generator hum + traffic
hum = (np.sin(2 * np.pi * 50 * y) + 0.5 * np.sin(2 * np.pi * 100 * y) + 0.25 * np.sign(np.sin(2 * np.pi * 150 * y)) * 0.3) * 0.12
humenv = np.interp(y, [0, 1, 5, 5.2, 12, 13, 16.5, 17.2, 20], [0, 0.6, 0.6, 0.2, 0.2, 1, 1, 0.1, 0])
fx[:, 0] += lp(hum * humenv, 800); fx[:, 1] += lp(hum * humenv, 800)
def horn(d=0.35): yy = tt(d); return lp(np.sign(np.sin(2 * np.pi * 415 * yy)) * 0.5 + np.sign(np.sin(2 * np.pi * 523 * yy)) * 0.5, 2500) * np.minimum(1, yy / 0.01) * np.minimum(1, (d - yy) / 0.05)
put(fx, horn(), 5.0, 0.22, 0.3); put(fx, horn(0.18), 8.5, 0.15, -0.3); put(fx, horn(0.25), 11.5, 0.25)
for i in range(10): put(fx, bp(rng.normal(0, 1, int(0.12 * SR)), 800, 7000) * np.exp(-tt(0.12) * 30), i * 0.5, 0.15)   # morph swishes
traffic = lp(rng.normal(0, 1, n), 500) * np.interp(y, [0, 12, 13, 16.5, 17, 20], [0, 0, 0.5, 0.5, 0, 0]) * 0.25
fx[:, 0] += traffic; fx[:, 1] += np.roll(traffic, 700)
# end hit
yy = tt(2.5); put(fx, np.sin(2 * np.pi * np.cumsum(40 * (1 + np.exp(-yy * 20))) / SR) * np.exp(-yy * 2.5), 18.5, 0.9)
mix = drums / np.max(np.abs(drums)) * 0.8 + fx
ir = rng.normal(0, 1, (int(0.9 * SR), 2)) * np.exp(-tt(0.9) * 6)[:, None]
wet = np.stack([fftconvolve(mix[:, c], lp(ir[:, c], 6000))[:n] for c in (0, 1)], 1)
out = mix / np.max(np.abs(mix)) + 0.1 * wet / np.max(np.abs(wet)); out = np.tanh(out * 1.3); out /= np.max(np.abs(out)) * 1.08
k = int(0.6 * SR); out[-k:] *= np.linspace(1, 0, k)[:, None]
w = wave.open(sys.argv[1], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype('<i2').tobytes()); w.close()
