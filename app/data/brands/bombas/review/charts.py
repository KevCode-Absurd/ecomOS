"""Small SVG chart helpers for the Bombas data review. No dependencies.
Every chart is drawn to scale from the aggregates. Colors come from CSS
classes so one SVG reads in light and dark (the <style> block carries both)."""
from __future__ import annotations
import math

STYLE = """
<style>
.rv{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;font-size:12px}
.rv .ink{fill:#0b0b0b}.rv .sec{fill:#52514e}.rv .mut{fill:#898781}
.rv .grid{stroke:#e1e0d9;stroke-width:1}.rv .axis{stroke:#c3c2b7;stroke-width:1}
.rv .surf{fill:#fcfcfb}.rv .ring{stroke:#fcfcfb}
.rv .s1{fill:#2a78d6}.rv .s2{fill:#eb6834}.rv .s3{fill:#1baf7a}.rv .s4{fill:#eda100}.rv .s5{fill:#e87ba4}.rv .s6{fill:#008300}.rv .s7{fill:#4a3aa7}
.rv .l1{stroke:#2a78d6}.rv .l2{stroke:#eb6834}.rv .l3{stroke:#1baf7a}.rv .l4{stroke:#eda100}
.rv .ref{stroke:#898781;stroke-width:1.5}
@media (prefers-color-scheme: dark){
.rv .ink{fill:#ffffff}.rv .sec{fill:#c3c2b7}.rv .mut{fill:#898781}
.rv .grid{stroke:#2c2c2a}.rv .axis{stroke:#383835}.rv .surf{fill:#1a1a19}.rv .ring{stroke:#1a1a19}
.rv .s1{fill:#3987e5}.rv .s2{fill:#d95926}.rv .s3{fill:#199e70}.rv .s4{fill:#c98500}.rv .s5{fill:#d55181}.rv .s6{fill:#008300}.rv .s7{fill:#9085e9}
.rv .l1{stroke:#3987e5}.rv .l2{stroke:#d95926}.rv .l3{stroke:#199e70}.rv .l4{stroke:#c98500}
}
</style>"""

W, H = 720, 300
PAD = dict(l=56, r=16, t=28, b=40)


def _ticks(lo, hi, n=4):
    if hi <= lo:
        hi = lo + 1
    raw = (hi - lo) / n
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        step = m * mag
        if raw <= step:
            break
    start = math.floor(lo / step) * step
    out = []
    v = start
    while v <= hi + 1e-9:
        out.append(round(v, 10))
        v += step
    return out


def _fmt(v, unit=""):
    if unit == "%":
        return f"{v * 100:.0f}%" if abs(v * 100 - round(v * 100)) < 1e-6 else f"{v * 100:.1f}%"
    if unit == "$":
        if abs(v) >= 1e6:
            return f"${v / 1e6:.0f}M" if v % 1e6 == 0 else f"${v / 1e6:.1f}M"
        if abs(v) >= 1e3:
            return f"${v / 1e3:.0f}k"
        return f"${v:.0f}"
    if unit == "x":
        return f"{v:.1f}x"
    if abs(v) >= 1e6:
        return f"{v / 1e6:.1f}M"
    if abs(v) >= 1e3:
        return f"{v / 1e3:.0f}k"
    if isinstance(v, float) and not float(v).is_integer():
        return f"{v:.2f}".rstrip("0").rstrip(".")
    return f"{v:.0f}"


def _esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;")


def _frame(title, subtitle, body, legend=None, w=W, h=H):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{_esc(title)}" class="rv">', STYLE,
             f'<rect class="surf" x="0" y="0" width="{w}" height="{h}" rx="6"/>',
             f'<text class="ink" x="{PAD["l"]}" y="18" font-weight="600">{_esc(title)}</text>']
    if subtitle:
        parts.append(f'<text class="mut" x="{w - PAD["r"]}" y="18" text-anchor="end" font-size="11">{_esc(subtitle)}</text>')
    parts.append(body)
    if legend:
        x = PAD["l"]
        y = h - 10
        for cls, name, kind in legend:
            if kind == "line":
                parts.append(f'<line class="{cls}" x1="{x}" y1="{y - 4}" x2="{x + 16}" y2="{y - 4}" stroke-width="2"/>')
            else:
                parts.append(f'<rect class="{cls}" x="{x}" y="{y - 9}" width="10" height="10" rx="2"/>')
            parts.append(f'<text class="sec" x="{x + 20}" y="{y}" font-size="11">{_esc(name)}</text>')
            x += 20 + 6.2 * len(name) + 22
    parts.append("</svg>")
    return "\n".join(parts)


