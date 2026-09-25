"""f05: Lato 400 and 700 are preloaded as TTF (75 KB raw, 36 KB gzip each). They are high-priority preloads
that share the first second of bandwidth with the LCP banner. Fix: same method as f02. A Latin WOFF2
subset per weight (preloaded), plus a unicode-range face with every other code point of the original file,
so coverage is unchanged.
"""
import html, io, re
from fontTools.ttLib import TTFont
from common import fresh, read, put_text, get_text, HOME, ORIGIN, CSS_MAIN
from f02 import LATIN, ranges, build_subset

NAME, PARENT = "arm-a-f05", "arm-a-f04"
FONTS = {"/_next/static/media/4291f48c2ea51320-s.p.ttf": "lato-400", "/_next/static/media/2c00c297d3cdabf8-s.p.ttf": "lato-700"}


def main():
    v = fresh(NAME, PARENT)
    page = html.unescape(read(HOME)[0].decode("utf-8"))
    want = {c for a, b in LATIN for c in range(a, b + 1)} | {ord(ch) for ch in page}
    css, doc = get_text(v, CSS_MAIN), get_text(v, HOME)
    for old, stem in FONTS.items():
        ttf = read(ORIGIN + old)[0]
        cmap = set(TTFont(io.BytesIO(ttf)).getBestCmap())
        main_cps, rest_cps = cmap & want, cmap - want
        main_url, rest_url = f"/_next/static/media/{stem}-latin.woff2", f"/_next/static/media/{stem}-rest.woff2"
        hdr = {"cache-control": "public, max-age=31536000, immutable"}
        main_b = build_subset(ttf, main_cps)
        v.add(ORIGIN + main_url, main_b, "font/woff2", headers=hdr)
        faces = f'src:url({main_url}) format("woff2");{{REST}};unicode-range:{ranges(main_cps)}'
        pat = re.compile(r"@font-face\{font-family:(__lato_\w+);src:url\(" + re.escape(old) + r"\) format\(\"truetype\"\);([^}]*)\}")
        m = pat.search(css); assert m, old
        fam, rest = m.group(1), m.group(2)
        new = f'@font-face{{font-family:{fam};src:url({main_url}) format("woff2");{rest};unicode-range:{ranges(main_cps)}}}'
        if rest_cps:
            v.add(ORIGIN + rest_url, build_subset(ttf, rest_cps), "font/woff2", headers=hdr)
            new += f'@font-face{{font-family:{fam};src:url({rest_url}) format("woff2");{rest};unicode-range:{ranges(rest_cps)}}}'
        css = css[:m.start()] + new + css[m.end():]
        pre_old = f'<link rel="preload" href="{old}" as="font" type="font/ttf" crossorigin="anonymous" data-next-font="size-adjust"/>'
        assert pre_old in doc, old
        doc = doc.replace(pre_old, f'<link rel="preload" href="{main_url}" as="font" type="font/woff2" crossorigin="anonymous" data-next-font="size-adjust"/>')
        print(stem, "ttf", len(ttf), "-> latin woff2", len(main_b), "| code points", len(main_cps), "kept,", len(rest_cps), "in the rest face")
    put_text(v, CSS_MAIN, css, "text/css")
    put_text(v, HOME, doc, "text/html; charset=utf-8")


if __name__ == "__main__":
    main()
