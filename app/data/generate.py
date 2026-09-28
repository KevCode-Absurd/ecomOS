#!/usr/bin/env python3
"""Generator v2: simulated connector tables for a brand calibrated by its brain.

Reads app/brain/<brand>/assumptions.json (and nothing else from the brain) and
writes, under app/data/brands/<brand>/:

    data.sqlite          every row-level table (git-ignored, rebuilt from the seed)
    aggregates/*.json    daily, monthly, channel, product, cohort and calibration
                         rollups (committed; screens and tests read these)
    assumptions.json     the brain fields used, with value, status and sources
    manifest.json        per calibration field: value used, brain or fallback, rule
    tables.json          every table: rows, where it lives, connector it is shaped like
    README.md            the same, for people

    python3 app/data/generate.py --brand bombas               scale 1.0 (the public revenue band)
    python3 app/data/generate.py --brand bombas --scale 0.1   fast dev build
    python3 app/data/generate.py --brand bombas --as-of 2026-09-27 --seed 7 --out DIR

Deterministic: same assumptions, seed, scale and as_of give the same rows.
The window is 24 months of days ending on the last full day in
America/New_York (730 days). Every row carries brand, captured_at or
computed_at, source and simulated = true.

Orders are the one truth. The chain, in order:

    daily order targets     revenue band x seasonality x growth x weekday, / AOV
    customers               new or repeat per order, from a scheduled repeat model
                            (2 warm-up years so the window opens with a real repeat base)
    orders + lines          basket, discount, shipping, tax, payment, journey (utm)
    ad_rows (Meta)          purchases = orders Meta claims: click credit on paid social
                            orders plus 1d_view credit on some other orders (overlap)
    google_rows             conversions = paid search orders credited plus brand search
                            overlap on organic and direct orders
    flows, campaign_sends   Klaviyo attributed orders: email and SMS orders plus overlap
                            on direct, organic, paid social and paid search orders;
                            matched_order_ids list them
    sessions (GA4)          transactions = orders GA4 tracked (91 to 95 percent, drawn daily);
                            sessions and funnel events are implied by them
    reversed_orders         returns, carrier returns and chargebacks, each on an order
    payouts                 Shopify Payments charges less fees, refunds, dispute moves
    tickets                 most on an order; reviews on skus people bought
    inventory, products, abandoned_checkouts, customers, fixtures
    wholesale_sell_in, marketplace_sales, paid_other_spend
                            monthly or daily fixtures at the brain's channel mix and paid split

Placeholder rates (not Bombas facts; the brain must not be asked for them):
conversion rate by channel (shape; scaled to the assumed sessions), CPA by
channel, CPM, CTR, return rate 6 percent, chargeback 0.15 percent, mobile 70
percent, GA4 capture 91 to 95 percent, Klaviyo overlap shares, Meta view-through
share, fees 2.9 percent plus 30 cents. They are listed in PLACEHOLDERS and copied
into manifest.json. Numbers the founder asked us to assume (sessions per month)
are in ASSUMED and marked assumed in the manifest. The S2.3c changes follow
app/data/brands/bombas/REVIEW.md, "Fixes for the generator".

Needs numpy (vectorised so scale 1.0, about 11 million orders, runs in minutes).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sqlite3
import sys
import time
import zlib
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

for _t, _f in ((np.int64, int), (np.int32, int), (np.int16, int), (np.int8, int), (np.float64, float), (np.bool_, int)):
    sqlite3.register_adapter(_t, _f)

HERE = Path(__file__).resolve().parent
APP = HERE.parent
BRAIN = APP / "brain"
BRANDS = HERE / "brands"
TZ = ZoneInfo("America/New_York")
DAYS = 730
WARMUP = 730
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

# ------------------------------------------------------------ placeholders
PLACEHOLDERS = {
    "note": "Shapes, not brand facts. Fixed constants in the generator.",
    "cvr_by_channel": {"paid_social": 0.011, "paid_search": 0.034, "organic_search": 0.028, "direct": 0.041,
                       "email": 0.038, "sms": 0.045, "other": 0.016},
    "device_share": {"mobile": 0.70, "desktop": 0.26, "tablet": 0.04},
    "cvr_device_mult": {"mobile": 0.85, "desktop": 1.45, "tablet": 1.0},
    "meta_cpa_usd": 34.0, "meta_q4_cpa_mult": 1.08, "meta_cpm_usd": 14.0, "meta_ctr": 0.012, "meta_link_ctr": 0.008,
    "meta_click_credit": 0.80, "meta_view_credit_on_other_orders": 0.07,
    "google_cpa_usd": {"brand_search": 8.0, "nonbrand_search": 45.0, "pmax": 30.0, "demand_gen": 80.0},
    "google_credit": 0.88, "google_brand_overlap": {"organic_search": 0.05, "direct": 0.04},
    "klaviyo_overlap": {"direct": 0.20, "organic_search": 0.08, "paid_social": 0.06, "paid_search": 0.04, "other": 0.05},
    "ga4_capture": [0.91, 0.95], "journey_ready": 0.97,
    "return_rate": 0.06, "carrier_return_rate": 0.004, "chargeback_rate": 0.0015, "chargeback_fee_usd": 15.0,
    "fee_online": [0.029, 0.30], "fee_pos": [0.026, 0.10], "payout_lag_days": 2,
    "payment_mix": {"card": 0.62, "shop_pay": 0.18, "apple_pay": 0.08, "paypal": 0.12},
    "ticket_rate": 0.05, "ticket_rate_dec": 0.08, "return_ticket_share": 0.30, "presale_ticket_rate": 0.006,
    "review_rate_per_line": 0.012,
    "abandoned_per_web_order": 2.0, "cogs_share_of_price": 0.30, "shipping_fee_usd": 5.99,
    "free_shipping_threshold_usd": 75.0, "first_order_code_pct": 20, "first_order_code_use": 0.55,
    "repeat_code_use": 0.10, "repeat_code_pct": 10,
    "bfcm_discount_pct": 20, "bfcm_code_use": 0.85, "q4_aov_mult": 1.04,
    "email_consent": 0.60, "sms_consent": 0.25,
    "owned_retail_open": "2025-11-01",
    "repeat_gap_median_days": [75, 120], "repeat_gap_sigma": 0.9,
    "repeat_continue_by_order": [0.45, 0.60, 0.70], "holiday_cohort_repeat_mult": 0.85,
    "returning_seasonality_weight": 0.7, "growth_noise_sigma": 0.04, "daily_noise_cv": 0.09,
    "wholesale_month_index": {"jan": 0.5, "feb": 0.9, "mar": 0.9, "apr": 0.9, "may": 0.9, "jun": 0.9, "jul": 0.9,
                              "aug": 1.3, "sep": 1.4, "oct": 1.3, "nov": 0.9, "dec": 0.6},
    "new_partner_ramp_by_quarter": [0.25, 0.50, 1.0], "new_partner_since_month": 10,
    "partner_year1_cap": {"DSW": 0.25},
    "marketplace_split": {"amazon": 0.80, "tiktok_shop": 0.20},
}

# Numbers the founder asked us to assume where the brain has none (S2.3c, 28 Sep 2026).
# Each one is marked assumed in manifest.json; the brain's open question stays open.
ASSUMED = {
    "site_sessions_monthly": {"value": 15_000_000, "unit": "sessions per month", "status": "assumed",
                              "note": "assumed from REVIEW.md fix 3 (public estimators put bombas.com in the single digit "
                                      "to low double digit millions); open question site_sessions_monthly stays in the brain"},
}

FALLBACK_ACQ_MIX = {"paid_social": 35, "paid_search": 20, "organic_search": 15, "direct": 15, "email_sms": 10, "other": 5}
FALLBACK_SEASON = {"jan": 0.9, "feb": 1.0, "mar": 1.0, "apr": 1.0, "may": 1.0, "jun": 1.0, "jul": 1.0, "aug": 1.0,
                   "sep": 1.0, "oct": 1.2, "nov": 1.6, "dec": 1.8}

CHANNELS = ["paid_social", "paid_search", "organic_search", "direct", "email", "sms", "other", "pos"]
CH = {c: i for i, c in enumerate(CHANNELS)}
RETURNING_MIX = {"paid_social": 0.20, "paid_search": 0.125, "organic_search": 0.15, "direct": 0.255,
                 "email": 0.176, "sms": 0.044, "other": 0.05}
WEEKDAY = [1.00, 0.99, 0.97, 0.96, 0.97, 1.05, 1.06]  # Mon..Sun
DEVICES = ["mobile", "desktop", "tablet"]
PAYMENTS = ["card", "shop_pay", "apple_pay", "paypal", "card_present"]
STATES = [("CA", 0.14, 0.0725), ("TX", 0.09, 0.0625), ("NY", 0.08, 0.04), ("FL", 0.08, 0.06), ("IL", 0.05, 0.0625),
          ("PA", 0.05, 0.06), ("OH", 0.04, 0.0575), ("GA", 0.04, 0.04), ("NC", 0.04, 0.0475), ("MI", 0.03, 0.06),
          ("NJ", 0.04, 0.06625), ("WA", 0.03, 0.065), ("MA", 0.03, 0.0625), ("CO", 0.03, 0.029), ("OR", 0.02, 0.0),
          ("other", 0.21, 0.055)]

# Catalog: the 25 SKU keys of finance_inputs.json (S2.3c, REVIEW.md fix 1), so cogs_landed joins by sku.
# Titles follow each finance row's reason; list prices are placeholders shaped to the AOV band and put
# landed cost near 22 to 30 percent of list. (sku, category, title, price, items per unit, popularity)
CATALOG = [
    ("BMB-SK-M-ANK-1", "socks", "Men's Ankle Sock", 14.0, 1, 2), ("BMB-SK-M-ANK-4", "socks", "Men's Ankle Sock 4-Pack", 52.0, 4, 7),
    ("BMB-SK-M-CRW-1", "socks", "Men's Calf Sock", 15.0, 1, 2), ("BMB-SK-M-CRW-4", "socks", "Men's Calf Sock 4-Pack", 56.0, 4, 5),
    ("BMB-SK-W-ANK-1", "socks", "Women's Ankle Sock", 13.0, 1, 2), ("BMB-SK-W-ANK-4", "socks", "Women's Ankle Sock 4-Pack", 50.0, 4, 7),
    ("BMB-SK-W-NSH-3", "socks", "Women's No Show Sock 3-Pack", 36.0, 3, 5),
    ("BMB-SK-W-CRW-4", "socks", "Women's Calf Sock 4-Pack", 54.0, 4, 4),
    ("BMB-SK-MER-1", "socks", "Merino Wool Calf Sock", 22.0, 1, 3), ("BMB-SK-MER-3", "socks", "Merino Wool Calf Sock 3-Pack", 63.0, 3, 3),
    ("BMB-SK-ATH-6", "socks", "Running Ankle Sock 6-Pack", 90.0, 6, 2), ("BMB-SK-GOLF-6", "socks", "Golf Ankle Sock 6-Pack", 84.0, 6, 1),
    ("BMB-SK-CMP-1", "socks", "Compression Sock", 25.0, 1, 2), ("BMB-SK-CMP-3", "socks", "Compression Sock 3-Pack", 72.0, 3, 2),
    ("BMB-SK-KID-8", "socks", "Kids Ankle Sock 8-Pack", 72.0, 8, 2), ("BMB-SK-GIFT-12", "socks", "Gift Box 12-Pack", 150.0, 12, 1),
    ("BMB-UW-M-BRF-1", "underwear", "Men's Boxer Brief", 24.0, 1, 2), ("BMB-UW-M-BRF-3", "underwear", "Men's Boxer Brief 3-Pack", 66.0, 3, 2),
    ("BMB-UW-W-HIP-1", "underwear", "Women's Hipster", 18.0, 1, 2), ("BMB-UW-W-BRL-1", "underwear", "Women's Bralette", 38.0, 1, 1),
    ("BMB-TS-M-CRW-1", "tshirts", "Men's Pima Cotton Tee", 35.0, 1, 1),
    ("BMB-TS-W-VNK-1", "tshirts", "Women's Pima Cotton V-Neck Tee", 35.0, 1, 1),
    ("BMB-SL-M-MOC-1", "slippers", "Men's Moccasin Slipper", 80.0, 1, 1),
    ("BMB-SL-W-SCF-1", "slippers", "Women's Sherpa Scuff Slipper", 60.0, 1, 2),
    ("BMB-FW-CLG-1", "footwear", "Clog", 90.0, 1, 1),
]
SOCK_LIKE = ("socks", "slippers", "footwear")  # the brain's 93 percent bucket; footwear_pct_2025 is not applied
SKUS = [c[0] for c in CATALOG]
PRICE = np.array([c[3] for c in CATALOG])
PAIRS = np.array([c[4] for c in CATALOG])

META_CAMPAIGNS = [("MC-1", "Prospecting | Advantage+"), ("MC-2", "Prospecting | Broad"),
                  ("MC-3", "Retargeting | Site 30d"), ("MC-4", "Holiday | Gift buyers")]
GOOGLE_CAMPAIGNS = [("GC-1", "Brand | Search", "SEARCH", "brand_search", 0.45), ("GC-2", "Non-brand | Search | Socks", "SEARCH", "nonbrand_search", 0.20),
                    ("GC-3", "Shopping | PMax", "PERFORMANCE_MAX", "pmax", 0.30), ("GC-4", "YouTube | Demand Gen", "DEMAND_GEN", "demand_gen", 0.05)]
SEARCH_TERMS = {"GC-1": ["bombas", "bombas socks", "bombas sale", "bombas ankle socks", "bombas slippers", "bombas underwear", "bombas coupon"],
                "GC-2": ["cushioned ankle socks", "best running socks", "merino wool socks", "compression socks for women",
                         "no show socks men", "athletic socks", "warm slippers", "socks gift box"]}
FLOWS = [("F-1", "Welcome Series", "added_to_list", [("FM-1", "email", "Welcome"), ("FM-2", "email", "Why people switch"), ("FM-3", "sms", "Your code is waiting")]),
         ("F-2", "Abandoned Checkout", "metric", [("FM-4", "email", "Still thinking it over?"), ("FM-5", "sms", "Your cart is saved")]),
         ("F-3", "Browse Abandonment", "metric", [("FM-6", "email", "Picked up where you left off")]),
         ("F-4", "Post-Purchase", "metric", [("FM-7", "email", "How are they fitting?")]),
         ("F-5", "Replenishment", "metric", [("FM-8", "email", "Time for a fresh pack?")]),
         ("F-6", "Winback", "segment", [("FM-9", "email", "We saved your size")])]
FLOW_MSG = [(f[0], f[1], f[2], m) for f in FLOWS for m in f[3]]
FLOW_CVR = {"F-1": 0.030, "F-2": 0.050, "F-3": 0.012, "F-4": 0.006, "F-5": 0.010, "F-6": 0.004}
LANDING = {
    "paid_social": ["/products/ankle-sock-4-pack", "/collections/best-sellers", "/", "/collections/gifts"],
    "paid_search": ["/", "/collections/mens-socks", "/collections/womens-socks", "/products/ankle-sock-4-pack"],
    "organic_search": ["/", "/collections/socks", "/pages/giving-back", "/products/merino-wool-calf-sock"],
    "direct": ["/", "/collections/best-sellers", "/account"],
    "email": ["/", "/collections/new-arrivals", "/cart"], "sms": ["/", "/cart"],
    "other": ["/", "/collections/running", "/pages/giving-back"], "pos": [None],
}
OTHER_SOURCES = [("pinterest", "social", "Organic Social"), ("tiktok", "social", "Organic Social"),
                 ("strava.com", "referral", "Referral"), ("youtube", "creator", "Paid Other")]
TICKET_REASONS_ORDER = ["where is my order", "size or fit", "return or exchange", "hole or defect", "discount code",
                        "change address", "cancel order", "damaged in transit"]
TICKET_W = [0.30, 0.14, 0.18, 0.12, 0.08, 0.06, 0.06, 0.06]
REVIEW_TEXT = {5: ["Comfortable all day.", "These fit well and stay up.", "Softest pair I own.", "Bought more for the family."],
               4: ["Good fit, a bit warm.", "Nice socks, took a week to arrive.", "Comfortable. Wish there were more colors."],
               3: ["Fine, not special.", "Fit runs small for me."],
               2: ["A hole after a few months.", "Did not stay up."], 1: ["Wore through fast.", "Wrong size and a slow exchange."]}


# ----------------------------------------------------------------- helpers
def stream(seed, name):
    return np.random.default_rng([seed, zlib.crc32(name.encode())])


def r2(a):
    return np.round(np.asarray(a, dtype=float) + 1e-9, 2)


def last_full_day():
    return (datetime.now(TZ) - timedelta(days=1)).date()


def iso_utc(epoch):
    """epoch seconds (int array) -> ISO strings with Z."""
    return np.char.add(np.asarray(epoch, dtype="int64").astype("datetime64[s]").astype(str), "Z")


def js(obj):
    return json.dumps(obj, separators=(",", ":"))


# ------------------------------------------------------------ calibration
def load_assumptions(brand):
    path = BRAIN / brand / "assumptions.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    return path, {r["field"]: r for r in raw}


def calibrate(fields, scale):
    """Resolve each calibration field to a value plus its manifest entry."""
    man, prof = {}, {}

    def rec(name, value, origin, rule=None, src=None):
        man[name] = {"value": value, "origin": origin, "rule": rule,
                     "status": (src or {}).get("status"), "as_of": (src or {}).get("as_of"),
                     "source_ids": (src or {}).get("source_ids", [])}

    rb = fields.get("revenue_band")
    v = (rb or {}).get("value") or {}
    if not (isinstance(v.get("low_usd"), (int, float)) and isinstance(v.get("high_usd"), (int, float))):
        raise SystemExit("revenue_band missing or partial: the generator stops and writes nothing (calibration.md)")
    point = v.get("point_usd") or (v["low_usd"] + v["high_usd"]) / 2
    series = sorted((s for s in v.get("series", []) if s.get("amount_usd")), key=lambda s: s["year"])
    growth = 0.0
    if len(series) >= 2:
        a, b = series[-2], series[-1]
        growth = (b["amount_usd"] / a["amount_usd"]) ** (1 / (b["year"] - a["year"])) - 1
    prof.update(revenue_point=point, revenue_low=v["low_usd"], revenue_high=v["high_usd"], growth=growth)
    rec("revenue_band", {"low_usd": v["low_usd"], "high_usd": v["high_usd"], "point_usd": point, "scale": scale,
                         "growth_per_year": round(growth, 4), "anchor": "trailing 12 months of the window = point x scale"},
        "brain", "growth from the last two dated series points, applied backward only", rb)

    av = (fields.get("aov_usd") or {}).get("value")
    if isinstance(av, dict) and isinstance(av.get("estimate"), (int, float)):
        prof["aov"] = float(av["estimate"])
        rec("aov", av, "brain", "AOV = net merchandise per order (after discount, before shipping and tax)", fields["aov_usd"])
    else:
        prof["aov"] = float(np.median(PRICE)) * 1.4
        rec("aov", prof["aov"], "fallback (catalog)", "median variant price x 1.4 units")

    rr = (fields.get("repeat_rate_12m") or fields.get("repeat_rate") or {})
    if isinstance(rr.get("value"), (int, float)):
        prof["repeat_12m"] = float(rr["value"])
        rec("repeat_rate", rr["value"], "brain", "share of new customers with a 2nd order within 365 days", rr)
    else:
        prof["repeat_12m"] = 0.25 * 1.4
        rec("repeat_rate", prof["repeat_12m"], "fallback (generic)", "25 percent at 90 days, about 35 percent at 12 months")

    cm = (fields.get("channel_mix") or {}).get("value") or {}
    parts = [cm.get("dtc_site_pct"), cm.get("wholesale_pct"), cm.get("owned_retail_pct")]
    mkt = cm.get("marketplaces_pct")  # null means unavailable: no marketplace fixture is written
    mkt_n = mkt if isinstance(mkt, (int, float)) else 0.0
    if all(isinstance(p, (int, float)) for p in parts) and abs(sum(parts) + mkt_n - 100) < 0.5:
        prof["sales_mix"] = {"dtc": parts[0] / 100, "wholesale": parts[1] / 100, "owned_retail": parts[2] / 100,
                             "marketplaces": mkt / 100 if isinstance(mkt, (int, float)) else None}
        rec("sales_channel_mix", {k: cm.get(k) for k in ("dtc_site_pct", "wholesale_pct", "owned_retail_pct", "marketplaces_pct")},
            "brain", "orders = dtc site plus owned retail (POS); wholesale and marketplaces are monthly fixtures, not orders",
            fields["channel_mix"])
    else:
        prof["sales_mix"] = {"dtc": 1.0, "wholesale": 0.0, "owned_retail": 0.0, "marketplaces": None}
        rec("sales_channel_mix", None, "fallback (all dtc)", "partial or missing")
    pm = (fields.get("paid_media_split") or {}).get("value") or {}
    keys = ("meta_pct", "google_pct", "youtube_creator_pct", "tiktok_pct", "pinterest_pct", "other_pct")
    if all(isinstance(pm.get(k), (int, float)) for k in keys) and abs(sum(pm[k] for k in keys) - 100) < 0.5:
        prof["paid_split"] = {k[:-4]: pm[k] / 100 for k in keys}
        rec("paid_media_split", {k: pm[k] for k in keys}, "brain",
            "Meta and Google spend ride on their orders; Google CPA is scaled so Meta to Google lands on the split; "
            "YouTube creators, TikTok, Pinterest and other are a daily spend fixture at their share", fields["paid_media_split"])
    else:
        prof["paid_split"] = None
        rec("paid_media_split", None, "missing", "only Meta and Google spend are written; other platforms read unavailable")
    ss = fields.get("site_sessions_monthly")
    if ss and isinstance(ss.get("value"), (int, float)):
        prof["sessions_monthly"] = float(ss["value"])
        rec("site_sessions_monthly", ss["value"], "brain", "cvr_by_channel is scaled so sessions land on this", ss)
    else:
        a = ASSUMED["site_sessions_monthly"]
        prof["sessions_monthly"] = float(a["value"])
        man["site_sessions_monthly"] = {"value": a["value"], "origin": "assumed", "rule": "cvr_by_channel is scaled so "
                                        "GA4 sessions over the last 12 months average this per month", "status": "assumed",
                                        "as_of": "2026-09-28", "source_ids": [], "note": a["note"]}
    # The brain's channel_mix is a sales-channel split. Acquisition mix is not in the brain.
    prof["acq_mix"] = {k: v / 100 for k, v in FALLBACK_ACQ_MIX.items()}
    rec("channel_mix", FALLBACK_ACQ_MIX, "fallback (generic)",
        "brain channel_mix is dtc / wholesale / retail, not acquisition; acquisition split uses the calibration.md fallback")

    se = (fields.get("seasonality") or {}).get("value") or {}
    mi = se.get("monthly_index") or {}
    if all(isinstance(mi.get(m), (int, float)) for m in MONTHS):
        prof["season"] = {m: float(mi[m]) for m in MONTHS}
        rec("seasonality", mi, "brain", "month curve on orders; BFCM and gifting weeks reshape days inside a month only",
            fields["seasonality"])
    else:
        prof["season"] = FALLBACK_SEASON
        rec("seasonality", FALLBACK_SEASON, "fallback (us_retail)", "calibration.md fallback")

    gu = fields.get("giving_units")
    if gu and gu.get("value"):
        rates = gu["value"].get("per_year_between_marks") or []
        prof["giving_rate_brain"] = rates[-1]["items_per_year"] if rates else None
        rec("giving_units", {"rule": "one item donated per item purchased; replacements and exchanges do not count",
                             "brain_items_per_year": prof["giving_rate_brain"]}, "brain",
            "orders.giving_units = items bought (pack size x qty); the brain rate is a cross-check, not a target", gu)
    else:
        prof["giving_rate_brain"] = None
        rec("giving_units", None, "missing", "giving column reads unavailable")

    cat = (fields.get("category_mix") or {}).get("value") or {}
    if isinstance(cat.get("socks_and_slippers_pct"), (int, float)):
        prof["category_mix"] = {"socks_slippers": cat["socks_and_slippers_pct"] / 100,
                                "underwear_tshirts": cat["underwear_and_tshirts_pct"] / 100}
        rec("category_mix", cat, "brain", "93 / 7 revenue split applied to lines; footwear_pct_2025 (single report) not applied",
            fields["category_mix"])
    else:
        prof["category_mix"] = {"socks_slippers": 0.93, "underwear_tshirts": 0.07}
        rec("category_mix", None, "fallback (catalog)", "")

    rp = (fields.get("retail_partners") or {}).get("value") or []
    prof["retail_partners"] = rp
    rec("retail_partners", rp, "brain" if rp else "missing", "wholesale fixture split by partner, from each start year", fields.get("retail_partners"))
    return prof, man


# --------------------------------------------------------------- the model
class Gen:
    def __init__(self, brand, scale=1.0, seed=7, as_of=None, log=print):
        self.brand, self.scale, self.seed = brand, float(scale), int(seed)
        self.as_of = as_of or last_full_day()
        self.start = self.as_of - timedelta(days=DAYS - 1)
        self.captured_at = f"{(self.as_of + timedelta(days=1)).isoformat()}T06:00:00Z"
        self.log = log
        self.assumptions_path, self.fields = load_assumptions(brand)
        self.p, self.manifest_fields = calibrate(self.fields, self.scale)
        self.days = [self.start + timedelta(days=i) for i in range(DAYS)]
        self.day_epoch = np.array([int(datetime(d.year, d.month, d.day, tzinfo=TZ).timestamp()) for d in self.days], dtype="int64")
        self.month_key = np.array([d.year * 100 + d.month for d in self.days])
        self.aggregates, self.tables = {}, {}

    def rng(self, name):
        return stream(self.seed, name)

    # ---- daily targets
    @staticmethod
    def thanksgiving(year):
        return date(year, 11, 1) + timedelta(days=(3 - date(year, 11, 1).weekday()) % 7 + 21)

    def is_bfcm(self, d):
        """Black Friday to Cyber Monday, both inclusive."""
        tg = self.thanksgiving(d.year)
        return tg + timedelta(days=1) <= d <= tg + timedelta(days=4)

    def day_shape(self, d):
        """Within-month day weight (mean about 1 inside a month before renormalising)."""
        w = WEEKDAY[d.weekday()]
        tg = self.thanksgiving(d.year)
        if tg + timedelta(days=1) <= d <= tg + timedelta(days=4):
            w *= [3.2, 2.0, 1.9, 2.8][(d - tg).days - 1]  # Black Friday .. Cyber Monday
        elif d.month == 12 and 2 <= d.day <= 15:
            w *= 1.3
        elif d.month == 12 and d.day >= 20:
            w *= 0.55
        return w

    def growth_path(self):
        """Monthly level multiplier: a random walk on the monthly growth factor, pinned to 1 in the as_of month.

        Step sd is growth_noise_sigma / sqrt(12), so the 12 month growth factor wobbles with sd growth_noise_sigma
        around the brain's trend (fix 8). Walked backward from as_of, so the calibrated last months stay near trend."""
        rng = self.rng("growth_noise")
        n = (WARMUP + DAYS) // 28 + 4
        steps = rng.normal(0, PLACEHOLDERS["growth_noise_sigma"] / math.sqrt(12), n)
        out, level = {}, 0.0
        y, m = self.as_of.year, self.as_of.month
        for i in range(n):
            out[y * 100 + m] = math.exp(level)
            level -= steps[i]
            y, m = (y, m - 1) if m > 1 else (y - 1, 12)
        return out

    def season_shape(self, days):
        """Season x day shape, renormalised inside each month; no growth, no noise."""
        p = self.p
        raw = np.array([p["season"][MONTHS[d.month - 1]] * self.day_shape(d) for d in days])
        keys = np.array([d.year * 100 + d.month for d in days])
        base = np.array([p["season"][MONTHS[d.month - 1]] for d in days])
        for k in np.unique(keys):
            m = keys == k
            raw[m] *= base[m].sum() / raw[m].sum()
        return raw

    def targets(self, days):
        """Expected orders per day (all order channels) for a list of dates: season x day shape x growth x growth noise."""
        p = self.p
        gp = self.growth_path()
        trend = np.array([(1 + p["growth"]) ** (-(self.as_of - d).days / 365.25) * gp.get(d.year * 100 + d.month, 1.0)
                          for d in days])
        return self.season_shape(days) * trend

    # ---- customers: who orders each day
    def schedule_customers(self):
        p, rng = self.p, self.rng("customers")
        pl = PLACEHOLDERS
        all_days = [self.start - timedelta(days=WARMUP - i) for i in range(WARMUP)] + self.days
        shape = self.targets(all_days)
        # day to day noise on the expected orders (fix 8), mean one, before the revenue anchor
        cv = pl["daily_noise_cv"]
        s2 = math.log(1 + cv * cv)
        shape = shape * np.exp(rng.normal(-s2 / 2, math.sqrt(s2), len(shape)))
        sm = p["sales_mix"]
        order_rev_share = sm["dtc"] + sm["owned_retail"]
        target_rev = p["revenue_point"] * self.scale * order_rev_share
        k = target_rev / p["aov"] / shape[-365:].sum()
        exp_orders = shape * k
        g1, g2 = pl["repeat_gap_median_days"]
        sig = pl["repeat_gap_sigma"]
        # returning orders follow the season with a weight (fix 4): repeat gaps run on a clock that
        # ticks faster in peak days, intensity = 1 + w x (season x day shape - 1), mean one over a year
        ext = all_days + [self.as_of + timedelta(days=i + 1) for i in range(1500)]
        ss = self.season_shape(ext)
        ss = ss / ss[:365].mean()
        w = pl["returning_seasonality_weight"]
        clock = np.cumsum(np.maximum(1 + w * (ss - 1), 0.05))
        # repeat probability after a first order: holiday cohorts repeat less (fix 5)
        hol = np.array([d.month in (11, 12) for d in all_days])
        cmult = np.where(hol, pl["holiday_cohort_repeat_mult"], 1.0)
        from statistics import NormalDist
        p_within = NormalDist().cdf(math.log(365 / g1) / sig)
        # recalibrate so the new-customer-weighted mean over the first window year stays on the brain's 12 month rate
        yr1 = slice(WARMUP, WARMUP + 365)
        mean_mult = float((exp_orders[yr1] * cmult[yr1]).sum() / exp_orders[yr1].sum())
        q = min(0.95, p["repeat_12m"] / p_within / mean_mult)
        self.repeat_mean_mult = mean_mult
        q_day = q * cmult
        cont_by = np.array(pl["repeat_continue_by_order"])  # after the 2nd order, the 3rd, the 4th and later
        pending = {}
        cap = int(exp_orders.sum() * 1.2) + 1000
        counts = np.zeros(cap, dtype=np.int32)
        spent_first = np.full(cap, -1, dtype=np.int32)  # first order day index (into all_days)
        next_id = 0
        out_c, out_new, out_idx, out_day = [], [], [], []
        for i, e in enumerate(exp_orders):
            T = rng.poisson(e)
            rep = pending.pop(i, None)
            rep = np.concatenate(rep) if rep else np.zeros(0, dtype=np.int64)
            n_new = max(T - len(rep), 0)
            new = np.arange(next_id, next_id + n_new, dtype=np.int64)
            next_id += n_new
            if next_id >= cap:
                raise RuntimeError("customer capacity exceeded")
            spent_first[new] = i
            # schedule the next order
            first_rep = new[rng.random(n_new) < q_day[i]]
            cont = cont_by[np.clip(counts[rep] - 1, 0, len(cont_by) - 1)]  # counts[rep] + 1 is this order's number
            again = rep[rng.random(len(rep)) < cont]
            for ids, med in ((first_rep, g1), (again, g2)):
                if len(ids):
                    gap = np.ceil(med * np.exp(rng.normal(0, sig, len(ids))))
                    due = np.searchsorted(clock, clock[i] + gap).astype(np.int64)
                    order = np.argsort(due, kind="stable")
                    due, ids = due[order], ids[order]
                    u, starts = np.unique(due, return_index=True)
                    for dd, part in zip(u, np.split(ids, starts[1:])):
                        pending.setdefault(int(dd), []).append(part)
            cust = np.concatenate([rep, new])
            counts[cust] += 1
            if i >= WARMUP:
                out_c.append(cust)
                out_new.append(np.r_[np.zeros(len(rep), bool), np.ones(n_new, bool)])
                out_idx.append(counts[cust].copy())
                out_day.append(np.full(len(cust), i - WARMUP, dtype=np.int32))
        self.q_repeat = q
        self.cust_counts_all = counts[:next_id]  # lifetime order count up to as_of (warm-up + window)
        self.cust_first_day = spent_first[:next_id] - WARMUP  # negative = before the window
        cust = np.concatenate(out_c)
        # shuffle within day so new and returning interleave (order ids follow time anyway)
        return cust, np.concatenate(out_new), np.concatenate(out_idx), np.concatenate(out_day), exp_orders[WARMUP:]

    # ---- orders
    def build_orders(self):
        t0 = time.time()
        p, rng = self.p, self.rng("orders")
        cust, is_new, oidx, day, exp = self.schedule_customers()
        n = len(cust)
        self.log(f"  customers scheduled: {n:,} orders in window, {len(self.cust_counts_all):,} customers ({time.time() - t0:.0f}s)")
        # time of day, then sort by timestamp so ids follow time
        hour = np.clip(rng.normal(14.5, 4.2, n), 0, 23.99)
        ts = self.day_epoch[day] + (hour * 3600).astype(np.int64)
        order = np.lexsort((ts,))
        cust, is_new, oidx, day, ts = cust[order], is_new[order], oidx[order], day[order], ts[order]
        o = {"cust": cust, "new": is_new, "oidx": oidx, "day": day, "ts": ts}
        # POS (owned retail) share: the brain's retail share of revenue, only after stores open
        open_day = (date.fromisoformat(PLACEHOLDERS["owned_retail_open"]) - self.start).days
        sm = p["sales_mix"]
        pos_share_rev = sm["owned_retail"] / (sm["dtc"] + sm["owned_retail"])
        last365 = day >= DAYS - 365
        open_frac = max(1, DAYS - max(open_day, DAYS - 365)) / 365
        pos_p = np.where(day >= open_day, pos_share_rev / open_frac, 0.0)
        pos = rng.random(n) < pos_p
        # acquisition channel: returning use a fixed mix; new take the rest of the overall mix per day
        ch = np.full(n, CH["pos"], dtype=np.int8)
        acq = p["acq_mix"]
        overall = np.array([acq["paid_social"], acq["paid_search"], acq["organic_search"], acq["direct"],
                            acq["email_sms"] * 0.8, acq["email_sms"] * 0.2, acq["other"]])
        ret_mix = np.array([RETURNING_MIX[c] for c in CHANNELS[:7]])
        web = ~pos
        rep_share = (~is_new & web).sum() / max(web.sum(), 1)
        new_mix = np.clip((overall - rep_share * ret_mix) / max(1 - rep_share, 1e-6), 0.004, None)
        new_mix /= new_mix.sum()
        u = rng.random(n)
        ch_new = np.searchsorted(np.cumsum(new_mix), u * 0.999999)
        ch_ret = np.searchsorted(np.cumsum(ret_mix), u * 0.999999)
        ch[web] = np.where(is_new[web], ch_new[web], ch_ret[web])
        o["ch"], o["pos"] = ch, pos
        self.mix_solved = {"new": dict(zip(CHANNELS[:7], np.round(new_mix, 4).tolist())),
                           "returning": dict(zip(CHANNELS[:7], ret_mix.tolist())), "repeat_share_web": round(float(rep_share), 4)}
        o["device"] = np.searchsorted(np.cumsum(list(PLACEHOLDERS["device_share"].values())), rng.random(n) * 0.999999).astype(np.int8)
        o["ready"] = web & (rng.random(n) < PLACEHOLDERS["journey_ready"])
        # GA4 tag capture drifts day to day (fix 14)
        lo, hi = PLACEHOLDERS["ga4_capture"]
        self.ga4_capture_day = self.rng("ga4_capture").uniform(lo, hi, DAYS)
        o["ga4"] = web & ((np.arange(n) * 2654435761 % 1000) < self.ga4_capture_day[day] * 1000)
        o["dtc_days"] = np.where(is_new, np.minimum(rng.geometric(0.35, n) - 1, 60), np.minimum(rng.geometric(0.6, n) - 1, 30)).astype(np.int16)
        o["dtc_days"][pos] = 0
        o["landing"] = np.zeros(n, dtype=np.int8)
        for c, pages in LANDING.items():
            m = ch == CH[c]
            o["landing"][m] = rng.integers(0, len(pages), m.sum())
        o["other_src"] = rng.integers(0, len(OTHER_SOURCES), n).astype(np.int8)
        o["state"] = np.searchsorted(np.cumsum([s[1] for s in STATES]), rng.random(n) * 0.999999).astype(np.int8)
        # stable state per customer: hash of customer id
        cust_state = np.searchsorted(np.cumsum([s[1] for s in STATES]), ((cust * 40503) % 10007) / 10007 * 0.999999)
        o["state"] = np.where(pos, 2, cust_state).astype(np.int8)  # POS stores in NY
        pm = np.searchsorted(np.cumsum(list(PLACEHOLDERS["payment_mix"].values())), rng.random(n) * 0.999999).astype(np.int8)
        o["pay"] = np.where(pos, 4, pm).astype(np.int8)
        self.o = o
        self.build_lines(rng)
        self.log(f"  orders and lines built: {n:,} orders, {len(self.l['order']):,} lines ({time.time() - t0:.0f}s)")

    def build_lines(self, rng):
        o, p = self.o, self.p
        n = len(o["cust"])
        pl = PLACEHOLDERS
        cats = np.array([c[1] for c in CATALOG])
        pop = np.array([c[5] for c in CATALOG], dtype=float)
        sock_like = np.isin(cats, SOCK_LIKE)
        # line weights so revenue by category hits the brain split
        w = pop.copy()
        for mask, share in ((sock_like, p["category_mix"]["socks_slippers"]), (~sock_like, p["category_mix"]["underwear_tshirts"])):
            rev = (pop[mask] * PRICE[mask]).sum()
            w[mask] = pop[mask] * share / rev
        w /= w.sum()
        qty_p = np.array([0.85, 0.12, 0.03])
        e_line = (w * PRICE).sum() * (qty_p * [1, 2, 3]).sum()
        # discount codes, per order, before the basket (the basket is solved against them)
        code = np.zeros(n, dtype=np.int8)  # 0 none, 1 first order, 2 repeat, 3 BFCM sitewide
        u = rng.random(n)
        web = ~o["pos"]
        code[web & o["new"] & (u < pl["first_order_code_use"])] = 1
        code[web & ~o["new"] & (u < pl["repeat_code_use"])] = 2
        bfcm_day = np.array([self.is_bfcm(d) for d in self.days])
        bf = web & bfcm_day[o["day"]]
        code[bf] = np.where(u[bf] < pl["bfcm_code_use"], 3, 0)  # fix 7: one sitewide code on those days
        pct = np.array([0, pl["first_order_code_pct"], pl["repeat_code_pct"], pl["bfcm_discount_pct"]])[code] / 100
        # basket size: Nov and Dec baskets are bigger (fix 6), then solve lines per order so the
        # mean net merchandise per order lands on the brain AOV: aov = e_line x (1 + lam) x mean(mult x (1 - pct))
        q4 = np.array([d.month in (11, 12) for d in self.days])[o["day"]]
        mult = np.where(q4, pl["q4_aov_mult"], 1.0)
        lam = max(p["aov"] / (e_line * float((mult * (1 - pct)).mean())) - 1, 0.0)
        lam_o = np.maximum((1 + lam) * mult - 1, 0.0)
        self.basket = {"lines_per_order": round(1 + lam, 4), "lines_per_order_q4": round((1 + lam) * pl["q4_aov_mult"], 4),
                       "expected_line_value": round(e_line, 2), "expected_discount": round(float(pct.mean()), 4)}
        nl = 1 + rng.poisson(lam_o)
        order_of_line = np.repeat(np.arange(n), nl)
        m = len(order_of_line)
        sku = np.searchsorted(np.cumsum(w), rng.random(m) * 0.999999).astype(np.int16)
        qty = (np.searchsorted(np.cumsum(qty_p), rng.random(m) * 0.999999) + 1).astype(np.int16)
        gross = PRICE[sku] * qty
        line_disc = r2(gross * pct[order_of_line])
        line_total = r2(gross - line_disc)
        unit_disc = r2(line_total / qty)
        starts = np.r_[0, np.cumsum(nl)[:-1]]
        sub = np.add.reduceat(line_total, starts)
        disc = np.add.reduceat(line_disc, starts)
        gross_o = np.add.reduceat(gross, starts)
        units = np.add.reduceat(qty.astype(np.int64), starts)
        items = np.add.reduceat((PAIRS[sku] * qty).astype(np.int64), starts)
        ship = np.where(o["pos"] | (sub >= PLACEHOLDERS["free_shipping_threshold_usd"]), 0.0, PLACEHOLDERS["shipping_fee_usd"])
        rate = np.array([s[2] for s in STATES])[o["state"]]
        tax = r2(sub * rate)
        o.update(code=code, gross=r2(gross_o), sub=r2(sub), disc=r2(disc), ship=ship, tax=tax, rate=rate,
                 total=r2(sub + ship + tax), units=units, items=items, line_start=starts, nl=nl)
        self.l = {"order": order_of_line, "sku": sku, "qty": qty, "unit_price": PRICE[sku], "unit_disc": unit_disc,
                  "line_total": line_total, "line_disc": line_disc, "cost": r2(PRICE[sku] * PLACEHOLDERS["cogs_share_of_price"]),
                  "qty_current": qty.copy()}

    # ---- attribution: Meta, Google, Klaviyo (subsets of orders, overlapping on purpose)
    def build_ads(self):
        rng = self.rng("meta_ads")
        ads = []
        active = []
        for di, d in enumerate(self.days):
            active = [a for a in active if a["end"] >= di]
            holiday = (d.month == 10 and d.day >= 15) or d.month in (11, 12)
            want = 25 + (6 if holiday else 0)
            while len(active) < want:
                camp = 3 if holiday and rng.random() < 0.25 else int(rng.choice([0, 0, 1, 1, 2]))
                life = int(np.clip(rng.lognormal(math.log(55), 0.5), 10, 200))
                start = di if di > 0 else -int(rng.integers(0, 60))
                end = min(start + life, di + life) if camp != 3 else min(start + life, di + max(1, (date(d.year, 12, 31) - d).days))
                fmt = str(rng.choice(["image", "video", "carousel"], p=[0.48, 0.35, 0.17]))
                a = {"idx": len(ads), "ad_id": f"MA-{len(ads) + 1:05d}", "camp": camp, "adset": f"MS-{camp + 1}-{int(rng.integers(1, 3))}",
                     "start": max(start, 0), "end": end, "fmt": fmt, "q": float(rng.lognormal(0, 0.45)),
                     "dynamic": bool(rng.random() < 0.15)}
                share = rng.random() < 0.12 and ads
                a["image_hash"] = ads[-1]["image_hash"] if share and fmt == "image" and ads[-1]["fmt"] == "image" else \
                    (hashlib.md5(a["ad_id"].encode()).hexdigest()[:16] if fmt != "video" else None)
                ads.append(a)
                active.append(a)
        self.ads = ads
        act = np.zeros((DAYS, len(ads)), dtype=bool)
        for a in ads:
            act[a["start"]:a["end"] + 1, a["idx"]] = True
        self.ad_active = act

    def attribute(self):
        o, rng = self.o, self.rng("attribution")
        n = len(o["cust"])
        ch, day = o["ch"], o["day"]
        # Meta: paid social orders carry the ad in utm_content
        self.build_ads()
        q = np.array([a["q"] for a in self.ads])
        o["meta_ad"] = np.full(n, -1, dtype=np.int32)
        o["meta_touch"] = np.zeros(n, dtype=np.int8)  # 1 click (7d_click), 2 view (1d_view)
        ps = np.flatnonzero(ch == CH["paid_social"])
        view_pool = np.flatnonzero(np.isin(ch, [CH["direct"], CH["organic_search"], CH["email"], CH["sms"], CH["other"]]))
        view = view_pool[rng.random(len(view_pool)) < PLACEHOLDERS["meta_view_credit_on_other_orders"]]
        for idxs, prosp_only in ((ps, False), (view, True)):
            dd = day[idxs]
            u = rng.random(len(idxs))
            res = np.empty(len(idxs), dtype=np.int32)
            order = np.argsort(dd, kind="stable")
            dsorted = dd[order]
            bounds = np.searchsorted(dsorted, np.arange(DAYS + 1))
            for di in range(DAYS):
                sl = order[bounds[di]:bounds[di + 1]]
                if not len(sl):
                    continue
                cand = np.flatnonzero(self.ad_active[di])
                if prosp_only:
                    cand = np.array([c for c in cand if self.ads[c]["camp"] in (0, 1)]) if len(cand) else cand
                wt = q[cand] / q[cand].sum()
                res[sl] = cand[np.searchsorted(np.cumsum(wt), u[sl] * 0.999999)]
            if not prosp_only:
                o["meta_ad"][idxs] = res
                o["meta_touch"][idxs] = np.where(rng.random(len(idxs)) < PLACEHOLDERS["meta_click_credit"], 1, 0)
            else:
                o["meta_ad"][idxs] = res
                o["meta_touch"][idxs] = 2
        o["meta_utm"] = ch == CH["paid_social"]  # meta_ad is also the utm ad for these
        # Google
        o["g_camp"] = np.full(n, -1, dtype=np.int8)
        o["g_credit"] = np.zeros(n, dtype=bool)
        gs = np.flatnonzero(ch == CH["paid_search"])
        gw = np.cumsum([c[4] for c in GOOGLE_CAMPAIGNS])
        o["g_camp"][gs] = np.searchsorted(gw, rng.random(len(gs)) * 0.999999)
        o["g_credit"][gs] = rng.random(len(gs)) < PLACEHOLDERS["google_credit"]
        o["g_term"] = np.full(n, -1, dtype=np.int8)
        for ci, key in ((0, "GC-1"), (1, "GC-2")):
            m = gs[o["g_camp"][gs] == ci]
            terms = SEARCH_TERMS[key]
            tw = 1 / np.arange(1, len(terms) + 1) ** 1.1
            o["g_term"][m] = np.searchsorted(np.cumsum(tw / tw.sum()), rng.random(len(m)) * 0.999999)
        for cname, share in PLACEHOLDERS["google_brand_overlap"].items():
            pool = np.flatnonzero(ch == CH[cname])
            hit = pool[rng.random(len(pool)) < share]
            o["g_camp"][hit] = 0
            o["g_credit"][hit] = True
        # Klaviyo: message index; flows 0..len(FLOW_MSG)-1, campaigns offset by 1000
        self.build_campaign_calendar()
        o["k_msg"] = np.full(n, -1, dtype=np.int32)
        pools = [np.flatnonzero(np.isin(ch, [CH["email"], CH["sms"]]))]
        for cname, share in PLACEHOLDERS["klaviyo_overlap"].items():
            pool = np.flatnonzero(ch == CH[cname])
            pools.append(pool[rng.random(len(pool)) < share])
        kl = np.sort(np.concatenate(pools))
        new = o["new"][kl]
        is_sms_ch = ch[kl] == CH["sms"]
        u = rng.random(len(kl))
        # flow choice by customer state; campaign choice by recent send
        flow_new = np.array([0, 1, 2, 3, 4], dtype=np.int32)   # welcome x3, abandoned x2
        flow_new_w = np.cumsum([0.30, 0.15, 0.10, 0.28, 0.17])
        flow_ret = np.array([3, 4, 5, 6, 7, 8], dtype=np.int32)  # abandoned, browse, post-purchase, replenish, winback
        flow_ret_w = np.cumsum([0.30, 0.12, 0.15, 0.13, 0.18, 0.12])
        msg = np.where(new, flow_new[np.searchsorted(flow_new_w, u * 0.999999)],
                       flow_ret[np.searchsorted(flow_ret_w, u * 0.999999)])
        sms_msgs = np.array([m for m, f in enumerate(FLOW_MSG) if f[3][1] == "sms"])
        # campaigns: half of non-welcome attributed orders go to a campaign sent in the last 5 days
        use_camp = (~new | (rng.random(len(kl)) < 0.3)) & (rng.random(len(kl)) < 0.5)
        dk = o["day"][kl]
        camp_choice = np.full(len(kl), -1, dtype=np.int32)
        for di in np.unique(dk[use_camp]):
            live = self.camp_live.get(int(di), [])
            if not live:
                continue
            sel = np.flatnonzero(use_camp & (dk == di))
            camp_choice[sel] = np.array(live)[rng.integers(0, len(live), len(sel))]
        msg = np.where(camp_choice >= 0, 1000 + camp_choice, msg)
        # sms channel orders go to an sms message when the flow has one
        flip = is_sms_ch & (msg < 1000) & ~np.isin(msg, sms_msgs)
        msg[flip] = np.where(new[flip], 2, 4)
        o["k_msg"][kl] = msg

    def build_campaign_calendar(self):
        rng = self.rng("klaviyo_campaigns")
        camps, live = [], {}
        subjects = ["New colors are in", "Built for the long run", "Cold mornings, warm feet", "Gift the pair they will wear",
                    "Last call for holiday delivery", "Restock: best sellers", "A sock for every sport", "One purchased, one donated"]
        for di, d in enumerate(self.days):
            holiday = d.month in (11, 12) and d.day <= 20
            send = d.weekday() in (1, 3, 5) or (holiday and d.weekday() != 6)
            if not send:
                continue
            channel = "sms" if rng.random() < 0.2 else "email"
            c = {"idx": len(camps), "id": f"KC-{len(camps) + 1:04d}", "day": di, "channel": channel,
                 "name": f"{d.isoformat()} {subjects[len(camps) % len(subjects)]}", "subject": subjects[len(camps) % len(subjects)],
                 "strategy": "static" if rng.random() < 0.8 else "smart_send_time",
                 "audience": "Engaged 90d" if rng.random() < 0.7 else "All subscribers", "smart_sending": bool(rng.random() < 0.9)}
            camps.append(c)
            for k in range(5):
                if di + k < DAYS:
                    live.setdefault(di + k, []).append(c["idx"])
        self.campaigns, self.camp_live = camps, live

    # ---- reversed orders, refunds
    def build_reversed(self):
        o, l, rng = self.o, self.l, self.rng("reversed")
        n = len(o["cust"])
        pl = PLACEHOLDERS
        web = np.flatnonzero(~o["pos"])
        rows = []
        o["refund"] = np.zeros(n)
        refund_day = np.full(n, -1, dtype=np.int32)
        as_of_day = DAYS - 1
        # returns: one line back per return
        ret = web[rng.random(len(web)) < pl["return_rate"]]
        open_d = o["day"][ret] + 4 + np.ceil(rng.lognormal(math.log(10), 0.6, len(ret))).astype(int)
        keep = open_d <= as_of_day
        ret, open_d = ret[keep], open_d[keep]
        close_d = open_d + rng.integers(4, 11, len(ret))
        pick = o["line_start"][ret] + (rng.random(len(ret)) * o["nl"][ret]).astype(int)
        amount = r2(l["line_total"][pick] * (1 + o["rate"][ret]))
        outcome = np.array(["refunded", "exchanged", "declined"])[np.searchsorted([0.70, 0.95, 1.0], rng.random(len(ret)))]
        closed = close_d <= as_of_day
        outcome = np.where(closed, outcome, None)
        refunded = closed & (outcome == "refunded")
        o["refund"][ret[refunded]] += amount[refunded]
        refund_day[ret[refunded]] = close_d[refunded]
        l["qty_current"][pick[refunded | (closed & (outcome == "exchanged"))]] = 0
        reasons = np.array(["size or fit", "changed mind", "hole or defect", "wrong item", "arrived late"])
        rsn = reasons[np.searchsorted([0.42, 0.66, 0.84, 0.94, 1.0], rng.random(len(ret)))]
        self.rev = {"return": dict(idx=ret, open=open_d, close=np.where(closed, close_d, -1), amount=amount, outcome=outcome,
                                   reason=rsn, line=pick)}
        # carrier returned: whole order back, excluded from return_rate
        cr = web[rng.random(len(web)) < pl["carrier_return_rate"]]
        cr = cr[~np.isin(cr, ret)]
        c_open = o["day"][cr] + rng.integers(8, 20, len(cr))
        keep = c_open <= as_of_day
        cr, c_open = cr[keep], c_open[keep]
        c_close = np.minimum(c_open + 3, as_of_day)
        o["refund"][cr] += o["total"][cr]
        refund_day[cr] = c_close
        cr_lines = np.concatenate([np.arange(o["line_start"][i], o["line_start"][i] + o["nl"][i]) for i in cr]) if len(cr) else np.zeros(0, int)
        l["qty_current"][cr_lines] = 0
        self.rev["carrier"] = dict(idx=cr, open=c_open, close=c_close, amount=o["total"][cr])
        # chargebacks: Shopify Payments orders only
        sp = web[o["pay"][web] != 3]
        cb = sp[rng.random(len(sp)) < pl["chargeback_rate"]]
        cb = cb[~np.isin(cb, np.r_[ret, cr])]
        cb_open = o["day"][cb] + rng.integers(20, 61, len(cb))
        keep = cb_open <= as_of_day
        cb, cb_open = cb[keep], cb_open[keep]
        cb_close = cb_open + rng.integers(30, 76, len(cb))
        closed = cb_close <= as_of_day
        won = rng.random(len(cb)) < 0.4
        cb_out = np.where(closed, np.where(won, "won", "lost"), "needs_response")
        cb_type = np.where(rng.random(len(cb)) < 0.8, "chargeback", "inquiry")
        self.rev["chargeback"] = dict(idx=cb, open=cb_open, close=np.where(closed, cb_close, -1), amount=o["total"][cb],
                                      outcome=cb_out, type=cb_type,
                                      reason=np.array(["fraudulent", "product_not_received", "unrecognized", "product_unacceptable"])[
                                          rng.integers(0, 4, len(cb))])
        o["refund"] = r2(o["refund"])
        o["refund_day"] = refund_day
        o["total_current"] = r2(o["total"] - o["refund"])

    # ---- write
    def write_sqlite(self, path):
        t0 = time.time()
        if path.exists():
            path.unlink()
        db = sqlite3.connect(path)
        db.execute("PRAGMA journal_mode=OFF")
        db.execute("PRAGMA synchronous=OFF")
        self.db = db
        self.counts = {}
        for name, fn in [("orders", self.t_orders), ("order_lines", None), ("customers", self.t_customers),
                         ("products", self.t_products), ("inventory", self.t_inventory), ("inbound_pos", None),
                         ("reversed_orders", self.t_reversed), ("payouts", self.t_payouts),
                         ("abandoned_checkouts", self.t_abandoned), ("sessions", self.t_sessions), ("ad_rows", self.t_ad_rows),
                         ("google_rows", self.t_google_rows), ("flows", self.t_flows), ("campaign_sends", None),
                         ("tickets", self.t_tickets), ("reviews", self.t_reviews), ("speed_runs", self.t_fixtures),
                         ("content_posts", None), ("search_console", None), ("marketplace_listings", None),
                         ("wholesale_sell_in", self.t_wholesale), ("marketplace_sales", self.t_marketplace),
                         ("paid_other_spend", self.t_paid_other)]:
            if fn:
                fn()
                db.commit()
                self.log(f"  wrote {name:22s} ({time.time() - t0:.0f}s)")
        for idx in ["CREATE INDEX ix_orders_created ON orders(created_at)", "CREATE INDEX ix_orders_customer ON orders(customer_id)",
                    "CREATE INDEX ix_lines_order ON order_lines(order_id)", "CREATE INDEX ix_sessions_date ON sessions(date)",
                    "CREATE INDEX ix_ad_rows_date ON ad_rows(date)", "CREATE INDEX ix_rev_order ON reversed_orders(order_id)",
                    "CREATE INDEX ix_tickets_order ON tickets(order_id)"]:
            db.execute(idx)
        db.commit()
        db.close()

    def insert(self, table, cols, rows, types=None):
        """cols: list of names; rows: iterable of tuples. Common columns are appended here."""
        first = table not in self.counts
        if first:
            common = {"brand": "TEXT", "simulated": "INTEGER", "source": "TEXT", "captured_at": "TEXT"}
            spec = ", ".join(f'"{c}" {(types or {}).get(c, "")}'.strip() for c in cols)
            spec += ", " + ", ".join(f"{k} {v}" for k, v in common.items())
            self.db.execute(f"CREATE TABLE {table} ({spec})")
            self.counts[table] = 0
        src = SOURCE.get(table, "generator")
        tail = (self.brand, 1, src, self.captured_at)
        q = f"INSERT INTO {table} VALUES ({', '.join('?' * (len(cols) + 4))})"
        batch = []
        for r in rows:
            batch.append(r + tail)
            if len(batch) >= 200_000:
                self.db.executemany(q, batch)
                self.counts[table] += len(batch)
                batch = []
        if batch:
            self.db.executemany(q, batch)
            self.counts[table] += len(batch)

    def ensure_table(self, table, cols, types=None):
        if table not in self.counts:
            self.insert(table, cols, [], types)

    def order_ids(self):
        return 5_000_000 + np.arange(len(self.o["cust"]), dtype=np.int64)

    def cust_ids(self, c):
        return 70_000_000 + np.asarray(c, dtype=np.int64)

    def insert_cols(self, table, cols, arrays, types=None, chunk=400_000):
        """Insert column arrays in chunks so scale 1.0 stays in memory."""
        n = len(arrays[0]) if arrays else 0
        if n == 0:
            self.insert(table, cols, [], types)
        for a in range(0, n, chunk):
            parts = [(x[a:a + chunk].tolist() if isinstance(x, np.ndarray) else x[a:a + chunk]) for x in arrays]
            self.insert(table, cols, zip(*parts), types)

    def t_orders(self):
        n = len(self.o["cust"])
        all_ids = self.order_ids()
        step = 400_000
        for a in range(0, n, step):
            o = {k: v[a:a + step] for k, v in self.o.items()}
            self.orders_chunk(o, all_ids[a:a + step])
        l, o = self.l, self.o
        cols = ["order_id", "line_no", "sku", "qty", "qty_current", "unit_price", "unit_price_discounted", "line_total", "line_discount", "cost"]
        line_no = np.arange(len(l["order"])) - o["line_start"][l["order"]] + 1
        self.insert_cols("order_lines", cols, [
            all_ids[l["order"]], line_no, np.array(SKUS, dtype=object)[l["sku"]], l["qty"], l["qty_current"], l["unit_price"],
            l["unit_disc"], l["line_total"], l["line_disc"], l["cost"]],
            {"order_id": "INTEGER", "line_no": "INTEGER", "qty": "INTEGER", "qty_current": "INTEGER", "unit_price": "REAL",
             "unit_price_discounted": "REAL", "line_total": "REAL", "line_discount": "REAL", "cost": "REAL"})

    def orders_chunk(self, o, ids):
        n = len(ids)
        created = iso_utc(o["ts"])
        ch = o["ch"]
        chan_name = np.array(CHANNELS)
        source_name = np.where(o["pos"], "pos", "web")
        ready = o["ready"]
        # utm per channel
        utm_src = np.full(n, None, dtype=object)
        utm_med = np.full(n, None, dtype=object)
        utm_camp = np.full(n, None, dtype=object)
        utm_cont = np.full(n, None, dtype=object)
        utm_term = np.full(n, None, dtype=object)
        m = ch == CH["paid_social"]
        utm_src[m] = np.where((o["cust"][m] % 10) < 7, "facebook", "instagram")
        utm_med[m] = "paid_social"
        ad = o["meta_ad"][m]
        camp_of_ad = np.array([a["camp"] for a in self.ads])
        utm_camp[m] = np.array([c[1] for c in META_CAMPAIGNS], dtype=object)[camp_of_ad[ad]]
        utm_cont[m] = np.array([a["ad_id"] for a in self.ads], dtype=object)[ad]
        m = ch == CH["paid_search"]
        utm_src[m], utm_med[m] = "google", "cpc"
        utm_camp[m] = np.array([c[1] for c in GOOGLE_CAMPAIGNS], dtype=object)[o["g_camp"][m]]
        for ci, key in ((0, "GC-1"), (1, "GC-2")):
            mm = m & (o["g_camp"] == ci) & (o["g_term"] >= 0)
            utm_term[mm] = np.array(SEARCH_TERMS[key], dtype=object)[o["g_term"][mm]]
        names = [f[3][2] for f in FLOW_MSG]
        for cname in ("email", "sms"):
            m = ch == CH[cname]
            utm_src[m], utm_med[m] = "klaviyo", cname
            km = o["k_msg"][m]
            utm_camp[m] = [(self.campaigns[k - 1000]["name"] if k >= 1000 else names[k]) if k >= 0 else None for k in km]
        m = ch == CH["other"]
        utm_src[m] = np.array([s[0] for s in OTHER_SOURCES], dtype=object)[o["other_src"][m]]
        utm_med[m] = np.array([s[1] for s in OTHER_SOURCES], dtype=object)[o["other_src"][m]]
        for arr in (utm_src, utm_med, utm_camp, utm_cont, utm_term):
            arr[~ready] = None
        landing = np.full(n, None, dtype=object)
        referrer = np.full(n, None, dtype=object)
        for c, pages in LANDING.items():
            mm = ch == CH[c]
            landing[mm] = np.array(pages, dtype=object)[o["landing"][mm]]
        referrer[ch == CH["organic_search"]] = "https://www.google.com/"
        referrer[ch == CH["paid_search"]] = "https://www.google.com/"
        referrer[ch == CH["paid_social"]] = np.where((o["cust"][ch == CH["paid_social"]] % 10) < 7, "https://m.facebook.com/", "https://l.instagram.com/")
        landing[~ready] = None
        referrer[~ready] = None
        first_visit = np.where(ready, iso_utc(o["ts"] - o["dtc_days"].astype(np.int64) * 86400 - 1800), None)
        last_visit = np.where(ready, iso_utc(o["ts"] - 600), None)
        dtc = np.where(ready, o["dtc_days"], None)
        idx = np.where(ready | o["pos"], o["oidx"], None)
        codes = np.array([None, '["FIRSTORDER20"]', '["THANKS10"]', '["BFCM20"]'], dtype=object)[o["code"]]
        st = [s[0] for s in STATES]
        tax_json = [None] * n
        tl = o["tax"].tolist()
        rl = o["rate"].tolist()
        sl = o["state"].tolist()
        for i in range(n):
            s = st[sl[i]]
            tax_json[i] = f'[{{"title":"{s} State Tax","rate":{rl[i]},"amount":{tl[i]},"channel_liable":false}}]'
        pay = np.array(PAYMENTS, dtype=object)[o["pay"]]
        cols = ["id", "created_at", "customer_id", "channel", "acquisition_channel", "subtotal", "discount", "discount_codes",
                "shipping", "tax", "tax_lines", "total", "total_current", "refunds", "utm_source", "utm_medium", "utm_campaign",
                "utm_content", "utm_term", "landing_page", "referrer", "first_visit_at", "last_visit_at", "days_to_conversion",
                "order_index", "journey_ready", "status", "payment_method", "units", "giving_units"]
        types = {"id": "INTEGER PRIMARY KEY", "customer_id": "INTEGER", "subtotal": "REAL", "discount": "REAL", "shipping": "REAL",
                 "tax": "REAL", "total": "REAL", "total_current": "REAL", "refunds": "REAL", "days_to_conversion": "INTEGER",
                 "order_index": "INTEGER", "journey_ready": "INTEGER", "units": "INTEGER", "giving_units": "INTEGER"}
        status = np.where(o["refund"] >= o["total"] - 0.005, "refunded", np.where(o["refund"] > 0, "partially_refunded", "paid"))
        acq = chan_name[ch]
        journey_ready = np.where(o["pos"], None, ready.astype(int))
        self.insert("orders", cols, zip(
            ids.tolist(), created.tolist(), self.cust_ids(o["cust"]).tolist(), source_name.tolist(), acq.tolist(),
            o["gross"].tolist(), o["disc"].tolist(), codes.tolist(), o["ship"].tolist(), tl, tax_json, o["total"].tolist(),
            o["total_current"].tolist(), o["refund"].tolist(), utm_src.tolist(), utm_med.tolist(), utm_camp.tolist(),
            utm_cont.tolist(), utm_term.tolist(), landing.tolist(), referrer.tolist(), first_visit.tolist(), last_visit.tolist(),
            dtc.tolist(), idx.tolist(), journey_ready.tolist(), status.tolist(), pay.tolist(), o["units"].tolist(), o["items"].tolist()), types)

    def t_customers(self):
        o, rng = self.o, self.rng("customers_table")
        c = np.unique(o["cust"])
        spent_window = np.bincount(o["cust"], weights=o["total_current"], minlength=len(self.cust_counts_all))
        count = self.cust_counts_all[c]
        win_count = np.bincount(o["cust"], minlength=len(self.cust_counts_all))[c]
        # lifetime spend: window spend plus pre-window orders at the brand AOV (with tax and shipping)
        pre = count - win_count
        total_spent = r2(spent_window[c] + pre * self.p["aov"] * 1.07)
        fd = self.cust_first_day[c]
        first_epoch = int(self.day_epoch[0]) + fd.astype(np.int64) * 86400 + 15 * 3600
        u = rng.random(len(c))
        email = np.where(u < PLACEHOLDERS["email_consent"], "SUBSCRIBED", np.where(u < 0.9, "NOT_SUBSCRIBED", "UNSUBSCRIBED"))
        level = np.where(email == "SUBSCRIBED", np.where(rng.random(len(c)) < 0.8, "SINGLE_OPT_IN", "CONFIRMED_OPT_IN"), None)
        consent_at = np.where(email != "NOT_SUBSCRIBED", iso_utc(first_epoch + 60), None)
        sms = np.where(rng.random(len(c)) < PLACEHOLDERS["sms_consent"], "SUBSCRIBED", "NOT_SUBSCRIBED")
        self.insert_cols("customers", ["id", "orders_count", "total_spent", "first_order_at", "email_consent", "email_opt_in_level",
                                       "email_consent_at", "sms_consent", "state"],
                         [self.cust_ids(c), count, total_spent, iso_utc(first_epoch), email, level, consent_at, sms,
                          np.full(len(c), None, dtype=object)],
                    {"id": "INTEGER PRIMARY KEY", "orders_count": "INTEGER", "total_spent": "REAL"})
        self.email_subscribers = int((email == "SUBSCRIBED").sum())

    def sku_units(self, days_from=0):
        o, l = self.o, self.l
        m = o["day"][l["order"]] >= days_from
        return np.bincount(l["sku"][m], weights=l["qty"][m], minlength=len(SKUS)), \
            np.bincount(l["sku"][m], weights=l["line_total"][m], minlength=len(SKUS))

    def t_products(self):
        rng = self.rng("products")
        units, rev = self.sku_units(DAYS - 28)
        views = np.round(units / 0.045 * rng.uniform(0.8, 1.2, len(SKUS)))
        adds = np.round(units / 0.36)
        checkouts = np.round(units / 0.62)
        cats = [c[1] for c in CATALOG]
        stock = self.stock_end if hasattr(self, "stock_end") else [None] * len(SKUS)
        self.insert("products", ["sku", "title", "category", "price", "compare_at_price", "stock", "tracked", "cost", "items_per_unit",
                                 "views", "adds", "checkouts", "purchased", "item_revenue", "cart_to_view", "purchase_to_view",
                                 "ga4_window_days", "type", "weight", "images"],
                    [(s, CATALOG[i][2], cats[i], float(PRICE[i]), None, stock[i], 1, r2(PRICE[i] * PLACEHOLDERS["cogs_share_of_price"]).item(),
                      int(PAIRS[i]), int(views[i]), int(adds[i]), int(checkouts[i]), int(units[i]), float(r2(rev[i])),
                      float(round(adds[i] / views[i], 4)) if views[i] else None, float(round(units[i] / views[i], 4)) if views[i] else None,
                      28, None, None, None) for i, s in enumerate(SKUS)],
                    {"price": "REAL", "cost": "REAL", "stock": "INTEGER"})

    def t_inventory(self):
        o, l, rng = self.o, self.l, self.rng("inventory")
        daily = np.zeros((DAYS, len(SKUS)))
        np.add.at(daily, (o["day"][l["order"]], l["sku"]), l["qty"])
        locs = [("LOC-EAST", "3PL East", 0.55), ("LOC-WEST", "3PL West", 0.45)]
        rows, pos_rows = [], []
        stock_end = np.zeros(len(SKUS), dtype=int)
        po_n = 0
        for li, (lid, lname, share) in enumerate(locs):
            dem = daily * share
            avg = np.maximum(dem[:60].mean(axis=0), 0.2)
            on_hand = np.round(avg * 90).astype(float)
            incoming = {}  # day -> array
            open_units = np.zeros(len(SKUS))
            for di in range(DAYS):
                arr = incoming.pop(di, None)
                if arr is not None:
                    on_hand += arr
                    open_units -= arr
                sold = np.round(dem[di])
                on_hand = np.maximum(on_hand - sold, 0)
                recent = np.maximum(dem[max(0, di - 28):di + 1].mean(axis=0), 0.2)
                cover = (on_hand + open_units) / recent
                need = cover < 50
                if need.any():
                    q = np.where(need, np.round(recent * 120), 0)
                    eta = di + int(rng.integers(45, 75))
                    incoming[eta] = incoming.get(eta, 0) + q
                    open_units += q
                    for s in np.flatnonzero(need):
                        po_n += 1
                        pos_rows.append((f"PO-{po_n:06d}", SKUS[s], lid, int(q[s]), self.days[di].isoformat(),
                                         (self.start + timedelta(days=eta)).isoformat(), "received" if eta <= DAYS - 1 else "open"))
                committed = np.minimum(np.round(sold * 0.4), on_hand)
                d = self.days[di].isoformat()
                for s in range(len(SKUS)):
                    rows.append((d, SKUS[s], lid, int(on_hand[s] - committed[s]), int(on_hand[s]), int(open_units[s]), int(committed[s]), 1))
            stock_end += (on_hand).astype(int)
        self.stock_end = stock_end.tolist()
        self.insert("inventory", ["date", "sku", "location_id", "available", "on_hand", "incoming", "committed", "tracked"], rows)
        self.insert("inbound_pos", ["po_id", "sku", "location_id", "qty", "ordered_on", "eta", "status"], pos_rows)

    def t_reversed(self):
        o, rv = self.o, self.rev
        ids = self.order_ids()
        rows = []
        ep = self.day_epoch

        def ts(d):
            return iso_utc(ep[np.asarray(d)] + 16 * 3600).tolist() if len(d) else []

        r = rv["return"]
        closes = [None if c < 0 else x for c, x in zip(r["close"].tolist(), ts(np.maximum(r["close"], 0)))]
        rows += list(zip(ids[r["idx"]].tolist(), ["return"] * len(r["idx"]), r["reason"].tolist(), r["amount"].tolist(),
                         ts(r["open"]), closes, r["outcome"].tolist()))
        c = rv["carrier"]
        rows += list(zip(ids[c["idx"]].tolist(), ["return"] * len(c["idx"]), ["carrier_returned"] * len(c["idx"]),
                         c["amount"].tolist(), ts(c["open"]), ts(c["close"]), ["refunded"] * len(c["idx"])))
        b = rv["chargeback"]
        closes = [None if x < 0 else y for x, y in zip(b["close"].tolist(), ts(np.maximum(b["close"], 0)))]
        rows += list(zip(ids[b["idx"]].tolist(), b["type"].tolist(), b["reason"].tolist(), b["amount"].tolist(), ts(b["open"]),
                         closes, b["outcome"].tolist()))
        rows.sort(key=lambda x: (x[4], x[0]))
        self.insert("reversed_orders", ["order_id", "type", "reason", "amount", "opened_at", "closed_at", "outcome"], rows,
                    {"order_id": "INTEGER", "amount": "REAL"})

    def t_payouts(self):
        o, rv = self.o, self.rev
        lag = PLACEHOLDERS["payout_lag_days"]
        sp = o["pay"] != 3
        nd = DAYS + lag
        fee_rate = np.where(o["pos"], PLACEHOLDERS["fee_pos"][0], PLACEHOLDERS["fee_online"][0])
        fee_fix = np.where(o["pos"], PLACEHOLDERS["fee_pos"][1], PLACEHOLDERS["fee_online"][1])
        fees = r2(o["total"] * fee_rate + fee_fix)
        pd = o["day"] + lag
        gross = np.bincount(pd[sp], weights=o["total"][sp], minlength=nd)
        fee = np.bincount(pd[sp], weights=fees[sp], minlength=nd)
        cnt = np.bincount(pd[sp], minlength=nd)
        rd = o["refund_day"]
        rm = sp & (rd >= 0)
        refunds = np.bincount(rd[rm] + lag, weights=o["refund"][rm], minlength=nd)
        b = rv["chargeback"]
        adj = np.zeros(nd)
        np.add.at(adj, b["open"] + lag, -(b["amount"] + PLACEHOLDERS["chargeback_fee_usd"]))
        won = b["outcome"] == "won"
        np.add.at(adj, b["close"][won] + lag, b["amount"][won])
        net = r2(gross) - r2(fee) - r2(refunds) + r2(adj)
        rows = []
        for k in range(lag, nd):
            dd = self.start + timedelta(days=k)
            summary = js({"charges_gross": float(r2(gross[k])), "charges_fee": float(r2(fee[k])), "charges_count": int(cnt[k]),
                          "refunds_gross": float(-r2(refunds[k])), "adjustments_gross": float(r2(adj[k]))})
            rows.append((f"PO-{dd.strftime('%Y%m%d')}", dd.isoformat(), "paid" if k <= DAYS - 1 else "scheduled",
                         float(r2(net[k])), float(r2(gross[k])), float(r2(fee[k])), float(-r2(refunds[k])), float(r2(adj[k])), summary, "USD"))
        self.insert("payouts", ["id", "issued_at", "status", "net", "charges_gross", "charges_fee", "refunds_gross",
                                "adjustments_gross", "summary", "currency"], rows,
                    {"net": "REAL", "charges_gross": "REAL", "charges_fee": "REAL", "refunds_gross": "REAL", "adjustments_gross": "REAL"})
        self.payout_totals = {"gross": float(r2(gross.sum())), "fees": float(r2(fee.sum())), "refunds": float(r2(refunds.sum())),
                              "adjustments": float(r2(adj.sum()))}

    def t_abandoned(self):
        o, rng = self.o, self.rng("abandoned")
        web_days = o["day"][~o["pos"]]
        per_day = np.bincount(web_days, minlength=DAYS)
        n_ab = rng.poisson(per_day * PLACEHOLDERS["abandoned_per_web_order"])
        day = np.repeat(np.arange(DAYS), n_ab)
        n = len(day)
        ts = self.day_epoch[day] + (np.clip(rng.normal(15, 4.5, n), 0, 23.99) * 3600).astype(np.int64)
        known = rng.random(n) < 0.6
        pool = o["cust"]
        cust = np.where(known, self.cust_ids(pool[rng.integers(0, len(pool), n)]), None)
        sku1 = rng.integers(0, len(SKUS), n)
        two = rng.random(n) < 0.35
        sku2 = rng.integers(0, len(SKUS), n)
        total = PRICE[sku1] + np.where(two, PRICE[sku2], 0)
        codes = np.where(rng.random(n) < 0.3, '["FIRSTORDER20"]', None)
        tax = r2(total * 0.06)
        ids = 9_000_000 + np.arange(n)
        sk = np.array(SKUS)
        lines = [f'[{{"sku":"{a}","qty":1}}' + (f',{{"sku":"{b}","qty":1}}]' if t else "]")
                 for a, b, t in zip(sk[sku1].tolist(), sk[sku2].tolist(), two.tolist())]
        self.insert_cols("abandoned_checkouts", ["id", "created_at", "customer_id", "abandoned_checkout_url", "lines", "discount_codes",
                                                 "tax_lines", "total"],
                         [ids, iso_utc(ts), cust, [f"simulated://checkouts/{i}" for i in ids.tolist()], lines,
                          codes, [f'[{{"title":"Sales Tax","rate":0.06,"amount":{t}}}]' for t in tax.tolist()], r2(total + tax)],
                         {"id": "INTEGER", "total": "REAL"})

    def ga4_dims(self):
        """Per order: (source, medium, campaign, channel_group) index into a dimension list."""
        o = self.o
        n = len(o["cust"])
        dims, key = [], {}

        def dim(t):
            if t not in key:
                key[t] = len(dims)
                dims.append(t)
            return key[t]

        out = np.full(n, -1, dtype=np.int32)
        ch = o["ch"]
        m = ch == CH["paid_social"]
        camp_of_ad = np.array([a["camp"] for a in self.ads])
        cam = np.where(o["meta_ad"] >= 0, camp_of_ad[np.maximum(o["meta_ad"], 0)], -1)
        for ci, (cid, cname) in enumerate(META_CAMPAIGNS):
            for fb in (True, False):
                mm = m & (cam == ci) & (((o["cust"] % 10) < 7) == fb)
                out[mm] = dim(("facebook" if fb else "instagram", "paid_social", cname, "Paid Social"))
        m = ch == CH["paid_search"]
        groups = {"SEARCH": "Paid Search", "PERFORMANCE_MAX": "Cross-network", "DEMAND_GEN": "Paid Video"}
        for ci, c in enumerate(GOOGLE_CAMPAIGNS):
            out[m & (o["g_camp"] == ci)] = dim(("google", "cpc", c[1], groups[c[2]]))
        out[ch == CH["organic_search"]] = dim(("google", "organic", "(organic)", "Organic Search"))
        out[ch == CH["direct"]] = dim(("(direct)", "(none)", "(direct)", "Direct"))
        for cname, grp in (("email", "Email"), ("sms", "SMS")):
            mm = ch == CH[cname]
            kc = o["k_msg"] >= 1000
            out[mm & kc] = dim(("klaviyo", cname, "campaign", grp))
            out[mm & ~kc] = dim(("klaviyo", cname, "flow", grp))
        for si, s in enumerate(OTHER_SOURCES):
            out[(ch == CH["other"]) & (o["other_src"] == si)] = dim((s[0], s[1], "(referral)", s[2]))
        return out, dims

    def t_sessions(self):
        o, rng = self.o, self.rng("sessions")
        dim_idx, dims = self.ga4_dims()
        m = o["ga4"]
        nl = max(len(p) for p in LANDING.values())
        key = ((o["day"].astype(np.int64) * len(dims) + dim_idx) * nl + o["landing"]) * 3 + o["device"]
        key = key * 2 + (~o["new"]).astype(np.int64)
        k = key[m]
        uk, inv = np.unique(k, return_inverse=True)
        tx = np.bincount(inv)
        rev = np.bincount(inv, weights=o["total"][m])
        # decode
        nvr = uk % 2
        rest = uk // 2
        dev = rest % 3
        rest //= 3
        land = rest % nl
        rest //= nl
        di = rest % len(dims)
        day = rest // len(dims)
        # channel for each dim (cvr lookup)
        chs = o["ch"][m]
        first = np.unique(inv, return_index=True)[1]
        chan = chs[first]
        cvr = np.array([PLACEHOLDERS["cvr_by_channel"][CHANNELS[c]] for c in chan]) * \
            np.array(list(PLACEHOLDERS["cvr_device_mult"].values()))[dev] * np.where(nvr == 1, 1.6, 0.8)
        # Fix 3: scale every channel rate by one factor so GA4 sessions over the last 12 months average
        # site_sessions_monthly x scale; the channel and device shape stays the placeholder's
        last = day >= DAYS - 365
        want = self.p["sessions_monthly"] * 12 * self.scale
        self.cvr_scale = float((tx[last] / cvr[last]).sum() / want) if want else 1.0
        cvr = np.minimum(cvr * self.cvr_scale, 0.9)
        self.cvr_solved = {c: round(v * self.cvr_scale, 4) for c, v in PLACEHOLDERS["cvr_by_channel"].items()}
        sessions = np.maximum(tx, rng.poisson(tx / cvr))
        engaged = np.round(sessions * rng.uniform(0.55, 0.7, len(uk)))
        users = np.round(sessions * 0.82)
        new_users = np.where(nvr == 0, users, 0)
        pv = np.round(sessions * rng.uniform(1.1, 1.5, len(uk)))
        atc = np.maximum(np.round(tx / 0.30 * rng.uniform(0.9, 1.1, len(uk))), tx)
        chk = np.maximum(np.round(tx / 0.55 * rng.uniform(0.9, 1.1, len(uk))), tx)
        landing_names = {c: p for c, p in LANDING.items()}
        land_str = [landing_names[CHANNELS[c]][l] if l < len(landing_names[CHANNELS[c]]) else None for c, l in zip(chan.tolist(), land.tolist())]
        dates = [self.days[d].isoformat() for d in day.tolist()]
        dimrows = [dims[i] for i in di.tolist()]
        self.insert("sessions", ["date", "session_source", "session_medium", "session_campaign", "channel_group", "landing_page", "device", "new_vs_returning",
                                 "sessions", "engaged_sessions", "users", "new_users", "product_view", "add_to_cart", "checkout",
                                 "purchase", "transactions", "revenue", "sampled", "thresholded", "other_row_loss"],
                    ((dates[i], dimrows[i][0], dimrows[i][1], dimrows[i][2], dimrows[i][3], land_str[i], DEVICES[dev[i]],
                      "returning" if nvr[i] else "new", int(sessions[i]), int(engaged[i]), int(users[i]), int(new_users[i]), int(pv[i]),
                      int(atc[i]), int(chk[i]), int(tx[i]), int(tx[i]), float(r2(rev[i])), 0, 0, 0) for i in range(len(uk))),
                    {"sessions": "INTEGER", "transactions": "INTEGER", "revenue": "REAL", "purchase": "INTEGER"})
        self.sessions_by_day = np.bincount(day, weights=sessions, minlength=DAYS)

    def t_ad_rows(self):
        o, rng = self.o, self.rng("ad_rows")
        n_ads = len(self.ads)
        credited = o["meta_touch"] > 0
        key = o["day"].astype(np.int64) * n_ads + o["meta_ad"]
        click = credited & (o["meta_touch"] == 1)
        view = o["meta_touch"] == 2
        size = DAYS * n_ads
        p_click = np.bincount(key[click], minlength=size).reshape(DAYS, n_ads)
        p_view = np.bincount(key[view], minlength=size).reshape(DAYS, n_ads)
        v_click = np.bincount(key[click], weights=o["total"][click], minlength=size).reshape(DAYS, n_ads)
        v_view = np.bincount(key[view], weights=o["total"][view], minlength=size).reshape(DAYS, n_ads)
        ps_orders = np.bincount(o["day"][o["ch"] == CH["paid_social"]], minlength=DAYS)
        q = np.array([a["q"] for a in self.ads])
        rows = []
        pl = PLACEHOLDERS
        camp_ids = [c[0] for c in META_CAMPAIGNS]
        spend_total = np.zeros(DAYS)
        for di, d in enumerate(self.days):
            cand = np.flatnonzero(self.ad_active[di])
            if not len(cand):
                continue
            q4 = d.month in (11, 12)
            cpa = pl["meta_cpa_usd"] * (pl["meta_q4_cpa_mult"] if q4 else 1.0)
            w = q[cand] ** 0.6 * rng.uniform(0.7, 1.3, len(cand))
            spend = r2(ps_orders[di] * cpa * w / w.sum())
            cpm = pl["meta_cpm_usd"] * (1.3 if q4 else 1.0) * rng.uniform(0.85, 1.15, len(cand))
            impr = np.round(spend / cpm * 1000).astype(int)
            spend_total[di] = spend.sum()
            for j, a in enumerate(cand):
                ad = self.ads[a]
                im = int(impr[j])
                if im <= 0:
                    continue
                reach = int(im / rng.uniform(1.3, 2.1))
                clicks = int(rng.binomial(im, pl["meta_ctr"]))
                link = int(min(clicks, rng.binomial(im, pl["meta_link_ctr"])))
                pc, pv = int(p_click[di, a]), int(p_view[di, a])
                purchases = pc + pv
                atc = int(round(purchases * 3.2 + link * 0.05))
                ic = int(round(purchases * 1.7))
                vid = ad["fmt"] == "video"
                v25 = int(im * 0.22) if vid else None
                rows.append((d.isoformat(), camp_ids[ad["camp"]], META_CAMPAIGNS[ad["camp"]][1], ad["adset"], ad["ad_id"],
                             float(spend[j]), im, reach, clicks, link, purchases, float(r2(v_click[di, a] + v_view[di, a])), pc, pv,
                             float(r2(v_click[di, a])), float(r2(v_view[di, a])), atc, ic, v25,
                             int(v25 * 0.55) if vid else None, int(v25 * 0.3) if vid else None, int(v25 * 0.18) if vid else None,
                             f"CR-{ad['ad_id'][3:]}", f"Simulated ad {ad['ad_id']} body", f"Simulated ad {ad['ad_id']} title",
                             "SHOP_NOW", ad["image_hash"], f"V-{ad['ad_id'][3:]}" if vid else None,
                             f"simulated://thumbs/{ad['ad_id']}.jpg", int(ad["dynamic"]), ad["fmt"]))
        self.insert("ad_rows", ["date", "campaign_id", "campaign_name", "adset_id", "ad_id", "spend", "impressions", "reach", "clicks",
                                "link_clicks", "purchases", "purchase_value", "purchases_7d_click", "purchases_1d_view",
                                "purchase_value_7d_click", "purchase_value_1d_view", "add_to_cart", "initiate_checkout",
                                "video_p25", "video_p50", "video_p75", "video_p100", "creative_id", "body", "title", "cta",
                                "image_hash", "video_id", "thumbnail_url", "is_dynamic", "format"], rows,
                    {"spend": "REAL", "impressions": "INTEGER", "purchases": "INTEGER", "purchase_value": "REAL"})
        self.meta_spend_by_day = spend_total

    def t_google_rows(self):
        o, rng = self.o, self.rng("google_rows")
        pl = PLACEHOLDERS
        rows = []
        ncamp = len(GOOGLE_CAMPAIGNS)
        credit = o["g_credit"]
        key = o["day"].astype(np.int64) * ncamp + np.maximum(o["g_camp"], 0)
        conv = np.bincount(key[credit], minlength=DAYS * ncamp).reshape(DAYS, ncamp)
        val = np.bincount(key[credit], weights=o["total"][credit], minlength=DAYS * ncamp).reshape(DAYS, ncamp)
        ps = o["ch"] == CH["paid_search"]
        utm_orders = np.bincount(key[ps], minlength=DAYS * ncamp).reshape(DAYS, ncamp)
        cpc = {"brand_search": 0.55, "nonbrand_search": 1.9, "pmax": 0.9, "demand_gen": 0.35}
        # Google CPAs keep their shape and take one scale so Meta to Google spend over the last 12 months
        # lands on the brain's paid split (expected value; the daily jitter has mean one)
        split = self.p.get("paid_split")
        base = np.maximum(utm_orders[DAYS - 365:], 0.2) @ np.array([pl["google_cpa_usd"][c[3]] for c in GOOGLE_CAMPAIGNS])
        meta = float(self.meta_spend_by_day[DAYS - 365:].sum())
        self.google_cpa_scale = float(meta * split["google"] / split["meta"] / base.sum()) if split and base.sum() else 1.0
        spend_total = np.zeros(DAYS)
        # term-level credited orders
        tkey = (o["day"].astype(np.int64) * 2 + np.maximum(o["g_camp"], 0)) * 16 + np.maximum(o["g_term"], 0)
        tm = credit & ps & (o["g_camp"] <= 1) & (o["g_term"] >= 0)
        tconv = np.bincount(tkey[tm], minlength=DAYS * 2 * 16).reshape(DAYS, 2, 16)
        for di, d in enumerate(self.days):
            ds = d.isoformat()
            for ci, (cid, cname, ctype, ckey, _) in enumerate(GOOGLE_CAMPAIGNS):
                spend = float(r2(max(utm_orders[di, ci], 0.2) * pl["google_cpa_usd"][ckey] * self.google_cpa_scale
                                 * rng.uniform(0.85, 1.15)))
                clicks = int(round(spend / cpc[ckey] * rng.uniform(0.9, 1.1)))
                impr = int(round(clicks / (0.09 if ckey == "brand_search" else 0.035 if ckey == "nonbrand_search" else 0.012)))
                spend_total[di] += spend
                is_ = top = abs_ = lb = lr = None
                clipped = 0
                if ctype == "SEARCH":
                    is_ = float(round(rng.uniform(0.86, 0.95) if ckey == "brand_search" else rng.uniform(0.3, 0.55), 4))
                    if is_ > 0.9001:
                        is_, clipped = None, 1
                    top = float(round(rng.uniform(0.6, 0.9), 4))
                    abs_ = float(round(top * rng.uniform(0.5, 0.8), 4))
                    lb = float(round(rng.uniform(0.0, 0.1), 4))
                    lr = float(round(1 - (is_ or 0.9001) - lb, 4))
                c = int(conv[di, ci])
                rows.append(("campaign", ds, cid, cname, "ENABLED", ctype, "MAXIMIZE_CONVERSION_VALUE" if ckey != "brand_search" else "TARGET_IMPRESSION_SHARE",
                             spend, impr, clicks, c, float(r2(val[di, ci])), float(round(c * 1.15, 2)), float(r2(val[di, ci] * 1.12)),
                             is_, top, abs_, lb, lr, clipped, None, None, None, None, None, None))
                if ctype == "SEARCH":
                    terms = SEARCH_TERMS[cid]
                    tw = 1 / np.arange(1, len(terms) + 1) ** 1.1
                    tw = tw / tw.sum()
                    for ti, term in enumerate(terms):
                        tclicks = int(round(clicks * tw[ti] * 0.8))
                        timpr = int(round(impr * tw[ti] * 0.8))
                        if timpr < 10:  # privacy threshold: term hidden, campaign row keeps it
                            continue
                        tc = int(tconv[di, ci, ti])
                        rows.append(("search_term", ds, cid, cname, "ENABLED", ctype, None, float(r2(spend * tw[ti] * 0.8)), timpr, tclicks,
                                     tc, None, None, None, None, None, None, None, None, 0, term,
                                     "ADDED" if ti < 2 else "NONE", f"AG-{cid[3:]}-1", int(rng.integers(5, 11)), None, None))
            if True:
                rows.append(("asset_group", ds, "GC-3", "Shopping | PMax", "ENABLED", "PERFORMANCE_MAX", None, None, None, None, None, None,
                             None, None, None, None, None, None, None, 0, None, None, None, None, "AG-PMAX-1",
                             "EXCELLENT" if di > 200 else "GOOD"))
        self.insert("google_rows", ["row_kind", "date", "campaign_id", "campaign_name", "campaign_status", "channel_type", "bidding",
                                    "spend", "impressions", "clicks", "conversions", "conversion_value", "all_conversions",
                                    "all_conversion_value", "impression_share", "top_is", "abs_top_is", "lost_is_budget", "lost_is_rank",
                                    "clipped", "search_term", "term_status", "ad_group_id", "quality_score", "asset_group_id",
                                    "ad_strength"], rows, {"spend": "REAL", "conversions": "REAL", "conversion_value": "REAL"})
        self.google_spend_by_day = spend_total

    def t_flows(self):
        o, rng = self.o, self.rng("flows")
        ids = self.order_ids()
        k = o["k_msg"]
        m = k >= 0
        km, dm, tot, oid = k[m], o["day"][m], o["total"][m], ids[m]
        order = np.lexsort((oid, dm, km))
        km, dm, tot, oid = km[order], dm[order], tot[order], oid[order]
        # groups by (msg, day)
        gk = km.astype(np.int64) * DAYS + dm
        uk, start = np.unique(gk, return_index=True)
        ends = np.r_[start[1:], len(gk)]
        grp = {int(u): (s, e) for u, s, e in zip(uk, start, ends)}
        rows = []
        for mi, (fid, fname, trig, (mid, chn, subj)) in enumerate(FLOW_MSG):
            for di, d in enumerate(self.days):
                s, e = grp.get(mi * DAYS + di, (0, 0))
                n_att = int(e - s)
                base = max(n_att, 0.3) / FLOW_CVR[fid] * rng.uniform(0.8, 1.2)
                sends = int(round(base))
                opens = int(round(sends * (0.48 if chn == "email" else 0)))
                clicks = int(round(sends * (0.045 if chn == "email" else 0.08)))
                rows.append((d.isoformat(), fid, fname, "live", trig, mid, chn, subj if chn == "email" else None, sends,
                             opens if chn == "email" else None, clicks, int(sends * 0.002), int(sends * 0.004),
                             float(r2(tot[s:e].sum())), n_att, js(oid[s:e].tolist()), "account_setting"))
        self.insert("flows", ["date", "flow_id", "flow_name", "flow_status", "trigger_type", "message_id", "channel", "subject",
                              "sends", "opens", "clicks", "unsubscribes", "bounces", "attributed_revenue", "attributed_orders",
                              "matched_order_ids", "attribution"], rows,
                    {"sends": "INTEGER", "attributed_revenue": "REAL", "attributed_orders": "INTEGER"})
        rows = []
        subs = max(getattr(self, "email_subscribers", 1000), 1000)
        for c in self.campaigns:
            for off in range(5):
                di = c["day"] + off
                if di >= DAYS:
                    break
                s, e = grp.get((1000 + c["idx"]) * DAYS + di, (0, 0))
                sends = int(subs * (0.55 if c["audience"] == "Engaged 90d" else 1.0) * (0.25 if c["channel"] == "sms" else 1)) if off == 0 else 0
                rows.append((self.days[di].isoformat(), c["id"], c["name"], "sent", iso_utc([self.day_epoch[c["day"]] + 14 * 3600])[0],
                             c["strategy"], c["audience"], int(c["smart_sending"]), c["channel"],
                             c["subject"] if c["channel"] == "email" else None, f"Simulated {c['channel']} body for {c['id']}",
                             sends, int(sends * 0.42) if c["channel"] == "email" else None, int(sends * 0.018), int(sends * 0.003),
                             int(sends * 0.004), float(r2(tot[s:e].sum())), int(e - s), js(oid[s:e].tolist()), "account_setting"))
        self.insert("campaign_sends", ["date", "campaign_id", "campaign_name", "status", "send_time", "send_strategy", "audiences",
                                       "use_smart_sending", "channel", "subject", "body", "sends", "opens", "clicks", "unsubscribes",
                                       "bounces", "attributed_revenue", "attributed_orders", "matched_order_ids", "attribution"], rows,
                    {"sends": "INTEGER", "attributed_revenue": "REAL", "attributed_orders": "INTEGER"})

    def t_tickets(self):
        o, rng = self.o, self.rng("tickets")
        ids = self.order_ids()
        n = len(ids)
        pl = PLACEHOLDERS
        # Fix 2: ticket_rate is all tickets per order. Returns (a share opens a ticket, the rest use the
        # returns portal) and pre-sale questions are part of it, so the order tickets take what is left.
        rate = np.where(self.month_key[o["day"]] % 100 == 12, pl["ticket_rate_dec"], pl["ticket_rate"])
        rate = rate - pl["presale_ticket_rate"] - np.where(o["pos"], 0.0, pl["return_rate"] * pl["return_ticket_share"])
        t = np.flatnonzero(rng.random(n) < np.maximum(rate, 0.0))
        tday = o["day"][t] + rng.integers(1, 15, len(t))
        keep = tday <= DAYS - 1
        t, tday = t[keep], tday[keep]
        reason = np.array(TICKET_REASONS_ORDER)[np.searchsorted(np.cumsum(TICKET_W), rng.random(len(t)) * 0.999999)]
        # a share of returned orders open a return ticket
        pick = rng.random(len(self.rev["return"]["idx"])) < pl["return_ticket_share"]
        rt = self.rev["return"]["idx"][pick]
        rt_day = self.rev["return"]["open"][pick]
        pres = rng.poisson(np.bincount(o["day"], minlength=DAYS) * pl["presale_ticket_rate"])
        p_day = np.repeat(np.arange(DAYS), pres)
        order_id = np.r_[ids[t], ids[rt], np.full(len(p_day), -1)]
        day = np.r_[tday, rt_day, p_day]
        rsn = np.r_[reason, np.full(len(rt), "return or exchange"),
                    np.array(["product question", "size or fit", "giving program"])[rng.integers(0, 3, len(p_day))]]
        m = len(day)
        ts = self.day_epoch[day] + (np.clip(rng.normal(13, 4, m), 0, 23.9) * 3600).astype(np.int64)
        order = np.argsort(ts, kind="stable")
        ts, order_id, rsn = ts[order], order_id[order], rsn[order]
        chan = np.array(["email", "chat", "sms", "phone", "social"])[np.searchsorted([0.45, 0.8, 0.88, 0.95, 1.0], rng.random(m))]
        first = np.round(rng.lognormal(math.log(95), 0.9, m)).astype(int)
        resolved = first + np.round(rng.lognormal(math.log(600), 1.0, m)).astype(int)
        csat = np.where(rng.random(m) < 0.3, np.clip(np.round(rng.normal(4.4, 0.9, m)), 1, 5), np.nan)
        self.insert("tickets", ["id", "created_at", "channel", "reason", "order_id", "first_response_min", "resolved_min", "csat"],
                    zip((800_000 + np.arange(m)).tolist(), iso_utc(ts).tolist(), chan.tolist(), rsn.tolist(),
                        [None if x < 0 else x for x in order_id.tolist()], first.tolist(), resolved.tolist(),
                        [None if math.isnan(x) else int(x) for x in csat.tolist()]),
                    {"id": "INTEGER", "order_id": "INTEGER", "first_response_min": "INTEGER", "resolved_min": "INTEGER", "csat": "INTEGER"})
        self.tickets_by_day = np.bincount(day, minlength=DAYS)

    def t_reviews(self):
        o, l, rng = self.o, self.l, self.rng("reviews")
        m = len(l["order"])
        pick = np.flatnonzero(rng.random(m) < PLACEHOLDERS["review_rate_per_line"])
        day = o["day"][l["order"][pick]] + rng.integers(14, 46, len(pick))
        keep = day <= DAYS - 1
        pick, day = pick[keep], day[keep]
        # the returned-line hole-or-defect story lowers ratings for returned lines
        rating = np.searchsorted(np.cumsum([0.03, 0.03, 0.06, 0.16, 0.72]), rng.random(len(pick)) * 0.999999) + 1
        texts = [REVIEW_TEXT[r][i % len(REVIEW_TEXT[r])] for r, i in zip(rating.tolist(), rng.integers(0, 12, len(pick)).tolist())]
        order = np.argsort(day, kind="stable")
        self.insert("reviews", ["sku", "rating", "text", "date", "review_source"],
                    zip(np.array(SKUS)[l["sku"][pick][order]].tolist(), rating[order].tolist(), [texts[i] for i in order],
                        [self.days[d].isoformat() for d in day[order].tolist()], ["site"] * len(pick)), {"rating": "INTEGER"})

    def t_fixtures(self):
        rng = self.rng("fixtures")
        rows = []
        for page in ("/", "/collections/best-sellers", "/products/ankle-sock-4-pack"):
            for variant in ("mobile", "desktop"):
                for run in range(1, 4):
                    lcp = int(rng.normal(2900 if variant == "mobile" else 1700, 250))
                    rows.append((page, variant, run, int(lcp * 1.4), lcp, int(lcp * 0.55), int(rng.normal(2_400_000, 200_000)), int(rng.normal(95, 8))))
        self.insert("speed_runs", ["page", "variant", "run", "load_ms", "lcp_ms", "fcp_ms", "bytes", "requests"], rows)
        rows = []
        for di in range(DAYS - 180, DAYS, 3):
            for plat in ("instagram", "tiktok"):
                views = int(rng.lognormal(math.log(40000 * max(self.scale, 0.01)), 0.8))
                rows.append((plat, self.days[di].isoformat(), str(rng.choice(["reel", "carousel", "static"])),
                             str(rng.choice(["Giving story", "Sock drawer swap", "Fit check", "Founder story", "Winter wool"])),
                             views, int(views * 0.01), int(views * 0.004), int(views * 0.0002)))
        self.insert("content_posts", ["platform", "date", "format", "hook", "views", "saves", "clicks", "matched_orders"], rows)
        rows = []
        queries = [("bombas", "/"), ("bombas socks", "/"), ("bombas slippers", "/collections/slippers"), ("best socks for running", "/collections/running"),
                   ("merino wool socks", "/products/merino-wool-calf-sock"), ("bombas donation", "/pages/giving-back"),
                   ("compression socks", "/collections/compression"), ("no show socks", "/collections/no-show")]
        for di in range(DAYS - 90, DAYS):
            for qi, (qq, page) in enumerate(queries):
                imp = int(rng.lognormal(math.log(60000 * self.scale / (qi + 1)), 0.2)) + 1
                pos = float(round(1.1 + qi * 1.6 + rng.normal(0, 0.3), 1))
                rows.append((self.days[di].isoformat(), qq, page, int(imp * (0.35 if qi < 3 else 0.04)), imp, max(pos, 1.0)))
        self.insert("search_console", ["date", "query", "page", "clicks", "impressions", "position"], rows)
        # marketplace share is null in the brain: the table exists with no rows (unavailable, not 0)
        self.insert("marketplace_listings", ["marketplace", "listing_id", "price", "buy_box", "stock", "rating", "reviews"], [])

    def t_wholesale(self):
        """Fixture: monthly sell-in by retail partner. Wholesale is not in orders; the brain gives its share."""
        rng = self.rng("wholesale")
        pl = PLACEHOLDERS
        sm = self.p["sales_mix"]
        partners = [pp for pp in self.p["retail_partners"]]
        ratio = sm["wholesale"] / (sm["dtc"] + sm["owned_retail"])
        # Fix 9: sell-in has its own month curve (retailers stock for holiday in Aug to Oct), on the brain's
        # growth trend; the last 12 months total the brain's wholesale share of orders revenue.
        wi = pl["wholesale_month_index"]
        wi_mean = sum(wi.values()) / 12
        trend = np.array([(1 + self.p["growth"]) ** (-(self.as_of - d).days / 365.25) for d in self.days])
        daily = trend * np.array([wi[MONTHS[d.month - 1]] / wi_mean for d in self.days])
        last = np.arange(DAYS) >= DAYS - 365
        daily *= float(self.o["sub"][self.o["day"] >= DAYS - 365].sum()) * ratio / daily[last].sum()
        start_m = pl["new_partner_since_month"]
        ramp = pl["new_partner_ramp_by_quarter"]
        rows = []
        for mk in np.unique(self.month_key):
            y, mo = divmod(int(mk), 100)
            live, months_in = [], []
            for pp in partners:
                since = pp.get("since") or 2018
                if since < y or (since == y and mo >= start_m):
                    live.append(pp)
                    months_in.append((y - since) * 12 + mo - start_m)  # 0 in the first month
            if not live:
                continue
            w = np.array([float(pp.get("stores") or 60) for pp in live])
            r = np.array([ramp[min(mi // 3, len(ramp) - 1)] for mi in months_in])  # 25, 50, then 100 percent of run rate
            w = w / w.sum() * r * rng.uniform(0.8, 1.2, len(live))
            w /= w.sum()
            for name, cap in pl["partner_year1_cap"].items():  # a first year rollout stays near its cap
                i = next((j for j, pp in enumerate(live) if pp["name"] == name), None)
                if i is not None and months_in[i] < 12 and w[i] > cap:
                    rest = w.sum() - w[i]
                    w = np.where(np.arange(len(w)) == i, cap, w * (1 - cap) / rest)
            total = float(daily[self.month_key == mk].sum())
            for pp, share in zip(live, w):
                rows.append((f"{y}-{mo:02d}", pp["name"], float(r2(total * share))))
        self.wholesale_by_day = daily
        self.insert("wholesale_sell_in", ["month", "partner", "net_sales"], rows, {"net_sales": "REAL"})

    def t_marketplace(self):
        """Fixture: monthly marketplace net sales at the brain's share. No connector, no listing detail (listings stay empty)."""
        rng = self.rng("marketplace")
        sm, pl = self.p["sales_mix"], PLACEHOLDERS
        if sm.get("marketplaces") is None:
            self.marketplace_by_day = None
            self.ensure_table("marketplace_sales", ["month", "marketplace", "net_sales"], {"net_sales": "REAL"})
            return
        # consumer demand: the site's own day curve, noise and all, at the marketplace share of revenue
        web = ~self.o["pos"]
        site = np.bincount(self.o["day"][web], weights=self.o["sub"][web], minlength=DAYS)
        daily = site * rng.uniform(0.9, 1.1, DAYS)
        ratio = sm["marketplaces"] / (sm["dtc"] + sm["owned_retail"])
        want = float(self.o["sub"][self.o["day"] >= DAYS - 365].sum()) * ratio
        daily *= want / daily[DAYS - 365:].sum()
        rows = []
        split = pl["marketplace_split"]
        for mk in np.unique(self.month_key):
            total = float(daily[self.month_key == mk].sum())
            w = np.array(list(split.values())) * rng.uniform(0.9, 1.1, len(split))
            w /= w.sum()
            for name, share in zip(split, w):
                rows.append((f"{mk // 100}-{mk % 100:02d}", name, float(r2(total * share))))
        self.marketplace_by_day = daily
        self.insert("marketplace_sales", ["month", "marketplace", "net_sales"], rows, {"net_sales": "REAL"})

    def t_paid_other(self):
        """Fixture: daily spend on the paid platforms that have no ad rows here, at the brain's paid split."""
        rng = self.rng("paid_other")
        split = self.p.get("paid_split")
        cols = ["date", "platform", "spend"]
        self.other_spend_by_day = None
        self.other_spend = {}
        if not split:
            self.ensure_table("paid_other_spend", cols, {"spend": "REAL"})
            return
        mg = self.meta_spend_by_day + self.google_spend_by_day
        mg_last = float(mg[DAYS - 365:].sum())
        rows, tot = [], np.zeros(DAYS)
        for plat in ("youtube_creator", "tiktok", "pinterest", "other"):
            d = mg * rng.uniform(0.8, 1.2, DAYS)
            d *= mg_last * split[plat] / (split["meta"] + split["google"]) / d[DAYS - 365:].sum()
            d = r2(d)
            self.other_spend[plat] = d
            tot += d
            rows += [(self.days[i].isoformat(), plat, float(d[i])) for i in range(DAYS)]
        rows.sort(key=lambda r: (r[0], r[1]))
        self.other_spend_by_day = tot
        self.insert("paid_other_spend", cols, rows, {"spend": "REAL"})

    # ---- aggregates
    def aggregates_build(self):
        o = self.o
        web = ~o["pos"]
        n_day = lambda m: np.bincount(o["day"][m], minlength=DAYS)
        s_day = lambda m, w: np.bincount(o["day"][m], weights=w[m], minlength=DAYS)
        allm = np.ones(len(o["day"]), bool)
        daily = {
            "orders": n_day(allm), "web_orders": n_day(web), "pos_orders": n_day(o["pos"]),
            "new_customer_orders": n_day(o["new"]), "returning_customer_orders": n_day(~o["new"]),
            "net_sales": s_day(allm, o["sub"]), "discounts": s_day(allm, o["disc"]), "gross_sales": s_day(allm, o["gross"]),
            "shipping": s_day(allm, o["ship"]), "tax": s_day(allm, o["tax"]), "total": s_day(allm, o["total"]),
            "refunds_on_orders": s_day(allm, o["refund"]), "units": s_day(allm, o["units"].astype(float)),
            "giving_units": s_day(allm, o["items"].astype(float)),
            "sessions": self.sessions_by_day, "ga4_transactions": n_day(o["ga4"]),
            "meta_spend": self.meta_spend_by_day, "meta_purchases": n_day(o["meta_touch"] > 0),
            "google_spend": self.google_spend_by_day, "google_conversions": n_day(o["g_credit"]),
            "klaviyo_attributed_orders": n_day(o["k_msg"] >= 0), "tickets": self.tickets_by_day,
        }
        if self.other_spend_by_day is not None:
            daily["other_paid_spend"] = self.other_spend_by_day
        # Fix 10: before the first store opened there is no POS to count, so pos_orders reads null, not 0
        open_day = (date.fromisoformat(PLACEHOLDERS["owned_retail_open"]) - self.start).days
        open_month = self.month_key[min(max(open_day, 0), DAYS - 1)] if open_day < DAYS else None
        counts = ("orders", "web_orders", "pos_orders", "new_customer_orders", "returning_customer_orders", "sessions",
                  "ga4_transactions", "meta_purchases", "google_conversions", "klaviyo_attributed_orders", "tickets",
                  "units", "giving_units")
        days = [d.isoformat() for d in self.days]
        rows = []
        for i in range(DAYS):
            r = {"date": days[i]}
            for k, v in daily.items():
                val = v[i]
                r[k] = int(val) if k in counts else float(r2(val))
            if i < open_day:
                r["pos_orders"] = None
            rows.append(r)
        self.aggregates["daily"] = rows
        # monthly
        months = []
        for mk in np.unique(self.month_key):
            m = self.month_key == mk
            r = {"month": f"{mk // 100}-{mk % 100:02d}", "days": int(m.sum())}
            for k, v in daily.items():
                r[k] = float(r2(np.asarray(v)[m].sum()))
            r["aov"] = float(r2(r["net_sales"] / r["orders"])) if r["orders"] else None
            if open_month is None or mk < open_month:
                r["pos_orders"] = None
            months.append(r)
        self.aggregates["monthly"] = months
        # channel x month; no pos rows for months before the first store opened
        rows = []
        for mk in np.unique(self.month_key):
            mm = self.month_key[o["day"]] == mk
            for c in CHANNELS:
                if c == "pos" and (open_month is None or mk < open_month):
                    continue
                m = mm & (o["ch"] == CH[c])
                rows.append({"month": f"{mk // 100}-{mk % 100:02d}", "channel": c, "orders": int(m.sum()),
                             "net_sales": float(r2(o["sub"][m].sum())), "new_customer_orders": int((m & o["new"]).sum())})
        self.aggregates["channels_monthly"] = rows
        # product x month
        l = self.l
        lm = self.month_key[o["day"][l["order"]]]
        rows = []
        for mk in np.unique(self.month_key):
            m = lm == mk
            u = np.bincount(l["sku"][m], weights=l["qty"][m], minlength=len(SKUS))
            rv = np.bincount(l["sku"][m], weights=l["line_total"][m], minlength=len(SKUS))
            for i, s in enumerate(SKUS):
                rows.append({"month": f"{mk // 100}-{mk % 100:02d}", "sku": s, "category": CATALOG[i][1], "units": int(u[i]),
                             "net_sales": float(r2(rv[i]))})
        self.aggregates["products_monthly"] = rows
        # cohorts: first order month in the window x months since, customers ordering
        fd = self.cust_first_day[o["cust"]]
        in_win = fd >= 0
        cm = self.month_key[np.maximum(fd, 0)]
        om = self.month_key[o["day"]]
        idx = lambda mk: (mk // 100) * 12 + mk % 100
        since = idx(om) - idx(cm)
        rows = []
        ci = idx(cm) - idx(self.month_key[0])
        packed = np.unique(((ci[in_win] * 64 + since[in_win]).astype(np.int64) << 32) + o["cust"][in_win])
        grid = np.bincount((packed >> 32), minlength=64 * 26)
        for mk in np.unique(self.month_key):
            c0 = idx(mk) - idx(self.month_key[0])
            size = int(grid[c0 * 64])
            if not size:
                continue
            counts = grid[c0 * 64: c0 * 64 + (idx(self.month_key[-1]) - idx(mk)) + 1].astype(int).tolist()
            rows.append({"cohort": f"{mk // 100}-{mk % 100:02d}", "customers": size, "active_by_month": counts})
        self.aggregates["cohorts"] = rows
        self.aggregates["wholesale_monthly"] = [dict(zip(("month", "partner", "net_sales"), r)) for r in
                                                self.db_rows("SELECT month, partner, net_sales FROM wholesale_sell_in ORDER BY month, partner")]
        self.aggregates["marketplace_monthly"] = [dict(zip(("month", "marketplace", "net_sales"), r)) for r in self.db_rows(
            "SELECT month, marketplace, net_sales FROM marketplace_sales ORDER BY month, marketplace")]
        # paid spend by platform x month: Meta and Google from their rows, the rest from the fixture
        rows = []
        plats = [("meta", self.meta_spend_by_day), ("google", self.google_spend_by_day)] + list(self.other_spend.items())
        for mk in np.unique(self.month_key):
            m = self.month_key == mk
            for plat, arr in plats:
                rows.append({"month": f"{mk // 100}-{mk % 100:02d}", "platform": plat, "spend": float(r2(arr[m].sum()))})
        self.aggregates["paid_media_monthly"] = rows
        self.aggregates["calibration"] = self.calibration_check()

    def db_rows(self, q):
        db = sqlite3.connect(self.sqlite_path)
        try:
            return db.execute(q).fetchall()
        finally:
            db.close()

    def review_checks(self):
        """The numbers REVIEW.md checks 1 to 11 read, from the generated rows (arithmetic here, not in prose)."""
        o, l, mk = self.o, self.l, self.month_key
        om = mk[o["day"]]
        web = ~o["pos"]
        out = {}
        # 1. growth by month and day to day noise
        months = np.unique(mk)
        net_m = {int(k): float(o["sub"][om == k].sum()) for k in months}
        full = {int(k) for k in months if (mk == k).sum() >= 28}
        yoy = {f"{k // 100}-{k % 100:02d}": round(net_m[k] / net_m[k - 100] - 1, 4)
               for k in sorted(full) if k - 100 in full and k >= mk[DAYS - 365]}
        out["yoy_growth"] = {"by_month": yoy, "min": min(yoy.values()) if yoy else None, "max": max(yoy.values()) if yoy else None}
        orders_d = np.bincount(o["day"], minlength=DAYS)
        cvs = {}
        for k in (202606, 202603):
            d = orders_d[mk == k]
            if len(d) >= 28:
                cvs[f"{k // 100}-{k % 100:02d}"] = round(float(d.std() / d.mean()), 4)
        out["daily_orders_cv"] = cvs
        # 2. AOV by season and BFCM discount depth
        def aov_of(keys):
            m = np.isin(om, keys)
            return round(float(o["sub"][m].sum() / m.sum()), 2) if m.any() else None
        y0 = self.as_of.year - 1
        out["aov"] = {"nov_dec": aov_of([y0 * 100 + 11, y0 * 100 + 12]), "jan_feb": aov_of([(y0 + 1) * 100 + 1, (y0 + 1) * 100 + 2]),
                      "year": round(float(o["sub"][o["day"] >= DAYS - 365].sum() / (o["day"] >= DAYS - 365).sum()), 2)}
        tg = self.thanksgiving(y0)
        bf = [(tg + timedelta(days=i) - self.start).days for i in range(0, 5)]
        out["bfcm"] = []
        for di in bf:
            if 0 <= di < DAYS:
                m = o["day"] == di
                out["bfcm"].append({"date": self.days[di].isoformat(), "orders": int(m.sum()),
                                    "discount_pct_of_gross": round(float(o["disc"][m].sum() / o["gross"][m].sum()), 4),
                                    "aov": round(float(o["sub"][m].mean()), 2), "new_share": round(float(o["new"][m].mean()), 4)})
        # 3. new versus returning, and the repeat curve
        last = o["day"] >= DAYS - 365
        dec = om == y0 * 100 + 12
        aug = om == y0 * 100 + 8
        out["new_share"] = {"year": round(float(o["new"][last].mean()), 4), "dec": round(float(o["new"][dec].mean()), 4),
                            "returning_rise_aug_to_dec": round(float((~o["new"] & dec).sum() / max((~o["new"] & aug).sum(), 1)), 3),
                            "new_rise_aug_to_dec": round(float((o["new"] & dec).sum() / max((o["new"] & aug).sum(), 1)), 3)}
        fd = self.cust_first_day
        cohort = []
        for ck in [202410, 202412, 202503, 202506]:
            days = np.flatnonzero(mk == ck)
            if not len(days):
                continue
            inc = (fd >= days[0]) & (fd <= days[-1])
            size = int(inc.sum())
            oc = inc[o["cust"]] & ~o["new"]
            gap = o["day"] - fd[o["cust"]]
            y1 = int((oc & (gap <= 365)).sum())
            y2 = int((oc & (gap > 365) & (gap <= 730)).sum())
            full2 = days[0] + 730 <= DAYS
            cohort.append({"cohort": f"{ck // 100}-{ck % 100:02d}", "customers": size, "repeat_orders_per_customer_yr1": round(y1 / size, 3),
                           "repeat_orders_per_customer_yr2": round(y2 / size, 3) if size else None, "yr2_is_full": bool(full2),
                           "yr2_over_yr1": round(y2 / y1, 3) if y1 else None})
        out["cohorts"] = cohort
        # 4. wholesale shape and partners
        ws = {r[0]: r[1] for r in self.db_rows("SELECT month, sum(net_sales) FROM wholesale_sell_in GROUP BY month")}
        share = {}
        for k in sorted(full):
            key = f"{k // 100}-{k % 100:02d}"
            if key in ws and net_m[k]:
                share[key] = round(ws[key] / net_m[k], 4)
        part = self.db_rows(f"SELECT partner, sum(net_sales) FROM wholesale_sell_in WHERE month >= '{self.days[DAYS - 365].isoformat()[:7]}' "
                            "GROUP BY partner ORDER BY 2 DESC")
        pt = sum(v for _, v in part) or 1
        out["wholesale"] = {"share_of_orders_revenue_by_month": share, "min": min(share.values()) if share else None,
                            "max": max(share.values()) if share else None,
                            "partners_last_12m": {n: round(v / pt, 4) for n, v in part}}
        # 5. funnel
        last_d = slice(DAYS - 365, DAYS)
        sess = float(self.sessions_by_day[last_d].sum())
        web_last = int((last & web).sum())
        out["funnel"] = {"sessions_per_month": round(sess / 12), "target": self.p["sessions_monthly"] * self.scale,
                         "cvr_on_web_orders": round(web_last / sess, 4) if sess else None,
                         "cvr_on_ga4_transactions": round(float((o["ga4"] & last).sum()) / sess, 4) if sess else None,
                         "cvr_scale": round(self.cvr_scale, 4), "cvr_by_channel_solved": self.cvr_solved}
        # 6. Meta by month
        credited = o["meta_touch"] > 0
        meta = {}
        for k in (y0 * 100 + 9, y0 * 100 + 10, y0 * 100 + 11, y0 * 100 + 12, (y0 + 1) * 100 + 2):
            dm = mk == k
            spend = float(self.meta_spend_by_day[dm].sum())
            m = credited & (om == k)
            meta[f"{k // 100}-{k % 100:02d}"] = {"spend": round(spend, 2), "cpa": round(spend / m.sum(), 2) if m.any() else None,
                                                 "roas": round(float(o["total"][m].sum()) / spend, 3) if spend else None}
        out["meta"] = meta
        out["google_cpa_scale"] = round(self.google_cpa_scale, 4)
        # 7. email
        out["klaviyo_share_of_orders"] = round(float((o["k_msg"][last] >= 0).mean()), 4)
        out["email_sms_last_click_share"] = round(float(np.isin(o["ch"][last], [CH["email"], CH["sms"]]).mean()), 4)
        # 8. tickets, chargebacks, abandonment, refunds
        t_last = float(self.tickets_by_day[last_d].sum())
        dec_d = mk == y0 * 100 + 12
        out["tickets_per_1000_orders"] = {"year": round(t_last / last.sum() * 1000, 1),
                                          "dec": round(float(self.tickets_by_day[dec_d].sum()) / max(dec.sum(), 1) * 1000, 1)}
        early = o["day"] < DAYS - 140  # disputes open 20 to 60 days after the order
        cb = self.rev["chargeback"]["idx"]
        out["chargebacks_per_web_order"] = round(float(np.isin(np.flatnonzero(early & web), cb).sum()) / max((early & web).sum(), 1), 5)
        ab = self.counts.get("abandoned_checkouts", 0)
        out["checkout_abandonment"] = round(ab / (ab + int(web.sum())), 4) if ab else None
        mature = last & (o["day"] < DAYS - 60)
        out["refunds_share_of_net_mature"] = round(float(o["refund"][mature].sum() / o["sub"][mature].sum()), 4)
        # 9. finance keys join the products, and margin by month where cost rows are in force
        out["finance_join"] = self.finance_join()
        # 10. zero versus unavailable
        out["ga4_capture_daily"] = {"min": round(float(self.ga4_capture_day.min()), 4), "max": round(float(self.ga4_capture_day.max()), 4)}
        return out

    def finance_join(self):
        """How many products carry a finance cogs_landed key, and gross margin by month from the rows in force."""
        path = BRANDS / self.brand / "finance_inputs.json"
        if not path.is_file():
            return None
        from importlib.util import module_from_spec, spec_from_file_location
        spec = spec_from_file_location("ecomos_finance_gen", HERE / "finance.py")
        fm = module_from_spec(spec)
        spec.loader.exec_module(fm)
        fin = fm.Finance(fm.load(path))
        keys = {r.get("scope_key") for r in fin.by_field.get("cogs_landed", [])}
        o, l = self.o, self.l
        lm = self.month_key[o["day"][l["order"]]]
        by_month = []
        for k in np.unique(self.month_key):
            days = np.flatnonzero(self.month_key == k)
            d0, d1 = self.days[days[0]].isoformat(), self.days[days[-1]].isoformat()
            cost0 = np.array([fin.value("cogs_landed", d0, s) for s in SKUS], dtype=object)
            cost1 = np.array([fin.value("cogs_landed", d1, s) for s in SKUS], dtype=object)
            m = lm == k
            net = float(l["line_total"][m].sum())
            units = np.bincount(l["sku"][m], weights=l["qty"][m], minlength=len(SKUS))
            sold = units > 0
            if any(c is None for c in cost0[sold]) or any(c is None for c in cost1[sold]) or list(cost0) != list(cost1):
                gm = None  # no cost rows in force (or a change inside the month): unavailable, never 0
            else:
                gm = round((net - float((units * cost0.astype(float)).sum())) / net, 4) if net else None
            by_month.append({"month": f"{k // 100}-{k % 100:02d}", "gross_margin": gm})
        return {"skus_with_cogs": sum(1 for s in SKUS if s in keys), "skus": len(SKUS),
                "finance_skus_without_product": sorted(k for k in keys if k not in SKUS),
                "gross_margin_by_month": by_month}

    def calibration_check(self):
        o, p = self.o, self.p
        last = o["day"] >= DAYS - 365
        net = float(o["sub"][last].sum())
        sm = p["sales_mix"]
        whole = float(self.wholesale_by_day[DAYS - 365:].sum())
        mkt = float(self.marketplace_by_day[DAYS - 365:].sum()) if self.marketplace_by_day is not None else None
        total = net + whole + (mkt or 0.0)
        site = float(o["sub"][last & ~o["pos"]].sum())
        pos = float(o["sub"][last & o["pos"]].sum())
        aov = float(o["sub"].sum() / len(o["sub"]))
        # repeat within 12 months, customers whose first order is in the first 12 months of the window
        fd = self.cust_first_day
        cohort = (fd >= 0) & (fd < DAYS - 365)
        order_c = o["cust"]
        first_in = cohort[order_c]
        later = first_in & ~o["new"] & ((o["day"] - fd[order_c]) <= 365)
        repeaters = len(np.unique(order_c[later]))
        size = int(cohort.sum())
        # seasonality: last 12 months, detrended by the growth curve
        mk = self.month_key
        months = np.unique(mk[DAYS - 365:])
        idx = []
        for k in months:
            m = mk[o["day"]] == k
            dm = mk == k
            mid = np.flatnonzero(dm).mean()
            trend = (1 + p["growth"]) ** (-(DAYS - 1 - mid) / 365.25)
            idx.append(o["sub"][m].sum() / trend / dm.sum())
        full = [k for k in months if (mk == k).sum() >= 28]
        vals = np.array([v for k, v in zip(months, idx) if k in full])
        vals = vals / vals.mean()
        want = np.array([p["season"][MONTHS[k % 100 - 1]] for k in full])
        want = want / want.mean()
        ch = {c: float(round((o["ch"][~o["pos"]] == CH[c]).mean(), 4)) for c in CHANNELS[:7]}
        cats = np.array([CATALOG[s][1] for s in range(len(SKUS))])[self.l["sku"]]
        sock = np.isin(cats, SOCK_LIKE)
        point = p["revenue_point"] * self.scale
        mix_gen = {"dtc_site": site / total, "wholesale": whole / total, "owned_retail": pos / total,
                   "marketplaces": None if mkt is None else mkt / total}
        mix_want = {"dtc_site": sm["dtc"], "wholesale": sm["wholesale"], "owned_retail": sm["owned_retail"],
                    "marketplaces": sm.get("marketplaces")}
        paid = {"meta": float(self.meta_spend_by_day[DAYS - 365:].sum()), "google": float(self.google_spend_by_day[DAYS - 365:].sum())}
        paid.update({k: float(v[DAYS - 365:].sum()) for k, v in self.other_spend.items()})
        paid_total = sum(paid.values())
        split = p.get("paid_split") or {}
        return {
            "scale": self.scale, "as_of": self.as_of.isoformat(),
            "revenue_last_12m": {"orders_net_sales": round(net, 2), "wholesale_fixture": round(whole, 2),
                                 "marketplace_fixture": None if mkt is None else round(mkt, 2), "total": round(total, 2),
                                 "point_scaled": point, "vs_point_pct": round((total / point - 1) * 100, 2),
                                 "band_scaled": [p["revenue_low"] * self.scale, p["revenue_high"] * self.scale],
                                 "in_band": p["revenue_low"] * self.scale <= total <= p["revenue_high"] * self.scale},
            "sales_channel_mix_last_12m": {
                "generated": {k: None if v is None else round(v, 4) for k, v in mix_gen.items()}, "target": mix_want,
                "max_gap_points": round(max(abs(mix_gen[k] - mix_want[k]) * 100 for k in mix_gen
                                            if mix_gen[k] is not None and mix_want[k] is not None), 2)},
            "paid_split_last_12m": {
                "spend": {k: round(v, 2) for k, v in paid.items()}, "total": round(paid_total, 2),
                "generated": {k: round(v / paid_total, 4) for k, v in paid.items()} if paid_total else None, "target": split or None,
                "max_gap_points": round(max(abs(paid[k] / paid_total - split[k]) * 100 for k in split), 2)
                if split and paid_total and set(split) <= set(paid) else None,
                "mer_on_total_revenue": round(total / paid_total, 3) if paid_total else None},
            "review_checks": self.review_checks(),
            "aov": {"generated": round(aov, 2), "target": p["aov"], "diff_pct": round((aov / p["aov"] - 1) * 100, 2)},
            "repeat_12m": {"generated": round(repeaters / size, 4) if size else None, "target": p["repeat_12m"], "cohort_customers": size},
            "seasonality_last_12m": {"months": [f"{k // 100}-{k % 100:02d}" for k in full], "generated": np.round(vals, 3).tolist(),
                                     "target": np.round(want, 3).tolist(), "max_abs_diff": float(round(np.abs(vals - want).max(), 3))},
            "acquisition_mix_web_orders": {"generated": ch, "target_fallback": {k: v / 100 for k, v in FALLBACK_ACQ_MIX.items()}},
            "category_mix_net_sales": {"socks_slippers": float(round(self.l["line_total"][sock].sum() / self.l["line_total"].sum(), 4)),
                                       "target": p["category_mix"]["socks_slippers"]},
            "giving_items_last_12m": {"generated_orders_only": int(o["items"][last].sum()), "brain_items_per_year": p.get("giving_rate_brain"),
                                      "note": "orders only; wholesale and retail units also donate, so this is below the brain rate"},
            "basket": self.basket, "repeat_q": round(self.q_repeat, 4), "repeat_cohort_mean_mult": round(self.repeat_mean_mult, 4),
            "mix_solved": self.mix_solved,
        }

    # ---- run
    def run(self, out):
        t0 = time.time()
        out = Path(out)
        (out / "aggregates").mkdir(parents=True, exist_ok=True)
        self.sqlite_path = out / "data.sqlite"
        self.log(f"generator v2: {self.brand}, scale {self.scale}, seed {self.seed}, {self.start} .. {self.as_of}")
        self.build_orders()
        self.attribute()
        self.build_reversed()
        self.write_sqlite(self.sqlite_path)
        # products needs inventory's final stock: rewrite it now
        db = sqlite3.connect(self.sqlite_path)
        for s, st in zip(SKUS, self.stock_end):
            db.execute("UPDATE products SET stock = ? WHERE sku = ?", (int(st), s))
        db.commit()
        db.close()
        self.aggregates_build()
        for name, rows in self.aggregates.items():
            doc = {"brand": self.brand, "simulated": True, "source": "generator", "computed_at": self.captured_at,
                   "as_of": self.as_of.isoformat(), "scale": self.scale, "seed": self.seed, "table": name, "rows": rows}
            (out / "aggregates" / f"{name}.json").write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
        self.write_meta(out)
        self.log(f"done in {time.time() - t0:.0f}s: {sum(self.counts.values()):,} rows, "
                 f"{self.sqlite_path.stat().st_size / 1e6:.0f} MB sqlite")
        return self

    def write_meta(self, out):
        used = [self.fields[k] for k in self.fields]
        (out / "assumptions.json").write_text(json.dumps({
            "brand": self.brand, "read_from": str(self.assumptions_path.relative_to(APP.parent)),
            "sha256": hashlib.sha256(self.assumptions_path.read_bytes()).hexdigest()[:16],
            "fields": used}, indent=1) + "\n", encoding="utf-8")
        calibrated = sum(1 for k in ("revenue_band", "aov", "repeat_rate", "channel_mix", "seasonality", "giving_units")
                         if self.manifest_fields[k]["origin"] == "brain")
        (out / "manifest.json").write_text(json.dumps({
            "brand": self.brand, "simulated": True, "generated_by": "app/data/generate.py", "version": 2, "seed": self.seed,
            "scale": self.scale, "as_of": self.as_of.isoformat(), "start": self.start.isoformat(), "days": DAYS,
            "calibrated_fields": f"{calibrated} of 6", "fields": self.manifest_fields, "placeholders": PLACEHOLDERS,
            "assumed": ASSUMED,
            "derived": {"basket": self.basket, "repeat_q": round(self.q_repeat, 4), "repeat_cohort_mean_mult": round(self.repeat_mean_mult, 4),
                        "mix_solved": self.mix_solved, "cvr_scale": round(self.cvr_scale, 4), "cvr_by_channel_solved": self.cvr_solved,
                        "google_cpa_scale": round(self.google_cpa_scale, 4), "payout_totals": self.payout_totals}},
            indent=1, default=str) + "\n", encoding="utf-8")
        tables = [{"table": t, "rows": n, "where": "data.sqlite", "source": SOURCE.get(t, "generator"),
                   "shaped_like": SHAPED_LIKE[t]} for t, n in self.counts.items()]
        tables += [{"table": f"aggregates/{k}", "rows": len(v), "where": f"aggregates/{k}.json", "source": "generator",
                    "shaped_like": "rollup of the tables above"} for k, v in self.aggregates.items()]
        (out / "tables.json").write_text(json.dumps({"brand": self.brand, "simulated": True, "as_of": self.as_of.isoformat(),
                                                     "scale": self.scale, "rows": tables}, indent=1) + "\n", encoding="utf-8")
        cal = self.aggregates["calibration"]
        rv, mix, paid, rc = cal["revenue_last_12m"], cal["sales_channel_mix_last_12m"], cal["paid_split_last_12m"], cal["review_checks"]
        pct = lambda v: "unavailable" if v is None else f"{v * 100:.1f}"
        mix_line = ", ".join(f"{k.replace('_', ' ')} {pct(mix['generated'][k])} vs {pct(mix['target'][k])}" for k in mix["generated"])
        paid_line = ", ".join(f"{k.replace('_', ' ')} {pct(v)} vs {pct((paid['target'] or {}).get(k))}"
                              for k, v in (paid["generated"] or {}).items())
        lines = [f"# {self.brand}: simulated data (generator v2)", "",
                 "Simulated data. Every row carries `simulated = 1`. Nothing here is a Bombas result. The shape follows the brain's",
                 f"public profile (`app/brain/{self.brand}/assumptions.json`); performance rates are placeholders listed in `manifest.json`.", "",
                 f"Build: scale {self.scale}, seed {self.seed}, {self.start} to {self.as_of} ({DAYS} days, last full day in America/New_York).",
                 f"Rebuild: `python3 app/data/generate.py --brand {self.brand} --scale {self.scale} --as-of {self.as_of}`.", "",
                 "`data.sqlite` is git-ignored (rebuilt from the seed). `aggregates/*.json`, `manifest.json`, `assumptions.json`, `tables.json` are committed.", "",
                 "## Calibration hit (last 12 months)", "",
                 f"- Revenue: orders {rv['orders_net_sales']:,.0f} plus wholesale fixture {rv['wholesale_fixture']:,.0f} plus marketplace fixture "
                 f"{rv['marketplace_fixture'] or 0:,.0f} = {rv['total']:,.0f} USD against the point {rv['point_scaled']:,.0f} "
                 f"({rv['vs_point_pct']:+.2f} percent); band x scale {rv['band_scaled'][0]:,.0f} to {rv['band_scaled'][1]:,.0f}; in band: {rv['in_band']}",
                 f"- Sales channel mix, percent of revenue (generated vs brain): {mix_line}; largest gap {mix['max_gap_points']} points",
                 f"- Paid split, percent of paid spend (generated vs brain): {paid_line}; largest gap {paid['max_gap_points']} points",
                 f"- AOV (net merchandise per order): {cal['aov']['generated']} vs {cal['aov']['target']} target",
                 f"- Repeat within 12 months: {cal['repeat_12m']['generated']} vs {cal['repeat_12m']['target']}",
                 f"- Seasonality (detrended month index): max gap {cal['seasonality_last_12m']['max_abs_diff']}",
                 f"- Socks, slippers and footwear share of line revenue: {cal['category_mix_net_sales']['socks_slippers']} vs {cal['category_mix_net_sales']['target']}",
                 f"- GA4 sessions per month: {rc['funnel']['sessions_per_month']:,} vs {rc['funnel']['target']:,.0f} assumed; "
                 f"conversion on web orders {pct(rc['funnel']['cvr_on_web_orders'])} percent",
                 f"- Finance join: {rc['finance_join']['skus_with_cogs'] if rc['finance_join'] else 'unavailable'} of {len(SKUS)} products carry a cogs_landed key", "",
                 "## Tables", "", "| Table | Rows | Where | Source | Shaped like |", "|---|---:|---|---|---|"]
        for t in tables:
            lines.append(f"| `{t['table']}` | {t['rows']:,} | {t['where']} | {t['source']} | {t['shaped_like']} |")
        lines += ["", "## How the tables tie together", "",
                  "- Orders are the one truth. GA4 `sessions.transactions` = orders GA4 tracked (a daily share between 91 and 95 percent of web orders); sessions are implied from them by the placeholder conversion rates, scaled by one factor so sessions average the assumed `site_sessions_monthly`.",
                  "- Meta `ad_rows.purchases` = paid social orders credited on click (80 percent) plus 1d_view credit on 7 percent of direct, organic, email, SMS and other orders. Those view orders overlap Google and Klaviyo on purpose.",
                  "- Google `google_rows` campaign conversions = 88 percent of paid search orders plus brand search credit on 5 percent of organic and 4 percent of direct orders. Search term rows drop terms under 10 impressions, so they never sum to the campaign row.",
                  "- Klaviyo `flows` and `campaign_sends`: attributed orders = every email and SMS order plus overlap on direct, organic, paid social and paid search orders. `matched_order_ids` lists them and each id is in `orders`.",
                  "- `payouts`: Shopify Payments charges (PayPal excluded) paid 2 days later, less fees, refunds and dispute moves. `net = charges_gross - charges_fee + refunds_gross + adjustments_gross` (refunds and adjustments are signed).",
                  "- `reversed_orders`: each row is on an order. Returns refund one line with its tax; carrier returns refund the whole order and are excluded from return rate; chargebacks are Shopify Payments orders only. `rto` is null for a US brand and not written.",
                  "- `tickets`: most carry an order id; pre-sale tickets carry none. `reviews` are written from order lines, so every sku is in `products` and review counts follow units sold.",
                  "- `tickets` per order equal `ticket_rate` (5 percent, 8 percent for December orders): order tickets, the 30 percent of returns that open a ticket, and pre-sale questions together.",
                  "- `inventory` falls with units sold and rises with `inbound_pos` receipts. `wholesale_sell_in` is a fixture: the brain's wholesale share of revenue on its own month curve (high in Aug to Oct, low in Dec and Jan), split by the retail partners from their start year; new partners ramp 25, 50, then 100 percent by quarter and DSW is capped at 25 percent of wholesale in its first year. It is not in `orders`.",
                  "- `marketplace_sales` is a fixture: the brain's marketplace share of revenue by month, split Amazon 80 and TikTok Shop 20 (assumed). It is not in `orders`. `marketplace_listings` has no rows: there is no listing detail, so it reads unavailable.",
                  "- `paid_other_spend` is a fixture: daily spend for YouTube creators, TikTok, Pinterest and other at the brain's paid split. Meta and Google spend come from `ad_rows` and `google_rows`; Google CPAs carry one scale so Meta to Google lands on the split.",
                  "- `orders` and `channels_monthly` carry no POS before the first store opened (2025-11-01); `monthly.pos_orders` and `daily.pos_orders` read null there, not 0.",
                  "- `products.sku` and `order_lines.sku` use the finance keys (`BMB-...`), so `finance_inputs.cogs_landed` joins by sku. `finance_inputs` is not written here; it is S2.4 (`contracts/finance-inputs.md`). Its rows start 2025-01-01, so margin before then reads unavailable.",
                  "- `orders.status` and `orders.payment_method` are filled by the generator; a live Shopify pull writes null until the census follow-up (data-sources.md).",
                  "- `orders.acquisition_channel` and `orders.units` are generator conveniences (not census fields); screens should derive channel from utm and units from lines for a real brand."]
        (out / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


SOURCE = {"speed_runs": "fixture", "content_posts": "fixture", "search_console": "fixture", "marketplace_listings": "fixture",
          "inbound_pos": "fixture", "tickets": "fixture", "reviews": "fixture", "wholesale_sell_in": "fixture",
          "marketplace_sales": "fixture", "paid_other_spend": "fixture"}
SHAPED_LIKE = {
    "orders": "Shopify Order + customerJourneySummary", "order_lines": "Shopify LineItem (nested in orders)",
    "customers": "Shopify Customer", "products": "Shopify ProductVariant + GA4 item report (28 days)",
    "inventory": "Shopify InventoryLevel, daily capture", "inbound_pos": "fixture (not in the Shopify census)",
    "reversed_orders": "Shopify Return, Fulfillment, ShopifyPaymentsDispute", "payouts": "ShopifyPaymentsPayout",
    "abandoned_checkouts": "Shopify AbandonedCheckout", "sessions": "GA4 runReport", "ad_rows": "Meta Insights level=ad, time_increment=1",
    "google_rows": "Google Ads GAQL campaign, search_term_view, asset_group", "flows": "Klaviyo Metric Aggregates by flow message",
    "campaign_sends": "Klaviyo Campaign + Metric Aggregates", "tickets": "fixture (Gorgias shape)", "reviews": "fixture (reviews app shape)",
    "speed_runs": "fixture (speed lab)", "content_posts": "fixture (platform exports)", "search_console": "fixture (Search Console shape)",
    "marketplace_listings": "fixture (Amazon Seller shape)", "wholesale_sell_in": "fixture (no connector; brain wholesale share)",
    "marketplace_sales": "fixture (no connector; brain marketplace share, Amazon and TikTok Shop)",
    "paid_other_spend": "fixture (no connector; YouTube creators, TikTok, Pinterest, other at the brain's paid split)",
}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generator v2: brain-calibrated simulated tables")
    ap.add_argument("--brand", default="bombas", help="brain folder name under app/brain/")
    ap.add_argument("--scale", type=float, default=1.0, help="1.0 = the public revenue band; 0.1 for fast dev")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--as-of", default=None, help="last full day (YYYY-MM-DD); default yesterday in America/New_York")
    ap.add_argument("--out", default=None, help="default app/data/brands/<brand>")
    args = ap.parse_args(argv)
    as_of = date.fromisoformat(args.as_of) if args.as_of else None
    out = Path(args.out) if args.out else BRANDS / args.brand
    Gen(args.brand, args.scale, args.seed, as_of).run(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
