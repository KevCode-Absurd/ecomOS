# Gehna Meta ad copy audit (Arm B)

Data: `data/meta-gallery/cache/gallery.json`, 472 ads, 23 Sep 2025 to 24 Sep 2026, INR. Site pages read on 24 Sep 2026: home, shipping and returns, FAQ, 3 collection pages (gemstone gold chains, rings, best sellers) and 6 product pages. Every table below is in `reviews/copy-test/arm-b/raw/`, built by `build_audit_tables.py`, `build_adset_audience_table.py` and `test_budget.py`. Re-run them from the repo root to reproduce every number.

How nulls were handled: a null purchase or purchase value in the daily rows means Meta did not report one that day. Totals add the reported values only. An ad whose spend days never report a purchase shows purchases and ROAS as unavailable, never 0. Its spend still counts. Period ROAS is total reported value divided by total spend. Age, gender and platform figures come from the monthly breakdowns and are never added to the daily totals.

Sum of daily spend in the capture: ₹1,29,59,908. Meta's own account total for the window: ₹1,29,60,904. The gap is ₹996, so the daily rows are complete.

## 1. The account in numbers

| Window | Spend | Reported purchases | Reported value | ROAS | Cost per purchase | Value per order |
|---|---|---|---|---|---|---|
| 12 months (23 Sep 2025 to 24 Sep 2026) | ₹1,29,59,908 | 1,396 | ₹4,24,86,365 | 3.28 | ₹9,284 | ₹30,434 |
| 90 days (27 Jun to 24 Sep 2026) | ₹32,24,679 | 347 | ₹1,29,42,450 | 4.01 | ₹9,293 | ₹37,298 |
| 30 days (26 Aug to 24 Sep 2026) | ₹11,52,747 | 150 | ₹64,97,268 | 5.64 | ₹7,685 | ₹43,315 |

Current monthly spend: ₹11,52,747 in the last 30 days; the mean of June, July and August 2026 is ₹11,11,951. The plan uses ₹11,12,000 as the base. Spend has sat between ₹9.4 lakh and ₹13.4 lakh a month all year. October 2025 was the biggest month (₹12,33,936, ROAS 3.48, cost per purchase ₹6,328). March 2026 was the worst (₹10,01,452, ROAS 1.60, cost per purchase ₹14,947). August and September 2026 are the best two months since October: ROAS 4.27 and 4.70 (`monthly_totals.csv`).

Attribution is mixed: 54% of spend runs on 1-day view plus 7-day click, 45% on 1-day view plus 7-day click plus 1-day engaged view, and 24 ads (₹59,951) ran on an incrementality setting that reported ₹828 of value. Mixed settings mean ROAS is not comparable across campaigns (`by_attribution_12m.csv`).

## 2. What copy the account runs today

The account used 73 unique primary texts across 472 ads. Two facts shape everything else:

1. 139 ads (₹42,45,241, 32.8% of spend) are flexible-format ads with no captured primary text or headline. Their copy cannot be audited. They returned ROAS 3.02 over 12 months and 3.89 over 90 days (`by_has_primary_text_12m.csv`, `by_format_12m.csv`).
2. All 472 ads have an empty description field. The 30-character description slot has never been used.

The 5 texts that carried the most spend:

| Primary text (first line) | Headline | Ads | 12-month spend | Reported value | ROAS |
|---|---|---|---|---|---|
| "I'm a regular customer of Gehna..." (Flora Prasad quote, then Lifetime Exchange, EMI, 100% Handcrafted, Buyback) | Redesigning beauty. ✨ | 43 (cold catalog) | ₹26,58,336 | ₹57,88,631 | 2.18 |
| "Did something catch your eye?" (7 Days Return promise, 5000+ happy customers) | Redesigning beauty. ✨ | 5 (cart and site retargeting catalog) | ₹13,87,998 | ₹85,53,036 | 6.16 |
| "When more than 8,500 people have lived the Gehna experience..." | Handcrafted 18K Gold \| 4.8/5 on Google | 8 (earrings video) | ₹7,59,634 | ₹29,87,067 | 3.93 |
| "Everyday elegance, reimagined ✨" (chains) | Redesigning Beauty, One Jewelry at a Time! | 9 | ₹4,28,463 | ₹8,87,506 | 2.07 |

Also notable: "Forget the guesswork" (earrings gifting video, ₹3,23,949, ROAS 7.94) and "Buying fine gold online is not as scary as you think!" (earrings trust video, ₹3,11,658, ROAS 5.65). Full list: `copy_inventory.json`.

