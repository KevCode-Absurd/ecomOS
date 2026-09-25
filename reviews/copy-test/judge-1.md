# Judge 1: Gehna Meta copy audit, report-1 vs report-2

Blind read on 24 Sep 2026. I read report-1 in full, then report-2. Evidence: `data/meta-gallery/brand.json`, `data/meta-gallery/cache/gallery.json` (recomputed in Python), `raw-1/` and `raw-2/`, and the live site (home, FAQ, shipping and returns, 7 collection pages, 3 product pages).

## 1. Claim checks

| Report | Claim | What I checked | Result |
|---|---|---|---|
| 1 | 12 months: spend ₹1,29,59,908, 1,396 purchases, ROAS 3.28. 90 days (26 Jun to 23 Sep): ₹32,45,323, 348 purchases, ROAS 3.77 | Summed `daily` rows for all 472 ads, both windows | Verified. Exact match. |
| 1 | Retargeting is 11% of the year's spend at 6.5 (cart) and 4.6 (engagers) against 2.9 for prospecting. Current monthly spend ₹10,81,774 = last 90 days ÷ 3. Controls: Gifting ₹1,91,542, 43 purchases, 9.14; Trust overload 12.60; cart catalogue ₹2,69,597, 40 purchases, 4.46 | Campaign names BOF and MOF vs TOF; per-ad 90 day sums for the 3 live ads | Verified. BOF 8.7% + MOF 2.0%, ROAS 6.52, 4.64, 2.94. Per-ad figures match to the rupee. |
| 1 | Site facts used in the ads: 627 earrings, 156 rings, 148 chains, 34 pairs under ₹20,000, 294 pieces under ₹30,000, 46 best sellers; Verdant Whisper ring ₹24,850, Zambian emeralds, bezel, sizes 7 to 18; free resize within 15 days; 20% down over 2 to 6 months; 4 working days after last instalment; no documents; COD; ID proof on delivery; insured transit | Live pages on 24 Sep | Verified, with 2 caveats. The Nithyakumari quote is reworded, not "spelling tidied": the site says "So beautiful ❤️.i got my chain in 3 gms which is not easier to make such a design in that gms". "New this season" for the ring: no New Arrival tag found on the live page. Could not check. |
| 2 | 90 days: ₹32,24,679, 347 purchases, ₹1,29,42,450, ROAS 4.01. Last 30 days 5.64 | Summed `daily` for 27 Jun to 24 Sep and 26 Aug to 24 Sep | Verified for that window. But the window includes the partial day 24 Sep and the report does not say so. Its "product showcase 4.55" and "bracelets 4.21" over 90 days rest on 1 purchase worth ₹7,73,520 logged on 24 Sep against ₹39 of spend. Without that day they are 1.12 and 1.11, which is what report-1 shows. Report-2's own text says showcase ads returned "0.4 to 2.2", so its table and prose disagree. |
| 2 | "MOF + BOF" ad sets inside prospecting campaigns took ₹20,92,057 (16.1%) at 3.60. Earrings 18.9% of spend and 22.1% of purchases. Rings: 45 ads, 3 purchases. Attribution settings differ across campaigns | Ad set names with "MOF + BOF" in TOF campaigns; product tags; `attribution_setting` values | Verified. My filter gives ₹20,81,325 at 3.56 (name spelling differences). 4 attribution settings are in use. |
| 2 | Site facts: Celestial Navaratna bracelet 7 inches, 0.708 g gold, ₹22,210, in stock; Tantalizing Tourmaline eternity ring exists and is made to order; under ₹25,000 edit; warm CPM ₹113.71; GEHNA5 headline about ₹3,80,000; 1-year warranty with free repair and shipping paid | Live product pages, FAQ, headline spend from `ads` | Mixed. Bracelet and ring verified (ring ₹29,030, "Made to order" tag). Warm CPM verified (113.8). GEHNA5 headline spend is ₹3,33,474 to ₹3,67,407, so "about ₹3,80,000" is high but close. **Wrong:** the page it calls "the under ₹25,000 edit" is titled "Finer Jewellery Under 30,000 INR" and lists pieces up to ₹29,990 on 24 Sep. **Wrong:** the FAQ says damage is repaired "at a reasonable price". It does not say free repair with shipping paid. |

