"""Opsi A dipoles: 3 variasi (glow kapur, bingkai papan, ringkas).

    python logo_a_poles.py  -> A1/A2/A3_1080.png, ringkasan_A_poles.png, pratinjau_A_poles_bulat.png
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from logo_kapur import (Kanvas, P, C, W, N, HERE, goresan, lingkaran, busur, debu, rgb, redup, grain,
                        bulat, font, HITAM, ABU_GELAP, ABU, TINTA, LANGIT, TOSKA, KUNYIT, DAUN)


def glow(kv, warna, gambar, radius=0.05, kuat=0.55):
    """Pendar halus di sekitar goresan, seperti debu kapur yang berkilau."""
    m = Image.new("L", (W, W), 0); gambar(ImageDraw.Draw(m))
    m = m.filter(ImageFilter.GaussianBlur(radius * C))
    a = np.asarray(m).astype(np.float32) / 255.0 * kuat
    col = np.array(rgb(warna), np.float32)
    kv.base = np.minimum(255, kv.base + col * a[..., None])  # aditif


def cincin_tangan(d, x, y, r, lebar, seed=0, lapis=2):
    """Lingkaran digambar tangan: cincin (annulus) dengan radius sedikit bergoyang."""
    g = np.random.default_rng(seed)
    t = np.linspace(0, 2 * math.pi, 360, endpoint=False)
    for L in range(lapis):
        ph = g.random() * 6.28
        off = (g.random() - 0.5) * 0.006, (g.random() - 0.5) * 0.006
        rr = r * (1 + 0.022 * np.sin(2 * t + ph) + 0.010 * np.sin(5 * t + 2 * ph))
        w = lebar * (1 - 0.18 * L) * (1 + 0.12 * np.sin(3 * t + ph))  # tebal goresan tidak rata
        luar = [P(x + off[0] + (q + h / 2) * math.cos(s), y + off[1] + (q + h / 2) * math.sin(s)) for s, q, h in zip(t, rr, w)]
        dalam = [P(x + off[0] + (q - h / 2) * math.cos(s), y + off[1] + (q - h / 2) * math.sin(s)) for s, q, h in zip(t, rr, w)]
        m = Image.new("L", d.im.size, 0); md = ImageDraw.Draw(m)
        md.polygon(luar, fill=255); md.polygon(dalam, fill=0)
        d.bitmap((0, 0), m, fill=255)


def gambar_A(varian):
    kv = Kanvas(); debu(kv)
    ringkas = varian == "A3"
    if ringkas:
        simpul = {"in": (-0.54, -0.02), "ai": (0.0, -0.06), "out": (0.54, 0.02), "a": (0.0, 0.44)}
        sisi = [("in", "a"), ("a", "out"), ("a", "ai"), ("in", "ai"), ("ai", "out")]
        kecil = ("a",); R = {"in": 0.15, "out": 0.15, "ai": 0.25}
    else:
        simpul = {"in": (-0.55, 0.0), "ai": (0.0, -0.08), "out": (0.55, 0.04),
                  "a": (-0.25, 0.40), "b": (0.27, 0.42)}
        sisi = [("in", "a"), ("a", "ai"), ("ai", "b"), ("b", "out"), ("a", "b"), ("in", "ai"), ("ai", "out")]
        kecil = ("a", "b"); R = {"in": 0.135, "out": 0.135, "ai": 0.22}
    pakai_glow = True

    # bingkai papan (A2): lingkaran kapur samar yang mengikuti potongan bulat
    if varian == "A2":
        kv.layer(ABU_GELAP, lambda d: cincin_tangan(d, 0, 0, 0.84, 0.018, seed=21, lapis=1), alpha=0.75)
        for k in range(14):  # titik-titik grid papan, samar
            pass

    # sisi
    for i, (u, v) in enumerate(sisi):
        utama = (u, v) in [("in", "ai"), ("ai", "out")]
        f = lambda d, u=u, v=v, i=i, utama=utama: goresan(d, [simpul[u], simpul[v]], 0.044 if utama else 0.030, seed=i)
        kv.layer(TINTA if utama else ABU, f, alpha=1.0 if utama else 0.85)

    # simpul kecil
    for j, k in enumerate(kecil):
        x, y = simpul[k]; r = 0.09 if ringkas else 0.08
        kv.layer(HITAM, lambda d, x=x, y=y, r=r: lingkaran(d, x, y, r + 0.02, fill=True), kasar=False)
        kv.layer(ABU, lambda d, x=x, y=y, r=r, j=j: cincin_tangan(d, x, y, r, 0.034, seed=30 + j))

    # simpul utama + glow
    for j, (k, col) in enumerate((("in", LANGIT), ("out", DAUN), ("ai", TOSKA))):
        x, y = simpul[k]; r = R[k]
        kv.layer(HITAM, lambda d, x=x, y=y, r=r: lingkaran(d, x, y, r + 0.03, fill=True), kasar=False)
        if pakai_glow:
            glow(kv, col, lambda d, x=x, y=y, r=r: lingkaran(d, x, y, r, 0.05),
                 radius=0.06 if k == "ai" else 0.045, kuat=0.45 if k == "ai" else 0.32)
        kv.layer(redup(col, 0.20), lambda d, x=x, y=y, r=r: lingkaran(d, x, y, r - 0.01, fill=True), kasar=False)
        kv.layer(col, lambda d, x=x, y=y, r=r, j=j: cincin_tangan(d, x, y, r, 0.050, seed=40 + j))
    # inti AI: titik + cincin dalam tipis (chip)
    cx, cy = simpul["ai"]; Rai = R["ai"]
    kv.layer(TOSKA, lambda d: cincin_tangan(d, cx, cy, Rai * 0.62, 0.020, seed=50, lapis=1), alpha=0.7)
    glow(kv, TOSKA, lambda d: lingkaran(d, cx, cy, Rai * 0.32, fill=True), radius=0.04, kuat=0.5)
    kv.layer(TOSKA, lambda d: lingkaran(d, cx, cy, Rai * 0.32, fill=True))

    # coret kapur kuning (satu-satunya kuning), miring tipis seperti garis bawah tangan
    y0 = -0.45 if not ringkas else -0.46
    pts = [(x, y + 0.06 * x) for x, y in busur(-0.38, 0.44, y0, 0.03)]
    glow(kv, KUNYIT, lambda d: goresan(d, pts, 0.05, jitter=0.004, seed=11), radius=0.05, kuat=0.35)
    kv.layer(KUNYIT, lambda d: goresan(d, pts, 0.055, jitter=0.004, seed=11))
    return kv


VAR = {"A1": ("Glow kapur", "pendar halus, cincin digambar tangan"),
       "A2": ("Bingkai papan", "A1 + lingkaran kapur sebagai bingkai"),
       "A3": ("Ringkas", "simpul lebih sedikit, paling tegas")}
REKOM = "A1"


def main():
    hasil = {k: gambar_A(k).simpan(HERE / f"{k}_1080.png") for k in VAR}
    cw, pad = 560, 40
    Rg = Image.new("RGB", (pad + 3 * (cw + pad), 980), (12, 12, 12)); d = ImageDraw.Draw(Rg)
    fj, ft, fm = font("SourceSerif4.ttf", 44), font("Inter.ttf", 24), font("JetBrainsMono.ttf", 22)
    for i, k in enumerate(VAR):
        nama, ket = VAR[k]; x = pad + i * (cw + pad)
        sq = hasil[k].resize((cw, cw), Image.LANCZOS).copy()
        ImageDraw.Draw(sq).ellipse([2, 2, cw - 3, cw - 3], outline=rgb("#2a2a2a"), width=2)
        Rg.paste(sq, (x, 150))
        rek = k == REKOM
        d.text((x, 40), k, font=fm, fill=rgb(KUNYIT if rek else ABU))
        if rek:
            tw = d.textlength(k, font=fm)
            d.rounded_rectangle([x + tw + 14, 38, x + tw + 190, 68], radius=15, outline=rgb(KUNYIT), width=2)
            d.text((x + tw + 26, 40), "REKOMENDASI", font=font("JetBrainsMono.ttf", 18), fill=rgb(KUNYIT))
        d.text((x, 72), nama, font=fj, fill=rgb(TINTA))
        d.text((x, 722), ket, font=ft, fill=rgb(ABU))
        b1, b2 = bulat(hasil[k], 110), bulat(hasil[k], 48)
        Rg.paste(b1, (x, 780), b1); Rg.paste(b2, (x + 140, 842), b2)
        d.text((x, 900), "110 px", font=fm, fill=rgb(ABU_GELAP)); d.text((x + 140, 900), "48 px", font=fm, fill=rgb(ABU_GELAP))
    Rg.save(HERE / "ringkasan_A_poles.png")

    P2 = Image.new("RGB", (3 * 200 + 40, 2 * 190 + 40), (0, 0, 0))
    ImageDraw.Draw(P2).rectangle([0, 210, P2.width, P2.height], fill=(245, 245, 245))
    for i, k in enumerate(VAR):
        for j in (0, 1):
            b = bulat(hasil[k], 110); P2.paste(b, (40 + i * 200, 40 + j * 190), b)
            ImageDraw.Draw(P2).text((160 + i * 200, 85 + j * 190), k, font=fm, fill=(120, 120, 120))
    P2.save(HERE / "pratinjau_A_poles_bulat.png")


if __name__ == "__main__":
    main()
