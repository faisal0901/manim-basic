"""Logo foto profil (KAPUR) - 3 opsi, gaya goresan kapur di papan hitam.

    python logo_kapur.py      -> opsi_A/B/C_1080.png, ringkasan_3_opsi.png, pratinjau_bulat_kecil.png

Butuh: pillow, numpy. Palet diambil dari design system KAPUR (tidak diubah).
"""
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
FONTS = next(p / "design-system" for p in HERE.parents if (p / "design-system").is_dir()) / "fonts"

# --- Palet KAPUR (sama persis dengan theme.py) ---
HITAM = "#000000"; GARIS = "#1E1E1E"; ABU_GELAP = "#454545"; ABU = "#9B9B9B"; TINTA = "#EDEDED"
LANGIT = "#5CC3E6"; TOSKA = "#4FD1B8"; KUNYIT = "#FFD54A"; DAUN = "#8BD17C"; JINGGA = "#F4A95C"

N = 1080          # ukuran akhir
SS = 2            # supersampling
W = N * SS
C = W / 2
rng = np.random.default_rng(7)


def rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def redup(h, a=0.18):
    return tuple(int(v * a) for v in rgb(h))


# ---------------------------------------------------------------- kapur
GRAIN = None
def grain():
    """Tekstur butir kapur: sebagian piksel goresan 'hilang' seperti kapur di papan."""
    global GRAIN
    if GRAIN is None:
        n = rng.random((W, W)).astype(np.float32)
        img = Image.fromarray((n * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))
        g = np.asarray(img).astype(np.float32) / 255.0
        g = (g - g.mean()) / (g.std() + 1e-6)
        # garis-garis halus searah (serat kapur)
        streak = Image.fromarray((rng.random((W // 6, W)) * 255).astype(np.uint8)).resize((W, W), Image.BILINEAR)
        s = (np.asarray(streak).astype(np.float32) / 255.0 - 0.5) * 2
        GRAIN = np.clip(0.90 + 0.16 * g + 0.08 * s, 0.35, 1.0)
    return GRAIN


class Kanvas:
    def __init__(self):
        self.base = np.zeros((W, W, 3), np.float32)

    def layer(self, warna, gambar, kasar=True, alpha=1.0):
        m = Image.new("L", (W, W), 0)
        gambar(ImageDraw.Draw(m))
        a = np.asarray(m).astype(np.float32) / 255.0 * alpha
        if kasar:
            a = a * grain()
        col = np.array(rgb(warna) if isinstance(warna, str) else warna, np.float32)
        self.base = self.base * (1 - a[..., None]) + col * a[..., None]

    def simpan(self, path):
        im = Image.fromarray(np.clip(self.base, 0, 255).astype(np.uint8))
        im = im.resize((N, N), Image.LANCZOS)
        im.save(path)
        return im


def P(x, y):
    """Koordinat logo: (0,0) pusat, satuan = fraksi dari setengah lebar (-1..1)."""
    return (C + x * C, C - y * C)


def goresan(d, pts, lebar, jitter=0.006, lapis=3, seed=0):
    """Garis tangan: beberapa lapis goresan yang sedikit bergoyang."""
    r = np.random.default_rng(seed)
    pts = np.array(pts, float)
    # bagi jadi titik rapat
    dense = []
    for a, b in zip(pts[:-1], pts[1:]):
        k = max(2, int(np.linalg.norm(b - a) * 60))
        for t in np.linspace(0, 1, k, endpoint=False):
            dense.append(a + (b - a) * t)
    dense.append(pts[-1]); dense = np.array(dense)
    for L in range(lapis):
        ph = r.random() * 6.28
        wob = np.sin(np.linspace(0, 3.0, len(dense)) + ph)[:, None] * jitter * (r.random() - 0.5) * 2
        q = dense + wob
        xy = [P(x, y) for x, y in q]
        w = int(lebar * C * (1.0 - 0.12 * L))
        d.line(xy, fill=255, width=w, joint="curve")
        for p in (xy[0], xy[-1]):
            d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=255)


def lingkaran(d, x, y, r, lebar=None, fill=False):
    cx, cy = P(x, y); R = r * C
    if fill:
        d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=255)
    else:
        w = int(lebar * C)
        d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=255, width=w)


def busur(x0, x1, y, lengkung, n=40):
    xs = np.linspace(x0, x1, n)
    t = np.linspace(-1, 1, n)
    return list(zip(xs, y - lengkung * (1 - t ** 2)))


def debu(kv):
    """Bekas hapusan kapur samar di papan (sangat tipis, tidak mengganggu)."""
    m = Image.new("L", (W, W), 0)
    d = ImageDraw.Draw(m)
    for _ in range(9):
        x, y = rng.uniform(0.15, 0.85) * W, rng.uniform(0.15, 0.85) * W
        rx, ry = rng.uniform(0.15, 0.35) * W, rng.uniform(0.04, 0.09) * W
        d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=int(rng.uniform(40, 90)))
    m = m.filter(ImageFilter.GaussianBlur(W * 0.04))
    a = np.asarray(m).astype(np.float32) / 255.0 * 0.10 * grain()
    col = np.array(rgb("#2A2A2A"), np.float32)
    kv.base = kv.base * (1 - a[..., None]) + col * a[..., None]


