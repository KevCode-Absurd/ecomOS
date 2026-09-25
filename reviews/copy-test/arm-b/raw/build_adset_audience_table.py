"""Spend and purchase value by ad set audience type, read from ad set names.
Run from the repo root: python3 reviews/copy-test/arm-b/raw/build_adset_audience_table.py
Same null rule as build_audit_tables.py: null purchases are 'not reported', not 0.
"""
import csv, json, os
from collections import defaultdict
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", ".."))
g = json.load(open(os.path.join(REPO, "data/meta-gallery/cache/gallery.json"), encoding="utf-8"))
ads, daily = g["ads"], g["daily"]
max_day = max(r[0] for rows in daily.values() for r in rows)
WIN = {"12m": (0, max_day), "90d": (max_day - 89, max_day)}

def aud(name):
    n = name.lower()
    if "atc" in n or "wv" in n or "cart" in n: return "Site visitors and cart (BOF)"
    if "engager" in n or "catalogue visitor" in n: return "Engagers and catalogue visitors (MOF)"
    if "mof" in n or "bof" in n: return "MOF + BOF audiences inside TOF campaigns"
    if "lookalike" in n or "lal" in n: return "Lookalike"
    if "interest" in n: return "Interest stack"
    if "broad" in n or "advantage" in n or "andromeda" in n or "consolidated" in n: return "Broad"
    return "Other or unnamed"

out = {}
for w, (lo, hi) in WIN.items():
    acc = defaultdict(lambda: {"ad_sets": set(), "ads": 0, "spend": 0.0, "purchases": 0.0, "value": 0.0, "rep": False})
    for aid, a in ads.items():
        rows = [r for r in daily.get(aid, []) if lo <= r[0] <= hi]
        s = sum(r[1] for r in rows)
        if s <= 0: continue
        k = aud(a["adset_name"])
        x = acc[k]; x["ad_sets"].add(a["adset_id"]); x["ads"] += 1; x["spend"] += s
        for r in rows:
            if r[2] is not None: x["purchases"] += r[2]; x["rep"] = True
            if r[3] is not None: x["value"] += r[3]; x["rep"] = True
    tot = sum(x["spend"] for x in acc.values())
    rows_out = []
    for k, x in acc.items():
        rows_out.append({"audience_type": k, "ad_sets": len(x["ad_sets"]), "ads": x["ads"], "spend": round(x["spend"], 2),
                         "spend_share_pct": round(100 * x["spend"] / tot, 2),
                         "purchases": x["purchases"] if x["rep"] else None,
                         "value": round(x["value"], 2) if x["rep"] else None,
                         "roas": round(x["value"] / x["spend"], 3) if x["rep"] else None,
                         "cpa": round(x["spend"] / x["purchases"], 2) if x["purchases"] else None})
    rows_out.sort(key=lambda r: -r["spend"])
    out[w] = rows_out
    with open(os.path.join(ROOT, f"by_adset_audience_{w}.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows_out[0].keys())); wr.writeheader()
        for r in rows_out: wr.writerow({k: ("unavailable" if v is None else v) for k, v in r.items()})
# ad set name inventory
names = defaultdict(float)
for aid, a in ads.items():
    names[a["adset_name"]] += sum(r[1] for r in daily.get(aid, []))
with open(os.path.join(ROOT, "adset_names_12m.csv"), "w", newline="", encoding="utf-8") as f:
    wr = csv.writer(f); wr.writerow(["adset_name", "audience_type", "spend_12m"])
    for n, s in sorted(names.items(), key=lambda kv: -kv[1]): wr.writerow([n, aud(n), round(s, 2)])
print(json.dumps(out, indent=1))
