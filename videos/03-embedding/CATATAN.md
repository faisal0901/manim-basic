# Catatan video-embedding-v1

## Isi folder
| File | Isi |
|---|---|
| `EMBEDDING_A_kalau_kamu_bikin_vertical.mp4` | Video final 9:16, 1080x1920, 60 fps, 69,4 dtk, tanpa suara |
| `embedding_kalau_kamu_bikin.py` | Kode Manim, kelas `EmbeddingKalauKamuBikin` (gaya A) |
| `naskah_A_kalau_kamu_bikin.md` | Naskah per adegan |
| `naskah_narasi_rekam.md` | Naskah rekam suara |
| `preview/vertical/A_*.png`, `preview/ringkasan_A.png` | Frame kunci dan lembar ringkasan |

Render ulang (dari folder ini; `theme.py` dicari otomatis di `design-system/` root repo):
```bash
STILLS=1 ORIENT=vertical manim -s -ql embedding_kalau_kamu_bikin.py EmbeddingKalauKamuBikin
ORIENT=vertical manim -qh embedding_kalau_kamu_bikin.py EmbeddingKalauKamuBikin
```

## Keputusan
- Gaya A, karena gantian (#1 A, #2 B).
- Tanpa teaser part berikutnya, sesuai permintaan Faisal.
- Sudut beda dari video RAG: di sini penonton menemukan *kenapa* embedding perlu dan *dari mana* angkanya.
- Narasi adegan 8 diubah dari "nggak ada satu kata pun yang sama" jadi "walau kata 'murah'-nya nggak ada sama sekali", karena kata "HP" sebenarnya sama.

## Tebakan dan ilustrasi (perlu konfirmasi)
- **Posisi titik di peta dan angka vektor** ([0.12, −0.83, …]) adalah ilustrasi, ditulis "angka ilustrasi" di layar. Model embedding tidak bisa diunduh dari cloud ini. Kalau mau angka nyata, bisa dihitung di laptop dengan model embedding gratis.
- **"Ratusan sampai ribuan sumbu"**: umum untuk model embedding (mis. text-embedding-3-small OpenAI 1.536 dimensi menurut dokumentasinya). Di layar tidak ditulis angka pastinya.
- **"Belajar dari kalimat"**: penyederhanaan cara model embedding dilatih.
- **Sumbu "HARGA"** cuma alat bantu cerita; batasnya disebut di layar ("sumbunya nggak punya nama kayak 'harga'").
- Kata pembeli ("murmer", "murceee", "worth it", dst.) dipilih supaya relate, bukan dari data pencarian nyata.
- Pil penutup memakai TOSKA (peran AI).
