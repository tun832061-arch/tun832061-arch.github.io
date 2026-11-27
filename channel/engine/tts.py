# tts.py — voices an episode script with Kokoro (offline, Apache-2.0 model) and writes the timing the renderer uses.
#   python3 tts.py ../ep01            -> ep01/build/vo.wav + ep01/build/timeline.json
# Model files: kokoro-v1.0.onnx and voices-v1.0.bin (github.com/thewh1teagle/kokoro-onnx releases), path in KOKORO_DIR.
import json, os, sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

ep = sys.argv[1]; S = json.load(open(os.path.join(ep, "script.json")))
out = os.path.join(ep, "build"); os.makedirs(out, exist_ok=True)
kd = os.environ.get("KOKORO_DIR", "/home/user/tts")
k = Kokoro(os.path.join(kd, "kokoro-v1.0.onnx"), os.path.join(kd, "voices-v1.0.bin"))
SR = 24000; LEAD = 0.6; TAIL = 1.6

def trim(x, th=0.006):
    idx = np.where(np.abs(x) > th)[0]
    if not len(idx): return x
    a = max(0, idx[0] - int(0.02 * SR)); b = min(len(x), idx[-1] + int(0.06 * SR))
    return x[a:b]

chunks, tl, t = [], [], LEAD
chunks.append(np.zeros(int(LEAD * SR)))
lines = S["lines"]
for i, L in enumerate(lines):
    a, _ = k.create(L["say"], voice=S.get("voice", "af_heart"), speed=S.get("speed", 1.0), lang="en-us")
    a = trim(np.asarray(a, dtype=np.float32)); d = len(a) / SR
    tl.append({"start": round(t, 3), "end": round(t + d, 3)})
    chunks.append(a); t += d
    if i + 1 < len(lines):
        nx = lines[i + 1]
        gap = 0.16 if nx.get("join") else 0.42
        if nx.get("scene", {}).get("type") in ("section", "title", "end"): gap += 0.35
        if L.get("scene", {}).get("type") == "section" or (L.get("scene") is None and False): pass
        chunks.append(np.zeros(int(gap * SR))); t += gap
    print(f"{i:02d} {d:5.2f}s  {L['say'][:60]}", flush=True)
chunks.append(np.zeros(int(TAIL * SR))); t += TAIL
vo = np.concatenate(chunks)
sf.write(os.path.join(out, "vo.wav"), vo, SR)
json.dump({"dur": round(len(vo) / SR, 3), "lines": tl}, open(os.path.join(out, "timeline.json"), "w"))
print("duration", round(len(vo) / SR, 1), "s")
