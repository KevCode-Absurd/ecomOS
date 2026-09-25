"""Record a filmstrip of the page loading through the replay server on the throttled mobile profile.

Usage: python3 speed_lab/filmstrip.py LABEL [--variant NAME] [--seconds 16] [--step 0.5]
Writes results/film-LABEL.json: frames as small JPEG data URIs with their time in seconds, plus the
moment the load event fired. Same profile as measure.py. Illustrative: the harness numbers are the record.
"""
import argparse, asyncio, base64, fcntl, io, json, os, sys, time
from PIL import Image
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lab import ROOT, set_active

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
UA = "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"


async def run(label, variant, seconds, step, url="https://www.gehnaindia.com/"):
    lock = open(os.path.join(ROOT, ".measure.lock"), "w"); fcntl.flock(lock, fcntl.LOCK_EX)
    set_active(variant)
    open(os.path.join(ROOT, "ACTIVE_RUN"), "w").write(f"film-{label}")
    frames, loaded_at = [], None
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME, headless=True, args=["--no-sandbox", "--host-resolver-rules=MAP * 127.0.0.1", "--ignore-certificate-errors", "--no-proxy-server"])
        ctx = await browser.new_context(user_agent=UA, viewport={"width": 393, "height": 851}, device_scale_factor=1.5, is_mobile=True, has_touch=True, ignore_https_errors=True)
        page = await ctx.new_page()
        cdp = await ctx.new_cdp_session(page)
        await cdp.send("Network.enable")
        await cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": 150, "downloadThroughput": 1.6 * 1024 * 1024 / 8, "uploadThroughput": 750 * 1024 / 8})
        await cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
        t0 = time.time()
        page.on("load", lambda: frames.append(("load", time.time() - t0)))
        nav = asyncio.ensure_future(page.goto(url, wait_until="load", timeout=int(seconds * 1000) + 60000))
        t = 0.0
        while t <= seconds:
            target = t0 + t
            now = time.time()
            if target > now: await asyncio.sleep(target - now)
            try:
                png = await page.screenshot(type="jpeg", quality=55, full_page=False)
                im = Image.open(io.BytesIO(png)).convert("RGB"); im = im.resize((260, int(im.height * 260 / im.width)), Image.LANCZOS).crop((0, 0, 260, 520))
                b = io.BytesIO(); im.save(b, "JPEG", quality=58, optimize=True)
                frames.append(("frame", round(time.time() - t0, 2), "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()))
            except Exception as e:
                frames.append(("err", round(time.time() - t0, 2), str(e)[:80]))
            t += step
        try: await nav
        except Exception: pass
        await ctx.close(); await browser.close()
    set_active(None); fcntl.flock(lock, fcntl.LOCK_UN)
    out = {"label": label, "variant": variant or "base", "seconds": seconds, "step": step,
           "loaded_at": next((f[1] for f in frames if f[0] == "load"), None),
           "frames": [{"t": f[1], "src": f[2]} for f in frames if f[0] == "frame"]}
    json.dump(out, open(os.path.join(ROOT, "results", f"film-{label}.json"), "w"))
    print(label, len(out["frames"]), "frames, load at", out["loaded_at"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("label"); ap.add_argument("--variant", default=None); ap.add_argument("--seconds", type=float, default=16); ap.add_argument("--step", type=float, default=0.5)
    a = ap.parse_args(); asyncio.run(run(a.label, a.variant, a.seconds, a.step))
