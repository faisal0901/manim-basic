# Naskah narasi: "Kenapa AI engineer bikin sistem RAG?"

Durasi video: ±73 detik. Waktu di bawah kira-kira, sesuaikan saat rekam suara.

| Waktu | Di layar | Narasi |
|---|---|---|
| 0:00–0:05 | Tumpukan dokumen, barisan karyawan | "Perusahaan kalian punya ratusan dokumen. Dan ratusan karyawan yang butuh jawaban dari situ." |
| 0:05–0:12 | Dokumen masuk ke AI, garis kuning membaca | "Cara paling gampang? Kasih semua dokumennya ke AI. AI bakal baca dari A sampai Z..." |
| 0:12–0:18 | Penghitung pertanyaan naik ke 100, karyawan bertanya | "...setiap kali ada pertanyaan. Seratus pertanyaan, berarti seratus kali baca ulang. Dan yang nanya bukan satu orang, tapi ratusan karyawan." |
| 0:18–0:25 | 500 × 100 = 50.000 halaman, bar biaya & waktu | "Lima ratus halaman kali seratus pertanyaan: lima puluh ribu halaman dibaca. Biayanya mahal, jawabannya lambat." |
| 0:25–0:30 | "Kenapa baca semuanya kalau cuma butuh sebagian?" | "Padahal... kenapa harus baca semuanya, kalau yang dibutuhkan cuma sebagian?" |
| 0:30–0:34 | Judul RAG | "Di sinilah RAG masuk. Retrieval-Augmented Generation. Cari dulu, baru jawab." |
| 0:34–0:39 | 1. Dokumen dipotong jadi chunk | "Pertama, dokumen dipotong jadi potongan kecil, namanya chunk." |
| 0:39–0:44 | 2. Chunk jadi titik vektor | "Tiap chunk diubah jadi vektor, deretan angka yang mewakili maknanya. Yang maknanya mirip, posisinya berdekatan." |
| 0:44–0:48 | 3. Pertanyaan jadi bintang di peta | "Waktu karyawan nanya, misalnya 'jatah cuti tahunan berapa?', pertanyaannya juga diubah jadi vektor." |
| 0:48–0:52 | 4. Lingkaran, ambil 3 terdekat | "Lalu sistem mencari chunk yang paling dekat. Ambil tiga teratas." |
| 0:52–0:56 | 5. Chunk relevan masuk ke AI | "Cuma tiga chunk itu yang dikirim ke AI. Bukan lima ratus halaman." |
| 0:56–1:00 | 6. Jawaban "12 hari" + sumber | "Hasilnya: jawaban cepat, tepat, dan ada sumbernya." |
| 1:00–1:06 | Tabel sebelum vs sesudah | "Bandingkan: dari dua ratus lima puluh ribu token jadi sekitar seribu lima ratus per pertanyaan. Dari lambat jadi hitungan detik." |
| 1:06–1:13 | "Inilah yang dikerjakan AI engineer: membangun sistem RAG" | "Dan inilah salah satu kerjaan AI engineer: membangun sistem RAG. Follow buat part berikutnya!" |

## Asumsi angka (dibulatkan, untuk ilustrasi)
- 1 halaman ≈ 500 token, jadi 500 halaman ≈ 250.000 token per pertanyaan; × 100 pertanyaan ≈ 25 juta token.
- 1 chunk ≈ 500 token, 3 chunk ≈ 1.500 token.
- "12 hari" dan "Peraturan Perusahaan, Bab 5" adalah contoh fiktif.
