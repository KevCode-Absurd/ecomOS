"""f06: The LCP element is the first hero slide (new-arrivals-mobile, 40 KB AVIF). It has fetchpriority=high but
no preload, so the browser only finds it when the HTML parser reaches it in the body, after 31 script tags
and 4 font preloads in the head. Fix: a <link rel="preload" as="image" fetchpriority="high"> with the same
imagesrcset and imagesizes, placed before the font preloads. This is what next/image emits for priority={true}.
"""
import re
from common import fresh, put_text, get_text, HOME

NAME, PARENT = "arm-a-f06", "arm-a-f05"
ANCHOR = '<meta name="theme-color" content="#f6b74d"/>'


def main():
    v = fresh(NAME, PARENT)
    doc = get_text(v, HOME)
    m = re.search(r'<img class="\w+" alt="New Arrivals" fetchPriority="high"[^>]*? sizes="([^"]+)" srcSet="([^"]+)"', doc)
    assert m and doc.count(ANCHOR) == 1
    link = f'<link rel="preload" as="image" fetchpriority="high" imagesizes="{m.group(1)}" imagesrcset="{m.group(2)}"/>'
    doc = doc.replace(ANCHOR, ANCHOR + link)
    put_text(v, HOME, doc, "text/html; charset=utf-8")
    print(link[:200])


if __name__ == "__main__":
    main()