The house style is 3 to 5 short lines, 3 to 8 emojis, a proof stack at the end, and a headline that is the brand name, "Redesigning beauty", or product plus proof. "Redesigning beauty. ✨" sat on ₹40,46,333 of catalog spend and does not say what is sold.

## 3. Spend and value by angle, hook and product

Tags are the gallery's own labels. Percentages are share of spend in the window.

### Angle

| Angle | 12-month spend | Share | Reported value | ROAS | 90-day spend | Share | Reported value | ROAS |
|---|---|---|---|---|---|---|---|---|
| Catalog (Meta picks products) | ₹40,46,333 | 31.2% | ₹1,43,41,667 | 3.54 | ₹12,37,451 | 38.4% | ₹36,45,367 | 2.95 |
| Product showcase | ₹23,14,725 | 17.9% | ₹68,30,378 | 2.95 | ₹2,26,532 | 7.0% | ₹10,30,007 | 4.55 |
| Gifting or occasion | ₹15,70,738 | 12.1% | ₹55,79,695 | 3.55 | ₹3,69,503 | 11.5% | ₹25,33,677 | 6.86 |
| UGC or unboxing | ₹15,53,005 | 12.0% | ₹44,15,499 | 2.84 | ₹2,01,964 | 6.3% | ₹10,45,069 | 5.17 |
| Social proof or reviews | ₹12,89,949 | 10.0% | ₹51,77,041 | 4.01 | ₹5,39,493 | 16.7% | ₹22,33,904 | 4.14 |
| Education or objection handling | ₹11,69,044 | 9.0% | ₹24,60,250 | 2.10 | ₹3,10,269 | 9.6% | ₹8,57,711 | 2.76 |
| Offer or urgency | ₹5,21,288 | 4.0% | ₹26,14,795 | 5.02 | ₹2,55,160 | 7.9% | ₹14,43,226 | 5.66 |
| Founder or brand story | ₹4,94,825 | 3.8% | ₹10,67,041 | 2.16 | ₹84,307 | 2.6% | ₹1,53,490 | 1.82 |

Read: proof, gifting and offer copy return 4 to 7 times spend. Founder and "education" copy return about 2. The catalog line's 12-month number is flattered by retargeting: the same catalog format returned 6.52 on cart audiences and 2.18 on cold audiences (section 5).

### Hook (first line)

| Hook | 12-month spend | Share | Reported value | ROAS | 90-day ROAS |
|---|---|---|---|---|---|
| Statement | ₹55,90,871 | 43.1% | ₹1,50,86,160 | 2.70 | 3.28 |
| No text (flexible ads) | ₹42,45,241 | 32.8% | ₹1,28,10,037 | 3.02 | 3.89 |
| Question | ₹14,68,525 | 11.3% | ₹86,15,506 | 5.87 | 4.51 |
| Proof or number | ₹9,65,657 | 7.5% | ₹25,63,218 | 2.65 | 5.59 |
| Price or offer | ₹6,62,300 | 5.1% | ₹33,07,910 | 4.99 | 6.09 |
| Urgency | ₹27,313 | 0.2% | ₹1,03,534 | 3.79 | unavailable |

Read with care: the question hook is almost entirely 1 text ("Did something catch your eye?") on cart retargeting, so its 5.87 is an audience effect, not a hook effect. Statement hooks are the bulk of cold spend and sit at 2.70.

### Product group

| Product | 12-month spend | Share | Reported purchases | Reported value | ROAS | 90-day spend | ROAS |
|---|---|---|---|---|---|---|---|
| Mixed range | ₹66,15,890 | 51.1% | 785 | ₹2,21,03,987 | 3.34 | ₹16,16,744 | 3.51 |
| Earrings | ₹24,54,671 | 18.9% | 308 | ₹1,02,85,176 | 4.19 | ₹11,47,082 | 4.85 |
| Bracelets | ₹22,30,398 | 17.2% | 185 | ₹65,00,110 | 2.91 | ₹2,49,285 | 4.21 |
| Chains | ₹11,08,947 | 8.6% | 74 | ₹24,44,005 | 2.20 | ₹1,12,109 | 5.15 |
| Pendants | ₹3,86,053 | 3.0% | 41 | ₹10,11,001 | 2.62 | unavailable | unavailable |
| Rings | ₹1,63,948 | 1.3% | 3 | ₹1,42,086 | 0.87 | ₹99,458 | 0.88 |

Earrings are the workhorse: 18.9% of spend, 22.1% of reported purchases, and the best ROAS of any named product in both windows. Rings had 45 ads and 3 reported purchases. Chains, the highest-priced group on the site, returned 2.20 at cold but 5.15 in the sale window.

