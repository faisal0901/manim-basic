# Setup lokal: Manim di laptop

Yang dibutuhkan: Python 3.10 sampai 3.12 (paling aman), ffmpeg, dan 3 font di `proyek/design-system/fonts/`. **Tidak perlu LaTeX**: semua teks pakai `Text`, bukan `MathTex`/`Tex`.

## 1. Pasang sistem

**Windows**
```powershell
winget install Python.Python.3.12
winget install Gyan.FFmpeg        # tutup lalu buka lagi terminal setelahnya
```
Manim di Windows terpasang dari wheel, tidak perlu Pango terpisah.

**macOS**
```bash
brew install python@3.12 ffmpeg pango pkg-config cairo
```

**Linux (Ubuntu/Debian)**
```bash
sudo apt install python3-venv python3-dev build-essential ffmpeg libcairo2-dev libpango1.0-dev pkg-config
```
(Di cloud dulu, `libpango1.0-dev` dan `pkg-config` wajib sebelum `pip install manim`.)

## 2. Pasang Manim
```bash
cd handoff/proyek
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r design-system/requirements.txt     # manim>=0.18,<0.23
manim --version
```
Catatan: Manim 0.19 ke atas sudah tidak butuh ffmpeg untuk render, tapi ffmpeg tetap berguna untuk gabung audio dan konversi.

## 3. Font
`theme.py` mendaftarkan font dari `fonts/` secara otomatis. Kalau muncul `[kapur] gagal mendaftarkan font bundel`, atau teks tampil dengan font default, install manual dengan klik dua kali tiap file: `Inter.ttf`, `SourceSerif4.ttf`, `JetBrainsMono.ttf`.
Cek font terbaca:
```bash
python -c "import manimpango as m; f=m.list_fonts(); print([x for x in ('Inter','Source Serif 4','JetBrains Mono') if x in f])"
```

## 4. Perintah render

Semua dijalankan dari dalam folder video (`proyek/video-rag-v2/`). Orientasi lewat env `ORIENT` (`vertical` default, atau `horizontal`).

| Tujuan | macOS/Linux | Waktu kira-kira |
|---|---|---|
| Frame kunci saja (PNG) | `STILLS=1 ORIENT=vertical manim -s -ql rag_dua_versi.py RAGHook` | ~20 dtk |
| Draf video kualitas rendah | `ORIENT=vertical manim -ql rag_dua_versi.py RAGHook` | ~1 mnt |
| Final 1080x1920 | `ORIENT=vertical manim -qh rag_dua_versi.py RAGKalauKamuBikin RAGHook` | beberapa menit |
| Final 16:9 | `ORIENT=horizontal manim -qh rag_dua_versi.py RAGHook` | beberapa menit |

Windows PowerShell, set env dulu (berlaku sampai terminal ditutup):
```powershell
$env:ORIENT="vertical"; $env:STILLS="1"; manim -s -ql rag_dua_versi.py RAGHook
Remove-Item Env:STILLS      # matikan STILLS sebelum render video
```

- PNG frame kunci masuk ke `preview/<orientasi>/` (nama dari `self.mark("...")`, berawalan A_ atau B_).
- Video masuk ke `media/videos/rag_dua_versi/<kualitas>/`.
- Kelas: `RAGKalauKamuBikin` (naskah A), `RAGHook` (naskah B). Di `design-system/`: `RAGKapur` (arsip) dan `PaletKapur` (lembar palet).

## 5. Revisi detail tanpa render ulang penuh
1. **Lihat PNG dulu, bukan video.** `STILLS=1 ... -s -ql` melompati animasi tapi tetap menyimpan tiap `mark()`. Ini cara paling cepat cek posisi, warna, ukuran teks.
2. **Render sebagian animasi saja** dengan `-n mulai,akhir` (nomor animasi `self.play`, mulai dari 0):
   `ORIENT=vertical manim -ql -n 12,18 rag_dua_versi.py RAGHook`
   Cari nomornya dengan menambah `print(self.renderer.num_plays)` sementara di dekat bagian yang diubah.
3. **Cache Manim otomatis.** Animasi yang tidak berubah tidak dirender ulang di run berikutnya (cache di `media/`). Jangan pakai `--disable_caching` saat revisi. Hapus `media/` hanya kalau hasilnya aneh.
4. **`-p` membuka video otomatis** setelah render: `manim -pql ...`.
5. **Ubah tempo lewat konstanta**, bukan angka di tiap baris: `JEDA` dan `JEDA_PANJANG` di atas `rag_dua_versi.py` (sekarang 1.8 dan 2.9), atau `KETUK/CEPAT/LAMBAT` di `theme.py`.
6. **Ubah warna/font lewat `theme.py`**: semua video ikut berubah. Jangan tulis hex langsung di file video.
7. **Pisah beat jadi kelas kecil** kalau sering revisi satu bagian: buat `class CobaLangkah2(RAGBase)` yang hanya memanggil bagian itu, render, lalu hapus.
8. **Render `-qh` hanya sekali di akhir**, setelah semua revisi lolos di `-ql`.

## 6. Masalah umum
| Gejala | Solusi |
|---|---|
| `ModuleNotFoundError: theme` | Jalankan dari `proyek/video-rag-v2/` dan pastikan `proyek/design-system/` ada di sebelahnya |
| Error LaTeX | Ada `MathTex`/`Tex`/`Integer`/`DecimalNumber` di kode. Ganti dengan `Text`/`teks()`/`mono()` |
| `pangocairo` tidak ditemukan saat pip install (Linux/mac) | Pasang `libpango1.0-dev pkg-config` (Linux) atau `brew install pango pkg-config` |
| Font salah | Lihat bagian 3 |
| `STILLS` tetap aktif saat render video | Video tetap jadi, tapi PNG ikut ditimpa. Hapus env-nya |
