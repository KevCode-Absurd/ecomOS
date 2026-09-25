"""Record a filmstrip of the page loading through the replay server on the throttled mobile profile.

Usage: python3 speed_lab/filmstrip.py LABEL [--variant NAME] [--seconds 16]
Writes results/film-LABEL.json: frames as small JPEG data URIs with their time in seconds, plus the
moment the load event fired. Same browser profile as measure.py (Pixel 5, 2.75x, slow 4G, 4x CPU).

Frames come from a CDP screencast, which streams a picture whenever the page repaints and never
blocks the page or the navigation. Identical repaints are dropped and frames closer than MIN_GAP
seconds to the last kept one are skipped. Illustrative: the harness numbers are the record.
"""
import argparse, asyncio, base64, fcntl, hashlib, io, json, os, sys, time
from PIL import Image
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lab import ROOT, set_active

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
UA = "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
W, H = 260, 520          # stored frame size (CSS px 393x851 scaled to 260 wide, top 520 kept)
MIN_GAP = 0.2            # seconds between kept frames


def shrink(jpeg_b64):
    im = Image.open(io.BytesIO(base64.b64decode(jpeg_b64))).convert("RGB")
    im = im.resize((W, max(H, int(im.height * W / im.width))), Image.LANCZOS).crop((0, 0, W, H))
    b = io.BytesIO(); im.save(b, "JPEG", quality=62, optimize=True)
    return b.getvalue()


async def run(label, variant, seconds, url="https://www.gehnaindia.com/"):
    lock = open(os.path.join(ROOT, ".measure.lock"), "w"); fcntl.flock(lock, fcntl.LOCK_EX)
    set_active(variant)
    open(os.path.join(ROOT, "ACTIVE_RUN"), "w").write(f"film-{label}")
    raw, loaded_at = [], None
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME, headless=True, args=["--no-sandbox", "--host-resolver-rules=MAP * 127.0.0.1", "--ignore-certificate-errors", "--no-proxy-server"])
        ctx = await browser.new_context(user_agent=UA, viewport={"width": 393, "height": 851}, device_scale_factor=2.75, is_mobile=True, has_touch=True, ignore_https_errors=True)
        page = await ctx.new_page()
        cdp = await ctx.new_cdp_session(page)
        await cdp.send("Network.enable")
        await cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": 150, "downloadThroughput": 1.6 * 1024 * 1024 / 8, "uploadThroughput": 750 * 1024 / 8})
        await cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
        t0 = time.time()

        def on_frame(ev):
            raw.append((time.time() - t0, ev["data"]))
            asyncio.ensure_future(cdp.send("Page.screencastFrameAck", {"sessionId": ev["sessionId"]}))
        cdp.on("Page.screencastFrame", on_frame)
        await cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 70, "maxWidth": 2 * W, "maxHeight": 2 * int(851 * W / 393) + 4, "everyNthFrame": 1})
        loads = []
        page.on("load", lambda: loads.append(time.time() - t0))
        nav = asyncio.ensure_future(page.goto(url, wait_until="load", timeout=int(seconds * 1000) + 60000))
        await asyncio.sleep(seconds)
        try: await cdp.send("Page.stopScreencast")
        except Exception: pass
        try: await nav
        except Exception: pass
        loaded_at = loads[0] if loads else None
        await ctx.close(); await browser.close()
    set_active(None); fcntl.flock(lock, fcntl.LOCK_UN)

    frames, last_t, last_hash = [], -10.0, None
    for t, data in raw:
        if t > seconds: break
        h = hashlib.sha1(data.encode()).hexdigest()
        if h == last_hash: continue
        if t - last_t < MIN_GAP: continue
        small = shrink(data)
        frames.append({"t": round(t, 2), "src": "data:image/jpeg;base64," + base64.b64encode(small).decode()})
        last_t, last_hash = t, h
    out = {"label": label, "variant": variant or "base", "seconds": seconds, "loaded_at": loaded_at, "frames": frames}
    json.dump(out, open(os.path.join(ROOT, "results", f"film-{label}.json"), "w"))
    print(label, len(raw), "screencast frames,", len(frames), "kept, load at", loaded_at)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("label"); ap.add_argument("--variant", default=None); ap.add_argument("--seconds", type=float, default=16)
    a = ap.parse_args(); asyncio.run(run(a.label, a.variant, a.seconds))
