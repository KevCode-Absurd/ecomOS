"""Rank: findings to rubric-scored actions, and the master list across screens.

Contract: app/contracts/depth.md sections 4 and 5. Every screen gets
`GET /api/<slug>/rank` for free from this module: it runs the screen's
audit.py, turns each finding into an action with an owner, steps, an
artefact and the six rubric scores, and sorts them. A screen overrides by
exporting `rank(brand, window)` from its api.py or audit.py; the server
prefers that and still validates the shape here.

`master(brand, window)` merges every screen's actions into one list,
applies snoozes from data/decisions.json, and groups bottlenecks.

No model call. Same tables, brain version and window give the same output.
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import json
import re
import sys
from pathlib import Path

APP = Path(__file__).resolve().parent
SCREENS = APP / "screens"
DECISIONS = APP / "data" / "decisions.json"
CATALOGUE = APP.parent / "agents" / "catalogue.json"

WEIGHTS = {"revenue": 30, "profit": 20, "reputation": 15, "satisfaction": 15, "ease": 10, "confidence": 10}
SEV_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
SEV_SCORE = {"critical": 4, "high": 3, "medium": 2, "low": 1}
OWNER_BY_AUTONOMY = {"agent_does": "agent", "agent": "agent", "founder_gate": "agent_drafts", "human_assist": "person"}
OWNERS = ("agent", "agent_drafts", "person")
SNOOZE_DAYS = 14
ARTEFACT_KINDS = ("ad_brief", "creative", "copy", "page_section", "landing_page", "offer", "price_change", "email", "flow",
                  "test_brief", "listing_fix", "feed_fix", "budget_move", "bid_change", "connector_setup", "brain_record",
                  "policy", "research_note", "ticket", "report")

# stage of the pipeline an entity type or screen sits at, upstream first (audit.md section 6)
UPSTREAM = {"brand": 0, "campaign": 1, "adset": 1, "ad": 1, "metric": 2, "page": 3, "device": 3, "sku": 4, "offer": 4,
            "ladder_rung": 4, "flow": 5, "stage": 2}
COST_SIDE = {"returns", "chargeback", "refund", "fee", "shipping", "inventory", "stock", "cogs", "payout", "dispute"}
REPUTATION_5 = {"claim", "disclosure", "forbidden", "policy", "legal", "privacy", "map ", "reseller", "competitor position", "positioning gap"}
REPUTATION_4 = {"one-star", "deal-breaker", "deal breaker", "review"}
REPUTATION_3 = {"copy", "creative", "positioning", "hook", "angle", "voice"}
SATISFACTION_5 = {"checkout", "mobile", "speed", "lcp", "stock-out", "stockout", "out of stock", "ticket", "backlog", "delivery", "broken"}
SATISFACTION_4 = {"return", "cx", "complaint", "refund", "support"}
SATISFACTION_3 = {"email", "flow", "post-purchase", "post purchase", "sms"}
SATISFACTION_2 = {"ad", "campaign", "spend", "roas", "cpa", "keyword", "bid"}

# default artefact by capability prefix, then by screen
ARTEFACT_BY_PREFIX = {"CREA": "ad_brief", "MEDIA": "budget_move", "SITE": "page_section", "LIFE": "offer", "BRAND": "brain_record",
                      "PROD": "listing_fix", "MONEY": "report", "ORG": "ticket", "BRN": "brain_record", "QA": "ticket",
                      "DIAG": "research_note", "PROP": "test_brief", "REG": "research_note", "ORCH": "report", "SCT": "policy"}
ARTEFACT_BY_SCREEN = {"09-creative": "ad_brief", "10-copy": "copy", "11-paid-social": "budget_move", "12-google-ads": "bid_change",
                      "13-affiliate-marketplace-ads": "budget_move", "14-email-messaging": "email", "15-customers-cx": "ticket",
                      "07-landing-pages-cro": "page_section", "08-site-speed": "ticket", "04-offers-pricing": "offer",
                      "19-supply-inventory": "ticket", "20-marketplaces": "listing_fix", "17-seo": "page_section",
                      "16-organic-content": "copy", "18-answer-engines": "page_section", "21-finance-cash": "report",
                      "22-measurement": "connector_setup", "24-security": "policy", "25-experiments": "test_brief",
                      "01-market-research": "research_note", "02-customers-avatars": "brain_record", "03-competitors": "research_note",
                      "05-brand-brain": "brain_record", "26-reports": "report", "27-wild-bets-pr": "research_note",
                      "23-team-ops": "ticket", "06-store-health": "ticket", "00-today": "report"}
ARTEFACT_LABEL = {"ad_brief": "an ad brief", "creative": "a creative", "copy": "copy", "page_section": "a page section",
                  "landing_page": "a landing page", "offer": "an offer spec", "price_change": "a price change", "email": "an email draft",
                  "flow": "a flow", "test_brief": "a test brief", "listing_fix": "a listing fix", "feed_fix": "a feed fix",
                  "budget_move": "a budget move", "bid_change": "a bid change", "connector_setup": "a connector set up",
                  "brain_record": "a brain record", "policy": "a policy change", "research_note": "a research note",
                  "ticket": "a ticket with the fix", "report": "a report"}

_catalogue: dict | None = None


def catalogue() -> dict:
    global _catalogue
    if _catalogue is None:
        try:
            rows = json.loads(CATALOGUE.read_text(encoding="utf-8"))
            _catalogue = {r["id"]: {"name": r.get("name") or r["id"], "autonomy": r.get("autonomy") or "human_assist",
                                    "external_write": bool((r.get("external_write") or {}).get("needed"))} for r in rows}
        except (OSError, ValueError, KeyError):
            _catalogue = {}
    return _catalogue


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def screen_slugs(root: Path = SCREENS) -> list[str]:
    return sorted(d.name for d in root.iterdir() if d.is_dir() and re.match(r"^\d{2}-[a-z0-9-]+$", d.name) and (d / "audit.py").is_file())


def default_window(days: int = 28, ends_on: str | None = None) -> dict:
    end = dt.date.fromisoformat(ends_on) if ends_on else dt.date.today() - dt.timedelta(days=1)
    return {"ends_on": end.isoformat(), "days": days, "trailing": 4}


# ---------------------------------------------------------------- scoring

def _ladder(share: float | None) -> int | None:
    if share is None:
        return None
    if share >= 0.05:
        return 5
    if share >= 0.02:
        return 4
    if share >= 0.01:
        return 3
    if share >= 0.005:
        return 2
    return 1 if share > 0 else 0


def _text(f: dict) -> str:
    ent = f.get("entity") or {}
    return " ".join(str(x or "") for x in [f.get("sentence"), f.get("rule_id"), ent.get("type"), ent.get("label"), f.get("screen")]).lower()


def _has(text: str, words: set[str]) -> bool:
    return any(w in text for w in words)


def score(f: dict, net_revenue_28d: float | None) -> dict:
    """The six rubric dimensions, 0 to 5, from finding fields only (depth.md section 4)."""
    sev = f.get("severity") or "medium"
    money = f.get("money_at_stake") or {}
    usd = money.get("usd") if isinstance(money.get("usd"), (int, float)) else None
    usd_rev = money.get("usd_revenue") if isinstance(money.get("usd_revenue"), (int, float)) else None
    margin_known = usd_rev is not None
    rev_amount = usd_rev if margin_known else usd
    share = (rev_amount / net_revenue_28d) if (rev_amount is not None and net_revenue_28d) else None
    revenue = _ladder(share) if share is not None else SEV_SCORE.get(sev, 2)
    text = _text(f)
    if margin_known and usd is not None and net_revenue_28d:
        profit = _ladder(usd / net_revenue_28d)
    else:
        profit = max(1, revenue - 1)
    if _has(text, COST_SIDE):
        profit = min(5, profit + 1)
    if _has(text, REPUTATION_5):
        reputation = 5
    elif _has(text, REPUTATION_4):
        reputation = 4
    elif _has(text, REPUTATION_3):
        reputation = 3
    elif "site" in text or "page" in text:
        reputation = 2
    else:
        reputation = 1
    if _has(text, SATISFACTION_5):
        satisfaction = 5
    elif _has(text, SATISFACTION_4):
        satisfaction = 4
    elif _has(text, SATISFACTION_3):
        satisfaction = 3
    elif _has(text, SATISFACTION_2):
        satisfaction = 2
    else:
        satisfaction = 1
    owner = owner_of(f)
    if f.get("status") == "unavailable":
        ease = 1
    elif owner == "agent":
        ease = 5
    elif owner == "agent_drafts":
        ease = 4
    else:
        ease = 2
    conf = f.get("confidence")
    confidence = int(round(conf * 5)) if isinstance(conf, (int, float)) else None
    r = {"revenue": revenue, "profit": profit, "reputation": reputation, "satisfaction": satisfaction, "ease": ease, "confidence": confidence}
    total = 0.0
    for k, w in WEIGHTS.items():
        v = r[k] if r[k] is not None else 2.5   # neutral when unknown, written down in depth.md rule 7
        total += w * v / 5
    r["total"] = round(total, 1)
    return r


def owner_of(f: dict) -> str:
    cap = f.get("capability") or {}
    autonomy = cap.get("autonomy") if isinstance(cap, dict) else None
    if f.get("status") == "unavailable":
        return "person"
    owner = OWNER_BY_AUTONOMY.get(autonomy or "", None)
    if owner is None:
        cid = cap.get("id") if isinstance(cap, dict) else cap
        owner = OWNER_BY_AUTONOMY.get(catalogue().get(cid, {}).get("autonomy", ""), "person")
    cid = cap.get("id") if isinstance(cap, dict) else None
    if owner == "agent" and catalogue().get(cid, {}).get("external_write"):
        owner = "agent_drafts"   # any external write is drafted and approved until Kevin lifts it
    return owner


# ---------------------------------------------------------------- action building

def _artefact_kind(f: dict) -> str:
    if f.get("status") == "unavailable":
        return "connector_setup"
    cap = f.get("capability") or {}
    cid = cap.get("id") if isinstance(cap, dict) else str(cap or "")
    prefix = cid.split("-")[0] if cid else ""
    return ARTEFACT_BY_SCREEN.get(f.get("screen"), None) or ARTEFACT_BY_PREFIX.get(prefix, "research_note")


def _title(f: dict, cap_name: str, rule_name: str = "") -> str:
    """Default title: the rule's own name when the audit lists one, else the capability name, plus the entity."""
    ent = f.get("entity") or {}
    label = ent.get("label") or ent.get("id") or ""
    if rule_name and f.get("status") != "unavailable":
        cap_name = rule_name
    if f.get("status") == "unavailable":
        un = f.get("unavailable") or {}
        con = un.get("connector") or "the missing source"
        return f"Connect {con} so this rule can run" + (f" on {label}" if label and ent.get("type") != "brand" else "")
    name = (cap_name or "Fix this").split(" (")[0]
    name = name[0].upper() + name[1:]
    if len(label) > 60:
        label = label[:57].rstrip() + "..."
    if label and ent.get("type") not in ("brand", None) and label.lower() not in name.lower():
        name = f"{name}: {label}"
    return name if len(name) <= 96 else name[:93].rstrip() + "..."


