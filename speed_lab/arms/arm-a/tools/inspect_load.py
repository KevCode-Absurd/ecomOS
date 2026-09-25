"""Diagnostic: one throttled load of a variant; save every request (method, url, status or failure), console
messages and the page text. Same profile and lock as measure.py. For debugging only, not a measurement.
Usage: python3 speed_lab/arms/arm-a/tools/inspect_load.py VARIANT|base OUT.json [--wait 6000]
"""
import argparse, asyncio, fcntl, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..")))
from lab import ROOT, set_active
from measure import CHROME, UA, RUN
from playwright.async_api import async_playwright


async def main(variant, out, wait):
    lock = open(os.path.join(ROOT, ".measure.lock"), "w")
    fcntl.flock(lock, fcntl.LOCK_EX)
    reqs, cons = [], []
    try:
        set_active(None if variant == "base" else variant)
        open(RUN, "w").write(f"arm-a-inspect-{int(time.time())}")
        async with async_playwright() as p:
            br = await p.chromium.launch(executable_path=CHROME, headless=True, args=["--no-sandbox", "--host-resolver-rules=MAP * 127.0.0.1", "--ignore-certificate-errors", "--no-proxy-server"])
            ctx = await br.new_context(user_agent=UA, viewport={"width": 393, "height": 851}, device_scale_factor=2.75, is_mobile=True, has_touch=True, ignore_https_errors=True)
            page = await ctx.new_page()
            t0 = time.time()
            page.on("requestfinished", lambda r: reqs.append({"t": round((time.time() - t0) * 1000), "m": r.method, "u": r.url[:200], "ok": True}))
            page.on("requestfailed", lambda r: reqs.append({"t": round((time.time() - t0) * 1000), "m": r.method, "u": r.url[:200], "ok": False, "f": r.failure}))
            page.on("console", lambda m: cons.append({"t": round((time.time() - t0) * 1000), "type": m.type, "text": m.text[:300]}))
            page.on("pageerror", lambda e: cons.append({"t": round((time.time() - t0) * 1000), "type": "pageerror", "text": str(e)[:300]}))
            cdp = await ctx.new_cdp_session(page)
            await cdp.send("Network.enable")
            await cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": 150, "downloadThroughput": 1.6 * 1024 * 1024 / 8, "uploadThroughput": 750 * 1024 / 8})
            await cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
            await page.goto("https://www.gehnaindia.com/", wait_until="load", timeout=180000)
            load_s = round(time.time() - t0, 2)
            await page.wait_for_timeout(wait)
            text = await page.evaluate("document.body.innerText")
            await page.screenshot(path=out.replace(".json", ".png"))
            await br.close()
    finally:
        set_active(None)
        fcntl.flock(lock, fcntl.LOCK_UN)
    json.dump({"variant": variant, "load_s": load_s, "wait_ms": wait, "requests": reqs, "console": cons, "text": text}, open(out, "w"), indent=1)
    print("load_s", load_s, "requests", len(reqs), "failed", sum(1 for r in reqs if not r["ok"]), "text", len(text))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("variant"); ap.add_argument("out"); ap.add_argument("--wait", type=int, default=6000)
    a = ap.parse_args()
    asyncio.run(main(a.variant, a.out, a.wait))
