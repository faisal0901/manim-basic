# Naskah A "Kalau kamu yang bikin...": temperature

Status: **dirender v1** (27 Nov 2026), disetujui Faisal ("boleh coba buat"). Durasi render sekitar 77 detik. Adegan 9 dipecah dua di layar (catatan, lalu tips).
Gaya A. 9:16, target sekitar 74 detik, sekitar 184 kata narasi. **Tanpa teaser part berikutnya.**

## Info video
- **Judul kerja:** Kenapa jawaban AI beda-beda tiap ditanya?
- **Satu ide:** AI milih kata berikutnya dengan mengundi kandidat yang punya peluang masing-masing; temperature ngatur seberapa "rata" undiannya.
- **Open loop:** "Pertanyaannya sama, kok hasilnya beda?" Dijawab di adegan 5.
- **Kasus (relate, bukan kantor):** minta AI bikin nama usaha kopi, coba 3 kali, hasilnya beda.
- **Analogi (satu):** toples undian. Tiap kandidat kata ditulis di kertas, makin besar peluangnya makin banyak kertasnya. Batasnya disebut di adegan 8: AI nggak beneran ngambil kertas, semuanya hitungan angka.
- **Istilah, dijelaskan dulu baru dinamai:** token (adegan 2) → probabilitas (adegan 3) → temperature (adegan 6).
- **Payoff:** tips kapan rendah vs tinggi, plus tips buat pengguna aplikasi chat yang nggak bisa geser kenopnya.

## Kunci warna
LANGIT pertanyaan kamu · TOSKA jawaban AI · KUNYIT kertas/kandidat yang lagi terpilih (1 per layar) · JINGGA angka persen & nilai temperature · DAUN konsisten/cocok · SAGA "sama semua" dan "ngawur".

## Per adegan

| # | Detik | Narasi | Visual (Manim) | Teks layar | mark |
|---|---|---|---|---|---|
| 1 | 0-4 | Minta AI bikin nama usaha kopi, tiga kali, hasilnya beda terus. Kok bisa? | Satu balon LANGIT "bikinin nama usaha kopi dong". Di bawahnya tiga balon TOSKA muncul berurutan, tiap balon ada label kecil "coba 1 / 2 / 3": "Kopi Senja", "Kopi Pagi", "Kopi Rindu". Kata kedua tiap balon berkedip beda. Tulisan "Kok beda?" KUNYIT. | "pertanyaan sama · coba 3×" | 01_hook |
| 2 | 4-12 | Kalau kamu yang bikin AI-nya: AI nulis jawaban sepotong-sepotong. Tiap potongan kata, namanya token, ditebak satu per satu dari kiri ke kanan. | Kalimat jawaban "Kopi ▢" di tengah. Kursor/panah TOSKA bergerak **dari kiri ke kanan**, tiap potongan muncul dalam chip berlabel ("Ko", "pi", "␣")... cukup sampai "Kopi", lalu kursor berhenti di slot kosong berlabel "kata berikutnya?". Label kecil "token = potongan kata". | "token = potongan kata" · "kata berikutnya?" | 02_token |
| 3 | 12-21 | Tapi... setelah "Kopi", banyak kata yang masuk akal. Jadi AI kasih tiap kandidat nilai peluang, seberapa cocok kata itu. Namanya probabilitas. | Dari slot "kata berikutnya?" turun daftar kandidat. Batang horizontal tumbuh **dari atas ke bawah** satu per satu, tiap batang berlabel kata + persen JINGGA: Senja 40%, Pagi 25%, Rindu 15%, Hangat 10%, Obeng 5%, lainnya 5%. Pojok: "angka contoh". | "probabilitas = peluang" · "angka contoh" | 03_probabilitas |
| 4 | 21-29 | Tapi kalau selalu ambil yang teratas, semua orang dapat "Kopi Senja". Membosankan. Jadi, kandidat diundi, kayak ambil kertas dari toples. | Tiga avatar LANGIT berlabel "kamu", "temanmu", "orang lain", semuanya dapat balon "Kopi Senja" → cap SAGA "sama semua". Lalu batang-batang "berubah" jadi kertas-kertas kecil yang jatuh ke toples. Tiap kertas bertuliskan katanya. | "selalu teratas = sama semua" | 04_toples |
| 5 | 29-37 | Yang peluangnya besar, kertasnya lebih banyak. Makanya tiap coba hasilnya bisa beda. Tapi... sesekali yang keambil kata aneh, kayak "Kopi Obeng". | Toples berisi 20 kertas: Senja 8, Pagi 5, Rindu 3, Hangat 2, Obeng 1, lainnya 1. Tangan/penjepit mengambil satu kertas, kertas terpilih KUNYIT, masuk ke slot: "coba 1: Senja", "coba 2: Pagi", "coba 3: Senja", "coba 4: Rindu". Lalu "coba 5: **Obeng**" → balon "Kopi Obeng" ditandai SAGA "ngawur". | "1 kertas = 5% · angka contoh" · "ngawur" | 05_undi |
| 6 | 37-48 | Jadi kamu kasih satu kenop buat ngatur seberapa rata isi toplesnya. Namanya temperature. Rendah: hampir semua kertas kandidat teratas, jawabannya konsisten. Tinggi: makin rata, lebih kreatif, tapi gampang ngawur. | Penggeser horizontal berlabel "temperature", angka JINGGA. Geser ke **kiri** ke 0,3: batang menajam (Senja 80%, Pagi 17%, Rindu 3%, sisanya ≈0%), toples hampir penuh "Senja", label DAUN "konsisten". Geser ke **kanan** ke 1,6: batang meratakan diri (31 / 23 / 17 / 13 / 8 / 8%), toples campur, label SAGA "kreatif · bisa ngawur". | "temperature" · "0,3 · 1,6 = angka contoh" | 06_kenop |
| 7 | 48-55 | Fakta, kode, ringkasan: pakai rendah. Ide nama, caption, brainstorming: pakai tinggi. | Dua kolom. Kiri "rendah" (DAUN) berisi chip: "fakta", "kode", "ringkasan". Kanan "tinggi" (TOSKA) berisi chip: "ide nama", "caption", "brainstorming". Penggeser kecil di atas tiap kolom. | "rendah → konsisten" · "tinggi → variasi" | 07_kapan |
| 8 | 55-61 | Selamat, kamu baru aja bikin temperature. Bedanya, AI nggak beneran ngambil kertas, semuanya hitungan angka. | "Selamat." + "temperature" KUNYIT besar. Toples memudar jadi deretan angka persen (batasan analogi). | "Selamat, kamu baru aja bikin temperature" | 08_selamat |
| 9 | 61-74 | Catatannya: di aplikasi chat, temperature diatur penyedianya, dan sebagian model terbaru malah ngunci nilainya. Temperature nol pun nggak selalu sama persis. Mau konsisten? Kasih instruksi jelas. Mau variasi? Minta sepuluh opsi sekaligus. | Kenop dengan gembok kecil berlabel "diatur penyedia". Lalu dua balon LANGIT contoh: "jawab singkat, format: nama + alasan" (DAUN "konsisten") dan "kasih 10 ide nama usaha kopi" → daftar 10 nama pendek (TOSKA). | "di aplikasi chat: diatur penyedia" · "temperature 0 ≠ selalu identik" | 09_tips |

