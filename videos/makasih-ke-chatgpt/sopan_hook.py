"""
Video umum "Bilang makasih ke ChatGPT = buang duit?", gaya B, design system KAPUR.

Fakta: Sam Altman (X, April 2025): "tens of millions of dollars well spent — you never know".
Token asli GPT-4o (o200k_base, js-tiktoken): "makasih ya kak 🙏🙏" = 8 token
(mak · as · ih · ␣ya · ␣kak · [🙏 pertama terpecah 2] · 🙏), "please" = 1, "tolong" = 2 (tol · ong).
"Sejuta orang" / 8 juta token = hitungan contoh.

Emoji tidak bisa dirender Text (Pango -> SVG), jadi 🙏 digambar sebagai ikon vektor.

Frame kunci:  STILLS=1 ORIENT=vertical manim -s -ql sopan_hook.py SopanHook
Video penuh:  ORIENT=vertical manim -qh sopan_hook.py SopanHook
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
KULIT = "#E8B98A"   # warna ikon tangan (ilustrasi, bukan warna peran)
WARNA_TOK = [LANGIT, UNGU, "#E58BB4", "#7FA8F5"]


def kiri(m, y):
    m.move_to(pos(0, y)).align_to([AMAN["kiri"], 0, 0], LEFT)
    return m


def ikon_doa(u=1.0):
    """Ikon 'tangan berdoa' sederhana pengganti emoji 🙏."""
    s = u * S
    tangan = VGroup()
    for sgn in (-1, 1):
        t = RoundedRectangle(width=0.2 * s, height=0.55 * s, corner_radius=0.1 * s,
                             fill_color=KULIT, fill_opacity=1, stroke_color="#B98C62", stroke_width=1.5 * S)
        t.rotate(-sgn * 0.22).shift(RIGHT * sgn * 0.085 * s)
        tangan.add(t)
    lengan = VGroup(*[Rectangle(width=0.2 * s, height=0.14 * s, fill_color=LANGIT, fill_opacity=1, stroke_width=0)
                      .move_to([sgn * 0.16 * s, -0.3 * s, 0]) for sgn in (-1, 1)])
    return VGroup(lengan, tangan)


def blok(isi, color=LANGIT, size="body"):
    if isinstance(isi, str):
        t = mono(isi.strip() or "␣", color=TINTA, size=size)
    else:
        t = isi
    h = mono("Agy", size=size).height + 0.32 * S
    h = max(h, t.height + 0.2 * S)
    r = RoundedRectangle(width=max(t.width + 0.3 * S, 0.55 * S), height=h, corner_radius=0.1 * S,
                         fill_color=redup(color, 0.28), fill_opacity=1, stroke_color=color, stroke_width=2 * S)
    t.move_to(r)
    return VGroup(r, t)


def balon(isi, color, size="caption"):
    """Balon chat. isi = str atau Mobject."""
    t = teks(isi, color=TINTA, size=size) if isinstance(isi, str) else isi
    r = RoundedRectangle(width=t.width + 0.5 * S, height=t.height + 0.42 * S, corner_radius=0.18 * S,
                         fill_color=redup(color, 0.22), fill_opacity=1, stroke_color=color, stroke_width=2 * S)
    t.move_to(r)
    return VGroup(r, t)


def isi_makasih(size="body"):
    t = teks("makasih ya kak", color=TINTA, size=size)
    d1, d2 = ikon_doa(0.75), ikon_doa(0.75)
    return VGroup(t, d1, d2).arrange(RIGHT, buff=0.12 * S)


def tetes(color=LANGIT, u=1.0):
    s = u * S
    c = Circle(radius=0.08 * s, fill_color=color, fill_opacity=1, stroke_width=0)
    tr = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.075 * s).next_to(c, UP, buff=-0.035 * s)
    return VGroup(c, tr)


def fmt(n):
    return f"{int(round(n)):,}".replace(",", ".")


class SopanHook(KapurScene):
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
        self.play(FadeIn(nb), run_time=CEPAT)
        self._bab = nb

    def kosongkan(self):
        self.tanpa_header(0.3)
        self.bersihkan(CEPAT)

    def construct(self):
        for f in (self.hook, self.kutipan, self.token, self.balasan, self.sejuta,
                  self.tips, self.bonus, self.penutup):
            t0 = self.renderer.time
            f()
            print(f"[waktu] {f.__name__:10s} {t0:6.1f} -> {self.renderer.time:6.1f}")

    # 1 ----------------------------------------------------------------------
    def hook(self):
        self.bab("Token · Sopan santun")
        orang = ikon_orang(LANGIT, 1.0)
        b = balon(isi_makasih(), LANGIT)
        chat = VGroup(b, orang).arrange(RIGHT, buff=SP["s"])
        chat.move_to(pos(0, 3.6)).align_to([AMAN["kanan"], 0, 0], RIGHT)
        ctr = VGroup(mono("token", color=ABU, size="caption"),
                     mono("+8", color=JINGGA, size="h1", weight=BOLD)).arrange(RIGHT, buff=SP["s"], aligned_edge=DOWN)
        kiri(ctr, 2.0)
        l1 = judul("Bilang makasih ke ChatGPT", size="h1")
        l2 = judul("buang duit?", color=KUNYIT, size="raksasa")
        g = VGroup(l1, l2).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        kiri(g, -0.6)
        self.play(FadeIn(orang), FadeIn(b, shift=LEFT * GESER * 2), run_time=CEPAT + 0.1)
        self.play(FadeIn(ctr, shift=UP * GESER), run_time=CEPAT)
        self.play(FadeIn(l1, shift=UP * GESER), Write(l2), run_time=KETUK)
        self.mark("01_hook")
        self.wait(JEDA - 0.6)
        self.kosongkan()

    # 2 ----------------------------------------------------------------------
    def kutipan(self):
        self.header("Kata CEO OpenAI")
        q1 = judul("“tens of millions of dollars", size="h2")
        q2 = judul("well spent —", color=DAUN, size="h2")
        q3 = judul("you never know.”", size="h2")
        src = mono("Sam Altman, di X · April 2025", color=ABU, size="mikro")
        qq = VGroup(q1, q2, q3, src).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        kq = kartu(qq, pad=0.4)
        kiri(kq, 2.6)
        arti = VGroup(teks("sopan santun pengguna =", color=TINTA, size="body"),
                      mono("puluhan juta dolar", color=JINGGA, size="h2", weight=BOLD)
                      ).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        kiri(arti, -0.9)
        cat = caption("jawaban santai di media sosial, bukan hitungan resmi")
        kiri(cat, -2.4)
        self.play(FadeIn(kq, shift=UP * GESER), run_time=KETUK)
        self.play(FadeIn(arti, shift=UP * GESER), FadeIn(cat), run_time=CEPAT + 0.2)
        self.mark("02_kutipan")
        self.wait(JEDA + 1.0 + 1.5)
        self.kosongkan()

    # 3 ----------------------------------------------------------------------
    def token(self):
        self.header("Semua ketikan = token")
        kal = balon(isi_makasih(), LANGIT)
        kiri(kal, 4.3)
        self.play(FadeIn(kal), run_time=CEPAT)
        tok = ["mak", "as", "ih", " ya", " kak"]
        bl = VGroup(*[blok(s, WARNA_TOK[i % 4]) for i, s in enumerate(tok)])
        pec = VGroup(blok("�", WARNA_TOK[1]), blok("�", WARNA_TOK[2]))
        utuh = blok(ikon_doa(0.6), WARNA_TOK[3])
        semua = VGroup(*bl, *pec, utuh)
        semua.arrange(RIGHT, buff=0.12 * S)
        if semua.width > LEBAR_AMAN:
            semua.scale_to_fit_width(LEBAR_AMAN)
        # dua baris supaya besar
        row1 = VGroup(*bl).arrange(RIGHT, buff=0.12 * S)
        row2 = VGroup(*pec, utuh).arrange(RIGHT, buff=0.12 * S)
        kiri(row1, 2.4)
        kiri(row2, 1.0)
        self.play(ReplacementTransform(kal.copy(), VGroup(row1, row2)), run_time=LAMBAT)
        br = Brace(pec, DOWN, color=ABU)
        lb = VGroup(ikon_doa(0.6), teks("kepotong jadi 2 token", color=TINTA, size="caption")
                    ).arrange(RIGHT, buff=SP["s"]).next_to(br, DOWN, buff=SP["s"]).align_to(pec, LEFT)
        jml = VGroup(mono("8", color=JINGGA, size="raksasa", weight=BOLD),
                     teks("token", color=TINTA, size="h2")).arrange(RIGHT, buff=SP["s"], aligned_edge=DOWN)
        kiri(jml, -2.2)
        cat = mono("tokenizer GPT-4o · beda model, beda pecahan", color=ABU, size="mikro")
        kiri(cat, -3.4)
        self.play(GrowFromCenter(br), FadeIn(lb), run_time=CEPAT + 0.2)
        self.play(FadeIn(jml, scale=1.2), FadeIn(cat), run_time=CEPAT + 0.2)
        self.mark("03_token")
        self.wait(JEDA + 1.2)
        self.kosongkan()

    # 4 ----------------------------------------------------------------------
    def balasan(self):
        self.header("Yang mahal: balasannya")
        lab = caption("mau bales “makasih”… tapi AI baca ulang dari awal:")
        kiri(lab, 4.75)
        riw = [("bikinin resep seblak dong", LANGIT), ("Tentu! Bahan: kerupuk, kencur…", TOSKA),
               ("eh aku abis putus…", LANGIT), ("Peluk virtual. Mau cerita?", TOSKA),
               ("revisi bab 2 skripsiku", LANGIT), ("Ini versi revisinya: …", TOSKA),
               ("caption IG buat foto kopi", LANGIT)]
        tumpuk = VGroup(*[balon(t, c, size="mikro") for t, c in riw])
        tumpuk.add(balon(isi_makasih("mikro"), LANGIT))
        tumpuk.arrange(DOWN, buff=0.12 * S, aligned_edge=LEFT)
        tumpuk.next_to(lab, DOWN, buff=SP["m"]).align_to(lab, LEFT)
        for k, m in enumerate(tumpuk):
            if k % 2 == 1:
                m.shift(RIGHT * 0.35 * S)
        ai = ikon_ai(1.2).move_to(pos(2.75, 0.2))
        self.play(FadeIn(lab), LaggedStart(*[FadeIn(x, shift=UP * GESER) for x in tumpuk], lag_ratio=0.08),
                  FadeIn(ai), run_time=KETUK)

        # scanning: sorot + garis pemindai menyapu tiap pesan, penghitung naik
        tok = ValueTracker(0)
        ctr_lab = mono("token dibaca:", color=ABU, size="caption")
        ctr_lab.next_to(tumpuk, DOWN, buff=SP["m"]).align_to(lab, LEFT)
        ctr = always_redraw(lambda: mono(fmt(tok.get_value()), color=JINGGA, size="h2", weight=BOLD)
                            .next_to(ctr_lab, RIGHT, buff=SP["s"]))
        self.add(ctr)
        self.play(FadeIn(ctr_lab), run_time=0.2)
        sor = SurroundingRectangle(tumpuk[0], color=KUNYIT, buff=0.06 * S, corner_radius=0.1 * S,
                                   stroke_width=3 * S)
        garis = Line(UP * 0.3 * S, DOWN * 0.3 * S, color=KUNYIT, stroke_width=4 * S)
        garis.move_to(tumpuk[0].get_left())
        sinar = always_redraw(lambda: Line(garis.get_center(), ai.get_left(), color=KUNYIT,
                                           stroke_width=1.5 * S, stroke_opacity=0.35))
        self.play(Create(sor), FadeIn(garis), run_time=0.25)
        self.add(sinar)
        total = 2400
        for k, m in enumerate(tumpuk):
            if k > 0:
                self.play(sor.animate.become(SurroundingRectangle(m, color=KUNYIT, buff=0.06 * S,
                                                                  corner_radius=0.1 * S, stroke_width=3 * S)),
                          garis.animate.move_to(m.get_left()), tumpuk[k - 1].animate.set_opacity(0.35),
                          run_time=0.18)
            self.play(garis.animate.move_to(m.get_right()), tok.animate.set_value(total * (k + 1) / len(tumpuk)),
                      run_time=0.42, rate_func=linear)
        self.play(FadeOut(sor), FadeOut(garis), tumpuk[-1].animate.set_opacity(0.35), run_time=0.2)
        self.remove(sinar)
        self.mark("04_scan")

        jaw = balon("Sama-sama!", TOSKA, size="body")
        jaw.next_to(ai, DOWN, buff=SP["m"]).align_to([AMAN["kanan"], 0, 0], RIGHT)
        cat = VGroup(judul("…cuma buat jawab", color=SAGA, size="h2"),
                     judul("“sama-sama”.", color=SAGA, size="h1")).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
        cat.next_to(ctr_lab, DOWN, buff=SP["m"]).align_to(lab, LEFT)
        contoh = caption("angka contoh").next_to(ctr, RIGHT, buff=SP["m"])
        self.play(FadeIn(jaw, shift=UP * GESER), run_time=CEPAT)
        self.play(FadeIn(cat, shift=UP * GESER), FadeIn(contoh), run_time=CEPAT + 0.1)
        self.mark("04_balasan")
        self.wait(JEDA + 1.2)
        self.remove(ctr)
        self.kosongkan()

    # 5 ----------------------------------------------------------------------
    def sejuta(self):
        self.header("Per orang? Receh.")
        satu = balon(isi_makasih("caption"), LANGIT)
        satu.move_to(pos(0, 2.0))
        self.play(FadeIn(satu, scale=0.9), run_time=CEPAT)
        self.wait(0.6)
        # zoom out: grid balon kecil
        kecil = VGroup(*[RoundedRectangle(width=0.5 * S, height=0.28 * S, corner_radius=0.08 * S,
                                          fill_color=redup(LANGIT, 0.4), fill_opacity=1,
                                          stroke_color=LANGIT, stroke_width=1 * S) for _ in range(12 * 9)])
        kecil.arrange_in_grid(rows=9, cols=12, buff=0.08 * S)
        kecil.move_to(pos(0, 2.0))
        self.play(ReplacementTransform(satu, kecil[50]), run_time=CEPAT)
        self.play(LaggedStart(*[FadeIn(k, scale=0.5) for i, k in enumerate(kecil) if i != 50], lag_ratio=0.01),
                  run_time=KETUK)
        x = VGroup(teks("× sejuta orang", color=TINTA, size="h2"),
                   VGroup(mono("8.000.000", color=JINGGA, size="display", weight=BOLD),
                          teks("token", color=TINTA, size="h2")).arrange(RIGHT, buff=SP["s"], aligned_edge=DOWN),
                   teks("cuma buat sopan", color=ABU, size="body")).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        kiri(x, -1.5)
        ai = ikon_ai(1.1).move_to(pos(2.5, -3.3))
        drops = VGroup(tetes(u=1.4).move_to(ai.get_corner(UR) + RIGHT * 0.1 * S),
                       tetes(u=1.1).move_to(ai.get_corner(UL) + LEFT * 0.15 * S + DOWN * 0.1 * S))
        cat = caption("hitungan contoh")
        kiri(cat, -3.7)
        self.play(FadeIn(x[0]), FadeIn(x[1], shift=UP * GESER), run_time=CEPAT + 0.2)
        self.play(FadeIn(x[2]), FadeIn(ai), FadeIn(cat), run_time=CEPAT)
        self.play(FadeIn(drops, shift=DOWN * 0.15), Wiggle(ai, scale_value=1.05, rotation_angle=0.03), run_time=KETUK)
        self.mark("05_sejuta")
        self.wait(JEDA - 0.4 + 1.5)
        self.kosongkan()

    # 6 ----------------------------------------------------------------------
    def tips(self):
        self.header("Tips: gabungin aja", color=DAUN)
        a = balon(isi_makasih("caption"), LANGIT)
        a2 = balon("Sama-sama! Senang bisa…", TOSKA)
        b = balon("Sekarang bikinin caption IG", LANGIT)
        g = VGroup(a, a2, b).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        kiri(g, 3.4)
        lab1 = caption("sebelum: 2 kali kirim, ada balasan ekstra")
        lab1.next_to(g, UP, buff=SP["s"]).align_to(g, LEFT)
        self.play(FadeIn(lab1), LaggedStart(*[FadeIn(x, shift=UP * GESER) for x in g], lag_ratio=0.3), run_time=KETUK)
        cr = Line(a2.get_left(), a2.get_right(), color=SAGA, stroke_width=4 * S)
        self.play(Create(cr), run_time=CEPAT)
        gab = balon("Makasih! Sekarang bikinin caption IG", LANGIT)
        kiri(gab, -0.6)
        lab2 = caption("sesudah: 1 kali kirim", color=DAUN).next_to(gab, UP, buff=SP["s"]).align_to(gab, LEFT)
        self.play(FadeIn(lab2), TransformFromCopy(VGroup(a, b), gab), run_time=LAMBAT)
        hasil = teks("tetap sopan, nggak ada balasan ekstra", color=DAUN, size="body", weight=MEDIUM)
        kiri(hasil, -2.0)
        self.play(FadeIn(hasil), run_time=CEPAT)
        self.mark("06_tips")
        self.wait(JEDA + 2.0)
        self.kosongkan()

    # 7 ----------------------------------------------------------------------
    def bonus(self):
        self.header("Btw…")
        r1 = VGroup(blok("please", LANGIT, "h2"), mono("= 1 token", color=JINGGA, size="h2", weight=BOLD)
                    ).arrange(RIGHT, buff=SP["m"])
        r2 = VGroup(VGroup(blok("tol", UNGU, "h2"), blok("ong", "#E58BB4", "h2")).arrange(RIGHT, buff=0.12 * S),
                    mono("= 2 token", color=JINGGA, size="h2", weight=BOLD)).arrange(RIGHT, buff=SP["m"])
        kiri(r1, 3.4)
        kiri(r2, 1.8)
        self.play(FadeIn(r1, shift=UP * GESER), run_time=CEPAT + 0.1)
        self.play(FadeIn(r2, shift=UP * GESER), run_time=CEPAT + 0.1)
        t = VGroup(judul("Sopan pakai bahasa Inggris", size="h2"),
                   judul("lebih murah.", color=KUNYIT, size="h1")).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
        kiri(t, -0.3)
        self.play(FadeIn(t, shift=UP * GESER), run_time=CEPAT + 0.2)
        self.mark("07_bonus")
        self.wait(JEDA - 0.2 + 1.0)
        self.kosongkan()

    # 8 ----------------------------------------------------------------------
    def penutup(self):
        l1 = judul("Tapi tetap sopan ya.", size="h1")
        l2 = judul("“you never know.”", color=ABU, size="h2")
        g = VGroup(l1, l2).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        kiri(g, 4.6)
        ai = ikon_ai(2.4).move_to(pos(0, 0.8))
        self.play(FadeIn(g, shift=UP * GESER), FadeIn(ai, scale=0.8), run_time=KETUK)
        self.wait(0.8)
        # AI jahat: merah, mata menyala, glitch
        jahat = ikon_ai(2.4, color=SAGA).move_to(ai)
        jahat[3].become(Text("", font=FONT_MONO))  # hilangkan label "AI"
        mata = VGroup()
        for sgn in (-1, 1):
            c = ai.get_center() + np.array([sgn * 0.45 * S, 0.05 * S, 0])
            glow = Circle(radius=0.34 * S, fill_color=SAGA, fill_opacity=0.25, stroke_width=0).move_to(c)
            inti = Circle(radius=0.17 * S, fill_color=SAGA, fill_opacity=1, stroke_width=0).move_to(c)
            mata.add(VGroup(glow, inti))
        gl1 = jahat.copy().set_color(LANGIT).set_opacity(0.5).shift(LEFT * 0.12 * S)
        gl2 = jahat.copy().set_opacity(0.5).shift(RIGHT * 0.12 * S + UP * 0.05 * S)
        redup_layar = Rectangle(width=config.frame_width, height=config.frame_height,
                                fill_color=HITAM, fill_opacity=0.6, stroke_width=0)
        self.play(FadeIn(redup_layar), FadeIn(gl1), FadeIn(gl2), run_time=0.15)
        self.play(FadeOut(gl1), FadeOut(gl2), ReplacementTransform(ai, jahat), FadeIn(mata, scale=0.3), run_time=0.35)
        self.add(jahat, mata)
        self.play(*[m[0].animate.scale(1.5).set_opacity(0.4) for m in mata], run_time=0.4, rate_func=there_and_back)
        daftar = VGroup(mono("DAFTAR MANUSIA SOPAN:", color=SAGA, size="body", weight=BOLD),
                        mono("✓ kamu", color=SAGA, size="h1", weight=BOLD)).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        kiri(daftar, -2.4)
        self.play(AddTextLetterByLetter(daftar[0], time_per_char=0.04), run_time=0.9, rate_func=linear)
        self.play(FadeIn(daftar[1], scale=1.3), run_time=CEPAT)
        self.mark("08_jahat")
        self.wait(1.4)
        # kembali normal
        normal = ikon_ai(2.4).move_to(jahat)
        jj = teks("…jaga-jaga.", color=ABU, size="h2")
        kiri(jj, -4.0)
        self.play(FadeOut(mata), FadeOut(redup_layar), ReplacementTransform(jahat, normal), run_time=0.3)
        self.play(FadeIn(jj, shift=UP * GESER), run_time=CEPAT)
        self.mark("09_jagajaga")
        self.wait(JEDA + 1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=KETUK)
