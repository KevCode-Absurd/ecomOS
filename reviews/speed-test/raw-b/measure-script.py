import asyncio, json, sys, time, os
from urllib.parse import urlparse
from playwright.async_api import async_playwright

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
OUT = "/home/user/ecomOS/reviews/speed-test/raw-b"
UA = "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"

INIT_JS = r"""
window.__m = {timeOrigin: performance.timeOrigin, lcp:[], cls:[], clsEntries:[], longtasks:[], fcp:null};
try{
new PerformanceObserver(l=>{for(const e of l.getEntries()){window.__m.lcp.push({t:e.startTime,size:e.size,url:e.url||null,tag:e.element?e.element.tagName:null,id:e.element?e.element.id:null,cls:e.element?String(e.element.className).slice(0,80):null,text:e.element?(e.element.innerText||'').slice(0,80):null,loadTime:e.loadTime,renderTime:e.renderTime});}}).observe({type:'largest-contentful-paint',buffered:true});
new PerformanceObserver(l=>{for(const e of l.getEntries()){if(!e.hadRecentInput){window.__m.cls.push(e.value);window.__m.clsEntries.push({t:e.startTime,v:e.value,src:(e.sources||[]).map(s=>s.node?(s.node.tagName+'#'+(s.node.id||'')+'.'+String(s.node.className||'').slice(0,60)+' '+((s.node.innerText||'').slice(0,40))):'?')});}}}).observe({type:'layout-shift',buffered:true});
new PerformanceObserver(l=>{for(const e of l.getEntries()){window.__m.longtasks.push({t:e.startTime,d:e.duration});}}).observe({type:'longtask',buffered:true});
new PerformanceObserver(l=>{for(const e of l.getEntries()){if(e.name==='first-contentful-paint')window.__m.fcp=e.startTime;}}).observe({type:'paint',buffered:true});
}catch(err){window.__m.err=String(err)}
"""

COLLECT_JS = r"""
() => {
 const nav = performance.getEntriesByType('navigation')[0];
 const res = performance.getEntriesByType('resource').map(r=>({name:r.name,type:r.initiatorType,dur:r.duration,start:r.startTime,end:r.responseEnd,size:r.transferSize,dec:r.decodedBodySize,proto:r.nextHopProtocol,rb:r.renderBlockingStatus||null}));
 const imgs=[...document.images].map(i=>{const r=i.getBoundingClientRect();return {src:(i.currentSrc||i.src||'').slice(0,200),nw:i.naturalWidth,nh:i.naturalHeight,w:Math.round(r.width),h:Math.round(r.height),top:Math.round(r.top+scrollY),loading:i.getAttribute('loading'),fp:i.getAttribute('fetchpriority'),hasWH:!!(i.getAttribute('width')&&i.getAttribute('height')),alt:(i.alt||'').slice(0,40),inView:(r.top<innerHeight&&r.bottom>0&&r.width>0)}});
 const fonts=[]; try{document.fonts.forEach(f=>fonts.push({family:f.family,weight:f.weight,style:f.style,status:f.status,display:f.display}))}catch(e){}
 const scripts=[...document.scripts].map(s=>({src:(s.src||'').slice(0,160),async:s.async,defer:s.defer,type:s.type,inline:!s.src?(s.textContent||'').length:0}));
 const iframes=[...document.querySelectorAll('iframe')].map(f=>f.src.slice(0,120));
 const videos=[...document.querySelectorAll('video')].map(v=>({src:(v.currentSrc||v.src||'').slice(0,120),autoplay:v.autoplay,preload:v.preload}));
 return {nav: nav?{ttfb:nav.responseStart,domInteractive:nav.domInteractive,dcl:nav.domContentLoadedEventEnd,load:nav.loadEventEnd,transfer:nav.transferSize,decoded:nav.decodedBodySize,proto:nav.nextHopProtocol,redirects:nav.redirectCount,type:nav.type}:null,
  m: window.__m, res, imgs, fonts, scripts, iframes, videos,
  domNodes: document.getElementsByTagName('*').length, bodyText: (document.body.innerText||'').length,
  vw: innerWidth, vh: innerHeight, dpr: devicePixelRatio, title: document.title, url: location.href,
  scrollHeight: document.documentElement.scrollHeight, links:[...new Set([...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')).filter(h=>h&&h.startsWith('/')))].slice(0,300) };
}
"""

