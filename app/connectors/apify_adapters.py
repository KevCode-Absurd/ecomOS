"""Apify items to brain records, one function per lane. Spec: app/contracts/connectors/apify.md.

Every record is in app/brain/schema.json shape, tier evidence, visibility public, with
source.ref apify:<actor>:<runId>:<itemUrl>. Fields are copied from a whitelist, so reviewer
names and Reddit usernames never reach a record; "u/<name>" mentions inside text are masked.
Quotes stay verbatim apart from that mask and an em dash swapped for a comma (the validator
rejects em dashes), trimmed to 300 characters. Theme and hook rules are plain term tables:
a first cut to sort the pile, not a judgement.
"""
from __future__ import annotations

import datetime as dt
import re
import statistics
from collections import Counter, defaultdict

QUOTE_MAX = 300
AD_QUOTE_MAX = 120
REDDIT_NOTE = "reddit language, not for testimonial use"
AMAZON_REVIEWS = "axesso_data~amazon-reviews-scraper"
AMAZON_LISTING = "junglee~amazon-crawler"
ADLIB = "curious_coder~facebook-ads-library-scraper"
REDDIT = "trudax~reddit-scraper-lite"

THEMES = {
    "durability": ["hole", "holes", "wore out", "wear out", "worn out", "thin", "pill", "fell apart", "coming apart", "last", "lasted"],
    "fit_sizing": ["size", "sizing", "tight", "loose", "slip", "slips", "slipped", "fall down", "falls down", "stay up", "small", "large"],
    "comfort": ["comfortable", "comfort", "soft", "cushion", "itchy", "scratchy", "hurt", "blister"],
    "price_value": ["price", "expensive", "pricey", "worth", "overpriced", "cheap", "sale"],
    "delivery": ["shipping", "arrived", "package", "delivery", "late"],
    "authenticity": ["fake", "counterfeit", "third party", "not real", "opened"],
    "mission": ["donate", "donated", "donation", "charity", "give back"],
}
NEGATIVE = ["hole", "wore out", "worn out", "slip", "tight", "too expensive", "overpriced", "fake", "hurt", "itchy",
            "not enough", "disappoint", "worse", "fell apart", "coming apart", "do not", "don't"]
POSITIVE = ["best", "great", "love", "comfortable", "worth", "stay up", "no holes", "only socks", "soft", "fine"]
SITUATIONS = {
    "shift_worker": ["nurse", "nurses", "shift", "on my feet"],
    "runner": ["run", "running", "runs", "mile"],
    "hiker": ["hike", "hiking", "hikers", "trail"],
    "traveller": ["travel", "onebag", "packing"],
    "gift_buyer": ["gift", "for my dad", "for my mom", "christmas"],
    "circulation": ["compression", "circulation", "swelling", "legs are done"],
}
COMPETITORS = ["Darn Tough", "Smartwool", "Stance", "Feetures", "Balega", "Comrad", "Injinji", "Uniqlo", "Kirkland", "Hanes", "Swiftwick"]
RECOMMEND_CUES = ["instead", "switch", "switched", "try ", "get ", "better", "go with", "recommend"]
FRAMES = {
    "buy_it_for_life": ["lifetime", "warranty", "for life", "years old", "last"],
    "worth_the_price": ["worth", "worth it"],
    "marketing_brand": ["marketing", "hype", "overpriced"],
    "mission_giving": ["donate", "donation", "charity", "one pair"],
}
HOOKS = [
    ("question", lambda s: s.rstrip().endswith("?")),
    ("number", lambda s: bool(re.match(r"^\d", s))),
    ("problem", lambda s: bool(re.match(r"^(tired of|sick of|stop|no more|why do)", s.lower()))),
    ("first_person", lambda s: bool(re.match(r"^(i |i'm |my |we )", s.lower()))),
    ("offer", lambda s: bool(re.search(r"\d+% off|free shipping|buy \d+ get|\bsale\b", s.lower()))),
]
SECTION_FIELD = {"language_bank": "phrase", "objections": "objection", "products": "review_themes",
                 "marketplaces": "listing", "competitors": "competitor", "offers": "promo", "learnings": "signal",
                 "content": "topic", "avatars": "avatar", "positioning": "frame", "seo_facts": "question"}
