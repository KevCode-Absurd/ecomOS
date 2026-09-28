"""Legal disclosure gate (US): is a page, policy, email or ad carrying what the rules require, before it ships?

Two parts, both rules in code, no model:
- `checks(brain)`: the site-level checks read from the brain. Each is pass, fail, unavailable (the source that
  answers it is not connected) or not applicable (the brand has no such surface), with the record as evidence
  and the fix as an action. A failed check is BRN-R19 in audit.py and blocks going live.
- `gate(brain, kind, text)`: a pasted draft checked for the elements its kind needs:
    email      an unsubscribe line and a postal address (CAN-SPAM);
    ad         a creator or partner mention needs a clear paid disclosure (FTC endorsement guides);
    pdp        a review or rating mention needs a note that reviews are collected honestly, and an incentive
               mention needs a disclosure (FTC reviews and testimonials rule, in force 21 Oct 2024);
    policy     an effective date;
    subscription  auto-renewal terms, cancellation path and the renewal price (state auto-renewal laws).
  Plus the claims scanner's forbidden and stale checks are re-run on the same text through claims.py.
This is a gate for a store, a light version of the regulated-industry tools. It names the rule family, never
gives legal advice; a fail says what is missing and who adds it.
"""
from __future__ import annotations

import re

UNSUB = re.compile(r"\b(unsubscribe|opt[- ]?out|manage (?:your )?preferences|stop receiving)\b", re.I)
POSTAL = re.compile(r"\b(?:\d{1,6}\s+[A-Za-z0-9.'\- ]{3,40}\s+(?:st|street|ave|avenue|rd|road|blvd|boulevard|ln|lane|dr|drive|way|suite|ste|floor|fl)\b|p\.?o\.?\s*box\s*\d+)", re.I)
ZIP = re.compile(r"\b[A-Z]{2}\s+\d{5}(?:-\d{4})?\b")
CREATOR = re.compile(r"\b(creator|influencer|partner(?:ship)?|ambassador|sponsored by|collab)\b", re.I)
PAID_DISCLOSURE = re.compile(r"(#ad\b|#sponsored|paid partnership|paid promotion|sponsored|advertisement|in partnership with)", re.I)
REVIEWS = re.compile(r"\b(reviews?|ratings?|stars?|testimonials?)\b", re.I)
INCENTIVE = re.compile(r"\b(free product|in exchange for|gift(?:ed)? in return|incentiv|compensat|received .{0,30}free)\b", re.I)
HONEST_REVIEWS = re.compile(r"(verified (?:buyer|purchase)|collected (?:from|by)|reviews are (?:from|by)|we do not (?:pay|edit)|not (?:paid|incentivi))", re.I)
EFFECTIVE = re.compile(r"\b(effective|last updated|updated on|revised)\b.{0,30}\b(20\d\d|\d{1,2}/\d{1,2}/\d{2,4})", re.I)
AUTO_RENEW = re.compile(r"\b(auto(?:matically)?[- ]?renew|renews? (?:each|every)|until you cancel)\b", re.I)
CANCEL = re.compile(r"\b(cancel(?:lation)?|how to cancel|to stop your subscription)\b", re.I)
RENEW_PRICE = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?\s*(?:per|a|each|/)\s*(?:month|year|delivery|order|box)", re.I)

KINDS = ["email", "ad", "pdp", "policy", "subscription"]


def _rec(brain, section, field):
    return next((r for r in brain.records(section) if r.get("field") == field), None)


def _pages(brain, field):
    r = _rec(brain, "site_map", field)
    v = r.get("value") if r else None
    return [p for p in v if isinstance(p, dict)] if isinstance(v, list) else []


def _has_page(pages, words):
    return next((p for p in pages if any(w in (p.get("url") or "").lower() for w in words)), None)


