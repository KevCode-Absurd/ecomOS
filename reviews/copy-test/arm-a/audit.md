# Gehna Meta ad copy audit

Prepared 24 Sep 2026. Data: the Meta ad account export in `data/meta-gallery/cache/gallery.json` (472 ads, 23 Sep 2025 to 24 Sep 2026), `data/meta-gallery/brand.json`, and public pages on gehnaindia.com. Every table below is saved under `reviews/copy-test/arm-a/raw/` and was built by `raw/build_tables.py` (ad data) and `raw/site_snapshot.py` (site). All arithmetic was done in those scripts.

Definitions. 12 months = the whole window, 23 Sep 2025 to 24 Sep 2026 (24 Sep is a partial day). 90 days = 26 Jun to 23 Sep 2026, 90 full days. ROAS = total purchase value ÷ total spend for the period. CPA = spend ÷ purchases. Where Meta returned no value, the cell is unavailable, not 0; the scripts skip those cells and count them. The captured ads cover ₹1,29,59,908 of the ₹1,29,60,904 the account reports for the window (99.99%), so the export is effectively the whole account. Attribution is the ad set default (mostly 1-day view, 7-day click, 1-day engaged view). Age, gender and platform figures come from a separate monthly breakdown pull and are never added to the daily totals.

## 1. What the account looks like

| | 12 months | 90 days |
|---|---|---|
| Spend | ₹1,29,59,908 | ₹32,45,323 |
| Purchases | 1,396 | 348 |
| Purchase value | ₹4,24,86,365 | ₹1,22,21,710 |
| ROAS | 3.28 | 3.77 |
| CPA | ₹9,284 | ₹9,326 |
| Average order | ₹30,434 | ₹35,120 |
| CTR (all clicks) | 4.06% | 4.03% |
| CPM | ₹38 | ₹33 |
| Ads with spend | 472 | 121 |

Source: `raw/account_totals.json`, `raw/monthly_account.csv`.

Monthly spend has been steady at about ₹10 lakh: ₹10,06,127 in June, ₹10,19,234 in July, ₹13,10,492 in August (End of Season Sale), ₹7,99,454 for 1 to 23 Sep. Current monthly spend, taken as the last 90 days divided by 3, is ₹10,81,774. Monthly ROAS ranged from 1.60 (March 2026) to 4.70 (September 2026 so far). August and September are the two best months of the year on ROAS, without the biggest spend.

Structure. 88.8% of 12-month spend is prospecting ("TOF" campaigns on broad, interest, lookalike and "combo" audiences). Retargeting is small: 8.7% on cart and 180-day catalogue retargeting ("BOF") and 2.0% on engagers and catalogue viewers ("MOF"). Over the last 90 days retargeting is 15.2% of spend (BOF ₹3,65,304, MOF ₹1,28,481). No campaign or ad set name refers to past customers. There is no customer-list or repeat-purchase audience anywhere in the account.

Ad set audiences are named Broad, Interest stack, Lookalike stack, Purchase lookalike and "MOF + BOF". They are stacked inside almost every campaign, so the same creative runs to cold and warm people with the same copy.

Formats over 12 months: Flexible or mixed-media ads 32.8% of spend, Catalog 31.2%, Video 22.5%, Single image 7.3%, Carousel 6.2%. Over 90 days video and catalog each take about 38%. The 139 flexible ads expose no primary text, headline or link in the export, so their copy is unavailable. That is one third of the year's spend whose words cannot be audited from this data. Source: `raw/by_format_12m.csv`, `raw/by_format_90d.csv`.

Where the money went by month and audience (breakdown pull, separate from totals): women take 71% of spend and return ROAS 3.98; men take 28% and return 1.53. Ages 35 to 44 return 4.21 and 45 to 54 return 3.99; 18 to 24 take 12.6% of spend and return 1.17. Over the last 3 months the picture is sharper: 55 to 64 returns 6.61 and 18 to 24 returns 1.06. Instagram is 50% of spend at ROAS 3.88; Facebook 48% at 2.63. Source: `raw/audience_breakdowns.json`.

## 2. Copy the account runs today

Only 33 of 472 ads are active. Active ads spent ₹15,89,630 in the last 90 days (49% of spend) and returned ROAS 4.83; paused ads returned 2.87. The account has been switching off what does not work. Source: `raw/by_status_90d.csv`, `raw/active_ads_90d.csv`.

Five primary texts carry most of the year's readable copy spend (`raw/primary_text_12m.csv`):