CREATOR_CUES = ["i wore", "honest review", "i tried", "my feet", "after 3 months", "unboxing", "pov"]


# ---- helpers ------------------------------------------------------------------
def slug(s: str, n: int = 40) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(s).lower()).strip("_")[:n] or "x"


def clean(text, limit: int = QUOTE_MAX) -> str:
    s = re.sub(r"\bu/[A-Za-z0-9_-]+", "u/[user]", str(text or ""))
    s = s.replace("\u2014", ", ").replace("\u2013", "-")
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= limit else s[: limit - 3].rstrip() + "..."


def ref(actor: str, run_id: str, url: str) -> str:
    return f"apify:{actor}:{run_id}:{url}"


def has(text: str, terms) -> bool:
    t = f" {text.lower()} "
    return any(term in t for term in terms)


def themes_of(text: str) -> list[str]:
    return [k for k, terms in THEMES.items() if has(text, terms)] or ["general"]


def record(brand, section, field_id, value, text, src_type, src_ref, captured_at, notes=None, evidence=None):
    rec = {"id": f"{brand}.{section}.{field_id}", "brand": brand, "section": section, "field": SECTION_FIELD[section],
           "value": value, "text": clean(text, 400),
           "source": {"type": src_type, "ref": src_ref, "captured_at": captured_at},
           "tier": "evidence", "visibility": "public"}
    if evidence:
        rec["evidence"] = evidence
    if notes:
        rec["notes"] = notes
    return rec


def _today(captured_at):
    return captured_at or dt.date.today().isoformat()


def parse_star(v):
    if isinstance(v, (int, float)):
        return int(round(v))
    m = re.search(r"(\d+(?:\.\d+)?)", str(v or ""))
    return int(round(float(m.group(1)))) if m else None


def parse_date(v):
    if not v:
        return None
    s = str(v)
    if re.match(r"^\d{4}-\d{2}-\d{2}", s):
        return s[:10]
    m = re.search(r"([A-Z][a-z]+ \d{1,2}, \d{4})", s)
    if m:
        try:
            return dt.datetime.strptime(m.group(1), "%B %d, %Y").date().isoformat()
        except ValueError:
            return None
    return None


def _epoch_date(v):
    if v in (None, ""):
        return None
    if isinstance(v, (int, float)):
        return dt.datetime.fromtimestamp(v, dt.timezone.utc).date()
    d = parse_date(v)
    return dt.date.fromisoformat(d) if d else None