def checks(brain) -> dict:
    out = []
    legal = _pages(brain, "legal_pages")
    facts = _pages(brain, "facts_pages")
    def add(key, label, law, status, evidence, why, fix, owner="person", capability="LOOP-C27", surface="site"):
        out.append({"key": key, "label": label, "law": law, "status": status, "evidence": evidence, "why": why, "surface": surface,
                    "action": {"title": fix, "owner": owner, "capability": capability} if status == "fail" else None})
    # privacy policy with an effective date (CCPA/CPRA and other state laws)
    pe = _rec(brain, "policies", "privacy_effective_date")
    pp = _has_page(legal, ["privacy"])
    if pe or pp:
        add("privacy_policy", "Privacy policy posted with an effective date", "CCPA/CPRA and state privacy laws", "pass" if pe else "fail",
            [x for x in (pe["id"] if pe else None, pp["url"] if pp else None) if x], "a privacy page exists" + (f", effective {pe.get('value')}" if pe else ", no effective date read"),
            "Add the effective date to the privacy policy page")
    else:
        add("privacy_policy", "Privacy policy posted with an effective date", "CCPA/CPRA and state privacy laws", "fail", [], "no privacy page in the site map", "Publish a privacy policy page with an effective date")
    sp = _has_page(legal, ["washington", "california", "ccpa", "state-privacy", "your-privacy-choices", "do-not-sell"])
    add("state_privacy", "State privacy notice or Your Privacy Choices link", "CCPA/CPRA, Washington MHMDA and other state laws", "pass" if sp else "fail",
        [sp["url"]] if sp else [], "a state privacy page exists" if sp else "no state privacy page in the site map", "Add a state privacy notice and a Your Privacy Choices link")
    te = _rec(brain, "policies", "terms_effective_date")
    tp = _has_page(legal, ["terms"])
    add("terms", "Terms of service posted with an effective date", "contract formation, UCC", "pass" if te else ("fail" if tp else "fail"),
        [x for x in (te["id"] if te else None, tp["url"] if tp else None) if x], f"effective {te.get('value')}" if te else "no effective date read", "Add the effective date to the terms page")
    rw = _rec(brain, "policies", "returns_window_days")
    add("returns_posted", "Return and refund terms posted as practised", "FTC Act section 5, state refund disclosure laws", "pass" if rw else "fail",
        [rw["id"]] if rw else [], f"returns window {rw.get('value')} days on file" if rw else "no returns window read from the site", "Publish the return and refund policy with the window and the method")
    cc = _rec(brain, "stack", "cookie_consent")
    add("cookie_consent", "Cookie consent manager live", "CCPA/CPRA opt-out of sale or sharing; GDPR where sold", "pass" if cc else "fail",
        [cc["id"]] if cc else [], f"{cc.get('value')} detected" if cc else "no consent manager detected in the stack", "Install a consent manager and honour opt-out signals")
    ap = _has_page(legal, ["accessib"])
    add("accessibility", "Accessibility statement posted", "ADA Title III as applied to web stores", "pass" if ap else "fail", [ap["url"]] if ap else [],
        "an accessibility page exists" if ap else "no accessibility page in the site map", "Publish an accessibility statement with a contact route")
    ca = _rec(brain, "learnings", "creator_ads")
    if ca:
        tagged = "partner" in (ca.get("text") or "").lower() or "tagged" in (ca.get("text") or "").lower()
        add("creator_disclosure", "Creator ads carry a paid partnership label", "FTC endorsement guides", "pass" if tagged else "fail", [ca["id"]],
            ca.get("text") or "", "Add the paid partnership label to every creator ad", owner="agent_drafts", surface="ads")
    else:
        add("creator_disclosure", "Creator ads carry a paid partnership label", "FTC endorsement guides", "na", [], "no creator ads in the brain", None, surface="ads")
    # things that need a source not yet connected
    add("can_spam", "Every marketing email has an unsubscribe line and a postal address", "CAN-SPAM", "unavailable", [], "no email platform connected; the gate below checks a pasted email", None, surface="email")
    add("pricing_disclosure", "Reference prices and strike-throughs are genuine former prices", "FTC guides against deceptive pricing, state laws", "unavailable", [], "compare-at prices are not in the crawl yet", None, surface="site")
    add("sales_tax_invoices", "Sales tax shown correctly on invoices", "state sales tax rules", "unavailable", [], "no store connector; invoices are not readable", None, surface="invoices")
    plans = brain.records("plans")
    add("auto_renewal", "Subscription terms disclose auto-renewal, the price and how to cancel", "state auto-renewal laws (California ARL and others)", "pass" if not plans else "unavailable",
        [], "no subscription plans in the brain, not applicable" if not plans else "plans exist; paste the checkout terms in the gate", None, surface="checkout")
    if not plans:
        out[-1]["status"] = "na"
    counts = {s: sum(1 for c in out if c["status"] == s) for s in ("pass", "fail", "unavailable", "na")}
    checked = counts["pass"] + counts["fail"]
    return {"checks": out, "counts": counts, "pass_rate": (round(counts["pass"] / checked, 2) if checked else None), "checked": checked,
            "note": "A store-level gate, not legal advice. Pass and fail come from the brain records the crawl wrote; unavailable names the source that answers it."}


