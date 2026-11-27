# channel/: Paycheck Math video engine

Faceless finance explainers made entirely in code: the script becomes an AI voice, the scenes are drawn frame by frame on a canvas, and ffmpeg encodes the MP4. Captions are burned in and also exported as `.srt`.

```
engine/tts.py        script.json -> build/vo.wav + build/timeline.json   (Kokoro TTS, offline)
engine/mix.py        original synthesised music bed, ducked under the voice -> build/mix.wav
engine/player.html   scene renderer (hook, bigtext, title, section, chips, calendar, stat, paychecks,
                     ledger, equation, stack, waterfall, compare, steps, end); 16:9 or 9:16
engine/render.cjs    -> build/video.mp4 + video.srt   (--stills 3,40 for check frames; --size 1080x1920 for Shorts)
engine/thumb.*       thumbnails, 1280x720
products/make_planner.py   builds "Paycheck Planner.xlsx", the product the videos sell
```

## Make a new episode
1. `mkdir epNN && cp ep02/script.json epNN/` and rewrite it. Each line has `say` (spoken text, numbers written as words) and optionally `cap` (the caption, with digits) and `scene` (starts a new visual). `join: true` shortens the pause before a line. Scene fields: see the scene functions (`D.<type>`) in `player.html` and the two episodes.
2. ```
   cd engine
   python3 tts.py ../epNN && python3 mix.py ../epNN
   node render.cjs ../epNN --stills 5,30,60      # check frames
   node render.cjs ../epNN                       # full video, about 1 min per minute of video
   ```
3. Add a thumbnail function to `thumb.html` (see `draw2`) and run `node thumb.cjs ../epNN`.

## Setup on a new machine
`pip install kokoro-onnx soundfile scipy numpy`, Node with Playwright and Chromium, and ffmpeg.
Model files go in `KOKORO_DIR` (default `/home/user/tts`). Get them from github.com/thewh1teagle/kokoro-onnx/releases (tag `model-files-v1.0`): `kokoro-v1.0.onnx` and `voices-v1.0.bin`.
Fonts: Anton and Inter from `../assets/fonts` (both OFL).
