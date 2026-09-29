"""Merge app/jtbd/v2/<slug>.json into JOBS-v2.md and a one-page HTML with a side-by-side view.

python3 app/jtbd/build_v2.py [--html OUT.html]

Total = 3 money + 3 struggle + 2 satisfaction + 1 speed + 1 ease (max 50).
Ties: a job whose hire_today is "nothing" ranks above one with the same total.
"""
import argparse
import glob
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.join(HERE, "v2")
FIELDS = ("job", "circumstance", "progress", "hire_today", "fire", "forces", "little_hire", "watch", "drives", "business", "now_after", "score", "not_for")
BUSINESS = {"revenue", "gross profit", "contribution margin", "cash", "customer satisfaction", "risk"}


def total(s):
    return 3 * s["money"] + 3 * s["struggle"] + 2 * s["satisfaction"] + s["speed"] + s["ease"]


def load():
    screens, problems = [], []
    for path in sorted(glob.glob(os.path.join(V2, "*.json"))):
        d = json.load(open(path, encoding="utf-8"))
        jobs = []
        for j in d.get("jobs", []):
            missing = [f for f in FIELDS if f not in j]
            if missing:
                problems.append(f"{d['screen']} rank {j.get('rank')}: missing {missing}")
                continue
            if j["business"] not in BUSINESS:
                problems.append(f"{d['screen']} rank {j.get('rank')}: business '{j['business']}'")
            for k in ("money", "struggle", "satisfaction", "speed", "ease"):
                v = j["score"].get(k)
                if not isinstance(v, int) or not 1 <= v <= 5:
                    problems.append(f"{d['screen']} rank {j.get('rank')}: score {k}={v}")
            for k in ("push", "pull", "habit", "anxiety"):
                if k not in j["forces"]:
                    problems.append(f"{d['screen']} rank {j.get('rank')}: forces missing {k}")
            for k in ("functional", "emotional", "social"):
                if k not in j["progress"]:
                    problems.append(f"{d['screen']} rank {j.get('rank')}: progress missing {k}")
            text = " ".join(str(j.get(k, "")) for k in ("job", "circumstance", "now_after"))
            if "—" in text or "–" in text:
                problems.append(f"{d['screen']} rank {j.get('rank')}: dash in text")
            if not j["job"].lower().startswith("when"):
                problems.append(f"{d['screen']} rank {j.get('rank')}: job does not start with When")
            j["total"] = total(j["score"])
            j["nonconsumption"] = str(j["hire_today"]).strip().lower().startswith("nothing")
            jobs.append(j)
        jobs.sort(key=lambda j: (-j["total"], not j["nonconsumption"], j.get("rank", 99)))
        for i, j in enumerate(jobs, 1):
            j["rank"] = i
        d["jobs"] = jobs
        for k in ("purpose", "fires", "not_for"):
            if not d.get(k):
                problems.append(f"{d['screen']}: missing screen-level {k}")
        screens.append(d)
    return screens, problems


def load_v1():
    out = {}
    for path in sorted(glob.glob(os.path.join(HERE, "*.json"))):
        d = json.load(open(path, encoding="utf-8"))
        out[d["screen"]] = d
    return out


def md(screens):
    out = ["# Jobs to be done, second list", "",
           "Written as progress in a circumstance, after Competing Against Luck. Ranked by 3 x money + 3 x struggle + 2 x satisfaction + speed + ease (max 50); nonconsumption breaks ties upward. Drafted 29 Sep 2026.", ""]
    for s in screens:
        out += [f"## {s['screen']}: {s['title']}", "", f"Purpose: {s.get('purpose','')}", "", f"Fires: {s.get('fires','')}", "", f"Not for: {s.get('not_for','')}", "",
                "| # | Job | Hire today | Fire | Anxiety | Watch | Business | Score |", "|---|---|---|---|---|---|---|---|"]
        for j in s["jobs"]:
            out.append(f"| {j['rank']} | {j['job']} | {j['hire_today']} | {j['fire']} | {j['forces'].get('anxiety','')} | {j['watch']['metric']} | {j['business']} | {j['total']} |")
        out.append("")
    return "\n".join(out)