**Jumlah kata narasi:** sekitar 184.

## Angka di layar
- Peluang awal 40 / 25 / 15 / 10 / 5 / 5% dan nilai temperature 0,3 dan 1,6 = **angka contoh**, ditulis "angka contoh" di layar.
- Batang setelah kenop digeser dihitung pakai rumus temperature yang sebenarnya (peluang dipangkatkan 1/T lalu dinormalkan), jadi bentuk perubahannya jujur walau angka awalnya contoh.
- 20 kertas di toples = 1 kertas per 5%.

## Fakta yang dipakai (dicek 27 Nov 2026, dokumentasi resmi)
- Anthropic, [Glossary](https://platform.claude.com/docs/en/about-claude/glossary): temperature mengatur keacakan prediksi; tinggi lebih kreatif dan beragam, rendah lebih konservatif. "Even with temperature set to 0, the results will not be fully deterministic, and identical inputs might produce different outputs across API calls."
- Anthropic, [Migrating to API version 2026-10-21](https://platform.claude.com/docs/en/api/migration-2026-10-21): di versi API itu, mengirim `temperature`, `top_p`, atau `top_k` ditolak (error 400); tanpa parameter dipakai default, termasuk temperature 1.0. Claude 4.7 dan model setelahnya sudah hanya menerima nilai default.
- OpenAI, [panduan model terbaru](https://developers.openai.com/api/docs/guides/latest-model): untuk model terbaru, `temperature` dan `top_p` disuruh dihilangkan dari request. (Bagian ini terbaca lewat ringkasan alat, bukan kutipan langsung. Perlu dicek ulang kalau mau dikutip.)
- Jadi kalimat "sebagian model terbaru malah ngunci nilainya" didukung dua penyedia. Google (Gemini) tidak berhasil dicek dari halaman resminya, jadi tidak disebut.

## Batas analogi & penyederhanaan
- Toples = gambaran. Aslinya AI menghitung angka skor untuk semua token di kosakatanya (puluhan ribu), lalu diubah jadi peluang.
- Kandidat di layar ditampilkan sebagai kata utuh, padahal yang ditebak token (bisa potongan kata). Adegan 2 sudah bilang token = potongan kata, jadi ini disederhanakan.
- Di aplikasi chat, jawaban beda juga bisa karena hal lain (memori, pencarian web, versi model). Video cuma bahas faktor undian.
- Ada pengatur lain selain temperature (top-p, top-k) yang memangkas kandidat ekor. Tidak dibahas supaya satu ide.

## Tebakan / perlu konfirmasi
- Nama "Kopi Senja/Pagi/Rindu/Hangat" dipilih generik, bukan merek besar (sengaja menghindari Kopi Kenangan, Janji Jiwa, Tuku). Tetap bisa kebetulan sama dengan kedai kecil.
- "Kopi Obeng" sebagai contoh ngawur yang lucu. Bisa diganti.
- Tips pengguna biasa ("minta 10 opsi", "kasih instruksi jelas") itu saran praktis, bukan dari dokumentasi.
- Durasi 74 detik, mepet batas 75. Kalau kepanjangan, adegan 4 bagian "semua orang dapat Kopi Senja" bisa dipersingkat.

## Caption usulan
```
Kenapa jawaban AI beda-beda padahal pertanyaannya sama? Kalau kamu yang bikin, kamu bakal nemu "temperature" sendiri.
#AI #ChatGPT #belajarAI #temperature
```
