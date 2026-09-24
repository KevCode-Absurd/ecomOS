"""Build every audit table from data/meta-gallery/cache/gallery.json.

Run from the repo root: python3 reviews/copy-test/blind/raw-1/build_tables.py
Writes CSV and JSON files next to this script. All arithmetic is done here.

Rules used
- Currency INR. Day 0 = 2025-09-23 (meta.window.since). Day 366 = 2026-09-24 (partial day).
- 12 months = day 0 to 366 (whole window). 90 days = day 276 to 365 = 2026-06-26 to 2026-09-23 (90 full days).
- null in daily rows means unavailable, not 0. Sums skip nulls; the count of null cells is kept.
- Period ROAS = total purchase value / total spend. CPA = spend / purchases. Ratios are None (unavailable)
  when the denominator is 0.
- Age, gender and platform rows come from `monthly` (a separate Meta breakdown pull) and are never added to daily totals.
"""
import csv
import json
import os
import re
import statistics
from collections import defaultdict
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SRC = os.path.join(ROOT, "data", "meta-gallery", "cache", "gallery.json")

g = json.load(open(SRC, encoding="utf-8"))
ads, daily, monthly = g["ads"], g["daily"], g["monthly"]
DAY0 = date.fromisoformat(g["meta"]["window"]["since"])
LAST_FULL_DAY = 365            # 2026-09-23
D90_START = LAST_FULL_DAY - 89  # 276 -> 2026-06-26
WINDOWS = {"12m": (0, 366), "90d": (D90_START, LAST_FULL_DAY)}


def d(i):
    return (DAY0 + timedelta(days=i)).isoformat()


def ratio(a, b):
    return round(a / b, 4) if b else None


def new_acc():
    return {"spend": 0.0, "purchases": 0.0, "purchase_value": 0.0, "impressions": 0.0, "clicks": 0.0,
            "days_with_spend": 0, "null_purchase_cells": 0, "ads": set()}


def add_row(acc, aid, r):
    _, spend, pur, val, imp, clk = r
    if spend:
        acc["spend"] += spend
        acc["days_with_spend"] += 1
        acc["ads"].add(aid)
    if pur is None:
        acc["null_purchase_cells"] += 1
    else:
        acc["purchases"] += pur
    if val is not None:
        acc["purchase_value"] += val
    if imp:
        acc["impressions"] += imp
    if clk:
        acc["clicks"] += clk


def finish(acc, total_spend=None):
    out = {
        "ads": len(acc["ads"]),
        "spend": round(acc["spend"], 2),
        "purchases": acc["purchases"],
        "purchase_value": round(acc["purchase_value"], 2),
        "impressions": int(acc["impressions"]),
        "clicks": int(acc["clicks"]),
        "roas": ratio(acc["purchase_value"], acc["spend"]),
        "cpa": round(acc["spend"] / acc["purchases"], 2) if acc["purchases"] else None,
        "aov": round(acc["purchase_value"] / acc["purchases"], 2) if acc["purchases"] else None,
        "ctr_pct": round(100 * acc["clicks"] / acc["impressions"], 3) if acc["impressions"] else None,
        "cpm": round(1000 * acc["spend"] / acc["impressions"], 2) if acc["impressions"] else None,
        "cpc": round(acc["spend"] / acc["clicks"], 2) if acc["clicks"] else None,
        "null_purchase_cells": acc["null_purchase_cells"],
    }
    if total_spend:
        out["spend_share_pct"] = round(100 * acc["spend"] / total_spend, 2)
    return out


def funnel(ad):
    n = ad["campaign_name"].upper()
    if "BOF" in n:
        return "BOF (cart and 180-day retargeting)"
    if "MOF" in n and "TOF" not in n:
        return "MOF (engagers and catalogue visitors)"
    if "MOF" in n:
        return "TOF + MOF (review ads)"
    if "EVENT" in n or "STORE VISIT" in n:
        return "Store or event"
    return "TOF (prospecting, combo or broad audiences)"


def theme(ad):
    n = ad["campaign_name"].lower()
    if any(k in n for k in ["bfcm", "eoss", "sale", "deal of the day", "countdown", "hours"]):
        return "Sale or countdown"
    if any(k in n for k in ["festive", "navratri", "karwa", "akshaya", "valentine", "rakhi"]):
        return "Festival or occasion"
    if "catalogue" in n:
        return "Catalogue"
    return "Evergreen"


