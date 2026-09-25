"""F01: subset the two NanumMyeongjo TTF files (3.0 MB each raw, about 1.0 MB each on the wire) to a
Latin plus symbols WOFF2 subset, and point the @font-face rules and the preload links at the new files.
Hangul, Jamo and CJK ideographs are dropped. Latin, Latin-1, Latin Extended, punctuation, currency,
arrows, math, shapes and dingbats that the font has are kept (the page uses stars, bullets, quotes, hearts).
Parent: base store."""
import io
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.subset import parse_unicodes
from common import fresh, put_text, get_text, add_new, lab, HOME

NAME, PARENT = "arm-b-f01", None
CSS = "https://www.gehnaindia.com/_next/static/css/f45806cc85ed262f.css"
FONTS = ["14a3fceaeabbcb56", "ae1a48c074c123e8"]  # NanumMyeongjo 400 and 700
RANGES = "U+0000-024F,U+02B0-036F,U+2000-206F,U+20A0-20CF,U+2100-214F,U+2190-21FF,U+2200-22FF,U+25A0-25FF,U+2600-27BF,U+FEFF,U+FFFD"


def woff2_subset(raw):
    o = subset.Options()
    o.flavor = "woff2"; o.layout_features = ["*"]; o.name_IDs = ["*"]; o.notdef_outline = True; o.hinting = True
    ft = TTFont(io.BytesIO(raw))
    s = subset.Subsetter(o); s.populate(unicodes=parse_unicodes(RANGES)); s.subset(ft)
    out = io.BytesIO(); ft.flavor = "woff2"; ft.save(out)
    return out.getvalue()


def main():
    v = fresh(NAME, PARENT)
    html, css = get_text(v, HOME), get_text(v, CSS)
    for h in FONTS:
        old = f"/_next/static/media/{h}-s.p.ttf"
        new = f"/_next/static/media/{h}-s.p.latin.woff2"
        raw, _ = lab.read("https://www.gehnaindia.com" + old)
        body = woff2_subset(raw)
        add_new(v, "https://www.gehnaindia.com" + new, body, "font/woff2", "font", headers={"cache-control": "public, max-age=31536000, immutable"})
        print(h, len(raw), "->", len(body))
        assert css.count(f'url({old}) format("truetype")') == 1
        css = css.replace(f'url({old}) format("truetype")', f'url({new}) format("woff2")')
        tag_old = f'<link rel="preload" href="{old}" as="font" type="font/ttf"'
        assert html.count(tag_old) == 1
        html = html.replace(tag_old, f'<link rel="preload" href="{new}" as="font" type="font/woff2"')
    put_text(v, CSS, css, "text/css")
    put_text(v, HOME, html, "text/html; charset=utf-8")
    print("built", NAME)


if __name__ == "__main__":
    main()
