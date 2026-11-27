"""Pictures of the skins ported from Archive's templates and the new ones: own work, CC0 (drawn
as SVG here, rendered by ImageMagick). Usage: python3 gen_assets2.py <skins/src> [names…]"""
import math, random, subprocess, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from chrome_render import chrome_render

OUT = pathlib.Path(sys.argv[1])
FONT = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"

def render(svg_text, target, *args):
    chrome_render(svg_text, OUT / target)

def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">{"".join(body)}</svg>'

# ------------------------------------------------------------------------- gilded corners
def gilded():
    gold, light = "#bc984f", "#e2c786"
    def corner(flip_x, flip_y):
        s = 200
        tx = f"translate({s if flip_x else 0},{s if flip_y else 0}) scale({-1 if flip_x else 1},{-1 if flip_y else 1})"
        b = [f'<g transform="{tx}" fill="none" stroke="{gold}" stroke-linecap="round">',
             f'<path d="M8 192 L8 40 Q8 8 40 8 L192 8" fill="none" stroke="{gold}" stroke-width="3"/>',
             f'<path d="M20 192 L20 52 Q20 20 52 20 L192 20" fill="none" stroke="{gold}" stroke-width="1.2"/>',
             # a scroll curling out of the corner, with leaves
             f'<path d="M20 20 C60 30 70 70 50 90 C38 102 22 92 30 78 C36 68 50 72 48 82" fill="none" stroke="{gold}" stroke-width="2.2"/>',
             f'<path d="M20 20 C30 60 70 70 90 50 C102 38 92 22 78 30 C68 36 72 50 82 48" fill="none" stroke="{gold}" stroke-width="2.2"/>',
             f'<path d="M96 22 q18 -10 34 0 q-18 10 -34 0 Z" fill="{light}" stroke="{gold}" stroke-width="1"/>',
             f'<path d="M22 96 q-10 18 0 34 q10 -18 0 -34 Z" fill="{light}" stroke="{gold}" stroke-width="1"/>',
             f'<circle cx="40" cy="40" r="5" fill="{gold}" stroke="none"/>',
             f'<path d="M140 8 l6 -6 l6 6 l-6 6 Z" fill="{gold}" stroke="none"/>',
             f'<path d="M8 140 l-6 6 l6 6 l6 -6 Z" fill="{gold}" stroke="none"/>',
             '</g>']
        return svg(s, s, b)
    for name, fx, fy in [("nw", 0, 0), ("ne", 1, 0), ("sw", 0, 1), ("se", 1, 1)]:
        render(corner(fx, fy), f"hoa_tien/images/corner-{name}.png")

# ------------------------------------------------------------------------- magazine art
def magazine():
    ink, red = "#1d1d1f", "#c8102e"
    b = [f'<g fill="none" stroke="{ink}" stroke-width="2">',
         '<circle cx="222" cy="138" r="106"/><circle cx="222" cy="138" r="74"/>',
         '<path d="M44 314 L314 44 M72 342 L342 72 M16 286 L286 16 M22 230 H338 M130 22 V338"/></g>',
         f'<circle cx="222" cy="138" r="30" fill="{red}"/>']
    render(svg(360, 360, b), "tap_chi/images/art.png")

# ------------------------------------------------------------------------- pixel world
P = 4  # one art pixel = 4 image px

def px(grid, palette, w, h, ox=0, oy=0):
    out = []
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch in palette and palette[ch]:
                out.append(f'<rect x="{(ox + x) * P}" y="{(oy + y) * P}" width="{P}" height="{P}" fill="{palette[ch]}"/>')
    return out

SUN = ["..yyyyyy..", ".yYYYYYYy.", "yYYWWWWYYy", "yYWWWWWWYy", "yYWWWWWWYy", "yYWWWWWWYy", "yYWWWWWWYy", "yYYWWWWYYy", ".yYYYYYYy.", "..yyyyyy.."]
MOON = ["..gggggg..", ".gGGGGGGg.", "gGGGgGGGGg", "gGGGGGGgGg", "gGgGGGGGGg", "gGGGGGGGGg", "gGGGGgGGGg", "gGGGGGGGGg", ".gGGGGGGg.", "..gggggg.."]

