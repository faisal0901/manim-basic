"""
Prompt caching, rangkaian zoom 3D: rak server -> satu server -> GPU -> memori GPU -> blok cocok.
Masih frame kunci (PNG), belum animasi. Pilihan Faisal: opsi "rak server" + zoom ke CPU/GPU.

Pegangan akurasi (sistem terbuka seperti vLLM/SGLang; detail penyedia besar tidak semuanya publik):
- Yang disimpan = KV cache (angka Key/Value hasil hitungan tiap token di tiap lapisan), bukan teks.
- Tempatnya terutama memori GPU (HBM); sebagian sistem memindah yang jarang dipakai ke RAM/SSD.
- CPU = manajer: terima permintaan, potong jadi blok token, hitung sidik (hash) blok, cari yang cocok,
  jadwalkan GPU. CPU tidak menghitung model.
- Sidik blok ikut menyertakan blok sebelumnya -> harus identik dari awal.
- Blok cocok -> GPU melewati hitungan bagian itu; cuma token baru yang dihitung.
- Memori penuh / lama tak dipakai -> digusur.
Penyederhanaan visual: jumlah GPU, bentuk chip, ukuran blok, dan angka di layar = ilustrasi.

Frame PNG:  ORIENT=vertical manim -s -ql caching_zoom_3d.py Z1Rak Z2Server Z3GPU Z4Memori Z5Cocok
"""
import sys
from pathlib import Path

_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_DIR))
from caching_server_3d import *  # noqa: E402,F403


def balok(w, d, h, color, pusat, isi=0.35, garis=2.2, fill=None):
    p = Prism(dimensions=[w, d, h], fill_color=fill or redup(color, 0.3), fill_opacity=isi,
              stroke_color=color, stroke_width=garis)
    p.move_to(pusat)
    return p


def lantai(n=12, op=0.35, pusat=ORIGIN):
    return Square(side_length=n, stroke_width=0, fill_color=GARIS, fill_opacity=op).move_to(pusat)


def tray(pusat, w=2.6, d=1.6, h=0.32, color=ABU_GELAP, lampu=True):
    g = VGroup(balok(w, d, h, color, pusat, isi=0.6, garis=2, fill=PERMUKAAN))
    if lampu:
        c = np.array(pusat)
        for j in range(3):
            g.add(Dot3D(c + np.array([-w / 2 + 0.25 + j * 0.2, -d / 2 - 0.01, 0]), radius=0.04,
                        color=TOSKA if j == 0 else ABU_GELAP))
    return g


class Z1Rak(Kapur3D):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-60 * DEGREES, zoom=0.74,
                                    frame_center=[0, 0, 3.2])
        self.add(lantai(16))
        fokus = None
        for i, x in enumerate([-3.1, 0.0, 3.1]):
            self.add(kotak_garis(2.8, 1.8, 7.0, pusat=[x, 0.3 * i, 3.5]))
            for k in range(8):
                t = tray([x, 0.3 * i, 0.5 + k * 0.82])
                if i == 1 and k == 4:
                    t[0].set_stroke(KUNYIT, width=4)
                    fokus = t
                self.add(t)
        self.header2d("Ini server AI", "ZOOM 1 · DATA CENTER")
        self.label("ribuan server kayak gini", (0, 4.6), color=ABU)
        self.label("kita masuk ke satu", (0.3, -3.7), color=KUNYIT)