def page(screens, v1):
    e = html.escape
    nav = '<a href="#" data-s="">All screens<span class="num">' + str(sum(len(s["jobs"]) for s in screens)) + '</span></a>' + "".join(
        f'<a href="#{e(s["screen"])}" data-s="{e(s["screen"])}">{e(s["screen"][:2])} {e(s["title"])}<span class="num">{len(s["jobs"])}</span></a>' for s in screens)
    opts = "".join(f'<option value="{e(s["screen"])}">{e(s["screen"][:2])} {e(s["title"])}</option>' for s in screens)
    body = ""
    for s in screens:
        rows = ""
        for j in s["jobs"]:
            w = j["watch"]; sc = j["score"]; p = j["progress"]; f = j["forces"]
            key = " ".join([j["job"], j["circumstance"], j["hire_today"], j["fire"], w["metric"], j["drives"]["metric"], f.get("anxiety", ""), p.get("emotional", "")]).lower()
            badge = '<i title="nobody does this today">new</i>' if j["nonconsumption"] else ""
            rows += (f'<div class="job" data-t="{e(key)}">'
                     f'<div class="rk num">{j["rank"]}{badge}</div>'
                     f'<div class="main"><div class="jt">{e(j["job"])}</div>'
                     f'<div class="cs"><b>Moment</b> {e(j["circumstance"])}</div>'
                     f'<div class="prog"><span><b>Do</b> {e(p.get("functional",""))}</span><span><b>Feel</b> {e(p.get("emotional",""))}</span><span><b>Look</b> {e(p.get("social",""))}</span></div>'
                     f'<div class="hf"><span class="hire"><b>Hires today</b> {e(j["hire_today"])}</span><span class="fire"><b>Must fire</b> {e(j["fire"])}</span><span><b>Comes back</b> {e(j["little_hire"])}</span></div>'
                     f'<div class="forces"><span><b>Push</b> {e(f.get("push",""))}</span><span><b>Pull</b> {e(f.get("pull",""))}</span><span><b>Habit</b> {e(f.get("habit",""))}</span><span class="anx"><b>Anxiety</b> {e(f.get("anxiety",""))}</span></div>'
                     f'<div class="chain"><span class="w">{e(w["metric"])}<small>{e(w.get("source",""))}</small></span><span class="ar">then</span><span>{e(j["drives"]["metric"])}</span><span class="ar">then</span><span class="b">{e(j["business"])}</span></div>'
                     f'<div class="na">{e(j["now_after"])}</div><div class="nf">Not for: {e(j["not_for"])}</div></div>'
                     f'<div class="sc"><div class="tot num">{j["total"]}</div><div class="bars" title="money {sc["money"]}, struggle {sc["struggle"]}, satisfaction {sc["satisfaction"]}, speed {sc["speed"]}, ease {sc["ease"]}">'
                     + "".join(f'<i style="height:{4*sc[k]}px" class="{k}"></i>' for k in ("money", "struggle", "satisfaction", "speed", "ease"))
                     + '</div></div></div>')
        body += (f'<section class="scr" id="{e(s["screen"])}"><div class="sh"><div><div class="eyebrow">{e(s["screen"])}</div><h2>{e(s["title"])}</h2>'
                 f'<p class="hire"><b>Purpose.</b> {e(s.get("purpose",""))}</p><p class="hire"><b>Fires.</b> {e(s.get("fires",""))}</p><p class="hire"><b>Not for.</b> {e(s.get("not_for",""))}</p></div>'
                 f'<span class="cnt num">{len(s["jobs"])} jobs</span></div>{rows}</section>')
    # side by side: top 10 of each list per screen
    cmp = ""
    for s in screens:
        a = v1.get(s["screen"], {}).get("jobs", [])[:10]
        b = s["jobs"][:10]
        rows = ""
        for i in range(10):
            l = a[i] if i < len(a) else None
            r = b[i] if i < len(b) else None
            rows += (f'<tr><td class="num">{i+1}</td><td>{e(l["job"]) if l else ""}<div class="sub">{e(l["watch"]["metric"]) if l else ""}</div></td>'
                     f'<td>{e(r["job"]) if r else ""}<div class="sub">{e(r["watch"]["metric"]) if r else ""}</div></td></tr>')
        cmp += f'<section class="scr cmp" id="cmp-{e(s["screen"])}"><div class="sh"><div><div class="eyebrow">{e(s["screen"])}</div><h2>{e(s["title"])}</h2></div></div><div class="tw"><table><thead><tr><th>#</th><th>First list: what the owner wants done</th><th>Second list: the moment and the progress</th></tr></thead><tbody>{rows}</tbody></table></section>'
    n = sum(len(s["jobs"]) for s in screens)
    return f'''<title>Jobs To Be Done, Second List</title>
<style>
:root{{--bg:#f4f5f8;--panel:#fff;--line:#d9dde6;--fg:#111827;--muted:#5b6474;--faint:#8b93a3;--accent:#1f4fd8;--soft:#e3e9fb;--m:#1f4fd8;--st:#c2410c;--s:#2f8f9d;--sp:#5d8f3c;--e:#c98a1b;--r:6px}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#0f1420;--panel:#171d2b;--line:#2a3447;--fg:#e8ecf4;--muted:#a3adc0;--faint:#6f7a90;--accent:#6f95ff;--soft:#1f2b4d;--m:#6f95ff;--st:#f0834f;--s:#5cc3d2;--sp:#8fc964;--e:#e6b04a;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0f1420;--panel:#171d2b;--line:#2a3447;--fg:#e8ecf4;--muted:#a3adc0;--faint:#6f7a90;--accent:#6f95ff;--soft:#1f2b4d;--m:#6f95ff;--st:#f0834f;--s:#5cc3d2;--sp:#8fc964;--e:#e6b04a;color-scheme:dark}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}}
.num{{font-variant-numeric:tabular-nums}} .eyebrow{{font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);font-weight:600}}
h1{{font-size:24px;margin:0;line-height:1.15}} h2{{font-size:19px;margin:2px 0 0;line-height:1.2}}
.top{{position:sticky;top:env(safe-area-inset-top,0px);background:var(--bg);border-bottom:1px solid var(--line);z-index:4}}
.topin{{max-width:1280px;margin:0 auto;padding:10px 20px;display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center}}
.topin select,.topin input{{border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:var(--r);padding:7px 10px;font:inherit;max-width:100%}}
.topin input{{flex:1 1 220px;min-width:160px}}
.tab{{border:1px solid var(--line);background:var(--panel);border-radius:999px;padding:6px 12px;font:inherit;font-size:13px;color:var(--muted);cursor:pointer}} .tab[aria-pressed="true"]{{background:var(--accent);border-color:var(--accent);color:#fff}}
.hits{{font-size:12px;color:var(--muted)}}
.wrap{{max-width:1280px;margin:0 auto;padding-inline:20px;padding-block:18px 70px;display:grid;grid-template-columns:230px minmax(0,1fr);gap:22px;align-items:start}}
.nav{{position:sticky;top:calc(env(safe-area-inset-top,0px) + 58px);max-height:calc(100vh - 80px);overflow:auto;display:flex;flex-direction:column;gap:1px}}
.nav a{{color:var(--muted);text-decoration:none;font-size:12.5px;padding:5px 8px;border-radius:var(--r);display:flex;justify-content:space-between;gap:6px}} .nav a:hover{{background:var(--panel);color:var(--fg)}} .nav a.on{{background:var(--soft);color:var(--fg);font-weight:600}} .nav a .num{{color:var(--faint);font-size:11px}}
.intro p{{margin:6px 0 0;color:var(--muted);max-width:78ch}}
.legend{{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:12px;color:var(--muted);margin:10px 0 4px}} .legend i{{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:5px;vertical-align:-1px}}
.scr{{margin-top:26px}} .sh{{display:flex;justify-content:space-between;align-items:end;gap:10px;border-bottom:2px solid var(--fg);padding-bottom:8px;margin-bottom:4px}} .hire{{margin:4px 0 0;color:var(--muted);max-width:90ch;font-size:13px}} .hire b{{color:var(--fg)}} .cnt{{font-size:12px;color:var(--muted);white-space:nowrap}}
.job{{display:grid;grid-template-columns:40px minmax(0,1fr) 92px;gap:12px;padding:12px 0;border-bottom:1px solid var(--line)}} .job.hide{{display:none}}
.rk{{font-size:13px;color:var(--faint);padding-top:2px}} .rk i{{display:block;font-style:normal;font-size:9px;letter-spacing:.06em;text-transform:uppercase;color:var(--st);font-weight:700;margin-top:3px}}
.jt{{font-weight:600;font-size:15px;line-height:1.35}}
.cs{{margin-top:4px;font-size:13px;color:var(--muted)}} .cs b,.prog b,.hf b,.forces b{{color:var(--fg);font-weight:600;margin-right:4px;font-size:11px;letter-spacing:.04em;text-transform:uppercase}}
.prog,.hf,.forces{{display:flex;flex-wrap:wrap;gap:3px 16px;margin-top:5px;font-size:12.5px;color:var(--muted)}} .prog span,.hf span,.forces span{{flex:1 1 220px;min-width:0}}
.hf .hire{{margin:0}} .hf .fire b{{color:var(--st)}} .forces .anx b{{color:var(--st)}}
.chain{{display:flex;flex-wrap:wrap;gap:4px 8px;align-items:center;margin-top:7px;font-size:12.5px}} .chain span{{background:var(--panel);border:1px solid var(--line);border-radius:999px;padding:2px 9px}} .chain .w{{border-color:var(--accent);background:var(--soft)}} .chain .w small{{color:var(--muted);margin-left:6px;font-size:11px}} .chain .ar{{border:0;background:none;color:var(--faint);padding:0;font-size:11px}} .chain .b{{font-weight:600}}
.na{{font-size:12.5px;color:var(--muted);margin-top:5px}} .nf{{font-size:12px;color:var(--faint);margin-top:3px}}
.sc{{text-align:right}} .tot{{font-size:20px;font-weight:700;line-height:1}} .bars{{display:inline-flex;gap:3px;align-items:flex-end;height:22px;margin-top:4px}} .bars i{{display:block;width:8px;border-radius:2px 2px 0 0}} .bars .money{{background:var(--m)}} .bars .struggle{{background:var(--st)}} .bars .satisfaction{{background:var(--s)}} .bars .speed{{background:var(--sp)}} .bars .ease{{background:var(--e)}}
.view{{display:none}} .view.on{{display:block}}
.tw{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-size:13px}} th,td{{text-align:left;padding:8px 8px;border-bottom:1px solid var(--line);vertical-align:top}} th{{font-size:11px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}} td .sub{{font-size:11.5px;color:var(--faint);margin-top:2px}}
@media (max-width:820px){{.wrap{{grid-template-columns:1fr;padding-inline:16px}} .nav{{display:none}} .job{{grid-template-columns:32px minmax(0,1fr)}} .sc{{grid-column:2;text-align:left;display:flex;gap:10px;align-items:center}} .bars{{margin:0}}}}
</style>
<div class="top"><div class="topin"><strong>Jobs to be done, second list</strong><select id="screen" aria-label="Choose a screen"><option value="">All screens</option>{opts}</select><input id="q" type="search" placeholder="Filter by a word: Monday, launch, stockout, agency, nothing" aria-label="Filter jobs"><button class="tab" id="t-list" aria-pressed="true">Full list</button><button class="tab" id="t-cmp" aria-pressed="false">Side by side, top 10</button><span class="hits" id="hits">{n} jobs across {len(screens)} screens</span></div></div>
<div class="wrap">
  <nav class="nav" aria-label="Screens">{nav}</nav>
  <div>
    <div class="intro"><div class="eyebrow">ecomOS · after Competing Against Luck</div><h1>The moment, the progress, and what gets fired</h1>
    <p>Each job is written from inside a moment: when this happens, help me make this progress, so I can get this outcome. It names what the owner hires today, what has to be fired, the four forces at the moment of choice, the metric that shows the progress, and who should not hire it. Score is 3 x money + 3 x struggle + 2 x satisfaction + speed + ease, out of 50. "New" marks a job nobody does today. Example numbers are illustrations.</p>
    <div class="legend"><span><i style="background:var(--m)"></i>money</span><span><i style="background:var(--st)"></i>struggle today</span><span><i style="background:var(--s)"></i>satisfaction</span><span><i style="background:var(--sp)"></i>speed to see it</span><span><i style="background:var(--e)"></i>ease to act</span></div></div>
    <div class="view on" id="v-list">{body}</div>
    <div class="view" id="v-cmp">{cmp}</div>
  </div>
</div>
<script>
const q=document.getElementById('q'),sel=document.getElementById('screen'),hits=document.getElementById('hits'),N={n},NS={len(screens)};
let view='list';
function apply(){{
  const v=q.value.trim().toLowerCase(), s=sel.value; let k=0;
  document.querySelectorAll('#v-list .scr').forEach(sec=>{{ const inS=!s||sec.id===s; let kk=0; sec.querySelectorAll('.job').forEach(j=>{{const on=inS&&(!v||j.dataset.t.includes(v)); j.classList.toggle('hide',!on); if(on)kk++;}}); sec.style.display=kk?'':'none'; k+=kk; }});
  document.querySelectorAll('#v-cmp .scr').forEach(sec=>{{ sec.style.display=(!s||sec.id==='cmp-'+s)?'':'none'; }});
  document.querySelectorAll('.nav a').forEach(a=>a.classList.toggle('on',a.dataset.s===s));
  hits.textContent=(s?sel.options[sel.selectedIndex].text+': ':'')+(v?k+' jobs match "'+v+'"':k+' jobs'+(s?'':' across '+NS+' screens'));
  try{{localStorage.setItem('jtbd2-screen',s);}}catch(e){{}}
}}
function setView(x){{ view=x; document.getElementById('v-list').classList.toggle('on',x==='list'); document.getElementById('v-cmp').classList.toggle('on',x==='cmp'); document.getElementById('t-list').setAttribute('aria-pressed',x==='list'?'true':'false'); document.getElementById('t-cmp').setAttribute('aria-pressed',x==='cmp'?'true':'false'); }}
document.getElementById('t-list').addEventListener('click',()=>setView('list')); document.getElementById('t-cmp').addEventListener('click',()=>setView('cmp'));
q.addEventListener('input',apply); sel.addEventListener('change',()=>{{apply(); window.scrollTo({{top:0}});}});
document.querySelectorAll('.nav a').forEach(a=>a.addEventListener('click',ev=>{{ev.preventDefault(); sel.value=a.dataset.s; apply(); window.scrollTo({{top:0}});}}));
(function(){{ let s=''; try{{s=localStorage.getItem('jtbd2-screen')||'';}}catch(e){{}} const h=(location.hash||'').slice(1); if(h&&[...sel.options].some(o=>o.value===h)) s=h; if([...sel.options].some(o=>o.value===s)) sel.value=s; apply(); }})();
</script>'''


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", default="")
    a = ap.parse_args()
    screens, problems = load()
    open(os.path.join(HERE, "JOBS-v2.md"), "w", encoding="utf-8").write(md(screens))
    if a.html:
        open(a.html, "w", encoding="utf-8").write(page(screens, load_v1()))
    for s in screens:
        nc = sum(1 for j in s["jobs"] if j["nonconsumption"])
        print(f"{s['screen']}: {len(s['jobs'])} jobs, {nc} nonconsumption, top: {s['jobs'][0]['job'][:90] if s['jobs'] else '-'}")
    print(f"{len(screens)} screens, {sum(len(s['jobs']) for s in screens)} jobs, {len(problems)} problems")
    for p in problems[:60]:
        print("  ", p)