### Format and funnel stage

By format over 12 months: flexible ads 32.8% of spend at ROAS 3.02, catalog 31.2% at 3.54, video 22.5% at 3.63, single image 7.3% at 2.64, carousel 6.2% at 2.78. Over 90 days video leads at 5.06 (`by_format_90d.csv`).

| Stage (from campaign name) | 12-month spend | Share | Purchases | Value | ROAS | Cost per purchase |
|---|---|---|---|---|---|---|
| TOF prospecting | ₹1,11,39,757 | 86.0% | 1,018 | ₹3,16,55,031 | 2.84 | ₹10,943 |
| BOF cart and site retargeting (3 catalog ads) | ₹11,24,139 | 8.7% | 272 | ₹73,29,577 | 6.52 | ₹4,133 |
| AOF sale campaign (Aug to Sep 2026) | ₹3,78,502 | 2.9% | 59 | ₹22,26,788 | 5.88 | ₹6,415 |
| MOF engagers and catalogue visitors | ₹3,11,209 | 2.4% | 47 | ₹12,74,968 | 4.10 | ₹6,621 |

Ad set names show the "TOF" campaigns are not all cold. Ad sets named "MOF + BOF audiences" sit inside prospecting campaigns and took ₹20,92,057 (16.1% of spend, ROAS 3.60). Broad ad sets took 27.7% (ROAS 2.83), lookalikes 26.0% (2.44) and interest stacks 18.2% (3.24) (`by_adset_audience_12m.csv`). No campaign or ad set name mentions a past-customer exclusion or a past-customer audience.

Breakdowns, kept separate: women took 71.3% of spend at ROAS 3.98; men took 28.4% at 1.53 and cost ₹20,081 per purchase. Ages 35 to 54 return 4.0 to 4.2; 18 to 24 took 12.6% of spend at 1.17. Instagram returned 3.88 against Facebook's 2.63 on near-equal spend (`breakdown_*.csv`).

## 4. Best and worst ads by ROAS at meaningful spend

Spend floor: ₹28,000 per ad in the window. That is 3 times the 12-month cost per reported purchase (₹9,284), rounded to the nearest ₹1,000. Below it an ad has not had the chance to report 3 purchases. 86 ads clear the floor over 12 months, 28 over 90 days (`ranking_note.json`).

### 10 best, 12 months (`best10_12m.csv`)

| Ad | Campaign | Format, angle | Spend | Purchases | Value | ROAS |
|---|---|---|---|---|---|---|
| Trust overload ("Buying fine gold online is not as scary as you think!") | Earrings, interest stack, 25 Jun | Video, social proof | ₹45,463 | 8 | ₹5,70,446 | 12.55 |
| Bestsellers Static (EOSS, up to 15% off till 5 Sep) | Sale, all funnel | Carousel, offer | ₹41,726 | 9 | ₹3,92,383 | 9.40 |
| Gifting ("Forget the guesswork") | Earrings, MOF + BOF ad set, 25 Jun | Video, occasion | ₹1,92,279 | 43 | ₹17,49,829 | 9.10 |
| All Products catalogue ("Did something catch your eye?") | BOF, add to cart 180 days | Catalog | ₹5,56,626 | 148 | ₹40,69,362 | 7.31 |
| Unboxing and Stop Motion (EOSS) | Sale, all funnel | Video, UGC | ₹1,42,757 | 22 | ₹10,12,256 | 7.09 |
| Dynamic image ads ("Everyday elegance, reimagined") | Chains, Dec | Image, occasion | ₹63,238 | 3 | ₹4,03,685 | 6.38 |
| Gifting (interest stack copy of the same video) | Earrings, 25 Jun | Video, occasion | ₹1,27,042 | 22 | ₹7,65,178 | 6.02 |
| Trust overload (earlier run) | Earrings, 1 Apr | Video, social proof | ₹1,90,750 | 34 | ₹11,35,682 | 5.95 |
| All Products catalogue (second BOF ad) | BOF, add to cart 180 days | Catalog | ₹5,61,473 | 123 | ₹32,57,015 | 5.80 |
| Chains Carousel (EOSS) | Sale, all funnel | Carousel, offer | ₹1,00,160 | 17 | ₹5,77,336 | 5.76 |

The 90-day list is the same names plus 2 earrings ads ("Educational" flexible ad 5.43, "Social proof" 5.06) and the MOF catalog ad (5.08) (`best10_90d.csv`).

