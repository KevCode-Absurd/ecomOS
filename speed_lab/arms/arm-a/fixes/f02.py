"""f02: Nanum Myeongjo 400 and 700 are full Korean TTFs (3.06 MB and 3.07 MB raw, 2.16 MB on the wire), preloaded.
Fix: a Latin subset in WOFF2 for each weight, preloaded instead, plus a second @font-face per weight that
covers every other code point of the original font with unicode-range. The browser downloads that second
file only if the page shows one of those characters, so glyph coverage is unchanged.
"""
import html, io, re
from fontTools import subset
from fontTools.ttLib import TTFont
from common import fresh, read, put_text, get_text, HOME, ORIGIN, CSS_MAIN

NAME, PARENT = "arm-a-f02", "arm-a-f01"
FONTS = {  # original url -> new file stem
    "/_next/static/media/14a3fceaeabbcb56-s.p.ttf": "nanum-400",
    "/_next/static/media/ae1a48c074c123e8-s.p.ttf": "nanum-700",
}
# Google Fonts 'latin' block, plus every character that appears in the served HTML (text and __NEXT_DATA__).
LATIN = [(0x0000, 0x00FF), (0x0131, 0x0131), (0x0152, 0x0153), (0x02BB, 0x02BC), (0x02C6, 0x02C6), (0x02DA, 0x02DA),
         (0x02DC, 0x02DC), (0x0304, 0x0304), (0x0308, 0x0308), (0x0329, 0x0329), (0x2000, 0x206F), (0x2074, 0x2074),
         (0x20AC, 0x20AC), (0x20B9, 0x20B9), (0x2122, 0x2122), (0x2191, 0x2191), (0x2193, 0x2193), (0x2212, 0x2212),
         (0x2215, 0x2215), (0xFEFF, 0xFEFF), (0xFFFD, 0xFFFD)]


def ranges(cps):
    cps = sorted(cps); out = []
    for c in cps:
        if out and c == out[-1][1] + 1: out[-1][1] = c
        else: out.append([c, c])
    return ",".join(f"U+{a:X}" if a == b else f"U+{a:X}-{b:X}" for a, b in out)


def build_subset(ttf_bytes, cps):
    f = TTFont(io.BytesIO(ttf_bytes))
    opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["*"]; opts.name_IDs = ["*"]
    opts.notdef_outline = True; opts.hinting = False; opts.desubroutinize = True
    s = subset.Subsetter(opts); s.populate(unicodes=cps); s.subset(f)
    b = io.BytesIO(); f.flavor = "woff2"; f.save(b); return b.getvalue()


def main():
    v = fresh(NAME, PARENT)
    page = html.unescape(read(HOME)[0].decode("utf-8"))
    want = {c for a, b in LATIN for c in range(a, b + 1)} | {ord(ch) for ch in page}
    css = get_text(v, CSS_MAIN)
    doc = get_text(v, HOME)
    for old, stem in FONTS.items():
        ttf = read(ORIGIN + old)[0]
        cmap = set(TTFont(io.BytesIO(ttf)).getBestCmap())
        main_cps, rest_cps = cmap & want, cmap - want
        main_url, rest_url = f"/_next/static/media/{stem}-latin.woff2", f"/_next/static/media/{stem}-rest.woff2"
        v.add(ORIGIN + main_url, build_subset(ttf, main_cps), "font/woff2", headers={"cache-control": "public, max-age=31536000, immutable"})
        v.add(ORIGIN + rest_url, build_subset(ttf, rest_cps), "font/woff2", headers={"cache-control": "public, max-age=31536000, immutable"})
        # CSS: replace the single TTF face with a Latin face plus a unicode-range face for everything else
        pat = re.compile(r"@font-face\{font-family:(__nanumMyeongjo_\w+);src:url\(" + re.escape(old) + r"\) format\(\"truetype\"\);([^}]*)\}")
        m = pat.search(css); assert m, old
        fam, rest = m.group(1), m.group(2)
        new = (f'@font-face{{font-family:{fam};src:url({main_url}) format("woff2");{rest};unicode-range:{ranges(main_cps)}}}'
               f'@font-face{{font-family:{fam};src:url({rest_url}) format("woff2");{rest};unicode-range:{ranges(rest_cps)}}}')
        css = css[:m.start()] + new + css[m.end():]
        # HTML: preload the small Latin file instead of the 3 MB TTF
        pre_old = f'<link rel="preload" href="{old}" as="font" type="font/ttf" crossorigin="anonymous" data-next-font="size-adjust"/>'
        assert pre_old in doc, old
        doc = doc.replace(pre_old, f'<link rel="preload" href="{main_url}" as="font" type="font/woff2" crossorigin="anonymous" data-next-font="size-adjust"/>')
    put_text(v, CSS_MAIN, css, "text/css")
    put_text(v, HOME, doc, "text/html; charset=utf-8")
    for u, e in v.idx.items():
        print(e["status"], e["size"], e["url"])


if __name__ == "__main__":
    main()