def write_csv(name, rows, fields):
    with open(os.path.join(HERE, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k) for k in fields})


def write_json(name, obj):
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


# ---------- per-ad totals per window ----------
per_ad = {w: {} for w in WINDOWS}
for aid, rows in daily.items():
    for w, (lo, hi) in WINDOWS.items():
        acc = new_acc()
        for r in rows:
            if lo <= r[0] <= hi:
                add_row(acc, aid, r)
        per_ad[w][aid] = acc

totals = {}
for w in WINDOWS:
    acc = new_acc()
    for aid, a in per_ad[w].items():
        for k in ("spend", "purchases", "purchase_value", "impressions", "clicks", "null_purchase_cells", "days_with_spend"):
            acc[k] += a[k]
        acc["ads"] |= a["ads"]
    totals[w] = finish(acc)
    totals[w]["window"] = [d(WINDOWS[w][0]), d(WINDOWS[w][1])]
totals["note"] = ("12m is the whole capture window incl. the partial day 2026-09-24. 90d is 90 full days ending 2026-09-23. "
                  "account_spend_check in gallery.json says Meta reports " + str(g["meta"]["account_spend_check"]["account_total_spend"]) +
                  " for the window; the daily rows only cover ads captured in the gallery (up to 30 per view), so the gap is uncaptured ads.")
totals["capture_gap_12m"] = round(g["meta"]["account_spend_check"]["account_total_spend"] - totals["12m"]["spend"], 2)
totals["capture_share_pct"] = round(100 * totals["12m"]["spend"] / g["meta"]["account_spend_check"]["account_total_spend"], 2)

# ---------- daily account totals and monthly spend ----------
day_acc = defaultdict(new_acc)
for aid, rows in daily.items():
    for r in rows:
        add_row(day_acc[r[0]], aid, r)
daily_rows = []
for i in sorted(day_acc):
    x = finish(day_acc[i])
    x.update({"day_index": i, "date": d(i)})
    daily_rows.append(x)
write_csv("daily_account.csv", daily_rows, ["day_index", "date", "ads", "spend", "purchases", "purchase_value", "roas", "impressions", "clicks", "ctr_pct", "cpm"])

month_acc = defaultdict(new_acc)
for aid, rows in daily.items():
    for r in rows:
        add_row(month_acc[d(r[0])[:7]], aid, r)
month_rows = []
for m in sorted(month_acc):
    x = finish(month_acc[m])
    x["month"] = m
    x["days_in_data"] = len({r["date"] for r in daily_rows if r["date"].startswith(m)})
    month_rows.append(x)
write_csv("monthly_account.csv", month_rows, ["month", "days_in_data", "ads", "spend", "purchases", "purchase_value", "roas", "cpa", "aov", "impressions", "clicks", "ctr_pct", "cpm"])

# current monthly spend: mean of the last 3 full months (Jun, Jul, Aug 2026) and Sep run-rate
full = {r["month"]: r for r in month_rows}
last3 = [full[m]["spend"] for m in ("2026-06", "2026-07", "2026-08")]
sep = full["2026-09"]
sep_days = 23  # 1-23 Sep are full days
current = {
    "last_3_full_months": {m: full[m]["spend"] for m in ("2026-06", "2026-07", "2026-08")},
    "mean_last_3_full_months": round(statistics.mean(last3), 2),
    "sep_2026_1_to_23_spend": sep["spend"],
    "sep_2026_daily_run_rate": round(sep["spend"] / sep_days, 2),
    "sep_2026_projected_30_days": round(sep["spend"] / sep_days * 30, 2),
    "last_90d_spend": totals["90d"]["spend"],
    "last_90d_per_30_days": round(totals["90d"]["spend"] / 3, 2),
    "chosen_current_monthly_spend": round(totals["90d"]["spend"] / 3, 2),
    "why": "Mean of the last 90 days per 30 days. It smooths the August sale peak and the quieter September.",
}
totals["current_monthly_spend"] = current
write_json("account_totals.json", totals)


