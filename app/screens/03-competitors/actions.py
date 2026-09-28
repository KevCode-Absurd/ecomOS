"""Competitors screen: findings to actions with real titles, steps and artefacts (depth.md section 5).

`build(brand, window, root)` runs audit.run, then one builder per rule turns each
finding into an action: owner, 2 to 8 steps with who does each, the artefact it
produces (ad_brief, offer, page_section, research_note, ticket, connector_setup)
with a draft written from the brain when the brain holds enough, a size, a win
rule, a stop rule and a check date. The rubric is scored by app/rank.py so the
master list compares like with like. No model call; same inputs, same output.

Competitor material in a draft is a signal only: format, hook type, run length.
A draft never carries competitor text, logos, products or faces.
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parents[1]
NEVER_COPY = "Never copy their text, logos, products or faces. Borrow layout and mood only."


def _load(name: str, path: Path):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


audit = _load("competitors_audit", HERE / "audit.py")
ranker = _load("ecomos_rank", APP / "rank.py")


def _step(n, who, text):
    return {"n": n, "who": who, "text": text}


def _steps(*pairs):
    return [_step(i + 1, who, text) for i, (who, text) in enumerate(pairs)]


def _plus(day: str, days: int) -> str:
    return (dt.date.fromisoformat(day) + dt.timedelta(days=days)).isoformat()


def _ev(f: dict, metric: str):
    for e in f.get("evidence") or []:
        if e["metric"] == metric:
            return e["value"]
    return None


def _proofs(m: dict) -> list[str]:
    v = m["brain"].get(f"{m['brand']}.positioning.proof_points")
    v = v.get("value") if v else None
    return [str(x) for x in v] if isinstance(v, list) else []


def _proof_for(m: dict, words: list[str]) -> str | None:
    for p in _proofs(m):
        if any(w in p.lower() for w in words):
            return p
    return None


# ---------------------------------------------------------------- one builder per rule

def act_angle(f: dict, m: dict) -> dict:
    """COMP-R01: an angle we hold and no tracked brand runs. Make 3 ads that lead with it."""
    key = f["entity"]["id"].removeprefix("angle_")
    angle = next((a for a in m["angles"] if a["key"] == key), None) or {"label": key, "keys": [key]}
    spec = next((a for a in audit.ANGLES if a["key"] == key), {"keys": [key]})
    proof = _proof_for(m, spec["keys"]) or "the brain record behind this angle"
    n, used, active = _ev(f, "competitors_tracked"), _ev(f, "brand_ads_with_angle"), _ev(f, "brand_active_ads")
    name = m["brand"].capitalize()
    target = max(3, round((active or 0) * audit.ANGLE_SHARE_MAX)) if active else 3
    draft = "\n".join([
        f"Ad brief: lead with {angle['label']}. {name} owns it; 0 of {n} tracked brands run it.",
        f"Proof to use: {proof}.",
        "3 ads: 1 video (first 3 seconds state the proof), 2 static images (proof as the headline).",
        "Same products and offer as the current best seller ads. Only the first line and first frame change.",
        f"Target: {target} of {active} active ads carry the angle (now {used}).",
        NEVER_COPY,
    ])
    return {
        "title": f"Make 3 ads that lead with {angle['label']}, the angle no tracked page runs",
        "owner": "agent_drafts",
        "artefact": {"kind": "ad_brief", "label": f"3 ad briefs that lead with {angle['label']}", "draft": draft},
        "steps": _steps(("agent", f"Pull the proof for {angle['label']} from the brain and the current top 3 ads by spend."),
                        ("agent", "Write 3 briefs: new first line and first frame, same product and offer."),
                        ("person", "Approve the briefs. Creative makes them. Log the decision as a creative test."),
                        ("agent", f"Launch as a test beside the control ads. Check on {_plus(f['last_seen'], 14)}.")),
        "size": {"text": f"{used} of {active} active ads now, {target} after", "count": target},
        "win_rule": "Cost per order at or below the control ads after 2,000 impressions each",
        "stop_rule": "Cost per order 30 percent above control after 7 days",
        "check_on": _plus(f["last_seen"], 14), "time_to_ship_hours": 6,
    }


def act_price(f: dict, m: dict) -> dict:
    """COMP-R02: price per pair far from the tracked median. Show the proof on the page before touching price."""
    idx = _ev(f, "price_position_index")
    price, med = _ev(f, "brand_price_per_pair"), _ev(f, "competitor_median_price_per_pair")
    below = idx is not None and idx < 100
    name = m["brand"].capitalize()
    proof = _proof_for(m, ["guarantee", "arch", "seamless", "donat"]) or "the proof points in the brain"
    if below:
        title = f"Stop discounting below the category: move the first order code off the best packs"
        draft = "\n".join([
            f"Offer spec: {name} nets ${price:.2f} a pair after discounts. Tracked median list is ${med:.2f}.",
            "Test: keep the first order code on singles and 3-packs, remove it from 6-packs and up.",
            "Replace it on those packs with the value line: price per pair and what it includes.",
            f"Proof line on the pack card: {proof}.",
            "Split 50 50 by visitor for 14 days. Brand price is simulated until the store connects.",
        ])
        kind, label = "offer", "an offer test: code off the 6-pack and up"
        steps = _steps(("agent", "Pull net price per pair by pack for the last full month and the code's share of orders."),
                       ("agent", "Draft the offer test and the value line for each pack card."),
                       ("person", "Approve the test. The store owner sets the code rules."),
                       ("agent", f"Read orders and net price per pair on {_plus(f['last_seen'], 14)}."))
        win, stop = "Net revenue per visitor up with orders down less than 5 percent", "Orders down 10 percent for 5 days"
    else:
        title = "Show why the price is higher: put the proof next to the price on every pack"
        draft = "\n".join([
            f"Page section: {name} sells at ${price:.2f} a pair against a tracked median of ${med:.2f}.",
            f"Under the price: {proof}.",
            "Add price per pair on every pack and a 3-line compare: us, a multi-pack, a premium brand.",
        ])
        kind, label = "page_section", "a price proof block for the pack cards"
        steps = _steps(("agent", "Pull the proof points and the pack prices from the brain."),
                       ("agent", "Draft the proof block and price per pair for each pack."),
                       ("person", "Approve and publish on the product pages."),
                       ("agent", f"Check add to cart rate on {_plus(f['last_seen'], 14)}."))
        win, stop = "Add to cart rate up 5 percent on pack pages", "Add to cart rate down 5 percent for 7 days"
    return {"title": title, "owner": "agent_drafts",
            "artefact": {"kind": kind, "label": label, "draft": draft}, "steps": steps,
            "size": {"text": f"index {idx} against a band of {audit.PRICE_BAND[0]} to {audit.PRICE_BAND[1]}"},
            "win_rule": win, "stop_rule": stop, "check_on": _plus(f["last_seen"], 14), "time_to_ship_hours": 4}


def act_offer_run(f: dict, m: dict) -> dict:
    """COMP-R03: a competitor keeps an offer type live that we hold but do not run. Put ours in ads."""
    key = f["entity"]["id"]
    o = next((x for x in m["offer_runs"] if x["key"] == key), None) or {"label": key, "competitors": []}
    top = o["competitors"][0] if o["competitors"] else {"name": "a tracked brand", "days": _ev(f, "competitor_longest_ad_days")}
    name = m["brand"].capitalize()
    held = m["brain"].get(f"{m['brand']}.{next((x['brain_ref'] for x in audit.OFFER_TYPES if x['key'] == key), '')}")
    held_text = str(held.get("value")) if held and held.get("value") else f"the {o['label']} in the brain"
    draft = "\n".join([
        f"Ad brief: put {name}'s {o['label']} in the first line of 3 ads.",
        f"What we offer: {held_text}.",
        f"Why now: {top['name']} has kept a {o['label']} ad live {top['days']} days. {len(o['competitors'])} tracked brands run one.",
        f"{name} runs it in {o.get('brand_ads', 0)} ads.",
        "Formats: 1 video with the promise said out loud, 2 static images with the promise as the headline.",
        NEVER_COPY,
    ])
    return {
        "title": f"Put our {o['label']} in 3 ads; {top['name']} has kept one live {top['days']} days",
        "owner": "agent_drafts",
        "artefact": {"kind": "ad_brief", "label": f"3 ad briefs with the {o['label']} up front", "draft": draft},
        "steps": _steps(("agent", f"Pull the {o['label']} wording from the brain and check it matches the site."),
                        ("agent", "Write 3 briefs with the promise in the first line."),
                        ("person", "Approve. Legal check on the promise wording."),
                        ("agent", f"Run beside control. Check on {_plus(f['last_seen'], 14)}.")),
        "size": {"text": f"{o.get('brand_ads', 0)} ads now, 3 after", "count": 3},
        "win_rule": "Click to order rate at or above control", "stop_rule": "Cost per order 30 percent above control after 7 days",
        "check_on": _plus(f["last_seen"], 14), "time_to_ship_hours": 6,
    }


def act_lookalike(f: dict, m: dict) -> dict:
    """COMP-R04: a lookalike page takes our shoppers. A person reports it; the agent drafts the report."""
    lk = m["lookalike"] or {}
    name = m["brand"].capitalize()
    draft = "\n".join([
        f"Report to Meta: page {lk.get('page_id')} impersonates {name}.",
        f"It ran {lk.get('ads_seen')} ads from {lk.get('created')} that link to {lk.get('links_to')}, not our store.",
        f"Ad Library: {lk.get('ref') or 'link in the brain record'}.",
        "Ask: remove the page and its ads. Attach the trademark registration and 3 screenshots.",
        "Also: post a short note on our page and add the domain to the support macro for lost orders.",
    ])
    return {
        "title": f"Report the lookalike page to Meta; it ran {lk.get('ads_seen')} ads to {lk.get('links_to')}",
        "owner": "person",
        "artefact": {"kind": "ticket", "label": "an impersonation report with the evidence", "draft": draft},
        "steps": _steps(("agent", "Collect the page id, ad count, first date and the domain from the capture."),
                        ("agent", "Draft the impersonation report and the support macro."),
                        ("person", "File the report in Meta's IP form with the trademark number."),
                        ("agent", f"Re-check the page in the Ad Library on {_plus(f['last_seen'], 7)}.")),
        "size": {"text": f"{lk.get('ads_seen')} lookalike ads live", "count": lk.get("ads_seen")},
        "win_rule": "0 active ads on the page", "stop_rule": None,
        "check_on": _plus(f["last_seen"], 7), "time_to_ship_hours": 1,
    }


def act_coverage(f: dict, m: dict) -> dict:
    """COMP-R05: an angle and format they run and we do not. The brief is the cell's own brief."""
    gid = f["entity"]["id"]
    g = next((x for x in m["coverage"]["gaps"] if x["gap_id"] == gid), None)
    label = f["entity"]["label"]
    return {
        "title": f"Brief 2 ads: {label.lower()}, a cell they fill and we leave empty",
        "owner": "agent_drafts",
        "artefact": {"kind": "ad_brief", "label": f"an ad brief: {label.lower()}", "draft": g["brief"] if g else None},
        "steps": _steps(("agent", "Pull our proof for the angle and the format spec."),
                        ("agent", "Write the brief: 2 ads, proof first, same product and offer as control."),
                        ("person", "Approve the brief. Creative makes the 2 ads."),
                        ("agent", f"Run beside control and read cost per order on {_plus(f['last_seen'], 14)}.")),
        "size": {"text": f"0 ads now, 2 after; they put {round((g or {}).get('them', 0) * 100)} percent of their ads here",
                 "count": 2},
        "win_rule": "Cost per order at or below control after 2,000 impressions each",
        "stop_rule": "Cost per order 30 percent above control after 7 days",
        "check_on": _plus(f["last_seen"], 14), "time_to_ship_hours": 4,
    }