def gate(brain, kind: str, text: str, claims_mod=None) -> dict:
    kind = kind if kind in KINDS else "pdp"
    t = text or ""
    missing, present = [], []
    def need(ok, key, label, fix):
        (present if ok else missing).append({"key": key, "label": label, "fix": fix})
    if kind == "email":
        need(bool(UNSUB.search(t)), "unsubscribe", "an unsubscribe or manage preferences line", "Add a one-click unsubscribe line in the footer.")
        need(bool(POSTAL.search(t) or ZIP.search(t)), "postal_address", "a physical postal address", "Add the brand's postal address in the footer.")
    elif kind == "ad":
        if CREATOR.search(t):
            need(bool(PAID_DISCLOSURE.search(t)), "paid_disclosure", "a clear paid partnership disclosure", "Add #ad or Paid partnership where it is seen before the claim.")
        else:
            present.append({"key": "paid_disclosure", "label": "no creator or partner mention, no disclosure needed", "fix": None})
    elif kind == "pdp":
        if REVIEWS.search(t):
            need(bool(HONEST_REVIEWS.search(t)), "honest_reviews", "a note on how reviews are collected (verified buyers, not paid)", "Add a line: reviews are from verified buyers and are not edited or paid for.")
        if INCENTIVE.search(t):
            need(bool(PAID_DISCLOSURE.search(t) or HONEST_REVIEWS.search(t)), "incentive_disclosure", "a disclosure next to incentivised reviews", "Label reviews written for a free product as such.")
        if not REVIEWS.search(t) and not INCENTIVE.search(t):
            present.append({"key": "reviews", "label": "no review or incentive mention", "fix": None})
    elif kind == "policy":
        need(bool(EFFECTIVE.search(t)), "effective_date", "an effective or last updated date", "Add an effective date at the top.")
    elif kind == "subscription":
        need(bool(AUTO_RENEW.search(t)), "auto_renewal_terms", "a plain statement that it renews automatically", "Say it renews automatically until cancelled.")
        need(bool(CANCEL.search(t)), "cancellation", "how to cancel", "Add the cancellation route, online, as easy as signing up.")
        need(bool(RENEW_PRICE.search(t)), "renewal_price", "the renewal price and cadence", "State the price per period.")
    scan = claims_mod.scan(brain, t) if claims_mod else None
    blocking = len(missing) + (scan["fails"] if scan else 0)
    return {"kind": kind, "verdict": "fail" if blocking else ("warn" if scan and scan["warns"] else "pass"), "missing": missing, "present": present,
            "claims": scan, "blocking": blocking, "note": "Rules only. A fail lists what is missing and the fix; a person signs off before it ships."}
