# Naskah: "Kalau kamu yang bikin… #3 Embedding" (gaya A, draf 1)

Status: **disetujui dan dirender** (26 Nov 2026), `EMBEDDING_A_kalau_kamu_bikin_vertical.mp4`, 69,4 detik.

## Info video
- **Gaya:** A "Kalau kamu yang bikin…" (selang-seling: #1 A, #2 B, #3 A)
- **Satu ide:** embedding = mengubah kata/kalimat jadi deretan angka, sehingga yang maknanya mirip letaknya berdekatan, walau hurufnya beda total.
- **Sudut baru (beda dari video RAG):** video RAG cuma *memakai* embedding. Di sini penonton *menemukan* kenapa embedding perlu dan dari mana angkanya datang (belajar dari kalimat).
- **Open loop:** gimana "HP murah" bisa ketemu "HP harga terjangkau" padahal nggak ada kata yang sama?
- **Analogi + batasnya:** posisi di peta. Bedanya, aslinya bukan 2 sumbu tapi ratusan sampai ribuan, dan sumbunya nggak punya nama jelas seperti "harga".
- **Istilah baru:** embedding (satu saja)
- **Penutup:** tanpa teaser part berikutnya (sesuai permintaan). Ditutup dengan hubungan ke RAG dan ke pengalaman pengguna.
- **Target:** sekitar 70 detik, sekitar 170 kata.

## Per adegan

| # | Detik | Narasi | Visual (Manim) | Warna |
|---|---|---|---|---|
| 1 | 0-4 | Kamu bikin toko online. Pembeli ngetik "HP murah". Produkmu tulisannya "HP harga terjangkau". | Kolom cari "HP murah" (LANGIT) di atas, kartu produk "HP harga terjangkau" di bawah, tanda tanya di antaranya. Paham tanpa suara. | LANGIT pembeli, KUNYIT "murah" vs "terjangkau" |
| 2 | 4-9 | Gampang: cari yang katanya sama persis. Tapi… "murah" dan "terjangkau" beda huruf. Hasilnya nol. | Huruf kedua kata dijajarkan, tidak ada yang cocok, coret merah. "0 hasil". | SAGA, JINGGA "0" |
| 3 | 9-15 | Jadi kamu bikin daftar sinonim. Tapi… orang juga ngetik "miring", "ramah kantong", "murmer". Nggak ada habisnya. | Daftar sinonim memanjang ke bawah, kata baru terus berdatangan keluar layar. | SAGA "Tapi…" |
| 4 | 15-25 | Jadi ganti cara. Tiap kata kamu kasih posisi di peta. Sumbu ini soal harga: murah di kiri, mahal di kanan. Murah dan terjangkau jatuh berdekatan. | Satu garis sumbu "harga". Titik "murah", "terjangkau", "miring" di kiri berdekatan, "mahal", "premium" di kanan. | DAUN kelompok dekat |
| 5 | 25-34 | Tapi… siapa yang ngisi posisi jutaan kata? Jadi biarin komputer belajar dari banyak sekali kalimat. Kata yang muncul di kalimat mirip, dapat posisi mirip. | Kalimat "HP ini ___ banget, cuma sejuta" dengan kata yang bergantian masuk ke celah: murah / terjangkau / miring. Titik-titiknya ditarik saling mendekat. | KUNYIT celah kalimat |
| 6 | 34-42 | Tapi… satu sumbu kurang. "Bisa" bisa berarti mampu, bisa juga racun ular. Jadi tambah sumbu. Ratusan, bahkan ribuan. | Kata "bisa" terbelah ke dua tempat. Sumbu kedua muncul (peta 2D), lalu kilasan banyak sumbu dengan label "ratusan–ribuan sumbu". | JINGGA angka |
| 7 | 42-50 | Tiap kata, bahkan tiap kalimat, sekarang jadi deretan angka. Yang maknanya mirip, angkanya berdekatan. | "HP harga terjangkau" → [0.12, −0.83, 0.47, …]. "HP murah" → deret yang mirip, ditaruh berdampingan. | JINGGA angka |
| 8 | 50-58 | Sekarang "HP murah" ketemu "HP harga terjangkau". Walau kata "murah"-nya nggak ada sama sekali. | Kembali ke toko: kolom cari menyala, produk muncul sebagai hasil teratas. | DAUN hasil |
| 9 | 58-70 | Selamat. Kamu baru aja bikin embedding. Ini yang dipakai RAG buat nyari potongan dokumen yang pas, dan yang bikin AI ngerti maksudmu walau kata-katamu beda. | "Selamat.", "Embedding" besar DAUN. Ikon kecil RAG dan gelembung chat. | DAUN |

**Jumlah kata narasi:** sekitar 172.

## Catatan dan tebakan
- Angka vektor dan posisi titik di peta adalah **ilustrasi**, bukan hasil model sungguhan (model embedding tidak bisa diunduh dari cloud ini). Kalau mau angka nyata, bisa dihitung di laptop dengan model embedding gratis, lalu kedekatan "murah"–"terjangkau" vs "murah"–"mahal" ditampilkan.
- "Ratusan sampai ribuan sumbu": umum untuk model embedding (contoh: text-embedding-3-small dari OpenAI 1.536 dimensi, menurut dokumentasinya). Perlu dicek ulang sebelum angkanya ditulis di layar.
- "Belajar dari kalimat": penyederhanaan dari cara model embedding dilatih (kata/kalimat yang muncul di konteks serupa dibuat berdekatan).
- Sumbu "harga" hanya alat bantu cerita. Sumbu asli tidak punya nama yang bisa dibaca manusia. Ini batas analogi yang disebut di adegan 6.
- Contoh "bisa" (mampu / racun ular) dipakai karena khas bahasa Indonesia.
- Caption postingan: "Gimana AI tahu 'murah' dan 'terjangkau' itu mirip? Kalau kamu yang bikin, kamu bakal nemuin embedding. #AI #ChatGPT #belajarAI #embedding"