# ---- Amazon -------------------------------------------------------------------
def amazon_reviews(items, brand, asin, listing=None, *, run_id="unknown", listing_run_id="unknown",
                   captured_at=None, actor=AMAZON_REVIEWS, listing_actor=AMAZON_LISTING):
    """Reviews (and an optional listing item) for one ASIN to language_bank, objections, products, marketplaces."""
    day = _today(captured_at)
    out, complaints, praise = [], defaultdict(list), defaultdict(list)
    for it in items:
        if it.get("asin") and it["asin"] != asin:
            continue
        body = clean(it.get("text"))
        if not body:
            continue
        star = parse_star(it.get("rating"))
        url = it.get("url") or f"https://www.amazon.com/dp/{asin}"
        rid = slug(it.get("reviewId") or url, 30)
        review = {"star": star, "verified": bool(it.get("verified")), "helpful": int(it.get("numberOfHelpful") or 0),
                  "date": parse_date(it.get("date")), "url": url, "source": "amazon", "quote": body}
        side = "complaint" if star is not None and star <= 2 else "praise" if star is not None and star >= 4 else "mixed"
        title = clean(it.get("title"), 120)
        out.append(record(brand, "language_bank", f"amazon_{slug(asin)}_{rid}",
                          {"theme": side, "phrase": title or body[:120], "asin": asin, "themes": themes_of(body),
                           "reviews": [review]},
                          f"Amazon {star}-star review of {asin}: {title or body[:80]}", "review",
                          ref(actor, run_id, url), day))
        for th in themes_of(f"{title} {body}"):
            (complaints if side == "complaint" else praise if side == "praise" else defaultdict(list))[th].append(review)
    for th, revs in sorted(complaints.items()):
        out.append(record(brand, "objections", f"amazon_{slug(asin)}_{th}",
                          {"objection": th, "asin": asin, "count": len(revs), "reviews": revs},
                          f"{len(revs)} one or two star Amazon reviews of {asin} raise {th.replace('_', ' ')}.",
                          "review", ref(actor, run_id, revs[0]["url"]), day))
    for kind, bucket in (("issues", complaints), ("praise", praise)):
        if bucket:
            first = next(iter(bucket.values()))[0]
            out.append(record(brand, "products", f"amazon_{slug(asin)}_{kind}",
                              {"asin": asin, "kind": kind, "themes": {k: len(v) for k, v in sorted(bucket.items())},
                               "quotes": [v[0]["quote"] for v in bucket.values()][:3]},
                              f"Amazon {kind} for {asin}: " + ", ".join(f"{k.replace('_', ' ')} {len(v)}" for k, v in sorted(bucket.items())) + ".",
                              "review", ref(actor, run_id, first["url"]), day))
    if listing:
        seller = ((listing.get("seller") or {}).get("name") if isinstance(listing.get("seller"), dict) else listing.get("seller")) or None
        price = listing.get("price")
        value = {"channel": "amazon", "asin": asin, "title": clean(listing.get("title"), 200),
                 "bullets": [clean(b, 200) for b in (listing.get("features") or [])],
                 "stars": listing.get("stars"), "review_count": listing.get("reviewsCount"),
                 "price": price.get("value") if isinstance(price, dict) else price,
                 "currency": price.get("currency") if isinstance(price, dict) else None,
                 "seller": seller,
                 "third_party_seller": None if not seller or not listing.get("brand") else seller.strip().lower() != str(listing["brand"]).strip().lower()}
        url = listing.get("url") or f"https://www.amazon.com/dp/{asin}"
        flag = " Sold by a third party seller." if value["third_party_seller"] else ""
        out.append(record(brand, "marketplaces", f"amazon_{slug(asin)}", value,
                          f"Amazon listing {asin}: {value['stars']} stars from {value['review_count']} reviews.{flag}",
                          "site", ref(listing_actor, listing_run_id, url), day))
    return out


# ---- Meta Ad Library ------------------------------------------------------------
def _hook(text: str) -> str:
    first = re.split(r"(?<=[.!?])\s", text.strip(), maxsplit=1)[0] if text else ""
    for name, test in HOOKS:
        if first and test(first):
            return name
    return "statement"


def _promos(text: str) -> list[str]:
    t, found = text or "", []
    for m in re.finditer(r"\bcode\s+([A-Z0-9]{4,})\b", t, re.I):
        found.append(f"code {m.group(1).upper()}")
    for m in re.finditer(r"(\d{1,2})% off", t, re.I):
        found.append(f"{m.group(1)}% off")
    if re.search(r"free shipping", t, re.I):
        found.append("free shipping" + (f" over ${m.group(1)}" if (m := re.search(r"free shipping on orders over \$(\d+)", t, re.I)) else ""))
    for m in re.finditer(r"buy (\d+) get (\d+)", t, re.I):
        found.append(f"buy {m.group(1)} get {m.group(2)}")
    return found


