"""Merge the third jobs list (app/jtbd/v3/<slug>.json) into JOBS-v3.md and an HTML page.

Tactical jobs grouped under top jobs, each with enablers, inputs, steps and a metric chain.
Total = 4 x money + 2 x satisfaction + 2 x speed + 2 x ease (max 50).
Start now = ready 4 or 5, and effort hours or days.

Usage: python3 app/jtbd/build_v3.py [--html OUT.html]
"""
import argparse, glob, html, json, os, re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.join(HERE, "v3")
FIELDS = ["id", "top", "job", "trigger", "enablers", "inputs", "steps", "output", "next", "watch", "drives", "business", "score", "ready", "effort"]
BUSINESS = {"revenue", "gross profit", "contribution margin", "cash", "customer satisfaction", "risk"}
STATUS = ["connected", "brain", "founder", "have", "setup", "buy", "enabler"]
STATUS_LABEL = {"connected": "connected on day one", "brain": "from the brain", "founder": "ask the founder", "have": "in ecomOS now",
                "setup": "set up in a day", "buy": "paid tool or person", "enabler": "build an enabler first"}
EFFORT = {"hours", "days", "weeks"}
SCORES = ("money", "satisfaction", "speed", "ease")


def total(s):
    return 4 * s["money"] + 2 * s["satisfaction"] + 2 * s["speed"] + 2 * s["ease"]


