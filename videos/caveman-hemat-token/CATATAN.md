# Catatan video-caveman-v1

## Isi folder
| File | Isi |
|---|---|
| `CAVEMAN_B_hook_vertical.mp4` | Video final 9:16, 1080x1920, 60 fps, tanpa suara |
| `caveman_hook.py` | Kode Manim, kelas `CavemanHook` (gaya B) |
| `naskah_B_hook.md` | Naskah per adegan + fakta + sumber |
| `naskah_narasi_rekam.md` | Naskah rekam suara |
| `preview/vertical/B_*.png`, `preview/ringkasan_B.png` | Frame kunci dan lembar ringkasan |

Render ulang (dari folder ini; `theme.py` dicari otomatis di `design-system/` root repo):
```bash
STILLS=1 ORIENT=vertical manim -s -ql caveman_hook.py CavemanHook
ORIENT=vertical manim -qh caveman_hook.py CavemanHook
```

## Keputusan
- Video umum, tanpa nomor seri dan tanpa teaser. Label bab: "Token · Caveman".
- Contoh pertanyaan "Gaji 2 juta, makan sebulan gimana?" (ide Faisal, meme gaji kecil) supaya relate untuk penonton umum. Adegan AI mikir: teks stream huruf per huruf, coretan "ayam tiap hari? ← kemahalan", "salmon? ← mimpi", akhirnya "pas ✓".

## Fakta (sumber di naskah_B_hook.md)
- README caveman: 65% lebih sedikit token **output** (rata-rata 10 prompt, rentang 22–87%); contoh 69 → 19 token.
- README caveman: "Input and reasoning tokens are untouched"; skill menambah ~1–1,5 ribu token input per giliran; di pekerjaan yang sudah ringkas bisa net rugi.

## Tebakan / ilustrasi
- Angka 3.000 mikir / 1.200 jawab / 300 caveman dan "−21%" = **contoh fiktif** (ditulis "angka contoh" di layar). 4.200 → 3.300 = 21,4%.
- Teks mikir AI dan jawaban "Telur. Tempe. Sayur. Muat." = ilustrasi, bukan keluaran model sungguhan. 2 juta ÷ 30 = 66.667, jadi "66rb sehari" benar.
- "Token reasoning dibayar sebagai output": berlaku untuk Claude extended thinking dan model reasoning OpenAI; cek ulang halaman harga sebelum upload.
- Token input biasanya lebih murah per token dibanding output, jadi "+1.000 input" tidak setara 1.000 token output. Tidak dibahas di video supaya tetap satu ide.
- README yang dibaca adalah fork repo juliusbrussee/caveman; angka sama dengan yang dikutip situs lain.
