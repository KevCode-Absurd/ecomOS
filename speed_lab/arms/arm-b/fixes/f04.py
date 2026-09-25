"""F04: right-size the 7 "browse categories" icons. They render at 60 x 60 CSS px (165 device px at DPR 2.75)
but the srcset offers w=256 (1x) and w=640 (2x), so the phone downloads 640 x 640 AVIFs (229 KB in total).
The fix serves what the Next.js image optimizer returns for w=128 and w=256 (same q=75, AVIF) and points
the srcset at 128 (1x) and 256 (2x). A developer gets the same result with width={60} or sizes="60px".
The new files are resized from the recorded 640 px AVIF with Lanczos, so the image is the same picture.
Parent: arm-b-f03."""
import io
from PIL import Image
from common import fresh, put_text, get_text, add_new, lab, HOME

NAME, PARENT = "arm-b-f04", "arm-b-f03"
ICONS = ["best-sellers", "earrings", "chains", "rings", "bracelets", "nosepins", "pendants"]
BASE = "/_next/image?url=%2Fstatic%2Fimages%2Fbrowse-categories%2F{n}.png&amp;w={w}&amp;q=75"


def main():
    v = fresh(NAME, PARENT)
    html = get_text(v, HOME)
    for n in ICONS:
        src640 = "https://www.gehnaindia.com" + BASE.format(n=n, w=640).replace("&amp;", "&")
        body, e = lab.read(src640)
        im = Image.open(io.BytesIO(body)).convert("RGBA")
        for w in (128, 256):
            out = io.BytesIO(); im.resize((w, w), Image.LANCZOS).save(out, "AVIF", quality=75)
            add_new(v, "https://www.gehnaindia.com" + BASE.format(n=n, w=w).replace("&amp;", "&"), out.getvalue(), "image/avif", "image",
                    headers={k: v_ for k, v_ in e["headers"].items() if k in ("cache-control", "vary")})
        old = f'srcSet="{BASE.format(n=n, w=256)} 1x, {BASE.format(n=n, w=640)} 2x" src="{BASE.format(n=n, w=640)}"'
        new = f'srcSet="{BASE.format(n=n, w=128)} 1x, {BASE.format(n=n, w=256)} 2x" src="{BASE.format(n=n, w=256)}"'
        assert html.count(old) == 1, n
        html = html.replace(old, new)
    put_text(v, HOME, html, "text/html; charset=utf-8")
    print("built", NAME)


if __name__ == "__main__":
    main()