1. ₹26,58,336 (20.5%), 43 catalogue ads, ROAS 2.18. The Flora Prasad review, then "We have everything you need to bring an unmatched shine to your beauty", then a tick list: Lifetime Exchange, Shop with EMI, 100% Handcrafted, Buyback available. This is the default prospecting catalogue text.
2. ₹13,87,998 (10.7%), 5 retargeting catalogue ads, ROAS 6.16. "Did something catch your eye?" then lightweight everyday options, 7 Days Return promise, "5000+ happy customers". The strongest text in the account, but the customer number is out of date.
3. ₹7,59,634 (5.9%), 8 earrings videos, ROAS 3.93. "When more than 8,500 people have lived the Gehna experience" then the proof stack: 18K BIS Hallmarked Gold, Natural and Certified Gemstones, Free shipping + Lifetime exchange.
4. ₹3,24,426 (2.5%), 7 earrings videos, ROAS 7.93. "Forget the guesswork. The best gift for her has always been jewellery she'll actually reach for, every single day."
5. ₹3,11,658 (2.4%), 8 earrings videos, ROAS 5.65. "Buying fine gold online is not as scary as you think!"

Headlines are few. "Redesigning beauty" sits on ₹38,26,013 of catalogue spend. "Handcrafted 18K Gold | 4.8/5 on Google" on ₹10,71,291 (ROAS 4.43). "Gehna" alone on ₹10,24,155. "Natural Gemstones | 18K Gold" on ₹3,24,426 (ROAS 7.93). No ad in the export has a description field filled. 443 of 472 ads have no link URL in the creative record, and 318 use Shop Now.

Patterns: a review quote or a question as the opener, then a short list of product features, then a proof stack of 3 to 4 items. The proof stack is close to the brand voice. The middle line is where copy drifts into inflated words ("unmatched shine", "transcendent", "opulent").

## 3. Spend and value by angle, hook and product

Source: `raw/by_angle_12m.csv`, `raw/by_angle_90d.csv`, `raw/by_hook_*.csv`, `raw/by_product_*.csv`. Angle, hook and product labels are the tags in the export.

### Angle

| Angle | 12m spend | 12m value | 12m ROAS | 90d spend | 90d value | 90d ROAS |
|---|---|---|---|---|---|---|
| Catalog (Meta picks products) | ₹40,46,333 | ₹1,43,41,667 | 3.54 | ₹12,46,757 | ₹36,68,627 | 2.94 |
| Product showcase | ₹23,14,725 | ₹68,30,378 | 2.95 | ₹2,28,981 | ₹2,56,487 | 1.12 |
| Gifting / occasion | ₹15,70,738 | ₹55,79,695 | 3.55 | ₹3,70,870 | ₹25,33,676 | 6.83 |
| UGC / unboxing | ₹15,53,005 | ₹44,15,499 | 2.84 | ₹2,01,964 | ₹10,45,069 | 5.17 |
| Social proof / reviews | ₹12,89,949 | ₹51,77,041 | 4.01 | ₹5,43,457 | ₹22,63,424 | 4.16 |
| Education / objection handling | ₹11,69,044 | ₹24,60,250 | 2.10 | ₹3,13,092 | ₹8,57,710 | 2.74 |
| Offer / urgency | ₹5,21,288 | ₹26,14,795 | 5.02 | ₹2,55,160 | ₹14,43,226 | 5.66 |
| Founder / brand story | ₹4,94,825 | ₹10,67,041 | 2.16 | ₹85,041 | ₹1,53,490 | 1.80 |

Reading: gifting, social proof and offer are the angles that return above the account average in both windows. Product showcase (ads that just show the piece with no argument) took ₹23 lakh over the year for ROAS 2.95 and has collapsed to 1.12 in the last 90 days. Founder story and education are below average in both windows. The catalogue is the biggest line and sits at the average; its retargeting half is good (6.5 ROAS over the year for BOF) and its prospecting half is weak (the broad catalogue campaigns return 1.2 to 2.4 in the last 90 days).

### Hook (first line)

| Hook | 12m spend | 12m ROAS | 90d spend | 90d ROAS |
|---|---|---|---|---|
| Statement | ₹55,90,871 | 2.70 | ₹17,40,315 | 3.27 |
| No text (flexible ads, copy unavailable) | ₹42,45,241 | 3.02 | ₹4,57,108 | 2.21 |
| Question | ₹14,68,525 | 5.87 | ₹4,99,184 | 4.52 |
| Proof or number | ₹9,65,657 | 2.65 | ₹1,14,242 | 5.62 |
| Price or offer | ₹6,62,300 | 4.99 | ₹4,34,474 | 6.05 |
| Urgency | ₹27,313 | 3.79 | unavailable in 90d | |

