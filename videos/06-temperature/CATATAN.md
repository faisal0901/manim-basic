# Catatan video temperature v1 (gaya A)

- File: `TEMPERATURE_A_kalau_kamu_bikin_vertical.mp4`, 1080x1920, 60 fps, sekitar 77 detik, tanpa suara.
- Kode: `videos/06-temperature/temperature_kalau_kamu_bikin.py` di repo manim-basic (salinan di folder ini), kelas `TemperatureKalauKamuBikin`.
  - Frame kunci: `STILLS=1 ORIENT=vertical manim -s -ql temperature_kalau_kamu_bikin.py TemperatureKalauKamuBikin` → `preview/vertical/A_*.png`
  - Video penuh: `ORIENT=vertical manim -qh temperature_kalau_kamu_bikin.py TemperatureKalauKamuBikin`
- Waktu per bagian: hook 0-4, token 4-12, probabilitas 12-21, toples 21-30, undi 30-39, kenop 39-50, kapan 50-57, selamat 57-64, catatan 64-70, tips 70-77.
- Naskah: `naskah_A_kalau_kamu_bikin.md`, naskah rekam: `naskah_narasi_rekam.md`.

## Aturan dari pengguna yang dipatuhi
- Hook dari pengalaman sendiri: minta nama usaha kopi 3x, hasilnya beda. Bukan kasus kantor.
- Istilah dijelaskan dulu baru dinamai: token, probabilitas, temperature.
- Tidak ada kotak polos: tiap batang berlabel kata + persen, tiap kertas di toples bertuliskan katanya, slot kosong berlabel "kata berikutnya?".
- Tidak ada zoom dan tidak ada transisi gelap.
- Arah gerak jelas: kursor token kiri → kanan, batang tumbuh atas → bawah, kertas terbang dari batangnya ke toples, kertas terpilih naik keluar mulut toples lalu jadi baris hasil, kenop geser kiri (rendah) → kanan (tinggi).
- Angka ilustrasi ditulis "angka contoh" (kanan atas, di bawah judul). Tanpa teaser part berikutnya.

## Default yang gw pilih
- Adegan terakhir dipecah dua biar nggak padat: "Catatan" (kenop digembok "di aplikasi chat: diatur penyedia", "temperature 0 ≠ selalu sama persis") lalu "Pakai aplikasi chat biasa?" (dua tips + 10 nama kopi).
- Kenop di adegan catatan menunjuk 1,0 karena itu default temperature di dokumentasi Anthropic.
- Isi toples: 20 kertas, dibagi sesuai peluang (T=1: 8/5/3/2/1/1; T=0,3: 16/3/1/0/0/0; T=1,6: 6/5/3/3/2/1).
- Potongan token "Coba / nama / : / Kopi" ditulis "ilustrasi", bukan hasil tokenizer sungguhan.

## Perlu dicek
- Durasi 77 detik, sedikit di atas target 75. Kalau kepanjangan setelah rekam suara, kurangi `self.wait` di adegan kenop atau tips.
- Di adegan kenop toplesnya lebih kecil, jadi kertas agak berdempetan. Yang penting kelihatan komposisinya berubah.
- Teks "Kopi Obeng" sengaja merah (SAGA) di batang dan kertas biar kebaca sebagai calon ngawur.
