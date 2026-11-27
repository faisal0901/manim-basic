"""
Video prompt caching, gaya A "Kalau kamu yang bikin...", design system KAPUR.

Kasus: bot CS toko online. Rantai: aturan toko dihitung ulang tiap pertanyaan -> tapi sama terus,
jadi simpan hasil hitungan (KV cache) di memori GPU -> zoom server 3D -> tapi gimana tahu sama,
jadi CPU cocokin sidik blok dari awal -> tapi memori terbatas, jadi sementara -> "Selamat, kamu
baru aja bikin prompt caching" -> hati-hati: cache ditulis tapi nggak pernah kebaca (jam di baris
pertama, toko sepi) -> tips.

Tiap adegan = satu kelas (2D: KapurScene, 3D: Kapur3D). Gabung pakai gabung.sh.
Angka: 3.000 token, 100 pembeli, jam, jeda menit = angka contoh. 1/10, 1,25x, 5 menit = dokumentasi
salah satu penyedia (Anthropic, dicek 27 Nov 2026), ditulis "salah satu penyedia".

Frame kunci:  STILLS=1 ORIENT=vertical manim -s -ql prompt_caching_kalau_kamu_bikin.py <Kelas>
Video:        ORIENT=vertical manim -qh prompt_caching_kalau_kamu_bikin.py <Kelas>   lalu  ./gabung.sh
"""
import sys
from pathlib import Path

_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_DIR))
from caching_zoom_3d import *  # noqa: E402,F403

JEDA = 1.8
JEDA_PANJANG = 2.9
BAB = "PROMPT CACHING"
ATURAN = [
    "Kamu CS Toko Gadget Jaya.",
    "Jawab ramah, singkat.",
    "Garansi resmi 1 tahun.",
    "Retur maks. 7 hari.",
    "Ongkir gratis > Rp200rb.",
]


# --------------------------------------------------------------------------
# Komponen 2D
# --------------------------------------------------------------------------
def blok2d(color, s=0.5, isi=0.35):
    return RoundedRectangle(width=s * S, height=s * S, corner_radius=0.07 * S, stroke_color=color,
                            stroke_width=2.2 * S, fill_color=redup(color, 0.4), fill_opacity=isi)


def menara2d(n, color=ABU, s=0.5, gap=0.07):
    return VGroup(*[blok2d(color, s) for _ in range(n)]).arrange(UP, buff=gap * S)


def chip(label="GPU", color=TOSKA, u=1.7):
    c = ikon_ai(ukuran=u, color=color)
    lab = Text(label, font=FONT_MONO, weight=BOLD, color=color, font_size=34 * S * u / 1.6).move_to(c[1])
    c.remove(c[3])
    c.add(lab)
    return c


def kolom_angka(n=6, color=JINGGA, seed=3):
    rng = np.random.default_rng(seed)
    rows = VGroup(*[mono("  ".join(f"{v:+.2f}" for v in rng.normal(0, 0.8, 3)), color=color, size="mikro")
                    for _ in range(n)])
    return rows.arrange(DOWN, buff=0.12 * S, aligned_edge=LEFT)


def kartu_aturan(baris_jam=None, jam_di="atas", lebar=6.6):
    """Kartu system prompt toko. baris_jam: teks jam (mis. 'Sekarang: 13:31:05')."""
    head = mono("ATURAN TOKO · instruksi bot", color=ABU, size="mikro", weight=BOLD)
    rows = [teks(r, size="caption") for r in ATURAN]
    jam = None
    if baris_jam:
        jam = mono(baris_jam, color=KUNYIT, size="caption", weight=BOLD)
        rows = [jam] + rows if jam_di == "atas" else rows + [jam]
    isi = VGroup(head, *rows).arrange(DOWN, buff=0.16 * S, aligned_edge=LEFT)
    k = kartu(isi, pad=0.35)
    k[0].stretch_to_fit_width(lebar * S).align_to(isi, LEFT).shift(LEFT * 0.35 * S)
    return k, jam, rows


def jam_ikon(r=0.45, color=JINGGA):
    c = Circle(radius=r * S, stroke_color=color, stroke_width=3 * S)
    jarum = Line(c.get_center(), c.get_center() + UP * r * 0.7 * S, color=color, stroke_width=3 * S)
    titik = Dot(c.get_center(), radius=0.04 * S, color=color)
    return VGroup(c, jarum, titik)


def ganti(scene, lama, baru, rt=CEPAT):
    scene.play(FadeOut(lama, shift=UP * GESER), FadeIn(baru, shift=UP * GESER), run_time=rt)
    return baru


