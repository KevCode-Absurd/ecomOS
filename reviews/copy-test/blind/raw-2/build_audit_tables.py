"""Build every table used in the Arm B audit from data/meta-gallery/cache/gallery.json.

Run from the repo root:  python3 reviews/copy-test/blind/raw-2/build_audit_tables.py

Rules applied:
- Day 0 = meta.window.since (2025-09-23). Last day index in the data = 366 (2026-09-24).
- Rows: [day_index, spend, purchases, purchase_value, impressions, clicks].
- A null purchase or purchase_value is "not reported by Meta for that day". Totals sum the
  reported values only. An ad whose spend days never report a purchase shows purchases and
  ROAS as "unavailable", never 0. Its spend still counts in the spend totals.
- Period ROAS = total reported purchase value / total spend. Never an average of ratios.
- 12 months = day 0 to day 366 (the full capture, 2025-09-23 to 2026-09-24).
- 90 days = the last 90 day indexes with data (day 277 to 366 = 2026-06-27 to 2026-09-24).
- Breakdowns (age, gender, platform) are read from `monthly` and never added to `daily` totals.
"""
import csv
import json
import os
from collections import defaultdict
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", "..", "..", ".."))
SRC = os.path.join(REPO, "data", "meta-gallery", "cache", "gallery.json")

g = json.load(open(SRC, encoding="utf-8"))
ads = g["ads"]
daily = g["daily"]
monthly = g["monthly"]
since = date.fromisoformat(g["meta"]["window"]["since"])
max_day = max(r[0] for rows in daily.values() for r in rows)
D90_LO = max_day - 89
WINDOWS = {"12m": (0, max_day), "90d": (D90_LO, max_day), "30d": (max_day - 29, max_day)}


def day_str(i):
    return (since + timedelta(days=i)).isoformat()


def agg(rows, lo, hi):
    """Sum spend, reported purchases, reported value, impressions, clicks for day range."""
    s = v = imp = clk = 0.0
    p = 0.0
    p_reported = False
    days = 0
    for r in rows:
        if lo <= r[0] <= hi:
            days += 1
            s += r[1] or 0.0
            if r[2] is not None:
                p += r[2]
                p_reported = True
            if r[3] is not None:
                v += r[3]
                p_reported = True
            imp += r[4] or 0.0
            clk += r[5] or 0.0
    return {
        "spend": round(s, 2),
        "purchases": p if p_reported else None,
        "value": round(v, 2) if p_reported else None,
        "impressions": imp,
        "clicks": clk,
        "days_with_spend": days,
    }


def ratio(a, b):
    return round(a / b, 4) if (a is not None and b) else None


def enrich(m):
    m["roas"] = ratio(m["value"], m["spend"]) if m["value"] is not None else None
    m["cpa"] = round(m["spend"] / m["purchases"], 2) if m["purchases"] else None
    m["ctr_pct"] = round(100 * m["clicks"] / m["impressions"], 3) if m["impressions"] else None
    m["cpm"] = round(1000 * m["spend"] / m["impressions"], 2) if m["impressions"] else None
    m["aov"] = round(m["value"] / m["purchases"], 2) if m["purchases"] else None
    return m


def funnel_stage(campaign_name):
    n = campaign_name.upper()
    if "BOF" in n:
        return "BOF (cart and site retargeting)"
    if "MOF" in n:
        return "MOF (engagers and catalogue visitors)"
    if "AOF" in n:
        return "AOF (all funnel, sale)"
    if "TOF" in n:
        return "TOF (prospecting)"
    if "BFCM" in n:
        return "TOF (prospecting)"
    if "EVENT" in n or "STORE VISIT" in n:
        return "Offline / store"
    return "Other"


def campaign_type(campaign_name):
    n = campaign_name.lower()
    if any(k in n for k in ["sale", "bfcm", "countdown", "hours", "days to go", "deal of the day", "eoss", "valentine", "akshaya", "festive", "diwali", "navratri", "karwa", "rakhi"]):
        return "promo or festival"
    return "evergreen"


