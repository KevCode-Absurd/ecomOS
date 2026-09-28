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
        "title": f"Make 3 ads that lead with {angle['label']}, the angle no tracked brand runs",
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
            "COMP-R05": act_coverage}


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
    m = audit.market(brand, today, root)
    nr = ranker.net_revenue_28d(brand, window)
    acts = [action(f, m, nr) for f in findings if f.get("status") in ("open", "unavailable")]
    acts = [a for a in acts if not ranker.validate_action(a)]
    acts.sort(key=ranker.sort_key)
    return {"screen": audit.SCREEN, "brand": brand, "window": window, "simulated": True,
            "brain_version": m["brain"].version(), "net_revenue_28d": nr, "findings": findings, "actions": acts}
