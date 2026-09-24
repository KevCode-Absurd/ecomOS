import asyncio, json, os, sys, time
from urllib.parse import urlparse
from playwright.async_api import async_playwright

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
OUT = "/home/user/ecomOS/reviews/speed-test/raw-a"
UA = "Mozilla/5.0 (Linux; Android 11; moto g power (2022)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
# Lighthouse mobile "slow 4G" profile: 1.6 Mbps down, 750 Kbps up, 150 ms RTT, 4x CPU slowdown
NET = dict(offline=False, latency=150, downloadThroughput=int(1.6*1024*1024/8), uploadThroughput=int(750*1024/8))
CPU = 4

INIT = r"""
window.__perf = {lcp: [], cls: [], longtasks: [], fcp: null, layoutShiftValue: 0};
try {
  new PerformanceObserver(l => { for (const e of l.getEntries()) {
    let el = e.element; let desc = null;
    if (el) { desc = {tag: el.tagName, id: el.id||null, cls: (el.className && el.className.baseVal===undefined ? String(el.className).slice(0,120) : null), src: (el.currentSrc||el.src||null), text: (el.innerText||'').slice(0,80)}; }
    window.__perf.lcp.push({time: e.startTime, renderTime: e.renderTime, loadTime: e.loadTime, size: e.size, url: e.url||null, element: desc});
  }}).observe({type:'largest-contentful-paint', buffered:true});
  new PerformanceObserver(l => { for (const e of l.getEntries()) {
    if (!e.hadRecentInput) { window.__perf.layoutShiftValue += e.value;
      window.__perf.cls.push({time: e.startTime, value: e.value, sources: (e.sources||[]).slice(0,3).map(s => { const n = s.node; return n ? {tag: n.tagName, id: n.id||null, cls: (n.className && typeof n.className==='string') ? n.className.slice(0,100) : null, text:(n.innerText||'').slice(0,60), prev: s.previousRect ? [s.previousRect.x,s.previousRect.y,s.previousRect.width,s.previousRect.height] : null, cur: s.currentRect ? [s.currentRect.x,s.currentRect.y,s.currentRect.width,s.currentRect.height] : null} : null; }) });
    }
  }}).observe({type:'layout-shift', buffered:true});
  new PerformanceObserver(l => { for (const e of l.getEntries()) { window.__perf.longtasks.push({start: e.startTime, duration: e.duration, name: e.name, attribution: (e.attribution||[]).map(a=>a.containerSrc||a.containerName||a.name).slice(0,2)}); } }).observe({type:'longtask', buffered:true});
  new PerformanceObserver(l => { for (const e of l.getEntries()) { if (e.name==='first-contentful-paint') window.__perf.fcp = e.startTime; } }).observe({type:'paint', buffered:true});
} catch (err) { window.__perf.error = String(err); }
"""

COLLECT = r"""
() => {
  const nav = performance.getEntriesByType('navigation')[0];
  const navj = nav ? nav.toJSON() : null;
  const res = performance.getEntriesByType('resource').map(r => ({name: r.name, type: r.initiatorType, start: r.startTime, dur: r.duration, transfer: r.transferSize, encoded: r.encodedBodySize, decoded: r.decodedBodySize, proto: r.nextHopProtocol, renderBlocking: r.renderBlockingStatus||null}));
  const imgs = Array.from(document.querySelectorAll('img')).map(i => { const r = i.getBoundingClientRect(); return {src: (i.currentSrc||i.src||'').slice(0,300), alt: (i.alt||'').slice(0,60), naturalW: i.naturalWidth, naturalH: i.naturalHeight, renderedW: Math.round(r.width), renderedH: Math.round(r.height), top: Math.round(r.top + window.scrollY), loading: i.getAttribute('loading'), fetchpriority: i.getAttribute('fetchpriority'), decoding: i.getAttribute('decoding'), hasWidthAttr: i.hasAttribute('width'), hasHeightAttr: i.hasAttribute('height'), inViewport: r.top < window.innerHeight && r.bottom > 0 && r.width > 0, complete: i.complete}; });
  const fonts = Array.from(document.fonts).map(f => ({family: f.family, weight: f.weight, style: f.style, status: f.status, display: f.display}));
  const scripts = Array.from(document.scripts).map(s => ({src: (s.src||'').slice(0,200), async: s.async, defer: s.defer, type: s.type, inlineLen: s.src ? 0 : (s.textContent||'').length}));
  const iframes = Array.from(document.querySelectorAll('iframe')).map(f => ({src: (f.src||'').slice(0,200), w: f.width, h: f.height}));
  const dom = document.getElementsByTagName('*').length;
  const links = Array.from(document.querySelectorAll('a[href]')).map(a => a.getAttribute('href')).filter(h => h && h.startsWith('/'));
  const productLinks = links.filter(h => /\/p\/|product|\/products\//i.test(h)).slice(0,10);
  const sheets = Array.from(document.styleSheets).map(s => { let n=0; try { n = s.cssRules.length; } catch(e) { n=-1; } return {href: s.href, rules: n}; });
  const mem = performance.memory ? {usedJSHeap: performance.memory.usedJSHeapSize, totalJSHeap: performance.memory.totalJSHeapSize} : null;
  return {nav: navj, resources: res, images: imgs, fonts, scripts, iframes, domNodes: dom, productLinks, allLinksCount: links.length, sheets, mem, perf: window.__perf, docHeight: document.documentElement.scrollHeight, viewport: [window.innerWidth, window.innerHeight], dpr: window.devicePixelRatio, title: document.title, generator: (document.querySelector('meta[name=generator]')||{}).content||null, nextData: !!document.getElementById('__NEXT_DATA__'), nextDataLen: (document.getElementById('__NEXT_DATA__')||{textContent:''}).textContent.length, bodyClass: document.body.className, html: document.documentElement.outerHTML.length};
}
"""