# ---------- per-ad table ----------
per_ad = []
for aid, a in ads.items():
    rows = daily.get(aid, [])
    c = a["creative"]
    rec = {
        "ad_id": aid,
        "ad_name": a.get("name"),
        "campaign": a.get("campaign_name"),
        "adset": a.get("adset_name"),
        "status": a.get("effective_status"),
        "attribution": a.get("attribution_setting"),
        "format": c.get("type"),
        "funnel_stage": funnel_stage(a.get("campaign_name", "")),
        "campaign_type": campaign_type(a.get("campaign_name", "")),
        "angle": a["tags"]["angle"]["code"],
        "product": a["tags"]["product"]["code"],
        "hook": a["tags"]["hook"]["code"],
        "headline": c.get("headline") or c.get("title") or "",
        "description": c.get("description") or "",
        "primary_text_first_line": (c.get("primary_text") or "").strip().split("\n")[0][:160],
        "primary_text_chars": len(c.get("primary_text") or ""),
        "has_primary_text": bool((c.get("primary_text") or "").strip()),
        "first_day": day_str(min(r[0] for r in rows)) if rows else None,
        "last_day": day_str(max(r[0] for r in rows)) if rows else None,
    }
    for w, (lo, hi) in WINDOWS.items():
        m = enrich(agg(rows, lo, hi))
        for k, v in m.items():
            rec[f"{w}_{k}"] = v
    per_ad.append(rec)

per_ad.sort(key=lambda r: -r["12m_spend"])


def write_csv(name, rows, fields=None):
    if not rows:
        return
    fields = fields or list(rows[0].keys())
    with open(os.path.join(ROOT, name), "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=fields)
        wr.writeheader()
        for r in rows:
            wr.writerow({k: ("unavailable" if r.get(k) is None else r.get(k)) for k in fields})


def write_json(name, obj):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)


write_csv("per_ad.csv", per_ad)

# ---------- account totals and monthly ----------
totals = {}
for w, (lo, hi) in WINDOWS.items():
    t = {"spend": 0.0, "purchases": 0.0, "value": 0.0, "impressions": 0.0, "clicks": 0.0}
    any_p = False
    for aid, rows in daily.items():
        m = agg(rows, lo, hi)
        t["spend"] += m["spend"]
        t["impressions"] += m["impressions"]
        t["clicks"] += m["clicks"]
        if m["purchases"] is not None:
            t["purchases"] += m["purchases"]
            t["value"] += m["value"]
            any_p = True
    if not any_p:
        t["purchases"] = t["value"] = None
    t["window"] = [day_str(lo), day_str(hi)]
    t["days"] = hi - lo + 1
    totals[w] = enrich(t)
    totals[w]["spend_per_day"] = round(t["spend"] / (hi - lo + 1), 2)

# monthly spend by calendar month
monthly_tot = defaultdict(lambda: {"spend": 0.0, "purchases": 0.0, "value": 0.0, "impressions": 0.0, "clicks": 0.0})
for aid, rows in daily.items():
    for r in rows:
        mo = day_str(r[0])[:7]
        mt = monthly_tot[mo]
        mt["spend"] += r[1] or 0
        mt["purchases"] += r[2] or 0
        mt["value"] += r[3] or 0
        mt["impressions"] += r[4] or 0
        mt["clicks"] += r[5] or 0
monthly_rows = []
for mo in sorted(monthly_tot):
    m = dict(monthly_tot[mo])
    m = enrich({k: (round(v, 2) if isinstance(v, float) else v) for k, v in m.items()})
    m["month"] = mo
    monthly_rows.append(m)
write_csv("monthly_totals.csv", monthly_rows, ["month", "spend", "purchases", "value", "roas", "cpa", "aov", "impressions", "clicks", "ctr_pct", "cpm"])

