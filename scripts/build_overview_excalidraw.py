"""Draw the ecomOS overview as an Excalidraw file plus a PNG preview.

Output: reviews/diagrams/ecomos-overview.excalidraw and .png
Usage:  python3 scripts/build_overview_excalidraw.py
The PNG is a geometry preview drawn with PIL so the layout can be checked here; Excalidraw draws the real thing.
"""
import json, os, random
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reviews", "diagrams")
os.makedirs(OUT, exist_ok=True)
random.seed(7)
E = []
FONT = 3  # Cascadia in Excalidraw

# palette (light fill, darker stroke)
INK = "#1e1e1e"; MUTED = "#5c5c5c"
TEAL = ("#d3f0ea", "#0e6b60"); AMBER = ("#fdebc8", "#9a600c"); GREY = ("#f1f3f1", "#7a8580"); BLUE = ("#dbe7f6", "#2f5d9e")
GREEN = ("#dff0e4", "#2c7a4b"); ROSE = ("#f6dfdb", "#b23a2d"); WHITE = ("#ffffff", "#7a8580"); DARK = ("#1e2a26", "#1e2a26")


def base(t, x, y, w, h, **k):
    d = {"id": k.pop("id", f"e{len(E)}"), "type": t, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
         "roughness": 0, "opacity": 100, "groupIds": [], "frameId": None, "roundness": {"type": 3} if t == "rectangle" else None,
         "seed": random.randint(1, 10**9), "version": 1, "versionNonce": random.randint(1, 10**9), "isDeleted": False,
         "boundElements": [], "updated": 1, "link": None, "locked": False}
    d.update(k); E.append(d); return d


def text(x, y, s, size=16, color=INK, align="left", w=None, bold=False):
    lines = s.split("\n"); h = int(size * 1.25 * len(lines)); w = w or int(max(len(l) for l in lines) * size * 0.62 + 4)
    return base("text", x, y, w, h, text=s, originalText=s, fontSize=size, fontFamily=FONT, textAlign=align, verticalAlign="top",
                strokeColor=color, lineHeight=1.25, containerId=None, autoResize=True, baseline=size, strokeWidth=1, roundness=None)


def rect(x, y, w, h, fill=WHITE, label=None, size=15, sw=2, dashed=False, id=None):
    r = base("rectangle", x, y, w, h, backgroundColor=fill[0], strokeColor=fill[1], strokeWidth=sw, strokeStyle="dashed" if dashed else "solid", id=id)
    if label:
        lines = label.split("\n"); th = int(size * 1.25 * len(lines))
        t = base("text", x + 8, y + (h - th) / 2, w - 16, th, text=label, originalText=label, fontSize=size, fontFamily=FONT, textAlign="center", verticalAlign="middle",
                 strokeColor=INK, lineHeight=1.25, containerId=r["id"], autoResize=False, baseline=size, strokeWidth=1, roundness=None)
        r["boundElements"].append({"id": t["id"], "type": "text"})
    return r


def ellipse(x, y, w, h, fill=TEAL, label=None, size=15, id=None):
    r = base("ellipse", x, y, w, h, backgroundColor=fill[0], strokeColor=fill[1], id=id)
    if label:
        lines = label.split("\n"); th = int(size * 1.25 * len(lines))
        t = base("text", x + 10, y + (h - th) / 2, w - 20, th, text=label, originalText=label, fontSize=size, fontFamily=FONT, textAlign="center", verticalAlign="middle",
                 strokeColor=INK, lineHeight=1.25, containerId=r["id"], autoResize=False, baseline=size, strokeWidth=1, roundness=None)
        r["boundElements"].append({"id": t["id"], "type": "text"})
    return r


def arrow(x1, y1, x2, y2, color=MUTED, sw=2, dashed=False, via=None, start=None, end=None):
    pts = [[0, 0]] + ([[vx - x1, vy - y1] for vx, vy in via] if via else []) + [[x2 - x1, y2 - y1]]
    a = base("arrow", x1, y1, abs(x2 - x1), abs(y2 - y1), points=pts, strokeColor=color, strokeWidth=sw, strokeStyle="dashed" if dashed else "solid",
             startArrowhead=None, endArrowhead="arrow", roundness={"type": 2}, lastCommittedPoint=None, elbowed=False,
             startBinding={"elementId": start["id"], "focus": 0, "gap": 4} if start else None, endBinding={"elementId": end["id"], "focus": 0, "gap": 4} if end else None)
    for el in (start, end):
        if el is not None:
            el["boundElements"].append({"id": a["id"], "type": "arrow"})
    return a


def line(x1, y1, x2, y2, color=MUTED, sw=1, dashed=False):
    return base("line", x1, y1, abs(x2 - x1) or 1, abs(y2 - y1) or 1, points=[[0, 0], [x2 - x1, y2 - y1]], strokeColor=color, strokeWidth=sw, strokeStyle="dashed" if dashed else "solid", roundness=None)