# ---------- group tables ----------
def group_table(w, keyfn, label):
    acc = defaultdict(new_acc)
    for aid, a in per_ad[w].items():
        if a["spend"] <= 0:
            continue
        k = keyfn(ads[aid])
        for f in ("spend", "purchases", "purchase_value", "impressions", "clicks", "null_purchase_cells", "days_with_spend"):
            acc[k][f] += a[f]
        acc[k]["ads"].add(aid)
    tot = sum(v["spend"] for v in acc.values())
    rows = []
    for k, v in acc.items():
        x = finish(v, tot)
        x[label] = k
        x["value_share_pct"] = round(100 * v["purchase_value"] / sum(z["purchase_value"] for z in acc.values()), 2) if sum(z["purchase_value"] for z in acc.values()) else None
        rows.append(x)
    rows.sort(key=lambda r: -r["spend"])
    return rows


FIELDS = lambda label: [label, "ads", "spend", "spend_share_pct", "purchases", "purchase_value", "value_share_pct", "roas", "cpa", "aov", "ctr_pct", "cpm", "null_purchase_cells"]
groups = {
    "angle": lambda a: a["tags"]["angle"]["label"],
    "hook": lambda a: a["tags"]["hook"]["label"],
    "product": lambda a: a["tags"]["product"]["label"],
    "format": lambda a: a["creative"]["type_label"],
    "funnel": funnel,
    "theme": theme,
    "campaign": lambda a: a["campaign_name"],
    "adset": lambda a: a["adset_name"],
    "status": lambda a: a["effective_status"],
}
for gname, fn in groups.items():
    for w in WINDOWS:
        write_csv(f"by_{gname}_{w}.csv", group_table(w, fn, gname), FIELDS(gname))

# angle x product cross table (12m and 90d)
for w in WINDOWS:
    rows = group_table(w, lambda a: a["tags"]["angle"]["label"] + " | " + a["tags"]["product"]["label"], "angle_x_product")
    write_csv(f"by_angle_x_product_{w}.csv", rows, FIELDS("angle_x_product"))

# ---------- ad-level table and top/bottom lists ----------
def ad_row(aid, w):
    a = ads[aid]
    x = finish(per_ad[w][aid])
    c = a["creative"]
    x.update({
        "ad_id": aid, "ad_name": a["name"], "status": a["effective_status"], "campaign": a["campaign_name"],
        "adset": a["adset_name"], "funnel": funnel(a), "theme": theme(a), "format": c["type_label"],
        "angle": a["tags"]["angle"]["label"], "hook": a["tags"]["hook"]["label"], "product": a["tags"]["product"]["label"],
        "headline": c.get("headline") or c.get("title"), "primary_text_first_line": (c.get("primary_text") or "").strip().split("\n")[0][:160],
        "days_with_spend": per_ad[w][aid]["days_with_spend"], "dynamic_creative": a["is_dynamic_creative"],
    })
    return x


AD_FIELDS = ["ad_id", "ad_name", "status", "campaign", "adset", "funnel", "theme", "format", "angle", "hook", "product", "spend", "purchases", "purchase_value", "roas", "cpa", "aov", "ctr_pct", "cpm", "days_with_spend", "dynamic_creative", "headline", "primary_text_first_line"]
for w in WINDOWS:
    rows = [ad_row(aid, w) for aid in ads if per_ad[w][aid]["spend"] > 0]
    rows.sort(key=lambda r: -r["spend"])
    write_csv(f"ads_{w}.csv", rows, AD_FIELDS)

# spend floor: 3 x the 12-month account CPA, rounded to the nearest 5,000. At that spend an average ad
# has bought about 3 purchases, so a zero is a signal rather than noise.
cpa12 = totals["12m"]["cpa"]
FLOOR_12M = int(round(3 * cpa12 / 5000) * 5000)
cpa90 = totals["90d"]["cpa"]
FLOOR_90D = int(round(3 * cpa90 / 5000) * 5000)
floors = {"12m": FLOOR_12M, "90d": FLOOR_90D,
          "rule": "3 x period account CPA rounded to the nearest 5,000 rupees", "cpa_12m": cpa12, "cpa_90d": cpa90}
for w, fl in (("12m", FLOOR_12M), ("90d", FLOOR_90D)):
    rows = [ad_row(aid, w) for aid in ads if per_ad[w][aid]["spend"] >= fl]
    rows = [r for r in rows if r["roas"] is not None]
    rows.sort(key=lambda r: -r["roas"])
    floors[f"ads_above_floor_{w}"] = len(rows)
    write_csv(f"top10_roas_{w}.csv", rows[:10], AD_FIELDS)
    write_csv(f"bottom10_roas_{w}.csv", list(reversed(rows[-10:])), AD_FIELDS)
    floors[f"median_roas_above_floor_{w}"] = round(statistics.median([r["roas"] for r in rows]), 3) if rows else None
    floors[f"p25_roas_above_floor_{w}"] = round(statistics.quantiles([r["roas"] for r in rows], n=4)[0], 3) if len(rows) > 3 else None
    floors[f"p75_roas_above_floor_{w}"] = round(statistics.quantiles([r["roas"] for r in rows], n=4)[2], 3) if len(rows) > 3 else None
