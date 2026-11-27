"""Pictures of the seasonal skins (own work, CC0), drawn as SVG and rendered with Chrome."""
import math, random, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from chrome_render import chrome_render
OUT = pathlib.Path(sys.argv[1])

def render(svg_text, target): chrome_render(svg_text, OUT / target)
def svg(w, h, body, defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><defs>{defs}</defs>{"".join(body)}</svg>'

def snowflake(x, y, r, color="#ffffff", width=2.0, op=1.0):
    p = [f'<g transform="translate({x:.0f},{y:.0f})" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-opacity="{op:.2f}" fill="none">']
    for i in range(6):
        a = math.radians(i * 60)
        ex, ey = math.cos(a) * r, math.sin(a) * r
        p.append(f'<line x1="0" y1="0" x2="{ex:.1f}" y2="{ey:.1f}"/>')
        for k in (0.5, 0.75):
            bx, by = math.cos(a) * r * k, math.sin(a) * r * k
            for s in (-1, 1):
                b2 = a + s * math.radians(45)
                p.append(f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx + math.cos(b2) * r * 0.25:.1f}" y2="{by + math.sin(b2) * r * 0.25:.1f}"/>')
    p.append('</g>')
    return "".join(p)

# ------------------------------------------------------------------ Halloween
def halloween():
    defs = ('<radialGradient id="moon" cx="0.45" cy="0.4" r="0.6"><stop offset="0" stop-color="#fff6d6"/><stop offset="1" stop-color="#f2c76b"/></radialGradient>'
            '<radialGradient id="glow" r="0.5"><stop offset="0" stop-color="#ffcf6b" stop-opacity="0.5"/><stop offset="1" stop-color="#ffcf6b" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="pump" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff9a2e"/><stop offset="1" stop-color="#d9590f"/></linearGradient>')
    # the moon with a bare branch and bats across it
    b = ['<circle cx="160" cy="130" r="120" fill="url(#glow)"/>', '<circle cx="160" cy="130" r="78" fill="url(#moon)"/>',
         '<circle cx="132" cy="110" r="12" fill="#e9b85a" fill-opacity="0.35"/><circle cx="182" cy="150" r="9" fill="#e9b85a" fill-opacity="0.3"/>',
         '<path d="M0 60 C60 70 90 90 130 80 M80 74 C90 50 100 40 120 34 M40 64 C44 90 36 104 22 118 M110 82 C126 96 140 98 158 96" fill="none" stroke="#1a1020" stroke-width="5" stroke-linecap="round"/>']
    def bat(x, y, s):
        return (f'<path transform="translate({x},{y}) scale({s})" d="M0 0 C-6 -8 -16 -10 -26 -4 C-20 -2 -18 4 -20 8 C-14 4 -8 6 -6 10 C-4 4 -2 2 0 4 '
                f'C2 2 4 4 6 10 C8 6 14 4 20 8 C18 4 20 -2 26 -4 C16 -10 6 -8 0 0 Z M-3 -2 l1 -5 l2 3 l2 -3 l1 5 Z" fill="#1a1020"/>')
    b += [bat(230, 70, 1.4), bat(268, 104, 1.0), bat(206, 116, 0.8)]
    render(svg(320, 260, b, defs), "halloween/images/moon.png")
    # pumpkins with carved faces
    def pumpkin(x, y, s, face):
        p = [f'<g transform="translate({x},{y}) scale({s})">',
             '<path d="M-4 -46 C-4 -60 6 -66 14 -64 C8 -58 6 -52 6 -44 Z" fill="#4f6b2b"/>']
        for dx, rx in [(-26, 26), (26, 26), (-10, 24), (10, 24), (0, 22)]:
            p.append(f'<ellipse cx="{dx}" cy="0" rx="{rx}" ry="44" fill="url(#pump)" stroke="#b9470c" stroke-width="2"/>')
        if face:
            p.append('<path d="M-26 -10 l10 -14 l10 14 Z M6 -10 l10 -14 l10 14 Z M-4 2 l4 -8 l4 8 Z" fill="#ffd36b"/>')
            p.append('<path d="M-30 14 Q0 40 30 14 L22 18 L16 12 L8 20 L0 12 L-8 20 L-16 12 L-22 18 Z" fill="#ffd36b"/>')
        p.append('</g>')
        return "".join(p)
    b = [pumpkin(70, 80, 1.0, True), pumpkin(150, 96, 0.62, False), pumpkin(205, 92, 0.75, True)]
    b.append('<ellipse cx="140" cy="132" rx="140" ry="8" fill="#000" fill-opacity="0.25"/>')
    render(svg(280, 140, b, defs), "halloween/images/pumpkins.png")
    # a cobweb for a corner
    b = ['<g stroke="#e8dff5" stroke-opacity="0.75" fill="none" stroke-width="1.4">']
    for i in range(7):
        a = math.radians(i * 15)
        b.append(f'<line x1="0" y1="0" x2="{math.cos(a)*170:.1f}" y2="{math.sin(a)*170:.1f}"/>')
    for r in (34, 62, 92, 124, 156):
        pts = []
        for i in range(7):
            a = math.radians(i * 15)
            pts.append((math.cos(a) * r, math.sin(a) * r))
        d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}" + "".join(
            f" Q{(pts[i][0]+pts[i+1][0])/2*0.9:.1f} {(pts[i][1]+pts[i+1][1])/2*0.9:.1f} {pts[i+1][0]:.1f} {pts[i+1][1]:.1f}" for i in range(6))
        b.append(f'<path d="{d}"/>')
    b.append('</g><line x1="120" y1="120" x2="120" y2="150" stroke="#e8dff5" stroke-width="1"/><circle cx="120" cy="156" r="6" fill="#1a1020" stroke="#e8dff5" stroke-width="1"/>')
    render(svg(180, 180, b), "halloween/images/web.png")
    # turned to hang from the page's foot corner
    import subprocess
    web = OUT / "halloween/images/web.png"
    subprocess.run(["magick", str(web), "-flip", "-flop", str(web.with_name("web-se.png"))], check=True)
    web.unlink()
    # bats scattered over the page
    rnd = random.Random(31)
    b = [bat(rnd.uniform(40, 680), rnd.uniform(40, 1240), rnd.uniform(0.5, 1.1)).replace("#1a1020", "#1a1020\" fill-opacity=\"0.5") for _ in range(9)]
    render(svg(720, 1280, b), "halloween/images/bats.png")

