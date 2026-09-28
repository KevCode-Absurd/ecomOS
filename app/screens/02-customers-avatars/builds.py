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
