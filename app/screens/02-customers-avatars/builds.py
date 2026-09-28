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

import re
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


# ---------------------------------------------------------------- cohort grid and retention moves

GRID_MONTHS = 12
GRID_COHORTS = 18
CLIFF_DROP = 0.40          # a cohort's active share falls 40 percent or more from one month to the next
CLIFF_SHARE = 0.5          # and half or more of the cohorts alive then fall together in the same calendar month
WEAK_COHORT = 0.8          # repeat in months 1 to 3 under 0.8x the median of the grid
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December"]


def _add(month: str, n: int) -> str:
    y, m = (int(x) for x in month.split("-"))
    m += n
    return f"{y + (m - 1) // 12}-{(m - 1) % 12 + 1:02d}"


def _median(xs: list[float]) -> float | None:
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    mid = len(xs) // 2
    return xs[mid] if len(xs) % 2 else (xs[mid - 1] + xs[mid]) / 2


def _move(mid, title, why, kind, label, cap, owner, steps, draft, check_days=28, stop=None, as_of=None):
    import datetime as _dt
    check = (_dt.date.fromisoformat(as_of) + _dt.timedelta(days=check_days)).isoformat() if as_of else None
    return {"id": f"{SCREEN}.retention.{mid}", "finding_ids": [], "title": title, "why": why, "severity": "medium",
            "status": "open", "owner": owner, "capability": {"id": cap[0], "autonomy": cap[1]},
            "artefact": {"kind": kind, "label": label, "draft": draft}, "steps": steps, "check_on": check, "stop_rule": stop}


def cohort_grid(cohorts: list[dict], monthly: list[dict], as_of: str, avatars: list[dict]) -> dict:
    """Active share by months since the first order, the breaks in it, and the retention move for each break.

    Active share: customers of a cohort who ordered again in a month, over the cohort size. A cell shows only once
    that calendar month has ended. Est. 12-month value: (1 + active months 1 to 12 over size) x the cohort month's
    AOV, which assumes one order per active customer per month; it is an estimate, labelled so.
    """
    if not cohorts:
        return {"available": False, "reason": "no cohort table", "rows": []}
    aov = {r["month"]: r.get("aov") for r in monthly if r.get("aov")}
    done = lambda m: _add(m, 1) <= as_of[:7]
    rows = []
    for c in cohorts[-GRID_COHORTS - 3:]:
        n, act = c.get("customers"), c.get("active_by_month") or []
        if not n:
            continue
        vals = []
        for k in range(1, GRID_MONTHS + 1):
            cal = _add(c["cohort"], k)
            vals.append(round(act[k] / n, 4) if k < len(act) and done(cal) else None)
        full12 = all(v is not None for v in vals)
        ltv = round((1 + sum(vals)) * aov[c["cohort"]], 2) if full12 and aov.get(c["cohort"]) else None
        r3 = round(sum(vals[:3]), 4) if all(v is not None for v in vals[:3]) else None
        if any(v is not None for v in vals):
            rows.append({"cohort": c["cohort"], "customers": n, "values": vals, "repeat_m1_m3": r3, "value_12m": ltv})
    rows = rows[-GRID_COHORTS:]
    # second-order peak: the month 1 to 3 with the highest median active share
    med_by_k = [_median([r["values"][k] for r in rows]) for k in range(GRID_MONTHS)]
    peak_k = max(range(3), key=lambda k: med_by_k[k] or -1) + 1
    # calendar cliff: the calendar month where most cohorts alive then fall 40 percent or more
    by_cal: dict[str, list[bool]] = {}
    for r in rows:
        for k in range(1, GRID_MONTHS):
            a, b = r["values"][k - 1], r["values"][k]
            if a and b is not None and k >= 2:
                by_cal.setdefault(_add(r["cohort"], k + 1), []).append(b <= a * (1 - CLIFF_DROP))
    cliffs = sorted(((m, sum(v) / len(v), len(v)) for m, v in by_cal.items() if len(v) >= 3 and sum(v) / len(v) >= CLIFF_SHARE),
                    key=lambda x: (-x[1], x[0]))
    # age break: the month after the peak with the largest median fall, leaving out cells in a calendar cliff month
    cliff_months = {m for m, _, _ in cliffs}
    med_ex = [_median([r["values"][k] for r in rows if _add(r["cohort"], k + 1) not in cliff_months]) for k in range(GRID_MONTHS)]
    drops = []
    for k in range(peak_k, GRID_MONTHS - 1):
        a, b = med_ex[k - 1], med_ex[k]
        if a and b is not None:
            drops.append((round(1 - b / a, 4), k))
    age_drop, age_k = max(drops) if drops else (None, None)
    rep = [r["repeat_m1_m3"] for r in rows if r["repeat_m1_m3"] is not None]
    rep_med = _median(rep)
    weak = [r for r in rows if r["repeat_m1_m3"] is not None and rep_med and r["repeat_m1_m3"] < WEAK_COHORT * rep_med]
    moves = []
    pk = round((med_by_k[peak_k - 1] or 0) * 100, 1)
    day = max(14, peak_k * 30 - 10)
    moves.append(_move(
        "second_order", f"Time the second-order email to day {day}",
        f"Month {peak_k} is when most repeat buyers come back: {pk} percent of a cohort, median of {len(rows)} cohorts.",
        "flow", "a post-purchase flow step", ("LIFE-C07", "founder_gate"), "agent_drafts",
        [{"n": 1, "who": "agent", "text": f"Read the post-purchase flow and find the step nearest day {day}."},
         {"n": 2, "who": "agent", "text": "Draft the step: the product they bought, the next one to try, their own words."},
         {"n": 3, "who": "person", "text": "Approve the email and set the send day in the email tool."},
         {"n": 4, "who": "agent", "text": f"Read month {peak_k} active share for the next 2 cohorts against {pk} percent."}],
        f"DRAFT flow step\nSend on: day {day} after the first order\nWhy then: month {peak_k} holds the most second orders ({pk} percent)\n"
        "Content: how their first pair is doing, the next product to try, a five-star line from the ladder.",
        stop=f"Stop if month {peak_k} active share falls below {round(pk * 0.9, 1)} percent for 2 cohorts", as_of=as_of))
    if age_k is not None and age_drop and age_drop >= 0.2:
        wd = age_k * 30
        a_, b_ = round(med_ex[age_k - 1] * 100, 1), round(med_ex[age_k] * 100, 1)
        moves.append(_move(
            "age_break", f"Start win-back at day {wd}, before month {age_k + 1}",
            f"Active share falls {round(age_drop * 100)} percent from month {age_k} ({a_} percent) to month {age_k + 1} ({b_} percent).",
            "flow", "a win-back flow", ("LIFE-C08", "founder_gate"), "agent_drafts",
            [{"n": 1, "who": "agent", "text": f"Read the win-back flow trigger. Note its current start day."},
             {"n": 2, "who": "agent", "text": f"Draft a 3-email win-back from day {wd}: reminder, their words, a small reason to come back."},
             {"n": 3, "who": "person", "text": "Approve the emails and any offer in them."},
             {"n": 4, "who": "agent", "text": f"Read month {age_k + 1} active share for the next 2 cohorts."}],
            f"DRAFT win-back\nStart: day {wd}\nEmail 1: what is new since their first order\nEmail 2: the top five-star line for their product\n"
            "Email 3: a small reason to come back. A person sets any offer.", as_of=as_of))
    for cal, share, n in cliffs[:1]:
        mname = MONTH_NAMES[int(cal[5:7]) - 1]
        moves.append(_move(
            f"calendar_{cal}", f"Plan a {mname} return for every past buyer",
            f"In {mname} {cal[:4]}, {round(share * 100)} percent of {n} cohorts fell 40 percent or more at once. It is the calendar, not their age.",
            "email", "a campaign plan for the month", ("LIFE-C20", "agent_does"), "agent_drafts",
            [{"n": 1, "who": "agent", "text": f"Pull what past buyers bought before {mname} and what they return for."},
             {"n": 2, "who": "agent", "text": f"Draft a {mname} plan: 2 emails and 1 ad for past buyers, no deep discount."},
             {"n": 3, "who": "person", "text": "Approve the plan and put it on the calendar."},
             {"n": 4, "who": "agent", "text": f"Compare {mname} active share with last year's fall."}],
            f"DRAFT {mname} plan\nAudience: every buyer from the last 12 months\nWhy: {round(share * 100)} percent of cohorts fell together in {mname} {cal[:4]}\n"
            "Emails: 2, one on what is new, one on a care or replace theme\nAd: 1 for past buyers", as_of=as_of))
    if weak:
        names = ", ".join(r["cohort"] for r in weak[:4])
        gifting = [a["name"] for a in avatars if any(w in " ".join(a.get("triggers") or []).lower() for w in ("gift", "holiday", "christmas"))]
        who = f" The gift avatar, {gifting[0]}, buys in these months." if gifting else ""
        moves.append(_move(
            "weak_cohorts", f"Give first buyers from {names} their own post-purchase path",
            f"These cohorts repeat at under {int(WEAK_COHORT * 100)} percent of the median in months 1 to 3 ({round((rep_med or 0) * 100, 1)} percent).{who}",
            "flow", "a post-purchase branch", ("LIFE-C07", "founder_gate"), "agent_drafts",
            [{"n": 1, "who": "agent", "text": "Split first orders in these months by gift or self from order notes and ship-to."},
             {"n": 2, "who": "agent", "text": "Draft a branch for gift buyers: a thank-you and a pair for themselves."},
             {"n": 3, "who": "person", "text": "Approve the branch in the email tool."},
             {"n": 4, "who": "agent", "text": "Read months 1 to 3 repeat for the next cohort from these months."}],
            f"DRAFT post-purchase branch\nFor: first buyers in {names}\nEmail 1: thank you, and how the gift landed\n"
            "Email 2: a pair for you, with a five-star line on comfort\nEmail 3: the care guide", as_of=as_of))
    cols = [f"M{k}" for k in range(1, GRID_MONTHS + 1)]
    return {"available": True, "rows": rows, "columns": cols, "median_by_month": [round(x, 4) if x is not None else None for x in med_by_k],
            "peak_month": peak_k, "age_break": {"month": age_k, "drop": age_drop} if age_k else None,
            "calendar_break": {"month": cliffs[0][0], "share": round(cliffs[0][1], 4), "cohorts": cliffs[0][2]} if cliffs else None,
            "weak": [r["cohort"] for r in weak], "repeat_median": rep_med, "moves": moves, "as_of": as_of, "simulated": True}


# ---------------------------------------------------------------- new against returning, and what drives it

SHARE_FALL_PTS = 0.02       # returning share down 2 points or more against the same month last year
PAID_RETURNING = 0.25       # a quarter or more of returning orders arrive through paid ads
OWNED = ("email", "sms")
PAID = ("paid_social", "paid_search")
OWNED_LAG_PTS = 0.05        # owned channels grow returning orders 5 points slower than the rest, year on year
CHANNEL_LABEL = {"paid_social": "paid social", "paid_search": "paid search", "organic_search": "organic search",
                 "direct": "direct", "email": "email", "sms": "SMS", "other": "other", "pos": "stores"}


