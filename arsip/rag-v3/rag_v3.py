"""
Video RAG gaya KAPUR, versi A "Kalau kamu yang bikin... #1" (revisi v3).

Perubahan dari v2:
  - Kasus diganti: bukan SOP kantor/jatah cuti, tapi riwayat grup chat alumni
    (20.000 pesan) dan pertanyaan "Reuni jadinya kapan?".
  - Ide 1: animasi AI "membaca" semua pesan satu per satu (garis pemindai +
    sorotan), penghitung token naik bersamaan.
  - Ide 2: gunting memotong riwayat chat jadi guntingan kertas berisi pesan nyata.
  - Ide 3: contoh kata (kucing / anak kucing vs mobil / motor) lalu potongan chat
    sebagai titik berlabel di peta makna; pertanyaan jatuh dekat potongan reuni.

Memakai design system di ../design-system (theme.py + fonts).

Frame kunci saja (cepat), hasil di preview/<orientasi>/:
    STILLS=1 ORIENT=vertical manim -s -ql rag_v3.py RAGKalauKamuBikinV3
Video penuh 1080x1920:
    ORIENT=vertical manim -qh rag_v3.py RAGKalauKamuBikinV3
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

# Jeda lebih panjang dari default KAPUR supaya muat narasi.
JEDA = 1.8
JEDA_PANJANG = 2.9

TINTA_KERTAS = "#2B2721"   # teks gelap di atas kertas
LIPAT_KERTAS = "#B9B2A2"

# ---------------------------------------------------------------------------
# Kasus: grup chat alumni. Satu potongan (chunk) = satu pesan pendek.
# (nama, isi pesan, label singkat di peta, posisi di peta, arah label)
# ---------------------------------------------------------------------------
POTONGAN = [
    ("Rina", "Fix ya, reuni Sabtu 14 Des!", "reuni Sabtu 14 Des", (1.2, 2.25), UP),
    ("Budi", "Tempatnya di Kafe Senja aja", "Kafe Senja", (2.85, 1.15), DOWN),
    ("Rina", "Kumpul jam 7 malam ya", "jam 7 malam", (0.75, 0.85), DOWN),
    ("Dodi", "Ada yang jual motor bekas?", "jual motor", (-2.7, 2.2), DOWN),
    ("Tari", "Minta resep rendang dong", "resep rendang", (-2.9, 0.1), DOWN),
    ("Andi", "Info loker admin, DM ya", "loker admin", (-0.7, -1.2), DOWN),
    ("Sari", "Makasih ucapan ultahnya!", "ucapan ultah", (2.5, -1.5), DOWN),
    ("Yoga", "Link zoom webinar besok", "link zoom", (-2.5, -2.2), UP),
    ("Tari", "Foto liburan di Bali nih", "foto liburan", (0.7, -2.55), UP),
]
NEAR = [0, 1, 2]
TITIK_TANYA = (1.75, 1.55)
PERTANYAAN = "Reuni jadinya kapan?"
TOTAL_PESAN = "20.000 pesan"
TOTAL_TOKEN = 250000


# ---------------------------------------------------------------------------
# Komponen khusus video ini
# ---------------------------------------------------------------------------
def ikon_chatlog(lebar=0.9):
    """Kartu kecil berisi 3 balon chat: mewakili segepok pesan."""
    w = lebar * S
    h = w * 0.7
    kotak = RoundedRectangle(width=w, height=h, corner_radius=0.07 * S,
                             fill_color=PERMUKAAN, fill_opacity=1,
                             stroke_color=ABU_GELAP, stroke_width=1.5 * S)
    balon = VGroup()
    for k, (lx, ww, warna) in enumerate([(-1, 0.55, ABU), (1, 0.45, LANGIT), (-1, 0.4, ABU)]):
        b = RoundedRectangle(width=w * ww, height=h * 0.17, corner_radius=h * 0.08,
                             fill_color=warna, fill_opacity=0.75, stroke_width=0)
        b.move_to(kotak.get_center() + UP * h * (0.27 - 0.27 * k))
        b.align_to(kotak, LEFT if lx < 0 else RIGHT).shift((RIGHT if lx < 0 else LEFT) * w * 0.09)
        balon.add(b)
    return VGroup(kotak, balon)


def guntingan(i, lebar=6.4):
    """Satu potongan kertas berisi satu pesan chat. Strip warna = identitas potongan."""
    nama, isi, *_ = POTONGAN[i]
    h = 0.62 * S
    kertas = Rectangle(width=lebar * S, height=h, fill_color=KERTAS, fill_opacity=1,
                       stroke_width=0)
    strip = Rectangle(width=0.16 * S, height=h, fill_color=KATEGORI[i], fill_opacity=1,
                      stroke_width=0).align_to(kertas, LEFT)
    tn = Text(nama + ":", font=FONT_TEKS, weight=BOLD, color=TINTA_KERTAS,
              font_size=TIPE["caption"] * S * 0.92)
    ti = Text(isi, font=FONT_TEKS, color=TINTA_KERTAS, font_size=TIPE["caption"] * S * 0.92)
    baris = VGroup(tn, ti).arrange(RIGHT, buff=0.12 * S)
    baris.move_to(kertas).align_to(kertas, LEFT).shift(RIGHT * 0.38 * S)
    # tn & ti beda tinggi huruf -> samakan baseline kasar
    ti.align_to(tn, DOWN)
    return VGroup(kertas, strip, baris)


def gunting(buka=0.35, ukuran=1.0, color=TINTA):
    """Ikon gunting menghadap kanan. buka = sudut bilah (radian)."""
    u = ukuran * S
    bagian = VGroup()
    for sgn in (1, -1):
        bilah = Polygon([0, 0.05 * u, 0], [0.95 * u, 0.0, 0], [0, -0.07 * u, 0],
                        fill_color=color, fill_opacity=1, stroke_width=0)
        gagang = Circle(radius=0.17 * u, stroke_color=color, stroke_width=4 * S)
        gagang.move_to([-0.42 * u, -sgn * 0.2 * u, 0])
        leher = Line([0, 0, 0], gagang.get_center() + (gagang.get_center() / np.linalg.norm(
            gagang.get_center())) * -0.17 * u, color=color, stroke_width=4 * S)
        half = VGroup(bilah, leher, gagang).rotate(sgn * buka / 2, about_point=ORIGIN)
        bagian.add(half)
    poros = Dot(ORIGIN, radius=0.05 * u, color=HITAM)
    return VGroup(bagian, poros)


# ---------------------------------------------------------------------------
# Scene
# ---------------------------------------------------------------------------
class RAGKalauKamuBikinV3(KapurScene):
    PREFIX = "A_"

    def mark(self, nama):
        if not os.environ.get("STILLS"):
            return
        out = _DIR / "preview" / ORIENT
        out.mkdir(parents=True, exist_ok=True)
        self.renderer.update_frame(self, ignore_skipping=True)
        self.renderer.camera.get_image().save(out / f"{self.PREFIX}{nama}.png")

    def construct(self):
        np.random.seed(7)
        self.pembuka()
        self.ide_tempel()
        self.ide_potong()
        self.ide_angka()
        self.ide_kirim()
        self.selamat()

    # --- util ---------------------------------------------------------------
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

    def tapi(self, s="Tapi…", y=-4.0):
        t = judul(s, color=SAGA, size="display").move_to(pos(0, y))
        self.play(FadeIn(t, shift=UP * GESER), run_time=CEPAT)
        return t

    def stempel(self, s):
        t = mono(s, color=SAGA, size="h2", weight=BOLD)
        r = RoundedRectangle(width=t.width + 0.4 * S, height=t.height + 0.3 * S,
                             corner_radius=0.08 * S, stroke_color=SAGA, stroke_width=4 * S,
                             fill_color=HITAM, fill_opacity=0.6)
        t.move_to(r)
        return VGroup(r, t).rotate(0.18)

    def tanya_orang(self):
        person = ikon_orang(LANGIT, 1.1)
        q = gelembung(PERTANYAAN, LANGIT).next_to(person, RIGHT, buff=SP["s"])
        return VGroup(person, q)

    # --- 0-8 dtk ------------------------------------------------------------
    def pembuka(self):
        self.bab("Kalau kamu yang bikin… #1")
        l1 = judul("Kamu mau AI yang bisa", size="h1")
        l2 = judul("jawab soal isi", size="h1")
        l3 = judul("grup chat-mu.", color=KUNYIT, size="display")
        g = VGroup(l1, l2, l3).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        g.move_to(pos(0, 2.2)).align_to([AMAN["kiri"], 0, 0], LEFT)
        tumpuk = VGroup(*[ikon_chatlog(1.25) for _ in range(3)])
        for k, m in enumerate(tumpuk):
            m.shift(UP * 0.14 * S * k + RIGHT * 0.14 * S * k)
        tumpuk.move_to(pos(-1.7, -1.4))
        jml = mono(TOTAL_PESAN, color=JINGGA).next_to(tumpuk, DOWN, buff=SP["s"])
        ai = ikon_ai(1.5).move_to(pos(1.7, -1.4))
        tanda = mono("?", color=ABU, size="h1").move_to(pos(0, -1.4))
        self.play(FadeIn(l1, shift=UP * GESER), FadeIn(l2, shift=UP * GESER), run_time=CEPAT + 0.1)
        self.play(Write(l3), LaggedStart(*[FadeIn(m, shift=UP * GESER) for m in tumpuk],
                                         lag_ratio=0.2),
                  FadeIn(jml), FadeIn(ai, scale=0.8), FadeIn(tanda), run_time=KETUK)
        ul = coret_kapur(l3)
        self.play(Create(ul), run_time=CEPAT)
        self.mark("01_pembuka")
        self.wait(0.8)
        self.play(FadeOut(VGroup(g, ul, tumpuk, jml, ai, tanda), shift=UP * GESER), run_time=CEPAT)

        self.header("Masalahnya…")
        tanya = self.tanya_orang().move_to(pos(-0.3, 4.0))
        ai = ikon_ai(1.5).move_to(pos(-2.3, 1.4))
        jawab = gelembung("Minggu, 21 Des!", TOSKA, size="body").next_to(ai, RIGHT, buff=SP["m"])
        self.play(FadeIn(tanya[0]), FadeIn(tanya[1], shift=LEFT * GESER), run_time=CEPAT + 0.1)
        self.play(FadeIn(ai, scale=0.8), run_time=CEPAT)
        self.play(FadeIn(jawab, shift=UP * GESER), run_time=CEPAT)
        st = self.stempel("NGARANG").next_to(jawab, DOWN, buff=SP["s"]).shift(RIGHT * 0.3 * S)
        self.play(FadeIn(st, scale=1.6), ai[1].animate.set_stroke(SAGA),
                  ai[3].animate.set_color(SAGA), run_time=CEPAT)
        cap = caption("AI nggak pernah baca chat grupmu. Jadi dia nebak.").move_to(pos(0, -1.6))
        self.play(FadeIn(cap), run_time=CEPAT)
        self.mark("02_ngarang")
        self.wait(JEDA)
        self.kosongkan()

    # --- 8-24 dtk -----------------------------------------------------------
    def ide_tempel(self):
        self.bab("Ide 1")
        self.header("Gampang: tempel seluruh chat")
        file_lbl = mono(f"chat_grup.txt · {TOTAL_PESAN}", color=JINGGA).move_to(pos(0, 4.5))
        logs = VGroup(*[ikon_chatlog(0.95) for _ in range(20)])
        logs.arrange_in_grid(rows=4, cols=5, buff=0.16 * S).move_to(pos(0, 2.35))
        self.play(FadeIn(file_lbl, shift=DOWN * GESER),
                  LaggedStart(*[FadeIn(d, shift=DOWN * 0.4) for d in logs], lag_ratio=0.03),
                  run_time=KETUK)
        chat = RoundedRectangle(width=6.9 * S, height=logs.height + 0.7 * S,
                                corner_radius=0.22 * S, fill_color=PERMUKAAN, fill_opacity=1,
                                stroke_color=LANGIT, stroke_width=2.5 * S).move_to(logs)
        kirim = caption("ditempel ke chat AI", color=LANGIT).next_to(chat, DOWN, buff=SP["s"])
        self.play(FadeIn(chat), FadeIn(kirim), FadeOut(file_lbl), run_time=CEPAT)
        self.bring_to_front(logs)
        self.mark("03_tempel")
        self.wait(0.4)

        # --- AI membaca SEMUA pesan, satu per satu ---
        self.play(FadeOut(kirim), run_time=0.3)
        baca = caption("AI membaca semuanya, satu per satu…", color=TINTA).next_to(chat, DOWN, buff=SP["s"])
        self.play(FadeIn(baca), run_time=0.3)
        n = len(logs)
        t = ValueTracker(0)
        satuan = teks("token per pertanyaan", color=ABU, size="caption").move_to(pos(0, -1.7))

        def idx():
            return min(int(t.get_value()), n - 1)

        def kepala():
            d = logs[idx()]
            return SurroundingRectangle(d, color=KUNYIT, buff=0.05 * S, corner_radius=0.08 * S,
                                        stroke_width=3.5 * S)

        def pindai():
            d = logs[idx()]
            frac = t.get_value() - int(t.get_value()) if t.get_value() < n else 1
            y = d.get_top()[1] - frac * d.height
            ln = Line([chat.get_left()[0] + 0.15 * S, y, 0], [chat.get_right()[0] - 0.15 * S, y, 0],
                      color=KUNYIT, stroke_width=2.5 * S, stroke_opacity=0.85)
            glow = Rectangle(width=chat.width - 0.3 * S, height=0.32 * S, stroke_width=0,
                             fill_color=KUNYIT, fill_opacity=0.10).next_to(ln, UP, buff=0)
            return VGroup(glow, ln)

        def angka():
            v = int(TOTAL_TOKEN * min(t.get_value() / n, 1))
            s = f"{v:,}".replace(",", ".")
            return mono(s, color=JINGGA if v < TOTAL_TOKEN * 0.6 else SAGA, size="display",
                        weight=BOLD).move_to(pos(0, -0.8))

        for i, d in enumerate(logs):
            d.add_updater(lambda m, i=i: m.set_opacity(0.32 if t.get_value() >= i + 1 else 1))
        k = always_redraw(kepala)
        p = always_redraw(pindai)
        num = always_redraw(angka)
        self.add(p, k, num)
        self.play(FadeIn(satuan), run_time=0.2)
        self.play(t.animate.set_value(n * 0.5), run_time=2.4, rate_func=linear)
        self.mark("04_scan")
        self.play(t.animate.set_value(n), run_time=2.2, rate_func=linear)
        for d in logs:
            d.clear_updaters()
        num.clear_updaters()
        self.play(FadeOut(k), FadeOut(p), FadeOut(baca), run_time=0.3)

        tp = self.tapi("Tapi… kepanjangan.", y=-2.7)
        self.play(chat.animate.set_stroke(SAGA), run_time=CEPAT)
        akibat = VGroup(pil("boros", SAGA), pil("lambat", SAGA), pil("gagal fokus", SAGA)
                        ).arrange(RIGHT, buff=0.3 * S).move_to(pos(0, -3.95))
        self.play(LaggedStart(*[FadeIn(x, shift=UP * GESER) for x in akibat], lag_ratio=0.25),
                  run_time=KETUK)
        self.mark("05_kepanjangan")
        self.wait(JEDA)
        self.kosongkan()

    # --- 24-40 dtk ----------------------------------------------------------
    def ide_potong(self):
        self.bab("Ide 2")
        self.header("Jadi… potong kecil-kecil")
        strips = VGroup(*[guntingan(i) for i in range(len(POTONGAN))])
        strips.arrange(DOWN, buff=0).move_to(pos(0, 1.4))
        bingkai = Rectangle(width=strips.width, height=strips.height, stroke_width=0,
                            fill_color=KERTAS, fill_opacity=1).move_to(strips)
        lipat = Polygon(bingkai.get_corner(UR) + LEFT * 0.45 * S, bingkai.get_corner(UR),
                        bingkai.get_corner(UR) + DOWN * 0.45 * S, fill_color=LIPAT_KERTAS,
                        fill_opacity=1, stroke_width=0)
        label = mono("chat_grup.txt", color=JINGGA, size="mikro").next_to(bingkai, UP, buff=SP["xs"]).align_to(bingkai, LEFT)
        self.play(FadeIn(bingkai), FadeIn(lipat), FadeIn(label),
                  LaggedStart(*[FadeIn(s[2]) for s in strips], lag_ratio=0.05), run_time=KETUK)
        self.add(strips)
        self.remove(bingkai)
        self.bring_to_front(lipat)

        # garis potong putus-putus di antara pesan
        x0, x1 = strips.get_left()[0] - 0.2 * S, strips.get_right()[0] + 0.2 * S
        ys = [(strips[i].get_bottom()[1]) for i in range(len(strips) - 1)]
        potong = VGroup(*[DashedLine([x0, y, 0], [x1, y, 0], color=ABU, stroke_width=2 * S,
                                     dash_length=0.12 * S) for y in ys])
        self.play(Create(potong), run_time=CEPAT)

        buka = ValueTracker(0.5)
        posisi = ValueTracker(0)  # 0..len(ys) -> baris & x

        def gg():
            v = posisi.get_value()
            r = min(int(v), len(ys) - 1)
            frac = v - int(v) if v < len(ys) else 1
            g = gunting(buka.get_value(), 1.15, color=KUNYIT)
            g.shift(np.array([x0 + frac * (x1 - x0), ys[r], 0]) - g[1].get_center())
            return g

        sc = always_redraw(gg)
        self.add(sc)
        # gunting menyusuri tiap garis sambil "kres-kres"
        tot = 0.0

        def snip(m, dt):
            nonlocal tot
            tot += dt
            m.set_value(0.08 + 0.42 * abs(np.sin(tot * 14)))

        buka.add_updater(snip)
        self.add(buka)
        self.play(posisi.animate.set_value(len(ys) / 2), run_time=1.5, rate_func=linear)
        self.mark("06_gunting")
        self.play(posisi.animate.set_value(len(ys)), run_time=1.5, rate_func=linear)
        buka.clear_updaters()
        self.remove(sc)

        # potongan terpisah: guntingan kertas
        tujuan = strips.copy().arrange(DOWN, buff=0.2 * S).move_to(pos(0, 1.3))
        self.sudut = [np.random.uniform(-0.04, 0.04) for _ in strips]
        self.play(FadeOut(potong), FadeOut(lipat), FadeOut(label),
                  *[strips[i].animate.move_to(tujuan[i]).rotate(self.sudut[i])
                    for i in range(len(strips))], run_time=KETUK)
        tag = pil("chunk", DAUN).next_to(strips, DOWN, buff=SP["m"])
        self.play(FadeIn(tag, shift=UP * GESER), run_time=CEPAT)
        self.mark("07_potong")
        self.wait(JEDA)

        # 9 potongan di layar, aslinya ribuan
        t = self.tapi("Tapi… kirim yang mana?", y=-3.6)
        # sebar tanpa saling tutup total: susun 9 slot acak dalam 2 kolom
        slots = [pos(cx, cy) for cy in (4.5, 3.4, 2.3, 1.2, 0.1, -1.0, -2.1) for cx in (-1.7, 1.5)]
        pick = np.random.permutation(len(slots))[:len(strips)]
        rot = [np.random.uniform(-0.22, 0.22) for _ in strips]
        self.sudut = [a + b for a, b in zip(self.sudut, rot)]
        self.play(FadeOut(tag),
                  *[s.animate.scale(0.52).move_to(slots[j] + np.array([np.random.uniform(-0.25, 0.25), np.random.uniform(-0.15, 0.15), 0]))
                    .rotate(r) for s, j, r in zip(strips, pick, rot)],
                  run_time=KETUK)
        qs = VGroup(*[mono("?", color=SAGA, size="h2", weight=BOLD).next_to(s, UP, buff=0.02)
                      for s in strips[1::3]])
        self.play(LaggedStart(*[FadeIn(q, scale=1.5) for q in qs], lag_ratio=0.15),
                  run_time=CEPAT + 0.2)
        sub = caption("aslinya ada ribuan potongan", color=ABU).next_to(t, DOWN, buff=SP["s"])
        self.play(FadeIn(sub), run_time=CEPAT)
        self.mark("08_yang_mana")
        self.wait(JEDA)
        self.play(FadeOut(t), FadeOut(qs), FadeOut(sub), run_time=CEPAT)
        self.strips = strips

    # --- 40-60 dtk ----------------------------------------------------------
    def ide_angka(self):
        self.bab("Ide 3")
        self.header("Jadi… ubah jadi angka")
        strips = self.strips
        contoh = strips[0]
        lain = VGroup(*[s for i, s in enumerate(strips) if i != 0])
        self.play(FadeOut(lain, scale=0.8),
                  contoh.animate.rotate(-self.sudut[0]).scale(5.2 / 6.4 / 0.52)
                  .move_to(pos(-0.3, 4.6)), run_time=KETUK)
        ar = Arrow(contoh.get_bottom(), contoh.get_bottom() + DOWN * 0.75 * S, buff=0.05 * S,
                   color=ABU, stroke_width=4 * S, tip_length=0.2 * S)
        vec = mono("[0.12, -0.83, 0.47, …]", color=JINGGA).next_to(ar, DOWN, buff=0.08 * S)
        self.play(GrowArrow(ar), FadeIn(vec, shift=DOWN * GESER), run_time=CEPAT + 0.2)
        self.wait(0.6)

        plane = grid_titik(7.4, 5.2).move_to(pos(0.1, -0.1))
        self.play(Create(plane), run_time=KETUK)

        # --- contoh kata: makna mirip = posisi berdekatan ---
        kata = [("kucing", (-2.3, 2.05), RIGHT), ("anak kucing", (-1.8, 1.4), RIGHT),
                ("kucing oren", (-2.15, 0.75), RIGHT),
                ("mobil", (1.9, -1.4), RIGHT), ("motor", (2.5, -2.1), RIGHT)]
        wk = [UNGU, UNGU, UNGU, "#7FA8F5", "#7FA8F5"]
        kd = VGroup()
        kl = VGroup()
        for (s, (x, y), arah), w in zip(kata, wk):
            d = Dot(plane.c2p(x, y), radius=0.11 * S, color=w)
            lb = teks(s, color=TINTA, size="caption").next_to(d, arah, buff=0.1 * S)
            kd.add(d)
            kl.add(lb)
        self.play(LaggedStart(*[AnimationGroup(GrowFromCenter(kd[i]), FadeIn(kl[i]))
                                for i in range(3)], lag_ratio=0.3), run_time=KETUK)
        dekat = Ellipse(width=VGroup(kd[:3], kl[:3]).width + 0.9 * S,
                        height=VGroup(kd[:3], kl[:3]).height + 0.75 * S, color=DAUN, stroke_width=2.5 * S
                        ).move_to(VGroup(kd[:3], kl[:3]))
        dk = caption("mirip → dekat", color=DAUN).next_to(dekat, LEFT, buff=0.1 * S).align_to(dekat, DOWN).shift(DOWN * 0.45 * S + RIGHT * 1.2 * S)
        self.play(Create(dekat), FadeIn(dk), run_time=CEPAT + 0.1)
        self.play(LaggedStart(*[AnimationGroup(GrowFromCenter(kd[i]), FadeIn(kl[i]))
                                for i in (3, 4)], lag_ratio=0.3), run_time=CEPAT + 0.2)
        awal = dekat.get_center() + np.array([dekat.width / 2 * 0.72, -dekat.height / 2 * 0.7, 0])
        jauh = DashedLine(awal, kd[3].get_center() + LEFT * 0.12 * S, color=SAGA, stroke_width=2.5 * S,
                          dash_length=0.15 * S)
        jk = caption("beda → jauh", color=SAGA).move_to(awal * 0.5 + kd[3].get_center() * 0.5).shift(RIGHT * 1.0 * S + UP * 0.3 * S)
        self.play(Create(jauh), FadeIn(jk), run_time=CEPAT + 0.1)
        note = caption("makna mirip = posisi berdekatan", color=TINTA).next_to(plane, DOWN, buff=SP["m"])
        self.play(FadeIn(note), run_time=CEPAT)
        self.mark("09_kata_mirip")
        self.wait(JEDA)

        # --- potongan chat juga begitu ---
        self.play(FadeOut(VGroup(kd, kl, dekat, dk, jauh, jk)), run_time=CEPAT)
        dots = VGroup()
        labels = VGroup()
        for i, (_, _, lab, (x, y), arah) in enumerate(POTONGAN):
            d = Dot(plane.c2p(x, y), radius=0.12 * S, color=KATEGORI[i])
            lb = teks(lab, color=TINTA, size="mikro").next_to(d, arah, buff=0.08 * S)
            dots.add(d)
            labels.add(lb)
        self.play(ReplacementTransform(VGroup(contoh, ar, vec), dots[0]), FadeIn(labels[0]),
                  run_time=KETUK)
        self.play(LaggedStart(*[AnimationGroup(GrowFromCenter(dots[i]), FadeIn(labels[i]))
                                for i in range(1, len(dots))], lag_ratio=0.12), run_time=LAMBAT)
        tag = pil("embedding", DAUN).next_to(note, DOWN, buff=SP["m"])
        self.play(FadeIn(tag, shift=UP * GESER), run_time=CEPAT)
        self.mark("10_embedding")
        self.wait(JEDA)

        # --- pertanyaan juga jadi titik ---
        self.header("Pertanyaanmu juga jadi angka")
        self.play(FadeOut(note), FadeOut(tag), run_time=0.3)
        tanya = self.tanya_orang().move_to(pos(0, 4.45))
        self.play(FadeIn(tanya[0]), FadeIn(tanya[1], shift=LEFT * GESER), run_time=CEPAT + 0.1)
        qdot = Star(n=5, outer_radius=0.24 * S, inner_radius=0.1 * S, color=KUNYIT,
                    fill_opacity=1, stroke_width=0).move_to(plane.c2p(*TITIK_TANYA))
        self.play(ReplacementTransform(tanya[1][1].copy(), qdot), run_time=KETUK)
        far = [i for i in range(len(dots)) if i not in NEAR]
        links = VGroup(*[DashedLine(qdot.get_center(), dots[i].get_center(), color=KUNYIT,
                                    stroke_width=2.5 * S) for i in NEAR])
        self.play(Create(links), *[dots[i].animate.scale(1.5) for i in NEAR],
                  *[dots[i].animate.set_opacity(0.25) for i in far],
                  *[labels[i].animate.set_opacity(0.3) for i in far],
                  *[labels[i].animate.set_color(DAUN) for i in NEAR], run_time=KETUK)
        top = caption("ambil 3 terdekat", color=KUNYIT).next_to(plane, DOWN, buff=SP["m"])
        tag2 = pil("retrieval", DAUN).next_to(top, DOWN, buff=SP["m"])
        self.play(FadeIn(top), FadeIn(tag2, shift=UP * GESER), run_time=CEPAT)
        self.mark("11_retrieval")
        self.wait(JEDA)
        self.peta = VGroup(plane, links, qdot, top, tag2,
                           VGroup(*[dots[i] for i in far]), VGroup(*[labels[i] for i in far]))
        self.dekat = (VGroup(*[dots[i] for i in NEAR]), VGroup(*[labels[i] for i in NEAR]))
        self.tanya = tanya

    # --- 60-70 dtk ----------------------------------------------------------
    def ide_kirim(self):
        self.bab("Terakhir")
        self.header("Tempel ke pertanyaan, kirim")
        dots, labels = self.dekat
        sel = VGroup(*[guntingan(i, lebar=6.2) for i in NEAR]).arrange(DOWN, buff=0.14 * S)
        q = gelembung(PERTANYAAN, LANGIT)
        isi = VGroup(q, sel).arrange(DOWN, buff=SP["m"], aligned_edge=LEFT)
        prompt = kartu(isi, pad=0.28).move_to(pos(0, 3.3))
        plab = mono("prompt", color=ABU, size="mikro").next_to(prompt, UP, buff=0.08 * S).align_to(prompt, LEFT)
        self.play(FadeOut(self.peta), FadeOut(self.tanya[0]),
                  ReplacementTransform(self.tanya[1], q),
                  *[ReplacementTransform(VGroup(dots[k], labels[k]), sel[k]) for k in range(3)],
                  run_time=KETUK)
        self.play(FadeIn(prompt[0]), FadeIn(plab), run_time=CEPAT)
        self.bring_to_front(q, sel)
        ai = ikon_ai(1.4).move_to(pos(0, -0.05))
        a1 = panah(prompt.get_bottom(), ai.get_top(), color=DAUN)
        self.play(GrowArrow(a1), FadeIn(ai, scale=0.8), run_time=CEPAT + 0.2)
        ans = kartu(VGroup(teks("Sabtu, 14 Des, jam 7 malam", color=TINTA, weight=MEDIUM),
                           teks("di Kafe Senja.", color=TINTA, weight=MEDIUM),
                           mono("sumber: chat Rina & Budi", color=ABU, size="mikro")
                           ).arrange(DOWN, buff=SP["xs"] * 1.5, aligned_edge=LEFT), aksen=DAUN)
        ans.move_to(pos(0, -2.55))
        a3 = panah(ai.get_bottom(), ans.get_top(), color=DAUN)
        self.play(GrowArrow(a3), FadeIn(ans, shift=DOWN * GESER), Indicate(ai, color=TOSKA),
                  run_time=KETUK)
        cap = caption("Sekarang dia jawab pakai contekan yang benar.").next_to(ans, DOWN, buff=SP["m"])
        self.play(FadeIn(cap), run_time=CEPAT)
        self.mark("12_jawaban")
        self.wait(JEDA_PANJANG)
        self.kosongkan()

    # --- 70-80 dtk ----------------------------------------------------------
    def selamat(self):
        self.bab("Kalau kamu yang bikin… #1")
        s1 = judul("Selamat.", size="display").move_to(pos(0, 4.4))
        s2 = judul("Kamu baru aja bikin", color=ABU, size="h2").next_to(s1, DOWN, buff=SP["m"])
        rag = judul("RAG", color=DAUN, size="raksasa").next_to(s2, DOWN, buff=SP["m"])
        sub = teks("Retrieval-Augmented Generation", color=ABU, size="caption").next_to(rag, DOWN, buff=SP["s"])
        p = VGroup(pil("chunk", DAUN), pil("embedding", DAUN), pil("retrieval", DAUN)
                   ).arrange(RIGHT, buff=0.45 * S).next_to(sub, DOWN, buff=SP["l"])
        ar = VGroup(*[panah(p[i].get_right(), p[i + 1].get_left(), color=ABU_GELAP, buff=0.05, tebal=3)
                      for i in range(2)])
        self.play(FadeIn(s1, shift=UP * GESER), run_time=CEPAT + 0.1)
        self.play(FadeIn(s2), run_time=CEPAT)
        self.play(Write(rag), run_time=KETUK)
        self.play(FadeIn(sub), LaggedStart(*[FadeIn(x, shift=UP * GESER) for x in p], lag_ratio=0.3),
                  Create(ar), run_time=KETUK)
        ul = coret_kapur(rag, color=DAUN)
        self.play(Create(ul), run_time=CEPAT)
        self.mark("13_selamat")
        self.wait(JEDA_PANJANG)

        t1 = teks("Tapi kenapa token bisa semahal itu?", color=TINTA, size="body").move_to(pos(0, -3.0))
        t2 = pil("#2  Tokenizer", JINGGA, size="body").next_to(t1, DOWN, buff=SP["m"])
        self.play(FadeIn(t1, shift=UP * GESER), run_time=CEPAT + 0.1)
        self.play(FadeIn(t2, scale=0.9), run_time=CEPAT)
        self.mark("14_teaser")
        self.wait(JEDA_PANJANG)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=KETUK)