def _yaxis(lo, hi, unit, h, ticks=None):
    ticks = ticks or _ticks(lo, hi)
    lo, hi = min(lo, ticks[0]), max(hi, ticks[-1])
    top, bot = PAD["t"], h - PAD["b"]
    sy = lambda v: bot - (v - lo) / (hi - lo) * (bot - top)
    g = []
    for t in ticks:
        y = sy(t)
        g.append(f'<line class="grid" x1="{PAD["l"]}" y1="{y:.1f}" x2="{W - PAD["r"]}" y2="{y:.1f}"/>')
        g.append(f'<text class="mut" x="{PAD["l"] - 6}" y="{y + 4:.1f}" text-anchor="end" font-size="11">{_fmt(t, unit)}</text>')
    return sy, "\n".join(g), lo, hi


def columns(title, labels, series, unit="", subtitle="", stacked=False, legend_names=None, ymax=None, ref=None, h=H, label_every=1, note_idx=None):
    """series: list of lists (one per series). stacked=True stacks them."""
    n = len(labels)
    tops = [sum(s[i] for s in series) if stacked else max(s[i] for s in series) for i in range(n)]
    hi = ymax or max(tops) * 1.08
    sy, grid, lo, hi = _yaxis(0, hi, unit, h)
    top, bot = PAD["t"], h - PAD["b"]
    band = (W - PAD["l"] - PAD["r"]) / n
    k = len(series)
    bw = min(24, band * 0.7 / (1 if stacked else k))
    out = [grid]
    for i, lab in enumerate(labels):
        x0 = PAD["l"] + band * i + band / 2
        base = 0
        for j, s in enumerate(series):
            v = s[i]
            if stacked:
                y1, y0 = sy(base + v), sy(base)
                x = x0 - bw / 2
                gap = 2 if j > 0 else 0
                hh = max(0, y0 - y1 - gap)
                out.append(f'<rect class="s{j + 1}" x="{x:.1f}" y="{y1:.1f}" width="{bw:.1f}" height="{hh:.1f}"/>')
                base += v
            else:
                x = x0 - (k * bw) / 2 + j * bw + (2 if j > 0 else 0)
                y1 = sy(v)
                out.append(f'<rect class="s{j + 1}" x="{x:.1f}" y="{y1:.1f}" width="{bw - (2 if j > 0 else 0):.1f}" height="{max(0, bot - y1):.1f}" rx="3"/>')
        if i % label_every == 0:
            out.append(f'<text class="mut" x="{x0:.1f}" y="{bot + 14}" text-anchor="middle" font-size="10">{_esc(lab)}</text>')
    if ref is not None:
        rv, rname = ref
        y = sy(rv)
        out.append(f'<line class="ref" x1="{PAD["l"]}" y1="{y:.1f}" x2="{W - PAD["r"]}" y2="{y:.1f}"/>')
        out.append(f'<text class="sec" x="{W - PAD["r"]}" y="{y - 4:.1f}" text-anchor="end" font-size="11">{_esc(rname)}</text>')
    # direct label the max
    im = max(range(n), key=lambda i: tops[i])
    x0 = PAD["l"] + band * im + band / 2
    out.append(f'<text class="ink" x="{x0:.1f}" y="{sy(tops[im]) - 5:.1f}" text-anchor="middle" font-size="11">{_fmt(tops[im], unit)}</text>')
    if note_idx is not None:
        i, txt = note_idx
        x0 = PAD["l"] + band * i + band / 2
        out.append(f'<text class="ink" x="{x0:.1f}" y="{sy(tops[i]) - 5:.1f}" text-anchor="middle" font-size="11">{_esc(txt)}</text>')
    out.append(f'<line class="axis" x1="{PAD["l"]}" y1="{bot}" x2="{W - PAD["r"]}" y2="{bot}"/>')
    legend = None
    if legend_names:
        legend = [(f"s{j + 1}", nm, "rect") for j, nm in enumerate(legend_names)]
        if ref is not None:
            legend.append(("ref", ref[1], "line"))
    return _frame(title, subtitle, "\n".join(out), legend, h=h)