write_json("spend_floor.json", floors)

# ---------- copy inventory ----------
MATHBOLD = {c: chr(ord("A") + (ord(c) - 0x1D5D4)) for c in map(chr, range(0x1D5D4, 0x1D5D4 + 26))}
MATHBOLD.update({c: chr(ord("a") + (ord(c) - 0x1D5EE)) for c in map(chr, range(0x1D5EE, 0x1D5EE + 26))})


def norm(t):
    t = "".join(MATHBOLD.get(ch, ch) for ch in (t or ""))
    return re.sub(r"\s+", " ", t).strip().lower()


def text_table(field, w, minlen=1):
    acc = defaultdict(lambda: {"acc": new_acc(), "sample": None, "ad_ids": []})
    for aid, a in per_ad[w].items():
        if a["spend"] <= 0:
            continue
        c = ads[aid]["creative"]
        raw = c.get(field) if field != "headline" else (c.get("headline") or c.get("title"))
        if field == "cards":
            raw = " || ".join((x.get("title") or "") + " / " + (x.get("body") or "") for x in (c.get("cards") or []))
        key = norm(raw)
        if len(key) < minlen:
            key = "(no text)"
        e = acc[key]
        for f in ("spend", "purchases", "purchase_value", "impressions", "clicks", "null_purchase_cells", "days_with_spend"):
            e["acc"][f] += a[f]
        e["acc"]["ads"].add(aid)
        e["sample"] = e["sample"] or ("".join(MATHBOLD.get(ch, ch) for ch in (raw or "")).strip())
        e["ad_ids"].append(aid)
    tot = sum(v["acc"]["spend"] for v in acc.values())
    rows = []
    for k, v in acc.items():
        x = finish(v["acc"], tot)
        x["text"] = v["sample"][:900]
        x["chars"] = len(v["sample"])
        x["ad_ids"] = ";".join(v["ad_ids"][:12])
        rows.append(x)
    rows.sort(key=lambda r: -r["spend"])
    return rows


TXT_FIELDS = ["text", "chars", "ads", "spend", "spend_share_pct", "purchases", "purchase_value", "roas", "cpa", "ctr_pct", "ad_ids"]
for w in WINDOWS:
    write_csv(f"primary_text_{w}.csv", text_table("primary_text", w), TXT_FIELDS)
    write_csv(f"headline_{w}.csv", text_table("headline", w), TXT_FIELDS)
    write_csv(f"description_{w}.csv", text_table("description", w), TXT_FIELDS)