def _mix_gap(f: dict, m: dict, kind: str) -> dict | None:
    key = {"first_line": f["entity"]["id"].removeprefix("first_line_"), "offer": f["entity"]["id"].removeprefix("offer_"),
           "discount": "discount_heavy"}[kind]
    return next((g for g in m["mix"]["gaps"] if g["kind"] == kind and g["key"] == key), None)


def act_first_line(f: dict, m: dict) -> dict:
    """COMP-R06: a first line kind they use and we do not. The agent builds and grades a hook bank."""
    g = _mix_gap(f, m, "first_line") or {"label": f["entity"]["label"], "draft": None, "pages": []}
    return {
        "title": f"Write 6 {g['label'].lower()} first lines and test the best 2",
        "owner": "agent",
        "artefact": {"kind": "copy", "label": f"a graded hook bank: 6 {g['label'].lower()} first lines", "draft": g["draft"]},
        "steps": _steps(("agent", "Pull praise phrases from the language bank and our proof points."),
                        ("agent", "Write 6 first lines in the kind and grade them on the hook bank rubric."),
                        ("agent", "Hand the best 2 to the creative queue as first line swaps on current ads."),
                        ("person", f"Read the test on {_plus(f['last_seen'], 14)} and keep or drop.")),
        "size": {"text": f"6 lines, 2 tested; {len(g['pages'])} pages open this way", "count": 6},
        "win_rule": "Thumb stop rate or click rate up 10 percent on the swapped ads",
        "stop_rule": "Click rate 20 percent below control after 3,000 impressions",
        "check_on": _plus(f["last_seen"], 14), "time_to_ship_hours": 2,
    }


