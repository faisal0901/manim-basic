# Naskah: #2 Tokenizer, gaya B (hook biasa)

## Info video
- **Judul kerja:** Kenapa AI salah hitung huruf R di strawberry?
- **Nomor seri:** #2 (menjawab teaser video A: "Tapi kenapa token bisa semahal itu?")
- **Gaya:** B hook biasa (masalah yang dialami penonton + klaim kontra-intuitif)
- **Satu ide:** AI membaca potongan teks (token) yang diganti nomor, bukan huruf.
- **Open loop utama:** kenapa AI bisa salah hitung huruf semudah itu?
- **Analogi + batasnya:** token mirip suku kata. Bedanya, potongannya bukan suku kata beneran ("berapa" jadi ber|apa, bukan be|ra|pa), dipilih dari potongan yang paling sering muncul di teks.
- **Istilah baru (urutan muncul):** token, tokenizer
- **Payoff:** strawberry = satu nomor (101830), huruf r tidak kelihatan. Tips eja pakai spasi: 10 token, tiga r kelihatan.
- **Penghubung ke biaya (jawaban teaser A):** token juga yang dihitung dan dibayar; kalimat Indonesia contoh 9 token vs Inggris 7 token.
- **Teaser:** "#3 Embedding": kalau AI cuma lihat nomor, gimana dia tahu dua kalimat artinya mirip?
- **Durasi:** 70,4 detik, 162 kata narasi.
- **Tokenizer yang dipakai:** o200k_base (GPT-4o) untuk semua pecahan, cl100k_base (GPT-4) sebagai pembanding. Dijalankan sungguhan dengan js-tiktoken 1.0.21 pada 26 Nov 2026. Hasil mentah: `data/hasil_tokenizer.txt`.

## Per adegan

| # | Detik | Narasi (diucapkan) | Visual (Manim) | Teks layar | Warna peran | Istilah | mark |
|---|---|---|---|---|---|---|---|
| 1 | 0-6,5 | Tanya AI: ada berapa huruf r di strawberry? Banyak AI pernah jawab: dua. Padahal tiga. | Gelembung pertanyaan, AI jawab "Ada 2.", stempel SALAH, kata "strawberry" besar dengan tiga r kuning bernomor 1 2 3 | "Padahal ada 3." + catatan kecil "kasus viral 2024 · model baru banyak yang sudah benar" | LANGIT tanya, TOSKA AI, SAGA salah, KUNYIT huruf r, JINGGA angka, DAUN benar | | 01_hook |
| 2 | 6,5-12,5 | Ini bukan karena AI bodoh. AI memang nggak baca huruf. | Kalimat besar, ikon AI | "AI memang nggak baca huruf." | KUNYIT "nggak baca huruf." | | 02_klaim |
| 3 | 12,5-18 | Sebelum dibaca, teks dipotong dulu. Mirip kita baca per suku kata. | Pertanyaan tertulis, contoh suku kata be·ra·pa | "mirip kita baca per suku kata" | LANGIT teks, ABU suku kata | | 03_analogi |
| 4 | 18-23 | Potongan ini namanya token. Pemotongnya disebut tokenizer. | Kalimat berubah jadi 9 blok warna-warni | "tokenizer", pil "token", "9 token" | JINGGA jumlah | token, tokenizer | 04_token |
| 5 | 23-28 | Bedanya, potongannya bukan suku kata beneran. "Berapa" jadi "ber" dan "apa". Dipilih dari potongan yang paling sering muncul. | Sorot ber + apa | "Bedanya: bukan suku kata beneran." | KUNYIT sorotan | | 05_batas |
| 6 | 28-29,5 | Dan strawberry? Utuh, satu token. | Sorot blok "strawberry" | "strawberry = 1 token utuh" | KUNYIT sorotan | | 06_utuh |
| 7 | 29,5-35 | Lalu tiap token diganti nomor. Yang sampai ke AI cuma deretan nomor ini. | Blok token pindah ke atas, salinan berubah jadi blok nomor | "yang sampai ke AI cuma ini:" | JINGGA nomor, KUNYIT 101830 | | 07_nomor |
| 8 | 35-39 | Strawberry jadi satu nomor. Huruf r-nya di mana? | Tetap | "Huruf r-nya di mana?" | SAGA | | 08_huruf_hilang |
| 9 | 39-46 | Pecahannya beda tiap model. GPT-4o motong jadi st, raw, berry. GPT-4 lain lagi. Tetap potongan, bukan huruf. | Dua baris blok + nomor: GPT-4o st/raw/berry, GPT-4 str/aw/berry | "Beda model, beda pecahan", nama tokenizer | TOSKA nama model | | 09_beda_model |
| 10 | 46-51 | Tipsnya: kalau mau AI hitung huruf, pisah hurufnya pakai spasi. Sekarang satu huruf, satu token. | Prompt "s t r a w b e r r y", 10 blok huruf, tiga r kuning bernomor 428 | "10 token · satu huruf, satu token" | KUNYIT huruf r, JINGGA angka | | 10_tips |
| 11 | 51-55 | AI jauh lebih gampang ngitung. | AI jawab "Ada 3." | "tiga r kelihatan, AI jauh lebih gampang ngitung" | DAUN | | 11_tips_hasil |
| 12 | 55-60 | Dan token ini juga yang dihitung dan dibayar. Kalimat Indonesia ini sembilan token. Versi Inggrisnya tujuh. | Dua kalimat bermakna sama dengan pecahan tokennya | "harga AI & batas panjang chat dihitung per token", "9 token" / "7 token" | JINGGA angka | | 12_biaya |
| 13 | 60-64 | Makin banyak token, makin mahal. | Tetap + kalimat penutup | "Makin banyak token, makin mahal." + catatan contoh | SAGA mahal | | 13_mahal |
| 14 | 64-71,5 | Tapi kalau AI cuma lihat nomor, gimana dia tahu dua kalimat artinya mirip? Itu di part tiga. | Kalimat teaser, pil "#3 Embedding" | "artinya mirip?" | KUNYIT, JINGGA pil | | 14_teaser |

