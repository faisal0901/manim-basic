# Catatan video-sopan-v1

## Isi folder
| File | Isi |
|---|---|
| `SOPAN_B_hook_vertical.mp4` | Video final 9:16, 1080x1920, 60 fps, tanpa suara |
| `sopan_hook.py` | Kode Manim, kelas `SopanHook` (gaya B) |
| `naskah_B_hook.md` | Naskah per adegan + fakta + sumber |
| `naskah_narasi_rekam.md` | Naskah rekam suara |
| `preview/vertical/B_*.png`, `preview/ringkasan_B.png` | Frame kunci dan lembar ringkasan |

Render ulang (dari folder ini; `theme.py` dicari otomatis di `design-system/` root repo):
```bash
STILLS=1 ORIENT=vertical manim -s -ql sopan_hook.py SopanHook
ORIENT=vertical manim -qh sopan_hook.py SopanHook
```

## Fakta
- Kutipan Sam Altman (X, April 2025): "tens of millions of dollars well spent — you never know". Jawaban santai, bukan hitungan resmi (ditulis di layar).
- Token asli GPT-4o (o200k_base, js-tiktoken 1.0.21): "makasih ya kak 🙏🙏" = 8 token; emoji 🙏 pertama terpecah jadi 2 token (tampil sebagai "�"), yang kedua 1 token. "please" = 1, "tolong" = 2 (tol · ong).

## Tebakan / ilustrasi
- "× sejuta orang = 8.000.000 token" = hitungan contoh (ditulis di layar).
- Emoji 🙏 digambar sebagai ikon vektor (Text Manim tidak bisa merender emoji berwarna). Warna tangan `#E8B98A` khusus ikon ini, bukan warna peran.
- Riwayat chat ("resep seblak", "curhat mantan", dst.) dan balasan AI = ilustrasi.
- AI jahat sengaja generik (chip KAPUR merah, mata menyala, glitch), bukan karakter film, supaya aman hak cipta.
- "AI baca ulang obrolan dari awal": benar secara konsep; layanan bisa memakai cache sehingga lebih murah. Tidak dibahas.
