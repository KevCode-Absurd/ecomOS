"""Peak readiness: the peaks in the next 90 days against what the brain holds for each, ending in asks and briefs.

The US retail peaks are computed from the date (Black Friday is the day after the 4th Thursday of November, Cyber
Monday 3 days on, Giving Tuesday the day after that, the holiday order-by date is 25 December less the slowest
standard shipping promise). Amazon's October deal days are listed with an unavailable date until Amazon announces
them. The brand's own calendar records with a date inside the window join the list. The seasonality index in
assumptions.json names the heavy months. For each peak, checks read the brain: an offer decided for it (a founder
`offers.peak_<key>` record), the holiday return window, the shipping cutoff, gift cards, the giving story and its
claim tier, seasonal creative in our own ads, the pricing disclosure check, the listings on Amazon. A check is ok,
a gap (a decision or a brief) or unavailable (a source is missing). Readiness is ok over ok plus gaps; unavailable
never counts as a gap. Rule BRN-R26 puts a peak with gaps on the master list, high when it is 30 days out or less.
Nothing here forecasts: dates are arithmetic, checks are record lookups, and a decision writes a founder record.
"""
from __future__ import annotations

import datetime as dt
import re

HORIZON_DAYS = 90
SURFACE_LABEL = {"sale": "site, email, ads", "gifting": "site, email, ads, CX", "mission": "email, ads, site", "marketplace": "Amazon listings", "event": "site, email, ads"}


def thanksgiving(year: int) -> dt.date:
    d = dt.date(year, 11, 1)
    first_thu = d + dt.timedelta(days=(3 - d.weekday()) % 7)
    return first_thu + dt.timedelta(days=21)


def _business_days_before(end: dt.date, n: int) -> dt.date:
    d = end
    left = n
    while left > 0:
        d -= dt.timedelta(days=1)
        if d.weekday() < 5:
            left -= 1
    return d


def _max_days(text) -> int | None:
    nums = [int(x) for x in re.findall(r"\d+", str(text or ""))]
    return max(nums) if nums else None


def _rec(brain, section, field):
    rows = [r for r in brain.records(section) if r.get("field") == field]
    rows.sort(key=lambda r: ({"approved": 0, "site_backed": 1}.get(r["tier"], 2), r["id"]))
    return rows[0] if rows else None


def _text(r) -> str:
    return (r.get("text") if isinstance(r.get("text"), str) else str(r.get("value") or "")) if r else ""


