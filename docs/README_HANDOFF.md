# ngajar: handoff ke laptop

Update terakhir: 26 Nov 2026. Semua yang sudah dikerjakan di cloud ada di folder ini, jadi kamu bisa lanjut di laptop tanpa buka session lama.

## Proyek ini apa
Seri video animasi pendek (Manim) tentang AI dan tech, bahasa Indonesia, untuk TikTok, Reels, dan Shorts (9:16). Versi 16:9 untuk YouTube menyusul.
Audiens: semua orang yang tertarik perkembangan AI, termasuk pengguna AI biasa, bukan cuma calon AI engineer.
Sudut seri: efisiensi, misalnya "kirim dokumen besar ke AI itu boros token".

## Status sekarang
| Bagian | Status |
|---|---|
| Design system KAPUR (warna, font, helper Manim) | Selesai, palet disetujui |
| Video RAG v2, naskah A "Kalau kamu yang bikin..." (~64 dtk) | Video 9:16 jadi, siap direvisi detail |
| Video RAG v2, naskah B hook biasa (~61 dtk) | Video 9:16 jadi, siap direvisi detail |
| Versi 16:9 v2 | Belum dibuat/dicek |
| Suara narasi, musik, subtitle | Belum ada |
| Upload dan uji A/B | Belum |
| Video RAG v1 dan RAG KAPUR | Arsip. Hook-nya (karyawan + dokumen) dinilai salah, jangan dipakai |

## Peta folder
```
handoff/
├── CLAUDE.md             konteks proyek untuk Claude Code (buka Claude Code dari folder ini)
├── README_HANDOFF.md      <- kamu di sini
├── SETUP_LOKAL.md         pasang Manim, render cepat, tips revisi
├── KEPUTUSAN.md           semua keputusan + yang masih tebakan
├── BRIEF_KONTEN.md        audiens, seri, dua gaya naskah, aturan hook, ringkasan riset
├── TEMPLATE_NASKAH.md     template per adegan untuk video baru
├── BACKLOG.md             langkah berikutnya, berurutan
└── proyek/                <- folder kerja, jalankan Manim dari sini
    ├── design-system/     theme.py (KAPUR), palet.py, rag_kapur.py, fonts/, requirements.txt, README.md
    ├── video-rag-v2/      rag_dua_versi.py (A dan B), naskah_A, naskah_B, video A/B, ringkasan preview
    └── video-rag/         arsip v1: rag_video.py dan naskah lama (referensi saja)
```
Penting: `video-rag-v2/rag_dua_versi.py` mengimpor `theme.py` dari `../design-system`. Jangan pisahkan dua folder itu; biarkan bersebelahan.

## Mulai cepat (5 menit setelah setup)
```bash
cd handoff/proyek
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r design-system/requirements.txt

cd video-rag-v2
# cek cepat: semua frame kunci jadi PNG di preview/vertical/ (tanpa video)
STILLS=1 ORIENT=vertical manim -s -ql rag_dua_versi.py RAGKalauKamuBikin
# video final 1080x1920
ORIENT=vertical manim -qh rag_dua_versi.py RAGKalauKamuBikin RAGHook
```
Kalau PNG hasilnya sama dengan `video-rag-v2/preview/ringkasan_A.png`, setup kamu benar. Detail per OS dan cara Windows ada di [SETUP_LOKAL.md](SETUP_LOKAL.md).

## Link
- Dokumen riset kreator short-form: https://claude.ai/artifact/ApHDWzSaELB7NDAnUm7ux4 (ringkasannya ada di BRIEF_KONTEN.md)
