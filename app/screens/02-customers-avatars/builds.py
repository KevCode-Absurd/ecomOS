"""What to build next for each avatar: a rule on the brain, a drafted artefact, an owner and steps.

Pure functions on the rows audit.py builds (`avatar_rows`, `rungs`). No model, no writes.
The same brain gives the same builds. Drafts are templates filled from brain records only;
they are marked as drafts and a person approves anything that ships.

Rule for the next build of one avatar, first match wins:
  1. Top doubt (the ladder rung naming the avatar with the most one-star mentions) has no
     proof, and the rung lists `offer` in its uses: an offer spec that removes the doubt
     (LIFE-C42, guarantee and risk reversal). Agent drafts, a person approves.
  2. Top doubt has no proof: a product page proof block that answers it (SITE-C38).
     Agent drafts, a person approves and a person ships it on the page.
  3. No quotes at all: a research note that pulls quotes before anything is made (BRAND-C01).
     Agent does it.
  4. Otherwise: an ad brief for the avatar's first trigger moment with the proof on file
     (CREA-C06). Agent drafts, a person approves.
An avatar that rests on 1 source keeps its build and carries a "provisional" flag.
"""
from __future__ import annotations

from urllib.parse import urlparse

SCREEN = "02-customers-avatars"
CHANNEL_OF_SOURCE = {"Bombas site": "our site", "Trustpilot": "review sites", "Sitejabber": "review sites",
                     "Amazon": "Amazon", "Target": "retail stores", "Nordstrom": "retail stores",
                     "Other retailers": "retail stores", "Reddit": "Reddit", "Press": "press"}
NOT_TESTIMONIAL = {"Reddit"}
CAPS = {"offer": ("LIFE-C42", "founder_gate"), "page_section": ("SITE-C38", "human_assist"),
        "research_note": ("BRAND-C01", "agent_does"), "ad_brief": ("CREA-C06", "agent_does")}


def channels(avatar: dict, raw_counts: dict | None, source_name) -> list[dict]:
    """Where the avatar's voice shows up, by channel, from quote sources and counted mentions."""
    by: dict[str, int] = {}
    for q in avatar["quotes"]:
        ch = CHANNEL_OF_SOURCE.get(q["source"] or "", q["source"] or "unknown")
        by[ch] = by.get(ch, 0) + 1
    for k, n in (raw_counts or {}).items():
        if n:
            ch = CHANNEL_OF_SOURCE.get(source_name(k), source_name(k))
            by[ch] = max(by.get(ch, 0), n)
    return [{"channel": k, "n": v} for k, v in sorted(by.items(), key=lambda kv: (-kv[1], kv[0]))]


def usable_quote(avatar: dict) -> dict | None:
    """The first quote we may show as a customer's words: never a Reddit line."""
    return next((q for q in avatar["quotes"] if q["source"] not in NOT_TESTIMONIAL), None)


def _steps(kind: str, name: str, doubt: str | None) -> list[dict]:
    if kind == "offer":
        return [{"n": 1, "who": "agent", "text": f"Read the one-star lines on \"{doubt}\" and the current policies."},
                {"n": 2, "who": "agent", "text": "Draft the offer spec: what we promise, the limit, the cost cap, the page and ad line."},
                {"n": 3, "who": "person", "text": "Approve the spec and the cost cap. Nothing ships before that."},
                {"n": 4, "who": "person", "text": "Add the promise to the product page and the next ad brief."},
                {"n": 5, "who": "agent", "text": "Recount one-star mentions of this doubt on the next review pull."}]
    if kind == "page_section":
        return [{"n": 1, "who": "agent", "text": f"Pull the one-star and five-star lines on \"{doubt}\"."},
                {"n": 2, "who": "agent", "text": "Draft the proof block: headline in the customer's words, the proof, one review."},
                {"n": 3, "who": "person", "text": "Approve the block and add it to the product page."},
                {"n": 4, "who": "agent", "text": "Record the change in the brain so ads and emails reuse it."}]
    if kind == "research_note":
        return [{"n": 1, "who": "agent", "text": f"Pull reviews and posts that describe the {name} situation."},
                {"n": 2, "who": "agent", "text": "Keep 5 quotes from 2 or more sources with links."},
                {"n": 3, "who": "agent", "text": "Write them into the avatar record. The card re-grades itself."}]
    return [{"n": 1, "who": "agent", "text": f"Draft the ad brief for {name} from the brain."},
            {"n": 2, "who": "person", "text": "Approve the brief. Creative makes 3 variants."},
            {"n": 3, "who": "agent", "text": "Tag the ads with this avatar and angle so coverage can be read."},
            {"n": 4, "who": "agent", "text": "Read cost per order after 7 days against the account median."}]


