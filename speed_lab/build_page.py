"""Build the Gehna speed lab page: baseline, two arms, a Fix it walkthrough per arm, verdict.

Usage: python3 speed_lab/build_page.py [--out reviews/speed-lab/gehna-speed-lab.html]
Reads speed_lab/results/*.json, speed_lab/arms/*/limiters.json and results/*-run1.png.
"""
import argparse, base64, io, json, os, re
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(ROOT, "results")

ARMS = {
    "arm-a": {"name": "Arm A", "sub": "general knowledge, harness and web", "chain": ["arm-a-f01", "arm-a-f02", "arm-a-f03", "arm-a-f04", "arm-a-f05", "arm-a-f06", "arm-a-f08", "arm-a-f09"], "tried": {"arm-a-f07": "Defer the email-decode script. Nothing measurable, reverted."},
              "labels": {"arm-a-f01": "Turn Rocket Loader off", "arm-a-f02": "Nanum fonts as Latin WOFF2 subsets", "arm-a-f03": "Tags load after the page (lazyOnload)", "arm-a-f04": "Category icons 640 to 256 px", "arm-a-f05": "Lato fonts as Latin WOFF2", "arm-a-f06": "Preload the hero image", "arm-a-f08": "Inline both stylesheets", "arm-a-f09": "Remove the dead Universal Analytics tag"}},
    "arm-b": {"name": "Arm B", "sub": "same, plus the idea bank and card library", "chain": ["arm-b-f01", "arm-b-f02", "arm-b-f03", "arm-b-f04", "arm-b-f05", "arm-b-f06", "arm-b-f07", "arm-b-f08"], "tried": {},
              "labels": {"arm-b-f01": "Nanum fonts as Latin WOFF2 subsets", "arm-b-f02": "Turn Rocket Loader off", "arm-b-f03": "7 tags load after the page (lazyOnload)", "arm-b-f04": "Category icons 640 to 256 px", "arm-b-f05": "Preload the hero image, drop Nanum preloads", "arm-b-f06": "Lato fonts as WOFF2", "arm-b-f07": "Remove the dead Universal Analytics tag", "arm-b-f08": "Email-decode script made non-blocking"}},
}


def load(label):
    p = os.path.join(RES, label + ".json")
    return json.load(open(p)) if os.path.exists(p) else None


def med(d):
    m = d["median"]
    return {"lcp": m["lcp_ms"], "fcp": m["fcp_ms"], "dcl": m["dcl_ms"], "load": m["load_ms"], "tbt": m["tbt_est_ms"], "bytes": m["wire_bytes"], "fp": m["first_party_bytes"], "tp": m["third_party_bytes"], "req": m["requests_served"]}