# --------------------------------------------------------------------------
# 01 hook
# --------------------------------------------------------------------------
class S01Hook(KapurScene):
    def construct(self):
        self.add(label_bab(BAB))
        tanya = gelembung("masih ready kak?", color=LANGIT, size="body")
        tanya.move_to(pos(0.9, 4.4))
        orang = ikon_orang(LANGIT, 1.3).next_to(tanya, RIGHT, buff=0.2 * S)
        self.play(FadeIn(tanya, shift=UP * GESER), FadeIn(orang), run_time=CEPAT)
        tower = menara2d(9, ABU, s=0.55).move_to(pos(-1.2, -0.3))
        lab = teks("+ aturan toko", color=TINTA, size="body", weight=MEDIUM).move_to(pos(1.6, 0.8))
        tok = mono("3.000 token", color=JINGGA, size="h2", weight=BOLD).next_to(lab, DOWN, buff=0.2 * S)
        cth = caption("angka contoh").next_to(tok, DOWN, buff=0.12 * S)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.6 * S) for b in tower], lag_ratio=0.12),
                  FadeIn(lab), run_time=1.3)
        self.play(FadeIn(tok), FadeIn(cth), run_time=CEPAT)
        nol = judul("dari nol.", color=SAGA, size="display").move_to(pos(1.6, -1.6))
        self.play(LaggedStart(*[b.animate.set_stroke(SAGA).set_fill(redup(SAGA, 0.5), 0.5) for b in tower],
                              lag_ratio=0.06), FadeIn(nol, scale=1.1), run_time=1.0)
        self.mark("A_01_hook")
        self.wait(JEDA)


# --------------------------------------------------------------------------
# 02 kalau kamu yang bikin
# --------------------------------------------------------------------------
class S02Kalau(KapurScene):
    def construct(self):
        self.header("Kalau kamu yang bikin…", chapter=BAB)
        tower = menara2d(7, ABU, s=0.5).move_to(pos(-2.7, 0.6))
        q = blok2d(LANGIT, 0.5, 0.6).next_to(tower, UP, buff=0.07 * S)
        lt = caption("aturan toko").next_to(tower, DOWN, buff=0.2 * S)
        lq = caption("pertanyaan", color=LANGIT).next_to(q, RIGHT, buff=0.15 * S)
        self.play(FadeIn(tower, shift=UP * GESER), FadeIn(q), FadeIn(lt), FadeIn(lq), run_time=CEPAT)
        g = chip("GPU", TOSKA, 1.9).move_to(pos(-0.2, 0.9))
        lg = teks("GPU · chip tukang hitung", color=TOSKA, size="caption", weight=MEDIUM)
        lg.next_to(g, DOWN, buff=0.35 * S)
        self.play(FadeIn(g, scale=0.9), FadeIn(lg), run_time=CEPAT)
        angka = kolom_angka(8).move_to(pos(2.75, 0.9))
        semua = VGroup(*tower, q)
        terbang = [b.copy() for b in semua]
        self.play(LaggedStart(*[t.animate.move_to(g.get_center()).scale(0.3).set_opacity(0) for t in terbang],
                              lag_ratio=0.1), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.3 * S) for r in angka], lag_ratio=0.1), run_time=1.2)
        rumus = VGroup(teks("token", color=TINTA, size="body"), teks("→", color=ABU, size="body"),
                       teks("angka", color=JINGGA, size="body", weight=MEDIUM)).arrange(RIGHT, buff=0.25 * S)
        rumus.move_to(pos(0, -2.6))
        self.play(FadeIn(rumus, shift=UP * GESER), run_time=CEPAT)
        self.mark("A_02_kalau")
        self.wait(JEDA)


