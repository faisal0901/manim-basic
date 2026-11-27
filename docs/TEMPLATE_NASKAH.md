# Template naskah

Salin file ini ke folder video baru, misalnya `proyek/video-token/naskah_A.md`.

## Info video
- **Judul kerja:**
- **Nomor seri:** #
- **Gaya:** A "Kalau kamu yang bikin..." / B hook biasa
- **Satu ide (satu kalimat):**
- **Open loop utama (pertanyaan yang dijawab di akhir):**
- **Analogi + batasnya:** "... seperti ..., bedanya ..."
- **Istilah baru (maks. 3), dalam urutan muncul:**
- **Payoff yang bikin orang share:** (sebelum vs sesudah, angka hemat)
- **Teaser part berikutnya:**
- **Target:** 60-75 dtk, 150-190 kata

## Per adegan
Satu baris = satu beat (5-10 dtk). `mark` = nama frame kunci di kode (`self.mark("...")`).

| # | Detik | Narasi (diucapkan) | Visual (Manim) | Teks layar | Warna peran | Istilah baru | mark |
|---|---|---|---|---|---|---|---|
| 1 | 0-3 | | | | | | 01_hook |
| 2 | 3-7 | | | | | | 02_ |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |
| 6 | | | | | | | |
| 7 | | | | | | | |
| 8 | | | | | | | |
| 9 | | | | | | | |
| 10 | | | | | | | 10_teaser |

Warna peran: LANGIT manusia/pertanyaan, TOSKA AI, KUNYIT fokus (1 per layar), DAUN solusi, SAGA masalah, JINGGA angka.

## Cek sebelum coding
- [ ] Detik 0-2 bisa dipahami tanpa suara
- [ ] Tidak dibuka dengan konteks korporat
- [ ] Tiap istilah dijelaskan dengan kata biasa sebelum namanya disebut
- [ ] Batas analogi disebut
- [ ] Gaya A: tiap beat pakai "tapi..." atau "jadi...", ditutup "Selamat, kamu baru aja bikin X"
- [ ] Jumlah kata 150-190 (baca keras pakai timer)
- [ ] Angka dicek; contoh fiktif ditandai
- [ ] Maks. satu hal kuning per layar
- [ ] Teaser konsisten dengan judul part berikutnya
- [ ] Caption postingan: kata kunci di awal + 3-5 hashtag

## Caption postingan
```
<kata kunci utama di awal kalimat> ...
#AI #ChatGPT #belajarAI #<topik>
```

## Catatan rekam suara
- Jeda dan tekan kata "tapi" dan "jadi".
- Rekam dulu, ukur durasi per beat, lalu sesuaikan `self.wait()` / `JEDA` di kode supaya visual mengikuti suara.
