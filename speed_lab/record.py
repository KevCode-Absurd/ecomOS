"""Record every response of one page load into speed_lab/store/.

Usage: python3 speed_lab/record.py https://www.gehnaindia.com/
Mobile UA, no throttling, waits for load plus 10 s of settling so lazy assets and pixels are captured.
"""
import asyncio, json, os, sys, time
from playwright.async_api import async_playwright
from lab import STORE, key, norm, save_index

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
UA = "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"


async def main(url):
    os.makedirs(STORE, exist_ok=True)
    idx, order = {}, []
    async with async_playwright() as p:
        proxy = {"server": os.environ["HTTPS_PROXY"]} if os.environ.get("HTTPS_PROXY") else None  # sandboxed sessions reach the web through a proxy
        browser = await p.chromium.launch(executable_path=CHROME, headless=True, args=["--no-sandbox"], proxy=proxy)
        ctx = await browser.new_context(user_agent=UA, viewport={"width": 393, "height": 851}, device_scale_factor=2.75, is_mobile=True, has_touch=True, ignore_https_errors=bool(proxy))
        page = await ctx.new_page()
        pending = []

        async def save(resp):
            try:
                u = norm(resp.url)
                k = key(u)
                if k in idx:
                    return
                headers = dict(resp.headers)
                body = b""
                try:
                    if resp.status not in (204, 301, 302, 303, 307, 308):
                        body = await resp.body()
                except Exception:
                    body = b""
                fn = k + ".bin" if body else None
                if fn:
                    open(os.path.join(STORE, fn), "wb").write(body)
                idx[k] = {"url": u, "status": resp.status, "headers": headers, "file": fn, "size": len(body), "type": resp.request.resource_type, "method": resp.request.method}
                order.append(u)
            except Exception as e:
                print("save error", str(e)[:120])

        page.on("response", lambda r: pending.append(asyncio.ensure_future(save(r))))
        t0 = time.time()
        await page.goto(url, wait_until="load", timeout=120000)
        await page.wait_for_timeout(10000)
        # scroll to trigger lazy assets, then back to top
        for y in (800, 1600, 2400, 3200, 4000):
            await page.evaluate(f"window.scrollTo(0,{y})")
            await page.wait_for_timeout(700)
        await page.evaluate("window.scrollTo(0,0)")
        await page.wait_for_timeout(3000)
        await asyncio.gather(*pending, return_exceptions=True)
        await ctx.close(); await browser.close()
    save_index(idx)
    json.dump(order, open(os.path.join(STORE, "order.json"), "w"), indent=0)
    tot = sum(e["size"] for e in idx.values())
    hosts = {}
    for e in idx.values():
        h = e["url"].split("/")[2]; hosts.setdefault(h, [0, 0]); hosts[h][0] += 1; hosts[h][1] += e["size"]
    print(f"recorded {len(idx)} responses, {tot/1024:.0f} KB decoded, {time.time()-t0:.0f}s")
    for h, (n, b) in sorted(hosts.items(), key=lambda x: -x[1][1]):
        print(f"  {h:45s} {n:4d} req {b/1024:8.0f} KB")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "https://www.gehnaindia.com/"))