def _draft(kind: str, avatar: dict, top: dict | None, proof_text: str | None) -> str:
    name = avatar["name"]
    trig = (avatar.get("triggers") or [None])[0]
    pains = avatar.get("pains") or []
    q = usable_quote(avatar)
    one = next((x for x in (top or {}).get("one_star_quotes") or [] if x), None)
    five = next((x for x in (top or {}).get("five_star_quotes") or [] if x), None)
    lines = [f"DRAFT for {name}"]
    if avatar.get("job"):
        lines.append(f"Job: {avatar['job']}")
    if kind == "offer":
        lines += [f"Doubt to remove: {top['doubt']} ({top['one_star']} one-star mentions)",
                  f"In their words: \"{one}\"" if one else "In their words: unavailable",
                  "Promise: unavailable until a person sets it. Start from the current guarantee.",
                  "Limit and cost cap: a person sets both before launch.",
                  "Where it shows: product page near the price, first line of the next ad, order email."]
    elif kind == "page_section":
        lines += [f"Section: answer to \"{top['doubt']}\"",
                  f"Headline: in the customer's words, like \"{one}\"" if one else "Headline: unavailable",
                  "Proof: none on file. A person adds the fact that answers it before this ships.",
                  f"Review to show: \"{five}\" (five-star)" if five else "Review to show: unavailable"]
    elif kind == "research_note":
        lines += ["Goal: 5 quotes from 2 or more sources.",
                  f"Known situation: {avatar.get('note') or name}"]
    else:
        lines += [f"Moment: {trig}" if trig else "Moment: unavailable",
                  f"Pain to open on: {pains[0]}" if pains else "Pain: unavailable",
                  f"Doubt to answer: {top['doubt']}" if top else "Doubt: none named",
                  f"Proof: {proof_text}" if proof_text else "Proof: unavailable",
                  f"Customer line: \"{five}\" (five-star)" if five else
                  (f"Customer line: \"{q['quote']}\" ({q['source']})" if q else "Customer line: unavailable"),
                  "Formats: 1 static, 1 short video, 1 carousel."]
    return "\n".join(lines)


def next_build(avatar: dict, top: dict | None) -> dict:
    """The one next build for an avatar, with owner, steps and a drafted artefact."""
    name = avatar["name"]
    if top and not top["proof_ids"]:
        kind = "offer" if "offer" in (top.get("uses") or []) else "page_section"
        title = (f"Offer that removes \"{top['doubt']}\"" if kind == "offer"
                 else f"Product page block that answers \"{top['doubt']}\"")
        why = f"{top['one_star'] if top['one_star'] is not None else 'Unknown'} one-star mentions ask this. No proof is on file."
    elif not avatar["quotes"]:
        kind, title = "research_note", f"Pull customer quotes for {name}"
        why = "No customer has said this in a quote we hold. It is a guess until they do."
    else:
        kind = "ad_brief"
        trig = (avatar.get("triggers") or ["their moment"])[0]
        title = f"Ad brief: {trig}, for {name}"
        why = (f"The top doubt, \"{top['doubt']}\", has proof on file. Put it in an ad." if top
               else "No doubt is named for this avatar. Lead with the job.")
    cap, autonomy = CAPS[kind]
    owner = "agent" if kind == "research_note" else "agent_drafts"
    proof_text = top.get("proof") if top else None
    return {"id": f"{SCREEN}.build.{avatar['key']}", "kind": kind, "title": title, "why": why, "owner": owner,
            "capability": {"id": cap, "autonomy": autonomy}, "steps": _steps(kind, name, top["doubt"] if top else None),
            "draft": _draft(kind, avatar, top, proof_text), "provisional": avatar["grounding"] != "grounded"}