def pixel():
    global P
    w_art, h_art = 120, 22  # a strip 960 x 176 px: drawn big, so it isn't blurred much scaled up
    P = 8
    for hour in range(24):
        b = []
        day = 6 <= hour < 18
        t = ((hour - 6) / 12.0) if day else (((hour - 18) % 24) / 12.0)
        x = int(4 + t * (w_art - 14))
        y = int(11 - math.sin(t * math.pi) * 10)
        if day:
            b += px(SUN, {"y": "#f7b733", "Y": "#ffd84a", "W": "#fff3a0"}, 10, 10, x, y)
        else:
            b += px(MOON, {"g": "#9aa3b8", "G": "#dfe4ee"}, 10, 10, x, y)
        render(svg(w_art * P, h_art * P, b), f"khoi/sky/sky-{hour:02d}.png")
    P = 4
    # the land: blocks of grass over dirt and stone, a few trees, a lake
    rnd = random.Random(5)
    W, H = 160, 26
    b = []
    heights = []
    hgt = 12
    for x in range(W):
        if rnd.random() < 0.18: hgt = max(8, min(16, hgt + rnd.choice([-1, 1])))
        heights.append(hgt)
    lake = range(96, 112)
    for x, top in enumerate(heights):
        for y in range(top, H):
            if x in lake and y < 17:
                if y >= 14: b.append(f'<rect x="{x*P}" y="{y*P}" width="{P}" height="{P}" fill="{"#3f76e4" if (x + y) % 3 else "#5b8cf0"}"/>')
                continue
            d = y - top
            if d == 0: c = rnd.choice(["#5a9e3a", "#64ad40", "#4f8f33"])
            elif d < 4: c = rnd.choice(["#8a5a35", "#7a4e2d", "#94643c"])
            else: c = rnd.choice(["#7d7d7d", "#888888", "#6f6f6f"]) if rnd.random() > 0.012 else "#3fb8c9"
            b.append(f'<rect x="{x*P}" y="{y*P}" width="{P}" height="{P}" fill="{c}"/>')
    for tx in (14, 47, 70, 128, 146):
        top = heights[tx]
        for y in range(top - 5, top): b.append(f'<rect x="{tx*P}" y="{y*P}" width="{P}" height="{P}" fill="#6b4a2b"/>')
        for dx in range(-2, 3):
            for dy in range(-9, -4):
                if abs(dx) == 2 and dy in (-9, -5): continue
                c = rnd.choice(["#3c7a2a", "#467f2f", "#2f6a24"])
                b.append(f'<rect x="{(tx+dx)*P}" y="{(top+dy)*P}" width="{P}" height="{P}" fill="{c}"/>')
    render(svg(W * P, H * P, b), "khoi/images/land.png")
    # the hotbar: nine slots, item icons, the selected slot framed
    ICONS = {
        "apple": (["...g..", "..g...", ".rrrr.", "rrrrWr", "rrrrrr", "rrrrrr", ".rrrr.", "..rr.."], {"g": "#3b7a2a", "r": "#d33b2f", "W": "#ff9c8f"}),
        "book": (["bbbbbb", "bWWWWb", "bWbbWb", "bWWWWb", "bWbbWb", "bWWWWb", "bbbbbb", "......"], {"b": "#7a3b22", "W": "#e9dcc0"}),
        "gem": (["..cc..", ".cCCc.", "cCWCCc", "cCCCCc", ".cCCc.", "..cc..", "......", "......"], {"c": "#1e9e8f", "C": "#4fe0cf", "W": "#e6fffb"}),
        "heart": ([".rr.rr", "rRRrRR", "rRRRRR", "rRRRRR", ".rRRRr", "..rRr.", "...r..", "......"], {"r": "#a3201c", "R": "#ea3b30"}),
        "map": (["pppppp", "pggppp", "pgggpp", "ppgbbp", "pppbbp", "pprppp", "pppppp", "......"], {"p": "#e9d9a6", "g": "#6aa04a", "b": "#4c7fd9", "r": "#d33b2f"}),
        "key": (["..yy..", ".y..y.", "..yy..", "..y...", "..yy..", "..y...", "..yy..", "......"], {"y": "#e8b830"}),
        "potion": (["..ww..", "..ww..", ".gggg.", "gmmmmg", "gmMmmg", "gmmmmg", ".gggg.", "......"], {"w": "#b08a5a", "g": "#cfe8f2", "m": "#a54bd6", "M": "#e2b0ff"}),
        "star": (["..y...", "..y...", "yyYyy.", ".yYy..", ".y.y..", "y...y.", "......", "......"], {"y": "#e8b830", "Y": "#fff2a0"}),
        "torch": (["..o...", ".oyo..", "..y...", "..b...", "..b...", "..b...", "..b...", "......"], {"o": "#ff8a1f", "y": "#ffe066", "b": "#7a5230"}),
    }
    names = list(ICONS)
    slot, inner = 20, 16
    for sel in range(9):
        b = [f'<rect x="0" y="0" width="{9*slot*P+2*P}" height="{(slot+2)*P}" fill="#000" fill-opacity="0.55"/>']
        for i, n in enumerate(names):
            x0 = P + i * slot * P
            b.append(f'<rect x="{x0 + P}" y="{2*P}" width="{(slot-2)*P}" height="{(slot-2)*P}" fill="#8b8b8b" fill-opacity="0.55" stroke="#2b2b2b" stroke-width="{P/2}"/>')
            grid, pal = ICONS[n]
            b += px(grid, pal, 6, 8, (x0 // P) + 4, 5)
        x0 = P + sel * slot * P
        b.append(f'<rect x="{x0 - P/2}" y="{P/2}" width="{slot*P + P}" height="{(slot+1)*P}" fill="none" stroke="#ffffff" stroke-width="{P}"/>')
        render(svg(9 * slot * P + 2 * P, (slot + 2) * P, b), f"khoi/hotbar/hotbar-{sel}.png")

# ------------------------------------------------------------------------- red sync
def sync():
    red, gold, ink = "#b42d2d", "#d8ba7e", "#f5f0e7"
    # rings of an orbit, ticks round them
    b = ['<g fill="none">', f'<circle cx="160" cy="160" r="150" stroke="{ink}" stroke-opacity="0.5" stroke-width="2"/>',
         f'<circle cx="160" cy="160" r="118" stroke="{gold}" stroke-width="3" stroke-dasharray="14 8"/>',
         f'<circle cx="160" cy="160" r="86" stroke="{ink}" stroke-opacity="0.35" stroke-width="1.5"/>', '</g>']
    for d in range(0, 360, 6):
        a = math.radians(d); r1 = 140 if d % 30 else 128
        b.append(f'<line x1="{160 + r1*math.cos(a):.1f}" y1="{160 + r1*math.sin(a):.1f}" x2="{160 + 150*math.cos(a):.1f}" y2="{160 + 150*math.sin(a):.1f}" stroke="{ink}" stroke-opacity="0.6" stroke-width="{2 if d % 30 == 0 else 1}"/>')
    b.append(f'<circle cx="{160 + 118*math.cos(-0.8):.1f}" cy="{160 + 118*math.sin(-0.8):.1f}" r="7" fill="{gold}"/>')
    render(svg(320, 320, b), "dong_bo/images/orbit.png")
    # hazard rules: slanted stripes across a band
    b = [f'<rect width="600" height="40" fill="none"/>']
    for x in range(-40, 640, 28):
        b.append(f'<polygon points="{x},40 {x+14},40 {x+34},0 {x+20},0" fill="{ink}" fill-opacity="0.9"/>')
    render(svg(600, 40, b), "dong_bo/images/stripes.png")
    # the wave: nine bars, a frame per page
    rnd = random.Random(2)
    for f in range(9):
        b = []
        for i in range(9):
            hgt = 8 + int(abs(math.sin((i + f * 1.7) * 0.9)) * 40 + rnd.uniform(0, 8))
            b.append(f'<rect x="{i*12}" y="{56-hgt}" width="7" height="{hgt}" fill="{gold if i == f else ink}" fill-opacity="{1 if i == f else 0.75}"/>')
        render(svg(106, 56, b), f"dong_bo/wave/wave-{f}.png")

# ------------------------------------------------------------------------- blue day
def blue_day():
    def cloud(cx, cy, s):
        return (f'<g fill="#ffffff"><circle cx="{cx}" cy="{cy}" r="{22*s}"/><circle cx="{cx+26*s}" cy="{cy-10*s}" r="{28*s}"/>'
                f'<circle cx="{cx+56*s}" cy="{cy}" r="{22*s}"/><rect x="{cx}" y="{cy}" width="{56*s}" height="{22*s}"/></g>')
    b = [cloud(40, 70, 1.0), cloud(250, 46, 0.7), cloud(420, 82, 1.2), cloud(600, 56, 0.8)]
    render(svg(720, 120, b), "ngay_xanh/images/clouds.png")
    b = [f'<circle cx="60" cy="60" r="56" fill="#ffe28b" fill-opacity="0.35"/>', f'<circle cx="60" cy="60" r="40" fill="#ffda59"/>',
         f'<circle cx="60" cy="60" r="30" fill="#ffe994"/>']
    render(svg(120, 120, b), "ngay_xanh/images/sun.png")
    b = [f'<circle cx="60" cy="60" r="54" fill="#fff3db" fill-opacity="0.18"/>', f'<circle cx="60" cy="60" r="36" fill="#fff3db"/>',
         f'<circle cx="76" cy="50" r="32" fill="#1f3566"/>']
    render(svg(120, 120, b), "ngay_xanh/images/moon.png")
    rnd = random.Random(11)
    b = [f'<circle cx="{rnd.uniform(0,720):.0f}" cy="{rnd.uniform(0,1280):.0f}" r="{rnd.choice([1,1.2,1.6,2.2])}" fill="#fff8e0" fill-opacity="{rnd.uniform(.4,1):.2f}"/>' for _ in range(160)]
    render(svg(720, 1280, b), "ngay_xanh/images/stars.png")

for name in (sys.argv[2:] or ["gilded", "magazine", "pixel", "sync", "blue_day"]):
    globals()[name]()
print("ok")