def act_offer_gap(f: dict, m: dict) -> dict:
    """COMP-R07: an offer we hold and never say while tracked pages say theirs."""
    g = _mix_gap(f, m, "offer") or {"label": f["entity"]["label"], "draft": None, "pages": []}
    return {
        "title": f"Test our {g['label'].lower()} line in 3 ads against the current offer",
        "owner": "agent_drafts",
        "artefact": {"kind": "test_brief", "label": f"an offer test: {g['label'].lower()} line against the code", "draft": g["draft"]},
        "steps": _steps(("agent", "Check the offer terms in the brain match the site today."),
                        ("agent", "Draft the test: 3 ads with the line in the first frame, 3 control."),
                        ("person", "Approve the test and the wording."),
                        ("agent", f"Read click to order rate and net revenue per order on {_plus(f['last_seen'], 14)}.")),
        "size": {"text": f"3 test ads against 3 control; {len(g['pages'])} pages show it", "count": 3},
        "win_rule": "Click to order rate up and net revenue per order flat or better",
        "stop_rule": "Net revenue per order down 10 percent after 7 days",
        "check_on": _plus(f["last_seen"], 14), "time_to_ship_hours": 4,
    }


def act_discount(f: dict, m: dict) -> dict:
    """COMP-R08: a code on most of our ads while direct peers run none. The founder gates any policy change."""
    g = _mix_gap(f, m, "discount") or {"draft": None, "ours": None, "pages": []}
    share = round((g.get("ours") or 0) * 100)
    return {
        "title": f"Run 6 proof-first ads with no code; {share} percent of our ads push one",
        "owner": "agent_drafts",
        "artefact": {"kind": "test_brief", "label": "a no-code ad test with proof first", "draft": g["draft"]},
        "steps": _steps(("agent", "Pick the 6 ads with the most spend that carry the code."),
                        ("agent", "Draft proof-first versions with no code; keep the code ads as control."),
                        ("person", "Founder approves the test. The code policy does not change yet."),
                        ("agent", f"Read net revenue per order and new customer orders on {_plus(f['last_seen'], 14)}.")),
        "size": {"text": f"6 of the code ads; {share} percent of ads push a code now", "count": 6},
        "win_rule": "Net revenue per order up with new customer orders down less than 5 percent",
        "stop_rule": "New customer orders down 15 percent after 7 days",
        "check_on": _plus(f["last_seen"], 14), "time_to_ship_hours": 4,
    }


