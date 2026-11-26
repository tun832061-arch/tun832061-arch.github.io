import numpy as np, wave, sys
from scipy.signal import butter, sosfilt
SR = 48000; RAW = len(sys.argv) > 2 and sys.argv[2] == 'raw'
SEG = [["c2", 0.15, 2.75], ["c2", 3.15, 7.95], ["c3", 1.10, 7.40], ["c1", 0.35, 4.15], ["c1", 4.42, 6.60]]
def load(c): w = wave.open(f'{c}48.wav'); return np.frombuffer(w.readframes(w.getnframes()), '<i2').reshape(-1, 2).astype(float) / 32768
clips = {c: load(c) for c in ('c1', 'c2', 'c3')}
talk = sum(b - a for _, a, b in SEG); T = talk + 3.0; n = int(round(T * 30)) * SR // 30; out = np.zeros((n, 2)); voice = np.zeros((n, 2))
t = 0.0; xf = int(0.012 * SR); bounds = []
for c, a, b in SEG:
    seg = clips[c][int(a * SR): int(b * SR)].copy(); seg[:xf] *= np.linspace(0, 1, xf)[:, None]; seg[-xf:] *= np.linspace(1, 0, xf)[:, None]
    i = int(t * SR); voice[i:i + len(seg)] += seg[: n - i]; bounds.append(t); t += b - a
def tt(d): return np.arange(int(d * SR)) / SR
def lp(x, f): return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
def bp(x, a, b): return sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
rng = np.random.default_rng(9)
def put(s, at, g=1.0, pan=0.0):
    i = int(at * SR); m = min(len(s), n - i)
    if m > 0: out[i:i+m, 0] += s[:m] * g * (1 - max(0, pan)); out[i:i+m, 1] += s[:m] * g * (1 + min(0, pan))
if not RAW:
    # soft bed: warm plucked chords + light kick/hat under the voice
    prog = [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]]; B = 0.5
    def pluck(f, d): y = tt(d); return (np.sin(2*np.pi*f*y) + 0.3*np.sin(4*np.pi*f*y)*np.exp(-y*8)) * np.exp(-y*4)
    for k in range(int(talk / B)):
        at = k * B; ch = prog[(k // 4) % 4]
        put(pluck(440 * 2 ** ((ch[k % 3] + 12 - 69) / 12), 0.6), at, 0.05, 0.3 * ((k % 2) * 2 - 1))
        if k % 2 == 0: put((lambda y: np.sin(2*np.pi*np.cumsum(50 + 90*np.exp(-y*30))/SR) * np.exp(-y*9))(tt(0.3)), at, 0.12)
        put(bp(rng.normal(0, 1, int(0.05*SR)), 6000, 12000) * np.exp(-tt(0.05)*60), at + B/2, 0.04)
    whoosh = lambda d=0.3: bp(rng.normal(0, 1, int(d*SR)), 600, 7000) * np.sin(np.pi * tt(d) / d) ** 2
    pop = lambda: (lambda y: np.sin(2*np.pi*np.cumsum(600*(1 + 2*np.exp(-y*50)))/SR) * np.exp(-y*35))(tt(0.1))
    def m(c, x):
        acc = 0
        for cc, a, b in SEG:
            if cc == c and a <= x <= b: return acc + (x - a)
            acc += b - a
    for c, x in [("c2", 6.23), ("c2", 7.17), ("c3", 2.50), ("c3", 3.21), ("c1", 1.44), ("c1", 2.15)]: put(pop(), m(c, x), 0.25)
    for b0 in bounds[1:]: put(whoosh(0.2), b0 - 0.1, 0.12)
    put(whoosh(0.5), m("c3", 5.86) - 0.2, 0.35)
    y = tt(2.0); put(np.sin(2*np.pi*55*y) * np.exp(-y*2.5) + bp(rng.normal(0, 1, len(y)), 300, 3000)*np.exp(-y*12)*0.3, talk, 0.5)
    for f in (220, 277.2, 329.6): put(np.sin(2*np.pi*f*tt(3.0)) * np.minimum(1, tt(3.0)/0.3) * np.exp(-tt(3.0)*0.8), talk, 0.06)
mix = voice * 0.95 + out
mix /= np.max(np.abs(mix)) * 1.06
k = int(0.4 * SR); mix[-k:] *= np.linspace(1, 0, k)[:, None]
w = wave.open(sys.argv[1], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype('<i2').tobytes()); w.close()
print('audio', round(T, 2))
