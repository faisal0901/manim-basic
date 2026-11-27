# Naskah rekam suara: prompt caching (gaya A)

Baca santai, sekitar 2,5 kata per detik. Sekitar 195 kata, target sekitar 78 detik.
`/` = jeda pendek. `//` = jeda panjang (ganti visual). **Tebal** = tekan.

---

**[0:00]** Tiap pembeli nanya "masih ready kak?", / bot CS tokomu baca ulang **tiga ribu token** aturan toko. / Dari **nol**. //

**[0:05]** Kalau **kamu** yang bikin AI-nya: / tiap pertanyaan, / aturan toko dikirim bareng, / dan GPU, / chip tukang hitung di server, / ngubah tiap token jadi tumpukan **angka**. //

**[0:14]** **Tapi...** / aturannya sama terus. / Seratus pembeli, / seratus kali dihitung ulang. / **Jadi**, / simpan aja angka hasil hitungannya / di memori GPU. //

**[0:22]** Pertanyaan berikutnya datang, / tinggal pakai yang **tersimpan**. / Cuma pertanyaan barunya yang dihitung. //

**[0:28]** **Tapi...** / gimana tahu awalnya sama? / **Jadi** CPU, / si manajer server, / bikin sidik tiap blok / dan nyocokin **dari awal**. / Beda satu kata di depan, / semua setelahnya dihitung ulang. / Yang tetap di **depan**, / yang berubah di **belakang**. //

**[0:40]** **Tapi...** / memori GPU terbatas. / **Jadi** simpanannya **sementara**. / Contohnya lima menit, / diperpanjang tiap dipakai. //

**[0:47]** **Selamat**, / kamu baru aja bikin **prompt caching**. / Di salah satu penyedia, / baca dari cache cuma **sepersepuluh** harga. //

**[0:54]** Tapi **hati-hati**. / Nyimpennya justru lebih mahal, / satu koma dua lima kali. / Misal kamu taruh **jam** / di baris pertama aturan, / biar bot tahu waktu. / Tiap detik, / awalnya beda. / Cache **ditulis** terus, / nggak pernah **kebaca**. / Bayar lebih, / hemat nol. //

**[1:06]** Sama kalau tokomu **sepi**: / jeda pembeli lebih dari lima menit, / simpanannya keburu hilang. //

**[1:11]** Jadi jam taruh di **belakang**, / dan cek laporan pemakaian: / kalau "cache read" **nol** terus, / cache-mu cuma ditulis.
