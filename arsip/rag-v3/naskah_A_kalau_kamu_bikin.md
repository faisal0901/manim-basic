# Naskah: "Kalau kamu yang bikin..." #1 RAG (v3)

Gaya: "you could have invented it". Durasi video sekitar 80 detik, sekitar 200 kata narasi.
Kasus baru: **riwayat grup chat alumni, 20.000 pesan**, pertanyaan **"Reuni jadinya kapan?"**.

Kenapa kasus ini: hampir semua orang punya grup chat yang info pentingnya tenggelam di ribuan pesan, dan malas scroll. Isinya pribadi, jadi masuk akal AI nggak pernah membacanya. Gampang divisualkan (balon chat, potongan pesan). Kasus lain yang ditimbang: modul kuliah (kurang cocok karena AI sering sudah tahu materi umum), syarat & ketentuan panjang (relate, tapi teksnya membosankan di layar), laporan tahunan (kurang relate untuk penonton umum).

Angka token: 20.000 pesan x sekitar 12 token per pesan = **sekitar 250.000 token** (tebakan kasar; pesan bahasa Indonesia rata-rata 8 kata).

| Detik (kira-kira) | Narasi | Visual (Manim) |
| --- | --- | --- |
| 0-4 | Kamu mau AI yang bisa jawab soal isi grup chat-mu. Dua puluh ribu pesan. | Judul "grup chat-mu." kuning, tumpukan chat "20.000 pesan", ikon AI dan tanda tanya. |
| 4-9 | Masalahnya, AI nggak pernah baca chat grupmu. Kamu tanya "reuni jadinya kapan?", dia jawab "Minggu, 21 Des". Ngarang. | Gelembung pertanyaan, AI menjawab, stempel merah "NGARANG". |
| 9-13 | Oke, gampang. Tempel aja seluruh chat-nya ke AI. | File "chat_grup.txt · 20.000 pesan" (20 kartu chat) masuk ke kotak chat. |
| 13-18 | Tapi tiap kali kamu nanya, AI harus baca semuanya dari awal, satu per satu. | Kotak sorotan kuning + garis pemindai menyapu kartu satu per satu dari atas ke bawah; kartu yang sudah dibaca meredup; angka token naik dari 0 ke 250.000 (oranye lalu merah). |
| 18-23 | Tapi... kepanjangan. Dua ratus lima puluh ribu token tiap pertanyaan. Boros, lambat, dan AI-nya gagal fokus. | "Tapi... kepanjangan.", kotak jadi merah, pil "boros", "lambat", "gagal fokus". |
| 23-30 | Jadi kamu gunting chat-nya jadi potongan kecil-kecil. Ini namanya chunk. | Riwayat chat jadi kertas berisi pesan nyata ("Rina: Fix ya, reuni Sabtu 14 Des!", "Dodi: Ada yang jual motor bekas?", dst.). Garis potong putus-putus, gunting menyusuri tiap garis, potongan kertas terpisah. Label "chunk". |
| 30-36 | Tapi... dari ribuan potongan, mana yang harus dikirim? | Guntingan kertas berserakan, tanda tanya merah, "aslinya ada ribuan potongan". |
| 36-41 | Jadi tiap potongan kamu ubah jadi deretan angka. | Potongan "Rina: Fix ya, reuni Sabtu 14 Des!" berubah jadi vektor [0.12, -0.83, 0.47, …]. |
| 41-48 | Angkanya diatur supaya kata yang maknanya mirip letaknya berdekatan. "Kucing", "anak kucing", "kucing oren" ngumpul. "Mobil" jauh di sana. | Peta makna: tiga titik kucing dalam lingkaran hijau "mirip → dekat"; mobil & motor di pojok lain, garis merah "beda → jauh". Teks "makna mirip = posisi berdekatan". |
| 48-53 | Potongan chat juga begitu. Semua yang ngomongin reuni ngumpul di satu sudut. | 9 potongan jadi titik berlabel: "reuni Sabtu 14 Des", "Kafe Senja", "jam 7 malam" berdekatan; "jual motor", "resep rendang", "loker admin", "ucapan ultah", "link zoom", "foto liburan" tersebar. Label "embedding". |
| 53-60 | Sekarang pertanyaanmu juga diubah jadi angka. Dia jatuh dekat potongan soal reuni. Ambil tiga yang paling dekat. | "Reuni jadinya kapan?" jadi bintang kuning di dekat klaster reuni; garis putus ke 3 titik terdekat, label hijau; sisanya meredup. "ambil 3 terdekat", label "retrieval". |
| 60-68 | Terakhir, tempel tiga potongan itu ke pertanyaan, baru kirim ke AI. Sekarang dia jawab: Sabtu, 14 Desember, jam 7 malam, di Kafe Senja. Pakai contekan yang benar. | Kartu "prompt" berisi pertanyaan + 3 potongan, panah ke AI, kartu jawaban hijau "Sabtu, 14 Des, jam 7 malam di Kafe Senja. sumber: chat Rina & Budi". |
| 68-75 | Selamat. Kamu baru aja bikin RAG: Retrieval-Augmented Generation. | "Selamat.", "RAG" besar, pil chunk → embedding → retrieval. |
| 75-80 | Tapi tunggu, kenapa token bisa semahal itu? Itu di part dua. | "Tapi kenapa token bisa semahal itu?", pil "#2 Tokenizer". |

## Catatan

- Kata "tapi" dan "jadi" tetap diberi jeda dan penekanan; itu open loop kecil di tiap beat.
- Batas analogi: titik di peta 2D cuma penyederhanaan. Aslinya vektor punya ratusan sampai ribuan dimensi, dan yang diukur kemiripan makna, bukan kata yang sama persis.
- Penyederhanaan: di video, satu chunk = satu pesan. Di praktik, satu chunk biasanya berisi beberapa pesan atau beberapa paragraf.
- Nama di chat (Rina, Budi, Dodi, Tari, Andi, Sari, Yoga) dan Kafe Senja fiktif.
- Caption postingan: "Kalau kamu yang bikin AI yang bisa baca ribuan chat grupmu, kamu bakal nemuin RAG sendiri. #RAG #AI #ChatGPT #belajarAI"

## Tebakan (perlu konfirmasi)

- Kasus grup chat alumni + pertanyaan reuni dipilih sendiri; kalau mau, bisa diganti grup kelas ("deadline tugas kelompok kapan?") dengan kode yang sama (cukup ubah daftar `POTONGAN` di rag_v3.py).
- Angka 250.000 token dan 12 token per pesan adalah perkiraan kasar.
- Teks di layar memakai kata "grup chat", bukan merek aplikasi tertentu.