def dot(x, y, r=7, fill=TEAL):
    return base("ellipse", x - r, y - r, 2 * r, 2 * r, backgroundColor=fill[1], strokeColor=fill[1])


# ---------------- Title ----------------
text(60, 40, "ecomOS: what has been built so far", 34)
text(60, 88, "25 Sep 2026. Left: the system, 4 layers with the founder deciding. Top right: the loop that runs every day.", 15, MUTED)
text(60, 110, "Bottom right: the build, in order, with what each step produced. Bottom: one job as a new hire does it.", 15, MUTED)

# ---------------- Section A: the layered system (left) ----------------
AX, AY, AW = 60, 170, 880
text(AX, AY, "THE SYSTEM", 13, "#0e6b60")
# Surfaces
rect(AX, AY + 26, AW, 92, GREY, sw=1)
text(AX + 16, AY + 36, "Surfaces", 18)
text(AX + 16, AY + 62, "what people see and act on", 13, MUTED)
for i, (lab, fill) in enumerate([("Today: the break\nand the top 10", TEAL), ("28 rooms\none per domain", TEAL), ("Brand brain\nviewer", WHITE), ("Registry and\nmemory", WHITE), ("Agency\nportfolio", WHITE)]):
    rect(AX + 300 + i * 112, AY + 40, 104, 62, fill, lab, 12, sw=1)
# Founder gate
gate = rect(AX, AY + 132, AW, 58, AMBER, sw=2)
text(AX + 16, AY + 142, "Founder gate", 18)
text(AX + 16, AY + 162, "nothing below runs on an idea the founder has not approved.\nWrites to Meta, the site or email stay off until switched on per surface.", 11, MUTED)
for i, lab in enumerate(["Let the agent do it", "Send to a person", "Not now, with reason"]):
    rect(AX + 548 + i * 110, AY + 143, 102, 34, WHITE, lab, 10, sw=1)