def mix(monthly: list[dict], channels: list[dict], as_of: str) -> dict:
    """Returning share of orders by month, this year against last, and the channels behind the change."""
    full = [r for r in monthly if r.get("orders") and _add(r["month"], 1) <= as_of[:7]]
    if len(full) < 13:
        return {"available": False, "reason": f"only {len(full)} full months; year on year needs 13", "moves": []}
    share = {r["month"]: r["returning_customer_orders"] / r["orders"] for r in full}
    last = full[-1]["month"]
    ly = _add(last, -12)
    months = [r["month"] for r in full[-12:]]
    series = {"this_year": [round(share[m], 4) for m in months],
              "last_year": [round(share[_add(m, -12)], 4) if _add(m, -12) in share else None for m in months]}
    now, before = share[last], share.get(ly)
    delta = round(now - before, 4) if before is not None else None
    ret = lambda m: {r["channel"]: r["orders"] - r["new_customer_orders"] for r in channels if r["month"] == m}
    a, b = ret(ly), ret(last)
    steps = [{"label": ly, "value": round(sum(a.values())), "kind": "total"}]
    contrib = []
    for ch in sorted(set(a) | set(b), key=lambda k: -abs(b.get(k, 0) - a.get(k, 0))):
        d = b.get(ch, 0) - a.get(ch, 0)
        contrib.append({"channel": ch, "label": CHANNEL_LABEL.get(ch, ch), "last_year": a.get(ch), "now": b.get(ch), "change": round(d),
                        "new_channel": ch not in a})
        steps.append({"label": CHANNEL_LABEL.get(ch, ch), "value": round(d), "kind": "up" if d >= 0 else "down"})
    steps.append({"label": last, "value": round(sum(b.values())), "kind": "total"})
    tot_b = sum(b.values())
    paid_share = round(sum(b.get(c, 0) for c in PAID) / tot_b, 4) if tot_b else None
    like = [c for c in b if c in a]
    growth = lambda chs: (sum(b[c] for c in chs) / sum(a[c] for c in chs) - 1) if chs and sum(a[c] for c in chs) else None
    owned_g = growth([c for c in like if c in OWNED])
    rest_g = growth([c for c in like if c not in OWNED])
    moves = []
    if delta is not None and delta <= -SHARE_FALL_PTS:
        worst = min(contrib, key=lambda x: x["change"])
        moves.append(_move(
            "share_fall", f"Win back returning orders lost in {worst['label']}",
            f"Returning share fell from {round(before * 100, 1)} to {round(now * 100, 1)} percent against {ly}. {worst['label'].capitalize()} lost the most: {abs(worst['change']):,} orders.",
            "flow", "a win-back plan for that channel", ("LIFE-C08", "founder_gate"), "agent_drafts",
            [{"n": 1, "who": "agent", "text": f"List what changed in {worst['label']} since {ly}: sends, audiences, offers."},
             {"n": 2, "who": "agent", "text": "Draft the fix: the flow or audience to restore, with its send or spend plan."},
             {"n": 3, "who": "person", "text": "Approve and ship the fix."},
             {"n": 4, "who": "agent", "text": "Read returning share next month against this month."}],
            f"DRAFT win-back plan\nChannel: {worst['label']}\nLost: {abs(worst['change']):,} returning orders against {ly}\n"
            "Fix: restore the flow or audience that carried these buyers. A person sets any offer.", as_of=as_of))
    if paid_share is not None and paid_share >= PAID_RETURNING:
        n_paid = round(sum(b.get(c, 0) for c in PAID))
        moves.append(_move(
            "paid_returning", "Move returning buyers from paid ads to email and SMS",
            f"{round(paid_share * 100, 1)} percent of returning orders came through paid ads in {last}: {n_paid:,} orders. We pay again to reach buyers we already have.",
            "budget_move", "an exclusion list and an owned-channel capture plan", ("MEDIA-C12", "human_assist"), "agent_drafts",
            [{"n": 1, "who": "agent", "text": "Build the past-buyer exclusion list for prospecting campaigns."},
             {"n": 2, "who": "agent", "text": "Draft an SMS and email opt-in step for the order page and first email."},
             {"n": 3, "who": "person", "text": "Approve the list and apply it in the ad account. The agent never writes there."},
             {"n": 4, "who": "agent", "text": "Read paid share of returning orders after 28 days."}],
            f"DRAFT\nExclude: buyers from the last 180 days from prospecting ad sets\nKeep: one retargeting ad set for past buyers, capped\n"
            f"Capture: SMS opt-in on the order page\nTarget: paid share of returning orders under {int(PAID_RETURNING * 100)} percent",
            stop="Stop if returning orders fall 5 percent for 2 weeks", as_of=as_of))
    if owned_g is not None and rest_g is not None and owned_g < rest_g - OWNED_LAG_PTS:
        moves.append(_move(
            "owned_lag", "Find why email and SMS bring back fewer buyers than other channels",
            f"Returning orders from email and SMS grew {round(owned_g * 100, 1)} percent against {ly}. Other channels grew {round(rest_g * 100, 1)} percent.",
            "report", "a flow health review", ("LIFE-C20", "agent_does"), "agent",
            [{"n": 1, "who": "agent", "text": "Pull flow and campaign orders by month for both years."},
             {"n": 2, "who": "agent", "text": "Name the flow or list that slowed, with its numbers."},
             {"n": 3, "who": "agent", "text": "Post the review here with the fix to approve."}],
            "DRAFT review outline\nFlows by orders, this year against last\nList size and send volume\nThe flow that slowed and the fix", as_of=as_of))
    return {"available": True, "months": months, "series": series, "latest": last, "last_year_month": ly,
            "share_now": round(now, 4), "share_last_year": round(before, 4) if before is not None else None, "delta": delta,
            "waterfall": steps, "contrib": contrib, "paid_share_returning": paid_share,
            "owned_growth": round(owned_g, 4) if owned_g is not None else None, "rest_growth": round(rest_g, 4) if rest_g is not None else None,
            "moves": moves, "simulated": True}


# ---------------------------------------------------------------- avatars served and not served

# Buying situations, as word stems. Category-level, not brand facts; see Contract asks in FEATURES.md.
SITUATIONS = {"hiking and outdoor": r"\b(hik|trail|outdoor)", "running": r"\b(running|runner|marathon)",
              "work shifts": r"\b(shift|nurse|work day|workday|at work)", "medical relief": r"\b(postpartum|pots|plantar|medical|doctor|relief)",
              "gifting": r"\b(gift|holiday|christmas)", "kids": r"\b(kid|child|toddler|teen)",
              "cold weather": r"\b(winter|cold|wool|merino)", "style": r"\b(style|fashion|self expression)",
              "compression": r"\bcompression"}


def _hits(text: str, pattern: str) -> bool:
    return re.search(pattern, text.lower()) is not None


def served(avatars: list[dict], all_rungs: list[dict], competitors: list[dict], positioning: list[dict]) -> dict:
    """Our avatars by reach and how well we serve them, and the buying situations the category serves that we do not."""
    pts, unplaced, verdicts = [], [], []
    tot_one = sum(r["one_star"] or 0 for r in all_rungs)
    tot_five = sum(r["five_star"] or 0 for r in all_rungs)
    mid_y = round(tot_five / (tot_one + tot_five), 4) if tot_one + tot_five else None
    for a in avatars:
        mine = [r for r in all_rungs if a["id"] in r["avatars"]]
        one = sum(r["one_star"] or 0 for r in mine)
        five = sum(r["five_star"] or 0 for r in mine)
        y = round(five / (one + five), 4) if one + five else None
        if a["share_estimate"] is None or y is None:
            unplaced.append({"name": a["name"], "why": "share unavailable" if a["share_estimate"] is None else "no rated doubts"})
            continue
        pts.append({"key": a["key"], "label": " ".join([w for w in a["name"].split() if w.lower() not in ("and", "for", "the", "of")][:2]), "name": a["name"], "x": a["share_estimate"], "y": y, "us": True, "size": one + five,
                    "note": f"{five} five-star, {one} one-star on its doubts"})
    mid_x = _median([p["x"] for p in pts])
    for p in pts:
        big, well = p["x"] >= (mid_x or 0), p["y"] >= (mid_y or 0)
        p["quadrant"] = ("core" if well else "fix_first") if big else ("scale" if well else "park")
        verdicts.append({"key": p["key"], "name": p["name"], "quadrant": p["quadrant"], "share": p["x"], "served": p["y"]})
    # the category conversation: situations competitors push, and situations Reddit names
    comp = []
    for r in competitors:
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        if v.get("positioning") and v.get("name"):
            comp.append({"name": v["name"], "id": r["id"],
                         "text": " ".join([v["positioning"], str(v.get("what_they_push") or ""), " ".join(v.get("hook_types") or [])])})
    reddit = {a["name"]: a for a in avatars if not a["quotes"] and a.get("count_by_source", {}).get("reddit")}
    segs = []
    for seg, stems in SITUATIONS.items():
        ours = [a["name"] for a in avatars if a["quotes"] and _hits(" ".join([a["name"], a.get("job") or "", *a.get("triggers", []), *a.get("pains", [])]), stems)]
        theirs = [c["name"] for c in comp if _hits(c["text"], stems)]
        talk = [n for n in reddit if _hits(n, stems)]
        mentions = sum(reddit[n]["count_by_source"].get("reddit", 0) for n in talk)
        if ours:
            verdict = "hold" if theirs else "own"
        elif len(theirs) >= 2:
            verdict = "gap"
        elif theirs or talk:
            verdict = "watch"
        else:
            continue
        action = None
        if verdict in ("gap", "watch"):
            action = {"id": f"{SCREEN}.segment.{seg.replace(' ', '_')}", "kind": "research_note", "owner": "agent_drafts",
                      "title": f"Size the {seg} buyer before we make anything for them",
                      "capability": {"id": "BRAND-C16", "autonomy": "founder_gate"},
                      "draft": "\n".join([f"DRAFT research note: {seg}",
                                          f"Who serves it: {', '.join(theirs) if theirs else 'no competitor in the brain'}",
                                          f"Reddit talk: {mentions} mentions" if talk else "Reddit talk: none in the brain",
                                          "Questions: do our buyers already use us for this, which product fits, what proof would they need",
                                          "Sources: our reviews that mention it, competitor reviews, 5 customer interviews",
                                          "Output: an avatar record with 5 quotes from 2 or more sources, or a no-go"]),
                      "steps": [{"n": 1, "who": "agent", "text": f"Search our reviews and tickets for {seg} words."},
                                {"n": 2, "who": "agent", "text": "Read what competitors promise these buyers and at what price."},
                                {"n": 3, "who": "agent", "text": "Draft the avatar record or a no-go with the numbers."},
                                {"n": 4, "who": "person", "text": "Decide: build for them, test one ad, or drop it."}]}
        segs.append({"segment": seg, "ours": ours, "theirs": theirs, "reddit_mentions": mentions if reddit else None,
                     "verdict": verdict, "action": action})
    order = {"gap": 0, "watch": 1, "hold": 2, "own": 3}
    segs.sort(key=lambda s: (order[s["verdict"]], -len(s["theirs"]), s["segment"]))
    gaps = [s["segment"] for s in segs if s["verdict"] == "gap"]
    fix = [v["name"] for v in verdicts if v["quadrant"] == "fix_first"]
    return {"points": pts, "mid_x": mid_x, "mid_y": mid_y, "unplaced": unplaced, "verdicts": verdicts, "segments": segs,
            "line": (f"Fix first: {', '.join(fix)}. " if fix else "") +
                    (f"The category serves {', '.join(gaps)} and we have no avatar for it." if gaps else "No contested situation is left unserved.")}


