"""Bombas calibration targets for the data generator, built from merged brain records.

Called by app/brain/merge.py as build(records, today) -> (assumptions, open_questions).

Each assumption names its status: `sourced` (a record states it), `derived`
(arithmetic in code on sourced records) or `assumed` (our estimate, with the
reasoning). Every number the generator reads comes from here, never from a
model. Fields nothing answers also go to open_questions as records.
"""
from __future__ import annotations

BRAND = "bombas"


def _find(records: list[dict], rid: str) -> dict | None:
    return next((r for r in records if r["id"] == rid), None)


def _refs(records: list[dict], ids: list[str]) -> list[str]:
    return sorted({(r.get("source") or {}).get("ref", "") for r in records if r["id"] in ids} - {""})


def _entry(records, field, value, status, ids, reasoning, unit=None, as_of=None):
    missing = [i for i in ids if not _find(records, i)]
    if missing and status not in ("assumed", "founder", "modelled"):
        status = "assumed"
        reasoning += f" Records missing at merge time: {', '.join(missing)}."
    out = {"field": field, "value": value, "status": status}
    if unit:
        out["unit"] = unit
    if as_of:
        out["as_of"] = as_of
    out.update(source_ids=[i for i in ids if i not in missing], source_refs=_refs(records, ids), reasoning=reasoning)
    return out


def _value(records, rid, key=None, default=None):
    rec = _find(records, rid)
    if not rec or "value" not in rec or rec["value"] is None:
        return default
    return rec["value"].get(key, default) if key else rec["value"]