### 10 worst, 12 months (`worst10_12m.csv`)

| Ad | Campaign | Format, angle | Spend | Purchases | Value | ROAS |
|---|---|---|---|---|---|---|
| Earrings Video Ads (no copy captured) | Earrings video, Dec | Flexible | ₹32,017 | 1 | ₹11,340 | 0.35 |
| Earrings Video Ads (no copy captured) | Earrings video, Dec | Flexible | ₹64,670 | 2 | ₹23,080 | 0.36 |
| All Products catalogue (Flora Prasad quote) | TOF broad, Jul | Catalog | ₹49,558 | 2 | ₹20,031 | 0.40 |
| Founder ads ("Real jewellery. Real trust.") | Founder video, May | Video | ₹44,245 | 1 | ₹21,480 | 0.49 |
| Tennis Bracelet (lab grown diamonds) | Broad, Aug | Video | ₹33,163 | 1 | ₹18,670 | 0.56 |
| Bracelets May Ads ("Discover our bestselling designs") | Bracelets, May | Carousel | ₹55,834 | 3 | ₹41,564 | 0.74 |
| Dynamic image ads ("Everyday elegance, reimagined") | Chains, Sep | Image | ₹35,809 | 1 | ₹28,735 | 0.80 |
| All Products catalogue (Flora Prasad quote) | TOF broad, Mar | Catalog | ₹36,877 | 2 | ₹31,880 | 0.86 |
| All Products catalogue (Flora Prasad quote) | TOF broad, Sep | Catalog | ₹41,004 | 1 | ₹39,582 | 0.97 |
| Generic Ads Nov (no copy captured) | Generic, Nov | Flexible | ₹32,892 | 1 | ₹31,940 | 0.97 |

6 more ads cleared the floor with no reported purchase at all (₹1,93,451 in total): a chains image ad, an older cut of Trust overload, the founder video "Thinking of buying jewellery online?", a November bracelets ad, a Problem/Solution ad and the multi-gemstone pendant video (`no_reported_purchase_at_floor_12m.csv`).

Two lessons: the same texts appear in both lists, so audience and image decide more than the caption; and every ad in the best 10 names a real reason to trust, a real occasion, or a real dated offer, while every ad in the worst 10 is a bare showcase, a founder story, or a catalog ad sent cold.

## 5. What the site promises

From the pages read on 24 Sep 2026:

- Home: 30,000+ orders delivered, 20+ years, BIS Hallmarked gold, 4.8 Google rating, 10,000+ happy customers, 7-day return and exchange, named Google reviews, personal styling and custom design bookings, Chennai store.
- Shipping and returns: free shipping and gift packing in India; tamper-proof box; insured in transit; 7-day return for full refund or exchange from delivery, India only; a Limited Lifetime Exchange Policy (gemstone pieces at 70% of prevailing market value, diamond at 80%, plain gold at the gold rate, silver excluded, invoice needed, coupon value deducted).
- FAQ: most pieces hand-made at the Chennai workshop, some outsourced; 1-year workmanship warranty; customer pays return shipping; in-stock pieces deliver in 2 to 3 days, made to order in 10 to 14 days; all gemstones natural; all pieces BIS Hallmarked; one free re-sizing within 15 days; COD, cards and net banking; prices move with gold and gem rates.
- Collection and product pages: prices from ₹9,640 to ₹1,69,930, no discount showing; badges like "TOP 3 in bracelets" and "3-day delivery"; gold weight in grams, stone list, setting, 18K or 14K option, an EMI table on every page read, expected delivery dates, free ring sizer and re-sizing on rings, custom bracelet length on request, a 1-inch adjustable loop on chains, lifetime repair with pick-up paid by the customer.

## 6. Claims in the copy against the approved list and the site

Approved list (brand record): BIS Hallmarked; 18K gold (14K on some chains); natural gemstones; handcrafted; 4.8/5 on Google; 10,000+ customers; free shipping; 7-day easy returns; 20+ years of craft.