def walk_text(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from walk_text(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk_text(v)


def load():
    problems = []
    enablers = {x["id"]: dict(x, origin="shared") for x in json.load(open(os.path.join(V3, "enablers.json"), encoding="utf-8"))}
    screens = []
    for f in sorted(glob.glob(os.path.join(V3, "[0-9][0-9]-*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception as ex:
            problems.append(f"{os.path.basename(f)}: bad JSON {ex}")
            continue
        for ne in d.get("new_enablers", []) or []:
            if ne.get("id") in enablers:
                if enablers[ne["id"]].get("origin") != "shared":
                    problems.append(f"{d['screen']}: new enabler id {ne['id']} also added by {enablers[ne['id']]['origin']}")
                continue
            enablers[ne["id"]] = dict(ne, origin=d["screen"])
        screens.append(d)
    ids = set()
    for d in screens:
        sid = d["screen"]
        for t in walk_text(d):
            if "—" in t:
                problems.append(f"{sid}: em dash in '{t[:60]}'")
        tops = {t["id"] for t in d.get("top_jobs", [])}
        if not 3 <= len(tops) <= 5:
            problems.append(f"{sid}: {len(tops)} top jobs")
        jobs = d.get("jobs", [])
        if len(jobs) != 20:
            problems.append(f"{sid}: {len(jobs)} jobs, expected 20")
        per_top = defaultdict(int)
        for j in jobs:
            miss = [k for k in FIELDS if k not in j]
            if miss:
                problems.append(f"{sid} {j.get('id')}: missing {miss}")
                continue
            if j["id"] in ids:
                problems.append(f"{sid}: duplicate id {j['id']}")
            ids.add(j["id"])
            if not j["id"].startswith(sid[:2] + "-"):
                problems.append(f"{sid}: id {j['id']} does not match screen")
            if j["top"] not in tops:
                problems.append(f"{sid} {j['id']}: top {j['top']} unknown")
            per_top[j["top"]] += 1
            for en in j["enablers"]:
                if en not in enablers:
                    problems.append(f"{sid} {j['id']}: unknown enabler {en}")
            for i in j["inputs"]:
                if i.get("status") not in STATUS:
                    problems.append(f"{sid} {j['id']}: input status {i.get('status')}")
            if not 3 <= len(j["steps"]) <= 7:
                problems.append(f"{sid} {j['id']}: {len(j['steps'])} steps")
            if j["business"] not in BUSINESS:
                problems.append(f"{sid} {j['id']}: business {j['business']}")
            if j["effort"] not in EFFORT:
                problems.append(f"{sid} {j['id']}: effort {j['effort']}")
            for k in SCORES:
                if not isinstance(j["score"].get(k), int) or not 1 <= j["score"][k] <= 5:
                    problems.append(f"{sid} {j['id']}: score {k}")
            if not isinstance(j["ready"], int) or not 1 <= j["ready"] <= 5:
                problems.append(f"{sid} {j['id']}: ready {j['ready']}")
            j["total"] = total(j["score"]) if all(isinstance(j["score"].get(k), int) for k in SCORES) else 0
            j["start_now"] = j["ready"] >= 4 and j["effort"] in ("hours", "days")
            j["screen"] = sid
            j["title"] = d["title"]
        for t in tops:
            if per_top[t] < 3:
                problems.append(f"{sid}: top job {t} has {per_top[t]} tactical jobs")
    for d in screens:
        d["jobs"] = [j for j in d["jobs"] if "total" in j]
    return screens, enablers, problems


def start_now(screens, n=30, cap=3):
    pool = sorted((j for d in screens for j in d["jobs"] if j["start_now"]), key=lambda j: (-j["total"], -j["ready"], j["id"]))
    out, per = [], defaultdict(int)
    for j in pool:
        if per[j["screen"]] < cap:
            out.append(j)
            per[j["screen"]] += 1
        if len(out) == n:
            break
    return out, len(pool)


def enabler_use(screens, enablers):
    use = defaultdict(list)
    for d in screens:
        for j in d["jobs"]:
            for en in j["enablers"]:
                use[en].append(j)
    rows = []
    for en, x in enablers.items():
        js = use.get(en, [])
        rows.append(dict(x, jobs=js, n=len(js), value=sum(j["total"] for j in js), now=sum(1 for j in js if j["start_now"]),
                         screens_used=sorted({j["screen"] for j in js})))
    rows.sort(key=lambda r: (-r["value"], r["id"]))
    return rows


def notes():
    t = open(os.path.join(HERE, "NOTES-KEVIN-29SEP.md"), encoding="utf-8").read()
    t = t.split("## What Kevin said")[0]
    return [l[2:].strip() for l in t.splitlines() if l.startswith("- ")]


def norm(s):
    return re.sub(r"[^a-z0-9 ]", " ", s.lower())


def note_map(enrows):
    """Each note to the enablers whose note field quotes it."""
    out = []
    for n in notes():
        key = norm(n)[:40].strip()
        hits = [r for r in enrows if r.get("note") and key and key in norm(r["note"])]
        out.append((n, hits))
    return out


def md(screens, enrows, top30, pool):
    L = ["# Jobs to be done, third list: tactical and executable", "",
         "Built by `app/jtbd/build_v3.py` from `app/jtbd/v3/*.json`. Brief: `BRIEF-v3.md`. Seed: `NOTES-KEVIN-29SEP.md`.",
         "Total = 4 x money + 2 x satisfaction + 2 x speed + 2 x ease, out of 50. Start now = inputs ready (4 or 5 of 5) and first output in hours or days.", "",
         f"## Start now: top {len(top30)} (from {pool} start-now jobs, at most 3 per screen)", ""]
    for i, j in enumerate(top30, 1):
        L.append(f"{i}. **{j['job']}** ({j['screen']}, {j['total']}, {j['effort']}). Enablers: {', '.join(j['enablers'])}.")
    L += ["", "## Enablers, by value of the jobs they power", "", "| Enabler | Jobs | Start now | Value | Screens |", "|---|---|---|---|---|"]
    for r in enrows:
        L.append(f"| {r['name']} (`{r['id']}`) | {r['n']} | {r['now']} | {r['value']} | {len(r['screens_used'])} |")
    for d in screens:
        L += ["", f"## {d['screen']} {d['title']}", ""]
        for t in d["top_jobs"]:
            L += [f"### {t['id']}. {t['job']}", "", f"Metric: {t['metric']}", ""]
            for j in sorted((j for j in d["jobs"] if j["top"] == t["id"]), key=lambda j: -j["total"]):
                flag = " Start now." if j["start_now"] else ""
                L.append(f"- **{j['id']} {j['job']}** Score {j['total']}, ready {j['ready']}/5, {j['effort']}.{flag}")
                L.append(f"  - When: {j['trigger']}. Enablers: {', '.join(j['enablers'])}.")
                L.append("  - Inputs: " + "; ".join(f"{i['need']} ({i['status']}, {i['from']})" for i in j["inputs"]) + ".")
                L.append("  - Steps: " + " ".join(f"{k}) {s}" for k, s in enumerate(j["steps"], 1)))
                L.append(f"  - Output: {j['output']}. Next: {j['next']}.")
                L.append(f"  - Watch: {j['watch']['metric']} ({j['watch'].get('window','')}, {j['watch'].get('source','')}), then {j['drives']}, then {j['business']}.")
    return "\n".join(L) + "\n"


def page(screens, enrows, top30, pool):
    e = html.escape
    N = sum(len(d["jobs"]) for d in screens)
    opts = "".join(f'<option value="{e(d["screen"])}">{e(d["screen"][:2])} {e(d["title"])}</option>' for d in screens)
    nav = f'<a href="#" data-s="">All screens<span class="num">{N}</span></a>' + "".join(
        f'<a href="#{e(d["screen"])}" data-s="{e(d["screen"])}">{e(d["screen"][:2])} {e(d["title"])}<span class="num">{len(d["jobs"])}</span></a>' for d in screens)
    en_name = {r["id"]: r["name"] for r in enrows}

    def chips_en(j):
        return "".join(f'<a class="en" href="#en-{e(x)}" data-en="{e(x)}">{e(en_name.get(x, x))}</a>' for x in j["enablers"])

    def chips_in(j):
        return "".join(f'<span class="in st-{e(i["status"])}" title="{e(STATUS_LABEL.get(i["status"], ""))}: {e(i.get("from",""))}">{e(i["need"])}</span>' for i in j["inputs"])

    def card(j):
        key = " ".join([j["job"], j["trigger"], j["output"], " ".join(j["steps"]), " ".join(i["need"] for i in j["inputs"]),
                        " ".join(j["enablers"]), j["watch"]["metric"], j["drives"]]).lower()
        sc = j["score"]
        now = '<i class="now">start now</i>' if j["start_now"] else ""
        steps = "".join(f"<li>{e(s)}</li>" for s in j["steps"])
        return (f'<div class="job" data-t="{e(key)}" data-now="{1 if j["start_now"] else 0}" id="j-{e(j["id"])}">'
                f'<div class="rk num">{e(j["id"])}{now}</div>'
                f'<div class="main"><div class="jt">{e(j["job"])}</div>'
                f'<div class="meta"><span><b>When</b> {e(j["trigger"])}</span><span><b>First output in</b> {e(j["effort"])}</span><span><b>Ready</b> {j["ready"]}/5</span></div>'
                f'<div class="row"><b>Enabled by</b>{chips_en(j)}</div>'
                f'<div class="row"><b>Needs</b>{chips_in(j)}</div>'
                f'<ol class="steps">{steps}</ol>'
                f'<div class="out"><b>You hold</b> {e(j["output"])}</div>'
                f'<div class="chain"><span class="w">{e(j["watch"]["metric"])}<small>{e(j["watch"].get("window",""))} · {e(j["watch"].get("source",""))}</small></span><span class="ar">then</span><span>{e(j["drives"])}</span><span class="ar">then</span><span class="b">{e(j["business"])}</span></div>'
                f'<div class="nx">Next: {e(j["next"])}</div></div>'
                f'<div class="sc"><div class="tot num">{j["total"]}</div><div class="bars" title="money {sc["money"]}, satisfaction {sc["satisfaction"]}, speed {sc["speed"]}, ease {sc["ease"]}">'
                + "".join(f'<i style="height:{4*sc[k]}px" class="{k}"></i>' for k in SCORES) + '</div></div></div>')

    body = ""
    for d in screens:
        groups = ""
        for t in d["top_jobs"]:
            js = sorted((j for j in d["jobs"] if j["top"] == t["id"]), key=lambda j: (-j["total"], j["id"]))
            groups += (f'<div class="tj"><div class="tjh"><span class="tid">{e(t["id"])}</span><div><div class="tjt">{e(t["job"])}</div>'
                       f'<div class="tjm">Top job metric: {e(t["metric"])}</div></div><span class="cnt num">{len(js)}</span></div>'
                       + "".join(card(j) for j in js) + "</div>")
        body += (f'<section class="scr" id="{e(d["screen"])}"><div class="sh"><div><div class="eyebrow">{e(d["screen"])}</div><h2>{e(d["title"])}</h2></div>'
                 f'<span class="cnt num">{len(d["top_jobs"])} top jobs · {len(d["jobs"])} tactical · {sum(1 for j in d["jobs"] if j["start_now"])} start now</span></div>{groups}</section>')

    rows = ""
    for i, j in enumerate(top30, 1):
        blockers = [i2 for i2 in j["inputs"] if i2["status"] in ("setup", "buy", "enabler", "founder")]
        bl = "".join('<span class="in st-%s">%s</span>' % (e(b["status"]), e(b["need"])) for b in blockers) or '<span class="sub">nothing</span>'
        rows += (f'<tr data-s="{e(j["screen"])}"><td class="num">{i}</td><td><a href="#j-{e(j["id"])}" class="jl" data-s="{e(j["screen"])}">{e(j["job"])}</a>'
                 f'<div class="sub">{e(j["output"])}</div></td><td>{e(j["screen"][:2])} {e(j["title"])}</td><td>{chips_en(j)}</td>'
                 f'<td>{bl}</td>'
                 f'<td class="num">{e(j["effort"])}</td><td class="num"><b>{j["total"]}</b></td></tr>')
    now_tbl = (f'<div class="intro"><h2>Start now: {len(top30)} jobs</h2><p>Picked from {pool} jobs whose inputs are ready on onboarding day (ready 4 or 5 of 5) and whose first output lands in hours or days. '
               f'Ranked by score, at most 3 per screen so one screen does not crowd the list. The "still needed" column shows what to set up or ask for first.</p></div>'
               f'<div class="tw"><table><thead><tr><th>#</th><th>Job</th><th>Screen</th><th>Enabled by</th><th>Still needed</th><th>Effort</th><th>Score</th></tr></thead><tbody>{rows}</tbody></table></div>')

    ens = ""
    for r in enrows:
        by_s = defaultdict(list)
        for j in r["jobs"]:
            by_s[j["screen"]].append(j)
        used = "".join(f'<div class="us"><b>{e(s[:2])}</b> ' + " ".join(f'<a href="#j-{e(j["id"])}" class="jl" data-s="{e(s)}" title="{e(j["job"])}">{e(j["id"])}</a>' for j in js) + "</div>" for s, js in sorted(by_s.items()))
        note = '<div class="note">From your note: "%s"</div>' % e(r["note"]) if r.get("note") else ""
        origin = "" if r.get("origin") == "shared" else f'<span class="new">added by {e(r["origin"])}</span>'
        ens += (f'<div class="enc" id="en-{e(r["id"])}" data-sc="{e(" ".join(r["screens_used"]))}" data-t="{e((r["name"]+" "+r.get("what","")+" "+(r.get("note") or "")).lower())}"><div class="ench"><div><div class="enn">{e(r["name"])} {origin}</div><div class="eyebrow">{e(r["id"])}</div></div>'
                f'<div class="ens"><span><b class="num">{r["n"]}</b> jobs</span><span><b class="num">{r["now"]}</b> start now</span><span><b class="num">{len(r["screens_used"])}</b> screens</span></div></div>'
                f'<p>{e(r.get("what",""))}</p>{note}'
                f'<div class="row"><b>Needs</b>' + "".join(f'<span class="in">{e(x)}</span>' for x in r.get("inputs", [])) + '</div>'
                f'<div class="row"><b>Powers</b>' + "".join(f'<span class="pw">{e(x)}</span>' for x in r.get("powers", [])) + '</div>'
                f'<details><summary>Jobs it powers</summary>{used or "<p class=sub>none yet</p>"}</details></div>')
    en_view = (f'<div class="intro"><h2>Enablers: build once, power many jobs</h2><p>An enabler is the engine behind a job, like the awareness heat map behind "publish more top of funnel ads". '
               f'Sorted by the total score of the jobs each one powers, so the top of this list is the best candidate to build first.</p></div>{ens}')

    nrows = ""
    cover = defaultdict(int)
    for r in enrows:
        cover[r["id"]] = r["n"]
    for n, hits in note_map(enrows):
        cells = " ".join(f'<a class="en" href="#en-{e(h["id"])}" data-en="{e(h["id"])}">{e(h["name"])}</a> <span class="sub num">{cover[h["id"]]} jobs</span>' for h in hits)
        nrows += f'<tr><td>{e(n)}</td><td>{cells or "<span class=sub>covered inside the enablers above it</span>"}</td></tr>'
    notes_view = (f'<div class="intro"><h2>Your notes, and where each one landed</h2><p>Every line from your notes, the enabler it became, and how many tactical jobs use it.</p></div>'
                  f'<div class="tw"><table><thead><tr><th>Your note</th><th>Enabler and jobs</th></tr></thead><tbody>{nrows}</tbody></table></div>')

    legend = "".join(f'<span><i class="in st-{k}"></i>{e(v)}</span>' for k, v in STATUS_LABEL.items())
    css = open(os.path.join(HERE, "v3", "page.css"), encoding="utf-8").read()
    js = open(os.path.join(HERE, "v3", "page.js"), encoding="utf-8").read().replace("__N__", str(N)).replace("__NS__", str(len(screens)))
    return f'''<title>Tactical Jobs List</title>
<style>{css}</style>
<div class="top"><div class="topin"><strong>Jobs to be done, third list</strong>
<button class="tab" data-v="now" aria-pressed="true">Start now</button><button class="tab" data-v="list" aria-pressed="false">By screen</button><button class="tab" data-v="en" aria-pressed="false">Enablers</button><button class="tab" data-v="notes" aria-pressed="false">Your notes</button>
<select id="screen" aria-label="Choose a screen"><option value="">All screens</option>{opts}</select>
<input id="q" type="search" placeholder="Filter: awareness, video, Clarity, Amazon, VIP" aria-label="Filter jobs">
<label class="ck"><input type="checkbox" id="onlynow"> start now only</label><span class="hits" id="hits"></span></div></div>
<div class="wrap">
  <nav class="nav" aria-label="Screens">{nav}</nav>
  <div>
    <div class="intro head"><div class="eyebrow">ecomOS · tactical layer · 29 Sep 2026</div><h1>What we do, what makes it possible, what it needs</h1>
    <p>Three levels. Each screen has 3 to 5 top jobs, the owner's progress from the second list. Under them sit {N} tactical jobs you can start this week, each with its steps. Every tactical job names the enabler behind it and the inputs it needs, coloured by how ready they are. Score is 4 x money + 2 x satisfaction + 2 x speed + 2 x ease, out of 50.</p>
    <div class="legend">{legend}</div></div>
    <div class="view on" id="v-now">{now_tbl}</div>
    <div class="view" id="v-list">{body}</div>
    <div class="view" id="v-en">{en_view}</div>
    <div class="view" id="v-notes">{notes_view}</div>
  </div>
</div>
<script>{js}</script>'''


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", default="")
    a = ap.parse_args()
    screens, enablers, problems = load()
    top30, pool = start_now(screens)
    enrows = enabler_use(screens, enablers)
    open(os.path.join(HERE, "JOBS-v3.md"), "w", encoding="utf-8").write(md(screens, enrows, top30, pool))
    if a.html:
        open(a.html, "w", encoding="utf-8").write(page(screens, enrows, top30, pool))
    for d in screens:
        print(f"{d['screen']}: {len(d['top_jobs'])} top, {len(d['jobs'])} jobs, {sum(1 for j in d['jobs'] if j['start_now'])} start now, new enablers {len(d.get('new_enablers') or [])}")
    unused = [r["id"] for r in enrows if r["n"] == 0]
    print(f"{len(screens)} screens, {sum(len(d['jobs']) for d in screens)} jobs, {pool} start now, {len(enrows)} enablers ({len(unused)} unused: {unused}), {len(problems)} problems")
    for p in problems[:80]:
        print("  ", p)
