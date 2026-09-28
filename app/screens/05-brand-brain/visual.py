"""Does it look like us: the brand palette, fonts and logo rules from the brain, and a check of any draft against them.

The palette is the `visual` section's colour tokens (site backed from the stylesheet, or approved by the founder),
each with a role guessed from its name (background, text, accent) and every text-on-background pair's WCAG contrast
ratio, computed here. Fonts are the font tokens. Logo rules are a founder record (`visual.logo_rules`) and read
unavailable until set. Two checks: paste CSS, HTML or a list of hex codes and every colour is matched to the nearest
token by RGB distance (off palette past TOLERANCE, with the nearest token named) and every font-family to the brand
fonts; drop a PNG and its dominant colours (a pure Python PNG read, sampled and binned) are matched the same way, so
a generated creative that drifts off the palette is caught before it runs. JPEG cannot be read here and says so.
Capability CREA-C12 owns image accuracy; this screen owns the palette. Rule BRN-R27 names the identity gaps.
"""
from __future__ import annotations

import base64
import re
import struct
import zlib

TOLERANCE = 40.0        # RGB euclidean distance under which a colour counts as on palette
NEUTRAL_SKIP = False    # white and black count; a brand that owns them should see them
MAX_PIXELS = 4_000_000
HEX = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
RGB = re.compile(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})", re.I)
FONT = re.compile(r"font-family\s*:\s*([^;}]+)", re.I)
ROLE_WORDS = [("background", ["white", "offwhite", "off_white", "cream", "grey_20", "gray_20", "grey_10", "background", "bg", "paper"]),
              ("text", ["black", "ink", "grey_80", "gray_80", "grey_90", "charcoal", "text"]),
              ("accent", ["blue", "green", "red", "yellow", "orange", "pink", "purple", "teal", "accent", "brand", "primary", "gold"]),
              ("neutral", ["grey", "gray", "silver", "stone", "sand"])]


def _hex_to_rgb(h: str) -> tuple[int, int, int] | None:
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        return None
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _rgb_to_hex(rgb) -> str:
    return "#%02x%02x%02x" % tuple(int(x) for x in rgb)


def _lum(rgb) -> float:
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b) -> float:
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


def _dist(a, b) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def _role(name: str) -> str:
    n = (name or "").lower()
    for role, words in ROLE_WORDS:
        if any(w in n for w in words):
            return role
    return "other"


def palette(brain) -> dict:
    colours, fonts = [], []
    for r in brain.records("visual"):
        f = r.get("field") or ""
        v = r.get("value")
        if f.startswith("color_") or f.startswith("colour_"):
            rgb = _hex_to_rgb(v) if isinstance(v, str) else None
            if rgb:
                colours.append({"key": f, "name": f.split("_", 1)[1].replace("_", " "), "hex": _rgb_to_hex(rgb), "rgb": rgb, "role": _role(f), "tier": r["tier"], "record": r["id"], "luminance": round(_lum(rgb), 3)})
        elif f.startswith("font_"):
            fonts.append({"key": f, "name": str(v), "role": f.split("_", 1)[1].replace("_", " "), "tier": r["tier"], "record": r["id"]})
    bgs = [c for c in colours if c["role"] == "background"] or [c for c in colours if c["luminance"] >= 0.8]
    texts = [c for c in colours if c["role"] == "text"] or [c for c in colours if c["luminance"] <= 0.1]
    pairs = []
    for t in texts:
        for b in bgs:
            ratio = contrast(t["rgb"], b["rgb"])
            pairs.append({"text": t["key"], "background": b["key"], "ratio": ratio, "aa": ratio >= 4.5, "aa_large": ratio >= 3.0})
    for a in [c for c in colours if c["role"] == "accent"]:
        for b in bgs[:2]:
            ratio = contrast(a["rgb"], b["rgb"])
            pairs.append({"text": a["key"], "background": b["key"], "ratio": ratio, "aa": ratio >= 4.5, "aa_large": ratio >= 3.0, "accent": True})
    logo = next((r for r in brain.records("visual") if r.get("field") == "logo_rules"), None)
    logo_rules = {"available": bool(logo), "record": logo["id"] if logo else None, "value": logo.get("value") if logo and isinstance(logo.get("value"), dict) else None, "tier": logo["tier"] if logo else None,
                  "reason": None if logo else "no logo rules on file; set the minimum size, the clear space and what never happens to the logo"}
    return {"colours": colours, "fonts": fonts, "pairs": pairs, "logo_rules": logo_rules,
            "counts": {"colours": len(colours), "fonts": len(fonts), "backgrounds": len(bgs), "texts": len(texts), "pairs": len(pairs), "aa_fail": sum(1 for p in pairs if not p["aa"] and not p.get("accent")), "accent_low": sum(1 for p in pairs if p.get("accent") and not p["aa_large"])},
            "available": bool(colours), "reason": None if colours else "no colour token in the visual section; the site crawl reads them from the stylesheet, or add them",
            "note": "Tokens from the brand's stylesheet or your approval. Roles are guessed from the token names. Contrast is the WCAG ratio: 4.5 passes for body text, 3 for large text and accents."}


