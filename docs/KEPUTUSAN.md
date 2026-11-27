# Keputusan proyek

Status: **Final** = sudah kamu setujui atau sudah jelas dari percakapan. **Tebakan** = dibuat Claude, belum kamu konfirmasi. **Terbuka** = belum diputuskan.

## Format dan platform
| Keputusan | Alasan | Status |
|---|---|---|
| Seri video animasi pendek pakai Manim | Gaya penjelasan visual ala 3Blue1Brown, cocok untuk konsep AI | Final |
| 9:16 utama (1080x1920), 16:9 untuk YouTube | TikTok, Reels, Shorts dulu; YouTube panjang belakangan | Final |
| Bahasa Indonesia santai | Audiens lokal, gaya ngobrol menang dari formal (prinsip Mayer) | Final |
| Durasi 60-75 detik, ~150-190 kata narasi | Satu ide per video; tempo bicara ~2,5 kata/dtk | Final |
| Render di laptop sendiri, bukan cloud | Revisi detail di cloud lambat | Final |

## Audiens dan sudut konten
| Keputusan | Alasan | Status |
|---|---|---|
| Audiens: semua yang tertarik AI, termasuk pengguna biasa | Pasar lebih luas dari "calon AI engineer" | Final |
| Sudut efisiensi: "kirim dokumen besar ke AI itu boros token" | Pengalaman yang dialami semua pengguna, ada angka konkret | Final |
| Naskah dibuka dari pengalaman pengguna, istilah teknis jadi bonus di akhir | Penonton awam tidak bertahan kalau dibuka dengan jargon | Final |
| Seri: RAG, token/tokenizer, embedding, chunking, caching/model kecil vs besar, AI engineer itu ngapain | Saling menyambung, tiap video jadi teaser video berikutnya | Usulan, urutan setelah RAG belum final |

## Naskah
| Keputusan | Alasan | Status |
|---|---|---|
| Hook v1 (karyawan dan ratusan dokumen) salah | Terlalu korporat, tidak relevan buat pengguna biasa | Final. v1 dan RAG KAPUR jadi arsip |
| Istilah (chunk, vektor, token, embedding) dijelaskan sebelum dipakai | Penonton awam hilang kalau dengar istilah dulu (pre-training Mayer) | Final |
| Dua gaya naskah diuji berdampingan | Kamu suka gaya "Kalau kamu yang bikin...", tapi perlu bukti dari data | Final |
| Gaya A: "Kalau kamu yang bikin..." (rantai tapi... jadi..., tutup "Selamat, kamu baru aja bikin X") | Penonton merasa menemukan sendiri; tiap "tapi" jadi open loop kecil | Final |
| Gaya B: hook biasa (masalah, klaim kontra-intuitif, atau angka) | Pola yang terbukti umum di short-form | Final |
| Nanti selang-seling A dan B; tanya gaya mana tiap video baru | Hasil uji menentukan porsinya | Final |
| Satu analogi per video, sebut batasnya | Analogi menyesatkan tetap terasa meyakinkan (Kulgemeyer & Wittwer 2022) | Final |
| Angka contoh ("12 hari", "Peraturan Perusahaan Bab 5", "hal. 47") fiktif | Ilustrasi | Final, sebaiknya disebut "contoh" di caption |

## Design system KAPUR
| Keputusan | Alasan | Status |
|---|---|---|
| Latar hitam penuh `#000000` | Permintaanmu; beda dari 3B1B (#333) | Final |
| Warna = peran, tetap di semua video | Penonton belajar arti warna; signaling | Final, palet disetujui |
| `LANGIT #5CC3E6` manusia/input/pertanyaan | | Final |
| `TOSKA #4FD1B8` AI/model | | Final |
| `KUNYIT #FFD54A` fokus, **maks. 1 hal kuning per layar** | Kalau semua disorot, tidak ada yang disorot | Final |
| `DAUN #8BD17C` solusi/benar/hemat, `SAGA #FF6B5E` masalah/salah/mahal, `JINGGA #F4A95C` angka & satuan | | Final |
| Netral: PERMUKAAN #0D0D0D, GARIS #1E1E1E, ABU_GELAP #454545, ABU #9B9B9B, TINTA #EDEDED, KERTAS #ECE6D8 | Teks utama bukan putih murni, lebih lembut | Final |
| Tanpa LaTeX, semua `Text` | Setup lebih ringan di laptop | Final |
| Tempo: KETUK 1.0, CEPAT 0.5, LAMBAT 1.6, easing smooth; v2 pakai JEDA 1.8 / JEDA_PANJANG 2.9 | Ruang untuk narasi 60-70 dtk | Final, sesuaikan setelah rekam suara |
| Zona aman 9:16: atas 1.4, bawah 3.4, kanan 0.9 unit | Tombol dan caption app | Final |
| Nama "KAPUR" | | **Tebakan** |
| Font: Source Serif 4 (judul), Inter (label), JetBrains Mono (angka/label bab) | | **Tebakan** |
| Belum ada logo/nama channel di layar | | **Tebakan** |
| Layout 16:9 dua kolom (sudah ada di rag_kapur.py) | | **Tebakan**, untuk v2 belum dicek |

## Masih terbuka
- Gaya mana yang menang (tunggu hasil uji A/B).
- Nama seri dan penomoran: "Kalau kamu yang bikin... #1" vs format seragam seperti "AI 60 Detik #1" (saran riset).
- Teaser part 2 tidak seragam: A bilang "#2 Tokenizer", B bilang "Part 2: kenapa token bikin AI mahal?". Samakan sebelum upload.
- Suara: rekam sendiri (rencana), musik latar belum dipilih.
- Nama channel, logo, template cover.
- Urutan seri setelah token.