# --------------------------------------------------------------------------
# 03 tapi sama terus -> jadi simpan
# --------------------------------------------------------------------------
class S03Tapi(KapurScene):
    def construct(self):
        self.header("Tapi… aturannya sama terus", chapter=BAB)
        tower = menara2d(7, ABU, s=0.5).move_to(pos(-1.6, 0.4))
        g = chip("GPU", TOSKA, 1.3).move_to(pos(1.8, 0.4))
        self.play(FadeIn(tower), FadeIn(g), run_time=CEPAT)
        hit = VGroup(teks("pembeli ke-", color=LANGIT, size="body"),
                     mono("1", color=JINGGA, size="h2", weight=BOLD)).arrange(RIGHT, buff=0.1 * S)
        hit.move_to(pos(0, 3.6))
        self.play(FadeIn(hit), run_time=CEPAT)
        for n, rt in [(1, 0.45), (2, 0.4), (3, 0.35), (47, 0.3), (100, 0.4)]:
            angka = mono(str(n), color=JINGGA, size="h2", weight=BOLD).move_to(hit[1], aligned_edge=LEFT)
            self.remove(hit[1])
            hit[1] = angka
            self.add(angka)
            self.play(LaggedStart(*[Indicate(b, color=SAGA, scale_factor=1.08) for b in tower], lag_ratio=0.05),
                      Indicate(g[1], color=SAGA, scale_factor=1.04), run_time=rt)
        boros = teks("100 pembeli = 100× hitung ulang", color=SAGA, size="body", weight=MEDIUM).move_to(pos(0, -2.2))
        cth = caption("angka contoh").next_to(boros, DOWN, buff=0.15 * S)
        self.play(FadeIn(boros, shift=UP * GESER), FadeIn(cth), run_time=CEPAT)
        self.mark("A_03_tapi")
        self.wait(1.2)
        self.header("Jadi, simpan hasil hitungannya", chapter=BAB)
        mem = RoundedRectangle(width=3.2 * S, height=2.2 * S, corner_radius=0.15 * S, stroke_color=TOSKA,
                               stroke_width=2.5 * S, fill_color=redup(TOSKA, 0.12), fill_opacity=1)
        mem.move_to(pos(0, 0.4))
        lm = teks("memori GPU", color=TOSKA, size="caption", weight=MEDIUM).next_to(mem, DOWN, buff=0.2 * S)
        simpan = menara2d(5, TOSKA, s=0.46).arrange(RIGHT, buff=0.08 * S).move_to(mem)
        self.play(FadeOut(hit), FadeOut(boros), FadeOut(cth), FadeOut(g), run_time=CEPAT)
        self.play(ReplacementTransform(tower[:5], simpan), FadeOut(tower[5:]), FadeIn(mem), FadeIn(lm),
                  run_time=LAMBAT)
        self.bring_to_front(simpan)
        bukan = caption("yang disimpan: angka hasil hitungan, bukan teks").move_to(pos(0, -2.2))
        self.play(FadeIn(bukan), run_time=CEPAT)
        self.mark("A_04_simpan")
        self.wait(1.2)


# --------------------------------------------------------------------------
# 3D: zoom masuk server
# --------------------------------------------------------------------------
def dunia_rak():
    g = VGroup(lantai(16))
    fokus = None
    for i, x in enumerate([-3.1, 0.0, 3.1]):
        g.add(kotak_garis(2.8, 1.8, 7.0, pusat=[x, 0.3 * i, 3.5]))
        for k in range(8):
            t = tray([x, 0.3 * i, 0.5 + k * 0.82])
            if i == 1 and k == 4:
                t[0].set_stroke(KUNYIT, width=4)
                fokus = t
            g.add(t)
    return g, fokus


def dunia_server():
    badan = balok(7.6, 6.2, 0.5, ABU_GELAP, [0, 0.4, 0], isi=0.8, garis=2.5, fill=PERMUKAAN)
    cpu = VGroup(balok(1.4, 1.4, 0.18, TINTA, [-2.4, -1.6, 0.35], isi=0.5, fill=redup(TINTA, 0.25)),
                 balok(0.8, 0.8, 0.1, TINTA, [-2.4, -1.6, 0.5], isi=0.3))
    ram = VGroup(*[balok(0.12, 1.6, 0.5, ABU, [-0.9 + j * 0.28, -1.6, 0.5], isi=0.6, garis=1.4) for j in range(4)])
    gpus = VGroup()
    fokus = None
    for r in range(2):
        for c in range(4):
            gp = balok(1.45, 1.3, 0.35, TOSKA, [-2.55 + c * 1.7, 0.75 + r * 1.65, 0.45], isi=0.45)
            if r == 0 and c == 2:
                fokus = gp
            gpus.add(gp)
    return VGroup(badan, cpu, ram, gpus), cpu, gpus, fokus


def dunia_gpu():
    papan = balok(6.4, 5.2, 0.16, ABU_GELAP, [0, 0, 0], isi=0.8, garis=2, fill=PERMUKAAN)
    inti = balok(2.6, 2.6, 0.3, TOSKA, [0, 0, 0.25], isi=0.5, garis=3)
    hbm = VGroup()
    for x, y in [(-2.1, -1.2), (-2.1, 1.2), (2.1, -1.2), (2.1, 1.2)]:
        hbm.add(VGroup(*[balok(1.0, 1.4, 0.16, KERTAS, [x, y, 0.16 + i * 0.2], isi=0.25, garis=1.6)
                         for i in range(8)]))
    return VGroup(papan, inti, hbm), inti, hbm, hbm[2]


PREFIX = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
LAIN = [(0, 2), (1, 2), (3, 3), (4, 2), (2, 3), (0, 3)]