# ---------------------------------------------------------------- opsi A
def opsi_A():
    """Titik terhubung: input (LANGIT) -> AI (TOSKA) -> jawaban (DAUN), coret kapur kuning."""
    kv = Kanvas(); debu(kv)
    simpul = {"in": (-0.56, 0.02), "ai": (0.0, -0.08), "out": (0.56, 0.06),
              "a": (-0.26, 0.42), "b": (0.26, 0.44)}
    sisi = [("in", "a"), ("a", "ai"), ("ai", "b"), ("b", "out"), ("a", "b"), ("in", "ai"), ("ai", "out")]
    for i, (u, v) in enumerate(sisi):
        utama = (u, v) in [("in", "ai"), ("ai", "out")]
        kv.layer(TINTA if utama else ABU,
                 lambda d, u=u, v=v, i=i, utama=utama: goresan(d, [simpul[u], simpul[v]], 0.042 if utama else 0.032, seed=i))
    for k in ("a", "b"):
        x, y = simpul[k]
        kv.layer(HITAM, lambda d, x=x, y=y: lingkaran(d, x, y, 0.085, fill=True), kasar=False)
        kv.layer(ABU, lambda d, x=x, y=y: lingkaran(d, x, y, 0.085, 0.034))
    for k, col, r in (("in", LANGIT, 0.135), ("out", DAUN, 0.135), ("ai", TOSKA, 0.22)):
        x, y = simpul[k]
        kv.layer(HITAM, lambda d, x=x, y=y, r=r: lingkaran(d, x, y, r, fill=True), kasar=False)
        kv.layer(redup(col, 0.22), lambda d, x=x, y=y, r=r: lingkaran(d, x, y, r, fill=True), kasar=False)
        kv.layer(col, lambda d, x=x, y=y, r=r: lingkaran(d, x, y, r, 0.052))
    kv.layer(TOSKA, lambda d: lingkaran(d, 0, -0.08, 0.075, fill=True))
    # coret kapur (tanda tangan KAPUR), miring sedikit seperti garis bawah tangan. Satu-satunya kuning.
    pts = [(x, y + 0.05 * x) for x, y in busur(-0.40, 0.44, -0.44, 0.035)]
    kv.layer(KUNYIT, lambda d: goresan(d, pts, 0.055, jitter=0.004, seed=11))
    return kv


# ---------------------------------------------------------------- opsi B
def opsi_B():
    """Potongan token: kalimat yang dipecah jadi kapsul + kursor kuning."""
    kv = Kanvas(); debu(kv)
    hh = 0.135
    caps = [(-0.62, 0.08, 0.24, LANGIT), (0.18, 0.62, 0.24, TOSKA),
            (-0.62, -0.10, -0.12, DAUN), (-0.00, 0.34, -0.12, JINGGA)]
    def kapsul(x0, x1, yc):
        def f(d, lebar=None, fill=False):
            a, b = P(x0, yc + hh), P(x1, yc - hh)
            if fill:
                d.rounded_rectangle([a, b], radius=hh * C, fill=255)
            else:
                d.rounded_rectangle([a, b], radius=hh * C, outline=255, width=int(lebar * C))
        return f
    for i, (x0, x1, yc, col) in enumerate(caps):
        k = kapsul(x0, x1, yc)
        kv.layer(redup(col, 0.24), lambda d, k=k: k(d, fill=True), kasar=False)
        kv.layer(col, lambda d, k=k: k(d, 0.045))
        kv.layer(col, lambda d, x0=x0, x1=x1, yc=yc, i=i: goresan(d, [(x0 + 0.12, yc), (x1 - 0.12, yc)], 0.04, seed=i), alpha=0.8)
    kv.layer(KUNYIT, lambda d: goresan(d, [(0.50, 0.03), (0.50, -0.27)], 0.055, jitter=0.002, seed=5))
    return kv


