"""Lembar referensi KAPUR (palet, tipe, komponen) sebagai satu gambar.

    ORIENT=horizontal manim -s -qh palet.py PaletKapur
"""
from theme import *


class PaletKapur(KapurScene):
    def construct(self):
        top = AMAN["atas"]
        L = AMAN["kiri"]
        self.add(label_bab("Kapur · design system v1"))
        self.add(judul("Kapur di papan hitam", size="h1").move_to([0, top - 0.6, 0]).align_to([L, 0, 0], LEFT))

        # Warna bermakna
        y = top - 1.55
        for i, (nama, peran) in enumerate(PERAN.items()):
            hexc = globals()[nama]
            x = L + 0.2 + i * 2.45
            sw = RoundedRectangle(width=2.2, height=0.8, corner_radius=0.12, fill_color=hexc,
                                  fill_opacity=1, stroke_width=0).move_to([x + 1.1, y - 0.4, 0])
            n = mono(nama, color=hexc, size=22, weight=BOLD).next_to(sw, DOWN, buff=0.12).align_to(sw, LEFT)
            h = mono(hexc, color=ABU, size=17).next_to(n, DOWN, buff=0.06).align_to(sw, LEFT)
            p = Paragraph(*peran.split(" · "), font=FONT_TEKS, font_size=16, color=TINTA,
                          line_spacing=0.6).next_to(h, DOWN, buff=0.1).align_to(sw, LEFT)
            self.add(sw, n, h, p)

        # Netral
        y2 = top - 4.4
        netral = [("HITAM", HITAM), ("PERMUKAAN", PERMUKAAN), ("GARIS", GARIS), ("ABU_GELAP", ABU_GELAP),
                  ("ABU", ABU), ("TINTA", TINTA), ("KERTAS", KERTAS)]
        for i, (nama, hexc) in enumerate(netral):
            x = L + 0.2 + i * 2.08
            sw = Square(side_length=0.7, fill_color=hexc, fill_opacity=1, stroke_color=ABU_GELAP,
                        stroke_width=1.5).move_to([x + 0.35, y2, 0])
            n = mono(nama, color=ABU, size=14).next_to(sw, RIGHT, buff=0.1).shift(UP * 0.12)
            h = mono(hexc, color=ABU_GELAP, size=13).next_to(n, DOWN, buff=0.05).align_to(n, LEFT)
            self.add(sw, n, h)

        # Tipografi
        y3 = top - 5.7
        t1 = judul("Source Serif 4 — judul", size="h2").move_to([0, y3, 0]).align_to([L + 0.2, 0, 0], LEFT)
        t2 = teks("Inter — label, caption, isi kartu", size="body").next_to(t1, DOWN, buff=0.25).align_to(t1, LEFT)
        t3 = mono("JetBrains Mono — angka & vektor [0.12, -0.83]", color=JINGGA, size="caption").next_to(t2, DOWN, buff=0.25).align_to(t1, LEFT)
        self.add(t1, t2, t3)

        # Komponen
        cx = 3.2
        comps = VGroup(
            VGroup(ikon_dokumen(0.6), ikon_orang(LANGIT, 1.2), ikon_ai(1.1)).arrange(RIGHT, buff=0.4),
            VGroup(pil("pil / label", DAUN), lencana(3), gelembung("balon chat", LANGIT)).arrange(RIGHT, buff=0.3),
            batang("batang", 0.7, color=SAGA, panjang=3.6, teks_nilai="70%"),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).scale(0.9).move_to([cx, y3 - 0.8, 0])
        self.add(comps)
        self.mark("00_referensi_palet")