def meta_ad_library(items, brand, page_role, *, run_id="unknown", captured_at=None, actor=ADLIB):
    """Ad items to competitors, offers, learnings and content signals. page_role: a role for every page, or {page name: role}."""
    day = _today(captured_at)
    today = dt.date.fromisoformat(day)
    pages = defaultdict(list)
    for it in items:
        pages[it.get("page_name") or "unknown"].append(it)
    out = []
    for page, ads in sorted(pages.items()):
        role = page_role.get(page, "competitor") if isinstance(page_role, dict) else page_role
        ps = slug(page, 30)
        rows = []
        for ad in ads:
            snap = ad.get("snapshot") or {}
            body = clean((snap.get("body") or {}).get("text") if isinstance(snap.get("body"), dict) else snap.get("body"), 1000)
            start = _epoch_date(ad.get("start_date"))
            end = _epoch_date(ad.get("end_date")) or today
            url = ad.get("url") or f"https://www.facebook.com/ads/library/?id={ad.get('ad_archive_id')}"
            rows.append({"body": body, "start": start, "days": (end - start).days if start else None,
                         "active": bool(ad.get("is_active")), "format": (snap.get("display_format") or "unknown").lower(),
                         "platforms": [p.lower() for p in ad.get("publisher_platform") or []], "hook": _hook(body),
                         "promos": _promos(f"{body} {snap.get('title') or ''}"), "url": url,
                         "creator": has(body, CREATOR_CUES)})
        days = [r["days"] for r in rows if r["days"] is not None]
        longest = max(rows, key=lambda r: r["days"] or -1)
        formats = dict(Counter(r["format"] for r in rows))
        hooks = dict(Counter(r["hook"] for r in rows))
        platforms = sorted({p for r in rows for p in r["platforms"]})
        offers_seen = sorted({p for r in rows for p in r["promos"]})
        evidence = [{"quote": clean(r["body"], AD_QUOTE_MAX), "ref": r["url"], "captured_at": day} for r in rows[:3] if r["body"]]
        src = ref(actor, run_id, longest["url"])
        if role != "self":
            out.append(record(brand, "competitors", f"adlib_{ps}",
                              {"page": page, "page_id": ads[0].get("page_id"), "ads_seen": len(rows),
                               "active_ads": sum(r["active"] for r in rows), "longest_run_days": longest["days"],
                               "formats": formats, "hook_types": hooks, "offers_seen": offers_seen, "platforms": platforms},
                              f"{page} runs {sum(r['active'] for r in rows)} active Meta ads; longest has run {longest['days']} days.",
                              "ad_library", src, day, evidence=evidence))
        else:
            by_promo = defaultdict(list)
            for r in rows:
                for p in r["promos"]:
                    by_promo[p].append(r)
            for promo, rs in sorted(by_promo.items()):
                starts = sorted(r["start"].isoformat() for r in rs if r["start"])
                out.append(record(brand, "offers", f"adlib_promo_{slug(promo, 30)}",
                                  {"promo": promo, "ads": len(rs), "first_seen": starts[0] if starts else None,
                                   "active_now": any(r["active"] for r in rs)},
                                  f"Own Meta ads show the promo '{promo}' in {len(rs)} ads.",
                                  "ad_library", ref(actor, run_id, rs[0]["url"]), day,
                                  evidence=[{"quote": clean(rs[0]["body"], AD_QUOTE_MAX), "ref": rs[0]["url"], "captured_at": day}]))
        out.append(record(brand, "learnings", f"adlib_{ps}_formats",
                          {"page": page, "role": role, "formats": formats, "hook_types": hooks,
                           "median_run_days": statistics.median(days) if days else None,
                           "long_runners_30d": sum(d >= 30 for d in days), "signal_only": True},
                          f"Signal, not proof: {page} ads by format {formats}; {sum(d >= 30 for d in days)} have run 30 days or more.",
                          "ad_library", src, day))
        creator = [r for r in rows if r["creator"]]
        if creator:
            out.append(record(brand, "content", f"adlib_{ps}_creator_style",
                              {"page": page, "role": role, "creator_style_ads": len(creator),
                               "formats": dict(Counter(r["format"] for r in creator))},
                              f"{page} runs {len(creator)} creator-style ads (first person, review voice).",
                              "ad_library", ref(actor, run_id, creator[0]["url"]), day))
    return out


# ---- Reddit -------------------------------------------------------------------
def _sentiment(text: str) -> str:
    neg, pos = has(text, NEGATIVE), has(text, POSITIVE)
    return "complaint" if neg and not pos else "praise" if pos and not neg else "mixed"