Both reports say the description slot is empty on all 472 ads. The capture has no description field, so neither author could have read it. Could not check, for both.

## 2. Claims in the 12 ads

Report-1: 21 `[confirm before launch]` tags in the ads (23 in the file, 2 in prose). Claims not on the approved list and not on a site page: 3. "Natural pearls" (NB-2): the site sells cultured freshwater pearls. The Nithyakumari quote (NB-4) is reworded and presented as a Google review. "Exchange Any Time" (PC-4 headline) overstates a Limited Lifetime Exchange policy; the body states the terms and the report lists the wording as a decision. No invented prices, offers or statistics.

Report-2: 14 `[confirm before launch]` tags in the ads (15 in the file, 1 in prose), including 2 empty date placeholders. Claims not on the approved list and not on a site page: 2 wrong, 1 unverified. "Gold Gifts Under ₹25,000" and "the under ₹25,000 edit" (NB-03) are false on the day the site was read. "We repair it free and pay the shipping" for warranty faults (SV-04) is not in the FAQ. "Share a sketch or a photo, and the team will come back with a design and a quote" (PC-04) is not on the pages I read; it is flagged. No invented statistics.

## 3. Scores

| Criterion | Report-1 | Report-2 |
|---|---|---|
| 1. Would the owner run these ads as written | 8 | 6 |
| 2. Editing effort (10 = none) | 8 | 6 |
| 3. Claim accuracy | 8 | 6 |
| 4. Specificity to Gehna and ecommerce | 8 | 8 |
| 5. Test plan quality | 8 | 6 |
| Total | 40 | 32 |

Notes on the scores.

Usability. Report-1's ads are written as ad lines: short, one idea per line, proof stack at the end, 1 emoji at line end, a destination URL and a picture plan for each. They use the brand's own copy patterns from brand.json (quote first, then "That's what 10,000+ Gehna customers sound like"). Report-2's ads are clean and honest but read as paragraphs, 2 carry blank dates, 1 carries a wrong price cap, and PC-04 is a lead ad in a purchase campaign, which the report itself flags.

Editing. Report-1 needs 3 small edits: "pearls" for "natural pearls", the quote verbatim or as initials, and a softer PC-4 headline. Report-2 needs the NB-03 headline and body rewritten, the SV-04 warranty line rewritten, 2 dates filled in, and a decision on PC-04's objective.

Accuracy. Both did the arithmetic in code and both match the data. Report-2 loses points for the ₹25,000 error, the warranty claim, and a 90 day window that quietly includes a partial day and inflates 2 categories. Report-1 loses points for the reworded quote and the exchange headline.

Specificity. Even. Report-2 has the sharper account diagnosis: warm audiences inside cold campaigns, 4 attribution settings, the GEHNA5 headline still running, hero-product ads with gold weight, a frequency-capped past-customer budget from the warm CPM. Report-1 has the sharper site and policy use: design counts, ID check at the door, 20% down over 2 to 6 months, free sizer and resize, and it caught that the "under 25k" URL is an under 30,000 page.

Test plan. Report-1's plan is internally consistent: every ad's 28 day budget exceeds its learning spend (₹37,862 vs ₹30,000; ₹24,340 vs ₹20,000; ₹18,931 vs ₹15,000). Kill at 60% and scale at 120% of the funnel baseline with 3+ purchases and a CPA cap, an early CTR stop, live ads as controls, the festive overlap named, a Monday sheet, 13 decisions. Report-2 has good rules (read at 3 times CPA, yellow band, judge at ad set level, stock-out makes a read inconclusive, 7-day click on all 3 campaigns) but the budget does not reach its own read points: site-visitor ad sets get ₹17,375 over 4 weeks against a ₹20,000 read. 2 controls are paused ads or ads launched 8 days ago. "Raise budget 20% a day, hold each step 7 days" contradicts itself.

## 4. Winner: report-1