# current monthly spend: last 30 days, and mean of last 3 full calendar months
full_months = [m for m in monthly_rows if m["month"] not in ("2025-09", "2026-09")]
last3 = full_months[-3:]
totals["current_monthly_spend"] = {
    "last_30_days_spend": totals["30d"]["spend"],
    "last_30_days_window": totals["30d"]["window"],
    "mean_of_last_3_full_months": round(sum(m["spend"] for m in last3) / 3, 2),
    "last_3_full_months": [m["month"] for m in last3],
    "mean_of_12_full_months": round(sum(m["spend"] for m in full_months) / len(full_months), 2),
    "account_amount_spent_reported_by_meta": g["meta"]["account_spend_check"]["account_total_spend"],
    "sum_of_daily_rows_in_capture": round(sum(r[1] for rows in daily.values() for r in rows), 2),
}
write_json("account_totals.json", totals)


# ---------- group tables ----------
def group_table(key, window):
    lo, hi = WINDOWS[window]
    acc = defaultdict(lambda: {"ads": 0, "spend": 0.0, "purchases": 0.0, "value": 0.0, "impressions": 0.0, "clicks": 0.0, "reported": False})
    for aid, a in ads.items():
        m = agg(daily.get(aid, []), lo, hi)
        if m["spend"] <= 0:
            continue
        k = per_ad_by_id[aid][key]
        x = acc[k]
        x["ads"] += 1
        x["spend"] += m["spend"]
        x["impressions"] += m["impressions"]
        x["clicks"] += m["clicks"]
        if m["purchases"] is not None:
            x["purchases"] += m["purchases"]
            x["value"] += m["value"]
            x["reported"] = True
    total_spend = sum(x["spend"] for x in acc.values())
    total_value = sum(x["value"] for x in acc.values())
    out = []
    for k, x in acc.items():
        row = {key: k, "ads_with_spend": x["ads"], "spend": round(x["spend"], 2),
               "purchases": x["purchases"] if x["reported"] else None,
               "value": round(x["value"], 2) if x["reported"] else None,
               "impressions": x["impressions"], "clicks": x["clicks"]}
        row = enrich(row)
        row["spend_share_pct"] = round(100 * x["spend"] / total_spend, 2) if total_spend else None
        row["value_share_pct"] = round(100 * x["value"] / total_value, 2) if (total_value and x["reported"]) else None
        out.append(row)
    out.sort(key=lambda r: -r["spend"])
    return out


per_ad_by_id = {r["ad_id"]: r for r in per_ad}
group_fields = None
for key in ["angle", "hook", "product", "format", "funnel_stage", "campaign_type", "attribution", "has_primary_text"]:
    for w in ["12m", "90d"]:
        rows = group_table(key, w)
        write_csv(f"by_{key}_{w}.csv", rows)

# headline table (12m and 90d)
for w in ["12m", "90d"]:
    rows = group_table("headline", w)
    write_csv(f"by_headline_{w}.csv", rows)

# campaign table 90d and 12m
for w in ["12m", "90d"]:
    rows = group_table("campaign", w)
    write_csv(f"by_campaign_{w}.csv", rows)

# ---------- best and worst ads at a spend floor ----------
# Floor: 3 x the account's 12-month cost per reported purchase (the 24-DEP kill rule uses 3x target CPA).
cpa12 = totals["12m"]["cpa"]
FLOOR = round(3 * cpa12, -3)  # rounded to the nearest 1,000
ranking_note = {
    "spend_floor_inr": FLOOR,
    "how_set": "3 x the account's 12-month cost per reported purchase (%.0f), rounded to the nearest 1,000. An ad below this spend has not had the chance to report 3 purchases." % cpa12,
}