def dunia_memori(tampil_prefix=True):
    isi = {p: ABU_GELAP for p in LAIN}
    if tampil_prefix:
        isi.update({p: TOSKA for p in PREFIX})
    grid, slots = blok_slot(isi=isi)
    papan = balok(5.6, 4.6, 0.12, ABU_GELAP, [0, 0, -0.08], isi=0.8, garis=2, fill=PERMUKAAN)
    return VGroup(papan, grid), slots


class Zoom3D(Kapur3D):
    """Kapur3D + header/label yang bisa masuk-keluar dengan animasi."""

    _hdr = None

    def judul3d(self, s, chapter=BAB):
        if not hasattr(self, "_bab_on"):
            self._bab_on = True
            self.overlay(label_bab(chapter))
        h = judul(s, size="h1").move_to([0, JUDUL_Y, 0]).align_to([AMAN["kiri"], 0, 0], LEFT)
        self.add_fixed_in_frame_mobjects(h)
        self.remove(h)
        anims = [FadeIn(h, shift=UP * GESER)]
        if self._hdr is not None:
            anims.append(FadeOut(self._hdr, shift=UP * GESER))
        self._hdr = h
        self.play(*anims, run_time=CEPAT)

    def lab(self, s, xy, color=TINTA, size="caption", weight=MEDIUM, mono_=False):
        t = (mono(s, color=color, size=size, weight=BOLD) if mono_ else teks(s, color=color, size=size, weight=weight))
        t.move_to([xy[0], xy[1], 0])
        self.add_fixed_in_frame_mobjects(t)
        self.remove(t)
        return t

    def masuk(self, world, target, zoom_akhir=3.2, rt=1.1, extra=()):
        """Kamera 'masuk': dunia digeser supaya target di tengah, zoom naik, lalu hilang."""
        geser = -np.array(target.get_center())
        self.move_camera(zoom=zoom_akhir, run_time=rt, rate_func=rate_functions.ease_in_quad,
                         added_anims=[world.animate.shift(geser).set_opacity(0), *extra])
        self.remove(world)


# v2: kamera TETAP (sudut & zoom sama di semua level). "Masuk" = dunia lama membesar pelan di sekitar
# objek sorotan sambil memudar, dunia baru muncul dari kecil di tengah, bersamaan (crossfade).
# Tidak ada layar gelap, tidak ada putar kamera, warna sorotan sudah ada sejak awal.
PHI, THETA, ZOOM = 62 * DEGREES, -66 * DEGREES, 0.78
PUSAT3D = [0, 0, 0.3]
T_GESER = 1.4   # geser pelan supaya sorotan ke tengah
T_MASUK = 1.8   # crossfade level
MEM_S = 1.35    # skala dunia memori di akhir zoom


def slots_center(p, nx=5, ny=4, s=0.9, gap=0.14):
    i, j = p
    return np.array([(i - (nx - 1) / 2) * (s + gap), (j - (ny - 1) / 2) * (s + gap), 0.0])


class Zoom3Dv2(Zoom3D):
    def kamera(self):
        self.set_camera_orientation(phi=PHI, theta=THETA, zoom=ZOOM, frame_center=PUSAT3D)

    def lab(self, s, xy, color=TINTA, size="body", weight=MEDIUM, mono_=False):
        return super().lab(s, xy, color=color, size=size, weight=weight, mono_=mono_)

    def masuk(self, lama, sorot, baru, keluar=(), datang=()):
        """Zoom penuh ke objek sorotan (kuning), baru pindah level.
        1) dunia digeser + dibesarkan pelan sampai sorotan memenuhi layar, objek lain meredup;
        2) level baru muncul di ukuran penuh sementara yang lama memudar (crossfade singkat)."""
        p = np.array(PUSAT3D, dtype=float)
        lebar_layar = config.frame_width / ZOOM
        k = min(6.0, 0.75 * lebar_layar / max(sorot.width, sorot.depth, sorot.height * 1.6))
        geser = p - np.array(sorot.get_center())
        lama.generate_target()
        lama.target.shift(geser).scale(k, about_point=p)
        jaga = {id(m) for m in sorot.get_family()}
        for m, tm in zip(lama.get_family(), lama.target.get_family()):
            if id(m) in jaga or m.submobjects:
                continue
            tm.set_stroke(opacity=0.08)
            tm.set_fill(opacity=0.03)
        self.play(MoveToTarget(lama), *[FadeOut(m) for m in keluar], run_time=2.6, rate_func=smooth)
        self.play(FadeOut(lama, scale=1.25), FadeIn(baru, scale=0.85), *[FadeIn(m) for m in datang],
                  run_time=1.0, rate_func=smooth)
        self.remove(lama)


def dunia_rak_v2():
    g, fokus = dunia_rak()
    g.scale(0.92).shift(IN * 3.0)
    return g, fokus


