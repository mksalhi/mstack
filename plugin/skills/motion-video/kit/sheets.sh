#!/usr/bin/env bash
# Review sheets for a rendered film. Look at every image this writes before showing the film to anyone.
#
#   ./sheets.sh out/final.mp4        contact.png, phone.png, loop_check.mp4
#   ./sheets.sh out/final.mp4 4.1    also strip.png: 12 consecutive frames starting at 4.1s
set -euo pipefail

video="$1"
dir="$(dirname "$video")"
seconds="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$video")"
rows() { awk -v s="$seconds" -v rate="$1" -v cols="$2" 'BEGIN { n = int(s * rate + 0.999); r = int((n + cols - 1) / cols); print (r < 1 ? 1 : r) }'; }

# Whole film at a glance: 2 frames per second, 6 across.
ffmpeg -y -loglevel error -i "$video" -vf "fps=2,scale=320:-2,tile=6x$(rows 2 6)" -frames:v 1 "$dir/contact.png"
# Phone test: one frame per second at 360 px wide. Anything unreadable here is unreadable in a feed.
ffmpeg -y -loglevel error -i "$video" -vf "fps=1,scale=360:-2,tile=5x$(rows 1 5)" -frames:v 1 "$dir/phone.png"
# Loop seam: the film twice, back to back.
ffmpeg -y -loglevel error -stream_loop 1 -i "$video" -c copy "$dir/loop_check.mp4"
# Fast action: consecutive frames, to catch pops, overlaps and one-frame glitches.
if [ "${2:-}" != "" ]; then
  ffmpeg -y -loglevel error -ss "$2" -i "$video" -vf "scale=320:-2,tile=12x1" -frames:v 1 "$dir/strip.png"
fi
echo "wrote $dir/contact.png $dir/phone.png $dir/loop_check.mp4${2:+ $dir/strip.png}"
