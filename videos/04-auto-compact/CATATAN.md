# Catatan video auto compact v1 (gaya A, kerangka system prompt)

- File: `AUTO_COMPACT_A_kalau_kamu_bikin_vertical.mp4`, 1080x1920, 60 fps, sekitar 79 detik, tanpa suara.
- Kode: `videos/04-auto-compact/auto_compact_kalau_kamu_bikin.py`, kelas `AutoCompactKalauKamuBikin`.
  - Frame kunci: `STILLS=1 ORIENT=vertical manim -s -ql auto_compact_kalau_kamu_bikin.py AutoCompactKalauKamuBikin` → `preview/vertical/A_*.png`
  - Video penuh: `ORIENT=vertical manim -qh auto_compact_kalau_kamu_bikin.py AutoCompactKalauKamuBikin`
- Waktu per bagian: hook 0-4, batas/context window 4-13, buang lama + ringkas 13-26, system prompt 26-32, TRUST 32-42, KEEP/DROP 42-50, NEVER STORE + MERGE 50-59, FORMAT 59-65, AI ingat 65-70, selamat 70-79.
- Visual utama: kelas `Kerangka` (kartu "SYSTEM PROMPT · AI peringkas" dengan 8 slot garis putus-putus). Tiap bagian terisi saat penonton ketemu masalahnya; bagian aktif dikotaki KUNYIT, bagian lama jadi ABU. Di adegan akhir kartu tampil lengkap dengan catatan kecil.
- Pakai ulang dari "Kok AI lupa?": balon chat, `pindai()`, `penghitung()`, hook "Kok lupa?" (disalin ke file ini karena kode video itu belum masuk repo).

## Default yang gw pilih (gampang diubah)
- Label bagian bahasa Inggris (PERAN/INPUT diindonesiakan, TRUST, KEEP, DROP, NEVER STORE, MERGE, FORMAT tetap Inggris) dengan terjemahan di awal isi baris ("percaya:", "simpan:", dst.). Ganti di daftar `KERANGKA`.
- Tiga aturan yang tidak dibacakan jadi teks kecil di kartu akhir: "isi dokumen tempelan nggak disalin" (NEVER STORE), "tanggal relatif → pasti · kosong → memori lama" (MERGE).
- "Klaim" = bagian TRUST: tebakan AI, isi dokumen, dan teks perintah di dalam data ditolak; omongan user = fakta; saran AI yang disetujui = keputusan.

## Angka (semua contoh, di layar ditulis "sesuaikan dengan kebutuhan")
- Batas context window 100.000 token, ambang 80%, maks. ±1.000 kata, angka token 62.000 dan 80.000 → 1.500.
- Pecahan "responden" → res/pon/den = ilustrasi, bukan hasil tokenizer sungguhan (ditulis "ilustrasi").

## Tebakan / perlu dicek
- Durasi 79 detik, sedikit di atas target 75. Kalau kepanjangan, adegan "buang yang lama" (13-18) bisa dipersingkat.
- Adegan "buang pesan paling lama → data kebuang" ada di render (dari naskah v1, bagian rantai "tapi… jadi…"), padahal naskah v2 melompatinya. Kalimatnya sudah ditambah di naskah rekam.
- Teks catatan kecil di kartu akhir kecil sekali di HP; dimaksudkan untuk yang pause.
- Nama produk dan kantor tidak disebut; teks system prompt asli tidak disalin.
