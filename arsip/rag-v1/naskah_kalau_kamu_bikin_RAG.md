# Naskah: "Kalau kamu yang bikin..." #1 RAG

Gaya: "you could have invented it". Durasi target 65-70 detik, sekitar 175 kata narasi.

| Detik | Narasi | Visual (Manim) |
| --- | --- | --- |
| 0-3 | Kamu mau AI yang bisa jawab soal dokumen kantormu. | Teks besar "Kalau kamu yang bikin... #1". Ikon PDF tebal dan ikon AI. |
| 3-7 | Masalahnya, AI nggak pernah baca dokumenmu. Jadi dia nebak. | AI menjawab, lalu stempel merah "NGARANG". |
| 7-14 | Oke, gampang. Tempel aja seluruh PDF ke chat. | PDF 200 halaman masuk ke kotak chat, kotaknya menggembung. |
| 14-21 | Tapi... kepanjangan. Boros token, lambat, dan AI-nya malah gagal fokus. | Penghitung token naik cepat, angka jadi merah. |
| 21-28 | Jadi kamu potong dokumennya jadi bagian kecil-kecil. | PDF terbelah jadi banyak kartu kecil. Label: "chunk". |
| 28-35 | Tapi... dari ratusan potongan, mana yang harus dikirim? | Kartu-kartu berserakan, tanda tanya di atasnya. |
| 35-45 | Jadi tiap potongan kamu ubah jadi deretan angka yang mewakili maknanya. Potongan yang maknanya mirip, angkanya juga berdekatan. | Kartu berubah jadi titik di peta 2D. Titik yang mirip berkumpul. Label: "embedding". |
| 45-52 | Sekarang pertanyaanmu juga diubah jadi angka, lalu kamu ambil tiga potongan yang paling dekat. | Titik pertanyaan muncul, tiga titik terdekat menyala. Label: "retrieval". |
| 52-60 | Terakhir, tempel tiga potongan itu ke pertanyaan, baru kirim ke AI. Sekarang dia jawab pakai contekan yang benar. | Tiga kartu + pertanyaan masuk ke AI. Jawaban muncul dengan rujukan "hal. 47". |
| 60-65 | Selamat. Kamu baru aja bikin RAG: Retrieval-Augmented Generation. | Teks "RAG" muncul, tiga label tadi tersusun jadi diagram. |
| 65-70 | Tapi tunggu, kenapa token bisa semahal itu? Itu di part dua. | Penghitung token berkedip. Teks "#2 Tokenizer". |

## Catatan

- Kata "tapi" dan "jadi" sengaja diberi jeda dan penekanan; itu open loop kecil di tiap beat.
- Batas analogi: angka embedding mengukur kemiripan makna, bukan kata yang sama persis. Kalau ada ruang, sebut satu kalimat di detik 35-45.
- Caption di layar cukup kata kunci: "chunk", "embedding", "retrieval", "RAG".
- Caption postingan: "Kalau kamu yang bikin AI yang bisa baca dokumenmu, kamu bakal nemuin RAG sendiri. #RAG #AI #ChatGPT #belajarAI"