def shot(label, width=330):
    p = os.path.join(RES, label + "-run1.png")
    if not os.path.exists(p): return None
    im = Image.open(p).convert("RGB")
    h = int(im.height * width / im.width)
    im = im.resize((width, h), Image.LANCZOS).crop((0, 0, width, min(h, 700)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=68, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def fidelity(label):
    import subprocess
    r = subprocess.run(["python3", os.path.join(ROOT, "check_fidelity.py"), os.path.join(RES, label + ".json")], capture_output=True, text=True)
    return r.stdout.strip().splitlines()[0] if r.stdout.strip() else "unknown"


def esc(s): return str(s).replace("&", "&amp;").replace("<", "&lt;")


def main(out):
    base = load("baseline")
    data = {"baseline": {"m": med(base), "shot": shot("baseline"), "fid": "PASS"}, "arms": {}}
    for k, a in ARMS.items():
        steps = []
        for v in a["chain"]:
            d = load(v)
            if not d: continue
            steps.append({"id": v, "label": a["labels"].get(v, v), "m": med(d), "shot": shot(v), "fid": fidelity(v)})
        lim = json.load(open(os.path.join(ROOT, "arms", k, "limiters.json")))
        data["arms"][k] = {"name": a["name"], "sub": a["sub"], "steps": steps, "tried": a["tried"], "limiters": lim}
    b = data["baseline"]["m"]
    font_kb = base["by_type_run1"].get("font", [0, 0])[1]
    font_txt = f"{font_kb/1048576:.1f} MB"
    fa = data["arms"]["arm-a"]["steps"][-1]["m"]; fb = data["arms"]["arm-b"]["steps"][-1]["m"]

    def lim_rows(lim):
        return "".join(f"<tr><td>{l['rank']}</td><td>{esc(l['title'])}</td><td>{esc(l['fix'])[:160]}</td><td>{esc(l.get('effort',''))}</td><td class='src'>{esc(l.get('source',''))}</td></tr>" for l in lim)

    def kpi(label, val, sub, cls=""):
        return f'<div class="kpi"><div class="l">{label}</div><div class="v {cls}">{val}</div><div class="s">{sub}</div></div>'

    def ms(x): return "unavailable" if x is None else (f"{x/1000:.1f} s" if x >= 1000 else f"{x:.0f} ms")
    def mb(x): return f"{x/1024/1024:.2f} MB"

    page = f'''<title>Gehna Speed Lab</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{--bg:#F5F4EF;--panel:#FFFFFF;--ink:#1E1C19;--muted:#6B665D;--line:#DAD6CC;--accent:#8E6A1C;--accent-ink:#FFFFFF;--r1:#2E5E6E;--r2:#7A3E5C;--good:#2F6B3A;--warn:#9A5A0A;--bad:#A03A2E;--code:#EFECE4;
--display:'Sora',system-ui,sans-serif;--body:'Source Sans 3',system-ui,sans-serif;--mono:'IBM Plex Mono',ui-monospace,monospace}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#17161A;--panel:#211F24;--ink:#EDEAE3;--muted:#A49E92;--line:#3A373F;--accent:#D8AE52;--accent-ink:#1E1C19;--r1:#7FB7C8;--r2:#D28BB0;--good:#7CC48A;--warn:#E0A552;--bad:#E07A6E;--code:#2B2930;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#17161A;--panel:#211F24;--ink:#EDEAE3;--muted:#A49E92;--line:#3A373F;--accent:#D8AE52;--accent-ink:#1E1C19;--r1:#7FB7C8;--r2:#D28BB0;--good:#7CC48A;--warn:#E0A552;--bad:#E07A6E;--code:#2B2930;color-scheme:dark}}
body{{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.5;padding-inline:16px;padding-block:0 56px}}
main{{max-width:1400px;margin:0 auto}}
h1{{font-family:var(--display);font-size:clamp(26px,3.6vw,38px);font-weight:700;letter-spacing:-.015em;margin:28px 0 6px;text-wrap:balance}}
h2{{font-family:var(--display);font-size:22px;margin:38px 0 10px;text-wrap:balance}}
h3{{font-family:var(--display);font-size:16px;margin:0 0 6px}}
p{{max-width:76ch;margin:0 0 10px}} .muted{{color:var(--muted)}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:14px 0}}
.kpi{{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:10px 12px}}
.kpi .l{{font:600 11px var(--display);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
.kpi .v{{font:500 22px var(--mono);font-variant-numeric:tabular-nums;margin-top:2px;white-space:nowrap}}
.kpi .v.bad{{color:var(--bad)}} .kpi .v.good{{color:var(--good)}} .kpi .v.warn{{color:var(--warn)}}
.kpi .s{{font-size:12px;color:var(--muted)}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:18px;align-items:start}}
@media (max-width:980px){{.cols{{grid-template-columns:1fr}}}}
.arm{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px 18px;min-width:0}}
.arm .tag{{display:inline-block;font:600 12px var(--display);letter-spacing:.05em;text-transform:uppercase;padding:4px 10px;border-radius:999px;color:#fff}}
.arm.a .tag{{background:var(--r1)}} .arm.b .tag{{background:var(--r2)}}
.arm .sub{{color:var(--muted);font-size:14px;margin:6px 0 12px}}
.metrics{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:10px 0 12px}}
@media (max-width:520px){{.metrics{{grid-template-columns:repeat(2,1fr)}}}}
.met{{border:1px solid var(--line);border-radius:6px;padding:8px 10px;background:var(--bg)}}
.met .l{{font:600 10.5px var(--display);letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
.met .v{{font:500 19px var(--mono);font-variant-numeric:tabular-nums}}
.met .d{{font:12px var(--mono);color:var(--muted)}} .met .d.good{{color:var(--good)}} .met .d.bad{{color:var(--bad)}}
.bar{{height:8px;background:var(--code);border-radius:4px;overflow:hidden;margin-top:6px}}
.bar i{{display:block;height:100%;background:var(--accent);border-radius:4px;transition:width .35s ease}}
.fixes{{list-style:none;padding:0;margin:0;display:grid;gap:6px}}
.fixes li{{display:grid;grid-template-columns:28px 1fr auto;gap:10px;align-items:center;border:1px solid var(--line);border-radius:6px;padding:8px 10px;background:var(--panel)}}
.fixes li .n{{font:600 13px var(--display);color:var(--muted)}}
.fixes li.on{{border-color:var(--accent);background:var(--code)}}
.fixes li.on .n{{color:var(--accent)}}
.fixes li .t{{font-size:14px}} .fixes li .fid{{font:11px var(--mono);color:var(--muted)}}
.fixes button{{font:600 12px var(--display);padding:6px 10px;border-radius:999px;border:1px solid var(--accent);background:var(--panel);color:var(--accent);cursor:pointer}}
.fixes button:disabled{{opacity:.45;cursor:default}}
.fixes li.on button{{background:var(--accent);color:var(--accent-ink)}}
.ctl{{display:flex;gap:8px;margin:10px 0 4px;flex-wrap:wrap}}
.ctl button{{font:600 13px var(--display);padding:7px 12px;border-radius:999px;border:1px solid var(--line);background:var(--panel);color:var(--ink);cursor:pointer}}
.ctl button.primary{{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}}
.shots{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}}
.shots figure{{margin:0;min-width:0}} .shots img{{width:100%;border:1px solid var(--line);border-radius:6px;display:block}}
.shots figcaption{{font-size:12px;color:var(--muted);margin-top:4px}}
details{{margin-top:12px}} summary{{cursor:pointer;font:600 14px var(--display)}}
.tbl{{overflow-x:auto}} table{{border-collapse:collapse;font-size:13px;min-width:640px;font-variant-numeric:tabular-nums}}
th,td{{border:1px solid var(--line);padding:5px 8px;text-align:left;vertical-align:top}} th{{background:var(--code);font-family:var(--display);font-size:12px}}
td.src{{font-family:var(--mono);font-size:11.5px}}
.verdict{{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:8px;padding:14px 18px;max-width:80ch}}
.note{{font-size:13px;color:var(--muted);max-width:80ch}}
button:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
@media (prefers-reduced-motion: reduce){{.bar i{{transition:none}}}}
</style>
<main>
<h1>Gehna homepage speed lab: two agents, one mirror, fix by fix</h1>
<p class="muted">The live homepage was mirrored offline with all 199 responses it loads, first and third party. Two agents audited the same mirror, ranked the top 10 limiters, then applied fixes one at a time to their own copy. Every step was measured 3 times on a throttled phone profile (slow 4G, 1.6 Mbps, 150 ms RTT, 4x CPU slowdown, cold cache) and checked to be the same page. Press Fix it to walk through each agent's sequence and watch the numbers move.</p>
<div class="kpis">
{kpi("Baseline load", ms(b["load"]), "until the load event", "bad")}{kpi("Baseline LCP", ms(b["lcp"]), "hero image painted", "warn")}{kpi("Baseline wire bytes", mb(b["bytes"]), f"{b['req']:.0f} requests", "bad")}{kpi("Fonts on the wire", font_txt, "4 TTF files, 2 are full Korean sets", "bad")}{kpi("Blocking time", ms(b["tbt"]), "mostly React hydration", "warn")}
</div>
<section class="cols" id="arms"></section>
<h2>Verdict</h2>
<div class="verdict" id="verdict"></div>
<h2>Every measurement</h2>
<div class="tbl" id="alltable"></div>
<p class="note">Medians of 3 cold runs per variant on the replay server. Absolute numbers are kinder than the live site (no server time, no real CDN, HTTP/1.1 on localhost) but every variant was measured the same way, so the deltas are fair. Fidelity: same title, body text within 3 percent, same images in view, no new console errors, nothing first-party unserved, in at least 2 of 3 runs. Code and data: <code>speed_lab/</code> in the ecomOS repo.</p>
</main>
<script>
const DATA = {json.dumps(data)};
const fmtMs = x => x==null ? 'unavailable' : (x>=1000 ? (x/1000).toFixed(1)+' s' : Math.round(x)+' ms');
const fmtMb = x => (x/1048576).toFixed(2)+' MB';
const B = DATA.baseline.m;
const METS = [['load','Load',fmtMs,true],['lcp','LCP',fmtMs,true],['fcp','FCP',fmtMs,true],['tbt','Blocking time',fmtMs,true],['bytes','Wire bytes',fmtMb,true],['tp','Third-party bytes',fmtMb,true]];
const state = {{'arm-a':0,'arm-b':0}};
function delta(k,cur,f,lower){{const d=cur-B[k]; if(Math.abs(d)<1e-9) return ['no change','']; const pct=B[k]?Math.round(d/B[k]*100):0; const good = lower? d<0 : d>0; return [(d>0?'+':'')+ (k==='bytes'||k==='tp'? fmtMb(d): fmtMs(Math.abs(d)).replace(/^/, d<0?'-':'')) + ' ('+(pct>0?'+':'')+pct+'%)', good?'good':'bad'];}}
function render(){{
  const root=document.getElementById('arms'); root.innerHTML='';
  for(const [k,arm] of Object.entries(DATA.arms)){{
    const n=state[k]; const cur = n===0? DATA.baseline : arm.steps[n-1];
    const el=document.createElement('article'); el.className='arm '+(k==='arm-a'?'a':'b');
    let mets=''; for(const [key,label,fmt,lower] of METS){{ const [dtxt,dcls]=delta(key,cur.m[key],fmt,lower); const w=Math.max(2,Math.min(100,Math.round(cur.m[key]/B[key]*100))); mets+=`<div class="met"><div class="l">${{label}}</div><div class="v">${{fmt(cur.m[key])}}</div><div class="d ${{dcls}}">${{n===0?'baseline':dtxt}}</div><div class="bar"><i style="width:${{w}}%"></i></div></div>`; }}
    let fixes=''; arm.steps.forEach((s,i)=>{{ const on=i<n; const next=i===n; fixes+=`<li class="${{on?'on':''}}"><span class="n">${{i+1}}</span><span><div class="t">${{s.label}}</div><div class="fid">${{on?('fidelity '+s.fid+' · load '+fmtMs(s.m.load)+' · LCP '+fmtMs(s.m.lcp)):''}}</div></span><button data-arm="${{k}}" data-step="${{i+1}}" ${{next?'':'disabled'}}>${{on?'Applied':(next?'Fix it':'Next')}}</button></li>`; }});
    const tried = Object.entries(arm.tried).map(([id,t])=>`<li><span class="n">x</span><span><div class="t">${{t}}</div></span><span class="fid">reverted</span></li>`).join('');
    const lim = arm.limiters.map(l=>`<tr><td>${{l.rank}}</td><td>${{l.title}}</td><td>${{(l.fix||'').slice(0,160)}}</td><td>${{l.effort||''}}</td><td class="src">${{l.source||''}}</td></tr>`).join('');
    el.innerHTML=`<span class="tag">${{arm.name}}</span><div class="sub">${{arm.sub}}</div>
      <div class="ctl"><button class="primary" data-arm="${{k}}" data-step="${{Math.min(n+1,arm.steps.length)}}" ${{n>=arm.steps.length?'disabled':''}}>Fix next</button><button data-arm="${{k}}" data-step="${{Math.max(0,n-1)}}" ${{n===0?'disabled':''}}>Undo</button><button data-arm="${{k}}" data-step="${{arm.steps.length}}">Apply all</button><button data-arm="${{k}}" data-step="0">Reset</button></div>
      <div class="metrics">${{mets}}</div>
      <h3>Fixes in the order the agent ranked them</h3><ul class="fixes">${{fixes}}${{tried}}</ul>
      <div class="shots"><figure><img src="${{DATA.baseline.shot}}" alt="Baseline above the fold"><figcaption>Baseline, above the fold</figcaption></figure><figure><img src="${{cur.shot||DATA.baseline.shot}}" alt="After ${{n}} fixes"><figcaption>${{n===0?'No fix applied yet':'After fix '+n+': '+cur.label}}</figcaption></figure></div>
      <details><summary>The agent's top 10 limiters and where each came from</summary><div class="tbl"><table><thead><tr><th>#</th><th>Limiter</th><th>Fix</th><th>Effort</th><th>Source</th></tr></thead><tbody>${{lim}}</tbody></table></div></details>`;
    root.appendChild(el);
  }}
  root.querySelectorAll('button[data-arm]').forEach(b=>b.addEventListener('click',()=>{{state[b.dataset.arm]=parseInt(b.dataset.step,10); render();}}));
  const fa=DATA.arms['arm-a'].steps.at(-1).m, fb=DATA.arms['arm-b'].steps.at(-1).m;
  document.getElementById('verdict').innerHTML = VERDICT;
  let rows=`<table><thead><tr><th>Variant</th><th>Fix</th><th>LCP</th><th>FCP</th><th>DCL</th><th>Load</th><th>Blocking</th><th>Wire</th><th>1st party</th><th>3rd party</th><th>Req</th><th>Fidelity</th></tr></thead><tbody>`;
  const row=(name,label,m,fid)=>`<tr><td>${{name}}</td><td>${{label}}</td><td>${{fmtMs(m.lcp)}}</td><td>${{fmtMs(m.fcp)}}</td><td>${{fmtMs(m.dcl)}}</td><td>${{fmtMs(m.load)}}</td><td>${{fmtMs(m.tbt)}}</td><td>${{fmtMb(m.bytes)}}</td><td>${{fmtMb(m.fp)}}</td><td>${{fmtMb(m.tp)}}</td><td>${{m.req}}</td><td>${{fid}}</td></tr>`;
  rows+=row('baseline','none',B,'PASS');
  for(const [k,arm] of Object.entries(DATA.arms)) arm.steps.forEach((s,i)=>{{rows+=row(s.id,s.label,s.m,s.fid)}});
  document.getElementById('alltable').innerHTML=rows+'</tbody></table>';
}}
const VERDICT = {json.dumps(open(os.path.join(ROOT, "VERDICT.html")).read() if os.path.exists(os.path.join(ROOT, "VERDICT.html")) else "<p>Verdict pending the final measurements.</p>")};
render();
</script>
'''
    open(out, "w", encoding="utf-8").write(page)
    print(out, len(page) // 1024, "KB", "| final A", fa, "| final B", fb)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default=os.path.join(os.path.dirname(ROOT), "reviews", "speed-lab", "gehna-speed-lab.html"))
    main(ap.parse_args().out)