async def run(url, label, n, browser):
    ctx = await browser.new_context(user_agent=UA, viewport={"width":412,"height":823}, device_scale_factor=1.75, is_mobile=True, has_touch=True, locale="en-IN", timezone_id="Asia/Kolkata")
    page = await ctx.new_page()
    cdp = await ctx.new_cdp_session(page)
    await cdp.send("Network.enable")
    await cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
    await cdp.send("Network.emulateNetworkConditions", NET)
    await cdp.send("Emulation.setCPUThrottlingRate", {"rate": CPU})
    await page.add_init_script(INIT)
    reqs = {}
    order = []
    def on_req(p):
        r = p["request"]; rid = p["requestId"]
        if p.get("redirectResponse"):
            reqs.setdefault(rid, {}).setdefault("redirects", []).append({"from": p["redirectResponse"]["url"], "status": p["redirectResponse"]["status"], "to": r["url"]})
        e = reqs.setdefault(rid, {})
        e.update({"url": r["url"], "method": r["method"], "type": p.get("type"), "initiator": (p.get("initiator") or {}).get("type"), "initiatorUrl": ((p.get("initiator") or {}).get("url") or ((p.get("initiator") or {}).get("stack") or {}).get("callFrames", [{}])[0].get("url")), "ts": p["timestamp"], "priority": r.get("initialPriority")})
        if rid not in order: order.append(rid)
    def on_resp(p):
        r = p["response"]; e = reqs.setdefault(p["requestId"], {})
        h = {k.lower(): v for k, v in r.get("headers", {}).items()}
        e.update({"status": r["status"], "mime": r.get("mimeType"), "protocol": r.get("protocol"), "fromCache": r.get("fromDiskCache") or r.get("fromServiceWorker"), "remoteIP": r.get("remoteIPAddress"), "headers": {k: h.get(k) for k in ["cache-control","content-encoding","content-type","content-length","age","cf-cache-status","x-cache","expires","etag","last-modified","server","vary","x-nextjs-cache","alt-svc","x-amz-cf-pop"] if k in h}, "timing": r.get("timing")})
    def on_fin(p):
        e = reqs.setdefault(p["requestId"], {}); e["encodedLength"] = p.get("encodedDataLength"); e["finishTs"] = p["timestamp"]
    def on_fail(p):
        e = reqs.setdefault(p["requestId"], {}); e["failed"] = p.get("errorText"); e["blocked"] = p.get("blockedReason")
    cdp.on("Network.requestWillBeSent", on_req); cdp.on("Network.responseReceived", on_resp); cdp.on("Network.loadingFinished", on_fin); cdp.on("Network.loadingFailed", on_fail)
    console = []
    page.on("console", lambda m: console.append({"type": m.type, "text": m.text[:200]}) if m.type in ("error","warning") else None)
    t0 = time.time()
    try:
        await page.goto(url, wait_until="load", timeout=90000)
    except Exception as ex:
        print("goto error", ex)
    load_wall = time.time() - t0
    try:
        await page.wait_for_load_state("networkidle", timeout=30000)
    except Exception as ex:
        print("networkidle timeout")
    await page.wait_for_timeout(3000)
    data = await page.evaluate(COLLECT)
    # also DOM element size check at LCP element via evaluate done above
    await page.screenshot(path=f"{OUT}/{label}-run{n}.png", full_page=False)
    metrics = await cdp.send("Performance.enable") if False else None
    # attach network
    net = []
    for rid in order:
        e = reqs.get(rid, {}); e = dict(e); e["id"] = rid; net.append(e)
    data.update({"url": url, "label": label, "run": n, "wallLoadSeconds": load_wall, "throttle": {"network": NET, "cpu": CPU}, "network": net, "console": console[:40], "finalUrl": page.url, "capturedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    with open(f"{OUT}/{label}-run{n}.json", "w") as f: json.dump(data, f, indent=1)
    lcp = data["perf"]["lcp"][-1] if data["perf"]["lcp"] else None
    nav = data["nav"] or {}
    tot = sum((e.get("encodedLength") or 0) for e in net)
    print(f"{label} run{n}: ttfb={nav.get('responseStart')} fcp={data['perf']['fcp']} lcp={lcp and lcp['time']} lcp_el={lcp and lcp['element']} dcl={nav.get('domContentLoadedEventEnd')} load={nav.get('loadEventEnd')} cls={data['perf']['layoutShiftValue']:.3f} reqs={len(net)} bytes={tot} longtasks={len(data['perf']['longtasks'])} products={data['productLinks'][:3]}")
    await ctx.close()
    return data

async def main():
    pages = json.loads(sys.argv[1])
    runs = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME, headless=True, args=["--no-sandbox","--disable-dev-shm-usage"], proxy={"server": os.environ.get("HTTPS_PROXY"), "bypass": "localhost,127.0.0.1"})
        for label, url in pages.items():
            for n in range(1, runs+1):
                await run(url, label, n, browser)
        await browser.close()

asyncio.run(main())
