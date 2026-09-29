# Brand and customers: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton (done 28 Sep 2026, S3.7, Bombas)

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: simulated badge, tiles, insights, chart, avatars, objection map, language bank, voice sheet, decision row, audit table | done |
| 0.2 | `api.py`: `overview`, `audit`, `POST voice/examples`. Brand facts through `app/brain/store.py`; cohorts through `app/data/tables.py` | done |
| 0.3 | 3 tiles (grounded avatars, objection coverage, repeat within 3 months), 2 insight rules, 1 chart (repeat within 3 months by first-order month) | done |
| 0.4 | Avatar cards: share estimate, intensity, job, up to 3 quotes with source links, top doubt with proof or no proof, badge grounded / one source / inferred | done |
| 0.5 | Objection map: objection, avatars (from ladder rungs), proof or open question, quotes, coverage in ads and on pages | done; ads and pages show unavailable (no angle field in `ad_rows`, no live page scan) |
| 0.6 | Language bank by theme: phrases with counts, mentions by source, one quote per phrase with link | done |
| 0.7 | Voice sheet: do, do not, tone by context from voice records; liked and disliked examples box writes founder records (`<brand>.voice.<kind>_example_<sha8>`) through `Brain.put`; marking the other way retires the old record | done |
| 0.8 | `audit.py`: CUST-R01 ungrounded avatar, CUST-R02 uncovered top objection, CUST-R03 objection coverage in ads (unavailable until ads name an angle) | done |

Round 0 notes:
- Repeat within 3 months is computed from `cohorts.json` `active_by_month` (months 1 to 3 summed, over cohort size). A buyer active in 2 of those months counts twice, so it is an upper bound. `repeat_rate_90d` in `metrics.py` needs order rows, which read as unreadable for Bombas, so the chart does not use it. A contract session could add a cohort-level repeat metric from the aggregates.
- The audit entity for an avatar is type `brand` with the avatar key as id: `audit.md` has no `avatar` type yet. Propose one in a contract session.
- Ad coverage needs an angle per ad. The simulated `ad_rows` has placeholder text and no angle; the generator or an ad naming rule would fill it.
- "Ungrounded" means no quotes, or quotes from fewer than 2 independent sources. On Bombas 7 of 11 avatars rest on 1 source.

## Round 1: the execution surface (from 28 Sep 2026)

Judged by `app/contracts/depth.md`. Each feature ends in an action with an owner, steps and an artefact.

| # | Feature | Status |
|---|---|---|
| 1.1 | Round 0 anti-patterns out: plan board first with ranked actions from `rank`, orientation beside it (new customers 28d, returning share, repeat in 3 months, avatars with proof, rungs without proof, oldest avatar check), what is wrong grouped by rule with evidence and a link to its action, action cards with steps, desk, audit and rule list at the bottom. Tiles, insights and the repeat bar chart removed. `rank(brand, window)` in `api.py` gives every action a real title | done |
| 1.2 | Avatar cards: job, moment, pain, top doubt with one-star and five-star counts, proof on file, where their voice shows (channel chips). Each ends in the next build from a rule in `builds.py` (offer when the top doubt has no proof and the rung lists offer, page block when it has no proof, research note when there are no quotes, else an ad brief), with owner, steps, a drafted artefact filled from the brain, Copy brief and the decision row. Reddit lines are never shown as testimonials | done |
| 1.3 | Where each avatar gets an answer: a coverage matrix of avatars by channel (ads and email, product page, Amazon listing, support replies, offer). Each cell is doubts answered with proof against doubts that channel must answer, from the ladder rungs and their `uses`. Red cells carry "Brief it", which opens a side panel with a drafted brief, owner, steps and the decision row. Beside it, Meta formats us against the category median from the Ad Library pulls in the brain, with a test brief for a format the category runs in 15 percent or more of live ads and we run at under half that | done |
| 1.4 | Doubts rung by rung, per avatar: pills filter the ladders by avatar with the count of rungs without proof. Each rung shows one-star against five-star as a split bar, the proof on file and a verdict from a rule: no proof (copy, or an offer when the rung lists offer), not landing (proof on file yet one-star is 2x five-star or more with 10 or more: move the proof to the first screen), lead with it (five-star above one-star: an ad brief), keep. Every move opens a drafted brief with owner and steps. The old objection table sits under a fold | done |
| 1.5 | Their words for each doubt: phrases from the language bank linked to each rung (through `derived_from`), split into how they say the doubt (complaint or 1 to 2 star) and how they say the win (praise, result or 4 to 5 star), up to 6 each, generic lines dropped, Reddit lines marked language only and unticked. Avatar pills. "Use in brief" builds a copy brief from the ticked lines with the proof, owner and steps. All phrases by theme sit under a fold | done |
| 1.6 | When buyers come back and where they stop: cohort grid of 18 first-order months by months 1 to 12 since the first order (active share, a cell only once its month ended), with the breaks named by rule: peak return month (months 1 to 3), calendar break (half or more of cohorts fall 40 percent or more in the same month: January 2026 for Bombas), age break (largest median fall after the peak, cliff months left out), weak cohorts (repeat months 1 to 3 under 0.8x the median). Each break becomes a retention move card: second-order email day, win-back start day, a plan for the cliff month, a post-purchase branch for weak cohorts, each with a draft, steps and a check date. Orientation: peak month, median repeat, estimated 12-month value | done |
| 1.7 | Who comes back and through which channel: returning share of orders by month, this year against last (line), and a waterfall of returning orders by channel from the same month last year to the latest full month. Rules: share down 2 points or more against last year (a win-back plan for the channel that lost most), a quarter or more of returning orders through paid ads (exclusion list and owned-channel capture, a person applies it in the ad account), email and SMS growing 5 points slower than other channels (a flow health review). Bombas: 29.9 percent of returning orders came through paid ads in Aug 2026 | done |
| 1.8 | Which avatars we serve and which we leave to others: a positioning map of avatars by share of buyers against how well we serve them (five-star share on their doubts), split at the median share and the all-doubt five-star share into core, fix first, scale and park, with a verdict table that opens each avatar's next build. Beside it, buying situations the category pushes (from competitor positioning and hooks in the brain, and Reddit) against the avatars we hold: gap when 2 or more competitors push it and we hold none, watch for 1 or Reddit only; gaps and watches carry a research note to size the buyer, a person decides. Bombas: hiking and outdoor is the gap (Stance, Darn Tough, Smartwool) | done |
| 1.9 | Where reviews say we misread an avatar: product lines from the brain's review summaries with their 1 and 2 star share against the median line, verdict problem (1.5x the median or more), split (praise and complaints name the same trait: an expectation copy brief) or fine. Misread cards: an avatar buys the line (2 or more linked reviews, from its own reviews and the reviews behind its doubts), a top complaint shares words with its job or pains, and the line sits at or above the median. Each becomes a fit block for the page, expectation copy, a product quality ticket or a fulfilment ticket, with owner and steps. Bombas: compression fails the Daily Compression Wearer on the job itself (17.3 percent 1 and 2 star, 2.24x the median) | done |
| 1.10 | Seven new audit rules from the desk (CUST-R04 proof not landing, R05 avatar misread on a product line, R06 unserved buying situation, R07 returning buyers bought back through paid ads, R08 calendar retention cliff, R09 retention age break, R10 split product line), all 10 firing on Bombas. `rank(brand, window)` pairs every finding with the drafted work from the same builders the page uses: real title, owner, steps, artefact kind and draft, stop rule and check date where the move has one; ease rescored by owner (agent 5, agent drafts 4, person with a draft 3, connector 1). 27 actions pass `validate_action`; the top one is the compression misread | done |

## Round 2: rules from the web pass (from 28 Sep 2026)

Web pass: Peel, Triple Whale, Lifetimely, Klaviyo predictive, Daasity RFM, Thematic and Enterpret theme impact, Copyhackers review mining, Fairing and KnoCommerce surveys, Moesta four forces, Dovetail evidence trace. Order-level rules wait on an aggregate (see Contract asks) and ship with a fixture test and an honest unavailable state.

