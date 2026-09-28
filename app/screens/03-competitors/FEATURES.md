# Competitors and market: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, simulated and public signal badge, lookalike page warning, decision row | done |
| 0.2 | `api.py` (overview, audit) reading the brain through `store.py`, raw Ad Library records as fallback, and simulated `products_monthly` for brand prices; unavailable states | done |
| 0.3 | 3 tiles (competitors tracked, price position index, competitor active ads), 2 insights as rules (same offer type run longer; price outside the 85 to 115 band), 1 chart (active ads per brand) | done |
| 0.4 | Competitor cards: positioning, price band, what they push, active ads, longest run as a signal, gap to own | done |
| 0.5 | Positioning map to scale: median price per pair (with public band) against a durability or comfort claim score (0 to 3, scored in code from hooks and positioning), open quadrants shaded | done |
| 0.6 | Price ladder table: each brand sock pack per pair against each competitor's median and band | done |
| 0.7 | What they run board: formats and hook types only, no ad text | done |
| 0.8 | `audit.py`: COMP-R01 unclaimed angle, COMP-R02 price gap, COMP-R03 same offer type run longer, COMP-R04 lookalike page; tests in `tests/test_screen_competitors.py` | done |

Round 0 notes (28 Sep 2026): brand price per pair is simulated net sales per unit (after discounts) for the last full month, so it reads lower than list. Competitor bands are one public capture, so price and angle findings are medium with confidence 0.5 or lower; the "2 consecutive captures" part of the price drift rule waits for a second capture. Claim scores are keyword rules, not judgement. Screenshot: `round0.png`.

## Round 1: the execution surface (depth contract)

| # | Feature | Status |
|---|---|---|
| 1.1 | Round 0 anti-patterns out: plan board first with ranked actions from `rank` (`actions.py`: real titles, steps, artefacts and drafts for COMP-R01 to R04), orientation beside it, what is wrong with evidence rows, action cards, desk, audit and rule list at the bottom; tiles, insight cards, the active-ads chart and the lookalike banner removed | done |
| 1.2 | Competitor pills (all, direct, basics and apparel, threats) and the side-by-side table: the 12 pages in the brain's competitive frame plus ours, active ads, format mix, median days live, offer share, offers seen; threat, watch or ignore from 5 counted points with the reason in numbers; row opens a panel with us against them, angle tags with the word that set each, a battlecard draft (BRAND-C57) and a weekly watch (BRN-C11). `pages.py` reads an ad-level snapshot first when one exists | done |
| 1.3 | Creative coverage matrix (`coverage.py`): 10 angles by 5 formats, our share of ads against theirs in every cell, all pages or direct only; gap when they put 3 percent or more and we put none; "Brief it" opens the cell's ad brief (format spec, our proof from the brain, signal pages) and logs a CREA-C06 decision; "Next to try" line; new rule COMP-R05 puts the top 3 gaps with proof on the plan. Estimated from page-level mixes until an ad-level snapshot exists, labelled | done |
| 1.4 | Hook and offer mix (`mix.py`): heatmap of first line kinds per page against ours, offer types seen per page, the offers held in our brain; answers per gap with owner and draft: a hook bank brief (CREA-C04), an offer test for an offer we hold and never say (LIFE-C47), a no-code ad test when most of our ads push a code and direct peers run none (LIFE-C38). New rules COMP-R06, R07, R08 on the plan | done |
| 1.5 | Longest running ads as signals (`references.py`): one per page with days live, start, share of ads live 30 days or more, study, watch or too new; relevance from 4 rules (our top angle, keeps half its ads 30 days, 3x our median, direct) with the reason shown; "Use as reference" opens a brief that says what to borrow (layout, pacing, mood), maps it to our angle and proof, and what never to copy; rights reference only; logs SCT-C04. Our own long runners on top with SCT-C02 | done |
| 1.6 | Price and pack ladder (`ladder.py`): band chart of each tracked price band per pair against our ladder by style (dots grow with pack size), the direct peers' median range shaded; ladder table with saving a pair from single to biggest pack, proof on file, position against the direct median; Amazon listing prices per pair as a public cross-check; rules COMP-R09 shallow ladder while a peer sells bundles (offer spec, LIFE-C39) and COMP-R10 priced above the peers with no proof (page section, CREA-C31). Pack labels fixed (style from the SKU) | done |
| 1.7 | Positioning map on `Charts.positioningMap`: price per pair against durability or comfort claim, us and every placed brand sized by active ads, pages with no price band listed as not placed; each corner ends in a move computed in code (hold, contest with the claim points we miss, claim, skip) with a BRAND-C20 decision row; rule COMP-R11 puts an open strong-claim corner on the plan as a 2-frame positioning test (does not fire on this capture, tested on an edited brain) | done |
| 1.8 | Launches and changes (`changes.py`): a 28-day timeline, newest first, from snapshot diffs when two ad-level snapshots exist (new ads, formats, offer types, angles) and from the brain now (full account refreshes, the lookalike page, our own launches); each change is follow, watch or ignore with the action and a BRN-C11 decision row; rule COMP-R12 puts a direct competitor's full refresh on the plan as a research note | done |
| 1.9 | Snapshot freshness and the re-pull: per page the page id, last capture, age and source (fresh, ageing, stale, no capture; never 0); "Re-pull: show the estimate first" reveals the plan from `snapshot.plan` (12 pages by page id, 1,800 ads cap, $2.08 estimate, $4 run and $30 week caps, week spend from the ledger, Allbirds skipped for no page id, whether the key is set), the run command and a person-owned BRN-C11 decision; the screen never spends. Rules COMP-R13 page with no id (person pastes it) and COMP-R14 stale capture (person approves the spend) | done |
| 1.10 | `rank` for all 14 rules (COMP-R01 to R14): each has a builder with a real title, owner, 2 to 5 steps with who, the artefact kind (ad_brief, copy, test_brief, offer, page_section, research_note, ticket, brain_record, connector_setup) and a draft from the brain where it can; findings grouped on the page by bottleneck (ads, offers, price, map corners, watch); orientation on the 12 pages (pages tracked, threats, our ads, theirs, price index); R01 now checks all 11 pages with data; the round 0 "what they run" board removed; phone width fixed; tests: every rule has a builder and a group, every open finding ranks and validates on edited brains and a late window, "Not now" snoozes 14 days | done |

