"""Measure a variant of the mirrored page through the replay server.

Usage: python3 speed_lab/measure.py LABEL [--variant NAME] [--runs 3] [--url https://www.gehnaindia.com/]
Profile: Pixel 5 viewport, slow 4G (1.6 Mbps down, 150 ms RTT), 4x CPU slowdown, cold cache, 3 runs, median.
Writes results/LABEL.json (all runs + summary), results/LABEL-runN.png, and prints the summary line.
Every host resolves to the replay server, so third-party bytes are counted exactly from the server log.
"""
import argparse, asyncio, fcntl, json, os, statistics, sys, time
from urllib.parse import urlparse
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lab import ROOT, set_active

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
OUT = os.path.join(ROOT, "results")
LOG = os.path.join(OUT, "serve.log")
RUN = os.path.join(ROOT, "ACTIVE_RUN")
UA = "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"

INIT_JS = r"""
window.__m = {lcp:[], cls:[], longtasks:[], fcp:null, hydrated:null};
try{var __hp=setInterval(function(){var n=document.getElementById("__next");if(n&&Object.keys(n).some(function(k){return k.indexOf("__react")===0})){window.__m.hydrated=performance.now();clearInterval(__hp);}},100);}catch(e){}
try{
new PerformanceObserver(l=>{for(const e of l.getEntries()){window.__m.lcp.push({t:e.startTime,size:e.size,url:e.url||null,tag:e.element?e.element.tagName:null,text:e.element?(e.element.innerText||'').slice(0,60):null});}}).observe({type:'largest-contentful-paint',buffered:true});
new PerformanceObserver(l=>{for(const e of l.getEntries()){if(!e.hadRecentInput)window.__m.cls.push(e.value);}}).observe({type:'layout-shift',buffered:true});
new PerformanceObserver(l=>{for(const e of l.getEntries()){window.__m.longtasks.push({t:e.startTime,d:e.duration});}}).observe({type:'longtask',buffered:true});
new PerformanceObserver(l=>{for(const e of l.getEntries()){if(e.name==='first-contentful-paint')window.__m.fcp=e.startTime;}}).observe({type:'paint',buffered:true});
}catch(err){window.__m.err=String(err)}
"""
COLLECT_JS = r"""
() => {
 const nav = performance.getEntriesByType('navigation')[0];
 const res = performance.getEntriesByType('resource').map(r=>({name:r.name.slice(0,200),type:r.initiatorType,start:r.startTime,end:r.responseEnd,size:r.transferSize,rb:r.renderBlockingStatus||null}));
 const imgs=[...document.images].map(i=>{const r=i.getBoundingClientRect();return {src:(i.currentSrc||i.src||'').slice(0,160),nw:i.naturalWidth,nh:i.naturalHeight,w:Math.round(r.width),h:Math.round(r.height),top:Math.round(r.top+scrollY),loading:i.getAttribute('loading'),fp:i.getAttribute('fetchpriority'),inView:(r.top<innerHeight&&r.bottom>0&&r.width>0),complete:i.complete}});
 const fonts=[]; try{document.fonts.forEach(f=>fonts.push({family:f.family,weight:f.weight,status:f.status,display:f.display}))}catch(e){}
 const scripts=[...document.scripts].map(s=>({src:(s.src||'').slice(0,140),async:s.async,defer:s.defer,type:s.type,inline:!s.src?(s.textContent||'').length:0}));
 return {nav: nav?{ttfb:nav.responseStart,dcl:nav.domContentLoadedEventEnd,load:nav.loadEventEnd,transfer:nav.transferSize}:null,
  m: window.__m, res, imgs, fonts, scripts, domNodes: document.getElementsByTagName('*').length, bodyText:(document.body.innerText||'').length, title: document.title, url: location.href};
}
"""


def read_log(run):
    rows = []
    if not os.path.exists(LOG): return rows
    for line in open(LOG):
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("run") == run: rows.append(r)
    return rows