# ---------------------------------------------------------------- avatar by channel coverage

# where an answer to a doubt ships, keyed by the rung's `uses` value
CHANNELS = [
    {"key": "copy", "label": "Ads and email", "kind": "ad_brief", "cap": ("CREA-C24", "agent_does"), "where": "the next ad and email"},
    {"key": "pdp", "label": "Product page", "kind": "page_section", "cap": ("SITE-C38", "human_assist"), "where": "the product page"},
    {"key": "amazon_listing", "label": "Amazon listing", "kind": "listing_fix", "cap": ("PROD-C34", "human_assist"), "where": "the Amazon listing"},
    {"key": "cx_macro", "label": "Support replies", "kind": "copy", "cap": ("LIFE-C27", "human_assist"), "where": "the support reply macro"},
    {"key": "offer", "label": "Offer", "kind": "offer", "cap": ("LIFE-C42", "founder_gate"), "where": "the offer"},
]
FORMAT_LABEL = {"dco": "dynamic creative", "dpa": "catalog ads", "video": "video", "image": "static image",
                "carousel": "carousel", "catalog": "catalog ads"}
FORMAT_GAP_SHARE = 0.15   # the category runs a format in 15 percent or more of live ads
FORMAT_GAP_RATIO = 0.5    # and we run it at under half that share


def _cell_brief(avatar: dict, ch: dict, open_rungs: list[dict]) -> dict:
    r = max(open_rungs, key=lambda x: (x["one_star"] or 0, x["level"] or 0))
    one = next((q for q in r.get("one_star_quotes") or [] if q), None)
    five = next((q for q in r.get("five_star_quotes") or [] if q), None)
    doubts = "; ".join(f"\"{x['doubt']}\" ({x['one_star'] if x['one_star'] is not None else 'unknown'} one-star)" for x in open_rungs)
    draft = "\n".join([f"DRAFT: {ch['label']} for {avatar['name']}",
                       f"Doubts with no answer here: {doubts}",
                       f"Lead doubt in their words: \"{one}\"" if one else "Lead doubt in their words: unavailable",
                       f"Five-star line to echo: \"{five}\"" if five else "Five-star line to echo: unavailable",
                       "Proof: none on file. A person adds the fact before this ships.",
                       f"Ships in: {ch['where']}."])
    owner = "agent_drafts"
    return {"id": f"{SCREEN}.cover.{avatar['key']}.{ch['key']}", "kind": ch["kind"],
            "title": f"{ch['label']}: answer \"{r['doubt']}\" for {avatar['name']}", "owner": owner,
            "capability": {"id": ch["cap"][0], "autonomy": ch["cap"][1]}, "draft": draft,
            "steps": [{"n": 1, "who": "agent", "text": "Pull the one-star and five-star lines for the doubt."},
                      {"n": 2, "who": "agent", "text": f"Draft the answer for {ch['where']}."},
                      {"n": 3, "who": "person", "text": "Add the proof and approve. Nothing ships before that."},
                      {"n": 4, "who": "agent", "text": "Mark the rung as answered in the brain so the cell turns green."}]}


