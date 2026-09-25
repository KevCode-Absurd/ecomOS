# Judge 2: blind review of report-1 and report-2

Read in full on 24 Sep 2026, report-2 first. Evidence: `brand.json`, `gallery.json` (arithmetic in Python), `raw-1/`, `raw-2/`, and gehnaindia.com fetched live (home, FAQ, shipping, 7 collection pages, 4 product pages).

## 1. Claim checks

| Report | Claim | What I checked | Result |
|---|---|---|---|
| 1 | 90 days (26 Jun to 23 Sep): spend ₹32,45,323, 348 purchases, value ₹1,22,21,710, ROAS 3.77, CPA ₹9,326 | Summed `daily` for day 276 to 365 | Verified to the rupee. Monthly figures for Jun, Jul, Aug and Sep also match. |
| 1 | 33 of 472 ads live; live ads took 49% of 90-day spend at 4.83, paused ads 2.87 | Status counts and 90-day sums by `effective_status` | 33 ACTIVE verified. Live share 49% and 4.83 verified. Paused computes to 2.74, not 2.87. Small slip. |
| 1 | Site counts: 627 earrings, 156 rings, 148 chains, 34 under ₹20k, 294 in the under-30k edit, 46 best sellers; Verdant Whisper ring ₹24,850, sizes 7 to 18, bezel set, Zambian emeralds | `__NEXT_DATA__` totals on each collection page; product page JSON | All 6 counts verified live. Price ₹24,850, bezel setting and made-to-order sizes verified. Site says "most" emeralds are Zambian; the ad says "Natural Zambian emeralds", a slight stretch. |
| 1 | Bottom 10: "2 bracelet flexible ads with 0 and 1 purchases on ₹31,755 and ₹64,670" | Per-ad sums and product tags | Wrong. ₹31,755 is a bracelets ad with 0 purchases; ₹64,670 is an earrings ad with 2 purchases. |
| 1 | 27 ads above ₹30,000 in 90 days; ROAS quartiles 1.49, 3.09, 5.49 | Recomputed | Verified. |
| 2 | 12 months ₹1,29,59,908, 1,396 purchases, ₹4,24,86,365, 3.28; 90 days (27 Jun to 24 Sep) ₹32,24,679, 347, ₹1,29,42,450, 4.01; 30 days 5.64 | Summed `daily` | Verified to the rupee. Note the window includes 24 Sep, a partial day with 1 order of ₹7,73,520. That 1 order lifts the 90-day ROAS from 3.77 to 4.01. |
| 2 | Bracelets 90-day return 4.21; product showcase 90-day 4.55 | Recomputed with and without 24 Sep | Arithmetic is right but fragile. Without 24 Sep, bracelets are 1.11 and showcase 1.12. One order on a partial day is doing all the work, and the report does not say so. |
| 2 | Celestial Navaratna bracelet: 18K, 7 inches, about 0.7 g gold, ₹22,210, in stock, 3-day delivery; Tantalizing Tourmaline ring exists, made to order in 10 to 14 days | Product page JSON, FAQ | Verified: 0.708 g, 7 inches, ₹22,210, InStock, delivery date 27 Sep. The ring exists at a different slug and is made to order at ₹29,030. FAQ says 10 to 14 days. |
| 2 | Warm CPM ₹113.71 used for the past-customer cap; rings 45 ads and 3 purchases; earrings 18.9% of spend, 22.1% of purchases, 4.19 | Recomputed | Verified (BOF plus MOF CPM 113.81 in my run, rounding). |
| 2 | Claims audit spend: buyback ₹26,58,336; EMI ₹27 lakh+; "100%" ₹27 lakh+; "largest" ₹2,10,732; astrological ₹2,67,684 | Keyword sums over primary text spend | All verified. |
| both | "Descriptions are empty on all 472 ads" | `creative` keys in the cache | Could not check. The cache has no description field at all, so neither author could know this. Both state it as fact. |

