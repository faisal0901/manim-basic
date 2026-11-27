# CLAUDE.md: ngajar

Seri video animasi pendek (Manim) tentang AI dan tech untuk TikTok, Reels, Shorts (9:16 utama, 16:9 untuk YouTube). Audiens: semua yang tertarik AI, termasuk pengguna biasa. Sudut seri: efisiensi ("kirim dokumen besar ke AI itu boros token").

Jalankan Claude Code dari root repo ini. Dokumen rujukan ada di `docs/`, baca sesuai kebutuhan, jangan salin isinya ke sini:
- `README.md` (root): struktur repo, setup, perintah render
- `docs/README_HANDOFF.md`: status per 26 Nov 2026
- `docs/SETUP_LOKAL.md`: instalasi, perintah render, tips revisi cepat
- `docs/KEPUTUSAN.md`: keputusan final, tebakan, hal terbuka. **Perbarui file ini setiap ada keputusan baru.**
- `docs/BRIEF_KONTEN.md`: audiens, seri, dua gaya naskah, aturan hook, metrik uji
- `docs/TEMPLATE_NASKAH.md`: template naskah per adegan
- `docs/BACKLOG.md`: urutan kerja berikutnya
- `design-system/README.md`: detail design system KAPUR

## Cara ngobrol
- Bahasa Indonesia santai ("gw/kamu" boleh). Jawaban singkat, langsung ke hasil.
- Sebelum naskah video baru, tanya dulu mau gaya A atau B.

## Peta kode
```
design-system/   theme.py (token + helper + KapurScene), palet.py, rag_kapur.py (arsip), fonts/
videos/
├── 01-rag/                rag_v4.py: RAGKalauKamuBikinV4 (final)
├── 02-tokenizer/          token_hook.py: TokenHook
├── 03-embedding/          embedding_kalau_kamu_bikin.py: EmbeddingKalauKamuBikin
├── caveman-hemat-token/   caveman_hook.py: CavemanHook
├── 06-temperature/        temperature_kalau_kamu_bikin.py: TemperatureKalauKamuBikin
└── makasih-ke-chatgpt/    sopan_hook.py: SopanHook
arsip/           rag-v1, rag-v2, rag-v3: jangan dikembangkan
logo/            logo_kapur.py, logo_a_poles.py (Pillow, bukan Manim)
```
File video mencari `design-system/` di folder induk terdekat (`_DS = next(p / "design-system" for p in _DIR.parents ...)`), jadi kedalaman folder bebas selama masih di dalam repo ini. Video baru: salin blok impor itu.

## Render (dari dalam folder video)
```bash
STILLS=1 ORIENT=vertical manim -s -ql token_hook.py TokenHook    # PNG frame kunci, cepat -> preview/vertical/
ORIENT=vertical manim -ql -n 12,18 token_hook.py TokenHook       # sebagian animasi saja
ORIENT=vertical manim -qh token_hook.py TokenHook                # final 1080x1920
ORIENT=horizontal manim -qh ...                                    # 16:9
```
Saat revisi: cek lewat PNG dulu, `-qh` hanya sekali di akhir. Jangan pakai `--disable_caching`. Windows: `$env:ORIENT="vertical"; $env:STILLS="1"`.

## Aturan design system KAPUR
- Latar selalu hitam penuh `#000000`.
- Warna = peran, selalu lewat token dari `theme.py`, jangan tulis hex langsung:
  `LANGIT` manusia/input/pertanyaan · `TOSKA` AI/model · `KUNYIT` fokus, **maks. 1 hal kuning per layar** · `DAUN` solusi/benar/hemat · `SAGA` masalah/salah/mahal · `JINGGA` angka & satuan. Isian kartu pakai `redup(warna)`.
- Font: `judul()` Source Serif 4, `teks()`/`caption()` Inter, `mono()` JetBrains Mono (angka, vektor, label bab).
- **Tanpa LaTeX**: jangan pakai `MathTex`, `Tex`, `Integer`, `DecimalNumber`. Pakai `Text` lewat helper.
- Posisi pakai `pos(x, y)`, jarak pakai `SP[...]`, ukuran pakai `TIPE`. Hormati zona aman `AMAN` (9:16: bawah 3.4 unit untuk caption dan tombol app).
- Tempo lewat konstanta (`KETUK`, `CEPAT`, `LAMBAT`, `JEDA`, `JEDA_PANJANG`), bukan angka lepas. Satu ide per ketukan.
- Kelas video turunan `KapurScene` (atau `RAGBase`), mulai bagian dengan `self.header(...)`, tandai frame kunci dengan `self.mark("NN_nama")`.

## Aturan naskah
- Satu video, satu ide, satu open loop. 60-75 detik, 150-190 kata.
- Detik pertama harus paham dari visual saja, tanpa suara.
- Jangan buka dengan konteks korporat (karyawan, ratusan dokumen). Buka dari pengalaman penonton.
- Jelaskan istilah (chunk, vektor, token, embedding) dengan kata biasa **sebelum** namanya dipakai.
- Satu analogi per video, sebut batasnya.
- Gaya A "Kalau kamu yang bikin...": rantai "tapi... jadi...", tutup "Selamat, kamu baru aja bikin X" + teaser.
- Gaya B hook biasa: masalah / klaim kontra-intuitif / angka, lalu langkah, sebelum vs sesudah, tips, teaser.
- Angka contoh fiktif harus ditandai fiktif.

## Penamaan file
- Folder per video: `videos/<nn>-<topik>/` (mis. `videos/04-agent/`).
- Kode: `<topik>_<deskripsi>.py`; kelas PascalCase (`TokenKalauKamuBikin`, `TokenHook`).
- Naskah: `naskah_A_kalau_kamu_bikin.md`, `naskah_B_hook.md`.
- Frame kunci: `self.mark("01_hook")`, nomor dua digit + nama beat; PNG berawalan `A_`/`B_` di `preview/<orientasi>/`.
- Video final: `<TOPIK>_<A|B>_<gaya>_<vertical|horizontal>.mp4` (mis. `RAG_B_hook_vertical.mp4`).

## Jangan diubah tanpa tanya
- Palet warna dan peran warna (sudah disetujui).
- Latar hitam `#000000`.
- Nilai di `theme.py` yang dipakai semua video (font, `TIPE`, `AMAN`, tempo dasar). Untuk satu video, override di file video saja, seperti `JEDA` di `arsip/rag-v2/rag_dua_versi.py`.
- Isi naskah yang sudah ada: usulkan perubahan dulu.
- Jangan hapus folder `arsip/`.
- Jangan commit PNG, MP4, ZIP (sudah di `.gitignore`).

## Masih tebakan (konfirmasi sebelum dijadikan permanen)
Nama "KAPUR", pilihan font, belum ada logo/nama channel, layout 16:9 v2. Detail di `KEPUTUSAN.md`.