def act_ladder(f: dict, m: dict) -> dict:
    """COMP-R09: our packs barely reward buying more while a peer sells bundles. Draft a deeper ladder."""
    lad = m["ladder"]
    b = lad["bundle"] or {}
    rows = [l for l in lad["ladders"] if l["saving"] is not None]
    lines = [f"Offer spec: a pack ladder that saves more per pair as the pack grows.",
             f"Now: packs save a median {round(lad['median_saving'] * 100)} percent a pair against a single (simulated net prices).",
             f"Peer signal: {b.get('page')} advertises {b.get('pct')} percent off bundles.",
             "Proposed steps: 3-pack saves 10 percent a pair, 6-pack 15 percent, 12-pack 20 percent. List price per pair on every card.",
             "Styles now: " + "; ".join(f"{l['style']} {round(l['saving'] * 100)} percent at {l['biggest_pairs']} pairs" for l in rows) + ".",
             "Margin check first: finance confirms each step keeps contribution above the floor."]
    return {
        "title": f"Deepen the pack ladder to 10, 15 and 20 percent a pair; ours saves {round(lad['median_saving'] * 100)} percent",
        "owner": "agent_drafts",
        "artefact": {"kind": "offer", "label": "a pack ladder offer spec with a margin check", "draft": "\n".join(lines)},
        "steps": _steps(("agent", "Pull net price per pair by style and pack and the contribution floor."),
                        ("agent", "Draft the ladder and the pack card copy with price per pair."),
                        ("person", "Founder approves the ladder after the margin check."),
                        ("agent", f"Test on 2 styles for 14 days; read pairs per order and net revenue per order on {_plus(f['last_seen'], 14)}.")),
        "size": {"text": f"median saving {round(lad['median_saving'] * 100)} percent now, 10 to 20 percent after"},
        "win_rule": "Pairs per order up 10 percent with net revenue per order flat or better",
        "stop_rule": "Contribution per order down 5 percent for 7 days",
        "check_on": _plus(f["last_seen"], 14), "time_to_ship_hours": 6,
    }


def act_above(f: dict, m: dict) -> dict:
    """COMP-R10: priced above the direct median with nothing in the brain to justify it."""
    style = f["entity"]["label"].replace(" single pair", "")
    draft = "\n".join([f"Page section: why {style} costs more.",
                       f"Price: {f['sentence'].split('. ')[0]}.",
                       "Add under the price: the proof (test result, material, guarantee), price per pair on each pack, and the guarantee line.",
                       "First add the proof record on the brand brain screen. No claim ships without it."])
    return {
        "title": f"Add a proof block to the {style} page before the next price review",
        "owner": "agent_drafts",
        "artefact": {"kind": "page_section", "label": f"a price proof block for {style}", "draft": draft},
        "steps": _steps(("person", f"Add the proof for {style} to the brand brain."),
                        ("agent", "Draft the block and the price per pair lines."),
                        ("person", "Approve and publish."),
                        ("agent", f"Check add to cart rate on the page on {_plus(f['last_seen'], 14)}.")),
        "size": None, "win_rule": "Add to cart rate up 5 percent on the page", "stop_rule": "Add to cart rate down 5 percent for 7 days",
        "check_on": _plus(f["last_seen"], 14), "time_to_ship_hours": 3,
    }


def act_corner(f: dict, m: dict) -> dict:
    """COMP-R11: an open strong-claim corner. Test a positioning line that takes it before any ad spend."""
    corner = f["entity"]["label"]
    frame = (m["brain"].get(f"{m['brand']}.positioning.frame") or {}).get("value") or "the current frame"
    draft = "\n".join([f"Positioning test: take the {corner} corner.",
                       f"Frame now: {frame}.",
                       "Write 2 lines: the current frame and a frame that claims the corner with our proof.",
                       "Test both on a 5 second preference poll with 200 shoppers, then as 2 ad first lines.",
                       "Keep the frame that wins both. Write it to the brain as an approved record."])
    return {"title": f"Test a positioning line that takes the open {corner} corner", "owner": "agent_drafts",
            "artefact": {"kind": "test_brief", "label": "a positioning test: 2 frames", "draft": draft},
            "steps": _steps(("agent", "Draft 2 frames from the brain's proof points."),
                            ("person", "Approve the frames."),
                            ("agent", "Run the poll and the 2 first lines; report the winner."),
                            ("person", "Approve the winning frame as a brain record.")),
            "size": None, "win_rule": "Preference share 10 points above the current frame", "stop_rule": "No frame beats the current by 5 points",
            "check_on": _plus(f["last_seen"], 21), "time_to_ship_hours": 6}


