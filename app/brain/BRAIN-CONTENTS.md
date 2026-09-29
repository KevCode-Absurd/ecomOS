# What the brand brain contains

Written 29 Sep 2026. Designed from the output side: what would the best person in each job need to know about this brand, beyond the numbers, to do their best work on day one? Everything below exists so that the screens and agents downstream can produce work a founder or agency owner would ship without rewriting it.

## Two layers, one rule

**The data layer** is raw and automatic: orders, sessions, ad rows, email events, tickets, reviews, rankings, stock, payouts. Connectors refresh it. Nobody edits it. Agents query it for numbers.

**The brand brain** is everything about the brand that is not a raw table: judged, tagged, annotated and founder-signed. It points at data rows; it does not copy them. It holds the things a new hire would spend three months learning.

The rule: if a connector can refresh it untouched, it lives in the data layer. If a person had to decide, tag, judge or approve it, it lives in the brain.

## Start from the outputs

| Output | What the best operator needs that no metric gives | Brain shelves that supply it |
|---|---|---|
| Ad copy | the angles that have won and lost, the exact customer words, the proof behind every claim, the banned claims, the voice with liked and disliked examples, the offer rules, the product facts | messaging, customers, claims, voice, ads, offers, products |
| Ad creative | every ad already run with its result, formats and hooks that fatigued, product photos with rights, UGC with rights, competitor formats as reference only, brand assets, the avatar each ad speaks to | ads, assets, creators, competitors, customers, brand kit |
| Paid media plans | winners and losers by angle and audience, seasonality per market, stock cover per SKU, margin floor and CAC ceiling, budget caps, what was tried and why it stopped | ads, history, calendar, operations, finance, goals |
| Landing pages and CRO | every page today with its template and purpose, what each page is for and how it performs, the objection ladder per avatar, proof per product, the funnel map, past tests, speed and tracking audits | site, customers, claims, products, history, audits |
| Email and SMS | every flow and message today with copy and results, list segments, the tone in emails specifically, offers allowed per segment, product launches ahead, deliverability facts | email, offers, calendar, voice, products, customers |
| SEO and content | the keyword universe with intent, content inventory and gaps, the brand's own facts page, competitors' pages, the questions buyers ask, internal linking map, technical audit | seo, site, customers, competitors, audits |
| Answer engines | a single facts page the brand signs, product specs, policies, claims allowed, what assistants currently say | claims, products, policies, seo |
| Creators and affiliates | who was paid, what it cost, what they produced, rights held, who the audience trusts, do-not-work-with list, the brief that worked | creators, assets, customers, history |
| Organic content | content pillars, posts with results, brand kit, founder's willingness to be on camera, the calendar, the stories that land | content, brand kit, voice, calendar, story bank |
| Offers and pricing | landed cost and margin per SKU, the discount rules and red lines, every offer run with results, competitor price bands, shipping threshold logic, guarantee terms | finance, offers, competitors, products, goals |
| Product and research | what the category rewards, what customers use products for, review themes per product, the roadmap, supply limits, marketplace listings and gaps | market, customers, products, operations, competitors |
| Customer service and retention | support macros, the doubts ranked, policies, product FAQs, why customers leave, avatars, tone in support | operations, customers, policies, voice, products |
| Marketplaces | listings today with content and price, parity rules, reviews per listing, category rules, which SKUs are allowed there | products, market, offers, operations |
| Finance and reports | unit economics, floors, cash cycle, budgets, unseen revenue, data trust notes, what the founder counts as success | finance, trust, goals |
| Every proposal to the founder | goals, constraints, red lines, decisions already made, who approves what, what failed before | goals, history, team, decisions |

## The shelves

Each shelf is a folder under `app/brain/<brand>/` with an `INDEX.md` a person can read and a structured file agents read. Every item carries source, date, tier (founder, site, data, public, inferred) and rights where media is involved.

### 1. core: `BRAND-BRAIN.md`
The one page every agent loads first. Identity, markets, goals and limits, who we sell to, what we say, what we sell, offers and rules, where we win and lose, what works and fails, channels live today, the numbers to know, trust, team, calendar, open questions. Under 3,000 words. Everything else is a shelf it points to. Founder signs it.

### 2. products
- Catalogue: every SKU with line, price per market, specs, materials or ingredients, sizes, care, what it is for, who it is for, the benefit behind each feature in plain words.
- Proof per product: tests, certifications, awards, review count and rating, top praised and top complained themes.
- FAQ per product from support and reviews, with the answer that works.
- Price history and stock state, with a pointer to the data rows.
- Roadmap: launches, discontinuations, what cannot scale.
- Approved product photos and renders, with rights and which are current.
Refresh: site crawl weekly, founder sign-off on launches.