Round 1 notes: `snapshot.py` plans and runs a page-id Ad Library pull through `app/connectors/apify.py` (12 pages with ids, 1,800 items cap, estimate $2.08, inside the $4 run and $30 week caps). The live run was blocked by the session's permission check on 28 Sep, so round 1 builds on the brain's 28 Sep pulls (page-level formats, hook types, offers, run lengths and 3 quoted ads a page) and the page says so.

## Round 5: hand-offs, execution lanes and the season

| # | Feature | Status |
|---|---|---|
| 5.1 | Hand-offs by the events contract (`handoff.py`): the `competitor_snapshot` table this screen owes customers and avatars, creative, and offers and pricing (one row per page: verdict, points, active ads, format mix, angles, offers, price band per unit, map quadrants, longest ad, capture date, source), written with each capture to `fixtures/competitor_snapshot_<brand>.json` and served at `GET competitor_snapshot`; experiment registry rows drafted in the contract shape (status proposed) from every open test action at `GET experiments`; a desk block shows both | done |
| 5.2 | Action lanes: the action cards filter by owner (agent does it, agent drafts and you approve, a person does it) with counts, hours of work per lane and how many are decided or waiting on the founder; each card shows the founder's logged decision from the decisions table | done |
| 5.3 | The holiday season against them (`season.py`): US dates computed in code (Black Friday 27 Nov, Cyber Monday 30 Nov, last gift order 17 Dec), the season's weight from the brain (26 percent of the year), 5 dated phases (watch, build, defend, gift window, read) with who and the moves; rule COMP-R30 (high inside 60 days) puts 3 gifting ad briefs on the plan because Darn Tough and Smartwool run a gifting angle and we run none | done |
| 5.4 | What the founder decides this quarter: a positioning review built in code (where we sit on both map axes, the threats, how shoppers frame the category and whether our line says it, pack ladder and price index) ending in 3 decisions: test the buy it for life line or keep ours, contest the durability corner or hold, hold the price index or move it; copy and a BRAND-C19 decision | done |
| 5.5 | Exports (depth section 7): CSV of 7 desk tables (pages, coverage matrix, first lines and offers, references, pack ladder, search seeds, room metrics), unavailable cells empty, never 0. Also fixes a fault 5.4 shipped: its new review function reused the name of the review-themes function, the page stopped loading at the desk; renamed, and a test now fails on any duplicate function name in screen.js | done |
| 5.6 | A browser smoke test in the screen's test file: it starts the server on a free port, loads the page and the report view in Chromium, and fails on any script error, fewer than 4 desk tabs, fewer than 5 plan items or an empty report; skipped where Playwright or Chromium is absent; checked that it fails on a broken script | done |