# ---------------------------------------------------------------- where reviews say an avatar is misread

LINE_PROBLEM = 1.5        # a line's 1 and 2 star share at 1.5x the median line or more
STOP = {"with", "that", "than", "after", "their", "they", "them", "from", "into", "only", "some", "more", "this", "have",
        "does", "like", "feel", "feels", "over", "vs", "the", "and", "for", "not", "enough", "every", "day", "socks", "sock"}
MIN_LINKS = 2             # the avatar is tied to the line by 2 or more reviews
ISSUE_KIND = [("order", r"\b(shipment|shipments|shipped|order|delivery)"), ("fit", r"\b(size|sizing|small|huge|short|fit|length|longer|knee|pull on|tight|slip|slides|rolls)"),
              ("wear", r"\b(thin|wear|pilling|thread|seam|apart|decline|quality|holes?|peel)"),
              ("feel", r"\b(warm|drape|felt|thick|support|compression)")]
KIND_ACTION = {"order": ("ticket", ("LIFE-C27", "human_assist"), "a fulfilment ticket and a support reply"),
               "fit": ("page_section", ("SITE-C38", "human_assist"), "a fit and size block for the product page"),
               "wear": ("ticket", ("PROD-C73", "human_assist"), "a product quality ticket with the review evidence"),
               "feel": ("copy", ("CREA-C24", "agent_does"), "expectation copy for the product page and ads")}


def _content(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]+", str(text or "").lower()) if len(w) >= 4 and w not in STOP}


def _issue_kind(issue: str) -> str:
    for k, pat in ISSUE_KIND:
        if re.search(pat, issue.lower()):
            return k
    return "feel"


def misreads(avatar_records: list[dict], avatars: list[dict], all_rungs: list[dict], lang_records: list[dict],
             product_records: list[dict]) -> dict:
    """Review themes by product line against what each avatar hires us for. A misread is a line the avatar buys
    whose top complaints hit the avatar's own job or pains, on a line at or above the median 1 and 2 star share."""
    lines = {}
    for r in product_records:
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        dist = v.get("yotpo_star_distribution")
        if r.get("field") != "review_summary" or not isinstance(dist, dict):
            continue
        tot = sum(n for n in dist.values() if isinstance(n, (int, float)))
        if not tot:
            continue
        lines[v["product_line"]] = {"line": v["product_line"], "product": v.get("yotpo_product"), "pdp": v.get("pdp"), "reviews": tot,
                                    "average": v.get("yotpo_average"), "neg_share": round((dist.get("1", 0) + dist.get("2", 0)) / tot, 4),
                                    "praise": v.get("praise") or [], "issues": v.get("issues") or [], "ref": r["id"]}
    if not lines:
        return {"available": False, "reason": "no review summary by product line in the brain", "rows": [], "lines": []}
    med = _median([l["neg_share"] for l in lines.values()])
    # which lines each avatar buys: its own reviews, then reviews linked to its doubts
    buys: dict[str, dict[str, int]] = {}
    for rec in avatar_records:
        for rv in ((rec.get("value") or {}).get("reviews") or []) if isinstance(rec.get("value"), dict) else []:
            if rv.get("line") in lines:
                buys.setdefault(rec["id"], {}).setdefault(rv["line"], 0)
                buys[rec["id"]][rv["line"]] += 1
    phrase_lines = {}
    for rec in lang_records:
        for rv in ((rec.get("value") or {}).get("reviews") or []):
            if rv.get("line") in lines:
                phrase_lines.setdefault(rec["id"], set()).add(rv["line"])
    for rg in all_rungs:
        ls = set().union(*[phrase_lines.get(p, set()) for p in rg["derived_from"]]) if rg["derived_from"] else set()
        for aid in rg["avatars"]:
            for ln in ls:
                buys.setdefault(aid, {}).setdefault(ln, 0)
                buys[aid][ln] += 1
    rows = []
    for a in avatars:
        need = _content(" ".join([a.get("job") or "", *a.get("pains", []), *a.get("triggers", [])]))
        for ln, n in sorted((buys.get(a["id"]) or {}).items(), key=lambda kv: (-kv[1], kv[0])):
            L = lines[ln]
            hit = [i for i in L["issues"] if _content(i) & need]
            if not hit or n < MIN_LINKS or L["neg_share"] < (med or 0):
                continue
            kind = _issue_kind(hit[0])
            art, cap, label = KIND_ACTION[kind]
            owner = "person" if art == "ticket" else "agent_drafts"
            why = (f"{a['name']} buys {ln.replace('_', ' ')} to get {a.get('job') or 'its job done'}. "
                   f"{round(L['neg_share'] * 100, 1)} percent of its {L['reviews']:,} reviews are 1 or 2 star against a {round(med * 100, 1)} percent median. "
                   f"Top complaint: {hit[0]}.")
            rows.append({"avatar": a["name"], "avatar_key": a["key"], "line": ln, "links": n, "neg_share": L["neg_share"], "median": med,
                         "hits": hit, "kind": kind, "why": why,
                         "action": {"id": f"{SCREEN}.misread.{a['key']}.{ln}", "kind": art, "owner": owner,
                                    "title": f"Fix what {ln.replace('_', ' ')} promises {a['name']}: {hit[0]}",
                                    "capability": {"id": cap[0], "autonomy": cap[1]},
                                    "draft": "\n".join([f"DRAFT: {label}", f"Line: {L['product'] or ln} ({L['pdp'] or 'no page on file'})",
                                                        f"Avatar: {a['name']}. Job: {a.get('job') or 'unavailable'}",
                                                        f"Complaints that hit the job: {'; '.join(hit)}",
                                                        f"Praise to keep: {'; '.join(L['praise']) or 'none on file'}",
                                                        f"1 and 2 star share: {round(L['neg_share'] * 100, 1)} percent, median {round(med * 100, 1)} percent"]),
                                    "steps": ([{"n": 1, "who": "agent", "text": "Pull 20 one and two star reviews for the line that name the complaint."},
                                               {"n": 2, "who": "person", "text": "Send the ticket to the product team with the batch and size data."},
                                               {"n": 3, "who": "agent", "text": "Add an honest line on the page until the fix ships."},
                                               {"n": 4, "who": "agent", "text": "Recount the complaint on the next review pull."}] if art == "ticket" else
                                              [{"n": 1, "who": "agent", "text": "Pull the reviews that name the complaint and the praise to keep."},
                                               {"n": 2, "who": "agent", "text": f"Draft {label}."},
                                               {"n": 3, "who": "person", "text": "Approve and ship it on the product page."},
                                               {"n": 4, "who": "agent", "text": "Recount the complaint and the line's 1 and 2 star share next pull."}])}})
    rows.sort(key=lambda r: (-r["neg_share"], -r["links"], r["avatar"]))
    table = []
    for L in sorted(lines.values(), key=lambda l: -l["neg_share"]):
        polar = sorted(set().union(*[_content(p) for p in L["praise"]]) & set().union(*[_content(i) for i in L["issues"]])) if L["praise"] and L["issues"] else []
        verdict = "problem" if med and L["neg_share"] >= LINE_PROBLEM * med else ("split" if polar else "fine")
        act = None
        if verdict == "split":
            act = {"id": f"{SCREEN}.split.{L['line']}", "kind": "copy", "owner": "agent_drafts",
                   "title": f"Set the expectation on {', '.join(polar)} for {L['line'].replace('_', ' ')}",
                   "capability": {"id": "CREA-C24", "autonomy": "agent_does"},
                   "draft": "\n".join([f"DRAFT: expectation copy for {L['product'] or L['line']}",
                                       f"Same trait, two reactions: praise says {'; '.join(L['praise'])}. Complaints say {'; '.join(L['issues'])}.",
                                       f"Say plainly who it suits and who it does not, on {', '.join(polar)}.",
                                       "Place: product page near the size picker, and the first line of retargeting ads."]),
                   "steps": [{"n": 1, "who": "agent", "text": "Pull the praise and complaint lines that share the trait."},
                             {"n": 2, "who": "agent", "text": "Draft 2 lines: who it suits, who it does not."},
                             {"n": 3, "who": "person", "text": "Approve and ship on the product page."},
                             {"n": 4, "who": "agent", "text": "Recount the complaint share on the next pull."}]}
        table.append(dict(L, ratio=round(L["neg_share"] / med, 2) if med else None, polar=polar, verdict=verdict, action=act,
                          avatars=sorted({r["avatar"] for r in rows if r["line"] == L["line"]})))
    return {"available": True, "rows": rows, "lines": table, "median": med,
            "line": (f"{len(rows)} avatar and line pairs where the complaints hit the job the avatar hires us for."
                     if rows else "No line fails the job its avatars buy it for.")}


# ---------------------------------------------------------------- theme impact: which themes cost the most stars

THEME_MIN = 8             # a theme needs 8 or more rated reviews in the sample
RISING_DAYS = 90          # recent window for a rising theme
RISING_RATIO = 1.5        # recent share 1.5x the earlier share or more
RISING_MIN = 5            # with 5 or more recent reviews on the theme


def _ladder_for(theme: str, ladders_rows: list[dict]) -> list[dict]:
    toks = {t for t in theme.split("_") if t not in ("and", "of")}
    return [r for r in ladders_rows if toks & set(r["theme"].split("_"))]


def theme_impact(lang_records: list[dict], ladders_rows: list[dict], as_of: str) -> dict:
    """Impact of each review theme on stars: share of rated reviews x (average with it - average without it).

    From the rated reviews behind the language bank, a public sample, so read it as a ranking, not a forecast.
    """
    import datetime as _dt
    rated = []
    for rec in lang_records:
        v = rec.get("value") if isinstance(rec.get("value"), dict) else {}
        themes = [t for t in (v.get("themes") or []) if t != "general"]
        for rv in v.get("reviews") or []:
            if isinstance(rv.get("star"), int):
                rated.append({"star": rv["star"], "themes": themes, "date": str(rv.get("date") or "")[:10], "id": rec["id"]})
    if len(rated) < THEME_MIN * 2:
        return {"available": False, "reason": f"only {len(rated)} rated reviews in the brain", "rows": []}
    cut = (_dt.date.fromisoformat(as_of) - _dt.timedelta(days=RISING_DAYS)).isoformat()
    recent = [r for r in rated if r["date"] > cut]
    older = [r for r in rated if r["date"] and r["date"] <= cut]
    rows = []
    for t in sorted({t for r in rated for t in r["themes"]}):
        w = [r["star"] for r in rated if t in r["themes"]]
        wo = [r["star"] for r in rated if t not in r["themes"]]
        if len(w) < THEME_MIN or not wo:
            continue
        share = len(w) / len(rated)
        gap = sum(w) / len(w) - sum(wo) / len(wo)
        rs = sum(1 for r in recent if t in r["themes"])
        rec_share = rs / len(recent) if recent else None
        old_share = sum(1 for r in older if t in r["themes"]) / len(older) if older else None
        rising = bool(rec_share and old_share and rs >= RISING_MIN and rec_share >= RISING_RATIO * old_share)
        lads = _ladder_for(t, ladders_rows)
        order = ("answer", "not_landing") if gap < 0 else ("lead",)
        move = next((r["action"] for v in order for r in lads if r["verdict"] == v and r["action"]), None)
        rows.append({"theme": t, "reviews": len(w), "share": round(share, 4), "avg_with": round(sum(w) / len(w), 2),
                     "avg_without": round(sum(wo) / len(wo), 2), "star_gap": round(gap, 2), "impact": round(share * gap, 3),
                     "recent_share": round(rec_share, 4) if rec_share is not None else None,
                     "older_share": round(old_share, 4) if old_share is not None else None, "rising": rising,
                     "ladders": sorted({r["theme"] for r in lads}), "action": move})
    rows.sort(key=lambda r: (r["impact"], r["theme"]))
    worst = [r for r in rows if r["impact"] < 0]
    return {"available": True, "rows": rows, "rated": len(rated), "recent": len(recent),
            "line": (f"{worst[0]['theme'].replace('_', ' ').capitalize()} costs the most: in {round(worst[0]['share'] * 100)} percent of rated reviews, "
                     f"{abs(worst[0]['star_gap'])} stars below the rest." if worst else "No theme pulls stars down.")}