def reddit(items, brand, *, run_id="unknown", captured_at=None, actor=REDDIT, notes=REDDIT_NOTE):
    """Posts and comments to language_bank, objections, avatars, competitors, positioning, seo_facts, content."""
    day = _today(captured_at)
    brand_word = brand.lower()
    out, rows = [], []
    for it in items:
        kind = it.get("dataType") or ("comment" if it.get("postId") else "post")
        title = clean(it.get("title"), 200) if kind == "post" else ""
        body = clean(it.get("body"))
        text = clean(f"{title} {body}".strip())
        if len(text) < 15:
            continue
        sub = it.get("parsedCommunityName") or str(it.get("communityName") or "").removeprefix("r/") or "unknown"
        rows.append({"kind": kind, "title": title, "text": text, "sub": sub, "up": int(it.get("upVotes") or 0),
                     "url": it.get("url") or "", "date": parse_date(it.get("createdAt")), "id": slug(it.get("parsedId") or it.get("id") or it.get("url"), 20),
                     "sentiment": _sentiment(text), "themes": themes_of(text)})

    def src(r):
        return ref(actor, run_id, r["url"])

    def quote(r):
        return {"star": None, "upvotes": r["up"], "subreddit": r["sub"], "date": r["date"], "url": r["url"],
                "source": "reddit", "quote": r["text"]}

    for r in rows:
        out.append(record(brand, "language_bank", f"reddit_{r['id']}",
                          {"theme": r["sentiment"], "phrase": r["text"][:160], "subreddit": r["sub"], "weight": r["up"],
                           "kind": r["kind"], "themes": r["themes"], "reviews": [quote(r)]},
                          f"r/{r['sub']} {r['kind']} ({r['up']} upvotes): {r['text'][:100]}",
                          "review", src(r), day, notes=notes))
    by_theme = defaultdict(list)
    for r in rows:
        if r["sentiment"] == "complaint" or (r["sentiment"] == "mixed" and has(r["text"], NEGATIVE)):
            for th in r["themes"]:
                by_theme[th].append(r)
    for th, rs in sorted(by_theme.items()):
        rs = sorted(rs, key=lambda r: -r["up"])
        out.append(record(brand, "objections", f"reddit_{th}",
                          {"objection": th, "mentions": len(rs), "upvotes": sum(r["up"] for r in rs), "reviews": [quote(r) for r in rs[:5]]},
                          f"Reddit threads raise {th.replace('_', ' ')} in {len(rs)} posts or comments.",
                          "review", src(rs[0]), day, notes=notes))
    by_sit = defaultdict(list)
    for r in rows:
        for sit, terms in SITUATIONS.items():
            if has(r["text"], terms):
                by_sit[sit].append(r)
    for sit, rs in sorted(by_sit.items()):
        if len(rs) < 2:
            continue
        out.append(record(brand, "avatars", f"reddit_{sit}",
                          {"situation": sit, "mentions": len(rs), "subreddits": sorted({r["sub"] for r in rs}),
                           "themes": dict(Counter(t for r in rs for t in r["themes"]))},
                          f"A repeat buying situation on Reddit: {sit.replace('_', ' ')} ({len(rs)} mentions).",
                          "review", src(rs[0]), day, notes=notes))
    rec_counts = defaultdict(list)
    for r in rows:
        low = r["text"].lower()
        for comp in COMPETITORS:
            if comp.lower() in low and has(low, RECOMMEND_CUES):
                rec_counts[comp].append(r)
    for comp, rs in sorted(rec_counts.items()):
        out.append(record(brand, "competitors", f"reddit_recommended_{slug(comp)}",
                          {"competitor": comp, "recommended_instead": len(rs), "upvotes": sum(r["up"] for r in rs),
                           "subreddits": sorted({r["sub"] for r in rs})},
                          f"Reddit recommends {comp} instead in {len(rs)} posts or comments.",
                          "review", src(rs[0]), day, notes=notes))
    for frame, terms in FRAMES.items():
        rs = [r for r in rows if has(r["text"], terms)]
        if rs:
            out.append(record(brand, "positioning", f"reddit_frame_{frame}",
                              {"frame": frame, "mentions": len(rs), "mentions_brand": sum(brand_word in r["text"].lower() for r in rs)},
                              f"Reddit frame '{frame.replace('_', ' ')}' appears in {len(rs)} posts or comments.",
                              "review", src(rs[0]), day, notes=notes))
    for r in rows:
        if r["kind"] == "post" and r["title"].endswith("?"):
            out.append(record(brand, "seo_facts", f"reddit_question_{r['id']}",
                              {"question": r["title"], "subreddit": r["sub"], "upvotes": r["up"]},
                              f"Question asked on r/{r['sub']}: {r['title']}", "review", src(r), day, notes=notes))
    topics = Counter((r["sub"], t) for r in rows for t in r["themes"])
    if topics:
        top = rows[0]
        out.append(record(brand, "content", "reddit_topics",
                          {"topics": [{"subreddit": s, "theme": t, "count": n} for (s, t), n in topics.most_common(20)]},
                          f"Reddit topics across {len({r['sub'] for r in rows})} subreddits, led by "
                          f"{topics.most_common(1)[0][0][1].replace('_', ' ')}.", "review", src(top), day, notes=notes))
    return out