# ---------- claims scan ----------
CLAIMS = [
    ("BIS Hallmarked", r"\bbis\b|hallmark", "approved", "home page, FAQ, product FAQ"),
    ("18K gold", r"\b18\s?k\b|18kt|18 karat", "approved", "collection filters and product pages"),
    ("14K gold", r"\b14\s?k\b|14kt", "approved (some chains)", "chains collection filter, pearl earrings karat option"),
    ("22K gold", r"\b22\s?k\b|22kt", "not on approved list", "collection filters show 22K items"),
    ("Natural gemstones", r"natural|real gem|real stone|genuine", "approved", "FAQ: all gemstones are natural"),
    ("Handcrafted / handmade", r"hand\s?crafted|hand\s?made|artisan|karigar", "approved", "FAQ: most jewellery hand-made in Chennai workshop"),
    ("4.8 Google rating", r"4\.8", "approved", "home page: 4.8 Google rating"),
    ("10,000+ customers", r"10,?000\+?|10k\+?", "approved", "home page: 10,000+ happy customers"),
    ("5,000+ customers (old number)", r"5,?000\+?", "not on approved list (superseded by 10,000+)", "not on site"),
    ("30,000+ orders", r"30,?000\+?", "not on approved list", "home page banner: 30,000+ orders delivered"),
    ("Free shipping", r"free ship|free deliver", "approved", "shipping page: free shipping in India"),
    ("7-day returns", r"7[- ]?days?|seven day", "approved", "shipping page and product FAQ"),
    ("20+ years", r"20\+? ?years|two decades|2 decades", "approved", "home page: 20+ years"),
    ("Lifetime exchange", r"lifetime exchange|life-?time exchange", "not on approved list", "shipping page: limited lifetime exchange policy"),
    ("Lifetime repair / warranty", r"lifetime repair|warranty|1[- ]year", "not on approved list", "FAQ: 1-year warranty; product FAQ: lifetime repair"),
    ("Free ring sizer / resizing", r"ring sizer|resiz|re-siz", "not on approved list", "ring product FAQ: free ring sizer and free resizing"),
    ("EMI / COD", r"\bemi\b|cash on delivery|\bcod\b|installment|instalment", "not on approved list", "FAQ: COD accepted, EMI plan; product pages show EMI table"),
    ("Certified gemstones (lab)", r"certif|lab[- ]tested|gemological", "not on approved list", "product FAQ: navratna stones certified by third-party lab"),
    ("Lab-grown diamonds", r"lab[- ]?grown", "conditional (only if product has them)", "no lab-grown filter seen on collection pages read"),
    ("Diamonds", r"diamond", "conditional (only if product has them)", "collection filter: Diamond jewellery type exists"),
    ("Lightweight", r"light\s?weight|lightweight|light on", "not on approved list", "product FAQ: lightweight yet durable"),
    ("Discount or % off", r"\d+\s?%|per ?cent off|flat \d|discount|% off", "offer (only while running)", "site shows 0% special price on pages read"),
    ("Sale / offer words", r"\bsale\b|offer|deal|bfcm|eoss|coupon|code", "offer (only while running)", "home: Sales Collections tile"),
    ("Urgency / countdown", r"hours left|hours to go|ends|last day|last chance|hurry|limited", "offer (only while running)", "none on site"),
    ("Rupee price in copy", r"₹|rs\.?\s?\d|inr", "price (confirm live)", "product pages show live prices"),
    ("Made to order / delivery time", r"ready to ship|ships in|deliver(y|ed) in|\d+[- ]?days? deliver", "not on approved list", "FAQ: 2-3 days in stock, 10-14 days made to order"),
    ("Chennai / store", r"chennai|store|showroom|boutique", "not on approved list", "home and FAQ: flagship store Harrington Road, Chennai"),
]
claim_rows = []
for w in WINDOWS:
    tot = sum(a["spend"] for a in per_ad[w].values())
    for label, pat, status, site in CLAIMS:
        rx = re.compile(pat, re.I)
        acc = new_acc()
        n_ads = 0
        for aid, a in per_ad[w].items():
            if a["spend"] <= 0:
                continue
            c = ads[aid]["creative"]
            blob = norm(" ".join([c.get("primary_text") or "", c.get("headline") or c.get("title") or "", c.get("description") or "",
                                  " ".join((x.get("title") or "") + " " + (x.get("body") or "") for x in (c.get("cards") or []))]))
            if rx.search(blob):
                n_ads += 1
                for f in ("spend", "purchases", "purchase_value", "impressions", "clicks", "null_purchase_cells", "days_with_spend"):
                    acc[f] += a[f]
                acc["ads"].add(aid)
        x = finish(acc, tot)
        x.update({"window": w, "claim": label, "status": status, "site_evidence": site, "ads_using": n_ads})
        claim_rows.append(x)
write_csv("claims_scan.csv", claim_rows, ["window", "claim", "status", "site_evidence", "ads_using", "spend", "spend_share_pct", "purchases", "purchase_value", "roas"])

# ---------- audience breakdowns (separate from totals) ----------
def bucket_in_90d(start, end):
    # a monthly bucket counts as "90d" when it starts on or after 2026-07-01 (Jul, Aug, Sep buckets)
    return start >= "2026-07-01"


aud = {}
for bd, per in monthly.items():
    for w in ("12m", "last_3_buckets"):
        acc = defaultdict(new_acc)
        for aid, rows in per.items():
            for r in rows:
                start, end, seg, spend, pur, val = r
                if w == "last_3_buckets" and not bucket_in_90d(start, end):
                    continue
                add_row(acc[seg], aid, [0, spend, pur, val, None, None])
        tot = sum(v["spend"] for v in acc.values())
        rows = []
        for seg, v in acc.items():
            x = finish(v, tot)
            x["segment"] = seg
            rows.append(x)
        rows.sort(key=lambda r: -r["spend"])
        aud[f"{bd}_{w}"] = rows