# ------------------------------------------------------------------ Noel
def noel():
    defs = ('<radialGradient id="red" cx="0.35" cy="0.35" r="0.7"><stop offset="0" stop-color="#ff8a80"/><stop offset="0.5" stop-color="#d62a2a"/><stop offset="1" stop-color="#8e1414"/></radialGradient>'
            '<radialGradient id="gold" cx="0.35" cy="0.35" r="0.7"><stop offset="0" stop-color="#fff1b8"/><stop offset="0.5" stop-color="#e1b73b"/><stop offset="1" stop-color="#a77c12"/></radialGradient>'
            '<radialGradient id="green" cx="0.35" cy="0.35" r="0.7"><stop offset="0" stop-color="#9be3b0"/><stop offset="0.5" stop-color="#2e8b57"/><stop offset="1" stop-color="#14532d"/></radialGradient>')
    # a garland of pine with baubles across the top
    w, h = 720, 120
    rnd = random.Random(6)
    b = ['<path d="M-10 20 Q180 90 360 40 T730 30" fill="none" stroke="#1f5a34" stroke-width="22" stroke-linecap="round"/>']
    for t in range(0, 740, 9):
        y = 20 + 50 * math.sin(t / 720 * math.pi * 1.6) * (1 - t / 1400)
        for _ in range(2):
            a = rnd.uniform(0, 6.3); l = rnd.uniform(10, 18)
            b.append(f'<line x1="{t}" y1="{y:.0f}" x2="{t + math.cos(a)*l:.0f}" y2="{y + math.sin(a)*l:.0f}" stroke="{rnd.choice(["#2f7a46", "#1f5a34", "#3c8f55"])}" stroke-width="3" stroke-linecap="round"/>')
    for i, x in enumerate(range(50, 720, 95)):
        y = 20 + 50 * math.sin(x / 720 * math.pi * 1.6) * (1 - x / 1400)
        g = ["red", "gold", "green"][i % 3]
        b.append(f'<line x1="{x}" y1="{y:.0f}" x2="{x}" y2="{y + 26:.0f}" stroke="#c9a227" stroke-width="1.5"/>')
        b.append(f'<rect x="{x-5}" y="{y + 22:.0f}" width="10" height="7" rx="1" fill="#c9a227"/>')
        b.append(f'<circle cx="{x}" cy="{y + 42:.0f}" r="14" fill="url(#{g})"/>')
    render(svg(w, h, b, defs), "noel/images/garland.png")
    # holly for a corner
    def leaf(x, y, rot, s):
        return (f'<path transform="translate({x},{y}) rotate({rot}) scale({s})" d="M0 0 C10 -6 14 -2 20 -8 C22 -2 28 0 34 -4 C34 2 40 6 46 4 C42 12 46 16 52 18 '
                f'C44 22 40 26 40 32 C34 28 28 30 26 36 C22 30 16 30 10 34 C10 26 4 22 0 0 Z" fill="#1f6b3a" stroke="#0f3f22" stroke-width="1.5"/>')
    b = [leaf(60, 60, -30, 1.4), leaf(60, 60, 60, 1.3), leaf(60, 60, 170, 1.2),
         '<circle cx="56" cy="56" r="10" fill="url(#red)"/><circle cx="72" cy="62" r="9" fill="url(#red)"/><circle cx="62" cy="72" r="9" fill="url(#red)"/>']
    render(svg(140, 140, b, defs), "noel/images/holly.png")
    rnd = random.Random(17)
    b = [snowflake(rnd.uniform(20, 700), rnd.uniform(20, 1260), rnd.uniform(5, 13), op=rnd.uniform(0.35, 0.85), width=1.6) for _ in range(40)]
    b += [f'<circle cx="{rnd.uniform(0,720):.0f}" cy="{rnd.uniform(0,1280):.0f}" r="{rnd.uniform(1.2,3):.1f}" fill="#fff" fill-opacity="{rnd.uniform(.3,.8):.2f}"/>' for _ in range(90)]
    render(svg(720, 1280, b), "noel/images/snow.png")
    b = ['<path d="M60 8 l6 16 l17 0 l-14 10 l6 17 l-15 -10 l-15 10 l6 -17 l-14 -10 l17 0 Z" fill="url(#gold)"/>']
    render(svg(120, 60, b, defs), "noel/images/star.png")