def dunia_server_v2():
    srv, cpu, gpus, fg = dunia_server()
    fg.set_stroke(KUNYIT, width=4)
    return srv, fg


def dunia_gpu_v2():
    gp, inti, hbm, fh = dunia_gpu()
    fh.set_stroke(KUNYIT, width=3)
    gp.scale(1.12)
    return gp, fh


def terang_memori(mem):
    """Papan & slot memori sedikit lebih terang supaya transisi nggak terasa gelap."""
    mem[0].set_stroke(ABU, width=2.5)
    for m in mem[1]:
        if isinstance(m, Square):
            m.set_stroke(ABU_GELAP, width=2.5)
        elif m.get_stroke_color() is not None and m.get_stroke_color().to_hex().upper() == ABU_GELAP.upper():
            m.set_stroke(ABU, width=2)
    return mem


class S04Zoom(Zoom3Dv2):
    def construct(self):
        self.kamera()
        rak_, fokus = dunia_rak_v2()
        l1 = self.lab("server AI di data center", (0, 4.6), color=ABU)
        self.add(rak_)
        self.judul3d("Kita intip servernya")
        self.play(FadeIn(l1), run_time=0.6)
        self.wait(0.6)
        self.mark("A_05_rak")
        # rak -> server
        srv, fg = dunia_server_v2()
        a = self.lab("GPU · tukang hitung", (0.6, 4.0), color=TOSKA)
        b = self.lab("CPU · manajer", (-1.9, -3.2), color=TINTA)
        b2 = self.lab("terima pesan, atur antrean", (-0.9, -3.85), color=ABU, size="caption")
        self.masuk(rak_, fokus, srv, keluar=[l1], datang=[a, b, b2])
        self.wait(1.0)
        self.mark("A_06_server")
        # server -> GPU
        gp, fh = dunia_gpu_v2()
        c = self.lab("memori GPU", (1.4, 3.7), color=KERTAS)
        d = self.lab("inti hitung", (-0.3, -3.4), color=TOSKA)
        self.masuk(srv, fg, gp, keluar=[a, b, b2], datang=[c, d])
        self.wait(0.9)
        self.mark("A_07_gpu")
        # GPU -> memori
        mem, slots = dunia_memori(tampil_prefix=False)
        mem.scale(MEM_S, about_point=ORIGIN)
        terang_memori(mem)
        self.masuk(gp, fh, mem, keluar=[c, d])
        isi = VGroup()
        for p in PREFIX:
            k = kubus(TOSKA, sisi=0.9 * 0.86 * MEM_S, isi=0.5)
            k.move_to(slots_center(p) * MEM_S + OUT * 0.39 * MEM_S)
            isi.add(k)
        e = self.lab("hasil hitungan aturan toko", (0, 4.45), color=TOSKA)
        self.play(FadeIn(e), LaggedStart(*[FadeIn(k, shift=IN * 0.6) for k in isi], lag_ratio=0.2), run_time=1.0)
        kartu_ = kartu(VGroup(mono("isi 1 blok (ilustrasi)", color=ABU, size="caption"),
                              mono("0.12  -0.87  0.45  1.03  …", color=JINGGA, size="body"))
                       .arrange(DOWN, buff=0.15, aligned_edge=LEFT), aksen=JINGGA).move_to([0, -3.1, 0])
        self.add_fixed_in_frame_mobjects(kartu_)
        self.remove(kartu_)
        f = self.lab("angka, bukan teks", (0, -4.3), color=KUNYIT)
        self.play(FadeIn(kartu_), FadeIn(f), run_time=0.8)
        self.mark("A_08_memori")
        self.wait(1.2)