# Execution
rect(AX, AY + 204, AW, 300, GREY, sw=1)
text(AX + 16, AY + 214, "Execution", 18)
text(AX + 16, AY + 240, "15 agents. 7 run and guard the loop, 8 do the work.", 13, MUTED)
orch = rect(AX + 16, AY + 268, 160, 54, BLUE, "Orchestrator\naccount manager", 12)
loopnames = ["Diagnose", "Propose", "Registrar", "QA Gate", "Brain Keeper", "Ref. Scout"]
for i, n in enumerate(loopnames):
    r = rect(AX + 16 + (i % 3) * 56, AY + 336 + (i // 3) * 40, 52, 34, BLUE, n, 9, sw=1)
text(AX + 16, AY + 420, "loop agents:\ncode does the maths,\nthe model fills evidence", 11, MUTED)
specs = [("Site", "05 07 08 09", "80"), ("Creative and copy", "10 11", "39"), ("Media buyer", "24 12", "50"), ("Lifecycle", "14 17 03", "53"), ("Organic and search", "13 15 16", "43"), ("Product and supply", "01 18 22", "72"), ("Money and ops", "20 21 06 23", "76"), ("Brand strategist", "02 04 19", "61")]
sx0, sy0 = AX + 230, AY + 262
srects = []
for i, (n, folders, caps) in enumerate(specs):
    x = sx0 + (i % 4) * 160; y = sy0 + (i // 4) * 104
    r = rect(x, y, 148, 84, TEAL, f"{n}\nfolders {folders}\n{caps} capabilities", 11, sw=1)
    srects.append(r)
# fan-out arrows from orchestrator to specialists (to first column only, to keep it clean) plus one label
arrow(AX + 176, AY + 295, sx0, sy0 + 42, MUTED, 2, start=orch, end=srects[0])
arrow(AX + 176, AY + 300, sx0, sy0 + 146, MUTED, 2, start=orch, end=srects[4])
text(sx0, AY + 474, "559 capabilities, one owner each  |  235 workflows  |  348 skills in a tree the agent picks from", 12, "#0e6b60")
# Inspiration
rect(AX, AY + 518, AW, 66, GREY, sw=1)
text(AX + 16, AY + 528, "Inspiration", 18)
text(AX + 16, AY + 554, "references by angle, format and mood. Structure only,\nnever another brand's text, logo, product or face.", 11, MUTED)
rect(AX + 640, AY + 528, 224, 44, WHITE, "7 competitor brands in the gallery\nReference Scout, creative retrieval", 11, sw=1)
# Intelligence
rect(AX, AY + 598, AW, 96, GREY, sw=1)
text(AX + 16, AY + 608, "Intelligence", 18)
text(AX + 16, AY + 634, "what experts know, as records code can filter and score", 12, MUTED)
rect(AX + 420, AY + 610, 140, 70, TEAL, "Idea bank\n4,650 ideas\n25 domains", 12, sw=1)
rect(AX + 572, AY + 610, 140, 70, TEAL, "Card library\n7,611 cards\n256 documents", 12, sw=1)
rect(AX + 724, AY + 610, 140, 70, WHITE, "Playbooks v2\nfrozen reference\n(2 blind tests)", 11, sw=1, dashed=True)
# Data
rect(AX, AY + 708, AW, 96, GREY, sw=1)
text(AX + 16, AY + 718, "Data: the brand brain", 18)
text(AX + 16, AY + 744, "the brand's own facts, numbers\nand decisions. Missing shows as\nunavailable, never 0.", 12, MUTED)
for i, (lab, fill) in enumerate([("Brand record\nclaims in 3 tiers", WHITE), ("Metric contract\ncomputed in code", WHITE), ("Experiment\nregistry", WHITE), ("277 tables\nby source", TEAL)]):
    rect(AX + 420 + i * 116, AY + 720, 108, 68, fill, lab, 11, sw=1)
text(AX, AY + 816, "Built today (teal): Meta cache 1 year, sales, brand record v0, competitors, speed lab, idea bank, cards.  To build (white): brain schema, contract, registry, agents.", 12, MUTED)
text(AX, AY + 836, "Dashed: kept but not loaded as instructions.", 12, MUTED)

# ---------------- Section B: the daily loop (top right) ----------------
BX, BY = 1020, 170
text(BX, BY, "THE LOOP, EVERY DAY", 13, "#0e6b60")
cx, cy, R = BX + 420, BY + 270, 240
import math
steps = [("04:00 Collect\nBrain Keeper", WHITE), ("04:20 Diagnose\nthe break, stake", BLUE), ("04:30 Propose\nbank + audit + web,\nrank in code", BLUE), ("09:00 Founder\ndecides", AMBER), ("Execute\nspecialist + skills", TEAL), ("QA Gate\nclaims, numbers,\nwrites", BLUE), ("Read point\nRegistrar", BLUE), ("Learn\nbrand prior updates", TEAL)]
nodes = []
for i, (lab, fill) in enumerate(steps):
    ang = -math.pi / 2 + i * 2 * math.pi / len(steps)
    x = cx + R * math.cos(ang) - 70; y = cy + R * math.sin(ang) - 30
    nodes.append(rect(x, y, 140, 60, fill, lab, 11, sw=2 if fill is AMBER else 1))
for i in range(len(steps)):
    a = nodes[i]; b = nodes[(i + 1) % len(steps)]
    ax, ay = a["x"] + 70, a["y"] + 30; bx_, by_ = b["x"] + 70, b["y"] + 30
    # shorten to box edges
    dx, dy = bx_ - ax, by_ - ay; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    t = min(70 / abs(ux) if ux else 1e9, 30 / abs(uy) if uy else 1e9) + 6
    arrow(ax + ux * t, ay + uy * t, bx_ - ux * t, by_ - uy * t, MUTED, 2, start=a, end=b)
text(cx - 110, cy - 24, "numbers first, web last,\nsource carries no weight", 12, MUTED, align="center", w=220)
text(BX, BY + 590, "Proof it works: the speed lab on Gehna's homepage. 8 fixes measured on a copy of the live page.", 13)
rect(BX, BY + 616, 200, 46, ROSE, "Before: 15.4 s fully loaded", 12, sw=1)
arrow(BX + 204, BY + 639, BX + 246, BY + 639, MUTED, 2)
rect(BX + 250, BY + 616, 200, 46, GREEN, "After: 5.2 s, LCP 1.70 to 1.22 s", 12, sw=1)
text(BX + 470, BY + 624, "4.34 MB to 1.98 MB. Founder page with 3 decisions per fix, filmstrip before and after.", 12, MUTED, w=380)

# ---------------- Section C: the build timeline (bottom right) ----------------
CX, CY = 1020, 880
text(CX, CY, "THE BUILD, IN ORDER", 13, "#0e6b60")
tl_x = CX + 14
line(tl_x, CY + 34, tl_x, CY + 34 + 8 * 62, MUTED, 2)
events = [
    ("24 Sep", "Library: 7,611 cards. Playbooks v2 tested twice, lost both, frozen.", GREY),
    ("24 Sep", "Idea bank: 4,650 ideas from 25 playbooks, schema, validator, ranker v0.", TEAL),
    ("24 Sep", "Speed lab on Gehna: 8 fixes, 15.4 s to 5.2 s, founder plan page, filmstrip.", TEAL),
    ("25 Sep", "Blueprint: business idea, new founder, existing brand, agency, architecture.", TEAL),
    ("25 Sep", "Wave 1 and 2: 15 agents, capabilities from the bank then from real roles. Review to 559.", TEAL),
    ("25 Sep", "Wave 3: 28 rooms, 465 metrics with formulas, 351 insights as rules, 277 tables.", TEAL),
    ("25 Sep", "Wave 4: 235 workflows, 348 skills with SKILL.md files, selection rules, routing.", TEAL),
    ("next", "Brand brain schema and metric contract for Gehna, then Diagnose and Propose end to end.", AMBER),
]
for i, (when, what, fill) in enumerate(events):
    y = CY + 34 + i * 62
    dot(tl_x, y + 10, 7, fill if fill is not GREY else ("#ffffff", "#7a8580"))
    text(tl_x + 22, y, when, 12, "#0e6b60" if fill is not AMBER else "#9a600c")
    text(tl_x + 90, y, what, 13, INK, w=720)
text(CX + 100, CY + 34 + 8 * 62 + 4, "4 pages published: Blueprint, Agent catalogue, Rooms, Workflows. All in the repo under agents/ and reviews/.", 12, MUTED, w=740)

# ---------------- Section D: one job end to end (bottom) ----------------
DX, DY = 60, 1480
text(DX, DY, "ONE JOB AS A NEW HIRE DOES IT: launch a paid creative test (CREA-W01, 14 steps, shown as 7)", 13, "#0e6b60")
job = [("1 Objection map\nand format scan", "crea/research/\nobjection-and-format-scan"), ("2 Competitor signal\nlayout and mood only", "crea/research/\ncompetitor-signal-pull"), ("3 Angles and\ntest plan", "crea/angle-and-test/\nangle-builder"), ("4 Audience spec\nhanded to Media", "crea/angle-and-test/\naudience-spec"), ("5 Hooks, scripts,\nbriefs per format", "crea/make-creatives/\nugc-video | static"), ("6 Claim check and\nScout references", "shared/claim-check\nreference-scout"), ("7 Launch checklist,\nread, registry", "shared/registry-entry\nfirst-read")]
line(DX, DY + 70, DX + 7 * 280 - 60, DY + 70, MUTED, 2)
for i, (st, sk) in enumerate(job):
    x = DX + i * 280
    dot(x + 10, DY + 70, 7, TEAL)
    text(x, DY + 84, st, 12)
    rect(x, DY + 126, 220, 44, TEAL, sk, 10, sw=1)
text(DX, DY + 186, "Every step: what the agent does, the inputs, the tools, the skill it loads, the output, the check, and when it stops to ask the founder. A sub-skill is picked by format, channel or platform.", 12, MUTED, w=1900)

# ---------------- write ----------------
doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com", "elements": E, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": 20}, "files": {}}
json.dump(doc, open(os.path.join(OUT, "ecomos-overview.excalidraw"), "w"), indent=1)

# ---------------- PIL preview ----------------
W = max(e["x"] + e["width"] for e in E) + 60; H = max(e["y"] + e["height"] for e in E) + 60
img = Image.new("RGB", (int(W), int(H)), "white"); dr = ImageDraw.Draw(img)
def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, int(sz * 0.9))
    return ImageFont.load_default()
