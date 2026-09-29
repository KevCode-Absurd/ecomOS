"""Merge app/jtbd/<slug>.json into JOBS.md and a one-page HTML.

python3 app/jtbd/build.py [--html OUT.html]

Recomputes each job's total (4 money + 2 satisfaction + 2 speed + 2 ease, max 50),
sorts by total then by the drafter's rank, and reports anything that breaks the brief.
"""
import argparse
import glob
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
FIELDS = ("job", "why", "watch", "drives", "business", "now_after", "score", "who_today")
BUSINESS = {"revenue", "gross profit", "contribution margin", "cash", "customer satisfaction", "risk"}


def total(s):
    return 4 * s["money"] + 2 * s["satisfaction"] + 2 * s["speed"] + 2 * s["ease"]


def load():
    screens, problems = [], []
    for path in sorted(glob.glob(os.path.join(HERE, "*.json"))):
        d = json.load(open(path, encoding="utf-8"))
        jobs = []
        for j in d.get("jobs", []):
            missing = [f for f in FIELDS if f not in j]
            if missing:
                problems.append(f"{d['screen']} rank {j.get('rank')}: missing {missing}")
                continue
            if j["business"] not in BUSINESS:
                problems.append(f"{d['screen']} rank {j.get('rank')}: business '{j['business']}' not in the list")
            for k in ("money", "satisfaction", "speed", "ease"):
                v = j["score"].get(k)
                if not isinstance(v, int) or not 1 <= v <= 5:
                    problems.append(f"{d['screen']} rank {j.get('rank')}: score {k}={v}")
            text = " ".join(str(j.get(k, "")) for k in ("job", "why", "now_after"))
            if "—" in text or "–" in text:
                problems.append(f"{d['screen']} rank {j.get('rank')}: dash in text")
            j["total"] = total(j["score"])
            jobs.append(j)
        jobs.sort(key=lambda j: (-j["total"], j.get("rank", 99)))
        for i, j in enumerate(jobs, 1):
            j["rank"] = i
        d["jobs"] = jobs
        screens.append(d)
    return screens, problems


def md(screens):
    out = ["# Jobs to be done, per screen", "",
           "Ranked by 4 x money + 2 x satisfaction + 2 x speed + 2 x ease (max 50). Each job names the metric to watch, what it drives, and the business number at the top of the chain. Drafted 29 Sep 2026 from the room specs and the idea bank; the founder refines it.", ""]
    for s in screens:
        out += [f"## {s['screen']}: {s['title']}", "", f"Hired for: {s['hired_for']}", "",
                "| # | Job | Watch | Drives | Business | Score | Who today |", "|---|---|---|---|---|---|---|"]
        for j in s["jobs"]:
            w = j["watch"]
            out.append(f"| {j['rank']} | **{j['job']}** {j['why']} | {w['metric']} ({w.get('source','')}) | {j['drives']['metric']} | {j['business']} | {j['total']} | {j['who_today']} |")
        out.append("")
    return "\n".join(out)


