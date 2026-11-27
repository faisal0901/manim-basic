"""
Video #3 Embedding, gaya A "Kalau kamu yang bikin…", design system KAPUR.

Kasus: pembeli toko online ngetik "HP murah", produk tertulis "HP harga terjangkau".
Rantai: cocok persis -> tapi 0 hasil -> sinonim -> tapi nggak habis -> posisi di peta
-> tapi siapa yang ngisi -> belajar dari kalimat -> tapi 1 sumbu kurang ("bisa")
-> ratusan-ribuan sumbu -> deretan angka -> ketemu. "Selamat, kamu baru aja bikin embedding."

Posisi titik dan angka vektor = ILUSTRASI, bukan hasil model sungguhan.

Frame kunci:  STILLS=1 ORIENT=vertical manim -s -ql embedding_kalau_kamu_bikin.py EmbeddingKalauKamuBikin
Video penuh:  ORIENT=vertical manim -qh embedding_kalau_kamu_bikin.py EmbeddingKalauKamuBikin
"""
import os
import sys
from pathlib import Path

import numpy as np

_DIR = Path(__file__).resolve().parent
# cari folder design-system/ di folder induk mana pun (repo root)
_DS = next(p / "design-system" for p in _DIR.parents if (p / "design-system").is_dir())
sys.path.insert(0, str(_DS))
from theme import *  # noqa: E402,F403

JEDA = 1.8
JEDA_PANJANG = 2.9

CARI = "HP murah"
PRODUK = "HP harga terjangkau"


# ---------------------------------------------------------------------------
# Komponen
# ---------------------------------------------------------------------------
def kiri(m, y):
    m.move_to(pos(0, y)).align_to([AMAN["kiri"], 0, 0], LEFT)
    return m


def kaca_pembesar(color=LANGIT, u=1.0):
    c = Circle(radius=0.16 * S * u, stroke_color=color, stroke_width=4 * S)
    g = Line(c.get_center() + np.array([0.11, -0.11, 0]) * S * u,
             c.get_center() + np.array([0.3, -0.3, 0]) * S * u, color=color, stroke_width=5 * S)
    return VGroup(c, g)


def kolom_cari(s=CARI, lebar=7.2):
    t = teks(s, color=TINTA, size="body")
    ic = kaca_pembesar()
    r = RoundedRectangle(width=lebar * S, height=0.95 * S, corner_radius=0.47 * S,
                         fill_color=redup(LANGIT, 0.16), fill_opacity=1,
                         stroke_color=LANGIT, stroke_width=2.5 * S)
    ic.move_to(r.get_left() + RIGHT * 0.5 * S)
    t.next_to(ic, RIGHT, buff=0.3 * S)
    return VGroup(r, ic, t)


def ikon_hp(color=ABU, u=1.0):
    b = RoundedRectangle(width=0.55 * S * u, height=0.95 * S * u, corner_radius=0.09 * S * u,
                         stroke_color=color, stroke_width=3 * S, fill_color=PERMUKAAN, fill_opacity=1)
    l = RoundedRectangle(width=0.42 * S * u, height=0.68 * S * u, corner_radius=0.04 * S * u,
                         stroke_width=0, fill_color=redup(color, 0.4), fill_opacity=1).move_to(b).shift(UP * 0.04 * S * u)
    d = Dot(radius=0.03 * S * u, color=color).move_to(b.get_bottom() + UP * 0.08 * S * u)
    return VGroup(b, l, d)


def kartu_produk(s=PRODUK, aksen=None):
    hp = ikon_hp(TINTA if aksen is None else aksen)
    t = teks(s, color=TINTA, size="body", weight=MEDIUM)
    sub = caption("stok ada · dikirim hari ini")
    isi = VGroup(hp, VGroup(t, sub).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
                 ).arrange(RIGHT, buff=SP["m"])
    return kartu(isi, aksen=aksen, pad=0.35)