for e in E:
    x, y, w, h = e["x"], e["y"], e["width"], e["height"]
    if e["type"] == "rectangle":
        dr.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=e["backgroundColor"] if e["backgroundColor"] != "transparent" else None, outline=e["strokeColor"], width=e["strokeWidth"])
    elif e["type"] == "ellipse":
        dr.ellipse([x, y, x + w, y + h], fill=e["backgroundColor"] if e["backgroundColor"] != "transparent" else None, outline=e["strokeColor"], width=e["strokeWidth"])
    elif e["type"] in ("arrow", "line"):
        pts = [(x + px, y + py) for px, py in e["points"]]
        dr.line(pts, fill=e["strokeColor"], width=e["strokeWidth"])
        if e["type"] == "arrow":
            (x1, y1), (x2, y2) = pts[-2], pts[-1]; ang = math.atan2(y2 - y1, x2 - x1)
            for s in (-0.5, 0.5):
                dr.line([(x2, y2), (x2 - 12 * math.cos(ang + s), y2 - 12 * math.sin(ang + s))], fill=e["strokeColor"], width=e["strokeWidth"])
for e in E:
    if e["type"] == "text":
        f = font(e["fontSize"]); lines = e["text"].split("\n"); lh = e["fontSize"] * 1.25
        for i, l in enumerate(lines):
            tw = dr.textlength(l, font=f)
            tx = e["x"] if e["textAlign"] == "left" else e["x"] + (e["width"] - tw) / 2
            ty = e["y"] + i * lh + (0 if e.get("containerId") is None else 0)
            dr.text((tx, ty), l, fill=e["strokeColor"], font=f)
img.save(os.path.join(OUT, "ecomos-overview.png"))
print(len(E), "elements;", img.size)
