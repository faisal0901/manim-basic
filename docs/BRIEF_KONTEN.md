# Brief konten

## Audiens dan niche
- **Siapa:** semua orang yang tertarik perkembangan AI. Pengguna ChatGPT biasa, pelajar, pekerja kantoran, juga yang ingin jadi AI engineer.
- **Niche:** cara kerja AI di balik layar, dari sudut efisiensi. Benang merahnya: "kenapa AI bisa ngarang, mahal, atau lambat, dan bagaimana engineer mengakalinya".
- **Janji ke penonton:** dalam satu menit kamu paham satu konsep AI dan bisa langsung pakai idenya.

## Seri (usulan)
| # | Topik | Pertanyaan pengguna | Teaser ke |
|---|---|---|---|
| 1 | RAG | "Kenapa AI ngarang soal dokumenku?" | Token |
| 2 | Token / tokenizer | "Kenapa jawaban panjang lebih mahal?" | Embedding |
| 3 | Embedding | "Gimana AI tahu dua kalimat artinya mirip?" | Chunking |
| 4 | Chunking | "Dokumen dipotong gimana biar nggak nyasar?" | Caching / model |
| 5 | Caching, model kecil vs besar | "Kenapa nggak pakai model paling pintar terus?" | AI engineer |
| 6 | AI engineer itu ngapain | "Jadi kerjaan AI engineer apa?" (rangkuman seri) | |

## Struktur video (60-75 dtk)
| Detik | Bagian | Isi |
|---|---|---|
| 0-2 | Hook visual + teks | Harus paham **dari visual saja tanpa suara** |
| 2-5 | Janji | "Namanya RAG, cuma 3 langkah" |
| 5-15 | Masalah konkret | Yang dialami penonton |
| 15-55 | Mekanisme | Satu langkah per beat, tiap beat ditutup "tapi..." atau "jadi..." |
| 55-65 | Payoff | Sebelum vs sesudah, angka hemat. Ini yang bikin orang share |
| 65-75 | Teaser | Pertanyaan yang dijawab part berikutnya |

## Dua gaya naskah
**A. "Kalau kamu yang bikin..."** (contoh: `proyek/video-rag-v2/naskah_A_kalau_kamu_bikin.md`)
- Judul layar: "Kalau kamu yang bikin... #N".
- Mulai dari keinginan sederhana, lalu rantai: solusi naif → **tapi** masalah → **jadi** solusi lebih baik → **tapi** ... 
- Istilah baru dimunculkan sebagai label tepat saat penonton "menemukannya" (chunk, embedding, retrieval).
- Tutup: "Selamat, kamu baru aja bikin X." + teaser.

**B. Hook biasa** (contoh: `proyek/video-rag-v2/naskah_B_hook.md`)
- Buka dengan salah satu: masalah penonton ("AI kamu ngarang?"), klaim kontra-intuitif ("ChatGPT sebenarnya nggak baca kata"), atau angka ("1.200 token jadi 300").
- Lalu janji, analogi, langkah bernomor, hasil sebelum/sesudah, satu tips praktis, teaser.

## Aturan hook dan naskah
1. Detik pertama harus bisa dipahami dari gambar dan teks saja.
2. Hook jujur sesuai isi. Bukan clickbait.
3. Jangan buka dengan konteks korporat (karyawan, perusahaan, ratusan dokumen). Buka dari pengalaman penonton sendiri.
4. Satu video, satu ide, satu open loop utama. ~150-190 kata.
5. Istilah dijelaskan dengan kata biasa **sebelum** disebut namanya.
6. Satu analogi per video, sebut batasnya ("bedanya, AI cari berdasarkan makna, bukan kata yang sama").
7. Angka konkret mengalahkan kata sifat. Cek angka ke dokumentasi resmi; tandai contoh fiktif.
8. Kalimat pendek, satu klausa per kalimat, gaya ngobrol.
9. Sesuatu berubah di layar tiap 1-3 detik. Narasi tepat bersamaan dengan visualnya.
10. Caption layar cuma kata kunci, bukan transkrip.
11. Ucapkan dan tulis kata kunci yang dicari: "RAG", "token", "ChatGPT".

## Ringkasan riset (dokumen lengkap: https://claude.ai/artifact/ApHDWzSaELB7NDAnUm7ux4)
- Ketiga platform menguji video ke penonton kecil dulu; yang dinilai terutama **retensi/watch time** dan **share**. Follower bukan faktor utama.
- Instagram (Mosseri, Jan 2025): sends via DM paling berpengaruh untuk menjangkau non-follower. Kejar share, bukan like.
- Shorts: cek "stayed to watch" (viewed vs swiped). Analisis Galloway (pihak ketiga): di bawah 60% jarang berhasil, terbaik 70-90%.
- Jangan hapus lalu unggah ulang video sepi (YouTube bisa anggap spam).
- Konsistensi: jadwal yang bisa dipertahankan, misalnya 2 video per minggu.
- Cover seragam dengan nomor part dan satu kata topik, untuk grid profil TikTok/IG.
- Caption: kata kunci di awal, 3-5 hashtag campuran.

## Uji A/B dan metrik
| Kapan | Cek | Artinya |
|---|---|---|
| 24-72 jam | % yang tidak langsung menggeser, retensi 2-3 detik awal | Hook bekerja atau tidak |
| 24-72 jam | Titik anjlok di grafik retensi | Bagian naskah yang membosankan/membingungkan |
| 24-72 jam | Rata-rata durasi tonton, % ditonton | Isi menahan sampai payoff |
| 3-7 hari | Share/sends dan save per view | Layak dikirim ke teman |
| 3-7 hari | % non-follower, sumber trafik | Masuk FYP atau hanya follower |

Aturan uji: ubah satu variabel per video, bandingkan di metrik yang sama, baca komentar untuk mencari salah paham. Di Instagram, Trial Reels bisa dipakai untuk menguji satu versi ke non-follower.