# ---------------------------------------------------------------- copy gap: their words against ours

OUR_SOURCES = ("site", "founder")
GAP_TOP = 20


def _norm(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", str(text or "").lower()))


def _record_text(r: dict) -> str:
    parts = [r.get("text") or ""]
    v = r.get("value")
    if isinstance(v, str):
        parts.append(v)
    elif isinstance(v, (list, dict)):
        parts.append(" ".join(str(x) for x in (v.values() if isinstance(v, dict) else v) if isinstance(x, str)))
    parts += [e.get("quote") or "" for e in r.get("evidence") or [] if isinstance(e, dict)]
    return " ".join(parts)


GAP_MIN_DOCS = 3           # a word counts once 3 or more distinct praise reviews use it
GAP_EXTRA_STOP = {"really", "just", "much", "well", "also", "even", "wear", "wore", "worn", "bought", "purchase", "purchased",
                  "love", "loves", "great", "good", "comfortable", "comfy", "quality", "price", "recommend", "definitely",
                  "would", "could", "because", "these", "those", "there", "what", "when", "which", "while", "about", "other",
                  "brand", "brands", "product", "products", "item", "items", "order", "ordered", "time", "times", "feet", "foot",
                  "were", "your", "down", "made", "show", "long", "very", "best", "many", "still", "since", "first", "every",
                  "most", "been", "being", "didn", "doesn", "dont", "don", "wasn", "isn", "can", "get", "got", "make", "need", "want"}


def _lemma(w: str) -> str:
    for suf in ("ing", "ed", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


def _lemmas(text: str, brand_tokens: set[str]) -> set[str]:
    out = set()
    for w in re.findall(r"[a-z]+", str(text or "").lower()):
        if len(w) < 4 or w in STOP or w in GENERIC or w in GAP_EXTRA_STOP or w in brand_tokens or \
                any(len(b) >= 5 and w.startswith(b[:5]) for b in brand_tokens):
            continue
        out.add(_lemma(w))
    return out


def _surface(text: str) -> dict[str, str]:
    """lemma to the first plain word it came from, for display."""
    out = {}
    for w in re.findall(r"[a-z]+", str(text or "").lower()):
        out.setdefault(_lemma(w), w)
    return out


def copy_gap(sections: dict[str, list[dict]], lang_records: list[dict], brand_tokens: set[str], source_name) -> dict:
    """Words buyers use when they praise us, checked against every site and founder record in the brain."""
    ours = [r for recs in sections.values() for r in recs if (r.get("source") or {}).get("type") in OUR_SOURCES]
    if not ours:
        return {"available": False, "reason": "no site or founder records in the brain to compare with", "rows": []}
    our_words = _lemmas(" ".join(_record_text(r) for r in ours), brand_tokens)
    docs: dict[str, list[dict]] = {}
    n_docs = 0
    for rec in lang_records:
        p = phrase_row(rec, source_name)
        if not p or p["side"] != "win" or p["language_only"]:
            continue
        v = rec.get("value") or {}
        for i, rv in enumerate(v.get("reviews") or [{}]):
            text = " ".join([v.get("phrase") or "", rv.get("quote") or ""])
            n_docs += 1
            toks = re.findall(r"[A-Za-z']+", text)
            for lm in _lemmas(text, brand_tokens):
                at = next((i for i, t in enumerate(toks) if _lemma(t.lower().strip("'")) == lm), 0)
                snip = " ".join(toks[max(0, at - 4): at + 5])
                docs.setdefault(lm, []).append({"id": rec["id"], "phrase": snip, "source": p["source"]})
    rows = []
    for lm, ds in docs.items():
        ids = {d["id"] for d in ds}
        if len(ids) < GAP_MIN_DOCS:
            continue
        ex = []
        for d in sorted(ds, key=lambda d: (len(d["phrase"]), d["id"])):
            if d["phrase"] not in ex:
                ex.append(d["phrase"])
            if len(ex) == 2:
                break
        rows.append({"word": lm, "reviews": len(ids), "share": round(len(ids) / n_docs, 4) if n_docs else None,
                     "verdict": "used" if lm in our_words else "missing", "examples": ex,
                     "sources": sorted({d["source"] for d in ds})})
    rows.sort(key=lambda r: ({"missing": 0, "used": 1}[r["verdict"]], -r["reviews"], r["word"]))
    top = sorted(rows, key=lambda r: (-r["reviews"], r["word"]))[:GAP_TOP]
    top.sort(key=lambda r: ({"missing": 0, "used": 1}[r["verdict"]], -r["reviews"], r["word"]))
    missing = [r for r in top if r["verdict"] == "missing"]
    action = None
    if missing:
        pick = missing[:5]
        action = {"id": f"{SCREEN}.copygap", "kind": "page_section", "owner": "agent_drafts",
                  "title": f"Use {len(pick)} words buyers praise us with and we never say",
                  "capability": {"id": "BRAND-C14", "autonomy": "agent_does"},
                  "draft": "\n".join(["DRAFT: buyer words to put on the page",
                                      *[f"- {r['word']} ({r['reviews']} praise reviews), like \"{r['examples'][0]}\"" for r in pick],
                                      "Where: product page bullets, the homepage hero sub-line, the first line of 2 ads.",
                                      "Rule: use their words as written. Keep claims inside what the brain allows."]),
                  "steps": [{"n": 1, "who": "agent", "text": "Match each word to the product and page where buyers said it."},
                            {"n": 2, "who": "agent", "text": "Draft the page bullets and 2 ad first lines."},
                            {"n": 3, "who": "person", "text": "Approve and ship on the page."},
                            {"n": 4, "who": "agent", "text": "Mark the words as used so reuse can be counted."}]}
    used = sum(1 for r in top if r["verdict"] == "used")
    return {"available": True, "rows": top, "our_records": len(ours), "praise_reviews": n_docs, "missing": len(missing), "used": used,
            "action": action,
            "line": f"Of the {len(top)} words buyers use most when they praise us, {len(missing)} never appear in our site and founder records."}


# ---------------------------------------------------------------- avatar evidence gate

GATE_QUOTES = 5
GATE = [  # key, label, core (needed to leave provisional), task
    ("job", "Job stated", True, ("agent", "research_note", "BRAND-C01", "Write the job from the avatar's quotes in one line.")),
    ("quotes", f"{GATE_QUOTES}+ quotes", True, ("agent", "research_note", "BRAND-C01", f"Pull quotes until the avatar has {GATE_QUOTES}, with links.")),
    ("sources", "2+ sources", True, ("agent", "research_note", "BRAND-C01", "Find the same pattern in a second independent source.")),
    ("share", "Share known", True, ("person", "research_note", "LIFE-C29", "Ask buyers in the post-purchase survey which situation fits them.")),
    ("doubt", "Doubt mapped", True, ("agent", "brain_record", "BRAND-C13", "Link the avatar to the ladder rungs its quotes raise.")),
    ("proof", "Top doubt proven", False, ("agent_drafts", "copy", "BRAND-C13", "Answer the top doubt with a proof record.")),
    ("moments", "2+ moments", False, ("agent", "brain_record", "BRAND-C01", "Add the moments that start a purchase, from the quotes.")),
    ("pains", "2+ pains", False, ("agent", "brain_record", "BRAND-C01", "Add the pains in the buyers' words.")),
    ("fresh", "Checked in time", False, ("agent", "brain_record", "BRAND-C15", "Re-check the avatar against the newest reviews.")),
]


def gate(avatars: list[dict], all_rungs: list[dict]) -> dict:
    """A checklist per avatar. It stays provisional until every core check passes; each failed check is a task."""
    rows = []
    for a in avatars:
        mine = [r for r in all_rungs if a["id"] in r["avatars"]]
        top = a.get("top_objection")
        checks = {"job": bool(a.get("job")), "quotes": a["quote_count"] >= GATE_QUOTES, "sources": len(a["sources"]) >= 2,
                  "share": a["share_estimate"] is not None, "doubt": bool(mine), "proof": bool(top and top["proof"]),
                  "moments": len(a.get("triggers") or []) >= 2, "pains": len(a.get("pains") or []) >= 2, "fresh": not a["expired"]}
        core = all(checks[k] for k, _, c, _ in GATE if c)
        tasks = []
        for k, label, c, (owner, kind, cap, text) in GATE:
            if checks[k]:
                continue
            tasks.append({"id": f"{SCREEN}.gate.{a['key']}.{k}", "check": k, "label": label, "core": c, "owner": owner, "kind": kind,
                          "title": f"{a['name']}: {text[0].lower() + text[1:].rstrip('.')}",
                          "capability": {"id": cap, "autonomy": {"agent": "agent_does", "agent_drafts": "founder_gate", "person": "human_assist"}[owner]},
                          "draft": f"DRAFT task for {a['name']}\nCheck failing: {label}\nHave: {a['quote_count']} quotes from {', '.join(a['sources']) or 'no source'}\nDo: {text}",
                          "steps": [{"n": 1, "who": "agent" if owner != "person" else "person", "text": text},
                                    {"n": 2, "who": "agent", "text": "Write the result into the avatar record as a draft."},
                                    {"n": 3, "who": "person", "text": "Approve the record. The gate re-checks itself."}]})
        rows.append({"key": a["key"], "name": a["name"], "checks": checks, "passed": sum(checks.values()), "total": len(checks),
                     "status": "validated" if core else "provisional", "tasks": tasks})
    rows.sort(key=lambda r: (r["status"] == "validated", r["passed"], r["name"]))
    val = sum(1 for r in rows if r["status"] == "validated")
    return {"rows": rows, "checks": [{"key": k, "label": l, "core": c} for k, l, c, _ in GATE], "validated": val,
            "tasks": sum(len(r["tasks"]) for r in rows),
            "line": f"{val} of {len(rows)} avatars pass every core check. The rest stay provisional: brief them, but do not bet a launch on them."}


# ---------------------------------------------------------------- hook bank: phrases buyers repeat

HOOK_MIN = 3        # distinct 4 and 5 star reviews
HOOK_TOP = 15
HOOK_FILL = {"a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "is", "are", "it", "i", "my", "they", "these", "this",
             "so", "very", "with", "but", "that", "was", "be", "as", "at", "have", "has", "me", "you", "we", "just", "them", "their",
             "not", "do", "does", "did", "all"}


def hooks(lang_records: list[dict], all_rungs: list[dict], avatars: list[dict], brand_tokens: set[str], source_name) -> dict:
    """2 to 4 word phrases found in 3 or more distinct 4 and 5 star reviews, with the avatars whose doubts they sit on."""
    avatar_of = {}
    names = {a["id"]: a["name"] for a in avatars}
    for r in all_rungs:
        for pid in r["derived_from"]:
            avatar_of.setdefault(pid, set()).update(names[x] for x in r["avatars"] if x in names)
    grams: dict[str, dict] = {}
    n = 0
    for rec in lang_records:
        v = rec.get("value") if isinstance(rec.get("value"), dict) else {}
        for rv in v.get("reviews") or []:
            star = rv.get("star")
            if not isinstance(star, int) or star < 4 or source_name(rv.get("source") or "") == "Reddit":
                continue
            n += 1
            toks = re.findall(r"[a-z']+", " ".join([v.get("phrase") or "", rv.get("quote") or ""]).lower().replace("’", "'"))
            seen = set()
            for k in (2, 3, 4):
                for i in range(len(toks) - k + 1):
                    g = toks[i:i + k]
                    if g[0] in HOOK_FILL or g[-1] in HOOK_FILL:
                        continue
                    content = [t for t in g if t not in HOOK_FILL and t not in GENERIC and t not in brand_tokens and len(t) >= 3]
                    if not content or any(len(b) >= 5 and t.startswith(b[:5]) for t in g for b in brand_tokens):
                        continue
                    key = " ".join(g)
                    if key in seen:
                        continue
                    seen.add(key)
                    e = grams.setdefault(key, {"hook": key, "ids": set(), "avatars": {}})
                    e["ids"].add(rec["id"])
                    for nm in avatar_of.get(rec["id"], set()):
                        e["avatars"][nm] = e["avatars"].get(nm, 0) + 1
    rows = [g for g in grams.values() if len(g["ids"]) >= HOOK_MIN]
    # keep the longest phrase when a shorter one only appears inside it
    rows.sort(key=lambda g: (-len(g["ids"]), -len(g["hook"]), g["hook"]))
    kept = []
    for g in rows:
        if any(g["hook"] in k["hook"] and len(k["ids"]) >= len(g["ids"]) for k in kept):
            continue
        kept.append(g)
    kept = kept[:HOOK_TOP]
    out = [{"hook": g["hook"], "reviews": len(g["ids"]),
            "avatars": [k for k, _ in sorted(g["avatars"].items(), key=lambda kv: (-kv[1], kv[0]))[:3]]} for g in kept]
    brief = {"id": f"{SCREEN}.hooks", "kind": "ad_brief", "owner": "agent_drafts", "title": "Ad brief from the hooks buyers repeat",
             "capability": {"id": "CREA-C04", "autonomy": "agent_does"},
             "head": ["AD BRIEF: hooks in the buyers' own words", "Rule: open on the hook as written. One hook per variant.",
                      "Formats: static first frame and a 6-second video open."],
             "steps": [{"n": 1, "who": "agent", "text": "Write one first line and one first frame per picked hook."},
                       {"n": 2, "who": "person", "text": "Approve the variants. Creative makes them."},
                       {"n": 3, "who": "agent", "text": "Tag each ad with its hook and read cost per order after 7 days."}]}
    return {"rows": out, "praise_reviews": n, "brief": brief,
            "line": f"{len(out)} phrases repeat across 3 or more praise reviews. Each is a tested opening line, written by buyers."}


# ---------------------------------------------------------------- four forces per avatar (Moesta)

FORCES = {
    "push": r"\b(tired of|sick of|fall(s|ing)? down|slide(s)? down|holes? in (my|the) old|my old|other brands?|used to wear|kept|always had)\b",
    "pull": r"\b(finally|stay(s)? (up|in place|put)|worth|best|favorite|soft|comfort|love|switch(ed)? to|no more)\b",
    "anxiety": r"\b(expensive|overpriced|price|pricey|worried|not sure|hesitant|risk|fake|counterfeit|will (they|it)|scam|sizing|too (small|big|tight))\b",
    "habit": r"\b(cheap(er)?|multi-?packs?|store brand|walmart|costco|target|amazon basics|used to buy|always bought)\b",
}
FORCE_MIN = 1                 # every force needs at least 1 line
TENSION_SHARE = 0.15          # anxiety plus habit under 15 percent of coded lines: we know why they like us, not what holds them back


def forces(avatars: list[dict], all_rungs: list[dict], lang_records: list[dict], competitor_names: list[str]) -> dict:
    """Code every line tied to an avatar as push, pull, anxiety or habit, from word patterns. Competitor names count as habit."""
    by_id = {r["id"]: r for r in lang_records}
    comp = [re.escape(n.lower()) for n in competitor_names if n]
    habit = FORCES["habit"] if not comp else FORCES["habit"][:-3] + "|" + "|".join(comp) + r")\b"
    pats = dict(FORCES, habit=habit)
    rows = []
    for a in avatars:
        lines = [q["quote"] for q in a["quotes"] if q["source"] != "Reddit"]
        for r in all_rungs:
            if a["id"] not in r["avatars"]:
                continue
            for pid in r["derived_from"]:
                rec = by_id.get(pid)
                v = (rec or {}).get("value") if isinstance((rec or {}).get("value"), dict) else {}
                for rv in v.get("reviews") or []:
                    if rv.get("quote") and rv.get("source") != "reddit":
                        lines.append(rv["quote"])
        lines = list(dict.fromkeys(lines))
        coded = {k: [] for k in pats}
        for ln in lines:
            low = ln.lower().replace("’", "'")
            for k, p in pats.items():
                if re.search(p, low):
                    coded[k].append(ln)
        total = sum(len(v) for v in coded.values())
        tension = (len(coded["anxiety"]) + len(coded["habit"])) / total if total else None
        missing = [k for k, v in coded.items() if len(v) < FORCE_MIN]
        under = bool(missing) or (tension is not None and tension < TENSION_SHARE) or not total
        action = None
        if under:
            qs = {"push": "What was going wrong with the socks you had before?", "pull": "What made you pick us that day?",
                  "anxiety": "What almost stopped you from buying?", "habit": "What did you buy before, and why did you stick with it?"}
            ask = missing or ["anxiety", "habit"]
            action = {"id": f"{SCREEN}.forces.{a['key']}", "kind": "research_note", "owner": "person",
                      "title": f"Run 5 switch interviews with {a['name']} buyers",
                      "capability": {"id": "BRAND-C05", "autonomy": "human_assist"},
                      "draft": "\n".join([f"DRAFT interview script: {a['name']}", "Who: 5 buyers from the last 90 days who fit this avatar",
                                          f"Forces with too few lines: {', '.join(ask)}", *[f"- {qs[k]}" for k in ask],
                                          "- Walk me through the day you bought. What happened first?",
                                          "Output: quotes coded by force, written back to the avatar record"]),
                      "steps": [{"n": 1, "who": "agent", "text": "Pick 20 recent buyers who fit the avatar and draft the invite."},
                                {"n": 2, "who": "person", "text": "Run 5 calls of 20 minutes with the script."},
                                {"n": 3, "who": "agent", "text": "Code the notes by force and write the quotes to the avatar record."},
                                {"n": 4, "who": "person", "text": "Approve the record update."}]}
        rows.append({"key": a["key"], "name": a["name"], "lines": len(lines),
                     "forces": {k: {"n": len(v), "example": _clip(v[0]) if v else None} for k, v in coded.items()},
                     "tension": round(tension, 4) if tension is not None else None, "under": under, "missing": missing, "action": action})
    rows.sort(key=lambda r: (not r["under"], -(r["lines"]), r["name"]))
    n_under = sum(1 for r in rows if r["under"])
    return {"rows": rows, "under": n_under,
            "line": f"{n_under} of {len(rows)} avatars lack lines on at least one force, or know why buyers like us but not what holds them back."}


# ---------------------------------------------------------------- draft a new avatar from a gap

DRAFT_QUOTES = 5


def draft_avatar(brand: str, segment: str, lang_records: list[dict], competitors: list[str], today: str, source_name) -> dict | None:
    """An avatar record drafted from the brain for an unserved situation. Tier inferred: a hypothesis, never a fact."""
    pat = SITUATIONS.get(segment)
    if not pat:
        return None
    quotes, by_source, ids = [], {}, []
    for rec in lang_records:
        v = rec.get("value") if isinstance(rec.get("value"), dict) else {}
        for rv in v.get("reviews") or [{}]:
            text = " ".join([v.get("phrase") or "", rv.get("quote") or ""])
            if not _hits(text, pat):
                continue
            src = source_name(rv.get("source") or ("reddit" if v.get("subreddit") else ""))
            by_source[src] = by_source.get(src, 0) + 1
            ids.append(rec["id"])
            if src != "Reddit" and rv.get("quote") and len(quotes) < DRAFT_QUOTES:
                quotes.append({"quote": _clip(rv["quote"]) if len(rv["quote"].split()) > MAX_WORDS * 2 else rv["quote"], "ref": rv.get("url") or ""})
    key = "situation_" + segment.replace(" ", "_")
    name = segment.capitalize() + " buyer"
    words = sorted({m.group(0) for rec in lang_records for m in [re.search(pat + r"[a-z]*", _record_text(rec).lower())] if m})
    rec = {"id": f"{brand}.avatars.{key}", "brand": brand, "section": "avatars", "field": "avatar",
           "value": {"name": name, "share_estimate": None, "intensity": None, "job": None,
                     "triggers": [f"a {segment} moment named in reviews: {', '.join(words[:4])}"] if words else [],
                     "pains": [], "emotional_driver": None, "inferred": True, "count_in_sample": sum(by_source.values()),
                     "count_by_source": {k.lower().replace(" ", "_"): n for k, n in sorted(by_source.items())},
                     "competitors_serving": competitors},
           "text": f"{name}: drafted from {sum(by_source.values())} mentions in the language bank; job unknown until buyers are asked.",
           "source": {"type": "agent", "ref": "02-customers-avatars avatar draft", "captured_at": today,
                      "derived_from": sorted(set(ids))[:40] or [f"{brand}.competitors"]},
           "confidence": 0.3, "tier": "inferred", "status": "active", "visibility": "private",
           "evidence": [q for q in quotes if q["ref"].startswith("http")],
           "notes": "Drafted by the Customers and avatars screen from a category gap. A hypothesis until 5 quotes from 2 sources and a survey share exist."}
    return {"segment": segment, "record": rec, "mentions": sum(by_source.values()), "by_source": by_source, "quotes": len(rec["evidence"])}


# ---------------------------------------------------------------- avatar moments calendar

# US moments by month (app/CLAUDE.md: US holidays by default). pattern -> (label, month, day the moment starts)
US_MOMENTS = [(r"\bchristmas|\bholiday", "Holiday gifting", 12, 1), (r"\bwinter|\bcold", "Winter", 11, 15),
              (r"\bvalentine", "Valentine's Day", 2, 1), (r"\bmother", "Mother's Day", 5, 1), (r"\bfather", "Father's Day", 6, 1),
              (r"\bback to school|\bschool", "Back to school", 8, 1), (r"\bsummer|\bheat", "Summer", 6, 1),
              (r"\bmarathon|\brace\b", "Fall race season", 9, 15), (r"\bnew year|\bresolution", "New Year", 1, 1)]
LEAD_DAYS = {"ad": 21, "email": 14}
HORIZON_MONTHS = 6


def moments(avatars: list[dict], monthly: list[dict], as_of: str) -> dict:
    """Upcoming moments named in avatar triggers, when each starts, what ships before it, and last year's sales index."""
    import datetime as _dt
    today = _dt.date.fromisoformat(as_of)
    sales = {r["month"]: r.get("net_sales") for r in monthly if r.get("net_sales") and r.get("days") and r["days"] >= 28}
    last12 = [sales[m] for m in sorted(sales)[-12:]]
    avg = sum(last12) / len(last12) if last12 else None
    found: dict[str, dict] = {}
    for a in avatars:
        text = " ".join(a.get("triggers") or []).lower()
        for pat, label, mon, day in US_MOMENTS:
            if re.search(pat, text):
                f = found.setdefault(label, {"label": label, "month": mon, "day": day, "avatars": []})
                if a["name"] not in f["avatars"]:
                    f["avatars"].append(a["name"])
    rows = []
    for f in found.values():
        yr = today.year if (f["month"], f["day"]) >= (today.month, today.day) else today.year + 1
        start = _dt.date(yr, f["month"], f["day"])
        months_out = (start.year - today.year) * 12 + start.month - today.month
        if months_out > HORIZON_MONTHS:
            continue
        ly = f"{yr - 1}-{f['month']:02d}"
        idx = round(sales[ly] / avg, 2) if avg and ly in sales else None
        ad_by, mail_by = start - _dt.timedelta(days=LEAD_DAYS["ad"]), start - _dt.timedelta(days=LEAD_DAYS["email"])
        late = ad_by < today
        rows.append({"label": f["label"], "starts": start.isoformat(), "avatars": f["avatars"], "sales_index_last_year": idx,
                     "ad_by": ad_by.isoformat(), "email_by": mail_by.isoformat(), "late": late,
                     "action": {"id": f"{SCREEN}.moment.{f['label'].lower().replace(' ', '_').replace(chr(39), '')}", "kind": "report",
                                "owner": "agent_drafts", "title": f"{f['label']} plan for {', '.join(f['avatars'][:2])}",
                                "capability": {"id": "LIFE-C20", "autonomy": "agent_does"},
                                "draft": "\n".join([f"DRAFT {f['label']} plan", f"Starts: {start.isoformat()}",
                                                    f"Ads live by: {ad_by.isoformat()}. Emails scheduled by: {mail_by.isoformat()}.",
                                                    f"Avatars: {', '.join(f['avatars'])}",
                                                    f"Last year this month sold at {idx}x the monthly average." if idx else "Last year's index: unavailable",
                                                    "Ships: 1 ad brief per avatar from its next build, 2 emails, the gift or pack offer if the brain has one."]),
                                "steps": [{"n": 1, "who": "agent", "text": "Pull each avatar's next build and last year's best sellers that month."},
                                          {"n": 2, "who": "agent", "text": "Draft the ad briefs and 2 emails with the dates above."},
                                          {"n": 3, "who": "person", "text": "Approve the plan and put it on the calendar."},
                                          {"n": 4, "who": "agent", "text": "Check ads are live on the ad date. Flag if not."}],
                                "check_on": ad_by.isoformat()}})
    rows.sort(key=lambda r: r["starts"])
    nxt = rows[0] if rows else None
    return {"rows": rows, "as_of": as_of,
            "line": (f"Next: {nxt['label']} starts {nxt['starts']}. Ads need to be live by {nxt['ad_by']}." if nxt else
                     "No avatar names a moment in the next 6 months.")}


# ---------------------------------------------------------------- post-purchase survey from the gaps

SURVEY_N = 385            # answers for a share within 5 points at 95 percent confidence
RESPONSE_RATE = 0.15      # assumed post-purchase survey response rate; replace with the brand's own once it runs
MAX_OPEN_RUNGS = 4


def survey(gate_rows: list[dict], ladders_rows: list[dict], forces_rows: list[dict], segments: list[dict],
           orders_per_day: float | None) -> dict:
    """A post-purchase survey whose every question closes a named gap on this screen."""
    qs = []
    options = [r["name"] for r in gate_rows if "(Reddit)" not in r["name"]] + \
              [s["segment"].capitalize() + " buyer" for s in segments if s["verdict"] in ("gap", "watch")]
    no_share = [r["name"] for r in gate_rows if not r["checks"]["share"] and "(Reddit)" not in r["name"]]
    qs.append({"q": "Which of these sounds most like you?", "type": "single choice", "options": options + ["None of these"],
               "closes": f"share for {len(no_share)} avatars with no share, and sizes the unserved situations",
               "gap_ids": [f"{SCREEN}.gate.{r['key']}.share" for r in gate_rows if not r["checks"]["share"]]})
    open_r = [r for r in ladders_rows if r["verdict"] == "answer"][:MAX_OPEN_RUNGS]
    if open_r:
        qs.append({"q": "What almost stopped you from buying?", "type": "multiple choice",
                   "options": [r["doubt"][:1].upper() + r["doubt"][1:] for r in open_r] + ["Nothing", "Something else"],
                   "closes": f"how common the {len(open_r)} doubts with no proof are among buyers, not only reviewers",
                   "gap_ids": [f"{SCREEN}.rung.{r['id']}" for r in open_r]})
    thin = [r for r in forces_rows if "push" in r["missing"] or "habit" in r["missing"]]
    if thin:
        qs.append({"q": "What did you buy before, and what made you switch?", "type": "open text", "options": [],
                   "closes": f"push and habit lines for {len(thin)} avatars", "gap_ids": [f"{SCREEN}.forces.{r['key']}" for r in thin]})
    qs.append({"q": "How did you first hear about us?", "type": "single choice with other",
               "options": ["Instagram or Facebook", "TikTok", "Google search", "A friend", "A store", "Amazon", "Podcast or creator", "Other"],
               "closes": "channel read to set against platform attribution", "gap_ids": []})
    qs.append({"q": "Who is this order for?", "type": "single choice", "options": ["Me", "A gift", "My family"],
               "closes": "gift share by month, for the gift avatar and weak holiday cohorts", "gap_ids": []})
    days = round(SURVEY_N / (orders_per_day * RESPONSE_RATE), 1) if orders_per_day else None
    draft = ["DRAFT post-purchase survey", f"Goal: {SURVEY_N} answers, a share within 5 points.",
             f"Days to get there: {days} at {int(RESPONSE_RATE * 100)} percent response" if days else "Days to get there: unavailable, order volume unknown",
             "Before launch: a person rewrites each avatar option in plain buyer words.", ""]
    for i, q in enumerate(qs, 1):
        draft.append(f"{i}. {q['q']} ({q['type']})")
        draft += [f"   - {o}" for o in q["options"]]
        draft.append(f"   Closes: {q['closes']}")
    action = {"id": f"{SCREEN}.survey", "kind": "research_note", "owner": "agent_drafts",
              "title": f"Run a {len(qs)}-question post-purchase survey that closes {sum(len(q['gap_ids']) for q in qs)} gaps",
              "capability": {"id": "LIFE-C50", "autonomy": "founder_gate"}, "draft": "\n".join(draft),
              "steps": [{"n": 1, "who": "agent", "text": "Draft the survey in the post-purchase survey tool's format."},
                        {"n": 2, "who": "person", "text": "Approve the questions and switch it on for the order page."},
                        {"n": 3, "who": "agent", "text": f"After {SURVEY_N} answers, write shares and quotes into the avatar records as drafts."},
                        {"n": 4, "who": "person", "text": "Approve the record updates. The gate and the map re-check."}]}
    return {"questions": qs, "days": days, "orders_per_day": round(orders_per_day) if orders_per_day else None,
            "target": SURVEY_N, "response_rate": RESPONSE_RATE, "action": action,
            "line": f"{len(qs)} questions close {sum(len(q['gap_ids']) for q in qs)} named gaps." +
                    (f" At {int(RESPONSE_RATE * 100)} percent response it takes {days} days to get {SURVEY_N} answers." if days else "")}


# ---------------------------------------------------------------- order-level rules (aggregate customer_paths)

GATEWAY_HI = 1.3          # a first product whose 180-day repeat is 1.3x the median first product or more
DEAD_END = 0.7            # 0.7x or less
GATEWAY_MIN_BUYERS = 100
NEXT_SHARE = 0.15         # the most common second product, shown at 15 percent or more of repeaters
NEXT_MIN = 50
DUE_X, WINBACK_X, LAPSED_X = 1.0, 1.5, 3.0
CHURN_MOVE = 0.20         # churning high-value cell up 20 percent or more on the prior period
PATHS_SHAPE = ('aggregates/customer_paths.json rows: {kind: "first_product", sku_group, first_buyers, repeat_180d, value_180d, '
               'next: [{sku_group, share, median_days}]}; {kind: "order_gap", group, median_days, n}; '
               '{kind: "rfm", frequency ("1", "2", "3+"), recency ("0-90", "91-364", "365+"), customers, prior_customers, revenue_share}')


def paths(rows: list[dict] | None, reason: str | None = None) -> dict:
    """Gateway products, second-order paths, win-back timing from order gaps and RFM cells, from the customer_paths aggregate."""
    if not rows:
        return {"available": False, "reason": reason or "no customer_paths aggregate yet", "shape": PATHS_SHAPE,
                "rules": ["Gateway: first product with 180-day repeat at 1.3x the median first product or more (100 or more first buyers).",
                          "Second order: the most common next product at 15 percent or more of repeaters, with its median days.",
                          "Win-back: due at 1x the median gap between orders, win-back at 1.5x, lapsed at 3x.",
                          "RFM: 9 cells of order count by days since the last order; alert when 3+ orders, 91 to 364 days grows 20 percent."],
                "moves": []}
    fp = [r for r in rows if r.get("kind") == "first_product" and (r.get("first_buyers") or 0) >= GATEWAY_MIN_BUYERS]
    med = _median([r["repeat_180d"] for r in fp if r.get("repeat_180d") is not None])
    prods = []
    for r in fp:
        ratio = r["repeat_180d"] / med if med else None
        verdict = "gateway" if ratio and ratio >= GATEWAY_HI else ("dead_end" if ratio is not None and ratio <= DEAD_END else "normal")
        nxt = max(r.get("next") or [], key=lambda n: n.get("share") or 0, default=None)
        path = nxt if nxt and (nxt.get("share") or 0) >= NEXT_SHARE and r["first_buyers"] * r["repeat_180d"] >= NEXT_MIN else None
        prods.append({"sku_group": r["sku_group"], "first_buyers": r["first_buyers"], "repeat_180d": r["repeat_180d"],
                      "value_180d": r.get("value_180d"), "ratio": round(ratio, 2) if ratio else None, "verdict": verdict, "next": path})
    prods.sort(key=lambda p: -(p["ratio"] or 0))
    gaps = [r for r in rows if r.get("kind") == "order_gap"]
    timing = [{"group": g["group"], "median_days": g["median_days"], "n": g.get("n"), "due": round(g["median_days"] * DUE_X),
               "winback": round(g["median_days"] * WINBACK_X), "lapsed": round(g["median_days"] * LAPSED_X)} for g in gaps if g.get("median_days")]
    rfm = [r for r in rows if r.get("kind") == "rfm"]
    churn = next((r for r in rfm if r.get("frequency") == "3+" and r.get("recency") == "91-364"), None)
    churn_move = (churn["customers"] / churn["prior_customers"] - 1) if churn and churn.get("prior_customers") else None
    moves = []
    for p in prods:
        if p["verdict"] == "gateway":
            moves.append({"id": f"{SCREEN}.paths.gateway.{p['sku_group']}", "kind": "ad_brief", "owner": "agent_drafts",
                          "title": f"Lead acquisition with {p['sku_group']}: its buyers come back {p['ratio']}x as often",
                          "capability": {"id": "CREA-C06", "autonomy": "agent_does"},
                          "draft": f"DRAFT ad brief\nProduct: {p['sku_group']}\nWhy: 180-day repeat {round(p['repeat_180d'] * 100, 1)} percent, {p['ratio']}x the median first product\nAudience: new buyers only",
                          "steps": [{"n": 1, "who": "agent", "text": "Draft 3 first-order ads that lead with this product."},
                                    {"n": 2, "who": "person", "text": "Approve and launch at a capped test budget."},
                                    {"n": 3, "who": "agent", "text": "Read 60-day repeat of the new buyers against the median."}]})
        if p["next"]:
            day = max(7, int(p["next"]["median_days"]) - 5)
            moves.append({"id": f"{SCREEN}.paths.next.{p['sku_group']}", "kind": "flow", "owner": "agent_drafts",
                          "title": f"Show {p['next']['sku_group']} to {p['sku_group']} buyers on day {day}",
                          "capability": {"id": "LIFE-C07", "autonomy": "founder_gate"},
                          "draft": f"DRAFT flow step\nAfter a first order of: {p['sku_group']}\nFeature: {p['next']['sku_group']} ({round(p['next']['share'] * 100)} percent of repeaters buy it next)\nSend on day: {day} (median {p['next']['median_days']} days, minus 5)",
                          "steps": [{"n": 1, "who": "agent", "text": "Draft the email step with the next product and a five-star line."},
                                    {"n": 2, "who": "person", "text": "Approve and set it live in the email tool."},
                                    {"n": 3, "who": "agent", "text": "Read the second-order rate of this group after 60 days."}]})
    if timing:
        t = next((x for x in timing if x["group"] == "all"), timing[0])
        moves.append({"id": f"{SCREEN}.paths.winback", "kind": "flow", "owner": "agent_drafts",
                      "title": f"Start win-back at day {t['winback']}, from the {t['median_days']}-day median gap",
                      "capability": {"id": "LIFE-C08", "autonomy": "founder_gate"},
                      "draft": f"DRAFT win-back timing\nDue: day {t['due']}\nWin-back: day {t['winback']}\nLapsed, sunset: day {t['lapsed']}",
                      "steps": [{"n": 1, "who": "agent", "text": "Compare the flow's start day with the day above."},
                                {"n": 2, "who": "person", "text": "Approve the new trigger days in the email tool."},
                                {"n": 3, "who": "agent", "text": "Read win-back orders after 28 days."}]})
    if churn_move is not None and churn_move >= CHURN_MOVE:
        moves.append({"id": f"{SCREEN}.paths.churning_hv", "kind": "flow", "owner": "agent_drafts",
                      "title": f"Save high-value buyers going quiet: up {round(churn_move * 100)} percent",
                      "capability": {"id": "LIFE-C08", "autonomy": "founder_gate"},
                      "draft": f"DRAFT save flow\nFor: 3 or more orders, last order 91 to 364 days ago ({churn['customers']:,} buyers)\nEmail 1: what is new; Email 2: a thank-you perk a person sets",
                      "steps": [{"n": 1, "who": "agent", "text": "Build the segment and draft 2 emails."},
                                {"n": 2, "who": "person", "text": "Approve the emails and any perk."},
                                {"n": 3, "who": "agent", "text": "Read the cell size next month."}]})
    return {"available": True, "products": prods, "median_repeat": med, "timing": timing, "rfm": rfm,
            "churn_move": round(churn_move, 4) if churn_move is not None else None, "moves": moves}


# ---------------------------------------------------------------- perception gap: our words against theirs

PERCEPTION_TOP = 20
POSITIONING_FIELDS = ("frame", "category_frame", "price_frame", "proof_points", "one_line_pitch", "category")


def perception(position_records: list[dict], lang_records: list[dict], brand_tokens: set[str], source_name) -> dict:
    """Share of the top buyer words that our positioning also uses, and positioning words buyers never echo."""
    def _val(r):
        v = r.get("value")
        return v if isinstance(v, str) else " ".join(x for x in v if isinstance(x, str)) if isinstance(v, list) else ""
    ours_txt = " ".join(_val(r) for r in position_records if r.get("field") in POSITIONING_FIELDS)
    ours = _lemmas(ours_txt, brand_tokens)
    if not ours:
        return {"available": False, "reason": "no positioning statement in the brain", "rows": []}
    docs: dict[str, set] = {}
    n = 0
    for rec in lang_records:
        v = rec.get("value") if isinstance(rec.get("value"), dict) else {}
        for i, rv in enumerate(v.get("reviews") or []):
            if source_name(rv.get("source") or "") == "Reddit" or not isinstance(rv.get("star"), int) or rv["star"] < 4:
                continue
            n += 1
            for lm in _lemmas(" ".join([v.get("phrase") or "", rv.get("quote") or ""]), brand_tokens):
                docs.setdefault(lm, set()).add(f"{rec['id']}.{i}")
    top = sorted(docs.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:PERCEPTION_TOP]
    theirs = [{"word": w, "reviews": len(ids), "in_positioning": w in ours} for w, ids in top]
    surf = _surface(ours_txt)
    unechoed = sorted(surf.get(w, w) for w in ours if len(docs.get(w, ())) == 0)
    echoed = sorted(((w, len(docs[w])) for w in ours if docs.get(w)), key=lambda x: -x[1])
    score = sum(1 for t in theirs if t["in_positioning"]) / len(theirs) if theirs else None
    missing = [t["word"] for t in theirs if not t["in_positioning"]][:5]
    action = {"id": f"{SCREEN}.perception", "kind": "brain_record", "owner": "agent_drafts",
              "title": "Rewrite the positioning line in the words buyers use",
              "capability": {"id": "BRAND-C59", "autonomy": "agent_does"},
              "draft": "\n".join(["DRAFT positioning check", f"Buyer words we do not use: {', '.join(missing) or 'none'}",
                                  f"Our words buyers never say: {', '.join(unechoed[:8]) or 'none'}",
                                  "Option A: keep the frame, add 1 buyer word to the lead line and test it in 2 ads.",
                                  "Option B: move the unechoed words to proof points, not the lead line.",
                                  "A person picks one. Nothing changes on the site before that."]),
              "steps": [{"n": 1, "who": "agent", "text": "Draft 3 lead lines that keep the frame and use the buyer words."},
                        {"n": 2, "who": "person", "text": "Pick one, or keep the current line."},
                        {"n": 3, "who": "agent", "text": "Test the pick in 2 ads against the current line for 14 days."},
                        {"n": 4, "who": "person", "text": "Approve the winner as a positioning record."}]}
    return {"available": True, "score": round(score, 4) if score is not None else None, "theirs": theirs, "unechoed": unechoed,
            "echoed": [{"word": w, "reviews": c} for w, c in echoed], "praise_reviews": n, "action": action,
            "line": f"{round((score or 0) * 100)} percent of the top {len(theirs)} buyer words appear in our positioning. "
                    f"{len(unechoed)} of our positioning words never show up in a praise review."}


# ---------------------------------------------------------------- claims under fire

CLAIM_HITS = 3            # 3 or more 1 and 2 star reviews use a claim's own feature words
CLAIM_SKIP = {"describe", "described", "state", "states", "claim", "claims", "item", "items", "purchase", "purchased",
              "technology", "system", "extra", "every", "always", "forever", "customer", "make", "right", "anything",
              "additional", "trigger", "include", "includes", "products", "product", "sock", "socks", "pair", "pairs"}


def claims_fire(claim_records: list[dict], lang_records: list[dict], brand_tokens: set[str], source_name,
                product_words: set[str] | None = None) -> dict:
    """Claims whose feature words show up in 1 and 2 star reviews: the promise buyers say we broke.
    Product names (from the brain's product lines) are left out: naming the product is not a broken promise."""
    skip = {_lemma(w) for w in CLAIM_SKIP} | {_lemma(w) for w in (product_words or set())}
    comp = []
    for rec in lang_records:
        v = rec.get("value") if isinstance(rec.get("value"), dict) else {}
        for i, rv in enumerate(v.get("reviews") or []):
            if isinstance(rv.get("star"), int) and rv["star"] <= 2 and source_name(rv.get("source") or "") != "Reddit":
                text = " ".join([v.get("phrase") or "", rv.get("quote") or ""])
                comp.append({"id": f"{rec['id']}.{i}", "lemmas": _lemmas(text, brand_tokens), "text": text})
    rows = []
    for c in claim_records:
        if c.get("tier") not in ("site_backed", "approved"):
            continue
        feats = {w for w in _lemmas(c.get("text") or "", brand_tokens) if w not in skip}
        hits = [x for x in comp if x["lemmas"] & feats]
        words = sorted({w for x in hits for w in x["lemmas"] & feats}, key=lambda w: -sum(1 for x in hits if w in x["lemmas"]))
        verdict = "under_fire" if len(hits) >= CLAIM_HITS else ("watch" if hits else "clear")
        ex = min((x["text"] for x in hits), key=len, default=None)
        action = None
        if verdict == "under_fire":
            action = {"id": f"{SCREEN}.claim.{c['id'].split('.')[-1]}", "kind": "copy", "owner": "agent_drafts",
                      "title": f"Back up or narrow the claim: {', '.join(words[:3])}",
                      "capability": {"id": "BRN-C03", "autonomy": "founder_gate"},
                      "draft": "\n".join([f"DRAFT claim fix", f"Claim: {c.get('text')}", f"1 and 2 star reviews on the same words: {len(hits)}",
                                          f"Example: \"{_clip(ex)}\"" if ex else "",
                                          "Option A: add the proof next to the claim (test result, guarantee terms).",
                                          "Option B: narrow the words to what buyers confirm in five-star reviews.",
                                          "A person picks one. The claim record changes only after that."]),
                      "steps": [{"n": 1, "who": "agent", "text": "Pull every 1 and 2 star line on the claim's words."},
                                {"n": 2, "who": "agent", "text": "Draft the proof line and a narrower claim."},
                                {"n": 3, "who": "person", "text": "Pick one and approve the claim record."},
                                {"n": 4, "who": "agent", "text": "Update every page and ad that carries the claim."}]}
        rows.append({"id": c["id"], "claim": c.get("text"), "tier": c.get("tier"), "hits": len(hits), "words": words[:4],
                     "example": _clip(ex) if ex else None, "verdict": verdict, "action": action})
    rows.sort(key=lambda r: (-r["hits"], r["id"]))
    fire = sum(1 for r in rows if r["verdict"] == "under_fire")
    return {"rows": rows, "complaints": len(comp),
            "line": f"{fire} of {len(rows)} live claims use words that 3 or more 1 and 2 star reviews throw back at us."}


# ---------------------------------------------------------------- lookalike pages

def lookalikes(competitor_records: list[dict], brand_name: str) -> dict:
    """Pages the Ad Library pull flagged as likely impostors of the brand, with the report and warning steps."""
    rows = []
    for r in competitor_records:
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        if "impostor" not in str(v.get("verdict") or "").lower():
            continue
        ref = (r.get("source") or {}).get("ref")
        rows.append({"id": r["id"], "page_id": v.get("page_id"), "ads_seen": v.get("ads_seen"), "links_to": v.get("links_to"),
                     "created": v.get("created"), "ad_library": ref, "note": r.get("text"),
                     "action": {"id": f"{SCREEN}.lookalike.{v.get('page_id')}", "kind": "ticket", "owner": "person",
                                "title": f"Report the lookalike page sending buyers to {v.get('links_to') or 'another site'}",
                                "capability": {"id": "MONEY-C48", "autonomy": "human_assist"},
                                "draft": "\n".join([f"DRAFT report and warning",
                                                    f"Page: {v.get('page_id')} ({ref or 'Ad Library link unavailable'})",
                                                    f"Ads seen: {v.get('ads_seen')}. Links to: {v.get('links_to')}. First seen: {v.get('created')}.",
                                                    f"Meta report: this page copies {brand_name}'s name and sends buyers to {v.get('links_to')}, which is not ours.",
                                                    f"Support reply: We only sell on our own site and the stores listed on it. {v.get('links_to')} is not us.",
                                                    "Social post: a short note naming our real site, pinned for 2 weeks."]),
                                "steps": [{"n": 1, "who": "person", "text": "Report the page and its ads to Meta as impersonation."},
                                          {"n": 2, "who": "agent", "text": "Add the support reply to the help desk macros as a draft."},
                                          {"n": 3, "who": "person", "text": "Approve the macro and the social note."},
                                          {"n": 4, "who": "agent", "text": "Re-check the page in the next Ad Library pull. Stop when it is gone."}]}})
    one = len(rows) == 1
    return {"rows": rows, "line": (f"{len(rows)} page{'' if one else 's'} in the Ad Library pull look{'s' if one else ''} like us and send{'s' if one else ''} buyers elsewhere."
                                   if rows else "No lookalike page in the latest Ad Library pull.")}


# ---------------------------------------------------------------- which offer answers which avatar

def offer_map(avatars: list[dict], all_rungs: list[dict], offer_records: list[dict], policy_records: list[dict]) -> dict:
    """Avatars against the offers and policies that answer their doubts, and the offer our ads push most."""
    levers = {}
    for r in offer_records + policy_records:
        v = r.get("value")
        if isinstance(v, dict) and ("ads" in v or "ads_with_code" in v or "promo" in v):
            continue   # ad sightings of a promo, read below
        if re.search(r"(confirmed|cost)$", r.get("field") or r["id"]):
            continue   # a confirmation or a fee, not a lever
        levers[r["id"]] = {"key": r["id"], "label": (r.get("field") or r["id"].split(".")[-1]).replace("_", " "), "text": r.get("text")}
    used = {p for r in all_rungs for p in r["proof_ids"]}
    cols = [levers[k] for k in sorted(levers) if k in used] + [levers[k] for k in sorted(levers) if k not in used and k.split(".")[1] == "offers"]
    rows, cells = [], {}
    for a in avatars:
        mine = [r for r in all_rungs if a["id"] in r["avatars"]]
        if not mine:
            continue
        rows.append({"key": a["key"], "label": a["name"], "sub": f"{sum(1 for r in mine if not r['proof_ids'])} doubts without an answer"})
        cells[a["key"]] = {}
        for c in cols:
            n = sum(1 for r in mine if c["key"] in r["proof_ids"])
            cells[a["key"]][c["key"]] = {"us": n if n else None, "unit": "n"}
    # the offer our ads push: the promo record with the most ads
    push = None
    for r in offer_records:
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        n = v.get("ads_with_code") or v.get("ads")
        if isinstance(n, int) and (push is None or n > push["ads"]):
            push = {"id": r["id"], "ads": n, "of": v.get("active_ads"), "text": r.get("text")}
    unused = [c["label"] for c in cols if not any(cells[k][c["key"]]["us"] for k in cells)]
    open_rungs = [r for r in all_rungs if not r["proof_ids"] and r["avatars"]]
    action = None
    if push and push["id"] not in used:
        action = {"id": f"{SCREEN}.offers.push", "kind": "ad_brief", "owner": "agent_drafts",
                  "title": "Test an ad that leads with the guarantee, not the discount",
                  "capability": {"id": "LIFE-C42", "autonomy": "founder_gate"},
                  "draft": "\n".join(["DRAFT offer test", f"Now: {push['text']}",
                                      f"The pushed offer answers 0 of {len(all_rungs)} ladder doubts. The top doubts are about wear and fit.",
                                      "Variant A: the current discount. Variant B: the guarantee as the first line, no code.",
                                      "Read cost per order and 60-day repeat. A person sets the budget."]),
                  "steps": [{"n": 1, "who": "agent", "text": "Draft variant B from the guarantee record and a five-star line."},
                            {"n": 2, "who": "person", "text": "Approve and launch A against B at a capped budget."},
                            {"n": 3, "who": "agent", "text": "Read cost per order after 14 days and repeat after 60."}]}
    return {"rows": rows, "cols": [{"key": c["key"], "label": c["label"], "title": c["text"] or ""} for c in cols], "cells": cells,
            "push": push, "unused": unused, "open_rungs": len(open_rungs), "action": action,
            "bare": [r["label"] for r in rows if not any(v["us"] for v in cells[r["key"]].values())],
            "line": ((f"Our ads push one offer in {push['ads']} of {push['of']} live ads; it answers none of the ladder doubts. " if push and push["id"] not in used else "")
                     + (f"{len(unused)} offers answer no avatar's doubt: {', '.join(unused)}." if unused else "Every offer answers at least one doubt."))}


# ---------------------------------------------------------------- messaging hierarchy from buyer evidence

def hierarchy(themes: dict, perception_x: dict, ladders_rows: list[dict], all_rungs: list[dict], proof_texts: dict[str, str],
              frame: str | None, brand: str, today: str) -> dict:
    """One lead line, 3 proof points and 1 doubt answer, each ranked by what buyers say, as a record to approve."""
    earn = [r for r in themes.get("rows", []) if r["impact"] > 0]
    lead_theme = max(earn, key=lambda r: r["impact"])["theme"] if earn else None
    words = [t["word"] for t in perception_x.get("theirs", [])][:3]
    score: dict[str, int] = {}
    for r in all_rungs:
        for p in r["proof_ids"]:
            score[p] = score.get(p, 0) + (r["five_star"] or 0)
    proofs = [{"id": p, "five_star": n, "text": proof_texts.get(p)} for p, n in sorted(score.items(), key=lambda kv: (-kv[1], kv[0]))[:3]]
    doubt = next((r for r in ladders_rows if r["verdict"] == "answer"), None) or next((r for r in ladders_rows if r["verdict"] == "not_landing"), None)
    lead = (f"Lead on {lead_theme.replace('_', ' ')}, in their words: {', '.join(words)}." if lead_theme else "Lead line unavailable: no theme earns stars yet.")
    value = {"lead": lead, "lead_theme": lead_theme, "buyer_words": words, "frame_now": frame,
             "proof_points": [p["id"] for p in proofs], "doubt_to_answer": doubt["id"] if doubt else None,
             "doubt_text": doubt["doubt"] if doubt else None}
    record = {"id": f"{brand}.positioning.messaging_hierarchy", "brand": brand, "section": "positioning", "field": "messaging_hierarchy",
              "value": value, "text": lead + (f" Answer first: {doubt['doubt']}." if doubt else ""),
              "tier": "approved", "confidence": 1.0, "visibility": "private",
              "source": {"type": "founder", "ref": "02-customers-avatars messaging hierarchy", "captured_at": today}}
    return {"lead": lead, "lead_theme": lead_theme, "words": words, "frame": frame, "proofs": proofs,
            "doubt": {"id": doubt["id"], "doubt": doubt["doubt"], "one_star": doubt["one_star"], "verdict": doubt["verdict"]} if doubt else None,
            "record": record,
            "line": "Built from buyer evidence: the theme that earns the most stars, the proof points behind the most five-star lines, the doubt that most needs an answer."}


# ---------------------------------------------------------------- voice check: does a line sound like us

MAX_SENTENCE_WORDS = 20
MAX_GRADE = 10
INFLATED = {"leverage", "unlock", "elevate", "revolutionary", "game-changing", "game changing", "ultimate", "world-class",
            "unparalleled", "cutting-edge", "synergy", "empower", "seamless experience", "next-level", "should", "consider"}
SUPERLATIVE = r"\b(best|#1|number one|most comfortable|perfect|guaranteed|never|always|100 ?%|clinically)\b"


def _syllables(w: str) -> int:
    w = w.lower()
    groups = re.findall(r"[aeiouy]+", w)
    n = len(groups) - (1 if w.endswith("e") and len(groups) > 1 else 0)
    return max(1, n)


def voice_check(text: str, forbidden: list[str], disliked: list[str], buyer_words: list[str], brand_tokens: set[str]) -> dict:
    """Deterministic checks of one line against the writing rules, the voice sheet and the claims register."""
    text = str(text or "").strip()
    checks = []
    add = lambda key, status, why: checks.append({"key": key, "status": status, "why": why})
    if not text:
        return {"verdict": "fail", "checks": [{"key": "empty", "status": "fail", "why": "Paste a line first."}]}
    sents = [s for s in re.split(r"[.!?]+\s*", text) if s.strip()]
    words = re.findall(r"[A-Za-z0-9'%$#-]+", text)
    longest = max((len(s.split()) for s in sents), default=0)
    add("length", "pass" if longest <= MAX_SENTENCE_WORDS else "fail", f"Longest sentence {longest} words; the rule is {MAX_SENTENCE_WORDS} or fewer.")
    if words:
        grade = 0.39 * (len(words) / max(1, len(sents))) + 11.8 * (sum(_syllables(w) for w in words) / len(words)) - 15.59
        add("grade", "pass" if grade <= MAX_GRADE else "warn", f"Reading grade about {round(grade, 1)}; the rule is under {MAX_GRADE}.")
    add("dash", "fail" if "—" in text else "pass", "Em dash found; use a full stop or a comma." if "—" in text else "No em dash.")
    low = text.lower()
    infl = sorted(w for w in INFLATED if re.search(r"\b" + re.escape(w) + r"\b", low))
    add("inflated", "fail" if infl else "pass", f"Inflated or weak words: {', '.join(infl)}." if infl else "No inflated words.")
    sup = sorted(set(m.group(0) for m in re.finditer(SUPERLATIVE, low)))
    add("claim", "warn" if sup else "pass", f"Claim words need proof on file before this ships: {', '.join(sup)}." if sup else "No unproven claim words.")
    tw = _lemmas(text, brand_tokens)
    bad = [f for f in forbidden if f and len(_lemmas(f, brand_tokens) & tw) >= max(2, len(_lemmas(f, brand_tokens)) // 2)]
    add("forbidden", "fail" if bad else "pass", f"Close to a forbidden claim: {bad[0]}" if bad else "No forbidden claim.")
    near = [d for d in disliked if d and len(_lemmas(d, brand_tokens) & tw) / max(1, len(_lemmas(d, brand_tokens))) >= 0.6]
    add("disliked", "warn" if near else "pass", f"Close to a line the founder marked not us: \"{near[0]}\"" if near else "Not close to any line marked not us.")
    used = [w for w in buyer_words if w in tw]
    add("buyer_words", "pass" if used else "warn", f"Uses buyer words: {', '.join(used)}." if used else f"Uses none of the buyer words, like {', '.join(buyer_words[:4])}.")
    verdict = "fail" if any(c["status"] == "fail" for c in checks) else ("warn" if any(c["status"] == "warn" for c in checks) else "pass")
    return {"verdict": verdict, "checks": checks}