aud["note"] = ("Breakdown rows come from the monthly age, gender and publisher_platform pulls. They cover only the ads in each monthly top-30 view, "
               "so their totals differ from daily totals and must not be added to them. last_3_buckets = Jul, Aug and 1-24 Sep 2026.")
write_json("audience_breakdowns.json", aud)

# ---------- active ads (candidate controls) ----------
rows = [ad_row(aid, "90d") for aid in ads if ads[aid]["effective_status"] == "ACTIVE"]
rows.sort(key=lambda r: -r["spend"])
write_csv("active_ads_90d.csv", rows, AD_FIELDS)

# ---------- baselines for the test plan ----------
def pct(vals, q):
    vals = sorted(vals)
    if not vals:
        return None
    k = (len(vals) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(vals) - 1)
    return round(vals[lo] + (vals[hi] - vals[lo]) * (k - lo), 3)


ad90 = [ad_row(aid, "90d") for aid in ads if per_ad["90d"][aid]["spend"] >= FLOOR_90D]
tof90 = [r for r in ad90 if r["funnel"].startswith("TOF")]
ret90 = [r for r in ad90 if r["funnel"].startswith(("BOF", "MOF"))]
by_funnel_90 = {r["funnel"]: r for r in group_table("90d", funnel, "funnel")}
by_funnel_12 = {r["funnel"]: r for r in group_table("12m", funnel, "funnel")}
baselines = {
    "account_90d": {k: totals["90d"][k] for k in ("spend", "purchases", "purchase_value", "roas", "cpa", "aov", "ctr_pct", "cpm", "cpc")},
    "account_12m": {k: totals["12m"][k] for k in ("spend", "purchases", "purchase_value", "roas", "cpa", "aov", "ctr_pct", "cpm", "cpc")},
    "funnel_90d": {k: {f: v[f] for f in ("spend", "purchases", "purchase_value", "roas", "cpa", "ctr_pct", "cpm")} for k, v in by_funnel_90.items()},
    "funnel_12m": {k: {f: v[f] for f in ("spend", "purchases", "purchase_value", "roas", "cpa", "ctr_pct", "cpm")} for k, v in by_funnel_12.items()},
    "ads_above_floor_90d": len(ad90),
    "ad_roas_90d_p25_median_p75": [pct([r["roas"] for r in ad90 if r["roas"] is not None], q) for q in (0.25, 0.5, 0.75)],
    "ad_ctr_90d_p25_median_p75": [pct([r["ctr_pct"] for r in ad90 if r["ctr_pct"] is not None], q) for q in (0.25, 0.5, 0.75)],
    "ad_cpa_90d_p25_median_p75": [pct([r["cpa"] for r in ad90 if r["cpa"] is not None], q) for q in (0.25, 0.5, 0.75)],
    "tof_ad_roas_90d_p25_median_p75": [pct([r["roas"] for r in tof90 if r["roas"] is not None], q) for q in (0.25, 0.5, 0.75)],
    "retargeting_ad_roas_90d_p25_median_p75": [pct([r["roas"] for r in ret90 if r["roas"] is not None], q) for q in (0.25, 0.5, 0.75)],
    "spend_floor_90d": FLOOR_90D,
}
# thresholds derived from baselines
acc90 = totals["90d"]
baselines["thresholds"] = {
    "learning_spend_per_ad": FLOOR_90D,
    "kill_roas_below": round(acc90["roas"] * 0.6, 2),
    "kill_ctr_below_pct": round(acc90["ctr_pct"] * 0.6, 3),
    "hold_roas_between": [round(acc90["roas"] * 0.6, 2), round(acc90["roas"] * 1.2, 2)],
    "scale_roas_above": round(acc90["roas"] * 1.2, 2),
    "scale_cpa_below": round(acc90["cpa"] * 0.8, 2),
    "rule": "kill = below 60% of the 90-day account ROAS or CTR after the learning spend; scale = above 120% of account ROAS with CPA under 80% of account CPA and at least 3 purchases",
}
write_json("baselines.json", baselines)

print(json.dumps({"totals": {w: totals[w] for w in WINDOWS}, "current": current, "floors": floors, "baselines": baselines}, indent=1))