def lines(title, labels, series, unit="", subtitle="", legend_names=None, ylo=None, yhi=None, h=H, label_every=1, ref=None, end_labels=True, dashed_idx=()):
    n = len(labels)
    allv = [v for s in series for v in s if v is not None]
    lo = min(allv) if ylo is None else ylo
    hi = max(allv) if yhi is None else yhi
    if ylo is None:
        lo = lo - (hi - lo) * 0.15
    if yhi is None:
        hi = hi + (hi - lo) * 0.12
    sy, grid, lo, hi = _yaxis(lo, hi, unit, h)
    top, bot = PAD["t"], h - PAD["b"]
    band = (W - PAD["l"] - PAD["r"]) / max(1, n - 1)
    sx = lambda i: PAD["l"] + band * i
    out = [grid]
    for i, lab in enumerate(labels):
        if i % label_every == 0:
            out.append(f'<text class="mut" x="{sx(i):.1f}" y="{bot + 14}" text-anchor="middle" font-size="10">{_esc(lab)}</text>')
    if ref is not None:
        rv, rname = ref
        y = sy(rv)
        out.append(f'<line class="ref" x1="{PAD["l"]}" y1="{y:.1f}" x2="{W - PAD["r"]}" y2="{y:.1f}"/>')
        out.append(f'<text class="sec" x="{W - PAD["r"]}" y="{y - 4:.1f}" text-anchor="end" font-size="11">{_esc(rname)}</text>')
    for j, s in enumerate(series):
        pts = [(sx(i), sy(v)) for i, v in enumerate(s) if v is not None]
        d = " ".join(f"{'M' if k == 0 else 'L'}{x:.1f},{y:.1f}" for k, (x, y) in enumerate(pts))
        dash = ' stroke-dasharray="4 3"' if j in dashed_idx else ""
        out.append(f'<path class="l{j + 1}" d="{d}" fill="none" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"{dash}/>')
        x, y = pts[-1]
        out.append(f'<circle class="s{j + 1} ring" cx="{x:.1f}" cy="{y:.1f}" r="4" stroke-width="2"/>')
        if end_labels:
            lastv = [v for v in s if v is not None][-1]
            out.append(f'<text class="ink" x="{x - 6:.1f}" y="{y - 8:.1f}" text-anchor="end" font-size="11">{_fmt(lastv, unit)}</text>')
    out.append(f'<line class="axis" x1="{PAD["l"]}" y1="{bot}" x2="{W - PAD["r"]}" y2="{bot}"/>')
    legend = [(f"l{j + 1}", nm, "line") for j, nm in enumerate(legend_names)] if legend_names else None
    if legend and ref is not None:
        legend.append(("ref", ref[1], "line"))
    return _frame(title, subtitle, "\n".join(out), legend, h=h)


def hbars(title, labels, values, unit="", subtitle="", ref=None, h=None, value_labels=None, series_cls=None, ref_values=None):
    n = len(labels)
    rowh = 26
    h = h or PAD["t"] + n * rowh + 30
    lab_w = 150
    x0 = PAD["l"] + lab_w
    x1 = W - PAD["r"] - 60
    hi = max(max(values), (ref[0] if ref else 0), *(ref_values or [0])) * 1.02
    ticks = _ticks(0, hi)
    hi = max(hi, ticks[-1])
    sx = lambda v: x0 + (v / hi) * (x1 - x0)
    out = []
    for t in ticks:
        out.append(f'<line class="grid" x1="{sx(t):.1f}" y1="{PAD["t"]}" x2="{sx(t):.1f}" y2="{PAD["t"] + n * rowh}"/>')
        out.append(f'<text class="mut" x="{sx(t):.1f}" y="{PAD["t"] + n * rowh + 14}" text-anchor="middle" font-size="10">{_fmt(t, unit)}</text>')
    for i, (lab, v) in enumerate(zip(labels, values)):
        y = PAD["t"] + i * rowh + 4
        cls = (series_cls[i] if series_cls else "s1")
        out.append(f'<text class="sec" x="{x0 - 8}" y="{y + 13}" text-anchor="end" font-size="11">{_esc(lab)}</text>')
        out.append(f'<rect class="{cls}" x="{x0}" y="{y}" width="{max(0, sx(v) - x0):.1f}" height="18" rx="3"/>')
        txt = value_labels[i] if value_labels else _fmt(v, unit)
        out.append(f'<text class="ink" x="{sx(v) + 6:.1f}" y="{y + 13}" font-size="11">{_esc(txt)}</text>')
        if ref_values:
            rx = sx(ref_values[i])
            out.append(f'<line class="ref" x1="{rx:.1f}" y1="{y - 2}" x2="{rx:.1f}" y2="{y + 20}"/>')
    if ref is not None:
        rv, rname = ref
        out.append(f'<line class="ref" x1="{sx(rv):.1f}" y1="{PAD["t"] - 4}" x2="{sx(rv):.1f}" y2="{PAD["t"] + n * rowh}"/>')
        out.append(f'<text class="sec" x="{sx(rv):.1f}" y="{PAD["t"] - 6}" text-anchor="middle" font-size="11">{_esc(rname)}</text>')
    legend = [("ref", "brain / target", "line")] if (ref_values or ref) else None
    if legend:
        h += 14
    return _frame(title, subtitle, "\n".join(out), legend, h=h)
