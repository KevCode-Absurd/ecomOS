"""Build the founder-facing retest page: 25 Sep against 12 Oct, what shipped, the next limiter.

Usage: python3 speed_lab/build_retest_page.py
Reads results/baseline-settle25.json, live-1012-settle25.json, live-1012-no-rocket.json and the two store indexes.
Writes reviews/speed-lab/gehna-speed-retest.html.
"""
import base64, html, io, json, os, re
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(ROOT, "results")
OUT = os.path.join(os.path.dirname(ROOT), "reviews", "speed-lab", "gehna-speed-retest.html")


def med(label):
    return json.load(open(os.path.join(RES, label + ".json")))["median"]


def shot(label, width=320):
    im = Image.open(os.path.join(RES, label + "-run1.png")).convert("RGB")
    h = int(im.height * width / im.width)
    im = im.resize((width, h), Image.LANCZOS).crop((0, 0, width, min(h, 560)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=68, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def store_stats(path):
    idx = json.load(open(os.path.join(path, "index.json")))
    fp = [e for e in idx.values() if e["url"].split("/")[2].endswith("gehnaindia.com")]
    fonts = sum(e["size"] for e in fp if e["type"] == "font")
    icons = [e for e in fp if "_next/image" in e["url"] and "browse-categories" in e["url"]]
    return {"fonts": fonts, "icons": sum(e["size"] for e in icons), "icon_w": re.search(r"w=(\d+)", icons[0]["url"]).group(1) if icons else "?",
            "scripts": sum(e["size"] for e in fp if e["type"] == "script")}


old, new, norl = med("baseline-settle25"), med("live-1012-settle25"), med("live-1012-no-rocket")
so, sn = store_stats(os.path.join(ROOT, "store")), store_stats(os.path.join(ROOT, "store-2026-10-12"))


def s(ms): return f"{ms/1000:.1f} s"
def mb(b): return f"{b/1048576:.2f} MB" if b >= 1048576 else f"{b/1024:.0f} KB"
def pct(a, b): return f"{(b-a)/a*100:+.0f}%"


MILESTONES = [("First paint", "fcp_ms"), ("Banner shown", "lcp_ms"), ("Load event", "load_ms"), ("Page responds to taps", "hydrated_ms"), ("Marketing tags start", "tags_start_ms")]


def dumbbell(a, b, la, lb, xmax, cls_a="s1", cls_b="s2", rows=MILESTONES, unit="s"):
    """Two-series dot plot, one row per milestone, to one x scale. Direct labels on both marks."""
    W, left, right, rowh, top = 500, 150, 26, 46, 28
    H = top + rowh * len(rows) + 30
    px = lambda v: left + (W - left - right) * min(v, xmax) / xmax
    ticks = list(range(0, int(xmax) + 1, 3))
    o = [f'<svg class="dumb" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(la)} against {html.escape(lb)}">']
    for t in ticks:
        x = px(t); o.append(f'<line class="grid" x1="{x:.1f}" y1="{top-8}" x2="{x:.1f}" y2="{H-26}"/><text class="tick" x="{x:.1f}" y="{H-8}" text-anchor="middle">{t}{unit}</text>')
    for i, (name, key) in enumerate(rows):
        y = top + rowh * i + rowh / 2
        va, vb = a[key] / 1000, b[key] / 1000
        o.append(f'<text class="lab" x="{left-12}" y="{y+4:.1f}" text-anchor="end">{html.escape(name)}</text>')
        o.append(f'<line class="link" x1="{px(va):.1f}" y1="{y:.1f}" x2="{px(vb):.1f}" y2="{y:.1f}"/>')
        for v, cls, lab in ((va, cls_a, la), (vb, cls_b, lb)):
            o.append(f'<g class="mark {cls}" tabindex="0"><title>{html.escape(lab)}: {html.escape(name)} at {v:.1f} s</title><circle cx="{px(v):.1f}" cy="{y:.1f}" r="7"/></g>')
        # direct labels: before above, now below, so they never collide
        o.append(f'<text class="val" x="{px(va):.1f}" y="{y-12:.1f}" text-anchor="middle">{va:.1f}</text>')
        o.append(f'<text class="val" x="{px(vb):.1f}" y="{y+22:.1f}" text-anchor="middle">{vb:.1f}</text>')
    o.append("</svg>")
    return "".join(o)


def bars(pairs, la, lb):
    """Grouped bars for byte sizes, one scale, direct labels."""
    W, left, right, rowh, top = 500, 150, 84, 48, 10
    H = top + rowh * len(pairs) + 6
    xmax = max(max(p[1], p[2]) for p in pairs)
    px = lambda v: (W - left - right) * v / xmax
    o = [f'<svg class="bars" viewBox="0 0 {W} {H}" role="img" aria-label="Bytes {html.escape(la)} against {html.escape(lb)}">']
    for i, (name, va, vb) in enumerate(pairs):
        y = top + rowh * i
        o.append(f'<text class="lab" x="{left-12}" y="{y+27}" text-anchor="end">{html.escape(name)}</text>')
        for j, (v, cls, lab) in enumerate(((va, "s1", la), (vb, "s2", lb))):
            yy = y + 6 + j * 18
            o.append(f'<g class="mark {cls}" tabindex="0"><title>{html.escape(lab)}: {html.escape(name)} {mb(v)}</title><rect x="{left}" y="{yy}" width="{max(px(v),2):.1f}" height="14" rx="3"/></g>')
            o.append(f'<text class="val" x="{left+px(v)+8:.1f}" y="{yy+11}">{mb(v)}</text>')
    o.append("</svg>")
    return "".join(o)


FIXES = [
    ("1", "Turn off Cloudflare Rocket Loader", False, "31 script tags are still rewritten and the loader still runs."),
    ("2", "Subset the two Korean fonts", True, f"Fonts went from {mb(so['fonts'])} TTF to {mb(sn['fonts'])} WOFF2."),
    ("3", "Load marketing tags after the page is ready", False, f"Still waiting for hydration. Tags start at {s(new['tags_start_ms'])}."),
    ("4", "Smaller category icons", True, f"7 icons at {sn['icon_w']} px WebP, {mb(sn['icons'])} instead of {mb(so['icons'])}."),
    ("5", "Lato in WOFF2", True, "Done with the font change."),
    ("6", "Preload the banner image", False, "No priority on the first slide yet."),
    ("8", "Inline the two render-blocking stylesheets", False, "2 CSS links remain."),
    ("9", "Remove the old Universal Analytics tag", False, "gtag/js?id=UA-41818105-2 still loads on every visit."),
]
done = sum(1 for f in FIXES if f[2])

tiles = [
    ("Load event", s(old["load_ms"]), s(new["load_ms"]), pct(old["load_ms"], new["load_ms"])),
    ("Banner shown", s(old["lcp_ms"]), s(new["lcp_ms"]), pct(old["lcp_ms"], new["lcp_ms"])),
    ("Page responds to taps", s(old["hydrated_ms"]), s(new["hydrated_ms"]), pct(old["hydrated_ms"], new["hydrated_ms"])),
    ("Bytes downloaded", mb(old["wire_bytes"]), mb(new["wire_bytes"]), pct(old["wire_bytes"], new["wire_bytes"])),
]

page = f'''<title>Gehna Speed Retest</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&display=swap">
<style>
/* Layout: one column, 860px max, tiles then charts then the fix ledger. Same palette as the speed plan page so the two read as one set. */
:root{{--bg:#F7F5F0;--panel:#FFFFFF;--ink:#1E1C19;--muted:#6B665D;--line:#DDD8CD;--accent:#8E6A1C;--accent-ink:#FFFFFF;--good:#2F6B3A;--goodbg:#E6F0E7;--warn:#9A5A0A;--warnbg:#F6EBD9;--code:#EFECE4;
--s1:#2a78d6;--s2:#eda100;--grid:#E6E1D6;
--display:'Sora',system-ui,sans-serif;--body:'Source Sans 3',system-ui,sans-serif}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#17161A;--panel:#211F24;--ink:#EDEAE3;--muted:#A49E92;--line:#3A373F;--accent:#D8AE52;--accent-ink:#1E1C19;--good:#7CC48A;--goodbg:#1F2E22;--warn:#E0A552;--warnbg:#332A1C;--code:#2B2930;--s1:#3987e5;--s2:#c98500;--grid:#33313A;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#17161A;--panel:#211F24;--ink:#EDEAE3;--muted:#A49E92;--line:#3A373F;--accent:#D8AE52;--accent-ink:#1E1C19;--good:#7CC48A;--goodbg:#1F2E22;--warn:#E0A552;--warnbg:#332A1C;--code:#2B2930;--s1:#3987e5;--s2:#c98500;--grid:#33313A;color-scheme:dark}}
body{{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:17px;line-height:1.55;padding-inline:16px;padding-block:0 60px}}
main{{max-width:860px;margin:0 auto}}
.eyebrow{{font:600 12px var(--display);letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-top:28px}}
h1{{font-family:var(--display);font-size:clamp(26px,4vw,36px);font-weight:700;letter-spacing:-.015em;margin:6px 0 10px;text-wrap:balance}}
h2{{font-family:var(--display);font-size:21px;margin:36px 0 10px;text-wrap:balance}}
p{{max-width:66ch;margin:0 0 10px}} .muted{{color:var(--muted)}} .small{{font-size:14px;color:var(--muted);max-width:72ch}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:10px;margin:18px 0 6px}}
.tile{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px;min-width:0}}
.tile .l{{font:600 12px var(--display);letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}}
.tile .v{{font:700 28px var(--display);margin-top:4px;letter-spacing:-.01em;font-variant-numeric:tabular-nums;color:var(--good)}}
.tile .was{{font-size:14px;color:var(--muted);font-variant-numeric:tabular-nums}} .tile .was s{{text-decoration-thickness:1.5px}}
.tile .d{{display:inline-block;margin-top:6px;font:600 13px var(--display);background:var(--goodbg);color:var(--good);border-radius:6px;padding:2px 7px}}
.tile .d.flat{{background:var(--code);color:var(--muted)}}
.chart{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px 8px;margin:12px 0}}
.chart h3{{font-family:var(--display);font-size:17px;margin:0 0 4px}}
.legend{{display:flex;gap:16px;flex-wrap:wrap;font-size:14px;color:var(--muted);margin:4px 0 6px}}
.legend i{{display:inline-block;width:12px;height:12px;border-radius:50%;vertical-align:-1px;margin-right:6px}}
.legend .a i{{background:var(--s1)}} .legend .b i{{background:var(--s2)}}
svg.dumb,svg.bars{{width:100%;height:auto;display:block;overflow:visible}}
svg .grid{{stroke:var(--grid);stroke-width:1}} svg .tick{{font:13px var(--body);fill:var(--muted)}}
svg .lab{{font:600 15px var(--body);fill:var(--ink)}} svg .val{{font:600 13px var(--body);fill:var(--muted);font-variant-numeric:tabular-nums}}
svg .link{{stroke:var(--line);stroke-width:2}}
svg .mark.s1 circle,svg .mark.s1 rect{{fill:var(--s1)}} svg .mark.s2 circle,svg .mark.s2 rect{{fill:var(--s2)}}
svg .mark circle{{stroke:var(--panel);stroke-width:2}} svg .mark:hover circle,svg .mark:focus circle{{r:9;outline:none}} svg .mark:focus-visible{{outline:2px solid var(--accent)}}
.shots{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:14px 0}}
.shots figure{{margin:0;min-width:0}} .shots img{{width:100%;max-width:100%;border:1px solid var(--line);border-radius:8px;display:block;background:var(--code)}} .shots figcaption{{font-size:13px;color:var(--muted);margin-top:4px}}
table{{width:100%;border-collapse:collapse;font-size:15px;margin:10px 0}} .tw{{overflow-x:auto}}
th{{text-align:left;font:600 12px var(--display);letter-spacing:.05em;text-transform:uppercase;color:var(--muted);padding:8px 10px;border-bottom:1px solid var(--line)}}
td{{padding:10px;border-bottom:1px solid var(--line);vertical-align:top}} td.n{{font:700 16px var(--display);color:var(--accent);width:28px}}
.pill{{display:inline-block;font:600 12px var(--display);border-radius:999px;padding:3px 9px;white-space:nowrap}}
.pill.ok{{background:var(--goodbg);color:var(--good)}} .pill.no{{background:var(--warnbg);color:var(--warn)}}
.box{{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:10px;padding:14px 18px;max-width:72ch;margin:14px 0}}
.box strong{{font-family:var(--display)}}
@media (max-width:520px){{.shots{{grid-template-columns:1fr 1fr}} svg .lab{{font-size:13px}}}}
@media (prefers-reduced-motion: no-preference){{svg .mark circle{{transition:r .15s}}}}
</style>
<main>
<div class="eyebrow">Gehna homepage, retested 12 October 2026</div>
<h1>The font fix worked. Now the page needs to wake up sooner.</h1>
<p>Same phone, same slow connection, same test as on 25 September. Your homepage now finishes loading in {s(new["load_ms"])} instead of {s(old["load_ms"])} and sends less than half the data. It still takes about {new["hydrated_ms"]/1000:.0f} seconds before search, cart and the carousels respond to a tap. One Cloudflare setting is now the reason.</p>

<div class="tiles">
{"".join(f'<div class="tile"><div class="l">{t[0]}</div><div class="v">{t[2]}</div><div class="was">was <s>{t[1]}</s></div><div class="d{" flat" if abs(float(t[3].strip("%+"))) < 5 else ""}">{t[3]}</div></div>' for t in tiles)}
</div>
<p class="small">Medians of 3 runs on a Pixel 5 profile, slow 4G at 1.6 Mbps, 4x slower processor, cold cache. The browser kept watching for 25 s after the load event, because the marketing tags now start on a timer. The 25 Sep copy of the page was re-run the same way, so both columns compare.</p>

<h2>When things happen, before and after</h2>
<div class="chart">
<h3>Seconds from the first tap on the link</h3>
<div class="legend"><span class="a"><i></i>25 Sep</span><span class="b"><i></i>12 Oct</span></div>
{dumbbell(old, new, "25 Sep", "12 Oct", 18)}
<p class="small">First paint and the banner barely moved: they were already quick. The load event moved from {s(old["load_ms"])} to {s(new["load_ms"])} because the two 3 MB font files are gone. The page becoming usable moved from {s(old["hydrated_ms"])} to {s(new["hydrated_ms"])}, and the trackers follow it.</p>
</div>

<div class="chart">
<h3>What the phone downloads</h3>
<div class="legend"><span class="a"><i></i>25 Sep</span><span class="b"><i></i>12 Oct</span></div>
{bars([("Everything", old["wire_bytes"], new["wire_bytes"]), ("Your site", old["first_party_bytes"], new["first_party_bytes"]), ("Trackers and tags", old["third_party_bytes"], new["third_party_bytes"]), ("Fonts, unpacked", so["fonts"], sn["fonts"]), ("7 category icons", so["icons"], sn["icons"])], "25 Sep", "12 Oct")}
<p class="small">Your own files halved. The trackers did not change: Google Tag Manager, the Meta pixel, Klaviyo and Clarity still add {mb(new["third_party_bytes"])} on every visit, half of the total now.</p>
</div>

<div class="shots">
<figure><img src="{shot("baseline-settle25")}" alt="Homepage on 25 Sep, 25 seconds after load"><figcaption>25 Sep, 25 s after the load event</figcaption></figure>
<figure><img src="{shot("live-1012-settle25")}" alt="Homepage on 12 Oct, 25 seconds after load"><figcaption>12 Oct, 25 s after the load event</figcaption></figure>
</div>

<h2>What shipped from the September plan</h2>
<p>{done} of 8 fixes are live. The 5 that are not are the ones that decide how soon the page responds.</p>
<div class="tw"><table>
<thead><tr><th>#</th><th>Fix</th><th>Status</th><th>What we see today</th></tr></thead>
<tbody>
{"".join(f'<tr><td class="n">{n}</td><td>{html.escape(t)}</td><td><span class="pill {"ok" if ok else "no"}">{"Done" if ok else "Not yet"}</span></td><td class="small">{html.escape(note)}</td></tr>' for n, t, ok, note in FIXES)}
</tbody></table></div>
<p class="small">Nothing else on the page changed: same Next.js build shape ({mb(sn["scripts"])} of script), same images, same inline styles, same tags.</p>

<h2>What a shopper feels now</h2>
<p>The page paints as fast as before and the banner shows a third of a second sooner. Nothing is downloading in the background for 14 seconds any more, so the phone stays cool and the data bill is half. But for about {new["hydrated_ms"]/1000:.0f} seconds the page looks ready and is not: taps on search, the cart, the menu and the product carousels do nothing. The code that makes the page work is held back by Rocket Loader, a Cloudflare add-on that runs your scripts one at a time after the load event.</p>

<h2>The next limiter, measured</h2>
<div class="chart">
<h3>12 Oct page, with Rocket Loader on and off</h3>
<div class="legend"><span class="a"><i></i>Rocket Loader on (today)</span><span class="b"><i></i>Rocket Loader off, nothing else changed</span></div>
{dumbbell(new, norl, "Rocket Loader on", "Rocket Loader off", 18)}
<p class="small">Off, the page responds at {s(norl["hydrated_ms"])} instead of {s(new["hydrated_ms"])}. But on its own it hurts: the banner slips to {s(norl["lcp_ms"])} because {mb(sn["scripts"])} of script now competes with it on the slow link, and the load event moves out to {s(norl["load_ms"])} because the trackers fire before it. The same pattern showed in September.</p>
</div>
<div class="box"><strong>Ship as one release:</strong> Rocket Loader off, the trackers moved to load after the page is ready (fix 3), and the banner preloaded (fix 6). Together they keep the fast banner and bring the page to life at about 5 to 6 seconds on this profile. Then fix 8, then fix 9. The developer briefs for each are on the <a href="https://claude.ai/artifact/UPCXKQJiadjRe6CP5NTMnA">speed plan page</a>.</div>

<p class="small">Method: an offline copy of www.gehnaindia.com recorded on 12 Oct and replayed on a local server, so every run sees the same files. Lab numbers are kinder than the live site because the server answers instantly. Differences between runs are fair; absolute seconds in the real world are longer. Raw results are in the ecomOS repo under speed_lab/results.</p>
</main>
'''
open(OUT, "w", encoding="utf-8").write(page)
print("wrote", OUT, f"{os.path.getsize(OUT)/1024:.0f} KB", "| fixes done", done, "| tiles", [(t[0], t[1], t[2], t[3]) for t in tiles])
