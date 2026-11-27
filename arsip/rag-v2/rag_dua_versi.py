"""
Video RAG gaya KAPUR, dua versi naskah untuk diuji di sosmed.

  A  RAGKalauKamuBikin : gaya "you could have invented it" (naskah_A_kalau_kamu_bikin.md)
  B  RAGHook           : hook masalah biasa (naskah_B_hook.md)

Memakai design system di ../design-system (theme.py + fonts).

Frame kunci saja (cepat), hasil di preview/<orientasi>/:
    STILLS=1 ORIENT=vertical manim -s -ql rag_dua_versi.py RAGKalauKamuBikin
Video penuh 1080x1920:
    ORIENT=vertical manim -qh rag_dua_versi.py RAGKalauKamuBikin RAGHook
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

# Jeda lebih panjang dari default KAPUR supaya muat narasi 60-70 detik.
JEDA = 1.8
JEDA_PANJANG = 2.9


# ----------------------------------------------------------------------------
# Bagian bersama
# ----------------------------------------------------------------------------
class RAGBase(KapurScene):
    PREFIX = ""

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

    # --- adegan AI ngarang ---
    def ai_ngarang(self, y_ai=1.4):
        person = ikon_orang(LANGIT, 1.1)
        q = gelembung("Jatah cuti tahunan berapa?", LANGIT).next_to(person, RIGHT, buff=SP["s"])
        tanya = VGroup(person, q).move_to(pos(-0.3, y_ai + 2.6))
        ai = ikon_ai(1.5).move_to(pos(-2.3, y_ai))
        jawab = gelembung("20 hari!", TOSKA, size="body").next_to(ai, RIGHT, buff=SP["m"])
        self.play(FadeIn(person), FadeIn(q, shift=LEFT * GESER), run_time=CEPAT + 0.1)
        self.play(FadeIn(ai, scale=0.8), run_time=CEPAT)
        self.play(FadeIn(jawab, shift=UP * GESER), run_time=CEPAT)
        stempel = self.stempel("NGARANG").next_to(jawab, DOWN, buff=SP["s"]).shift(RIGHT * 0.3 * S)
        self.play(FadeIn(stempel, scale=1.6), ai[1].animate.set_stroke(SAGA),
                  ai[3].animate.set_color(SAGA), run_time=CEPAT)
        return VGroup(tanya, ai, jawab, stempel)

    def stempel(self, s):
        t = mono(s, color=SAGA, size="h2", weight=BOLD)
        r = RoundedRectangle(width=t.width + 0.4 * S, height=t.height + 0.3 * S,
                             corner_radius=0.08 * S, stroke_color=SAGA, stroke_width=4 * S,
                             fill_color=HITAM, fill_opacity=0.6)
        t.move_to(r)
        return VGroup(r, t).rotate(0.18)

    # --- komponen RAG ---
    def buat_chunks(self, center, n=9):
        return VGroup(*[
            RoundedRectangle(width=1.15 * S, height=0.58 * S, corner_radius=0.08 * S,
                             fill_color=redup(KATEGORI[i], 0.35), fill_opacity=1,
                             stroke_color=KATEGORI[i], stroke_width=2.5 * S)
            for i in range(n)
        ]).arrange_in_grid(rows=3, cols=3, buff=0.2 * S).move_to(center)

    P = [(-3, 2), (-2.2, -1.8), (2.2, 1.6), (2.8, 2.2), (1.6, 2.4),
         (-1, 0.4), (3.2, -1.5), (-3.2, -0.8), (0.4, -2.3)]
    NEAR = [2, 3, 4]

    def peta_makna(self, chunks, y=0.2, label=None):
        plane = grid_titik(7.4, 5.2).move_to(pos(0.1, y))
        self.play(Create(plane), run_time=KETUK)
        dots = VGroup(*[Dot(plane.c2p(x, yy), radius=0.12 * S, color=KATEGORI[i])
                        for i, (x, yy) in enumerate(self.P)])
        self.play(LaggedStart(*[ReplacementTransform(chunks[i].copy(), dots[i])
                                for i in range(len(self.P))], lag_ratio=LAG),
                  run_time=LAMBAT)
        return plane, dots

    def cari_terdekat(self, plane, dots, chunks, q_source):
        qdot = Star(n=5, outer_radius=0.24 * S, inner_radius=0.1 * S, color=KUNYIT,
                    fill_opacity=1, stroke_width=0).move_to(plane.c2p(2.3, 1.95))
        self.play(ReplacementTransform(q_source.copy(), qdot), run_time=KETUK)
        far = [i for i in range(9) if i not in self.NEAR]
        ring = Circle(radius=1.1 * S, color=KUNYIT, stroke_width=3 * S).move_to(qdot)
        links = VGroup(*[DashedLine(qdot.get_center(), dots[i].get_center(), color=KUNYIT,
                                    stroke_width=2.5 * S) for i in self.NEAR])
        self.play(Create(ring), run_time=CEPAT + 0.2)
        self.play(Create(links), *[dots[i].animate.scale(1.5) for i in self.NEAR],
                  *[dots[i].animate.set_opacity(0.2) for i in far],
                  *[chunks[i].animate.set_opacity(0.2) for i in far], run_time=KETUK)
        return qdot, ring, links

    def kirim_ke_ai(self, chunks, tanya, sisa):
        sel = VGroup(*[chunks[i] for i in self.NEAR])
        far = VGroup(*[chunks[i] for i in range(9) if i not in self.NEAR])
        self.play(FadeOut(sisa), FadeOut(far), run_time=CEPAT)
        ai = ikon_ai(1.7).move_to(pos(1.9, 0.6))
        self.play(FadeIn(ai, scale=0.8),
                  sel.animate.arrange(DOWN, buff=0.18 * S).scale(1.6).move_to(pos(-2.2, 0.6)),
                  tanya.animate.move_to(pos(0, 4.0)), run_time=KETUK)
        a1 = panah(sel.get_right(), ai.get_left(), color=DAUN)
        a2 = panah(tanya[1].get_bottom(), ai.get_top(), color=LANGIT)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=CEPAT + 0.1)
        return ai, VGroup(sel, a1, a2)

    def kartu_jawaban(self):
        return kartu(VGroup(teks("Jatah cuti tahunan: 12 hari", color=TINTA, weight=MEDIUM),
                            mono("sumber: Peraturan Perusahaan, Bab 5", color=ABU, size="mikro")
                            ).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT), aksen=DAUN)

    def penghitung_token(self, akhir=250000, y=0.0, run_time=LAMBAT):
        nilai = ValueTracker(0)

        def angka():
            v = int(nilai.get_value())
            s = f"{v:,}".replace(",", ".")
            warna = JINGGA if v < akhir * 0.4 else SAGA
            return mono(s, color=warna, size="display", weight=BOLD).move_to(pos(0, y))

        num = always_redraw(angka)
        satuan = teks("token per pertanyaan", color=ABU, size="caption").move_to(pos(0, y - 1.0))
        self.add(num)
        self.play(FadeIn(satuan), nilai.animate.set_value(akhir), run_time=run_time,
                  rate_func=rush_into)
        num.clear_updaters()
        return VGroup(num, satuan)


# ----------------------------------------------------------------------------
# A. "Kalau kamu yang bikin..." (you could have invented it)
# ----------------------------------------------------------------------------
class RAGKalauKamuBikin(RAGBase):
    PREFIX = "A_"

    def construct(self):
        np.random.seed(7)
        self.pembuka()
        self.ide_tempel()
        self.ide_potong()
        self.ide_angka()
        self.ide_kirim()
        self.selamat()

    def tapi(self, s="Tapi…"):
        t = judul(s, color=SAGA, size="display").move_to(pos(0, -4.0))
        self.play(FadeIn(t, shift=UP * GESER), run_time=CEPAT)
        return t

    def jadi(self, s):
        self.header(s)

    # 0-7 dtk
    def pembuka(self):
        self.bab("Kalau kamu yang bikin… #1")
        l1 = judul("Kamu mau AI yang bisa", size="h1")
        l2 = judul("jawab soal dokumen", size="h1")
        l3 = judul("kantormu.", color=KUNYIT, size="display")
        g = VGroup(l1, l2, l3).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT)
        g.move_to(pos(0, 2.0)).align_to([AMAN["kiri"], 0, 0], LEFT)
        doc = ikon_dokumen(1.2).move_to(pos(-1.6, -1.6))
        ai = ikon_ai(1.5).move_to(pos(1.6, -1.6))
        tanda = mono("?", color=ABU, size="h1").move_to(pos(0, -1.6))
        self.play(FadeIn(l1, shift=UP * GESER), FadeIn(l2, shift=UP * GESER), run_time=CEPAT + 0.1)
        self.play(Write(l3), FadeIn(doc, shift=UP * GESER), FadeIn(ai, scale=0.8),
                  FadeIn(tanda), run_time=KETUK)
        ul = coret_kapur(l3)
        self.play(Create(ul), run_time=CEPAT)
        self.mark("01_pembuka")
        self.wait(0.6)
        self.play(FadeOut(VGroup(g, ul, doc, ai, tanda), shift=UP * GESER), run_time=CEPAT)

        self.header("Masalahnya…")
        grp = self.ai_ngarang()
        cap = caption("AI nggak pernah baca dokumenmu. Jadi dia nebak.").move_to(pos(0, -2.4))
        self.play(FadeIn(cap), run_time=CEPAT)
        self.mark("02_ngarang")
        self.wait(JEDA)
        self.kosongkan()

    # 7-21 dtk
    def ide_tempel(self):
        self.bab("Ide 1")
        self.header("Gampang: tempel seluruh PDF")
        chat = RoundedRectangle(width=6.6 * S, height=1.1 * S, corner_radius=0.2 * S,
                                fill_color=PERMUKAAN, fill_opacity=1,
                                stroke_color=LANGIT, stroke_width=2.5 * S).move_to(pos(0, 3.2))
        ph = caption("Ketik pesan…").move_to(chat).align_to(chat, LEFT).shift(RIGHT * 0.3 * S)
        docs = VGroup(*[ikon_dokumen(0.42) for _ in range(20)])
        docs.arrange_in_grid(rows=4, cols=5, buff=0.1 * S).move_to(pos(0, 0.4))
        lbl = mono("200 halaman", color=JINGGA).next_to(docs, DOWN, buff=SP["s"])
        self.play(FadeIn(chat), FadeIn(ph), run_time=CEPAT)
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.4) for d in docs], lag_ratio=0.03),
                  FadeIn(lbl), run_time=KETUK)
        besar = chat.copy().stretch_to_fit_height(3.6 * S).move_to(pos(0, 2.0))
        self.play(FadeOut(ph), FadeOut(lbl),
                  docs.animate.scale(0.7).move_to(besar.get_center()),
                  Transform(chat, besar), run_time=KETUK)
        self.mark("03_tempel")
        self.wait(0.6)

        t = self.tapi("Tapi… kepanjangan.")
        self.play(t.animate.move_to(pos(0, -0.6)), chat.animate.set_stroke(SAGA), run_time=CEPAT)
        cnt = self.penghitung_token(250000, y=-1.9, run_time=KETUK + 0.4)
        akibat = VGroup(pil("boros", SAGA), pil("lambat", SAGA), pil("gagal fokus", SAGA)
                        ).arrange(RIGHT, buff=0.3 * S).move_to(pos(0, -3.9))
        self.play(LaggedStart(*[FadeIn(x, shift=UP * GESER) for x in akibat], lag_ratio=0.25),
                  run_time=KETUK)
        self.mark("04_kepanjangan")
        self.wait(JEDA)
        self.kosongkan()

    # 21-35 dtk
    def ide_potong(self):
        self.bab("Ide 2")
        self.jadi("Jadi… potong kecil-kecil")
        big = ikon_dokumen(2.2).move_to(pos(0, 1.6))
        self.play(FadeIn(big, scale=0.85), run_time=CEPAT + 0.1)
        chunks = self.buat_chunks(pos(0, 1.6))
        self.play(ReplacementTransform(big, chunks), run_time=KETUK)
        tag = pil("chunk", DAUN).next_to(chunks, DOWN, buff=SP["l"])
        self.play(FadeIn(tag, shift=UP * GESER), run_time=CEPAT)
        self.mark("05_potong")
        self.wait(JEDA)

        t = self.tapi("Tapi… kirim yang mana?")
        tujuan = [pos(np.random.uniform(-3.2, 3.0), np.random.uniform(-1.6, 4.4)) for _ in chunks]
        self.play(FadeOut(tag),
                  *[c.animate.move_to(p).rotate(np.random.uniform(-0.5, 0.5))
                    for c, p in zip(chunks, tujuan)], run_time=KETUK)
        qs = VGroup(*[mono("?", color=SAGA, size="h2", weight=BOLD).next_to(c, UP, buff=0.05)
                      for c in chunks[::3]])
        self.play(LaggedStart(*[FadeIn(q, scale=1.5) for q in qs], lag_ratio=0.15),
                  run_time=CEPAT + 0.2)
        self.mark("06_yang_mana")
        self.wait(JEDA)
        self.play(FadeOut(t), FadeOut(qs), run_time=CEPAT)
        self.chunks = chunks

    # 35-52 dtk
    def ide_angka(self):
        self.bab("Ide 3")
        self.jadi("Jadi… ubah jadi angka")
        chunks = self.chunks
        rapi = self.buat_chunks(pos(-2.4, 4.1)).scale(0.55)
        self.play(*[Transform(chunks[i], rapi[i]) for i in range(9)], run_time=KETUK)
        vec = mono("[0.12, -0.83, 0.47, …]", color=JINGGA).move_to(pos(1.3, 4.1))
        self.play(FadeIn(vec), run_time=CEPAT)
        plane, dots = self.peta_makna(chunks)
        note = caption("makna mirip = posisinya berdekatan").next_to(plane, DOWN, buff=SP["m"])
        tag = pil("embedding", DAUN).next_to(note, DOWN, buff=SP["m"])
        self.play(FadeIn(note), FadeIn(tag, shift=UP * GESER), run_time=CEPAT)
        self.mark("07_embedding")
        self.wait(JEDA)

        self.header("Pertanyaanmu juga jadi angka")
        self.play(FadeOut(vec), FadeOut(note), FadeOut(tag), run_time=0.3)
        person = ikon_orang(LANGIT, 1.1)
        q = gelembung("Jatah cuti tahunan berapa?", LANGIT).next_to(person, RIGHT, buff=SP["s"])
        tanya = VGroup(person, q).move_to(pos(0, -3.3))
        self.play(FadeIn(person), FadeIn(q, shift=LEFT * GESER), run_time=CEPAT + 0.1)
        qdot, ring, links = self.cari_terdekat(plane, dots, chunks, q[1])
        top = mono("ambil 3 terdekat", color=KUNYIT).next_to(ring, DOWN, buff=SP["xs"])
        tag2 = pil("retrieval", DAUN).move_to(pos(0, -4.4))
        self.play(FadeIn(top), FadeIn(tag2, shift=UP * GESER), run_time=CEPAT)
        self.mark("08_retrieval")
        self.wait(JEDA)
        self.sisa = VGroup(plane, dots, ring, links, top, qdot, tag2)
        self.tanya = tanya

    # 52-60 dtk
    def ide_kirim(self):
        self.bab("Terakhir")
        self.header("Tempel ke pertanyaan, kirim")
        ai, kabel = self.kirim_ke_ai(self.chunks, self.tanya, self.sisa)
        ans = self.kartu_jawaban().move_to(pos(0, -2.3))
        a3 = panah(ai.get_bottom(), ans.get_top(), color=DAUN)
        self.play(GrowArrow(a3), FadeIn(ans, shift=DOWN * GESER), Indicate(ai, color=TOSKA),
                  run_time=KETUK)
        cap = caption("Sekarang dia jawab pakai contekan yang benar.").next_to(ans, DOWN, buff=SP["m"])
        self.play(FadeIn(cap), run_time=CEPAT)
        self.mark("09_jawaban")
        self.wait(JEDA_PANJANG)
        self.kosongkan()

    # 60-70 dtk
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
        self.mark("10_selamat")
        self.wait(JEDA_PANJANG)

        t1 = teks("Tapi kenapa token bisa semahal itu?", color=TINTA, size="body").move_to(pos(0, -3.0))
        t2 = pil("#2  Tokenizer", JINGGA, size="body").next_to(t1, DOWN, buff=SP["m"])
        self.play(FadeIn(t1, shift=UP * GESER), run_time=CEPAT + 0.1)
        self.play(FadeIn(t2, scale=0.9), run_time=CEPAT)
        self.mark("11_teaser")
        self.wait(JEDA_PANJANG)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=KETUK)


# ----------------------------------------------------------------------------
# B. Hook biasa: "AI kamu ngarang?"
# ----------------------------------------------------------------------------
class RAGHook(RAGBase):
    PREFIX = "B_"

    def construct(self):
        np.random.seed(7)
        self.hook()
        self.masalah()
        self.analogi()
        self.langkah()
        self.hasil()
        self.tips()

    def langkah_header(self, n, s):
        self.header(s, chapter=f"RAG · langkah {n}/3")

    # 0-6 dtk
    def hook(self):
        self.bab("AI 60 detik · RAG")
        big = judul("AI kamu ngarang?", color=SAGA, size="display").move_to(pos(0, 5.0))
        self.play(Write(big), run_time=CEPAT + 0.2)
        grp = self.ai_ngarang(y_ai=0.4)
        grp.shift(DOWN * 0.4 * S)
        self.mark("01_hook")
        self.wait(0.8)
        self.play(FadeOut(VGroup(big, grp), shift=UP * GESER), run_time=CEPAT)

        rag = judul("RAG", color=DAUN, size="raksasa").move_to(pos(0, 2.6))
        sub = judul("obatnya, cuma 3 langkah", size="h2").next_to(rag, DOWN, buff=SP["m"])
        nums = VGroup(*[lencana(i) for i in (1, 2, 3)]).arrange(RIGHT, buff=0.9 * S)
        nums.next_to(sub, DOWN, buff=SP["xl"])
        self.play(Write(rag), FadeIn(sub, shift=UP * GESER), run_time=KETUK)
        self.play(LaggedStart(*[GrowFromCenter(n) for n in nums], lag_ratio=0.2), run_time=CEPAT + 0.2)
        self.mark("02_rag")
        self.wait(0.6)
        self.play(FadeOut(VGroup(rag, sub, nums)), run_time=CEPAT)

    # 6-13 dtk
    def masalah(self):
        self.header("Kenapa AI ngarang?", chapter="Masalah")
        ai = ikon_ai(2.0).move_to(pos(-1.4, 1.6))
        ilmu = caption("pengetahuan umum\ndari data latihan", color=TOSKA).next_to(ai, DOWN, buff=SP["m"])
        doc = ikon_dokumen(1.1).move_to(pos(2.2, 1.6))
        silang = VGroup(Line(UL, DR), Line(UR, DL)).set_stroke(SAGA, 7 * S).scale(0.55 * S).move_to(doc)
        dlab = caption("dokumen kantormu", color=KERTAS).next_to(doc, DOWN, buff=SP["m"])
        self.play(FadeIn(ai, scale=0.8), FadeIn(ilmu), run_time=CEPAT + 0.2)
        self.play(FadeIn(doc, shift=LEFT * GESER), FadeIn(dlab), run_time=CEPAT)
        self.play(Create(silang), run_time=CEPAT)
        kes = judul("Jadi dia nebak.", color=SAGA, size="h1").move_to(pos(0, -2.6))
        self.play(FadeIn(kes, shift=UP * GESER), run_time=CEPAT)
        self.mark("03_masalah")
        self.wait(JEDA_PANJANG)
        self.kosongkan()

    # 13-20 dtk
    def analogi(self):
        self.header("Bayangin ujian", chapter="Analogi")
        k1 = kartu(VGroup(teks("Tanpa RAG", color=SAGA, size="h2", weight=MEDIUM),
                          caption("ujian tutup buku: nebak dari ingatan")
                          ).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT),
                   aksen=SAGA, lebar=7.0 * S).move_to(pos(0, 2.6))
        k2 = kartu(VGroup(teks("Dengan RAG", color=DAUN, size="h2", weight=MEDIUM),
                          caption("ujian open book: boleh nyontek dulu")
                          ).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT),
                   aksen=DAUN, lebar=7.0 * S).move_to(pos(0, -0.2))
        for k in (k1, k2):
            k[1].align_to(k[0], LEFT).shift(RIGHT * 0.35 * S)
        self.play(FadeIn(k1, shift=UP * GESER), run_time=KETUK)
        self.play(FadeIn(k2, shift=UP * GESER), run_time=KETUK)
        self.play(Circumscribe(k2, color=KUNYIT, buff=0.1 * S), run_time=KETUK)
        self.mark("04_analogi")
        self.wait(JEDA)
        self.kosongkan()

    # 20-46 dtk
    def langkah(self):
        self.langkah_header(1, "Potong dokumen")
        big = ikon_dokumen(2.2).move_to(pos(0, 1.6))
        self.play(FadeIn(big, scale=0.85), run_time=CEPAT + 0.1)
        chunks = self.buat_chunks(pos(0, 1.6))
        self.play(ReplacementTransform(big, chunks), run_time=KETUK)
        cap = caption("jadi bagian-bagian kecil").next_to(chunks, DOWN, buff=SP["l"])
        self.play(FadeIn(cap), run_time=CEPAT)
        self.mark("05_langkah1")
        self.wait(JEDA_PANJANG)

        self.langkah_header(2, "Cari yang maknanya mirip")
        self.play(FadeOut(cap), chunks.animate.scale(0.55).move_to(pos(-2.4, 4.1)), run_time=KETUK)
        plane, dots = self.peta_makna(chunks)
        person = ikon_orang(LANGIT, 1.1)
        q = gelembung("Jatah cuti tahunan berapa?", LANGIT).next_to(person, RIGHT, buff=SP["s"])
        tanya = VGroup(person, q).move_to(pos(0, -3.3))
        self.play(FadeIn(person), FadeIn(q, shift=LEFT * GESER), run_time=CEPAT + 0.1)
        qdot, ring, links = self.cari_terdekat(plane, dots, chunks, q[1])
        note = caption("bukan kata yang sama, tapi maknanya", color=KUNYIT).move_to(pos(0, -4.4))
        self.play(FadeIn(note), run_time=CEPAT)
        self.mark("06_langkah2")
        self.wait(JEDA_PANJANG)

        self.langkah_header(3, "Tempel ke pertanyaan")
        ai, kabel = self.kirim_ke_ai(chunks, tanya, VGroup(plane, dots, ring, links, qdot, note))
        small = pil("3 potongan, bukan 200 halaman", DAUN, size="body").move_to(pos(0, -1.6))
        self.play(FadeIn(small, shift=UP * GESER), Indicate(ai, color=TOSKA), run_time=KETUK)
        self.mark("07_langkah3")
        self.wait(JEDA_PANJANG)
        self.kosongkan()

    # 46-53 dtk
    def hasil(self):
        self.header("Hasilnya", chapter="Sebelum vs sesudah")
        h1 = pil("Tanpa RAG", SAGA, size="body").move_to(pos(0, 3.9))
        salah = gelembung("Jatah cuti: 20 hari!", TOSKA, size="body").next_to(h1, DOWN, buff=SP["m"])
        coret = Line(salah[1].get_left(), salah[1].get_right(), color=SAGA, stroke_width=6 * S)
        h2 = pil("Dengan RAG", DAUN, size="body").move_to(pos(0, 0.3))
        benar = self.kartu_jawaban().next_to(h2, DOWN, buff=SP["m"])
        self.play(FadeIn(h1), FadeIn(salah, shift=UP * GESER), run_time=CEPAT + 0.2)
        self.play(Create(coret), run_time=CEPAT)
        self.play(FadeIn(h2), FadeIn(benar, shift=UP * GESER), run_time=KETUK)
        self.play(Circumscribe(benar, color=KUNYIT, buff=0.1 * S), run_time=KETUK)
        self.mark("08_hasil")
        self.wait(JEDA)
        self.kosongkan()

    # 53-65 dtk
    def tips(self):
        self.header("Tips buat kamu", chapter="Praktis")
        t1 = kartu(VGroup(teks("Nanya soal dokumen?", color=LANGIT, weight=MEDIUM),
                          caption("upload dokumennya ke AI")
                          ).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT),
                   aksen=LANGIT, lebar=7.0 * S).move_to(pos(0, 3.0))
        t2 = kartu(VGroup(teks("Tetap cek sumbernya", color=JINGGA, weight=MEDIUM),
                          caption("RAG mengurangi ngarang,\nbukan menghapus")
                          ).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT),
                   aksen=JINGGA, lebar=7.0 * S).move_to(pos(0, 0.6))
        for k in (t1, t2):
            k[1].align_to(k[0], LEFT).shift(RIGHT * 0.35 * S)
        self.play(FadeIn(t1, shift=UP * GESER), run_time=KETUK)
        self.play(FadeIn(t2, shift=UP * GESER), run_time=KETUK)
        self.mark("09_tips")
        self.wait(JEDA_PANJANG)

        n1 = teks("Part 2: kenapa token bikin AI mahal?", color=TINTA).move_to(pos(0, -2.0))
        n2 = pil("Follow biar nggak ketinggalan", ABU).next_to(n1, DOWN, buff=SP["m"])
        self.play(FadeIn(n1, shift=UP * GESER), run_time=CEPAT + 0.1)
        self.play(FadeIn(n2), run_time=CEPAT)
        self.mark("10_teaser")
        self.wait(JEDA_PANJANG)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=KETUK)
