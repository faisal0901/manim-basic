"""
Video temperature, gaya A "Kalau kamu yang bikin…", design system KAPUR.

Kasus: minta AI bikin nama usaha kopi 3x, hasilnya beda terus.
Rantai: AI nulis per token -> tapi banyak kandidat -> probabilitas -> tapi selalu teratas
= sama semua -> diundi (toples) -> tapi kadang ngawur ("Kopi Obeng") -> kenop temperature
-> kapan rendah/tinggi -> "Selamat, kamu baru aja bikin temperature" -> catatan + tips.

Peluang awal 40/25/15/10/5/5 % dan nilai temperature 0,3 / 1,6 = ANGKA CONTOH.
Batang setelah kenop digeser dihitung pakai rumus asli (p^(1/T), dinormalkan).

Frame kunci:  STILLS=1 ORIENT=vertical manim -s -ql temperature_kalau_kamu_bikin.py TemperatureKalauKamuBikin
Video penuh:  ORIENT=vertical manim -qh temperature_kalau_kamu_bikin.py TemperatureKalauKamuBikin
"""
import os
import sys
from pathlib import Path

import numpy as np

_DIR = Path(__file__).resolve().parent
_DS = next(p / "design-system" for p in _DIR.parents if (p / "design-system").is_dir())
sys.path.insert(0, str(_DS))
from theme import *  # noqa: E402,F403

JEDA = 1.8
JEDA_PANJANG = 2.9

KATA = ["Senja", "Pagi", "Rindu", "Hangat", "Obeng", "lainnya"]
P_DASAR = [0.40, 0.25, 0.15, 0.10, 0.05, 0.05]


def peluang(T):
    w = np.array(P_DASAR) ** (1.0 / T)
    return list(w / w.sum())


def jumlah_kertas(ps, total=20):
    """Bagi 20 kertas sesuai peluang (largest remainder)."""
    raw = np.array(ps) * total
    n = np.floor(raw).astype(int)
    sisa = total - n.sum()
    for i in np.argsort(-(raw - n))[:sisa]:
        n[i] += 1
    return list(n)


def persen(p):
    v = p * 100
    return "≈0%" if v < 0.5 else f"{v:.0f}%"


# ---------------------------------------------------------------------------
# Komponen
# ---------------------------------------------------------------------------
def kiri(m, y):
    m.move_to(pos(0, y)).align_to([AMAN["kiri"], 0, 0], LEFT)
    return m


TRACK_X0 = -1.55  # awal track batang (koordinat layar)
TRACK_W = 3.7
TINGGI_BARIS = 0.68


def baris(kata, p, y, color=TOSKA):
    lab = teks(kata, color=SAGA if kata == "Obeng" else TINTA, size="body")
    lab.move_to([0, y, 0]).align_to([AMAN["kiri"], 0, 0], LEFT)
    track = RoundedRectangle(width=TRACK_W * S, height=0.36 * S, corner_radius=0.18 * S,
                             fill_color=GARIS, fill_opacity=1, stroke_width=0)
    track.move_to([0, y, 0]).align_to([TRACK_X0, 0, 0], LEFT)
    w = max(0.02, TRACK_W * S * p)
    isi = RoundedRectangle(width=w, height=0.36 * S, corner_radius=min(0.18 * S, w / 2),
                           fill_color=color, fill_opacity=1 if p >= 0.005 else 0, stroke_width=0)
    isi.align_to(track, LEFT).set_y(y)
    val = mono(persen(p), color=JINGGA, size="body", weight=BOLD)
    val.move_to([0, y, 0]).align_to([TRACK_X0 + TRACK_W * S + 0.25, 0, 0], LEFT)
    return VGroup(lab, track, isi, val)


def daftar_batang(ps, y0):
    return VGroup(*[baris(k, p, y0 - i * TINGGI_BARIS * S) for i, (k, p) in enumerate(zip(KATA, ps))])


def kertas(kata, sorot=False):
    r = RoundedRectangle(width=0.98 * S, height=0.42 * S, corner_radius=0.05 * S,
                         fill_color=KERTAS, fill_opacity=1,
                         stroke_color=KUNYIT if sorot else "#B9B2A2", stroke_width=(5 if sorot else 1) * S)
    t = Text(kata, font=FONT_TEKS, weight=MEDIUM, font_size=19 * S,
             color=SAGA if kata == "Obeng" else "#3A352C")
    if t.width > r.width - 0.12 * S:
        t.scale_to_fit_width(r.width - 0.12 * S)
    t.move_to(r)
    return VGroup(r, t)