### 3. customers
- ICP in one paragraph and up to 4 avatars, each with share of orders from data, first product, triggers to buy, doubts, words, where they spend time.
- The voice of customer corpus: reviews, support tickets, DMs, survey answers, call notes, forum threads. Tagged by product, theme, sentiment, avatar. Quotes verbatim with source; forum quotes never used as testimonials.
- Objection ladder: every doubt ranked by sales lost, with the answer, the proof and where the answer lives.
- Language bank: their words for the product, the problem and the result; our words they never use.
- Segments with data pointers: new vs repeat, by market, by first product, by channel.
- Why customers leave, from their own words.
Refresh: corpus weekly from connectors; avatars re-signed quarterly.

### 4. messaging
- Positioning: one line, the win moment, the category frame we claim.
- Value props ranked with proof under each.
- Angles library: every angle with hook examples, the proof it needs, the avatar it fits, the offer it pairs with, its win or loss record from ads and pages.
- Story bank: origin, making-of choices, founder story, customer stories with rights.
- Taglines and lines in use, with where they run.
- Per-market variants where a line changes by country.
Refresh: after every creative round; founder signs positioning.

### 5. claims
- Allowed claims with the proof file for each and where it is used today.
- Forbidden claims with the reason and who set the rule.
- Words never used, visuals never shown.
- Regulatory notes per market: what this category may and may not say there.
- Site claims still waiting for proof.
Refresh: on every founder round; legal review per market yearly.

### 6. voice
- Tone in three words, then the rules: sentence length, person, humour, formality, emoji, capitals.
- Liked examples: 20 pieces the founder would ship as is, across ads, emails, pages, support, with why.
- Disliked examples: 20 pieces the founder rejected, with why.
- Banned words and phrases. Preferred spellings and names.
- Voice per channel: ads, email, support, social, marketplace listings.
- Founder on camera: yes or no, and how much time.
Refresh: the founder rates agent outputs; ratings feed this shelf.

### 7. ads
- Every own ad ever run: creative file, copy, headline, format, placement, dates, audience, the angle and hook tags, status, spend and results as a dated snapshot with a pointer to the data rows, the learning in one line.
- The winner board and the loser board, by angle, hook, format, avatar and product.
- Fatigue notes: what stopped working and when.
- Competitor ads: reference only, image and thumbnail, angle and format tags, run length. Never text, logos, products or faces into generation.
- Live ads today, with what each is for.
Refresh: daily from the ad account; competitor pull weekly.

### 8. site
- Full crawl snapshot: every page, text, HTML, screenshot, template, purpose, the products and offers it carries, dated.
- Page inventory: type, goal, audience, traffic and conversion as dated snapshots with data pointers.
- Landing page library: every landing page built, its goal, audience, offer, structure, result, and whether it is live.
- Funnel map: the paths buyers take, where they drop.
- Site diff: what changed between crawls.
- Templates and components available, so a brief matches what can be built.
Refresh: crawl weekly, diff on every crawl.

### 9. audits
- Speed audit: dated runs per page type, the fix list and who owns it.
- SEO technical audit: crawl health, indexing, structured data, links.
- CRO audit: per page, the findings and the tests they became.
- Tracking audit: pixels, events, consent, gaps and the date each gap started.
- Accessibility and legal disclosures per market.
Refresh: monthly, or after a site change.

### 10. seo
- Keyword universe: every term with intent, volume band, current rank, page that ranks, competitor that ranks, priority.
- Content inventory: every article and guide with its target, rank, traffic, refresh date.
- Topic clusters and gaps.
- Questions buyers ask, from search, support and forums.
- Backlink profile and the sites that link to competitors.
- The facts page: what the brand wants search engines and AI assistants to say.
Refresh: rankings weekly, inventory monthly.

### 11. email
- Flow map: every automated flow with trigger, timing, every message's copy and design, results as dated snapshots.
- Campaign archive: every send with copy, segment, offer, result.
- Segments and list health: size, growth, engagement, deliverability facts.
- Templates in use.
- What the best emails had in common; what was unsubscribed most.
Refresh: from the email platform daily; annotations after each campaign review.

### 12. offers
- Offers live today, with the rule each follows.
- Offer archive: every offer run with structure, dates, economics, results, learning.
- Discount rules: deepest allowed, never-discounted products, when allowed, per market.
- Shipping thresholds, bundles, guarantees, loyalty terms.
- Competitor offers seen, dated.
Refresh: weekly from site and ads; founder signs rules.

