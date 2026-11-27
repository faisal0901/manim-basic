# Naskah varian: "Kalau kamu yang bikin… #2 Tokenizer" (gaya A, belum dirender)

Hanya naskah, untuk dibandingkan dengan versi B (`naskah_B_hook.md`). Isi, data token, tips, dan teaser sama; yang beda cara bercerita.
Perkiraan sekitar 70 detik, 172 kata. Semua pecahan dari tokenizer GPT-4o (o200k_base), lihat `data/hasil_tokenizer.txt`.

| Detik (kira-kira) | Narasi | Visual (Manim) |
|---|---|---|
| 0-4 | Kamu mau bikin AI yang bisa baca chat. Masalahnya, komputer cuma ngerti angka. | Judul "Kalau kamu yang bikin… #2". Gelembung chat LANGIT, ikon AI TOSKA, tanda tanya. |
| 4-11 | Gampang. Tiap huruf kamu kasih nomor. a satu, b dua, dan seterusnya. | Huruf "s t r a w b e r r y" turun satu-satu, tiap huruf dapat nomor JINGGA. |
| 11-17 | Tapi… kalimat jadi panjang banget. Satu huruf, satu langkah. AI-mu lambat dan susah nangkep makna. | "Tapi…" SAGA. Deretan nomor memanjang keluar layar, penghitung naik. |
| 17-24 | Jadi tiap kata kamu kasih nomor. Lebih pendek. | Kata utuh jadi blok: "strawberry" satu nomor. |
| 24-31 | Tapi… kata di dunia ada jutaan. Typo, nama baru, "wkwkwk". Nggak punya nomor. | "Tapi…" SAGA. Kata "wkwkwk", "stroberiii" mental dari kamus, stempel "TIDAK DIKENAL". |
| 31-41 | Jadi kamu ambil tengahnya. Potongan yang sering muncul dapat satu nomor. Kata umum tetap utuh. Kata panjang atau jarang dipecah. | "mempertanggungjawabkan" dipotong jadi mem · pert · anggung · jaw · ab · kan (6 blok). "strawberry" di kalimat tetap 1 blok. |
| 41-45 | Potongan ini namanya token. | Label "token". |
| 45-53 | Tapi… ada efek sampingnya. AI-mu nggak pernah lihat huruf. Tanya "ada berapa r di strawberry?", dia cuma lihat satu nomor. | "Tapi…" SAGA. Pertanyaan jadi blok, " strawberry" → 101830 KUNYIT. AI jawab "2", stempel SALAH. |
| 53-59 | Makanya kalau mau dia ngitung, eja pakai spasi. Satu huruf, satu token. | "s t r a w b e r r y" → 10 blok, tiga r kuning. AI jawab "3". |
| 59-65 | Selamat. Kamu baru aja bikin tokenizer. Dan token inilah yang dihitung dan dibayar: kalimat Indonesia sering butuh lebih banyak token. | "Selamat.", "Tokenizer" DAUN. Baris kecil: Indonesia 9 token vs Inggris 7 token. |
| 65-70 | Tapi kalau AI cuma lihat nomor, gimana dia tahu dua kalimat artinya mirip? Itu di part tiga. | "artinya mirip?" KUNYIT, pil "#3 Embedding". |

## Catatan
- Analogi pada versi ini: tidak ada analogi suku kata. Penonton "menemukan" token lewat rantai huruf → kata → potongan. Ini sesuai pola gaya A.
- "a satu, b dua" hanya ilustrasi; nomor token asli tidak urut alfabet (mis. "s" = 82). Sebut "contoh" kalau perlu.
- Penyederhanaan: tokenizer asli (BPE) dibangun dengan menggabungkan pasangan potongan yang paling sering muncul di teks latihan, berulang kali. Istilah BPE tidak disebut supaya tetap satu istilah baru.
- Kalau mau direnderkan, butuh adegan baru (huruf bernomor, kamus kata, stempel "TIDAK DIKENAL"); komponen blok token dan nomor bisa dipakai ulang dari `token_hook.py`.
