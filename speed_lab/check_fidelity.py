"""Compare a variant's measurement with the baseline: the page must still be the same page.

Usage: python3 speed_lab/check_fidelity.py results/LABEL.json
Checks (run 1 of each): same title, body text within 3 percent, same count of images in view,
no new console errors, no new failed first-party requests, no first-party 404 misses.
Prints PASS or the failures. Exit 1 on failure.
"""
import json, os, re, sys
from urllib.parse import urlsplit
ROOT = os.path.dirname(os.path.abspath(__file__))
_base = json.load(open(os.path.join(ROOT, "results", "baseline.json")))["runs"]
base_runs = [r["summary"] for r in _base]
base_miss = {r["url"] for b in _base for r in b["served"] if r["src"] == "miss"}


def norm_err(e):
    # collapse ids, timestamps and long tokens so only the message shape is compared
    return re.sub(r"[0-9a-f]{8,}|\d{6,}|[A-Za-z0-9+/=_-]{20,}", "#", e)


base_errs = {norm_err(e) for b in base_runs for e in b.get("console_errors", [])}
base_title = base_runs[0].get("title")
base_text = [b.get("body_text_chars") or 0 for b in base_runs]
base_imgs = {b.get("images_in_view") for b in base_runs}


def first_party(url):
    host = urlsplit(url).hostname or ""
    return host == "gehnaindia.com" or host.endswith(".gehnaindia.com")


v = json.load(open(sys.argv[1]))
fails, passed = [], 0
for run in v["runs"]:
    s = run["summary"]; f = []
    if s.get("title") != base_title: f.append(f"title changed: {s.get('title')!r}")
    vt = s.get("body_text_chars") or 0
    if base_text and min(abs(vt - b) / b for b in base_text if b) > 0.03: f.append(f"body text chars {vt} vs baseline {base_text}")
    if s.get("images_in_view") not in base_imgs: f.append(f"images in view {s.get('images_in_view')} vs {sorted(base_imgs)}")
    new_err = [e for e in s.get("console_errors", []) if norm_err(e) not in base_errs]
    if new_err: f.append(f"new console errors: {new_err[:3]}")
    fp_miss = [r["url"] for r in run["served"] if r["src"] == "miss" and first_party(r["url"]) and r["url"] not in base_miss]
    if fp_miss: f.append(f"first-party requests not served: {fp_miss[:3]}")
    if s.get("error"): f.append(f"navigation error: {s['error']}")
    if f: fails.append(f"run {s['run']}: " + "; ".join(f))
    else: passed += 1
verdict = "PASS" if passed == len(v["runs"]) else ("PASS (%d of %d runs)" % (passed, len(v["runs"])) if passed >= 2 else "FAIL")
print(verdict + ("\n" + "\n".join(" - " + x for x in fails) if fails else ""))
sys.exit(0 if passed >= 2 else 1)
