# Catatan video-token-v1

## Isi folder
| File | Isi |
|---|---|
| `TOKEN_B_hook_vertical.mp4` | Video final 9:16, 1080x1920, 60 fps, 70,4 dtk, tanpa suara |
| `token_hook.py` | Kode Manim, kelas `TokenHook` (gaya B) |
| `naskah_B_hook.md` | Naskah per adegan + tabel data token |
| `naskah_narasi_rekam.md` | Naskah untuk rekam suara, dengan tanda jeda dan tekanan |
| `naskah_A_kalau_kamu_bikin.md` | Varian gaya A, naskah saja (belum dirender) |
| `preview/vertical/B_*.png`, `preview/ringkasan_B.png` | Frame kunci dan lembar ringkasan |
| `data/hasil_tokenizer.txt`, `data/cek_token.mjs` | Hasil mentah dan skrip tokenizer |

Render ulang (dari folder ini; `theme.py` dicari otomatis di `design-system/` root repo):
```bash
STILLS=1 ORIENT=vertical manim -s -ql token_hook.py TokenHook   # frame kunci
ORIENT=vertical manim -qh token_hook.py TokenHook               # final
```
Cek ulang token: `npm i js-tiktoken` lalu `node data/cek_token.mjs`.

## Fakta (sudah dicek)
- Semua pecahan dan nomor token dihasilkan sungguhan dengan js-tiktoken 1.0.21 (port resmi tiktoken ke JavaScript), encoding `o200k_base` (GPT-4o) dan `cl100k_base` (GPT-4 / GPT-3.5), 26 Nov 2026. Tiktoken Python tidak bisa mengunduh file encoding dari cloud ini (host diblokir), jadi dipakai port JS yang membawa file encoding di paketnya. Hasilnya sama karena memakai file encoding yang sama.
- " strawberry" (dengan spasi depan, seperti di dalam kalimat) = 1 token di kedua tokenizer. "strawberry" sendirian = 3 token, pecahannya beda per model.
- Tokenizer model lain (Claude, Gemini, Llama) tidak dicek dan bisa memecah berbeda. Di layar ditulis "Beda model, beda pecahan".

## Tebakan dan penyederhanaan (perlu konfirmasi)
- **Nomor seri:** video ini saya beri label "#2 · Tokenizer" karena video A menjanjikan "#2 Tokenizer". Teasernya ke "#3 Embedding" (urutan seri di BRIEF_KONTEN.md, masih usulan).
- **Jawaban "kenapa token semahal itu":** dijawab singkat saja (token = satuan yang dihitung dan dibayar; kalimat Indonesia contoh 9 token vs Inggris 7). Tidak ada angka rupiah atau harga per token, supaya tidak perlu cek harga yang sering berubah.
- **"Banyak AI pernah jawab dua":** ini kasus viral 2024 (ChatGPT dan model lain). Model baru yang "mikir dulu" sering sudah benar; ini ditulis kecil di layar supaya hook tetap jujur.
- **"Harga AI & batas panjang chat dihitung per token":** benar untuk harga API dan batas konteks. Langganan ChatGPT biasa tidak bayar per token secara langsung; kalimat ini menyederhanakan.
- **"Dipilih dari potongan yang paling sering muncul":** penyederhanaan dari BPE (gabung pasangan yang paling sering muncul di teks latihan).
- **Tips eja pakai spasi:** pecahan 10 token itu fakta; klaim "AI jauh lebih gampang ngitung" masuk akal dan umum dipakai, tapi tidak dijamin selalu benar di semua model. Jawaban "Ada 3." di layar adalah ilustrasi.
- **Selisih Indonesia vs Inggris:** contoh satu kalimat (9 vs 7 di GPT-4o, 12 vs 7 di GPT-4). Kalimat lain bisa beda selisihnya; ditulis di layar.
- **Warna blok token:** bergantian LANGIT, UNGU, merah muda, biru dari daftar `KATEGORI` di theme.py. Sengaja tanpa DAUN/SAGA/KUNYIT supaya tidak bentrok dengan makna warna. Palet tidak diubah.
- **Durasi 70,4 dtk:** jeda diatur untuk narasi 162 kata. Sesuaikan setelah rekam suara.