| # | Feature | Status |
|---|---|---|
| 2.1 | Which review themes cost us the most stars: impact = share of rated reviews with the theme x (average stars with it minus without it), from the rated reviews in the language bank (8 or more per theme), with a rising flag (last 90 days share 1.5x the earlier share, 5 or more reviews). A diverging bar per theme; a theme that costs stars links to its ladder's open answer or not-landing fix, a theme that earns stars to its lead-with-it ad brief. Bombas: price and value costs the most (12 percent of rated reviews, 0.52 stars below the rest); comfort earns 2 stars | done |
| 2.2 | Which words buyers praise us with that we never say: words in 3 or more praise reviews (4 and 5 star or praise themes, Reddit left out, brand name and filler dropped), the top 20 by reviews, each checked against every site and founder record in the brain, with 2 snippets of how buyers say it. "Brief the top 5" drafts page bullets and ad first lines from the missing words. Bombas: soft (16 reviews), slip, wash, worth and durable never appear in our own records. Not a live crawl; a page scan would replace the brain corpus | done |
| 2.3 | Which avatars we can bet on: a gate table of every avatar against 9 checks (core: job stated, 5 or more quotes, 2 or more sources, share known, doubt mapped; plus top doubt proven, 2 or more moments, 2 or more pains, checked in time). Validated only when every core check passes. Every failed cell is a Fix button with a task: owner, steps ending in a person approving the record, and a draft. Bombas: 0 of 13 pass, the brain holds 3 to 4 quotes per avatar; 42 tasks | done |
| 2.4 | Which lines buyers repeat that could open an ad: 2 to 4 word phrases found in 3 or more distinct 4 and 5 star reviews (Reddit left out, filler at either end dropped, a shorter phrase kept only when it stands apart), top 15 with review counts and the 3 avatars they sit on most. Tick hooks and "Brief the picked hooks" drafts an ad brief, one hook per variant. Bombas: great quality (8), stay in place (6), don't slip (5), worth the price (3) | done |
| 2.5 | What pushes each avatar to switch and what holds them back: every line tied to an avatar (its quotes and the reviews behind its doubts, Reddit left out) coded as push, pull, anxiety or habit by word patterns, with competitor names from the brain counted as habit. Under-researched when a force has no line or anxiety plus habit is under 15 percent; each gets a 5-call switch interview script (a person runs it, the agent codes the notes back into the record). Bombas: push is thin everywhere; 5 of 13 avatars under-researched | done |
| 2.6 | Draft a new avatar from a gap: for every gap or watch situation, a drafted avatar record from the brain (mentions by source from the language bank, up to 5 non-Reddit quotes with links, the competitors that serve it; job, share and pains left unavailable). "Add as provisional avatar" posts to `POST avatars/draft`, which writes it through `Brain.put` as tier inferred with an agent source and `derived_from`, once. Bombas: hiking and outdoor (2 Reddit mentions, served by Stance, Darn Tough, Smartwool) and style | done |
| 2.7 | Which avatar moments are coming and what ships before each: moments named in avatar triggers matched to US dates (holiday gifting, winter, Valentine's, Mother's and Father's Day, back to school, summer, race season, New Year), 6 months ahead, with ads live 21 days and emails 14 days before, last year's sales index for that month, a timeline and a dated plan card per moment (check date is the ads-live date; late when that date has passed). Bombas: winter from 15 Nov (ads by 25 Oct, 1.51x) and holiday gifting from 1 Dec (ads by 10 Nov, 1.93x) | done |
| 2.8 | What we ask buyers to close these gaps: a post-purchase survey where every question names the gaps it closes (which avatar sounds like you, with the unserved situations as options; what almost stopped you, from the rungs without proof; what you bought before, for avatars missing push or habit lines; how you heard about us; who the order is for). Days to 385 answers (a share within 5 points) from orders a day and an assumed 15 percent response. "Open the survey draft" gives the spec, owner and steps; answers are written back to the avatar records as drafts a person approves. Bombas: 5 questions, 15 gaps | done |
| 2.9 | Which first product brings buyers back and when to nudge them: gateway products (180-day repeat 1.3x the median first product or more, 100 or more first buyers) and dead ends (0.7x or less), the second-order path (next product at 15 percent or more of repeaters, email on its median day minus 5), win-back timing from the median order gap (due 1x, win-back 1.5x, lapsed 3x), and a save flow when the 3+ orders, 91 to 364 days cell grows 20 percent. Reads a `customer_paths` aggregate; tested on a fixture. Bombas shows the rules and an honest unavailable state until the aggregate exists (Contract asks) | done |
| 2.10 | Six more audit rules (CUST-R11 review theme costs stars, R12 buyer words we never say, R13 provisional avatars with the survey as the fix, R14 under-researched avatar, R15 avatar moment within 45 days of its ads-live date, R16 order-level paths unavailable until the aggregate exists), all 16 firing on Bombas. `rank` pairs each with its drafted work; 38 actions pass `validate_action`. Helpers the page and the audit share moved into `audit.py`. Screenshot `round2.png` (gate, forces, survey) | done |

## Round 3: brand side of the room (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 3.1 | Do buyers describe us the way we describe ourselves: the brain's positioning records (frame, category, price frame, proof points, pitch) against the top 20 words in praise reviews. Score = share of their top words our positioning uses; their words we lack in red; our words buyers never echo, and the ones they do. Brief it drafts 3 lead lines that keep the frame in buyer words, tested in 2 ads before a person approves a new positioning record. Bombas: 25 percent; soft, stay, wash, slip never appear; performance, engineered, extreme are never echoed | done |
| 3.2 | Which claims unhappy buyers throw back at us: every site-backed or approved claim against the 1 and 2 star reviews in the brain (Reddit left out); under fire when 3 or more use the claim's own feature words (product line names from the brain left out), watch for 1 or 2. Each claim under fire opens a fix: add the proof next to it or narrow the words; a person picks and the claim record changes only then (BRN-C03). Bombas: the calf sock stay-up and heel claim meets 12 reviews about sliding down at the heel | done |
| 3.3 | Is anyone pretending to be us: pages the Ad Library pull marks as likely impostors, with ads seen, first seen, where they link and the Ad Library link. Each is a person-owned action (the agent never writes to Meta): report the page as impersonation, a drafted support macro and a social note naming the real site, re-checked on the next pull. Bombas: 1 page, 54 gift sale ads linking to sockscool.com | done |
| 3.4 | Which offer answers which avatar: a matrix of avatars against the offers, policies and claims that answer their doubts (from the ladder proof records), then offers no ladder uses. The offer our ads push most (from the Ad Library promo records) is read against the doubts; when it answers none, Brief the offer test drafts a discount-against-guarantee A/B a person budgets. Bombas: COMFORT20 sits in 21 of 23 live ads and answers no doubt; nothing answers the Daily Compression Wearer | done |
| 3.5 | What every page and email leads with: a messaging hierarchy built from buyer evidence (lead on the theme that earns the most stars, in the top buyer words; 3 proof points ranked by the five-star lines on the doubts they answer; 1 doubt to answer first), beside our current frame. "Approve" writes it through `POST messaging/approve` as an approved founder positioning record every screen reads. Bombas: lead on comfort (soft, stay, wash); proofs: ankle sock build (78), pack ladder (31), exchanges (28); answer first: holes within weeks | done |
| 3.6 | Does this line sound like us: paste a headline, ad line or email opener beside the voice sheet and `POST voice/check` returns pass, warn or fail with a reason per check: longest sentence (20 words), reading grade (under 10), em dashes, inflated or weak words, unproven claim words (best, perfect, never, clinically), close to a forbidden claim in the brain, close to a line the founder marked not us, and whether it uses the buyer words from 2.2. Nothing is written | done |
| 3.7 | Is the brand getting stronger or weaker with buyers: a 12-month trend strip from our own store data (returning share, repeat in months 1 to 3 by cohort, tickets per 1,000 orders, items given per order), rules for repeat down 3 points over the last 3 cohorts and tickets per 1,000 orders up 20 percent over 3 months (each a cause review the agent runs), and person-owned connect cards for the lines that need a source: branded search, mentions and sentiment, review rating by month. Bombas: nothing moving the wrong way | done |
| 3.8 | One-pager for a creator: every avatar card opens a plain-text brief from `GET avatar/<key>/brief` with share and evidence status, job, moments, pains, each doubt with its proof or "no proof yet, do not promise it", their words for the win and the doubt (Reddit left out), hooks tied to the avatar, misreads to watch, dates, the next build and what not to say. Copy and print from the panel | done |
| 3.9 | When in the year each doubt peaks: a heatmap of 1 and 2 star reviews behind each ladder theme by month of year (Reddit left out). A season is a 3-month window where the theme's share of all complaints is 1.5x its share over the year, with 4 or more, so months the pull over-samples do not fake a season. Each season is a page, email and macro answer to ship 21 days before it starts, flagged ship now when it has started. Bombas: price and value doubts peak Oct to Dec (48 percent of complaints against 26) | done |
| 3.10 | Seven more audit rules (CUST-R17 perception gap under 50 percent, R18 claim under fire, R19 lookalike page, R20 pushed offer answers no doubt, R21 doubt season, R22 no approved messaging hierarchy, R23 brand health line falling), each paired in `rank` with its drafted work; reputation raised to 5 for R18 and R19 per the audit docstring. 46 actions; the lookalike report, the comfort season and the calf claim now sit in the top 4. Approving the hierarchy clears R22. Screenshot `round3.png` | done |

## Round 4: one desk, hand-offs, and the room's remaining jobs (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 4.1 | The desk in tabs by job (Avatars, Doubts and words, Offers and claims, Retention, Brand and voice) below the plan, what is wrong and the actions; `#tab=<key>` opens a tab. Every desk section sits in exactly one tab (tested); the plan stays the first section | done |
| 4.2 | Plan by job: every ranked action carries a `job` that matches a desk tab (rule to job map in `api.RULE_JOB`, tested against the rule list). Pills over the plan filter the 10 moves by job with counts, and "Open the desk" jumps to that tab. Bombas: avatars 19, doubts and words 9, offers and claims 8, retention 5, brand and voice 3 | done |
| 4.3 | Which tests this screen proposes: `GET tests` returns registry rows (events.md shape, status proposed, id left to 25-experiments, metric names from `metrics.py`, registered on the window end, start a week out, read point by the test's minimum days): guarantee against discount (cpa), lead line in buyer words (ctr), buyer hooks (cpa), the seasonal doubt answer (add to cart rate), the compression fit block (return rate). Shown under the actions with Copy row and Copy as JSON. 25-experiments owns ids, overlap checks and results | done |
| 4.4 | What other screens get from here: `GET handoff` builds one pack per reading screen in events.md (09-creative: ad briefs, lead-with-it briefs, the format test, the hook bank; 10-copy: copy briefs in their words, the copy gap, the messaging hierarchy; 07-landing-pages-cro: fit blocks, first-screen proof moves, seasonal answers, expectation copy, claim fixes; 14-email-messaging: retention moves, moment emails, the survey). Cards with counts by kind, Copy the pack and a link to the screen. Nothing is sent; readers pull. Bombas: 16, 18, 13 and 6 items | done |
| 4.5 | Name ads so the matrix can count them: a naming convention built from the brain (AV-<avatar key>, ANG-<doubt theme>, FMT-<format>, HK-<hook>) with every valid key and an example, under the coverage matrix with Copy and steps. `audit.parse_ad_name` reads the tags from ad names, so CUST-R03 runs once live ads carry them; its connect action now carries the convention as the draft. Untagged ads stay unknown, never zero | done |
| 4.6 | Is each avatar one buyer or two (BRAND-C12): product lines behind each avatar (its own reviews count 3 times a review linked through a doubt) and its doubt themes. Two buyers when 2 lines each hold 30 percent or more and their top complaints share no words: a drafted split into 2 avatar records a person approves. Broad when 3 or more doubt themes and none at half: a research note. Bombas: Parent Buying For Kids splits into calf sock and slipper buyers; Price and Mission Skeptic is broad | done |
| 4.7 | Who our live ads speak to (replaces the brain drift timeline, parked: the brain holds one capture date, so there is no drift to show yet): our live ads by hook from the Ad Library read in the brain, matched to the avatar whose name the hook names, against each avatar's share of buyers. Silent (no ad), under (less than half its share), fair, heavy (over 2x). Silent and under avatars get an ad brief. Bombas: 10 of 23 ads speak to the Everyday Comfort Seeker (13 percent of buyers); none speak to 6 avatars holding 80 percent of buyers; 13 ads name no avatar | done |
| 4.8 | What we decided here: a timeline from the shared `GET /api/decisions?screen=` route, newest first, with the action title (matched by finding id), who owns it, and the check date, or the date a "Not now" comes back on the plan (14 days). Counts by choice in the line. Empty until the founder decides something; nothing is written by this feature | done |
| 4.9 | Which avatar we build for next (replaces avatar value by product revenue, which needs a SKU to product-line map; see Contract asks): one score out of 100 per avatar with a share, from fixed weights shown on the page (share of buyers 40, how poorly we serve them 30, how little our ads speak to them 20, share of doubts still open 10), top of the Avatars tab, each row opening its next build. Bombas: build for the Durability Disappointed Repeat Customer next (89), then the Guarantee Reassured Loyalist (85) | done |
| 4.10 | Two more audit rules (CUST-R24 avatar may be two buyers, CUST-R25 an avatar with 12 percent or more of buyers that no live ad speaks to), with their drafted split and ad briefs in `rank` and a job for the plan filter; the audit's avatars now carry their next build. 25 rules, 24 firing on Bombas (brand health is steady). Screenshot `round4.png` (the desk tabs, focus score, avatar cards) | done |

## Round 5: returns, support and depth per cell (from 28 Sep 2026)

Lead's review: rounds 1 to 4 passed. Focus: returns and tickets by avatar, depth of each existing block, and depth.md section 3 applied to this screen.

| # | Feature | Status |
|---|---|---|
| 5.1 | Depth rules as tests on this screen: rule 11 (no brand, competitor, promo or dollar fact in `screen.js` or `index.html`), rule 12 (no em dash, should, consider or leverage in titles, whys, steps or the page; under 45 words), rule 4 (every open finding shows its numbers), rule 8 (rules that read tables carry simulated evidence), rule 7 (unavailable is null or a connect action, never zero). One heading fixed | done |
| 5.2 | Which avatars send the most back: return risk per avatar (the lines it buys, weighted by how often, times each line's 1 and 2 star share and the share of its top complaints that are fit or wear), high at 1.25x the median with a fit-before and day-2-after email brief; refunds over net sales for the last 3 months as orientation; the ticket and return reason read as a person-owned connect card until tickets are aggregated by reason and line (Contract asks). Bombas: the Daily Compression Wearer at 1.68x, driven by compression that is hard to pull on | done |
| 5.3 | What support says to each doubt: a drafted reply for every rung whose uses include support macros, in the buyer's words, answered from the proof on file (ready), from a guarantee or exchange policy a person checks (check), or left for a person to write; complaint rungs apologise and ask for the order number, question rungs answer plainly. Copy all, and a fifth hand-off pack for 15-customers-cx. Bombas: 16 replies, 11 ready, 5 to check | done |
| 5.4 | Each coverage cell explains itself: every avatar by channel cell carries the rungs behind its count (doubt, one-star and five-star counts, the proof or open), and a click opens them in a side panel with "Brief the open ones". A cell with no doubt says so | done |
| 5.5 | Are marketplace buyers a different avatar: where each avatar's reviews come from (its quotes plus the rated reviews behind its doubts, Reddit left out); marketplace-led at half or more on Amazon, with a listing fix that answers its top Amazon doubts in the first 3 bullets, for 20-marketplaces. Sampling caveat on the page. Bombas: the In-Store Single Pair Trier (74 percent Amazon), Guarantee Reassured Loyalist and Price and Mission Skeptic, all led by "is it worth more than ordinary socks" | done |
| 5.6 | Which avatars need a re-check soon: every avatar and ladder record by its expiry date (expired, due within 30 days, ok, no date), with one agent task that re-reads the sources and proposes updates to the brand brain review queue, checked on the first expiry. Bombas: 11 avatars expire on 28 Oct; the 7 ladders and 2 Reddit avatars carry no expiry | done |
| 5.7 | How strong is each read: a fold above the desk tabs lists the sample behind every block (quotes, mentions on rungs, rated, praise and complaint reviews, dated complaints, coded lines, linked reviews, live ads read, first-time buyers) with its tab, thin under 100 reviews or 30 items (60 quotes for avatar cards). Thin blocks get one "widen the thin reads" pull plan; a person approves the spend before any pull. Bombas: avatar cards (38 quotes) and the ad read (23 ads) are thin | done |
| 5.8 | Avatar cards say what we know and what we do not: each card gains chips for its build rank (from 4.9), ad voice (silent, under, fair, heavy), return risk against the median, where it speaks (Amazon or our site) and the split read, plus a "we do not know yet" line listing every evidence check it fails. Built once in `builds.card_meta` from the same builders | done |
| 5.9 | Which avatars doubt the price and what answers it: the share of each avatar's one-star mentions on price rungs, price-led at 30 percent or more, with the facts the brain holds as orientation (free shipping point, lowest single pair, shipping as a share of one pair, pairs to free shipping) and a pack picker brief that shows the free shipping line; per-pair price by pack stays unavailable until pack prices are in the brain (Contract asks). Bombas: the In-Store Single Pair Trier, Price and Mission Skeptic and Guarantee Reassured Loyalist are price-led; one pair pays 61 percent on top in shipping | done |
| 5.10 | Five more audit rules (CUST-R26 avatar with high return risk, satisfaction 4 per the docstring; R27 marketplace-led avatar; R28 price-led avatar; R29 records due for a re-check; R30 thin read, one per thin block), each with its drafted work in `rank` and a job. 30 rules, 29 firing on Bombas. Screenshot `round5.png` (avatar cards with the new chips and gaps) | done |

## Round 6: any brand, any screen size, one weekly view (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 6.1 | Plug and play on a second brand: every route (overview, rank, audit, handoff, tests) renders for the sparse `example` brain with no sample-brand fact and honest unavailable states (tested). Fixed on the way: the simulated note reads the brand name from the brain; the brand's own site is found from its site map and identity urls instead of a coded host; the copy gap is unavailable with no praise reviews; the messaging hierarchy cannot be approved, and CUST-R22 does not fire, until a theme earns stars | done |
| 6.2 | One action per artefact: findings that ask for the same draft become one action, led by the highest-scoring finding, carrying every finding id and an "also answers" note, so the founder approves the work once. Every finding still maps to exactly one action and no two open actions carry the same draft (tested). Bombas: the durability offer now answers R02 and R11, the price proof move R04 and R11; 59 actions | done |
| 6.3 | What is due in the next 30 days: `GET agenda` puts every real date on one list (ads live and emails for avatar moments, seasonal ship-by dates, record re-checks, checks a plan dated, proposed test starts), overdue first, with who does it; default check dates are left out so the list stays short. Bombas: 2 seasonal answers overdue, winter ads by 25 Oct, 11 avatar records re-checked by 28 Oct | done |
| 6.4 | How two avatars differ: pick any two and read 14 rows side by side (share, served well, build rank, top doubt and its proof, open doubts, our ads, return risk, where they speak, price share, lines they buy, their win words, evidence status, next build), rows that differ tinted. Built in `builds.compare_rows` from the same builders | done |
| 6.5 | Each ladder rung opens its evidence: click a rung for a side panel with its counts, mentions by source (Reddit marked language only), the proof, the avatars it names and up to 8 one-star and 8 five-star lines, with Brief it. Also: a test runs `node --check` on `screen.js`, so a syntax slip can no longer reach the page | done |
| 6.6 | Since your last visit: a strip under the head names the new moves (up to 3) and how many were resolved or merged since this browser last loaded the screen, and whether the brain changed. Per-viewer only, in browser storage wrapped so a blocked store just hides the strip; the shared record of decisions stays in the decisions log | done |
| 6.7 | The page at phone width: checked in a 360 px browser on all 5 desk tabs; the served map grid pushed the Avatars tab to 580 px. Fixed in `screen.css`: grid children may shrink, two-column desk grids stack under 720 px, wide tables scroll inside their card, the desk tabs wrap. Page width is 360 on every tab, nothing past the edge | done |
| 6.8 | A monthly customer report for the founder: "Monthly report" in the head opens `GET report` in a panel, 8 short sections in plain words (the three moves to approve, who buys and who to build for next, what stops them, what they say that we do not, who comes back, risks to the brand, due in the next 30 days, what we do not know yet), with Copy and Print; print shows only the report. Works for a second brand | done |
| 6.9 | Faster loads: the overview and `rank` are built once per brand, day or window, brain version, aggregates timestamp and brain root, and every caller gets a copy, so a brain edit or a data refresh rebuilds them and nothing leaks between callers (tested). Overview 0.215 s cold, 0.013 s warm | done |
| 6.10 | Money on the audit where the tables allow: CUST-R07 prices paid returning orders against the brand's own 12-month median paid share (share gap x returning orders x paid spend per paid order, cost-side, inputs written so a founder can redo it; `builds.paid_stake`). Bombas: 29.9 percent sits on its median, so the stake is null with that reason, not a number pushed by the 25 percent target. Checked the master list: 59 actions, best 62, none in the top 10 because no finding here has a baseline gap in money yet. Screenshot `round6.png` (the monthly report) | done |

## Round 7: depth rules on this screen, money where history allows, briefs to take away (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 7.1 | Depth rule 5, sized with a stop rule: every action that moves money or traffic (offer, ad brief, page section, listing, copy, flow, email, budget move) carries a size from its finding's first number (money first when known), a stop condition with a count and a check date. Thresholds are named in `builds.size_stop`; the card shows the size where it said "stake unavailable" | done |
| 7.2 | Depth rule 10, reads in one pass: all 33 desk blocks keep their question heading and rule line, and now show the window they read (brain date, Ad Library read, or store months, simulated) beside the heading and one caveat line at the foot, with the sample from the strength read when there is one ("Based on 3,844,512 first-time buyers, simulated."). Built in `builds.block_notes`; tested for every desk id, both brands, sentences under 20 words | done |
| 7.3 | Depth rule 9, gaps not only totals: every desk block now leads with one computed gap line, marked never tried, cross-source check or against competitors ("6 avatars hear no live ad of ours: 80 percent of buyers", "Our claims against 136 reviews of 1 or 2 stars: 1 of 6 under fire, 4 to watch", "1 segment the category serves and we have no avatar for: hiking and outdoor"). A block with no inputs says unavailable with its reason; on Bombas only customer paths does. Built in `builds.block_gaps`, counts tested against the blocks | done |
| 7.4 | Depth rule 14, the founder can disagree: the screen's `rank` now reads the decisions log fresh on every call, after the cache. The latest decision on any finding an action carries shows on the action with its date. "Not now" sets status snoozed with the day it comes back (14 days, the shared snooze), moves it out of the plan, the actions, the agenda and the report, and lists it under the actions with both dates. Saving a decision reloads the page. Tested on a temp log, never the shared one | done |
| 7.5 | Money on retention against own history. CUST-R08 (calendar cliff): per cohort, the share the month before x the median step at that age outside cliff months, minus the share in the cliff month, x cohort size, summed, x that month's AOV; a note says when the same month last year is outside the grid, so part may be the season. CUST-R09 (age break): the fall above the median fall at other ages x the share x the median cohort size x the median AOV, per cohort. Both redo from their inputs (tested). Bombas: January 2026 cost $5,842,578 (80,046 orders over 10 cohorts); the month-7 break $63,664 per cohort. The January plan now leads this screen and is number 5 on the master top 10, the first of ours to make it | done |
| 7.6 | Take an avatar away: "One page to take away" on each avatar card opens 8 sections from the same builders (at a glance from the compare rows, job and moments, doubts top first with proof or NO PROOF YET, their words, what to build in order with owner, size, stop rule and check date, what we do not know, dates and watch-outs, do not say), with Copy and a Print that prints only the page. Actions match by avatar name, avatar key or the avatar's own doubts. Replaces the round 3 plain-text one-pager. Works for a second brand | done |
| 7.7 | Keyboard: j and k move focus through the plan items and the action cards, Enter opens or closes how it gets done, ? lists the keys, Esc closes any panel (kit). Keys are left alone while typing, on a button or link, or with a panel open. Checked in a browser: j, j, Enter, k, ?, Esc all land | done |
| 7.8 | Do reviews and sales agree on who buys: each line's store sales over 12 full months (`products_monthly`, SKU to line through a local fixture until the data layer carries the map) split across avatars by their share of that line's linked reviews, next to each avatar's share from reviews. Differ at 1.5x either way; each disagreement, and each avatar with a share from sales only, gets a drafted survey check to settle it. Bombas: lines cover 61 percent of sales; 4 of 7 avatars differ (the Everyday Comfort Seeker is 13 percent of reviews but 3.6 percent of sales) and 4 more get a share for the first time (In-Store Single Pair Trier 18.2 percent). Unavailable with the reason for a second brand | done |
| 7.9 | Print polish: the monthly report and each avatar page open with one line naming the brand, the window and the simulated label, once, in the panel, the copy and the print. Print keeps each section whole, sets page margins and prints black on white. The three moves in the report now carry their money or size ("$5,842,578 at stake, 2026-01"); "12 1 and 2 star reviews" reads "12 reviews of 1 or 2 stars". Checked as a print PDF in a browser | done |
| 7.10 | CUST-R31 reviews and sales disagree on who buys: one low finding per avatar whose share of sales by line is 1.5x its review share either way, or who has a share from sales only; each maps to its drafted survey check in `rank` (LIFE-C29, founder gate, agent drafts; 7.8's action fixed to match the catalogue). Unavailable with a connect step when product sales cannot be read. 31 rules, 30 firing on Bombas; 67 actions, 32 of them sized with a stop rule. The rule docstring now says which rules carry money. Also: "12 1 and 2 star reviews" reads "12 reviews of 1 or 2 stars" in the claims finding and line. Screenshot `round7.png` (the plan, led by the January stake) | done |

## Round 8: the desk as deep as the plan, sales in the scores, a second check on January (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 8.1 | Depth rule 5 inside the desk: every move in a block that changes money or traffic carries the size, stop rule and check date of the ranked action built from it (32), or a size from its own row (one-star mentions, share of buyers, praise reviews) with its kind's stop rule and a 7-day check (67). 9 say "size unavailable": avatars with no share yet and one cohort move. Brief panels show size, stop and check. The overview reuses the cached `rank`, so the page load stays the same | done |
| 8.2 | The January cliff against last year: when the monthly table holds the same step a year earlier, that is the baseline, and the stake is only the fall beyond last year's. Bombas: returning orders fell 42.5 percent into January 2026 against 44.2 percent a year before, so the drop is the season and no money is claimed; the 7.5 figure against a normal month ($5,842,578) stays as `season_usd` and in the reason. The finding and the January move now say it is the season. The January plan leaves the master top 10; that is the honest read. Contract ask: a `last_year` baseline kind | done |
| 8.3 | Sales share in the scores: the focus score uses the share of sales by line where reviews give none, with served well read from the ladders the same way, marked "share from sales" on the page; the compare view gains a "Share of sales, by line" row. Bombas: 11 avatars scored, up from 7; the In-Store Single Pair Trier comes in third (79.3) on 18.2 percent of sales. Build ranks on the cards follow | done |
| 8.4 | The avatar page from the compare view: under the pair, "Page for" each avatar opens its one-page brief, and "Copy the N differences" copies only the rows where they differ, for a brief that must not blur the two. Checked in a browser | done |
| 8.5 | Settle it lands in the survey: every "Settle it" move from 7.8 is a gap the survey's situation question closes ("settles 8 avatars where reviews and sales disagree"), and each move's first step names that question. Bombas: the 5 questions now close 23 named gaps, up from 15 (tested: every settle id is in the question's gap ids) | done |
| 8.6 | Browser smoke test: starts the real server on a free port, loads the page in Chromium, waits for the plan, opens all 5 desk tabs, the monthly report and one avatar page, and fails on any script error, console error or same-origin 4xx or 5xx, or on a missing plan, desk block, report section or avatar section. Other hosts are left out (web fonts fail behind this sandbox's proxy). About 5 s; skipped without Node and Playwright. Clicks no decision, so it writes nothing | done |
| 8.7 | Money on weak cohorts, as rule CUST-R32: one medium finding per first-order month that repeats in months 1 to 3 under 0.8x the grid's median, priced as (median repeat minus the cohort's) x cohort size x that month's AOV, with a note on whether the same month last year was weak too (the season, which the post-purchase branch fixes). Maps to the weak-cohort branch in `rank`. Bombas: no weak cohort (December 2025 repeats at 17.94 percent against a line of 17.92), so it stays silent; tested on a cut fixture both ways. Also checked: paid returning share by channel (social, search, email, SMS) sits on its own 12-month median, so no money there either | done |
| 8.8 | Depth rules 7 and 11 on the real page: the screen now passes `?brand=<slug>` from its address to every call, so the same page renders another brain (the example brand shows its own badge and 6 plan items). The smoke test runs both brands and fails on any "undefined", "NaN", "null" or "[object Object]" on any tab, in the report or on an avatar page. Both clean. The rubric side of rule 7 already holds: every dimension has an input or a written fallback (revenue by severity with no money, ease 1 with a connector missing) | done |
| 8.9 | Money on the page head: a "money at stake" number beside the plan, summed from open moves with a stake against the brand's own history, with how many carry it; unavailable with the reason, never 0, when none does. Its title names the seasonal drop left out. Bombas: $63,664 on 1 of 65 moves (the month-7 fall); the $5,842,578 January season is named, not added. To stay within the contract's 3 to 6 numbers, "avatars with proof" folds into the title of "rungs without proof" | done |
| 8.10 | Audit and `rank` for round 8: 32 rules (R32 weak cohort from 8.7, silent here), 31 firing on Bombas; 67 actions. Money now sits only where the brand's own history shows a gap: the month-7 fall ($63,664); January and paid returning are flat against their own past, so none of ours makes the master top 10 (best 62, cut-off 63). Full screen suite: only the known site speed failures. Screenshot `round8.png` (the plan head with money at stake, the focus table with sales-share avatars) | done |

## Round 9: the rules checked everywhere, answers back into the brain (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 9.1 | The first screen: at 1280 by 800 the orientation numbers and at least 3 whole plan items sit above the fold (depth.md section 2), checked by the browser smoke test for both brands. Bombas: orientation ends at 262 px, 4 whole plan items fit | done |
| 9.2 | Writing rules on every sentence the screen writes, across overview, rank, audit, report and an avatar page (678 distinct strings): no em dash, no "should", "consider" or "leverage", sentences under 20 words, customer quotes masked, brain record text copied word for word exempt. 12 of ours failed and were rewritten: the misread why no longer pastes the whole job, the macros, forces, hierarchy, claims, survey and sales-share lines split, the silent-avatar sentence splits, the R25 title reads "Give X an ad of their own", the January reason splits, a test hypothesis shortened. Now a test | done |
| 9.3 | Decisions on the avatar page: a ninth section, "What we decided", lists every decision on this avatar's moves (matched by name, key or its own doubts) with what was chosen, the date and, for "Not now", the day it comes back; "Nothing decided" when the log has none. Read fresh from the decisions log through `rank`. Tested on a temp log | done |
| 9.4 | Survey answers back into shares: the situation question's answers, from a `survey_answers` table when the data layer has one or a local fixture, become a share per avatar with its 95 percent margin. At 385 answers or more the focus score prefers them over reviews and sales (marked "share from survey"); under that they are shown, not used. Bombas: unavailable until the survey runs, said in the sales and reviews block. Contract ask: a `survey_answers` table | done |
| 9.5 | A faster cold overview: profiled; a build read brain sections about 200 times (a third of the time in JSON parsing) and built the desk twice. `audit.ReadBrain` parses each section once per instance and drops the memo on any write; `audit.desk_for` builds the desk once per brand, brain root, day, brain version and aggregates timestamp for both the audit and the plans. Cold overview 0.61 s to 0.23 s, this screen's tests 70 s to 40 s; a brain edit still rebuilds (tested) | done |
| 9.6 | Depth rule 4 as a test: every open finding carries a baseline or threshold, and every number its sentence quotes is in its evidence (star labels, month labels and dates are labels). Fixed: R08 now carries its 40 percent fall line, R12 the 20 praise words read, R20 the 23 live ads, R21 the season's share of complaints against its share over the year, and R31 the median share of sales for avatars with a share from sales only | done |
| 9.7 | Depth rule 6, no dead buttons: 14 row buttons (Keep, No gap, Nothing to do, Site-led and the like) did nothing when clicked. Each now opens why the row needs no move, in plain words with no threshold in page code, and says the row becomes a move when its rule fires. A theme with no ladder now says to add a rung in the brain. Tested: no empty click handler left | done |
| 9.8 | Depth rule 13 as a test: two cold processes with different hash seeds give the same 67 actions (ids, order, totals, finding ids, sizes) and the same 69 findings with the same sentences, so no set or dict order leaks into the ranking; the screen's code imports nothing that could call a model or the network | done |
| 9.9 | The page at phone width, re-checked with the round 7 and 8 blocks (sales and reviews, gap lines, caveats, compare buttons): 360 px on all 5 tabs, nothing past the edge. The smoke test now checks page width at 360 px on every tab for both brands, so a wide block can no longer slip in | done |
| 9.10 | Round 9 close: no new rule; the 32 rules now pass depth rules 4, 6, 12 and 13 as tests, and the page passes 7, 11 and the first-screen and phone checks in the browser for both brands. 67 actions; none in the master top 10 (best 62, cut-off 63), as in round 8. Fixed on the way: a buyer line could show twice on an avatar page and in the compare row. Full screen suite: only the known site speed failures. Screenshot `round9.png` (an avatar page with the share of sales and its decisions section) | done |

## Round 10: the last pass (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 10.1 | No thresholds in page code (depth.md anti-pattern "brand facts in code"): the rule line of all 31 desk blocks is now written in `builds.block_rules` from the builders' own constants, shorter, and the page only shows it with the block's line. The format verdict, the focus tier (next, soon, later), the emails per moment, the snooze days and the agenda window come from the api too. Tested: no percent, multiplier, day count or "N or more" left in `screen.js` strings | done |
| 10.2 | A brand with nothing (an empty brain, no tables): every route renders, all 6 orientation numbers read unavailable, all 34 blocks say unavailable with a reason, and none shows a 0 for an unknown. Fixed on the way: the re-check, survey, lookalike and voice gap lines no longer claim facts when there is no data ("No voice record in the brain yet"), "only 0 rated reviews" reads "no rated reviews yet", and with no avatar at all the top move is "Find the first avatars: 5 quotes each from 2 sources" (CUST-R30 high) | done |
| 10.3 | Anti-patterns walked against the page (depth.md section 7), each tied to a test: a report (plan first, desk, audit last), tiles without a next step (3 to 6 orientation numbers inside the plan, no tile row), findings without an owner (every open or unavailable finding sits in an action with an owner), charts for their own sake (10.9), long prose (every rule and caveat line at most 3 sentences under 20 words; the focus rule shortened), buttons that lead nowhere (9.7), brand facts in code (10.1, 6.1), zero for unknown (10.2, 8.8), one voice for every screen (this desk has its own verdicts and moves), asking the founder to pick features (never done) | done |
| 10.4 | Depth.md sections 1 to 5 last pass. Sections 1 to 3 were under test (section order, the first screen, all 14 rules). Now also: section 4, every rubric dimension 1 to 5, the total the weighted sum and confidence the finding's times 5 on all 67 actions; section 5, the rank route's shape and every action's 20 fields, owners and artefact kinds | done |
| 10.5 | `HANDOFF.md` in this folder for Kevin and the next session: what the screen does and in what order, the files, every route, how each number is made (shares, focus, return risk, the 4 money rules, sizes), the tunable thresholds, each of the 9 contract asks with the exact function to change when it lands, what is still open, and how to check the screen. The api docstring brought up to date. Tested for coverage of routes, asks and money rules | done |
| 10.6 | Loose ends in this file: the room's 14 questions marked built (8), partial (4) or open (2) with where each lives; the contract asks made one list of 9, each with its fallback. The 2 open questions (drift over time, mystery shopper and pretests) and the 4.7 park go to `HANDOFF.md` | done |
| 10.7 | Thresholds a brand can tune (depth.md section 8): a brain `learnings` record with field `threshold_<name>` and a number sets one of 12 thresholds (price-led, sales gap, high return risk, marketplace share, split share, ads under, season lift, claim hits, paid returning, weak cohort, focus soon, re-check days), each inside fixed bounds; anything else is ignored. The build runs with the brand's values under a lock and puts the defaults back, so a threaded server never mixes two brands. The rules, the findings and the rule lines follow (tested: price-led at 60 percent drops avatars from CUST-R28 and the line says 60 percent) | done |
| 10.8 | The plan's connect strip (depth.md section 5): already built, now under the browser test. Unavailable actions never enter the plan; they sit in their own "Connect first" strip, one card each. Bombas: 2 (the store's channel orders for paid returning, and the customer paths table), 0 connect items in the plan | done |
| 10.9 | Charts: each of the 5 charts sits beside the moves it drives, so none goes; each now names the decision it changes in its note (the cohort grid: the day of the second-order email, the day win-back starts and the month to plan for; brand health: whether a line needs a move; the returning-share line: whether win-back is due; the channel waterfall: which channel to fix first; the served map: which avatar to fix first and which to park). Tested: every chart has its line | done |
| 10.10 | Round 10 close: 32 rules, 67 actions, every depth.md rule and anti-pattern tied to a test, about 210 tests on this screen, the browser test for 2 brands at desktop and phone width. No row in this file is left as todo (tested). Screenshot `round10.png` (the price block with its rule line from the api and its gap). The 10 rounds are done; the report to the lead is this session's final message, since no tool here can message the lead session | done |

## Round 11: hand-offs on the shared table, depth again, the open questions (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 11.1 | Hand-offs on the shared table (events.md): each pack (creative, copy, landing pages, email, cx) is also a list of rows in the table's shape, each carrying its move's why, stop rule, check date, owner, capability and id. "Send N to <team>" posts the rows that team does not already have from this screen, then shows how many sit on its list by status. Sending twice adds nothing twice. Another brand copies instead of sending until the table carries a brand (contract ask). Browser-tested against a server whose logs sit in a temp folder, so the real list is never touched | done |
| 11.2 | Decisions by brand: `rank`, the avatar page and the decisions list read only this brand's decisions, the latest per finding winning; a row with no brand is the default brand's, as the server reads it. The page learns only whether it is the default brand, so no brand name leaks to another brand. Posting still has no brand: the kit's decision row does not send one yet (contract ask) | done |
| 11.3 | Depth second pass, walked block by block in the browser for both brands. Every block already had a gap line; now every block also ends in an action. An unavailable block gets "Fill this block" on its gap line: a drafted brief with owner, steps and a check date (brain records drafted for a person to approve, the store connected read-only by a person, or an Ad Library pull by page id with spend approved). Bombas: the customer paths block was the one without an action; the example brand had 21. The browser test now fails on any block with no button; sized moves and unavailable-not-zero stay under their round 7 to 10 tests | done |
| 11.4 | Drift over time, as far as the brain allows: a new Brand-tab block, "What changed in what buyers say about us?", compares each theme's share of praise and complaint reviews in the last 180 days against the 180 before, from dated public reviews. Worse at 5 points with 10 or more mentions, watch with 5 to 9 (thin), each with its answer brief. Bombas: durability complaints 5 to 13 percent (thin, 1 to 6 mentions); price complaints fell. Our own site, ads and email stay unavailable (one capture in the brain), with a drafted quarterly scan plan to start the series | done |
| 11.5 | Mystery shopper and pretests, as far as the brain allows: a new Brand-tab block, "Would a real shopper get stuck, and does our message land?". The run sheet has 8 checkpoints (home, product page, size help, cart, checkout, order email, support, return), each against the brain fact it must match (the lead message, the top doubt, the free shipping line, the first-order code, the returns window and refund method, our drafted support reply); a person runs it, support passes inside 24 hours. A message pretest per top avatar puts our line against one in the avatar's words on its own top doubt, shown to 5 matching buyers. No model runs here. Results are unavailable until a runs table exists; the run sheet goes to cx and the pretests to creative in the hand-off packs | done |
| 11.6 | Two rules so the new blocks reach the plan: CUST-R33 buyers drift the wrong way (high at 10 or more mentions, low when thin), mapped to the theme's answer; CUST-R34 no mystery shopper run on file (low, a person runs it), mapped to the full run sheet. Bombas: the durability drift joins the durability offer, which now answers 3 findings; the run sheet is a move of its own. 34 rules, 68 actions | done |
| 11.7 | The inbox: "What have other screens asked of us?" lists hand-off rows sent to this screen (or to the brand or customers team) by any other screen, newest first, with who sent it, the kind, the date and check date, the why, "Open the draft", and the decision row logged against the hand-off's id. Read only: this screen never edits another screen's row. Empty today; browser-tested with a seeded row in a temp folder | done |
| 11.8 | `HANDOFF.md` brought up to round 11: 34 rules; how sending, the inbox, decisions by brand and "Fill this block" work; how drift and the shopper run sheet are made; the 3 new contract asks with the exact change when each lands; the open list narrowed to our own assets' drift and shopper results | done |
| 11.9 | The new blocks at phone width and in the report: both fit at 360 px on the Brand tab (the browser test covers every tab for both brands); the monthly report now names buyers drifting the wrong way under brand risks ("durability complaints went from 5 to 13 percent in 180 days (thin)") and the missing shopper run and pretest under what we do not know | done |
| 11.10 | Round 11 close: 34 rules, 68 actions; hand-offs on the shared table both ways; every block ends in an action for both brands; the two open room questions now partial. The shopper table's brain-fact column trimmed so it fits the card. Full screen suite: only the known site speed failures. Screenshot `round11.png` (the shopper run sheet and the message pretests) | done |

## Round 12: what came back, results, and the watch on what is ours (from 28 Sep 2026)

| # | Feature | Status |
|---|---|---|
| 12.1 | What the teams did with our hand-offs: rows are append-only, so a receiving team's choice lives in the decisions log against the hand-off's id. Each pack's line now says how many sent briefs the team answered and how ("1 answered by the team: 1 agent does it, last on 26 Sep"), or that none is answered yet. Browser-tested with a seeded answer in a temp folder | done |
| 12.2 | Shopper run and pretest results read back from a `shopper_runs` table when the data layer has one, else `fixtures/shopper_runs/<brand>.json`. The latest run marks each checkpoint passed or failed. A fail becomes rule CUST-R35 (high) with a drafted fix by step, a page section for a page step, an email for the order email, a ticket for checkout, support or returns. CUST-R34 resolves while a run is under 90 days old and fires again after. A pretest the buyers' line wins with 3 of 5 votes or more becomes "Lead with it", a copy move with its stop rule. Bombas: no results yet, so nothing changes; tested on a temp fixture both ways. 35 rules | done |
| 12.3 | Scan one of our own assets: what the brain already captured of our site (distinct pages on our own hosts and the statements read from them), our ads (the Ad Library read of our page) and our email (none), with dates, shown in the drift block as the baseline the next quarterly scan compares against. Bombas: 26 pages and 108 statements, 23 live ads, all 28 Sep 2026; email never captured | done |
| 12.4 | Watch what is ours: the lookalike block now opens with what is ours on file (brand name, domains, our Ad Library page, social handles, trademark registrations), each on file or missing, and "Plan the monthly watch": a person-owned watch of our name in the Ad Library inside the weekly cap, close domain spellings and unknown marketplace sellers, with what to add to the brain first. Bombas: 3 of 5 on file; handles and trademarks are not in the brain | done |
| 12.5 | Third depth pass on rounds 11 and 12. The new blocks (drift, shopper, inbox) already pass the writing sweep, the rule and gap lines, the empty brand, phone width and the no-action browser check. One gap was found: the result moves (a shopper fix, a pretest lead) change a page or copy but had no size. They now carry one ("1 of 8 checkpoints failed on the 20 Sep run", "4 of 5 buyers chose their words") with their stop rule and check date, tested through `rank` | done |
| 12.6 | Pretests into the experiment registry shape, so an approved pretest is a proposed test | todo |
| 12.7 | HANDOFF.md and the API docstring brought up to round 12 | todo |
| 12.8 to 12.10 | Picked after 12.7; close with round12.png | todo |

### Round 11 founder note (28 Sep 2026)

1. Briefs now reach the other teams for real. "Send" puts each brief on the shared hand-off list once, with its stop rule and check date.
2. What other screens ask of us now shows in one inbox, each with its draft and your choice.
3. Every block now ends in a move. When a block has no data, it offers the move that gets the data.
4. Buyers now complain more about durability: 5 to 13 percent of bad reviews in the last half-year. The sample is thin, so it is a watch. It joins the durability offer.
5. A mystery shopper run sheet checks 8 steps of a real order against what the brain says. 3 message pretests put our line against the buyers' own words.
6. Next, round 12: the results tables for the shopper run and pretests when they land, and a dated scan of our own site, ads and email.

### Round 10 founder note (28 Sep 2026)

1. The 10 rounds are done. This screen tells you who buys, what stops them, and what to build next, and every move says who does it.
2. Every rule you see is written from one list of numbers in code. You can change 12 of them from the brand brain, like when an avatar counts as price-led.
3. It works for any brand. A brand with nothing gets its first move: find the first avatars, 5 quotes each from 2 sources.
4. Every chart says which decision it changes, and every button does something.
5. `HANDOFF.md` says how each number is made, and what to change when the survey, order paths, returns and pack price data land.
6. Still open: brand drift over time, mystery shopper runs, and trademark watch. Each needs data that does not exist yet.

### Round 9 founder note (28 Sep 2026)

1. The screen now checks itself on every run. Every sentence passes the writing rules, and every number in a finding is backed in its evidence.
2. The page loads in a quarter of a second, down from 0.6. It fits a phone and shows your top 3 moves without scrolling, for any brand.
3. No button does nothing any more. "Keep" and "Nothing to do" now say why the row needs no move.
4. Each avatar page now lists what you decided on its moves, with dates and when a "Not now" comes back.
5. Survey answers will set avatar shares once 385 are in. Until the survey runs, shares come from reviews, or from sales where reviews give none.
6. Next, round 10: a last pass on depth, the data layer's order, ticket and survey tables if they land, and a hand-off note for Kevin.

### Round 8 founder note (28 Sep 2026)

1. January is the season, not a new problem. Returning orders fell 42.5 percent into January, against 44.2 percent the year before. The $5.8 million from round 7 is no longer claimed as money at stake.
2. So this screen prices one move: $63,664 per cohort, for the fall after month 6. None of our moves is in your top 10 now, because nothing else is off against its own past.
3. 4 more avatars are now ranked, using their share of sales. The In-Store Single Pair Trier comes in third, at 18.2 percent of sales.
4. One survey question now settles 8 avatars where reviews and sales disagree. The survey closes 23 gaps in all.
5. Every move on the page has a stop rule and a check date, and 99 of 108 have a size. The page works for any brand, and a browser test checks both brands on every run.
6. Next, round 9: order, ticket and return data as the data layer lands, so more moves can be priced.

### Round 7 founder note (28 Sep 2026)

1. Your first priced move from this screen: the January drop cost about $5.8 million against a normal month. The plan to bring past buyers back in January is number 5 on your master top 10.
2. That figure may be partly the season. Last January sits outside the data, and the page says so next to the number.
3. Every move that spends money or changes a page now shows its size, a stop rule and a check date. "Not now" shows its date and the day the move comes back.
4. Reviews and sales disagree on who buys. The Everyday Comfort Seeker is 13 percent of reviews but 3.6 percent of sales. 4 avatars get a share for the first time, from sales. Each gap has a survey question ready.
5. Each avatar has one page to hand a creator or an agency, and it prints clean. Every block says what it reads, its gap and its caveat. Keys j and k move through the plan.
6. Next, round 8: real order and ticket data when the data layer lands, and money on more rules where our own history allows.

### Round 6 founder note (28 Sep 2026)

1. The screen now works for any brand: a second, sparse brain renders every route with honest unavailable states and no Bombas facts in code.
2. Findings that ask for the same draft are one action now, so you approve the durability offer once for 2 findings; 59 actions in all.
3. "Monthly report" gives you one page in plain words: 3 moves to approve, who to build for, what stops them, and what is due in 30 days. Copy or print it.
4. What is due is on one list: 2 seasonal answers are late, winter ads by 25 Oct, 11 avatar records re-checked by 28 Oct.
5. Compare any 2 avatars on 14 rows, open any ladder rung for its reviews, and see what changed since your last visit. The page works at phone width and loads in 0.013 s once built.
6. None of our moves reach your top 10 yet: 30 percent of returning orders come through paid ads, but that is flat against our own year, so no money is claimed. Order and ticket data would price the rest.

### Round 5 founder note (28 Sep 2026)

1. The screen now checks itself against the depth rules on every test run: no brand facts in page code, plain words, numbers on every finding, unavailable never zero.
2. The Daily Compression Wearer sends the most back (1.68x the median avatar), driven by compression that is hard to pull on; a fit line and a day 2 email are drafted.
3. Support has a drafted reply for 16 doubts, 11 ready from proof and 5 to check against a policy, in a pack for the CX screen.
4. Three avatars speak mostly on Amazon and three are price-led; one pair pays 61 percent on top in shipping, so the pack picker brief leads with the free shipping line.
5. Every avatar card now says its build rank, ad voice, return risk and what we do not know yet; every coverage cell shows the doubts behind it; thin reads are flagged with a pull plan to approve.
6. Next, round 6: pack prices, ticket reasons and customer paths as the data layer lands, and a printable monthly customer report for the founder.

### Round 4 founder note (28 Sep 2026)

1. You can now read the screen in one pass: the plan, then the actions, tests and hand-offs, then a desk in 5 tabs by job; the plan filters by job too.
2. The Avatars tab opens on one call: build for the Durability Disappointed Repeat Customer next (score 89), then the Guarantee Reassured Loyalist (85).
3. Our live ads mostly speak to comfort: 10 of 23 ads, for 13 percent of buyers; 6 avatars holding 80 percent of buyers hear none. Each gets an ad brief.
4. Parent Buying For Kids is two buyers, calf socks and slippers, with different complaints; the split is drafted.
5. Five tests are proposed in the experiment registry shape, and each reading screen (creative, copy, landing pages, email) has a ready pack. An ad naming convention lets the ads column fill once ads are tagged.
6. Next, round 5: whatever Kevin or the lead flags from rounds 1 to 4; otherwise the Contract asks as they land and deeper checks on returns and tickets by avatar.

### Round 3 founder note (28 Sep 2026)

1. You can now see a lookalike page running 54 ads that send buyers to sockscool.com; the report, support macro and social note are drafted for a person to send.
2. The calf sock "stay-up" and heel claim meets 12 one and two star reviews about sliding down; a proof-or-narrow fix is ready to approve.
3. Only 25 percent of the words buyers praise us with are in our positioning; a messaging hierarchy (lead on comfort, 3 proof points, answer holes first) is one click from approved.
4. 21 of 23 live ads push a discount that answers none of the buyers' doubts; a guarantee-led A/B test is drafted.
5. Price and value complaints peak Oct to Dec; the seasonal answer is due now. Any line can be checked against our voice before it ships, and each avatar has a one-pager for creators.
6. Next, round 4: the Contract asks (customer_paths aggregate, ad angle tags, situations record) and deeper cross-screen hand-offs to offers, copy and CX.

### Round 2 founder note (28 Sep 2026)

1. You can now see which review themes cost stars (price and value, delivery, durability) and which earn them (comfort), each tied to its fix.
2. Buyers praise us with words our own pages never use: soft, slip, wash, worth, durable. One click drafts page bullets and ad lines from them.
3. A hook bank of lines buyers repeat (stay in place, don't slip, worth the price) turns picked hooks into an ad brief.
4. A gate says no avatar is bet-ready yet: each holds 3 to 4 quotes. The five-question post-purchase survey closes 15 of those gaps in under a day of orders.
5. Winter ads for the wool avatar need to be live by 25 Oct and holiday gifting by 10 Nov; both plans are drafted. Hiking can be added as a provisional avatar in one click.
6. Next, round 3: the customer paths aggregate from the lead (gateway products, win-back day), review sources beyond the sample, and live-page checks for the copy gap.

### Round 1 founder note (28 Sep 2026)

1. You can now open Customers and avatars and see the 10 next moves first, each with an owner, steps and a drafted artefact to approve.
2. Top move: compression fails the Daily Compression Wearer on the job itself (17.3 percent 1 and 2 star, 2.24x the median line). A fit block for the page is drafted.
3. Every avatar card ends in its next build; red cells in the avatar by channel matrix and every ladder rung open a drafted brief.
4. Their own words sit on each doubt; tick lines and "Use in brief" makes a copy brief. Reddit lines stay language only.
5. Cohorts name the January cliff and the month-6 break, and the mix shows 29.9 percent of returning orders come back through paid ads; each has a move.
6. Next, round 2: rules from the web pass (gateway product, second-order path, win-back timing by gap, RFM cells, theme impact, copy gap check) and hiking as a sized avatar.

## Contract asks

Each ask has a local fallback, so the screen works today. `HANDOFF.md` says what to change when each lands.

- A `shopper_runs` table (run id, checkpoint, pass or fail, note, date) and a `pretests` table (avatar, line A, line B, choices, date), so 11.5 reads results instead of marking them on the sheet.
- The kit's decision row (`web/ui-kit.js`) to send `brand` when a screen passes one, now that decisions take it. Until then a decision made on `?brand=example` is logged as the default brand's.
- A `brand` field on hand-off rows (as decisions now have). 11.1 sends only for the default brand until then; another brand copies the pack.
- A `survey_answers` table in the data layer (the post-purchase survey tool, read-only): per question, answer counts by option and the window. 9.4 reads it by that name, falls back to `fixtures/survey_answers/<brand>.json`, and shows unavailable until either exists.
- A `last_year` value for `baseline_kind` in `audit.md` (same period a year earlier). 8.2 uses it for the January cliff and writes `threshold` until the contract has it.
- Pack prices in the brain offers (price per pack size and line), so 5.9 can show the per-pair price at each pack. Fallback: unavailable, with the free shipping facts.
- A tickets and returns aggregate by reason and product line (monthly), so 5.2 reads real return reasons per avatar. Fallback: the review-complaint proxy and a connect card.
- A SKU to product-line map in the brain's products section (for example BMB-SK-CMP-3 to compression), so avatar value can read revenue by line from `products_monthly`. Fallback: 4.9 scores avatars without revenue; from 7.8, `fixtures/sku_lines/<brand>.json` maps SKU style codes to lines locally, and unmapped sales are counted as unmapped. Retire the fixture when the data layer carries the map.
- A `customer_paths` aggregate from `generate.py` (first product repeat and next product, order gaps, RFM cells; shape in `builds.PATHS_SHAPE`). Fallback: 2.9 shows the rules and unavailable.
- A `situations` brain record per category (buying situations as word patterns), so 1.8 reads them from the brain instead of the category-level constant in `builds.py`. Fallback: the constant.
- An `avatar` entity type in `audit.md` (round 0 note). Fallback: type `brand` with the avatar key.
- An angle and avatar tag per ad in `ad_rows`, so coverage in ads can be counted (CUST-R03). Fallback: unavailable finding.

## Room jobs (room "Brand and customers", agent BRAND)

| Job | Question | Capabilities |
|---|---|---|
| know who really buys and why, with evidence | who is my customer and what job did they hire us for | BRAND-C01, BRAND-C02, BRAND-C03, BRAND-C04, BRAND-C08, BRAND-C09, BRAND-C10, BRAND-C11 |
| reuse customers' own words in copy and creative instead of guessing | what exact words do our customers use for this | BRAND-C14, CREA-C03 |
| split one avatar into separate records when the job changes | is this really one customer or three | BRAND-C12 |
| pair every named objection with the real thing that removed it | what actually gets someone past this objection | BRAND-C13 |
| confirm what research found at wider scale | does this hold up outside the sample we already read | BRAND-C05, BRAND-C06 |
| find an untapped avatar when the category feels saturated | is there a customer nobody else is claiming | BRAND-C16 |
| keep the voice sheet current and check assets against it before they ship | does this sound like us, and is every claim in it safe | BRAND-C32, LOOP-C12, BRN-C03 |
| walk the live site, ads and email against the guidelines on a cadence | where has the brand drifted since last quarter | BRAND-C37 |
| track the brand's health line separate from any one campaign | is the brand getting stronger or weaker | BRAND-C48 |
| keep the founder-facing brand brain current | what does the brand stand for right now, in one place | BRAND-C15, LOOP-C11 |
| check what we say we are against what customers actually say | do customers describe us the way we describe ourselves | BRAND-C59 |
| run automated checks on the brand's own journey and messaging before spending | would a real shopper get stuck, and does this message land | BRAND-C67, BRAND-C66 |
| watch for trademark, domain and handle risk | is anyone about to take something that is ours | MONEY-C48 |
| keep every page and channel leading with the same one idea | what is the one message this page or email should lead with | BRAND-C33 |

The job to be done for each avatar is brand data: it lives in `app/brain/<brand>/avatars.json` (`value.job`) and shows on the avatar cards, not here.

## The room's questions after 10 rounds

| Question | Status | Where |
|---|---|---|
| who is my customer and what job did they hire us for | built | avatar cards 0.4 and 5.8, gate 3.x, focus 4.9, avatar page 7.6 |
| what exact words do our customers use for this | built | language bank 0.6, words per doubt, hooks, copy gap, voice check |
| is this really one customer or three | built | split 4.8, compare 6.4 |
| what actually gets someone past this objection | built | ladders with rung evidence 6.5, offer map, support replies 5.3 |
| does this hold up outside the sample we already read | partial | strength of each read 5.7, sales against reviews 7.8, survey answers 9.4 wait on a survey table |
| is there a customer nobody else is claiming | built | served map and segments 1.8 |
| does this sound like us, and is every claim in it safe | built | voice sheet and line check, claims under fire |
| where has the brand drifted since last quarter | partial | drift in what buyers say from dated reviews (11.4); our own assets wait on a quarterly scan, drafted |
| is the brand getting stronger or weaker | partial | brand health from store data; branded search, mentions and review stars wait on connectors |
| what does the brand stand for right now, in one place | partial | messaging hierarchy here; the brand brain screen owns the rest |
| do customers describe us the way we describe ourselves | built | perception gap |
| would a real shopper get stuck, and does this message land | partial | run sheet and pretests drafted from the brain (11.5); results wait on a runs table |
| is anyone about to take something that is ours | partial | lookalike pages, what is ours on file and a drafted monthly watch (12.4); handles and trademarks wait on brain records |
| what is the one message this page or email should lead with | built | messaging hierarchy with approve |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- who is my customer and what job did they hire us for  (BRAND-C01, BRAND-C02, BRAND-C03, BRAND-C04, BRAND-C08, BRAND-C09, BRAND-C10, BRAND-C11)
- what exact words do our customers use for this  (BRAND-C14, CREA-C03)
- is this really one customer or three  (BRAND-C12)
- what actually gets someone past this objection  (BRAND-C13)
- does this hold up outside the sample we already read  (BRAND-C05, BRAND-C06)
- is there a customer nobody else is claiming  (BRAND-C16)
- does this sound like us, and is every claim in it safe  (BRAND-C32, LOOP-C12, BRN-C03)
- where has the brand drifted since last quarter  (BRAND-C37)
- is the brand getting stronger or weaker  (BRAND-C48)
- what does the brand stand for right now, in one place  (BRAND-C15, LOOP-C11)
- do customers describe us the way we describe ourselves  (BRAND-C59)
- would a real shopper get stuck, and does this message land  (BRAND-C67, BRAND-C66)
- is anyone about to take something that is ours  (MONEY-C48)
- what is the one message this page or email should lead with  (BRAND-C33)

### Metrics specified

- `avatar_coverage`: Share of last 90 days' revenue tied to a gated, complete avatar record. revenue from orders matched to a primary or segmented avatar / total revenue
- `avatar_evidence_count`: How many independent quotes back each avatar's job statement. count of distinct sourced quotes per avatar record
- `avatar_freshness_days`: Days since this avatar was last re-checked against real orders and reviews. today minus last audit date
- `language_bank_size`: Exact customer phrases on file per avatar. count of tracked phrases per avatar, deduplicated
- `language_bank_reuse_rate`: Share of live ad, page and email lines that trace back to a banked customer phrase. lines matched to a bank phrase / total scored lines
- `voice_compliance_score`: Share of live assets that pass the voice sheet check. assets passing / assets scanned, across site, ads and email
- `voice_drift_flags`: New drift issues found this audit that were not flagged last time. count of new rule violations this run
- `claims_risk_count`: Claims waiting on evidence or legal review before they can ship. count of claims in the registry without a passed evidence tier
- `branded_search_index`: How often people search for the brand by name, indexed to a base month. branded query volume / volume in the base month, times 100
- `mention_volume`: Public mentions of the brand across tracked sources. count of mentions per period
- `mention_sentiment_net`: Share of mentions reading positive minus share reading negative. (positive mentions minus negative mentions) / total mentions
- `repeat_purchase_rate`: Share of customers in the window who bought again. customers with 2 or more orders / customers with 1 or more orders
- `review_rating_trend`: Average star rating over time. mean rating per period, all verified reviews
- `objection_coverage`: Share of named objections that have a proven remover attached. objections with a paired remover / total named objections
- `mystery_shopper_pass_rate`: Share of journey checkpoints that passed on the last run. checkpoints passed / checkpoints tested
- `trademark_watch_alerts`: Open alerts on the brand's own marks, domains or handles. count of open alerts (renewal due, lookalike registration)
- `messaging_hierarchy_adoption`: Share of live page and channel types that lead with the current top message. page or channel instances matching the current hierarchy top line / total scanned
- `perception_gap_score`: How closely customer language matches the positioning statement. share of top review and mention terms that also appear in the positioning statement and voice sheet

### Insights specified (rules in code)

- avatar gone stale: avatar_freshness_days over 90 for the primary avatar → "The primary avatar has not been re-checked in {n} days. Confirm it still holds before the next brief." (action BRAND-C15)
- new objection not yet mapped: a phrase cluster appears in 5 or more reviews or tickets in a period and matches no entry in the objection map → "{n} customers raised '{phrase}' this month. It has no listed remover yet." (action BRAND-C13)
- voice drift on a live asset: an asset scanned this audit fails a voice rule it passed last audit → "{asset} now breaks the voice sheet on {rule}. It passed last time." (action BRAND-C37)
- unverified claim about to ship: a claim tagged for a live page or ad has no passed evidence tier → "'{claim}' is scheduled to go live with no evidence on file." (action BRN-C03)
- branded search falling at flat spend: branded_search_index drops more than 15 percent over 8 weeks while paid spend is flat or up → "Branded search fell {pct} percent over 8 weeks while spend held steady." (action BRAND-C48)
- sentiment turned amid a mention spike: mention_volume rises more than 2x the trailing average and mention_sentiment_net turns negative in the same week → "Mentions jumped {x}x this week and sentiment went negative. This may need a holding statement." (action BRAND-C54)
- repeat rate falling for the primary avatar: repeat_purchase_rate for the primary avatar's segment drops more than 5 points quarter over quarter → "Repeat purchase among {avatar} fell {pts} points this quarter." (action BRAND-C48)
- banked phrase never used: a phrase logged 10 or more times in the language bank appears in zero live assets → "Customers say '{phrase}' often, but it is in none of our live copy." (action BRAND-C14)
- trademark or handle risk: a renewal falls due within 60 days, or a new registration matches the brand name closely → "{item} needs attention: {reason}." (action MONEY-C48)
- mystery shopper found a broken step: a journey checkpoint fails on the latest run that passed on the prior run → "The {step} step of the buying journey failed on the latest check." (action BRAND-C67)
- AI persona pretest flagged a miss: a persona pretest scores a message or name below the pass threshold set for that test → "'{concept}' scored low with the {persona} persona before any real spend." (action BRAND-C66)
- perception gap widening: perception_gap_score drops more than 10 points quarter over quarter → "What customers say about us now matches our positioning statement {pct} percent less than last quarter." (action BRAND-C59)

### Visuals specified

- avatar evidence board (card grid, one card per avatar): job statement, 5W profile, quote count, freshness, provisional flag
- language bank frequency chart (horizontal bar list): top phrases by mention count, tagged used or unused in live copy
- voice compliance heatmap (heatmap, channel by period): pass or fail per audit for site, ads and email over time
- brand health trend lines (4 small line charts): branded search, mention volume, net sentiment and repeat rate over time
- objection to remover table (paired table): each named objection next to its proven remover and coverage flag
- mystery shopper journey funnel (step funnel with pass or fail marks): browse, cart, checkout, confirmation, support reply, each marked pass or fail on the latest run

### Not in the usual tools

- the avatar record gates every field against a completeness checklist and marks itself provisional until a pattern shows across independent sources
- the language bank tracks reuse rate of real customer phrases in live copy, not just a tone score on a draft
- the consistency audit walks the live site, live ads and live email together on one cadence with one rule set
- brand health here joins branded search, mentions, sentiment and repeat purchase from the brand's own store data into one line
- the perception gap check compares the positioning statement word for word against the brand's own reviews and support tickets
- the mystery shopper audit runs the brand's own live journey end to end, including a real support query, on demand and repeatably
- objection pairing here is the real thing that removed the objection for a real customer, tied to a support macro

### Data this screen needs

- `avatar_records`: brand, avatar_id, tier, job_statement, 5w_profile, quote_ids, status, primary_flag, last_audit_date (BRAND-C09 through BRAND-C11, BRAND-C15)
- `language_bank`: brand, avatar_id, phrase, source_type, source_id, first_seen, repeat_count, used_in_live_copy (BRAND-C14)
- `reviews_raw`: brand, review_id, star_rating, text, date, product_id (store review export, BRAND-C01)
- `support_tickets_raw`: brand, ticket_id, channel (email, sms, call; whatsapp where used, markets: IN, EU, LATAM), reason_code, return_or_failed_delivery_flag (return_to_sender_rate for US, rto_flag for India orders markets: IN), text, date (helpdesk export, BRAND-C02)
- `onsite_search_and_behavior`: brand, query, result_count, converted_flag, session_id, date (site search log, BRAND-C04)
- `objection_map`: brand, objection, remover, source_id, coverage_flag (BRAND-C13)
- `voice_sheet`: brand, version, liked_examples, disliked_examples, rules, approved_date (BRAND-C32)
- `claims_registry`: brand, claim_id, claim_text, evidence_tier, status, target_asset (BRAND-C22, BRAND-C38)
- `brand_consistency_audits`: brand, audit_id, channel, asset_id, rule, pass_fail, date (BRAND-C37)
- `brand_health`: brand, period, branded_search_index, mention_volume, mention_sentiment_net, repeat_purchase_rate, review_rating_avg (search console or SEO tool, mention listening feed, store order history, BRAND-C48)
- `mystery_shopper_runs`: brand, run_id, step, pass_fail, note, date (BRAND-C67)
- `ai_persona_pretests`: brand, test_id, concept, persona, score, date (BRAND-C66)
- `trademark_domain_watch`: brand, item, type (mark, domain, handle), renewal_date, alert_reason (BRAND-C69)
- `messaging_hierarchy`: brand, page_or_channel_type, top_message, supporting_points, approved_date (BRAND-C33)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | skeleton, 0.1 to 0.8 | 28 Sep 2026 | Bombas brain plus simulated cohorts; screenshot `round0.png` |
| 1 | 1.1 to 1.10, no picks (depth brief) | 28 Sep 2026 | done; screenshot `round1.png` |
| 2 | 2.1 to 2.10, from the web pass | 28 Sep 2026 | done; screenshot `round2.png` |
| 3 | 3.1 to 3.10, the brand side of the room | 28 Sep 2026 | done; screenshot `round3.png` |
| 4 | 4.1 to 4.10, one desk, hand-offs, remaining jobs | 28 Sep 2026 | done; screenshot `round4.png` |
| 5 | 5.1 to 5.10, returns, support and depth per cell | 28 Sep 2026 | done; screenshot `round5.png` |
| 6 | 6.1 to 6.10, any brand, one action per draft, agenda, compare, report, speed, phone width | 28 Sep 2026 | done; screenshot `round6.png` |
| 7 | 7.1 to 7.10, depth rules 5, 9, 10 and 14 on this screen, money on retention, sales against reviews, avatar pages, keys, print | 28 Sep 2026 | done; screenshot `round7.png` |
| 8 | 8.1 to 8.10, desk moves sized, January against last year, sales in the scores, survey settles, browser smoke test, weak cohorts, any brand on the page, money tile | 28 Sep 2026 | done; screenshot `round8.png` |
| 9 | 9.1 to 9.10, first screen, writing rules everywhere, decisions per avatar, survey answers back, faster overview, depth rules 4, 6 and 13 as tests, phone width | 28 Sep 2026 | done; screenshot `round9.png` |
| 10 | 10.1 to 10.10, no thresholds in page code, a brand with nothing, anti-patterns and depth sections under test, tunable thresholds, connect strip, charts that decide, loose ends, hand-off | 28 Sep 2026 | done; screenshot `round10.png` |
| 11 | 11.1 to 11.10, hand-offs on the shared table, inbox, decisions by brand, every block acts, buyer drift, shopper run and pretests, 2 rules, report | 28 Sep 2026 | done; screenshot `round11.png` |