def _nearest(rgb, colours: list[dict]) -> tuple[dict | None, float | None]:
    if not colours:
        return None, None
    best = min(colours, key=lambda c: _dist(rgb, c["rgb"]))
    return best, round(_dist(rgb, best["rgb"]), 1)


def check_text(brain, text: str) -> dict:
    pal = palette(brain)
    found: dict[str, int] = {}
    for m in HEX.finditer(text or ""):
        rgb = _hex_to_rgb(m.group(1))
        if rgb:
            found[_rgb_to_hex(rgb)] = found.get(_rgb_to_hex(rgb), 0) + 1
    for m in RGB.finditer(text or ""):
        rgb = tuple(min(255, int(x)) for x in m.groups())
        found[_rgb_to_hex(rgb)] = found.get(_rgb_to_hex(rgb), 0) + 1
    rows = []
    for h, n in sorted(found.items(), key=lambda kv: -kv[1]):
        rgb = _hex_to_rgb(h)
        near, d = _nearest(rgb, pal["colours"])
        rows.append({"hex": h, "times": n, "on_palette": d is not None and d <= TOLERANCE, "nearest": near["key"] if near else None, "nearest_hex": near["hex"] if near else None, "distance": d})
    fonts_found = []
    brand_fonts = {f["name"].lower() for f in pal["fonts"]}
    for m in FONT.finditer(text or ""):
        for name in m.group(1).split(","):
            name = name.strip().strip("'\"").strip()
            if name and name.lower() not in ("inherit", "sans-serif", "serif", "monospace", "system-ui"):
                fonts_found.append({"name": name, "brand": name.lower() in brand_fonts})
    seen = set()
    fonts_found = [f for f in fonts_found if not (f["name"].lower() in seen or seen.add(f["name"].lower()))]
    off = [r for r in rows if not r["on_palette"]]
    off_fonts = [f for f in fonts_found if not f["brand"]]
    verdict = "unavailable" if not pal["available"] else ("pass" if not off and not off_fonts else ("warn" if len(off) <= 2 and not off_fonts else "fail"))
    return {"colours": rows, "fonts": fonts_found, "off_palette": off, "off_fonts": off_fonts, "verdict": verdict, "tolerance": TOLERANCE, "palette_available": pal["available"],
            "counts": {"colours": len(rows), "off": len(off), "fonts": len(fonts_found), "off_fonts": len(off_fonts)},
            "summary": (f"{len(rows)} colour{'s' if len(rows) != 1 else ''} found, {len(off)} off the palette" + (f"; {len(off_fonts)} font{'s' if len(off_fonts) != 1 else ''} not ours" if fonts_found else "")) if pal["available"] else "no palette on file to check against"}


