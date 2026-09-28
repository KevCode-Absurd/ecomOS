"""The category ladder: every real alternative a shopper weighs, from doing nothing up to the closest
direct rival, with our rung marked and the move that wins shoppers on each rung.

Rungs are built by rules from the brain, never typed per brand:
  do_nothing   keep the socks they have. Signal: Reddit "buy it for life" frame mentions and the most
               upvoted "won't pay more" question in seo_facts.
  value        cheap multipacks: alternatives recommended instead of us that are not tracked pages and
               have no price band. Signal: their Reddit upvotes.
  adjacent     basics and apparel pages in the competitive frame. Signal: their active ads.
  direct       direct pages at or below the tracked median price per pair. Signal: active ads.
  premium      direct pages above the tracked median. Signal: active ads.
The brand sits on the rung its median price per pair falls in against the direct pages. Demand trend per
rung (the room's "a lower rung is gaining") needs a search or trends source and reads unavailable.
"""
from __future__ import annotations

MOVES = {
    "do_nothing": ("Show the cost of waiting: a worn sock against a new one, price per wear.", "CREA-C31", "copy"),
    "value": ("Frame price per wear and the guarantee against a cheap multipack.", "CREA-C31", "copy"),
    "adjacent": ("Win the basics buyer with a socks-plus-underwear bundle.", "LIFE-C39", "offer"),
    "direct": ("Out-prove them on comfort in the first 3 seconds of the ad.", "CREA-C06", "ad_brief"),
    "premium": ("Take their durability shoppers with the guarantee said out loud.", "CREA-C06", "ad_brief"),
}
AUTONOMY = {"CREA-C31": "agent_does", "LIFE-C39": "founder_gate", "CREA-C06": "agent_does"}
LABELS = {"do_nothing": "Do nothing: keep the old pairs", "value": "Cheap multipacks", "adjacent": "Basics and apparel brands",
          "direct": "Direct sock brands, at or below the median", "premium": "Premium sock brands, above the median"}


def build(m: dict, brain) -> dict:
    split = m["category_median"]
    frames = (brain.get(f"{brain.brand}.positioning.reddit_frames") or {}).get("value") or {}
    q = sorted([r.get("value") for r in brain.records("seo_facts") if isinstance(r.get("value"), dict)],
               key=lambda v: -(v.get("upvotes") or 0))
    losses = (m.get("losses") or {}).get("rows") or []
    prices = {c["name"]: c["price"]["median"] for c in m["competitors"]}
    def price_of(name):
        return next((v for k, v in prices.items() if k.lower()[:6] == name.lower()[:6]), None)
    rungs = {k: {"key": k, "label": LABELS[k], "members": [], "signal": None, "signal_text": None} for k in LABELS}
    rungs["do_nothing"]["members"] = ["no purchase"]
    bifl = frames.get("buy_it_for_life")
    rungs["do_nothing"]["signal"] = bifl
    rungs["do_nothing"]["signal_text"] = (f"{bifl} Reddit mentions of buy it for life" if bifl is not None else "unavailable") + (
        f"; top question {q[0]['upvotes']} upvotes in r/{q[0]['subreddit']}" if q else "")
    val = [x for x in losses if x["theme"] == "value"]
    rungs["value"]["members"] = [x["name"] for x in val]
    ups = [x["upvotes"] for x in val if x["upvotes"] is not None]
    rungs["value"]["signal"] = sum(ups) if ups else None
    rungs["value"]["signal_text"] = f"{sum(ups)} upvotes on threads naming them" if ups else "unavailable"
    for p in m["pages"]:
        if p["role"] == "self":
            continue
        if p["frame"] == "basics":
            key = "adjacent"
        else:
            pr = price_of(p["name"])
            key = "premium" if pr is not None and split is not None and pr > split else "direct"
        rungs[key]["members"].append(p["name"])
        if isinstance(p["active_ads"], int):
            rungs[key]["signal"] = (rungs[key]["signal"] or 0) + p["active_ads"]
    for k in ("adjacent", "direct", "premium"):
        s = rungs[k]["signal"]
        rungs[k]["signal_text"] = f"{s} active ads across the rung" if s is not None else "unavailable"
    ours = m["packs"].get("median_per_pair") if m["packs"]["available"] else None
    our_rung = None if ours is None or split is None else ("premium" if ours > split else "direct")
    order = ["premium", "direct", "adjacent", "value", "do_nothing"]
    out = []
    for k in order:
        r = rungs[k]
        move, cap, kind = MOVES[k]
        r.update(move=move, capability=cap, autonomy=AUTONOMY[cap], artefact=kind, ours=(k == our_rung), trend=None)
        out.append(r)
    return {"rungs": out, "our_rung": our_rung, "our_price": ours, "split": split,
            "coverage": sum(1 for r in out if r["members"]), "trend_reason": "needs a search trends source; not connected",
            "rule": "Rungs by rule: direct pages split at the tracked median price; basics pages are adjacent; alternatives "
                    "recommended instead that are not tracked are cheap multipacks; doing nothing is always a rung."}
