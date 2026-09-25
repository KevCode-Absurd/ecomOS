"""Arm B diagnostic load: same profile as measure.py, one run, dumps page text, element info and timings.
Holds the measurement lock so it never overlaps a measurement, and tags its own serve.log lines.
Usage: python3 speed_lab/arms/arm-b/diag.py VARIANT|base OUTPREFIX [--wait MS] [--trace]"""
import asyncio, fcntl, json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import measure as M
from lab import ROOT, set_active
from playwright.async_api import async_playwright

async def main(variant, out, wait, trace):
    lock = open(os.path.join(ROOT, ".measure.lock"), "w"); fcntl.flock(lock, fcntl.LOCK_EX)
    set_active(None if variant == "base" else variant)
    tag = f"armb-diag-{int(time.time())}"; open(M.RUN, "w").write(tag)
    try:
        async with async_playwright() as p:
            br = await p.chromium.launch(executable_path=M.CHROME, headless=True, args=["--no-sandbox", "--host-resolver-rules=MAP * 127.0.0.1", "--ignore-certificate-errors", "--no-proxy-server"])
            ctx = await br.new_context(user_agent=M.UA, viewport={"width": 393, "height": 851}, device_scale_factor=2.75, is_mobile=True, has_touch=True, ignore_https_errors=True)
            page = await ctx.new_page(); errs = []
            page.on("console", lambda m: errs.append(m.type + ": " + m.text[:300]))
            page.on("pageerror", lambda e: errs.append("pageerror: " + str(e)[:300]))
            await page.add_init_script(M.INIT_JS)
            cdp = await ctx.new_cdp_session(page)
            await cdp.send("Network.enable")
            await cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": 150, "downloadThroughput": 1.6 * 1024 * 1024 / 8, "uploadThroughput": 750 * 1024 / 8})
            await cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
            if trace:
                await br.start_tracing(page=page, path=out + "-trace.json", categories=["devtools.timeline", "disabled-by-default-devtools.timeline", "v8.execute", "blink.user_timing"])
            await page.goto("https://www.gehnaindia.com/", wait_until="load", timeout=180000)
            await page.wait_for_timeout(wait)
            if trace:
                await br.stop_tracing()
            data = await page.evaluate(M.COLLECT_JS)
            data["innerText"] = await page.evaluate("document.body.innerText")
            data["fontUse"] = await page.evaluate("""() => { const out = {}; const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
              while (w.nextNode()) { const n = w.currentNode; const t = n.textContent.trim(); if (!t) continue; const el = n.parentElement; const r = el.getBoundingClientRect();
                if (r.width === 0 || r.height === 0) continue; const cs = getComputedStyle(el); const inView = r.top < innerHeight && r.bottom > 0;
                const k = cs.fontFamily.split(',')[0] + ' ' + cs.fontWeight + (inView ? ' INVIEW' : ''); out[k] = (out[k] || 0) + t.length; } return out; }""")
            data["console"] = errs
            await page.screenshot(path=out + ".png", full_page=True)
            json.dump(data, open(out + ".json", "w"), indent=1)
            await br.close()
    finally:
        set_active(None); fcntl.flock(lock, fcntl.LOCK_UN)
    print("done", out)

if __name__ == "__main__":
    a = sys.argv[1:]
    wait = int(a[a.index("--wait") + 1]) if "--wait" in a else 6000
    asyncio.run(main(a[0], a[1], wait, "--trace" in a))