def _steps(f: dict, owner: str, kind: str) -> list[dict]:
    ent = f.get("entity") or {}
    label = ent.get("label") or ent.get("id") or "the entity"
    if f.get("status") == "unavailable":
        un = f.get("unavailable") or {}
        fix = un.get("fix") or "Connect the source in Setup, read-only."
        return [{"n": 1, "who": "person", "text": fix},
                {"n": 2, "who": "agent", "text": f"Pull the window and run {f.get('rule_id')} again."},
                {"n": 3, "who": "agent", "text": "Report the finding here with its evidence."}]
    art = ARTEFACT_LABEL.get(kind, "the artefact")
    first = "agent" if owner != "person" else "person"
    steps = [{"n": 1, "who": "agent", "text": f"Read the evidence rows and the brain records for {label}."},
             {"n": 2, "who": first, "text": f"Draft {art} that closes the gap the rule found."}]
    if owner == "agent_drafts":
        steps.append({"n": 3, "who": "person", "text": "Approve the draft. Nothing ships before that."})
    elif owner == "person":
        steps.append({"n": 3, "who": "person", "text": f"Ship {art} and mark it done here."})
    else:
        steps.append({"n": 3, "who": "agent", "text": f"Ship {art} and log it in the experiment registry."})
    steps.append({"n": len(steps) + 1, "who": "agent", "text": "Re-run the rule on the next window. The finding resolves when the number recovers."})
    return steps


