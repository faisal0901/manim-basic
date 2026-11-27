#!/usr/bin/env bash
# Render semua adegan (opsional: RENDER=1) lalu gabung jadi satu MP4.
set -e
cd "$(dirname "$0")"
F=prompt_caching_kalau_kamu_bikin
KELAS="S01Hook S02Kalau S03Tapi S04Zoom S05Cocok S06Terbatas S07Selamat S08HatiHati S09Sepi S10Tips"
if [ -n "$RENDER" ]; then
  for k in $KELAS; do ORIENT=vertical manim -qh $F.py $k; done
fi
: > daftar.txt
for k in $KELAS; do echo "file 'media/videos/$F/1920p60/$k.mp4'" >> daftar.txt; done
ffmpeg -y -f concat -safe 0 -i daftar.txt -c copy PROMPT_CACHING_A_kalau_kamu_bikin_v2_vertical.mp4
rm daftar.txt
