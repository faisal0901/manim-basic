# Naskah: "Bilang makasih ke ChatGPT = buang duit?" (gaya B, draf 1)

Status: **disetujui dan dirender** (27 Nov 2026), `SOPAN_B_hook_vertical.mp4`. Revisi 1: adegan 4 jadi animasi scanning. Video umum, selingan ringan, tanpa teaser.

## Info video
- **Gaya:** B hook biasa (pertanyaan lucu + kutipan nyata + angka)
- **Satu ide:** sopan ke AI memang makan token, terutama karena AI membalas, tapi per orang receh. Jadi boleh tetap sopan, dan bisa lebih hemat.
- **Analogi:** tidak perlu analogi baru; token sudah dijelaskan di video #2 (cukup "potongan kecil teks").
- **Tips:** gabung "makasih" dengan pertanyaan berikutnya, supaya tidak ada balasan ekstra.
- **Penutup lucu:** AI jahat generik (chip AI matanya merah, glitch), bukan karakter film. Tulisan "DAFTAR MANUSIA SOPAN: ✓ kamu".
- **Target:** sekitar 65 detik, sekitar 160 kata.

## Per adegan

| # | Detik | Narasi | Visual (Manim) |
|---|---|---|---|
| 1 | 0-4 | Bilang makasih ke ChatGPT itu buang duit? | Chat "makasih ya kak 🙏🙏" terkirim, penghitung token di pojok "+8". Teks besar "buang duit?" |
| 2 | 4-11 | CEO OpenAI, Sam Altman, pernah bilang sopan santun pengguna ngabisin puluhan juta dolar. Terus dia tambahin: "well spent". Uang yang nggak sia-sia. | Kartu kutipan: "tens of millions of dollars well spent — you never know" · Sam Altman, April 2025. Angka "puluhan juta dolar" JINGGA. |
| 3 | 11-19 | Kok bisa? AI ngitung semua ketikanmu dalam token, potongan kecil teks. "Makasih ya kak" plus dua emoji: delapan token. | Kalimat pecah jadi blok: mak · as · ih · ya · kak · 🙏(2 blok) · 🙏. "8 token" JINGGA. |
| 4 | 18-29 | Tapi yang mahal bukan makasihnya. Biar bisa bales, AI baca ulang seluruh obrolan dari awal. Resep seblak, curhat, skripsi… semua. Cuma buat jawab: "sama-sama". | Riwayat 8 pesan (resep seblak, curhat putus, revisi skripsi, caption IG, makasih). Sorotan kuning + garis pemindai menyapu tiap pesan dari atas, pesan yang sudah dibaca meredup, "token dibaca" naik ke 2.400 (angka contoh). Lalu AI bales "Sama-sama!" dan teks merah "…cuma buat jawab 'sama-sama'." |
| 5 | 29-38 | Per orang? Receh banget. Tapi kalikan sejuta orang yang bilang makasih. Delapan juta token, cuma buat sopan. | Satu balon jadi grid ratusan balon (zoom out), penghitung "8.000.000" JINGGA, server keringetan (ikon AI dengan tetes keringat). "hitungan contoh". |
| 6 | 38-47 | Jadi harus berhenti sopan? Nggak juga. Gabungin aja makasihnya ke pertanyaan berikutnya: "Makasih! Sekarang bikinin…". Sekali kirim, nggak ada balasan ekstra. | Header "Tips" DAUN. Dua balon terpisah digabung jadi satu balon. Balasan ekstra dicoret. |
| 7 | 47-53 | Btw, "please" cuma satu token. "Tolong" dua. Sopan pakai bahasa Inggris lebih murah. | please = 1 blok, tol · ong = 2 blok. Emoji 🤡/wajah datar opsional. |
| 8 | 53-65 | Tapi tetap sopan ya. Kata Sam Altman: you never know. | Layar meredup, chip AI berubah merah (SAGA), mata menyala, efek glitch. Teks mono: "DAFTAR MANUSIA SOPAN: ✓ kamu". Lalu AI berkedip, kembali TOSKA, "jaga-jaga." |

**Jumlah kata narasi:** sekitar 160.

## Fakta (dicek 26 Nov 2026)
- Altman menjawab pertanyaan pengguna X (April 2025) soal biaya listrik dari orang yang bilang "please" dan "thank you": "tens of millions of dollars well spent — you never know." Sifatnya jawaban santai, bukan hasil hitungan resmi. Sumber: [TechRadar](https://www.techradar.com/computing/artificial-intelligence/chatgpt-spends-tens-of-millions-of-dollars-on-people-playing-please-and-thank-you-but-sam-altman-says-its-worth-it), [Windows Central](https://www.windowscentral.com/software-apps/please-and-thank-you-to-chatgpt-worth-it-ceo-jokes), [Cointelegraph](https://cointelegraph.com/news/being-polite-chatgpt-costing-openai-millions-says-sam-altman).
- Token asli, tokenizer GPT-4o (o200k_base, js-tiktoken):
  - "makasih ya kak 🙏🙏" = 8 token: mak · as · ih · ␣ya · ␣kak · (🙏 pertama terpecah 2 token) · 🙏
  - "please" = 1 token, "tolong" = 2 token (tol · ong), "thank you" = 2, "terima kasih" = 3

## Tebakan / perlu konfirmasi
- "Sejuta orang" dan 8 juta token = **hitungan contoh** (8 × 1.000.000), bukan data pengguna asli.
- "AI baca ulang obrolan dari awal": benar secara konsep (riwayat chat ikut dikirim sebagai input tiap giliran). Layanan seperti ChatGPT bisa memakai cache sehingga biayanya lebih murah; tidak dibahas supaya tetap satu ide.
- AI jahat sengaja generik (chip KAPUR versi merah), bukan karakter film tertentu, supaya aman hak cipta.
- Caption: "Bilang makasih ke ChatGPT itu buang duit? Kata CEO-nya: puluhan juta dolar. #AI #ChatGPT #token #belajarAI"