def titik(label, p, color=TINTA, arah=UP, size="caption", r=0.09):
    d = Dot(p, radius=r * S, color=color)
    t = teks(label, color=color, size=size, weight=MEDIUM).next_to(d, arah, buff=0.12 * S)
    return VGroup(d, t)


def vektor(nilai, color=JINGGA, size="caption"):
    s = "[" + ", ".join(nilai) + ", …]"
    return mono(s, color=color, size=size)


def stempel(s, color=SAGA):
    t = mono(s, color=color, size="h2", weight=BOLD)
    r = RoundedRectangle(width=t.width + 0.4 * S, height=t.height + 0.3 * S,
                         corner_radius=0.08 * S, stroke_color=color, stroke_width=4 * S,
                         fill_color=HITAM, fill_opacity=0.6)
    t.move_to(r)
    return VGroup(r, t).rotate(0.18)


# ---------------------------------------------------------------------------
class EmbeddingKalauKamuBikin(KapurScene):
    PREFIX = "A_"

    def mark(self, nama):
        if not os.environ.get("STILLS"):
            return
        out = _DIR / "preview" / ORIENT
        out.mkdir(parents=True, exist_ok=True)
        self.renderer.update_frame(self, ignore_skipping=True)
        self.renderer.camera.get_image().save(out / f"{self.PREFIX}{nama}.png")

    def bab(self, s):
        nb = label_bab(s)
        if self._bab is None:
            self.play(FadeIn(nb), run_time=CEPAT)
        else:
            self.play(FadeTransform(self._bab, nb), run_time=CEPAT)
        self._bab = nb

    def kosongkan(self):
        self.tanpa_header(0.3)
        self.bersihkan(CEPAT)

    def tapi(self, s, y=-3.6, size="h1"):
        t = judul(s, color=SAGA, size=size)
        kiri(t, y)
        self.play(FadeIn(t, shift=UP * GESER), run_time=CEPAT)
        return t

    def construct(self):
        for f in (self.pembuka, self.cocok_persis, self.sinonim, self.peta, self.belajar,
                  self.banyak_sumbu, self.deret_angka, self.ketemu, self.selamat):
            t0 = self.renderer.time
            f()
            print(f"[waktu] {f.__name__:14s} {t0:6.1f} -> {self.renderer.time:6.1f}")

    # 1 ----------------------------------------------------------------------
    def pembuka(self):
        self.bab("Kalau kamu yang bikin… #3")
        l1 = judul("Kamu bikin", size="h1")
        l2 = judul("toko online.", color=KUNYIT, size="display")
        g = VGroup(l1, l2).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        kiri(g, 4.9)
        ul = coret_kapur(l2)
        orang = ikon_orang(LANGIT, 1.0)
        lab1 = caption("pembeli ngetik:", color=LANGIT)
        cari = kolom_cari()
        kiri(lab1, 2.6)
        kiri(cari, 1.8)
        orang.next_to(lab1, RIGHT, buff=SP["s"])
        tanda = mono("?", color=ABU, size="display").move_to(pos(0, 0.3))
        lab2 = caption("produkmu tertulis:")
        kiri(lab2, -1.0)
        prod = kartu_produk()
        kiri(prod, -2.2)

        self.play(FadeIn(l1, shift=UP * GESER), Write(l2), run_time=KETUK)
        self.play(Create(ul), FadeIn(lab1), FadeIn(orang), FadeIn(cari, shift=UP * GESER), run_time=KETUK)
        self.play(FadeIn(tanda), FadeIn(lab2), FadeIn(prod, shift=UP * GESER), run_time=KETUK)
        self.mark("01_pembuka")
        self.wait(JEDA)
        self.kosongkan()

    # 2 ----------------------------------------------------------------------
    def cocok_persis(self):
        self.header("Gampang: cari kata yang sama")
        a = mono("murah", color=LANGIT, size="h1")
        ne = mono("≠", color=SAGA, size="h1")
        b = mono("terjangkau", color=TINTA, size="h1")
        VGroup(a, ne, b).arrange(RIGHT, buff=SP["m"], aligned_edge=DOWN)
        kiri(VGroup(a, ne, b), 3.0)
        la = caption("diketik pembeli").next_to(a, UP, buff=SP["s"]).align_to(a, LEFT)
        lb = caption("di produkmu").next_to(b, UP, buff=SP["s"]).align_to(b, LEFT)
        self.play(FadeIn(a), FadeIn(la), FadeIn(b), FadeIn(lb), run_time=CEPAT + 0.2)
        self.wait(0.6)
        self.play(FadeIn(ne, scale=1.4), run_time=CEPAT)
        cari = kolom_cari(lebar=7.2)
        kiri(cari, 0.0)
        hasil = VGroup(mono("0", color=JINGGA, size="display", weight=BOLD),
                       teks("hasil", color=ABU, size="h2")).arrange(RIGHT, buff=SP["s"], aligned_edge=DOWN)
        kiri(hasil, -1.5)
        self.play(FadeIn(cari, shift=UP * GESER), run_time=CEPAT)
        t = self.tapi("Tapi… beda huruf.", y=-3.3)
        self.play(FadeIn(hasil, shift=UP * GESER), run_time=CEPAT)
        self.mark("02_nol")
        self.wait(JEDA)
        self.kosongkan()

    # 3 ----------------------------------------------------------------------
    def sinonim(self):
        self.header("Jadi: bikin daftar sinonim")
        baris = VGroup(
            VGroup(teks("murah", color=LANGIT, size="body"), mono("=", color=ABU, size="body"),
                   teks("terjangkau", size="body"), teks("✓", color=DAUN, size="body")
                   ).arrange(RIGHT, buff=SP["s"]))
        kiri(baris, 4.3)
        self.play(FadeIn(baris, shift=UP * GESER), run_time=CEPAT)
        self.wait(0.8)
        kata = ["miring", "ramah kantong", "murmer", "hemat", "nggak nguras dompet",
                "budget", "harga pelajar", "worth it", "murceee"]
        pos_ = [(-2.6, 2.9), (0.9, 2.9), (-2.4, 1.9), (0.3, 1.9), (-1.2, 0.9),
                (2.4, 1.9), (-2.4, -0.1), (0.7, -0.1), (2.3, -1.0)]
        pils = VGroup(*[pil(k, LANGIT if i < 3 else ABU, size="body") for i, k in enumerate(kata)])
        x, yy, rowh = 0.0, 0.0, pils[0].height + 0.3 * S
        for p in pils:
            if x + p.width > LEBAR_AMAN:
                x, yy = 0.0, yy - rowh
            p.move_to([x + p.width / 2, yy, 0])
            x += p.width + 0.25 * S
        lab = caption("pembeli juga ngetik:")
        kiri(lab, 3.3)
        pils.next_to(lab, DOWN, buff=SP["m"]).align_to(lab, LEFT)
        self.play(FadeIn(lab), LaggedStart(*[FadeIn(p, shift=DOWN * GESER) for p in pils[:3]],
                                           lag_ratio=0.3), run_time=KETUK)
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * GESER) for p in pils[3:]], lag_ratio=0.15),
                  run_time=KETUK)
        self.tapi("Tapi… nggak ada habisnya.", y=-3.2)
        self.mark("03_sinonim")
        self.wait(JEDA)
        self.kosongkan()

    # 4 ----------------------------------------------------------------------
    def peta(self):
        self.header("Jadi: kasih posisi di peta")
        y0 = 1.0
        garis = Line(pos(-3.5, y0), pos(3.5, y0), color=ABU_GELAP, stroke_width=3 * S)
        ujung = VGroup(mono("← lebih murah", color=ABU, size="mikro"), mono("lebih mahal →", color=ABU, size="mikro"))
        ujung[0].next_to(garis, DOWN, buff=1.5 * S).align_to(garis, LEFT)
        ujung[1].next_to(garis, DOWN, buff=1.5 * S).align_to(garis, RIGHT)
        sumbu = mono("sumbu: HARGA", color=ABU, size="caption").next_to(garis, UP, buff=1.6 * S)
        sumbu.align_to(garis, LEFT)
        self.play(Create(garis), FadeIn(ujung), FadeIn(sumbu), run_time=KETUK)

        data = [("murah", -3.0, UP, LANGIT), ("terjangkau", -2.2, DOWN, TINTA),
                ("mahal", 3.0, UP, TINTA), ("premium", 2.2, DOWN, TINTA)]
        pts = VGroup(*[titik(s, pos(x, y0), c, arah=a, size="body") for s, x, a, c in data])
        self.play(LaggedStart(*[FadeIn(p, scale=0.6) for p in pts], lag_ratio=0.25), run_time=KETUK)
        kel = SurroundingRectangle(VGroup(pts[0], pts[1]), color=DAUN, buff=0.18 * S,
                                   corner_radius=0.2 * S, stroke_width=3 * S)
        dk = teks("berdekatan", color=DAUN, size="body", weight=MEDIUM).next_to(kel, UP, buff=SP["s"])
        dk.align_to(kel, LEFT)
        self.play(Create(kel), FadeIn(dk), run_time=CEPAT + 0.2)
        self.mark("04_peta")
        self.wait(JEDA + 0.6)
        self.p = dict(garis=garis, pts=pts, y0=y0)
        self.play(FadeOut(kel), FadeOut(dk), FadeOut(ujung), FadeOut(sumbu), run_time=CEPAT)

    # 5 ----------------------------------------------------------------------
    def belajar(self):
        garis, pts, y0 = self.p["garis"], self.p["pts"], self.p["y0"]
        t = self.tapi("Tapi… siapa yang ngisi", y=-1.4, size="h2")
        t2 = judul("posisi jutaan kata?", color=SAGA, size="h2").next_to(t, DOWN, buff=SP["xs"]).align_to(t, LEFT)
        self.play(FadeIn(t2, shift=UP * GESER), run_time=CEPAT)
        self.wait(1.2)
        self.play(FadeOut(VGroup(t, t2)), run_time=CEPAT)
        self.header("Jadi: belajar dari kalimat")

        # pindahkan peta ke bawah, kalimat di atas
        self.play(VGroup(garis, pts).animate.shift(DOWN * 3.0 * S), run_time=CEPAT)
        a = teks("“HP ini", size="body")
        slot = RoundedRectangle(width=2.6 * S, height=0.7 * S, corner_radius=0.1 * S,
                                stroke_color=KUNYIT, stroke_width=3 * S, fill_color=redup(KUNYIT, 0.15),
                                fill_opacity=1)
        b = teks("banget,", size="body")
        kal = VGroup(a, slot, b).arrange(RIGHT, buff=SP["s"])
        c = teks("cuma sejuta.”", size="body")
        kal2 = VGroup(kal, c).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        kiri(kal2, 3.9)
        self.play(FadeIn(kal2, shift=UP * GESER), run_time=CEPAT)
        isi = ["murah", "terjangkau", "miring"]
        cur = None
        for k, s in enumerate(isi):
            w = teks(s, color=LANGIT if k == 0 else TINTA, size="body", weight=MEDIUM).move_to(slot)
            if cur is None:
                self.play(FadeIn(w, shift=DOWN * GESER), run_time=CEPAT)
            else:
                self.play(FadeOut(cur, shift=DOWN * GESER), FadeIn(w, shift=DOWN * GESER), run_time=CEPAT)
            cur = w
            self.wait(0.3)
        # tambah "miring" ke peta, lalu rapatkan kelompok murah
        g0 = garis.get_y()
        mir = titik("miring", np.array([pos(0.2, 0)[0], g0, 0]), TINTA, arah=UP, size="body")
        self.play(FadeIn(mir, scale=0.6), run_time=CEPAT)
        target_x = [-2.75, -2.1, None, None]
        anim = [pts[0].animate.shift(RIGHT * 0.1 * S), pts[1].animate.shift(LEFT * 0.1 * S),
                mir.animate.shift(LEFT * 1.4 * S)]
        self.play(*anim, run_time=KETUK)
        cap = caption("muncul di kalimat mirip → dapat posisi mirip", color=DAUN)
        kiri(cap, 1.0)
        self.play(FadeIn(cap), run_time=CEPAT)
        self.mark("05_belajar")
        self.wait(JEDA)
        self.kosongkan()

    # 6 ----------------------------------------------------------------------
    def banyak_sumbu(self):
        self.header("Tapi… satu sumbu kurang", color=SAGA)
        bisa = judul("“bisa”", size="display")
        kiri(bisa, 4.0)
        a1 = teks("= mampu", color=TINTA, size="body").next_to(bisa, RIGHT, buff=SP["m"]).shift(UP * 0.3 * S)
        a2 = teks("= racun ular", color=TINTA, size="body").next_to(a1, DOWN, buff=SP["s"]).align_to(a1, LEFT)
        self.play(FadeIn(bisa), run_time=CEPAT)
        self.play(FadeIn(a1, shift=RIGHT * GESER), FadeIn(a2, shift=RIGHT * GESER), run_time=KETUK)
        self.wait(0.6)

        grid = grid_titik(7.2, 4.6).move_to(pos(0, 0.0))
        lab_y = mono("sumbu 2", color=ABU, size="mikro").next_to(grid, UP, buff=SP["xs"]).align_to(grid, LEFT)
        self.play(FadeIn(grid), FadeIn(lab_y), run_time=KETUK)
        c = grid.c2p
        pts = VGroup(
            titik("bisa (mampu)", c(-2.6, 1.8), LANGIT, UP),
            titik("sanggup", c(-1.7, 1.1), TINTA, DOWN),
            titik("bisa (racun)", c(2.1, -1.4), LANGIT, UP),
            titik("ular", c(3.0, -2.1), TINTA, UP),
            titik("murah", c(-2.6, -1.9), TINTA, UP),
        )
        self.play(LaggedStart(*[FadeIn(p, scale=0.6) for p in pts], lag_ratio=0.2), run_time=KETUK)
        n = VGroup(teks("Aslinya:", color=TINTA, size="body", weight=MEDIUM),
                   mono("ratusan–ribuan sumbu", color=JINGGA, size="body", weight=BOLD)
                   ).arrange(RIGHT, buff=SP["s"])
        kiri(n, -3.0)
        cat = caption("dan sumbunya nggak punya nama kayak “harga”")
        kiri(cat, -3.75)
        self.play(FadeIn(n, shift=UP * GESER), FadeIn(cat), run_time=CEPAT + 0.2)
        self.mark("06_sumbu")
        self.wait(JEDA + 0.4)
        self.kosongkan()

    # 7 ----------------------------------------------------------------------
    def deret_angka(self):
        self.header("Tiap kalimat jadi deretan angka")
        rows = [
            (PRODUK, ["0.12", "−0.83", "0.47", "0.05"], TINTA, None),
            (CARI, ["0.10", "−0.79", "0.51", "0.02"], LANGIT, DAUN),
            ("HP mahal", ["0.15", "0.61", "−0.40", "0.33"], TINTA, SAGA),
        ]
        grp = VGroup()
        for s, v, col, tanda in rows:
            t = teks(f"“{s}”", color=col, size="body", weight=MEDIUM)
            vv = vektor(v, size="body")
            g = VGroup(t, vv).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
            grp.add(g)
        grp.arrange(DOWN, buff=SP["l"] + 0.2, aligned_edge=LEFT)
        kiri(grp, 1.3)
        self.play(FadeIn(grp[0][0]), run_time=CEPAT)
        self.play(TransformFromCopy(grp[0][0], grp[0][1]), run_time=KETUK)
        self.play(FadeIn(grp[1], shift=UP * GESER), run_time=KETUK)
        self.play(FadeIn(grp[2], shift=UP * GESER), run_time=KETUK)
        m1 = pil("mirip → dekat", DAUN).next_to(grp[1][0], RIGHT, buff=SP["m"])
        m2 = pil("beda → jauh", SAGA).next_to(grp[2][0], RIGHT, buff=SP["m"])
        cat = caption("angka ilustrasi")
        kiri(cat, -3.8)
        self.play(FadeIn(m1), FadeIn(m2), FadeIn(cat), run_time=CEPAT)
        self.mark("07_angka")
        self.wait(JEDA + 0.6)
        self.kosongkan()

    # 8 ----------------------------------------------------------------------
    def ketemu(self):
        self.header("Sekarang…")
        cari = kolom_cari()
        kiri(cari, 4.0)
        self.play(FadeIn(cari, shift=UP * GESER), run_time=CEPAT)
        lab = caption("hasil teratas:")
        kiri(lab, 2.6)
        prod = kartu_produk(aksen=DAUN)
        kiri(prod, 1.4)
        ok = pil("ketemu", DAUN, size="caption").next_to(prod, DOWN, buff=SP["m"]).align_to(prod, LEFT)
        self.play(FadeIn(lab), FadeIn(prod, shift=UP * GESER), run_time=KETUK)
        self.play(FadeIn(ok, scale=0.9), run_time=CEPAT)
        c1 = judul("Walau kata “murah”-nya", color=TINTA, size="h2")
        c2 = judul("nggak ada sama sekali.", color=KUNYIT, size="h2")
        cc = VGroup(c1, c2).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
        kiri(cc, -2.4)
        self.play(FadeIn(c1, shift=UP * GESER), FadeIn(c2, shift=UP * GESER), run_time=CEPAT + 0.2)
        self.mark("08_ketemu")
        self.wait(JEDA + 0.6)
        self.kosongkan()

    # 9 ----------------------------------------------------------------------
    def selamat(self):
        s1 = judul("Selamat.", size="display").move_to(pos(0, 4.4))
        kiri(s1, 4.4)
        s2 = judul("Kamu baru aja bikin", color=ABU, size="h2").next_to(s1, DOWN, buff=SP["m"]).align_to(s1, LEFT)
        emb = judul("Embedding", color=DAUN, size="raksasa").next_to(s2, DOWN, buff=SP["m"]).align_to(s1, LEFT)
        sub = teks("kata & kalimat → deretan angka bermakna", color=ABU, size="caption")
        sub.next_to(emb, DOWN, buff=SP["m"]).align_to(s1, LEFT)
        self.play(FadeIn(s1, shift=UP * GESER), run_time=CEPAT + 0.1)
        self.play(FadeIn(s2), run_time=CEPAT)
        self.play(Write(emb), run_time=KETUK)
        ul = coret_kapur(emb, color=DAUN)
        self.play(Create(ul), FadeIn(sub), run_time=CEPAT + 0.2)
        self.wait(1.2)
        lab = caption("dipakai di:", color=ABU)
        p = VGroup(pil("RAG: cari potongan dokumen yang pas", TOSKA),
                   pil("AI ngerti maksudmu walau katanya beda", TOSKA)
                   ).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        VGroup(lab, p).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        kiri(VGroup(lab, p), -1.6)
        self.play(FadeIn(lab), LaggedStart(*[FadeIn(x, shift=UP * GESER) for x in p], lag_ratio=0.4),
                  run_time=KETUK)
        self.mark("09_selamat")
        self.wait(JEDA_PANJANG + 1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=KETUK)
