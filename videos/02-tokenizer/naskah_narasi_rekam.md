# Naskah rekam suara: #2 Tokenizer (gaya B)

Baca santai, sekitar 2,5 kata per detik. Total 162 kata, target sekitar 70 detik.
`/` = jeda pendek. `//` = jeda panjang (ganti visual). **Tebal** = tekan.

---

**[0:00]** Tanya AI: / ada berapa huruf **r** di **strawberry**? / Banyak AI pernah jawab: / **dua**. / Padahal **tiga**. //

**[0:06]** Ini bukan karena AI bodoh. / AI memang **nggak baca huruf**. //

**[0:12]** Sebelum dibaca, / teks **dipotong** dulu. / Mirip kita baca per suku kata. /
Potongan ini namanya **token**. / Pemotongnya disebut **tokenizer**. //

**[0:23]** Bedanya, / potongannya bukan suku kata beneran. / "Berapa" jadi "ber" dan "apa". / Dipilih dari potongan yang paling sering muncul. //

**[0:28]** Dan strawberry? / **Utuh**, / satu token. //

**[0:29]** Lalu tiap token diganti **nomor**. / Yang sampai ke AI / cuma deretan nomor ini. /
Strawberry jadi **satu nomor**. / Huruf r-nya / di mana? //

**[0:39]** Pecahannya **beda tiap model**. / GPT-4o motong jadi / st, / raw, / berry. / GPT-4 lain lagi. / Tetap potongan, / bukan huruf. //

**[0:46]** **Tipsnya**: / kalau mau AI hitung huruf, / pisah hurufnya pakai **spasi**. / Sekarang satu huruf, / satu token. / AI jauh lebih gampang ngitung. //

**[0:55]** Dan token ini juga yang **dihitung dan dibayar**. / Kalimat Indonesia ini / **sembilan** token. / Versi Inggrisnya / **tujuh**. / Makin banyak token, / makin **mahal**. //

**[1:04]** **Tapi** / kalau AI cuma lihat nomor, / gimana dia tahu dua kalimat **artinya mirip**? / Itu di part tiga.

---

Catatan: rekam dulu, ukur durasi per bagian, lalu sesuaikan `self.wait(...)` per adegan di `token_hook.py` (baris yang berisi `JEDA + ...`). Waktu tiap bagian dicetak saat render (`[waktu] ...`).
