# KAPUR: design system video Manim (v1)

"Kapur di papan hitam." Latar hitam penuh, tinta terang, warna dipakai sebagai **makna**.
Terinspirasi cara 3Blue1Brown memakai warna dan gerak, tapi palet, font, dan layout-nya milik sendiri.

![referensi](preview/referensi_palet.png)

## Isi folder
| File | Fungsi |
|---|---|
| `theme.py` | Token (warna, tipe, spasi, tempo) + helper + `KapurScene` |
| `rag_kapur.py` | Video RAG versi KAPUR (contoh pemakaian) |
| `palet.py` | Lembar referensi palet (gambar di atas) |
| `fonts/` | Inter, Source Serif 4, JetBrains Mono (lisensi OFL), didaftarkan otomatis |
| `preview/` | Frame kunci per bagian, 9:16 dan 16:9 |

## Aturan
**Warna = peran.** Satu warna selalu berarti hal yang sama di semua video.

| Token | Hex | Peran |
|---|---|---|
| `LANGIT` | #5CC3E6 | manusia, input, pertanyaan |
| `TOSKA` | #4FD1B8 | AI / model |
| `KUNYIT` | #FFD54A | fokus/sorotan. **Maksimal 1 hal kuning per layar** |
| `DAUN` | #8BD17C | solusi, benar, hemat |
| `SAGA` | #FF6B5E | masalah, salah, mahal |
| `JINGGA` | #F4A95C | angka & satuan penting |
| `HITAM` / `PERMUKAAN` / `GARIS` / `ABU_GELAP` / `ABU` / `TINTA` / `KERTAS` | #000 … #ECE6D8 | netral: latar, kartu, grid, sumbu, teks sekunder, teks utama, dokumen |

Isian kartu/kapsul memakai `redup(warna)` (≈18% di atas hitam), outline memakai warna penuh.

**Tipografi.** `judul()` = Source Serif 4 SemiBold (judul, kalimat besar). `teks()`/`caption()` = Inter (label). `mono()` = JetBrains Mono (angka, vektor, label bab).
Skala `TIPE`: raksasa 120 · display 68 · h1 52 · h2 40 · body 32 · caption 25 · mikro 19 (dikali `S`; 16:9 memakai S=0.8).

**Identitas.** Label bab kecil di kiri atas (`● BAB 2 · MASALAH`), judul rata kiri, garis bawah "kapur" melengkung (`coret_kapur`) di bawah kata kunci.

**Gerak.** Satu ide per ketukan. `KETUK`=1.0 dtk (default Manim), `CEPAT`=0.5, `LAMBAT`=1.6, `JEDA`=1.2 setelah ide penting, easing `smooth`.
`Write` untuk kata kunci, `FadeIn(shift=GESER)` untuk pendukung, `Transform` saat sesuatu *berubah menjadi* sesuatu yang lain, `Indicate`/`Circumscribe` kuning untuk fokus.

**Layout.** Pakai `pos(x, y)`, jangan koordinat mentah. Zona aman 9:16: atas 1.4, bawah 3.4 (caption & tombol app), kanan 0.9. Grid spasi `SP` xs/s/m/l/xl.

## Render di laptop
Butuh Python 3.10+ dan ffmpeg. **Tidak perlu LaTeX.**
```bash
# Windows: winget install ffmpeg   |  macOS: brew install ffmpeg pango pkg-config
# Ubuntu: sudo apt install ffmpeg libpango1.0-dev pkg-config
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# gambar frame kunci saja (cepat, ~20 dtk) -> preview/vertical/*.png
STILLS=1 ORIENT=vertical manim -s -ql rag_kapur.py RAGKapur
# video penuh 1080x1920 (hasil di media/videos/...)
ORIENT=vertical manim -qh rag_kapur.py RAGKapur
ORIENT=horizontal manim -qh rag_kapur.py RAGKapur
```
Windows PowerShell: `$env:ORIENT="vertical"; $env:STILLS="1"; manim -s -ql rag_kapur.py RAGKapur`.
Kalau font tidak terbaca (pesan `[kapur] gagal mendaftarkan font`), install 3 file di `fonts/` dengan klik dua kali.

## Video baru
```python
from theme import *
class VideoBaru(KapurScene):
    def construct(self):
        self.header("Apa itu embedding?", chapter="Bab 1 · Konsep")
        ai = ikon_ai().move_to(pos(0, 1))
        self.play(FadeIn(ai, scale=0.8), run_time=KETUK)
        self.mark("01_konsep")
```

## Riset & sumber
- Warna 3B1B: palet bertingkat A–E per hue (mis. BLUE_C #58C4DD, YELLOW_C #FFFF00, GREEN_C #83C167, RED_C #FC6255, TEAL_C #5CD0B3, GREY #888888). [manimlib/default_config.yml](https://github.com/3b1b/manim/blob/master/manimlib/default_config.yml)
- Default gerak: `run_time` 1.0 dtk, `rate_func=smooth`, `Write` menghitung durasi dari jumlah bagian. [manimlib/animation/animation.py](https://github.com/3b1b/manim/blob/master/manimlib/animation/animation.py), [creation.py](https://github.com/3b1b/manim/blob/master/manimlib/animation/creation.py)
- Manim dirancang agar "smoothness and cleanliness of style" jadi default. [3blue1brown.com/about](https://www.3blue1brown.com/about/)
- Gaya umum: latar gelap, aksen biru→kuning pada istilah kunci, `Transform` halus. [QuantumSketch blog](https://blog.quantumsketch.app/how-to-animate-like-3blue1brown/) (sumber pihak ketiga)

**Yang diambil:** warna sebagai makna, kuning untuk fokus, tempo tenang 1 dtk + smooth, transformasi untuk menunjukkan perubahan.
**Yang dibedakan:** latar #000 (3B1B default #333333 di config), hue sendiri yang lebih lembut, serif modern (bukan Computer Modern), label bab mono, layout rata kiri, zona aman untuk app vertikal.

## Tebakan v1 (perlu konfirmasi)
- Nama "KAPUR" dan belum ada logo/nama channel di layar.
- Pemilihan font (Source Serif 4 + Inter + JetBrains Mono).
- Layout 16:9: hook, masalah, perbandingan memakai dua kolom (flag `H` di `rag_kapur.py`); bagian lain adaptasi otomatis lewat `pos()`.
