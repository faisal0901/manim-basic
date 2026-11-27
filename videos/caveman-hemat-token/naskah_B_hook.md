# Naskah: "Caveman hemat token? Iya, tapi…" (gaya B, draf 1)

Status: **disetujui dan dirender** (26 Nov 2026), `CAVEMAN_B_hook_vertical.mp4`. Video umum (bukan bagian seri bernomor), tanpa teaser.

## Info video
- **Gaya:** B hook biasa (klaim + angka). Gantian: #2 B, #3 A, ini B.
- **Satu ide:** caveman memangkas jawaban yang kamu baca, bukan "coretan mikir" (reasoning) model, padahal coretan itu juga dihitung dan dibayar.
- **Open loop:** klaim hemat 65% itu bener nggak?
- **Analogi + batas:** reasoning = coretan di kertas buram sebelum nulis jawaban di lembar ujian. Bedanya, kertas buram AI bisa ribuan token, sering disembunyikan, tapi tetap dihitung.
- **Istilah baru:** reasoning (token mikir)
- **Tips praktis:** buat tugas gampang, turunkan level mikir (mode mikir rendah / model tanpa reasoning). Itu yang memotong kertas buramnya.
- **Target:** sekitar 70 detik, sekitar 175 kata.

## Per adegan

| # | Detik | Narasi | Visual (Manim) |
|---|---|---|---|
| 1 | 0-4 | Ada plugin viral yang bikin AI ngomong kayak manusia gua. Klaimnya: hemat 65% token. | Pertanyaan "Gaji 2 juta, makan sebulan gimana?". Balon AI biasa (panjang) vs caveman "Telur. Tempe. Sayur. Muat." Angka besar "−65% token?" JINGGA. |
| 2 | 4-7 | Dan itu bener. Tapi cuma separuh cerita. | "Bener." DAUN, lalu "…separuh cerita." KUNYIT. |
| 3 | 7-14 | Angka 65% itu dihitung dari jawaban yang kamu baca. Contoh dari pembuatnya: jawaban biasa 69 token, versi caveman 19. | Dua batang: 69 vs 19 token. Label "token output (jawaban)". |
| 4 | 14-24 | Masalahnya, banyak AI sekarang mikir dulu sebelum jawab. Mirip kamu nyoret-nyoret di kertas buram sebelum nulis di lembar ujian. Coretan ini namanya reasoning. | Kertas buram "AI lagi mikir…": teks muncul huruf per huruf: "hmm… gaji 2 juta sebulan", "dibagi 30… 66rb sehari", "belum kos, bensin, cicilan…", "ayam tiap hari?" dicoret (kemahalan), "salmon?" dicoret (mimpi), "oke: telur, tempe, sayur, sesekali ayam. cek total… pas ✓". Penghitung token mikir naik ke 3.000. Lalu lembar jawaban caveman muncul. |
| 5 | 24-31 | Bedanya, kertas buram AI bisa ribuan token, dan sering nggak ditampilkan. Tapi tetap dihitung. Tetap dibayar. | Kertas buram memanjang ke bawah, lalu meredup ("disembunyikan"), penghitung token tetap jalan. |
| 6 | 31-42 | Caveman cuma motong lembar jawabannya. Kertas buramnya utuh. Contoh: mikir 3.000, jawab 1.200. Pakai caveman: mikir tetap 3.000, jawab 300. Hematnya bukan 65%, cuma sekitar 21%. | Batang bertumpuk: reasoning (besar) + jawaban. Hanya bagian jawaban yang menyusut. Angka "−21%" JINGGA. Catatan "angka contoh". |
| 7 | 42-50 | Plus, instruksi caveman-nya sendiri nambah sekitar seribu token input tiap giliran. | Kotak kecil "+~1.000 token input" masuk di depan batang. |
| 8 | 50-57 | Pembuatnya sendiri jujur: yang dipotong cuma output. Reasoning dan input nggak kesentuh. Di jawaban yang udah pendek, bisa malah rugi. | Kutipan pendek dari README di kartu, tiga baris centang/silang. |
| 9 | 57-65 | Tipsnya: buat tugas gampang, turunkan level mikirnya. Pakai mode mikir rendah, atau model tanpa reasoning. Itu yang motong kertas buramnya. | Tombol/slider "mikir: tinggi → rendah", kertas buram menipis. DAUN. |
| 10 | 65-70 | Caveman bikin jawaban enak dibaca. Tapi soal hemat, yang mahal sering bukan jawabannya. Tapi mikirnya. | Kalimat penutup, "mikirnya." KUNYIT. |

## Fakta (dari sumber, dicek 26 Nov 2026)
- README caveman: "Same answers, 65% fewer output tokens"; rata-rata 65% dari 10 prompt (rentang 22–87%), "Output tokens only". Contoh jawaban 69 token vs 19 token.
- README caveman (kotak "Important"): "Caveman only shrinks output tokens. Input and reasoning tokens are untouched, and the skill itself adds ~1–1.5k input tokens per turn."
- README juga menyebut penghematan satu sesi lebih kecil dari angka output, dan di pekerjaan yang sudah ringkas "can go net-negative".
- Token reasoning/thinking dihitung sebagai token output saat penagihan (Claude extended thinking, model reasoning OpenAI). Perlu dicek ulang ke halaman harga sebelum final.

Sumber: [ClaudePluginHub: caveman](https://www.claudepluginhub.com/plugins/juliusbrussee-caveman), [README (fork) caveman](https://github.com/Sandy4321/caveman-july2026), [DEV: Caveman mode for Claude Code](https://dev.to/ahmad_dogar_7d098f5e48f72/caveman-mode-for-claude-code-fewer-output-tokens-same-facts-27l6), [Mayhemcode](https://www.mayhemcode.com/2026/04/caveman-claude-code-how-to-save-tokens.html)

## Tebakan / perlu konfirmasi
- Angka 3.000 mikir + 1.200 jawab adalah **contoh fiktif** untuk menunjukkan proporsi; rasio nyata beda-beda per tugas dan model.
- README yang terbaca adalah fork dari repo asli juliusbrussee/caveman; angkanya sama dengan yang dikutip halaman lain.
- Nama "caveman" disebut langsung. Nadanya adil: klaimnya diakui benar untuk output, dan keterbatasannya diambil dari pengakuan pembuatnya sendiri.
- Caption: "Caveman hemat 65% token? Iya, tapi cuma jawabannya. Reasoning tetap dibayar. #AI #ClaudeCode #ChatGPT #token #belajarAI"
