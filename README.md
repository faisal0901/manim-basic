# manim-basic · ngajar

Source code seri video animasi pendek (Manim) tentang AI dan tech, bahasa Indonesia,
untuk TikTok, Reels, dan Shorts (9:16). Semua video memakai design system **KAPUR**
(latar hitam, gaya terinspirasi 3Blue1Brown).

Repo ini hanya berisi kode dan naskah. Video (`.mp4`) dan gambar (`.png`) tidak di-commit;
render ulang dari kode.

## Struktur

```
.
├── design-system/          dipakai semua video
│   ├── theme.py            token warna, font, ukuran, tempo, helper, KapurScene
│   ├── palet.py            scene referensi palet (PaletKapur)
│   ├── rag_kapur.py        contoh pertama pakai KAPUR (RAGKapur, arsip)
│   ├── fonts/              Source Serif 4, Inter, JetBrains Mono (.ttf)
│   └── README.md           aturan design system
├── videos/
│   ├── 01-rag/                 RAG "Kalau kamu yang bikin… #1" (final v4)
│   ├── 02-tokenizer/           Tokenizer, hook "strawberry"
│   ├── 03-embedding/           Embedding "Kalau kamu yang bikin… #3"
│   ├── caveman-hemat-token/    "Caveman hemat token? Iya, tapi…"
│   └── makasih-ke-chatgpt/     Bilang makasih ke ChatGPT itu boros?
├── arsip/                  versi RAG lama (v1, v2, v3), referensi saja
├── logo/                   generator logo foto profil (Pillow)
├── docs/                   keputusan, brief konten, template naskah, setup lokal
├── CLAUDE.md               konteks proyek untuk Claude Code
└── requirements.txt
```

Tiap folder video berisi script `.py`, naskah per adegan (`naskah_*.md`), naskah rekam suara
(`naskah_narasi_rekam.md`), dan `CATATAN.md` (fakta, sumber, tebakan) bila ada.

| Folder | Script | Kelas scene |
|---|---|---|
| `videos/01-rag` | `rag_v4.py` | `RAGKalauKamuBikinV4` |
| `videos/02-tokenizer` | `token_hook.py` | `TokenHook` |
| `videos/03-embedding` | `embedding_kalau_kamu_bikin.py` | `EmbeddingKalauKamuBikin` |
| `videos/caveman-hemat-token` | `caveman_hook.py` | `CavemanHook` |
| `videos/makasih-ke-chatgpt` | `sopan_hook.py` | `SopanHook` |
| `arsip/rag-v1` | `rag_video.py` | `RAGVideo` (tanpa KAPUR) |
| `arsip/rag-v2` | `rag_dua_versi.py` | `RAGKalauKamuBikin`, `RAGHook` |
| `arsip/rag-v3` | `rag_v3.py` | `RAGKalauKamuBikinV3` |

## Setup

Butuh Python 3.10+ dan FFmpeg. LaTeX **tidak** perlu (semua teks pakai `Text`).

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Linux: pasang dulu `libpango1.0-dev pkg-config` (dan `libcairo2-dev`) sebelum `pip install`,
supaya `manimpango` bisa dibangun. Detail per OS ada di [docs/SETUP_LOKAL.md](docs/SETUP_LOKAL.md).

## Render

Jalankan dari dalam folder video. Orientasi diatur lewat env `ORIENT` (`vertical` 9:16 atau `horizontal` 16:9).

```bash
cd videos/02-tokenizer

# cepat: semua frame kunci jadi PNG di preview/vertical/ (tanpa video)
STILLS=1 ORIENT=vertical manim -s -ql token_hook.py TokenHook

# sebagian animasi saja (animasi ke-12 s.d. 18)
ORIENT=vertical manim -ql -n 12,18 token_hook.py TokenHook

# final 1080x1920
ORIENT=vertical manim -qh token_hook.py TokenHook
```

Windows PowerShell: `$env:ORIENT="vertical"; $env:STILLS="1"; manim -s -ql token_hook.py TokenHook`.

Hasil video masuk ke `media/videos/...` di folder itu. `media/` dan `preview/` diabaikan git.

Logo (Pillow, bukan Manim): `cd logo && python logo_kapur.py` atau `python logo_a_poles.py`.
PNG hasilnya ditulis di folder `logo/`.

## Cara impor design system

Script video tidak perlu dipasang sebagai paket. Di awal tiap script:

```python
_DIR = Path(__file__).resolve().parent
_DS = next(p / "design-system" for p in _DIR.parents if (p / "design-system").is_dir())
sys.path.insert(0, str(_DS))
from theme import *
```

Jadi folder video boleh di kedalaman mana pun selama masih di dalam repo. Video baru cukup
menyalin blok ini, lalu membuat kelas turunan `KapurScene`.

## Font

Font `.ttf` di `design-system/fonts/` (total ±2,2 MB) **ikut di-commit karena kode membutuhkannya**:
`theme.py` mendaftarkan semua `.ttf` di folder itu lewat `manimpango.register_font`, dan
`logo/logo_kapur.py` memuatnya lewat Pillow. Tanpa font ini teks akan jatuh ke font sistem
dan tampilannya berbeda. Ketiganya font Google dengan lisensi SIL Open Font License, jadi
boleh didistribusikan ulang.
