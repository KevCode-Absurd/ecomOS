"""Fetch public gehnaindia.com pages and save the promises they make.

Run: python3 reviews/copy-test/blind/raw-1/site_snapshot.py
Writes: reviews/copy-test/blind/raw-1/site_snapshot.json
Only public pages are read. Nothing is written to the site.
"""
import html
import json
import os
import re
import sys
import urllib.request

BASE = "https://www.gehnaindia.com"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site_snapshot.json")

PAGES = {
    "home": "/",
    "shipping_and_returns": "/shipping-and-returns",
    "faqs": "/faqs",
}
COLLECTIONS = ["rings", "gemstone-gold-chains", "bracelets", "earrings", "best-seller-gold-jewellery", "gold-earrings-under-20k", "gold-jewellry-under-25k", "pendants"]
PRODUCTS = [
    "celestial-navaratna-18k-gold-bracelet",
    "verdant-whisper-emerald-18k-gold-ring",
    "ivory-natural-pearl-18k-gold-hook-earrings",
    "celestial-navaratna-18k-gold-chain",
]


def fetch(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0 (audit script)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "ignore")


def visible_text(s):
    s = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    s = re.sub(r"<style.*?</style>", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "\n", s)
    s = html.unescape(s)
    out, prev = [], None
    for line in s.split("\n"):
        line = line.strip()
        if line and line != prev:
            out.append(line)
        prev = line
    return out


def next_data(s):
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', s, re.S)
    return json.loads(m.group(1)) if m else None


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", " ", s or "")).strip()


snap = {"fetched_from": BASE, "pages": {}, "collections": {}, "products": {}}

for key, path in PAGES.items():
    try:
        s = fetch(path)
    except Exception as e:  # noqa: BLE001
        snap["pages"][key] = {"url": BASE + path, "error": str(e)}
        continue
    lines = visible_text(s)
    title = re.findall(r"<title>(.*?)</title>", s, re.S)
    snap["pages"][key] = {"url": BASE + path, "title": html.unescape(title[0]) if title else None, "text": lines}

for c in COLLECTIONS:
    path = "/m/" + c
    try:
        d = next_data(fetch(path))
    except Exception as e:  # noqa: BLE001
        snap["collections"][c] = {"url": BASE + path, "error": str(e)}
        continue
    st = d["props"]["pageProps"]["initialApolloState"]
    root = st.get("ROOT_QUERY", {})
    meta, total = None, None
    for k, v in root.items():
        if isinstance(v, dict) and v.get("__typename") == "ProductSearchResult":
            meta, total = v.get("pageMetadata"), v.get("total")
    price = st.get("ProductSearchFilterGroup:price", {})
    metals = {}
    for k, v in st.items():
        if k.startswith("ProductSearchFilterItem:") and ("K " in v["name"] or "Gold" in v["name"]):
            metals[v["name"]] = v["count"]
    items = []
    for k, v in st.items():
        if k.startswith("ProductSearchItem:"):
            items.append({
                "name": v.get("websiteName") or v.get("name"),
                "slug": v.get("slug"),
                "url": BASE + "/" + v.get("slug", ""),
                "selling_price_inr": v.get("sellingPrice"),
                "special_price_inr": v.get("specialPrice"),
                "discount_pct": v.get("specialPricePercentage"),
                "tag": v.get("productTag"),
                "fast_ship": v.get("isShipFastTagApplicable"),
            })
    snap["collections"][c] = {
        "url": BASE + path,
        "meta_title": (meta or {}).get("meta_title"),
        "meta_description": (meta or {}).get("meta_description"),
        "total_products": total,
        "price_min_inr": price.get("min"),
        "price_max_inr": price.get("max"),
        "metal_counts": metals,
        "first_page_items": items,
    }

for p in PRODUCTS:
    path = "/" + p
    try:
        s = fetch(path)
        d = next_data(s)
    except Exception as e:  # noqa: BLE001
        snap["products"][p] = {"url": BASE + path, "error": str(e)}
        continue
    pp = d["props"]["pageProps"]
    st = pp["initialApolloState"]
    props = {k: v.get("name") for k, v in st.items() if k.startswith("PropertyType:")}

    def names(refs):
        return [props.get(r["__ref"]) for r in (refs or []) if isinstance(r, dict)]

    prod = next(v for k, v in st.items() if k.startswith("ProductType:"))
    var = next(v for k, v in st.items() if k.startswith("VariationType:"))
    snap["products"][p] = {
        "url": BASE + path,
        "name": prod.get("website_name") or prod.get("name"),
        "product_code": prod.get("product_code"),
        "description": prod.get("description"),
        "collection_type": names(prod.get("collection_type")),
        "gemstone": names(prod.get("gemstone")),
        "metal_karatage": names(prod.get("metal_karatage")),
        "setting": names(prod.get("gemstone_setting_type")),
        "order_type": props.get((prod.get("order_type") or {}).get("__ref")),
        "karat_options": [m.get("metal_karatage") for m in (prod.get("metal_karatages") or [])],
        "selling_price_inr": var.get("selling_price"),
        "special_price_inr": var.get("special_price"),
        "gross_weight_g": var.get("gross_weight"),
        "gold_weight_g": var.get("gold_weight"),
        "gem_stone_weight_ct": var.get("gem_stone_weight"),
        "emi_table": var.get("emi_table"),
        "expected_delivery_range": prod.get("expected_delivery_date_range"),
        "in_store_stock": prod.get("is_stock_available_at_gehna_store"),
        "badge": strip_tags((prod.get("social_badge") or {}).get("value")),
        "faq": [{"q": q.get("question"), "a": strip_tags(q.get("answer"))} for q in (prod.get("frequent_questions") or [])],
        "json_ld_offer": (pp.get("jsonLdStructuredProductData") or {}).get("offers"),
    }

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(snap, f, ensure_ascii=False, indent=1)
print("wrote", OUT)
for c, v in snap["collections"].items():
    print(c, v.get("total_products"), v.get("price_min_inr"), v.get("price_max_inr"))
for p, v in snap["products"].items():
    print(p, v.get("selling_price_inr"), v.get("order_type"), v.get("expected_delivery_range"))