def action_from_finding(f: dict, net_revenue_28d: float | None = None, rule_names: dict | None = None) -> dict:
    cap = f.get("capability") or {}
    cid = cap.get("id") if isinstance(cap, dict) else str(cap or "")
    cat = catalogue().get(cid, {})
    rule_name = (rule_names or {}).get(f.get("rule_id"), "")
    owner = owner_of(f)
    kind = _artefact_kind(f)
    un = f.get("unavailable") or {}
    end = f.get("last_seen") or f.get("first_seen")
    check_on = None
    if end:
        try:
            check_on = (dt.date.fromisoformat(str(end)[:10]) + dt.timedelta(days=7)).isoformat()
        except ValueError:
            check_on = None
    return {
        "id": f["id"], "finding_ids": [f["id"]], "screen": f.get("screen"), "rule_id": f.get("rule_id"),
        "title": _title(f, cat.get("name", ""), rule_name), "why": f.get("sentence") or "",
        "severity": f.get("severity") or "medium", "status": f.get("status") or "open", "confidence": f.get("confidence"),
        "entity": f.get("entity"), "capability": {"id": cid, "autonomy": (cap.get("autonomy") if isinstance(cap, dict) else None) or cat.get("autonomy")},
        "owner": owner,
        "artefact": {"kind": kind, "label": (f"{un.get('connector') or 'the source'} connected, read-only" if kind == "connector_setup" else ARTEFACT_LABEL.get(kind, kind)), "draft": None},
        "steps": _steps(f, owner, kind),
        "size": None, "stop_rule": None, "check_on": check_on, "time_to_ship_hours": {"agent": 2, "agent_drafts": 4, "person": 8}[owner],
        "rubric": score(f, net_revenue_28d),
        "money_at_stake": f.get("money_at_stake"), "brain_refs": f.get("brain_refs") or [],
        "first_seen": f.get("first_seen"), "last_seen": f.get("last_seen"), "decision": None,
    }


