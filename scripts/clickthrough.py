#!/usr/bin/env python3
"""Click-through page: one screenshot per screen from the running app server, plus one line per screen on
what it now lets the founder do, written to app/review/clickthrough.html (self-contained, images inline).

Usage:
  python3 scripts/clickthrough.py --base http://127.0.0.1:8770 [--out app/review/clickthrough.html] [--only 05-brand-brain,00-today]

Needs the app server running and Playwright for node at /opt/node22/lib/node_modules/playwright with
Chromium at /opt/pw-browsers/chromium (never `playwright install`). The line per screen comes from the
screen's rank route (its top action and counts) and the last row of its FEATURES.md rounds table. No model call.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import html
import json
import re
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"
NODE_PW = "/opt/node22/lib/node_modules/playwright"
CHROMIUM = "/opt/pw-browsers/chromium"

SHOT_JS = r"""
const { chromium } = require(process.argv[2]);
(async () => {
  const jobs = JSON.parse(require('fs').readFileSync(process.argv[3], 'utf8'));
  const browser = await chromium.launch({ executablePath: process.argv[4], args: ['--no-sandbox'] });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  const out = [];
  for (const j of jobs) {
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', (e) => errors.push(String(e).slice(0, 200)));
    try {
      await page.goto(j.url, { waitUntil: 'networkidle', timeout: 45000 });
      await page.waitForTimeout(700);
      const h = await page.evaluate(() => document.documentElement.scrollHeight);
      const first = await page.evaluate(() => { const s = document.querySelector('.screen'); if (!s) return null; const kids = Array.from(s.children).filter((k) => !k.hidden && k.offsetHeight > 0); const f = kids.find((k) => !k.classList.contains('sample-badge') && !k.classList.contains('screen-head')); return f ? (f.querySelector('.plan') ? 'plan' : f.className || f.tagName) : null; });
      await page.screenshot({ path: j.out, type: 'jpeg', quality: 72, fullPage: false });
      out.push({ slug: j.slug, ok: true, height: h, first, errors });
    } catch (e) { out.push({ slug: j.slug, ok: false, error: String(e).slice(0, 200), errors }); }
    await page.close();
  }
  await browser.close();
  console.log(JSON.stringify(out));
})();
"""


def get(url: str, timeout: float = 30):
    with urllib.request.urlopen(url, timeout=timeout) as res:
        return json.loads(res.read().decode("utf-8"))


def last_round(slug: str) -> tuple[str, str]:
    p = APP / "screens" / slug / "FEATURES.md"
    if not p.is_file():
        return "", ""
    text = p.read_text(encoding="utf-8")
    m = re.search(r"^## Rounds\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        return "", ""
    rows = [ln for ln in m.group(1).splitlines() if ln.startswith("|") and not ln.startswith("|---") and not ln.startswith("| Round")]
    if not rows:
        return "", ""
    cells = [c.strip() for c in rows[-1].strip("|").split("|")]
    return (cells[0] if cells else ""), (cells[-1] if cells else "")


def line_for(slug: str, base: str, purpose: str) -> tuple[str, dict]:
    """One plain line: what the founder can do here now, from the rank route and the rounds table."""
    info = {"actions": None, "top": None, "source": None}
    try:
        r = get(f"{base}/api/{slug}/rank")
        acts = [a for a in r.get("actions", []) if a.get("status") != "unavailable"]
        conn = [a for a in r.get("actions", []) if a.get("status") == "unavailable"]
        info = {"actions": len(acts), "connect": len(conn), "top": acts[0] if acts else None, "source": r.get("source")}
    except Exception:  # noqa: BLE001
        pass
    rnd, note = last_round(slug)
    parts = []
    if info.get("top"):
        t = info["top"]
        parts.append(f"{info['actions']} ranked actions, top: {t['title']} ({t['owner'].replace('_', ' ')}).")
    elif info.get("actions") == 0:
        parts.append("No open action this window" + (f", {info.get('connect')} wait on a connector." if info.get("connect") else "."))
    else:
        parts.append("Rank route unavailable.")
    if info.get("source") == "screen":
        parts.append("The screen ranks its own actions.")
    if rnd:
        parts.append(f"Round {rnd}: {note}" if note else f"Round {rnd}.")
    return " ".join(parts), info


def build(base: str, out: Path, only: list[str] | None) -> Path:
    screens = get(f"{base}/api/screens")["screens"]
    brand = get(f"{base}/api/brand")
    if only:
        screens = [s for s in screens if s["slug"] in only]
    tmp = Path(tempfile.mkdtemp())
    jobs = [{"slug": s["slug"], "url": f"{base}/screens/{s['slug']}/", "out": str(tmp / (s["slug"] + ".jpg"))} for s in screens if s.get("built")]
    (tmp / "jobs.json").write_text(json.dumps(jobs), encoding="utf-8")
    (tmp / "shot.js").write_text(SHOT_JS, encoding="utf-8")
    res = subprocess.run(["node", str(tmp / "shot.js"), NODE_PW, str(tmp / "jobs.json"), CHROMIUM], capture_output=True, text=True, timeout=900)
    if res.returncode != 0:
        sys.stderr.write(res.stderr[-2000:])
        raise SystemExit("screenshots failed")
    shots = {r["slug"]: r for r in json.loads(res.stdout.strip().splitlines()[-1])}
    now = dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y %H:%M UTC")
    cards = []
    plan_first = 0
    for s in screens:
        slug = s["slug"]
        line, info = line_for(slug, base, s.get("purpose", "")) if s.get("built") else ("Not built yet.", {})
        sh = shots.get(slug, {})
        img = ""
        if sh.get("ok"):
            b = (tmp / (slug + ".jpg")).read_bytes()
            img = f'<img loading="lazy" alt="{html.escape(s["room"])} at 1280 wide" src="data:image/jpeg;base64,{base64.b64encode(b).decode()}">'
        pf = sh.get("first") == "plan"
        plan_first += 1 if pf else 0
        badge = '<span class="b good">plan first</span>' if pf else ('<span class="b">round 0 layout</span>' if s.get("built") else '<span class="b">not built</span>')
        errs = "".join(f'<li>{html.escape(e)}</li>' for e in (sh.get("errors") or [])[:3])
        cards.append(f"""
