"""f04: The 7 category icons in the first screen render at 60 x 60 CSS px but next/image is given width 200,
so the srcset is w=256 1x and w=640 2x, and a 2.75x phone fetches the 640 x 640 file (229 KB for 7 icons).
They start at 0.7 s, in parallel with the LCP banner and the app JS.
Fix: srcset w=128 1x, w=256 2x (what next/image emits for width={128}); the CSS keeps them at 60 px, so a
2.75x phone gets 256 px, still above the 165 device px it draws. The 128 and 256 files are made here by
downscaling the stored 640 px AVIF with Lanczos and re-encoding as AVIF (the source PNGs are not in the mirror).
Pillow quality 60 is used because re-encoding the stored 640 px files at 60 gives about the same bytes as the
site optimizer (checked on 3 icons: 38,297 vs 38,863; 50,495 vs 52,098; 19,684 vs 19,795).
"""
import io
from PIL import Image
from common import fresh, put_text, get_text, read, HOME, ORIGIN

NAME, PARENT = "arm-a-f04", "arm-a-f03"
ICONS = ["best-sellers", "earrings", "chains", "rings", "bracelets", "nosepins", "pendants"]


def url(name, w):
    return f"/_next/image?url=%2Fstatic%2Fimages%2Fbrowse-categories%2F{name}.png&w={w}&q=75"


def main():
    v = fresh(NAME, PARENT)
    doc = get_text(v, HOME)
    total_old = total_new = 0
    for n in ICONS:
        src640 = read(ORIGIN + url(n, 640))[0]
        total_old += len(src640)
        im = Image.open(io.BytesIO(src640)).convert("RGBA")
        for w in (128, 256):
            b = io.BytesIO()
            im.resize((w, w), Image.LANCZOS).save(b, "AVIF", quality=60)
            v.add(ORIGIN + url(n, w), b.getvalue(), "image/avif", headers={"cache-control": "public, max-age=315360000, immutable"})
            if w == 256: total_new += len(b.getvalue())
        amp = lambda s: s.replace("&", "&amp;")
        old = f'srcSet="{amp(url(n, 256))} 1x, {amp(url(n, 640))} 2x" src="{amp(url(n, 640))}"'
        new = f'srcSet="{amp(url(n, 128))} 1x, {amp(url(n, 256))} 2x" src="{amp(url(n, 256))}"'
        assert doc.count(old) == 1, n
        doc = doc.replace(old, new)
    put_text(v, HOME, doc, "text/html; charset=utf-8")
    print("640 px files", total_old, "bytes -> 256 px files", total_new, "bytes")


if __name__ == "__main__":
    main()
