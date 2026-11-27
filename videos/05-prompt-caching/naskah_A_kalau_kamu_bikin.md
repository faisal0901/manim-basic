# Naskah A "Kalau kamu yang bikin...": prompt caching

Target 9:16, sekitar 78 detik, sekitar 195 kata, tanpa teaser part berikutnya.
Kasus: bot CS toko online (nyambung ke video RAG v4). Visual server 3D: `server-3d/zoom1..5` + `opsi3_cocok_dari_bawah`.
Kunci warna: LANGIT pembeli/pertanyaan · TOSKA AI/hasil hitungan · DAUN cocok/hemat · SAGA mahal/hitung ulang · JINGGA angka · KUNYIT 1 fokus.

| # | Waktu | Visual | Teks di layar | Narasi |
|---|---|---|---|---|
| 01 hook | 0-5 | Balon pembeli "masih ready kak?" (LANGIT) kecil. Di belakangnya menara aturan toko tinggi ikut terkirim, berkedip SAGA "dari nol". | "masih ready kak?" · "+ 3.000 token aturan toko (angka contoh)" | Tiap pembeli nanya "masih ready kak?", bot CS tokomu baca ulang 3.000 token aturan toko. Dari nol. |
| 02 kalau kamu | 5-14 | Menara masuk ke server, GPU (chip TOSKA) mengubah blok jadi kolom angka kecil. | "GPU = chip tukang hitung" · "token → angka" | Kalau kamu yang bikin AI-nya: tiap pertanyaan, aturan toko dikirim bareng, dan GPU, chip tukang hitung di server, ngubah tiap token jadi tumpukan angka. |
| 03 tapi sama | 14-22 | Penghitung "pembeli ke-1, 2, … 100", menara dihitung ulang tiap kali (SAGA). Lalu kalimat "jadi, simpan". | "100 pembeli = 100× hitung ulang" | Tapi... aturannya sama terus. Seratus pembeli, seratus kali dihitung ulang. Jadi, simpan aja angka hasil hitungannya di memori GPU. |
| 04 zoom server | 22-28 | zoom1 → zoom2 → zoom3 → zoom4 (kamera masuk: rak, server, GPU, memori, blok 1-5 terisi). | "memori GPU" · "angka, bukan teks" | Pertanyaan berikutnya datang, tinggal pakai yang tersimpan. Cuma pertanyaan barunya yang dihitung. |
| 05 tapi cocok? | 28-40 | zoom5 (CPU cocokin sidik, 5 blok DAUN, 2 baru KUNYIT) → opsi3 (beda 1 kata di depan → merah ke atas). | "CPU = manajer" · "cocokin dari awal" · "tetap → depan · berubah → belakang" | Tapi... gimana tahu awalnya sama? Jadi CPU, si manajer server, bikin sidik tiap blok dan nyocokin dari awal. Beda satu kata di depan, semua setelahnya dihitung ulang. Yang tetap di depan, yang berubah di belakang. |
| 06 tapi terbatas | 40-47 | Memori penuh blok, blok lama memudar & digusur. Jam kecil; blok dipakai → menyala lagi. | "sementara" · "contoh: 5 menit, diperpanjang tiap dipakai" | Tapi... memori GPU terbatas. Jadi simpanannya sementara. Contohnya lima menit, diperpanjang tiap dipakai. |
| 07 selamat | 47-54 | Judul besar PROMPT CACHING. Batang: hitung biasa (penuh) vs baca dari cache (1/10, DAUN). | "Selamat, kamu baru aja bikin **prompt caching**" · "baca dari cache: 1/10 harga (salah satu penyedia)" | Selamat, kamu baru aja bikin prompt caching. Di salah satu penyedia, baca dari cache cuma sepersepuluh harga. |
| 08 hati-hati | 54-66 | Aturan toko dengan baris pertama "Sekarang: 13:31:05" (KUNYIT). Tiap pesan jamnya beda → blok 1 merah → semua merah. Ikon "TULIS" menyala terus, "BACA" tetap 0. Batang: tanpa cache 1× vs cache cuma ditulis 1,25× (SAGA). | "cache ditulis terus, nggak pernah kebaca" · "nulis cache: 1,25× harga" | Tapi hati-hati. Nyimpennya justru lebih mahal, 1,25 kali. Misal kamu taruh jam di baris pertama aturan, biar bot tahu waktu. Tiap detik awalnya beda. Cache ditulis terus, nggak pernah kebaca. Bayar lebih, hemat nol. |
| 09 toko sepi | 66-71 | Timeline pembeli jarang (jeda 7, 12 menit). Blok keburu hilang sebelum pembeli berikutnya. | "jeda > 5 menit → simpanan hilang" | Sama kalau tokomu sepi: jeda pembeli lebih dari lima menit, simpanannya keburu hilang. |
| 10 tips | 71-78 | Aturan toko dengan baris jam pindah ke paling bawah (DAUN). Kartu laporan pemakaian: "cache write ↑ · cache read 0" → coret. | "jam → taruh di belakang" · "cek: cache read nol terus? = cuma ditulis" | Jadi jam taruh di belakang, dan cek laporan pemakaian: kalau "cache read" nol terus, cache-mu cuma ditulis. |