def build(records: list[dict], today: str) -> tuple[list[dict], list[dict]]:
    a = []

    # Revenue: the newest stated figure is a 2025 projection near 500 million dollars.
    series = [
        {"year": 2017, "amount_usd": _value(records, "bombas.economics.revenue_band_2017_projection", "amount_usd"), "kind": "on track for"},
        {"year": 2018, "amount_usd": _value(records, "bombas.economics.revenue_band_2018", "amount_usd"), "kind": "exceeded"},
        {"year": 2023, "amount_usd": _value(records, "bombas.economics.revenue_band_2023", "amount_usd"), "kind": "over"},
        {"year": 2025, "amount_usd": 500_000_000, "kind": "projected near"},
    ]
    point = 500_000_000
    band = {"year": 2025, "low_usd": round(point * 0.9), "high_usd": round(point * 1.1), "point_usd": point, "series": series}
    a.append(_entry(records, "revenue_band", band, "sourced",
                    ["bombas.operations.revenue_mix.1", "bombas.economics.revenue_band_2023",
                     "bombas.economics.revenue_band_2018", "bombas.economics.revenue_band_2017_projection"],
                    "Press in October 2025 projects Bombas near 500 million dollars for 2025. The plus or minus 10 percent "
                    "band around it is ours. Growth check: 300 million in 2023 to 500 million in 2025 is about "
                    f"{round(((500 / 300) ** 0.5 - 1) * 100)} percent a year.",
                    unit="usd per year", as_of="2025-10"))

    # AOV: nothing states it. Bracket it with the price ladder, pack sizes, free shipping line and first order code.
    single = _value(records, "bombas.products.price_ladder_socks", "min_usd", 13.0)
    threshold = _value(records, "bombas.offers.free_shipping_threshold_usd", default=75)
    code_pct = _value(records, "bombas.offers.first_order_code", "discount_pct", 20)
    low = round(4 * single, 2)
    high = round(threshold / (1 - code_pct / 100), 2)
    mid = round((low + high) / 2)
    a.append(_entry(records, "aov_usd", {"estimate": mid, "low": low, "high": high}, "assumed",
                    ["bombas.products.price_ladder_socks", "bombas.products.pack_sizes",
                     "bombas.offers.free_shipping_threshold_usd", "bombas.offers.first_order_code"],
                    f"No source states AOV. Low: the smallest common multi pack (4) at the lowest single sock price "
                    f"({single} dollars) is {low}. High: the list total a first order needs to stay at {threshold} dollars "
                    f"after the {code_pct} percent code is {high}. The estimate is the midpoint. Shoppers tend to build "
                    "baskets toward a free shipping line, so the band sits around it.",
                    unit="usd", as_of=today))

    # Repeat rate: nothing states it. The generator needs a number, so it runs on an assumption until answered.
    a.append(_entry(records, "repeat_rate_12m", 0.35, "assumed",
                    ["bombas.avatars.guarantee_reassured_loyalist", "bombas.avatars.durability_disappointed_repeat_customer"],
                    "No source states a repeat rate. Reviews show a loyal repeat group and a repeat group let down by "
                    "durability. Socks and underwear wear out and are rebought, so we assume 35 percent of first time "
                    "buyers order again within 12 months. Open question: repeat_rate.",
                    unit="share of new customers", as_of=today))

    # Channel mix: 97/3 DTC to wholesale in 2020, wholesale under 10 percent in 2025, 3 owned stores from late 2025.
    wholesale, retail = 9, 1
    mix = {"dtc_site_pct": 100 - wholesale - retail, "wholesale_pct": wholesale, "owned_retail_pct": retail,
           "marketplaces_pct": None,
           "history": [{"as_of": "2020-02", "dtc_pct": _value(records, "bombas.economics.wholesale_vs_dtc_mix_2020", "dtc_share_pct"),
                        "wholesale_pct": _value(records, "bombas.economics.wholesale_vs_dtc_mix_2020", "wholesale_share_pct")},
                       {"as_of": "2025-10", "wholesale_pct": "under 10"}]}
    a.append(_entry(records, "channel_mix", mix, "assumed",
                    ["bombas.economics.wholesale_vs_dtc_mix_2020", "bombas.operations.revenue_mix.1",
                     "bombas.channels.flagship_retail_2025", "bombas.calendar.flagship_store_nyc_2025"],
                    "Sourced: 97 percent DTC and 3 percent wholesale in early 2020, and wholesale under 10 percent in "
                    "October 2025. Assumed: wholesale at 9 percent now that Target and DSW are rolling out, 1 percent "
                    "from 3 owned stores opened in late 2025, the rest on the site. Marketplace share is unknown and "
                    "reads null. Open question: channel_mix.",
                    unit="percent of revenue", as_of=today))

    paid = ["Meta (paid social, first order code in 21 of 23 active ads)", "YouTube creator ads via Agentio",
            "TikTok and TikTok Shop", "Instagram", "Pinterest", "Strava"]
    a.append(_entry(records, "paid_channels_present", paid, "sourced",
                    ["bombas.offers.promo_share_active_ads", "bombas.channels.channel_priority.1",
                     "bombas.channels.channel_priority.3", "bombas.channels.channel_priority.6"],
                    "Channels named in the Ad Library and in job posts. Spend split between them is not stated. "
                    "Open question: paid_spend_split.", as_of=today))

    # Seasonality: signals point to a holiday peak; no source gives a monthly share.
    raw_index = [0.85, 0.75, 0.8, 0.8, 0.85, 0.8, 0.8, 0.85, 0.9, 1.05, 1.6, 1.9]
    scale = 12 / sum(raw_index)
    index = [round(x * scale, 3) for x in raw_index]
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    a.append(_entry(records, "seasonality", {"peaks": ["nov", "dec"], "secondary": ["oct", "jan"],
                                             "monthly_index": dict(zip(months, index))}, "assumed",
                    ["bombas.offers.guarantee", "bombas.policies.returns_window_days", "bombas.offers.gifting",
                     "bombas.avatars.holiday_gift_buyer", "bombas.objections.gift_order_arrival_risk",
                     "bombas.avatars.cold_weather_wool_loyalist", "bombas.learnings.hook_types"],
                    "Sourced signals: a 60 day return window for November and December orders, a gift card and bulk "
                    "gifting program, a holiday gift buyer group in reviews, late holiday order complaints, a cold "
                    "weather wool group and seasonal cozy hooks in current ads. The peak months follow from these; the "
                    "monthly index is ours, scaled so the 12 months average 1. Open question: seasonality.",
                    unit="index, mean 1", as_of=today))

    # Giving units: cumulative donation milestones; one donated per one purchased, so they track units sold.
    marks = [(2016, _value(records, "bombas.story_bank.mission_proof_giving_1m", "items_donated"), "bombas.story_bank.mission_proof_giving_1m"),
             (2018, _value(records, "bombas.story_bank.mission_proof_giving_10m", "items_donated"), "bombas.story_bank.mission_proof_giving_10m"),
             (2022, 75_000_000, "bombas.operations.fulfillment_fact.5"),
             (2023, 100_000_000, "bombas.story_bank.mission_proof_giving_100m"),
             (2026, _value(records, "bombas.identity.giving_partner_network_2026", "donations_total"), "bombas.identity.giving_partner_network_2026")]
    marks = [m for m in marks if m[1]]
    per_year = [{"from": a0, "to": a1, "items_per_year": round((v1 - v0) / (a1 - a0))}
                for (a0, v0, _), (a1, v1, _) in zip(marks, marks[1:])]
    a.append(_entry(records, "giving_units", {"cumulative": [{"year": y, "items_donated": v} for y, v, _ in marks],
                                              "per_year_between_marks": per_year}, "derived",
                    [m[2] for m in marks],
                    "Cumulative items donated at dated milestones; the yearly rate between them is arithmetic. The "
                    "model is one donated per one purchased, so the rate is also a floor on units sold (replacements "
                    "do not trigger a donation). Note: a 2018 press record says 20 million pairs sold and donated "
                    "each, which does not fit 10 million donated around November 2018; the story bank milestones are "
                    "used here.", unit="items", as_of="2026"))

    partners = [{"name": "Nordstrom", "since": 2018}, {"name": "Dick's Sporting Goods", "since": 2018},
                {"name": "Athleta", "since": 2020, "stores": 190}, {"name": "Target", "since": 2025, "category": "socks"},
                {"name": "DSW", "since": 2025, "category": "footwear", "stores": 500}, {"name": "Scheels", "since": None}]
    a.append(_entry(records, "retail_partners", partners, "sourced",
                    ["bombas.channels.wholesale_launch_2018", "bombas.channels.athleta_partnership_2020",
                     "bombas.channels.target_dsw_2025", "bombas.operations.revenue_mix.1"],
                    "Wholesale partners named in press, with the year each started where stated. Scheels is named in "
                    "October 2025 press without a start year.", as_of="2025-10"))

    a.append(_entry(records, "category_mix", {"socks_and_slippers_pct": 93, "underwear_and_tshirts_pct": 7,
                                              "footwear_pct_2025": 20}, "sourced",
                    ["bombas.economics.category_revenue_mix_2023", "bombas.economics.footwear_share_2025"],
                    "93 to 7 split as of March 2023. Footwear near 20 percent of sales by late 2025 is a single report "
                    "at 0.5 confidence.", unit="percent of revenue", as_of="2023-03"))

    # Founder and modelled overrides (S1.4 review, 28 Sep 2026): an approved economics record wins over any
    # estimate above; a modelled (inferred) record answers an open question and marks the assumption modelled.
    def _founder(field, key=None):
        r = _find(records, f"{BRAND}.economics.{field}")
        if not r or r.get("tier") not in ("approved", "inferred"):
            return None, None
        v = r.get("value")
        return (v.get(key) if key and isinstance(v, dict) else v), r
    answered = set()
    v, r = _founder("revenue_point_usd")
    if v:
        for e in a:
            if e["field"] == "revenue_band":
                e["value"]["point_usd"] = v
                e["status"] = "founder"; e["source_ids"] = [r["id"]]
                e["reasoning"] = "Kevin set the simulated point at the low end of the public band, as an uneven number."
    v, r = _founder("aov_usd")
    if v:
        for e in a:
            if e["field"] == "aov_usd":
                e["value"]["estimate"] = v; e["status"] = "founder"; e["source_ids"] = [r["id"]]
        answered.add("aov")
    v, r = _founder("repeat_rate_12m")
    if v:
        for e in a:
            if e["field"] == "repeat_rate_12m":
                e["value"] = v; e["status"] = "founder"; e["source_ids"] = [r["id"]]
        answered.add("repeat_rate")
    v, r = _founder("channel_mix")
    if v:
        for e in a:
            if e["field"] == "channel_mix":
                e["value"] = {**v, "history": e["value"].get("history")}; e["status"] = "founder"; e["source_ids"] = [r["id"]]
                e["reasoning"] = "Kevin's split for the simulation: site 74, wholesale 12, owned stores 6, marketplaces 8."
        answered.add("channel_mix")
    v, r = _founder("paid_media_split")
    if v:
        a.append(_entry(records, "paid_media_split", v, "founder", [r["id"]],
                        "Kevin set Meta 60 and Google 20 and asked for the rest to be made up.", unit="percent of paid spend", as_of=today))
        answered.add("paid_spend_split")
    v, r = _founder("gross_margin_model")
    if v:
        a.append(_entry(records, "gross_margin", v, "modelled", [r["id"]],
                        "Modelled from DTC basics benchmarks with the donated item counted as a second unit at about half the sold unit's cost. Not a Bombas figure.", unit="percent of net revenue", as_of=today))
        answered.add("gross_margin")
    v, r = _founder("return_share_model")
    if v:
        a.append(_entry(records, "return_share", v, "modelled", [r["id"]],
                        "Modelled from sock and basics return norms and the guarantee's replacement policy. Not a Bombas figure.", unit="percent of orders", as_of=today))
        answered.add("return_rate")
    v, r = _founder("monthly_revenue_shape")
    if v:
        answered.add("seasonality")

    questions = [
        ("repeat_rate", "What share of first time buyers order again within 12 months?", "avatars",
         "Sets retention in the simulated orders and every LTV number.", "Shopify or Klaviyo, or the founder"),
        ("aov", "What is the average order value on the US site?", "economics",
         f"The assumed {mid} dollars drives order counts from revenue.", "Shopify, or the founder"),
        ("seasonality", "What share of yearly site revenue lands in each month?", "calendar",
         "The monthly index is our estimate from holiday signals.", "Shopify or GA4, or the founder"),
        ("channel_mix", "What share of revenue comes from the site, wholesale, owned stores and marketplaces?", "channels",
         "Only a 2020 split and a 2025 wholesale ceiling are public; marketplace share is unknown.", "the founder"),
        ("paid_spend_split", "How is paid media spend split across Meta, YouTube, TikTok, Google and others?", "channels",
         "Shapes the simulated ad tables and blended CAC.", "Meta, Google and TikTok ad accounts, or the founder"),
        ("gross_margin", "What is gross margin after product, freight and fulfilment cost?", "economics",
         "Needed for contribution margin and break even ROAS.", "the founder or finance"),
        ("return_rate", "What share of orders is returned or replaced under the Happiness Guarantee?", "economics",
         "Sets the returns leg of reversed orders.", "Shopify or the support desk, or the founder"),
    ]
    oq = [{
        "id": f"{BRAND}.open_questions.{key}", "brand": BRAND, "section": "open_questions", "field": key,
        "value": {"question": q, "section": sec, "why": why, "who_can_answer": who, "asked_on": None, "answered_on": None},
        "text": q, "visibility": "private",
    } for key, q, sec, why, who in questions if key not in answered]
    return a, oq
