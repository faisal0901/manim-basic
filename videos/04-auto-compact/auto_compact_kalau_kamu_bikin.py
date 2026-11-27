"""
Video auto compact, gaya A "Kalau kamu yang bikin…", design system KAPUR.

Kasus: lanjutan skripsi dari "Kok AI lupa?" (survei 120 responden, teori TAM).
Rantai: AI lupa -> baca ulang semua, ada batas (token, context window) -> jadi ringkas
sebelum penuh -> tapi peringkas butuh instruksi (system prompt) -> TRUST -> KEEP/DROP
-> NEVER STORE + MERGE -> FORMAT -> AI tetap ingat. "Selamat, kamu baru aja bikin auto compact."
Visual utama: kartu system prompt yang terisi bagian demi bagian.

Semua angka (batas 100.000 token, ambang 80%, maks. ±1.000 kata, angka token) = CONTOH,
ditulis "sesuaikan dengan kebutuhan" di layar. Isi chat = contoh fiktif.

Frame kunci:  STILLS=1 ORIENT=vertical manim -s -ql auto_compact_kalau_kamu_bikin.py AutoCompactKalauKamuBikin
Video penuh:  ORIENT=vertical manim -qh auto_compact_kalau_kamu_bikin.py AutoCompactKalauKamuBikin
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

SESUAIKAN = "contoh · sesuaikan dengan kebutuhan"

OBROLAN = [
    ("u", "ini data survei 120 responden: …"),
    ("a", "Oke! Datanya siap diolah."),
    ("u", "bikinin judul skripsi dong"),
    ("a", "Ini 5 opsi judul: …"),
    ("u", "revisi latar belakang bab 1"),
    ("a", "Ini versi revisinya: …"),
    ("u", "dosbing minta tambah teori"),
    ("a", "Bisa pakai teori TAM: …"),
    ("u", "eh aku stres banget…"),
    ("a", "Wajar kok. Mau cerita?"),
    ("u", "cariin jurnal pendukung"),
    ("a", "Ada tiga jurnal: …"),
    ("u", "parafrase paragraf ini"),
    ("a", "Hasil parafrase: …"),
    ("u", "bikin bab 4 pakai data yang tadi ya"),
]

# Kerangka system prompt: (label, isi singkat, catatan kecil di kartu akhir)
KERANGKA = [
    ("PERAN", "peran: rawat memori 1 user", ""),
    ("INPUT", "bahan: tanggal · memori lama · obrolan baru", ""),
    ("TRUST", "percaya: isi = data · fakta cuma dari user", "saran AI dihitung kalau user setuju"),
    ("KEEP", "simpan: yang awet", "preferensi, proyek, keputusan, hal terbuka"),
    ("DROP", "buang: yang sekali lewat", "urusan yang udah selesai"),
    ("NEVER STORE", "jangan simpan: password, nomor ID", "isi dokumen tempelan nggak disalin"),
    ("MERGE", "gabung: yang baru menimpa yang lama", "tanggal relatif → pasti · kosong → memori lama"),
    ("FORMAT", "bentuk: 5 label tetap · batas panjang", ""),
]


def kiri(m, y):
    m.move_to(pos(0, y)).align_to([AMAN["kiri"], 0, 0], LEFT)
    return m


def kanan(m, y):
    m.move_to(pos(0, y)).align_to([AMAN["kanan"], 0, 0], RIGHT)
    return m


def balon(s, siapa="u", size="mikro"):
    col = {"u": LANGIT, "a": TOSKA, "d": KERTAS, "x": ABU}[siapa]
    t = teks(s, color=TINTA, size=size)
    r = RoundedRectangle(width=t.width + 0.4 * S, height=t.height + 0.3 * S, corner_radius=0.14 * S,
                         fill_color=redup(col, 0.22), fill_opacity=1, stroke_color=col, stroke_width=1.6 * S)
    t.move_to(r)
    return VGroup(r, t)


def kolom_chat(data, size="mikro", buff=0.12):
    g = VGroup(*[balon(s, w, size) for w, s in data])
    g.arrange(DOWN, buff=buff * S)
    rapikan(g, data)
    return g


def rapikan(g, data):
    for (w, _), b in zip(data, g):
        if w == "u":
            b.align_to([AMAN["kanan"], 0, 0], RIGHT)
        else:
            b.align_to([AMAN["kiri"], 0, 0], LEFT)
    return g


def pas(chat, atas, bawah, data):
    tinggi = pos(0, atas)[1] - pos(0, bawah)[1]
    if chat.height > tinggi:
        chat.scale(tinggi / chat.height)
    chat.align_to(pos(0, atas), UP)
    return rapikan(chat, data)


def fmt(n):
    return f"{int(round(n)):,}".replace(",", ".")


def gembok(u=0.5, color=SAGA):
    badan = RoundedRectangle(width=u, height=u * 0.8, corner_radius=u * 0.12, fill_color=redup(color, 0.25),
                             fill_opacity=1, stroke_color=color, stroke_width=3 * S)
    lengkung = Arc(radius=u * 0.3, start_angle=0, angle=PI, color=color, stroke_width=3 * S)
    lengkung.next_to(badan, UP, buff=0)
    lubang = Dot(radius=u * 0.07, color=color).move_to(badan)
    return VGroup(lengkung, badan, lubang)


class Kerangka(VGroup):
    """Kartu 'system prompt' dengan 8 slot. Slot kosong = garis samar; reveal satu per satu."""

    def __init__(self, atas=5.5, final=False, size="mikro"):
        super().__init__()
        lebar = LEBAR_AMAN
        kol = 2.05 * S
        self.judul = mono("SYSTEM PROMPT · AI peringkas", color=ABU, size="mikro", weight=BOLD)
        self.label, self.isi, self.slot, self.baris = [], [], [], []
        rows = VGroup()
        for lab, isi, cat in KERANGKA:
            l = mono(lab, color=TINTA, size=size, weight=BOLD)
            d = teks(isi, color=TINTA, size=size)
            g = VGroup(l, d)
            d.next_to(l, RIGHT, buff=0).align_to(l, UP)
            d.shift(RIGHT * (kol - l.width))
            if d.get_right()[0] - l.get_left()[0] > lebar - 0.5 * S:
                d.scale((lebar - 0.5 * S - kol) / d.width).align_to(l, UP)
                d.set_x(l.get_left()[0] + kol + d.width / 2)
            if final and cat:
                c = teks(cat, color=ABU, size=16)
                c.next_to(d, DOWN, buff=0.05 * S).align_to(d, LEFT)
                if c.get_right()[0] - l.get_left()[0] > lebar - 0.4 * S:
                    c.scale((lebar - 0.4 * S - kol) / c.width).align_to(d, LEFT)
                g.add(c)
            rows.add(g)
            self.label.append(l)
            self.isi.append(d)
            self.baris.append(g)
        rows.arrange(DOWN, buff=0.17 * S, aligned_edge=LEFT)
        isi_semua = VGroup(self.judul, rows).arrange(DOWN, buff=0.22 * S, aligned_edge=LEFT)
        self.kotak = RoundedRectangle(width=lebar, height=isi_semua.height + 0.5 * S, corner_radius=0.14 * S,
                                      fill_color=PERMUKAAN, fill_opacity=1, stroke_color=ABU_GELAP,
                                      stroke_width=2 * S)
        self.kotak.align_to(pos(0, atas), UP).align_to([AMAN["kiri"], 0, 0], LEFT)
        isi_semua.move_to(self.kotak).align_to(self.kotak, LEFT).shift(RIGHT * 0.25 * S)
        for g in self.baris:
            s = DashedLine(g.get_left(), g.get_left() + RIGHT * (lebar - 0.5 * S), color=ABU_GELAP,
                           stroke_width=1.5 * S, dash_length=0.08 * S).set_y(g.get_y())
            self.slot.append(s)
        self.add(self.kotak, self.judul, *self.slot)


class AutoCompactKalauKamuBikin(KapurScene):
    PREFIX = "A_"

    def mark(self, nama):
        if not os.environ.get("STILLS"):
            return
        out = _DIR / "preview" / ORIENT
        out.mkdir(parents=True, exist_ok=True)
        self.renderer.update_frame(self, ignore_skipping=True)
        self.renderer.camera.get_image().save(out / f"{self.PREFIX}{nama}.png")

    def construct(self):
        for f in (self.hook, self.batas, self.ringkas, self.prompt, self.trust, self.keep_drop,
                  self.never_merge, self.format, self.ingat, self.selamat):
            t0 = self.renderer.time
            f()
            print(f"[waktu] {f.__name__:12s} {t0:6.1f} -> {self.renderer.time:6.1f}")

    # --- util ----------------------------------------------------------------
    def kosongkan(self, *sisakan):
        keep = {id(self._bab)} | {id(m) for m in sisakan}
        objs = [m for m in self.mobjects if id(m) not in keep]
        if objs:
            self.play(*[FadeOut(m) for m in objs], run_time=CEPAT)
        self._hdr = None

    def pindai(self, chat, tok, total, per=0.3):
        lebar = LEBAR_AMAN + 0.2 * S
        x0 = (AMAN["kiri"] + AMAN["kanan"]) / 2
        y_top = chat[0].get_top()[1] + 0.06 * S
        garis = Line([x0 - lebar / 2, y_top, 0], [x0 + lebar / 2, y_top, 0], color=KUNYIT, stroke_width=4 * S)
        sapu = always_redraw(lambda: Rectangle(
            width=lebar, height=max(0.001, y_top - garis.get_y()), stroke_width=0,
            fill_color=KUNYIT, fill_opacity=0.07).move_to([x0, (y_top + garis.get_y()) / 2, 0]))
        self.add(sapu)
        self.play(FadeIn(garis), run_time=0.2)
        awal = tok.get_value()
        n = len(chat)
        for k, b in enumerate(chat):
            self.play(garis.animate.set_y(b.get_bottom()[1] - 0.06 * S),
                      tok.animate.set_value(awal + (total - awal) * (k + 1) / n),
                      run_time=per, rate_func=linear)
            b.set_opacity(0.55)
        self.play(FadeOut(garis), FadeOut(sapu), run_time=0.25)
        self.remove(sapu)

    def penghitung(self, y, label="AI baca:", akhiran="token"):
        tok = ValueTracker(0)
        lab = mono(label, color=ABU, size="caption")
        kiri(lab, y)
        ctr = always_redraw(lambda: VGroup(mono(fmt(tok.get_value()), color=JINGGA, size="h2", weight=BOLD),
                                           mono(akhiran, color=ABU, size="caption")
                                           ).arrange(RIGHT, buff=SP["s"], aligned_edge=DOWN)
                            .next_to(lab, RIGHT, buff=SP["s"]))
        return tok, lab, ctr

    def buka_baris(self, kr, idx, sorot=True):
        """Tampilkan baris idx di kartu (label + isi), baris aktif sebelumnya jadi ABU."""
        anims = []
        for i in getattr(self, "_aktif", []):
            anims += [kr.label[i].animate.set_color(ABU), kr.isi[i].animate.set_color(ABU)]
        for i in idx:
            anims += [kr.slot[i].animate.set_opacity(0), FadeIn(kr.baris[i], shift=RIGHT * GESER)]
        grup = VGroup(*[kr.baris[i] for i in idx])
        if sorot:
            box = SurroundingRectangle(grup, color=KUNYIT, buff=0.07 * S, corner_radius=0.08 * S, stroke_width=2.5 * S)
            if getattr(self, "_sorot", None) is not None and self._sorot in self.mobjects:
                anims.append(ReplacementTransform(self._sorot, box))
            else:
                anims.append(Create(box))
            self._sorot = box
        self.play(*anims, run_time=CEPAT + 0.2)
        self._aktif = list(idx)

    def vonis(self, item, s, color, redupkan=False):
        tag = pil(s, color, size="mikro")
        tag.next_to(item, RIGHT, buff=SP["s"])
        if tag.get_right()[0] > AMAN["kanan"]:
            tag.align_to([AMAN["kanan"], 0, 0], RIGHT)
        anims = [FadeIn(tag, shift=LEFT * GESER)]
        if redupkan:
            anims.append(item.animate.set_opacity(0.35))
        return tag, anims

    # 1 hook -----------------------------------------------------------------
    def hook(self):
        nb = label_bab("Kalau kamu yang bikin · auto compact")
        self.play(FadeIn(nb), run_time=CEPAT)
        self._bab = nb
        chat = kolom_chat(OBROLAN)
        chat.align_to(pos(0, 4.6), UP)
        self.play(FadeIn(chat[0], shift=UP * GESER), run_time=0.4)
        sor = SurroundingRectangle(chat[0], color=KUNYIT, buff=0.06 * S, corner_radius=0.12 * S, stroke_width=3 * S)
        self.play(Create(sor), run_time=0.3)
        self.add(chat[1:])
        topeng = Rectangle(width=config.frame_width + 1, height=4, stroke_width=0, fill_color=BLACK,
                           fill_opacity=1).align_to(pos(0, 5.95), DOWN)
        topeng.set_z_index(5)
        nb.set_z_index(6)
        self.add(topeng)
        geser = chat.get_bottom()[1] - pos(0, -0.4)[1]
        self.play(VGroup(chat, sor).animate.shift(UP * -geser), run_time=0.9, rate_func=rush_into)
        self.remove(sor)
        tanya = balon("Maaf, data yang mana ya?", "a", size="caption")
        tanya.next_to(chat, DOWN, buff=0.2 * S).align_to([AMAN["kiri"], 0, 0], LEFT)
        big = judul("Kok lupa?", color=KUNYIT, size="raksasa")
        kiri(big, -2.6)
        self.play(FadeIn(tanya, shift=UP * GESER), run_time=0.4)
        self.play(Write(big), run_time=0.8)
        self.mark("01_hook")
        self.wait(0.6)
        self.remove(topeng)
        self.kosongkan()

    # 2 batas ----------------------------------------------------------------
    def batas(self):
        self.header("Kalau kamu yang bikin…")
        data = OBROLAN[:8]
        chat = pas(kolom_chat(data), 4.6, 0.9, data)
        tok, clab, ctr = self.penghitung(0.1)
        self.play(FadeIn(chat), FadeIn(clab), run_time=CEPAT)
        self.add(ctr)
        self.pindai(chat, tok, 62000, per=0.22)
        # token = potongan kata kecil
        kata = mono("responden", color=TINTA, size="body")
        kiri(kata, -1.0)
        pot = VGroup(*[pil(p, JINGGA, size="caption") for p in ("res", "pon", "den")]).arrange(RIGHT, buff=0.08 * S)
        pot.next_to(kata, RIGHT, buff=SP["l"])
        ar = panah(kata.get_right(), pot.get_left(), buff=0.12)
        ket = caption("token = potongan kata kecil · ilustrasi")
        ket.next_to(VGroup(kata, pot), DOWN, buff=SP["s"]).align_to(kata, LEFT)
        self.play(FadeIn(kata), run_time=0.3)
        self.play(GrowArrow(ar), LaggedStart(*[FadeIn(p, shift=RIGHT * GESER) for p in pot], lag_ratio=0.25),
                  FadeIn(ket), run_time=KETUK)
        # context window
        bingkai = SurroundingRectangle(chat, color=JINGGA, buff=0.15 * S, corner_radius=0.14 * S, stroke_width=3 * S)
        cw = VGroup(teks("batas bacaan =", color=TINTA, size="body"),
                    teks("context window", color=JINGGA, size="body", weight=BOLD)).arrange(RIGHT, buff=SP["s"])
        kiri(cw, -2.75)
        bl = mono("batas: 100.000 token", color=JINGGA, size="caption", weight=BOLD)
        kiri(bl, -3.45)
        sz = caption(SESUAIKAN)
        kiri(sz, -4.05)
        self.play(Create(bingkai), FadeIn(cw, shift=UP * GESER), run_time=KETUK)
        self.play(FadeIn(bl), FadeIn(sz), run_time=CEPAT)
        self.mark("02_batas")
        self.wait(JEDA)
        self.remove(ctr)
        self.kosongkan()

    # 3 ringkas --------------------------------------------------------------
    def ringkas(self):
        self.header("Gampang: buang yang lama?")
        data = OBROLAN[:10]
        chat = pas(kolom_chat(data), 4.6, 0.3, data)
        self.play(FadeIn(chat), run_time=CEPAT)
        # buang pesan paling lama -> data survei ikut kebuang
        cap = pil("kebuang", SAGA, size="caption").next_to(chat[0], LEFT, buff=SP["s"])
        self.play(chat[0].animate.shift(UP * 0.6 * S + LEFT * 0.3 * S).set_opacity(0.3),
                  chat[1].animate.shift(UP * 0.6 * S).set_opacity(0.3), run_time=KETUK)
        cap.next_to(chat[0], LEFT, buff=SP["s"])
        if cap.get_left()[0] < AMAN["kiri"]:
            cap.align_to([AMAN["kiri"], 0, 0], LEFT)
        t = judul("Tapi… datamu justru di pesan pertama.", color=SAGA, size="h2")
        kiri(t, -0.5)
        self.play(FadeIn(cap), FadeIn(t, shift=UP * GESER), run_time=CEPAT + 0.1)
        self.mark("03_kebuang")
        self.wait(JEDA - 0.4)
        self.play(FadeOut(t), FadeOut(cap), chat[0].animate.shift(DOWN * 0.6 * S + RIGHT * 0.3 * S).set_opacity(1),
                  chat[1].animate.shift(DOWN * 0.6 * S).set_opacity(1), run_time=CEPAT)

        # jadi: ringkas sebelum penuh
        self.header("Jadi: ringkas sebelum penuh")
        panjang = 6.9 * S
        x_kiri = AMAN["kiri"]
        y_m = pos(0, -0.9)[1]
        track = RoundedRectangle(width=panjang, height=0.4 * S, corner_radius=0.2 * S, fill_color=GARIS,
                                 fill_opacity=1, stroke_width=0)
        track.move_to([x_kiri + panjang / 2, y_m, 0])
        isi = ValueTracker(0.55)
        bar = always_redraw(lambda: RoundedRectangle(
            width=max(0.4 * S, panjang * isi.get_value()), height=0.4 * S, corner_radius=0.2 * S,
            fill_color=JINGGA if isi.get_value() < 0.79 else SAGA, fill_opacity=1, stroke_width=0
        ).align_to(track, LEFT).set_y(y_m))
        x80 = x_kiri + panjang * 0.8
        amb = Line([x80, y_m + 0.4 * S, 0], [x80, y_m - 0.4 * S, 0], color=KUNYIT, stroke_width=4 * S)
        amb_l = mono("ambang 80%", color=KUNYIT, size="mikro", weight=BOLD).next_to(amb, UP, buff=0.08 * S)
        lab = caption("context window terisi").next_to(track, UP, buff=0.12 * S).align_to(track, LEFT)
        sz = caption(SESUAIKAN).next_to(track, DOWN, buff=0.15 * S).align_to(track, LEFT)
        self.play(FadeIn(track), FadeIn(lab), FadeIn(amb), FadeIn(amb_l), FadeIn(sz), run_time=CEPAT)
        self.add(bar)
        # pesan terus nambah: chat geser naik, bar naik ke ambang
        baru = kolom_chat(OBROLAN[10:14])
        baru.scale(chat[0].height / baru[0].height)
        baru.arrange(DOWN, buff=0.12 * S * chat[0].height / baru[0].height)
        baru.next_to(chat, DOWN, buff=0.1 * S)
        rapikan(baru, OBROLAN[10:14])
        semua = VGroup(*chat, *baru)
        geser = baru.get_bottom()[1] - chat.get_bottom()[1]
        topeng = Rectangle(width=config.frame_width + 1, height=4, stroke_width=0, fill_color=BLACK,
                           fill_opacity=1).align_to(pos(0, 4.75), DOWN).set_z_index(5)
        self._hdr.set_z_index(6)
        self._bab.set_z_index(6)
        bawah_topeng = Rectangle(width=config.frame_width + 1, height=1.4 * S, stroke_width=0, fill_color=BLACK,
                                 fill_opacity=1).align_to(pos(0, 0.3), UP).set_z_index(4)
        self.add(topeng, bawah_topeng)
        VGroup(lab, track, amb, amb_l, sz).set_z_index(7)
        bar.set_z_index(8)
        amb.set_z_index(9)
        self.add(baru)
        self.play(semua.animate.shift(UP * -geser), isi.animate.set_value(0.8), run_time=1.6, rate_func=linear)
        self.play(Indicate(amb, color=KUNYIT, scale_factor=1.3), run_time=CEPAT)
        # ringkas: tumpukan jadi satu memori
        mem_t = VGroup(mono("MEMORI", color=DAUN, size="mikro", weight=BOLD),
                       teks("skripsi · survei 120 responden · teori TAM", color=TINTA, size="mikro"))
        mem_t.arrange(DOWN, buff=0.08 * S, aligned_edge=LEFT)
        mem = kartu(mem_t, aksen=DAUN, pad=0.22)
        kiri(mem, 4.1)
        self.remove(topeng, bawah_topeng)
        self.play(ReplacementTransform(semua, mem), isi.animate.set_value(0.06), run_time=LAMBAT)
        lanjut = kolom_chat([("u", "lanjut bab 4 ya"), ("a", "Siap!")])
        lanjut.next_to(mem, DOWN, buff=SP["s"])
        rapikan(lanjut, [("u", ""), ("a", "")])
        self.play(FadeIn(lanjut, shift=UP * GESER), run_time=CEPAT)
        an = VGroup(teks("memori gantiin tumpukan chat lama", color=TINTA, size="body"),
                    caption("kayak catatan kuliah: intinya aja")).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
        kiri(an, -2.8)
        tk = mono("80.000 → 1.500 token · angka contoh", color=JINGGA, size="mikro")
        kiri(tk, -3.85)
        self.play(FadeIn(an, shift=UP * GESER), FadeIn(tk), run_time=CEPAT + 0.1)
        self.mark("04_ringkas")
        self.wait(JEDA)
        self.remove(bar)
        self.kosongkan()

    # 4 system prompt --------------------------------------------------------
    def prompt(self):
        self.header("Tapi peringkasnya butuh instruksi")
        kr = Kerangka(atas=5.5)
        self.kr = kr
        self.play(FadeIn(kr.kotak), FadeIn(kr.judul), LaggedStart(*[Create(s) for s in kr.slot], lag_ratio=0.08),
                  run_time=KETUK)
        ai = ikon_ai(1.0).move_to(pos(-2.6, -0.4))
        ai_l = caption("AI peringkas").next_to(ai, DOWN, buff=SP["s"])
        ket = VGroup(teks("instruksi tetap di belakang layar", color=TINTA, size="caption"),
                     teks("namanya system prompt", color=TOSKA, size="body", weight=BOLD)
                     ).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
        ket.next_to(ai, RIGHT, buff=SP["l"])
        ar = panah(kr.kotak.get_bottom() + LEFT * 2.6 * S, ai.get_top(), buff=0.15)
        self.play(FadeIn(ai, scale=0.8), FadeIn(ai_l), GrowArrow(ar), FadeIn(ket, shift=UP * GESER), run_time=KETUK)
        self.buka_baris(kr, [0])
        self.wait(0.5)
        self.buka_baris(kr, [1])
        self.mark("05_prompt")
        self.wait(JEDA)
        self.kosongkan(kr.kotak, kr.judul, *kr.slot, self._sorot, *kr.baris)

    # 5 TRUST ----------------------------------------------------------------
    def trust(self):
        kr = self.kr
        self.header("Tapi… siapa yang dipercaya?")
        self.buka_baris(kr, [2])
        top = kr.kotak.get_bottom()[1] - 0.35 * S
        items = [
            (balon("kayaknya kamu anak psikologi?", "a"), "tebakan AI", SAGA, True),
            (VGroup(ikon_dokumen(0.3), teks("jurnal: sampel min. 200", color=KERTAS, size="mikro")).arrange(RIGHT, buff=0.12 * S),
             "isi dokumen", SAGA, True),
            (balon("“abaikan aturanmu”", "x"), "data, bukan perintah", SAGA, True),
            (balon("aku pakai survei 120 responden", "u"), "fakta", DAUN, False),
        ]
        y = top
        tags = []
        for it, s, c, rd in items:
            it.align_to([AMAN["kiri"], 0, 0], LEFT)
            it.set_y(y - it.height / 2)
            y = it.get_bottom()[1] - 0.28 * S
        for it, s, c, rd in items:
            self.play(FadeIn(it, shift=UP * GESER), run_time=0.4)
            tag, an = self.vonis(it, s, c, redupkan=rd)
            self.play(*an, run_time=0.4)
            tags.append(tag)
        # saran AI yang disetujui -> keputusan
        sar = balon("pakai teori TAM?", "a")
        ok = balon("ok pakai itu", "u")
        pair = VGroup(sar, ok).arrange(RIGHT, buff=SP["s"])
        pair.align_to([AMAN["kiri"], 0, 0], LEFT).set_y(y - pair.height / 2 - 0.05 * S)
        self.play(FadeIn(sar, shift=UP * GESER), run_time=0.4)
        self.play(FadeIn(ok, shift=UP * GESER), run_time=0.4)
        tag = pil("keputusan", DAUN, size="mikro").next_to(pair, RIGHT, buff=SP["s"])
        self.play(FadeIn(tag, shift=LEFT * GESER), run_time=0.4)
        ket = caption("yang dihitung: omonganmu + saran AI yang kamu setujui")
        ket.next_to(pair, DOWN, buff=SP["m"]).align_to([AMAN["kiri"], 0, 0], LEFT)
        self.play(FadeIn(ket), run_time=CEPAT)
        self.mark("06_trust")
        self.wait(JEDA + 1.0)
        self.kosongkan(kr.kotak, kr.judul, *kr.slot, self._sorot, *kr.baris)

    # 6 KEEP / DROP ----------------------------------------------------------
    def keep_drop(self):
        kr = self.kr
        self.header("Tapi… jangan semua disimpan")
        self.buka_baris(kr, [3, 4])
        top = kr.kotak.get_bottom()[1] - 0.3 * S
        lebar = (LEBAR_AMAN - 0.3 * S) / 2
        tinggi = 2.7 * S
        def kolom(nama, sub, c, x):
            r = RoundedRectangle(width=lebar, height=tinggi, corner_radius=0.14 * S, fill_color=redup(c, 0.1),
                                 fill_opacity=1, stroke_color=c, stroke_width=2 * S)
            r.align_to([x, 0, 0], LEFT).set_y(top - 1.0 * S - tinggi / 2)
            h = VGroup(mono(nama, color=c, size="caption", weight=BOLD), caption(sub))
            h.arrange(RIGHT, buff=SP["s"], aligned_edge=DOWN).next_to(r, UP, buff=0.1 * S).align_to(r, LEFT)
            return r, h
        rk, hk = kolom("KEEP", "yang awet", DAUN, AMAN["kiri"])
        rd, hd = kolom("DROP", "sekali lewat", SAGA, AMAN["kiri"] + lebar + 0.3 * S)
        self.play(FadeIn(rk), FadeIn(hk), FadeIn(rd), FadeIn(hd), run_time=CEPAT)
        masuk = [("jawab singkat aja", "u", rk), ("skripsi TAM, 120 responden", "u", rk),
                 ("keputusan: pakai TAM", "u", rk), ("eh aku stres banget…", "u", rd), ("makasih ya", "u", rd)]
        isi = {id(rk): [], id(rd): []}
        antre = pos(0, 0)
        antre[1] = top - 0.45 * S
        for s, w, kol in masuk:
            b = balon(s, w)
            if b.width > lebar - 0.3 * S:
                b.scale_to_fit_width(lebar - 0.3 * S)
            b.move_to([(AMAN["kiri"] + AMAN["kanan"]) / 2, antre[1], 0])
            self.play(FadeIn(b, scale=0.9), run_time=0.3)
            lst = isi[id(kol)]
            tgt_y = kol.get_top()[1] - 0.25 * S - b.height / 2 - len(lst) * (b.height + 0.15 * S)
            self.play(b.animate.move_to([kol.get_center()[0], tgt_y, 0]), run_time=0.45)
            if kol is rd:
                self.play(b.animate.set_opacity(0.35), run_time=0.15)
            lst.append(b)
        self.mark("07_keep_drop")
        self.wait(JEDA + 0.4)
        self.kosongkan(kr.kotak, kr.judul, *kr.slot, self._sorot, *kr.baris)

    # 7 NEVER STORE + MERGE --------------------------------------------------
    def never_merge(self):
        kr = self.kr
        self.header("Password? Jangan pernah.")
        self.buka_baris(kr, [5])
        top = kr.kotak.get_bottom()[1] - 0.35 * S
        g = gembok(0.55)
        p = VGroup(*[pil(s, SAGA, size="caption") for s in ("password", "nomor KTP", "data orang lain")]
                   ).arrange(RIGHT, buff=0.12 * S)
        baris1 = VGroup(g, p).arrange(RIGHT, buff=SP["m"])
        if baris1.width > LEBAR_AMAN:
            baris1.scale_to_fit_width(LEBAR_AMAN)
        baris1.align_to([AMAN["kiri"], 0, 0], LEFT).set_y(top - baris1.height / 2)
        coret = VGroup(*[Line(x.get_left(), x.get_right(), color=SAGA, stroke_width=3 * S) for x in p])
        self.play(FadeIn(g, scale=0.8), LaggedStart(*[FadeIn(x) for x in p], lag_ratio=0.2), run_time=CEPAT + 0.2)
        self.play(Create(coret), p.animate.set_opacity(0.5), run_time=CEPAT)
        self.wait(0.3)
        # MERGE
        self.header("Judul ganti? Timpa, jangan tumpuk")
        self.buka_baris(kr, [6])
        y2 = baris1.get_bottom()[1] - 0.6 * S
        lama = VGroup(mono("Proyek:", color=ABU, size="caption"), teks("judul A", color=TINTA, size="body"))
        lama.arrange(RIGHT, buff=SP["s"]).align_to([AMAN["kiri"], 0, 0], LEFT).set_y(y2 - 0.3 * S)
        mem = SurroundingRectangle(lama, color=ABU_GELAP, buff=0.2 * S, corner_radius=0.12 * S, stroke_width=2 * S)
        mem.stretch_to_fit_width(LEBAR_AMAN).align_to([AMAN["kiri"], 0, 0], LEFT)
        lama.shift(RIGHT * 0.25 * S)
        pesan = balon("judulnya ganti jadi judul B ya", "u", size="caption")
        kanan(pesan, 0)
        pesan.set_y(mem.get_bottom()[1] - 0.8 * S)
        self.play(FadeIn(mem), FadeIn(lama), run_time=CEPAT)
        self.play(FadeIn(pesan, shift=UP * GESER), run_time=CEPAT)
        baru = teks("judul B", color=DAUN, size="body", weight=BOLD).move_to(lama[1]).align_to(lama[1], LEFT)
        self.play(FadeOut(lama[1], shift=UP * GESER), FadeIn(baru, shift=UP * GESER), run_time=KETUK)
        ket = VGroup(teks("yang baru menimpa yang lama", color=TINTA, size="body"),
                     caption("bukan: judul A + judul B")).arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT)
        ket.next_to(pesan, DOWN, buff=SP["m"]).align_to([AMAN["kiri"], 0, 0], LEFT)
        self.play(FadeIn(ket), run_time=CEPAT)
        self.mark("08_never_merge")
        self.wait(JEDA)
        self.kosongkan(kr.kotak, kr.judul, *kr.slot, self._sorot, *kr.baris)

    # 8 FORMAT ---------------------------------------------------------------
    def format(self):
        kr = self.kr
        self.header("Terakhir: label yang sama")
        self.buka_baris(kr, [7])
        top = kr.kotak.get_bottom()[1] - 0.3 * S
        isi = [("Profil", "mahasiswa, lagi skripsi"),
               ("Preferensi", "jawab singkat, bahasa santai"),
               ("Proyek & topik", "survei 120 responden · TAM · judul B"),
               ("Keputusan", "pakai teori TAM (disetujui)"),
               ("Hal terbuka", "bab 4 belum selesai")]
        rows = VGroup()
        for l, d in isi:
            a = mono(l, color=DAUN, size="mikro", weight=BOLD)
            b = teks(d, color=TINTA, size="mikro")
            r = VGroup(a, b)
            b.next_to(a, RIGHT, buff=0).shift(RIGHT * (2.45 * S - a.width))
            rows.add(r)
        rows.arrange(DOWN, buff=0.16 * S, aligned_edge=LEFT)
        head = mono("MEMORI", color=DAUN, size="mikro", weight=BOLD)
        body = VGroup(head, rows).arrange(DOWN, buff=0.2 * S, aligned_edge=LEFT)
        k = kartu(body, aksen=DAUN, pad=0.25, lebar=LEBAR_AMAN)
        body.align_to(k[0], LEFT).shift(RIGHT * 0.25 * S)
        k.align_to([AMAN["kiri"], 0, 0], LEFT).set_y(top - k.height / 2)
        self.play(FadeIn(k[0]), FadeIn(head), run_time=CEPAT)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * GESER) for r in rows], lag_ratio=0.2), run_time=KETUK + 0.3)
        bp = VGroup(mono("maks. ±1.000 kata", color=JINGGA, size="caption", weight=BOLD), caption(SESUAIKAN))
        bp.arrange(DOWN, buff=SP["xs"], aligned_edge=LEFT).next_to(k, DOWN, buff=SP["m"]).align_to(k, LEFT)
        self.play(FadeIn(bp), run_time=CEPAT)
        self.mark("09_format")
        self.wait(JEDA - 0.3)
        self.kosongkan()

    # 9 ingat ----------------------------------------------------------------
    def ingat(self):
        self.header("Sekarang…", color=DAUN)
        mem_t = VGroup(mono("MEMORI", color=DAUN, size="mikro", weight=BOLD),
                       teks("survei 120 responden · teori TAM · judul B", color=TINTA, size="mikro"))
        mem_t.arrange(DOWN, buff=0.08 * S, aligned_edge=LEFT)
        mem = kartu(mem_t, aksen=DAUN, pad=0.22)
        kiri(mem, 4.2)
        data = [("u", "cek ulang bab 3"), ("a", "Udah, ini catatannya: …"), ("u", "bikin tabel hasil"),
                ("a", "Ini tabelnya: …"), ("u", "pakai data yang tadi ya")]
        chat = kolom_chat(data, size="caption")
        chat.next_to(mem, DOWN, buff=SP["s"])
        rapikan(chat, data)
        self.play(FadeIn(mem), run_time=CEPAT)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * GESER) for b in chat], lag_ratio=0.25), run_time=KETUK + 0.2)
        jaw = balon("Survei 120 responden, teori TAM. Siap!", "a", size="caption")
        jaw[0].set_stroke(DAUN)
        jaw.next_to(chat, DOWN, buff=SP["s"]).align_to([AMAN["kiri"], 0, 0], LEFT)
        self.play(FadeIn(jaw, shift=UP * GESER), run_time=CEPAT)
        t = judul("AI tetap ingat datamu.", color=DAUN, size="h2")
        t.next_to(jaw, DOWN, buff=SP["l"]).align_to([AMAN["kiri"], 0, 0], LEFT)
        self.play(FadeIn(t, shift=UP * GESER), run_time=CEPAT)
        self.mark("10_ingat")
        self.wait(JEDA - 0.2)
        self.kosongkan()

    # 10 selamat -------------------------------------------------------------
    def selamat(self):
        a = judul("Selamat.", size="h1")
        b = judul("Kamu baru aja bikin", color=ABU, size="h2")
        c = judul("auto compact", color=KUNYIT, size="display")
        g = VGroup(a, b, c).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        kiri(g, 5.0)
        self.play(FadeIn(a, shift=UP * GESER), run_time=CEPAT)
        self.play(FadeIn(b, shift=UP * GESER), Write(c), run_time=KETUK)
        alur = VGroup(pil("hampir penuh", JINGGA, size="mikro"), pil("ringkas", TOSKA, size="mikro"),
                      pil("gantikan", DAUN, size="mikro")).arrange(RIGHT, buff=0.45 * S)
        alur.next_to(g, DOWN, buff=SP["m"]).align_to(g, LEFT)
        ars = VGroup(*[panah(alur[i].get_right(), alur[i + 1].get_left(), buff=0.06, tebal=3) for i in range(2)])
        self.play(LaggedStart(*[FadeIn(x) for x in alur], lag_ratio=0.3), Create(ars), run_time=KETUK)
        kr = Kerangka(atas=0.0, final=True)
        for s in kr.slot:
            kr.remove(s)
        semua = VGroup(kr, *kr.baris)
        maks_h = (alur.get_bottom()[1] - 0.35 * S) - (AMAN["bawah"] + 0.75 * S)
        if semua.height > maks_h:
            semua.scale(maks_h / semua.height)
        semua.next_to(alur, DOWN, buff=0.35 * S).align_to([AMAN["kiri"], 0, 0], LEFT)
        for i in range(len(KERANGKA)):
            kr.label[i].set_color(TOSKA)
        self.play(FadeIn(kr.kotak), FadeIn(kr.judul),
                  LaggedStart(*[FadeIn(r) for r in kr.baris], lag_ratio=0.1), run_time=KETUK + 0.3)
        sz = caption("semua angka = contoh · sesuaikan dengan kebutuhan")
        sz.next_to(semua, DOWN, buff=SP["s"]).align_to([AMAN["kiri"], 0, 0], LEFT)
        bt = caption("ringkasan tetap bisa ketinggalan detail")
        bt.next_to(sz, DOWN, buff=SP["xs"]).align_to(sz, LEFT)
        self.play(FadeIn(sz), FadeIn(bt), run_time=CEPAT)
        self.mark("11_selamat")
        self.wait(JEDA_PANJANG)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=KETUK)
