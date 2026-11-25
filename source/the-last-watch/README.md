# The Last Watch — source

The film is drawn in code. `lw.html` draws any frame with `render(frame)`, `audio.py` makes the score and sound
design, and `render.cjs` renders all 1,500 frames and encodes them with the audio.

    python3 audio.py lw.wav                    # needs numpy + scipy
    node render.cjs the-last-watch.mp4 lw.wav  # needs Playwright (Chromium) + ffmpeg

Fonts: Cormorant Garamond and Cormorant SC (SIL Open Font License).