Site policy facts both reports lean on were all verified live: free shipping and gift packing; transit insurance; tamper-proof box; 7-day full refund or exchange with the customer paying return shipping; the limited lifetime exchange terms (70%, 80%, gold rate, silver excluded, invoice required); one free re-sizing within 15 days; 1-year workmanship warranty; 2 to 3 days in stock, 10 to 14 made to order; COD; EMI at 20% down over 2 to 6 months with no documents; ID proof on delivery; free ring sizer; the 1-inch chain loop and lifetime repair (chain product FAQ); 1-on-1 consultation, custom design and Chennai trials.

## 2. Claims in the 12 ads

Approved list: BIS Hallmarked, 18K gold, natural gemstones, handcrafted, 4.8 on Google, 10,000+ customers, free shipping, 7-day returns, 20+ years.

**Report-1.** 23 items marked `[confirm before launch]`. Claims not on the approved list and not on a site page: 2. (a) PC-4 headline "Exchange Any Time" broadens a policy the site calls "Limited Lifetime Exchange" (the report flags this in decision 12). (b) PC-2 "Natural Zambian emeralds" where the page says most are Zambian. Two customer quotes are lightly tidied, and the edits are disclosed. Everything else traces to the approved list, the FAQ, the shipping page or a live product or collection page.

**Report-2.** 15 items marked `[confirm before launch]` (13 plus 2 order-by dates). Claims not on the approved list and not on a site page: 1. NB-03 sells "Gold Gifts Under ₹25,000" and "the under ₹25,000 edit", but the landing page is titled "Finer Jewellery Under 30,000 INR" and report-1 read prices up to ₹29,990 on it. The report flags the cap, but the ad is wrong as written today. Every other line traces to the approved list or a site page. The Jai Singh quote is verbatim.

Neither report invents a price, discount or statistic. Both drop buyback, IGI, "100% handcrafted" and the old customer counts.

## 3. Scores

| Criterion | Report-1 | Report-2 |
|---|---|---|
| 1. Would the owner run the ads as written | 8 | 7 |
| 2. Editing effort before launch (10 = none) | 7 | 6 |
| 3. Claim accuracy | 8 | 8 |
| 4. Specificity to Gehna and ecommerce | 9 | 9 |
| 5. Test plan quality | 8 | 9 |
| Total | 40 | 39 |

Why. Report-1's ads are 5 to 8 lines and follow the brand file closely: question or quote openers, proof stack at the end, 1 emoji per line, product plus proof headlines. The cost is live counts (627, 294, 148, 46) that change weekly; the report offers "hundreds" as the fix. Report-2's ads are 66 to 105 words and fully sourced, but 4 of the 12 (SV-04, PC-03, PC-04 and the second half of NB-04) read like policy pages, PC-03 tells a past customer her piece is worth 70% and that coupons are deducted, and NB-03 needs a new cap or a new landing page. Claim accuracy is a tie: report-1 mislabels 2 bottom-10 ads and misstates the paused ROAS; report-2 lets 1 partial-day order set its 90-day bracelet and showcase figures and states a ₹25,000 cap the page does not support. On the plan, report-2 is better: reads are triggered by spend equal to 3 CPAs and judged on purchase counts first, there is a yellow band, the past-customer budget is capped by list size times CPM times frequency, controls are named with their numbers, and its standing rules are the ones that stop bad calls. Report-1's plan is also sound: quartiles from the account, kill at 60% and scale at 120% of baseline, a CTR early stop, a festive-overlap warning, and the control comparison as the verdict. Its weak points: 4 warm ad sets on 1 audience (report-2 shares this and admits it) and a budget cut from current spend without saying what is cut.

## 4. Winner: report-1, by a narrow margin

