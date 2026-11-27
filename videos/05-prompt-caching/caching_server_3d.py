"""
Prompt caching, adegan server 3D (eksplorasi visual, 3 opsi), design system KAPUR.

Metafora: prompt = menara blok. Lantai bawah = awal prompt (instruksi panjang yang sama),
lantai atas = bagian yang berubah (pertanyaan baru). Server menyimpan hasil hitungan
lantai-lantai bawah (prefix). Permintaan berikut yang lantai bawahnya identik langsung
memakai blok tersimpan; cuma lantai baru yang dihitung.

Warna: LANGIT = input/prompt yang dikirim, TOSKA = hasil hitungan AI yang tersimpan,
DAUN = cocok/dipakai ulang (hemat), SAGA = beda/hitung ulang (mahal), KUNYIT = 1 fokus.

Frame PNG:  ORIENT=vertical manim -s -qh caching_server_3d.py OpsiRak OpsiFondasi OpsiCocok
"""
import os
import sys
from pathlib import Path

_DIR = Path(__file__).resolve().parent
_DS = next(p / "design-system" for p in _DIR.parents if (p / "design-system").is_dir())
sys.path.insert(0, str(_DS))
from theme import *  # noqa: E402,F403

SISI = 0.9  # sisi kubus (unit dunia 3D)


def kubus(color, isi=0.55, garis=2.6, sisi=SISI, kosong=False):
    """Kubus gaya kapur: isi warna redup, tepi warna terang."""
    c = Cube(side_length=sisi, fill_color=redup(color, 0.35), fill_opacity=0.0 if kosong else isi,
             stroke_color=color, stroke_width=garis)
    return c


def menara(warna, x=0.0, y=0.0, z0=0.0, sisi=SISI, gap=0.08, **kw):
    """warna: list warna dari lantai bawah ke atas. Kembalikan VGroup kubus."""
    g = VGroup()
    for i, w in enumerate(warna):
        k = kubus(w, sisi=sisi, **kw) if not isinstance(w, tuple) else kubus(w[0], sisi=sisi, kosong=w[1] == "kosong", **kw)
        k.move_to([x, y, z0 + sisi / 2 + i * (sisi + gap)])
        g.add(k)
    return g