class Z2Server(Kapur3D):
    def construct(self):
        self.set_camera_orientation(phi=55 * DEGREES, theta=-70 * DEGREES, zoom=0.75,
                                    frame_center=[0, 0, 0])
        badan = balok(7.6, 6.2, 0.5, ABU_GELAP, [0, 0.4, 0], isi=0.8, garis=2.5, fill=PERMUKAAN)
        # CPU (manajer) depan kiri
        cpu = VGroup(balok(1.4, 1.4, 0.18, TINTA, [-2.4, -1.6, 0.35], isi=0.5, fill=redup(TINTA, 0.25)),
                     balok(0.8, 0.8, 0.1, TINTA, [-2.4, -1.6, 0.5], isi=0.3))
        ram = VGroup(*[balok(0.12, 1.6, 0.5, ABU, [-0.9 + j * 0.28, -1.6, 0.5], isi=0.6, garis=1.4)
                       for j in range(4)])
        # 8 GPU (tukang hitung) di belakang
        gpus = VGroup()
        for r in range(2):
            for c in range(4):
                g = balok(1.45, 1.3, 0.35, TOSKA, [-2.55 + c * 1.7, 0.75 + r * 1.65, 0.45], isi=0.45)
                if r == 0 and c == 2:
                    g.set_stroke(KUNYIT, width=4)
                gpus.add(g)
        self.add(badan, cpu, ram, gpus)
        self.header2d("Di dalam satu server", "ZOOM 2 · SERVER")
        self.label("GPU · tukang hitung", (0.6, 3.9), color=TOSKA, size="body", weight=MEDIUM)
        self.label("ngitung model AI", (0.6, 3.35), color=ABU, size="caption")
        self.label("CPU · manajer", (-2.0, -3.15), color=TINTA, size="body", weight=MEDIUM)
        self.label("terima permintaan, atur antrean", (-0.9, -3.7), color=ABU, size="caption")
        self.label("RAM", (0.3, -2.45), color=ABU, size="mikro", mono_=True)


class Z3GPU(Kapur3D):
    def construct(self):
        self.set_camera_orientation(phi=58 * DEGREES, theta=-62 * DEGREES, zoom=0.9,
                                    frame_center=[0, 0, 0.4])
        papan = balok(6.4, 5.2, 0.16, ABU_GELAP, [0, 0, 0], isi=0.8, garis=2, fill=PERMUKAAN)
        inti = balok(2.6, 2.6, 0.3, TOSKA, [0, 0, 0.25], isi=0.5, garis=3)
        hbm = VGroup()
        tempat = [(-2.1, -1.2), (-2.1, 1.2), (2.1, -1.2), (2.1, 1.2)]
        for n, (x, y) in enumerate(tempat):
            tumpuk = VGroup(*[balok(1.0, 1.4, 0.16, KERTAS, [x, y, 0.16 + i * 0.2], isi=0.25, garis=1.6)
                              for i in range(8)])
            if n == 2:
                tumpuk.set_stroke(KUNYIT, width=3)
            hbm.add(tumpuk)
        self.add(papan, inti, hbm)
        self.header2d("Di dalam GPU", "ZOOM 3 · GPU")
        self.label("inti hitung", (-0.2, -3.3), color=TOSKA, size="body", weight=MEDIUM)
        self.label("memori GPU (HBM)", (1.0, 3.55), color=KERTAS, size="body", weight=MEDIUM)
        self.label("chip memori bertumpuk, nempel di inti", (0.2, 3.0), color=ABU, size="caption")
        self.label("hasil hitungan disimpan di sini", (0.6, -4.05), color=ABU, size="caption")


def blok_slot(nx=5, ny=4, s=0.9, gap=0.14, z=0.0, isi=None):
    """Grid slot memori. isi: dict {(i,j): warna}. Slot kosong = kotak garis samar."""
    g = VGroup()
    slots = {}
    for i in range(nx):
        for j in range(ny):
            x = (i - (nx - 1) / 2) * (s + gap)
            y = (j - (ny - 1) / 2) * (s + gap)
            sq = Square(side_length=s, stroke_color=GARIS, stroke_width=2, fill_opacity=0).move_to([x, y, z])
            g.add(sq)
            if isi and (i, j) in isi:
                w = isi[(i, j)]
                k = kubus(w, sisi=s * 0.86, isi=0.5 if w != ABU_GELAP else 0.15)
                k.move_to([x, y, z + s * 0.43])
                g.add(k)
                slots[(i, j)] = k
    return g, slots