def sort_key(a: dict):
    m = a.get("money_at_stake") or {}
    usd = m.get("usd") if isinstance(m.get("usd"), (int, float)) else None
    days_open = 0
    try:
        if a.get("first_seen") and a.get("last_seen"):
            days_open = (dt.date.fromisoformat(str(a["last_seen"])[:10]) - dt.date.fromisoformat(str(a["first_seen"])[:10])).days
    except ValueError:
        days_open = 0
    ent = a.get("entity") or {}
    pinned = 0 if a.get("severity") == "critical" else 1
    return (pinned, -(usd or 0) if pinned == 0 else 0, -float((a.get("rubric") or {}).get("total") or 0), SEV_ORDER.get(a.get("severity"), 9),
            0 if usd is not None else 1, -(usd or 0), -days_open, UPSTREAM.get(ent.get("type"), 9), a.get("id") or "")


def validate_action(a: dict) -> list[str]:
    errs = []
    for k in ("id", "title", "why", "severity", "owner", "artefact", "steps", "rubric", "capability", "finding_ids"):
        if k not in a:
            errs.append(f"missing {k}")
    if a.get("owner") not in OWNERS:
        errs.append("owner must be agent, agent_drafts or person")
    steps = a.get("steps") or []
    if not (2 <= len(steps) <= 8) or any("who" not in s or "text" not in s for s in steps):
        errs.append("steps must be 2 to 8 entries with who and text")
    art = a.get("artefact") or {}
    if not art.get("kind"):
        errs.append("artefact.kind missing")
    r = a.get("rubric") or {}
    if not isinstance(r.get("total"), (int, float)):
        errs.append("rubric.total missing")
    return errs