def calendar(brain, angles_of=None) -> list[dict]:
    """The peaks in the window, US by default, plus the brand's own dated calendar records."""
    today = brain.today
    out = []
    for year in (today.year, today.year + 1):
        tg = thanksgiving(year)
        bf = tg + dt.timedelta(days=1)
        out += [
            {"key": f"black_friday_{year}", "label": "Black Friday", "date": bf, "kind": "sale", "why": "the year's biggest discount day; the offer, the stack with the first order code and the return window are decided before it"},
            {"key": f"cyber_monday_{year}", "label": "Cyber Monday", "date": bf + dt.timedelta(days=3), "kind": "sale", "why": "the online peak of the same weekend; a second offer or the same one, decided with Black Friday"},
            {"key": f"giving_tuesday_{year}", "label": "Giving Tuesday", "date": bf + dt.timedelta(days=4), "kind": "mission", "why": "a day the giving story earns attention without a discount"},
            {"key": f"holiday_orderby_{year}", "label": "Holiday order-by date", "date": None, "kind": "gifting", "why": "the last day standard shipping lands before 25 December; gift buyers need it on the site and in email"},
            {"key": f"christmas_{year}", "label": "Christmas", "date": dt.date(year, 12, 25), "kind": "gifting", "why": "gift cards carry the sales after the order-by date; returns run on the holiday window"},
            {"key": f"prime_deal_days_{year}", "label": "Amazon October deal days", "date": None, "kind": "marketplace", "window": f"early to mid October {year}", "estimated": True, "why": "Amazon's autumn deal event; listings, prices and stock on the marketplace are checked before it"},
            {"key": f"valentines_{year}", "label": "Valentine's Day", "date": dt.date(year, 2, 14), "kind": "gifting", "why": "a gifting peak for small, packable products"},
            {"key": f"mothers_day_{year}", "label": "Mother's Day", "date": dt.date(year, 5, 1) + dt.timedelta(days=(6 - dt.date(year, 5, 1).weekday()) % 7 + 7), "kind": "gifting", "why": "the spring gifting peak"},
            {"key": f"fathers_day_{year}", "label": "Father's Day", "date": dt.date(year, 6, 1) + dt.timedelta(days=(6 - dt.date(year, 6, 1).weekday()) % 7 + 14), "kind": "gifting", "why": "the early summer gifting peak"},
            {"key": f"back_to_school_{year}", "label": "Back to school", "date": dt.date(year, 8, 15), "kind": "sale", "why": "the August basics peak"},
        ]
    # the holiday order-by date from the slowest standard shipping promise
    so = _rec(brain, "policies", "shipping_options")
    slowest = None
    if so and isinstance(so.get("value"), list):
        days = [_max_days(o.get("business_days")) for o in so["value"] if isinstance(o, dict) and "standard" in str(o.get("name") or "").lower()]
        days = [d for d in days if d]
        slowest = max(days) if days else None
    for p in out:
        if p["key"].startswith("holiday_orderby_"):
            year = int(p["key"].rsplit("_", 1)[1])
            cutoff = _rec(brain, "policies", "holiday_shipping_cutoff")
            if cutoff and isinstance(cutoff.get("value"), str) and re.match(r"\d{4}-\d{2}-\d{2}$", cutoff["value"]) and cutoff["value"].startswith(str(year)):
                p["date"], p["derived"], p["source"] = dt.date.fromisoformat(cutoff["value"]), False, cutoff["id"]
            elif slowest:
                p["date"], p["derived"], p["source"] = _business_days_before(dt.date(year, 12, 25), slowest), True, so["id"]
                p["derivation"] = f"25 December less {slowest} business days, the slowest standard shipping promise on the site"
            else:
                p["derived"], p["source"] = None, None
    # prime deal days: an estimated window in October
    for p in out:
        if p["key"].startswith("prime_deal_days_"):
            year = int(p["key"].rsplit("_", 1)[1])
            p["window_start"], p["window_end"] = dt.date(year, 10, 6), dt.date(year, 10, 16)
    # the brand's own calendar records with a date in the window
    for r in brain.records("calendar"):
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        d = v.get("date") or (v.get("month") + "-15" if isinstance(v.get("month"), str) and re.match(r"\d{4}-\d{2}$", v.get("month")) else None)
        if isinstance(d, str) and re.match(r"\d{4}-\d{2}-\d{2}$", d) and (r.get("field") or "").startswith("peak_") is False:
            try:
                dd = dt.date.fromisoformat(d)
            except ValueError:
                continue
            if today <= dd <= today + dt.timedelta(days=HORIZON_DAYS):
                out.append({"key": r.get("field"), "label": v.get("event") or v.get("category") or (r.get("field") or "").replace("_", " "), "date": dd, "kind": "event", "own": True, "record": r["id"], "why": _text(r)[:160]})
    window = []
    for p in out:
        if p.get("date"):
            days_to = (p["date"] - today).days
            if 0 <= days_to <= HORIZON_DAYS:
                window.append(dict(p, days_to=days_to))
        elif p.get("window_start") and today <= p["window_end"] and (p["window_start"] - today).days <= HORIZON_DAYS:
            window.append(dict(p, days_to=None, days_to_window=max(0, (p["window_start"] - today).days)))
        elif p.get("derived") is None and p["key"].startswith("holiday_orderby_") and 0 <= (dt.date(int(p["key"].rsplit("_", 1)[1]), 12, 25) - today).days <= HORIZON_DAYS:
            window.append(dict(p, days_to=None, unavailable_reason="no standard shipping promise in the brain; the cutoff cannot be derived"))
    window.sort(key=lambda p: (p.get("days_to") if p.get("days_to") is not None else p.get("days_to_window", 10 ** 6), p["label"]))
    return window


