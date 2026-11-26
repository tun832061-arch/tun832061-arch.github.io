#!/usr/bin/env bash
# previews.sh — makes the short silent loops that play on the homepage cards.
#   ./previews.sh            (then: node build.mjs)
# One line per piece: slug, source video, start second, length. Vertical sources get a blurred fill.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p assets/video/preview
while read -r slug src start len; do
  [ -z "$slug" ] && continue
  [ -f "assets/video/$src" ] || continue
  out="assets/video/preview/$slug.mp4"
  w=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "assets/video/$src")
  if [ "${w%,*}" -lt "${w#*,}" ]; then
    vf="fps=30,split[a][b];[a]scale=960:-2,crop=960:600,boxblur=24:2,eq=brightness=-0.3[bg];[b]scale=-2:600[fg];[bg][fg]overlay=(W-w)/2:0"
  else
    vf="fps=30,scale=-2:600,crop=960:600"
  fi
  ffmpeg -nostdin -v error -y -ss "$start" -t "$len" -i "assets/video/$src" -an -filter_complex "$vf" \
    -c:v libx264 -preset slow -crf 26 -pix_fmt yuv420p -movflags +faststart "$out"
  echo "preview: $out"
done <<'LIST'
nova               nova.mp4               3.6  5
clown-club         clown-club.mp4         2.0  5
bez-and-the-boos   bez-and-the-boos.mp4   10.5 4.5
no-after-effects   no-after-effects.mp4   5.0  5
raise-trap         raise-trap.mp4         12   5
corvo              corvo-bumper.mp4       0.3  5.5
pulse              pulse-v2.mp4           3.0  5
make-it-move       make-it-move-v2.mp4    7.5  5
the-last-watch     the-last-watch.mp4     36   6
say-it-slower      say-it-slower.mp4      0    5
kettle-and-kiln    kettle-and-kiln.mp4    0    5
splitly            splitly.mp4            24.4 5
kicks-drop         kicks-drop.mp4         0    5
lagos-in-24-frames lagos-in-24-frames.mp4 4.0  5
kairo              kairo.mp4              6.0  5
bite               bite.mp4               3.0  5
LIST