## Round 4: the rest of the room, and a depth pass on the screen

| # | Feature | Status |
|---|---|---|
| 4.1 | Where they run their ads: Meta placements per page (Facebook, Instagram, Threads, WhatsApp, Messenger, Audience Network) as a heatmap against ours, a gap line (a placement most direct pages run and we do not), ours unavailable until the pull fills them; captures now keep placements and threat points, and a rival on a new placement is a change (the room's "entered a new channel" rule) | done |
| 4.2 | Depth pass, gap lines: every one of the 20 desk blocks now ends in one line computed in code, either "Gap:" with the finding sentence, the move, its owner and a button to the action (or its connect step), or "Holding:" with what holds; unavailable gaps name the source to connect; the action column header no longer shows raw code (per-row labels ride on the rows); test that every desk section has a line and every linked action exists | done |
| 4.3 | Depth pass, sized with a stop rule (depth rule 5): every action that changes money or traffic (ad brief, offer, test, page section, copy, listing fix, ticket) carries a size, a stop rule and a dated check; the 4 that lacked a stop rule (durability answer, compare blocks, lookalike report, Amazon check) and 2 dormant builders (counter brief, stale card) now have one; tests on the live actions and on the dormant builders | done |
| 4.4 | Depth pass, brand content from the brain: the price unit ("pair") is read from the competitors' public price bands in the brain, never typed; every page label, chart axis, orientation title, simulated note and audit sentence uses it; test that screen.js holds no unit word and that a second brand's unit comes from its own bands. The internal field names keep per_pair | done |
| 4.5 | Depth pass, unavailable never zero: a scan of every number on a brand with almost no data found 5 zeros that meant "not read"; now None and "unavailable" on the page: our ads with an angle when our active ads are unknown, the coverage note's ad totals, our Amazon listing counts, our discount depth and the "no discount seen" signal when no offer or ad was read (premium scores count known signals only); the heatmap shows n/a for unknown signals; tests on the second brand | done |
| 4.6 | Phone width at 360 px: the top and each of the 4 desk tabs checked with every panel open, no page scroll and nothing wider than the screen outside the table, matrix and chart scrollers; found and fixed a live-server fault on the way: the server reloads api.py but not the modules it loads, so the page served a stale mix after edits; api.py now drops this folder's cached modules on reload | done |
| 4.7 | Who is getting more dangerous: threat points per page across the dated captures as a trend strip, highest first, with ads now; a gap line names any page whose points rose since the first capture (refresh its battlecard, read its new ads); one capture on file now, so it says the trend starts with the next | done |
| 4.8 | What support can paste today: answers to "how do you compare to X" for each name we lose to and to the top 3 review doubts, built only from verified brain proof plus the guarantee, each with its source record; a doubt or name with no proof gets no answer and lands on "proof to add" (Stance, look better); copy one or all; BRAND-C57 decision | done |
| 4.9 | The room's 15 specified metrics in the audit, each with value, formula and, when it cannot be computed, the reason (price change count needs 2 captures, new creative count needs 2 ad-level snapshots, win rate needs interviews, niche size and positioning test score need their sources); none reads 0 for unknown | done |
| 4.10 | Round close: 29 rules, 23 desk blocks each ending in a gap line, every money action sized with a stop rule, brand facts and the price unit only from the brain, unavailable never zero, 360 px clean on every tab; all screen tests green apart from the 4 known site speed ones; screenshot `round4.png` | done |

### Round 4 status for Kevin (28 Sep 2026)

1. Every block on the desk now ends in one line: the gap, the move, who owns it and a button to it, or what holds. A founder can read the desk top to bottom and act at each stop.
2. New: support answers you can paste (from verified proof only), each rival's threat trend, where rivals run their ads with an alert when one enters a new placement, and the room's 15 metrics with their formulas.
3. Every action that spends money or traffic now has a size, a stop rule and a check date. The 6 that lacked a stop rule have one.
4. Nothing reads 0 when it was never read (5 fixes), the price unit comes from the brain, and the page is clean at phone width on every tab.
5. Fixed on the way: the live server served a stale mix of code after an edit; it now reloads the whole screen. Still missing: the ad-level pull, rival site captures, search and trend data; each is a connect step.
6. Next, round 5: exact counts once the pull lands, the first rival page captures, a quarterly positioning review, and an Amazon listing comparison against rivals once their listings are pulled.

## Round 3: watching over time, reports and the rest of the room

| # | Feature | Status |
|---|---|---|
| 3.1 | Dated page-summary captures (`capture.py`, brain only, no spend) and their diff: active ads up or down 25 percent, a new format, a new or dropped offer, a new angle, a new flight; the alerts flow into the changes timeline (follow, watch, ignore) and rule COMP-R24 puts a direct competitor's new offer or angle on the plan as a counter brief; first capture on file for 28 Sep, so alerts light with the next brain refresh | done |
| 3.2 | Price moves from the dated captures (each capture holds every page's price band): median price per pair up or down 15 percent between the latest two, shown above the price ladder; rule COMP-R25 (high for a direct page) puts a sharp cut on the plan with a value answer and a watch rule, never a reflex match (CREA-C31) | done |
| 3.3 | Landing page tracking for the top 3 threats (`landing.py`): by threat points, the urls to visit weekly from public links in the brain (site, products feed, Ad Library page) plus ad landing domains once a snapshot exists, what to diff (headline, offer banner, guarantee, best seller price per pair, new collections), last capture "not tracked yet"; rule COMP-R26 puts "start tracking" on the plan as an agent task (BRN-C01, public read) | done |
| 3.4 | The printable weekly report (`?view=report` on the same page, since the server serves only index.html, screen.js and screen.css from a screen folder): the top 10 moves with who and check dates, what changed, who is a threat, the numbers to watch against their bars, caveats; Print button and print styles; linked from the head | done |
| 3.5 | Battlecards for support: one per direct competitor from verified brain fields, the date the facts were checked, fresh or stale at 90 days, copy one or all; rule COMP-R27 puts a stale card on the plan for the agent to re-verify (BRAND-C57) | done |
| 3.6 | Does our line match how shoppers frame the category (`frames.py`, BRAND-C20): the Reddit category frames with mentions, whether we are named and whether our line says them; 3 lines to test by rule (current, the top frame with its proof, the contested map corner); test score unavailable until a test is on file; rule COMP-R28 puts a 5-second poll plus ad-line test on the plan when the top frame (buy it for life, 9 mentions) is not in our line | done |
| 3.7 | Win-loss interview kit (BRAND-C58, human assist): screener, 6-question guide, reason-code sheet and readout for 5 interviews against each name we lose to, shown and copyable under the losses table; rule COMP-R29 puts the interviews on the plan as a person task while none are on file | done |
| 3.8 | Thresholds the brand tunes: 12 rule thresholds (price band, stale days, angle share, threat and watch points, coverage gap, ad surge, price move, discount depth gap, pack saving, Amazon undercut) read from a `plans` record `competitor_thresholds`, reset to defaults each run, shown in the audit as "thresholds in force" with value, default and source | done |
| 3.9 | Plug and play on a second brand: a minimal hat brand (one competitor record, one product line) renders every route (overview, plan, digest, audit, rank) with honest unavailable states and no Bombas fact; the category word now comes from the brain (pull config, else the first product line), so ladder labels, search seeds, the interview screener, frame lines and price sentences say "hats" for a hat brand; test added. Known limit: the price model still reads bands "per pair" | done |
| 3.10 | Round close: 29 rules ranked through `rank` (27 actions on this capture), every rule with a builder and a desk group, full page and report checked at 1280 and 360 wide with no page scroll, all screen tests green apart from the 4 known site speed ones; screenshot `round3.png` | done |

### Round 3 status for Kevin (28 Sep 2026)

1. The screen now watches rivals over time. Dated captures of every page turn a new offer, a new angle, an ad surge or a price cut into an alert with a move. The first capture is on file, so alerts start with the next brain refresh.
2. New things to ship: battlecards for support with a freshness date, a win-loss interview kit, a positioning test (shoppers frame socks as "buy it for life"; our line never says it), and weekly tracking of the top 3 threats' pages.
3. A printable weekly report (the head's "Printable weekly report" link) carries the top 10 moves, what changed, the threats and the numbers to watch.
4. Plug and play is proven: a made-up hat brand renders every route with no Bombas facts, and the category word follows the brand. Twelve rule thresholds can be tuned from one brain record.
5. Honest gaps: still no ad-level pull (Kevin can run it), no site captures of rival pages yet, no search or trends data. Each shows as unavailable with a connect step. The price model still reads bands "per pair".
6. Next, round 4: counted matrix cells and ad alerts once the pull lands, first landing page captures, a threat score history chart, answers the support team can paste, and a quarterly positioning review.

## Round 2: who we lose to, the market around us, and counted signals

| # | Feature | Status |
|---|---|---|
| 2.1 | Who shoppers pick instead of us (`losses.py`): the named alternatives recommended instead of us on Reddit (times, upvotes), the reason a rule reads from their ad angles (last longer, cost less, look better), our one-star count on that theme and the doubts with no proof; "Answer" opens a compare block, FAQ and support macro from verified brain facts (BRAND-C57) and a win-loss interview decision (BRAND-C58); win rate reads unavailable until interviews exist; rule COMP-R15 on the plan | done |

| 2.2 | The category ladder (`category.py`): 5 rungs by rule (premium above the median, direct at or below, basics and apparel, cheap multipacks from Reddit, doing nothing), members and a signal per rung (active ads, upvotes, Reddit frame mentions), our rung marked, a move per rung with its capability and decision row; demand trend by rung reads unavailable and rule COMP-R16 (a lower rung gaining) becomes a connect action for a search trends source | done |

| 2.3 | Review themes against their claims (`reviews.py`): our one-star and five-star counts per theme from the objection ladders, praise share, top doubt, and the pages that lead their ads with the same theme; attacked, contested or quiet; competitor review counts unavailable (no pull yet); rule COMP-R17 (high) when a top 2 one-star theme is led with by 2 or more direct pages: durability now, against Darn Tough, Smartwool and Feetures; the answer is a guarantee block, 2 ad lines and a product ticket (LIFE-C42) | done |

| 2.4 | Are we cheaper on Amazon than on our site (`market_presence.py`): our Amazon listings (count, priced by pair, median stars, reviews), per style the Amazon median price per pair against our site's net price per pair, sellers unknown; competitor marketplace listings unavailable; rule COMP-R18 when a style is 15 percent or more cheaper on Amazon with 2 or more listings: ankle, 40 percent; the answer is a seller and price check (PROD-C46, agent) | done |

| 2.5 | Creative velocity and share of voice (`velocity.py`, the Motion and Foreplay job rebuilt as a rule): estimated new ads a week per page (active ads / median days live x 7) as a bar against the direct median, our counted rate this month beside our estimate, share of voice among direct pages by ads live (a signal of testing, never spend); rule COMP-R19 when our rate is under half the direct median: a weekly volume plan that doubles today's pace, fed by the coverage gaps (CREA-C06) | done |

| 2.6 | The weekly competitor brief (the Foreplay alert job, rebuilt): `GET digest` writes the brief in code from the plan (what changed that crosses a rule, the top 5 moves with owners, threats, our pace against the direct pace, the price index); on the page with copy and a BRN-C11 decision to send it weekly; web pass recorded below | done |
| 2.7 | Which niches are big enough (`niche.py`, BRAND-C23): the bar in buyers from our own economics (1 percent of 12-month revenue / AOV x orders a buyer; now 46,504 buyers a year, about $1.26M contribution), unavailable when an input is missing; candidate niches from the coverage matrix (angles with 5 percent or more of their ads where our share is under a third); search demand unavailable; rule COMP-R20 puts a sizing note for the top candidate on the plan | done |
| 2.8 | Do we discount like a premium brand (`premium.py`): a scorecard heatmap of 6 premium signals per page (guarantee, lifetime, origin, mission, tested or rated, no discount seen) with a score, and the discount depth each page shows (0 when ads were read and no percent seen); rule COMP-R21 when our score is at or above the direct median while our code runs 10 points deeper (now 20 against 0): an offer policy that caps the code at 10 percent and swaps depth for a gift or pack step (LIFE-C38) | done |
| 2.9 | Which search terms do they go after (`search.py`): seed terms by rule from each page's public lines (the word before "socks", plus material and angle words), contested on 2 or more pages, gaps only they use, and ours too; terms only we say; rankings, bids and volume unavailable; rules COMP-R22 (a keyword check brief for the Google Ads and SEO screens, agent) and COMP-R23 (connect a search data source, person) | done |
| 2.10 | The desk as 4 job tabs (Rivals, Ads, Price and offer, Market and data) so the plan, what is wrong and the actions stay above a compact desk; 23 rules now rank through `rank` (24 actions on this capture); test that every desk section sits in a tab; screenshot `round2.png` | done |

Web pass (28 Sep 2026; Foreplay, Motion, Atria, Pathmatics, Similarweb, Semrush and SpyFu, Meta Ad Library). Rebuilt on our data: long runners as signals (1.5), format share and offer share (1.2, 1.4), hook and angle gaps (1.3, 1.4), share of voice by ad count labelled not spend (2.5), price band gaps (1.6), word of mouth by name (2.1), review themes against rival claims (2.3), weekly alerts as a brief (2.6). Not rebuildable yet, data named: launch velocity counted and new-ad alerts (weekly snapshots or a start date per ad), spend and impressions share (modelled spend data), traffic by channel (Similarweb-type visits), keyword overlap (a keyword API), price moves (dated price captures). Sources: foreplay.co/spyder, motionapp.com, tryatria.com, sensortower.com/product/digital-advertising/pathmatics, support.similarweb.com, spyfu.com/blog/semrush-vs-spyfu, transparency.meta.com/researchtools/ad-library-tools.

Round 2 notes: the lead authorised the $2.08 pull on 28 Sep; the session's permission check had already refused that paid run and said not to retry it, so it was not re-run. Still listed under Contract asks.

### Round 2 status for Kevin (28 Sep 2026)

1. The plan now ranks 24 moves from 23 rules. First up: answer the durability attack. Durability draws 64 of our one-star reviews, and Darn Tough, Smartwool and Feetures lead their ads with it.
2. New jobs a founder can act on: who shoppers pick instead of us, by name, with a drafted answer; the category ladder from doing nothing up, with a move per rung; review themes against their claims.
3. Also new: ankle socks sell 40 percent cheaper on Amazon than on our site (seller check); a code cap, since we discount 20 percent while direct peers show none; a creative volume plan; a sizing bar of 46,504 buyers; keyword seeds for the ads and SEO screens.
4. Every Monday brief is built in code from the plan: what changed, the top 5 moves, threats and pace. The desk sits in 4 job tabs under the plan.
5. Honest gaps: the ad-level pull still did not run (the lead authorised it; this session's permission check had refused it). Search volume, trends, competitor reviews and marketplace listings read unavailable, each as a connect action.
6. Next, round 3: counted cells once a snapshot lands, snapshot diffs for launch alerts, landing page tracking for the top 3 threats, dated price captures for price moves, and a printable weekly report.

### Round 1 status for Kevin (28 Sep 2026)

1. A founder can now open Competitors and see 13 ranked moves first: ads to make, offers to test, a pack ladder to fix, a lookalike page to report, each with owner, steps and a drafted brief.
2. Behind the plan: the 12 tracked pages side by side with threat, watch or ignore; a coverage matrix of angles by format with "Brief it" on every gap; the hook and offer mix with an answer per gap.
3. Also new: longest running ads as references (borrow layout and mood, never copy), the price and pack ladder against the bands, the positioning map with a move per corner, a 28-day changes timeline, and freshness with the re-pull estimate shown first.
4. What changed: 14 audit rules (was 4), all ranked through our own `rank`; tiles, insight cards, the ads chart, the lookalike banner and the formats board are gone.
5. Honest gaps: the live Ad Library pull ($2.08, inside the caps) was blocked by this session's permission check, so the matrix and mixes are estimates from the brain's page summaries and say so; offer share, main CTA and new-in-14-days wait for an ad-level snapshot.
6. Next, round 2: run the snapshot (Kevin's approval) to make every cell counted, then the room's SERP overlap, marketplace presence, review comparison and pricing moves, and a web pass on what Foreplay, Motion, Atria and Similarweb do, rebuilt as rules.

## Contract asks

- `competitor_snapshot` has no shared table in the data layer yet; it is written to `fixtures/competitor_snapshot_<brand>.json` in this folder and served read-only. A home under `app/data/brands/<brand>/` would let readers find it without knowing this folder.

- `server.py` serves only index.html, screen.js and screen.css (plus fixtures) from a screen folder; a report page or split JS files need an allow-list entry. Local fallback: the report is `?view=report` on the same page.

- A snapshot run needs a permission for `snapshot.py --live` (Apify, page ids only, inside the Bombas caps) in the session settings; local fallback: the screen reads the brain's page summaries and labels every estimate.

## Room jobs (JTBD)

| Job | Question | Capability | Round 0 |
|---|---|---|---|
| map every real alternative a shopper compares against, including doing nothing | who or what are we really competing with | BRAND-C18 | competitor set only; no ladder yet |
| see which corners of the market are open | where is there room nobody has taken | BRAND-C19 | positioning map, open quadrants |
| write and test the positioning statement against real shopper frames | does this positioning actually win against the alternative | BRAND-C20 | todo |
| find an unclaimed angle when no slot is open head on | is there a dimension nobody has claimed, or a reframe of the whole category | BRAND-C21 | COMP-R01, gap to own on cards |
| check whether price sits inside or outside the category's learned range | are we priced right, and is discounting undercutting us | BRAND-C24 | price tile, insight, ladder table, COMP-R02 |
| size the market and a candidate niche from the brand's own numbers | is this idea big enough to matter at our numbers | BRAND-C23 | todo |
| watch the tracked competitors for changes and alert only when it matters | what did they change this week that we should know about | BRN-C11 | todo (needs a second capture) |
| turn a verified difference into something support can actually say | what do we say when a customer asks how we compare | BRAND-C57 | todo |
| learn why an almost-buyer chose a named competitor instead | why do we lose the ones we lose, by name | BRAND-C58 | todo |
| read competitor ads, pages, reviews and Q&A as public signal | what is the market doing that we are not seeing | BRAND-C07 | what they run board, lookalike warning |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- who or what are we really competing with  (BRAND-C18)
- where is there room nobody has taken  (BRAND-C19)
- does this positioning actually win against the alternative  (BRAND-C20)
- is there a dimension nobody has claimed, or a reframe of the whole category  (BRAND-C21)
- are we priced right, and is discounting undercutting us  (BRAND-C24)
- is this idea big enough to matter at our numbers  (BRAND-C23)
- what did they change this week that we should know about  (BRN-C11)
- what do we say when a customer asks how we compare  (BRAND-C57)
- why do we lose the ones we lose, by name  (BRAND-C58)
- what is the market doing that we are not seeing  (BRAND-C07)

### Metrics specified

- `competitors_tracked`: How many named competitor brands are on watch. count of active entries in the competitor set
- `price_position_index`: Where the brand's price sits versus the tracked competitors on a matched product. brand price / median competitor price for the matched product, times 100
- `price_change_count`: How many price moves the tracked competitors made. count of price changes across all competitors
- `new_creative_count`: New competitor ads detected. count of ad creatives first seen this period, per competitor
- `new_launch_count`: New products, collections or channels a competitor entered. count of new SKUs, collections or marketplace listings detected
- `positioning_openness_score`: How much of the positioning map is unclaimed. open quadrants / total quadrants on the map
- `category_ladder_coverage`: How many real alternatives, including doing nothing, are mapped. count of distinct rungs logged on the ladder
- `market_size_estimate`: How many repeat buyers at this brand's own AOV and margin would sustain the business. target profit / (AOV times margin times repeat orders per buyer per year)
- `addressable_niche_size`: Estimated demand for a candidate niche. search or category demand signal for the niche, scaled by the brand's realistic capture rate
- `win_rate_vs_named_competitor`: Share of studied almost-buyers who chose the brand over one named competitor. wins / (wins plus losses) in the win-loss sample
- `battlecard_freshness_days`: Days since a battlecard claim was last verified. today minus last verification date, per claim
- `competitor_activity_share`: Share of tracked competitor ad activity by count, as a public signal only. this competitor's new creatives / total new creatives across all tracked competitors
- `premium_signal_score`: How many premium signals the brand shows versus the category norm. count of premium signals present (packaging, guarantee, service, price anchor) / count expected for the category
- `discount_depth_vs_category`: How deep the brand discounts versus tracked competitors. brand's average discount percent minus competitor median discount percent
- `positioning_test_score`: Which of 2 positioning frames won when tested against each other. share preferring frame A minus share preferring frame B, in the test sample

### Insights specified (rules in code)

- competitor cut price sharply: a tracked competitor's price on a matched product drops more than 15 percent versus its own trailing 30-day average → "{competitor} cut the price on {product} by {pct} percent." (action BRN-C11)
- competitor tried a new angle: a tracked competitor's new creative uses a hook or product tag not seen from them in the trailing 90 days → "{competitor} is now running a new angle: {angle}." (action BRN-C11)
- competitor entered a new channel: a tracked competitor's product is newly listed on a marketplace or channel it was not on last capture → "{competitor} is now selling on {channel}." (action BRN-C11)
- open quadrant with real demand: a positioning map quadrant has zero competitors plotted and a non-zero demand signal → "No tracked brand is claiming '{quadrant}', and there is real search demand for it." (action BRAND-C19)
- price has drifted outside the category range: price_position_index falls outside the learned range (a set band around the category median) for 2 consecutive captures → "The brand's price is now {pct} percent {above_below} the category range." (action BRAND-C24)
- discounting is undercutting premium positioning: discount_depth_vs_category is positive and premium_signal_score is above the category norm at the same time → "The brand discounts {pct} points deeper than the category while claiming a premium position." (action BRAND-C24)
- the same loss reason keeps repeating: the same coded reason appears in 3 or more win-loss interviews against the same named competitor → "{n} people chose {competitor} over us for the same reason: {reason}." (action BRAND-C58)
- battlecard claim is stale: battlecard_freshness_days exceeds 90 for a claim still in active use → "The claim '{claim}' on the {competitor} battlecard has not been checked in {n} days." (action BRAND-C57)
- a lower rung of the ladder is gaining: public demand signal for a lower-commitment alternative (including doing nothing) rises faster than demand for the category itself → "Interest in '{rung}' is growing faster than interest in the category." (action BRAND-C18)

### Visuals specified

- XY positioning map (scatter plot, 2 axes): brand and every tracked competitor plotted, with open quadrants marked
- price ladder (horizontal band chart): brand and the 7 competitors' prices on a matched product, with the category range shaded
- competitor change feed (reverse-chronological timeline): new creative, price move or launch per competitor, most recent first
- category ladder diagram (vertical ladder): every rung from doing nothing up to the closest direct rival, with the brand's position marked
- battlecard table (comparison table): brand versus one named competitor, verified differences only, with a freshness flag
- win-loss reason breakdown (bar chart): count of losses to a named competitor, grouped by coded reason

### Not in the usual tools

- the positioning map plots the brand against every real shopper alternative, including doing nothing and adjacent categories, not only direct rivals
- the price audit ties price band to the category's own learned range and the brand's premium signals, not just a raw price diff
- competitor watch here reads only public signal (ads, sites, prices, launches) for the 7 brands already in this brand's gallery, and alerts only on real crossings
- win-loss research asks real almost-buyers why they chose a named competitor, producing comparison language no price or ad tool can give
- the category ladder explicitly includes doing nothing and job-based alternatives outside the obvious category
- battlecards here are gated on verified differences with a refresh cadence and a staleness flag

### Data this screen needs

- `competitor_set`: brand, competitor_name, site_url, ad_library_id, marketplace_listings, active_flag (meta_gallery competitors.json, BRAND-C07)
- `competitor_price_capture`: competitor_name, product_match_id, price, price_incl_tax (sales tax for US; GST for an India-market competitor, markets: IN), discount_pct, captured_at (price capture script (not yet built))
- `competitor_ad_capture`: competitor_name, creative_id, first_seen, angle_tag, channel, media_url (meta_gallery comp_media.json, BRAND-C56)
- `category_ladder`: brand, rung_name, rung_type (do_nothing, adjacent, direct), demand_signal (BRAND-C18)
- `positioning_map`: brand_or_competitor, axis_x_score, axis_y_score, quadrant_label (BRAND-C19)
- `battlecards`: brand, competitor_name, claim, evidence, last_verified (BRAND-C57)
- `win_loss_interviews`: brand, respondent_id, outcome (win, loss), named_competitor, reason_code, quote, date (BRAND-C58)
- `brand_own_margin_data`: brand, aov, gross_margin_pct, orders_per_repeat_buyer (store order and finance export, BRAND-C23)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | 0.1 to 0.8 | 2026-09-28 | Bombas brain and simulated prices |
| 5 | 5.1 to 5.6 | 2026-09-28 | Hand-offs; action lanes; season plan; quarterly review; exports (and the 5.4 load fix); browser smoke test |
| 4 | 4.1 to 4.10 | 2026-09-28 | Placements and new channel alerts; gap lines; stop rules; unit from the brain; never zero; phone width; threat history; support answers; room metrics. Screenshot `round4.png` |
| 3 | 3.1 to 3.10 | 2026-09-28 | Page-summary captures and diffs; price moves; landing page tracking; printable report; battlecards; positioning test; win-loss kit; tunable thresholds; second brand. Screenshot `round3.png` |
| 2 | 2.1 to 2.10 | 2026-09-28 | Lost by name; category ladder; review themes; Amazon against our site; creative velocity; weekly brief; niche sizing; premium signals; search seeds; desk tabs. Screenshot `round2.png` |
| 1 | 1.1 to 1.10 | 2026-09-28 | Plan first; rank override; 12 pages side by side; coverage matrix; hook and offer mix; references; price and pack ladder; positioning map with moves; changes timeline; freshness and re-pull; rank for all 14 rules. Screenshot `round1.png` |