class S05Cocok(Zoom3Dv2):
    def construct(self):
        self.kamera()
        mem, slots = dunia_memori()
        mem.scale(MEM_S, about_point=ORIGIN)
        terang_memori(mem)
        self.add(mem)
        self.judul3d("Pertanyaan berikutnya")
        # dunia memori geser ke atas pelan, pesan baru masuk dari bawah
        s = 0.9
        req = VGroup()
        for n in range(7):
            k = kubus(LANGIT if n < 5 else KUNYIT, sisi=s * 0.86, isi=0.3 if n < 5 else 0.55)
            k.move_to([(n - 3) * (s + 0.1) + 0.5, -2.9, s * 0.43])
            req.add(k)
        l0 = self.lab("pesan baru masuk", (-1.9, -3.95), color=LANGIT)
        self.play(mem.animate.scale(1.05 / MEM_S, about_point=ORIGIN).shift(UP * 1.5), run_time=1.2, rate_func=smooth)
        self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.5) for k in req], lag_ratio=0.1), FadeIn(l0), run_time=1.2)
        l1 = self.lab("CPU cocokin sidik tiap blok, dari awal", (0, 4.5), color=TINTA, size="caption")
        self.play(FadeIn(l1), run_time=0.6)
        tali = VGroup()
        for n, p in enumerate(PREFIX):
            t = garis_putus(req[n].get_center() + UP * 0.4, slots[p].get_center() + DOWN * 0.4, color=DAUN, w=2.5)
            tali.add(t)
            self.play(Create(t), req[n].animate.set_stroke(DAUN).set_fill(redup(DAUN, 0.35), 0.35), run_time=0.4)
        l2 = self.lab("sama → GPU loncatin hitungannya", (0, -2.0), color=DAUN, size="caption")
        l3 = self.lab("baru → dihitung", (2.2, -3.95), color=KUNYIT)
        self.play(FadeIn(l2), FadeIn(l3), run_time=0.6)
        self.mark("A_09_cocok")
        self.wait(1.4)
        # crossfade ke aturan "dari awal": kamera tetap
        sisi, gap = 0.72, 0.07
        simpan = menara([TOSKA] * 5, x=-2.6, sisi=sisi, gap=gap)
        cocok = menara([DAUN] * 5 + [LANGIT, LANGIT], x=0.0, sisi=sisi, gap=gap)
        beda = menara([DAUN] * 7, x=2.6, sisi=sisi, gap=gap)
        towers = VGroup(simpan, cocok, beda).shift(IN * 2.3)
        lama = VGroup(mem, req, tali)
        self.judul3d("Dicocokin dari awal")
        m1 = self.lab("tersimpan", (-2.75, -3.2), color=TOSKA, size="caption")
        m2 = self.lab("sama persis", (0.0, -3.2), color=DAUN, size="caption")
        self.play(FadeOut(lama), FadeOut(VGroup(l0, l1, l2, l3)), FadeIn(towers), FadeIn(m1), FadeIn(m2),
                  run_time=1.4, rate_func=smooth)
        m3 = VGroup(self.lab("beda 1 kata", (2.65, -3.2), color=SAGA, size="caption"),
                    self.lab("di depan", (2.65, -3.7), color=SAGA, size="caption"))
        self.play(beda[1].animate.set_stroke(KUNYIT, width=4).set_fill(redup(KUNYIT, 0.4), 0.6), FadeIn(m3),
                  run_time=0.8)
        self.play(LaggedStart(*[k.animate.set_stroke(SAGA).set_fill(redup(SAGA, 0.4), 0.55) for k in beda[2:]],
                              lag_ratio=0.2), run_time=1.4)
        m4 = self.lab("semua setelahnya dihitung ulang", (1.4, 3.3), color=SAGA, size="caption")
        m5 = self.lab("yang tetap → depan · berubah → belakang", (0, -4.5), color=TINTA, size="caption")
        self.play(FadeIn(m4), FadeIn(m5), run_time=0.7)
        self.mark("A_10_dari_awal")
        self.wait(JEDA)



# --------------------------------------------------------------------------
# 06 tapi memori terbatas
# --------------------------------------------------------------------------
class S06Terbatas(KapurScene):
    def construct(self):
        self.header("Tapi… memori GPU terbatas", chapter=BAB)
        nx, ny, s = 6, 5, 0.78
        slot = VGroup(*[Square(s * S, stroke_color=GARIS, stroke_width=2 * S) for _ in range(nx * ny)])
        slot.arrange_in_grid(ny, nx, buff=0.1 * S).move_to(pos(0, 1.0))
        rng = np.random.default_rng(5)
        mine = [0, 1, 2, 3, 4]
        blok = VGroup()
        for i, sq in enumerate(slot):
            col = TOSKA if i in mine else ABU_GELAP
            b = blok2d(col, s * 0.82, 0.5 if i in mine else 0.2).move_to(sq)
            blok.add(b)
        self.play(FadeIn(slot), run_time=CEPAT)
        order = list(range(nx * ny))
        self.play(LaggedStart(*[FadeIn(blok[i], scale=0.6) for i in order], lag_ratio=0.03), run_time=1.3)
        penuh = teks("penuh", color=SAGA, size="body", weight=MEDIUM).next_to(slot, DOWN, buff=0.3 * S)
        self.play(FadeIn(penuh), run_time=CEPAT)
        self.header("Jadi, simpanannya sementara", chapter=BAB)
        lama = [i for i in range(nx * ny) if i not in mine and rng.random() < 0.55]
        self.play(*[FadeOut(blok[i], scale=0.6) for i in lama], FadeOut(penuh), run_time=0.9)
        jam = jam_ikon(0.5).move_to(pos(-2.4, -2.6))
        lj = VGroup(teks("contoh: 5 menit", color=JINGGA, size="body", weight=MEDIUM),
                    caption("salah satu penyedia"), caption("diperpanjang tiap dipakai", color=DAUN)).arrange(DOWN, buff=0.12 * S,
                                                                                      aligned_edge=LEFT)
        lj.next_to(jam, RIGHT, buff=0.35 * S)
        self.play(FadeIn(jam), FadeIn(lj), run_time=CEPAT)
        self.play(Rotate(jam[1], -PI * 1.2, about_point=jam[0].get_center()), run_time=1.0)
        self.play(*[Indicate(blok[i], color=DAUN, scale_factor=1.12) for i in mine],
                  Rotate(jam[1], PI * 1.2, about_point=jam[0].get_center()), run_time=0.8)
        self.mark("A_11_sementara")
        self.wait(1.2)


