"""
Video "Kenapa AI engineer bikin sistem RAG?" versi design system KAPUR.

Video penuh:
    ORIENT=vertical   manim -qh rag_kapur.py RAGKapur
    ORIENT=horizontal manim -qh rag_kapur.py RAGKapur
Hanya gambar frame kunci (cepat, tanpa video), hasil di preview/<orientasi>/:
    STILLS=1 ORIENT=vertical manim -s -ql rag_kapur.py RAGKapur
"""
import numpy as np

from theme import *

H = not VERTIKAL  # 16:9 memakai layout dua kolom


class RAGKapur(KapurScene):
    def construct(self):
        np.random.seed(7)
        self.hook()
        self.problem()
        self.turning()
        self.rag()
        self.compare()
        self.outro()

    # ---------- 1. HOOK ----------
    def hook(self):
        bab = label_bab("Bab 1 · Konteks")
        self.play(FadeIn(bab), run_time=CEPAT)
        self._bab = bab

        docs = VGroup(*[ikon_dokumen(0.5) for _ in range(28)])
        docs.arrange_in_grid(rows=4, cols=7, buff=0.18 * S).move_to(pos(-4.6, 0.3) if H else pos(0, 2.6))
        for d in docs:
            d.rotate(np.random.uniform(-0.1, 0.1))
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.5, scale=0.7) for d in docs],
                              lag_ratio=0.03), run_time=LAMBAT)
        t1 = judul("Ratusan dokumen,", size="display").move_to(pos(3.6, 2.4) if H else pos(0, 0.0))
        self.play(Write(t1), run_time=KETUK)

        people = VGroup(*[ikon_orang(LANGIT) for _ in range(9)]).arrange(RIGHT, buff=0.24 * S)
        people.move_to(pos(3.6, 0.2) if H else pos(0, -1.5))
        t2 = judul("ratusan karyawan.", color=LANGIT, size="display").move_to(pos(3.6, -2.0) if H else pos(0, -2.8))
        self.play(LaggedStart(*[GrowFromCenter(p) for p in people], lag_ratio=0.06),
                  Write(t2), run_time=KETUK)
        self.mark("01_hook")
        self.wait(JEDA)
        self.hook_docs = docs
        self.play(FadeOut(t1), FadeOut(t2), FadeOut(people), run_time=CEPAT)

    # ---------- 2. MASALAH ----------
    def problem(self):
        self.header("Cara naif: kasih semua ke AI", chapter="Bab 2 · Masalah")
        docs = self.hook_docs
        stack = VGroup(*[ikon_dokumen(0.38) for _ in range(20)])
        stack.arrange_in_grid(rows=5, cols=4, buff=0.08 * S).move_to(pos(-6.6, 1.2) if H else pos(-2.0, 2.6))
        self.play(Transform(docs, stack), run_time=KETUK)
        lbl = mono("500 halaman", color=JINGGA).next_to(docs, DOWN, buff=SP["s"])
        ai = ikon_ai(1.6).move_to(pos(-2.2, 1.2) if H else pos(2.1, 2.6))
        arr = panah(docs.get_right(), ai.get_left(), color=ABU, buff=0.3)
        self.play(FadeIn(lbl), FadeIn(ai, scale=0.8), GrowArrow(arr), run_time=KETUK)

        scan = Rectangle(width=docs.width + 0.2 * S, height=0.08 * S, stroke_width=0,
                         fill_color=KUNYIT, fill_opacity=0.9).move_to(docs.get_top())
        reading = caption("membaca dari A sampai Z…", color=KUNYIT).move_to(pos(-4.4, -4.2) if H else pos(0, 0.25))
        self.add(scan)
        self.play(FadeIn(reading), scan.animate.move_to(docs.get_center()),
                  run_time=KETUK, rate_func=linear)

        cnt_lbl = teks("Pertanyaan ke-", color=TINTA).move_to(pos(4.2, 4.0) if H else pos(-0.5, -0.6))
        num = mono("100", color=SAGA, size="h1", weight=BOLD).next_to(cnt_lbl, RIGHT, buff=SP["s"])
        self.play(FadeIn(cnt_lbl), FadeIn(num), run_time=CEPAT)

        calc1 = teks("500 halaman × 100 pertanyaan", color=TINTA).move_to(pos(4.6, 2.0) if H else pos(0, -1.6))
        calc2 = judul("= 50.000 halaman dibaca", color=SAGA, size="h2").move_to(pos(4.6, 0.3) if H else pos(0, -2.35))
        self.play(Write(calc1), run_time=KETUK)
        self.play(FadeIn(calc2, shift=UP * GESER), run_time=CEPAT)

        b1 = batang("Biaya", 0.95, color=SAGA, panjang=6.2, teks_nilai="MAHAL")
        b2 = batang("Waktu", 0.85, color=SAGA, panjang=6.2, teks_nilai="LAMBAT")
        VGroup(b1, b2).arrange(DOWN, buff=SP["m"], aligned_edge=LEFT).move_to(pos(4.6, -3.0) if H else pos(0, -3.9))
        self.play(FadeIn(b1), FadeIn(b2), ai[1].animate.set_stroke(SAGA),
                  ai[3].animate.set_color(SAGA), run_time=KETUK)
        self.mark("02_masalah")
        self.wait(JEDA)

    # ---------- 3. TITIK BALIK ----------
    def turning(self):
        self.tanpa_header(0.3)
        self.bersihkan(CEPAT)
        nb = label_bab("Bab 3 · Titik balik")
        self.play(FadeTransform(self._bab, nb), run_time=CEPAT)
        self._bab = nb
        q1 = judul("Kenapa baca semuanya", size="display")
        q2 = judul("kalau cuma butuh", size="display")
        q3 = judul("sebagian?", color=KUNYIT, size=96)
        g = VGroup(q1, q2, q3).arrange(DOWN, buff=SP["m"]).move_to(pos(0, 0.6))
        self.play(FadeIn(q1, shift=UP * GESER), run_time=CEPAT + 0.1)
        self.play(FadeIn(q2, shift=UP * GESER), run_time=CEPAT + 0.1)
        self.play(Write(q3), run_time=KETUK)
        ul = coret_kapur(q3)
        self.play(Create(ul), run_time=CEPAT)
        self.mark("03_titik_balik")
        self.wait(JEDA_PANJANG)
        self.play(FadeOut(VGroup(g, ul), shift=UP * GESER), run_time=CEPAT)

    # ---------- 4. RAG ----------
    def step(self, n, s):
        self.header(s, chapter=f"Bab 4 · RAG langkah {n}/6")

    def rag(self):
        nb = label_bab("Bab 4 · Solusi")
        self.play(FadeTransform(self._bab, nb), run_time=CEPAT)
        self._bab = nb
        title = judul("RAG", color=DAUN, size="raksasa").move_to(pos(0, 1.2))
        sub = teks("Retrieval-Augmented Generation", color=ABU).next_to(title, DOWN, buff=SP["m"])
        sub2 = judul("cari dulu, baru jawab", size="h2").next_to(sub, DOWN, buff=SP["l"])
        ul = coret_kapur(sub2, color=DAUN)
        self.play(Write(title), run_time=KETUK)
        self.play(FadeIn(sub, shift=UP * GESER), run_time=CEPAT)
        self.play(FadeIn(sub2), Create(ul), run_time=CEPAT + 0.2)
        self.mark("04_rag_judul")
        self.wait(JEDA)
        self.play(FadeOut(VGroup(title, sub, sub2, ul)), run_time=CEPAT)

        # 1) chunk
        self.step(1, "Potong dokumen jadi chunk")
        big = ikon_dokumen(2.2).move_to(pos(0, 1.6))
        self.play(FadeIn(big, scale=0.85), run_time=CEPAT + 0.1)
        chunks = VGroup(*[
            RoundedRectangle(width=1.15 * S, height=0.58 * S, corner_radius=0.08 * S,
                             fill_color=redup(KATEGORI[i], 0.35), fill_opacity=1,
                             stroke_color=KATEGORI[i], stroke_width=2.5 * S)
            for i in range(9)
        ]).arrange_in_grid(rows=3, cols=3, buff=0.2 * S).move_to(pos(0, 1.6))
        self.play(ReplacementTransform(big, chunks), run_time=KETUK)
        clbl = caption("chunk = potongan kecil teks").next_to(chunks, DOWN, buff=SP["l"])
        self.play(FadeIn(clbl), run_time=CEPAT)
        self.mark("05_langkah1_chunk")
        self.wait(JEDA)

        # 2) vektor
        self.step(2, "Ubah tiap chunk jadi vektor")
        self.play(FadeOut(clbl), chunks.animate.scale(0.55).move_to(pos(-2.4, 4.1)),
                  run_time=KETUK)
        plane = grid_titik(7.4, 5.2).move_to(pos(0.1, 0.2))
        self.play(Create(plane), run_time=KETUK)
        P = [(-3, 2), (-2.2, -1.8), (2.2, 1.6), (2.8, 2.2), (1.6, 2.4),
             (-1, 0.4), (3.2, -1.5), (-3.2, -0.8), (0.4, -2.3)]
        dots = VGroup(*[Dot(plane.c2p(x, y), radius=0.12 * S, color=KATEGORI[i])
                        for i, (x, y) in enumerate(P)])
        vec = mono("[0.12, -0.83, 0.47, …]", color=JINGGA).move_to(pos(1.3, 4.1))
        self.play(FadeIn(vec), run_time=CEPAT)
        self.play(LaggedStart(*[ReplacementTransform(chunks[i].copy(), dots[i])
                                for i in range(9)], lag_ratio=LAG), run_time=LAMBAT)
        note = caption("makna mirip = posisi berdekatan").next_to(plane, DOWN, buff=SP["m"])
        self.play(FadeIn(note), run_time=CEPAT)
        self.mark("06_langkah2_vektor")
        self.wait(JEDA)

        # 3) pertanyaan
        self.step(3, "Pertanyaan juga jadi vektor")
        self.play(FadeOut(vec), FadeOut(note), run_time=0.3)
        person = ikon_orang(LANGIT, 1.1)
        q = gelembung("Jatah cuti tahunan berapa?", LANGIT).next_to(person, RIGHT, buff=SP["s"])
        pq = VGroup(person, q).move_to(pos(0, -3.3))
        self.play(FadeIn(person), FadeIn(q, shift=LEFT * GESER), run_time=CEPAT + 0.1)
        qdot = Star(n=5, outer_radius=0.24 * S, inner_radius=0.1 * S, color=KUNYIT,
                    fill_opacity=1, stroke_width=0).move_to(plane.c2p(2.3, 1.95))
        self.play(ReplacementTransform(q[1].copy(), qdot), run_time=KETUK)
        self.play(Flash(qdot, color=KUNYIT, line_length=0.25 * S), run_time=CEPAT)
        self.mark("07_langkah3_pertanyaan")
        self.wait(CEPAT)

        # 4) terdekat
        self.step(4, "Cari chunk paling dekat")
        near = [2, 3, 4]
        far = [i for i in range(9) if i not in near]
        ring = Circle(radius=1.1 * S, color=KUNYIT, stroke_width=3 * S).move_to(qdot)
        links = VGroup(*[DashedLine(qdot.get_center(), dots[i].get_center(), color=KUNYIT,
                                    stroke_width=2.5 * S) for i in near])
        self.play(Create(ring), run_time=KETUK)
        self.play(Create(links), *[dots[i].animate.scale(1.5) for i in near],
                  *[dots[i].animate.set_opacity(0.2) for i in far],
                  *[chunks[i].animate.set_opacity(0.2) for i in far], run_time=KETUK)
        topk = mono("top-3", color=KUNYIT).next_to(ring, DOWN, buff=SP["xs"])
        self.play(FadeIn(topk), run_time=CEPAT)
        self.mark("08_langkah4_terdekat")
        self.wait(JEDA)

        # 5) ke AI
        self.step(5, "Kirim chunk relevan saja")
        sel = VGroup(*[chunks[i] for i in near])
        others = VGroup(plane, dots, ring, links, topk, qdot, *[chunks[i] for i in far])
        self.play(FadeOut(others), run_time=CEPAT)
        ai = ikon_ai(1.7).move_to(pos(1.9, 0.6))
        self.play(FadeIn(ai, scale=0.8),
                  sel.animate.arrange(DOWN, buff=0.18 * S).scale(1.6).move_to(pos(-2.2, 0.6)),
                  pq.animate.move_to(pos(0, 4.0)), run_time=KETUK)
        a1 = panah(sel.get_right(), ai.get_left(), color=DAUN)
        a2 = panah(q.get_bottom(), ai.get_top(), color=LANGIT)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=CEPAT + 0.1)
        small = pil("3 chunk, bukan 500 halaman", DAUN, size="body").move_to(pos(0, -1.6))
        self.play(FadeIn(small, shift=UP * GESER), Indicate(ai, color=TOSKA), run_time=KETUK)
        self.mark("09_langkah5_ke_ai")
        self.wait(CEPAT)

        # 6) jawaban
        self.step(6, "Jawaban cepat & tepat")
        self.play(FadeOut(small), run_time=0.3)
        ans = kartu(VGroup(teks("Jatah cuti tahunan: 12 hari", color=TINTA, weight=MEDIUM),
                           mono("sumber: Peraturan Perusahaan, Bab 5", color=ABU, size="mikro")
                           ).arrange(DOWN, buff=SP["s"], aligned_edge=LEFT),
                    aksen=DAUN).move_to(pos(0, -2.1))
        a3 = panah(ai.get_bottom(), ans.get_top(), color=DAUN)
        self.play(GrowArrow(a3), FadeIn(ans, shift=DOWN * GESER), run_time=KETUK)
        self.mark("10_langkah6_jawaban")
        self.wait(JEDA_PANJANG)
        self.tanpa_header(0.3)
        self.bersihkan(CEPAT)

    # ---------- 5. SEBELUM / SESUDAH ----------
    def compare(self):
        self.header("Sebelum vs sesudah RAG", chapter="Bab 5 · Perbandingan")
        cx = (-1.95, 1.95)
        h1 = pil("Tanpa RAG", SAGA, size="body").move_to(pos(cx[0], 4.0))
        h2 = pil("Dengan RAG", DAUN, size="body").move_to(pos(cx[1], 4.0))
        self.play(FadeIn(h1), FadeIn(h2), run_time=CEPAT)
        rows = [("Dibaca / pertanyaan", "500 hal.", "3 chunk"),
                ("Token / pertanyaan", "±250.000", "±1.500"),
                ("Waktu jawab", "lambat", "detik"),
                ("Biaya", "mahal", "hemat")]
        if H:  # tabel 3 kolom: nama | tanpa | dengan
            cx = (0.5, 5.5)
            h1.move_to(pos(cx[0], 4.6))
            h2.move_to(pos(cx[1], 4.6))
        y = 2.6 if H else 2.7
        groups = []
        for name, a, b in rows:
            if H:
                n = teks(name, color=ABU).move_to(pos(-4.5, y))
                va = mono(a, color=TINTA, size="h2", weight=BOLD).move_to(pos(cx[0], y))
                vb = mono(b, color=DAUN, size="h2", weight=BOLD).move_to(pos(cx[1], y))
                sep = Line(pos(-8.2, y - 1.05), pos(8.2, y - 1.05), color=GARIS, stroke_width=2)
                y -= 2.1
            else:
                n = caption(name).move_to(pos(0, y))
                va = mono(a, color=TINTA, size="h2", weight=BOLD).move_to(pos(cx[0], y - 0.6))
                vb = mono(b, color=DAUN, size="h2", weight=BOLD).move_to(pos(cx[1], y - 0.6))
                sep = Line(pos(-3.7, y - 1.15), pos(3.7, y - 1.15), color=GARIS, stroke_width=2)
                y -= 1.6
            groups.append(VGroup(n, va, vb, sep))
        self.play(LaggedStart(*[FadeIn(g, shift=UP * GESER) for g in groups], lag_ratio=0.4),
                  run_time=LAMBAT * 2)
        self.play(Circumscribe(groups[1][2], color=KUNYIT, buff=0.12 * S), run_time=KETUK)
        self.mark("11_sebelum_sesudah")
        self.wait(JEDA_PANJANG)
        self.tanpa_header(0.3)
        self.bersihkan(CEPAT)

    # ---------- 6. PENUTUP ----------
    def outro(self):
        nb = label_bab("Bab 6 · Penutup")
        self.play(FadeTransform(self._bab, nb), run_time=CEPAT)
        self._bab = nb
        l1 = judul("Inilah yang dikerjakan", size="h2", color=ABU).move_to(pos(0, 4.6) if H else pos(0, 2.2))
        l2 = judul("AI engineer", color=LANGIT, size="raksasa").next_to(l1, DOWN, buff=SP["m"])
        l3 = judul("membangun sistem RAG", color=DAUN, size="h1").next_to(l2, DOWN, buff=SP["l"])
        ul = coret_kapur(l3, color=DAUN)
        self.play(FadeIn(l1, shift=UP * GESER), run_time=CEPAT + 0.1)
        self.play(Write(l2), run_time=KETUK)
        self.play(FadeIn(l3, shift=UP * GESER), Create(ul), run_time=KETUK)
        cta = pil("Follow untuk part berikutnya", ABU).next_to(l3, DOWN, buff=SP["xl"])
        self.play(FadeIn(cta, shift=UP * GESER), run_time=CEPAT)
        self.mark("12_penutup")
        self.wait(JEDA_PANJANG)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=KETUK)