class Toples(VGroup):
    """Toples undian berlabel, 20 slot kertas (4 kolom x 5 baris)."""

    KOL, BRS = 4, 5

    def __init__(self, center, **kw):
        super().__init__(**kw)
        w, h = 4.7 * S, 3.2 * S
        self.badan = RoundedRectangle(width=w, height=h, corner_radius=0.35 * S,
                                      fill_color=redup(TINTA, 0.06), fill_opacity=1,
                                      stroke_color=ABU, stroke_width=3 * S).move_to(center)
        self.mulut = RoundedRectangle(width=w * 0.86, height=0.26 * S, corner_radius=0.08 * S,
                                      fill_color=HITAM, fill_opacity=1, stroke_color=ABU,
                                      stroke_width=3 * S).move_to(self.badan.get_top())
        self.label = caption("toples undian · 1 kertas = 5%").next_to(self.badan, DOWN, buff=SP["s"])
        self.add(self.badan, self.mulut, self.label)
        self.kertas = VGroup()

    def slot(self, i):
        b = self.badan
        kol, brs = i % self.KOL, i // self.KOL
        x = b.get_left()[0] + 0.25 * S + (kol + 0.5) * (b.width - 0.5 * S) / self.KOL
        y = b.get_bottom()[1] + 0.2 * S + (brs + 0.5) * (b.height - 0.55 * S) / self.BRS
        return np.array([x, y, 0])

    def isi_kertas(self, counts, seed=3):
        rng = np.random.default_rng(seed)
        g = VGroup()
        i = 0
        for k, n in zip(KATA, counts):
            for _ in range(n):
                kp = kertas("…lain" if k == "lainnya" else k)
                kp.rotate(rng.uniform(-0.12, 0.12)).move_to(self.slot(i))
                kp.kata = k
                g.add(kp)
                i += 1
        return g


def penggeser(T, y, lebar=5.6):
    x0 = -lebar / 2 * S + 0.3
    track = Line([x0, y, 0], [x0 + lebar * S, y, 0], color=ABU_GELAP, stroke_width=6 * S)
    ticks = VGroup()
    for v in (0, 1, 2):
        x = x0 + lebar * S * v / 2
        ticks.add(Line([x, y - 0.12, 0], [x, y + 0.12, 0], color=ABU_GELAP, stroke_width=3 * S))
        ticks.add(mono(str(v), color=ABU, size="mikro").move_to([x, y - 0.38 * S, 0]))
    knob = Circle(radius=0.2 * S, fill_color=JINGGA, fill_opacity=1, stroke_color=HITAM,
                  stroke_width=3 * S).move_to([x0 + lebar * S * T / 2, y, 0])
    lab = teks("temperature", color=TINTA, size="body", weight=MEDIUM)
    val = mono(f"{T:.1f}".replace(".", ","), color=JINGGA, size="h2", weight=BOLD)
    kepala = VGroup(lab, val).arrange(RIGHT, buff=SP["m"]).next_to(track, UP, buff=SP["m"])
    return VGroup(track, ticks, knob, kepala), knob, val


def gembok(color=ABU, u=1.0):
    s = S * u
    body = RoundedRectangle(width=0.5 * s, height=0.4 * s, corner_radius=0.06 * s,
                            fill_color=color, fill_opacity=1, stroke_width=0)
    arc = Arc(radius=0.16 * s, start_angle=0, angle=PI, color=color, stroke_width=5 * s)
    arc.next_to(body, UP, buff=-0.02 * s)
    lub = Dot(radius=0.04 * s, color=HITAM).move_to(body)
    return VGroup(arc, body, lub)


def stempel(s, color=SAGA, size="h2"):
    t = mono(s, color=color, size=size, weight=BOLD)
    r = RoundedRectangle(width=t.width + 0.4 * S, height=t.height + 0.3 * S,
                         corner_radius=0.08 * S, stroke_color=color, stroke_width=4 * S,
                         fill_color=HITAM, fill_opacity=0.75)
    t.move_to(r)
    return VGroup(r, t).rotate(0.15)


