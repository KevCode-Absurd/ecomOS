"""Vendor and platform contracts: what renews before we notice, and what has no renewal date on file.

The register lives in the brain's operations section as founder records `contract_<vendor>` with value
{vendor, type, renewal_date, notice_days, rate_card, sla_terms, source_doc}. Vendors the brain already knows
(the stack records: platform, reviews app, consent, testing, tag manager, performance, security; the 3PL and
agency named in operations and team text) are listed with "no contract on file" until the founder adds one.

Alert windows by vendor type are sized to how long a renegotiation takes (room spec): platform and 3PL 90 days,
agency and payments 60, apps, SMS and SaaS 30. A contract inside its window is BRN-R17; a stored contract with
no renewal date, and vendors with no contract at all, are BRN-R18. Days left are computed from the brain's
today. No document is read here; the document extractor proposes contract records from a dropped file later.
"""
from __future__ import annotations

import datetime as dt
import re

WINDOW_DAYS = {"platform": 90, "3pl": 90, "carrier": 60, "agency": 60, "payments": 60, "app": 30, "saas": 30, "sms": 30, "email": 30, "other": 30}
STACK_TYPE = {"platform": "platform", "reviews_app": "app", "upsell_app": "app", "tag_manager": "saas", "cookie_consent": "saas",
              "ab_testing": "saas", "performance_vendor": "saas", "form_security": "saas", "esp": "email", "sms": "sms", "support_desk": "saas"}
CONTRACT_TYPES = sorted(WINDOW_DAYS)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (s or "").lower()).strip("_")[:40]


def _vendor_name(value) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.split(",")[0].split(" via ")[0].strip()[:60]
    if isinstance(value, dict):
        for k in ("vendor", "name", "tool"):
            if value.get(k):
                return str(value[k])[:60]
    return None


def known_vendors(brain) -> list[dict]:
    """Vendors named by typed stack records, plus the text records in operations and team that name a partner."""
    out, seen = [], set()
    for r in brain.records("stack"):
        t = STACK_TYPE.get(r.get("field") or "")
        name = _vendor_name(r.get("value"))
        if not t or not name or slug(name) in seen:
            continue
        seen.add(slug(name))
        out.append({"vendor": name, "type": t, "from": r["id"], "how": (r.get("field") or "").replace("_", " ")})
    for sec, fields, t in (("operations", ("fulfillment_fact", "3pl", "carrier"), "3pl"), ("team", ("outside_agency",), "agency")):
        for r in brain.records(sec):
            if r.get("field") not in fields:
                continue
            name = _vendor_name(r.get("value"))
            if not name:
                m = re.search(r"\b(?:partner|agency|through|with|via)\s+([A-Z][A-Za-z0-9&]+(?:\s+[A-Z][A-Za-z0-9&]+){0,2})", r.get("text") or "")
                name = m.group(1) if m else None
            if not name or slug(name) in seen:
                continue
            seen.add(slug(name))
            out.append({"vendor": name, "type": t, "from": r["id"], "how": (r.get("field") or "").replace("_", " ")})
    return out


def stored(brain) -> list[dict]:
    out = []
    for r in brain.records("operations"):
        if not (r.get("field") or "").startswith("contract_"):
            continue
        v = r.get("value") if isinstance(r.get("value"), dict) else {}
        out.append(dict(v, record=r["id"], vendor=v.get("vendor") or (r.get("field") or "")[9:].replace("_", " "), tier=r["tier"], date=r["date"]))
    return out