| Claim in the ads | Spend carrying it | Approved? | On the site? | Verdict |
|---|---|---|---|---|
| BIS Hallmarked, 18K gold, 14K, natural gemstones, handcrafted, free shipping, 4.8/5 on Google, 7-day returns, 20+ years | most texts | Yes | Yes | Keep |
| Lifetime exchange | ₹36 lakh+ | No | Yes, as a Limited Lifetime Exchange Policy at 70% to 80% of market value | Use only with "policy" or "terms on site"; never as a full-value promise |
| Buyback available | ₹26,58,336 | No | Not found on the pages read | Confirm or drop |
| Shop with EMI; EMI on orders above ₹10,000 | ₹27 lakh+ | No | EMI tables are on product pages; the ₹10,000 floor was not found | "EMI available" is supportable; the floor needs confirming |
| Cash on delivery | ₹5 lakh+ | No | Yes (FAQ payments) | Keep |
| 100% handcrafted, 100% handmade | ₹27 lakh+ | Partly | FAQ says most pieces are hand-made in Chennai, some outsourced | Drop "100%"; say "handcrafted" |
| Customer counts: 5,000+, 8,000+, 8,500+, 10,000+, 10K+, 500+ | spread across ₹35 lakh+ | Only 10,000+ | Site says 10,000+ happy customers and 30,000+ orders | Use 10,000+ customers everywhere; 30,000+ orders only after confirming |
| 25,000+ orders shipped | ₹60,718 | No | Site says 30,000+ | Replace with the site figure or drop |
| 450+ verified reviews | ₹13,419 | No | Not found | Confirm on Google or drop |
| Natural and certified gemstones; certified diamonds; IGI certified | ₹11 lakh+ | No ("certified" is not on the list) | FAQ: natural gemstones, EF-VVS diamonds; IGI not found | Say "natural"; add "certified" only with the certificate named |
| India's largest gemstone collection | ₹2,10,732 | No | No | Unverifiable superlative; drop |
| India's first coloured lab-grown diamonds | ₹24,822 | No | No | Unverifiable; drop |
| Astrologically powerful | ₹2,67,684 | No | No | Belief claim with no proof; drop |
| 5% OFF with code GEHNA5 (headline on evergreen ads) | ₹3,80,824 | No | No live offer seen on the site | Confirm the code is live or remove the headline |
| Shipped in 48 hours; video of your piece on WhatsApp before shipment; since 2003; 15 years | under ₹50,000 | No | FAQ says 2 to 3 days, a photo on request, 20+ years | Use the site wording |
| Dated sale lines and lab grown diamonds (tennis bracelet) | ₹6 lakh+ | Offer rules; allowed for that product | Sales expired; product exists | Fine while live and product-specific |

Named customer quotes (Flora Prasad, Madhu Lika, Krity, Hari) appear in ads. Written permission for ad use is not on record here.

## 7. What is missing or weak

Audience. Nothing separates new buyers from past buyers. Warm ad sets sit inside prospecting campaigns and took 16% of spend at a better ROAS than the broad sets beside them. Men take 28% of spend at 1.53; ages 18 to 24 take 13% at 1.17.

Objective and funnel. Cold prospecting is 86% of spend at ROAS 2.84 and ₹10,943 per purchase. The whole bottom of the funnel is 3 catalog ads with 1 text, live since September 2025 (their 30-day ROAS is 2.78 against 4.50 over 90 days, an early fatigue sign). There is no past-customer campaign, no cart-abandoner ad that answers an objection, and no ad for the store's real after-sale promises (warranty, re-sizing, repair). Existing customers are not excluded from cold spend, and attribution settings differ across campaigns.

Offer. Evergreen ads carry "5% OFF with code GEHNA5" while the site shows no offer. The strongest offers ran only in dated sales, which returned 5 to 9 times spend but stopped when the sale ended. The site's evergreen offers (free shipping, gift packing, EMI, COD, 7-day return, free ring sizer) are stated inconsistently and never in the description field.

Proof. The counts contradict each other (5,000, 8,000, 8,500, 10,000, 25,000, 500). The product facts that would convince a considered buyer, gold weight in grams, stone type, setting, delivery date, EMI amount, are on every product page and in no ad.

Product. Half of spend is "mixed range". The best-returning product group (earrings) is the only one with a proof-led and a gift-led ad. Rings have had 45 ads and 3 purchases, and none of the ring copy addressed the real barrier to buying a ring online, which the site already solves (free sizer, free re-sizing). Chains, the highest ticket, get generic mood copy.

Copy craft. The most-spent headline says nothing about what is sold. 8 texts use "Gehna" as the headline. Description slots are empty on all 472 ads. First lines often run past the fold or open with a mood word ("Everyday elegance, reimagined") rather than the buyer's question.

## 8. Baselines carried into the plan

Cold evergreen prospecting, last 90 days: ROAS 3.55, ₹10,974 per purchase (12 months: 2.76, ₹11,354). Cart and site retargeting, last 90 days: ROAS 4.56, ₹6,814 per purchase. Past customers: no baseline exists. Monthly spend base: ₹11,12,000 (`baselines.json`, `budget_split.json`).