def page(screens):
    e = html.escape
    nav = "".join(f'<a href="#{e(s["screen"])}">{e(s["screen"][:2])} {e(s["title"])}<span class="num">{len(s["jobs"])}</span></a>' for s in screens)
    body = ""
    for s in screens:
        rows = ""
        for j in s["jobs"]:
            w = j["watch"]; sc = j["score"]
            rows += (f'<div class="job" data-t="{e((j["job"] + " " + j["why"] + " " + w["metric"] + " " + j["drives"]["metric"]).lower())}">'
                     f'<div class="rk num">{j["rank"]}</div>'
                     f'<div class="main"><div class="jt">{e(j["job"])}</div><div class="why">{e(j["why"])}</div>'
                     f'<div class="chain"><span class="w">{e(w["metric"])}<small>{e(w.get("source",""))}</small></span><span class="ar">then</span><span>{e(j["drives"]["metric"])}</span><span class="ar">then</span><span class="b">{e(j["business"])}</span></div>'
                     f'<div class="na">{e(j["now_after"])}</div></div>'
                     f'<div class="sc"><div class="tot num">{j["total"]}</div><div class="bars" title="money {sc["money"]}, satisfaction {sc["satisfaction"]}, speed {sc["speed"]}, ease {sc["ease"]}">'
                     + "".join(f'<i style="height:{4*sc[k]}px" class="{k}"></i>' for k in ("money", "satisfaction", "speed", "ease"))
                     + f'</div><div class="who">{e(j["who_today"])}</div></div></div>')
        body += f'<section class="scr" id="{e(s["screen"])}"><div class="sh"><div><div class="eyebrow">{e(s["screen"])}</div><h2>{e(s["title"])}</h2><p class="hire">{e(s["hired_for"])}</p></div><span class="cnt num">{len(s["jobs"])} jobs</span></div>{rows}</section>'
    n = sum(len(s["jobs"]) for s in screens)
    return f'''<title>Jobs To Be Done</title>
<style>
:root{{--bg:#f4f5f8;--panel:#fff;--line:#d9dde6;--fg:#111827;--muted:#5b6474;--faint:#8b93a3;--accent:#1f4fd8;--soft:#e3e9fb;--m:#1f4fd8;--s:#2f8f9d;--sp:#5d8f3c;--e:#c98a1b;--r:6px}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#0f1420;--panel:#171d2b;--line:#2a3447;--fg:#e8ecf4;--muted:#a3adc0;--faint:#6f7a90;--accent:#6f95ff;--soft:#1f2b4d;--m:#6f95ff;--s:#5cc3d2;--sp:#8fc964;--e:#e6b04a;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0f1420;--panel:#171d2b;--line:#2a3447;--fg:#e8ecf4;--muted:#a3adc0;--faint:#6f7a90;--accent:#6f95ff;--soft:#1f2b4d;--m:#6f95ff;--s:#5cc3d2;--sp:#8fc964;--e:#e6b04a;color-scheme:dark}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}}
.num{{font-variant-numeric:tabular-nums}} .eyebrow{{font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);font-weight:600}}
h1{{font-size:24px;margin:0;line-height:1.15}} h2{{font-size:19px;margin:2px 0 0;line-height:1.2}}
.top{{position:sticky;top:env(safe-area-inset-top,0px);background:var(--bg);border-bottom:1px solid var(--line);z-index:4}}
.topin{{max-width:1240px;margin:0 auto;padding:10px 20px;display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center}}
.topin input{{flex:1 1 220px;min-width:160px;border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:var(--r);padding:7px 10px;font:inherit}}
.hits{{font-size:12px;color:var(--muted)}}
.wrap{{max-width:1240px;margin:0 auto;padding-inline:20px;padding-block:18px 70px;display:grid;grid-template-columns:230px minmax(0,1fr);gap:22px;align-items:start}}
.nav{{position:sticky;top:calc(env(safe-area-inset-top,0px) + 58px);max-height:calc(100vh - 80px);overflow:auto;display:flex;flex-direction:column;gap:1px}}
.nav a{{color:var(--muted);text-decoration:none;font-size:12.5px;padding:5px 8px;border-radius:var(--r);display:flex;justify-content:space-between;gap:6px}} .nav a:hover{{background:var(--panel);color:var(--fg)}} .nav a .num{{color:var(--faint);font-size:11px}}
.intro{{margin-bottom:8px}} .intro p{{margin:6px 0 0;color:var(--muted);max-width:76ch}}
.legend{{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:12px;color:var(--muted);margin:10px 0 4px}} .legend i{{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:5px;vertical-align:-1px}}
.scr{{margin-top:26px}} .sh{{display:flex;justify-content:space-between;align-items:end;gap:10px;border-bottom:2px solid var(--fg);padding-bottom:8px;margin-bottom:4px}} .hire{{margin:4px 0 0;color:var(--muted);max-width:80ch}} .cnt{{font-size:12px;color:var(--muted);white-space:nowrap}}
.job{{display:grid;grid-template-columns:34px minmax(0,1fr) 92px;gap:12px;padding:10px 0;border-bottom:1px solid var(--line)}}
.job.hide{{display:none}}
.rk{{font-size:13px;color:var(--faint);padding-top:2px}}
.jt{{font-weight:600;font-size:15px;line-height:1.3}} .why{{color:var(--muted);margin-top:2px}}
.chain{{display:flex;flex-wrap:wrap;gap:4px 8px;align-items:center;margin-top:6px;font-size:12.5px}} .chain span{{background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:2px 9px}} .chain .w{{border-color:var(--accent);background:var(--soft)}} .chain .w small{{color:var(--muted);margin-left:6px;font-size:11px}} .chain .ar{{border:0;background:none;color:var(--faint);padding:0;font-size:11px}} .chain .b{{font-weight:600}}
.na{{font-size:12.5px;color:var(--muted);margin-top:5px}}
.sc{{text-align:right}} .tot{{font-size:20px;font-weight:700;line-height:1}} .bars{{display:inline-flex;gap:3px;align-items:flex-end;height:22px;margin-top:4px}} .bars i{{display:block;width:8px;border-radius:2px 2px 0 0}} .bars .money{{background:var(--m)}} .bars .satisfaction{{background:var(--s)}} .bars .speed{{background:var(--sp)}} .bars .ease{{background:var(--e)}}
.who{{font-size:11px;color:var(--faint);margin-top:4px}}
@media (max-width:820px){{.wrap{{grid-template-columns:1fr;padding-inline:16px}} .nav{{display:none}} .job{{grid-template-columns:28px minmax(0,1fr)}} .sc{{grid-column:2;text-align:left;display:flex;gap:10px;align-items:center}} .bars{{margin:0}}}}
</style>
<div class="top"><div class="topin"><strong>Jobs to be done</strong><input id="q" type="search" placeholder="Filter jobs by a word: bounce, margin, stockout, claim" aria-label="Filter jobs"><span class="hits" id="hits">{n} jobs across {len(screens)} screens</span></div></div>
<div class="wrap">
  <nav class="nav" aria-label="Screens">{nav}</nav>
  <div>
    <div class="intro"><div class="eyebrow">ecomOS</div><h1>Why an owner hires each screen</h1>
    <p>One list per screen, ranked. Each job says what the owner wants done, the metric to watch first, what it drives, and the business number at the top. Score is 4 x money + 2 x satisfaction + 2 x speed + 2 x ease, out of 50. Example numbers in the now and after lines are illustrations, not data.</p>
    <div class="legend"><span><i style="background:var(--m)"></i>money</span><span><i style="background:var(--s)"></i>satisfaction</span><span><i style="background:var(--sp)"></i>speed to see it move</span><span><i style="background:var(--e)"></i>ease to act</span></div></div>
    {body}
  </div>
</div>
<script>
const q=document.getElementById('q'),jobs=[...document.querySelectorAll('.job')],hits=document.getElementById('hits'),N={n};
q.addEventListener('input',()=>{{const v=q.value.trim().toLowerCase();let k=0;jobs.forEach(j=>{{const on=!v||j.dataset.t.includes(v);j.classList.toggle('hide',!on);if(on)k++;}});document.querySelectorAll('.scr').forEach(s=>{{s.style.display=s.querySelectorAll('.job:not(.hide)').length?'':'none';}});hits.textContent=v?k+' of '+N+' jobs match':N+' jobs across {len(screens)} screens';}});
</script>'''


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", default="")
    a = ap.parse_args()
    screens, problems = load()
    open(os.path.join(HERE, "JOBS.md"), "w", encoding="utf-8").write(md(screens))
    if a.html:
        open(a.html, "w", encoding="utf-8").write(page(screens))
    for s in screens:
        print(f"{s['screen']}: {len(s['jobs'])} jobs, top: {s['jobs'][0]['job'] if s['jobs'] else '-'}")
    print(f"{len(screens)} screens, {sum(len(s['jobs']) for s in screens)} jobs, {len(problems)} problems")
    for p in problems[:40]:
        print("  ", p)
