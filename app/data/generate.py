#!/usr/bin/env python3
"""Deterministic sample-brand data for the ecomOS app.

Reads sample-brand/brand.json and writes every table in
app/contracts/data-sources.md under sample-brand/ as JSON or CSV, plus
tables.json, the manifest the server reads to find each table.

Same brand.json, same seed, same bytes. Standard library only.

    python app/data/generate.py            write the tables
    python app/data/generate.py --check    regenerate in memory, compare with disk, write nothing
    python app/data/generate.py --out DIR  write somewhere else

How the numbers hang together (the order matters):

    ad_rows (Meta) and google_rows      paid clicks
    flows and campaign_sends (Klaviyo)  email clicks
    sessions (GA4)                      organic base plus the clicks above, then the funnel
    orders (Shopify)                    one order per funnel purchase
    customers, inventory, reversed_orders, tickets, reviews, payouts,
    content_posts, marketplace_listings, search_console, speed_runs
    claims, decisions, registry, contract_status

Four stories are planted on purpose so the first screens have something to
find. They are listed in sample-brand/README.md, not hidden.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import random
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "sample-brand"
DAY = timedelta(days=1)


# ----------------------------------------------------------------- helpers
def r2(x):
    return round(x + 1e-9, 2)


def slug(text):
    out = []
    prev_dash = False
    for c in text.lower():
        if c.isalnum():
            out.append(c)
            prev_dash = False
        elif not prev_dash:
            out.append("-")
            prev_dash = True
    return "".join(out).strip("-")


def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def binom(rng, n, p):
    if n <= 0 or p <= 0:
        return 0
    if p >= 1:
        return n
    if n < 40:
        return sum(1 for _ in range(n) if rng.random() < p)
    mu = n * p
    sd = math.sqrt(n * p * (1 - p))
    return max(0, min(n, int(round(rng.gauss(mu, sd)))))


def lognorm(rng, median, sigma):
    return median * math.exp(rng.gauss(0, sigma))


def pick(rng, items, weights):
    return rng.choices(items, weights=weights, k=1)[0]


def noise(rng, spread):
    return 1 + rng.uniform(-spread, spread)


# ------------------------------------------------------------ fixed lists
MONTH_MULT = {1: 0.72, 2: 0.80, 3: 0.88, 4: 0.95, 5: 1.02, 6: 0.98,
              7: 0.90, 8: 0.90, 9: 0.95, 10: 1.05, 11: 1.45, 12: 1.35}
WEEKDAY_MULT = [1.08, 1.10, 1.05, 1.02, 0.95, 0.85, 0.95]
SPECIAL_DAYS = [  # (start, end, multiplier) layered on the month curve
    (date(2025, 11, 25), date(2025, 11, 27), 1.5),
    (date(2025, 11, 28), date(2025, 11, 28), 3.0),   # Black Friday
    (date(2025, 11, 29), date(2025, 11, 30), 1.9),
    (date(2025, 12, 1), date(2025, 12, 1), 2.6),     # Cyber Monday
    (date(2025, 12, 2), date(2025, 12, 15), 1.35),
    (date(2025, 12, 16), date(2025, 12, 19), 1.1),
    (date(2025, 12, 20), date(2025, 12, 26), 0.5),   # past the shipping cutoff
    (date(2025, 12, 27), date(2025, 12, 31), 0.7),
    (date(2026, 5, 3), date(2026, 5, 9), 1.25),      # Mother's Day week
    (date(2026, 6, 14), date(2026, 6, 20), 1.12),    # Father's Day week
    (date(2026, 7, 4), date(2026, 7, 5), 0.8),
]

# sku, type, title, price, cost, weight_lb, popularity
PRODUCTS = [
    ("TG-CI-001", "cast iron", "10-inch Skillet", 78, 27, 5.2, 8),
    ("TG-CI-002", "cast iron", "12-inch Skillet", 98, 34, 7.4, 10),
    ("TG-CI-003", "cast iron", "8-inch Skillet", 58, 20, 3.6, 6),
    ("TG-CI-004", "cast iron", "5.5-quart Dutch Oven", 165, 58, 12.5, 5),
    ("TG-CI-005", "cast iron", "Double Burner Griddle", 120, 42, 10.8, 3),
    ("TG-CI-006", "cast iron", "Grill Pan", 88, 31, 6.4, 3),
    ("TG-CI-007", "cast iron", "Cornbread Pan", 44, 15, 3.1, 3),
    ("TG-CI-008", "cast iron", "3.5-quart Braiser", 145, 51, 9.6, 2),
    ("TG-LN-001", "linen", "Kitchen Apron, Flax", 68, 22, 0.9, 6),
    ("TG-LN-002", "linen", "Kitchen Apron, Charcoal", 68, 22, 0.9, 4),
    ("TG-LN-003", "linen", "Tea Towel Set of 3", 42, 13, 0.6, 9),
    ("TG-LN-004", "linen", "Napkin Set of 4", 48, 15, 0.5, 5),
    ("TG-LN-005", "linen", "Table Runner", 56, 18, 0.7, 2),
    ("TG-LN-006", "linen", "Bread Bag", 28, 9, 0.3, 3),
    ("TG-LN-007", "linen", "Oven Mitt Pair", 36, 12, 0.5, 5),
    ("TG-LN-008", "linen", "Tablecloth 60 by 90", 110, 36, 1.6, 2),
    ("TG-WB-001", "wooden boards", "End Grain Cutting Board, Walnut", 120, 44, 8.0, 5),
    ("TG-WB-002", "wooden boards", "End Grain Cutting Board, Maple", 105, 38, 7.6, 4),
    ("TG-WB-003", "wooden boards", "Serving Board, Long", 64, 22, 2.4, 5),
    ("TG-WB-004", "wooden boards", "Serving Board, Round", 58, 20, 2.1, 4),
    ("TG-WB-005", "wooden boards", "Bread Board with Crumb Groove", 72, 25, 3.2, 5),
    ("TG-WB-006", "wooden boards", "Mini Cheese Board", 38, 13, 1.1, 4),
    ("TG-WB-007", "wooden boards", "Butcher Block Board", 140, 52, 11.0, 2),
    ("TG-WB-008", "wooden boards", "Board Wax and Oil Kit", 24, 7, 0.8, 7),
    ("TG-KT-001", "kitchen tools", "Chainmail Scrubber", 24, 6, 0.4, 11),
    ("TG-KT-002", "kitchen tools", "Seasoning Wax Puck", 26, 7, 0.3, 10),
    ("TG-KT-003", "kitchen tools", "Walnut Spatula", 32, 10, 0.3, 5),
    ("TG-KT-004", "kitchen tools", "Wooden Spoon Set of 3", 38, 12, 0.5, 4),
    ("TG-KT-005", "kitchen tools", "Pan Scraper Set", 24, 5, 0.2, 5),
    ("TG-KT-006", "kitchen tools", "Silicone Handle Cover", 28, 6, 0.3, 6),
    ("TG-KT-007", "kitchen tools", "Lid for 12-inch Skillet", 48, 16, 3.8, 3),
    ("TG-KT-008", "kitchen tools", "Iron Trivet", 34, 11, 1.6, 3),
    ("TG-GS-001", "gift sets", "Skillet Starter Set", 128, 46, 8.6, 5),
    ("TG-GS-002", "gift sets", "Cast Iron Care Kit", 58, 18, 1.2, 5),
    ("TG-GS-003", "gift sets", "Host Gift Set", 95, 33, 3.5, 3),
    ("TG-GS-004", "gift sets", "Bread Baking Set", 145, 52, 5.8, 2),
    ("TG-GS-005", "gift sets", "Full Kitchen Set", 220, 82, 16.0, 1),
    ("TG-GS-006", "gift sets", "Linen Table Set", 150, 50, 2.6, 2),
    ("TG-GS-007", "gift sets", "Board and Knife Rest Set", 98, 35, 4.2, 2),
    ("TG-GS-008", "gift sets", "Newlywed Set", 185, 66, 12.0, 2),
]
HERO_SKU = "TG-CI-002"
PROBLEM_SKU = "TG-WB-005"     # warps: the reviews and returns story
PROBLEM_FROM = date(2026, 5, 15)
CROSS_SELL = {
    "cast iron": ["TG-KT-001", "TG-KT-002", "TG-KT-006", "TG-KT-007", "TG-KT-005", "TG-GS-002"],
    "wooden boards": ["TG-WB-008", "TG-KT-003", "TG-LN-003"],
    "linen": ["TG-LN-003", "TG-LN-004", "TG-LN-007"],
    "kitchen tools": ["TG-KT-001", "TG-KT-002", "TG-CI-001"],
    "gift sets": ["TG-LN-003", "TG-KT-001", "TG-WB-008"],
}

# code, share of population, combined sales tax rate where the brand has nexus (None: not collected)
STATES = [
    ("CA", 0.117, 0.0868), ("TX", 0.088, 0.0820), ("FL", 0.066, 0.0700), ("NY", 0.060, 0.0850),
    ("PA", 0.039, 0.0634), ("IL", 0.038, 0.0880), ("OH", 0.036, 0.0725), ("GA", 0.032, 0.0735),
    ("NC", 0.032, 0.0698), ("MI", 0.030, 0.0600), ("NJ", 0.028, 0.0663), ("VA", 0.026, 0.0575),
    ("WA", 0.024, 0.0920), ("AZ", 0.022, 0.0837), ("MA", 0.021, 0.0625), ("TN", 0.021, None),
    ("IN", 0.020, None), ("MD", 0.019, None), ("MO", 0.019, None), ("WI", 0.018, None),
    ("CO", 0.018, None), ("MN", 0.017, None), ("SC", 0.016, None), ("AL", 0.015, None),
    ("LA", 0.014, None), ("KY", 0.014, None), ("OR", 0.013, None), ("OK", 0.012, None),
    ("CT", 0.011, None), ("UT", 0.010, None), ("IA", 0.010, None), ("NV", 0.010, None),
    ("AR", 0.009, None), ("MS", 0.009, None), ("KS", 0.009, None), ("NM", 0.006, None),
    ("NE", 0.006, None), ("ID", 0.006, None), ("WV", 0.005, None), ("HI", 0.004, None),
    ("NH", 0.004, None), ("ME", 0.004, None), ("MT", 0.003, None), ("RI", 0.003, None),
    ("DE", 0.003, None), ("SD", 0.003, None), ("ND", 0.002, None), ("AK", 0.002, None),
    ("VT", 0.002, None), ("WY", 0.002, None), ("DC", 0.002, None),
]
STATE_NAMES = {"CA": "California", "TX": "Texas", "FL": "Florida", "NY": "New York", "PA": "Pennsylvania",
               "IL": "Illinois", "OH": "Ohio", "GA": "Georgia", "NC": "North Carolina", "MI": "Michigan",
               "NJ": "New Jersey", "VA": "Virginia", "WA": "Washington", "AZ": "Arizona", "MA": "Massachusetts"}

FIRST_NAMES = ["Dana", "Priya", "Marcus", "Elena", "Tom", "Jordan", "Aisha", "Ben", "Chloe", "Derek",
               "Grace", "Hector", "Ivy", "Jamal", "Kara", "Liam", "Maya", "Noah", "Olivia", "Paul",
               "Quinn", "Rosa", "Sam", "Tara", "Uma", "Victor", "Wes", "Ximena", "Yusuf", "Zoe",
               "Andre", "Bea", "Cal", "Dee", "Eli", "Fay", "Gus", "Hana", "Ian", "Jo",
               "Kip", "Lena", "Milo", "Nia", "Otis", "Pia", "Reed", "Sol"]
LAST_NAMES = ["Reyes", "Okafor", "Lindqvist", "Nguyen", "Brooks", "Patel", "Kowalski", "Haddad", "Murphy", "Santos",
              "Ito", "Fischer", "Delgado", "Osei", "Carter", "Moreau", "Singh", "Byrne", "Novak", "Alvarez",
              "Kim", "Rossi", "Weber", "Chen", "Dubois", "Ferreira", "Hughes", "Jensen", "Larsen", "Mendes",
              "Nakamura", "Oduya", "Petrov", "Quon", "Ruiz", "Schmidt", "Tanaka", "Ueda", "Varga", "Walsh"]

# (source, medium, cvr multiplier, share of the organic base, landing pages with weights)
ORGANIC_SOURCES = [
    ("google", "organic", 1.0, 0.40, [("/", 0.30), ("/products/12-inch-skillet", 0.20), ("/collections/cast-iron", 0.18),
                                       ("/pages/cast-iron-care-guide", 0.17), ("/blogs/journal/how-to-season", 0.15)]),
    ("(direct)", "(none)", 1.3, 0.25, [("/", 0.60), ("/collections/cast-iron", 0.20), ("/collections/gifts", 0.20)]),
    ("instagram", "organic_social", 0.5, 0.08, [("/", 0.45), ("/products/12-inch-skillet", 0.30), ("/collections/linen", 0.25)]),
    ("tiktok", "organic_social", 0.45, 0.06, [("/", 0.40), ("/products/12-inch-skillet", 0.35), ("/products/chainmail-scrubber", 0.25)]),
    ("pinterest.com", "referral", 0.6, 0.04, [("/collections/linen", 0.40), ("/collections/gifts", 0.30), ("/products/end-grain-cutting-board-walnut", 0.30)]),
    ("klaviyo", "sms", 1.6, 0.05, [("/", 0.35), ("/collections/cast-iron", 0.35), ("/collections/gifts", 0.30)]),
    ("bing", "organic", 1.0, 0.03, [("/", 0.50), ("/products/12-inch-skillet", 0.25), ("/collections/cast-iron", 0.25)]),
]
PAID_LANDING = {
    "TG | Prospecting | Broad": [("/products/12-inch-skillet", 0.55), ("/collections/cast-iron", 0.30), ("/", 0.15)],
    "TG | Retargeting | Site 30d": [("/products/12-inch-skillet", 0.35), ("/collections/all", 0.35), ("/cart", 0.30)],
    "TG | Q4 Gifting | Gift buyers": [("/products/skillet-starter-set", 0.50), ("/collections/gifts", 0.50)],
    "Brand Search": [("/", 0.70), ("/collections/cast-iron", 0.30)],
    "Non-brand Search": [("/products/12-inch-skillet", 0.45), ("/collections/cast-iron", 0.30), ("/products/end-grain-cutting-board-walnut", 0.25)],
    "Shopping": [("/products/12-inch-skillet", 0.40), ("/products/10-inch-skillet", 0.25), ("/products/end-grain-cutting-board-walnut", 0.20), ("/products/kitchen-apron-flax", 0.15)],
}
EMAIL_LANDING = [("/", 0.30), ("/collections/cast-iron", 0.25), ("/products/12-inch-skillet", 0.20), ("/collections/gifts", 0.15), ("/cart", 0.10)]

# Meta campaigns, ad sets and ads
META_CAMPAIGNS = [
    ("120210000000101", "TG | Prospecting | Broad", None, None),
    ("120210000000102", "TG | Retargeting | Site 30d", None, None),
    ("120210000000103", "TG | Q4 Gifting | Gift buyers", date(2025, 11, 1), date(2025, 12, 22)),
]
META_ADSETS = {
    "A11": ("120210000000111", "120210000000101", "Broad US 25-55"),
    "A12": ("120210000000112", "120210000000101", "Lookalike 1% purchasers 180d"),
    "A21": ("120210000000121", "120210000000102", "Site visitors 30d"),
    "A22": ("120210000000122", "120210000000102", "Added to cart, no purchase, 7d"),
    "A31": ("120210000000131", "120210000000103", "Gift buyers, broad"),
}
# id, adset, name, creative_id, format, launch, end, ctr0, cvr0, fatigue_k (impressions), weight, dynamic
META_ADS = [
    ("120210000001001", "A11", "Seasoned once, cooks for decades | 12-inch skillet | static", "cr-9001", "image", date(2025, 8, 25), None, 0.0115, 0.028, 4_000_000, 1.0, False),
    ("120210000001002", "A11", "Heavy for a reason | UGC video", "cr-9002", "video", date(2025, 10, 6), None, 0.0140, 0.030, 12_000_000, 0.9, False),
    ("120210000001003", "A11", "Same image, gift copy | static", "cr-9001", "image", date(2025, 11, 1), None, 0.0090, 0.024, 9_000_000, 0.5, False),
    ("120210000001004", "A11", "Dynamic creative | 3 images, 2 texts", "cr-9004", "dynamic", date(2026, 2, 10), None, 0.0120, 0.027, 15_000_000, 0.7, True),
    ("120210000001005", "A12", "Founder story | 45s video", "cr-9005", "video", date(2025, 8, 25), None, 0.0120, 0.031, 5_000_000, 0.8, False),
    ("120210000001006", "A12", "Care guide carousel", "cr-9006", "carousel", date(2026, 4, 14), None, 0.0100, 0.026, 10_000_000, 0.6, False),
    ("120210000001007", "A12", "Skillet vs nonstick | video", "cr-9007", "video", date(2026, 7, 27), None, 0.0190, 0.036, 20_000_000, 1.2, False),
    ("120210000001008", "A21", "Still thinking? 30 days free returns | static", "cr-9008", "image", date(2025, 8, 25), None, 0.0160, 0.060, 30_000_000, 1.0, False),
    ("120210000001009", "A21", "Reviews carousel", "cr-9009", "carousel", date(2025, 8, 25), None, 0.0130, 0.055, 30_000_000, 0.8, False),
    ("120210000001010", "A22", "Your cart, 30 days free returns | catalog", "cr-9010", "dynamic", date(2025, 8, 25), None, 0.0200, 0.080, 40_000_000, 1.0, True),
    ("120210000001011", "A31", "Gift guide | the Starter Set | video", "cr-9011", "video", date(2025, 11, 1), date(2025, 12, 22), 0.0150, 0.035, 6_000_000, 1.0, False),
    ("120210000001012", "A31", "Ships in 2 days from Ohio | static", "cr-9012", "image", date(2025, 11, 10), date(2025, 12, 22), 0.0120, 0.030, 6_000_000, 0.7, False),
]
META_CVR_MULT = {"TG | Prospecting | Broad": 0.30, "TG | Retargeting | Site 30d": 0.9, "TG | Q4 Gifting | Gift buyers": 0.4}

GOOGLE_CAMPAIGNS = [
    # id, name, type, daily cost, ctr, cpc, conv rate, cvr multiplier on site, terms with weights
    ("2101", "Brand Search", "search", 35, 0.18, 0.45, 0.075, 2.2,
     [("tallgrass goods", 0.40), ("tallgrass cast iron", 0.20), ("tallgrass skillet", 0.15), ("tall grass goods skillet", 0.10), ("tallgrass goods returns", 0.08), ("tallgrass goods discount code", 0.07)]),
    ("2102", "Non-brand Search", "search", 55, 0.045, 1.65, 0.018, 0.70,
     [("cast iron skillet", 0.25), ("best cast iron skillet", 0.15), ("12 inch cast iron skillet", 0.15), ("end grain cutting board", 0.12),
      ("linen apron", 0.10), ("cast iron dutch oven", 0.08), ("wedding gift for cooks", 0.07), ("how to season cast iron", 0.05), ("chainmail scrubber", 0.03)]),
    ("2103", "Shopping", "shopping", 40, 0.012, 0.85, 0.022, 0.80,
     [("cast iron skillet 12 inch", 0.30), ("cast iron skillet", 0.20), ("walnut cutting board", 0.15), ("linen kitchen apron", 0.10),
      ("cast iron griddle", 0.10), ("wooden serving board", 0.08), ("cast iron care kit", 0.07)]),
]

# flow, trigger rate (per organic base session unless noted), messages: (channel, name, delay days, retention), open, click, unsub, cvr mult
FLOWS = [
    ("F-01", "Welcome Series", "signups", 0.028,
     [("email", "Email 1: Welcome to Tallgrass", 0, 1.0), ("email", "Email 2: Why cast iron", 2, 0.92), ("sms", "SMS 1: 10% welcome code", 4, 0.35)],
     0.52, 0.090, 0.0030, 1.4),
    ("F-02", "Abandoned Cart", "carts", 0.045,
     [("email", "Email 1: You left something", 0, 1.0), ("email", "Email 2: Free returns, remember", 1, 0.85), ("sms", "SMS 1: Your cart is waiting", 2, 0.30)],
     0.45, 0.075, 0.0020, 2.6),
    ("F-03", "Browse Abandonment", "browses", 0.060,
     [("email", "Email 1: Still looking?", 0, 1.0), ("email", "Email 2: What people say", 2, 0.80)],
     0.40, 0.040, 0.0030, 1.2),
    ("F-04", "Post Purchase", "orders", 1.0,
     [("email", "Email 1: How to season", 3, 1.0), ("email", "Email 2: First cook ideas", 10, 0.95), ("email", "Email 3: Leave a review", 21, 0.90)],
     0.55, 0.050, 0.0010, 0.8),
    ("F-05", "Winback 90d", "winback", 40,
     [("email", "Email 1: It has been a while", 0, 1.0), ("email", "Email 2: New since you visited", 7, 0.85)],
     0.30, 0.025, 0.0060, 1.3),
    ("F-06", "Cast Iron Care", "care", 18,
     [("email", "Email 1: Cleaning without soap fear", 0, 1.0), ("email", "Email 2: Rust is fixable", 14, 0.90), ("email", "Email 3: Restock scrubber and wax", 30, 0.85)],
     0.48, 0.060, 0.0020, 0.6),
]

CAMPAIGN_SUBJECTS = {
    8: ["Back to the stove", "The one pan for weeknights", "Tea towels are back in stock", "How we make the skillet"],
    9: ["Fall table refresh", "Braising season", "New: walnut boards", "The care guide, short version"],
    10: ["Cornbread pan is here", "Host season starts now", "A note on why it is heavy", "Gift guide: for the host"],
    11: ["Gift guide: for the cook who has everything", "Black Friday: the Starter Set", "Cyber Monday: sets only", "Ship by Dec 18 for Christmas",
         "Gift guide: under $50", "What we will not discount", "The Newlywed Set", "Free shipping on every set"],
    12: ["Last day for Christmas shipping", "Gift cards, instant", "Cook the holidays in cast iron", "Thank you, from Ohio"],
    1: ["Cook at home this January", "Rust is fixable", "The Dutch oven, explained", "New year, same skillet"],
    2: ["Valentine dinner at home", "Bread baking set is back", "Why end grain", "Reader recipes"],
    3: ["Spring table linens", "The griddle for pancakes", "Restock: chainmail scrubber", "How to strip and reseason"],
    4: ["Mother's Day gift guide", "New: charcoal apron", "Grill pan season", "Board care in 3 steps"],
    5: ["Mother's Day: order by May 5", "The Host Gift Set", "Wedding season gifts", "Seasoning wax, explained"],
    6: ["Father's Day: the griddle", "Camp cooking in cast iron", "Summer table runner", "Reviews of the month"],
    7: ["Prime Day? We are on Amazon too", "Cornbread, the summer way", "Care kit restock", "The bread board, back in stock"],
}
CAMPAIGN_CODES = {"Black Friday: the Starter Set": "STARTER20", "Cyber Monday: sets only": "SETS20", "Gift guide: for the host": "HOST15",
                  "Mother's Day gift guide": "MOM15", "Father's Day: the griddle": "DAD15", "Valentine dinner at home": "DINNER10"}

TICKET_REASONS = ["where is my order", "product question", "cancel or change order", "discount code", "damaged item",
                  "wrong item", "return request", "shipping question", "unrecognized charge", "other"]

HOOKS = [
    "Seasoned once. Cooks for decades.", "Heavy for a reason.", "The pan my grandmother would have bought.",
    "Stop washing it wrong.", "Rust is not the end.", "3 things nonstick cannot do.", "What 12 inches of iron gets you.",
    "We ship from Ohio in 2 days.", "One board, 8 years, still flat.", "The apron that hides flour.",
    "Cornbread the way it was meant to be.", "Free returns. No questions.", "Why we recycle iron.",
    "The griddle that feeds 6.", "How to strip and reseason in an afternoon.", "A gift they will use every day.",
    "The scrubber that fixes everything.", "Bread board, crumb groove, no mess.", "Sear like a restaurant.",
    "One pan, whole dinner.", "The Dutch oven for people who bake.", "Season with wax, not oil.",
    "What a $98 skillet buys you.", "Linen gets better with washing.", "Made for hosting.",
]

REVIEW_OPENERS = [
    "I bought this before hosting Thanksgiving and it did the whole bird sides.",
    "Gift for my sister's housewarming. She texted a photo of the first cook.",
    "Third piece of Tallgrass iron in my kitchen.",
    "First cast iron I have ever owned.",
    "Replaced a nonstick that lasted 14 months.",
    "Ordered on a Tuesday, cooking on Thursday.",
    "Wedding gift for a couple who cook every night.",
    "I cook for 5 most nights and this gets used daily.",
    "Got this for my dad who thinks nonstick is a scam.",
    "Was skeptical about the price.",
]
REVIEW_PRAISE = {
    "cast iron": ["The seasoning was ready out of the box, eggs slid on day 2.", "Heavy, yes, but the heat holds like nothing else I own.",
                  "Sear on a steak is restaurant level.", "Smooth cooking surface, not the bumpy kind.", "The handle stays cooler than my old pan.",
                  "Cornbread comes out with real crust.", "Went from stove to oven with no drama."],
    "linen": ["Flour wipes right off and it hides stains.", "Soft after the first wash, softer after the fifth.", "Straps are long enough to tie in front.",
              "The napkins look good crumpled, which is how they end up.", "Thick enough to grab a hot handle through."],
    "wooden boards": ["Flat, heavy and the knife stays sharp longer.", "The crumb groove actually catches crumbs.", "Big enough for a whole chicken.",
                      "Oiled it once and the grain came alive.", "Feet keep it from sliding."],
    "kitchen tools": ["The scrubber takes stuck bits off in 10 seconds.", "The wax puck is easier than oil and does not go sticky.",
                      "Spatula edge is thin enough to get under eggs.", "Handle cover means I stop burning myself.", "Scraper set fits every pan corner."],
    "gift sets": ["Came boxed, no wrapping needed.", "The card explains seasoning in plain words.", "Everything in the set gets used.",
                  "Good value against buying the pieces alone.", "Arrived 2 days after ordering, in time for the party."],
}
REVIEW_DETAILS = ["Shipping was fast and the box was solid.", "Customer service answered a care question in an hour.",
                  "I followed the care guide and it has been easy.", "Packaging had no plastic.", "It is heavier than the photos suggest.",
                  "Cheaper than the big brands and I cannot tell the difference.", "Wish I had bought the lid at the same time."]
REVIEW_CLOSERS = ["Would buy again.", "Buying the 10-inch next.", "Recommend to anyone who cooks daily.", "Worth the money.",
                  "This is the one to get.", "Will pass this down."]
REVIEW_COMPLAINTS = {
    "warped": ["The bread board warped within 3 weeks. It rocks on the counter now.", "Board cupped after a month even with oiling.",
               "Crack along the grain after 6 weeks. Support offered a replacement but I wanted it to last."],
    "damaged": ["Arrived with a chip on the rim. The box was crushed.", "Corner of the box was open and the pan had a scratch."],
    "expectation": ["Heavier than I expected, hard for me to lift with one hand.", "Seasoning looked patchy and took 3 cooks to even out.",
                    "Color is darker than the photos.", "Smaller than I pictured. Measure first."],
    "late": ["Took 9 days to arrive, not the 2 days promised on the page.", "Carrier lost it for a week."],
}
REVIEW_TITLES_GOOD = ["Does the job", "Daily driver", "Heavy and worth it", "Best pan in the kitchen", "Great gift", "Exactly as described",
                      "Keeper", "Better than expected", "Solid", "Buy the big one"]
REVIEW_TITLES_BAD = ["Warped", "Not as expected", "Arrived damaged", "Disappointed", "Late and heavy", "Sent it back"]

SC_TERMS = {
    "brand": (["tallgrass goods", "tallgrass cast iron", "tallgrass skillet", "tallgrass goods reviews", "tallgrass goods discount", "tallgrass goods returns",
               "tallgrass linen apron", "tallgrass dutch oven", "tallgrass cutting board", "tall grass goods"], "/", 2.0),
    "product": (["cast iron skillet", "12 inch cast iron skillet", "10 inch cast iron skillet", "8 inch cast iron skillet", "cast iron dutch oven", "cast iron griddle",
                 "cast iron grill pan", "cornbread pan", "cast iron braiser", "smooth cast iron skillet", "recycled cast iron", "made in usa cast iron",
                 "linen apron", "linen kitchen apron", "linen tea towels", "linen napkins", "linen table runner", "linen bread bag", "linen oven mitts", "linen tablecloth",
                 "end grain cutting board", "walnut cutting board", "maple cutting board", "serving board", "bread board with crumb groove", "cheese board",
                 "butcher block board", "board wax", "chainmail scrubber", "seasoning wax", "walnut spatula", "wooden spoon set", "pan scraper", "silicone handle cover",
                 "cast iron lid", "iron trivet", "cast iron starter set", "cast iron care kit", "host gift set", "bread baking set"], "/products/", 12.0),
    "howto": (["how to season cast iron", "how to clean cast iron", "cast iron rust", "how to strip cast iron", "cast iron soap", "cast iron dishwasher",
               "why is my cast iron sticky", "cast iron on glass top stove", "cast iron on induction", "how to oil a cutting board", "cutting board warped",
               "how to wash linen", "linen apron care", "cast iron eggs sticking", "reseason cast iron in oven", "cast iron smoking", "cast iron flaking",
               "store cast iron", "cast iron vs carbon steel", "cast iron vs nonstick"], "/pages/cast-iron-care-guide", 9.0),
    "gift": (["gift for home cook", "housewarming gift", "wedding gift for cooks", "gift for cast iron lover", "kitchen gift set", "gift for dad who cooks",
              "mother's day kitchen gift", "gifts under 50 kitchen", "gift for bread baker", "newlywed kitchen gift"], "/collections/gifts", 14.0),
    "compare": (["best cast iron skillet", "best cast iron skillet 2026", "lodge vs tallgrass", "best cutting board", "best linen apron", "best dutch oven under 200",
                 "cast iron skillet review", "cheap vs expensive cast iron", "is cast iron worth it", "best pan for searing"], "/blogs/journal/", 18.0),
}


# ---------------------------------------------------------------- the generator
class Generator:
    def __init__(self, brand, as_of=None):
        self.brand = brand
        self.name = brand["brand"]
        self.seed = int(brand["seed"])
        self.as_of = date.fromisoformat(as_of or brand["as_of"])
        self.start = self.as_of - timedelta(days=395)          # 13 months, 396 days
        self.days = [self.start + timedelta(days=i) for i in range(396)]
        self.captured_at = iso(datetime.combine(self.as_of + DAY, datetime.min.time()) + timedelta(hours=6))
        self.break_start = self.as_of - timedelta(days=34)     # mobile checkout drop
        self.delay_start = self.as_of - timedelta(days=13)     # USPS delays
        self.speed_regress = date(2026, 8, 17)                 # PDP got heavier
        self.viral_start, self.viral_end = date(2026, 3, 11), date(2026, 3, 20)
        self.day_mult = {}
        n = len(self.days)
        for i, d in enumerate(self.days):
            m = MONTH_MULT[d.month] * WEEKDAY_MULT[d.weekday()] * (1 + 0.25 * i / (n - 1))
            for a, b, k in SPECIAL_DAYS:
                if a <= d <= b:
                    m *= k
            self.day_mult[d] = m
        self.products = [dict(sku=s, type=t, title=ti, price=p, cost=c, weight_lb=w, popularity=pop, handle=slug(ti))
                         for s, t, ti, p, c, w, pop in PRODUCTS]
        self.by_sku = {p["sku"]: p for p in self.products}
        self.tables = {}   # name -> dict(rows, format, source, shaped_like, extra)

    def rng(self, name):
        return random.Random(f"{self.seed}:{name}")

    def in_q4(self, d):
        return d.month in (11, 12) and d.year == 2025

    def paid_mult(self, d):
        return 1.6 if date(2025, 11, 1) <= d <= date(2025, 12, 20) else 1.0

    def growth(self, d):
        return 1 + 0.25 * (d - self.start).days / 395

    # ------------------------------------------------------------- products
    def gen_products(self):
        rng = self.rng("products")
        rows = []
        for p in self.products:
            created = self.start - timedelta(days=rng.randint(120, 900))
            rows.append({
                "sku": p["sku"], "title": p["title"], "handle": p["handle"], "type": p["type"],
                "price": p["price"], "cost": p["cost"], "weight_lb": p["weight_lb"],
                "stock": None,   # filled after inventory
                "images": [f"/img/products/{p['sku'].lower()}-{i}.jpg" for i in (1, 2, 3)],
                "created_at": iso(datetime.combine(created, datetime.min.time()) + timedelta(hours=14)),
                "status": "active",
                "tags": [p["type"], "hero" if p["sku"] == HERO_SKU else "core"],
            })
        self.tables["products"] = dict(rows=rows, format="json", source="shopify_products", shaped_like="Shopify products export plus a cost sheet")

    # ------------------------------------------------------------- Meta ads
    def gen_ad_rows(self):
        rng = self.rng("ad_rows")
        rows = []
        cum = {a[0]: 0 for a in META_ADS}
        camp_by_id = {c[0]: c for c in META_CAMPAIGNS}
        for d in self.days:
            total = 660 * self.day_mult[d] * self.paid_mult(d) * noise(rng, 0.12)
            gifting_on = date(2025, 11, 1) <= d <= date(2025, 12, 22)
            split = {"120210000000101": 0.45 if gifting_on else 0.70,
                     "120210000000102": 0.20 if gifting_on else 0.30,
                     "120210000000103": 0.35 if gifting_on else 0.0}
            cpm = 13.5 * (1.55 if self.in_q4(d) else 1.0) * noise(rng, 0.10)
            for cid, cname, c_start, c_end in META_CAMPAIGNS:
                budget = total * split[cid]
                if budget <= 0:
                    continue
                active = []
                for ad in META_ADS:
                    aid, akey, aname, cr, fmt, launch, end, ctr0, cvr0, k, w, dyn = ad
                    adset = META_ADSETS[akey]
                    if adset[1] != cid or d < launch or (end and d > end):
                        continue
                    weight = w
                    if aid == "120210000001001" and d >= date(2026, 6, 1):
                        weight *= 0.6   # budget shifts away from the tired winner
                    active.append((ad, adset, weight))
                if not active:
                    continue
                wsum = sum(a[2] for a in active)
                for ad, adset, weight in active:
                    aid, akey, aname, cr, fmt, launch, end, ctr0, cvr0, k, w, dyn = ad
                    spend = budget * weight / wsum * noise(rng, 0.15)
                    impressions = int(spend / cpm * 1000)
                    sat = 1 - math.exp(-cum[aid] / k)
                    freq_base = 2.5 if cid == "120210000000102" else 1.15
                    freq = freq_base + (1.5 if cid == "120210000000102" else 0.9) * sat
                    reach = int(impressions / freq)
                    ctr = ctr0 * (0.5 + 0.5 * (1 - sat)) * noise(rng, 0.12)
                    clicks = binom(rng, impressions, ctr)
                    link_clicks = binom(rng, clicks, 0.82)
                    cvr = cvr0 * (0.6 + 0.4 * (1 - sat)) * (1.15 if self.in_q4(d) else 1.0)
                    purchases = binom(rng, link_clicks, cvr)
                    value = sum(lognorm(rng, 88, 0.35) for _ in range(purchases))
                    cum[aid] += impressions
                    rows.append({
                        "date": d.isoformat(), "campaign_id": cid, "campaign_name": cname,
                        "adset_id": adset[0], "adset_name": adset[2], "ad_id": aid, "ad_name": aname,
                        "creative_id": cr, "format": fmt, "is_dynamic_creative": dyn,
                        "spend": r2(spend), "impressions": impressions, "reach": reach, "frequency": r2(freq),
                        "clicks": clicks, "link_clicks": link_clicks, "purchases": purchases, "purchase_value": r2(value),
                        "attribution": "7d_click_1d_view",
                    })
        self.tables["ad_rows"] = dict(rows=rows, format="csv", source="meta_ads_read", shaped_like="Meta ad-level daily insights")
        self.meta_clicks = {}
        for r in rows:
            key = (r["date"], r["campaign_name"])
            self.meta_clicks[key] = self.meta_clicks.get(key, 0) + r["link_clicks"]

    # ----------------------------------------------------------- Google ads
    def gen_google_rows(self):
        rng = self.rng("google_rows")
        rows = []
        self.google_clicks = {}
        for d in self.days:
            for cid, name, ctype, cost_day, ctr, cpc, cr, _, terms in GOOGLE_CAMPAIGNS:
                cost = cost_day * self.day_mult[d] * self.paid_mult(d) * noise(rng, 0.15)
                if name == "Brand Search":
                    cost *= self.growth(d)
                for term, w in terms:
                    c = cost * w * noise(rng, 0.2)
                    clicks = int(c / (cpc * noise(rng, 0.1)))
                    impressions = int(clicks / max(ctr * noise(rng, 0.15), 0.002)) if clicks else int(rng.uniform(5, 40))
                    conv = binom(rng, clicks, cr)
                    rows.append({
                        "date": d.isoformat(), "campaign_id": cid, "campaign": name, "campaign_type": ctype, "search_term": term,
                        "impressions": impressions, "clicks": clicks, "cost": r2(c), "conversions": conv,
                        "conversion_value": r2(sum(lognorm(rng, 86, 0.35) for _ in range(conv))),
                    })
                    key = (d.isoformat(), name)
                    self.google_clicks[key] = self.google_clicks.get(key, 0) + clicks
        self.tables["google_rows"] = dict(rows=rows, format="csv", source="google_ads_read", shaped_like="Google Ads daily by campaign and search term")

    # ------------------------------------------------------------ Klaviyo
    def gen_flows(self):
        rng = self.rng("flows")
        base = {d: 700 * self.day_mult[d] for d in self.days}
        expected_orders = {d: 30 * self.day_mult[d] for d in self.days}
        triggers = {}
        for fid, fname, kind, rate, msgs, o, c, u, mult in FLOWS:
            series = {}
            for d in self.days:
                if kind == "signups":
                    v = base[d] * rate
                elif kind == "carts":
                    v = base[d] * rate
                elif kind == "browses":
                    v = base[d] * rate
                elif kind == "orders":
                    v = expected_orders[d]
                else:
                    v = rate * self.growth(d)
                series[d] = v
            triggers[fid] = series
        rows = []
        self.email_clicks = {}
        for fid, fname, kind, rate, msgs, open_rate, click_rate, unsub_rate, mult in FLOWS:
            for mi, (channel, mname, delay, retention) in enumerate(msgs, start=1):
                for d in self.days:
                    src = d - timedelta(days=delay)
                    if src < self.start:
                        continue
                    sends = int(round(triggers[fid][src] * retention * noise(rng, 0.15)))
                    if sends <= 0:
                        continue
                    delivered = binom(rng, sends, 0.985)
                    if channel == "sms":
                        opens, clicks = None, binom(rng, delivered, click_rate * 1.6)
                        unsubs = binom(rng, delivered, unsub_rate * 1.5)
                    else:
                        opens = binom(rng, delivered, open_rate)
                        clicks = binom(rng, opens, click_rate / open_rate)
                        unsubs = binom(rng, delivered, unsub_rate)
                    rows.append({
                        "flow_id": fid, "flow": fname, "message_id": f"{fid}-M{mi}", "message": mname, "channel": channel,
                        "date": d.isoformat(), "sends": sends, "delivered": delivered, "opens": opens, "clicks": clicks,
                        "unsubscribes": unsubs, "bounces": sends - delivered, "matched_order_ids": [],
                    })
                    if channel == "email":
                        key = (d.isoformat(), fname)
                        self.email_clicks[key] = self.email_clicks.get(key, 0) + clicks
        self.tables["flows"] = dict(rows=rows, format="json", source="klaviyo_flows", shaped_like="Klaviyo flow messages by day")
        self.flow_cvr = {f[1]: f[8] for f in FLOWS}

        # campaigns: 8 a month, 12 in November
        rng2 = self.rng("campaign_sends")
        crows = []
        list_size = 18_000
        n = 0
        for d in self.days:
            send_days = [2, 5, 9, 12, 16, 19, 23, 26] + ([20, 24, 28, 29] if d.month == 11 else [])
            if d.day not in send_days:
                continue
            list_size = int(list_size + 42 * self.day_mult[d] * noise(rng2, 0.3))
            subjects = CAMPAIGN_SUBJECTS[d.month]
            subject = subjects[n % len(subjects)] if d.month != 11 else subjects[send_days.index(d.day) % len(subjects)]
            n += 1
            segment = pick(rng2, ["Engaged 90d", "All subscribers", "Buyers"], [0.6, 0.25, 0.15])
            share = {"Engaged 90d": 0.45, "All subscribers": 1.0, "Buyers": 0.28}[segment]
            sends = int(list_size * share)
            delivered = binom(rng2, sends, 0.992)
            opens = binom(rng2, delivered, 0.38 * noise(rng2, 0.15))
            clicks = binom(rng2, opens, 0.058 * noise(rng2, 0.2))
            name = f"{d.isoformat()} {subject}"
            crows.append({
                "campaign_id": f"C-{len(crows) + 1:04d}", "campaign": name, "subject": subject, "sent_at": iso(datetime.combine(d, datetime.min.time()) + timedelta(hours=14)),
                "channel": "email", "segment": segment, "list_size": list_size, "sends": sends, "delivered": delivered, "opens": opens, "clicks": clicks,
                "unsubscribes": binom(rng2, delivered, 0.0025), "bounces": sends - delivered, "spam_complaints": binom(rng2, delivered, 0.0002),
                "discount_code": CAMPAIGN_CODES.get(subject), "matched_order_ids": [],
            })
            for offset, share_c in ((0, 0.72), (1, 0.28)):
                dd = d + timedelta(days=offset)
                if dd > self.as_of:
                    continue
                key = (dd.isoformat(), name)
                self.email_clicks[key] = self.email_clicks.get(key, 0) + int(clicks * share_c)
        self.tables["campaign_sends"] = dict(rows=crows, format="json", source="klaviyo_campaigns", shaped_like="Klaviyo campaign sends")
        self.campaign_codes = {r["campaign"]: r["discount_code"] for r in crows}

    # ------------------------------------------------------------ sessions
    def funnel(self, rng, n, device, cvr_mult, d, landing):
        if device == "mobile":
            pv, atc, co, pur = 0.56, 0.095, 0.50, 0.52
        else:
            pv, atc, co, pur = 0.62, 0.12, 0.55, 0.58
        if landing.startswith("/products/"):
            pv = 0.97
        if landing == "/cart":
            pv, atc = 0.85, 0.75
        m = math.sqrt(max(cvr_mult, 0.05))
        atc = min(atc * m, 0.9)
        pur = min(pur * m, 0.95)
        if device == "mobile" and d >= self.break_start:
            co *= 0.78
        v = binom(rng, n, pv)
        a = binom(rng, v, atc)
        c = binom(rng, a, co)
        p = binom(rng, c, pur)
        return v, a, c, p

    def gen_sessions(self):
        rng = self.rng("sessions")
        rows = []
        for d in self.days:
            ds = d.isoformat()
            base = 700 * self.day_mult[d] * noise(rng, 0.08)
            specs = []   # (source, medium, campaign, n, cvr_mult, landing weights)
            for source, medium, mult, share, landing in ORGANIC_SOURCES:
                n = base * share
                if source == "google" and medium == "organic":
                    n *= 1 + 0.35 * (d - self.start).days / 395
                if medium == "organic_social" and self.viral_start <= d <= self.viral_end:
                    n *= 6.0 if source == "tiktok" else 2.2
                specs.append((source, medium, "(not set)", int(n), mult, landing))
            for cid, cname, _, _ in META_CAMPAIGNS:
                clicks = self.meta_clicks.get((ds, cname), 0)
                if clicks:
                    fb = int(clicks * 0.88 * 0.6)
                    ig = int(clicks * 0.88) - fb
                    specs.append(("facebook", "paid_social", cname, fb, META_CVR_MULT[cname], PAID_LANDING[cname]))
                    specs.append(("instagram", "paid_social", cname, ig, META_CVR_MULT[cname], PAID_LANDING[cname]))
            for cid, name, ctype, _, _, _, _, mult, _ in GOOGLE_CAMPAIGNS:
                clicks = self.google_clicks.get((ds, name), 0)
                if clicks:
                    specs.append(("google", "cpc", name, int(clicks * 0.9), mult, PAID_LANDING[name]))
            for (dd, cname), clicks in self.email_clicks.items():
                if dd != ds or clicks <= 0:
                    continue
                mult = self.flow_cvr.get(cname, 1.5)
                landing = [("/cart", 0.6), ("/products/12-inch-skillet", 0.4)] if cname == "Abandoned Cart" else EMAIL_LANDING
                specs.append(("klaviyo", "email", cname, int(clicks * 0.95), mult, landing))
            for source, medium, campaign, n, mult, landing in specs:
                if n <= 0:
                    continue
                mobile = binom(rng, n, 0.70 if medium != "(none)" else 0.62)
                for device, count in (("mobile", mobile), ("desktop", n - mobile)):
                    if count <= 0:
                        continue
                    pages = [p for p, _ in landing]
                    weights = [w for _, w in landing]
                    alloc = {p: 0 for p in pages}
                    for _ in range(count):
                        alloc[pick(rng, pages, weights)] += 1
                    for page in pages:
                        k = alloc[page]
                        if k <= 0:
                            continue
                        v, a, c, p = self.funnel(rng, k, device, mult, d, page)
                        rows.append({"date": ds, "source": source, "medium": medium, "campaign": campaign, "landing_page": page, "device": device,
                                     "sessions": k, "product_view": v, "add_to_cart": a, "checkout": c, "purchase": p})
        self.tables["sessions"] = dict(rows=rows, format="csv", source="ga4_export", shaped_like="GA4 daily sessions by source, medium, campaign, landing page and device")

    # -------------------------------------------------------------- orders
    def gen_orders(self):
        rng = self.rng("orders")
        state_codes = [s[0] for s in STATES]
        state_w = [s[1] for s in STATES]
        tax_rate = {s[0]: s[2] for s in STATES}
        customers = []
        cust_index = {}
        orders = []
        handle_to_sku = {p["handle"]: p["sku"] for p in self.products}
        hour_w = [1, 1, 1, 1, 1, 2, 3, 5, 7, 8, 9, 9, 9, 8, 8, 9, 10, 11, 13, 14, 13, 11, 8, 4]

        def new_customer(d):
            n = len(customers)
            first, last = rng.choice(FIRST_NAMES), rng.choice(LAST_NAMES)
            c = {"id": 7000000000 + n + 1, "first_name": first, "last_name": last, "email": f"{first.lower()}.{last.lower()}.{n + 1}@example.com",
                 "state": pick(rng, state_codes, state_w), "segment": pick(rng, ["home_cook", "gift_buyer", "enthusiast"], [0.55, 0.30, 0.15]),
                 "email_consent": rng.random() < 0.78, "sms_consent": rng.random() < 0.31, "first_order_at": None, "last_order_at": None,
                 "orders_count": 0, "total_spent": 0.0}
            customers.append(c)
            return c

        def pick_customer(d, source):
            n = len(customers)
            p_repeat = 0.27 if n > 400 else 0.27 * n / 400
            if source == "klaviyo":
                p_repeat += 0.25
            if rng.random() < p_repeat and n:
                pool = customers[-2500:] if rng.random() < 0.6 else customers
                a, b = rng.choice(pool), rng.choice(pool)
                return a if a["segment"] == "enthusiast" or b["segment"] != "enthusiast" else b
            return new_customer(d)

        def choose_items(d, landing, segment):
            gift_mult = 2.0 if self.in_q4(d) else 1.0
            if segment == "gift_buyer":
                gift_mult *= 1.8
            weights = [p["popularity"] * (gift_mult if p["type"] == "gift sets" else 1.0) * (1.3 if p["sku"] == HERO_SKU and self.in_q4(d) else 1.0)
                       for p in self.products]
            items = []
            first = None
            if landing.startswith("/products/") and rng.random() < 0.5:
                first = handle_to_sku.get(landing.split("/")[-1])
            if first is None:
                first = pick(rng, self.products, weights)["sku"]
            items.append(first)
            n_items = pick(rng, [1, 2, 3], [0.70, 0.22, 0.08])
            while len(items) < n_items:
                ptype = self.by_sku[items[0]]["type"]
                if rng.random() < 0.65:
                    cand = rng.choice(CROSS_SELL[ptype])
                else:
                    cand = pick(rng, self.products, weights)["sku"]
                if cand not in items:
                    items.append(cand)
            lines = []
            for sku in items:
                p = self.by_sku[sku]
                qty = 2 if rng.random() < 0.05 else 1
                lines.append({"sku": sku, "title": p["title"], "qty": qty, "price": p["price"], "line_total": r2(p["price"] * qty)})
            return lines

        sessions = self.tables["sessions"]["rows"]
        for srow in sessions:
            for _ in range(srow["purchase"]):
                d = date.fromisoformat(srow["date"])
                hour = pick(rng, list(range(24)), hour_w)
                created = datetime.combine(d, datetime.min.time()) + timedelta(hours=hour, minutes=rng.randint(0, 59), seconds=rng.randint(0, 59))
                cust = pick_customer(d, srow["source"])
                is_new = cust["orders_count"] == 0
                lines = choose_items(d, srow["landing_page"], cust["segment"])
                subtotal = r2(sum(l["line_total"] for l in lines))
                code, pct = None, 0
                camp_code = self.campaign_codes.get(srow["campaign"]) if srow["medium"] == "email" else None
                if camp_code and rng.random() < 0.55:
                    code, pct = camp_code, int(camp_code[-2:]) / 100
                elif is_new and rng.random() < 0.38:
                    code, pct = "WELCOME10", 0.10
                elif not is_new and rng.random() < 0.12:
                    code, pct = "BACKAGAIN10", 0.10
                discount = r2(subtotal * pct)
                merch = r2(subtotal - discount)
                shipping = 0.0 if merch >= 75 else 6.95
                rate = tax_rate[cust["state"]]
                tax_lines = []
                tax = 0.0
                if rate:
                    tax = r2(merch * rate)
                    tax_lines.append({"jurisdiction": f"US-{cust['state']}", "rate": rate, "amount": tax})
                total = r2(merch + shipping + tax)
                pm = pick(rng, ["card", "shop_pay", "paypal", "apple_pay", "affirm"], [0.52, 0.27, 0.10, 0.08, 0.03])
                if pm == "affirm" and total < 100:
                    pm = "card"
                gateway = {"card": "shopify_payments", "shop_pay": "shopify_payments", "apple_pay": "shopify_payments", "paypal": "paypal", "affirm": "affirm"}[pm]
                cancelled = rng.random() < 0.015
                weight = sum(self.by_sku[l["sku"]]["weight_lb"] * l["qty"] for l in lines)
                carrier = "UPS" if weight > 8 or rng.random() < 0.45 else "USPS"
                ship_days = self.brand["fulfilment"]["ships_in_days"] + pick(rng, [-1, 0, 1, 2], [0.15, 0.55, 0.22, 0.08])
                shipped = datetime.combine(created.date() + timedelta(days=max(ship_days, 0)), datetime.min.time()) + timedelta(hours=14, minutes=rng.randint(0, 210))
                transit = rng.randint(2, 4) if carrier == "UPS" else rng.randint(3, 5)
                if carrier == "USPS" and shipped.date() >= self.delay_start:
                    transit += 3
                delivered = shipped + timedelta(days=transit, hours=rng.randint(-6, 6))
                if cancelled:
                    fstatus, shipped_at, delivered_at = None, None, None
                elif shipped.date() > self.as_of:
                    fstatus, shipped_at, delivered_at = "unfulfilled", None, None
                elif delivered.date() > self.as_of:
                    fstatus, shipped_at, delivered_at = "in_transit", iso(shipped), None
                else:
                    fstatus, shipped_at, delivered_at = "delivered", iso(shipped), iso(delivered)
                tracking = None
                if shipped_at:
                    tracking = ("1Z" + "".join(rng.choice("0123456789ABCDEFGHJKLMNPQRSTUVWXYZ") for _ in range(10))) if carrier == "UPS" \
                        else "94" + "".join(rng.choice("0123456789") for _ in range(12))
                order = {
                    "id": None, "name": None, "created_at": iso(created), "customer_id": cust["id"], "customer_is_new": is_new,
                    "line_items": lines, "subtotal": subtotal,
                    "discount": {"code": code, "amount": discount} if code else None,
                    "shipping": shipping, "tax_lines": tax_lines, "tax": tax, "total": total, "currency": "USD",
                    "payment_method": pm, "gateway": gateway, "cod_confirmed": None,
                    "channel": "shop_app" if (pm == "shop_pay" and rng.random() < 0.25) else "online_store",
                    "utm": {"source": srow["source"], "medium": srow["medium"], "campaign": srow["campaign"]},
                    "landing_page": srow["landing_page"], "device": srow["device"],
                    "ship_state": cust["state"], "ship_country": "US",
                    "financial_status": "voided" if cancelled else "paid",
                    "fulfillment_status": fstatus, "cancelled_at": iso(created + timedelta(hours=rng.randint(1, 30))) if cancelled else None,
                    "fulfilment": {"carrier": carrier if shipped_at else None, "tracking": tracking, "shipped_at": shipped_at, "delivered_at": delivered_at},
                    "refund": None, "return": None, "chargeback": None, "rto": None,
                    "_cust": cust, "_lines_cost": r2(sum(self.by_sku[l["sku"]]["cost"] * l["qty"] for l in lines)),
                }
                orders.append(order)
                if not cancelled:
                    cust["orders_count"] += 1
                    cust["total_spent"] = r2(cust["total_spent"] + total)
                    if cust["first_order_at"] is None:
                        cust["first_order_at"] = order["created_at"]
                    cust["last_order_at"] = order["created_at"]
        orders.sort(key=lambda o: o["created_at"])
        for i, o in enumerate(orders):
            o["id"] = 5700000000000 + i + 1
            o["name"] = f"#{10001 + i}"
            o["order_number"] = 10001 + i
            o["cogs"] = o.pop("_lines_cost")
        self.orders = orders
        self.customers = customers
        self.tables["orders"] = dict(rows=orders, format="json", source="shopify_orders", shaped_like="Shopify orders export")

    def gen_customers(self):
        rows = []
        for c in self.customers:
            if c["orders_count"] == 0:
                continue
            rows.append({k: v for k, v in c.items()})
        self.tables["customers"] = dict(rows=rows, format="csv", source="shopify_customers", shaped_like="Shopify customers export")

    # --------------------------------------------------------- reversed orders
    def gen_reversed(self):
        rng = self.rng("reversed_orders")
        rows = []
        n_ret = n_cb = 0
        for o in self.orders:
            f = o["fulfilment"]
            if o["financial_status"] != "paid":
                continue
            created = datetime.strptime(o["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            if f["delivered_at"]:
                delivered = datetime.strptime(f["delivered_at"], "%Y-%m-%dT%H:%M:%SZ")
                p = 0.06
                types = [self.by_sku[l["sku"]]["type"] for l in o["line_items"]]
                skus = [l["sku"] for l in o["line_items"]]
                if "linen" in types:
                    p += 0.015
                if PROBLEM_SKU in skus and created.date() >= PROBLEM_FROM:
                    p += 0.14
                if rng.random() < p:
                    opened = delivered + timedelta(days=rng.randint(3, 24), hours=rng.randint(0, 20))
                    if opened.date() <= self.as_of:
                        line = rng.choice(o["line_items"])
                        if PROBLEM_SKU in skus and created.date() >= PROBLEM_FROM and rng.random() < 0.7:
                            line = [l for l in o["line_items"] if l["sku"] == PROBLEM_SKU][0]
                            reason = "warped or cracked"
                        else:
                            heavy = self.by_sku[line["sku"]]["weight_lb"] > 5
                            reason = pick(rng, ["changed mind", "not as expected", "damaged in transit", "wrong item", "arrived late", "size or fit"],
                                          [0.30, 0.25, 0.28 if heavy else 0.12, 0.07, 0.10, 0.10 if self.by_sku[line["sku"]]["type"] == "linen" else 0.02])
                        rate = o["tax_lines"][0]["rate"] if o["tax_lines"] else 0
                        amount = r2(line["line_total"] * (1 + rate))
                        closed = opened + timedelta(days=rng.randint(5, 18))
                        outcome = pick(rng, ["refunded", "exchanged", "denied"], [0.78, 0.14, 0.08])
                        n_ret += 1
                        rid = f"RET-{n_ret:05d}"
                        row = {"id": rid, "order_id": o["id"], "type": "return", "reason": reason, "sku": line["sku"], "amount": amount,
                               "opened_at": iso(opened), "closed_at": iso(closed) if closed.date() <= self.as_of else None,
                               "outcome": outcome if closed.date() <= self.as_of else "open", "carrier_received": closed.date() <= self.as_of}
                        rows.append(row)
                        o["return"] = rid
                        if row["outcome"] == "refunded":
                            o["refund"] = {"amount": amount, "at": row["closed_at"], "reason": reason}
            if rng.random() < 0.0048:
                opened = created + timedelta(days=rng.randint(10, 60))
                if opened.date() <= self.as_of:
                    closed = opened + timedelta(days=rng.randint(30, 75))
                    n_cb += 1
                    cid = f"CB-{n_cb:04d}"
                    outcome = pick(rng, ["won", "lost"], [0.45, 0.55]) if closed.date() <= self.as_of else "open"
                    rows.append({"id": cid, "order_id": o["id"], "type": "chargeback",
                                 "reason": pick(rng, ["fraudulent", "product not received", "product unacceptable", "unrecognized"], [0.45, 0.30, 0.15, 0.10]),
                                 "sku": None, "amount": o["total"], "fee": 15.0, "opened_at": iso(opened),
                                 "closed_at": iso(closed) if outcome != "open" else None, "outcome": outcome, "gateway": o["gateway"]})
                    o["chargeback"] = cid
        rows.sort(key=lambda r: (r["opened_at"], r["id"]))
        self.tables["reversed_orders"] = dict(rows=rows, format="json", source="shopify_returns_and_gateway_disputes",
                                              shaped_like="returns, RTO and chargebacks in one table",
                                              extra={"legs": {"return": n_ret, "rto": None, "chargeback": n_cb},
                                                     "rto_note": "null: RTO is a cash-on-delivery leg and this brand sells in the US with no cash on delivery"})

    # -------------------------------------------------------------- tickets
    def gen_tickets(self):
        rng = self.rng("tickets")
        rows = []
        channels = ["email", "chat", "instagram", "phone"]
        ch_w = [0.50, 0.30, 0.12, 0.08]
        frt = {"email": (240, 0.8), "chat": (6, 0.7), "instagram": (120, 0.9), "phone": (3, 0.5)}
        res = {"email": (1440, 0.9), "chat": (40, 0.8), "instagram": (900, 0.9), "phone": (25, 0.6)}

        def make(created, reason, order_id, csat_bias=0):
            ch = pick(rng, channels, ch_w)
            first = lognorm(rng, *frt[ch])
            solved = first + lognorm(rng, *res[ch])
            still_open = (self.as_of - created.date()).days < 2 and rng.random() < 0.5
            csat = None
            if not still_open and rng.random() < 0.45:
                w = [0.05, 0.05, 0.08, 0.22, 0.60]
                if csat_bias:
                    w = [0.15, 0.15, 0.15, 0.25, 0.30]
                csat = pick(rng, [1, 2, 3, 4, 5], w)
            rows.append({"id": None, "created_at": iso(created), "channel": ch, "reason": reason, "order_id": order_id,
                         "first_response_min": int(first), "resolved_min": None if still_open else int(solved),
                         "status": "open" if still_open else "closed", "csat": csat, "tags": [slug(reason), ch]})

        for o in self.orders:
            if o["financial_status"] != "paid":
                continue
            created = datetime.strptime(o["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            f = o["fulfilment"]
            slow = False
            if f["shipped_at"]:
                shipped = datetime.strptime(f["shipped_at"], "%Y-%m-%dT%H:%M:%SZ")
                if f["delivered_at"]:
                    slow = (datetime.strptime(f["delivered_at"], "%Y-%m-%dT%H:%M:%SZ") - shipped).days >= 6
                else:
                    slow = (datetime.combine(self.as_of, datetime.min.time()) - shipped).days >= 5
            p = 0.07 + (0.12 if slow else 0) + (0.25 if o["return"] else 0) + (0.5 if o["chargeback"] else 0)
            if rng.random() >= p:
                continue
            if o["chargeback"] and rng.random() < 0.5:
                make(created + timedelta(days=rng.randint(8, 40)), "unrecognized charge", o["id"])
            elif o["return"]:
                make(created + timedelta(days=rng.randint(6, 25)), pick(rng, ["return request", "damaged item"], [0.7, 0.3]), o["id"])
            elif slow and rng.random() < 0.75:
                shipped = datetime.strptime(f["shipped_at"], "%Y-%m-%dT%H:%M:%SZ")
                t = shipped + timedelta(days=rng.randint(4, 8), hours=rng.randint(8, 21))
                if t.date() <= self.as_of:
                    make(t, "where is my order", o["id"], csat_bias=1)
            else:
                reason = pick(rng, ["where is my order", "product question", "cancel or change order", "discount code", "damaged item", "wrong item", "other"],
                              [0.25, 0.20, 0.15, 0.12, 0.10, 0.05, 0.13])
                delay = {"where is my order": (3, 8), "product question": (1, 20), "cancel or change order": (0, 1), "discount code": (0, 1),
                         "damaged item": (4, 12), "wrong item": (4, 10), "other": (0, 30)}[reason]
                t = created + timedelta(days=rng.randint(*delay), hours=rng.randint(0, 14))
                if t.date() <= self.as_of:
                    make(t, reason, o["id"])
        for d in self.days:
            k = binom(rng, 60, 0.04 * self.day_mult[d])
            for _ in range(k):
                t = datetime.combine(d, datetime.min.time()) + timedelta(hours=rng.randint(7, 22), minutes=rng.randint(0, 59))
                make(t, pick(rng, ["product question", "shipping question", "discount code"], [0.55, 0.25, 0.20]), None)
        rows.sort(key=lambda r: r["created_at"])
        for i, r in enumerate(rows):
            r["id"] = f"T-{100001 + i}"
        self.tables["tickets"] = dict(rows=rows, format="json", source="gorgias_tickets", shaped_like="Gorgias tickets export")

    # -------------------------------------------------------------- reviews
    def gen_reviews(self):
        rng = self.rng("reviews")
        rows = []
        for o in self.orders:
            f = o["fulfilment"]
            if not f["delivered_at"]:
                continue
            cust = o["_cust"]
            p = 0.045 * (1.4 if cust["segment"] == "enthusiast" else 1.0)
            if o["line_items"][0]["sku"] == PROBLEM_SKU and o["created_at"][:10] >= PROBLEM_FROM.isoformat():
                p *= 3.0
            if rng.random() >= p:
                continue
            delivered = datetime.strptime(f["delivered_at"], "%Y-%m-%dT%H:%M:%SZ")
            posted = delivered + timedelta(days=rng.randint(5, 40))
            if posted.date() > self.as_of:
                continue
            line = o["line_items"][0]
            sku = line["sku"]
            ptype = self.by_sku[sku]["type"]
            problem = sku == PROBLEM_SKU and datetime.strptime(o["created_at"], "%Y-%m-%dT%H:%M:%SZ").date() >= PROBLEM_FROM
            if problem:
                rating = pick(rng, [1, 2, 3, 4, 5], [0.20, 0.20, 0.15, 0.15, 0.30])
            elif o["return"]:
                rating = pick(rng, [1, 2, 3, 4, 5], [0.30, 0.30, 0.20, 0.15, 0.05])
            else:
                rating = pick(rng, [1, 2, 3, 4, 5], [0.02, 0.03, 0.06, 0.20, 0.69])
            source = pick(rng, ["site", "amazon"], [0.72, 0.28])
            if rating >= 4:
                parts = []
                if rng.random() < 0.8:
                    parts.append(rng.choice(REVIEW_OPENERS))
                parts.append(rng.choice(REVIEW_PRAISE[ptype]))
                if rng.random() < 0.55:
                    parts.append(rng.choice(REVIEW_PRAISE[ptype]))
                if rng.random() < 0.5:
                    parts.append(rng.choice(REVIEW_DETAILS))
                if rating == 4 and rng.random() < 0.6:
                    parts.append(rng.choice(REVIEW_COMPLAINTS["expectation"]))
                if rng.random() < 0.7:
                    parts.append(rng.choice(REVIEW_CLOSERS))
                title = rng.choice(REVIEW_TITLES_GOOD)
            else:
                if problem:
                    key = "warped"
                else:
                    key = pick(rng, ["damaged", "expectation", "late"], [0.35, 0.45, 0.20])
                parts = [rng.choice(REVIEW_COMPLAINTS[key])]
                if rating == 3:
                    parts.append(rng.choice(REVIEW_PRAISE[ptype]))
                if rng.random() < 0.4:
                    parts.append("Support was quick to answer." if rng.random() < 0.6 else "Still waiting to hear back from support.")
                title = rng.choice(REVIEW_TITLES_BAD)
            text = " ".join(dict.fromkeys(parts))
            rows.append({"id": None, "source": source, "sku": sku, "product": line["title"], "rating": rating, "title": title, "text": text,
                         "author": f"{cust['first_name']} {cust['last_name'][0]}.", "verified": True if source == "site" else rng.random() < 0.8,
                         "order_id": o["id"] if source == "site" else None, "date": posted.date().isoformat(),
                         "responded_at": (posted + timedelta(days=rng.randint(1, 5))).date().isoformat() if rating <= 3 and rng.random() < 0.8 else None})
        rows.sort(key=lambda r: (r["date"], r["sku"]))
        for i, r in enumerate(rows):
            r["id"] = f"R-{i + 1:05d}"
        self.tables["reviews"] = dict(rows=rows, format="json", source="judgeme_and_amazon_reviews", shaped_like="site and Amazon reviews")

    # ------------------------------------------------------------ inventory
    def gen_inventory(self):
        rng = self.rng("inventory")
        sold = {}
        for o in self.orders:
            if o["financial_status"] != "paid":
                continue
            d = o["created_at"][:10]
            for l in o["line_items"]:
                sold[(d, l["sku"])] = sold.get((d, l["sku"]), 0) + l["qty"]
        rows, pos = [], []
        lead = {"cast iron": 42, "linen": 28, "wooden boards": 21, "kitchen tools": 21, "gift sets": 30}
        current = {}
        for p in self.products:
            sku = p["sku"]
            total = sum(v for (d, s), v in sold.items() if s == sku)
            avg = max(total / 396, 0.2)
            lt0 = lead[p["type"]]
            on_hand = int(round((lt0 + 60) * avg))
            reorder_at = int(round(1.6 * lt0 * avg))
            qty = int(round(84 * avg))
            open_po = None
            n_po = 0
            for d in self.days:
                ds = d.isoformat()
                received = 0
                if open_po and open_po["expected_at"] <= ds and open_po["received_at"] is None:
                    open_po["received_at"] = ds
                    received = open_po["qty"]
                    on_hand += received
                    open_po = None
                s = sold.get((ds, sku), 0)
                backordered = 0
                if s > on_hand:
                    backordered = s - on_hand
                    on_hand = 0
                else:
                    on_hand -= s
                if open_po is None and on_hand <= reorder_at:
                    n_po += 1
                    lt = lead[p["type"]]
                    note = None
                    if sku == HERO_SKU and d >= date(2026, 6, 1):
                        lt += 21
                        note = "port delay, supplier confirmed 21 days late"
                    open_po = {"po_id": f"PO-{sku}-{n_po:02d}", "sku": sku, "qty": qty, "ordered_at": ds,
                               "expected_at": (d + timedelta(days=lt)).isoformat(), "received_at": None, "unit_cost": p["cost"], "note": note}
                    pos.append(open_po)
                rows.append({"date": ds, "sku": sku, "on_hand": on_hand, "sold": s, "received": received, "backordered": backordered,
                             "inbound": open_po["qty"] if open_po else 0, "inbound_expected": open_po["expected_at"] if open_po else None})
            current[sku] = on_hand
        rows.sort(key=lambda r: (r["date"], r["sku"]))
        pos.sort(key=lambda r: (r["ordered_at"], r["sku"]))
        for row in self.tables["products"]["rows"]:
            row["stock"] = current[row["sku"]]
        self.tables["inventory"] = dict(rows=rows, format="csv", source="shopify_inventory_and_3pl", shaped_like="stock by sku by day")
        self.tables["purchase_orders"] = dict(rows=pos, format="json", source="3pl_inbound", shaped_like="inbound purchase orders (companion to inventory)")

    # -------------------------------------------------------------- payouts
    def gen_payouts(self):
        rows = []
        refunds_by_day = {}
        cb_by_day = {}
        for r in self.tables["reversed_orders"]["rows"]:
            if r["type"] == "chargeback":
                cb_by_day[(r["opened_at"][:10], r["gateway"])] = cb_by_day.get((r["opened_at"][:10], r["gateway"]), 0) + r["amount"]
        order_gw = {o["id"]: o["gateway"] for o in self.orders}
        for r in self.tables["reversed_orders"]["rows"]:
            if r["type"] == "return" and r["outcome"] == "refunded":
                key = (r["closed_at"][:10], order_gw[r["order_id"]])
                refunds_by_day[key] = refunds_by_day.get(key, 0) + r["amount"]
        fee = {"shopify_payments": (0.029, 0.30), "paypal": (0.0349, 0.49), "affirm": (0.0599, 0.30)}
        for gw in ("shopify_payments", "paypal", "affirm"):
            start = self.start
            while start <= self.as_of:
                end = min(start + timedelta(days=6), self.as_of)
                s, e = start.isoformat(), end.isoformat()
                ords = [o for o in self.orders if o["gateway"] == gw and o["financial_status"] == "paid" and s <= o["created_at"][:10] <= e]
                gross = r2(sum(o["total"] for o in ords))
                fees = r2(sum(o["total"] * fee[gw][0] + fee[gw][1] for o in ords))
                refunds = r2(sum(v for (d, g), v in refunds_by_day.items() if g == gw and s <= d <= e))
                cbs = r2(sum(v for (d, g), v in cb_by_day.items() if g == gw and s <= d <= e))
                cb_fees = 15.0 * sum(1 for (d, g), v in cb_by_day.items() if g == gw and s <= d <= e)
                net = r2(gross - fees - refunds - cbs - cb_fees)
                deposit = end + timedelta(days=2 if end.weekday() < 5 else 4)
                rows.append({"gateway": gw, "period_start": s, "period_end": e, "orders": len(ords), "gross": gross, "fees": fees, "refunds": refunds,
                             "chargebacks": cbs, "chargeback_fees": cb_fees, "net": net, "currency": "USD", "deposit_date": deposit.isoformat(),
                             "status": "paid" if deposit <= self.as_of else "pending"})
                start = end + DAY
        # Amazon settles every 14 days
        rng = self.rng("payouts")
        start = self.start
        while start <= self.as_of:
            end = min(start + timedelta(days=13), self.as_of)
            units = 0
            gross = 0.0
            for i in range((end - start).days + 1):
                d = start + timedelta(days=i)
                u = int(round(14 * self.day_mult[d] * (1 + 0.6 * (d - self.start).days / 395) * (3.0 if d in (date(2026, 7, 14), date(2026, 7, 15)) else 1.0) * noise(rng, 0.2)))
                units += u
                gross += u * 92 * noise(rng, 0.1)
            gross = r2(gross)
            fees = r2(gross * 0.15 + units * 6.5)
            refunds = r2(gross * 0.05)
            net = r2(gross - fees - refunds)
            rows.append({"gateway": "amazon", "period_start": start.isoformat(), "period_end": end.isoformat(), "orders": units, "gross": gross, "fees": fees,
                         "refunds": refunds, "chargebacks": 0.0, "chargeback_fees": 0.0, "net": net, "currency": "USD",
                         "deposit_date": (end + timedelta(days=5)).isoformat(), "status": "paid" if end + timedelta(days=5) <= self.as_of else "pending"})
            start = end + DAY
        rows.sort(key=lambda r: (r["period_start"], r["gateway"]))
        self.tables["payouts"] = dict(rows=rows, format="json", source="shopify_payments_paypal_affirm_amazon", shaped_like="gateway and marketplace settlements")

    # ---------------------------------------------------------- content posts
    def gen_content_posts(self):
        rng = self.rng("content_posts")
        rows = []
        n = 0
        for d in self.days:
            if d.weekday() not in (0, 2, 4):
                continue
            n += 1
            platform = pick(rng, ["instagram", "tiktok", "youtube_shorts", "pinterest"], [0.45, 0.35, 0.10, 0.10])
            fmt = {"instagram": pick(rng, ["reel", "carousel", "static"], [0.55, 0.30, 0.15]), "tiktok": "video", "youtube_shorts": "short", "pinterest": "pin"}[platform]
            median = {"instagram": 6000, "tiktok": 18000, "youtube_shorts": 9000, "pinterest": 2500}[platform]
            views = int(lognorm(rng, median * self.growth(d), 0.8))
            hook = rng.choice(HOOKS)
            if d == self.viral_start:
                platform, fmt, views, hook = "tiktok", "video", 1_240_000, "Stop washing it wrong."
            rows.append({"id": f"P-{n:04d}", "platform": platform, "date": d.isoformat(), "format": fmt, "hook": hook,
                         "views": views, "saves": binom(rng, views, 0.018), "clicks": binom(rng, views, 0.006), "matched_order_ids": []})
        # match organic social orders to the newest post on that platform in the last 3 days
        by_platform = {}
        for r in rows:
            by_platform.setdefault(r["platform"], []).append(r)
        for o in self.orders:
            if o["utm"]["medium"] != "organic_social":
                continue
            plat = o["utm"]["source"]
            d = o["created_at"][:10]
            cands = [r for r in by_platform.get(plat, []) if r["date"] <= d and (date.fromisoformat(d) - date.fromisoformat(r["date"])).days <= 3]
            if cands:
                cands[-1]["matched_order_ids"].append(o["id"])
        for r in rows:
            r["matched_orders"] = len(r["matched_order_ids"])
        self.tables["content_posts"] = dict(rows=rows, format="json", source="platform_exports", shaped_like="organic posts with matched orders")

    # --------------------------------------------------------- search console
    def gen_search_console(self):
        rng = self.rng("search_console")
        rows = []
        months = []
        d = self.start.replace(day=1)
        while d <= self.as_of:
            months.append(d)
            d = (d.replace(day=28) + timedelta(days=4)).replace(day=1)
        for tier, (terms, page, base_pos) in SC_TERMS.items():
            for t in terms:
                pos0 = base_pos * noise(rng, 0.5)
                impr0 = {"brand": 900, "product": 1400, "howto": 2600, "gift": 800, "compare": 1600}[tier] * lognorm(rng, 1, 0.7)
                target = page
                if page.endswith("/") and page != "/":
                    target = page + slug(t)
                for i, m in enumerate(months):
                    pos = max(1.0, pos0 * (1 - 0.35 * i / max(len(months) - 1, 1)))
                    ctr = min(0.45, 0.32 * math.exp(-0.28 * (pos - 1)) + 0.005)
                    season = MONTH_MULT[m.month] * (1.6 if tier == "gift" and m.month in (11, 12, 5) else 1.0)
                    impressions = int(impr0 * season * (1 + 0.35 * i / max(len(months) - 1, 1)) * noise(rng, 0.2))
                    clicks = binom(rng, impressions, ctr)
                    rows.append({"month": m.strftime("%Y-%m"), "query": t, "page": target, "clicks": clicks, "impressions": impressions,
                                 "ctr": round(clicks / impressions, 4) if impressions else 0.0, "position": round(pos, 1)})
        self.tables["search_console"] = dict(rows=rows, format="csv", source="search_console", shaped_like="Search Console query and page report by month")

    # ------------------------------------------------------- marketplace
    def gen_marketplace(self):
        rng = self.rng("marketplace_listings")
        rows = []
        top = sorted(self.products, key=lambda p: -p["popularity"])[:15]
        top.sort(key=lambda p: p["sku"])
        for p in top:
            asin = "B0" + "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789") for _ in range(8))
            bb = round(rng.uniform(0.82, 0.99), 2)
            note = None
            if p["sku"] == HERO_SKU:
                bb, note = 0.42, "buy box lost to reseller KitchenDeals LLC at $91.99 since 2026-09-03"
            price = math.floor(p["price"] * 1.04) + 0.99
            rows.append({"marketplace": "amazon", "listing_id": asin, "sku": p["sku"], "title": f"Tallgrass Goods {p['title']}", "price": price,
                         "buy_box_share": bb, "stock": int(lognorm(rng, 60, 0.6)), "rating": round(rng.uniform(4.2, 4.8), 1),
                         "reviews_count": int(lognorm(rng, 120, 0.7)), "units_30d": int(p["popularity"] * lognorm(rng, 9, 0.4)),
                         "bsr_category": int(lognorm(rng, 4000, 0.9)), "referral_fee_rate": 0.15, "fba_fee": r2(4.5 + 0.35 * p["weight_lb"]),
                         "status": "active", "snapshot_date": self.as_of.isoformat(), "note": note})
        self.tables["marketplace_listings"] = dict(rows=rows, format="json", source="amazon_seller_read", shaped_like="Amazon Seller listing snapshot")

    # ------------------------------------------------------------ speed runs
    def gen_speed_runs(self):
        rng = self.rng("speed_runs")
        rows = []
        pages = [("home", "/", 2100, 1100, 5200, 1_900_000, 78, 380, 0.04),
                 ("collection", "/collections/cast-iron", 2400, 1200, 5600, 2_300_000, 84, 420, 0.06),
                 ("pdp", "/products/12-inch-skillet", 2300, 1150, 5400, 2_100_000, 88, 450, 0.05),
                 ("cart", "/cart", 1800, 950, 4100, 1_400_000, 61, 260, 0.02)]
        profile = "Moto G Power, slow 4G 1.6 Mbps 150 ms RTT, 4x CPU, cold cache"
        run_id = 0

        def one(page, url, variant, run, d, lcp, fcp, load, size, req, tbt, cls, third_share, errors):
            nonlocal run_id
            run_id += 1
            n = noise(rng, 0.06)
            return {"run_id": run_id, "page": page, "url": f"https://www.tallgrassgoods.example{url}", "variant": variant, "run": run, "device": "mobile",
                    "profile": profile, "fcp_ms": int(fcp * n), "lcp_ms": int(lcp * n), "dcl_ms": int(load * 0.55 * n), "load_ms": int(load * n),
                    "cls": round(cls * noise(rng, 0.3), 3), "tbt_est_ms": int(tbt * n), "requests": int(req * noise(rng, 0.03)),
                    "bytes": int(size * n), "first_party_bytes": int(size * n * (1 - third_share)), "third_party_bytes": int(size * n * third_share),
                    "console_errors": errors, "measured_at": iso(datetime.combine(d, datetime.min.time()) + timedelta(hours=3)), "note": "fixture, not a measured run"}

        for d in self.days:
            if d.weekday() != 0:
                continue
            for page, url, lcp, fcp, load, size, req, tbt, cls in pages:
                third = 0.22
                errors = 0
                if page == "pdp" and d >= self.speed_regress:
                    lcp, fcp, load, size, req, tbt, third, errors = 3900, 1500, 7800, 3_100_000, 112, 910, 0.41, 2
                rows.append(one(page, url, "baseline", 1, d, lcp, fcp, load, size, req, tbt, cls, third, errors))
        fix_day = self.as_of - timedelta(days=2)
        chain = [("f01-defer-reviews-widget", 3000, 1350, 6600, 2_600_000, 98, 640, 0.30, 1),
                 ("f02-defer-chat-script", 2500, 1200, 5900, 2_250_000, 90, 470, 0.24, 0),
                 ("f03-image-sizes", 2200, 1150, 5400, 2_000_000, 88, 450, 0.24, 0)]
        for variant, lcp, fcp, load, size, req, tbt, third, errors in chain:
            for run in (1, 2, 3):
                rows.append(one("pdp", "/products/12-inch-skillet", variant, run, fix_day, lcp, fcp, load, size, req, tbt, 0.05, third, errors))
        self.tables["speed_runs"] = dict(rows=rows, format="json", source="speed_lab.measure", shaped_like="speed lab run summaries (fixture)")

    # ------------------------------------------- brand brain and memory tables
    def gen_memory_tables(self):
        claims = []
        for tier in ("approved", "site_backed", "forbidden"):
            for i, text in enumerate(self.brand["claims"][tier], start=1):
                claims.append({"id": f"CLM-{tier[:3].upper()}-{i:02d}", "claim_text": text, "tier": tier,
                               "source": "brand.json" if tier != "site_backed" else "site: /pages/warranty",
                               "product_or_page": "cast iron" if "iron" in text else "sitewide", "added_at": self.start.isoformat()})
        self.tables["claims"] = dict(rows=claims, format="json", source="brand_brain", shaped_like="claims with tiers")
        decisions = [
            {"id": "DEC-0001", "at": iso(datetime(2026, 9, 8, 15, 20)), "screen": "11-paid-social", "capability_id": "CREA-C15",
             "capability": "Diagnose creative fatigue and plan revivals", "autonomy": "agent_does", "choice": "agent",
             "context": "Ad 120210000001001 CTR down 45 percent from its 90 day median at frequency 2.1", "note": "seed example, not a real decision"},
            {"id": "DEC-0002", "at": iso(datetime(2026, 9, 15, 10, 5)), "screen": "19-supply-inventory", "capability_id": "MEDIA-C42",
             "capability": "Pace ad spend against live stock", "autonomy": "human_assist", "choice": "not_now",
             "context": "12-inch Skillet cover under 3 weeks with the PO 21 days late", "note": "seed example, not a real decision"},
        ]
        self.tables["decisions"] = dict(rows=decisions, format="json", source="screens", shaped_like="decision log (seed examples; the live log is app/data/decisions.json)")
        registry = [
            {"id": "EXP-0001", "name": "Free shipping threshold $75 vs $60", "screen": "04-offers-pricing", "capability_id": "SITE-C18",
             "hypothesis": "A $60 threshold lifts conversion more than it costs in shipping", "metric": "contribution_margin",
             "started_at": "2026-02-03", "ended_at": "2026-03-02", "status": "lost", "result": "CVR +0.1 point, margin per order down $2.40",
             "learning": "Keep $75. Push the second item instead."},
            {"id": "EXP-0002", "name": "PDP hero video vs static on the 12-inch skillet", "screen": "07-landing-pages-cro", "capability_id": "SITE-C36",
             "hypothesis": "A 12 second video of the sear lifts add to cart on mobile", "metric": "add_to_cart_rate",
             "started_at": "2026-05-11", "ended_at": "2026-06-08", "status": "won", "result": "Add to cart +11 percent on mobile, flat on desktop",
             "learning": "Ship the video to the 10-inch page next."},
            {"id": "EXP-0003", "name": "Welcome SMS with 10 percent vs free shipping", "screen": "14-email-messaging", "capability_id": "LIFE-C04",
             "hypothesis": "Free shipping converts new subscribers as well as 10 percent at lower cost", "metric": "revenue_by_flow_order_matched",
             "started_at": "2026-09-01", "ended_at": None, "status": "running", "result": None, "learning": None},
        ]
        self.tables["registry"] = dict(rows=registry, format="json", source="screens", shaped_like="experiment registry")

    def gen_contract_status(self):
        tables = []
        for name, t in self.tables.items():
            tables.append({"table": name, "source": t["source"], "rows": len(t["rows"]), "captured_at": self.captured_at, "fresh": True})
        metrics = [
            ("sessions", True, None, None), ("product_view_rate", True, None, None), ("add_to_cart_rate", True, None, None),
            ("checkout_rate", True, None, None), ("cvr_overall", True, None, None), ("aov", True, None, None),
            ("repeat_rate_90d", True, None, None), ("money_at_stake", True, None, None),
            ("return_rate", True, None, None), ("chargeback_rate", True, None, None), ("dispute_win_rate", True, None, None),
            ("return_to_sender_rate", False, "carrier exception feed not connected", "carrier_events"),
            ("rto_rate", False, "market US: no cash on delivery, so no return to origin leg", None),
            ("payment_method_mix", True, "cod_share reads null for a US brand", None),
            ("spend", True, None, None), ("period_roas", True, None, None), ("mer", True, None, None), ("cpa", True, None, None), ("frequency", True, None, None),
            ("revenue_by_flow_order_matched", True, None, None), ("list_growth", True, "from welcome sends and unsubscribes, not a list export", None),
            ("ltv_180d", True, None, None), ("contribution_margin", True, None, None),
            ("cash_runway_weeks", False, "no bank or accounting connector", "accounting"),
            ("sales_tax_collected", True, "collected in 15 nexus states; other states read 0 by policy, not by gap", None),
            ("fully_loaded_ms", True, "speed_runs is a fixture, not a measured run", None),
        ]
        mrows = [{"metric": m, "available": a, "note": n, "connector_that_fixes_it": c} for m, a, n, c in metrics]
        self.tables["contract_status"] = dict(rows=tables, format="json", source="generate.py", shaped_like="table freshness and metric availability",
                                              extra={"metrics": mrows, "computed_at": self.captured_at})

    # ---------------------------------------------------------------- match
    def match_email_orders(self):
        by_key = {}
        for o in self.orders:
            if o["utm"]["medium"] == "email":
                by_key.setdefault((o["created_at"][:10], o["utm"]["campaign"]), []).append(o["id"])
        for r in self.tables["flows"]["rows"]:
            if r["channel"] == "email":
                r["matched_order_ids"] = by_key.get((r["date"], r["flow"]), [])
                r["matched_orders"] = len(r["matched_order_ids"])
            else:
                r["matched_orders"] = 0
        for r in self.tables["campaign_sends"]["rows"]:
            d0 = date.fromisoformat(r["sent_at"][:10])
            ids = []
            for k in range(3):
                ids += by_key.get(((d0 + timedelta(days=k)).isoformat(), r["campaign"]), [])
            r["matched_order_ids"] = ids
            r["matched_orders"] = len(ids)

    # ------------------------------------------------------------------ run
    def run(self):
        self.gen_products()
        self.gen_ad_rows()
        self.gen_google_rows()
        self.gen_flows()
        self.gen_sessions()
        self.gen_orders()
        self.gen_customers()
        self.gen_reversed()
        self.gen_tickets()
        self.gen_reviews()
        self.gen_inventory()
        self.gen_payouts()
        self.gen_content_posts()
        self.gen_search_console()
        self.gen_marketplace()
        self.gen_speed_runs()
        self.gen_memory_tables()
        self.match_email_orders()
        for o in self.orders:
            o.pop("_cust", None)
        self.gen_contract_status()
        return self.render()

    def render(self):
        files = {}
        manifest = {"brand": self.name, "fictional": True, "seed": self.seed, "as_of": self.as_of.isoformat(), "start": self.start.isoformat(),
                    "captured_at": self.captured_at, "generated_by": "app/data/generate.py", "tables": {}}
        for name, t in self.tables.items():
            fname = f"{name}.{t['format']}"
            rows = t["rows"]
            if t["format"] == "json":
                head = {"brand": self.name, "fictional": True, "source": t["source"], "captured_at": self.captured_at, "table": name, "rows_count": len(rows)}
                head.update(t.get("extra", {}))
                buf = io.StringIO()
                buf.write("{\n")
                for k, v in head.items():
                    buf.write(f"{json.dumps(k)}: {json.dumps(v, ensure_ascii=True)},\n")
                buf.write('"rows": [\n')
                for i, r in enumerate(rows):
                    buf.write(json.dumps(r, separators=(",", ":"), ensure_ascii=True))
                    buf.write(",\n" if i < len(rows) - 1 else "\n")
                buf.write("]\n}\n")
                files[fname] = buf.getvalue().encode("utf-8")
            else:
                buf = io.StringIO()
                cols = list(rows[0].keys()) if rows else []
                w = csv.writer(buf, lineterminator="\n")
                w.writerow(cols)
                for r in rows:
                    w.writerow(["" if r[c] is None else ("true" if r[c] is True else "false" if r[c] is False else r[c]) for c in cols])
                files[fname] = buf.getvalue().encode("utf-8")
            manifest["tables"][name] = {"file": fname, "format": t["format"], "rows": len(rows), "source": t["source"],
                                        "shaped_like": t["shaped_like"], "captured_at": self.captured_at,
                                        "sha256": hashlib.sha256(files[fname]).hexdigest()[:16]}
        files["tables.json"] = (json.dumps(manifest, indent=1) + "\n").encode("utf-8")
        return files


# ----------------------------------------------------------------- entry
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--brand", default=str(SAMPLE / "brand.json"))
    ap.add_argument("--out", default=str(SAMPLE))
    ap.add_argument("--as-of", default=None, help="override brand.json as_of (YYYY-MM-DD)")
    ap.add_argument("--check", action="store_true", help="regenerate in memory and compare with the files on disk; write nothing")
    args = ap.parse_args(argv)
    brand = json.loads(Path(args.brand).read_text(encoding="utf-8"))
    files = Generator(brand, args.as_of).run()
    out = Path(args.out)
    if args.check:
        bad = 0
        for fname, data in files.items():
            p = out / fname
            same = p.exists() and p.read_bytes() == data
            print(f"{'same' if same else 'DIFF'}  {fname}")
            bad += 0 if same else 1
        print("identical" if not bad else f"{bad} file(s) differ")
        return 1 if bad else 0
    out.mkdir(parents=True, exist_ok=True)
    total = 0
    for fname, data in files.items():
        (out / fname).write_bytes(data)
        total += len(data)
    manifest = json.loads(files["tables.json"].decode("utf-8"))
    for name, t in manifest["tables"].items():
        print(f"{name:22s} {t['rows']:7d} rows  {t['file']}")
    print(f"{len(files)} files, {total / 1e6:.1f} MB, as_of {manifest['as_of']}, seed {manifest['seed']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