def coverage(avatars: list[dict], all_rungs: list[dict]) -> dict:
    """Avatar by channel: doubts that channel must answer (them) against doubts answered with proof (us)."""
    rows, cells, skipped = [], {}, []
    for a in avatars:
        mine = [r for r in all_rungs if a["id"] in r["avatars"]]
        if not mine:
            skipped.append(a["name"])
            continue
        rows.append({"key": a["key"], "label": a["name"], "sub": f"share {round(a['share_estimate'] * 100)} percent"
                     if a["share_estimate"] is not None else "share unavailable"})
        cells[a["key"]] = {}
        for ch in CHANNELS:
            need = [r for r in mine if ch["key"] in (r.get("uses") or [])]
            done = [r for r in need if r["proof_ids"]]
            open_ = [r for r in need if not r["proof_ids"]]
            cell = {"us": len(done) if need else None, "them": len(need) if need else None, "unit": "n", "open": len(open_)}
            if open_:
                cell["brief"] = _cell_brief(a, ch, open_)
            cells[a["key"]][ch["key"]] = cell
    gaps = [(r, ch) for r in rows for ch in CHANNELS if cells[r["key"]][ch["key"]].get("open")]
    by_col = {ch["key"]: sum(1 for r, c in gaps if c["key"] == ch["key"]) for ch in CHANNELS}
    worst = max(CHANNELS, key=lambda c: by_col[c["key"]])
    line = (f"{len(gaps)} cells have a doubt with no answer. {worst['label']} has the most: {by_col[worst['key']]}."
            if gaps else "Every doubt is answered in every channel that needs it.")
    return {"rows": rows, "cols": [{"key": c["key"], "label": c["label"]} for c in CHANNELS], "cells": cells,
            "gaps": len(gaps), "line": line, "skipped": skipped}


def format_mix(learnings: list[dict]) -> dict:
    """Our live Meta format mix against the category median, from the Ad Library pulls in the brain."""
    own, comp = None, []
    for r in learnings:
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        f = v.get("formats")
        if not isinstance(f, dict) or not v.get("page"):
            continue
        tot = sum(n for n in f.values() if isinstance(n, (int, float)))
        if not tot:
            continue
        share = {k: n / tot for k, n in f.items() if isinstance(n, (int, float))}
        if v.get("role") == "self":
            own = {"page": v["page"], "share": share, "ads": tot}
        elif v.get("role") == "competitor":
            comp.append({"page": v["page"], "share": share, "ads": tot})
    if own is None or not comp:
        return {"available": False, "reason": "no Ad Library format pull for us and the category in the brain", "rows": []}
    fmts = sorted({k for c in comp for k in c["share"]} | set(own["share"]))
    rows = []
    for k in fmts:
        vals = sorted(c["share"].get(k, 0.0) for c in comp)
        mid = len(vals) // 2
        med = vals[mid] if len(vals) % 2 else (vals[mid - 1] + vals[mid]) / 2
        us = own["share"].get(k, 0.0)
        runs = sum(1 for c in comp if c["share"].get(k, 0) > 0)
        gap = med >= FORMAT_GAP_SHARE and us < med * FORMAT_GAP_RATIO
        rows.append({"format": k, "label": FORMAT_LABEL.get(k, k), "us": round(us, 4), "them": round(med, 4), "pages_running": runs, "gap": gap})
    rows.sort(key=lambda r: -r["them"])
    gaps = [r["label"] for r in rows if r["gap"]]
    return {"available": True, "rows": rows, "own_ads": own["ads"], "pages": len(comp),
            "line": (f"The category leans on {', '.join(gaps)} and we barely run it." if gaps
                     else "Our format mix is close to the category median."), "gaps": gaps}


def format_brief(row: dict, avatars: list[dict]) -> dict:
    """A test brief for a format the category runs and we do not: one variant per avatar with proof on its top doubt."""
    picks = [a for a in avatars if a.get("top_objection") and a["top_objection"]["proof"]][:3]
    lines = [f"DRAFT: {row['label']} test, one variant per avatar",
             f"Why: the category median runs it in {round(row['them'] * 100)} percent of live ads. We run {round(row['us'] * 100)} percent."]
    for i, a in enumerate(picks, 1):
        t = a["top_objection"]
        lines.append(f"Variant {i}, {a['name']}: open on \"{(a.get('triggers') or [a['job']])[0]}\", answer \"{t['doubt']}\" with: {t['proof_text']}")
    if not picks:
        lines.append("No avatar has proof on its top doubt yet. Answer a doubt first.")
    lines.append("Tag each ad with its avatar so the matrix can read coverage.")
    return {"id": f"{SCREEN}.format.{row['format']}", "kind": "test_brief", "owner": "agent_drafts",
            "title": f"Test {row['label']} with {len(picks)} avatar variants",
            "capability": {"id": "CREA-C06", "autonomy": "agent_does"}, "draft": "\n".join(lines),
            "steps": [{"n": 1, "who": "agent", "text": "Draft one variant per avatar from the brain."},
                      {"n": 2, "who": "person", "text": "Approve the brief. Creative builds the variants."},
                      {"n": 3, "who": "person", "text": "Launch at a capped test budget in the ad account."},
                      {"n": 4, "who": "agent", "text": "Read cost per order after 7 days against the account median."}]}