def register(brain) -> dict:
    today = brain.today
    rows = []
    stored_by = {slug(c["vendor"]): c for c in stored(brain)}
    for c in stored_by.values():
        t = c.get("type") if c.get("type") in WINDOW_DAYS else "other"
        window = WINDOW_DAYS[t]
        rd = c.get("renewal_date")
        days_left = None
        try:
            days_left = (dt.date.fromisoformat(str(rd)[:10]) - today).days if rd else None
        except ValueError:
            days_left = None
        notice = c.get("notice_days") if isinstance(c.get("notice_days"), (int, float)) else None
        if days_left is None:
            v = {"kind": "fix", "text": "No renewal date", "reason": "stored contract without a renewal date; marked incomplete"}
        elif days_left < 0:
            v = {"kind": "stop", "text": "Passed", "reason": f"renewal date passed {-days_left} days ago; it likely auto-renewed"}
        elif days_left <= max(window, notice or 0):
            v = {"kind": "stop", "text": f"Renews in {days_left} d", "reason": f"inside the {max(window, notice or 0)} day window for a {t.replace('_', ' ')}"}
        else:
            v = {"kind": "keep", "text": f"{days_left} d left", "reason": f"outside the {window} day window"}
        rows.append({"vendor": c["vendor"], "slug": slug(c["vendor"]), "type": t, "renewal_date": rd, "days_left": days_left, "notice_days": notice,
                     "window_days": window, "rate_card": c.get("rate_card"), "sla_terms": c.get("sla_terms"), "source_doc": c.get("source_doc"),
                     "record": c["record"], "on_file": True, "verdict": v, "action": _action(c["vendor"], t, v["kind"], days_left, c.get("rate_card"))})
    missing = []
    for k in known_vendors(brain):
        if slug(k["vendor"]) in stored_by:
            continue
        missing.append(k)
        rows.append({"vendor": k["vendor"], "slug": slug(k["vendor"]), "type": k["type"], "renewal_date": None, "days_left": None, "notice_days": None,
                     "window_days": WINDOW_DAYS[k["type"]], "rate_card": None, "sla_terms": None, "source_doc": None, "record": k["from"], "on_file": False,
                     "how": k["how"], "verdict": {"kind": "wait", "text": "No contract on file", "reason": f"known from {k['how']}; add the renewal date"},
                     "action": _action(k["vendor"], k["type"], "wait", None, None)})
    order = {"stop": 0, "fix": 1, "wait": 2, "keep": 3}
    rows.sort(key=lambda r: (order.get(r["verdict"]["kind"], 9), r["days_left"] if r["days_left"] is not None else 9999, r["vendor"]))
    horizon = [r for r in rows if r["days_left"] is not None and 0 <= r["days_left"] <= 365]
    return {"contracts": rows, "types": CONTRACT_TYPES, "windows": WINDOW_DAYS,
            "counts": {"on_file": sum(1 for r in rows if r["on_file"]), "inside_window": sum(1 for r in rows if r["verdict"]["kind"] == "stop"),
                       "no_date": sum(1 for r in rows if r["on_file"] and r["days_left"] is None), "known_without_contract": len(missing)},
            "next": min(horizon, key=lambda r: r["days_left"]) if horizon else None,
            "calendar": sorted(({"vendor": r["vendor"], "date": r["renewal_date"], "days_left": r["days_left"], "window_days": r["window_days"], "type": r["type"]} for r in horizon), key=lambda x: x["days_left"]),
            "note": "Windows: platform and 3PL 90 days, agency and payments 60, apps, SaaS, SMS and email 30. A vendor the brain knows from the stack or a partner mention shows here until its contract is on file."}


def _action(vendor: str, t: str, kind: str, days_left, rate_card) -> dict:
    if kind == "wait":
        return {"title": f"Put the {vendor} contract on file", "owner": "person", "capability": "LOOP-C28", "artefact": "brain_record",
                "steps": [{"n": 1, "who": "person", "text": f"Type the renewal date, notice days and the rate card for {vendor} below, or drop the contract in Files in."},
                          {"n": 2, "who": "agent", "text": f"Watch the date. An alert fires {WINDOW_DAYS[t]} days before renewal for a {t.replace('_', ' ')}."}]}
    if kind == "fix":
        return {"title": f"Add the renewal date for {vendor}", "owner": "person", "capability": "LOOP-C28", "artefact": "brain_record",
                "steps": [{"n": 1, "who": "person", "text": "Find the renewal date in the contract or the last invoice and type it below."},
                          {"n": 2, "who": "agent", "text": "Compute the window and set the alert."}]}
    if kind == "stop":
        return {"title": f"Renegotiate or renew {vendor}" + (f" ({days_left} days left)" if days_left is not None and days_left >= 0 else " (date passed)"), "owner": "person", "capability": "LOOP-C28", "artefact": "ticket",
                "steps": [{"n": 1, "who": "agent", "text": "Pull the last terms" + (f": {rate_card}" if rate_card else "") + " and 12 months of spend with this vendor from finance, if connected."},
                          {"n": 2, "who": "agent", "text": "Draft 3 asks: rate, term, exit clause. Compare with 2 alternatives from the sources registry."},
                          {"n": 3, "who": "person", "text": "Send the notice before the notice deadline, or let it renew on purpose and log the decision."},
                          {"n": 4, "who": "agent", "text": "Write the new terms into the contract record."}]}
    return {"title": f"{vendor} is outside its window", "owner": "agent", "capability": "LOOP-C28", "artefact": "brain_record", "steps": [{"n": 1, "who": "agent", "text": "Watch the date."}, {"n": 2, "who": "agent", "text": "Alert inside the window."}]}