def heavy_months(brain, assumptions_mod) -> dict:
    rows = assumptions_mod.load(brain) if assumptions_mod else []
    se = next((r for r in rows if r.get("field") == "seasonality"), None)
    if not se or not isinstance(se.get("value"), dict):
        return {"available": False, "reason": "no seasonality index in the assumptions", "months": []}
    mi = se["value"].get("monthly_index") or {}
    order = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    today = brain.today
    months = []
    for i in range(4):
        m = (today.month - 1 + i) % 12
        y = today.year + (today.month - 1 + i) // 12
        idx = mi.get(order[m])
        if isinstance(idx, (int, float)):
            months.append({"month": f"{y}-{m + 1:02d}", "label": order[m].capitalize(), "index": idx, "heavy": idx >= 1.2})
    return {"available": True, "months": months, "peaks": se["value"].get("peaks") or [], "status": se.get("status"), "reasoning": (se.get("reasoning") or "")[:200]}


def checks_for(brain, peak: dict, angles_of, legal_mod=None) -> list[dict]:
    kind = peak["kind"]
    key = peak["key"]
    out = []

    def add(ckey, label, status, evidence, fix, who, records=None, capability=None, note=None):
        out.append({"key": ckey, "label": label, "status": status, "evidence": evidence, "fix": fix, "who": who, "records": records or [], "capability": capability, "note": note})

    plan = _rec(brain, "offers", f"peak_{key}")
    if kind in ("sale", "gifting", "mission", "marketplace", "event") and not key.startswith("holiday_orderby"):
        if plan and isinstance(plan.get("value"), dict) and plan["value"].get("offer"):
            add("offer", "Offer decided", "ok", f"{plan['value']['offer']}" + (f" ({plan['value'].get('note')})" if plan["value"].get("note") else ""), None, "person", [plan["id"]])
        else:
            fo = _rec(brain, "offers", "first_order_code")
            stack = f" The first order code {fo['value'].get('code')} ({fo['value'].get('discount_pct')} percent) runs all year; decide whether it stacks." if fo and isinstance(fo.get("value"), dict) and kind == "sale" else ""
            add("offer", "Offer decided" if kind != "mission" else "Plan decided", "gap", "no offer record for this peak", f"Decide the {'offer' if kind != 'mission' else 'plan'} for {peak['label']} and write it here; every screen reads it." + stack, "person", [fo["id"]] if fo else [], "BRN-C07")
    if kind in ("sale", "gifting"):
        texts = " ".join(_text(r) for r in brain.records("policies") + brain.records("offers") if r.get("field") in ("returns_window_days", "guarantee", "happiness_guarantee", "holiday_returns", "returns_window_holiday_days"))
        m = re.search(r"(\d+)\s*days?\s+(?:for|on)\s+(?:[a-z-]+\s+){0,3}?(nov|dec|holiday|gift)", texts, re.I)
        hol = _rec(brain, "policies", "holiday_returns") or _rec(brain, "policies", "returns_window_holiday_days")
        if hol:
            add("returns_holiday", "Holiday return window", "ok", _text(hol)[:120], None, "person", [hol["id"]])
        elif m:
            add("returns_holiday", "Holiday return window", "ok", f"{m.group(1)} days for {m.group(2).lower()} purchases, from the guarantee text", None, "person", [r["id"] for r in brain.records("offers") if r.get("field") == "guarantee"][:1], note="read from the guarantee wording; confirm it as a policy record")
        else:
            add("returns_holiday", "Holiday return window", "gap", "no extended window on file", "Confirm the return window for gifts bought in November and December, and write it as a policy record.", "person", [], "BRN-C07")
    if kind == "gifting" or key.startswith("christmas") or key.startswith("holiday_orderby"):
        if peak.get("date") and key.startswith("holiday_orderby"):
            add("cutoff", "Shipping cutoff published", "ok" if not peak.get("derived") else "gap", peak["date"].isoformat() + (", derived: " + peak.get("derivation", "") if peak.get("derived") else ", set by you"),
                None if not peak.get("derived") else "Confirm the order-by date with the carrier promise and write it as a policy record; the site and email read it.", "person", [peak.get("source")] if peak.get("source") else [], "BRN-C07")
        gc = _rec(brain, "products", "gift_card") or _rec(brain, "offers", "gifting")
        if gc:
            add("gift_cards", "Gift cards on file", "ok", _text(gc)[:120], None, "agent", [gc["id"]])
        else:
            add("gift_cards", "Gift cards on file", "gap", "no gift card record", "Confirm whether gift cards exist and their values; they carry the sales after the cutoff.", "person", [], "BRN-C07")
    if kind in ("mission", "gifting"):
        gm = _rec(brain, "identity", "giving_model")
        dp = _rec(brain, "claims", "donation_pledge")
        if gm and dp and dp["tier"] in ("approved", "site_backed"):
            add("giving", "Giving story with a usable claim", "ok", f"{_text(gm)[:80]}; claim {dp['tier'].replace('_', ' ')}", None, "agent", [gm["id"], dp["id"]])
        elif gm:
            add("giving", "Giving story with a usable claim", "gap", "the giving model is on file but its claim is " + (dp["tier"] if dp else "missing"), "Approve the donation claim in the claims desk before the mission creative runs.", "person", [gm["id"]] + ([dp["id"]] if dp else []), "BRN-C03")
        else:
            add("giving", "Giving story with a usable claim", "gap" if kind == "mission" else "ok", "no giving model on file" if kind == "mission" else "no giving model; not needed for gifting", "Write the giving model as an identity record, or skip Giving Tuesday." if kind == "mission" else None, "person", [], "BRN-C07")
    if kind in ("sale", "gifting", "mission"):
        hooks = next((r for r in brain.records("learnings") if r.get("field") == "hook_types" and isinstance(r.get("value"), dict)), None)
        want = {"sale": "offer", "gifting": "seasonal", "mission": "mission"}[kind]
        n = 0
        if hooks:
            for label, cnt in hooks["value"].items():
                if want in (angles_of(label) if angles_of else []):
                    n += cnt if isinstance(cnt, (int, float)) else 1
        if hooks is None:
            add("creative", f"{want.capitalize()} creative in our ads", "unavailable", "no ad read in the brain", "Connect Meta or pull the Ad Library page to read our own hooks.", "agent", [], "BRN-C11")
        elif n:
            add("creative", f"{want.capitalize()} creative in our ads", "ok", f"{n} of our ads open on a {want} hook", None, "agent", [hooks["id"]])
        else:
            add("creative", f"{want.capitalize()} creative in our ads", "gap", f"0 of our ads open on a {want} hook", f"Brief 3 {want} concepts for {peak['label']}; the creative agent drafts, you approve.", "agent_drafts", [hooks["id"]], "CREA-C06")
    if kind == "sale" and legal_mod is not None:
        try:
            pd = next((c for c in legal_mod.checks(brain)["checks"] if c["key"] == "pricing_disclosure"), None)
        except Exception:  # noqa: BLE001
            pd = None
        if pd:
            add("pricing", "Reference prices are genuine former prices", pd["status"] if pd["status"] in ("ok", "pass", "fail", "unavailable") else "unavailable", pd.get("why") or "", "Connect the store so compare-at prices can be checked before the sale." if pd["status"] == "unavailable" else (pd.get("action") or {}).get("title"), "agent", [], "LOOP-C27")
            out[-1]["status"] = {"pass": "ok", "fail": "gap"}.get(out[-1]["status"], out[-1]["status"])
    if kind == "marketplace":
        listings = [r for r in brain.records("marketplaces") if r.get("field") == "amazon_listing"]
        if listings:
            add("listings", "Amazon listings on file", "ok", f"{len(listings)} listings read", None, "agent", [r["id"] for r in listings[:3]])
            add("parity", "Prices and packs match the site", "unavailable", "the MAP and seller names are founder inputs on the marketplace parity block", "Set MAP and the seller names in the parity block; the check runs on the next load.", "person", [], "PROD-C46")
        else:
            add("listings", "Amazon listings on file", "unavailable", "no marketplace listing in the brain", "Pull the listings (read-only) or skip the event if the brand is not on Amazon.", "agent", [], "BRN-C11")
    if kind in ("sale", "gifting", "mission"):
        add("email", "Send plan in the email tool", "unavailable", "no email platform connected", "Connect Klaviyo (read-only) so the calendar can be checked against the sends.", "agent", [], "BRN-C02")
    if kind in ("sale", "gifting"):
        add("stock", "Stock cover for the peak", "unavailable", "no store or inventory connector", "Connect the store so stock cover can be read; the supply screen owns the buy.", "agent", [], "BRN-C02")
    return out