# ---------------------------------------------------------------- ladders per avatar

NOT_LANDING_RATIO = 2.0   # proof on file, yet one-star mentions are 2x or more the five-star ones
NOT_LANDING_MIN = 10      # and at least 10 one-star mentions
LEAD_RATIO = 1.0          # five-star mentions above one-star: a strength to lead with


def rung_verdict(r: dict) -> str:
    one, five = r["one_star"], r["five_star"]
    if not r["proof_ids"]:
        return "answer"
    if isinstance(one, int) and isinstance(five, int) and one >= NOT_LANDING_MIN and one >= NOT_LANDING_RATIO * max(five, 1):
        return "not_landing"
    if isinstance(one, int) and isinstance(five, int) and five > one * LEAD_RATIO:
        return "lead"
    return "keep"


def _rung_action(r: dict, verdict: str, names: list[str]) -> dict | None:
    one = next((q for q in r["one_star_quotes"] if q), None)
    five = next((q for q in r["five_star_quotes"] if q), None)
    who = ", ".join(names[:3]) + (f" and {len(names) - 3} more" if len(names) > 3 else "") if names else "no avatar named"
    counts = f"{r['one_star'] if r['one_star'] is not None else 'unknown'} one-star, {r['five_star'] if r['five_star'] is not None else 'unknown'} five-star"
    base = f"{SCREEN}.rung.{r['id']}"
    if verdict == "answer":
        offer = "offer" in (r.get("uses") or [])
        kind, cap = ("offer", ("LIFE-C42", "founder_gate")) if offer else ("copy", ("CREA-C24", "agent_does"))
        title = f"{'Offer' if offer else 'Copy'} that answers \"{r['doubt']}\""
        draft = [f"DRAFT: {'offer spec' if offer else 'objection copy'} for \"{r['doubt']}\"", f"For: {who}", f"Counts: {counts}",
                 f"Their words: \"{one}\"" if one else "Their words: unavailable",
                 "Proof: none on file. " + ("A person sets the promise, the limit and the cost cap." if offer
                                             else "A person adds the fact that answers it."),
                 "Ships in: " + ", ".join(u.replace("_", " ") for u in r.get("uses") or []) + "."]
        steps = [{"n": 1, "who": "agent", "text": "Pull every one-star line on this doubt."},
                 {"n": 2, "who": "agent", "text": f"Draft the {'offer spec' if offer else 'answer copy'} in their words."},
                 {"n": 3, "who": "person", "text": "Add the proof and approve."},
                 {"n": 4, "who": "agent", "text": "Link the proof record to the rung. It turns green here."}]
    elif verdict == "not_landing":
        kind, cap = "page_section", ("SITE-C38", "human_assist")
        title = f"Move the proof for \"{r['doubt']}\" to the first screen"
        draft = [f"DRAFT: page and ad change for \"{r['doubt']}\"", f"For: {who}", f"Counts: {counts}. Proof is on file, but doubters still win.",
                 f"Proof: {r['proof']}", f"Their words: \"{one}\"" if one else "Their words: unavailable",
                 "Change: put the proof in the product page first screen and the first line of ads for these avatars."]
        steps = [{"n": 1, "who": "agent", "text": "Find where the proof shows today on the product page and ads."},
                 {"n": 2, "who": "agent", "text": "Draft the first-screen block and 2 ad first lines."},
                 {"n": 3, "who": "person", "text": "Approve and ship the page block."},
                 {"n": 4, "who": "agent", "text": "Recount one-star mentions on the next review pull."}]
    elif verdict == "lead":
        kind, cap = "ad_brief", ("CREA-C06", "agent_does")
        title = f"Lead ads with the answer to \"{r['doubt']}\""
        draft = [f"DRAFT: ad brief on a strength", f"For: {who}", f"Counts: {counts}. Buyers praise this more than they doubt it.",
                 f"Proof: {r['proof']}", f"Five-star line to echo: \"{five}\"" if five else "Five-star line: unavailable",
                 "Formats: 1 static, 1 short video."]
        steps = [{"n": 1, "who": "agent", "text": "Draft the brief from the proof and the five-star lines."},
                 {"n": 2, "who": "person", "text": "Approve the brief. Creative makes 2 variants."},
                 {"n": 3, "who": "agent", "text": "Read cost per order after 7 days against the account median."}]
    else:
        return None
    return {"id": base, "kind": kind, "title": title, "owner": "agent_drafts",
            "capability": {"id": cap[0], "autonomy": cap[1]}, "draft": "\n".join(draft), "steps": steps}


