# Backlog (berurutan)

## Sekarang
1. **Setup laptop.** Ikuti SETUP_LOKAL.md, render frame kunci A, bandingkan dengan `video-rag-v2/preview/ringkasan_A.png`.
2. **Revisi detail video A dan B** di `proyek/video-rag-v2/rag_dua_versi.py`. Cek lewat PNG (`STILLS=1 -s -ql`), render `-qh` di akhir.
3. **Samakan teaser part 2** di A ("#2 Tokenizer") dan B ("Part 2: kenapa token bikin AI mahal?").
4. **Rekam suara** naskah A dan B. Ukur durasi tiap beat, lalu sesuaikan `JEDA`/`self.wait()` supaya animasi ikut suara. Gabung audio di editor (CapCut/DaVinci) atau pakai `self.add_sound("narasi.wav")` di Manim.
5. **Subtitle kata kunci + musik latar pelan** (opsional), lalu ekspor final 9:16.

## Uji
6. **Upload A dan B**, beri jarak, caption dan hashtag setara, jam posting serupa. Ubah hanya gaya naskah.
7. **Catat metrik** di 24-72 jam dan 3-7 hari: % tidak menggeser, retensi detik awal, titik anjlok, rata-rata durasi tonton, share/sends, save, % non-follower (tabel di BRIEF_KONTEN.md).
8. **Putuskan porsi gaya** A vs B untuk video berikutnya. Catat hasil di KEPUTUSAN.md.

## Berikutnya
9. **Versi 16:9 v2** untuk YouTube: render `ORIENT=horizontal -s -ql`, cek layout tiap frame, pakai pola dua kolom seperti `rag_kapur.py` (`H = not VERTIKAL`).
10. **Naskah #2 token/tokenizer** pakai TEMPLATE_NASKAH.md (sambil menunggu hasil uji). Pertanyaan inti: "kenapa jawaban panjang lebih mahal?" Analogi "potongan kata" + batasnya. Cek angka token ke dokumentasi resmi.
11. **Coding video token** di folder baru `proyek/video-token/`, salin pola import dari `rag_dua_versi.py` (`sys.path` ke `../design-system`).
12. **Konfirmasi tebakan:** nama KAPUR, font, logo/nama channel di layar, nama dan penomoran seri.
13. **Template cover** seragam: nomor part + satu kata topik.
14. **Naskah seri lanjutan:** embedding, chunking, caching/model kecil vs besar, AI engineer itu ngapain.

## Rapi-rapi
15. Taruh folder `proyek/` di Git (GitHub) supaya ada riwayat revisi. Tambahkan `.gitignore` berisi `media/`, `.venv/`, `__pycache__/`.
16. Jadwal posting yang bisa dipertahankan, misalnya 2 video per minggu.