## Data token asli (o200k_base, GPT-4o)

| Teks | Jumlah | Pecahan | Nomor |
|---|---|---|---|
| Ada berapa huruf r di strawberry? | 9 | Ada · ␣ber · apa · ␣hur · uf · ␣r · ␣di · ␣strawberry · ? | 139151, 5009, 7063, 21317, 1427, 428, 1320, 101830, 30 |
| strawberry (tanpa spasi di depan) | 3 | st · raw · berry | 302, 1618, 19772 |
| s t r a w b e r r y | 10 | s · ␣t · ␣r · ␣a · ␣w · ␣b · ␣e · ␣r · ␣r · ␣y | 82, 260, 428, 261, 286, 287, 319, 428, 428, 342 |
| Tolong jelaskan cara kerja mesin cuci | 9 | T · olong · ␣jel · askan · ␣cara · ␣kerja · ␣mesin · ␣c · uci | |
| Please explain how a washing machine works | 7 | Please · ␣explain · ␣how · ␣a · ␣washing · ␣machine · ␣works | |

Pembanding cl100k_base (GPT-4): strawberry = str · aw · berry (496, 675, 15717). Kalimat Indonesia di atas jadi 12 token, Inggrisnya tetap 7.

␣ = spasi. Di layar spasi depan tidak ditulis, cukup jadi jarak antar blok.

## Cek sebelum upload
- [x] Detik 0-2 bisa dipahami tanpa suara (pertanyaan, "Ada 2.", SALAH, tiga r bernomor)
- [x] Tidak dibuka dengan konteks korporat
- [x] Token dan tokenizer dijelaskan dengan kata biasa sebelum namanya disebut
- [x] Batas analogi disebut (bukan suku kata beneran)
- [x] Jumlah kata 162
- [x] Angka token dari tokenizer sungguhan, tokenizer disebut di layar
- [x] Maks. satu hal kuning per layar (tiga huruf r dihitung satu kelompok)
- [x] Teaser konsisten: "#3 Embedding"

## Caption postingan
```
Kenapa AI salah hitung huruf R di strawberry? Karena AI baca token, bukan huruf. Tips: eja pakai spasi.
#AI #ChatGPT #belajarAI #tokenizer #token
```
