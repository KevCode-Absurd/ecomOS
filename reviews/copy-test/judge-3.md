# Judge 3: Gehna Meta copy audit, blind A/B

Read in order: report-1.md, then report-2.md. Checked against brand.json, gallery.json (my own Python), raw-1 and raw-2, and gehnaindia.com on 24 Sep 2026. Day 0 in gallery.json is 23 Sep 2025; day 366 is 24 Sep 2026, a partial day captured at 09:18 IST.

## 1. Claim checks

| Report | Claim | What I checked | Result |
|---|---|---|---|
| 1 | 90 days (26 Jun to 23 Sep): spend ₹32,45,323, 348 purchases, ₹1,22,21,710, ROAS 3.77, CPA ₹9,326 | Summed daily rows for days 276 to 365 | Verified exactly. Retargeting 90d (₹4,93,785, 73, ₹22,58,272, 4.57, CPA ₹6,764) also exact. |
| 1 | Only 33 of 472 ads live; the cart text "Did something catch your eye?" is 5 ads, ₹13,87,998, ROAS 6.16 and says "5000+ happy customers" | effective_status counts; grouped ads by primary_text | Verified. 33 ACTIVE. 5 ads, ₹13,87,998, 6.16. Text says 5000+. |
| 1 | Site counts and prices used in the ads: 627 earrings, 156 rings from ₹13,500, 148 chains, 34 under ₹20,000 (₹13,490 to ₹19,980), 294 under ₹30,000, 46 best sellers, Verdant Whisper ring ₹24,850, sizes 7 to 18, Zambian emeralds, free sizer | Parsed the pages' Next.js data on 24 Sep | Verified, every figure. "New this season" tag: could not find on the page. |
| 2 | 90 days: ₹32,24,679, 347 purchases, ₹1,29,42,450, ROAS 4.01; last 30 days 5.64; bracelets 4.21 and product showcase 4.55 over 90 days | Days 277 to 366 and 337 to 366 | Arithmetic verified, but the window includes the partial day 24 Sep, which holds 1 order of ₹7,73,520 on ₹39 of spend (a paused-campaign bracelet showcase ad). Without that day bracelets are 1.11 and showcase 1.12, which is what report 1 says. The 5.64 falls to about 5.2. |
| 2 | Prospecting ₹1,11,39,757 at 2.84; cart and site retargeting ₹11,24,139 at 6.52, ₹4,133 per purchase; "MOF + BOF" ad sets ₹20,92,057 at 3.60; warm CPM ₹113.71 | Grouped by campaign and ad set names | Verified. My figures: prospecting 2.83, BOF exact, MOF + BOF exact, warm CPM ₹113.81. Engager ₹3,11,209 at 4.10 is close (my 2 campaigns give 4.64, 13 ads with review ads give 4.11). |
| 2 | "EMI above ₹10,000: the ₹10,000 floor was not found on the site" (claims table, SV-02 and decision 6) | FAQ page, EMI section | Wrong. The FAQ says "the minimum cart value is 10000 INR to avail the EMI plan." The old ads were right. |

Other checks. Empty descriptions on all 472 ads: gallery.json has no description field, so could not check (raw-1 shows blank for all 472). Missing customer list and exclusions: no targeting data in the cache, could not check. Attribution settings do differ (313 ads on one setting, 134 on another, 24 incrementality): report 2 verified. Both monthly spend figures are exact. Report 2's GEHNA5 spend is "about ₹3,80,000" in the text but ₹3,33,474 in its own raw table.

## 2. Claims in the 12 ads

Site facts that hurt both: the under ₹30,000 edit and the best-seller page both list "Synthetic Pearl" and "Lab Grown Diamond" filters, and best sellers include a 14K lab-grown pendant. The under ₹20,000 earrings page lists cultured and synthetic pearls. "Lifetime repair, most repairs free" is not on the FAQ, product pages I read, or the shipping page; the FAQ says damage repairs are "at a reasonable price" and only making faults are free under the 1-year warranty.

Report 1. Claims not on the approved list and not backed by a site page: 5. "Natural pearls" for the under ₹20,000 page (NB-2, PC-3; that page has synthetic pearls). "Every one is 18K gold" on best sellers (RT-4; a 14K pendant is there). "Exchange Any Time" as a headline for a limited policy (PC-4). "Fixes most pieces free" (PC-4, flagged). The Jai Singh quote is shortened without saying so (RT-4). "Every chain has a 1-inch loop" is one product FAQ stretched to 148 chains (NB-4, PC-1). `[confirm before launch]` tags: 22 across 10 ads.

Report 2. Claims not on the approved list and not backed by a site page: 4. "Under ₹25,000" headline and text landing on an edit priced up to ₹29,990 (NB-03; the flag asks to confirm a cap the page already fails), and "chains" in an edit that has no chains filter. "Every piece is BIS Hallmarked 18K gold with natural gemstones" on best sellers (SV-03, marked "Nothing to confirm"). "Most repairs are free" (SV-04, flagged). "A 1-inch adjustable loop" on all chains (SV-04, PC-01). `[confirm before launch]` tags: 11, plus 2 `[date, confirm before launch]` placeholders, so 13.

Report 2 quotes the review verbatim and says so. Report 1's policy details (ID check at the door, 20% down over 2 to 6 months, 4 working days, no documents) all verified.

## 3. Scores

| Criterion | Report 1 | Report 2 |
|---|---|---|
| 1. Would the owner run these ads as written | 7 | 6 |
| 2. Editing effort (10 = none) | 7 | 6 |
| 3. Claim accuracy | 7 | 6 |
| 4. Specificity to Gehna and ecommerce | 9 | 8 |
| 5. Test plan quality | 8 | 7 |
| Total | 38 | 33 |

