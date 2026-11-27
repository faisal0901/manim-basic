"""
KAPUR — design system Manim untuk channel ngajar
=================================================
"Kapur di papan hitam": latar hitam pekat, tinta terang, dan warna dipakai
sebagai MAKNA, bukan hiasan. Terinspirasi cara 3Blue1Brown memakai warna dan
gerak, tapi dengan palet, tipografi, dan aturan layout sendiri.

Pakai:
    from theme import *            # token + helper + KapurScene
    class Video(KapurScene):
        def construct(self):
            self.header("Judul bagian", chapter="BAB 1 · HOOK")
            ...
            self.mark("01_hook")      # simpan PNG bila STILLS=1

Orientasi dipilih lewat env ORIENT=vertical (9:16, default) | horizontal (16:9).
Tidak butuh LaTeX: semua teks memakai Text (Pango) dengan font yang dibundel
di folder fonts/.
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
from manim import *  # noqa: F401,F403

# --------------------------------------------------------------------------
# 0. Font: daftarkan file font yang dibundel supaya hasil sama di laptop mana pun
# --------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
try:
    import manimpango

    for _f in sorted((_HERE / "fonts").glob("*.ttf")):
        manimpango.register_font(str(_f))
except Exception as _e:  # macOS lama, dsb. -> install font manual (lihat README)
    print(f"[kapur] gagal mendaftarkan font bundel: {_e}")

FONT_JUDUL = "Source Serif 4"   # judul & kalimat besar (karakter "buku", ala papan tulis)
FONT_TEKS = "Inter"             # label, caption, isi kartu (paling terbaca di HP)
FONT_MONO = "JetBrains Mono"    # angka teknis, vektor, kode, label bab

# --------------------------------------------------------------------------
# 1. Warna
# --------------------------------------------------------------------------
# Netral (dari papan ke kapur)
HITAM = "#000000"        # latar. SELALU hitam penuh.
PERMUKAAN = "#0D0D0D"    # isi kartu / panel
GARIS = "#1E1E1E"        # grid, garis bantu paling samar
ABU_GELAP = "#454545"    # sumbu, pembatas, outline kartu
ABU = "#9B9B9B"          # teks sekunder, caption
TINTA = "#EDEDED"        # teks utama (bukan putih murni: lebih lembut di mata)
KERTAS = "#ECE6D8"       # dokumen / kertas (sedikit hangat)

# Warna bermakna. Satu warna = satu peran di seluruh video.
LANGIT = "#5CC3E6"   # manusia, pengguna, input, pertanyaan
TOSKA = "#4FD1B8"    # AI / model
KUNYIT = "#FFD54A"   # FOKUS: "lihat ini". Hanya 1 hal kuning per layar.
DAUN = "#8BD17C"     # solusi, benar, hemat, hasil
SAGA = "#FF6B5E"     # masalah, salah, mahal, lambat
JINGGA = "#F4A95C"   # angka & satuan penting (token, halaman, rupiah)
UNGU = "#B497E0"     # cadangan / kategori ke-7+

# Versi redup untuk isian kartu/latar sorotan (≈ 18% di atas hitam)
def redup(hex_color: str, a: float = 0.18) -> str:
    c = np.array(color_to_rgb(hex_color))
    return rgb_to_hex(c * a)

# Warna kategori (chunk, cluster, seri data). Urutan tetap.
KATEGORI = [LANGIT, TOSKA, DAUN, JINGGA, UNGU, "#E58BB4", "#7FA8F5", "#C9D46A", "#6FD6E0"]

PERAN = {  # dipakai di halaman referensi
    "LANGIT": "manusia · input · pertanyaan",
    "TOSKA": "AI · model",
    "KUNYIT": "fokus · sorotan · maks. 1 per layar",
    "DAUN": "solusi · benar · hemat",
    "SAGA": "masalah · salah · mahal",
    "JINGGA": "angka & satuan penting",
}

config.background_color = HITAM

# --------------------------------------------------------------------------
# 2. Layout & orientasi
# --------------------------------------------------------------------------
ORIENT = os.environ.get("ORIENT", "vertical")
VERTIKAL = ORIENT == "vertical"

if VERTIKAL:  # 9:16, TikTok / Reels / Shorts
    config.pixel_width, config.pixel_height = 1080, 1920
    config.frame_width, config.frame_height = 9.0, 16.0
    S = 1.0
    # Zona aman: atas 1.4 (status bar + judul app), bawah 3.4 (caption & tombol app),
    # kanan 0.9 (tombol like/share), kiri 0.6
    AMAN = dict(atas=6.6, bawah=-4.6, kiri=-3.9, kanan=3.6)
    PUSAT = np.array([-0.15, -0.2, 0])
    SY = 1.0  # skala posisi vertikal
else:  # 16:9, YouTube
    config.pixel_width, config.pixel_height = 1920, 1080
    config.frame_width, config.frame_height = 16.0, 9.0
    S = 0.8
    AMAN = dict(atas=3.9, bawah=-3.9, kiri=-7.3, kanan=7.3)
    PUSAT = np.array([0, -0.45, 0])
    SY = 0.66  # 16:9 lebih pendek: posisi vertikal dipadatkan

LEBAR_AMAN = AMAN["kanan"] - AMAN["kiri"]
JUDUL_Y = AMAN["atas"] - 0.75 * S
BAB_Y = AMAN["atas"]

# Grid spasi: kelipatan 0.25 unit
SP = dict(xs=0.1 * S, s=0.2 * S, m=0.4 * S, l=0.7 * S, xl=1.2 * S)

# Skala tipe (font_size Manim, sudah dikali S)
TIPE = dict(
    raksasa=120,  # satu kata kunci (mis. "RAG")
    display=68,   # kalimat titik balik
    h1=52,        # judul bagian
    h2=40,        # subjudul / kolom
    body=32,      # label utama
    caption=25,   # keterangan
    mikro=19,     # sumber, label bab
)


def pos(x: float, y: float) -> np.ndarray:
    """Koordinat relatif pusat area konten, ikut diskalakan per orientasi."""
    return PUSAT + np.array([S * x, S * SY * y, 0])


# --------------------------------------------------------------------------
# 3. Gerak (tempo)
# --------------------------------------------------------------------------
# Prinsip: satu ide per ketukan; gerak halus (smooth) seperti default Manim;
# lebih baik diam sebentar daripada ramai.
KETUK = 1.0        # durasi standar satu animasi (= default Manim)
CEPAT = 0.5        # masuk/keluar elemen pendukung
LAMBAT = 1.6       # transformasi penting, garis kapur menulis judul
JEDA = 1.2         # self.wait setelah ide penting (beri waktu narasi)
JEDA_PANJANG = 2.0
GESER = 0.25 * S   # jarak geser FadeIn/FadeOut
LAG = 0.08         # LaggedStart untuk grup
GERAK = smooth     # rate_func default


# --------------------------------------------------------------------------
# 4. Teks
# --------------------------------------------------------------------------
def _txt(s, size, color, font, weight, **kw):
    return Text(s, font=font, font_size=size * S, color=color, weight=weight, **kw)


def judul(s, color=TINTA, size="h1", **kw):
    """Judul serif. Untuk header bagian dan kalimat besar."""
    t = _txt(s, TIPE.get(size, size), color, FONT_JUDUL, SEMIBOLD, **kw)
    if t.width > LEBAR_AMAN:
        t.scale_to_fit_width(LEBAR_AMAN)
    return t


def teks(s, color=TINTA, size="body", weight=NORMAL, **kw):
    """Teks sans (Inter) untuk label & isi."""
    t = _txt(s, TIPE.get(size, size), color, FONT_TEKS, weight, **kw)
    if t.width > LEBAR_AMAN:
        t.scale_to_fit_width(LEBAR_AMAN)
    return t


def caption(s, color=ABU, **kw):
    return teks(s, color=color, size="caption", **kw)


def mono(s, color=TINTA, size="caption", weight=NORMAL, **kw):
    return _txt(s, TIPE.get(size, size), color, FONT_MONO, weight, **kw)


def label_bab(s, color=ABU):
    """Label kecil 'BAB 2 · MASALAH' di pojok kiri atas: penanda identitas."""
    dot = Dot(radius=0.06 * S, color=KUNYIT)
    t = mono(s.upper(), color=color, size="mikro")
    g = VGroup(dot, t).arrange(RIGHT, buff=0.15 * S)
    g.move_to([0, BAB_Y, 0]).align_to([AMAN["kiri"], 0, 0], LEFT)
    return g


def coret_kapur(mob, color=KUNYIT, width=6):
    """Garis bawah sedikit melengkung, tanda tangan visual 'kapur'."""
    a = mob.get_corner(DL) + DOWN * 0.12 * S
    b = mob.get_corner(DR) + DOWN * 0.12 * S
    return ArcBetweenPoints(a, b, angle=-0.08, color=color, stroke_width=width * S)


# --------------------------------------------------------------------------
# 5. Komponen
# --------------------------------------------------------------------------
def kartu(isi: Mobject, aksen=None, pad=0.3, lebar=None, tinggi=None):
    """Panel gelap dengan outline tipis. aksen=warna -> garis tepi kiri berwarna."""
    w = lebar or isi.width + 2 * pad * S
    h = tinggi or isi.height + 2 * pad * S
    r = RoundedRectangle(width=w, height=h, corner_radius=0.14 * S,
                         fill_color=PERMUKAAN if aksen is None else redup(aksen, 0.14),
                         fill_opacity=1, stroke_color=ABU_GELAP if aksen is None else aksen,
                         stroke_width=2 * S if aksen is None else 2.5 * S)
    r.move_to(isi)
    return VGroup(r, isi)


def pil(s, color=LANGIT, size="caption", isi_gelap=False):
    """Kapsul/label. isi_gelap=False -> isi warna redup + teks berwarna."""
    t = teks(s, color=color if not isi_gelap else HITAM, size=size, weight=MEDIUM)
    r = RoundedRectangle(width=t.width + 0.45 * S, height=t.height + 0.3 * S,
                         corner_radius=(t.height + 0.3 * S) / 2,
                         fill_color=color if isi_gelap else redup(color, 0.2),
                         fill_opacity=1, stroke_color=color, stroke_width=1.5 * S)
    t.move_to(r)
    return VGroup(r, t)


def gelembung(s, color=LANGIT, size="caption"):
    """Balon chat (pertanyaan/jawaban)."""
    t = teks(s, color=TINTA, size=size)
    r = RoundedRectangle(width=t.width + 0.5 * S, height=t.height + 0.42 * S,
                         corner_radius=0.18 * S, fill_color=redup(color, 0.22),
                         fill_opacity=1, stroke_color=color, stroke_width=2 * S)
    ekor = Polygon(r.get_corner(DL) + RIGHT * 0.25 * S, r.get_corner(DL) + RIGHT * 0.55 * S,
                   r.get_corner(DL) + RIGHT * 0.2 * S + DOWN * 0.22 * S,
                   fill_color=redup(color, 0.22), fill_opacity=1, stroke_color=color,
                   stroke_width=2 * S)
    t.move_to(r)
    return VGroup(ekor, r, t)


def lencana(n, color=KUNYIT):
    """Nomor langkah dalam lingkaran."""
    c = Circle(radius=0.28 * S, stroke_color=color, stroke_width=3 * S,
               fill_color=HITAM, fill_opacity=1)
    t = mono(str(n), color=color, size="body", weight=BOLD).move_to(c)
    return VGroup(c, t)


def panah(a, b, color=ABU, buff=0.15, tebal=4):
    return Arrow(a, b, buff=buff * S, color=color, stroke_width=tebal * S,
                 max_tip_length_to_length_ratio=0.18, tip_length=0.22 * S)


def batang(label, nilai, maks=1.0, color=SAGA, panjang=4.5, teks_nilai=None):
    """Bar horizontal: label | track | isi. Kembalikan VGroup(lab, track, isi, val)."""
    lab = teks(label, color=ABU, size="caption")
    track = RoundedRectangle(width=panjang * S, height=0.34 * S, corner_radius=0.17 * S,
                             fill_color=GARIS, fill_opacity=1, stroke_width=0)
    w = max(0.34 * S, panjang * S * nilai / maks)
    isi = RoundedRectangle(width=w, height=0.34 * S, corner_radius=0.17 * S,
                           fill_color=color, fill_opacity=1, stroke_width=0)
    lab.next_to(track, UP, buff=0.1 * S).align_to(track, LEFT)
    isi.align_to(track, LEFT).set_y(track.get_y())
    g = VGroup(lab, track, isi)
    if teks_nilai:
        v = mono(teks_nilai, color=color, size="caption", weight=BOLD)
        v.next_to(track, UP, buff=0.1 * S).align_to(track, RIGHT)
        g.add(v)
    return g


# --- Ikon (geometri sederhana, garis rapi, tanpa gambar luar) ---------------
def ikon_dokumen(lebar=0.55, color=KERTAS):
    w = lebar * S
    h = w * 1.3
    lipat = w * 0.28
    body = Polygon(
        [-w / 2, h / 2, 0], [w / 2 - lipat, h / 2, 0], [w / 2, h / 2 - lipat, 0],
        [w / 2, -h / 2, 0], [-w / 2, -h / 2, 0],
        fill_color=color, fill_opacity=1, stroke_width=0)
    sudut = Polygon([w / 2 - lipat, h / 2, 0], [w / 2 - lipat, h / 2 - lipat, 0],
                    [w / 2, h / 2 - lipat, 0], fill_color="#B9B2A2", fill_opacity=1,
                    stroke_width=0)
    garis = VGroup(*[
        Line([-w * 0.3, 0, 0], [w * (0.3 if i % 3 else 0.05), 0, 0],
             stroke_width=max(1.2, 2.2 * lebar) * S, color="#7A7466")
        for i in range(4)
    ]).arrange(DOWN, buff=h * 0.12).move_to(body).shift(DOWN * h * 0.06)
    return VGroup(body, sudut, garis)


def ikon_orang(color=LANGIT, skala=1.0):
    s = skala * S
    kepala = Circle(radius=0.14 * s, fill_color=color, fill_opacity=1, stroke_width=0)
    badan = Sector(radius=0.26 * s, angle=PI, start_angle=0, fill_color=color,
                   fill_opacity=1, stroke_width=0)
    badan.next_to(kepala, DOWN, buff=0.05 * s)
    return VGroup(kepala, badan)


def ikon_ai(ukuran=1.6, color=TOSKA):
    """Chip AI: kotak outline + pin + label mono. Garis, bukan blok penuh."""
    u = ukuran * S
    kotak = RoundedRectangle(width=u, height=u, corner_radius=u * 0.16,
                             fill_color=redup(color, 0.16), fill_opacity=1,
                             stroke_color=color, stroke_width=3.5 * S)
    inti = RoundedRectangle(width=u * 0.5, height=u * 0.5, corner_radius=u * 0.06,
                            fill_opacity=0, stroke_color=color, stroke_width=2 * S)
    label = Text("AI", font=FONT_MONO, weight=BOLD, color=color,
                 font_size=44 * S * ukuran / 1.6).move_to(kotak)
    pin = VGroup()
    for k in (-0.25, 0, 0.25):
        for d in (LEFT, RIGHT, UP, DOWN):
            p = Line(ORIGIN, d * u * 0.12, stroke_width=3 * S, color=color)
            off = (UP if d[0] != 0 else RIGHT) * k * u
            p.shift(kotak.get_center() + d * u / 2 + off)
            pin.add(p)
    return VGroup(pin, kotak, inti, label)


def grid_titik(lebar=7, tinggi=4.6):
    """Bidang vektor bergaya 3B1B tapi lebih samar: grid tipis + sumbu abu."""
    return NumberPlane(
        x_range=[-4, 4, 1], y_range=[-3, 3, 1],
        x_length=lebar * S, y_length=tinggi * S,
        background_line_style={"stroke_color": GARIS, "stroke_width": 1.5},
        axis_config={"stroke_color": ABU_GELAP, "stroke_width": 2},
    )


# --------------------------------------------------------------------------
# 6. Scene dasar
# --------------------------------------------------------------------------
class KapurScene(Scene):
    """Scene dengan header, label bab, pembersih, dan ekspor frame kunci.

    STILLS=1 -> self.mark(nama) menyimpan PNG ke preview/<orientasi>/nama.png.
    Paling cepat dijalankan dengan `manim -s` (animasi dilompati).
    """

    _hdr = None
    _bab = None

    # --- header & bab ---
    def header(self, s, chapter=None, color=TINTA, run_time=CEPAT + 0.1):
        anims = []
        if chapter is not None:
            nb = label_bab(chapter)
            anims.append(FadeIn(nb) if self._bab is None else FadeTransform(self._bab, nb))
            self._bab = nb
        new = judul(s, color=color, size="h1")
        if new.width > LEBAR_AMAN:
            new.scale_to_fit_width(LEBAR_AMAN)
        new.move_to([0, JUDUL_Y, 0]).align_to([AMAN["kiri"], 0, 0], LEFT)
        if self._hdr is None:
            anims.append(FadeIn(new, shift=DOWN * GESER))
        else:
            anims += [FadeOut(self._hdr, shift=UP * GESER), FadeIn(new, shift=UP * GESER)]
        self._hdr = new
        self.play(*anims, run_time=run_time)

    def tanpa_header(self, run_time=CEPAT):
        objs = [m for m in (self._hdr,) if m is not None]
        if objs:
            self.play(*[FadeOut(m) for m in objs], run_time=run_time)
        self._hdr = None

    def bersihkan(self, run_time=CEPAT, sisakan_header=True):
        keep = {id(self._bab)}
        if sisakan_header and self._hdr is not None:
            keep.add(id(self._hdr))
        objs = [m for m in self.mobjects if id(m) not in keep]
        if objs:
            self.play(*[FadeOut(m) for m in objs], run_time=run_time)
        if not sisakan_header:
            self._hdr = None

    # --- ekspor frame kunci ---
    def mark(self, nama: str):
        if not os.environ.get("STILLS"):
            return
        out = _HERE / "preview" / ORIENT
        out.mkdir(parents=True, exist_ok=True)
        self.renderer.update_frame(self, ignore_skipping=True)
        self.renderer.camera.get_image().save(out / f"{nama}.png")