def act_refresh(f: dict, m: dict) -> dict:
    """COMP-R12: a direct competitor replaced every ad. The agent reads the new flight and says what overlaps ours."""
    page = f["entity"]["label"].replace(" new flight", "")
    p = next((x for x in m["pages"] if x["name"] == page), {})
    draft = "\n".join([f"Research note: {page}'s new flight.",
                       f"What changed: {f['sentence']}",
                       f"Their angles on file: {', '.join(a['label'].lower() for a in p.get('angles') or []) or 'none tagged'}.",
                       f"Our top angles: {', '.join(m['our_top_angles'])}.",
                       "Read: formats, first line kinds, offers and landing pages of the new ads, by page id only.",
                       "Output: 3 lines on what overlaps ours and whether to answer. Signals only; never copy their ads."])
    return {"title": f"Read {page}'s new flight and say what overlaps ours", "owner": "agent",
            "artefact": {"kind": "research_note", "label": f"a research note on {page}'s new ads", "draft": draft},
            "steps": _steps(("agent", f"Pull {page}'s active ads by page id at the next capture, inside the Apify caps."),
                            ("agent", "Tag angles, formats, first lines and offers; diff against the last capture."),
                            ("agent", "Write the 3-line note; raise a brief only if a new angle overlaps ours.")),
            "size": {"text": f"{p.get('active_ads')} new ads to read", "count": p.get("active_ads")},
            "win_rule": None, "stop_rule": None, "check_on": _plus(f["last_seen"], 7), "time_to_ship_hours": 1}


def act_no_id(f: dict, m: dict) -> dict:
    """COMP-R13: a tracked page with no page id. A person finds and pastes it; the agent adds it to the pull."""
    page = f["entity"]["label"].replace(" page id", "")
    return {"title": f"Paste {page}'s Ad Library page id so it can be pulled", "owner": "person",
            "artefact": {"kind": "brain_record", "label": f"{page} page id in the pull config", "draft":
                         f"Open the Ad Library, search the page name {page}, open the page, copy view_all_page_id from the url. "
                         "Paste it here. The agent adds it to config/apify.json. Never pull by keyword."},
            "steps": _steps(("person", f"Find {page}'s page id in the Ad Library and paste it."),
                            ("agent", "Add the id to the pull config and include it in the next capture.")),
            "size": None, "win_rule": None, "stop_rule": None, "check_on": _plus(f["last_seen"], 7), "time_to_ship_hours": 1}


def act_stale(f: dict, m: dict) -> dict:
    """COMP-R14: the capture is stale. A person approves the Apify spend shown first; the agent runs the capped pull."""
    return {"title": "Approve a fresh Ad Library capture; the estimate shows before it runs", "owner": "person",
            "artefact": {"kind": "research_note", "label": "a fresh ad-level snapshot of the tracked pages", "draft": None},
            "steps": _steps(("agent", "Show the pages, the item cap, the estimate and the caps left this week."),
                            ("person", "Approve the spend."),
                            ("agent", "Run the pull by page id through the capped connector; the ledger logs it."),
                            ("agent", "Re-run the audit on the new snapshot.")),
            "size": None, "win_rule": None, "stop_rule": None, "check_on": _plus(f["last_seen"], 7), "time_to_ship_hours": 1}


def act_lost(f: dict, m: dict) -> dict:
    """COMP-R15: shoppers pick a named alternative. Write the compare block and the support macro from verified facts."""
    key = f["entity"]["id"].removeprefix("lost_")
    x = next((r for r in m["losses"]["rows"] if r["key"] == key), None) or {"name": key, "answer": None, "theme_label": ""}
    return {"title": f"Write our answer to {x['name']}: a compare block, an FAQ and a support macro",
            "owner": "agent_drafts",
            "artefact": {"kind": "page_section", "label": f"a how we compare block against {x['name']}", "draft": x["answer"]},
            "steps": _steps(("agent", "Pull the verified proof for the theme and the doubts with no proof."),
                            ("agent", "Draft the compare block, 1 FAQ answer and 1 support macro. No disparaging lines."),
                            ("person", "Approve; legal checks any named comparison."),
                            ("agent", f"Publish the FAQ and macro; check the theme's one-star count on {_plus(f['last_seen'], 28)}.")),
            "size": {"text": f"{x.get('times')} Reddit recommendations, {x.get('upvotes')} upvotes"},
            "win_rule": "Fewer one-star reviews on the theme next quarter", "stop_rule": None,
            "check_on": _plus(f["last_seen"], 28), "time_to_ship_hours": 3}


def act_attack(f: dict, m: dict) -> dict:
    """COMP-R17: they lead with the theme we are weakest on. Say our guarantee against it; send the doubt to product."""
    a = m["reviews"]["attack"] or {}
    return {"title": f"Answer the {a.get('label')} attack: the guarantee up front and the top doubt to product",
            "owner": "agent_drafts",
            "artefact": {"kind": "page_section", "label": f"a guarantee block against the {a.get('label')} doubt, plus a product ticket",
                         "draft": audit.revmod.draft(a, m["brand"].capitalize()) if a else None},
            "steps": _steps(("agent", "Pull the rung doubts, their one-star reviews and the guarantee wording."),
                            ("agent", "Draft the page block, 2 ad lines and the product ticket."),
                            ("person", "Founder approves the guarantee wording."),
                            ("person", "Product owner takes the ticket on the top doubt."),
                            ("agent", f"Check one-star reviews on the theme on {_plus(f['last_seen'], 28)}.")),
            "size": {"text": f"{a.get('one_star')} one-star reviews on the theme", "count": a.get("one_star")},
            "win_rule": "One-star share on the theme down next quarter", "stop_rule": None,
            "check_on": _plus(f["last_seen"], 28), "time_to_ship_hours": 4}