# ---------------------------------------------------------------- opsi C
def opsi_C():
    """Vektor: sumbu kapur + panah TOSKA ke titik kuning, titik-titik makna di sekitar."""
    kv = Kanvas(); debu(kv)
    o = (-0.50, -0.48)
    kv.layer(ABU, lambda d: goresan(d, [(o[0], 0.56), o, (0.60, o[1])], 0.036, seed=1))
    for (x, y, col) in [(0.36, 0.48, LANGIT), (-0.18, 0.30, DAUN), (0.50, -0.02, JINGGA)]:
        kv.layer(col, lambda d, x=x, y=y: lingkaran(d, x, y, 0.055, fill=True))
    tip = (0.18, 0.18)
    kv.layer(TOSKA, lambda d: goresan(d, [o, tip], 0.058, seed=3))
    ang = math.atan2(tip[1] - o[1], tip[0] - o[0])
    for s in (+1, -1):
        a2 = ang + math.pi + s * 0.55
        e = (tip[0] + 0.19 * math.cos(a2), tip[1] + 0.19 * math.sin(a2))
        kv.layer(TOSKA, lambda d, e=e: goresan(d, [e, tip], 0.058, seed=4 + s))
    kv.layer(HITAM, lambda d: lingkaran(d, 0.26, 0.26, 0.10, fill=True), kasar=False)
    kv.layer(KUNYIT, lambda d: lingkaran(d, 0.26, 0.26, 0.088, fill=True))
    return kv


OPSI = {"A": ("Titik terhubung", "input → AI → jawaban", opsi_A),
        "B": ("Potongan token", "teks dipecah jadi token", opsi_B),
        "C": ("Vektor", "makna jadi arah & angka", opsi_C)}
REKOMENDASI = "A"


def bulat(im, d):
    im = im.resize((d, d), Image.LANCZOS)
    m = Image.new("L", (d * 4, d * 4), 0); ImageDraw.Draw(m).ellipse([0, 0, d * 4 - 1, d * 4 - 1], fill=255)
    out = Image.new("RGBA", (d, d)); out.paste(im, (0, 0), m.resize((d, d), Image.LANCZOS))
    return out


def font(nama, s):
    return ImageFont.truetype(str(FONTS / nama), s)


def main():
    hasil = {}
    for k, (nama, _, fn) in OPSI.items():
        im = fn().simpan(HERE / f"opsi_{k}_1080.png")
        hasil[k] = im
        print("ok", k)

    # Ringkasan perbandingan: tiap opsi = persegi + panduan lingkaran + bulat 110px + bulat 48px
    cw, pad = 560, 40
    R = Image.new("RGB", (pad + 3 * (cw + pad), 980), (12, 12, 12))
    d = ImageDraw.Draw(R)
    fj, ft, fm = font("SourceSerif4.ttf", 44), font("Inter.ttf", 26), font("JetBrainsMono.ttf", 22)
    for f in (fj,):
        try: f.set_variation_by_name("SemiBold")
        except Exception: pass
    for i, k in enumerate(OPSI):
        nama, makna, _ = OPSI[k]
        x = pad + i * (cw + pad)
        sq = hasil[k].resize((cw, cw), Image.LANCZOS).copy()
        sd = ImageDraw.Draw(sq)
        sd.ellipse([2, 2, cw - 3, cw - 3], outline=rgb(ABU_GELAP), width=2)
        R.paste(sq, (x, 150))
        rek = k == REKOMENDASI
        d.text((x, 40), f"Opsi {k}", font=fm, fill=rgb(KUNYIT if rek else ABU))
        d.text((x, 72), nama, font=fj, fill=rgb(TINTA))
        if rek:
            tw = d.textlength(f"Opsi {k}", font=fm)
            d.rounded_rectangle([x + tw + 14, 38, x + tw + 190, 68], radius=15, outline=rgb(KUNYIT), width=2)
            d.text((x + tw + 26, 40), "REKOMENDASI", font=font("JetBrainsMono.ttf", 18), fill=rgb(KUNYIT))
        d.text((x, 720), makna, font=ft, fill=rgb(ABU))
        b1, b2 = bulat(hasil[k], 110), bulat(hasil[k], 48)
        R.paste(b1, (x, 780), b1); R.paste(b2, (x + 140, 842), b2)
        d.text((x, 900), "110 px", font=fm, fill=rgb(ABU_GELAP)); d.text((x + 140, 900), "48 px", font=fm, fill=rgb(ABU_GELAP))
    R.save(HERE / "ringkasan_3_opsi.png")

    # Pratinjau bulat kecil, di atas latar gelap & terang (mode gelap/terang app)
    P2 = Image.new("RGB", (3 * 200 + 40, 2 * 170 + 40), (0, 0, 0))
    ImageDraw.Draw(P2).rectangle([0, 210, P2.width, P2.height], fill=(245, 245, 245))
    for i, k in enumerate(OPSI):
        for j, bg in enumerate((0, 1)):
            b = bulat(hasil[k], 110)
            P2.paste(b, (40 + i * 200, 40 + j * 190), b)
            ImageDraw.Draw(P2).text((165 + i * 200, 85 + j * 190), k, font=fm, fill=(120, 120, 120))
    P2.save(HERE / "pratinjau_bulat_kecil.png")


if __name__ == "__main__":
    main()
