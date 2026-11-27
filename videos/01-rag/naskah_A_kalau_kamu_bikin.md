# Naskah: "Kalau kamu yang bikin..." #1 RAG (v4, kasus CS toko online)

Gaya: "you could have invented it". Durasi sekitar 78 detik (sama dengan v3), sekitar 200 kata narasi.
Kasus: **AI customer service toko elektronik online**. Dokumen toko **500 halaman** (katalog, kebijakan garansi, retur, ongkir, FAQ). Pertanyaan pelanggan: **"Layar HP pecah, bisa garansi?"**

Kenapa kasus ini: kasus RAG perusahaan yang paling umum di dunia nyata, dan semua orang pernah jadi pelanggan yang ketemu chatbot CS. Taruhannya jelas: kalau AI ngarang soal garansi, toko yang rugi.

Angka token: 500 halaman x sekitar 500 token per halaman = **sekitar 250.000 token** (perkiraan kasar).

| Detik (kira-kira) | Narasi | Visual (Manim) |
| --- | --- | --- |
| 0-4 | Kamu mau bikin AI CS buat jawab pelanggan toko onlinemu. Dokumennya 500 halaman. | Judul "toko onlinemu." kuning, tumpukan dokumen "500 halaman", ikon AI dan tanda tanya. |
| 4-9 | Masalahnya, AI nggak pernah baca aturan tokomu. Pelanggan tanya "layar HP pecah, bisa garansi?", dia jawab "bisa, gratis!". Ngarang. Tokomu yang rugi. | Gelembung pertanyaan, AI menjawab, stempel merah "NGARANG". |
| 9-13 | Oke, gampang. Tempel aja semua dokumennya ke AI. | Label "katalog + garansi + retur + FAQ · 500 halaman", 20 ikon halaman masuk ke kotak chat. |
| 13-18 | Tapi tiap ada pertanyaan, AI harus baca semuanya dari awal, halaman demi halaman. | Kotak sorot kuning + garis pemindai menyapu halaman satu per satu; halaman yang sudah dibaca meredup; token naik 0 sampai 250.000. |
| 18-23 | Tapi... kepanjangan. Dua ratus lima puluh ribu token tiap pertanyaan. Boros, lambat, dan AI-nya gagal fokus. | "Tapi... kepanjangan.", kotak merah, pil "boros", "lambat", "gagal fokus". |
| 23-30 | Jadi kamu gunting dokumennya jadi potongan kecil-kecil. Ini namanya chunk. | Dokumen berisi kalimat nyata ("Garansi: layar pecah tak ditanggung", "Ongkir: gratis min. belanja 100rb", dst.), gunting kuning memotong tiap garis, potongan kertas terpisah. Label "chunk". |
| 30-36 | Tapi... dari ribuan potongan, mana yang harus dikirim? | Potongan berserakan, tanda tanya merah, "aslinya ada ribuan potongan". |
| 36-41 | Jadi tiap potongan kamu ubah jadi deretan angka. | "Garansi: layar pecah tak ditanggung" jadi vektor [0.12, -0.83, 0.47, …]. |
| 41-48 | Angkanya diatur supaya yang maknanya mirip letaknya berdekatan. "Rusak", "mati total", "nggak mau nyala" ngumpul. "Gratis ongkir" jauh di sana. | Peta makna: tiga kata dalam lingkaran hijau "mirip → dekat"; "gratis ongkir" & "diskon" jauh, garis merah "beda → jauh". |
| 48-53 | Potongan dokumen juga begitu. Yang ngomongin layar dan garansi ngumpul di satu sudut. | 9 titik berlabel: "layar pecah", "garansi 12 bulan", "servis layar" berdekatan; "gratis ongkir", "cicilan 0%", "retur 7 hari", "spek HP X10", "COD & transfer", "ganti password" tersebar. Label "embedding". |
| 53-60 | Sekarang pertanyaan pelanggan juga diubah jadi angka. Dia jatuh dekat potongan soal garansi. Ambil tiga yang paling dekat. | Bintang kuning dekat klaster garansi, garis ke 3 titik terdekat, sisanya meredup. "ambil 3 terdekat", label "retrieval". |
| 60-68 | Terakhir, tempel tiga potongan itu ke pertanyaan, baru kirim ke AI. Sekarang jawabannya: layar pecah karena jatuh nggak ditanggung garansi, tapi bisa servis mulai 450 ribu. Pakai contekan yang benar. | Kartu "prompt" (pertanyaan + 3 potongan) → AI → kartu jawaban hijau, "sumber: Kebijakan Garansi hal. 12". |
| 68-75 | Selamat. Kamu baru aja bikin RAG: Retrieval-Augmented Generation. | "Selamat.", "RAG", pil chunk → embedding → retrieval. |
| 75-80 | Tapi tunggu, kenapa token bisa semahal itu? Itu di part dua. | "Tapi kenapa token bisa semahal itu?", pil "#2 Tokenizer". |

## Catatan

- Batas analogi: peta 2D cuma penyederhanaan; aslinya vektor punya ratusan sampai ribuan dimensi, dan yang diukur kemiripan makna, bukan kata yang sama persis.
- Penyederhanaan: di video satu chunk = satu kalimat aturan. Di praktik biasanya satu paragraf atau beberapa ratus token.
- Nama toko tidak disebut; "HP X10", harga servis Rp450 ribu, dan "hal. 12" fiktif.
- Caption postingan: "Kalau kamu yang bikin AI CS buat toko online, kamu bakal nemuin RAG sendiri. #RAG #AI #ChatGPT #belajarAI"

## Tebakan (perlu konfirmasi)

- 500 token per halaman adalah perkiraan kasar.
- Contoh kata mirip pakai kosakata kasus (rusak / mati total / nggak mau nyala); bisa balik ke kucing / mobil kalau mau lebih universal.
