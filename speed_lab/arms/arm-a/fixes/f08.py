"""f08: First paint waits for 2 render-blocking stylesheets (f45806cc 15 KB and 69294e78 14 KB raw after f05,
about 8 KB gzip together). They are requested only when the parser reaches them, so each costs a round trip
(150 ms on this profile) plus download before anything can paint. Fix: inline both in <style> tags.
The global sheet becomes a plain <style>. The page sheet becomes <style data-n-href="..."> because that is
the element Next.js itself creates and toggles for page CSS on client-side navigation, so route changes keep
working. Next.js leaves stylesheets alone on the first render. Built on f06: f07 (defer email-decode) gave no
measurable gain and was reverted.
"""
import re
from common import fresh, put_text, get_text, HOME, ORIGIN

NAME, PARENT = "arm-a-f08", "arm-a-f06"
G, P = "/_next/static/css/f45806cc85ed262f.css", "/_next/static/css/69294e788452cb15.css"


def main():
    v = fresh(NAME, PARENT)
    doc = get_text(v, HOME)
    g_css, p_css = get_text(v, ORIGIN + G), get_text(v, ORIGIN + P)
    for c in (g_css, p_css):
        rel = [u for u in re.findall(r"url\(([^)]+)\)", c) if not u.strip("'\"").startswith(("/", "data:", "http"))]
        assert not rel, rel  # relative urls would break when moved into the HTML
        assert "</style" not in c
    reps = {
        f'<link rel="preload" href="{G}" as="style"/>': "",
        f'<link rel="stylesheet" href="{G}" data-n-g=""/>': f"<style>{g_css}</style>",
        f'<link rel="preload" href="{P}" as="style"/>': "",
        f'<link rel="stylesheet" href="{P}" data-n-p=""/>': f'<style data-n-href="{P}">{p_css}</style>',
    }
    for a, b in reps.items():
        assert doc.count(a) == 1, a
        doc = doc.replace(a, b)
    put_text(v, HOME, doc, "text/html; charset=utf-8")
    print("inlined", len(g_css), "+", len(p_css), "bytes of CSS")


if __name__ == "__main__":
    main()
