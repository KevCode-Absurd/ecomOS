"""F05: let the LCP image go first. The hero image (the LCP element) is discovered after 4 font preloads and
2 stylesheets, and the replay host speaks HTTP/1.1 (6 sockets per host), so it waits for a socket and then
shares bandwidth with about 175 KB of fonts. The fix:
  1. adds <link rel="preload" as="image" fetchpriority="high"> for the hero, with the same imagesrcset and
     imagesizes as the <img>, as the first request hint in <head>;
  2. drops the preload for the 2 NanumMyeongjo files. A text walk of the rendered page (diag.py fontUse) shows
     no NanumMyeongjo text in the first viewport; only Lato is used there. The @font-face rules stay, so the
     headings further down still get the font (font-display: swap).
Parent: arm-b-f04."""
from common import fresh, put_text, get_text, HOME

NAME, PARENT = "arm-b-f05", "arm-b-f04"
IMG = "/_next/image?url=%2Fstatic%2Fimages%2Fbanner%2Fnew-arrivals-mobile.png&amp;w={w}&amp;q=75"
WIDTHS = [640, 750, 828, 1080, 1200, 1920, 2560]


def main():
    v = fresh(NAME, PARENT)
    html = get_text(v, HOME)
    srcset = ", ".join(f"{IMG.format(w=w)} {w}w" for w in WIDTHS)
    assert html.count(f'srcSet="{srcset}"') == 2  # <source> and <img> of the hero
    preload = f'<link rel="preload" as="image" fetchpriority="high" imagesrcset="{srcset}" imagesizes="100vw"/>'
    anchor = '<meta name="viewport" content="minimum-scale=1, initial-scale=1, width=device-width, shrink-to-fit=no"/>'
    assert html.count(anchor) == 1
    html = html.replace(anchor, anchor + preload)
    for h in ["14a3fceaeabbcb56", "ae1a48c074c123e8"]:
        tag = f'<link rel="preload" href="/_next/static/media/{h}-s.p.latin.woff2" as="font" type="font/woff2" crossorigin="anonymous" data-next-font="size-adjust"/>'
        assert html.count(tag) == 1, h
        html = html.replace(tag, "")
    put_text(v, HOME, html, "text/html; charset=utf-8")
    print("built", NAME)


if __name__ == "__main__":
    main()