def kotak_garis(lebar, dalam, tinggi, pusat=ORIGIN, color=ABU_GELAP, w=2.5):
    """Rangka balok (12 rusuk) untuk rak server."""
    x, y, z = lebar / 2, dalam / 2, tinggi / 2
    P = [np.array(pusat) + np.array([sx * x, sy * y, sz * z])
         for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    rusuk = VGroup()
    for i in range(8):
        for j in range(i + 1, 8):
            if np.sum(np.abs(P[i] - P[j]) > 1e-6) == 1:
                rusuk.add(Line3D(P[i], P[j], color=color, thickness=0.012 * w) if False else
                          Line(P[i], P[j], color=color, stroke_width=w))
    return rusuk


def rak(lebar=3.2, dalam=1.8, tinggi=7.2, pusat=ORIGIN, tingkat=4):
    g = kotak_garis(lebar, dalam, tinggi, pusat)
    c = np.array(pusat)
    for k in range(1, tingkat):
        z = c[2] - tinggi / 2 + k * tinggi / tingkat
        a = c + np.array([-lebar / 2, -dalam / 2, 0]); a[2] = z
        sq = Polygon(a, a + [lebar, 0, 0], a + [lebar, dalam, 0], a + [0, dalam, 0],
                     stroke_color=ABU_GELAP, stroke_width=2, fill_color=GARIS, fill_opacity=0.5)
        g.add(sq)
    # lampu kecil server di sisi depan tiap tingkat
    for k in range(tingkat):
        z = c[2] - tinggi / 2 + (k + 0.15) * tinggi / tingkat
        for j in range(3):
            d = Dot3D([c[0] - lebar / 2 + 0.25 + j * 0.22, c[1] - dalam / 2, z], radius=0.045,
                      color=TOSKA if j == 0 else ABU_GELAP)
            g.add(d)
    return g


def garis_putus(a, b, color=DAUN, w=3):
    return DashedLine(a, b, color=color, stroke_width=w, dash_length=0.12)


class Kapur3D(ThreeDScene):
    """ThreeDScene dengan overlay 2D (header, label bab) yang tetap di layar."""

    def overlay(self, *mobs):
        self.add_fixed_in_frame_mobjects(*mobs)

    def mark(self, nama: str):
        if not os.environ.get("STILLS"):
            return
        out = _DIR / "preview" / ORIENT
        out.mkdir(parents=True, exist_ok=True)
        self.renderer.update_frame(self, ignore_skipping=True)
        self.renderer.camera.get_image().save(out / f"{nama}.png")

    def header2d(self, s, chapter):
        bab = label_bab(chapter)
        h = judul(s, size="h1").move_to([0, JUDUL_Y, 0]).align_to([AMAN["kiri"], 0, 0], LEFT)
        self.overlay(bab, h)
        return h

    def label(self, s, xy, color=TINTA, size="caption", weight=MEDIUM, mono_=False):
        t = (mono(s, color=color, size=size, weight=BOLD) if mono_ else
             teks(s, color=color, size=size, weight=weight))
        t.move_to([xy[0], xy[1], 0])
        self.overlay(t)
        return t


N_PREFIX = 5


class OpsiRak(Kapur3D):
    """Opsi 1: rak server menyimpan prefix; permintaan baru 'nyambung' ke blok tersimpan."""

    def construct(self):
        self.set_camera_orientation(phi=68 * DEGREES, theta=-62 * DEGREES, zoom=0.78,
                                    frame_center=[0.2, 0, 2.6])
        r = rak(pusat=[2.0, 1.2, 3.6])
        # prefix tersimpan di rak: berdiri di tingkat 1 (rak bawah) -> menara pendek 5 blok kecil
        simpan = menara([TOSKA] * N_PREFIX, x=2.0, y=1.2, z0=0.0, sisi=0.62, gap=0.06)
        # (rak punya tingkat; letakkan simpanan lain samar di tingkat atas)
        lain1 = menara([ABU_GELAP] * 2, x=1.3, y=1.2, z0=5.4, sisi=0.55, gap=0.05, kosong=True)
        lain2 = menara([ABU_GELAP] * 2, x=2.6, y=1.2, z0=5.4, sisi=0.55, gap=0.05, kosong=True)
        # permintaan baru: 5 lantai cocok (DAUN) + 2 lantai baru (KUNYIT = fokus)
        baru = menara([DAUN] * N_PREFIX + [KUNYIT, KUNYIT], x=-1.6, y=-0.6, z0=0.0, gap=0.1)
        for k in baru[:N_PREFIX]:
            k.set_fill(redup(DAUN, 0.3), 0.25)
        lantai = Square(side_length=9, stroke_width=0, fill_color=GARIS, fill_opacity=0.35).move_to([0.3, 0.3, 0])
        sambung = VGroup(*[garis_putus(baru[i].get_center() + RIGHT * SISI / 2,
                                       simpan[i].get_center() + LEFT * 0.31, color=DAUN, w=2.5)
                           for i in range(N_PREFIX)])
        self.add(lantai, r, lain1, lain2, simpan, baru, sambung)

        self.header2d("Server nyimpen awal prompt", "OPSI 1 · RAK SERVER")
        self.label("RAK SERVER · CACHE", (2.2, 4.75), color=ABU, size="mikro", mono_=True)
        self.label("permintaan baru", (-2.6, 4.8), color=LANGIT, size="caption")
        self.label("simpanan hilang kalau lama nggak dipakai", (1.1, -4.3), color=ABU, size="mikro")
        self.label("baru → dihitung", (-2.65, 4.2), color=KUNYIT, size="caption")
        self.label("sama → pakai ulang", (-2.2, -3.3), color=DAUN)
        self.label("hasil hitungan tersimpan", (2.4, -2.75), color=TOSKA, size="mikro")
        self.wait(0.1)


class OpsiFondasi(Kapur3D):
    """Opsi 2: satu fondasi (prefix tersimpan) dipakai banyak menara (permintaan)."""

    def construct(self):
        self.set_camera_orientation(phi=74 * DEGREES, theta=-48 * DEGREES, zoom=0.72,
                                    frame_center=[0, 0, 2.4])
        # fondasi 3x3x? : instruksi panjang yang sama, TOSKA (tersimpan)
        fondasi = VGroup()
        for i in range(4):
            for j in range(2):
                for k in range(2):
                    c = kubus(TOSKA, sisi=0.9, isi=0.5)
                    c.move_to([-1.4 + i * 0.95, -0.45 + j * 0.95, 0.45 + k * 0.95])
                    fondasi.add(c)
        alas = fondasi.get_center()
        top_z = 0.45 + 1 * 0.95 + 0.45
        # tiga menara permintaan, lantai atas beda-beda (LANGIT = input baru)
        tinggi = [2, 4, 3]
        xs = [-1.4, 0.5, 1.45]
        ys = [-0.45, -0.45, 0.5]
        tower = VGroup()
        for n, x, y in zip(tinggi, xs, ys):
            t = menara([LANGIT] * n, x=x, y=y, z0=top_z + 0.12, sisi=0.8, gap=0.08)
            tower.add(t)
        tower[1].set_stroke(KUNYIT)  # fokus: permintaan yang sedang dihitung
        tower[1].set_fill(redup(KUNYIT, 0.35), 0.5)
        lantai = Square(side_length=10, stroke_width=0, fill_color=GARIS, fill_opacity=0.35)
        # ring cahaya di bawah fondasi = "tersimpan di server"
        ring = Rectangle(width=4.6, height=2.8, stroke_color=TOSKA, stroke_width=2,
                         fill_opacity=0).move_to([alas[0], alas[1], 0.01])
        self.add(lantai, ring, fondasi, tower)

        self.header2d("Fondasinya dipakai bareng", "OPSI 2 · FONDASI")
        self.label("awal prompt yang sama", (0, -3.05), color=TOSKA)
        self.label("dihitung sekali · disimpan server", (0, -3.6), color=ABU, size="mikro")
        self.label("pertanyaan beda-beda", (0, 4.6), color=LANGIT)
        self.label("cuma lantai atas yang dihitung", (0, 4.05), color=ABU, size="mikro")


class OpsiCocok(Kapur3D):
    """Opsi 3: dicocokkan lantai demi lantai dari bawah; beda di awal = hitung ulang semua."""

    def construct(self):
        self.set_camera_orientation(phi=72 * DEGREES, theta=-78 * DEGREES, zoom=0.8,
                                    frame_center=[0, 0, 2.7])
        sisi = 0.72
        gap = 0.07
        # tersimpan (kiri), cocok (tengah), beda di lantai 2 (kanan)
        simpan = menara([TOSKA] * 5, x=-2.6, sisi=sisi, gap=gap)
        cocok = menara([DAUN] * 5 + [LANGIT, LANGIT], x=0.0, sisi=sisi, gap=gap)
        beda = menara([DAUN] + [SAGA] * 6, x=2.6, sisi=sisi, gap=gap)
        beda[1].set_stroke(KUNYIT, width=4)  # fokus: lantai yang beda
        beda[1].set_fill(redup(KUNYIT, 0.4), 0.6)
        lantai = Square(side_length=10, stroke_width=0, fill_color=GARIS, fill_opacity=0.35)
        zs = [k.get_center()[2] for k in simpan]
        rel = VGroup()
        for i, z in enumerate(zs):
            rel.add(garis_putus([-2.6 + sisi / 2, 0, z], [0 - sisi / 2, 0, z], color=DAUN, w=2.2))
        # "server": kotak rangka di sekitar menara tersimpan
        box = kotak_garis(1.5, 1.5, 5 * (sisi + gap) + 0.4, pusat=[-2.6, 0, (5 * (sisi + gap)) / 2 + 0.1],
                          color=ABU_GELAP)
        self.add(lantai, box, simpan, cocok, beda, rel)

        self.header2d("Dicocokin dari awal", "OPSI 3 · COCOK DARI BAWAH")
        self.label("tersimpan", (-2.75, -3.0), color=TOSKA)
        self.label("sama persis", (0.0, -3.0), color=DAUN)
        self.label("beda 1 kata", (2.65, -3.0), color=SAGA)
        self.label("di awal", (2.65, -3.5), color=SAGA, size="mikro")
        self.label("pakai ulang", (0.0, -3.5), color=ABU, size="mikro")
        self.label("hitung ulang", (2.7, 2.75), color=SAGA, size="mikro")
        self.label("bagian yang berubah: taruh di atas", (0, -4.25), color=ABU, size="mikro")