# ------------------------------------------------------------------ Xuân (Tết)
def xuan():
    defs = ('<radialGradient id="lan" cx="0.4" cy="0.4" r="0.7"><stop offset="0" stop-color="#ff6a4d"/><stop offset="0.6" stop-color="#d81e1e"/><stop offset="1" stop-color="#8f0e0e"/></radialGradient>'
            '<radialGradient id="mai" cx="0.5" cy="0.5" r="0.6"><stop offset="0" stop-color="#fff3a6"/><stop offset="1" stop-color="#f5c518"/></radialGradient>')
    def lantern(x, y, s):
        return (f'<g transform="translate({x},{y}) scale({s})"><line x1="0" y1="-60" x2="0" y2="-34" stroke="#b8860b" stroke-width="2"/>'
                '<rect x="-14" y="-36" width="28" height="8" rx="2" fill="#e8b52e"/>'
                '<ellipse cx="0" cy="0" rx="34" ry="30" fill="url(#lan)"/>'
                '<path d="M-14 -28 Q-22 0 -14 28 M14 -28 Q22 0 14 28 M0 -30 V30" fill="none" stroke="#a31414" stroke-width="1.5"/>'
                '<rect x="-14" y="28" width="28" height="8" rx="2" fill="#e8b52e"/>'
                '<path d="M-8 36 V70 M-3 36 V74 M3 36 V74 M8 36 V70" stroke="#e8b52e" stroke-width="2"/>'
                '<text x="0" y="8" font-family="Songti SC, serif" font-size="22" font-weight="bold" text-anchor="middle" fill="#ffd54a">福</text></g>')
    b = [lantern(50, 70, 1.0), lantern(130, 90, 0.75)]
    render(svg(180, 180, b, defs), "xuan/images/lanterns.png")
    def mai(x, y, r):
        p = [f'<g transform="translate({x},{y})">']
        for i in range(5):
            a = math.radians(i * 72 - 90)
            p.append(f'<circle cx="{math.cos(a)*r*0.55:.1f}" cy="{math.sin(a)*r*0.55:.1f}" r="{r*0.5:.1f}" fill="url(#mai)" stroke="#e0a800" stroke-width="0.8"/>')
        p.append(f'<circle r="{r*0.22:.1f}" fill="#e07a00"/>')
        for i in range(8):
            a = math.radians(i * 45)
            p.append(f'<line x1="0" y1="0" x2="{math.cos(a)*r*0.45:.1f}" y2="{math.sin(a)*r*0.45:.1f}" stroke="#c45f00" stroke-width="0.8"/>')
        p.append('</g>')
        return "".join(p)
    b = ['<path d="M0 30 C80 40 140 30 200 70 C250 100 300 90 360 120" fill="none" stroke="#4a3426" stroke-width="7" stroke-linecap="round"/>',
         '<path d="M120 36 C140 70 150 100 170 130 M240 92 C230 130 236 160 250 190" fill="none" stroke="#4a3426" stroke-width="4" stroke-linecap="round"/>']
    rnd = random.Random(3)
    for (x, y, r) in [(30, 34, 15), (70, 38, 13), (104, 34, 16), (146, 46, 14), (190, 64, 17), (226, 86, 13), (270, 98, 15), (320, 108, 14),
                      (136, 74, 13), (156, 110, 15), (236, 130, 13), (246, 172, 15), (350, 120, 11)]:
        b.append(mai(x, y, r))
    for (x, y) in [(88, 46), (208, 80), (300, 106), (168, 128)]:
        b.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#8bbf3a"/>')
    render(svg(380, 220, b, defs), "xuan/images/mai.png")
    rnd = random.Random(21)
    b = []
    for _ in range(20):
        x, y, r = rnd.uniform(20, 700), rnd.uniform(20, 1260), rnd.uniform(4, 8)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#f5c518" fill-opacity="{rnd.uniform(.4,.8):.2f}"/>')
    render(svg(720, 1280, b), "xuan/images/petals.png")

