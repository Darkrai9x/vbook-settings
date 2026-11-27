"""Pictures of the original skins (own work, CC0), drawn as SVG and rendered with Chrome."""
import math, random, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from chrome_render import chrome_render
OUT = pathlib.Path(sys.argv[1])

def render(svg_text, target):
    chrome_render(svg_text, OUT / target)

def svg(w, h, body, defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><defs>{defs}</defs>{"".join(body)}</svg>'

# ------------------------------------------------------------------ Art Deco
def deco():
    gold = "#d4af37"; pale = "#f1d98a"
    grad = f'<linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{pale}"/><stop offset="1" stop-color="{gold}"/></linearGradient>'
    # the sunburst fan over the masthead
    w, h = 480, 200
    cx, cy = w / 2, h - 6
    b = []
    for i in range(19):
        a0 = math.pi + i * math.pi / 19
        a1 = a0 + math.pi / 19 * 0.55
        r = 180 if i % 2 == 0 else 150
        b.append(f'<path d="M{cx} {cy} L{cx + r*math.cos(a0):.1f} {cy + r*math.sin(a0):.1f} A{r} {r} 0 0 1 {cx + r*math.cos(a1):.1f} {cy + r*math.sin(a1):.1f} Z" fill="url(#g)" fill-opacity="{0.9 if i % 2 == 0 else 0.55}"/>')
    for r in (60, 72, 84):
        b.append(f'<path d="M{cx - r} {cy} A{r} {r} 0 0 1 {cx + r} {cy}" fill="none" stroke="{gold}" stroke-width="{3 if r == 60 else 1.5}"/>')
    b.append(f'<path d="M{cx - 52} {cy} A52 52 0 0 1 {cx + 52} {cy} Z" fill="#0f0f12"/>')
    b.append(f'<path d="M{cx - 40} {cy} A40 40 0 0 1 {cx + 40} {cy} Z" fill="url(#g)"/>')
    b.append(f'<line x1="0" y1="{cy + 3}" x2="{w}" y2="{cy + 3}" stroke="{gold}" stroke-width="3"/>')
    render(svg(w, h, b, grad), "art_deco/images/fan.png")
    # a stepped corner
    def corner(fx, fy):
        s = 180
        t = f"translate({s if fx else 0},{s if fy else 0}) scale({-1 if fx else 1},{-1 if fy else 1})"
        p = [f'<g transform="{t}">',
             f'<path d="M4 176 V4 H176" fill="none" stroke="{gold}" stroke-width="3"/>',
             f'<path d="M16 176 V36 H36 V16 H176" fill="none" stroke="{gold}" stroke-width="1.5"/>',
             f'<path d="M28 120 V48 H48 V28 H120" fill="none" stroke="{gold}" stroke-width="1"/>',
             f'<rect x="10" y="10" width="14" height="14" transform="rotate(45 17 17)" fill="{gold}"/>',
             f'<path d="M60 4 l8 10 l8 -10" fill="none" stroke="{gold}" stroke-width="1.5"/>',
             f'<path d="M4 60 l10 8 l-10 8" fill="none" stroke="{gold}" stroke-width="1.5"/>', '</g>']
        return svg(s, s, p)
    for n, fx, fy in [("nw", 0, 0), ("ne", 1, 0), ("sw", 0, 1), ("se", 1, 1)]:
        render(corner(fx, fy), f"art_deco/images/corner-{n}.png")
    # the divider: a diamond between chevrons
    b = [f'<line x1="0" y1="20" x2="150" y2="20" stroke="{gold}" stroke-width="1.5"/>', f'<line x1="210" y1="20" x2="360" y2="20" stroke="{gold}" stroke-width="1.5"/>',
         f'<path d="M150 20 l10 -8 l10 8 l-10 8 Z M190 20 l10 -8 l10 8 l-10 8 Z" fill="none" stroke="{gold}" stroke-width="1.5"/>',
         f'<rect x="172" y="12" width="16" height="16" transform="rotate(45 180 20)" fill="url(#g)"/>']
    render(svg(360, 40, b, grad), "art_deco/images/divider.png")

# ------------------------------------------------------------------ Ink wash
def ink():
    w, h = 1820, 260  # wide as a page's head on a phone or a spread: cut at the sides, never the sky
    defs = ('<filter id="soft" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="4"/></filter>'
            '<filter id="mist" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="10"/></filter>')
    rnd = random.Random(8)
    def ridge(base, amp, seed, step=6):
        # peaks from a few sines of random phase: mountains, not a flat band
        r = random.Random(seed)
        waves = [(r.uniform(0.004, 0.009), r.uniform(0, 6.3), 1.0), (r.uniform(0.012, 0.02), r.uniform(0, 6.3), 0.45), (r.uniform(0.03, 0.05), r.uniform(0, 6.3), 0.15)]
        pts = [f"M0 {h}"]
        for x in range(0, w + step, step):
            y = base - amp * sum(k * (0.5 + 0.5 * math.sin(f * x + ph)) for f, ph, k in waves) / 1.6
            pts.append(f"L{x} {y:.0f}")
        pts.append(f"L{w} {h} Z")
        return " ".join(pts)
    b = [f'<path d="{ridge(200, 110, 1)}" fill="#2b2b2b" fill-opacity="0.18" filter="url(#mist)"/>',
         f'<path d="{ridge(215, 90, 2)}" fill="#2b2b2b" fill-opacity="0.32" filter="url(#soft)"/>',
         f'<path d="{ridge(235, 60, 3)}" fill="#1e1e1e" fill-opacity="0.62" filter="url(#soft)"/>',
         f'<path d="{ridge(252, 26, 4)}" fill="#111" fill-opacity="0.85"/>',
         f'<rect x="0" y="206" width="{w}" height="30" fill="#f3eee2" fill-opacity="0.3" filter="url(#mist)"/>']
    # a few pines on the nearest ridge
    for px_ in (90, 130, 560, 610, 640, 1180, 1230, 1600, 1650):
        b.append(f'<path d="M{px_} 236 l-12 0 l12 -30 l12 30 Z M{px_} 222 l-9 0 l9 -22 l9 22 Z" fill="#111" fill-opacity="0.9"/>')
    # birds
    for (bx, by) in [(1020, 70), (1046, 82), (1070, 64)]:
        b.append(f'<path d="M{bx} {by} q6 -6 12 0 q6 -6 12 0" fill="none" stroke="#222" stroke-width="2"/>')
    render(svg(w, h, b, defs), "thuy_mac/images/mountains.webp")
    # the vermilion moon / sun disc
    render(svg(120, 120, ['<circle cx="60" cy="60" r="52" fill="#c0392b" fill-opacity="0.9"/>', '<circle cx="60" cy="60" r="58" fill="#c0392b" fill-opacity="0.12"/>']), "thuy_mac/images/sun.png")
    # a seal: 山水 carved in white
    b = ['<rect x="6" y="6" width="108" height="108" rx="8" fill="#b8312a"/>',
         '<rect x="14" y="14" width="92" height="92" rx="3" fill="none" stroke="#f6e9d8" stroke-width="3"/>',
         '<text x="60" y="56" font-family="Songti SC, STSong, serif" font-size="40" font-weight="bold" text-anchor="middle" fill="#f6e9d8">山</text>',
         '<text x="60" y="98" font-family="Songti SC, STSong, serif" font-size="40" font-weight="bold" text-anchor="middle" fill="#f6e9d8">水</text>']
    render(svg(120, 120, b), "thuy_mac/images/seal.png")

# ------------------------------------------------------------------ Sakura
def sakura():
    def flower(x, y, r, rot, fill="#f8c8d4", edge="#e89aae", center="#d0546f"):
        p = [f'<g transform="translate({x},{y}) rotate({rot})">']
        for i in range(5):
            a = i * 72
            p.append(f'<path transform="rotate({a})" d="M0 0 C{-r*0.55} {-r*0.4} {-r*0.5} {-r*1.05} 0 {-r} C{r*0.5} {-r*1.05} {r*0.55} {-r*0.4} 0 0 Z" fill="{fill}" stroke="{edge}" stroke-width="0.8"/>')
            p.append(f'<path transform="rotate({a})" d="M0 {-r} l-3 -4 M0 {-r} l3 -4" stroke="{edge}" stroke-width="1"/>')
        p.append(f'<circle r="{r*0.22}" fill="{center}"/>')
        for i in range(6):
            a = math.radians(i * 60 + rot)
            p.append(f'<circle cx="{math.cos(a)*r*0.4:.1f}" cy="{math.sin(a)*r*0.4:.1f}" r="1.6" fill="#a8324f"/>')
        p.append('</g>')
        return "".join(p)
    w, h = 420, 300
    b = ['<path d="M420 20 C330 30 280 60 220 70 C170 80 120 70 60 110" fill="none" stroke="#5b3a33" stroke-width="9" stroke-linecap="round"/>',
         '<path d="M300 44 C290 90 270 120 240 150" fill="none" stroke="#5b3a33" stroke-width="5" stroke-linecap="round"/>',
         '<path d="M180 76 C170 110 150 130 120 150" fill="none" stroke="#5b3a33" stroke-width="4" stroke-linecap="round"/>']
    rnd = random.Random(4)
    spots = [(390, 30, 22), (350, 50, 18), (310, 36, 20), (270, 62, 24), (300, 90, 17), (250, 140, 21), (210, 66, 18),
             (160, 92, 22), (125, 146, 18), (90, 98, 19), (60, 112, 16), (230, 110, 14)]
    for (x, y, r) in spots:
        b.append(flower(x, y, r, rnd.uniform(0, 72)))
    for (x, y) in [(330, 70), (190, 100), (140, 120), (280, 110)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#f4a6ba"/>')
    render(svg(w, h, b), "anh_dao/images/branch.png")
    # petals drifting down the page
    rnd = random.Random(12)
    b = []
    for _ in range(26):
        x, y, s, rot = rnd.uniform(0, 720), rnd.uniform(0, 1280), rnd.uniform(5, 11), rnd.uniform(0, 360)
        b.append(f'<path transform="translate({x:.0f},{y:.0f}) rotate({rot:.0f})" d="M0 0 C{-s*0.6:.1f} {-s*0.5:.1f} {-s*0.5:.1f} {-s*1.2:.1f} 0 {-s:.1f} C{s*0.5:.1f} {-s*1.2:.1f} {s*0.6:.1f} {-s*0.5:.1f} 0 0 Z" fill="#f6b9c8" fill-opacity="{rnd.uniform(0.5, 0.9):.2f}"/>')
    render(svg(720, 1280, b), "anh_dao/images/petals.png")
    render(svg(60, 60, [flower(30, 30, 24, 10)]), "anh_dao/images/flower.png")

# ------------------------------------------------------------------ Notebook
def notebook():
    # the spiral binding across the top
    w, h = 720, 70
    b = []
    for x in range(24, w, 36):
        b.append(f'<circle cx="{x}" cy="46" r="7" fill="#2a2a2a" fill-opacity="0.75"/>')
        b.append(f'<path d="M{x-4} 46 C{x-6} 10 {x+10} 6 {x+8} 30" fill="none" stroke="#9aa0a8" stroke-width="5" stroke-linecap="round"/>')
        b.append(f'<path d="M{x-4} 46 C{x-6} 10 {x+10} 6 {x+8} 30" fill="none" stroke="#e8ecf0" stroke-width="2" stroke-linecap="round"/>')
    render(svg(w, h, b), "vo_hoc_tro/images/spiral.png")
    # graph paper: a fine grid with a stronger line every fifth
    w, h = 720, 1280
    b = []
    for i, x in enumerate(range(0, w + 1, 24)):
        b.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="#7fb3e0" stroke-opacity="{0.55 if i % 4 == 0 else 0.25}" stroke-width="1"/>')
    for i, y in enumerate(range(0, h + 1, 24)):
        b.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="#7fb3e0" stroke-opacity="{0.55 if i % 4 == 0 else 0.25}" stroke-width="1"/>')
    render(svg(w, h, b), "vo_hoc_tro/images/grid.png")
    # doodles: a star, a heart, a tiny rocket, a smiley sun
    stroke = 'fill="none" stroke="#3a6fd8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"'
    star = f'<path d="M40 8 L48 30 L72 30 L52 44 L60 68 L40 54 L20 68 L28 44 L8 30 L32 30 Z" {stroke}/>'
    render(svg(80, 80, [star]), "vo_hoc_tro/images/star.png")
    sun = (f'<circle cx="40" cy="40" r="16" {stroke}/>' + "".join(
        f'<line x1="{40 + 22*math.cos(math.radians(a)):.1f}" y1="{40 + 22*math.sin(math.radians(a)):.1f}" x2="{40 + 32*math.cos(math.radians(a)):.1f}" y2="{40 + 32*math.sin(math.radians(a)):.1f}" {stroke}/>'
        for a in range(0, 360, 45)) + f'<path d="M33 44 q7 6 14 0" {stroke}/><circle cx="34" cy="36" r="1.5" fill="#3a6fd8"/><circle cx="46" cy="36" r="1.5" fill="#3a6fd8"/>')
    render(svg(80, 80, [sun]), "vo_hoc_tro/images/sun.png")
    # chalk versions for the blackboard night
    chalk = stroke.replace("#3a6fd8", "#f4f1e8")
    render(svg(80, 80, [star.replace(stroke, chalk)]), "vo_hoc_tro/images/star-chalk.png")
    render(svg(80, 80, [sun.replace(stroke, chalk).replace('#3a6fd8', '#f4f1e8')]), "vo_hoc_tro/images/sun-chalk.png")

# ------------------------------------------------------------------ Autumn
def autumn():
    def maple(x, y, s, rot, fill):
        pts = []
        # a seven-lobed maple outline from polar points
        lobes = [(0, 1.0), (25, 0.45), (45, 0.85), (70, 0.4), (95, 0.62), (125, 0.3), (155, 0.12), (180, 0.08)]
        full = lobes + [(360 - a, r) for a, r in reversed(lobes[1:-1])]
        for a, r in full:
            rad = math.radians(a - 90)
            pts.append(f"{math.cos(rad)*r*s:.1f},{math.sin(rad)*r*s:.1f}")
        return (f'<g transform="translate({x},{y}) rotate({rot})"><polygon points="{" ".join(pts)}" fill="{fill}"/>'
                f'<path d="M0 {s*0.15:.1f} L0 {s*0.7:.1f}" stroke="#6b3a1f" stroke-width="{max(1.5, s/18):.1f}"/>'
                f'<path d="M0 0 L0 {-s*0.85:.1f} M0 0 L{s*0.6:.1f} {-s*0.4:.1f} M0 0 L{-s*0.6:.1f} {-s*0.4:.1f}" stroke="#000" stroke-opacity="0.18" stroke-width="1.2"/></g>')
    colors = ["#c4421a", "#d9661f", "#e8a33a", "#a8321b", "#d14f24", "#b8741e"]
    rnd = random.Random(9)
    b = []
    for (x, y, s) in [(300, 60, 56), (350, 120, 44), (240, 40, 40), (380, 40, 34), (200, 90, 30), (320, 170, 28), (270, 130, 36)]:
        b.append(maple(x, y, s, rnd.uniform(-40, 40), rnd.choice(colors)))
    render(svg(420, 240, b), "mua_thu/images/leaves.png")
    b = []
    for _ in range(12):
        b.append(maple(rnd.uniform(20, 700), rnd.uniform(20, 1260), rnd.uniform(10, 20), rnd.uniform(0, 360), rnd.choice(colors)))
    render(svg(720, 1280, b), "mua_thu/images/fall.png")

for name in (sys.argv[2:] or ["deco", "ink", "sakura", "notebook", "autumn"]):
    globals()[name]()
print("ok")