## Fakta yang dipakai (dicek 27 Nov 2026, dokumentasi resmi)
- Anthropic, [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching):
  - Awalan harus identik; konten tetap di depan, yang berubah (timestamp, konteks per permintaan) di belakang.
  - Masa berlaku default 5 menit, diperpanjang gratis tiap dipakai (opsi 1 jam).
  - Baca dari cache 0,1× harga input; tulis cache 1,25× (5 menit) atau 2× (1 jam).
  - Contoh resmi soal timestamp: "You pay for a fresh cache write on every request and never get a read."
  - Deteksi: kolom pemakaian `cache_creation_input_tokens` (ditulis) dan `cache_read_input_tokens` (kebaca).
  - Yang disimpan representasi KV cache + hash di memori, bukan teks prompt.
- OpenAI, [Prompt Caching 201](https://developers.openai.com/cookbook/examples/prompt_caching_201): "We've seen customers accidentally invalidate their cache by including a timestamp early in their request." Awalan harus cocok persis; yang disimpan KV tensor, bukan token.
- Cara kerja server (CPU cocokkan hash blok, GPU loncati hitungan awal): mengikuti sistem terbuka seperti vLLM/SGLang.

## Kasus "ditulis tapi nggak kebaca" lain (tidak masuk narasi, buat caption/komentar)
- Percakapan makin panjang dan titik cache dipasang terlalu jauh (sistem cuma melihat mundur 20 blok).
- Banyak permintaan paralel dikirim sebelum permintaan pertama selesai menulis cache: semuanya bayar nulis.
- Daftar tools diubah atau urutan kunci JSON acak tiap kirim: awalan beda.
- Prompt di bawah batas minimal (512-4.096 token tergantung model): tidak di-cache sama sekali, tanpa error.
- Catatan: di OpenAI model lama, nulis cache tidak dikenai biaya tambahan, jadi rugi 1,25× berlaku di penyedia yang mengenakan biaya tulis.

## Angka di layar
- "3.000 token", "100 pembeli", jam "13:31:05", jeda "7, 12 menit" = angka contoh.
- "1/10", "1,25×", "5 menit" = angka salah satu penyedia (Anthropic), ditulis "salah satu penyedia" karena beda tiap penyedia dan bisa berubah.

## Batas analogi & penyederhanaan
- Menara/blok kubus = gambaran. Aslinya angka Key/Value per token per lapisan, tersebar ke beberapa GPU.
- 1 blok di gambar = sekumpulan token (vLLM default 16), bukan satu kata.
- "Beda satu kata di depan, semua setelahnya dihitung ulang": blok sebelum titik beda kadang masih bisa dipakai, tergantung sistem.
- "Bayar lebih, hemat nol": tepatnya 1,25× dibanding 1× tanpa cache, kalau cache tidak pernah kebaca.
- Durasi sekitar 78 detik, sedikit di atas target 75. Kalau kepanjangan, adegan 09 (toko sepi) bisa dipindah ke caption.
