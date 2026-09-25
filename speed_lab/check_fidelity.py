"""Compare a variant's measurement with the baseline: the page must still be the same page.

Usage: python3 speed_lab/check_fidelity.py results/LABEL.json
Checks (run 1 of each): same title, body text within 3 percent, same count of images in view,
no new console errors, no new failed first-party requests, no first-party 404 misses.
Prints PASS or the failures. Exit 1 on failure.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
_b = json.load(open(os.path.join(ROOT, "results", "baseline.json")))["runs"][0]
base = _b["summary"]
base_miss = {r["url"] for r in _b["served"] if r["src"] == "miss"}
v = json.load(open(sys.argv[1]))
s = v["runs"][0]["summary"]
fails = []
if s.get("title") != base.get("title"): fails.append(f"title changed: {s.get('title')!r}")
bt, vt = base.get("body_text_chars") or 0, s.get("body_text_chars") or 0
if bt and abs(vt - bt) / bt > 0.03: fails.append(f"body text chars {vt} vs baseline {bt}")
if s.get("images_in_view") != base.get("images_in_view"): fails.append(f"images in view {s.get('images_in_view')} vs {base.get('images_in_view')}")
new_err = [e for e in s.get("console_errors", []) if e not in base.get("console_errors", [])]
if new_err: fails.append(f"new console errors: {new_err[:3]}")
fp_miss = [r["url"] for r in v["runs"][0]["served"] if r["src"] == "miss" and "gehnaindia.com" in r["url"] and r["url"] not in base_miss]
if fp_miss: fails.append(f"first-party requests not served: {fp_miss[:3]}")
if s.get("error"): fails.append(f"navigation error: {s['error']}")
print("PASS" if not fails else "FAIL\n" + "\n".join(" - " + f for f in fails))
sys.exit(1 if fails else 0)