async def run(url, label, runs=3, throttle=True, cpu=4, cache_repeat=False, desktop=False):
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME, headless=True, args=["--no-sandbox"])
        results = []
        for i in range(runs):
            ctx = await (browser.new_context(viewport={"width":1366,"height":768}, device_scale_factor=1) if desktop else browser.new_context(user_agent=UA, viewport={"width":393,"height":851}, device_scale_factor=2.75, is_mobile=True, has_touch=True))
            page = await ctx.new_page()
            await page.add_init_script(INIT_JS)
            cdp = await ctx.new_cdp_session(page)
            await cdp.send("Network.enable")
            if throttle:
                # Chrome "Slow 4G" preset (was "Fast 3G"): 1.6 Mbps down, 750 kbps up, 150 ms RTT
                await cdp.send("Network.emulateNetworkConditions", {"offline":False,"latency":150,"downloadThroughput":1.6*1024*1024/8,"uploadThroughput":750*1024/8})
            if cpu and cpu>1:
                await cdp.send("Emulation.setCPUThrottlingRate", {"rate":cpu})
            headers = {}
            statuses = []
            async def on_resp(r):
                try:
                    u=r.url
                    if len(statuses)<400:
                        statuses.append({"url":u[:200],"status":r.status,"ct":(r.headers.get("content-type") or "")[:60],"cc":r.headers.get("cache-control"),"enc":r.headers.get("content-encoding"),"xcache":r.headers.get("x-cache") or r.headers.get("cf-cache-status"),"age":r.headers.get("age")})
                    if u.rstrip('/')==url.rstrip('/') or (r.request.resource_type=="document" and not headers):
                        headers.update({k:v for k,v in r.headers.items()})
                except Exception as e:
                    pass
            page.on("response", on_resp)
            navs=[]; loads=[]
            page.on("load", lambda: loads.append(time.time()-t0))
            page.on("framenavigated", lambda f: navs.append({"t":time.time()-t0,"url":f.url[:200],"main":f==page.main_frame}))
            t0=time.time()
            try:
                await page.goto(url, wait_until="load", timeout=120000)
                await page.wait_for_timeout(6000)
            except Exception as e:
                print("goto error", e)
            data=None
            for attempt in range(4):
                try:
                    data = await page.evaluate(COLLECT_JS); break
                except Exception as e:
                    print("evaluate retry", attempt, str(e)[:100]); await page.wait_for_timeout(3000)
            if data is None:
                data={"nav":None,"m":{"lcp":[],"cls":[],"clsEntries":[],"longtasks":[],"fcp":None},"res":[],"imgs":[],"fonts":[],"scripts":[],"iframes":[],"videos":[],"url":page.url}
            data["navigations"]=navs; data["load_events"]=loads; data["t0_epoch_ms"]=t0*1000
            data["final_url"]=page.url
            data["wall_s"]=time.time()-t0
            data["doc_headers"]=headers
            data["responses"]=statuses
            data["run"]=i+1
            data["throttle"]=("slow4g_cpu%dx"%cpu if throttle else "none")+("_desktop" if desktop else "_mobile")
            # summary
            res=data["res"]
            by={}
            for r in res:
                host=urlparse(r["name"]).hostname or ""
                t=r["type"]; by.setdefault(t,{"n":0,"bytes":0}); by[t]["n"]+=1; by[t]["bytes"]+=r["size"] or 0
            hosts={}
            for r in res:
                host=urlparse(r["name"]).hostname or ""; hosts.setdefault(host,{"n":0,"bytes":0}); hosts[host]["n"]+=1; hosts[host]["bytes"]+=r["size"] or 0
            lcp=data["m"]["lcp"][-1] if data["m"]["lcp"] else None
            tot=sum((r["size"] or 0) for r in res)+(data["nav"]["transfer"] if data["nav"] else 0)
            tbt=sum(max(0,lt["d"]-50) for lt in data["m"]["longtasks"])
            data["summary"]={"ttfb":data["nav"]["ttfb"] if data["nav"] else None,"fcp":data["m"]["fcp"],"lcp":lcp["t"] if lcp else None,"lcp_el":lcp,"cls":sum(data["m"]["cls"]),"longtasks":len(data["m"]["longtasks"]),"tbt_est":tbt,"load":data["nav"]["load"] if data["nav"] else None,"requests":len(res)+1,"bytes":tot,"by_type":by,"hosts":hosts}
            results.append(data)
            print(json.dumps({"label":label,"run":i+1,**{k:v for k,v in data["summary"].items() if k not in("by_type","hosts","lcp_el")},"lcp_el":(lcp or {}).get("url") or (lcp or {}).get("text")}), flush=True)
            await page.screenshot(path=f"{OUT}/{label}-run{i+1}.png", full_page=False)
            await ctx.close()
        await browser.close()
        with open(f"{OUT}/{label}.json","w") as f: json.dump(results,f)
        return results

if __name__=="__main__":
    url=sys.argv[1]; label=sys.argv[2]; runs=int(sys.argv[3]) if len(sys.argv)>3 else 3
    throttle = (sys.argv[4]!="none") if len(sys.argv)>4 else True
    desktop = (len(sys.argv)>5 and sys.argv[5]=="desktop")
    asyncio.run(run(url,label,runs,throttle,cpu=(1 if desktop else 4),desktop=desktop))