def act_undercut(f: dict, m: dict) -> dict:
    """COMP-R18: Amazon price per pair below our site. The agent checks every listing's seller and price."""
    style = f["entity"]["label"].replace(" on Amazon", "")
    st = next((x for x in m["presence"]["styles"] if x["style"] == style), None)
    return {"title": f"Check who sells {style} on Amazon {round((st or {}).get('gap', 0) * 100)} percent below our site",
            "owner": "agent",
            "artefact": {"kind": "listing_fix", "label": f"a seller and price check of the {style} listings",
                         "draft": audit.mktmod.draft(st, m["brand"].capitalize()) if st else None},
            "steps": _steps(("agent", "Read each listing's seller, pack size and price per pair (read only)."),
                            ("agent", "Flag resellers for the brand registry and MAP team; flag our own listings for a pack price fix."),
                            ("person", "The marketplace owner acts on the flags."),
                            ("agent", f"Re-check the listings on {_plus(f['last_seen'], 14)}.")),
            "size": {"text": f"{(st or {}).get('listings')} listings, {round((st or {}).get('gap', 0) * 100)} percent gap"},
            "win_rule": "Amazon price per pair within 10 percent of the site", "stop_rule": None,
            "check_on": _plus(f["last_seen"], 14), "time_to_ship_hours": 2}


def act_velocity(f: dict, m: dict) -> dict:
    """COMP-R19: we ship new ads far slower than direct pages. A weekly volume plan fed by the gaps."""
    v = m["velocity"]
    gaps = [f"{g['angle_label'].lower()} in {g['format']}" for g in m["coverage"]["gaps"]]
    return {"title": f"Ship {v['target']:g} new ads a week from the gaps; we ship {audit.velmod.now_rate(v):g} now",
            "owner": "agent_drafts",
            "artefact": {"kind": "ad_brief", "label": "a weekly creative volume plan with the first week's briefs",
                         "draft": audit.velmod.draft(v, gaps)},
            "steps": _steps(("agent", "List the coverage gaps, the hook bank lines and the 2 best ads."),
                            ("agent", "Draft the week: 2 concepts, 3 first line swaps, 1 new format."),
                            ("person", "Approve the week; creative makes it."),
                            ("agent", f"Count new ads live and cost per order each week; review on {_plus(f['last_seen'], 28)}.")),
            "size": {"text": f"{audit.velmod.now_rate(v):g} a week now, {v['target']:g} after"},
            "win_rule": "Blended cost per order flat or better at the higher volume", "stop_rule": "Cost per order up 15 percent for 2 weeks",
            "check_on": _plus(f["last_seen"], 28), "time_to_ship_hours": 6}


def act_niche(f: dict, m: dict) -> dict:
    """COMP-R20: size the biggest niche they serve and we barely do, against our own bar."""
    key = f["entity"]["id"].removeprefix("niche_")
    c = next((x for x in m["niche"]["candidates"] if x["angle"] == key), None) or {"label": key, "their_share": 0, "our_share": 0, "pages": []}
    return {"title": f"Size the {c['label'].lower()} niche against our bar before making ads for it", "owner": "agent",
            "artefact": {"kind": "research_note", "label": f"a sizing note on {c['label'].lower()}",
                         "draft": audit.nichemod.draft(c, m["niche"]["bar"], m["brand"].capitalize())},
            "steps": _steps(("agent", "Pull search demand, review mentions and Reddit threads for the niche's terms."),
                            ("agent", "Compare the evidence to the bar in buyers."),
                            ("agent", "Write the 3-line note; raise a test brief only if it clears the bar.")),
            "size": {"text": f"bar {m['niche']['bar']['buyers']:,} buyers a year" if m["niche"].get("bar") else None},
            "win_rule": None, "stop_rule": None, "check_on": _plus(f["last_seen"], 14), "time_to_ship_hours": 2}


def act_premium(f: dict, m: dict) -> dict:
    """COMP-R21: premium signals with a deep code. Cap the code, swap depth for a gift or pack step."""
    pr = m["premium"]
    return {"title": f"Cap the code at 10 percent; we show premium signals and discount {pr['our_depth']} percent",
            "owner": "agent_drafts",
            "artefact": {"kind": "offer", "label": "an offer policy: code cap and a gift instead of depth",
                         "draft": audit.premmod.draft(pr, m["brand"].capitalize())},
            "steps": _steps(("agent", "Pull code use, net price per pair and the premium signals on file."),
                            ("agent", "Draft the policy and the 14-day test on half of new visitors."),
                            ("person", "Founder approves the test."),
                            ("agent", f"Read net revenue per order and new customer orders on {_plus(f['last_seen'], 14)}.")),
            "size": {"text": f"{pr['our_depth']} percent now, 10 percent after"},
            "win_rule": "Net revenue per new order up with new orders down less than 5 percent",
            "stop_rule": "New customer orders down 10 percent for 5 days", "check_on": _plus(f["last_seen"], 14), "time_to_ship_hours": 4}


