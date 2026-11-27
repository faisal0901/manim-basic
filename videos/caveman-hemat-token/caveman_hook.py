"""
Video umum "Caveman hemat token? Iya, tapi…", gaya B (hook biasa), design system KAPUR.

Ide: plugin caveman memangkas token JAWABAN (output yang kamu baca), bukan token
REASONING (coretan mikir) dan bukan input. Padahal reasoning juga dihitung & dibayar.

Fakta dari README caveman: "65% fewer output tokens" (output saja), contoh 69 -> 19 token,
"Input and reasoning tokens are untouched", skill menambah ~1-1.5k token input per giliran.
Angka 3.000 / 1.200 / 300 = CONTOH FIKTIF untuk proporsi.

Frame kunci:  STILLS=1 ORIENT=vertical manim -s -ql caveman_hook.py CavemanHook
Video penuh:  ORIENT=vertical manim -qh caveman_hook.py CavemanHook
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

TANYA = "Gaji 2 juta, makan sebulan gimana?"
JAWAB_BIASA = ["Tentu! Dengan gaji Rp2 juta, berikut", "rencana menu hemat sebulan", "yang tetap bergizi…"]
JAWAB_CAVE = "Telur. Tempe. Sayur. Muat."

# (teks, coretan atau False) -> coretan mikir AI, muncul huruf per huruf
MIKIR = [
    ("hmm… gaji 2 juta sebulan", False),
    ("dibagi 30… 66rb sehari", False),
    ("belum kos, bensin, cicilan…", False),
    ("ayam tiap hari?", "kemahalan"),
    ("salmon?", "mimpi"),
    ("oke: telur, tempe, sayur,", False),
    ("sesekali ayam. cek total…", False),
]


def kiri(m, y):
    m.move_to(pos(0, y)).align_to([AMAN["kiri"], 0, 0], LEFT)
    return m


def balon_ai(baris, color=TOSKA, size="caption", lebar=None):
    t = VGroup(*[teks(b, color=TINTA, size=size) for b in baris]).arrange(DOWN, buff=0.08 * S, aligned_edge=LEFT)
    r = RoundedRectangle(width=lebar or t.width + 0.5 * S, height=t.height + 0.42 * S,
                         corner_radius=0.18 * S, fill_color=redup(color, 0.22), fill_opacity=1,
                         stroke_color=color, stroke_width=2 * S)
    t.move_to(r).align_to(r, LEFT).shift(RIGHT * 0.25 * S)
    return VGroup(r, t)


def bar(nilai, skala, color, isi=1.0, h=0.55, stroke=None):
    w = max(0.06 * S, nilai * skala)
    return Rectangle(width=w, height=h * S, fill_color=color, fill_opacity=isi,
                     stroke_color=stroke or color, stroke_width=2 * S if stroke else 0)


def fmt(n):
    return f"{int(round(n)):,}".replace(",", ".")


class CavemanHook(KapurScene):
    PREFIX = "B_"

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

    def construct(self):
        for f in (self.hook, self.separuh, self.angka_jawaban, self.mikir, self.disembunyikan,
                  self.hitung, self.input_tambah, self.jujur, self.tips, self.penutup):
            t0 = self.renderer.time
            f()
            print(f"[waktu] {f.__name__:14s} {t0:6.1f} -> {self.renderer.time:6.1f}")

    # 1 hook -----------------------------------------------------------------
    def hook(self):
        self.bab("Token · Caveman")
        orang = ikon_orang(LANGIT, 1.0)
        q = gelembung(TANYA, LANGIT, size="caption")
        tq = VGroup(orang, q).arrange(RIGHT, buff=SP["s"])
        kiri(tq, 5.1)
        l1 = caption("AI biasa:")
        b1 = balon_ai(JAWAB_BIASA)
        l2 = caption("AI mode caveman:")
        b2 = balon_ai([JAWAB_CAVE], size="body")
        kiri(l1, 3.8)
        b1.next_to(l1, DOWN, buff=SP["s"]).align_to(l1, LEFT)
        l2.next_to(b1, DOWN, buff=SP["m"]).align_to(l1, LEFT)
        b2.next_to(l2, DOWN, buff=SP["s"]).align_to(l1, LEFT)
        klaim = VGroup(mono("−65%", color=JINGGA, size="raksasa", weight=BOLD),
                       judul("token?", color=TINTA, size="h1")).arrange(RIGHT, buff=SP["m"], aligned_edge=DOWN)
        kiri(klaim, -2.5)
        self.play(FadeIn(orang), FadeIn(q, shift=LEFT * GESER), run_time=CEPAT)
        self.play(FadeIn(l1), FadeIn(b1, shift=UP * GESER), run_time=CEPAT)
        self.play(FadeIn(l2), FadeIn(b2, shift=UP * GESER), run_time=CEPAT)
        self.play(FadeIn(klaim, scale=1.2), run_time=CEPAT + 0.2)
        self.mark("01_hook")
        self.wait(JEDA - 0.4)
        self.kosongkan()

    # 2 ----------------------------------------------------------------------
    def separuh(self):
        a = judul("Bener.", color=DAUN, size="display")
        b = judul("Tapi cuma", size="h1")
        c = judul("separuh cerita.", color=KUNYIT, size="display")
        g = VGroup(a, b, c).arrange(DOWN, buff=SP["m"], aligned_edge=LEFT)
        kiri(g, 2.0)
        self.play(FadeIn(a, shift=UP * GESER), run_time=CEPAT)
        self.play(FadeIn(b, shift=UP * GESER), Write(c), run_time=KETUK)
        self.play(Create(coret_kapur(c)), run_time=CEPAT)
        self.mark("02_separuh")
        self.wait(0.8)
        self.kosongkan()

    # 3 ----------------------------------------------------------------------
    def angka_jawaban(self):
        self.header("65% itu dari jawabannya")
        sub = caption("token jawaban · contoh dari pembuat caveman")
        kiri(sub, 4.7)
        skala = 6.6 / 69
        r1 = VGroup(teks("biasa", color=ABU, size="caption"), bar(69, skala, TOSKA)).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
        r2 = VGroup(teks("caveman", color=ABU, size="caption"), bar(19, skala, TOSKA)).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
        kiri(r1, 3.2)
        kiri(r2, 1.5)
        n1 = mono("69", color=JINGGA, size="h2", weight=BOLD).next_to(r1[1], DOWN, buff=SP["xs"]).align_to(r1[1], RIGHT)
        n2 = mono("19", color=JINGGA, size="h2", weight=BOLD).next_to(r2[1], RIGHT, buff=SP["s"])
        self.play(FadeIn(sub), FadeIn(r1[0]), GrowFromEdge(r1[1], LEFT), run_time=KETUK)
        self.play(FadeIn(n1), FadeIn(r2[0]), GrowFromEdge(r2[1], LEFT), run_time=KETUK)
        self.play(FadeIn(n2), run_time=CEPAT)
        cat = teks("yang kamu baca jadi lebih pendek", color=DAUN, size="body")
        kiri(cat, -0.3)
        self.play(FadeIn(cat, shift=UP * GESER), run_time=CEPAT)
        self.mark("03_jawaban")
        self.wait(JEDA)
        self.kosongkan()

    # 4 AI mikir (stream) ---------------------------------------------------
    def mikir(self):
        self.header("Padahal AI mikir dulu")
        # kertas buram
        lab_k = VGroup(Dot(radius=0.06 * S, color=TOSKA), mono("AI lagi mikir…", color=TOSKA, size="caption")
                       ).arrange(RIGHT, buff=SP["s"])
        kertas = RoundedRectangle(width=7.4 * S, height=5.4 * S, corner_radius=0.15 * S,
                                  fill_color=PERMUKAAN, fill_opacity=1,
                                  stroke_color=ABU_GELAP, stroke_width=2 * S)
        kiri(kertas, 1.9)
        lab_k.next_to(kertas.get_corner(UL), DR, buff=0.25 * S)
        nama = pil("kertas buram = reasoning", TOSKA, size="caption")
        nama.next_to(kertas, UP, buff=SP["s"]).align_to(kertas, LEFT)
        nama.set_opacity(0)
        # penghitung token
        tok = ValueTracker(0)
        ctr_lab = mono("token mikir:", color=ABU, size="caption")
        ctr = always_redraw(lambda: mono(fmt(tok.get_value()), color=JINGGA, size="h2", weight=BOLD)
                            .next_to(ctr_lab, RIGHT, buff=SP["s"]))
        ctr_lab.next_to(kertas, DOWN, buff=SP["s"]).align_to(kertas, LEFT)
        self.play(FadeIn(kertas), FadeIn(lab_k), FadeIn(ctr_lab), run_time=CEPAT)
        self.add(ctr)

        baris = []
        y = lab_k.get_bottom()[1] - 0.35 * S
        x0 = kertas.get_left()[0] + 0.3 * S
        total = 3000
        langkah = total / len(MIKIR)
        for k, (s, coret) in enumerate(MIKIR):
            t = mono(s, color=ABU if not k >= 5 else TINTA, size="caption")
            t.move_to([x0 + t.width / 2, y - t.height / 2, 0])
            rt = 0.06 * len(s)
            self.play(AddTextLetterByLetter(t, time_per_char=0.035),
                      tok.animate.set_value(langkah * (k + 0.7)), run_time=max(0.6, rt), rate_func=linear)
            g = VGroup(t)
            if coret:
                ln = Line(t.get_left(), t.get_right(), color=SAGA, stroke_width=3 * S)
                ket = mono(f"← {coret}", color=SAGA, size="caption").next_to(t, RIGHT, buff=SP["s"])
                self.play(Create(ln), FadeIn(ket, shift=LEFT * 0.1), tok.animate.set_value(langkah * (k + 1)),
                          run_time=0.45)
                g.add(ln, ket)
            baris.append(g)
            y = t.get_bottom()[1] - 0.22 * S
        cek = mono("pas ✓", color=DAUN, size="body", weight=BOLD)
        cek.next_to(baris[-1], RIGHT, buff=SP["s"])
        self.play(FadeIn(cek, scale=1.3), tok.animate.set_value(total), run_time=CEPAT)
        self.mark("04_mikir")
        self.wait(0.4)

        # lembar jawaban
        jaw = balon_ai([JAWAB_CAVE], size="body")
        lab_j = pil("lembar jawaban", DAUN, size="caption")
        kiri(VGroup(lab_j), -2.25)
        jaw.next_to(lab_j, DOWN, buff=SP["s"]).align_to(lab_j, LEFT)
        nama.set_opacity(1)
        self.play(FadeIn(nama, shift=DOWN * GESER), run_time=CEPAT)
        self.play(FadeIn(lab_j), FadeIn(jaw, shift=UP * GESER), run_time=CEPAT)
        self.mark("05_jawaban")
        self.wait(JEDA)
        self.st = dict(kertas=kertas, baris=VGroup(*baris, cek, lab_k), nama=nama, ctr=ctr,
                       ctr_lab=ctr_lab, tok=tok, jaw=VGroup(jaw, lab_j))

    # 5 ----------------------------------------------------------------------
    def disembunyikan(self):
        st = self.st
        tutup = RoundedRectangle(width=st["kertas"].width, height=st["kertas"].height,
                                 corner_radius=0.15 * S, fill_color=HITAM, fill_opacity=0.97,
                                 stroke_width=0).move_to(st["kertas"])
        sem = VGroup(mono("▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒", color=ABU_GELAP, size="h1"),
                     mono("sering nggak ditampilkan", color=ABU, size="caption")
                     ).arrange(DOWN, buff=SP["s"]).move_to(st["kertas"])
        self.play(FadeIn(tutup), FadeIn(sem), run_time=KETUK)
        tok = st["tok"]
        self.play(tok.animate.set_value(3000), run_time=0.1)
        bayar = VGroup(judul("Tetap dihitung.", color=SAGA, size="h2"),
                       judul("Tetap dibayar.", color=SAGA, size="h2")).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
        bayar.next_to(st["ctr_lab"], RIGHT, buff=0).align_to(st["ctr_lab"], UP)
        kiri(bayar, -3.4)
        self.play(FadeOut(st["jaw"]), run_time=CEPAT)
        kiri(bayar, -2.6)
        self.play(FadeIn(bayar, shift=UP * GESER), run_time=CEPAT)
        self.mark("06_tersembunyi")
        self.wait(JEDA)
        self.remove(st["ctr"])
        self.kosongkan()

    # 6 ----------------------------------------------------------------------
    def hitung(self):
        self.header("Caveman cuma motong jawaban")
        skala = 7.0 / 4200
        def baris(lab, mik, jaw, y):
            l = teks(lab, color=ABU, size="caption", weight=MEDIUM)
            b1 = bar(mik, skala, redup(TOSKA, 0.5), stroke=TOSKA)
            b2 = bar(jaw, skala, TOSKA)
            b = VGroup(b1, b2).arrange(RIGHT, buff=0)
            n = mono(f"mikir {fmt(mik)}  +  jawab {fmt(jaw)}", color=JINGGA, size="caption")
            g = VGroup(l, b, n).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
            return kiri(g, y)
        r1 = baris("tanpa caveman", 3000, 1200, 3.4)
        r2 = baris("pakai caveman", 3000, 300, 0.9)
        self.play(FadeIn(r1[0]), GrowFromEdge(r1[1], LEFT), FadeIn(r1[2]), run_time=KETUK)
        self.wait(0.8)
        r2b = r2[1].copy()
        r2b[1].stretch_to_fit_width(1200 * skala).align_to(r2b[0], LEFT).shift(RIGHT * r2b[0].width)
        self.play(FadeIn(r2[0]), FadeIn(r2b), FadeIn(r2[2]), run_time=CEPAT + 0.2)
        self.play(Transform(r2b, r2[1]), run_time=LAMBAT)
        self.wait(0.5)
        h1 = mono("−65%", color=ABU, size="h1")
        h2 = VGroup(teks("total hemat:", color=TINTA, size="body"),
                    mono("−21%", color=JINGGA, size="display", weight=BOLD)).arrange(RIGHT, buff=SP["m"], aligned_edge=DOWN)
        kiri(h1, -1.4)
        h2.next_to(h1, RIGHT, buff=SP["l"]).align_to(h1, DOWN)
        coret = Line(h1.get_left(), h1.get_right(), color=SAGA, stroke_width=4 * S)
        cat = caption("angka contoh · rasio asli beda tiap tugas & model")
        kiri(cat, -3.0)
        self.play(FadeIn(h1), run_time=CEPAT)
        self.play(Create(coret), FadeIn(h2, shift=UP * GESER), FadeIn(cat), run_time=KETUK)
        self.mark("07_hitung")
        self.wait(JEDA + 0.6)
        self.st2 = dict(r2=VGroup(r2[0], r2b, r2[2]), rest=VGroup(r1, h1, coret, h2, cat))

    # 7 ----------------------------------------------------------------------
    def input_tambah(self):
        r2, rest = self.st2["r2"], self.st2["rest"]
        self.play(FadeOut(rest), run_time=CEPAT)
        self.header("Plus…")
        self.play(r2.animate.move_to(pos(0, 2.2)).align_to([AMAN["kiri"], 0, 0], LEFT), run_time=CEPAT)
        skala = 7.0 / 4200
        blk = bar(1000, skala, redup(LANGIT, 0.6), stroke=LANGIT)
        blk.next_to(r2[1], DOWN, buff=SP["l"]).align_to(r2[1], LEFT)
        lb = VGroup(mono("+~1.000", color=JINGGA, size="body", weight=BOLD),
                    teks("token instruksi caveman", color=TINTA, size="caption"),
                    ).arrange(RIGHT, buff=SP["s"]).next_to(blk, RIGHT, buff=SP["s"])
        lb2 = caption("masuk sebagai input, tiap giliran").next_to(blk, DOWN, buff=SP["s"]).align_to(blk, LEFT)
        self.play(GrowFromEdge(blk, LEFT), FadeIn(lb), run_time=KETUK)
        self.play(FadeIn(lb2), run_time=CEPAT)
        self.mark("08_input")
        self.wait(JEDA)
        self.kosongkan()

    # 8 ----------------------------------------------------------------------
    def jujur(self):
        self.header("Pembuatnya sendiri jujur")
        q = mono("“Input and reasoning tokens", color=TINTA, size="caption")
        q2 = mono(" are untouched.”", color=TINTA, size="caption")
        src = mono("— README caveman", color=ABU, size="mikro")
        qq = VGroup(q, q2, src).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
        kq = kartu(qq, pad=0.35)
        kiri(kq, 3.9)
        self.play(FadeIn(kq, shift=UP * GESER), run_time=CEPAT + 0.2)
        rows = [("✓", DAUN, "output (jawaban)", "dipotong"),
                ("✗", SAGA, "reasoning (mikir)", "utuh"),
                ("✗", SAGA, "input", "malah nambah")]
        g = VGroup()
        for ic, col, a, b in rows:
            g.add(VGroup(teks(ic, color=col, size="h2", weight=BOLD),
                         teks(a, color=TINTA, size="body"),
                         teks(b, color=col, size="body", weight=MEDIUM)).arrange(RIGHT, buff=SP["m"]))
        g.arrange(DOWN, buff=SP["m"], aligned_edge=LEFT)
        kiri(g, 0.9)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * GESER) for x in g], lag_ratio=0.35), run_time=KETUK + 0.4)
        rugi = teks("jawaban yang udah pendek? bisa malah rugi", color=SAGA, size="caption")
        kiri(rugi, -1.4)
        self.play(FadeIn(rugi), run_time=CEPAT)
        self.mark("09_jujur")
        self.wait(JEDA + 0.4)
        self.kosongkan()

    # 9 ----------------------------------------------------------------------
    def tips(self):
        self.header("Tips hemat beneran", color=DAUN)
        lab = caption("buat tugas gampang, turunkan level mikirnya:")
        kiri(lab, 4.6)
        track = RoundedRectangle(width=6.6 * S, height=0.22 * S, corner_radius=0.11 * S,
                                 fill_color=GARIS, fill_opacity=1, stroke_width=0)
        kiri(track, 3.6)
        knob = Circle(radius=0.24 * S, fill_color=DAUN, fill_opacity=1, stroke_width=0)
        knob.move_to(track.get_right() + LEFT * 0.3 * S)
        ujung = VGroup(mono("rendah", color=ABU, size="mikro").next_to(track, DOWN, buff=SP["s"]).align_to(track, LEFT),
                       mono("tinggi", color=ABU, size="mikro").next_to(track, DOWN, buff=SP["s"]).align_to(track, RIGHT))
        judul_s = mono("level mikir", color=TINTA, size="caption").next_to(track, UP, buff=SP["s"]).align_to(track, LEFT)
        kertas = RoundedRectangle(width=6.6 * S, height=3.2 * S, corner_radius=0.15 * S,
                                  fill_color=PERMUKAAN, fill_opacity=1, stroke_color=ABU_GELAP, stroke_width=2 * S)
        kiri(kertas, 0.6)
        garis = VGroup(*[Line(LEFT * 2.9 * S, RIGHT * (2.9 - (k % 3) * 0.9) * S, color=ABU_GELAP, stroke_width=3 * S)
                         for k in range(8)]).arrange(DOWN, buff=0.28 * S, aligned_edge=LEFT).move_to(kertas)
        ket = mono("token mikir", color=ABU, size="mikro").next_to(kertas, UP, buff=SP["xs"]).align_to(kertas, RIGHT)
        self.play(FadeIn(lab), FadeIn(track), FadeIn(knob), FadeIn(ujung), FadeIn(judul_s), run_time=CEPAT + 0.2)
        self.play(FadeIn(kertas), FadeIn(garis), FadeIn(ket), run_time=CEPAT)
        kertas2 = kertas.copy().stretch_to_fit_height(0.9 * S).align_to(kertas, UP)
        garis2 = garis[:2].copy()
        self.play(knob.animate.move_to(track.get_left() + RIGHT * 0.3 * S),
                  Transform(kertas, kertas2), FadeOut(garis[2:]),
                  garis[:2].animate.move_to(kertas2), run_time=LAMBAT)
        opsi = VGroup(teks("• mode mikir rendah", color=TINTA, size="body"),
                      teks("• atau model tanpa reasoning", color=TINTA, size="body")
                      ).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        kiri(opsi, -0.9)
        hasil = teks("yang kepotong: kertas buramnya", color=DAUN, size="body", weight=MEDIUM)
        kiri(hasil, -2.7)
        self.play(FadeIn(opsi, shift=UP * GESER), run_time=CEPAT + 0.2)
        self.play(FadeIn(hasil), run_time=CEPAT)
        self.mark("10_tips")
        self.wait(JEDA + 0.6)
        self.kosongkan()

    # 10 ---------------------------------------------------------------------
    def penutup(self):
        a = judul("Caveman bikin jawaban", size="h1")
        b = judul("enak dibaca.", color=DAUN, size="h1")
        c = judul("Tapi soal hemat, yang mahal", color=ABU, size="h2")
        d = judul("sering bukan jawabannya.", color=ABU, size="h2")
        e = judul("Tapi mikirnya.", color=KUNYIT, size="display")
        g = VGroup(VGroup(a, b).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT),
                   VGroup(c, d).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT), e
                   ).arrange(DOWN, buff=SP["l"], aligned_edge=LEFT)
        kiri(g, 2.2)
        self.play(FadeIn(g[0], shift=UP * GESER), run_time=CEPAT + 0.2)
        self.wait(1.0)
        self.play(FadeIn(g[1], shift=UP * GESER), run_time=CEPAT + 0.2)
        self.wait(0.8)
        self.play(Write(e), run_time=KETUK)
        self.play(Create(coret_kapur(e)), run_time=CEPAT)
        self.mark("11_penutup")
        self.wait(JEDA_PANJANG)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=KETUK)