### 13. competitors
- Profile per competitor: site crawl, prices, offers, positioning, ad archive, reviews of them, where they win and where they lose, who their buyers are.
- Battlecards: what to say when a shopper compares.
- Substitutes: what buyers do instead of the category.
- Price bands and the map of claims.
- What we refuse to copy, what we wish we had started.
Refresh: weekly crawl and ad pull; battlecards on founder round.

### 14. creators
- Every creator, affiliate and agency paid: who, niche, audience, cost, what they made, results, rights held, use again or not.
- Candidates found, with why.
- UGC library: every customer photo, video and quote with rights status and where used.
- The briefs that worked and the ones that failed.
- Do-not-work-with list with reason.
Refresh: on every campaign; rights checked before every use.

### 15. content and brand kit
- Brand kit: logos, colours, fonts, templates, photo style, do and do not examples.
- Asset library: product photos, lifestyle shots, videos, with rights, date and current or retired.
- Organic posts archive with results and the pillar each belongs to.
- Content pillars and the calendar.
Refresh: assets on every shoot; posts weekly from platforms.

### 16. market
- Category facts: what the category rewards, buying frequency, gifting, who pays and who uses, seasonality per market.
- Regulations per market for this category.
- Marketplace rules and category requirements.
- Price bands and demand signals: search volume by month, trends.
- What an outsider gets wrong, from the founder.
Refresh: quarterly, plus on entering a market.

### 17. operations
- Supply: lead time, minimum order, supplier reliability, which SKUs cannot scale.
- Fulfilment: carriers, delivery days per region, failed delivery causes, cash on delivery share.
- Returns: process, real cost, top causes per product.
- Support: macros, policies, escalation rules, tone.
- Apps and stack, with owner and cost.
Refresh: monthly; founder signs supply limits.

### 18. finance
- Unit economics per SKU: price, landed cost, margin, per market.
- Floors: lowest contribution per order, highest cost per new customer, per first and repeat order.
- Budgets and caps per channel.
- Cash cycle: supplier terms, payout days, the tight months.
- Revenue outside the connected accounts and where it lives.
Refresh: monthly with the founder.

### 19. history
- Experiment registry: every test with hypothesis, setup, dates, result, learning, and the rule it changed.
- What worked and stopped; what failed and why; what must never be repeated.
- Agency and tool history.
- Agent output ratings: every piece the founder rated, with the note, so the next piece is better.
Refresh: on every test read and every founder round.

### 20. decisions and goals
- Goals: the 12 month target, the constraint, what is off the table.
- Decisions log: date, decision, why, who, what it changed.
- Approval rules: who approves what, budget caps, what an agent may do alone.
- Red lines that no proposal crosses.
Refresh: on every founder round.

### 21. trust and access
- Connected accounts with last refresh and health.
- Numbers not to trust, why, since when.
- Who sees what: roles, agency access, what leaves with the brand if the relationship ends.
- Unanswered questions with owner and date.
Refresh: automatic for health; founder round for trust notes.

### 22. calendar
- Peaks and dead zones per market with prep start dates.
- Launches, events, PR moments, stock arrivals.
- What was under-prepared last year.
Refresh: monthly.

### 23. inspiration
- Swipe file: ads, pages, emails and posts from anywhere, tagged by domain, angle, format, and why it is good. Own brand items in full; others as reference only, never into generation.
Refresh: continuous; purge on request per origin brand.

## What each shelf lets downstream do

- ads plus messaging plus claims plus voice: write and design a new ad that does not repeat a loser, uses a hook that has won, carries only allowed claims with proof, and sounds like the brand.
- site plus customers plus products plus history: brief a landing page that fits an existing template, answers the top doubts in order, uses proof per product, and does not retest a settled question.
- email plus offers plus calendar: build a flow that does not duplicate a live message, offers only what the rules allow to that segment, and lands before the peak.
- seo plus site plus competitors: pick the next page to write from a real gap, with the questions buyers ask and the competitor page to beat.
- creators plus assets plus customers: brief a creator who fits the avatar, with the angle, the proof, the rights terms and the brief that worked last time.
- offers plus finance plus competitors: propose an offer that clears the margin floor, respects the red lines and answers the competitor's move.
- goals plus history plus decisions: rank any proposal and stop the ones the founder has already said no to.

## Sizing

A brain for one brand: the core under 3,000 words; the shelves as large as the sources allow. Agents never load a shelf whole. They load the core, then the index of the shelves they need, then the items those indexes point to, inside a token budget per job. The core says which shelves each job reads.
