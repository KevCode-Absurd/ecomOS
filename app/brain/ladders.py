"""Build objection ladders from a brand's review records, then re-merge and republish.

Usage: python3 app/brain/ladders.py bombas [--today 2026-09-28] [--no-merge] [--no-publish]

Contract: app/contracts/brand-brain.md section 6.2. Reads every review-derived
record in `app/brain/<brand>/raw/<lane>/` (source type review or ticket, or any
record carrying `value.reviews`) and the merged `avatars`, `policies`, `offers`
and `claims` sections. Writes one `objection_ladders` record per theme:

- quotes come from `value.reviews` (star, source, url) or, when a record has no
  reviews, from its `evidence`; one quote cited by several records is counted once;
- side: stars 1-2 are complaints, 4-5 praise; a 3-star or unstarred quote is
  split by the sentiment of its text and an unstarred one is marked `star_unknown`;
- theme and rung come from the term table `THEMES` (generic ecommerce doubts,
  mild doubt at level 1 to deal-breaker at the top); a quote with no term hit
  falls back to its record's own text (objection, phrase, pains, issues);
- counts are by side, by star and by source (own_site, amazon, trustpilot,
  retailer, reddit, plus other when seen); lanes with no records (a blocked
  extractor that left only `sources.json`) are listed in `counts.empty_lanes`;
- proof is the first policies, offers or claims record whose text matches the
  rung's proof terms; a rung with complaints and no proof gets an open question;
- avatars are the avatar records whose quotes landed on the rung or whose
  pains match it; uses are drawn from offer, copy, pdp, amazon_listing, cx_macro.

Every ladder is tier inferred, source type agent, and cites `derived_from`
record ids. `run` re-merges raw/ first (merge.py), then writes the ladders,
adds the ladder open questions to `open_questions.json`, regenerates
`freshness.json` and republishes BRAIN.md through router.py. Rerun this, not
merge.py alone, whenever a review lane changes. No third-party packages, no
network calls.
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

SOURCES = ("own_site", "amazon", "trustpilot", "retailer", "reddit")
USES = ("offer", "copy", "pdp", "amazon_listing", "cx_macro")
PROOF_SECTIONS = ("policies", "offers", "claims")
REVIEW_TYPES = {"review", "ticket"}
RETAILERS = ("nordstrom", "target", "walmart", "dsw", "zappos", "rei.com", "dickssportinggoods", "macys",
             "kohls", "costco", "bestbuy", "ulta", "sephora", "nordstromrack", "scheels")
PRAISE_THEMES = {"result", "surprise", "gift", "praise"}
QUOTE_CHARS = 160
MAX_QUOTES = 3
MAX_AVATARS = 3

# Mild doubt first, deal-breaker last. Terms are regex fragments matched from a word start.
THEMES = [
    {"theme": "durability", "praise": [r"durable", r"last(s|ed|ing)?\b", r"hole[- ]free", r"held up", r"holding up",
                                        r"still (look|in|going)"],
     "rungs": [
         {"level": 1, "doubt": "will they pill, shed or go fuzzy",
          "terms": [r"pill", r"fuzz", r"shed", r"lint"],
          "proof": [r"happiness guarantee", r"replacement"]},
         {"level": 2, "doubt": "is the quality lower than the pairs I bought before",
          "terms": [r"used to be", r"thinner", r"deteriorat", r"quality (has|is|went|gone|declin|really)", r"not what it",
                    r"older pairs", r"years ago", r"lower quality", r"taken a dive", r"taken a dice"],
          "proof": [r"happiness guarantee", r"replacement"]},
         {"level": 3, "doubt": "will a hole or seam give out within weeks",
          "terms": [r"holes?\b", r"coming apart", r"came apart", r"fall(ing|s)? apart", r"unravel", r"threads? (com|loose|pull)",
                    r"loose threads?", r"string", r"rip", r"tear", r"wore through", r"wear(s)? through", r"snag", r"worn out"],
          "proof": [r"reinforced", r"wear test", r"lab test", r"durability test", r"abrasion"]},
     ]},
    {"theme": "fit_and_sizing", "praise": [r"stay(s|ed)? (in place|up|put|on)", r"fits? (perfect|great|well|true)",
                                          r"not (too )?tight", r"true to size", r"(don't|doesn't|didn't) slide", r"actually stay"],
     "rungs": [
         {"level": 1, "doubt": "will the size fit my foot, leg or body",
          "terms": [r"siz(e|es|ing)", r"runs? (small|large|big|short|long)", r"too (small|big|tight|long|short|loose)",
                    r"tight", r"short\b", r"length"],
          "proof": [r"exchange"]},
         {"level": 2, "doubt": "will it slip, slide or roll down",
          "terms": [r"slip", r"slid", r"slide", r"ride(s)? down", r"roll(s|ed|ing)? down", r"fall(s)? down", r"bunch"],
          "proof": [r"stay-up", r"stay up", r"stays? put", r"(no|won't|doesn't) slip"]},
         {"level": 3, "doubt": "can I wear it at all",
          "terms": [r"(could|can)( ?not|'t| never) get", r"hard to (pull|put|get)", r"huge", r"men's shirt", r"unwearable",
                    r"doesn't fit at all", r"had to return"],
          "proof": [r"size chart", r"fit guide", r"measure"]},
     ]},
    {"theme": "comfort_and_feel", "praise": [r"comfort", r"soft", r"cozy", r"warm", r"cushion", r"arch support",
                                            r"no seam", r"seam toe", r"dry", r"breathab", r"jumped for joy", r"feel better"],
     "rungs": [
         {"level": 1, "doubt": "will it feel as soft, thick or warm as it looks",
          "terms": [r"thin\b", r"not warm", r"cold", r"sole", r"thick", r"heavy", r"scratch", r"itch", r"drape"],
          "proof": [r"cushion", r"extra-long staple", r"merino"]},
         {"level": 2, "doubt": "will a seam or band rub or irritate",
          "terms": [r"seams?\b", r"rub", r"irritat", r"blister", r"marks?\b", r"dig"],
          "proof": [r"invisitoe", r"blister tab", r"seamless"]},
         {"level": 3, "doubt": "will it do the job it claims, like support or compression",
          "terms": [r"compression", r"support", r"feels? nothing", r"no effect", r"does nothing", r"pouch"],
          "proof": [r"graduated compression", r"mmhg", r"clinical"]},
     ]},
    {"theme": "price_and_value", "praise": [r"worth (it|the|every)", r"value", r"pricey but", r"expensive but"],
     "rungs": [
         {"level": 1, "doubt": "is it worth more than ordinary socks",
          "terms": [r"price", r"pricey", r"expensive", r"\$\d", r"\d+ dollars", r"cost", r"cheaper", r"walmart", r"per pair",
                    r"a pair\b"],
          "proof": [r"per pack price", r"discount", r"free standard shipping"]},
         {"level": 2, "doubt": "did I overpay for something that failed",
          "terms": [r"not worth", r"overpriced", r"waste of money", r"rip ?off", r"justify", r"no better than"],
          "proof": [r"happiness guarantee", r"make a purchase right"]},
     ]},
    {"theme": "order_and_delivery", "praise": [r"arrived (quick|fast|on time|early)", r"fast shipping", r"replaced",
                                              r"(customer )?service (was|is) (great|amazing|stellar|exceptional|excellent)",
                                              r"stellar", r"exceptional"],
     "rungs": [
         {"level": 1, "doubt": "will it arrive in time",
          "terms": [r"late\b", r"arriv", r"deliver", r"shipping", r"christmas", r"holiday", r"in time"],
          "proof": [r"priority shipping", r"business days"]},
         {"level": 2, "doubt": "will the order come short or wrong",
          "terms": [r"missing", r"only received", r"half of my order", r"wrong (size|color|colour|item)", r"incomplete",
                    r"short (shipped|shipment)"],
          "proof": [r"replacement", r"exchange"]},
         {"level": 3, "doubt": "will anyone help me fix it",
          "terms": [r"no (reply|response|answer)", r"never heard", r"(does|did)( not|n't) (reply|respond|answer)",
                    r"customer (service|experience|support)", r"support team", r"chat\b", r"emailed"],
          "proof": [r"response time", r"reply within", r"within \d+ hours"]},
     ]},
    {"theme": "mission_trust", "praise": [r"one goes", r"homeless", r"donat", r"giving back", r"good cause"],
     "rungs": [
         {"level": 1, "doubt": "is the giving model real or only marketing",
          "terms": [r"donat", r"giving", r"homeless", r"one for one", r"mission", r"charit", r"marketing"],
          "proof": [r"donates one item", r"for every item"]},
     ]},
    {"theme": "marketplace_trust", "praise": [r"genuine", r"authentic", r"same as (the )?(site|website|store)"],
     "rungs": [
         {"level": 1, "doubt": "is the marketplace listing the real product and pack",
          "terms": [r"reseller", r"seller", r"fewer pairs", r"fake", r"counterfeit", r"listing", r"pairs? than (shown|pictured)",
                    r"only (got|came with) \d"],
          "proof": [r"sold by", r"brand store", r"authorized"]},
     ]},
]

NEGATIVE = [r"not worth", r"no better", r"not (comfortable|warm|soft|good|great)", r"disappoint", r"worst", r"terrible",
            r"awful", r"waste", r"overpriced", r"holes?\b", r"apart", r"pill", r"slip", r"slid", r"refund", r"return",
            r"missing", r"late\b", r"never", r"thin", r"cheap", r"poor", r"broke", r"unravel", r"tight", r"itch",
            r"fell", r"won't", r"doesn't", r"didn't", r"deteriorat", r"used to be", r"fewer", r"grossly", r"shed", r"worn out"]
POSITIVE = [r"love", r"best", r"comfort", r"great", r"perfect", r"worth (it|the|every)", r"soft", r"warm", r"stay",
            r"happy", r"amazing", r"excellent", r"favorite", r"recommend", r"durable", r"cozy", r"stellar", r"exceptional",
            r"replaced", r"joy", r"finally", r"well made", r"quality"]


def _hits(text: str, terms) -> int:
    return sum(1 for t in terms if re.search(r"(?<![a-z])" + t, text))


def sentiment(text: str) -> int:
    """+1 praise, -1 complaint, 0 unclear. Negative phrases are counted before positive ones."""
    t = text.lower()
    neg = _hits(t, NEGATIVE)
    t2 = re.sub(r"not worth|no better|not (comfortable|warm|soft|good|great)", " ", t)
    pos = _hits(t2, POSITIVE)
    return (pos > neg) - (neg > pos)


def source_bucket(src: str | None, url: str | None, brand: str) -> str:
    s, u = (src or "").lower(), (url or "").lower()
    host = re.sub(r"^https?://", "", u).split("/")[0]
    if "own_site" in s or (brand and brand in host):
        return "own_site"
    if "amazon" in s or "amazon." in host:
        return "amazon"
    if "trustpilot" in s or "trustpilot" in host:
        return "trustpilot"
    if "reddit" in s or "reddit" in host:
        return "reddit"
    if "retailer" in s or any(r in host for r in RETAILERS):
        return "retailer"
    return "other"


def _clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text.replace("—", ", ").replace("–", "-")).strip()
    if len(text) <= QUOTE_CHARS:
        return text
    return text[:QUOTE_CHARS].rsplit(" ", 1)[0].rstrip(",.;") + "..."


def _key(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())[:60]


def _context(rec: dict) -> str:
    v = rec.get("value")
    parts = [rec.get("text") or ""]
    if isinstance(v, dict):
        for k in ("objection", "phrase", "name", "job"):
            if isinstance(v.get(k), str):
                parts.append(v[k])
        for k in ("pains", "triggers", "issues"):
            if isinstance(v.get(k), list):
                parts += [x for x in v[k] if isinstance(x, str)]
    return " ".join(parts).lower()


def _hint(rec: dict) -> int:
    v = rec.get("value") if isinstance(rec.get("value"), dict) else {}
    if rec.get("section") == "language_bank":
        return 1 if v.get("theme") in PRAISE_THEMES else -1
    if rec.get("section") == "objections":
        return -1
    return 0


def is_review_record(rec: dict) -> bool:
    v = rec.get("value")
    return ((rec.get("source") or {}).get("type") in REVIEW_TYPES
            or (isinstance(v, dict) and isinstance(v.get("reviews"), list)))


def load_lanes(brand_dir: Path) -> tuple[dict[str, list[dict]], list[dict]]:
    """Review records by lane, and the lanes that hold no records at all."""
    lanes, empty = {}, []
    raw = brand_dir / "raw"
    if not raw.is_dir():
        return lanes, empty
    for folder in sorted(p for p in raw.iterdir() if p.is_dir()):
        recs = []
        for path in sorted(folder.glob("*.json")):
            if path.stem != "sources":
                recs.extend(r for r in json.loads(path.read_text(encoding="utf-8")) if isinstance(r, dict))
        if not recs:
            note = ""
            src = folder / "sources.json"
            if src.exists():
                data = json.loads(src.read_text(encoding="utf-8")) or []
                note = next((d.get("note", "") for d in data if isinstance(d, dict) and d.get("note")), "")
            empty.append({"lane": folder.name, "note": _clean(note) if note else "no records"})
            continue
        review = [r for r in recs if is_review_record(r)]
        if review:
            lanes[folder.name] = review
    return lanes, empty


def extract_quotes(brand: str, lanes: dict[str, list[dict]]) -> list[dict]:
    """One entry per distinct quote, with every record id that cites it."""
    quotes = {}
    for lane, recs in lanes.items():
        for rec in recs:
            v = rec.get("value") if isinstance(rec.get("value"), dict) else {}
            items = v.get("reviews") or []
            if items:
                rows = [(i.get("quote"), i.get("star"), i.get("source"), i.get("url")) for i in items if isinstance(i, dict)]
            else:
                rows = [(e.get("quote"), None, None, e.get("ref")) for e in rec.get("evidence") or [] if isinstance(e, dict)]
            for text, star, src, url in rows:
                if not text:
                    continue
                k = _key(text)
                if len(k) >= 30:
                    k = next((e for e in quotes if len(e) >= 30 and (e.startswith(k) or k.startswith(e))), k)
                q = quotes.get(k)
                if q is None:
                    q = quotes[k] = {"quote": text, "star": star if isinstance(star, int) else None,
                                     "source": source_bucket(src, url, brand), "lane": lane,
                                     "records": [], "contexts": [], "hints": []}
                elif q["star"] is None and isinstance(star, int):
                    q["star"] = star
                if rec["id"] not in q["records"]:
                    q["records"].append(rec["id"])
                    q["contexts"].append(_context(rec))
                    q["hints"].append(_hint(rec))
    out = []
    for q in quotes.values():
        star = q["star"]
        if star is not None and star <= 2:
            side = -1
        elif star is not None and star >= 4:
            side = 1
        else:
            side = sentiment(q["quote"]) or (1 if sum(q["hints"]) > 0 else -1)
        q["side"] = "praise" if side > 0 else "complaint"
        q["star_unknown"] = star is None
        out.append(q)
    return out


def classify(text: str, context: str, themes=THEMES) -> tuple[str | None, int]:
    """(theme, rung level) for one quote; the record context is the fallback."""
    for probe in (text.lower(), context):
        best, score = None, 0
        for th in themes:
            s = sum(_hits(probe, r["terms"]) for r in th["rungs"]) + _hits(probe, th.get("praise", []))
            if s > score:
                best, score = th, s
        if best:
            for probe2 in (text.lower(), context):
                levels = [r["level"] for r in best["rungs"] if _hits(probe2, r["terms"])]
                if levels:
                    return best["theme"], max(levels)
            return best["theme"], best["rungs"][0]["level"]
    return None, 0


def find_proof(terms, sections: dict[str, list[dict]]) -> dict | None:
    """The first active policies, offers or claims record matching the earliest proof term."""
    for term in terms:
        for sec in PROOF_SECTIONS:
            for rec in sections.get(sec, []):
                if rec.get("status", "active") != "active":
                    continue
                if _hits((rec.get("text") or json.dumps(rec.get("value"))).lower(), [term]):
                    return rec
    return None


def _pick(quotes: list[dict], want: int, terms) -> list[str]:
    """Quotes that name the rung themselves first, then the wanted star, then shorter."""
    ranked = sorted(quotes, key=lambda q: (not _hits(q["quote"].lower(), terms), q["star"] != want,
                                           q["star_unknown"], len(q["quote"])))
    return [_clean(q["quote"]) for q in ranked[:MAX_QUOTES]]


def _counts(quotes: list[dict]) -> dict:
    by_star = {str(s): 0 for s in range(1, 6)}
    by_star["star_unknown"] = 0
    srcs = {s: 0 for s in SOURCES}
    for q in quotes:
        by_star["star_unknown" if q["star"] is None else str(q["star"])] += 1
        srcs[q["source"]] = srcs.get(q["source"], 0) + 1
    return {"one_star": sum(q["side"] == "complaint" for q in quotes),
            "five_star": sum(q["side"] == "praise" for q in quotes), "by_star": by_star, "sources": srcs}


def _avatars(rung: dict, quotes: list[dict], avatars: list[dict]) -> list[str]:
    score = {}
    for a in avatars:
        s = _hits(_context(a), rung["terms"])
        s += 2 * sum(a["id"] in q["records"] for q in quotes)
        if s:
            score[a["id"]] = s
    return [k for k, _ in sorted(score.items(), key=lambda kv: -kv[1])][:MAX_AVATARS]


def _labels(records: list[dict], theme: dict, praise: bool) -> list[str]:
    out = []
    for rec in records:
        v = rec.get("value") if isinstance(rec.get("value"), dict) else {}
        labels = []
        if rec.get("section") == "language_bank" and isinstance(v.get("phrase"), str):
            if (v.get("theme") in PRAISE_THEMES) == praise:
                labels.append(v["phrase"])
        labels += [x for x in v.get("praise" if praise else "issues", []) or [] if isinstance(x, str)]
        for lab in labels:
            terms = [t for r in theme["rungs"] for t in r["terms"]] + theme.get("praise", [])
            if _hits(lab.lower(), terms) and lab not in out:
                out.append(lab)
    return out[:6]


def build(brand: str, lanes: dict[str, list[dict]], empty_lanes: list[dict], sections: dict[str, list[dict]],
          today: str, themes=THEMES) -> tuple[list[dict], list[dict]]:
    """(ladder records, open question records) for one brand."""
    quotes = extract_quotes(brand, lanes)
    for q in quotes:
        q["theme"], q["level"] = classify(q["quote"], " ".join(q["contexts"]), themes)
    avatars = sections.get("avatars", [])
    review_recs = [r for recs in lanes.values() for r in recs]
    ladders, questions = [], []
    for th in themes:
        tq = [q for q in quotes if q["theme"] == th["theme"]]
        if not tq:
            continue
        rungs, derived = [], []
        for spec in th["rungs"]:
            rq = [q for q in tq if q["level"] == spec["level"]]
            if not rq:
                continue
            complaints = [q for q in rq if q["side"] == "complaint"]
            praise = [q for q in rq if q["side"] == "praise"]
            ids = sorted({i for q in rq for i in q["records"]})
            proof = find_proof(spec["proof"], sections)
            counts = _counts(rq)
            rung = {"level": spec["level"], "doubt": spec["doubt"], "one_star": _pick(complaints, 1, spec["terms"]),
                    "five_star": _pick(praise, 5, spec["terms"] + th.get("praise", [])), "counts": counts}
            uses = set()
            if praise:
                uses.add("copy")
            if proof:
                rung["proof"] = proof.get("text") or str(proof.get("value"))
                rung["proof_ids"] = [proof["id"]]
                ids_p = [proof["id"]]
                if complaints:
                    uses |= {"pdp", "cx_macro"}
            else:
                ids_p = []
                rung["proof"] = "no public proof; open question for the founder"
                if complaints:
                    uses |= {"offer", "cx_macro"}
                    qid = f"{brand}.open_questions.ladder_{th['theme']}_{spec['level']}"
                    ask = f"What proof answers \"{spec['doubt']}\"? {len(complaints)} complaint quotes raise it and no policy, offer or claim covers it."
                    questions.append({
                        "id": qid, "brand": brand, "section": "open_questions", "field": qid.split(".", 2)[2],
                        "value": {"question": ask, "section": "objection_ladders",
                                  "why": "A doubt with no proof is an offer, guarantee or product problem; copy alone cannot answer it.",
                                  "who_can_answer": "the founder", "asked_on": None, "answered_on": None},
                        "text": ask, "visibility": "private"})
                    rung["open_question"] = qid
            if counts["sources"].get("amazon") or th["theme"] == "marketplace_trust":
                uses.add("amazon_listing")
            rung["avatars"] = _avatars(spec, rq, avatars)
            rung["uses"] = [u for u in USES if u in uses]
            rung["derived_from"] = ids
            rungs.append(rung)
            derived += ids + ids_p + rung["avatars"]
        total = _counts(tq)
        lane_n = {}
        for q in tq:
            lane_n[q["lane"]] = lane_n.get(q["lane"], 0) + 1
        total["lanes"] = lane_n
        total["empty_lanes"] = empty_lanes
        top = rungs[-1]
        uses = [u for u in USES if any(u in r["uses"] for r in rungs)]
        answered = "has proof" if top.get("proof_ids") else "has no public proof yet"
        label = th["theme"].replace("_", " ")
        text = (f"{label.capitalize()}: {total['one_star']} complaint and {total['five_star']} praise quotes. "
                f"Top rung \"{top['doubt']}\": {top['counts']['one_star']} complaint quotes, {answered}.")
        ladders.append({
            "id": f"{brand}.objection_ladders.{th['theme']}", "brand": brand, "section": "objection_ladders",
            "field": "ladder",
            "value": {"theme": th["theme"], "rungs": rungs, "counts": total, "uses": uses,
                      "what_works": _labels(review_recs, th, True), "what_fails": _labels(review_recs, th, False)},
            "text": text,
            "source": {"type": "agent", "ref": "app/brain/ladders.py", "captured_at": today,
                       "derived_from": list(dict.fromkeys(derived))},
            "tier": "inferred", "confidence": round(min(0.8, 0.4 + 0.01 * len(tq)), 2), "visibility": "public"})
    ladders.sort(key=lambda r: -r["value"]["counts"]["one_star"])
    return ladders, questions


def _read(path: Path) -> list:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def load_sections(brand_dir: Path) -> dict[str, list[dict]]:
    skip = {"sources", "assumptions", "freshness", "open_questions", "objection_ladders"}
    return {p.stem: _read(p) for p in sorted(brand_dir.glob("*.json")) if p.stem not in skip}


def run(brand: str, root: Path | None = None, today: str | None = None, remerge: bool = True,
        publish: bool = True) -> dict:
    import merge
    root = root or HERE
    today = today or dt.date.today().isoformat()
    brand_dir = root / brand
    if remerge:
        merge.run(brand, root, today, publish=False)
    sections = load_sections(brand_dir)
    lanes, empty = load_lanes(brand_dir)
    ladders, questions = build(brand, lanes, empty, sections, today)
    merge._dump(brand_dir / "objection_ladders.json", ladders)
    oq = [q for q in _read(brand_dir / "open_questions.json") if ".open_questions.ladder_" not in q.get("id", "")]
    merge._dump(brand_dir / "open_questions.json", oq + questions)
    conflicts = _read(brand_dir / "review" / "conflicts.json")
    records = [r for recs in sections.values() for r in recs] + ladders
    merge._dump(brand_dir / "freshness.json", merge.freshness(brand, records, conflicts, today))
    if publish:
        import router
        router.write(brand, root, dt.date.fromisoformat(today))
    return {"ladders": len(ladders), "rungs": sum(len(l["value"]["rungs"]) for l in ladders),
            "open_questions_added": len(questions), "lanes": {k: len(v) for k, v in lanes.items()},
            "empty_lanes": [e["lane"] for e in empty]}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("brand")
    ap.add_argument("--today")
    ap.add_argument("--no-merge", action="store_true")
    ap.add_argument("--no-publish", action="store_true")
    args = ap.parse_args(argv[1:])
    print(json.dumps(run(args.brand, today=args.today, remerge=not args.no_merge, publish=not args.no_publish)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