def act_search(f: dict, m: dict) -> dict:
    """COMP-R22: terms they go after that we never say. A keyword check brief for the Google Ads and SEO screens."""
    s = m["search"]
    return {"title": "Check the search terms they go after and we never say; hand the live ones to ads and SEO",
            "owner": "agent",
            "artefact": {"kind": "research_note", "label": "a keyword check brief", "draft": audit.searchmod.draft(s, m["brand"].capitalize())},
            "steps": _steps(("agent", "Take the seed list: gaps first, then contested terms."),
                            ("agent", "Check volume and cost per click once a keyword source is connected; until then, mark them unchecked."),
                            ("agent", "Hand the terms with volume to the Google Ads and SEO screens as a brief.")),
            "size": {"text": f"{sum(1 for r in s['rows'] if not r['ours'])} terms to check"},
            "win_rule": None, "stop_rule": None, "check_on": _plus(f["last_seen"], 14), "time_to_ship_hours": 1}


def act_new_move(f: dict, m: dict) -> dict:
    """COMP-R24: a direct competitor started a new offer or angle. Brief our counter from our own proof."""
    what = f["entity"]["label"]
    draft = "\n".join([f"Counter brief: {what}.", f"Seen: {f['sentence']}",
                       f"Our top angles: {', '.join(m['our_top_angles'])}. Our proof: {', '.join(audit.covmod.proof_points(m['brain'])[:2]) or 'none on file'}.",
                       "Answer in 2 ads within 7 days if it overlaps our angles; otherwise log it and watch the next capture.",
                       NEVER_COPY])
    return {"title": f"Brief our counter: {what}", "owner": "agent_drafts",
            "artefact": {"kind": "ad_brief", "label": "a counter brief: 2 ads", "draft": draft},
            "steps": _steps(("agent", "Read the new move by page id at the next capture."),
                            ("agent", "Decide overlap with our angles by rule; draft 2 counter ads if it overlaps."),
                            ("person", "Approve the counter."),
                            ("agent", f"Check their move is still live on {_plus(f['last_seen'], 14)}.")),
            "size": {"text": "2 counter ads", "count": 2}, "win_rule": None, "stop_rule": None,
            "check_on": _plus(f["last_seen"], 14), "time_to_ship_hours": 4}


def act_price_cut(f: dict, m: dict) -> dict:
    """COMP-R25: a competitor cut its price. Answer with value, not a reflex match; the founder decides any price change."""
    page = f["entity"]["label"].replace(" price cut", "")
    draft = "\n".join([f"Answer to {page}'s price cut: {f['sentence']}",
                       "Do not match by reflex. First: watch our add to cart and conversion on the overlapping packs for 7 days.",
                       "Now: add price per pair and the guarantee line to the overlapping pack cards; 1 ad on price per wear.",
                       "If conversion drops 10 percent: the founder decides on a pack step, not a code."])
    return {"title": f"Answer {page}'s price cut with value; no reflex match", "owner": "agent_drafts",
            "artefact": {"kind": "copy", "label": "value framing for the overlapping packs, and a watch rule", "draft": draft},
            "steps": _steps(("agent", "Find our packs within 20 percent of their new price per pair."),
                            ("agent", "Draft price per pair and guarantee lines for those cards and 1 price per wear ad."),
                            ("person", "Approve the copy. The founder owns any price change."),
                            ("agent", f"Watch add to cart on those packs for 7 days; report on {_plus(f['last_seen'], 7)}.")),
            "size": None, "win_rule": "Conversion on the overlapping packs holds within 5 percent",
            "stop_rule": "Conversion down 10 percent for 5 days: escalate to the founder", "check_on": _plus(f["last_seen"], 7),
            "time_to_ship_hours": 3}


def act_landing(f: dict, m: dict) -> dict:
    """COMP-R26: start weekly landing page tracking for the top threats (public read)."""
    rows = [r for r in m["landing"]["rows"] if not r["tracked"]]
    return {"title": f"Start weekly landing page tracking for {len(rows)} top threats", "owner": "agent",
            "artefact": {"kind": "research_note", "label": "a tracking plan and the first dated capture",
                         "draft": audit.landmod.plan_text(rows)},
            "steps": _steps(("agent", "Visit each watch url (public read) and store the first dated capture."),
                            ("agent", "Diff weekly: headline, offer, guarantee, best seller price per pair, new collections."),
                            ("agent", "Raise an alert on the changes timeline when a rule crosses.")),
            "size": {"text": f"{sum(len(r['urls']) for r in rows)} urls a week"}, "win_rule": None, "stop_rule": None,
            "check_on": _plus(f["last_seen"], 7), "time_to_ship_hours": 2}


def act_card(f: dict, m: dict) -> dict:
    """COMP-R27: a stale battlecard. The agent re-verifies each fact against a fresh capture and refreshes the card."""
    page = f["entity"]["label"].replace(" battlecard", "")
    return {"title": f"Re-verify the {page} battlecard before support uses it again", "owner": "agent",
            "artefact": {"kind": "copy", "label": f"a refreshed {page} battlecard with dates", "draft": None,
                         "draft_note": "Drafted from the next capture."},
            "steps": _steps(("agent", f"Pull a fresh capture of {page} (page id, inside the caps) and its price feed."),
                            ("agent", "Check each line of the card; drop what no longer holds; date the rest."),
                            ("agent", "Publish the refreshed card to the support macros.")),
            "size": None, "win_rule": None, "stop_rule": None, "check_on": _plus(f["last_seen"], 7), "time_to_ship_hours": 1}