def ranked(window):
    lo, hi = WINDOWS[window]
    elig = [r for r in per_ad if r[f"{window}_spend"] >= FLOOR]
    with_roas = [r for r in elig if r[f"{window}_roas"] is not None]
    no_purchase = [r for r in elig if r[f"{window}_purchases"] is None]
    best = sorted(with_roas, key=lambda r: -r[f"{window}_roas"])[:10]
    worst = sorted(with_roas, key=lambda r: r[f"{window}_roas"])[:10]
    cols = ["ad_id", "ad_name", "campaign", "funnel_stage", "format", "angle", "product", "hook", "headline", "primary_text_first_line",
            f"{window}_spend", f"{window}_purchases", f"{window}_value", f"{window}_roas", f"{window}_cpa", f"{window}_ctr_pct", "attribution", "status"]
    return elig, best, worst, no_purchase, cols


for w in ["12m", "90d"]:
    elig, best, worst, nop, cols = ranked(w)
    write_csv(f"best10_{w}.csv", best, cols)
    write_csv(f"worst10_{w}.csv", worst, cols)
    write_csv(f"no_reported_purchase_at_floor_{w}.csv", sorted(nop, key=lambda r: -r[f"{w}_spend"]), cols)
    ranking_note[f"{w}_ads_at_or_above_floor"] = len(elig)
    ranking_note[f"{w}_ads_at_floor_with_no_reported_purchase"] = len(nop)
write_json("ranking_note.json", ranking_note)

# ---------- baselines for the test plan ----------
# Baselines from evergreen TOF ads only, since the new ads are cold prospecting first.
def baseline(filter_fn, window):
    lo, hi = WINDOWS[window]
    t = {"spend": 0.0, "purchases": 0.0, "value": 0.0, "impressions": 0.0, "clicks": 0.0}
    rep = False
    n = 0
    for aid, a in ads.items():
        r = per_ad_by_id[aid]
        if not filter_fn(r):
            continue
        m = agg(daily.get(aid, []), lo, hi)
        if m["spend"] <= 0:
            continue
        n += 1
        t["spend"] += m["spend"]
        t["impressions"] += m["impressions"]
        t["clicks"] += m["clicks"]
        if m["purchases"] is not None:
            t["purchases"] += m["purchases"]
            t["value"] += m["value"]
            rep = True
    if not rep:
        t["purchases"] = t["value"] = None
    t["ads"] = n
    return enrich(t)


baselines = {
    "account_12m": totals["12m"],
    "account_90d": totals["90d"],
    "account_30d": totals["30d"],
    "tof_evergreen_12m": baseline(lambda r: r["funnel_stage"].startswith("TOF") and r["campaign_type"] == "evergreen", "12m"),
    "tof_evergreen_90d": baseline(lambda r: r["funnel_stage"].startswith("TOF") and r["campaign_type"] == "evergreen", "90d"),
    "tof_promo_12m": baseline(lambda r: r["funnel_stage"].startswith("TOF") and r["campaign_type"] != "evergreen", "12m"),
    "bof_mof_12m": baseline(lambda r: r["funnel_stage"].startswith(("BOF", "MOF")), "12m"),
    "bof_mof_90d": baseline(lambda r: r["funnel_stage"].startswith(("BOF", "MOF")), "90d"),
    "aof_sale_90d": baseline(lambda r: r["funnel_stage"].startswith("AOF"), "90d"),
    "tof_non_catalog_12m": baseline(lambda r: r["funnel_stage"].startswith("TOF") and r["format"] != "catalog_dynamic", "12m"),
    "tof_non_catalog_90d": baseline(lambda r: r["funnel_stage"].startswith("TOF") and r["format"] != "catalog_dynamic", "90d"),
}
write_json("baselines.json", baselines)