<section class="card" id="{slug}">
  <header><span class="n">{html.escape(slug[:2] if slug != 'setup' else '>')}</span><h2>{html.escape(s['room'])}</h2>{badge}<a class="open" href="{base}/screens/{slug}/">open</a></header>
  <p class="line">{html.escape(line)}</p>
  <p class="purpose">{html.escape(s.get('purpose', ''))}</p>
  {img or '<div class="noshot">no screenshot</div>'}
  {('<ul class="errs">' + errs + '</ul>') if errs else ''}
</section>""")
    built = sum(1 for s in screens if s.get("built"))
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ecomOS click-through</title>
<style>
:root{{color-scheme:light dark;--ink:#0b1220;--muted:#526075;--line:#e3e8ef;--bg:#f3f5f8;--card:#fff;--accent:#1f4fe0;--good:#0f7b5f;--good-soft:#dcf3ea}}
@media (prefers-color-scheme:dark){{:root{{--ink:#e9edf5;--muted:#a4afc3;--line:#212c42;--bg:#0b101a;--card:#121827;--accent:#7ea0ff;--good:#4fd1a5;--good-soft:#10302a}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 Inter,system-ui,sans-serif}}
.wrap{{max-width:1320px;margin:0 auto;padding:20px 16px 60px}}
h1{{font-size:22px;margin:0 0 4px;letter-spacing:-.02em}} .sub{{color:var(--muted);margin:0 0 16px}}
.toc{{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 18px}} .toc a{{font-size:12px;padding:3px 9px;border:1px solid var(--line);border-radius:999px;color:var(--muted);text-decoration:none;background:var(--card)}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:0 0 16px;break-inside:avoid}}
header{{display:flex;align-items:center;gap:10px;flex-wrap:wrap}} header h2{{font-size:16px;margin:0}} .n{{font-family:ui-monospace,monospace;font-size:11px;color:var(--muted);width:18px}}
.b{{font-size:11px;font-weight:600;padding:1px 8px;border-radius:999px;background:var(--line);color:var(--muted)}} .b.good{{background:var(--good-soft);color:var(--good)}}
.open{{margin-left:auto;font-size:12px;color:var(--accent)}}
.line{{font-size:14px;font-weight:600;margin:8px 0 2px}} .purpose{{color:var(--muted);font-size:12.5px;margin:0 0 10px}}
img{{width:100%;height:auto;border:1px solid var(--line);border-radius:10px;display:block}}
.noshot{{padding:30px;text-align:center;color:var(--muted);border:1px dashed var(--line);border-radius:10px}}
.errs{{font-size:11px;color:#c8262c;margin:8px 0 0;padding-left:18px}}
.note{{font-size:12px;color:var(--muted);border-left:3px solid var(--accent);padding:6px 10px;margin:0 0 16px}}
</style></head><body><div class="wrap">
<h1>ecomOS click-through</h1>
<p class="sub">{html.escape(brand.get('brand', ''))}, {'simulated data' if brand.get('fictional') else 'live data'}. {built} of {len(screens)} screens built, {plan_first} with the plan first. Shot at 1280 wide, {now}. One line per screen says what it lets the founder do now, from its rank route and its rounds table.</p>
<p class="note">Every number on these pages is simulated and labelled so on the page. Screens marked "plan first" meet section 1 of the depth contract; "round 0 layout" screens are queued for their manager.</p>
<nav class="toc">{''.join(f'<a href="#{s["slug"]}">{html.escape(s["room"])}</a>' for s in screens)}</nav>
{''.join(cards)}
</div></body></html>"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB), {built} built, {plan_first} plan first")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="http://127.0.0.1:8770")
    ap.add_argument("--out", default=str(APP / "review" / "clickthrough.html"))
    ap.add_argument("--only", default="")
    ns = ap.parse_args(argv)
    build(ns.base.rstrip("/"), Path(ns.out), [s for s in ns.only.split(",") if s] or None)


if __name__ == "__main__":
    main()