def act_frames(f: dict, m: dict) -> dict:
    """COMP-R28: test the positioning line against the top shopper frame before rewriting it."""
    fr = m["frames"]
    return {"title": f"Test our line against the {fr['top']['label']} frame shoppers use", "owner": "agent_drafts",
            "artefact": {"kind": "test_brief", "label": "a positioning test: the current line against the frame lines",
                         "draft": audit.framemod.draft(fr)},
            "steps": _steps(("agent", "Build the lines from the brain: current, the top frame with its proof, the contested corner."),
                            ("person", "Approve the lines; every claim has its proof on file."),
                            ("agent", "Run the 5-second poll with 200 shoppers, then the winner as an ad first line for 7 days."),
                            ("person", "Approve the winning line as a brain record.")),
            "size": {"text": "200 shoppers, 2 ad lines"}, "win_rule": "The new line wins the poll by 10 points and the ad test",
            "stop_rule": "No line beats the current one by 5 points", "check_on": _plus(f["last_seen"], 21), "time_to_ship_hours": 6}


def act_connect(f: dict, m: dict) -> dict:
    un = f.get("unavailable") or {}
    con = un.get("connector") or "the missing source"
    return {"title": f"Connect {con} so {f['rule_id']} can run", "owner": "person",
            "artefact": {"kind": "connector_setup", "label": f"{con}, read-only", "draft": None},
            "steps": _steps(("person", un.get("fix") or "Connect the source in Setup, read-only."),
                            ("agent", f"Pull the window and run {f['rule_id']} again."),
                            ("agent", "Report the finding here with its evidence.")),
            "size": None, "win_rule": None, "stop_rule": None, "check_on": _plus(f["last_seen"], 7),
            "time_to_ship_hours": 1}


BUILDERS = {"COMP-R01": act_angle, "COMP-R02": act_price, "COMP-R03": act_offer_run, "COMP-R04": act_lookalike,
            "COMP-R05": act_coverage, "COMP-R06": act_first_line, "COMP-R07": act_offer_gap, "COMP-R08": act_discount,
            "COMP-R09": act_ladder, "COMP-R10": act_above, "COMP-R11": act_corner,
            "COMP-R12": act_refresh, "COMP-R13": act_no_id, "COMP-R14": act_stale,
            "COMP-R15": act_lost, "COMP-R16": act_connect,
            "COMP-R17": act_attack, "COMP-R18": act_undercut,
            "COMP-R19": act_velocity, "COMP-R20": act_niche,
            "COMP-R21": act_premium, "COMP-R22": act_search, "COMP-R23": act_connect,
            "COMP-R24": act_new_move, "COMP-R25": act_price_cut,
            "COMP-R26": act_landing, "COMP-R27": act_card,
            "COMP-R28": act_frames}   # R16 has no data source yet: always a connect action


def action(f: dict, m: dict, net_revenue: float | None) -> dict:
    fn = act_connect if f.get("status") == "unavailable" else BUILDERS.get(f["rule_id"])
    if fn is None:
        return ranker.action_from_finding(f, net_revenue)
    parts = fn(f, m)
    a = {"id": f["id"], "finding_ids": [f["id"]], "screen": audit.SCREEN, "rule_id": f["rule_id"],
         "why": f["sentence"], "severity": f["severity"], "status": f["status"], "confidence": f["confidence"],
         "entity": f["entity"], "capability": f["capability"], "money_at_stake": f.get("money_at_stake"),
         "brain_refs": f.get("brain_refs") or [], "first_seen": f["first_seen"], "last_seen": f["last_seen"],
         "evidence": f.get("evidence") or [], "decision": None}
    a.update(parts)
    a["rubric"] = ranker.score(dict(f, capability=f["capability"], owner=a["owner"]), net_revenue)
    a["rubric"].update(audit.RUBRIC_OVERRIDES.get(f["rule_id"], {}))
    # ease follows the owner this builder chose, not only the capability (depth.md section 4)
    if f.get("status") != "unavailable":
        a["rubric"]["ease"] = {"agent": 5, "agent_drafts": 4, "person": 3 if (a["artefact"] or {}).get("draft") else 2}[a["owner"]]
    a["rubric"]["total"] = round(sum(w * (a["rubric"][k] if a["rubric"][k] is not None else 2.5) / 5
                                     for k, w in ranker.WEIGHTS.items()), 1)
    return a


def build(brand: str, window: dict | None = None, root: Path | None = None) -> dict:
    window = window or ranker.default_window()
    findings = audit.run(brand, window, root)
    today = dt.date.fromisoformat(window["ends_on"]) + dt.timedelta(days=1)
    m = audit.market_full(brand, today, root)
    nr = ranker.net_revenue_28d(brand, window)
    acts = [action(f, m, nr) for f in findings if f.get("status") in ("open", "unavailable")]
    acts = [a for a in acts if not ranker.validate_action(a)]
    acts.sort(key=ranker.sort_key)
    return {"screen": audit.SCREEN, "brand": brand, "window": window, "simulated": True,
            "brain_version": m["brain"].version(), "net_revenue_28d": nr, "findings": findings, "actions": acts}