# ---------- breakdowns (kept separate) ----------
for dim in ["age", "gender", "publisher_platform"]:
    acc = defaultdict(lambda: {"spend": 0.0, "purchases": 0.0, "value": 0.0, "reported": False})
    acc90 = defaultdict(lambda: {"spend": 0.0, "purchases": 0.0, "value": 0.0, "reported": False})
    for aid, rows in monthly[dim].items():
        if not rows:
            continue
        for r in rows:
            start, end, seg, sp, pu, va = r
            x = acc[seg]
            x["spend"] += sp or 0
            if pu is not None:
                x["purchases"] += pu
                x["value"] += va or 0
                x["reported"] = True
            if start >= "2026-07-01":
                y = acc90[seg]
                y["spend"] += sp or 0
                if pu is not None:
                    y["purchases"] += pu
                    y["value"] += va or 0
                    y["reported"] = True
    for label, a in [("12m", acc), ("jul_sep_2026", acc90)]:
        tot = sum(x["spend"] for x in a.values())
        rows_out = []
        for seg, x in a.items():
            row = {dim: seg, "spend": round(x["spend"], 2), "purchases": x["purchases"] if x["reported"] else None,
                   "value": round(x["value"], 2) if x["reported"] else None, "impressions": None, "clicks": None}
            row = enrich(row)
            row["spend_share_pct"] = round(100 * x["spend"] / tot, 2) if tot else None
            rows_out.append(row)
        rows_out.sort(key=lambda r: -r["spend"])
        write_csv(f"breakdown_{dim}_{label}.csv", rows_out, [dim, "spend", "spend_share_pct", "purchases", "value", "roas", "cpa"])

# ---------- active ads now ----------
active = [r for r in per_ad if r["status"] == "ACTIVE"]
write_csv("active_ads.csv", sorted(active, key=lambda r: -r["30d_spend"]))

# ---------- copy inventory ----------
copy_rows = defaultdict(lambda: {"ads": 0, "spend_12m": 0.0, "value_12m": 0.0, "spend_90d": 0.0, "value_90d": 0.0, "rep": False, "rep90": False, "headlines": set(), "campaigns": set()})
for aid, a in ads.items():
    pt = (a["creative"].get("primary_text") or "").strip()
    x = copy_rows[pt]
    r = per_ad_by_id[aid]
    x["ads"] += 1
    x["spend_12m"] += r["12m_spend"]
    x["spend_90d"] += r["90d_spend"]
    if r["12m_value"] is not None:
        x["value_12m"] += r["12m_value"]
        x["rep"] = True
    if r["90d_value"] is not None:
        x["value_90d"] += r["90d_value"]
        x["rep90"] = True
    x["headlines"].add(r["headline"])
    x["campaigns"].add(r["campaign"])
copy_out = []
for pt, x in copy_rows.items():
    copy_out.append({
        "primary_text": pt,
        "chars": len(pt),
        "first_line": pt.split("\n")[0][:160],
        "ads": x["ads"],
        "spend_12m": round(x["spend_12m"], 2),
        "value_12m": round(x["value_12m"], 2) if x["rep"] else None,
        "roas_12m": round(x["value_12m"] / x["spend_12m"], 3) if (x["rep"] and x["spend_12m"]) else None,
        "spend_90d": round(x["spend_90d"], 2),
        "value_90d": round(x["value_90d"], 2) if x["rep90"] else None,
        "roas_90d": round(x["value_90d"] / x["spend_90d"], 3) if (x["rep90"] and x["spend_90d"]) else None,
        "headlines": " || ".join(sorted(h for h in x["headlines"] if h)),
        "campaigns": " || ".join(sorted(x["campaigns"]))[:400],
    })
copy_out.sort(key=lambda r: -r["spend_12m"])
write_json("copy_inventory.json", copy_out)

print("windows", {k: [day_str(a), day_str(b)] for k, (a, b) in WINDOWS.items()})
print("totals", json.dumps(totals, indent=1))
print("ranking", json.dumps(ranking_note, indent=1))
print("baselines", json.dumps(baselines, indent=1))