Questions and offers beat statements by a wide margin. The question hook is mostly one text ("Did something catch your eye?") on retargeting, so part of that gap is audience, not words. Even so, the statement openers, which carry 43% of spend, are the weakest readable group.

### Product group

| Product | 12m spend | 12m value | 12m ROAS | 90d spend | 90d value | 90d ROAS |
|---|---|---|---|---|---|---|
| Mixed range | ₹66,15,890 | ₹2,21,03,987 | 3.34 | ₹16,26,785 | ₹56,90,478 | 3.50 |
| Earrings | ₹24,54,671 | ₹1,02,85,176 | 4.19 | ₹11,52,133 | ₹55,91,123 | 4.85 |
| Bracelets | ₹22,30,398 | ₹65,00,110 | 2.91 | ₹2,48,321 | ₹2,75,157 | 1.11 |
| Chains / necklaces | ₹11,08,947 | ₹24,44,005 | 2.20 | ₹1,15,865 | ₹5,77,336 | 4.98 |
| Pendants | ₹3,86,053 | ₹10,11,000 | 2.62 | unavailable | | |
| Rings | ₹1,63,948 | ₹1,42,086 | 0.87 | ₹1,02,219 | ₹87,616 | 0.86 |

Earrings are the engine: 19% of yearly spend, 24% of value, and 46% of value in the last 90 days from one campaign ("Earrings Ads, Combo Audiences, 25/06": ₹10,48,883 spend, ₹54,15,340 value, ROAS 5.16). Rings have had 45 ads, ₹1,63,948 and 3 purchases. The ring copy is the closest to the brand voice in `brand.json` ("Stack them. Layer them. Never take them off.") and it did not sell. Bracelets did well last winter and have fallen to 1.11.

### Campaign theme

Sale and countdown campaigns took only 6.1% of yearly spend and returned 5.47; festival campaigns 4.2% at 2.75; evergreen 58.5% at 2.95; catalogue 31.2% at 3.54. Over 90 days the End of Season Sale campaign spent ₹3,78,502 for ₹22,26,788 (5.88). Source: `raw/by_theme_*.csv`, `raw/by_campaign_90d.csv`.

## 4. Best and worst ads by ROAS

Spend floor: 3 × the period CPA, rounded to ₹5,000. Both periods give ₹30,000. At that spend an average ad has bought about 3 orders, so a zero is a signal, not noise. 83 ads clear the floor over 12 months; 27 over 90 days. Median ROAS above the floor: 2.19 (12m), 3.09 (90d). Source: `raw/spend_floor.json`, `raw/top10_roas_*.csv`, `raw/bottom10_roas_*.csv`.

Top 10, 12 months (spend, purchases, ROAS):

1. Trust overload, earrings video, "Buying fine gold online is not as scary as you think!" ₹45,463, 8, 12.55. Active.
2. Bestsellers Static, EOSS carousel, "End of Season Sale is LIVE!! Up to 15% OFF" ₹41,726, 9, 9.40. Paused.
3. Gifting, earrings video, "Forget the guesswork." ₹1,92,279, 43, 9.10. Active.
4. All Products, BOF catalogue, "Did something catch your eye?" ₹5,56,626, 148, 7.31. Active.
5. Unboxing and Stop Motion, EOSS video, "10K+ Customers Love Gehna" ₹1,42,757, 22, 7.09. Paused.
6. Dynamic image ads, chains, "Everyday elegance, reimagined" ₹63,238, 3, 6.38 (3 orders, high value; treat as luck).
7. Gifting (second placement), earrings video ₹1,27,042, 22, 6.02. Active.
8. Trust overload (April run) ₹1,90,750, 34, 5.95. Paused.
9. All Products, BOF catalogue (26/03 copy) ₹5,61,473, 123, 5.80. Active.
10. Chains Carousel, EOSS ₹1,00,160, 17, 5.76. Paused.

Bottom 10, 12 months: two Bracelets flexible ads with 0 and 1 orders (₹31,755 and ₹64,670), the Founder Video "Thinking of Buying Jewellery Online?" (₹32,030, 0 orders), one Trust overload placement with 0 orders at ₹35,265, one chains dynamic image at 0 orders (₹37,153), a broad catalogue ad at 0.40, the Founder "From Our Hands to Yours" at 0.49 (₹44,245), the Tennis Bracelet launch at 0.56 (₹33,163), and the Bracelets carousel "Discover our bestselling designs" at 0.74 (₹55,834).