def readiness(brain, angles_of=None, legal_mod=None, assumptions_mod=None) -> dict:
    peaks = calendar(brain, angles_of)
    rows = []
    for p in peaks:
        checks = checks_for(brain, p, angles_of, legal_mod)
        ok = [c for c in checks if c["status"] == "ok"]
        gaps = [c for c in checks if c["status"] == "gap"]
        unav = [c for c in checks if c["status"] == "unavailable"]
        denom = len(ok) + len(gaps)
        pct = round(100 * len(ok) / denom) if denom else None
        verdict = {"kind": "keep", "text": "Ready"} if not gaps and denom else ({"kind": "fix", "text": f"{len(gaps)} to decide"} if gaps else {"kind": "wait", "text": "Nothing to check yet"})
        if gaps and p.get("days_to") is not None and p["days_to"] <= 30:
            verdict = {"kind": "stop", "text": f"{len(gaps)} to decide, {p['days_to']} days"}
        row = dict(p, date=p["date"].isoformat() if p.get("date") else None, window_start=p["window_start"].isoformat() if p.get("window_start") else None, window_end=p["window_end"].isoformat() if p.get("window_end") else None,
                   checks=checks, counts={"ok": len(ok), "gaps": len(gaps), "unavailable": len(unav)}, readiness_pct=pct, verdict=verdict, surfaces=SURFACE_LABEL.get(p["kind"], ""))
        rows.append(row)
    hm = heavy_months(brain, assumptions_mod)
    return {"today": brain.today.isoformat(), "horizon_days": HORIZON_DAYS, "peaks": rows, "heavy_months": hm,
            "counts": {"peaks": len(rows), "ready": sum(1 for r in rows if r["verdict"]["kind"] == "keep"), "with_gaps": sum(1 for r in rows if r["counts"]["gaps"]), "gaps": sum(r["counts"]["gaps"] for r in rows), "unavailable": sum(r["counts"]["unavailable"] for r in rows)},
            "note": "US peaks are computed from the date; the brand's own dated calendar records join them. Each check reads a record: ok, a gap to decide or brief, or unavailable until a source connects. Readiness is ok over ok plus gaps. A decision here writes a founder record every screen reads."}


