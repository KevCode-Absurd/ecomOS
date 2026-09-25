"""F06: serve the 2 Lato files (already a 275-glyph Latin subset) as WOFF2 instead of TTF. Same glyphs, same
tables, only the container changes (lossless). The @font-face src and the 2 preload links point at the new
files. Lato is the only web font used in the first viewport, so these 2 files are preloaded next to the
LCP image. Parent: arm-b-f05."""
import io
from fontTools.ttLib import TTFont
from common import fresh, put_text, get_text, add_new, lab, HOME

NAME, PARENT = "arm-b-f06", "arm-b-f05"
CSS = "https://www.gehnaindia.com/_next/static/css/f45806cc85ed262f.css"
FONTS = ["4291f48c2ea51320", "2c00c297d3cdabf8"]  # Lato 400 and 700


def main():
    v = fresh(NAME, PARENT)
    html, css = get_text(v, HOME), get_text(v, CSS)
    for h in FONTS:
        old, new = f"/_next/static/media/{h}-s.p.ttf", f"/_next/static/media/{h}-s.p.woff2"
        raw, _ = lab.read("https://www.gehnaindia.com" + old)
        ft = TTFont(io.BytesIO(raw)); ft.flavor = "woff2"; out = io.BytesIO(); ft.save(out)
        add_new(v, "https://www.gehnaindia.com" + new, out.getvalue(), "font/woff2", "font", headers={"cache-control": "public, max-age=31536000, immutable"})
        assert css.count(f'url({old}) format("truetype")') == 1
        css = css.replace(f'url({old}) format("truetype")', f'url({new}) format("woff2")')
        tag = f'<link rel="preload" href="{old}" as="font" type="font/ttf"'
        assert html.count(tag) == 1
        html = html.replace(tag, f'<link rel="preload" href="{new}" as="font" type="font/woff2"')
        print(h, len(raw), "->", len(out.getvalue()))
    put_text(v, CSS, css, "text/css")
    put_text(v, HOME, html, "text/html; charset=utf-8")
    print("built", NAME)


if __name__ == "__main__":
    main()
