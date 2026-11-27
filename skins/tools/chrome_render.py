import re, subprocess, pathlib
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def chrome_render(svg_text: str, target: pathlib.Path):
    """Rasterises an SVG with Chrome headless (ImageMagick's own renderer drops unfilled strokes)."""
    w = int(float(re.search(r'width="([\d.]+)"', svg_text).group(1)))
    h = int(float(re.search(r'height="([\d.]+)"', svg_text).group(1)))
    target.parent.mkdir(parents=True, exist_ok=True)
    html = target.with_suffix(".tmp.html")
    html.write_text(f'<!doctype html><html><body style="margin:0;background:transparent">{svg_text}</body></html>')
    png = target.with_suffix(".tmp.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--default-background-color=00000000", f"--window-size={w},{h}", f"--screenshot={png}", html.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    html.unlink()
    if target.suffix == ".png":
        subprocess.run(["magick", str(png), "-strip", str(target)], check=True)
    else:
        subprocess.run(["magick", str(png), "-quality", "86", str(target)], check=True)
    png.unlink()
