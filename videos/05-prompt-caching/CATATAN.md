# Catatan video prompt caching v1 (gaya A, zoom server 3D)

- File: `PROMPT_CACHING_A_kalau_kamu_bikin_vertical.mp4`, 1080x1920, 60 fps, tanpa suara, sekitar 85 detik (render v1).
- Kode: `videos/05-prompt-caching/` (salinan di folder `kode/`):
  - `prompt_caching_kalau_kamu_bikin.py`: 10 adegan, satu kelas per adegan (S01Hook … S10Tips). 2D pakai `KapurScene`, 3D (S04Zoom, S05Cocok) pakai `ThreeDScene` + overlay teks 2D yang tetap di layar.
  - `caching_zoom_3d.py`, `caching_server_3d.py`: komponen 3D (kubus kapur, rak, server, GPU, memori).
  - `gabung.sh`: render semua (`RENDER=1 ./gabung.sh`) lalu gabung jadi satu MP4 dengan ffmpeg.
  - Frame kunci: `STILLS=1 ORIENT=vertical manim -s -ql prompt_caching_kalau_kamu_bikin.py S04Zoom` → `preview/vertical/A_*.png`.
- Revisi satu adegan: render ulang kelas itu saja, lalu `./gabung.sh` (tanpa RENDER) buat gabung ulang.
- Naskah: `naskah_A_kalau_kamu_bikin.md` (tabel visual + fakta + sumber), `naskah_narasi_rekam.md` (baca suara). Naskah B cadangan: `naskah_B_hook.md`, `naskah_narasi_rekam_B.md`.

## Default yang gw pilih (gampang diubah)
- Kasus bot CS "Toko Gadget Jaya" (fiktif), aturan toko 5 baris contoh.
- Zoom 3D dibuat "potong-zoom": kamera maju ke objek yang disorot kuning, memudar, lalu adegan berikutnya muncul dari jauh. Bukan satu dunia nyambung, biar render ringan.
- CPU digambar sebagai manajer (nerima pesan, cocokin sidik blok), GPU tukang hitung. Memori GPU digambar sebagai tumpukan chip HBM.

## Angka
- Angka contoh: 3.000 token, pembeli ke-100, jam 13:31:05, kedatangan pembeli menit 0/8/19, isi blok "0.12 -0.87 …", laporan "cache write 3.000".
- Angka salah satu penyedia (dokumentasi Anthropic, dicek 27 Nov 2026): baca cache 0,1× harga input, nulis cache 1,25× (masa berlaku 5 menit), masa berlaku default 5 menit dan diperpanjang tiap dipakai. Di layar ditulis "salah satu penyedia".

## Batas analogi & akurasi
- Kubus/blok = gambaran. Aslinya angka Key/Value per token per lapisan model, tersebar ke beberapa GPU.
- 1 blok di gambar = sekumpulan token (vLLM default 16), bukan satu kata.
- Cara kerja server mengikuti sistem terbuka (vLLM, SGLang). Detail internal penyedia besar tidak semuanya publik.
- "Beda satu kata di depan, semua setelahnya dihitung ulang": blok sebelum titik beda kadang masih kepakai, tergantung sistem.
- Rugi 1,25× cuma di penyedia yang mengenakan biaya nulis cache. Di OpenAI model lama, nulis cache gratis.
- Prompt di bawah batas minimal (512-4.096 token tergantung model) tidak di-cache sama sekali; tidak disebut di video.

## Tebakan / perlu dicek
- Durasi render 85 detik, di atas target 75 dan naskah ±78. Setelah rekam suara, sesuaikan `self.wait(...)` per adegan; adegan zoom (S04, 14 dtk) dan toko sepi (S09) paling gampang dipangkas.
- Teks kecil (caption 25, mikro 19) di adegan 3D bisa kekecilan di HP.
