"""
Video #2 Tokenizer, gaya B (hook biasa), design system KAPUR.

Hook: "Kenapa AI salah hitung huruf R di strawberry?"
Jawaban: AI membaca potongan (token), bukan huruf. Tiap token diganti nomor.

Semua pecahan token di file ini ASLI, hasil js-tiktoken 1.0.21 (26 Nov 2026):
  - o200k_base  = tokenizer GPT-4o (dipakai utama)
  - cl100k_base = tokenizer GPT-4 / GPT-3.5 (pembanding "beda model, beda pecahan")
Lihat data/hasil_tokenizer.txt dan data/cek_token.mjs.

Frame kunci (cepat), hasil di preview/vertical/:
    STILLS=1 ORIENT=vertical manim -s -ql token_hook.py TokenHook
Video penuh 1080x1920:
    ORIENT=vertical manim -qh token_hook.py TokenHook
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

# Jeda lebih panjang dari default KAPUR supaya muat narasi (sama dengan v2-v4).
JEDA = 1.8
JEDA_PANJANG = 2.9

# ---------------------------------------------------------------------------
# Data token asli (o200k_base). Spasi di depan token ditampilkan sebagai jarak.
# ---------------------------------------------------------------------------
TANYA = "Ada berapa huruf r di strawberry?"
TANYA_TOK = ["Ada", " ber", "apa", " hur", "uf", " r", " di", " strawberry", "?"]
TANYA_ID = [139151, 5009, 7063, 21317, 1427, 428, 1320, 101830, 30]
I_STRAW = 7

SENDIRI_4O = ["st", "raw", "berry"]          # o200k_base
SENDIRI_4O_ID = [302, 1618, 19772]
SENDIRI_4 = ["str", "aw", "berry"]           # cl100k_base
SENDIRI_4_ID = [496, 675, 15717]

EJA = list("strawberry")                     # "s t r a w b e r r y" -> 10 token
EJA_ID = [82, 260, 428, 261, 286, 287, 319, 428, 428, 342]

ID_KAL = "Tolong jelaskan cara kerja mesin cuci"
ID_TOK = ["T", "olong", " jel", "askan", " cara", " kerja", " mesin", " c", "uci"]   # 9
EN_KAL = "Please explain how a washing machine works"
EN_TOK = ["Please", " explain", " how", " a", " washing", " machine", " works"]       # 7

# Warna blok token bergantian. Sengaja tidak memakai warna peran (DAUN/SAGA/KUNYIT).
WARNA_TOK = [LANGIT, UNGU, "#E58BB4", "#7FA8F5"]


# ---------------------------------------------------------------------------
# Komponen
# ---------------------------------------------------------------------------
_TINGGI_REF = {}


def blok(s, color=LANGIT, size="body", isi=0.28, stroke=2.0):
    """Satu token: kapsul kotak berisi teks mono. Tinggi seragam per ukuran."""
    tampil = s.strip() if s.strip() else "␣"
    t = mono(tampil, color=TINTA, size=size)
    if size not in _TINGGI_REF:
        _TINGGI_REF[size] = mono("Agy", size=size).height
    h = _TINGGI_REF[size] + 0.32 * S
    r = RoundedRectangle(width=max(t.width + 0.3 * S, 0.5 * S), height=h, corner_radius=0.1 * S,
                         fill_color=redup(color, isi), fill_opacity=1,
                         stroke_color=color, stroke_width=stroke * S)
    t.move_to(r)
    return VGroup(r, t)


def deret_blok(tokens, size="body", warna=None, offset=0):
    warna = warna or WARNA_TOK
    return VGroup(*[blok(s, warna[(i + offset) % len(warna)], size) for i, s in enumerate(tokens)])


def susun(g, lebar=LEBAR_AMAN, buff=0.14, baris=0.3, kiri=True):
    """Tata blok kiri->kanan, pindah baris bila melebihi lebar. Kembalikan g."""
    x, y, h = 0.0, 0.0, 0.0
    rows, cur = [], []
    for m in g:
        w = m.width
        if cur and x + w > lebar:
            rows.append(cur)
            cur, x = [], 0.0
        cur.append(m)
        x += w + buff * S
    rows.append(cur)
    for k, row in enumerate(rows):
        xx = 0.0
        for m in row:
            m.move_to([xx + m.width / 2, -k * (m.height + baris * S), 0])
            xx += m.width + buff * S
    if not kiri:
        for row in rows:
            VGroup(*row).set_x(0)
    return g


def nomor(n, color=JINGGA, size="caption"):
    return mono(f"{n}", color=color, size=size, weight=BOLD)


def kata_warna(s, warna_idx, color=KUNYIT, size="display"):
    """Kata serif besar dengan huruf tertentu diwarnai."""
    t = judul(s, size=size)
    for i in warna_idx:
        t[i].set_color(color)
    return t


def stempel(s, color=SAGA):
    t = mono(s, color=color, size="h2", weight=BOLD)
    r = RoundedRectangle(width=t.width + 0.4 * S, height=t.height + 0.3 * S,
                         corner_radius=0.08 * S, stroke_color=color, stroke_width=4 * S,
                         fill_color=HITAM, fill_opacity=0.6)
    t.move_to(r)
    return VGroup(r, t).rotate(0.18)


def kiri(m, y):
    m.move_to(pos(0, y)).align_to([AMAN["kiri"], 0, 0], LEFT)
    return m


# ---------------------------------------------------------------------------
# Scene
# ---------------------------------------------------------------------------
class TokenHook(KapurScene):
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
        for f in (self.hook, self.klaim, self.potong, self.jadi_nomor, self.beda_model,
                  self.tips, self.biaya, self.teaser):
            t0 = self.renderer.time
            f()
            print(f"[waktu] {f.__name__:12s} {t0:6.1f} -> {self.renderer.time:6.1f}")

    # --- 0-5 dtk: hook -------------------------------------------------------
    def hook(self):
        self.bab("#2 · Tokenizer")
        orang = ikon_orang(LANGIT, 1.1)
        q = gelembung("Ada berapa huruf r di strawberry?", LANGIT, size="caption")
        tanya = VGroup(orang, q).arrange(RIGHT, buff=SP["s"]).move_to(pos(0, 5.0))
        ai = ikon_ai(1.3).move_to(pos(-2.6, 2.9))
        jawab = gelembung("Ada 2.", TOSKA, size="h2").next_to(ai, RIGHT, buff=SP["m"])
        cap = stempel("SALAH").next_to(jawab, RIGHT, buff=SP["s"]).shift(UP * 0.1 * S)

        kata = kata_warna("strawberry", [2, 7, 8], size="raksasa").move_to(pos(0, 0.0))
        angka = VGroup(*[nomor(k + 1, size="h2").next_to(kata[i], DOWN, buff=SP["m"])
                         for k, i in enumerate([2, 7, 8])])
        tiga = judul("Padahal ada 3.", color=DAUN, size="h1").move_to(pos(0, -2.3))

        self.play(FadeIn(orang), FadeIn(q, shift=LEFT * GESER), run_time=CEPAT)
        self.play(FadeIn(ai, scale=0.8), FadeIn(jawab, shift=UP * GESER), run_time=CEPAT)
        self.play(FadeIn(cap, scale=1.4), Write(kata), run_time=KETUK)
        self.play(LaggedStart(*[FadeIn(a, shift=UP * GESER) for a in angka], lag_ratio=0.35),
                  run_time=KETUK)
        jujur = VGroup(mono("kasus viral 2024", color=ABU, size="mikro"),
                       mono("model baru banyak yang sudah benar", color=ABU, size="mikro")
                       ).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
        kiri(jujur, -3.4)
        self.play(FadeIn(tiga, shift=UP * GESER), FadeIn(jujur), run_time=CEPAT)
        self.mark("01_hook")
        self.wait(JEDA + 0.6)
        self.hook_obj = VGroup(tanya, ai, jawab, cap, kata, angka, tiga, jujur)

    # --- 5-9 dtk: klaim kontra-intuitif -------------------------------------
    def klaim(self):
        self.play(FadeOut(self.hook_obj, shift=UP * GESER), run_time=CEPAT)
        l1 = judul("Bukan karena AI bodoh.", color=ABU, size="h1")
        l2 = judul("AI memang", size="display")
        l3 = judul("nggak baca huruf.", color=KUNYIT, size="display")
        g = VGroup(l1, l2, l3).arrange(DOWN, buff=SP["m"], aligned_edge=LEFT)
        kiri(g, 1.6)
        ul = coret_kapur(l3)
        ai = ikon_ai(1.5).move_to(pos(0, -2.4))
        self.play(FadeIn(l1, shift=UP * GESER), run_time=CEPAT)
        self.wait(0.6)
        self.play(FadeIn(l2, shift=UP * GESER), FadeIn(ai, scale=0.8), run_time=CEPAT)
        self.play(Write(l3), run_time=KETUK)
        self.play(Create(ul), run_time=CEPAT)
        self.mark("02_klaim")
        self.wait(JEDA)
        self.play(FadeOut(VGroup(g, ul, ai), shift=UP * GESER), run_time=CEPAT)

    # --- 9-24 dtk: teks dipotong jadi token + analogi suku kata --------------
    def potong(self):
        self.header("Teks dipotong dulu")
        kal = teks(TANYA, color=LANGIT, size="body")
        kiri(kal, 4.4)
        self.play(FadeIn(kal, shift=UP * GESER), run_time=CEPAT)

        # Analogi: suku kata
        an_l = caption("mirip kita baca per suku kata", color=ABU)
        suku = VGroup(*[blok(s, ABU, "body", isi=0.12, stroke=1.5) for s in ["be", "ra", "pa"]]
                      ).arrange(RIGHT, buff=0.12 * S)
        an = VGroup(an_l, suku).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        kiri(an, 2.7)
        self.play(FadeIn(an_l), LaggedStart(*[FadeIn(b, shift=UP * GESER) for b in suku],
                                            lag_ratio=0.3), run_time=KETUK)
        self.mark("03_analogi")
        self.wait(1.6)

        # Pecahan asli tokenizer
        blk = susun(deret_blok(TANYA_TOK), lebar=LEBAR_AMAN - 0.2)
        kiri(blk, 0.0).align_to(pos(0, 0.3), UP)
        lab_tok = pil("token", LANGIT, size="caption")
        lab_tok.next_to(blk, DOWN, buff=SP["m"]).align_to(blk, LEFT)
        jml = mono("9 token", color=JINGGA, size="body", weight=BOLD).next_to(lab_tok, RIGHT, buff=SP["m"])
        alat = VGroup(teks("tokenizer", color=TINTA, size="caption", weight=MEDIUM),
                      mono("pemotong teks", color=ABU, size="mikro")).arrange(RIGHT, buff=SP["s"])
        alat.next_to(blk, UP, buff=SP["m"]).align_to(blk, LEFT)
        self.play(FadeIn(alat), run_time=CEPAT)
        self.play(ReplacementTransform(kal.copy(), blk), run_time=LAMBAT)
        self.play(FadeIn(lab_tok, shift=UP * GESER), FadeIn(jml), run_time=CEPAT)
        self.mark("04_token")
        self.wait(JEDA + 1.0)

        # Batas analogi
        b1 = teks("Bedanya: bukan suku kata beneran.", color=TINTA, size="caption", weight=MEDIUM)
        b2 = caption("Potongan dipilih dari yang paling sering muncul di teks.")
        bat = VGroup(b1, b2).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
        kiri(bat, -3.4)
        # sorot ber|apa vs be|ra|pa
        sor = SurroundingRectangle(VGroup(blk[1], blk[2]), color=KUNYIT, buff=0.08 * S,
                                   corner_radius=0.1 * S, stroke_width=3 * S)
        self.play(FadeIn(bat, shift=UP * GESER), Create(sor), run_time=KETUK)
        self.mark("05_batas")
        self.wait(JEDA + 1.6)

        # strawberry utuh
        self.play(FadeOut(sor), FadeOut(bat), FadeOut(an), run_time=CEPAT)
        sor2 = SurroundingRectangle(blk[I_STRAW], color=KUNYIT, buff=0.08 * S,
                                    corner_radius=0.1 * S, stroke_width=4 * S)
        utuh = teks("strawberry = 1 token utuh", color=TINTA, size="body", weight=MEDIUM)
        kiri(utuh, -3.2)
        self.play(Create(sor2), FadeIn(utuh, shift=UP * GESER), run_time=KETUK)
        self.mark("06_utuh")
        self.wait(JEDA)
        self.st = dict(kal=kal, blk=blk, lab_tok=lab_tok, jml=jml, alat=alat, sor2=sor2, utuh=utuh)

    # --- 24-33 dtk: tiap token jadi nomor ------------------------------------
    def jadi_nomor(self):
        st = self.st
        blk = st["blk"]
        self.play(FadeOut(st["utuh"]), FadeOut(st["alat"]), FadeOut(st["kal"]),
                  FadeOut(st["lab_tok"]), FadeOut(st["jml"]), FadeOut(st["sor2"]), run_time=CEPAT)
        self.header("Lalu tiap token jadi nomor")
        self.play(blk.animate.align_to(pos(0, 4.6), UP), run_time=CEPAT)

        # Blok nomor: posisi sama urutannya, isi angka (JINGGA), strawberry kuning.
        nb = VGroup(*[blok(str(n), JINGGA, "body", isi=0.14) for n in TANYA_ID])
        nb[I_STRAW][0].set_stroke(KUNYIT, width=4 * S)
        nb[I_STRAW][1].set_color(KUNYIT)
        susun(nb, lebar=LEBAR_AMAN - 0.2)
        kiri(nb, 0).align_to(pos(0, 1.2), UP)
        lab = caption("yang sampai ke AI cuma ini:", color=ABU)
        lab.next_to(nb, UP, buff=SP["m"]).align_to(nb, LEFT)
        self.play(FadeIn(lab), LaggedStart(*[TransformFromCopy(blk[i], nb[i]) for i in range(len(nb))],
                                           lag_ratio=0.1), run_time=LAMBAT)
        self.mark("07_nomor")
        self.wait(1.8)

        q = judul("Huruf r-nya di mana?", color=SAGA, size="h1")
        kiri(q, -2.2)
        sub = caption("AI cuma lihat satu nomor untuk seluruh kata.", color=TINTA)
        sub.next_to(q, DOWN, buff=SP["s"]).align_to(q, LEFT)
        self.play(FadeIn(q, shift=UP * GESER), FadeIn(sub), run_time=CEPAT)
        self.mark("08_huruf_hilang")
        self.wait(JEDA + 1.0)
        self.kosongkan()

    # --- 33-40 dtk: beda model, beda pecahan ---------------------------------
    def beda_model(self):
        self.header("Beda model, beda pecahan")
        sub = caption('kata "strawberry" ditulis sendiri:')
        kiri(sub, 4.6)
        self.play(FadeIn(sub), run_time=CEPAT)

        def baris(nama, tok, ids, y):
            lab = mono(nama, color=TOSKA, size="caption", weight=BOLD)
            b = deret_blok(tok, size="h2").arrange(RIGHT, buff=0.14 * S)
            n = VGroup(*[nomor(x, size="caption").next_to(bb, DOWN, buff=0.1 * S)
                         for x, bb in zip(ids, b)])
            g = VGroup(lab, VGroup(b, n)).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
            return kiri(g, y)

        r1 = baris("GPT-4o", SENDIRI_4O, SENDIRI_4O_ID, 2.9)
        r2 = baris("GPT-4", SENDIRI_4, SENDIRI_4_ID, 0.2)
        self.play(FadeIn(r1, shift=UP * GESER), run_time=KETUK)
        self.play(FadeIn(r2, shift=UP * GESER), run_time=KETUK)
        cat = VGroup(teks("Tetap potongan, bukan huruf.", color=TINTA, size="caption", weight=MEDIUM),
                     mono("tokenizer: o200k_base (GPT-4o)", color=ABU, size="mikro"),
                     mono("           cl100k_base (GPT-4)", color=ABU, size="mikro")
                     ).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
        cat[1].shift(DOWN * 0.0)
        kiri(cat, -2.6)
        self.play(FadeIn(cat, shift=UP * GESER), run_time=CEPAT)
        self.mark("09_beda_model")
        self.wait(JEDA + 1.2)
        self.kosongkan()

    # --- 40-52 dtk: tips -----------------------------------------------------
    def tips(self):
        self.header("Tips: pisah hurufnya", color=DAUN)
        orang = ikon_orang(LANGIT, 1.0)
        q = gelembung("Hitung huruf r di: s t r a w b e r r y", LANGIT, size="caption")
        g = VGroup(orang, q).arrange(RIGHT, buff=SP["s"])
        kiri(g, 4.4)
        self.play(FadeIn(orang), FadeIn(q, shift=LEFT * GESER), run_time=CEPAT + 0.1)

        b = deret_blok(EJA, size="h2", warna=[ABU_GELAP]).arrange(RIGHT, buff=0.1 * S)
        if b.width > LEBAR_AMAN:
            b.scale_to_fit_width(LEBAR_AMAN)
        kiri(b, 2.0)
        for i in (2, 7, 8):
            b[i][0].set_stroke(KUNYIT, width=3.5 * S).set_fill(redup(KUNYIT, 0.25), 1)
        n = VGroup(*[nomor(x, size="mikro").next_to(bb, DOWN, buff=0.1 * S) for x, bb in zip(EJA_ID, b)])
        self.play(LaggedStart(*[FadeIn(x, shift=UP * GESER) for x in b], lag_ratio=0.08),
                  run_time=KETUK)
        self.play(FadeIn(n), run_time=CEPAT)
        l1 = VGroup(mono("10 token", color=JINGGA, size="body", weight=BOLD),
                    teks("satu huruf, satu token", color=TINTA, size="caption")
                    ).arrange(RIGHT, buff=SP["m"])
        kiri(l1, 0.3)
        self.play(FadeIn(l1, shift=UP * GESER), run_time=CEPAT)
        self.mark("10_tips")
        self.wait(0.8)

        ai = ikon_ai(1.2).move_to(pos(-2.7, -1.9))
        jw = gelembung("Ada 3.", TOSKA, size="h2").next_to(ai, RIGHT, buff=SP["m"])
        cat = caption("tiga r kelihatan, AI jauh lebih gampang ngitung", color=DAUN)
        kiri(cat, -3.6)
        self.play(FadeIn(ai, scale=0.8), FadeIn(jw, shift=UP * GESER), run_time=CEPAT)
        self.play(FadeIn(cat), run_time=CEPAT)
        self.mark("11_tips_hasil")
        self.wait(JEDA + 0.8)
        self.kosongkan()

    # --- 52-63 dtk: token = yang dihitung & dibayar --------------------------
    def biaya(self):
        self.header("Token juga yang dibayar")
        sub = caption("harga AI & batas panjang chat dihitung per token")
        kiri(sub, 4.7)
        self.play(FadeIn(sub), run_time=CEPAT)

        def baris(judul_s, kal, tok, n, y, color):
            lab = teks(judul_s, color=ABU, size="caption", weight=MEDIUM)
            k = teks(f"“{kal}”", color=TINTA, size="caption")
            b = susun(deret_blok(tok, size="caption"), lebar=LEBAR_AMAN - 0.1, buff=0.1, baris=0.18)
            jm = mono(f"{n} token", color=JINGGA, size="body", weight=BOLD)
            g = VGroup(VGroup(lab, jm).arrange(RIGHT, buff=SP["m"]), k, b
                       ).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
            return kiri(g, y)

        r1 = baris("Indonesia", ID_KAL, ID_TOK, 9, 2.7, SAGA)
        r2 = baris("Inggris", EN_KAL, EN_TOK, 7, -0.1, DAUN)
        self.play(FadeIn(r1, shift=UP * GESER), run_time=KETUK)
        self.play(FadeIn(r2, shift=UP * GESER), run_time=KETUK)
        self.mark("12_biaya")
        self.wait(1.8)
        t = judul("Makin banyak token, makin mahal.", color=SAGA, size="h2")
        kiri(t, -2.5)
        cat = VGroup(mono("contoh 1 kalimat · tokenizer GPT-4o", color=ABU, size="mikro"),
                     mono("selisihnya beda tiap kalimat & model", color=ABU, size="mikro")
                     ).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
        kiri(cat, -3.4)
        self.play(FadeIn(t, shift=UP * GESER), FadeIn(cat), run_time=CEPAT + 0.1)
        self.mark("13_mahal")
        self.wait(JEDA + 0.8)
        self.kosongkan()

    # --- 63-70 dtk: teaser ---------------------------------------------------
    def teaser(self):
        l1 = judul("Tapi kalau AI cuma", size="h1")
        l2 = judul("lihat nomor…", size="h1")
        l3 = judul("gimana dia tahu dua kalimat", color=ABU, size="h2")
        l4 = judul("artinya mirip?", color=KUNYIT, size="display")
        g = VGroup(VGroup(l1, l2).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT),
                   VGroup(l3, l4).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
                   ).arrange(DOWN, buff=SP["l"], aligned_edge=LEFT)
        kiri(g, 2.4)
        p = pil("#3  Embedding", JINGGA, size="body")
        kiri(p, -1.2)
        self.play(FadeIn(VGroup(l1, l2), shift=UP * GESER), run_time=CEPAT + 0.1)
        self.play(FadeIn(l3, shift=UP * GESER), Write(l4), run_time=KETUK)
        self.play(FadeIn(p, scale=0.9), run_time=CEPAT)
        self.mark("14_teaser")
        self.wait(JEDA_PANJANG + 1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=KETUK)