# ---------------------------------------------------------------- running

def net_revenue_28d(brand: str, window: dict | None = None) -> float | None:
    """Trailing 28-day net sales from the brand's daily aggregate, ending on the window end. None when absent, never 0."""
    p = APP / "data" / "brands" / brand / "aggregates" / "daily.json"
    if not p.is_file():
        return None
    try:
        rows = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    rows = rows.get("rows") if isinstance(rows, dict) else rows
    if not isinstance(rows, list):
        return None
    end = (window or {}).get("ends_on")
    days = [r for r in rows if isinstance(r, dict) and isinstance(r.get("net_sales"), (int, float)) and (not end or str(r.get("date", ""))[:10] <= end)]
    days = days[-28:]
    if len(days) < 28:
        return None
    return float(sum(r["net_sales"] for r in days))


def load_findings(slug: str, brand: str, window: dict, root: Path = SCREENS) -> list[dict]:
    mod = _load(f"rank_audit_{slug.replace('-', '_')}", root / slug / "audit.py")
    return list(mod.run(brand, window))


def rule_names(slug: str, root: Path = SCREENS) -> dict:
    """rule_id to the rule's name from the screen's audit RULES list, for default titles."""
    mod = sys.modules.get(f"rank_audit_{slug.replace('-', '_')}")
    if mod is None:
        try:
            mod = _load(f"rank_audit_{slug.replace('-', '_')}", root / slug / "audit.py")
        except Exception:  # noqa: BLE001
            return {}
    out = {}
    for r in getattr(mod, "RULES", []) or []:
        if isinstance(r, dict) and r.get("rule_id") and r.get("name"):
            out[r["rule_id"]] = str(r["name"])
    return out


def screen_override(slug: str, root: Path = SCREENS):
    for fname in ("api.py", "audit.py"):
        p = root / slug / fname
        if not p.is_file():
            continue
        try:
            mod = sys.modules.get(f"rank_over_{slug.replace('-', '_')}_{fname[:-3]}") or _load(f"rank_over_{slug.replace('-', '_')}_{fname[:-3]}", p)
        except Exception:  # noqa: BLE001
            continue
        if callable(getattr(mod, "rank", None)):
            return mod.rank
    return None