def ladders(all_rungs: list[dict], avatars: list[dict]) -> dict:
    """Every rung with its counts, proof, verdict and action, and the avatars it names."""
    names = {a["id"]: a["name"] for a in avatars}
    keys = {a["id"]: a["key"] for a in avatars}
    rows = []
    for r in all_rungs:
        v = rung_verdict(r)
        av = [names[x] for x in r["avatars"] if x in names]
        one, five = r["one_star"], r["five_star"]
        rows.append({"id": r["id"], "theme": r["theme"], "level": r["level"], "doubt": r["doubt"], "one_star": one, "five_star": five,
                     "proof": r["proof"] if r["proof_ids"] else None, "proof_ids": r["proof_ids"], "verdict": v,
                     "avatars": [keys[x] for x in r["avatars"] if x in keys], "avatar_names": av,
                     "uses": r.get("uses") or [], "action": _rung_action(r, v, av)})
    order = {"answer": 0, "not_landing": 1, "lead": 2, "keep": 3}
    rows.sort(key=lambda x: (order[x["verdict"]], -(x["one_star"] or 0), x["id"]))
    counts = {k: sum(1 for x in rows if x["verdict"] == k) for k in order}
    return {"rows": rows, "counts": counts,
            "line": f"{counts['answer']} rungs have no proof. {counts['not_landing']} have proof that is not landing. "
                    f"{counts['lead']} are strengths to lead with."}


# ---------------------------------------------------------------- language bank by rung

WORDS_PER_SIDE = 6
MAX_WORDS = 14
GENERIC = {"great", "good", "love", "loved", "socks", "sock", "product", "these", "this", "very", "the", "are", "is", "best",
           "nice", "awesome", "amazing", "item", "a", "and", "it", "they", "them", "my", "i", "so", "pair", "pairs", "ever",
           "will", "buy", "again", "more", "from", "vendor", "excellent", "perfect", "star", "stars", "five", "one"}
WIN_THEMES = {"praise", "result", "gift", "surprise"}


def _clip(text: str) -> str:
    words = str(text or "").split()
    return " ".join(words[:MAX_WORDS]) + ("..." if len(words) > MAX_WORDS else "")


def _generic(text: str, brand_tokens: set[str]) -> bool:
    toks = [t.strip(".,!?'\"’()").lower() for t in str(text or "").split()]
    return not [t for t in toks if t and t not in GENERIC and t not in brand_tokens]


