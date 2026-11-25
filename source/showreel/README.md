# Showreel — source

Collage intro → one piece at a time (each enters over the last) → grid → end card. 32 s, 120 BPM.
`reel.html` draws frames from JPEG sequences cut from the finished videos (frames/<clip>_<mode>/f00001.jpg; the
clips and source times are listed in `CL` at the top). `music2.py` makes the beat; `render.cjs` renders and encodes.
