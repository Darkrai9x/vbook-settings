"""Draws the pictures of co_thu, dem_sao, hai_trinh and terminal (own work, CC0): python3 skins/tools/gen_assets.py skins/src"""
import math, random, subprocess, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from chrome_render import chrome_render

OUT = pathlib.Path(sys.argv[1])

def render(svg: str, target: pathlib.Path, fmt_args=()):
    chrome_render(svg, target)

# --- Starry sky: a starfield and 8 moon phases -------------------------------------------
def stars():
    rnd = random.Random(7)
    w, h = 720, 1280
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">']
    for _ in range(520):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.choice([0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 1.9])
        a = rnd.uniform(0.25, 0.95) if r < 1.4 else rnd.uniform(0.7, 1)
        col = rnd.choice(["#ffffff", "#fff4dc", "#dfe8ff", "#ffffff"])
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}" fill-opacity="{a:.2f}"/>')
    # a few bright stars with a soft halo
    for _ in range(14):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#fff6e0" fill-opacity="0.10"/>')
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="#fffaf0" fill-opacity="0.95"/>')
    parts.append("</svg>")
    render("".join(parts), OUT / "dem_sao/images/stars.png")

def moons():
    size, c, r = 128, 64, 52
    lit, dim = "#f4e9c8", "#3a4166"
    for i in range(8):
        k = i / 8.0  # 0 new, 0.5 full
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}">',
               f'<circle cx="{c}" cy="{c}" r="{r + 10}" fill="{lit}" fill-opacity="0.07"/>',
               f'<circle cx="{c}" cy="{c}" r="{r}" fill="{dim}" fill-opacity="0.9"/>']
        if i == 4:
            svg.append(f'<circle cx="{c}" cy="{c}" r="{r}" fill="{lit}"/>')
        elif i != 0:
            rx = abs(math.cos(2 * math.pi * k)) * r
            crescent = abs(math.cos(2 * math.pi * k)) > 0 and (k < 0.25 or k > 0.75)
            if k < 0.5:  # waxing: the right half lit
                sweep = 0 if crescent else 1
                svg.append(f'<path d="M {c} {c - r} A {r} {r} 0 0 1 {c} {c + r} A {rx:.2f} {r} 0 0 {sweep} {c} {c - r} Z" fill="{lit}"/>')
            else:  # waning: the left half lit
                sweep = 1 if crescent else 0
                svg.append(f'<path d="M {c} {c - r} A {r} {r} 0 0 0 {c} {c + r} A {rx:.2f} {r} 0 0 {sweep} {c} {c - r} Z" fill="{lit}"/>')
        for (dx, dy, rr) in [(-14, -12, 8), (12, 10, 6), (-4, 22, 5), (20, -16, 4), (-24, 12, 3)]:
            svg.append(f'<circle cx="{c + dx}" cy="{c + dy}" r="{rr}" fill="#000" fill-opacity="0.07"/>')
        svg.append("</svg>")
        render("".join(svg), OUT / f"dem_sao/moon/moon-{i}.png")

# --- Voyage log: a compass rose and a chart grid ------------------------------------------
def compass():
    size, c = 240, 120
    ink = "#3b2f22"
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}">',
         f'<circle cx="{c}" cy="{c}" r="104" fill="none" stroke="{ink}" stroke-width="2.5"/>',
         f'<circle cx="{c}" cy="{c}" r="96" fill="none" stroke="{ink}" stroke-width="1"/>']
    for d in range(0, 360, 10):
        a = math.radians(d)
        r1 = 96 if d % 30 else 88
        s.append(f'<line x1="{c + r1 * math.sin(a):.1f}" y1="{c - r1 * math.cos(a):.1f}" x2="{c + 104 * math.sin(a):.1f}" y2="{c - 104 * math.cos(a):.1f}" stroke="{ink}" stroke-width="1.2"/>')
    def point(angle, length, width, fill):
        a = math.radians(angle)
        tip = (c + length * math.sin(a), c - length * math.cos(a))
        l = (c + width * math.sin(a - math.pi / 2), c - width * math.cos(a - math.pi / 2))
        r = (c + width * math.sin(a + math.pi / 2), c - width * math.cos(a + math.pi / 2))
        s.append(f'<polygon points="{tip[0]:.1f},{tip[1]:.1f} {l[0]:.1f},{l[1]:.1f} {c},{c}" fill="{fill}"/>')
        s.append(f'<polygon points="{tip[0]:.1f},{tip[1]:.1f} {r[0]:.1f},{r[1]:.1f} {c},{c}" fill="{ink}"/>')
    for d in (45, 135, 225, 315):
        point(d, 62, 10, "#e9dcbc")
    for d in (0, 90, 180, 270):
        point(d, 92, 14, "#e9dcbc")
    s.append(f'<circle cx="{c}" cy="{c}" r="6" fill="#a33a2c"/>')
    s.append(f'<text x="{c}" y="13" font-family="serif" font-size="16" font-weight="bold" text-anchor="middle" fill="{ink}">N</text>')
    s.append("</svg>")
    render("".join(s), OUT / "hai_trinh/images/compass.png")

def chart():
    w, h = 720, 1280
    ink = "#5b4a33"
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">']
    for x in range(0, w + 1, 90):
        s.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{ink}" stroke-width="1" stroke-opacity="0.5"/>')
    for y in range(0, h + 1, 90):
        s.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{ink}" stroke-width="1" stroke-opacity="0.5"/>')
    rnd = random.Random(3)
    # rhumb lines from two wind roses, as on a portolan chart
    for (cx, cy) in [(160, 300), (560, 980)]:
        for d in range(0, 360, 22):
            a = math.radians(d + 11)
            s.append(f'<line x1="{cx}" y1="{cy}" x2="{cx + 1400 * math.sin(a):.0f}" y2="{cy - 1400 * math.cos(a):.0f}" stroke="{ink}" stroke-width="0.8" stroke-opacity="0.35"/>')
    # a stretch of coast
    pts = []
    x, y = -10, 1100
    while x < w + 20:
        pts.append(f"{x:.0f},{y:.0f}")
        x += rnd.uniform(14, 30)
        y += rnd.uniform(-22, 18)
    s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{ink}" stroke-width="2" stroke-opacity="0.6"/>')
    s.append("</svg>")
    render("".join(s), OUT / "hai_trinh/images/chart.png")

# --- Terminal: scanlines -------------------------------------------------------------------
def scanlines():
    w, h = 64, 1280
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">']
    for y in range(0, h, 4):
        s.append(f'<rect x="0" y="{y}" width="{w}" height="1.6" fill="#000" fill-opacity="0.55"/>')
    s.append("</svg>")
    render("".join(s), OUT / "terminal/images/scanlines.png")

# --- Old book: a seal ----------------------------------------------------------------------
def seal():
    size = 160
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}">',
         f'<rect x="8" y="8" width="144" height="144" rx="10" fill="#a33a2c"/>',
         f'<rect x="18" y="18" width="124" height="124" rx="4" fill="none" stroke="#f4e6c8" stroke-width="5"/>',
         f'<text x="80" y="76" font-family="serif" font-size="52" font-weight="bold" text-anchor="middle" fill="#f4e6c8">v</text>',
         f'<text x="80" y="128" font-family="serif" font-size="44" font-weight="bold" text-anchor="middle" fill="#f4e6c8">Book</text>',
         "</svg>"]
    render("".join(s), OUT / "co_thu/images/seal.png")

import os
for f in os.environ.get("ONLY", "stars moons compass chart scanlines seal").split():
    globals()[f]()
print("ok")