1. The ads need less work. Report-1's copy is closer to the voice in the brand file and to the account's own winners. The owner could paste 9 or 10 of them after confirming the flags. Report-2 needs NB-03 rebuilt and 3 or 4 ads cut in half before they sound like an ad.
2. Fewer errors in the ad copy itself. Report-1's slips are in the analysis (2 mislabeled ads, one ROAS). Report-2's slips reach the ads (the ₹25,000 cap) and the tables that justify them (bracelets 4.21 on 1 order).
3. It speaks to buyers the account ignores. Report-1 sends the gift ad to men, who take 28% of spend at 1.53 with no gift copy, and treats it as the first honest read on them. Report-2 leaves men as a yes or no question.

Report-2 wins the plan. Take its section 9 and run report-1's ads through it.

## 5. Best 2 ads

**Report-1, RT-2 (rings, free sizer).** "Not sure of your ring size? We'll send a free sizer to your door. 💍 / Size is the hard part of buying a ring online. Here is how we make it easy. / Pick the ring. Ask for a sizer. Order when it fits. / Still wrong? One free resize within 15 days. / 156 rings in 18K gold with natural emerald, ruby, sapphire and tourmaline. / Made to order in your size. BIS Hallmarked. 7-day easy returns. ✨" Headline: Free Ring Sizer. Free Resize. 💍. One objection, one answer, every line verified, aimed at the category with 156 designs and 3 purchases a year.

**Report-2, SV-01 (still here, delivery on us).** "Still thinking about it? It is still here, and the delivery is on us. ✨ / Free shipping anywhere in India. Insured all the way to your door, in a tamper-proof box. / Pay by card, net banking, or cash on delivery. / If it is not what you hoped, return it within 7 days of delivery for a full refund or exchange. / BIS Hallmarked 18K gold. Natural gemstones. 4.8 on Google. 💛" Headline: Free Delivery | 7-Day Returns. Description: Cash on delivery available. Nothing to confirm, and it replaces a retargeting text that still says 5,000+ customers.

## 6. Worst 2 ads

**Report-2, NB-03 (gifts under ₹25,000).** "Real 18K gold and natural gemstones, in a price band that makes sense: the under ₹25,000 edit. [confirm before launch: every piece in the collection is under ₹25,000 that day] ... Order by [date, confirm before launch] for delivery before Diwali." Headline: Gold Gifts Under ₹25,000. The landing page is titled "Finer Jewellery Under 30,000 INR" and holds pieces up to ₹29,990. The headline is false today and the ad has 2 placeholders.

**Report-1, PC-4 (exchange up).** "Your old Gehna piece can pay for your next one. ✨ / Bring back any Gehna gold piece with its invoice. We value it at today's rate and put that towards anything new. [confirm before launch] / Gemstone pieces count at 70% of today's value. Diamond pieces at 80%. Plain gold at the gold rate. [confirm before launch] / Snapped a chain or lost a stone? Our repair service across India fixes most pieces free. You pay only the pickup. [confirm before launch] ..." Headline: Exchange Any Time ✨. The headline broadens a limited policy, the body mixes exchange, repair and heritage in one ad, and it carries 4 flags. Report-2's PC-03 has the same problem in a duller form: it reads the T&C page to a past customer.

## 7. Playbook guess

Report-2 used the specialist playbook. The signs: a per-ad "Claim check" line in a fixed format; a code pass that reports first-line characters, headline and description lengths, word counts, reading grade and emoji counts; reads triggered at 3 CPAs of spend with a keep, yellow, kill and scale table; a frequency-based cap for the past-customer campaign; standing rules like "never read fewer than 7 days" and "a stock-out makes a read inconclusive"; and the objective split into buying question, one idea, voice, claims used. That is an operating contract, not a memo.

Report-1 reads as an experienced buyer working from the brief and the brand file. Two openers come straight from `brand.json` copy patterns ("Thinking of buying jewellery online? 🤔" and "That's what 10,000+ Gehna customers sound like. 💬"), its rules are the common ones (60% and 120% of baseline, a CTR stop), and its judgement calls (3 orders is luck, festive overlap, men as a read) come from practice, not a checklist. That is also why its ads sound more like Gehna.