class Z4Memori(Kapur3D):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-70 * DEGREES, zoom=0.82,
                                    frame_center=[0, 0, 0.3])
        prefix = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        isi = {p: TOSKA for p in prefix}
        for p in [(0, 2), (1, 2), (3, 3), (4, 2), (2, 3), (0, 3)]:
            isi[p] = ABU_GELAP
        grid, slots = blok_slot(isi=isi)
        papan = balok(5.6, 4.6, 0.12, ABU_GELAP, [0, 0, -0.08], isi=0.8, garis=2, fill=PERMUKAAN)
        self.add(papan, grid)
        for n, p in enumerate(prefix):
            self.add(Text(str(n + 1), font=FONT_MONO, color=TOSKA, font_size=30, weight=BOLD)
                     .rotate(PI / 2, RIGHT).move_to(slots[p].get_center() + DOWN * 0.47))
        self.header2d("Isinya: KV cache", "ZOOM 4 · MEMORI GPU")
        self.label("hasil hitungan awal prompt", (0, 4.45), color=TOSKA, size="body", weight=MEDIUM)
        self.label("disimpan per blok · 1 → 5", (0, 3.9), color=ABU, size="caption")
        isi_angka = mono("0.12  -0.87  0.45  1.03  …", color=JINGGA, size="caption")
        k = kartu(VGroup(mono("isi 1 blok (ilustrasi)", color=ABU, size="mikro"), isi_angka)
                  .arrange(DOWN, buff=0.15, aligned_edge=LEFT), aksen=JINGGA)
        k.move_to([0, -3.15, 0])
        self.overlay(k)
        self.label("angka, bukan teks", (0, -4.25), color=KUNYIT, size="caption")
        self.label("blok user lain", (2.65, 2.15), color=ABU, size="mikro")


class Z5Cocok(Kapur3D):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-70 * DEGREES, zoom=0.78,
                                    frame_center=[0, 0, 0.3])
        prefix = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        isi = {p: TOSKA for p in prefix}
        for p in [(0, 2), (1, 2), (3, 3), (4, 2), (2, 3), (0, 3)]:
            isi[p] = ABU_GELAP
        grid, slots = blok_slot(isi=isi)
        papan = balok(5.6, 4.6, 0.12, ABU_GELAP, [0, 0, -0.08], isi=0.8, garis=2, fill=PERMUKAAN)
        # permintaan baru: baris blok di depan memori (y negatif), 5 cocok + 2 baru
        s = 0.9
        req = VGroup()
        for n in range(7):
            x = (n - 3) * (s + 0.1) + 0.5
            w = DAUN if n < 5 else KUNYIT
            k = kubus(w, sisi=s * 0.86, isi=0.3 if n < 5 else 0.55)
            k.move_to([x, -4.4, s * 0.43])
            req.add(k)
        tali = VGroup(*[garis_putus(req[n].get_center() + UP * 0.4, slots[p].get_center() + DOWN * 0.4,
                                    color=DAUN, w=2.5) for n, p in enumerate(prefix)])
        VGroup(papan, grid, req, tali).shift(UP * 1.6)
        self.add(papan, grid, req, tali)
        self.header2d("Permintaan berikutnya", "ZOOM 5 · COCOK")
        self.label("memori GPU", (-2.6, 3.7), color=ABU, size="mikro", mono_=True)
        self.label("CPU cocokin sidik tiap blok", (0, 4.5), color=TINTA, size="caption", weight=MEDIUM)
        self.label("sama → GPU loncatin hitungannya", (0, -2.85), color=DAUN, size="caption")
        self.label("baru → dihitung", (2.15, -3.85), color=KUNYIT, size="caption")
        self.label("permintaan baru", (-2.2, -3.85), color=LANGIT, size="caption")