def rank(slug: str, brand: str = "bombas", window: dict | None = None, root: Path = SCREENS, use_override: bool = True) -> dict:
    window = window or default_window()
    nr = net_revenue_28d(brand, window)
    actions = None
    source = "default"
    if use_override:
        over = screen_override(slug, root)
        if over is not None:
            try:
                out = over(brand, window)
                actions = out.get("actions") if isinstance(out, dict) else out
                source = "screen"
            except Exception:  # noqa: BLE001
                actions = None
    if actions is None:
        findings = load_findings(slug, brand, window, root)
        names = rule_names(slug, root)
        actions = [action_from_finding(f, nr, names) for f in findings if f.get("status") in ("open", "unavailable", None)]
    good = []
    for a in actions:
        if "rubric" not in a and a.get("finding_ids"):
            a["rubric"] = score(a, nr)
        a.setdefault("screen", slug)
        if not validate_action(a):
            good.append(a)
    good.sort(key=sort_key)
    try:
        sys.path.insert(0, str(APP / "brain"))
        from store import Brain  # noqa: WPS433
        version = Brain(brand).version()
    except Exception:  # noqa: BLE001
        version = None
    return {"screen": slug, "brand": brand, "window": window, "computed_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "brain_version": version, "simulated": True, "source": source, "net_revenue_28d": nr, "actions": good}


def decisions_by_finding(path: Path = DECISIONS) -> dict:
    try:
        rows = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    out = {}
    for r in rows if isinstance(rows, list) else []:
        key = r.get("finding_id") or (r.get("screen"), r.get("capability"))
        out[key] = r
    return out


def apply_decisions(actions: list[dict], today: dt.date | None = None, path: Path = DECISIONS) -> list[dict]:
    today = today or dt.date.today()
    dec = decisions_by_finding(path)
    kept = []
    for a in actions:
        d = dec.get(a["id"]) or dec.get((a.get("screen"), (a.get("capability") or {}).get("id")))
        if d:
            a["decision"] = {"choice": d.get("choice"), "time": d.get("time"), "reason": d.get("reason")}
            if d.get("choice") == "not_now":
                try:
                    when = dt.date.fromisoformat(str(d.get("time"))[:10])
                    if (today - when).days < SNOOZE_DAYS:
                        a["status"] = "snoozed"
                        continue
                except ValueError:
                    pass
        kept.append(a)
    return kept


def master(brand: str = "bombas", window: dict | None = None, root: Path = SCREENS, top: int = 10, decisions_path: Path = DECISIONS) -> dict:
    window = window or default_window()
    by_id: dict[str, dict] = {}
    screens = []
    for slug in screen_slugs(root):
        try:
            r = rank(slug, brand, window, root)
        except Exception as exc:  # noqa: BLE001
            screens.append({"screen": slug, "actions": 0, "error": type(exc).__name__})
            continue
        screens.append({"screen": slug, "actions": len(r["actions"]), "source": r["source"]})
        for a in r["actions"]:
            if a["id"] not in by_id:
                by_id[a["id"]] = a
    actions = apply_decisions(list(by_id.values()), path=decisions_path)
    actions.sort(key=sort_key)
    # bottlenecks: group by screen, rank groups by the sum of totals of open actions
    groups: dict[str, dict] = {}
    for a in actions:
        g = groups.setdefault(a["screen"], {"screen": a["screen"], "open": 0, "unavailable": 0, "critical": 0, "stake_usd": 0.0, "stake_known": False, "score": 0.0, "top": None})
        if a.get("status") == "unavailable":
            g["unavailable"] += 1
        else:
            g["open"] += 1
        if a.get("severity") == "critical":
            g["critical"] += 1
        m = a.get("money_at_stake") or {}
        if isinstance(m.get("usd"), (int, float)):
            g["stake_usd"] += m["usd"]
            g["stake_known"] = True
        g["score"] += float((a.get("rubric") or {}).get("total") or 0)
        if g["top"] is None:
            g["top"] = {"id": a["id"], "title": a["title"], "owner": a["owner"]}
    bottlenecks = sorted(groups.values(), key=lambda g: (-g["critical"], -g["score"]))
    for g in bottlenecks:
        if not g["stake_known"]:
            g["stake_usd"] = None
        g["score"] = round(g["score"], 1)
        g.pop("stake_known", None)
    counts = {"actions": len(actions), "open": sum(1 for a in actions if a.get("status") != "unavailable"),
              "unavailable": sum(1 for a in actions if a.get("status") == "unavailable"),
              "snoozed": len(by_id) - len(actions), "screens": len(screens),
              "by_owner": {o: sum(1 for a in actions if a["owner"] == o) for o in OWNERS}}
    stake = [a["money_at_stake"]["usd"] for a in actions if isinstance((a.get("money_at_stake") or {}).get("usd"), (int, float))]
    open_actions = [a for a in actions if a.get("status") != "unavailable"]
    connect = [a for a in actions if a.get("status") == "unavailable"]
    return {"brand": brand, "window": window, "computed_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "simulated": True, "rubric_weights": WEIGHTS, "counts": counts, "stake_usd": sum(stake) if stake else None,
            "net_revenue_28d": net_revenue_28d(brand, window),
            "screens": screens, "bottlenecks": bottlenecks, "top": open_actions[:top], "connect": connect[:top], "actions": actions}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="rank one screen or the master list")
    ap.add_argument("--screen", help="slug like 11-paid-social; omit for the master list")
    ap.add_argument("--brand", default="bombas")
    ap.add_argument("--ends-on")
    ap.add_argument("--days", type=int, default=28)
    ns = ap.parse_args()
    w = default_window(ns.days, ns.ends_on)
    out = rank(ns.screen, ns.brand, w) if ns.screen else master(ns.brand, w)
    print(json.dumps(out, indent=1)[:20000])
