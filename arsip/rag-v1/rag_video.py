"""
Video animasi: "Kenapa AI engineer bikin sistem RAG?"
Gaya Manim, teks Bahasa Indonesia (tanpa LaTeX).

Render vertikal 9:16 (TikTok / Reels / Shorts):
    ORIENT=vertical   manim -qh rag_video.py RAGVideo
Render horizontal 16:9 (YouTube):
    ORIENT=horizontal manim -qh rag_video.py RAGVideo
"""
import os
import numpy as np
from manim import *

ORIENT = os.environ.get("ORIENT", "vertical")
VERTICAL = ORIENT == "vertical"

if VERTICAL:
    config.pixel_width, config.pixel_height = 1080, 1920
    config.frame_height = 16.0
    config.frame_width = 9.0
    S = 1.05                       # skala konten
    C = np.array([0, -0.3, 0])     # pusat area konten
    HEADER_Y, HEADER_FS = 5.4, 50
else:
    config.pixel_width, config.pixel_height = 1920, 1080
    config.frame_height = 9.0
    config.frame_width = 16.0
    S = 0.82
    C = np.array([0, -0.4, 0])
    HEADER_Y, HEADER_FS = 3.75, 40

config.background_color = "#0B1120"
FONT = "Inter"

# Palet
DOC_C = "#E2E8F0"
AI_C = "#8B5CF6"
BAD = "#F43F5E"
GOOD = "#22C55E"
ACC = "#38BDF8"
GOLD = "#FACC15"
MUTED = "#94A3B8"


def at(x, y):
    return C + S * np.array([x, y, 0])


def T(s, fs=36, color=WHITE, weight=NORMAL, **kw):
    return Text(s, font=FONT, font_size=fs * S, color=color, weight=weight, **kw)


def doc_icon(w=0.55, color=DOC_C):
    w = w * S
    h = w * 1.3
    body = RoundedRectangle(width=w, height=h, corner_radius=w * 0.12,
                            fill_color=color, fill_opacity=1, stroke_width=0)
    lines = VGroup(*[
        Line(LEFT * w * 0.32, RIGHT * w * (0.32 if i % 3 else 0.1),
             stroke_width=2.2 * S, color="#64748B")
        for i in range(4)
    ]).arrange(DOWN, buff=h * 0.13).move_to(body)
    return VGroup(body, lines)


def person_icon(color=ACC, s=1.0):
    s = s * S
    head = Circle(radius=0.13 * s, fill_color=color, fill_opacity=1, stroke_width=0)
    body = ArcBetweenPoints(LEFT * 0.24 * s, RIGHT * 0.24 * s, angle=-PI)
    body = VGroup(body, Line(LEFT * 0.24 * s, RIGHT * 0.24 * s))
    torso = Sector(radius=0.24 * s, angle=PI, start_angle=0,
                   fill_color=color, fill_opacity=1, stroke_width=0)
    torso.next_to(head, DOWN, buff=0.04 * s)
    return VGroup(head, torso)


def ai_box(size=1.7):
    size = size * S
    box = RoundedRectangle(width=size, height=size, corner_radius=size * 0.18,
                           fill_color=AI_C, fill_opacity=1, stroke_color="#C4B5FD",
                           stroke_width=4 * S)
    label = Text("AI", font=FONT, weight=BOLD, font_size=60 * S * size / (1.7 * S))
    label.move_to(box)
    # "pin" sirkuit kecil di sisi kotak
    pins = VGroup()
    for k in (-0.25, 0, 0.25):
        for d in (LEFT, RIGHT, UP, DOWN):
            p = Line(ORIGIN, d * size * 0.12, stroke_width=3 * S, color="#C4B5FD")
            off = (UP if d[0] != 0 else RIGHT) * k * size
            p.shift(box.get_center() + d * size / 2 + off)
            pins.add(p)
    return VGroup(pins, box, label)