def plan(brain, key: str, label: str, date: str | None, offer: str, note: str, cutoff: str | None) -> list[dict]:
    """The founder records a peak decision writes: the offer for the peak, the peak on the calendar, and the shipping cutoff when given."""
    today = brain.today.isoformat()
    src = {"type": "founder", "ref": "05-brand-brain peak readiness", "captured_at": today}
    recs = [{"id": f"{brain.brand}.offers.peak_{key}", "brand": brain.brand, "section": "offers", "field": f"peak_{key}",
             "value": {"peak": key, "label": label, "date": date, "offer": offer[:200], "note": (note or "")[:200] or None},
             "text": f"{label}" + (f" ({date})" if date else "") + f": {offer[:160]}" + (f". {note[:120]}" if note else ""), "tier": "approved", "confidence": 1.0, "visibility": "private", "source": src},
            {"id": f"{brain.brand}.calendar.peak_{key}", "brand": brain.brand, "section": "calendar", "field": f"peak_{key}",
             "value": {"date": date, "event": label, "peak": key, "planned": True}, "text": f"{label}" + (f" on {date}" if date else "") + " is a planned peak with an offer decided.", "tier": "approved", "confidence": 1.0, "visibility": "private", "source": src}]
    if cutoff and re.match(r"\d{4}-\d{2}-\d{2}$", cutoff):
        recs.append({"id": f"{brain.brand}.policies.holiday_shipping_cutoff", "brand": brain.brand, "section": "policies", "field": "holiday_shipping_cutoff", "value": cutoff,
                     "text": f"Order by {cutoff} for standard shipping to land before 25 December.", "tier": "approved", "confidence": 1.0, "visibility": "public", "source": src})
    return recs