# --------------------------------------------------------------------------
# 07 selamat
# --------------------------------------------------------------------------
class S07Selamat(KapurScene):
    def construct(self):
        self.add(label_bab(BAB))
        a = teks("Selamat, kamu baru aja bikin", color=ABU, size="h2").move_to(pos(0, 4.2))
        b = judul("prompt caching", color=TINTA, size="raksasa").next_to(a, DOWN, buff=0.4 * S)
        c = coret_kapur(b)
        self.play(FadeIn(a, shift=UP * GESER), run_time=CEPAT)
        self.play(Write(b), run_time=LAMBAT)
        self.play(Create(c), run_time=CEPAT)
        b1 = batang("hitung biasa", 1.0, color=SAGA, panjang=6.4, teks_nilai="1×").move_to(pos(0, 0.2))
        b2 = batang("baca dari cache", 0.1, color=DAUN, panjang=6.4, teks_nilai="0,1×").move_to(pos(0, -1.2))
        for bb in (b1, b2):
            bb.align_to([AMAN["kiri"] + 0.3, 0, 0], LEFT)
        sumber = caption("harga input · salah satu penyedia · bisa berubah").move_to(pos(0, -2.4))
        self.play(FadeIn(b1), run_time=CEPAT)
        self.play(FadeIn(b2), FadeIn(sumber), run_time=CEPAT)
        self.mark("A_12_selamat")
        self.wait(JEDA)


# --------------------------------------------------------------------------
# 08 hati-hati: ditulis terus, nggak pernah kebaca
# --------------------------------------------------------------------------
class S08HatiHati(KapurScene):
    def construct(self):
        self.header("Tapi hati-hati", chapter=BAB)
        k, jam, rows = kartu_aturan("Sekarang: 13:31:05", "atas")
        k.move_to(pos(0, 2.7))
        self.play(FadeIn(k, shift=UP * GESER), run_time=CEPAT)
        tulis = VGroup(mono("cache ditulis", color=ABU, size="caption"), mono("0", color=JINGGA, size="h2", weight=BOLD))
        baca = VGroup(mono("cache kebaca", color=ABU, size="caption"), mono("0", color=SAGA, size="h2", weight=BOLD))
        for g in (tulis, baca):
            g.arrange(DOWN, buff=0.12 * S)
        VGroup(tulis, baca).arrange(RIGHT, buff=1.4 * S).move_to(pos(0, -0.4))
        self.play(FadeIn(tulis), FadeIn(baca), run_time=CEPAT)
        for n, detik in enumerate(["06", "07", "08"], start=1):
            jam_baru = mono(f"Sekarang: 13:31:{detik}", color=KUNYIT, size="caption", weight=BOLD).move_to(jam, aligned_edge=LEFT)
            angka = mono(str(n), color=JINGGA, size="h2", weight=BOLD).move_to(tulis[1])
            self.play(Transform(jam, jam_baru), Transform(tulis[1], angka), Indicate(baca[1], color=SAGA), run_time=0.6)
        ket = caption("awal prompt beda tiap detik → nggak pernah cocok").move_to(pos(0, -1.6))
        self.play(FadeIn(ket), run_time=CEPAT)
        self.mark("A_13_jam")
        self.wait(2.0)
        b1 = batang("tanpa cache", 1.0, color=ABU, panjang=5.2, teks_nilai="1×").move_to(pos(0, -2.5))
        b2 = batang("cache cuma ditulis", 1.25, color=SAGA, panjang=5.2, teks_nilai="1,25×").move_to(pos(0, -3.6))
        b1.align_to(b2, LEFT)
        for bb in (b1, b2):
            bb.align_to([AMAN["kiri"] + 0.3, 0, 0], LEFT)
        b1[2].stretch_to_fit_width(b1[1].width / 1.25, about_edge=LEFT)
        b1[1].stretch_to_fit_width(b2[1].width, about_edge=LEFT)
        self.play(FadeOut(ket), FadeIn(b1), FadeIn(b2), run_time=CEPAT)
        sumber = caption("nulis cache 1,25× harga · salah satu penyedia").move_to(pos(0, -4.35))
        self.play(FadeIn(sumber), run_time=CEPAT)
        self.mark("A_14_rugi")
        self.wait(JEDA_PANJANG)