def bubble(s, color=WHITE, fs=26, text_color="#0B1120"):
    t = T(s, fs, color=text_color, weight=MEDIUM)
    r = RoundedRectangle(width=t.width + 0.5 * S, height=t.height + 0.4 * S,
                         corner_radius=0.2 * S, fill_color=color, fill_opacity=1,
                         stroke_width=0)
    t.move_to(r)
    return VGroup(r, t)


class RAGVideo(Scene):
    # ---------- util header ----------
    def header(self, s, color=WHITE, run_time=0.6):
        new = Text(s, font=FONT, font_size=HEADER_FS, weight=BOLD, color=color)
        maxw = config.frame_width - 1.0
        if new.width > maxw:
            new.scale_to_fit_width(maxw)
        new.move_to([0, HEADER_Y, 0])
        if getattr(self, "_hdr", None) is None:
            self.play(FadeIn(new, shift=DOWN * 0.3), run_time=run_time)
        else:
            self.play(FadeOut(self._hdr, shift=UP * 0.3),
                      FadeIn(new, shift=UP * 0.3), run_time=run_time)
        self._hdr = new

    def clear_content(self, run_time=0.6):
        keep = [self._hdr] if getattr(self, "_hdr", None) else []
        objs = [m for m in self.mobjects if m not in keep]
        if objs:
            self.play(*[FadeOut(m) for m in objs], run_time=run_time)

    def construct(self):
        self._hdr = None
        self.hook()          # 0  - 5 dtk
        self.problem()       # 5  - 25 dtk
        self.turning()       # 25 - 30 dtk
        self.rag()           # 30 - 70 dtk
        self.outro()         # 70 - 85 dtk

    # ---------- 1. HOOK ----------
    def hook(self):
        docs = VGroup(*[doc_icon(0.55) for _ in range(28)])
        docs.arrange_in_grid(rows=4, cols=7, buff=0.16 * S).move_to(at(0, 1.4))
        for d in docs:
            d.rotate(np.random.uniform(-0.12, 0.12))
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.6, scale=0.6) for d in docs],
                              lag_ratio=0.04), run_time=1.4)
        t1 = T("Ratusan dokumen,", 50, weight=BOLD).move_to(at(0, -1.1))
        self.play(Write(t1), run_time=0.7)

        people = VGroup(*[person_icon(ACC) for _ in range(9)]).arrange(RIGHT, buff=0.22 * S)
        people.move_to(at(0, -2.4))
        t2 = T("ratusan karyawan.", 50, weight=BOLD, color=ACC).move_to(at(0, -3.4))
        self.play(LaggedStart(*[GrowFromCenter(p) for p in people], lag_ratio=0.06),
                  Write(t2), run_time=1.1)
        self.wait(1.3)
        self.hook_docs, self.hook_people = docs, people
        self.play(FadeOut(t1), FadeOut(t2), FadeOut(people), run_time=0.5)

    # ---------- 2. MASALAH ----------
    def problem(self):
        self.header("Cara naif: kasih SEMUA ke AI")
        docs = self.hook_docs
        stack = VGroup(*[doc_icon(0.42) for _ in range(20)])
        stack.arrange_in_grid(rows=5, cols=4, buff=0.08 * S).move_to(at(-2.2, 1.8))
        self.play(Transform(docs, stack), run_time=0.9)
        lbl = T("500 halaman", 28, color=MUTED).next_to(docs, DOWN, buff=0.2 * S)
        ai = ai_box(1.7).move_to(at(2.3, 1.8))
        arrow = Arrow(docs.get_right(), ai.get_left(), buff=0.25 * S,
                      color=WHITE, stroke_width=5 * S)
        self.play(FadeIn(lbl), FadeIn(ai, scale=0.7), GrowArrow(arrow), run_time=0.9)

        # Scanner membaca A -> Z
        scan = Rectangle(width=docs.width + 0.2 * S, height=0.12 * S, stroke_width=0,
                         fill_color=GOLD, fill_opacity=0.85)
        scan.move_to(docs.get_top())
        reading = T("membaca dari A sampai Z...", 26, color=GOLD).move_to(at(0, -1.0))
        self.add(scan)
        self.play(FadeIn(reading), scan.animate.move_to(docs.get_bottom()),
                  run_time=1.8, rate_func=linear)

        # Diulang 100 kali
        counter_lbl = T("Pertanyaan ke-", 34).move_to(at(-0.6, -1.9))
        tracker = ValueTracker(1)
        def make_num():
            return T(str(int(tracker.get_value())), 46, color=BAD, weight=BOLD).next_to(
                counter_lbl, RIGHT, buff=0.15 * S)
        num = always_redraw(make_num)
        top, bot = docs.get_top(), docs.get_bottom()
        phase = ValueTracker(0)
        scan.add_updater(lambda m: m.move_to(
            top + (bot - top) * ((phase.get_value() % 1.0))))
        self.play(FadeIn(counter_lbl), FadeIn(num), run_time=0.4)
        self.play(tracker.animate.set_value(100), phase.animate.set_value(14),
                  rate_func=rate_functions.ease_in_quad, run_time=3.6)
        num.clear_updaters()
        self.play(Indicate(num, color=BAD, scale_factor=1.4), run_time=0.6)

        # Ratusan karyawan bertanya
        people = VGroup(*[person_icon(ACC, 0.8) for _ in range(12)])
        people.arrange_in_grid(rows=2, cols=6, buff=(0.25 * S, 0.15 * S)).move_to(at(0, -3.4))
        qs = VGroup(*[T("?", 22, color=GOLD, weight=BOLD).next_to(p, UP, buff=0.04 * S)
                      for p in people[:6]])
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in people], lag_ratio=0.05),
                  run_time=0.9)
        self.play(LaggedStart(*[FadeIn(q, scale=2) for q in qs], lag_ratio=0.06),
                  phase.animate.set_value(22), run_time=1.0, rate_func=linear)
        scan.clear_updaters()
        self.wait(0.4)

        # Angka konkret
        self.play(*[FadeOut(m) for m in (scan, reading, counter_lbl, num, people, qs)],
                  run_time=0.5)
        calc1 = T("500 halaman  ×  100 pertanyaan", 34).move_to(at(0, -1.0))
        calc2 = T("= 50.000 halaman dibaca", 40, color=BAD, weight=BOLD).move_to(at(0, -1.8))
        calc3 = T("≈ 25 juta token, per karyawan", 30, color=MUTED).move_to(at(0, -2.5))
        self.play(Write(calc1), run_time=0.9)
        self.play(FadeIn(calc2, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(calc3), run_time=0.6)

        # Biaya & waktu membengkak
        def meter(name, y):
            lab = T(name, 30).move_to(at(-3.0, y)).align_to(at(-3.6, 0), LEFT)
            base = at(-1.9, y)
            bar = Rectangle(width=0.05, height=0.42 * S, fill_color=BAD,
                            fill_opacity=1, stroke_width=0)
            bar.move_to(base, aligned_edge=LEFT)
            return lab, bar, base
        l1, b1, base1 = meter("Biaya", -3.4)
        l2, b2, base2 = meter("Waktu", -4.05)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(b1), FadeIn(b2), run_time=0.4)
        up1 = T("MAHAL", 26, color=BAD, weight=BOLD)
        up2 = T("LAMBAT", 26, color=BAD, weight=BOLD)
        self.play(
            b1.animate.stretch_to_fit_width(5.2 * S).move_to(base1, aligned_edge=LEFT),
            b2.animate.stretch_to_fit_width(4.6 * S).move_to(base2, aligned_edge=LEFT),
            ai[1].animate.set_fill(BAD).set_stroke("#FDA4AF"), run_time=1.6, rate_func=rate_functions.ease_in_expo)
        up1.next_to(b1, RIGHT, buff=0.1 * S).shift(LEFT * (up1.width + 0.25 * S))
        up2.next_to(b2, RIGHT, buff=0.1 * S).shift(LEFT * (up2.width + 0.25 * S))
        up1.set_color(WHITE); up2.set_color(WHITE)
        self.play(FadeIn(up1), FadeIn(up2), Wiggle(ai), run_time=0.8)
        self.wait(1.2)

    # ---------- 3. TITIK BALIK ----------
    def turning(self):
        self.play(FadeOut(self._hdr), run_time=0.3)
        self._hdr = None
        self.clear_content(0.5)
        q1 = T("Kenapa baca semuanya", 48, weight=BOLD)
        q2 = T("kalau cuma butuh", 48, weight=BOLD)
        q3 = T("sebagian?", 64, weight=BOLD, color=GOLD)
        g = VGroup(q1, q2, q3).arrange(DOWN, buff=0.3 * S).move_to(at(0, 0))
        self.play(FadeIn(q1, shift=UP * 0.3), run_time=0.6)
        self.play(FadeIn(q2, shift=UP * 0.3), run_time=0.6)
        self.play(GrowFromCenter(q3), run_time=0.6)
        ul = Underline(q3, color=GOLD, stroke_width=6 * S)
        self.play(Create(ul), run_time=0.5)
        self.wait(1.8)
        self.play(FadeOut(VGroup(g, ul), shift=UP * 0.4), run_time=0.5)

    # ---------- 4. SOLUSI RAG ----------
    def rag(self):
        title = T("RAG", 110, weight=BOLD, color=GOOD).move_to(at(0, 0.8))
        sub = T("Retrieval-Augmented Generation", 32, color=MUTED).next_to(title, DOWN, buff=0.3 * S)
        sub2 = T("cari dulu, baru jawab", 30, color=WHITE).next_to(sub, DOWN, buff=0.25 * S)
        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(sub2), run_time=0.4)
        self.wait(1.0)
        self.play(FadeOut(VGroup(title, sub, sub2)), run_time=0.5)

        # 1) Potong jadi chunk
        self.header("1. Potong dokumen jadi chunk")
        big = doc_icon(2.0).move_to(at(0, 0.6))
        self.play(FadeIn(big, scale=0.8), run_time=0.6)
        colors = [ACC, "#A78BFA", "#F472B6", GOLD, GOOD, "#FB923C", "#2DD4BF", "#60A5FA", "#E879F9"]
        chunks = VGroup(*[
            RoundedRectangle(width=1.1 * S, height=0.55 * S, corner_radius=0.08 * S,
                             fill_color=colors[i], fill_opacity=0.9, stroke_width=0)
            for i in range(9)
        ]).arrange_in_grid(rows=3, cols=3, buff=0.18 * S).move_to(at(0, 0.6))
        cut_lines = VGroup(*[
            DashedLine(big.get_left() + (big.get_top() - big.get_center()) * k,
                       big.get_right() + (big.get_top() - big.get_center()) * k,
                       color=BAD, stroke_width=3 * S)
            for k in (0.33, -0.33)
        ])
        self.play(Create(cut_lines), run_time=0.6)
        self.play(FadeOut(cut_lines), ReplacementTransform(big, chunks), run_time=0.9)
        clbl = T("chunk = potongan kecil teks", 28, color=MUTED).move_to(at(0, -1.6))
        self.play(FadeIn(clbl), run_time=0.4)
        self.wait(0.8)

        # 2) Ubah jadi vektor
        self.header("2. Ubah tiap chunk jadi vektor")
        self.play(FadeOut(clbl), chunks.animate.scale(0.6).move_to(at(-2.6, 2.0)), run_time=0.7)
        plane = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            x_length=7.0 * S, y_length=4.6 * S,
            background_line_style={"stroke_color": "#1E293B", "stroke_width": 2},
            axis_config={"stroke_color": "#334155"},
        ).move_to(at(0.3, -1.3))
        self.play(Create(plane), run_time=0.8)
        pos = [(-3, 2), (-2.2, -1.8), (2.2, 1.6), (2.8, 2.2), (1.6, 2.4),
               (-1, 0.4), (3.2, -1.5), (-3.2, -0.8), (0.4, -2.3)]
        dots = VGroup()
        for i, (x, y) in enumerate(pos):
            d = Dot(plane.c2p(x, y), radius=0.13 * S, color=colors[i])
            dots.add(d)
        vec_txt = T("[0.12, -0.83, 0.47, ...]", 24, color=ACC).move_to(at(1.6, 2.0))
        self.play(FadeIn(vec_txt), run_time=0.4)
        self.play(LaggedStart(*[ReplacementTransform(chunks[i].copy(), dots[i])
                                for i in range(9)], lag_ratio=0.08), run_time=1.6)
        note = T("makna mirip = posisi berdekatan", 24, color=MUTED).next_to(plane, DOWN, buff=0.15 * S)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(1.2)

        # 3) Pertanyaan juga jadi vektor
        self.header("3. Pertanyaan juga jadi vektor")
        self.play(FadeOut(vec_txt), FadeOut(note), run_time=0.3)
        person = person_icon(ACC, 1.1)
        q = bubble("Jatah cuti tahunan berapa?", WHITE, 24).next_to(person, RIGHT, buff=0.2 * S)
        VGroup(person, q).move_to(at(1.4, 2.0))
        self.play(FadeIn(person), FadeIn(q, shift=LEFT * 0.2), run_time=0.6)
        qdot = Star(n=5, outer_radius=0.24 * S, inner_radius=0.1 * S, color=GOLD,
                    fill_opacity=1, stroke_width=0).move_to(plane.c2p(2.3, 1.95))
        self.play(ReplacementTransform(q[0].copy(), qdot), run_time=1.0)
        self.play(Flash(qdot, color=GOLD, line_length=0.25 * S), run_time=0.6)
        self.wait(0.6)

        # 4) Cari yang terdekat
        self.header("4. Cari chunk yang paling dekat")
        near = [2, 3, 4]
        ring = Circle(radius=1.15 * S, color=GOLD, stroke_width=4 * S).move_to(qdot)
        links = VGroup(*[DashedLine(qdot.get_center(), dots[i].get_center(),
                                    color=GOLD, stroke_width=3 * S) for i in near])
        self.play(Create(ring), run_time=0.7)
        self.play(Create(links), *[dots[i].animate.scale(1.6) for i in near], run_time=0.8)
        far = [i for i in range(9) if i not in near]
        self.play(*[dots[i].animate.set_opacity(0.2) for i in far],
                  *[chunks[i].animate.set_opacity(0.2) for i in far], run_time=0.6)
        topk = T("ambil 3 teratas", 26, color=GOLD).next_to(ring, DOWN, buff=0.1 * S)
        self.play(FadeIn(topk), run_time=0.4)
        self.wait(0.8)

        # 5) Hanya chunk relevan ke AI
        self.header("5. Kirim chunk relevan saja ke AI")
        sel = VGroup(*[chunks[i] for i in near])
        others = VGroup(plane, dots, ring, links, topk, qdot,
                        *[chunks[i] for i in far])
        self.play(FadeOut(others), run_time=0.6)
        ai = ai_box(1.7).move_to(at(1.8, -0.8))
        self.play(FadeIn(ai, scale=0.7),
                  sel.animate.arrange(DOWN, buff=0.15 * S).scale(1.4).move_to(at(-2.3, -0.8)),
                  VGroup(person, q).animate.move_to(at(0, 2.2)),
                  run_time=0.9)
        arr = Arrow(sel.get_right(), ai.get_left(), buff=0.2 * S, color=GOOD,
                    stroke_width=5 * S)
        qarr = Arrow(q.get_bottom(), ai.get_top(), buff=0.15 * S, color=WHITE,
                     stroke_width=4 * S)
        self.play(GrowArrow(arr), GrowArrow(qarr), run_time=0.6)
        self.play(LaggedStart(*[c.copy().animate.move_to(ai).scale(0.2).set_opacity(0)
                                for c in sel], lag_ratio=0.2),
                  run_time=1.0)
        small = T("3 chunk, bukan 500 halaman", 28, color=GOOD, weight=BOLD).move_to(at(0, -2.8))
        self.play(FadeIn(small), Indicate(ai, color="#A78BFA"), run_time=0.8)
        self.wait(0.8)

        # 6) Jawaban
        self.header("6. Jawaban keluar, cepat & tepat")
        ans = bubble("Jatah cuti tahunan: 12 hari", GOOD, 28).move_to(at(0, -3.9))
        src = T("sumber: Peraturan Perusahaan, Bab 5", 20, color=MUTED).next_to(ans, DOWN, buff=0.15 * S)
        aarr = Arrow(ai.get_bottom(), ans.get_top(), buff=0.12 * S, color=GOOD,
                     stroke_width=4 * S)
        self.play(FadeOut(small), run_time=0.4)
        self.play(GrowArrow(aarr), FadeIn(ans, shift=DOWN * 0.3), run_time=0.8)
        self.play(FadeIn(src), run_time=0.4)
        self.wait(1.8)
        self.play(FadeOut(self._hdr), run_time=0.3)
        self._hdr = None
        self.clear_content(0.6)

    # ---------- 5. PENUTUP ----------
    def outro(self):
        self.header("Sebelum vs sesudah RAG")
        colx = (-2.0, 2.0)
        h1 = T("Tanpa RAG", 34, weight=BOLD, color=BAD).move_to(at(colx[0], 2.6))
        h2 = T("Dengan RAG", 34, weight=BOLD, color=GOOD).move_to(at(colx[1], 2.6))
        div = Line(at(0, 3.0), at(0, -2.6), color="#334155", stroke_width=3 * S)
        self.play(FadeIn(h1), FadeIn(h2), Create(div), run_time=0.6)

        rows = [
            ("Dibaca / pertanyaan", "500 halaman", "3 chunk"),
            ("Token / pertanyaan", "± 250.000", "± 1.500"),
            ("Waktu jawab", "lambat", "detik"),
            ("Biaya", "mahal", "hemat"),
        ]
        y = 1.6
        anims = []
        for name, a, b in rows:
            n = T(name, 22, color=MUTED).move_to(at(0, y + 0.45))
            n.set_z_index(2)
            bg = BackgroundRectangle(n, color=config.background_color, fill_opacity=1, buff=0.08)
            va = T(a, 32, weight=BOLD).move_to(at(colx[0], y - 0.05))
            vb = T(b, 32, weight=BOLD, color=GOOD).move_to(at(colx[1], y - 0.05))
            anims.append(AnimationGroup(FadeIn(bg), FadeIn(n), FadeIn(va, shift=RIGHT * 0.2),
                                        FadeIn(vb, shift=LEFT * 0.2)))
            y -= 1.15
        self.play(LaggedStart(*anims, lag_ratio=0.5), run_time=3.2)
        self.wait(2.0)
        self.play(FadeOut(self._hdr), run_time=0.3)
        self._hdr = None
        self.clear_content(0.6)

        l1 = T("Inilah yang dikerjakan", 40).move_to(at(0, 1.6))
        l2 = T("AI engineer:", 64, weight=BOLD, color=ACC).next_to(l1, DOWN, buff=0.35 * S)
        l3 = T("membangun sistem RAG", 48, weight=BOLD, color=GOOD).next_to(l2, DOWN, buff=0.45 * S)
        self.play(FadeIn(l1, shift=UP * 0.2), run_time=0.6)
        self.play(Write(l2), run_time=0.8)
        self.play(GrowFromCenter(l3), run_time=0.7)
        box = SurroundingRectangle(l3, color=GOOD, buff=0.2 * S, corner_radius=0.15 * S,
                                   stroke_width=4 * S)
        self.play(Create(box), run_time=0.6)
        cta = T("Follow untuk part berikutnya", 26, color=MUTED).move_to(at(0, -2.4))
        self.play(FadeIn(cta, shift=UP * 0.2), run_time=0.5)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