def label_contoh():
    t = mono("angka contoh", color=ABU, size="mikro")
    t.move_to([0, JUDUL_Y - 0.6 * S, 0]).align_to([AMAN["kanan"], 0, 0], RIGHT)
    return t


# ---------------------------------------------------------------------------
class TemperatureKalauKamuBikin(KapurScene):
    PREFIX = "A_"

    def mark(self, nama):
        if not os.environ.get("STILLS"):
            return
        out = _DIR / "preview" / ORIENT
        out.mkdir(parents=True, exist_ok=True)
        self.renderer.update_frame(self, ignore_skipping=True)
        self.renderer.camera.get_image().save(out / f"{self.PREFIX}{nama}.png")

    def kosongkan(self):
        self.tanpa_header(0.3)
        self.bersihkan(CEPAT)

    def construct(self):
        for f in (self.hook, self.token, self.probabilitas, self.toples, self.undi,
                  self.kenop, self.kapan, self.selamat, self.catatan, self.tips):
            t0 = self.renderer.time
            f()
            print(f"[waktu] {f.__name__:14s} {t0:6.1f} -> {self.renderer.time:6.1f}")

    # 1 (0-4) ----------------------------------------------------------------
    def hook(self):
        q = gelembung("bikinin nama usaha kopi dong", LANGIT, size="body")
        kiri(q, 4.6)
        self.add(q)
        jaw = VGroup()
        for i, nama in enumerate(["Kopi Senja", "Kopi Pagi", "Kopi Rindu"]):
            tag = mono(f"coba {i + 1}", color=ABU, size="caption")
            b = gelembung(nama, TOSKA, size="h2")
            row = VGroup(tag, b).arrange(RIGHT, buff=SP["m"])
            kiri(row, 2.5 - i * 1.55)
            jaw.add(row)
        self.play(LaggedStart(*[FadeIn(r, shift=UP * GESER) for r in jaw], lag_ratio=0.45),
                  run_time=1.7)
        kok = judul("Kok beda?", color=KUNYIT, size="display")
        kiri(kok, -2.6)
        sub = caption("pertanyaan sama · coba 3×").next_to(kok, DOWN, buff=SP["s"]).align_to(kok, LEFT)
        self.play(FadeIn(kok, scale=1.1), FadeIn(sub), run_time=CEPAT)
        self.mark("01_hook")
        self.wait(1.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

    # 2 (4-12) ---------------------------------------------------------------
    def token(self):
        self.header("Kalau kamu yang bikin AI-nya…", chapter="TEMPERATURE")
        info = teks("AI nulis jawaban sepotong-sepotong", color=ABU, size="body")
        kiri(info, 4.1)
        self.play(FadeIn(info), run_time=CEPAT)
        potong = ["Coba", " nama", ":", " Kopi"]
        chips = VGroup(*[pil(p.strip() or p, TOSKA, size="body") for p in potong])
        chips.arrange(RIGHT, buff=0.12 * S)
        slot_t = teks("?", color=TOSKA, size="body", weight=BOLD)
        slot_r = DashedVMobject(RoundedRectangle(width=1.3 * S, height=chips.height,
                                                 corner_radius=chips.height / 2, stroke_color=TOSKA,
                                                 stroke_width=2 * S), num_dashes=24)
        slot = VGroup(slot_r, slot_t.move_to(slot_r))
        baris_ = VGroup(chips, slot).arrange(RIGHT, buff=0.12 * S)
        kiri(baris_, 2.4)
        kursor = Line(UP * 0.35 * S, DOWN * 0.35 * S, color=TOSKA, stroke_width=5 * S)
        kursor.move_to(chips[0].get_left() + LEFT * 0.08)
        arah = VGroup(Arrow(LEFT, RIGHT, color=ABU, stroke_width=4 * S, buff=0).scale(0.6),
                      caption("kiri → kanan, satu per satu")).arrange(RIGHT, buff=SP["s"])
        kiri(arah, 1.2)
        self.add(kursor)
        self.play(FadeIn(arah), run_time=CEPAT)
        for c in chips:
            self.play(FadeIn(c, shift=RIGHT * 0.15), kursor.animate.move_to(c.get_right() + RIGHT * 0.06),
                      run_time=0.45)
        self.play(FadeIn(slot), kursor.animate.move_to(slot.get_left()), run_time=0.5)
        lab = caption("kata berikutnya?", color=TOSKA).next_to(slot, DOWN, buff=SP["s"])
        lab.align_to(slot, RIGHT)
        self.play(FadeIn(lab), run_time=CEPAT)
        # definisi token
        d1 = teks("tiap potongan kata = ", color=TINTA, size="body")
        d2 = teks("token", color=TOSKA, size="h2", weight=BOLD)
        d = VGroup(d1, d2).arrange(RIGHT, buff=0.1 * S)
        kiri(d, -0.6)
        cat = caption("potongan di sini = ilustrasi").next_to(d, DOWN, buff=SP["s"]).align_to(d, LEFT)
        self.play(FadeIn(d, shift=UP * GESER), FadeIn(cat), run_time=CEPAT + 0.2)
        self.mark("02_token")
        self.wait(1.9)
        self.play(FadeOut(VGroup(info, arah, d, cat, chips[:3], kursor)), run_time=CEPAT)
        # sisakan "Kopi ?" dan pindah ke atas
        self.kalimat = VGroup(chips[3], slot, lab)
        self.play(self.kalimat.animate.move_to(pos(0, 0)).align_to([AMAN["kiri"], 0, 0], LEFT)
                  .set_y(pos(0, 4.3)[1]), run_time=CEPAT)

    # 3 (12-21) --------------------------------------------------------------
    def probabilitas(self):
        self.header("Tapi… banyak kata cocok", color=SAGA)
        y0 = pos(0, 2.7)[1]
        self.batang = daftar_batang(P_DASAR, y0)
        for r in self.batang:
            r[2].save_state()
        start = [r[2].copy().stretch_to_fit_width(0.02).align_to(r[1], LEFT) for r in self.batang]
        self.play(LaggedStart(*[FadeIn(r[0]) for r in self.batang], lag_ratio=0.15), run_time=1.0)
        self.wait(0.6)
        self.header("Jadi: tiap kandidat dikasih peluang")
        for r, s0 in zip(self.batang, start):
            r[2].become(s0)
        self.add(*[r[1] for r in self.batang], *[r[2] for r in self.batang])
        self.play(LaggedStart(*[AnimationGroup(Restore(r[2]), FadeIn(r[3]))
                                for r in self.batang], lag_ratio=0.25), run_time=2.2)
        d1 = teks("peluang = ", color=TINTA, size="body")
        d2 = teks("probabilitas", color=TOSKA, size="h2", weight=BOLD)
        d = VGroup(d1, d2).arrange(RIGHT, buff=0.1 * S)
        kiri(d, -1.6)
        sub = caption("seberapa cocok kata itu jadi kata berikutnya").next_to(d, DOWN, buff=SP["s"])
        sub.align_to(d, LEFT)
        self.contoh = label_contoh()
        self.play(FadeIn(d, shift=UP * GESER), FadeIn(sub), FadeIn(self.contoh), run_time=CEPAT + 0.2)
        self.mark("03_probabilitas")
        self.wait(2.6)
        self.play(FadeOut(d), FadeOut(sub), run_time=CEPAT)

    # 4 (21-29) --------------------------------------------------------------
    def toples(self):
        self.header("Tapi… kalau selalu ambil teratas?", color=SAGA)
        # sorot baris teratas sebentar, batang lain meredup
        self.play(*[r.animate.set_opacity(0.3) for r in self.batang[1:]], run_time=CEPAT)
        orang = VGroup()
        for nm in ("kamu", "temanmu", "orang lain"):
            ic = ikon_orang(LANGIT, 1.2)
            lb = caption(nm, color=LANGIT)
            b = gelembung("Kopi Senja", TOSKA, size="caption")
            orang.add(VGroup(ic, lb, b).arrange(DOWN, buff=SP["s"]))
        orang.arrange(RIGHT, buff=SP["m"])
        orang.move_to(pos(0, -1.9))
        self.play(LaggedStart(*[FadeIn(o, shift=UP * GESER) for o in orang], lag_ratio=0.3), run_time=1.2)
        st = stempel("SAMA SEMUA").move_to(orang.get_center() + UP * 0.1)
        self.play(FadeIn(st, scale=1.3), run_time=CEPAT)
        self.wait(1.2)
        self.play(FadeOut(orang), FadeOut(st), *[r.animate.set_opacity(1) for r in self.batang[1:]],
                  run_time=CEPAT)
        # batang -> mengecil ke atas, toples muncul di bawah
        self.header("Jadi: diundi, kayak toples")
        self.play(self.batang.animate.scale(0.78).align_to([AMAN["kiri"], 0, 0], LEFT)
                  .set_y(pos(0, 2.2)[1]),
                  self.kalimat.animate.set_y(pos(0, 4.45)[1]), run_time=CEPAT + 0.2)
        self.jar = Toples(pos(0.3, -2.0))
        self.play(FadeIn(self.jar), run_time=CEPAT)
        counts = jumlah_kertas(P_DASAR)
        self.kertas = self.jar.isi_kertas(counts)
        # kertas terbang dari batangnya masing-masing ke toples (atas -> bawah)
        anims = []
        for kp in self.kertas:
            r = self.batang[KATA.index(kp.kata)]
            tujuan = kp.get_center()
            kp.move_to(r[2].get_right())
            anims.append(kp.animate.move_to(tujuan))
        self.add(*self.kertas)
        self.play(LaggedStart(*anims, lag_ratio=0.06), run_time=2.0)
        self.mark("04_toples")
        self.wait(0.6)

    # 5 (29-37) --------------------------------------------------------------
    def undi(self):
        self.header("Peluang besar = kertas lebih banyak")
        self.play(FadeOut(self.batang), FadeOut(self.kalimat), run_time=CEPAT)
        # toples geser ke kiri, kolom hasil di kanan
        self.play(VGroup(self.jar, self.kertas).animate.scale(0.9).move_to(pos(-1.5, 1.3)), run_time=CEPAT)
        x_hasil = self.jar.badan.get_right()[0] + 0.55 * S
        y_hasil0 = pos(0, 3.6)[1]
        urutan = ["Senja", "Pagi", "Senja", "Rindu", "Obeng"]
        terpakai = set()
        hasil = VGroup()
        for i, k in enumerate(urutan):
            idx = next(j for j, kp in enumerate(self.kertas) if kp.kata == k and j not in terpakai)
            terpakai.add(idx)
            kp = self.kertas[idx]
            tag = mono(f"#{i + 1}", color=ABU, size="caption")
            word = teks(f"Kopi {k}", color=SAGA if k == "Obeng" else TOSKA, size="body", weight=MEDIUM)
            row = VGroup(tag, word).arrange(RIGHT, buff=SP["s"])
            row.move_to([0, y_hasil0 - i * 0.72 * S, 0]).align_to([x_hasil, 0, 0], LEFT)
            angkat = kertas(kp[1].text, sorot=True).scale(0.9).move_to(kp)
            self.play(FadeOut(kp), FadeIn(angkat), run_time=0.2)
            self.play(angkat.animate.move_to(self.jar.mulut.get_top() + UP * 0.45 * S), run_time=0.3)
            self.play(ReplacementTransform(angkat, row), run_time=0.45)
            hasil.add(row)
            if k != "Obeng":
                self.wait(0.05)
        st = stempel("NGAWUR", size="body").next_to(hasil[-1], DOWN, buff=SP["m"]).align_to(hasil[-1], LEFT)
        self.play(FadeIn(st, scale=1.3), run_time=CEPAT)
        self.mark("05_undi")
        self.wait(0.8)
        self.play(FadeOut(hasil), FadeOut(st), run_time=CEPAT)
        # kertas yang diambil dikembalikan (toples penuh lagi)
        baru = self.jar.isi_kertas(jumlah_kertas(P_DASAR))
        self.play(FadeOut(self.kertas), FadeIn(baru), run_time=0.3)
        self.kertas = baru

    # 6 (37-48) --------------------------------------------------------------
    def kenop(self):
        self.header("Jadi: kasih satu kenop")
        # tata ulang: penggeser atas, batang tengah, toples bawah
        g, knob, val = penggeser(1.0, pos(0, 3.75)[1])
        self.play(VGroup(self.jar, self.kertas).animate.scale(0.82 / 0.9).move_to(pos(-1.25, -2.8)),
                  run_time=CEPAT)
        self.batang = daftar_batang(P_DASAR, pos(0, 2.35)[1]).scale(0.85)
        self.batang.align_to([AMAN["kiri"], 0, 0], LEFT)
        ket = caption("ngatur seberapa rata isi toples")
        kiri(ket, 5.05)
        self.play(FadeIn(g), FadeIn(self.batang), FadeIn(ket), run_time=CEPAT + 0.2)
        self.wait(0.5)
        self.header("Namanya: temperature", color=TINTA)
        self.wait(0.5)
        self.slider, self.knob, self.val = g, knob, val
        for T, kata, warna in ((0.3, "rendah\nkonsisten", DAUN), (1.6, "tinggi\nkreatif,\nbisa ngawur", SAGA)):
            ps = peluang(T)
            g2, knob2, val2 = penggeser(T, pos(0, 3.75)[1])
            bt2 = daftar_batang(ps, pos(0, 2.35)[1]).scale(0.85).align_to([AMAN["kiri"], 0, 0], LEFT)
            k2 = self.jar.isi_kertas(jumlah_kertas(ps), seed=int(T * 10))
            k1, *k_rest = kata.split("\n")
            tag = VGroup(pil(k1, warna, size="body"),
                         teks("\n".join(k_rest), color=warna, size="body", line_spacing=0.9)
                         ).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
            tag.next_to(self.jar.badan, RIGHT, buff=SP["m"]).align_to(self.jar.badan, UP)
            self.play(Transform(self.knob, knob2), Transform(self.val, val2),
                      Transform(self.batang, bt2), run_time=1.3)
            self.play(FadeOut(self.kertas), FadeIn(k2), FadeIn(tag), run_time=CEPAT + 0.2)
            self.kertas = k2
            self.mark("06_kenop_rendah" if T < 1 else "06_kenop_tinggi")
            self.wait(1.4)
            self.play(FadeOut(tag), run_time=0.3)
        self.kosongkan()

    # 7 (48-55) --------------------------------------------------------------
    def kapan(self):
        self.header("Kapan rendah, kapan tinggi?")
        kol = VGroup()
        for judul_, T, warna, isi in (("rendah", 0.3, DAUN, ["fakta", "kode", "ringkasan"]),
                                      ("tinggi", 1.6, TOSKA, ["ide nama", "caption", "brainstorming"])):
            h = teks(judul_, color=warna, size="h2", weight=BOLD)
            mini, _, _ = penggeser(T, 0, lebar=2.6)
            mini.remove(mini[3])  # tanpa kepala
            v = mono(f"temp. {T:.1f}".replace(".", ","), color=JINGGA, size="caption")
            chips = VGroup(*[pil(s, warna, size="body") for s in isi]).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
            hasil = caption("→ konsisten" if T < 1 else "→ variasi", color=warna)
            col = VGroup(h, v, mini, chips, hasil).arrange(DOWN, buff=SP["m"], aligned_edge=LEFT)
            kol.add(col)
        kol.arrange(RIGHT, buff=SP["xl"], aligned_edge=UP)
        kol.move_to(pos(0, 1.2))
        self.play(FadeIn(kol[0], shift=UP * GESER), run_time=CEPAT + 0.2)
        self.wait(1.8)
        self.play(FadeIn(kol[1], shift=UP * GESER), run_time=CEPAT + 0.2)
        c = label_contoh()
        self.add(c)
        self.mark("07_kapan")
        self.wait(2.6)
        self.kosongkan()

    # 8 (55-61) --------------------------------------------------------------
    def selamat(self):
        s1 = judul("Selamat.", size="display")
        kiri(s1, 4.4)
        s2 = judul("Kamu baru aja bikin", color=ABU, size="h2").next_to(s1, DOWN, buff=SP["m"]).align_to(s1, LEFT)
        tem = judul("temperature", color=KUNYIT, size="raksasa").next_to(s2, DOWN, buff=SP["m"]).align_to(s1, LEFT)
        self.play(FadeIn(s1, shift=UP * GESER), run_time=CEPAT + 0.1)
        self.play(FadeIn(s2), run_time=CEPAT)
        self.play(Write(tem), run_time=KETUK)
        ul = coret_kapur(tem, color=KUNYIT)
        self.play(Create(ul), run_time=CEPAT)
        # batas analogi: kertas -> angka
        kp = VGroup(*[kertas(k) for k in ("Senja", "Pagi", "Rindu")]).arrange(RIGHT, buff=0.12 * S)
        ang = mono("0,40 · 0,25 · …", color=JINGGA, size="body")
        g = VGroup(kp, Arrow(LEFT, RIGHT, color=ABU, stroke_width=4 * S, buff=0).scale(0.45), ang)
        g.arrange(RIGHT, buff=SP["s"])
        if g.width > LEBAR_AMAN:
            g.scale_to_fit_width(LEBAR_AMAN)
        kiri(g, -1.4)
        cat = caption("aslinya bukan kertas, tapi hitungan angka").next_to(g, DOWN, buff=SP["s"]).align_to(g, LEFT)
        self.play(FadeIn(kp), run_time=CEPAT)
        self.play(GrowArrow(g[1]), FadeIn(ang, shift=RIGHT * 0.2), FadeIn(cat), run_time=CEPAT + 0.2)
        self.mark("08_selamat")
        self.wait(1.8)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self._bab], run_time=CEPAT)

    # 9a (61-67) -------------------------------------------------------------
    def catatan(self):
        self.header("Catatan")
        g, knob, _ = penggeser(1.0, pos(0, 3.0)[1], lebar=4.6)
        gb = gembok(ABU, 1.3).move_to(knob.get_center() + UP * 0.05)
        lab = pil("di aplikasi chat: diatur penyedia", LANGIT, size="body")
        kiri(lab, 1.5)
        sub = caption("sebagian model terbaru: nilainya dikunci").next_to(lab, DOWN, buff=SP["s"]).align_to(lab, LEFT)
        self.play(FadeIn(g), run_time=CEPAT)
        self.play(FadeIn(gb, shift=DOWN * 0.2), FadeIn(lab), run_time=CEPAT + 0.2)
        self.play(FadeIn(sub), run_time=CEPAT)
        self.wait(0.8)
        nol = VGroup(mono("temperature 0", color=JINGGA, size="body", weight=BOLD),
                     teks("≠ selalu sama persis", color=TINTA, size="body")).arrange(RIGHT, buff=SP["s"])
        kiri(nol, -1.0)
        dua = VGroup(*[gelembung(s, TOSKA, size="caption") for s in ("Kopi Senja", "Kopi Senja", "Kopi Pagi")])
        dua.arrange(RIGHT, buff=SP["s"])
        kiri(dua, -2.4)
        self.play(FadeIn(nol, shift=UP * GESER), run_time=CEPAT)
        self.play(LaggedStart(*[FadeIn(d) for d in dua], lag_ratio=0.3), run_time=0.9)
        self.mark("09_catatan")
        self.wait(1.0)
        self.kosongkan()

    # 9b (67-74) -------------------------------------------------------------
    def tips(self):
        self.header("Pakai aplikasi chat biasa?")
        r1 = teks("Mau konsisten?", color=DAUN, size="h2", weight=BOLD)
        q1 = gelembung("jawab singkat · format: nama + alasan", LANGIT, size="caption")
        b1 = VGroup(r1, q1).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        kiri(b1, 4.0)
        r2 = teks("Mau variasi?", color=TOSKA, size="h2", weight=BOLD)
        q2 = gelembung("kasih 10 ide nama usaha kopi", LANGIT, size="caption")
        b2 = VGroup(r2, q2).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        kiri(b2, 1.3)
        nama = ["Senja", "Pagi", "Rindu", "Hangat", "Seduh", "Teduh", "Ampas", "Sudut", "Tepi", "Fajar"]
        daftar = VGroup(*[pil(f"Kopi {n}", TOSKA, size="caption") for n in nama])
        daftar.arrange_in_grid(rows=4, cols=3, buff=(0.15 * S, 0.15 * S), flow_order="rd")
        kiri(daftar, -2.0)
        self.play(FadeIn(b1, shift=UP * GESER), run_time=CEPAT + 0.2)
        self.wait(1.2)
        self.play(FadeIn(b2, shift=UP * GESER), run_time=CEPAT + 0.2)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.15) for d in daftar], lag_ratio=0.12), run_time=1.4)
        self.mark("10_tips")
        self.wait(1.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=KETUK)