Notes on the scores. Report 1's ads follow brand.json's copy patterns (question or quote first, one idea per line, proof stack last, an emoji at the end of a line) and read like the account's best live texts. Report 2's ads are 3 to 6 paragraphs of 66 to 105 words with explanatory sentences ("Buying gold online feels like a leap. Here is what comes with every pair"); the brand file asks for short lines, so more trimming is needed before launch. Report 1 puts design counts and prices in 8 ads, so weekly edits (it says so in decision 4). Report 2 avoids counts but leaves 2 date placeholders and a wrong price cap.

On the plan: report 1's budgets reach its own read points (new buyers ₹1,352 a day gets to ₹30,000 by day 23; visitors ₹869 a day gets to ₹20,000 by day 24). Report 2's site-visitor ad sets get ₹621 a day, ₹17,375 in 28 days, below its own ₹20,000 read spend, so 4 of 12 ad sets cannot be read on the plan's own rule. Its scale rule ("raise budget 20% a day, hold each step 7 days") contradicts itself. Report 2 does 3 things report 1 does not: it moves all 3 campaigns to 7-day click so old and new are comparable, it caps past-customer spend by list size and frequency (customers × CPM ÷ 1,000 × 6), and it runs each concept on 3 owned visuals so the read is about the idea. Report 1 does 3 things report 2 does not: quartiles of the 27 live ads above the floor so its kill and scale lines are placed against real spread, an early CTR stop that no top ad of the year would trip, and a festive-season caveat with the control comparison as the verdict.

## 4. Winner: Report 1

1. Less rewriting. The ads are already in the brand's shape and length. Report 2's ads need cutting into lines and the NB-03 headline needs a new number before anything can run.
2. The numbers behind the recommendations are cleaner. Report 1 stopped at 23 Sep. Report 2 included the partial 24 Sep, and 1 order of ₹7,73,520 on ₹39 of spend turns bracelets from 1.11 to 4.21 and product showcase from 1.12 to 4.55. Report 2 then leads its plan with a bracelet showcase ad (NB-02). It also states the EMI floor is not on the site when the FAQ says ₹10,000.
3. The test plan is executable as written. Every threshold is derived from the 90-day account, every ad set reaches its read spend inside 28 days, and the owner gets 13 concrete decisions. Report 2's plan has better structural ideas (attribution, frequency cap, concept over file) but its visitor budgets cannot reach its own read rule.

## 5. Best 2 ads

Report 1, RT-2. "Not sure of your ring size? We'll send a free sizer to your door. 💍 / Size is the hard part of buying a ring online. Here is how we make it easy. / Pick the ring. Ask for a sizer. Order when it fits. / Still wrong? One free resize within 15 days." Rings have 156 designs and 3 purchases in a year; this is the first ad in the account that answers why. Every fact is on the FAQ or ring page. Headline "Free Ring Sizer. Free Resize." is a real reason to click.

Report 2, NB-01. "Real 18K gold. Natural stones. And 7 days to change your mind. ✨ ... Not right for you? Return it within 7 days of delivery for a full refund or exchange. You pay only the return courier. / That is how 10,000+ customers bought their first Gehna piece, and why we hold a 4.8 rating on Google. 💛" Nothing to confirm, the return-courier line is honest, and it sits on the account's best category with the trust video as control. It only needs its paragraphs shortened.

## 6. Worst 2 ads

Report 2, NB-03. "Real 18K gold and natural gemstones, in a price band that makes sense: the under ₹25,000 edit. ... Earrings, bracelets, chains and pendants. ... Order by [date, confirm before launch] for delivery before Diwali." Headline "Gold Gifts Under ₹25,000". The landing page is "Finer Jewellery Under 30,000 INR", priced ₹10,100 to ₹29,990, with no chains filter and with synthetic pearl and lab-grown items in it. The price promise fails on day 1 and the ad depends on a date the owner has not given.

Report 1, PC-4. "Your old Gehna piece can pay for your next one. ✨ / Bring back any Gehna gold piece with its invoice. We value it at today's rate ... Gemstone pieces count at 70% of today's value. Diamond pieces at 80%. ... Our repair service across India fixes most pieces free. You pay only the pickup." Headline "Exchange Any Time". The policy is "limited", the company sets the valuation, coupons are deducted, and the free-repair line is not on the site. It puts a policy table into an ad and overstates it in the headline. Report 2's PC-03 has the same idea, states the limits more fully, and reads like terms and conditions; neither should run before the owner answers decision 12.

## 7. Which report used the specialist playbook

Both share one skeleton: the 3 objectives, "the question in her head and the one idea", `[confirm before launch]`, a ₹28,000 to ₹30,000 spend floor at 3 times CPA, and the same length limits (first line 125 characters, body 300 words, headline 40, description 30). That looks like a common brief.

My guess is Report 2. Its plan carries rules that read as imported checklist items rather than things the data suggested: "never read fewer than 7 days", "judge at the ad set level, never on 1 ad's return", "never edit a winning ad set, add new creative beside it", "a stock-out or tracking gap makes a read inconclusive, not lost", a Keep, Yellow, Kill table, read spend at 3 times CPA "rounded to ₹1,000", the frequency-cap formula, a claims log, and reading-grade scoring of every ad "in code". Its ad format is also fixed: hook, explainer, proof, claim check, in the same order 12 times. Report 1 reads as an analyst working from the account: it computes quartiles, treats a 3-order winner as luck, and adjusts for the festive overlap. If the playbook is the source of Report 2's discipline, it also explains why its copy is longer and more uniform than the brand's own best texts.