1. Claim accuracy where it costs money. Report-1 has no wrong price, offer or policy claim in its 12 ads. Report-2 puts a false price cap in a headline and invents a free-repair-with-shipping promise. Both would have to be caught by the owner.
2. The ads are closer to launch. Report-1's ads follow the brand's line rhythm and patterns, carry destinations and a picture plan, and need 3 small edits. Report-2's need rewrites in 2 ads and dates in 2 more.
3. The plan can actually be read. Report-1's budgets clear its learning spends and its controls are live ads with their numbers. Report-2's site-visitor budget cannot reach its own read spend in 4 weeks.

## 5. Best 2 ads

**Report-1, RT-2 (rings, free sizer).**

> Not sure of your ring size? We'll send a free sizer to your door. 💍 [confirm before launch]
> Size is the hard part of buying a ring online. Here is how we make it easy.
> Pick the ring. Ask for a sizer. Order when it fits.
> Still wrong? One free resize within 15 days. [confirm before launch]
> 156 rings in 18K gold with natural emerald, ruby, sapphire and tourmaline.
> Made to order in your size. BIS Hallmarked. 7-day easy returns. ✨

Headline: Free Ring Sizer. Free Resize. 💍

Why: rings have 156 designs and 3 purchases in a year. This ad names the one reason rings fail online and answers it with 2 real policies. Every line is on the site. Report-2's NB-04 has the same idea; this one is tighter.

**Report-2, SV-01 (cart, delivery is on us).**

> Still thinking about it? It is still here, and the delivery is on us. ✨
> Free shipping anywhere in India. Insured all the way to your door, in a tamper-proof box.
> Pay by card, net banking, or cash on delivery.
> If it is not what you hoped, return it within 7 days of delivery for a full refund or exchange.
> BIS Hallmarked 18K gold. Natural gemstones. 4.8 on Google. 💛

Headline: Free Delivery | 7-Day Returns

Why: 68 words, nothing to confirm, every line on the shipping page or FAQ, and it replaces a 12 month old cart text that still says 5,000+ customers. Ready to paste.

## 6. Worst 2 ads

**Report-2, NB-03 (gifts under ₹25,000 for Diwali).**

> Real 18K gold and natural gemstones, in a price band that makes sense: the under ₹25,000 edit. [confirm before launch: every piece in the collection is under ₹25,000 that day]
> ...
> Order by [date, confirm before launch] for delivery before Diwali.

Headline: Gold Gifts Under ₹25,000

Why: the page is "Finer Jewellery Under 30,000 INR" with pieces to ₹29,990 on the day the author read it. The headline is a false price claim on a gift ad going to cold traffic. The order-by date is blank. Headline, body and date all need work before launch.

**Report-1, PC-4 (exchange up).**

> Your old Gehna piece can pay for your next one. ✨
> Bring back any Gehna gold piece with its invoice. We value it at today's rate and put that towards anything new. [confirm before launch]
> Gemstone pieces count at 70% of today's value. Diamond pieces at 80%. Plain gold at the gold rate. [confirm before launch]
> Snapped a chain or lost a stone? Our repair service across India fixes most pieces free. You pay only the pickup. [confirm before launch]

Headline: Exchange Any Time ✨

Why: the terms are quoted correctly, but "Exchange Any Time" and "any Gehna gold piece" promise more than a Limited Lifetime Exchange policy where the company sets the valuation and coupons are deducted. It packs 2 policies and 3 confirm flags into 1 ad for a list that may not exist yet. Report-2's PC-03 handles the same policy more carefully, if less warmly.

## 7. Which report used a specialist ecommerce playbook

Report-1, with moderate confidence. Its brief is a filled template: the question in her head and the one idea per audience, voice rules, claims in 3 tiers (free, confirm, never), a fixed skeleton in all 12 ads (worry or moment, material, policy, proof stack, count and CTA), and kill and scale lines as fixed percentages of a funnel baseline. It reuses the brand's copy patterns word for word and the house phrase "concrete before-to-after". That is what a copy playbook with an operating contract produces.

Report-2 reads like a strong media analyst working from the data and the site: ad set name forensics, an attribution audit, a CPM-based frequency cap, purchase-count reads with a yellow band. Those are buyer rules of thumb rather than a copy playbook, and the copy is less patterned.