Top 10, 90 days: the same earrings videos (Trust overload 12.60, Gifting 9.14 and 6.05, Social proof 5.05), the three EOSS ads (9.40, 7.09, 5.76), one broad catalogue ad at 5.54, the Educational earrings flexible ad at 5.43 (₹1,08,892, 16 orders) and the MOF catalogue ad at 5.11.

Bottom 10, 90 days: broad prospecting catalogue ads at 0.49, 0.97, 1.34, 1.35 and 1.50 (together about ₹3,70,000 of spend), the Tennis Bracelet launch at 0.56, an Educational earrings flexible ad at 1.00 (₹68,096), Bracelets May flexible at 1.47 (₹1,55,306), Founder Gemstone Video at 1.59, and the EOSS earrings carousel at 1.80.

What the lists say together. The same creative can sit in both lists (Trust overload, Educational, the catalogue). Placement, audience and timing move an ad by 10× more than the copy. Sale copy wins for 2 weeks a year. Outside sales, the winners share one shape: a plain first line that names the buyer's worry or gift moment, a product-specific promise (earrings, gemstones, 18K), then a proof stack. The losers share another: brand-first lines ("From Our Hands to Yours", "Redesigning Beauty"), collection launches with no reason to buy now, and bracelets and rings shown without an argument.

## 5. What the site promises

Pages read on 24 Sep 2026: home, shipping and returns, FAQ, the rings, chains, bracelets, earrings and best-seller collections, and 4 product pages. Saved in `raw/site_snapshot.json`.

Home page trust bar: "30,000+ orders delivered", "20+ years of delivering jewellery", "BIS hallmarked gold", "4.8 Google rating". "Why choose Gehna" tiles: BIS Hallmarked, Easy Returns ("hassle-free 7-day return and exchange policy"), 10,000+ Happy Customers, 20+ Years. Reviews on the home page mention COD and EMI, a free ring sizer sent before the order, fast delivery, custom pieces, and buying online "exactly as advertised".

Shipping and returns page: free shipping and gift packing in India; Blue Dart or UPS; tamper-proof box; transit insurance; 7-day return for full refund or exchange within India; a limited lifetime exchange policy (gemstone pieces exchanged at 70% of prevailing value, diamond pieces at 80%, with the original invoice); no returns on international orders.

FAQ: all gemstones natural; all jewellery BIS Hallmarked; most pieces hand-made at the Chennai workshop; one-year workmanship warranty; 7-day satisfaction return (customer pays return shipping, refund in 4 to 5 working days); one free ring resize within 15 days; in-stock pieces ship in 2 to 3 days, made-to-order in 10 to 14 days; COD, cards, net banking and an interest-free style monthly instalment plan with no documents; prices move with the gold rate and are not matched later; diamond pieces use EF-VVS grades.

Collection pages: rings 156 designs, ₹13,500 to ₹3,67,010; gemstone gold chains 148, ₹10,120 to ₹3,94,220; bracelets 105, ₹9,550 to ₹3,63,450; earrings 627, ₹13,490 to ₹10,27,020; best sellers 46, ₹7,150 to ₹1,69,930. Almost all pieces are 18K yellow gold; 14K is a filter on chains (14 designs) and an option on some earrings; 22K exists in small numbers. Collection meta text promises "lifetime exchange", "free returns" and "free delivery".

Product pages (live prices on 24 Sep, confirm before use): Celestial Navaratna 18K Gold Bracelet ₹22,210, in stock, 0.71 g gold, badge "#1 most-added bracelet this season"; Verdant Whisper Emerald 18K Gold Ring ₹24,850, made to order by size, Zambian emeralds, free ring sizer and free resize in its FAQ; Ivory Natural Pearl 18K Gold Hook Earrings ₹16,690, 14K option, badge "#1 most-added earring this season"; Celestial Navaratna 18K Gold Chain ₹49,840, 1-inch adjustable loop. Every product page shows an EMI table (20% down, 2 to 6 months), a delivery date 3 to 4 days out, "lifetime repair service across India", "Thousands of customers shop with us online every month", and a 7-day no-questions return.

## 6. Claims the copy uses, and whether they are allowed

Approved list from `brand.json`: BIS Hallmarked, 18K gold (14K on some chains), natural gemstones, handcrafted, 4.8/5 on Google, 10,000+ customers, free shipping, 7-day easy returns, 20+ years of craft. Source table: `raw/claims_scan.csv` (share of 12-month spend in ads that use the claim).