def read_png(data: bytes) -> dict | tuple[int, dict]:
    """A pure Python PNG read: IHDR, the IDAT stream, the 5 scanline filters; colour types 0, 2, 4, 6 at 8 bits, and 3 (palette)."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return 400, {"error": "not a PNG; only PNG can be read here (export a PNG, JPEG cannot be decoded without a library)"}
    pos, idat, ihdr, plte = 8, [], None, None
    while pos + 8 <= len(data):
        ln, typ = struct.unpack(">I4s", data[pos:pos + 8])
        chunk = data[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            ihdr = struct.unpack(">IIBBBBB", chunk)
        elif typ == b"IDAT":
            idat.append(chunk)
        elif typ == b"PLTE":
            plte = chunk
        elif typ == b"IEND":
            break
        pos += 12 + ln
    if not ihdr or not idat:
        return 400, {"error": "PNG without IHDR or IDAT"}
    w, h, depth, ctype, _, _, interlace = ihdr
    if depth != 8 or interlace != 0 or ctype not in (0, 2, 3, 4, 6):
        return 400, {"error": f"PNG with bit depth {depth}, colour type {ctype}, interlace {interlace} cannot be read here; export an 8 bit non interlaced PNG"}
    if w * h > MAX_PIXELS:
        return 400, {"error": f"PNG of {w}x{h} is over the {MAX_PIXELS} pixel limit; export a smaller one"}
    bpp = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    raw = zlib.decompress(b"".join(idat))
    stride = w * bpp
    prev = bytearray(stride)
    pixels = []
    p = 0
    for _ in range(h):
        ft = raw[p]
        line = bytearray(raw[p + 1:p + 1 + stride])
        p += 1 + stride
        if ft == 1:
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 255
        elif ft == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 255
        elif ft == 3:
            for i in range(stride):
                line[i] = (line[i] + ((line[i - bpp] if i >= bpp else 0) + prev[i]) // 2) & 255
        elif ft == 4:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                b = prev[i]
                c = prev[i - bpp] if i >= bpp else 0
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        pixels.append(bytes(line))
        prev = line
    return {"width": w, "height": h, "ctype": ctype, "bpp": bpp, "rows": pixels, "plte": plte}


def dominant(png: dict, top: int = 6, step: int | None = None) -> list[dict]:
    w, h, ctype, bpp, rows, plte = png["width"], png["height"], png["ctype"], png["bpp"], png["rows"], png["plte"]
    step = step or max(1, int((w * h / 40_000) ** 0.5))
    bins: dict[tuple, int] = {}
    total = 0
    for y in range(0, h, step):
        row = rows[y]
        for x in range(0, w, step):
            i = x * bpp
            if ctype == 0:
                rgb = (row[i], row[i], row[i])
            elif ctype == 4:
                rgb = (row[i], row[i], row[i])
            elif ctype == 3:
                k = row[i] * 3
                rgb = (plte[k], plte[k + 1], plte[k + 2]) if plte and k + 2 < len(plte) else (0, 0, 0)
            else:
                if ctype == 6 and row[i + 3] < 32:
                    continue
                rgb = (row[i], row[i + 1], row[i + 2])
            key = (rgb[0] >> 4, rgb[1] >> 4, rgb[2] >> 4)
            bins[key] = bins.get(key, 0) + 1
            total += 1
    out = []
    for key, n in sorted(bins.items(), key=lambda kv: -kv[1])[:top]:
        rgb = tuple(k * 16 + 8 for k in key)
        out.append({"hex": _rgb_to_hex(rgb), "rgb": rgb, "share": round(n / total, 3) if total else None})
    return out


def check_png(brain, content_base64: str) -> dict | tuple[int, dict]:
    try:
        data = base64.b64decode(str(content_base64), validate=True)
    except (ValueError, TypeError):
        return 400, {"error": "content_base64 is not valid base64"}
    png = read_png(data)
    if isinstance(png, tuple):
        return png
    pal = palette(brain)
    doms = dominant(png)
    rows = []
    on_share = 0.0
    for d in doms:
        near, dist = _nearest(d["rgb"], pal["colours"])
        on = dist is not None and dist <= TOLERANCE
        if on and d["share"]:
            on_share += d["share"]
        rows.append(dict(d, on_palette=on, nearest=near["key"] if near else None, nearest_hex=near["hex"] if near else None, distance=dist))
    off = [r for r in rows if not r["on_palette"]]
    covered = sum(r["share"] or 0 for r in rows)
    verdict = "unavailable" if not pal["available"] else ("pass" if not off else ("warn" if on_share >= 0.7 * covered else "fail"))
    return {"width": png["width"], "height": png["height"], "colours": rows, "off_palette": off, "verdict": verdict, "on_palette_share": round(on_share, 3) if pal["available"] else None, "tolerance": TOLERANCE, "palette_available": pal["available"],
            "summary": (f"{len(rows)} dominant colours, {len(off)} off the palette; {round(on_share * 100)} percent of the sampled pixels sit on a brand colour") if pal["available"] else "no palette on file to check against",
            "note": "Dominant colours are the top bins of a sampled read, so a thin line or a small logo may not appear. Product colours are not brand colours: a sock in a new shade is expected to be off the palette."}


def logo_record(brain, body: dict) -> dict:
    v = {"min_size_px": int(body["min_size_px"]) if str(body.get("min_size_px") or "").isdigit() else None,
         "clear_space": str(body.get("clear_space") or "")[:120] or None,
         "never": [str(x).strip()[:80] for x in (body.get("never") if isinstance(body.get("never"), list) else str(body.get("never") or "").split(";")) if str(x).strip()][:10],
         "backgrounds": [str(x).strip()[:40] for x in (body.get("backgrounds") if isinstance(body.get("backgrounds"), list) else str(body.get("backgrounds") or "").split(",")) if str(x).strip()][:6]}
    text = "Logo rules: " + ", ".join(x for x in [f"minimum {v['min_size_px']} px wide" if v["min_size_px"] else "", f"clear space {v['clear_space']}" if v["clear_space"] else "", ("never " + "; ".join(v["never"])) if v["never"] else "", ("on " + ", ".join(v["backgrounds"])) if v["backgrounds"] else ""] if x) + "."
    return {"id": f"{brain.brand}.visual.logo_rules", "brand": brain.brand, "section": "visual", "field": "logo_rules", "value": v, "text": text, "tier": "approved", "confidence": 1.0, "visibility": "private",
            "source": {"type": "founder", "ref": "05-brand-brain visual check", "captured_at": brain.today.isoformat()}}