# --------------------------------------------------------------------------
# 09 toko sepi
# --------------------------------------------------------------------------
class S09Sepi(KapurScene):
    def construct(self):
        self.header("Toko lagi sepi?", chapter=BAB)
        x0, x1 = AMAN["kiri"] + 0.4, AMAN["kanan"] - 0.2
        y = pos(0, 0.6)[1]
        sumbu = Line([x0, y, 0], [x1, y, 0], color=ABU_GELAP, stroke_width=3 * S)
        menit = 22
        def X(m):
            return x0 + (x1 - x0) * m / menit
        ticks = VGroup()
        for m in (0, 5, 10, 15, 20):
            ticks.add(mono(f"{m}", color=ABU, size="mikro").move_to([X(m), y - 0.35 * S, 0]))
        lm = caption("menit (angka contoh)").next_to(sumbu, DOWN, buff=0.6 * S)
        self.play(Create(sumbu), FadeIn(ticks), FadeIn(lm), run_time=CEPAT)
        datang = [0, 8, 19]
        for i, m in enumerate(datang):
            o = ikon_orang(LANGIT, 0.9).move_to([X(m), y + 0.75 * S, 0])
            hidup = Rectangle(width=X(5) - X(0), height=0.24 * S, stroke_width=0, fill_color=TOSKA,
                              fill_opacity=0.8).move_to([X(m) + (X(5) - X(0)) / 2, y + 0.14 * S, 0])
            self.play(FadeIn(o, shift=DOWN * GESER), run_time=0.35)
            if i > 0:
                hilang = teks("udah hilang", color=SAGA, size="mikro").next_to(o, UP, buff=0.12 * S)
                self.play(FadeIn(hilang), run_time=0.3)
            self.play(GrowFromEdge(hidup, LEFT), run_time=0.5)
            self.play(hidup.animate.set_fill(opacity=0.15), run_time=0.3)
        ket = VGroup(teks("jeda > 5 menit", color=JINGGA, size="body", weight=MEDIUM),
                     teks("cache ditulis lagi, nggak sempat kebaca", color=SAGA, size="caption")).arrange(DOWN, buff=0.15 * S)
        ket.move_to(pos(0, -2.3))
        self.play(FadeIn(ket, shift=UP * GESER), run_time=CEPAT)
        self.mark("A_15_sepi")
        self.wait(1.0)


# --------------------------------------------------------------------------
# 10 tips
# --------------------------------------------------------------------------
class S10Tips(KapurScene):
    def construct(self):
        self.header("Jadi…", chapter=BAB)
        k, jam, rows = kartu_aturan("Sekarang: 13:31:05", "atas")
        k.move_to(pos(0, 3.0))
        self.add(k)
        self.play(FadeIn(k), run_time=CEPAT)
        # jam pindah ke paling bawah
        isi = k[1]
        lain = VGroup(*[r for r in rows if r is not jam])
        bawah = lain[-1].get_bottom()
        self.play(lain.animate.shift(UP * (jam.height + 0.16 * S)),
                  jam.animate.move_to([jam.get_center()[0], bawah[1] + 0.0, 0], aligned_edge=UP).set_color(DAUN),
                  run_time=LAMBAT)
        t1 = teks("jam → taruh di belakang", color=DAUN, size="body", weight=MEDIUM).next_to(k, DOWN, buff=0.35 * S)
        self.play(FadeIn(t1), run_time=CEPAT)
        lap = VGroup(mono("LAPORAN PEMAKAIAN", color=ABU, size="mikro", weight=BOLD),
                     mono("cache write   3.000", color=JINGGA, size="caption"),
                     mono("cache read        0", color=SAGA, size="caption", weight=BOLD)).arrange(DOWN, buff=0.15 * S,
                                                                                           aligned_edge=LEFT)
        kl = kartu(lap, pad=0.3).move_to(pos(0, -1.6))
        self.play(FadeIn(kl, shift=UP * GESER), run_time=CEPAT)
        sorot = SurroundingRectangle(lap[2], color=KUNYIT, buff=0.08 * S, corner_radius=0.06 * S, stroke_width=3 * S)
        t2 = teks("nol terus? cache-mu cuma ditulis", color=TINTA, size="caption").next_to(kl, DOWN, buff=0.3 * S)
        self.play(Create(sorot), FadeIn(t2), run_time=CEPAT)
        self.mark("A_16_tips")
        self.wait(JEDA_PANJANG)