async def run(url, label, variant, runs, settle=6):
    os.makedirs(OUT, exist_ok=True)
    lock = open(os.path.join(ROOT, ".measure.lock"), "w")
    fcntl.flock(lock, fcntl.LOCK_EX)  # one measurement at a time; the replay server has one active variant
    set_active(variant)
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME, headless=True, args=["--no-sandbox", "--host-resolver-rules=MAP * 127.0.0.1", "--ignore-certificate-errors", "--no-proxy-server"])
        for i in range(runs):
            tag = f"{label}-run{i+1}-{int(time.time())}"
            open(RUN, "w").write(tag)
            ctx = await browser.new_context(user_agent=UA, viewport={"width": 393, "height": 851}, device_scale_factor=2.75, is_mobile=True, has_touch=True, ignore_https_errors=True)
            page = await ctx.new_page()
            console_errors, failed = [], []
            page.on("console", lambda m: console_errors.append(m.text[:200]) if m.type in ("error",) else None)
            page.on("pageerror", lambda e: console_errors.append(("pageerror: " + str(e))[:200]))
            page.on("requestfailed", lambda r: failed.append(r.url[:160]))
            await page.add_init_script(INIT_JS)
            cdp = await ctx.new_cdp_session(page)
            await cdp.send("Network.enable")
            await cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": 150, "downloadThroughput": 1.6 * 1024 * 1024 / 8, "uploadThroughput": 750 * 1024 / 8})
            await cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
            t0 = time.time()
            err = None
            try:
                await page.goto(url, wait_until="load", timeout=180000)
                await page.wait_for_timeout(settle * 1000)  # settle time after load; tags that fire on a timer need 25 s or more
            except Exception as e:
                err = str(e)[:200]
            data = None
            for attempt in range(3):
                try:
                    data = await page.evaluate(COLLECT_JS); break
                except Exception:
                    await page.wait_for_timeout(2000)
            if data is None:
                data = {"nav": None, "m": {"lcp": [], "cls": [], "longtasks": [], "fcp": None}, "res": [], "imgs": [], "fonts": [], "scripts": []}
            await page.screenshot(path=os.path.join(OUT, f"{label}-run{i+1}.png"), full_page=False)
            await ctx.close()
            served = read_log(tag)
            by_type, by_host = {}, {}
            for r in served:
                t = r.get("type") or "other"; h = urlparse(r["url"]).hostname or ""
                by_type.setdefault(t, [0, 0]); by_type[t][0] += 1; by_type[t][1] += r["wire"]
                by_host.setdefault(h, [0, 0]); by_host[h][0] += 1; by_host[h][1] += r["wire"]
            lcp = data["m"]["lcp"][-1] if data["m"]["lcp"] else None
            summary = {
                "run": i + 1, "variant": variant or "base", "error": err,
                "fcp_ms": data["m"]["fcp"], "lcp_ms": lcp["t"] if lcp else None, "lcp_el": lcp,
                "dcl_ms": data["nav"]["dcl"] if data["nav"] else None, "load_ms": data["nav"]["load"] if data["nav"] else None,
                "cls": round(sum(data["m"]["cls"]), 4), "hydrated_ms": data["m"].get("hydrated"), "tags_start_ms": min([x["start"] for x in data["res"] if any(t in x["name"] for t in ("googletagmanager.com/gtm.js", "klaviyo.js?company", "fbevents.js"))] or [None]) if data["res"] else None, "long_tasks": len(data["m"]["longtasks"]), "tbt_est_ms": round(sum(max(0, lt["d"] - 50) for lt in data["m"]["longtasks"])),
                "requests_served": len(served), "misses": sum(1 for r in served if r["status"] == 404 and r["src"] == "miss"),
                "wire_bytes": sum(r["wire"] for r in served), "by_type": by_type, "by_host": by_host,
                "first_party_bytes": sum(v[1] for h, v in by_host.items() if h.endswith("gehnaindia.com")),
                "third_party_bytes": sum(v[1] for h, v in by_host.items() if not h.endswith("gehnaindia.com")),
                "images_in_view": sum(1 for im in data["imgs"] if im["inView"]), "dom_nodes": data.get("domNodes"), "body_text_chars": data.get("bodyText"), "title": data.get("title"),
                "console_errors": console_errors[:20], "failed_requests": failed[:20], "wall_s": round(time.time() - t0, 1),
            }
            results.append({"summary": summary, "detail": data, "served": served})
            print(json.dumps({k: v for k, v in summary.items() if k not in ("by_type", "by_host", "lcp_el", "console_errors", "failed_requests")}), flush=True)
        await browser.close()
    med = {}
    for k in ("fcp_ms", "lcp_ms", "dcl_ms", "load_ms", "hydrated_ms", "tags_start_ms", "cls", "tbt_est_ms", "wire_bytes", "first_party_bytes", "third_party_bytes", "requests_served"):
        vals = [r["summary"][k] for r in results if r["summary"][k] is not None]
        med[k] = statistics.median(vals) if vals else None
    out = {"label": label, "variant": variant or "base", "url": url, "profile": "Pixel 5, slow 4G 1.6 Mbps 150 ms RTT, 4x CPU, cold cache", "settle_s": settle, "store": os.environ.get("SPEED_LAB_STORE") or "store", "runs": results, "median": med, "by_type_run1": results[0]["summary"]["by_type"], "by_host_run1": results[0]["summary"]["by_host"]}
    json.dump(out, open(os.path.join(OUT, f"{label}.json"), "w"), indent=1)
    set_active(None)
    fcntl.flock(lock, fcntl.LOCK_UN)
    print("MEDIAN", json.dumps(med))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("label"); ap.add_argument("--variant", default=None); ap.add_argument("--runs", type=int, default=3); ap.add_argument("--url", default="https://www.gehnaindia.com/"); ap.add_argument("--settle", type=int, default=6, help="seconds to wait after load")
    a = ap.parse_args()
    asyncio.run(run(a.url, a.label, a.variant, a.runs, a.settle))
