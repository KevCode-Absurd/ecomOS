"""Same checks as speed_lab/check_fidelity.py, with one change: console error text is compared after
replacing digit runs and UUIDs with placeholders. Reason: the replay server does not read POST bodies,
so a beacon body (Cloudflare RUM, with a timestamp and page-load UUID) is parsed as the next request line
and logged as a 501 error whose text differs on every load. check_fidelity.py flags those as new errors
even for an unchanged page. Second change: a first-party miss is judged by host (ends with gehnaindia.com,
the same rule measure.py uses for first-party bytes), not by substring, because third-party beacons carry
dl=www.gehnaindia.com in their query string. This script is a supplement, not a replacement; results.md reports both.
Usage: python3 speed_lab/arms/arm-a/tools/fidelity_norm.py speed_lab/results/LABEL.json [--run N]
"""
import json, os, re, sys
from urllib.parse import urlsplit
LAB = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def norm(e):
    # A 501 "Unsupported method ('<text>')" is always the replay server reading a leftover POST body as the
    # next request line; the text is the beacon payload and changes on every load. Collapse it to one token.
    e = re.sub(r"Unsupported method \(.*", "Unsupported method (<replayed POST body>)", e)
    return re.sub(r"\d+", "#", UUID.sub("<uuid>", e))


def check(path, run=0):
    _b = json.load(open(os.path.join(LAB, "results", "baseline.json")))["runs"][0]
    base = _b["summary"]
    base_miss = {r["url"] for r in _b["served"] if r["src"] == "miss"}
    v = json.load(open(path))
    s = v["runs"][run]["summary"]
    fails = []
    if s.get("title") != base.get("title"): fails.append(f"title changed: {s.get('title')!r}")
    bt, vt = base.get("body_text_chars") or 0, s.get("body_text_chars") or 0
    if bt and abs(vt - bt) / bt > 0.03: fails.append(f"body text chars {vt} vs baseline {bt}")
    if s.get("images_in_view") != base.get("images_in_view"): fails.append(f"images in view {s.get('images_in_view')} vs {base.get('images_in_view')}")
    bn = {norm(e) for e in base.get("console_errors", [])}
    new_err = [e for e in s.get("console_errors", []) if norm(e) not in bn]
    if new_err: fails.append(f"new console errors: {new_err[:3]}")
    fp_miss = [r["url"] for r in v["runs"][run]["served"] if r["src"] == "miss" and (urlsplit(r["url"]).hostname or "").endswith("gehnaindia.com") and r["url"] not in base_miss]
    if fp_miss: fails.append(f"first-party requests not served: {fp_miss[:3]}")
    if s.get("error"): fails.append(f"navigation error: {s['error']}")
    return fails


if __name__ == "__main__":
    path = sys.argv[1]
    runs = [int(sys.argv[3]) - 1] if "--run" in sys.argv else [0]
    if "--all" in sys.argv:
        runs = list(range(len(json.load(open(path))["runs"])))
    bad = False
    for r in runs:
        f = check(path, r)
        print(f"run {r+1}:", "PASS (normalized)" if not f else "FAIL\n" + "\n".join(" - " + x for x in f))
        bad |= bool(f)
    sys.exit(1 if bad else 0)
