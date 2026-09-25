"""Arm B companion to speed_lab/check_fidelity.py. Runs the same checks on every run (not only run 1),
with one change: console errors are normalized before comparison. The replay server does not read POST
bodies, so a beacon body left on a keep-alive socket is parsed as the next request line and answered 501
"Unsupported method ('<beacon body>')". The body holds a timestamp and a random page-load id, so the
string differs on every load, including repeat loads of the unmodified baseline. Normalizing keeps the
error class ("501 Unsupported method") and drops the random payload; any other new error still fails.
Usage: python3 speed_lab/arms/arm-b/check_norm.py speed_lab/results/LABEL.json"""
import json, os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
B = json.load(open(os.path.join(ROOT, "results", "baseline.json")))["runs"]


def norm(e):
    e = re.sub(r"Unsupported method \(.*", "Unsupported method (<beacon payload>)", e)
    return e


base_err = {norm(e) for r in B for e in r["summary"]["console_errors"]}
base = B[0]["summary"]
base_miss = {r["url"] for r in B[0]["served"] if r["src"] == "miss"}


def check(run):
    s = run["summary"]; f = []
    if s.get("title") != base.get("title"): f.append(f"title changed: {s.get('title')!r}")
    bt, vt = base.get("body_text_chars") or 0, s.get("body_text_chars") or 0
    if bt and abs(vt - bt) / bt > 0.03: f.append(f"body text chars {vt} vs baseline {bt}")
    if s.get("images_in_view") != base.get("images_in_view"): f.append(f"images in view {s.get('images_in_view')} vs {base.get('images_in_view')}")
    new = sorted({norm(e) for e in s.get("console_errors", [])} - base_err)
    if new: f.append(f"new console errors: {new[:3]}")
    fp = [r["url"] for r in run["served"] if r["src"] == "miss" and "gehnaindia.com" in r["url"] and r["url"] not in base_miss]
    if fp: f.append(f"first-party requests not served: {fp[:3]}")
    if s.get("error"): f.append(f"navigation error: {s['error']}")
    return f


if __name__ == "__main__":
    v = json.load(open(sys.argv[1]))
    allok = True
    for i, run in enumerate(v["runs"]):
        f = check(run); allok &= not f
        print(f"run {i+1}: " + ("PASS" if not f else "FAIL " + "; ".join(f)))
    print("NORMALIZED", "PASS" if allok else "FAIL")
    sys.exit(0 if allok else 1)
