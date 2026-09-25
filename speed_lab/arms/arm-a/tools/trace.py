"""Diagnostic: one throttled load of a variant with a Chrome trace; attribute long tasks to scripts.

Usage: python3 speed_lab/arms/arm-a/tools/trace.py VARIANT|base [--out FILE]
Uses the same profile as measure.py and takes the same lock, so it never overlaps a measurement.
Not a measurement: numbers here are for attribution only, never reported as results.
"""
import argparse, asyncio, fcntl, json, os, sys, time
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, LAB)
from lab import ROOT, set_active
from measure import CHROME, UA, RUN
from playwright.async_api import async_playwright

CATS = ["devtools.timeline", "disabled-by-default-devtools.timeline", "v8.execute", "blink.user_timing", "loading"]


async def main(variant, out):
    lock = open(os.path.join(ROOT, ".measure.lock"), "w")
    fcntl.flock(lock, fcntl.LOCK_EX)
    try:
        set_active(None if variant == "base" else variant)
        open(RUN, "w").write(f"arm-a-trace-{int(time.time())}")
        async with async_playwright() as p:
            br = await p.chromium.launch(executable_path=CHROME, headless=True, args=["--no-sandbox", "--host-resolver-rules=MAP * 127.0.0.1", "--ignore-certificate-errors", "--no-proxy-server"])
            ctx = await br.new_context(user_agent=UA, viewport={"width": 393, "height": 851}, device_scale_factor=2.75, is_mobile=True, has_touch=True, ignore_https_errors=True)
            page = await ctx.new_page()
            cdp = await ctx.new_cdp_session(page)
            await cdp.send("Network.enable")
            await cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": 150, "downloadThroughput": 1.6 * 1024 * 1024 / 8, "uploadThroughput": 750 * 1024 / 8})
            await cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
            await br.start_tracing(page=page, categories=CATS)
            await page.goto("https://www.gehnaindia.com/", wait_until="load", timeout=180000)
            await page.wait_for_timeout(6000)
            data = await br.stop_tracing()
            await br.close()
    finally:
        set_active(None)
        fcntl.flock(lock, fcntl.LOCK_UN)
    tr = json.loads(data)
    ev = tr["traceEvents"] if isinstance(tr, dict) else tr
    # main renderer thread
    names = {(e["pid"], e["tid"]): e["args"]["name"] for e in ev if e.get("name") == "thread_name"}
    mains = [k for k, v in names.items() if v == "CrRendererMain"]
    nav = [e for e in ev if e.get("name") == "navigationStart" and (e["pid"], e["tid"]) in mains]
    # pick the renderer with most RunTask time
    best = max(mains, key=lambda k: sum(e.get("dur", 0) for e in ev if (e["pid"], e["tid"]) == k and e.get("name") == "RunTask"))
    t0 = min(e["ts"] for e in nav if (e["pid"], e["tid"]) == best) if any((e["pid"], e["tid"]) == best for e in nav) else 0
    th = sorted([e for e in ev if (e["pid"], e["tid"]) == best and e.get("ph") == "X"], key=lambda e: e["ts"])
    tasks = [e for e in th if e["name"] == "RunTask" and e.get("dur", 0) > 50000]
    rows = []
    for t in tasks:
        end = t["ts"] + t["dur"]
        inside = [e for e in th if t["ts"] <= e["ts"] < end and e is not t]
        by = defaultdict(float)
        for e in inside:
            if e["name"] in ("EvaluateScript", "FunctionCall", "v8.compile", "v8.compileModule", "TimerFire", "EventDispatch", "FireAnimationFrame", "V8.Execute"):
                d = (e.get("args", {}).get("data") or {})
                u = d.get("url") or d.get("scriptName") or d.get("type") or ""
                if e["name"] in ("EvaluateScript", "FunctionCall", "v8.compile"):
                    by[(e["name"], u[:110])] += e.get("dur", 0) / 1000
        top = sorted(by.items(), key=lambda x: -x[1])[:4]
        rows.append({"t": round((t["ts"] - t0) / 1000), "d": round(t["dur"] / 1000), "top": [(k[0], k[1], round(v)) for k, v in top]})
    json.dump(rows, open(out, "w"), indent=1) if out else None
    for r in rows:
        print(r["t"], r["d"], r["top"])
    print("TBT-like sum", sum(max(0, r["d"] - 50) for r in rows))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("variant"); ap.add_argument("--out")
    a = ap.parse_args()
    asyncio.run(main(a.variant, a.out))