def phrase_row(rec: dict, source_name) -> dict | None:
    v = rec.get("value") if isinstance(rec.get("value"), dict) else {}
    revs = v.get("reviews") or []
    first = revs[0] if revs else {}
    star = first.get("star")
    theme = v.get("theme")
    if theme == "complaint" or (isinstance(star, int) and star <= 2):
        side = "doubt"
    elif theme in WIN_THEMES or (isinstance(star, int) and star >= 4):
        side = "win"
    else:
        return None
    raw = first.get("source") or v.get("source")
    if not raw:
        ref = first.get("url") or (rec.get("source") or {}).get("ref") or ""
        url = ref[ref.find("http"):] if "http" in ref else ""
        host = urlparse(url).netloc
        raw = host[4:] if host.startswith("www.") else host
    src = source_name(raw or "") if raw else "summary"
    reddit = src == "Reddit" or bool(v.get("subreddit"))
    return {"id": rec["id"], "text": _clip(v.get("phrase") or rec.get("text")), "side": side, "star": star,
            "source": "Reddit" if reddit else src, "language_only": reddit,
            "weight": (len(revs), 1 if first.get("verified") else 0, first.get("helpful") or first.get("upvotes") or 0)}


def words(lang_records: list[dict], all_rungs: list[dict], avatars: list[dict], brand_tokens: set[str], source_name) -> dict:
    """Customers' own words per rung, split into how they say the doubt and how they say the win."""
    by_id = {r["id"]: r for r in lang_records}
    names = {a["id"]: a["name"] for a in avatars}
    keys = {a["id"]: a["key"] for a in avatars}
    rows, used = [], set()
    for r in all_rungs:
        phrases = []
        for pid in r["derived_from"]:
            rec = by_id.get(pid)
            if rec is None:
                continue
            p = phrase_row(rec, source_name)
            if p and not _generic(p["text"], brand_tokens):
                phrases.append(p)
        seen, sides = set(), {"doubt": [], "win": []}
        for p in sorted(phrases, key=lambda x: (x["language_only"], -x["weight"][0], -x["weight"][1], -x["weight"][2], len(x["text"]), x["id"])):
            k = p["text"].lower()
            if k in seen:
                continue
            seen.add(k)
            if len(sides[p["side"]]) < WORDS_PER_SIDE:
                sides[p["side"]].append({x: p[x] for x in ("id", "text", "star", "source", "language_only")})
        if not sides["doubt"] and not sides["win"]:
            continue
        used.update(x["id"] for s in sides.values() for x in s)
        who = [names[x] for x in r["avatars"] if x in names]
        head = [f"COPY BRIEF: answer \"{r['doubt']}\"", f"For: {', '.join(who) if who else 'every buyer'}",
                f"Proof: {r['proof']}" if r["proof_ids"] else "Proof: none on file. A person adds it before this ships.",
                "Rule: use their words as written. Lines marked language only are never quoted as a review."]
        rows.append({"id": r["id"], "doubt": r["doubt"], "theme": r["theme"], "level": r["level"],
                     "avatars": [keys[x] for x in r["avatars"] if x in keys], "doubt_words": sides["doubt"], "win_words": sides["win"],
                     "proof": bool(r["proof_ids"]),
                     "brief": {"id": f"{SCREEN}.words.{r['id']}", "title": f"Copy brief in their words: \"{r['doubt']}\"",
                               "head": head, "owner": "agent_drafts", "kind": "copy",
                               "capability": {"id": "BRAND-C14", "autonomy": "agent_does"},
                               "steps": [{"n": 1, "who": "agent", "text": "Write 5 headlines and 3 ad first lines from the picked words."},
                                         {"n": 2, "who": "person", "text": "Approve the lines. Nothing ships before that."},
                                         {"n": 3, "who": "agent", "text": "Log which banked phrases went live, so reuse can be counted."}]}})
    rows.sort(key=lambda x: (x["proof"], -(len(x["doubt_words"]) + len(x["win_words"])), x["id"]))
    lang = sum(1 for rec in lang_records if phrase_row(rec, source_name))
    return {"rows": rows, "phrases_used": len(used), "phrases_total": len(lang_records), "phrases_sided": lang,
            "line": f"{len(used)} of {len(lang_records)} banked phrases sit on a rung. Pick lines and make a copy brief."}