# ------------------------------------------------------------------ Hạ (summer: flame trees and the sea)
def ha():
    defs = ('<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4fc3f7"/><stop offset="1" stop-color="#0277bd"/></linearGradient>')
    w, h = 720, 110
    b = []
    for k, (col, base, amp, op) in enumerate([("#81d4fa", 40, 8, 0.8), ("#29b6f6", 58, 10, 0.9), ("url(#sea)", 76, 9, 1.0)]):
        d = f"M0 {h} L0 {base}" + "".join(f" Q{x + 30} {base - amp if (x // 60) % 2 == 0 else base + amp} {x + 60} {base}" for x in range(0, w, 60)) + f" L{w} {h} Z"
        b.append(f'<path d="{d}" fill="{col}" fill-opacity="{op}"/>')
    for x in range(20, w, 90):
        b.append(f'<path d="M{x} 50 q8 -6 16 0 q8 -6 16 0" fill="none" stroke="#ffffff" stroke-width="2" stroke-opacity="0.8"/>')
    render(svg(w, h, b, defs), "ha/images/waves.png")
    # a branch of flame-tree (phượng) blossoms with feathery leaves
    def bloom(x, y, r, rot):
        p = [f'<g transform="translate({x},{y}) rotate({rot})">']
        for i in range(5):
            a = i * 72
            fill = "#ffe0b2" if i == 0 else "#e53935"
            p.append(f'<ellipse transform="rotate({a})" cx="0" cy="{-r*0.6:.1f}" rx="{r*0.42:.1f}" ry="{r*0.6:.1f}" fill="{fill}" stroke="#b71c1c" stroke-width="0.8"/>')
        p.append(f'<circle r="{r*0.18:.1f}" fill="#b71c1c"/>')
        for i in range(6):
            a = math.radians(i * 60 + 20)
            p.append(f'<line x1="0" y1="0" x2="{math.cos(a)*r*0.9:.1f}" y2="{math.sin(a)*r*0.9:.1f}" stroke="#7f0000" stroke-width="1"/>')
        p.append('</g>')
        return "".join(p)
    def frond(x0, y0, x1, y1):
        p = [f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="#2e7d32" stroke-width="2"/>']
        n = 10
        for i in range(1, n):
            t = i / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            ang = math.atan2(y1 - y0, x1 - x0)
            for s in (-1, 1):
                a = ang + s * 1.2
                p.append(f'<ellipse cx="{x + math.cos(a)*6:.1f}" cy="{y + math.sin(a)*6:.1f}" rx="6" ry="2.4" transform="rotate({math.degrees(a):.0f} {x + math.cos(a)*6:.1f} {y + math.sin(a)*6:.1f})" fill="#43a047"/>')
        return "".join(p)
    b = ['<path d="M400 10 C320 20 260 40 200 70 C150 95 90 100 20 130" fill="none" stroke="#5d4037" stroke-width="8" stroke-linecap="round"/>']
    for (a, bb, c, d) in [(330, 26, 300, 90), (260, 46, 220, 110), (180, 80, 150, 150), (120, 100, 70, 160), (360, 18, 380, 80)]:
        b.append(frond(a, bb, c, d))
    rnd = random.Random(14)
    for (x, y, r) in [(380, 22, 18), (340, 34, 16), (300, 30, 18), (250, 54, 20), (214, 66, 16), (170, 86, 19), (130, 96, 16),
                      (90, 110, 18), (50, 124, 15), (280, 70, 14), (200, 100, 14)]:
        b.append(bloom(x, y, r, rnd.uniform(0, 72)))
    render(svg(420, 200, b), "ha/images/phuong.png")
    b = ['<circle cx="70" cy="70" r="64" fill="#ffe082" fill-opacity="0.35"/>', '<circle cx="70" cy="70" r="44" fill="#ffca28"/>', '<circle cx="70" cy="70" r="34" fill="#ffe082"/>']
    render(svg(140, 140, b), "ha/images/sun.png")

# ------------------------------------------------------------------ Đông (winter)
def dong():
    w, h = 720, 150
    rnd = random.Random(2)
    def pine(x, base, s, col):
        p = [f'<g transform="translate({x},{base}) scale({s})"><rect x="-4" y="-10" width="8" height="12" fill="#4e342e"/>']
        for i, (wd, y) in enumerate([(36, -10), (30, -30), (24, -48), (16, -64)]):
            p.append(f'<path d="M{-wd} {y} L0 {y - 30} L{wd} {y} Z" fill="{col}"/>')
            p.append(f'<path d="M{-wd*0.6:.0f} {y - 12} Q0 {y - 22} {wd*0.6:.0f} {y - 12} L0 {y - 30} Z" fill="#ffffff" fill-opacity="0.9"/>')
        p.append('</g>')
        return "".join(p)
    b = [f'<path d="M0 {h} L0 118 Q180 96 360 116 T720 110 L720 {h} Z" fill="#eef5fb"/>']
    for x in range(10, w, 46):
        s = rnd.uniform(0.6, 1.25)
        b.append(pine(x + rnd.uniform(-10, 10), 128 + rnd.uniform(-6, 6), s, rnd.choice(["#2e5d4b", "#244c3e", "#35695a"])))
    b.append(f'<path d="M0 {h} L0 134 Q200 120 380 136 T720 130 L720 {h} Z" fill="#ffffff"/>')
    render(svg(w, h, b), "dong/images/forest.png")
    rnd = random.Random(44)
    b = [snowflake(rnd.uniform(20, 700), rnd.uniform(20, 1260), rnd.uniform(4, 10), color="#ffffff", op=rnd.uniform(0.3, 0.8), width=1.4) for _ in range(30)]
    b += [f'<circle cx="{rnd.uniform(0,720):.0f}" cy="{rnd.uniform(0,1280):.0f}" r="{rnd.uniform(1,2.6):.1f}" fill="#fff" fill-opacity="{rnd.uniform(.35,.9):.2f}"/>' for _ in range(140)]
    render(svg(720, 1280, b), "dong/images/snow.png")
    render(svg(80, 80, [snowflake(40, 40, 34, color="#8fb8de", width=3)]), "dong/images/flake.png")

for name in (sys.argv[2:] or ["halloween", "noel", "xuan", "ha", "dong"]):
    globals()[name]()
print("ok")