| Claim in copy | Spend share | Approved? | On the site? |
|---|---|---|---|
| BIS Hallmarked | 25.8% | Yes | Yes, home and FAQ |
| 18K gold | 27.0% | Yes | Yes |
| 14K gold | 4.5% | Yes for some chains | Yes, chains and some earrings |
| Natural gemstones | 23.7% | Yes | Yes, FAQ |
| Handcrafted / 100% handmade | 32.5% | "Handcrafted" yes | FAQ says most pieces are hand-made, some outsourced. "100% handcrafted" overstates it. |
| 4.8 on Google | 9.6% | Yes | Yes |
| 10,000+ customers | 2.1% | Yes | Yes |
| 5,000+ happy customers | 11.2% | No, old number | Not on site. Used by the best retargeting text. |
| 8,500 people, 25,000+ orders, 15 years | small | No | Not on site. Three different numbers in the same account. |
| Free shipping | 10.5% | Yes | Yes, India only |
| 7-day returns | 12.6% | Yes | Yes |
| 20+ years | 0.5% | Yes | Yes |
| Lifetime exchange | 31.2% | Not on the list | Yes, as a limited policy at 70% to 80% of value. Needs a softer wording. |
| EMI / Cash on Delivery | 27.3% | Not on the list | Yes, FAQ and product pages |
| Buyback available | in the main catalogue text | Not on the list | Not found on the pages read |
| Certified gemstones, IGI certified | 11.8% | Not on the list | Product FAQ: navratna stones certified by a third-party lab. IGI not found. |
| Lightweight | 16.6% | Not on the list | Product FAQ: "lightweight yet durable" |
| Discount or % off | 28.8% | Only while running | 0% special price on all pages read |
| Diamonds / natural diamonds | 4.5% | Only if the product has them | Diamond filter exists |
| Lab-grown diamonds | 0.5% | Only if the product has them | No lab-grown filter found |
| India's largest gemstone collection | ₹2,10,732 | No | Not on site. Unprovable. |
| Astrologically powerful | ₹2,67,684 | No | Not on site |

The safe, proven set for new copy: BIS Hallmarked, 18K gold, natural gemstones, handcrafted, 4.8 on Google, 10,000+ customers, free shipping, 7-day returns, 20+ years. Site-backed extras that the owner can approve: COD and instalments, free ring sizer and one free resize, 1-year warranty, transit insurance, lifetime exchange (worded as "exchange any time" with the conditions on the page), Chennai workshop and store, delivery in 2 to 3 days for in-stock pieces.

## 7. What is missing or weak

Audience. Every prospecting campaign stacks cold and warm audiences and shows them the same words. Men take 28% of spend at ROAS 1.53 with no gifting copy written for them. 18 to 24 takes 12.6% of spend at 1.17. Past customers get nothing: no customer list ad set, no repeat or second-piece copy, even though the site's own reviews are full of "I have bought so many pieces" and the average order is ₹30,000 to ₹35,000.

Objective and funnel stage. Retargeting is 9 to 15% of spend and returns 4.5 to 6.5. It runs one catalogue text that has not changed in 18 months and still says 5,000+ customers. There is no cart-abandon copy that answers the reason people leave (price, size, trust in online gold, delivery time), all of which the FAQ answers well.

Offer. Sale copy returns 5 to 9 but runs 2 weeks a year. Outside sales the account has no standing offer language at all, although the site has real, always-on reasons to buy that cost nothing: free shipping, COD, instalments, free sizer, 7-day return, insured delivery. These sit in the FAQ, not the ads.

Proof. The proof numbers are inconsistent: 5,000+, 8,500, 10K+, 25,000+ orders, 30,000+ orders, 15 years, 20+ years. One set should be used everywhere. Customer quotes are used in only one text, and it is the weakest of the big five.

Product. Rings and chains have the most designs on the site (156 and 148) and the least sales in the ads. Ring copy is brand-voice but abstract; it never says the buyer can get a free sizer, a free resize, or that most rings are under ₹25,000 [confirm before launch]. Bracelets lost their angle after winter. Pendants and nose pins are not in the last 90 days at all. Nothing in the account talks about the emerald, ruby, pearl or navratna gemstone edits that the home page leads with.

Copy craft. Descriptions are empty on every ad. Headlines repeat "Gehna" or "Redesigning beauty" on ₹48 lakh of spend. Flexible ads hide their copy from any audit, so a third of spend cannot be learned from. Inflated words ("unmatched", "opulent", "transcendent", "cosmic") appear in the weakest texts.

Measurement. Purchase cells are unavailable on 8,238 of 9,345 daily rows, so per-ad ROAS at low spend is noisy; the ₹30,000 floor is the minimum for any judgement. There is no view of new versus returning buyers in the ad data, so the "past customers" objective will need a customer list and a separate campaign to be measured at all.
