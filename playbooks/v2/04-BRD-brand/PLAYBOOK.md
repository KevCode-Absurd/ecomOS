# 04-BRD-brand playbook

version: 2.0-draft  |  date: 24 Sep 2026  |  sources: 12 mini playbooks (11 independent voices: 02 and 07 are both Seth Godin)  |  cards: 524  |  built from: sources/*.md

## 0. How to use this playbook

**Ecommerce first.** This playbook is for stores, not for general branding. Section 3.0 is the ranking: it says which lever to work on first, in order, before the detailed rule groups. Store-type conditions (hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy vs DTC-only, considered vs impulse) decide which rules in the groups below actually apply to a given brand.

**Who runs it.** The brand strategy and identity agent. It writes positioning, chooses and screens names, builds the identity system (marks, colour, type, photography, voice, packaging, touchpoints), writes brand guidelines and the brand voice sheet, and audits pages and ads for brand consistency. It hands avatar research to 02-AVT, offer and discount structure to 03-OFF, page layout to 07-LPG, ad creative and hook formats to 10-MCR, ad copy to 11-ADC, organic content mechanics to 13-ORG, post-purchase and unboxing flows to 17-CXP, and team or vendor hiring to 21-OPS.

**What the sources are.** Read section 12 before trusting any number. In short: source 01 is a 2008 neuromarketing book by a consultant who sold neuromarketing services; every brain claim in it is the author's own report of his own commissioned study. Sources 02 and 03 are marketing books (2018 and 1981) whose cases run from the 1960s to the 2010s and never mention ecommerce. Source 04 is one CPG founder on a podcast with 2 sponsor reads. Source 05 is an excerpt of a design textbook (2013) that is missing the process chapters. Sources 06 to 12 are creators and practitioners: a naming agency founder, a Godin interview, a workshop talk that matches Alex Hormozi, one Shopify-sponsored rebrand case study, an agency pitch, a course-funnel mindset talk, and a freelance designer's single project. Several carry affiliate, sponsor or course pitches. Every ecommerce mapping in the mini playbooks (PDP, unboxing, Shopify, search) was added by the card writer or the pass 1 writer; the books never said it. This playbook marks those as "pass 1 adaptation" wherever they appear.

**ecomOS rules that override every source in this folder.**
1. No invented claims. A positioning claim, name story, origin story, spec comparison or "first" or "only" claim goes into a deliverable only if the brand record supports it or a `[web check]` confirms it. Sources 03, 04 and 10 each show or permit a claim the agent must not copy without proof (a "first in" claim, an "only thing under $3 that's luxury" claim, a spec gap the founder admits he does not know). Those lines are marked "reject unless proven" below.
2. Claims match the brand record. Where a source's example claim and the brand record disagree, the brand record wins and the source example is dropped.
3. Brand voice from the brand record wins. Voice rules in this playbook are defaults for a brand with no voice sheet. Once `brands/<brand>/` holds a voice sheet, it overrides section 3 group F and checklist 5.5.
4. Reading level below tenth grade for every client-facing deliverable. Short sentences, simple words, digits, no em dashes. Source 05's "polish and cut" rule and source 09's "no jargon" rule agree; source 03's long aphoristic style does not, and is not a model for output.
5. No copying competitor names, marks, text or products. Competitor material is used for the ladder, the XY map and the category audit only. A "reposition the competitor" ad (source 03) that names a competitor needs a `[web check: legal review of comparative claims in the brand's selling countries]` before it ships.
6. Generated images do not replace real product photos where accuracy matters. Source 09's photography rule (warm grading, film grain) carries its own warning that grading can misrepresent product colour. Packaging, PDP hero and any image where colour, size, texture or fit matters uses the real product photo.
7. Brands stay apart. Gehna, Peach Bucket and TrailFold each get their own positioning, name screens and identity work. Nothing from one brand's record informs another's deliverable.

**Which sections to load for which task.**

| Task | Load |
|---|---|
| Write or review a positioning statement | 3 group A, P1, P2, checklist 5.1, 6, 7 (C1, C11, C12) |
| Map the category and find open space | 3 group A (R3 to R12), P1, P2 |
| Reposition against a leader or a category | 3 group A (R7, R8, R13, R14), P3, 7 (C1) |
| Premium positioning or price-as-signal decision | 3 group B, P4, checklist 5.6, 7 (C5) |
| Write the brand brief (purpose, values, promise, story, enemy) | 3 group C, P5, 9.2 |
| Name a brand, product or line | 3 group D, P6, P7, checklist 5.2, 7 (C2), 11 |
| Decide whether to rename | 3 group E (R84 to R88), P8 |
| Decide house name vs new name for a new product | 3 group E (R76 to R83), P9, 7 (C1) |
| Build or refresh the identity system | 3 group F, P10, P11, checklist 5.3, 7 (C3) |
| Write brand guidelines or a brand book | 3 group F (R106 to R110), P12, checklist 5.4, 9.5 |
| Small brand with no agency, full identity process | P13 (which sequences P5, P6, P10, P12 at small scale) |
| Apply brand psychology (sensory, ritual, mascot, smashable cues) | 3 group G (all marked as claims), P14, 7 (C3) |
| Audience building and content for brand | 3 group H, P15, P16, 7 (C6, C8) |
| Check a PDP or ad for brand consistency | checklist 5.5, 3 group F (R104, R105), 9.6 |
| Decide whether to persist, change or stop | 3 group I, 7 (C4, C9) |
| Write the brand voice sheet for the brand brain | 9.6, P12 step 6, 3 group F (R103 to R105) |
| Any point where sources disagree | 7 |

**What the agent must fetch before acting.** From the brand record: product facts and provable claims, current name and marks, current price points and the category price band, existing customer language (reviews, support, UGC), sales history by SKU, promo history, selling countries, and any existing voice sheet or guidelines. From the data layer: sales by SKU and channel, repeat rate, search terms on site. From the web: trademark and domain availability per finalist name, competitor set for the ladder and XY map, and cultural readings of any symbol or colour for each selling market. Section 10 lists every tag.

## 1. Scope and outcomes

**Covers.** Positioning (the ladder in the prospect's mind, first in mind, cherchez le creneau, repositioning the competition, the against position, the everybody trap, category creation, XY axis maps, smallest viable market, status and affiliation vs dominance). Premium positioning and price as a signal. Brand strategy elements (purpose, values, promise, story, worldview, tension, enemy). Naming (process, types, criteria, sound symbolism, trademark and domain screens, rename decisions). Brand architecture and line extension. The identity system (marks, colour, typography, photography, voice, packaging, touchpoints, guidelines). Brand psychology claims (sensory cues, rituals, mirror neurons, somatic markers, smashable brands), marked as claims. Audience building and content for brand. The identity process for a small brand with no agency.

**Does not cover.** Avatar interviews and survey design (02-AVT). Offer structure, discount depth and guarantees (03-OFF). Page layout and wireframes (07-LPG). Test design and significance (09-CRO). Ad hooks, formats and hook-rate benchmarks (10-MCR). Ad copy (11-ADC). Organic content mechanics, posting cadence and platform tactics (13-ORG). Unboxing flows and retention programs (17-CXP). Retail distribution, margins, MOQ and demand planning: source 04 covers these at length, but they belong in 18-COG and 20-FIN; this playbook keeps only the positioning and packaging parts of 04. Hiring and fundraising (21-OPS, 20-FIN). Crisis communications: source 05 gives a checklist; it is summarised in P12 step 8 and otherwise out of scope.

**Business measures it moves.** Unaided brand recall and correct category association (03, 06). Share of prospects who name the brand in the top rungs of the category ladder (03). Price realised vs category band, and gross margin protected without discounting (04, 10, 02). Repeat rate and cohort retention as a brand-equity signal (10, 01). Branded search volume vs generic (02). Consistency of voice and visuals across touchpoints, measured by audit score (05, 09). None of the sources gives a validated benchmark for any of these; section 6 marks confidence.

**What is timeless and what is case-bound.** Timeless mechanisms the sources agree on and which do not depend on the era: positioning happens in the prospect's mind (03, 02, 05, 09, 12); the mind holds a short ranked list per category (03); first in mind beats better in product (03); find an open slot rather than fight the leader head-on (03, 02, 09); narrow the target (03, 02, 07, 04); the name is the highest-frequency asset (03, 06, 05); a name that means one thing is easier to hold than a name stretched across two (03); strategy before visuals (05, 12, 09); shape reads before colour before words (05); hold a position for years and vary only tactics (03, 02, 07, 11). Case-bound and not to be quoted as current fact: every dollar, share and awareness figure in 03 (1960s to 1980), every fMRI and SST number in 01 (2004 to 2007, small samples, vendor stake), the Uber, USHG and platform cases in 02, the retail margins and SKU thresholds in 04 (one founder, one category), the naming fees and AI adoption figures in 06, the follower and view counts in 07, 08 and 11, and the single-project choices in 09 and 12.

## 2. Inputs the agent needs

| Input | From where | Required or optional | Why |
|---|---|---|---|
| Product facts: what it is, what is provably different, ingredients or materials, origin, specs | Brand record | Required | Every claim in positioning, naming and identity must trace to a fact (override 1). Sources 06 and 04 both start with a product audit |
| Provable claims list and claims the brand may not make | Brand record | Required | Override 1 and 2. Source 04's "only luxury under $3" and 03's "first" claims are examples of claims that need proof |
| Current brand name, marks, colours, type, packaging files | Brand record | Required for identity and rename work | Source 09: audit equity before replacing anything; source 05: identity is the tangible system |
| Existing voice sheet or guidelines | Brand record | Optional; overrides group F if present | Override 3 |
| Customer language: reviews, support tickets, UGC, on-site search terms | Data layer, brand record | Required for positioning, promise and voice | Sources 02, 03, 06, 09 all fill the promise and ladder from customer words, not internal taste; source 01 weights revealed behaviour over stated |
| Unprompted category ladder from real prospects (who they name, in order) | User or 02-AVT research | Required for a positioning program | Source 03's first question; no substitute exists in the sources `[needs brand data: ladder interviews or search-term proxy]` |
| Competitor set: direct competitors and out-of-category alternatives, with their claimed positions | Web | Required | XY map (02, 09) and ladder (03) need every alternative, not just direct rivals `[web check: competitor claims and price points]` |
| Category price band and the brand's price points | Brand record, web | Required for group B | Source 04 prices inside the learned band; 02 and 03 use price as a claim |
| Sales by SKU, repeat rate, cohort retention | Data layer | Required for line extension, hero SKU and premium measurement | Sources 04, 10, 03 (reorder curve after an extension) |
| Promo history (depth, frequency, share of days on promotion) | Data layer | Required for the premium signal audit | Source 10's discount cadence check |
| Selling countries and languages | Brand record | Required for naming and symbols | Sources 05 and 06 test names and symbols per market; 01 warns on numbers and colours per culture |
| Trademark and domain availability per finalist name | Web | Required before any name is presented as a finalist | Sources 05, 06 `[web check: trademark registers and domain registrars per selling country]` |
| Cultural readings of candidate symbols, colours and numbers per market | Web | Required for mark and packaging work | Sources 12 (clover leaf dropped), 05 (black in China), 01 (number 4) `[web check]` |
| Awareness stage split of the audience (unaware vs comparing) | 02-AVT | Optional | Source 10 splits exclusivity triggers by stage |
| Founder's willingness to be the face, and for how long | User | Required for founder-led brands | Source 04: founder as early face, then remove; 10: founder documentaries; 05: personal brand rules |
| Budget and runway for holding the position (money and months) | User | Required | Source 03 questions 4 and 5; source 07's Dip check |
| Which touchpoint decides the purchase (packaging, PDP, ad, menu, interface) | User plus data layer | Required for identity priority | Source 12: put the best execution where the business touches the customer; 05: moments of truth |
| Existing content archive and founder footage | Brand record | Optional | Source 04: document from day one; feeds story and premium creative |

## 3. Decision rules

Every rule states the condition, the mini playbooks that support it (by number), conflicts if any, and card ids. Where only 1 source says it, the rule says "Source N says". Where the pass 1 file added an ecommerce mapping the book never made, the rule says "pass 1 adaptation".

### 3.0 Ecommerce priority order

1. Category rung and the one claim (R3, R4, R7). Hero-SKU brands claim a rung fast; catalogue stores claim it per hero category (R82, R101). `[general practice]` for the split.
2. Price band and premium-vs-value call, before design spend (R29 to R31, R33, C5). High-AOV brands protect price; low-AOV brands can use price as an entry creneau (R8). `[general practice]`
3. Claims register and provable-claims gate (override 1, R48). Before naming or ads, every store type; a false "first" or "only" claim is a legal and marketplace-policy risk.
4. Name and searchability (R57 to R60, R70, R71, C2). Marketplace-heavy stores weight descriptive names higher; a flagship brand with no marketplace listing can risk coined sooner. `[general practice]`
5. PDP and homepage brand consistency (checklist 5.5, R104, R105). Highest-traffic surface for any store; run before ad creative is greenlit.
6. Packaging or unboxing as the decisive touchpoint (R99, R41, R53). Above identity work for a physical product; below the PDP for a digital-only listing. `[general practice]`
7. SKU and line-extension gate (P9, R76 to R82, checklist 5.7). A hero-SKU brand waits until the hero clears its revenue bar (R79); a catalogue brand runs this on every new listing.
8. Promo cadence vs premium position (checklist 5.6, C5). High for a considered-purchase or premium brand; lower where discounting is part of the value story.
9. Founder-as-face decision (C13, R132). High for a founder-led DTC brand in years 1 to 3; drops out with no visible founder.
10. Voice sheet and reading-level compliance (R103, override 4, 9.6). Above full identity work; every piece of copy needs it now and it is cheap.
11. Owned audience and permission asset (R128). Higher for subscription and repeat-purchase brands, since R114's replenishment cues need a channel to land in.
12. Identity system depth: marks, colour, type (R89 to R102). Last; cheapest to iterate later and least likely to move revenue alone. `[general practice]`

Load this block first; the groups below are the detail.

### Group A. Positioning fundamentals

**R1. A PDP headline, price or pack change is a mind-share move; judge it by ladder movement, not a spec sheet.** Condition: any time the brand wants to be remembered inside a category the prospect already has an opinion about. A name, price, package or claim change is a move to secure a slot in the mind; it is not a product change and should not be judged as one. Sources: 03 (the core thesis; Kotler's foreword cases Volvo, Häagen-Dazs, L'eggs, Little Caesars), 02 (a brand is the customer's shorthand for a promise), 05 (brand is the perception held, identity is the tangible system), 09 (brand is the customer's gut feeling), 12 (branding is how the business is perceived). 5 of 12 sources agree; no source disagrees. `[bb615728597c]` `[94ce0d0c21b6]` `[177aa8d4c957]` `[1c1a35e393b7]` `[5a833673f348]` `[c39f9828740f]`

**R2. On a PDP or hero ad, cut to the one line a scrolling mobile shopper reads in 3 seconds; a subhead and at most 2 bullets carry the rest.** Condition: any paid or owned message competing for attention. Source 03 calls this a "selection project": the mind holds about 7 units per category, often 1 or 2 in a low-interest category (citing George Miller). Source 05 agrees with 1 big idea and at most 3 key messages (borrowed from Vincent Covello's risk-communication work). Source 11 agrees ("strip to one idea"). Source 03's dollar figures ($376.62 per capita US ad spend, 12,000 supermarket products) are 1980 data and must not be quoted. `[079c0cc5fa06]` `[d6bb004cc9ea]` `[a5504e4a6a39]` `[9568b3b120a2]`

**R3. Map the category ladder before writing any positioning claim.** Condition: every positioning program. Ask real prospects to name the brands in the category, unprompted, in order. Record who is first, second, third, and who is missing. Your message depends on your rung: a number 2 or lower does not advertise as if it were the leader; an unranked brand needs a new ladder or an against position. Source 03 gives no sample size or survey design. Pass 1 adaptation: on-site search terms and review mentions can stand in as a rough proxy `[needs brand data: unprompted ladder interviews]`. `[d6bb004cc9ea]` `[92e5149e81d9]` `[e247ee27ad80]`

**R4. Check who already claims the slot on the category's Amazon, Flipkart or Google Shopping results before writing a "first" claim.** Condition: entering a category or a new dimension of one. "First" means first to claim the slot in the mind, not first to invent (IBM did not invent the computer; Amerigo Vespucci arrived 5 years after Columbus and named the continent). Source 03 states "second is nowhere" as doctrine; the pass 1 file and this playbook note that many durable number 2 and number 3 brands contradict the absolute form. Use the rule as "claim a slot first", not as "second always loses". Source 02 agrees in softer form (position one step ahead of today so the tribe follows). `[1a89c8f731f5]` `[c548656c431c]` `[2f504f814390]`

**R5. Do not build a PDP or comparison page that repeats the leader's exact promise (free shipping, fastest delivery); pick an angle the leader's listing does not use.** Condition: a category with a recognised leader in the prospect's mind. Source 03's closing first rule, backed by the RCA vs IBM case (a reported $250M loss after RCA declared a "firm number 2" computer position) and the Xerox and IBM cross-attacks that both failed. Source 02 agrees: the status quo resists because of status, not because your idea is wrong. Source 09 agrees in practice: it looked for open space on the map rather than contesting the crowded pool. `[78e52b831776]` `[d68f5389fbe9]` `[24bbaad92a51]` `[84c08bf1872c]`

**R6. Check whether the brand can get there from here before spending.** Condition: any position the mind may refuse to give. A great product, sales force and budget still fail against a slot the mind will not open (RCA in computers). Source 03's prescription: relate to a position you already own (NCR in retail data entry). Source 03 also says outright failure can beat expensive mediocre failure; that is a resource opinion, not a finding. `[d68f5389fbe9]` `[97bafe17846b]`

**R7. If you are not first, take the against position: state your rank relative to the leader instead of claiming to be better.** Condition: an actual recognised leader exists; if none does, there is nothing to be against. Source 03's Avis case (13 years of losses, then reported profits of $1.2M, $2.6M, $5M in 3 years after "We're only number 2, so we try harder"; the authors credit the relation to Hertz, not the "try harder" line) and 7-Up's "uncola". Source 03 also says the against position can be "what we are not" (the "not" frame for a new category). Source 02 states the same mechanism as "we're this, not that" as a service to the right customer. `[4f50a6f783d7]` `[078eeee4243e]` `[0d6ad2f3cdfc]` `[ff2d9fce9f88]` `[6c5720ed9b21]` `[de650f79961f]`

**R8. Cherchez le creneau: find the hole in the mind, not the hole in your product line.** Condition: a follower brand that cannot be first in the category. Source 03's named creneau types: size (Volkswagen "Think small"), high price (Michelob; see R29), low price (works for unproven new products where the buyer takes a chance; weak where retailers already trained shoppers to expect discounts), gender, age (Aim toothpaste reached about 10% share against Crest and Colgate), time of day (NyQuil gave up the daytime market to own night), distribution (L'eggs in supermarkets), heavy-user framing (Schaefer). Timing rule: being first on a dimension works; copying a dimension someone owns fails (Luke, Eve). Source 04 agrees with a modern example: over-deliver on one measurable spec (500 mg sodium vs a competitor range he admits he does not know) and hold the line while buyer education catches up. The spec-gap claim is "reject unless proven" under override 1. `[7cbf151d9951]` `[7f129dfe890c]` `[6eae715aafa4]` `[a7054e16df6c]` `[32a728894b48]` `[8d0d1d8f914c]`

**R9. A factory creneau is not a mind creneau.** Condition: any new SKU proposed to "fill a gap in the range". Source 03: Edsel filled a gap between Mercury and Lincoln in Ford's line and had no slot in the buyer's mind; Frost 8/80 was the first dry white whisky and died within 2 years at a third of forecast volume because gin, vodka, rum and tequila already held the slot. Source 04 agrees from the other direction: gate every new SKU on an anchor customer and size of prize before production (see R79). `[47ce0c7f290e]` `[e175eacb2b24]`

**R10. A homepage written for every buyer (gift shopper, self-purchaser, wholesale) dilutes conversion; name the primary shopper in the hero and route the rest to a secondary collection.** Condition: any brand building a position rather than defending an already dominant one. Source 03 (Rheingold's ads showing every ethnic group alienated all of them; positioning requires "sacrifice"). Source 02 (smallest viable market; "it's not for you" said out loud; 12% of Harry Potter's 21,000 Amazon reviews were 1 or 2 stars, and that is normal). Source 07 (the smallest viable market has 2 bounds; too narrow cannot sustain a business, too broad is a commodity). Source 04 (state who the product is not for and use the concession as a trust signal; entered running before anything broader). Source 11 (go deep, not wide). 5 sources agree. Conflict C12: 03 also warns a position can be too narrow (Rolls-Royce at about 0.01% of the US market); see section 7. `[32142fdf5893]` `[8bc6ea16e3c6]` `[cdc515a379b0]` `[f97dfa662068]` `[e2ffdd118cf5]` `[0bc28a1a4edf]` `[1956336eab48]` `[6e16b5cd6b2a]`

**R11. Size the target by how many repeat buyers at the store's AOV and margin sustain the business; a hero-SKU brand may need only a few thousand.** Condition: initial target choice for any launch or reposition; source 02 says this precedes and outranks positioning against competitors. Choose the minimum number of people you can delight and still make the business worthwhile, then serve them obsessively (Union Square Cafe curated its 600 daily seats; Kevin Kelly's 1,000 true fans sustain "a decent living, not a fortune"). Segment by the story people tell themselves (Lakoff's worldview), not age or income; JCPenney's 2011 CEO cut coupons on his own worldview and sales fell more than 50%. Source 12 and 09 agree (psychographics; personas by behaviour and required treatment). Source 04 agrees (enter a market too small to attract competition, credited to Peter Thiel). Source 10 agrees (map psychology per segment, not a demographic avatar). `[cdc515a379b0]` `[f52853b6346f]` `[9696a0aeb3b7]` `[573fc71dee16]` `[3a3aa51fd789]` `[06c534df85f9]` `[a04096752c25]` `[ebe9a9117702]` `[9e9810f99d99]`

**R12. Plot the brand against every checkout alternative, including doing nothing and a marketplace private label, on axes a shopper weighs mid-cart, like price vs delivery speed.** Condition: the core positioning exercise; re-run it with different axis pairs, since a category maps many ways. Source 02's axis menu: speed, price, performance, ingredients, purity, sustainability, obviousness, maintenance cost, safety, edginess, distribution, network effect, imminence, visibility, trendiness, privacy, professionalism, difficulty, elitism, danger, experimental, limited, incomplete. The crowded middle needs an ad budget to win; an overlooked corner does not. Source 09 ran the same exercise with opposing-quality axes (understated vs outspoken, warm vs stark, curated vs raw, premium vs budget) and plotted out-of-category brands, which revealed space that category-only comparison hid; it found itself "swimming in a crowded pool" and moved. Source 03 agrees with the aim (an open rung) but uses the ladder, not a grid. Source 09 says axis choice is subjective and the map is an alignment tool, not a scoring model. `[cdddb1268ba4]` `[93e68a951096]` `[84c08bf1872c]`

**R13. Reposition the competitor's meaning rather than running "we're better" comparative ads.** Condition: no open creneau exists and a competitor holds the slot. Source 03: Tylenol spent about 60 words on aspirin's stomach risks before naming itself and became the top analgesic; Wise read the Pringle's ingredient label aloud and Pringle's share reportedly fell from 18% to 10%; Royal Doulton named Lenox's real factory town. Comparative ads ("Ban is more effective than Right Guard, Secret, Sure") invite "if you're so good, why aren't you the leader?". Pass 1 adaptation: an "us vs them" page that states a specific, verifiable fact about a competitor's product does this work; one that only claims superiority does not. ecomOS override 5 applies: every named-competitor fact needs `[web check: legal review of comparative claims per selling country]` and no competitor mark or copy is reproduced. `[4e43c308641d]` `[326a3dca9341]` `[a57fe56ea376]` `[266a692c2863]` `[db70929c9e07]`

**R14. When a small budget cannot outspend the category, reposition the category around the leaders' shared weakness.** Condition: a follower with a real, voiced customer frustration the leaders share. Source 03's Milk Duds case ("America's long-lasting alternative to the candy bar" reversed a sales decline; the angle had not appeared in 15 years of prior ads). Source 03's research note: the real Milk Duds buyer was a cautious 10-year-old "purchasing agent", so define the real prospect first. Source 03 only. `[babb616ba8a9]`

**R15. A genuinely new category needs a new ladder, and the mind resists it unless it is explained against an old one.** Condition: category creation. Source 03: "horseless carriage", "lead-free gasoline", "sugar-free soda"; Mailgram tested "the impact of a Telegram at a fraction of the cost" against "a new high-speed service for important messages" in 6 US cities over 13 weeks, and the Telegram anchor raised awareness from 23% to 47% while the letter anchor fell from 27% to 25%. Pass 1 adaptation: on a PDP, anchor a novel format to the nearest thing the shopper already knows ("the X without the downside of X") rather than a features list. Source 02 agrees with the mechanism as pattern match vs pattern interrupt: a pattern interrupt requires breaking a habit, most people say no, and the best targets are people whose life just broke the pattern (new parents, movers, a new platform's first users). `[92e5149e81d9]` `[1b114afd066c]` `[9794ccdb926c]` `[8c7a16df0f13]`

**R16. Position the destination before the vehicle: if demand for the category or place does not exist, positioning the brand inside it is wasted spend.** Condition: the real problem sits one level above the product (source 03: Sabena's problem was Belgium, not the airline; 7-Up's was cola's share of mind, not lemon-lime preference). Source 03's Belgium program used an outside authority (5 Michelin three-star cities vs 1 in Holland) and was abandoned by new management; treat the method as sound and the outcome as unproven. `[6b46650fd04c]` `[7a5f6e23a28d]` `[f0d81e00c9a5]`

**R17. Borrow a credible, independent authority to justify an inconvenience or a premium; never fabricate one.** Condition: a genuine third-party list, rating, certification or guide exists. Source 03's Stowe case (the only Eastern US resort on a published top 10 list). Source 05 agrees: certification symbols are a decision shortcut but must be earned through a real third-party test. Override 1 applies: a self-made "top 10" is an invented claim. `[2e309f07feea]` `[2abe90be27a4]`

**R18. Before shooting a PDP hero image, check whether competitors use the same category cliche shot; shoot the image shoppers have not scrolled past.** Condition: any hero image, packaging or ad set for a brand or a place. Source 03: Jamaica's positioning came from the verbal image prospects already held (matching Hawaii), and generic beach-and-palm imagery is tuned out. Source 12 agrees: no mountains or pine trees for a Himalayan brand. Source 01 agrees: 60 car ads spliced together were indistinguishable. `[2362e3449185]` `[ea573c35f69c]` `[c10449bf351d]` `[8311a6869eb4]`

**R19. Position one step ahead of today's culture, not ten.** Condition: creative or aesthetic refreshes and category-defining launches. Source 02: JetBlue only had to be hipper than American and Delta; Virgin America 6 years later had to be hipper than JetBlue. Source 02 only. `[2f504f814390]`

**R20. Write the promise as 3 sentences: "My product is for people who believe ___. I will focus on people who want ___. I promise that engaging with what I make will help you get ___."** Condition: every positioning statement, homepage hero and PDP headline. Fill the first blank with a belief, not a demographic; the second with an aspiration the customer already pursues; the third with a concrete emotional transformation. A promise is not a guarantee. Source 02's template; source 05's "big idea" and source 10's "identity mirrored" are compatible formats. `[25d09eedd419]` `[e5b4497dc979]` `[5e39aa1931b9]`

**R21. Decide whether the segment runs on affiliation or dominion, and write for that frame; never average the two.** Condition: acquisition creative, influencer briefs, community mechanics. Dominion is vertical (winning, power, "I did this myself"); affiliation is horizontal (who knows you, who trusts you, being in sync). The same person flips by context, so check the purchase moment, not the personality. Fashion is usually affiliation; affiliation tolerates abundance, dominion leans on scarcity. Source 02 only; test against real customer language before spend. `[bbfb0fef7597]` `[b87302554feb]` `[c89ca806685c]` `[963941c44199]`

**R22. Define "us" narrowly and explicitly in every "people like us do things like this" statement.** Condition: manifestos, community language, About pages. A vague "us" is useless. Source 02 (the 100 blue ribbons case). `[f3fcf887a035]` `[1381647866a6]`

**R23. Build an exclusive cohort (belonging the group controls) rather than only an elite one (respect outsiders can revoke).** Condition: loyalty tiers, member communities, gated access. Source 02, citing Gladwell. `[0917788c7038]`

**R24. Read the semiotics: people scan, not study, so every touchpoint must remind them of the right thing.** Condition: storefront, PDP, packaging and ad audits. Source 02: a flashing-GIF site or a robocall pause reads as a scam and is hard to undo; big-company logos look alike on purpose; the symbol lives in the viewer's mind. Source 05 agrees (perception is shape, then colour, then words; see R91). Source 07 agrees with context (Joshua Bell ignored in a subway). Source 12 agrees (semiotic filtering of symbols). `[b1ae1eab635d]` `[b4d995b1ac08]` `[751a21990d7c]` `[33a9a29e4bd2]` `[c10449bf351d]`

**R25. Run the commodity-swap check: if a customer switched to the nearest competitor would not notice or care, there is no brand yet.** Condition: any brand-investment decision. Source 02. `[dfa417998535]`

**R26. Prove traction in the small before spending to scale a position.** Condition: gate before raising acquisition spend or rolling out. Source 02 (who uses it daily, who would miss it). Source 07 agrees (first talks to 6 people; watch who lights up). Source 03 agrees from the rollout side (dominate 1 market, then the next; see R146). Source 04 agrees (1 SKU, 1 flavour for about a year). `[1652f9bf8c62]` `[6ef98e0e935d]` `[67d6adbf5558]` `[c842ee26e172]`

**R27. Match the story to the worldview the audience already holds; changing a belief is far harder than affirming one.** Condition: before writing creative or choosing a channel. Source 07 (Lands' End buyers would need to become different people first). Source 03 agrees ("mind-changing is the road to advertising disaster"). Source 02 agrees (change the ritual, not the underlying need: Lion Guardians replaced lion-killing with lion-tracking as the same rite of passage). `[33a9a29e4bd2]` `[079c0cc5fa06]` `[f1188b0479f4]`

**R28. Answer the 6 positioning questions in writing before any creative: what position do we own, what position do we want, whom must we outgun, do we have enough money, can we stick it out, does our execution match.** Condition: the start of every positioning program. Source 03. Source 12's 4 strategy questions (why care, what is different, who are we speaking to, what are we trying to change) cover the same ground for a small brand and can be merged into P1. `[e247ee27ad80]` `[4c9bc44b263f]` `[843d2f160b77]`

### Group B. Premium positioning and price as a signal

**R29. Price is a signal and a positioning claim; decide it with the position, not after it.** Condition: setting or restructuring price points. Source 02: the choice between the cheapest and priciest wine says nothing about the wine, only about the story the buyer wants; price must match the XY extreme claimed elsewhere. Source 03: high price is a creneau, but "the secret is being first to establish the high-price position with a valid product story in a category open to it"; charging more is not by itself the way to get rich. Source 01 reports a wine-pricing fMRI study (20 volunteers) in which the same wine at a higher stated price activated the pleasantness region more; treat it as a claim (see group G). `[070a742b6c8b]` `[19792f53199d]` `[7f129dfe890c]` `[e85eec884526]`

**R30. Premium is a function of positioning, content, partnerships and distribution, not of price.** Condition: a value-priced product that wants a premium perception. Source 04's brand sells an under $3 can as "the champagne of electrolytes"; source 10 says premium brands make buyers "want to pay 10 times" through exclusivity, identity and storytelling; source 07's Festool jigsaw sells at about $220 vs about $25 by being best on every dimension. Source 04's "only thing under $3 that's luxury" is "reject unless proven" under override 1. `[341ada6f7913]` `[6d7746b8892c]` `[0bc28a1a4edf]`

**R31. Price inside the category's learned range unless you have a valid story for a new band; 2 to 3 times the norm generally fails with the same shopper.** Condition: launching into an aisle or listing set with an established price band. Source 04 watched the shelf, kept the can under $3, and spent the difference on liquid, design and positioning. Source 03 gives the opposite case (Michelob built the premium band) but only where the category was open to it. Conflict C5. `[563e8d7206aa]` `[7f129dfe890c]`

**R32. Ask the "ten times" question before adding a premium tier; reject "more of the same" answers.** Condition: premium tiers and luxury bundles. What would justify charging 10 times more? More words, bigger portions or a louder stereo do not multiply willingness to pay; a different story or a different scarcity (access, curation, relationship, transformation) might. Source 02 only. `[b48af12fdcd2]`

**R33. Lowering price does not build trust; on high-ticket items it can do the opposite.** Condition: high-ticket items and premium subscriptions facing hesitation; not a licence to raise price without quality. Source 02 ("cheap is another way to say scared"; a costly commitment can create trust through dissonance). Source 10 agrees (repeated 40 to 60% off damages identity; the figure is the presenter's illustration, not a measured line). Conflict C5 with discount-led offers in 03-OFF. `[e8ed1256772e]` `[19792f53199d]` `[c2131b88c294]`

**R34. Exclusivity is a narrative angle the competitors have not used, not a stock-out.** Condition: any premium message. Source 10 is explicit: "exclusivity is not scarcity". Source 04 agrees for daily-use products: a sellout is a demand-planning failure and "no one is loyal" through a stockout. Source 01 and 10 allow manufactured scarcity for drops and seasonal withdrawal (Mallomars, Supreme, Represent). Conflict C10: the sellout signal depends on product type. `[9e9810f99d99]` `[3cdbc042d560]` `[9ee51a3f9c3d]` `[32c97afcbe0f]`

**R35. Map what "exclusive" means per segment and per awareness stage before writing premium copy.** Condition: premium positioning. A Patek Philippe buyer may value thousands of hours of complication; another buyer cares about something else. Split unaware customers from those already comparing. Source 10 gives no method; use 02-AVT. `[9e9810f99d99]`

**R36. Write a marketing vector (core positioning, identity mirrored, story told) and a spectrum of ad variance, and let media buyers and creators work from both.** Condition: any brand running paid acquisition against a premium position. Ads may be more aggressive than organic but must stay inside the vector. Revisit the vector when entering a new category, not when one ad underperforms. Decide promotional intensity in advance. Source 10 only; it gives no template. `[c2131b88c294]`

**R37. Test whether removing the product from a PDP or lifestyle hero image still signals the brand's promise; a generic lifestyle shot with no buyer-specific aspiration fails this.** Condition: premium creative. Source 10 (Chanel No. 5's "every woman alive" framing; Nespresso's "What else?"). Source 07 agrees (the Birkin buyer already owned a purse; she bought the ability to be seen carrying it). Source 02 agrees (sell the feeling, not the feature). All are opinion with no data. `[6d7746b8892c]` `[32c97afcbe0f]` `[eb0068016eec]` `[872478a7aa27]` `[71ce8dd57f50]`

**R38. Premium creative casts real practitioners and community members, not models, in 15 to 30 second lifestyle mini-documentaries.** Condition: premium video acquisition. Source 10 (Lululemon's yoga teachers and runners). Source 01 agrees from a different angle: "real people" and wholesome imagery tested better than supermodel-level beauty for women in one cited study, and sexual creative suppresses brand recall (see R120). Source 04 agrees (elite athletes ground authenticity but sell little; volume creators sell). Hand format and hook detail to 10-MCR. `[32c97afcbe0f]` `[47ec35b97f3d]` `[3fd73a09748d]` `[89dde8726b63]`

**R39. Judge premium creative on hook rate, hold rate, CTR and cohort retention alongside ROAS, and do not kill a concept on ROAS alone.** Condition: premium brands. Source 10; no target values given. Conflict C4 with source 02's "refuse to measure brand marketing". `[b16d4573aa7e]` `[7f0f81a9e158]`

**R40. Change only 1 to 2% of a known format; do not reinvent the container.** Condition: entering an established product category. Source 04 kept a standard 355 ml can and spent on liquid, design and positioning. Source 03 agrees in principle (hook the new to what is already in the mind). Source 04 only for the number. `[43695ce04547]` `[1b114afd066c]`

**R41. Design the pack for the channel it must win in and iterate on sell-through, not taste.** Condition: any physical product, especially DTC to retail. Source 04 rebuilt its can 3 times in about 300 days; a minimal design that looked good online failed in 2 retail doors; a coloured rim plus "no sugar, no caffeine" callouts is reported to have tripled sales on the same liquid (1 brand, 2 stores, unverified). About 35% of the pack is untouchable (barcode, mandated text). Source 12 agrees: packaging is the first real proof of an identity for a physical product. Source 05 agrees: unknown brands need pictorial or descriptive support on the pack. `[72056cea16a3]` `[b3388c024bae]` `[7b87514c30ba]`

**R42. Free ideas that spread, paid souvenirs worth paying for; never make everything free.** Condition: content, sampling and community-to-purchase ladders. A purchase creates tension and enrollment a giveaway forfeits; no cash flow means no reinvestment. Source 02 only. `[2ee5aff46dcf]`

**R151. Branch the PDP and cart by AOV band: a low-AOV impulse item leans on trust badges and fast checkout; a high-AOV considered item leans on reviews near the price, financing or pay-later messaging, and proof before the buy button.** Condition: any store deciding PDP and cart layout priorities. R33 covers only the high-ticket half of this branch (price alone does not build trust); no source in this folder gives the low-AOV half. `[general practice]` No library source; verify against brand data before use.

### Group C. Brand strategy elements: purpose, values, promise, story, worldview, tension, enemy

**R43. Strategy comes before any visual work, and it is written down before visuals are shown.** Condition: new brand, rebrand or major identity project. Source 12 (4 questions, then purpose, mission, vision, 3 to 5 values, before opening a design tool). Source 05 ("meaning is like a campfire": a written framework of essence and attributes stops approval from becoming a taste fight). Source 09 (several weeks of Discover and Define before Develop). Source 03 (6 questions first). 4 sources agree; none disagrees. `[843d2f160b77]` `[c4d91190801b]` `[0416e9b4f0ca]` `[5a833673f348]` `[e247ee27ad80]`

**R44. Brand strategy is one central unifying idea built from 4 inputs: vision, alignment with business strategy, values and culture, and customer understanding; it must work for employees and partners, not only buyers.** Condition: precedes naming, logo and tagline. Source 05. Source 09 agrees (4 attribute lenses: values and beliefs, features and benefits, voice and tone, look and feel). `[d3471950043d]` `[69143a5b063b]` `[a85cb5eecad5]`

**R45. Fix 3 to 5 non-negotiable core values and use them as creative filters at every later gate.** Condition: every approval (mood board, sketch, asset sign-off, partnership). Source 12. Source 09 agrees (stylescapes scored against previously defined values). Source 05 agrees (judge decisions against the 9 or 10 brand ideals: vision, meaning, authenticity, coherence, flexibility, commitment, value, differentiation, sustainability, plus design excellence). The numbers 3 to 5 and 9 are each 1 source's practice. `[843d2f160b77]` `[3d381bacc1a4]` `[50ae9056bb7a]` `[0416e9b4f0ca]`

**R46. Turn discovery into a small number of written "How might we" challenges and use them as the acceptance test for every later decision.** Condition: once discovery findings converge on repeated themes. Source 09 wrote 3 (crafted products that bring joy and warmth; high-end yet humble identity; a site that guides newcomers and enthusiasts). Source 09 only. `[ee667d0641e8]`

**R47. Differentiation must be demonstrated in imagery and copy the customer grasps in seconds, not declared.** Condition: any positioning or homepage claim. Source 05. Source 03 agrees (make the execution be the strategy; the ideal ad is simple enough to be the strategy statement). `[b2d4685817ad]` `[bac208e763af]`

**R48. Behaviour must match the image: no image management without behaviour management.** Condition: any claim on packaging, listings or pages. Source 05 (IBM's Jon Iwata). Source 02 agrees (trust is earned through action: what you did on a refund, a breach, a closure). Source 03 agrees (United Jersey changed 7 operations before the "fast-moving bank" ads ran). Source 12 agrees (perception is shaped by how you handle feedback). Override 2 enforces this: claims match the brand record. `[9ff53840ee86]` `[e4fcc6c178a1]` `[6355cdae1a6b]` `[c39f9828740f]`

**R49. Tell the founder or brand story as Story of Self, Story of Us, Story of Now.** Condition: About pages, launch emails, founder video. Self establishes "I am people like us, I did things like this" without catastrophising or fake vulnerability; Us explains why this audience should care; Now is the concrete, peer-backed call to act. Source 02 (Marshall Ganz). Source 07 agrees on the elements (occasion, who else is in, what is at stake, where the possibility is, who it is for). `[1d9f9a55d030]` `[846111480ab9]`

**R50. Create tension, never fear.** Condition: acquisition, cart recovery, launch scarcity, community pressure. Tension is the pull of "this might work" or "I might be left behind" and resolves with one simple action; fear paralyses. Source 02. Source 01 agrees that fear-based markers are powerful and abused and predicts more of them; it does not endorse them. Override 1 forbids invented scarcity. `[e1cc02e44a65]` `[8d76a2fd3089]` `[00978aa1938e]` `[18a609b6840b]` `[844b2776ac81]`

**R51. Name the enemy as a belief, a category habit or a competitor's real behaviour, not as a person.** Condition: brand manifestos and against positions. Source 03 names competitors' real facts (Lenox's factory town, city banks' Bahamas branches). Source 01 lists "power over enemies" as one of 10 traits it claims strong brands share with religions (from 14 interviews, no sampling method). Source 02 warns against Alinsky-style tactics (ridicule, freeze and polarise a person) and offers generous mirror images: disagree with institutions, not people. Source 08 says publicity from controversy raises reach but not positive direction. Override 5 applies. `[326a3dca9341]` `[fcfff9855adc]` `[2f826d11d900]` `[e8a586c2dde0]` `[357f0df4609a]`

**R52. Say who a change is for and who it is not for when price or policy changes.** Condition: pricing, tipping or loyalty changes affecting existing customers. Source 02's USHG case (no tipping, prices up about 20%; some big tippers lost a status ritual, fairness-minded diners gained a story). `[7c300cb94734]`

**R53. Design the product or experience so the customer has a reason to tell others; the marketer does not spread the word, the customer does.** Condition: packaging, unboxing, post-purchase and referral design. Two bridge questions: "What will I tell my friends?" and "Why will I tell them?" The why must benefit the friend, not the brand. Visible use spreads (TOMS shoes); private use does not (TOMS coffee). Source 02, 07. Source 01 agrees (a Wii unboxing video viewed about 71,000 times in a week, as anecdote). `[5f5e55f7d191]` `[f315eb5389c3]` `[141441a7be8f]` `[800ade0c28a2]` `[d96b818935a8]`

**R54. Reframe customers as students and design tension and relief into every step of the journey.** Condition: onboarding, content sequencing, PDP flow. Source 02 (Penguin Magic shows the trick's result, not the method; the Open Heart Project's 8-part system). `[16af7cf20f56]` `[25f6ebc5c073]` `[db8055815e43]` `[85c6164c8044]`

**R55. Copy a proven business model; spend originality on the story and experience.** Condition: launch planning. Source 07 (franchising already worked; do not invent a structure). Source 02 agrees (scrapbook proven elements). `[1e1b6ad921c2]` `[c9a73bf85977]`

**R56. Separate goal, strategy and tactics; hold the strategy for years and change only tactics.** Condition: annual planning and channel-kill decisions. Source 02 (Patagonia's strategy stable 30+ years). Source 03 agrees (stick to a basic position and vary only tactics; find new ways for Ronald McDonald to eat a hamburger). Source 10 agrees (revisit the vector on a new category, not on one bad ad). `[8d1d09b4c8e5]` `[74102b158e33]` `[c2131b88c294]`

**R152. Write a subscription brand's promise around the replenishment ritual and churn-aware messaging, not only the one-time-purchase story; name tiers so a shopper can say which tier they are in.** Condition: subscription and repeat-purchase brands. Source 02's card `573fc71dee16` sizes the smallest viable market for a subscription business but does not cover promise-writing; the promise-writing part is `[general practice]`. See R49 (story) and R114 (engineered ritual). No library source for the promise-writing rule; verify against brand data before use. `[573fc71dee16]`

### Group D. Naming

**R57. The name is the single most important and highest-frequency brand decision; do not let a placeholder become permanent.** Condition: any name meant to last. Source 03 ("the name is the hook that hangs the brand on the ladder"). Source 06 (it appears on every ad, pack, PDP title and subject line; a rushed "our attorney called, we need a name" placeholder compounds friction for years). Source 05 rejects the myths "I will know it when I hear it" and "we cannot afford to test the name". 3 sources agree. `[526980d48d67]` `[46a0f217dd38]` `[24a1ee273847]` `[fa435f935bc2]` `[87d34d6ea872]`

**R58. Run a category audit, a product audit and a buyer audit before generating any name.** Condition: every naming project. List every name in the category and its pattern (source 06's fibre example: "Fiber One", "Fiber Plus" are all descriptive), state what is actually different about the product, and state why buyers buy and the ultimate benefit up the ladder. Then answer 4 questions in order: how do you define winning, what do you have to win, what do you need to win, what do we need to say. Source 06. Source 03 agrees (a name should begin the positioning). `[0c6615eb4029]` `[14751ff10cd0]`

**R59. Name the ultimate benefit or a surprising idea, not the category, and keep the category word visible in secondary copy, tags and metadata.** Condition: brand-level names. Source 06 (Swiffer, not "ProMop": nobody wants to mop; Impossible Burger, not "Natural Farms"). Source 06 itself gives the search resolution: keep "fiber" on the label and in metadata so a benefit-led name does not hurt discovery. Conflict C2 with R60. `[6286b8c570e9]` `[24a1ee273847]`

**R60. For product and collection titles, which double as search terms, default to a descriptive title with the benefit visible in the first 60 characters of a mobile result; save a coined name for the parent brand only.** Condition: product and line names, and brand names on small budgets. Source 03 (Spray 'n Wash, Head & Shoulders, DieHard; Kodak and Kleenex worked because they were first). Source 05 lists descriptive as a type that "communicates intent, can become limiting" and fabricated as "distinctive, needs market education spend". Conflict C2: source 06 pulls the other way at brand level; see section 7 for what to do. `[b17d31320962]` `[9e3ddfa5cf56]` `[449e6bdd1311]`

**R61. Screen every candidate against 7 qualities: meaningful, distinctive, future-oriented, modular, protectable, positive in every served market, visual.** Condition: any naming decision. Source 05. Source 06 adds 3 jobs (get attention, hold attention through processing fluency, be surprising) and a believability gate. Source 03 adds the sound test. Merged into checklist 5.2. `[87d34d6ea872]` `[24a1ee273847]` `[b7494c09d18d]`

**R62. Generate across the 6 naming types on purpose, not from unstructured brainstorming.** Condition: candidate generation. Founder (Tory Burch; easy to protect, tied to a person), descriptive (E*TRADE), fabricated (Kodak, Pinterest), metaphor (Nike, Patagonia, Amazon), acronym (IBM; hard to remember, needs heavy spend), magic spell (Flickr, Netflix), plus combinations. Source 05. Source 06 adds systematic mining: Latin and Greek roots, mythology, an enriched periodic table (Pentium), a cross-category "small things" archive, and 3 differently briefed lenses (full product story, an altered detail, an unrelated domain). `[449e6bdd1311]` `[4e009c4e7883]` `[8d9104bffa0d]`

**R63. Generate far more than feels necessary and defer judgement to a scheduled evaluation.** Condition: the ideation phase only; a feasibility, legal and margin pass still happens later. Source 06: clients get stuck at 50 to 100 names; the agency works toward about 2,000 raw candidates; kill nothing in the room; use "approximate thinking" (present half-baked ideas). Source 12 agrees for marks (sketching is a volume exercise). Source 06's small-team finding (group brainstorming degrades output past 4 to 10 people) comes from a study its own author calls "sloppy and crude". `[3b6889a898c9]` `[ae16dc1d542a]` `[69fd0d7859ec]` `[7fec0334bcfe]` `[5b189a6b6181]`

**R64. Shortlist for the tension zone, not the comfort zone; do not use consensus as the tiebreaker.** Condition: shortlisting, not launch readiness. Source 06 (Andy Grove on Pentium: a name that makes people uncomfortable has energy in it; "Ready Mop" tested as "a mop", which is comprehension, not differentiation). Score with a "no sevens" rule. A polarising name still needs believability, legal clearance and a commercial check. Source 06 only. `[9d81ed21b342]` `[0db63ae1d97c]` `[99647fecb304]`

**R65. Test sound, not just spelling: the mind processes a name aurally first.** Condition: every finalist. Source 03: count syllables; RCA (3) beats "Radio Corporation of America" (12); TWA is not shorter than "Trans World"; common English initial letters are S, C, P, A, T and the rarest are X, Z, Y, Q, K. Source 06 (sound symbolism as a scored criterion; "B is one of the most reliable sounds in English"; "the letter X always says innovation"). Both are practitioner opinion; the pass 1 file notes no controlled study is cited. `[7bd3e22840b8]` `[99647fecb304]`

**R66. Initials and acronyms only work after the brand is famous.** Condition: brands not yet household names. Source 03 (case detail moved to Appendix A). Source 05 agrees (IBM and GE used full names for years first). Test: is there real phonetic shortening, does the mind still hold the full name, does it sort sensibly in a list. `[868f7e43ad95]` `[dca1b04ea88b]` `[449e6bdd1311]`

**R67. Guard against the name becoming generic.** Condition: a descriptive name that succeeds. Source 03: "Lite beer from Miller" became "Miller Lite" and Miller lost exclusive rights to "light" for beer. Source 03 only. `[5fffd494c3af]`

**R68. Do not hide the product's nature behind a euphemism; a negative or plain name can polarise and build pride of origin.** Condition: names for categories with a trust problem. Source 03 ("soy butter" over "margarine"; "corn sugars"). Source 03 only, and the examples are dated. `[9eb8f61cd2ab]`

**R69. Do not name the brand after the founder if the brand is meant to outlive the founder's visibility.** Condition: founder-led brands planning to reduce founder presence. Source 04 (the founder is "fuel, not the fire"). Source 05 lists founder names as a valid type with real trade-offs (easier to protect, tied to a person). Conflict C13. `[7927ac1ccf6e]` `[449e6bdd1311]`

**R70. Run trademark and domain checks on every finalist before it is presented as a finalist, and test pronunciation and connotation in every selling language.** Condition: every naming project. Source 05 (protectable = trademark plus domain; "hundreds of names are reviewed before one clears"; the frameworks are not trademark advice). Source 06 (legal review prunes the list to 10 to 15; BlackBerry tested in about 6 languages). Source 05's China chapter: test across dialects and register early. `[web check: trademark registers, domain registrars and dialect readings per selling country]`. `[87d34d6ea872]` `[4e009c4e7883]` `[9e4834e83109]`

**R71. Present finalists in realistic context mock-ups, not as a list, and pass a sub-second believability gate; mock-ups must not imply real coverage, endorsements or claims that do not exist.** Condition: presenting to a decision maker. Source 06 (decision makers have little practice judging creative; Azure was believable as a cloud brand). Override 1 governs the mock-ups. `[b7494c09d18d]`

**R72. Use AI to ask questions about the subject and to bulk-generate raw candidates; keep the judgement framework and category knowledge in-house.** Condition: any naming project after 2024. Source 06: anyone can generate 200 to 300 names with an assistant; judging is the scarce skill; define the criteria before looking at candidates. `[verify UI: assistant capabilities change]`. `[d9c1184d1dd6]` `[0b1a266ee4fd]` `[bcf903029405]`

**R73. Deliver more than the name: nomenclature (how the product is described), a positioning line and a short brand story; then track how the name lands at about 90 to 120 days.** Condition: agency-scale naming; scale down for a small brand. Source 06 only. `[a714872495ee]` `[d08af5a4ebfa]`

**R74. A tagline is typed by its job: imperative, descriptive, superlative, provocative or specific; it must be short, differentiated, memorable, legible small, protectable and free of negative readings.** Condition: whether a tagline earns a place at all. Strip test: remove the product image and check the tagline still says the category or the claim. Source 05 only. `[9e41c8e1ca32]` `[612c157ef1c5]`

**R75. Words are empty containers; if a name cannot hold the intended position, rename rather than force it.** Condition: repositioning into a tier the current name cannot carry. Source 03 (Volkswagen could not carry a luxury car; Audi could; Eastern Airlines' regional-sounding name kept it ranked 4th of 4). `[e75b50392fca]` `[86ea8f99ebef]` `[defb93a85270]`

### Group E. Brand architecture, line extension and renaming

**R76. One name cannot stand for 2 distinctly different products without one meaning weakening as the other strengthens (the teeter-totter).** Condition: any proposal to put an established name on a different job-to-be-done. Source 03's era cases: Protein 21 fell from 13% to 2% share after hairspray and men's variants; Pall Mall fell from 14.4% to 3.8% after menthol and light extensions; Heinz became ketchup and lost pickles to Vlasic; Xerox ran "This Xerox machine can't make a copy" and wrote off $84.4M more. Source 03 concedes exceptions (GE, Vaseline Intensive Care, which earned its own name in speech). Conflict C1 with sources 04, 12 and 05. `[ad5c24b3c953]` `[1aaf6ab34b2e]` `[322fbe17b694]` `[8a909a51fd89]` `[3dc57a790b44]` `[ecf11f686ff7]` `[779fc1b761d8]`

**R77. Run the shopping-list test and the bartender test before any extension.** Condition: every extension proposal. Shopping list: write only the brand name; if a shopper cannot say which single product to bring back, the name is already diffuse. Bartender: order the brand name alone; if it is ambiguous between tiers (Cutty Sark vs Cutty 12), give the premium or entry tier its own sayable name (Chivas Regal). Source 03. `[6b22f8028e70]` `[c4a8fdae883c]` `[4fc88b60ad48]` `[3bdfbcd79086]` `[03327dab7ce5]`

**R78. Reverse line extension is safe: keep the identical product, package and name and promote a new use occasion.** Condition: growth without a new SKU. Source 03 (Johnson's baby shampoo promoted to adults; Arm & Hammer in the fridge; a separate "Arm & Hammer deodorant" went nowhere). Source 03 only. `[3ca345f68121]`

**R79. Decide house name vs new name with the 5 rules of the road: expected volume, competition, advertising support, significance, distribution.** Condition: a genuine new product. A potential winner, a crowded field, a big ad budget, a breakthrough and self-serve distribution each favour a new name; a small-volume item, a vacuum, a small budget, a commodity and rep-sold distribution each favour the house name. Weighed together, not scored. Source 03. Source 05 frames the same choice as monolithic, endorsed or pluralistic architecture chosen per category, and notes there is no industry-standard terminology. Source 04 agrees on gating: no new SKU without size of prize, MOQ, margin, lead time, channel strategy and an anchor customer with a launch window; the hero SKU should reach the founder's own bar ($10M revenue, his category only) before the next flavour. `[e192263b85cc]` `[4f6df01afd17]` `[4e20426232bb]` `[936a15cb7c7e]` `[a18c1c43a8c2]` `[e175eacb2b24]` `[c842ee26e172]`

**R80. A famous name gives no free ride to a different product.** Condition: attaching a new product to a known name to save launch spend. Source 03 (case detail moved to Appendix A). Source 03 allows exceptions (GE). `[46df3117bf9a]` `[e2d2e2bdb4c6]`

**R81. Watch the reorder curve, not the launch flash, for 6 or more months after an extension.** Condition: any line extension. Source 03: trade stocking books an "instant flash" (about $35 of stock per US supermarket booked $1M in first orders in its arithmetic) that looks like a hit until reorders stall. `[3c603945dca9]`

**R82. Small brands default to one master brand; split off a sub-brand only when a genuinely different audience or price tier needs distance.** Condition: a store with 1 real product line. Pass 1 adaptation of source 05's architecture caveat (endorsed and pluralistic cost extra design and marketing per brand). Source 12 agrees in practice (design the first product's identity as a component of a parent brand: decide what the parent owns, values, type, palette, seal, and what each product owns, flavour name and accent). Source 04 agrees (multi-format line under 1 brand with a halo effect). `[a18c1c43a8c2]` `[c2dd2664000b]` `[17301f63a26b]`

**R83. Cover a competitive threat with a separate brand, not a stretched one; multibrand is single-position strategy.** Condition: a leader facing a new sub-category. Source 03 (case detail moved to Appendix A). Source 03 only. `[be7172025ae3]`

**R84. Rename when the name causes a legal problem, or when it creates measurable friction (hard to spell, hard to find, hard to recall), or when it cannot hold the intended position; not for taste.** Condition: an existing brand. Source 06 (a legal trigger decides it; Kodium to Windsurf took about 6 weeks because nobody could spell or search it). Source 03 (Pullman and Greyhound stuck to old identities; only a name change fixes name obsolescence). Source 05 lists rename, revitalise the brand, revitalise the identity, integrate a system and merger as distinct triggers with their own symptoms. `[fa435f935bc2]` `[dc9410d03a81]` `[f83b39ad5c0e]`

**R85. Weigh company stage: a rename is "not traumatic" at Series A or B; a brand with deep accumulated equity needs a compelling reason.** Condition: rename decisions. Source 06's claim that he has "never seen" equity loss from a well-launched rename is his own account. `[fa435f935bc2]`

**R86. Launch a rename with an explicit story ("we were here, now we're going this way, and here is the benefit to you") and reassure customers that the product has not changed; budget 6 to 9 months of extra resources.** Condition: any rename. Source 06 only. `[fa435f935bc2]`

**R87. In a rebrand, audit equity first and decide what to keep before deciding what to change.** Condition: redesigning a business that already sells. Source 09 kept its logo unchanged because it already worked and wrote usage rules instead. Source 05 (evolutionary vs revolutionary, decided on equity, not taste; identify elements to preserve). Source 03 agrees (the F.W.M.T.S. trap: Avis dropped the number 2 line after being bought and never found a remembered replacement). `[5a833673f348]` `[a913f3dfc742]` `[4469bf1ed068]` `[a3b068db34cd]`

**R88. A rebrand forces catalogue decisions; expect to discontinue products that no longer fit.** Condition: positioning sharpens. Source 09 only. `[ee667d0641e8]`

**R153. Decide which SKUs get brand-building spotlight and which stay workhorse listings; do not spend identity budget evenly across a catalogue.** Condition: catalogue stores with more than 1 real product line. Source 02's long-tail-escape card `2b78cfe849b3` was in the sources but not carried into pass 2; this rule carries it in. See R82 (master brand default) and R101 (parent-kit scaling). `[2b78cfe849b3]`

**R154. Choose which product format or pack size goes to DTC, which to marketplace, and which to retail, before building the identity kit for each; do not assume 1 format serves every channel.** Condition: a brand selling across more than 1 channel. Source 04's card `b5c53d8871d1` was in the sources but not carried into pass 2. See R79 (house name vs new name) for the same gating logic applied to channel format. `[b5c53d8871d1]`

### Group F. Identity system: marks, colour, typography, photography, voice, packaging, touchpoints, guidelines

**R89. A refresh that changes only the logo, not the PDP template, the packaging insert and the shipping confirmation email, has not changed the brand.** Condition: any conversation that conflates "our logo" with "our brand". Sources 05, 12, 09, 02 ("logos matter less than designers claim and more than committees realise: pick a workable one, don't over-invest, keep it as long as you keep your name"; Google, Sephora and Costco have unmemorable logos and strong brands). `[1c1a35e393b7]` `[c39f9828740f]` `[5a833673f348]` `[177aa8d4c957]`

**R90. Brands do 3 jobs for the customer: navigation (stand out), reassurance (validate the choice) and engagement (identify with); audit every element against all 3.** Condition: any identity audit. Source 05 (David Haigh's typology). `[846c635999c6]`

**R91. Design for the sequence of cognition: shape first, colour second, words last; shape and colour alone must identify the brand at favicon, thumbnail and packaging-panel size.** Condition: any mark meant to register small or fast. Source 05 (colour can be trademarked: Kodak, Tiffany). Source 01's "smashable" test says the same from the other end (see R117). Source 12 agrees (clean the vector until it reads at small scale). `[751a21990d7c]` `[daa4a003c6a4]` `[01da2ffeccbe]`

**R92. Match the mark type to the recognition budget: an unknown brand uses a pictorial, descriptive, wordmark or letterform mark; abstract marks and mascots are for brands that can pay to teach their meaning.** Condition: mark selection. Source 05 (7 mark types; abstract marks carry no meaning until marketing invests; characters need periodic redrawing and, at best, a voice). Pass 1 adaptation of 05: a bootstrapped DTC brand should not attempt an abstract mark or mascot. Conflict C3 with source 01's mascot and smashable-cue enthusiasm. `[7b87514c30ba]` `[ecef7364f49a]` `[1956b7a59e66]`

**R93. Every proposed mark clears 9 functional criteria before aesthetics are argued: bold and memorable, immediately recognisable, consistent with the company image, communicates the persona, legally protectable, enduring, works across media and scale, works in black and white, works in colour.** Condition: logo approval. Source 05 gives no method for trade-offs between criteria. `[df0d1cef5653]`

**R94. Filter symbols semiotically: decide the feeling first, rule out category clichés, then check each candidate's actual cultural reading in every selling market and drop mismatches.** Condition: mark, motif and packaging symbol choice. Source 12 (clover leaf dropped for its Irish reading; ginkgo chosen for Asian readings of longevity and resilience). Source 05 (Deloitte's green dot on black everywhere except China, where black connotes death). Source 01 (numbers and colours must be adapted per market: 4 vs 8 in Chinese-influenced markets, 13 in Western markets). `[web check: symbol and colour readings per selling market]`. `[c10449bf351d]` `[8462323ed8e5]` `[af6598864147]` `[b43f8160f55f]` `[afc9e3363d43]`

**R95. Explore 3 genuinely distinct creative directions before any custom design, score them on team resonance and fit to the written values, and merge elements rather than picking one outright.** Condition: strategy is agreed and the look is not; skip only if there is no time or budget. Source 12 (3 mood boards; 1 rejected as not premium, 1 for feeling disconnected, its serif type carried into the winner). Source 09 (3 stylescapes across touchpoints merged into "The Story of Craft"). Both say 3 is their working number, not a tested optimum. `[0060a896ab51]` `[3d381bacc1a4]`

**R96. Anchor the palette on 1 memorable core colour plus a small set of accents, validated on print and screen, not a flat palette of equals.** Condition: any palette that must work on packaging and site. Source 09 (deep green as "bold yet calming"; colour review was "one of the most intense parts"; no contrast threshold given). Source 12 (a minimal palette: black, white, subtle red, chosen for that brand only). Source 01 reports colour effects as claims (see R116). No source gives an accessibility threshold; add the brand's own or a `[web check: WCAG contrast ratios]`. `[9b48715e763f]` `[01da2ffeccbe]` `[2e704af4c88b]`

**R97. Assign typography by the job the copy does, test pairings in a specimen and then on 2 real sample pages with real images and buttons before committing.** Condition: a brand mixing expressive and technical copy. Source 09 (serif and sans for header and body, monospace for specs, bitmap selectively; overuse of a decorative face dilutes it). Source 12 agrees on pairing a typeface with the mark before application. `[acd8f5a64996]` `[01da2ffeccbe]`

**R98. Write photography as a short list of explicit constraints with reference images, and check every shot against it; grading must not misrepresent product colour.** Condition: briefing photography or selecting UGC. Source 09's 4 rules (strong directional light; warm natural tones with subtle grain; lived-in but not messy; people never detract from the product) plus its own caveat that warm grading and grain can misrepresent colour. Override 6 applies: accurate real product photos where colour, size or texture matters; generated images do not replace them. `[8a3a065898f8]`

**R99. Put the identity's best execution on the one touchpoint that decides the purchase, and revisit that choice as the business changes.** Condition: any identity budget. Source 12 (physical product: packaging and promotional material; cafe: menu; software: interface). Source 05 agrees (moments of truth: concentrate on the instants the customer cannot skip). Source 04 agrees (design the pack for the shelf it must win on). `[90bb50a21f09]` `[c383852eb750]` `[f4bd6b669b5c]` `[72056cea16a3]`

**R100. Apply the locked asset kit to the decisive physical touchpoint as the first proof; if it feels off, revisit the creative direction, not the layout.** Condition: physical products. Source 12 (label and outer packaging). Source 09 (the website first, because it forces type, imagery and colour to resolve together; sitemap, then 2 placeholder pages, then build). Which touchpoint goes first depends on R99. `[b3388c024bae]` `[c46421294324]`

**R101. Design the launch identity to scale to the parent brand: decide what the parent owns and what each product owns so new SKUs reuse the kit.** Condition: a first product under a brand meant to grow a range. Source 12. Source 05 agrees (flexibility is a paired requirement with coherence; "not licence for inconsistency"). `[c2dd2664000b]` `[d658546a61ae]`

**R102. Coherence is one voice, one strategy, uniform quality and every touchpoint treated as a brand experience; it is not rigidity, and over-enforcement kills needed creativity.** Condition: building standards. Source 05. Source 09 agrees in practice (a named, contained "alter-ego" visual layer kept separate from the core system). `[e1cc915bc7d7]` `[a913f3dfc742]`

**R103. Brand voice default: professional but not corporate, friendly but not fake, no jargon and no buzzwords, with technical specs still available for research-heavy buyers.** Condition: a brand with no voice sheet (override 3). Source 09 (drafted over several passes in a shared document). Source 05 agrees (polish and cut; "a sentence should contain no unnecessary words"; cutting must not remove what the buyer needs). Source 02 agrees (avoid buzzword "change" stories). ecomOS override 4 sets the reading level. `[3cac34e1c33d]` `[6aa0c57779c2]` `[8ed5982aa5df]`

**R104. Stay on message across every asset: nomenclature, taglines, descriptors, mission and vision, value propositions, key messages, vocabulary, boilerplate and elevator pitch, applied to site, PDP, ads, email, support scripts and packaging.** Condition: more than 1 person writes brand copy. Source 05. Source 02 agrees (every touchpoint should let a customer guess all of you; be specific, then overdo it). Source 03 agrees (execution must match the position). `[304f64fb3d93]` `[dfa417998535]` `[bac208e763af]`

**R105. Make the execution be the strategy: a stranger should infer the position from the ad or PDP alone; clever creative that obscures the position fails.** Condition: PDP and ad brand-consistency checks (checklist 5.5). Source 03. Source 10 agrees (ads must not waver from the vector). `[bac208e763af]` `[c2131b88c294]`

**R106. Package the identity as a brand book with 4 parts: logo usage rules, one cohesive visual language (type, colour, imagery), explicit language rules with ready messaging samples, and "brand expressions" applied across surfaces as thought starters.** Condition: the identity is otherwise settled. Source 09. Source 05 names guidelines and standards as Phase 5 but the excerpt does not contain that chapter, so 09 is the only source with content. Checklist 5.4 lists what a complete guideline holds. `[a913f3dfc742]` `[58c51fa34a38]`

**R107. Measure rebrand progress by shipped artifacts (guidelines, site, packaging, content capability, product), not by strategy documents; expect the last 10% to take the most time.** Condition: scoping a rebrand as done. Source 09 (about 4 months to first deliverables; no revenue outcome given). `[1d643039b4fd]` `[a913f3dfc742]`

**R108. Separate fixed and adaptable elements for other markets: keep name, product, price, function, symbols, colour and sound fixed; adapt taste, humour, aspiration and ritual meaning; include native experts and test often.** Condition: selling into a second culture. Source 05 (2 related frameworks used side by side). Source 01 agrees on numbers and colours. `[8462323ed8e5]` `[af6598864147]` `[b43f8160f55f]`

**R109. A mascot or character is only worth it if it expresses real brand attributes, carries a voice, and has a redraw budget; it rarely ages well.** Condition: character proposals. Source 05 (Michelin Man, GEICO Gecko). Source 01 claims a mascot can build a cheap, durable somatic marker (Andrex's puppy, a reported 2:1 share lead over Kleenex on equal spend, per Robert Heath's account); that is a claim (R113). Conflict C3. `[1956b7a59e66]` `[80f3f6bcd431]`

**R110. Disclose commercial relationships where the reader meets the content, do not delete negative comments, and write the crisis plan before it is needed.** Condition: any branded social, influencer or founder content. Source 05 (over-disclose; 3 questions: would we be uncomfortable if family were involved, embarrassed if public, using a loophole). `[web check: current disclosure rules per selling country]`. `[6c5906e5113f]` `[fcea49ea73e9]` `[a9088311cadc]` `[15f1c9517cfd]`

**R155. Walk the full funnel in order (search result, PDP, cart, checkout, shipping email, unboxing, support) and mark each touchpoint functional or experiential; do not stop at the single decisive touchpoint R99 names.** Condition: any full identity or guidelines build. Source 05's moments-of-truth cards `c383852eb750` and `f4bd6b669b5c` give this full walk; pass 2 had compressed it to 1 line in R99. Deliverable: 9.9. `[c383852eb750]` `[f4bd6b669b5c]`

**R156. Write the returns and exchange policy as a brand trust signal, not only an operations page; a policy that contradicts the brand's promise breaks override 2.** Condition: any store with a returns flow. Source 09's card `a9b87b90a092` and source 05's behaviour-matches-image card `9ff53840ee86` support the mechanism; P11 step 5 only touched this once as an unproven inference. `[a9b87b90a092]` `[9ff53840ee86]`

**R157. Apply the identity kit to the marketplace brand page and buy-box content (Amazon A+ content, Flipkart brand store) with the same voice and visual rules as the site; hand the account mechanics to 24-DEP.** Condition: marketplace-heavy stores. `[general practice]` No library source; verify against brand data before use.

**R158. Design the hero and buy button for thumb reach on mobile first, and add the trust signals the market needs: cash-on-delivery and payment-trust badges for a mobile-first India audience, festival-demand timing where relevant, and the local equivalents for a US audience.** Condition: mobile-first and market-specific execution. Source 05 lists a mobile and apps chapter in its table of contents, but that chapter is missing from the extracted source text. `[general practice]` No library source; verify against brand data before use.

### Group G. Brand psychology claims (all marked as claims)

Every rule in this group comes mainly from source 01, a 2008 book by a consultant with a vendor stake, reporting his own commissioned study with small samples and no peer-reviewed publication. The pass 1 file lists post-2008 public critiques `[web check: critiques of Buyology's methods and the "90 percent unconscious" figure]`. Treat each rule as a hypothesis to test with the brand's own data, never as a fact for a client page. Where a second source agrees, it is named.

**R111. Claim: stated preference and revealed behaviour diverge, so weight order data, repeat rate and search terms over survey answers when they disagree.** Condition: deciding what to build, stock or advertise from research. Source 01 (smokers said warnings reduced craving; the fMRI reportedly showed the opposite; the Pepsi Challenge; the Quizmania study in which questionnaires did not separate a known hit from a known flop). Source 03 agrees in part (expectation filters perception) but built its bank positioning on semantic-differential surveys (Long Island Trust). Source 06 warns that a high comprehension score in name testing is not differentiation. Source 07 agrees (watch who lights up, not what they say). Conflict C14. `[b6e70f8909c7]` `[1c02b00e5cfd]` `[7cd163b89089]` `[47ec35b97f3d]` `[482e12294329]`

**R112. Claim: about half of point-of-sale decisions are made without deliberation; the "90 percent unconscious" figure is the author's synthesis, not a measurement.** Condition: quoting either number. Source 01 cites Gruppe Nymphenberg for the "over 50 percent" figure with no method. Do not put either number on a client page. `[f19c742bb5e3]` `[a3640e21d284]`

**R113. Claim: a distinctive, even odd, mascot, packaging quirk or signature moment builds a "somatic marker" faster than a feature list, but only with repetition.** Condition: commodity-like products where features are hard to differentiate. Source 01 (Andrex puppy; Blendtec's "Will It Blend?"; a pink bank the author advised after "a number of glasses of wine", with results reported by the client only). Source 06 agrees indirectly (a surprising name compounds through familiarity). Conflict C3. `[a340e6a9c132]` `[2bdfd34d3777]` `[80f3f6bcd431]` `[5ef563bcc38e]`

**R114. Claim: products with an attached ritual are stickier; a ritual can be engineered, not only discovered.** Condition: repeat-purchase categories. Source 01 (Corona and lime began as a 1981 bartender bet; Guinness engineered the "119.53 second" pour; Oreo dunking; Magners on ice). Source 02 agrees on the mechanism from the culture side (change the ritual, keep the need). Pass 1 adaptation: a designed first-use sequence, unboxing order or replenishment cue in packaging and post-purchase flows. `[needs brand data: repeat rate for customers exposed to a ritual-style onboarding vs not]`. `[9c5d9ee989d0]` `[3b56299b42e4]` `[f8ee55b77565]` `[0cbf890ca84b]` `[f1188b0479f4]`

**R115. Claim: watching someone use a product fires the same regions as using it ("mirror neurons"), so first-person demos, unboxing and "customer using it" imagery may sell by imitation rather than information.** Condition: PDP video, UGC and lifestyle imagery. Source 01 (Rizzolatti's macaque studies; the Crocs anecdote; A&F's "clubhouse" stores). Sources 10 and 07 agree in practice without the neuroscience (real practitioners in lifestyle mini-docs; visible use spreads). Pass 1 adaptation: prioritise POV demo content over static feature shots `[needs brand data: PDP video vs static conversion]`. `[8a5b7d650559]` `[e9c09bb38c14]` `[e0305647c836]` `[a12162ab18df]` `[3c6a5508abe9]`

**R116. Claim: colour shifts attention, recall and price perception, and can outweigh substance in a blind comparison.** Condition: packaging, PDP hero and site theming. Source 01 (a Tiffany-blue box with no logo raised heart rate about 20% in 600 women, the author's own test; Heinz green ketchup sold over 10 million bottles in 7 months; a Seoul colour expo figure of up to 80% recognition lift). Source 05 agrees colour is second in cognition and can be trademarked. Source 09 treats colour as the hardest decision. Test with standard A/B methods in 09-CRO. `[2e704af4c88b]` `[830ad040b9b1]` `[751a21990d7c]`

**R117. Claim: test recognition from packaging alone, logo covered, at thumbnail size; relevant only once repeat buyers already recognise the brand, not for a store's first collection.** Condition: established brands with an already-learned code; explicitly not new or low-awareness brands, which have no code to be free of. Source 01 (Silk Cut's purple silk billboards reportedly identified by 98% of consumers after the UK tobacco ad ban; the Marlboro imagery fMRI). Source 01 contradicts itself elsewhere (Apple, Nike and McDonald's symbols remain powerful). Source 02 agrees logos matter less than the promise. Conflict C3. `[b7da48474acd]` `[d80a660bafff]` `[b5a2ca86be10]` `[bbc8849d1c61]` `[72e04566a275]`

**R118. Claim: congruent sensory pairs (image with matching scent or sound) rate more pleasant and are remembered better than either alone; incongruent pairs rate worse than either alone.** Condition: any multi-sensory execution (unboxing scent insert, video sound design, in-store scent). Source 01's "Pete's" study (20 subjects, 9-point scale). Pass 1 adaptation: for ecommerce, smell and touch live in the unboxing moment, sound in notification and video design. Test congruent vs mismatched before scaling (P14). `[20fbba1a4005]` `[598a56fddd0e]` `[c197d7564abe]` `[d96ee4fa4d8b]` `[fcd208a6a2cb]`

**R119. Claim: touch and weight signal quality independent of function.** Condition: physical product and packaging. Source 01's Bang & Olufsen remote test (100 consumers judged the lighter remote "broken"). Source 04 agrees loosely (premium via design and material inside the price band). `[501ed81d0942]`

**R120. Claim: sexual or shock creative "eats" the brand (the Vampire Effect); brand recall fell to 9.8% vs about 20% for men and 10.85% vs 22.3% for women in a 400-subject eye-tracking study; extreme beauty can also suppress recall.** Condition: any ad or PDP image trading on sexual or shock content. Source 01. Controversy (not sex) is the more reliable attention driver and carries reputational and legal risk. If the route is taken, test brand recall by creative variant, not clicks `[needs brand data]`. `[43f966448348]` `[15242b826b8b]` `[73f6e00507f3]` `[8046d8d903e6]` `[382d5f7fae30]` `[47ec35b97f3d]`

*R121 moved to Appendix A: the sonic-asset and Nokia ring-tone test (source 01, claim). Card ids: `[3c9b9d4f6d00]` `[2c808611a9bb]` `[e519920226cf]` `[774df5ca9ac9]`.*

**R122. Claim: brand presence only lifts recall when the brand is load-bearing in the narrative; a stronger co-brand can suppress recall of the weaker one.** Condition: sponsorships, placements, co-branded promotions, shared media. Source 01's American Idol SST study (Coke on screen about 60% of the time gained; Ford with only 30-second spots fell below its own baseline at a reported $26M a year). Source 08 agrees on adjacency (who you appear next to teaches an association). `[14e9e290ba3e]` `[0fdfce48d0e0]` `[3bdf718b5a61]` `[357f0df4609a]`

*R123 moved to Appendix A: the brand-vs-religion 10-trait checklist (source 01, claim). Card ids: `[992d9678d728]` `[2f826d11d900]` `[f951cfe57e4e]` `[6118970e983c]`.*

**R124. Claim: a "low stock" or "selling fast" PDP badge must match the real stock file; a fabricated counter breaks override 1 and risks a marketplace policy strike.** Condition: brands that can credibly withdraw and reintroduce (Mallomars), invitation-only tiers (Gmail, Centurion), expandable ranges (Hello Kitty's 22,000+ SKUs). Source 01. Override 1: scarcity must be true. Conflict C10 with source 04's daily-use rule. `[9ee51a3f9c3d]` `[8723c0ddc0dd]` `[0a83b57e9364]` `[fa843a0610e6]` `[502ec2ab644a]`

**R125. Claim: new product failure rates are high (8 of 10 within 3 months in the US per source 01's loosely cited figures), so some predictive test should precede scaling spend.** Condition: any launch. Source 01. Source 02 agrees without the number (prove traction in the small). Do not quote the figures externally `[web check]`. `[cce38d2b0f78]` `[1652f9bf8c62]`

### Group H. Audience building and content for brand

**R126. Run the 5 steps of marketing in order: invent something worth making with a story worth telling; build it so a few people particularly benefit; tell the story that matches their narrative; spread the word by designing the conditions for customers to tell others; show up regularly, consistently and generously for years.** Condition: any launch or brand build; most teams skip to step 4. Sources 02 and 07 (same author, stated twice). `[1a1c714f09a8]` `[f36e1af62b85]`

**R127. Be market-driven, not marketing-driven; find the lock before fashioning the key.** Condition: product roadmap, positioning and range decisions. Source 02 (do not reverse-engineer a "change" story to justify what you already sell; do not pick a grandiose, unresourceable change). `[c496d321604d]` `[ae66960f68e1]` `[8ed5982aa5df]`

**R128. Own a permission asset (email, SMS, community) instead of renting reach; a platform audience is sharecropping.** Condition: any reliance on platform reach. Source 02 (real permission means people ask where you went if you stop). Source 07 agrees (choose channels for fit, not the algorithm; "unpaid employees"). Source 08 agrees partially (align with the platform's own objectives, not hacks). Hand list mechanics to 14-EML. `[b39a993e6adc]` `[7589bd4ba273]` `[565ac57d818d]` `[6ff737f56ea5]` `[3aa148337062]`

**R129. Judge organic content by revenue and owned-audience growth, not views or followers.** Condition: any creator or content campaign. Source 07 (40 million TikTok views and about $200 of product). Source 08 agrees (publicity raises reach, not influence or direction). Source 04 agrees (a sub-2:10 marathoner with 8,000 followers sold none; a 4-hour marathoner with 400,000 followers did $20k on one swipe-up; volume creators drive about 99% of his DTC revenue, self-reported). `[35873b25b23b]` `[357f0df4609a]` `[89dde8726b63]`

**R130. Separate the give from the ask: organic content carries no direct CTA; the ask lives in paid ads and the link in bio.** Condition: source 08 frames this for businesses running organic and paid together, with a longer consideration cycle; its own card says stores with one-touch purchases may not see the same payoff and lose direct attribution. Conflict C8. Hand posting mechanics to 13-ORG. `[dd681a3febd1]`

**R131. Brand is a behaviour-changing association; evaluate it on 3 axes: strength of influence, direction (toward or away) and reach; and choose adjacencies (stages, sponsors, collabs) for the association they teach.** Condition: any appearance, sponsorship or collaboration decision. Source 08 (rejects "all publicity is good publicity"). Source 04 agrees on collabs: non-competitive categories serving the same customer, with a brand-fit veto regardless of ROI. Source 01 agrees on co-brand recall suppression (R122). `[357f0df4609a]` `[37211e67c319]` `[89dde8726b63]`

**R132. Use the founder as the early face, keep founder content to 1 to 3 themes, and plan the handover so the brand can live past the founder; remaining the face indefinitely is a valid alternative, not a mistake.** Condition: founder-led brands in years 1 to 3. Source 04 (tracks which customers arrive via founder content). Source 10 agrees (founder documentaries as the storytelling beacon). Source 05 agrees that a founder's personal brand needs the same discipline because "the web never forgets". Conflict C13. `[d5e25e56fca4]` `[7927ac1ccf6e]` `[32c97afcbe0f]` `[7c27afd2db6f]` `[ff0f7ee210d7]`

**R133. Document the brand's journey from day one; the archive is a marketing asset and negotiating currency with partners who lack production capability.** Condition: any early-stage brand. Source 04 (an iPhone is enough; he regrets not doing it at his first company). Source 10 agrees (founder documentaries). `[19c209ab925b]` `[6573a73a2c17]` `[f4a424edb189]`

**R134. Pick 1 platform and 1 format and go all in; publish 3 to 4 niche pieces per 1 broad piece, and treat the ratio as a pendulum.** Condition: an organic channel with a defined buyer. Source 11 (one platform, one format). Source 08 (3:1 to 4:1, adjusted on view-to-buyer data). Source 07 agrees (Godin: 1 blog, no social). Source 04 disagrees mildly (multi-format across DTC, Amazon and retail), but that is product formats, not content. `[64a076c5bf54]` `[c4306d7bb6d7]` `[6ff737f56ea5]`

*R135 to R138 moved to Appendix A: video-hook structure, framework-building from a creator's own data, craft over metrics, and PR as fame (source 08, 11). Content mechanics already routed to 13-ORG and 10-MCR. Card ids: `[f608ae070ae4]` `[21b075fbec0d]` `[6d2e83617810]` `[389836501590]` `[bfb0f531453b]` `[d0a254b5a856]` `[59457b9fbb09]` `[b75dfff1cc41]` `[0bc28a1a4edf]`.*

**R139. Identify and over-invest in superusers who already advocate; fixed resources mean you cannot treat everyone better.** Condition: ambassador, UGC and review programs. Source 02 (watch behaviour, "adopt back" whoever is already leading). Source 04 agrees (a creator who posted daily for a year became a major driver and was hired). `[b1d6d86a7bc5]` `[a4515f778cd0]` `[f4a424edb189]`

**R140. Seed a few respected insiders where trust already exists to trigger a cascade; the specific headcounts (about 3 at TED, about 15 in a theatre) illustrate the mechanism, not a formula.** Condition: launch seeding in high-trust communities. Source 02. Source 04 agrees in practice (a collab with a running community opened New York). `[99309de7a12b]` `[37211e67c319]`

### Group I. Persistence, measurement and change

**R141. Positioning is cumulative: hold the same basic strategy for years and vary only tactics; change the creative when the accountant is tired of it, not when you are.** Condition: deciding whether to refresh creative, retire a tagline or abandon a channel. Sources 03 (Mailgram's volume fell after a late switch to "next-day delivery"; F.W.M.T.S.), 02 and 07 (Jay Levinson's accountant rule; a 5-year daily blog before readership), 11 (decades, not years; 1.1^100 is about 13,800). 4 sources agree. Conflict C9 with R148. `[74102b158e33]` `[c4d605d4c327]` `[a3b068db34cd]` `[440b65714a23]` `[6a08abe16376]` `[bcee1e69de76]`

**R142. Consistency is the promise; authenticity is for amateurs.** Condition: any customer-facing moment; the boundary is "don't do work you're not proud of, and don't burn out". Source 07 (the touring musician plays the hit). Source 02 agrees (emotional labour instead of striving for authenticity). Source 05 lists authenticity as a brand ideal but defines it as self-knowledge and keeping promises, which matches 07 more than it conflicts. Conflict C7 with source 11's weirdness. `[e1a3cf352d92]` `[a5326e07ad57]` `[7b89da87c95e]`

**R143. Classify every ad line as performance (ROAS, CAC) or brand (branded search lift, repeat rate); do not kill brand-building creative on a performance yardstick.** Condition: budget allocation. Source 02 (credited to Lester Wunderman). Conflict C4: sources 10, 03, 06 and 08 all measure brand work in some form. `[4a787df73c0a]` `[025ead1f1433]`

**R144. Track position movement with the same instrument over time: unaided awareness, per-attribute scores, correct category association, and the reorder curve; re-run 12 to 15 months later for a repositioning, 90 to 120 days after a name launch.** Condition: any positioning or naming program with a budget. Source 03 (Long Island Trust moved from last to first on 2 attributes in 15 months; United Jersey's unaided awareness "almost tripled" in about a year). Source 06 (post-launch tracking at 90 to 120 days). Source 10 (hook, hold, CTR, cohort retention). `[needs brand data: a research budget or a proxy]`. `[fcfff9855adc]` `[6355cdae1a6b]` `[d08af5a4ebfa]` `[b16d4573aa7e]`

**R145. Establish lifetime value before buying ads to build a position; if you cannot see the funnel, do not buy the ads.** Condition: setting acquisition budgets. Source 02. Hand the arithmetic to 06-MEA and 20-FIN. `[4c18bce6cf22]` `[f10089962425]`

**R146. If you cannot launch at full scale, overspend in one market, segment, cohort or channel, confirm the position is established, then repeat the identical claim in the next.** Condition: limited budget. Source 03 (geographic, demographic, chronologic and distribution rollouts; Marlboro on campuses; Wella through salons). Source 04 agrees (running first, then broader; Target, then Walmart, then CVS by month). `[d1ef31a9421a]` `[67d6adbf5558]` `[fa2b890e7de4]`

**R147. Get a second person for objectivity: positioning "is a game best played by two"; an outside facilitator lets the design lead hold the vision while someone challenges assumptions.** Condition: any positioning or identity program. Source 03. Source 09 (Ben Burns as outside facilitator). Source 05 (companies often need an outsider to articulate what is already there). A solo operator substitutes a structured written exercise and expects less challenge. `[6c449ac708b9]` `[0f1d54432687]` `[a85cb5eecad5]` `[12311750b25b]`

**R148. Locate the Dip before starting; if the resources and stamina to get through the hardest stretch are not there, do not start; quit early at the low-commitment point, never mid-dip.** Condition: under-resourced or unprepared projects; source 07's own qualifier is that this is not "every setback". Conflict C9 with R141. `[0f5eadcb74ad]` `[4408b6534f31]`

**R149. Separate decision quality from outcome when reviewing a positioning or naming bet.** Condition: retros. Source 07 (Annie Duke: a lottery win is still a bad decision). `[893fba99c769]`

**R150. Expect a chasm between early adopters and the mass market; the bridge is a real network effect or a local status ratchet, not hype.** Condition: category entry and expansion. Source 02 (Facebook school by school; LEED; Slack). Source 04 agrees that scaling a niche-community brand to mass is "genuinely hard" and rarely done. `[894eb8e32170]` `[bc48055c28ea]` `[a22d3c512164]` `[341ada6f7913]`

## 4. Procedures (implementation)

Each procedure states its goal, preconditions, steps with checks, and rollback. Steps the sources did not give are marked "pass 1 adaptation" or "this playbook's sequencing"; the agent should not present them as a source's method.

### P1. Positioning program (6 questions plus ladder plus XY plus promise)

Goal: a written positioning statement and map the brand can hold for years. Preconditions: product facts and provable claims from the brand record; customer language; a competitor set; a budget and runway answer from the user. Sources: 03 (6 questions, ladder), 02 (XY grid, promise), 09 (XY with out-of-category brands), 12 (4 strategy questions).

1. Write the category the way a customer says it, not the internal taxonomy. Check: the word appears in reviews or search terms `[needs brand data: on-site search terms and review language]`. `[d6bb004cc9ea]`
2. Map the ladder: ask real prospects to name brands in that category unprompted, in order. Record rungs 1 to 7 and who is missing. If no interviews are possible, use search volume and review mentions as a proxy and label the ladder "proxy" in the deliverable. Check: the brand's rung is stated, not assumed. `[d6bb004cc9ea]` `[e247ee27ad80]`
3. Answer question 1, "what position do we already own", from the marketplace, not the marketing team. Look one level up first: is the problem the category's or the place's share of mind, not the product's (Sabena, 7-Up)? `[e247ee27ad80]` `[6b46650fd04c]`
4. List every alternative the customer could choose, including other formats, marketplaces, DIY and doing nothing. `[cdddb1268ba4]`
5. Pick 2 axes people care about (source 02's menu in R12, or source 09's opposing-quality pairs). Plot every alternative, including out-of-category brands. Mark the crowded pool. Check: the brand is not sitting on top of competitors on both axes; if it is, change an axis pair or move. Re-run with at least 1 other axis pair. `[93e68a951096]` `[84c08bf1872c]`
6. Answer question 2, "what position do we want to own": one open rung or corner, not held firmly by anyone, not so broad it cannot be defended (Rheingold) and not so narrow it cannot sustain a business (Rolls-Royce). If no open slot exists, go to P3. `[e247ee27ad80]` `[15fe2dcc077a]`
7. Answer question 3, "whom must we outgun": name the competitor actually in the prospect's mind, and confirm the chosen claim does not contest the leader's exact claim head-on. `[78e52b831776]`
8. Confirm the brand can deliver the claim operationally (sourcing, service, returns) before it is written. If operations must change first, list the changes and their owners (United Jersey changed 7 things before advertising). `[6355cdae1a6b]`
9. Answer questions 4 and 5: is there enough money to establish and hold the position, and can the brand stick with it for years? If not, shrink the map (P16) rather than underspend everywhere. `[67d6adbf5558]` `[d1ef31a9421a]`
10. Write the 3-sentence promise: "My product is for people who believe ___. I will focus on people who want ___. I promise that engaging with what I make will help you get ___." Fill blank 1 with a belief from customer language, blank 2 with an aspiration they already pursue, blank 3 with a concrete transformation. `[25d09eedd419]`
11. Write the 1-sentence positioning statement: category as the customer says it, target by worldview, the single claim, and the leader or creneau it is positioned against or in. Pass 1 adaptation of source 03's ladder rule. `[526980d48d67]`
12. Check every claim word against the brand record (override 1). Mark any word that needs a `[web check]` (a "first", "only" or spec comparison).
13. Answer question 6: does the execution match? Read the current homepage hero, top PDP and lead ad against the statement. Flag any touchpoint with no connection to the promise. `[4c9bc44b263f]` `[bac208e763af]`
14. Run checklist 5.1. Deliver 9.1.
Rollback: a position not yet advertised can be redrawn at no cost; a position already advertised and working is not changed without a test (P2) and a stated reason (R141).

### P2. Test 2 positioning frames before committing (Mailgram and Long Island Trust methods)

Goal: choose between candidate frames on evidence. Preconditions: 2 plausible mental anchors; a research or media test budget `[needs brand data: budget]`. Source: 03.

1. Identify at least 2 anchors already in the mind (Mailgram: the Telegram vs first-class mail). `[9794ccdb926c]`
2. Write 1 distinct theme per anchor. Do not blend them.
3. For an awareness test: pick comparable markets or audiences; source 03 used 6 cities over 13 weeks. Measure unaided and aided awareness before and after in each; awareness change is the leading indicator, not short-term volume. Track the "cannibalised" product's volume too (Telegram volume held). `[9794ccdb926c]`
4. For a perception test: pick 4 to 6 attributes that matter in the category, add 1 or 2 the brand might uniquely win, and have prospects score every named competitor 1 to 10 on each. Build the position on the attribute the brand already wins, not the ones it is trying to fix (Long Island Trust was last on 4 attributes and first on 2 local ones). `[fcfff9855adc]`
5. Pass 1 adaptation: with no research budget, run the 2 frames as 2 ad creatives or 2 landing-page heroes and hand test design to 09-CRO; read the result as directional, since a click test measures response, not position.
6. Roll out the winning frame and hold it; re-run the identical instrument 12 to 15 months later and report movement per attribute. `[c4d605d4c327]`
Rollback: keep the pre-test creative; a frame that lost awareness (the "high-speed letter" frame fell from 27% to 25%) is retired.

### P3. Reposition the competition or the category when no open slot exists

Goal: move a competitor or the category's leaders out of the slot by changing what the prospect believes. Preconditions: a verifiable fact about the competitor's product or a voiced frustration the leaders share; legal review scoped. Sources: 03, 02 (tension), 08 (adjacency).

1. Study the competitor, not your own product (the Tylenol approach). Find the structural weakness the prospect will accept: an ingredient, an origin, a policy, a slowness, a shrinking pack. `[326a3dca9341]` `[4e43c308641d]`
2. If no single competitor is the target, name the frustration the category's leaders share and redefine the category around it (Milk Duds as "the long-lasting alternative to the candy bar"). `[babb616ba8a9]`
3. Write the claim as a specific, verifiable statement about the competitor's product or the category, never "we're better". Override 5: no competitor mark, copy or product image. `[web check: legal review of comparative claims per selling country]`. `[a57fe56ea376]`
4. Change operations first so the promise is true (R48). `[6355cdae1a6b]`
5. Check the tension-vs-fear line: the claim should create a resolvable pull, not a scare (R50). `[e1cc02e44a65]`
6. Check adjacency: what association does naming this competitor teach (R131)? `[357f0df4609a]`
7. Track unaided awareness and the competitor attribute scores with the P2 instrument.
Rollback: pull any claim a legal review or a `[web check]` fails; keep the against position (P1 step 6) as the fallback.

### P4. Premium positioning (3-step loop plus price-band decision)

Goal: a premium position that holds without discounting. Preconditions: product quality that survives first use (source 04: the first thing a customer does is open and use it); segment profiles from 02-AVT; promo history; category price band. Sources: 10 (3 steps), 04 (price band, pack, spec), 02 (price as signal, ten times question), 07 (Festool).

1. Psychology mapping per segment: what each segment values, aspires to, and what triggers its sense of exclusivity; split unaware from comparing. Write an aspirational identity statement per segment. Source 10 gives no interview script; use 02-AVT. `[9e9810f99d99]`
2. Choose the exclusivity angle: a narrative the competitors have not used, based on a provable product fact (R34, override 1). Not a stock-out. `[9e9810f99d99]`
3. Decide the price band: default inside the category's learned range (source 04); go above it only where the category is open to a premium band and the brand is first to claim it with a valid story (source 03's Michelob rule). Ask the ten-times question for any premium tier; reject "more of the same". Record the decision and the reason. Conflict C5 applies. `[563e8d7206aa]` `[7f129dfe890c]` `[b48af12fdcd2]`
4. If pricing inside the band, spend the difference on product, design and positioning: change only 1 to 2% of the known format; over-deliver on 1 measurable spec that is provable. `[43695ce04547]` `[32a728894b48]`
5. Write the marketing vector: core positioning, identity mirrored, story told. Write the spectrum of ad variance: formats, concepts and angles allowed. Write the promotional intensity rule in advance (source 10's illustration of "too much" is repeated 40 to 60% off). Hand discount structure to 03-OFF. `[c2131b88c294]`
6. Creative format: 15 to 30 second lifestyle mini-documentaries with real practitioners, a founder documentary if founder-led, 1 simple slogan; hand hook and production detail to 10-MCR. `[32c97afcbe0f]`
7. Instrument hook rate, hold rate, CTR and cohort retention next to ROAS; define which movements trigger iteration. No target values exist in the sources `[needs brand data: baselines]`. `[b16d4573aa7e]`
8. Run checklist 5.6 each quarter. Revisit the vector on a new category, not on 1 bad ad. `[7f0f81a9e158]`
Rollback: a premium claim that fails checklist 5.6 (for example, more than the agreed share of days on promotion) is a vector breach, fixed by the promo calendar, not by rewriting the vector.

### P5. Brand strategy workshop (attributes, values, promise, story, enemy)

Goal: the brand brief (9.2). Preconditions: business goals in writing; research from 02-AVT or at least reviews and support tickets; a facilitator or a structured written exercise (R147). Sources: 09 (4 lenses, How might we), 12 (4 questions, 3 to 5 values), 05 (4 inputs, ideals), 02 (promise, story, enemy), 04 (who it is not for).

1. Write the top-line business goals (source 09 wrote 4, including a 5-year revenue aim). `[5a833673f348]`
2. Answer the 4 strategy questions: why should people care, what makes us different, who are we speaking to, what are we trying to change. `[843d2f160b77]`
3. Run 4 separate brainstorms with focused prompts: values and beliefs; features and benefits; voice and tone; look and feel. Group into clusters; prioritise what resonates. Source 09 does not show its prompts. `[a85cb5eecad5]`
4. Fix 3 to 5 non-negotiable values. Check: each value can reject a real proposal (a mood board, a partnership); a value that rejects nothing is decoration. `[843d2f160b77]`
5. Write purpose, mission and vision in 1 sentence each. Check the vision against source 03's "5 to 10 years out" test. `[843d2f160b77]` `[78b60e028cb6]`
6. Write the 3-sentence promise (P1 step 10) and the big idea in under 6 words (Apple "Think different", Method "People against dirty"). `[5e39aa1931b9]`
7. Write the worldview statement: what the customer believed before we arrived and the assumptions they live by (R27). `[33a9a29e4bd2]`
8. Write the tension: what becomes less true for the customer if they do not act, stated without fear (R50). `[e1cc02e44a65]`
9. Write the enemy as a belief, a category habit or a competitor's verifiable behaviour, never a person (R51). Write who the brand is not for (R10). `[1956336eab48]`
10. Write 3 "How might we" challenges that will accept or reject later decisions. `[ee667d0641e8]`
11. Write the Story of Self, Us, Now for the About page and launch email (P16 covers voice). `[1d9f9a55d030]`
12. Score the whole brief against source 05's ideals (vision, meaning, authenticity, coherence, flexibility, commitment, value, differentiation, sustainability). A weak score is a reason to revise, not a numeric gate. `[50ae9056bb7a]`
13. Check every sentence against the brand record (override 1 and 2) and the reading level (override 4).
Rollback: the brief is versioned; a later change to values must state which decision it would have changed.

### P6. Naming project (full and compressed)

Goal: a naming shortlist with screens (9.3). Preconditions: the P5 brief, or at least product facts and customer language; selling countries; a trademark search route. Sources: 06 (process), 05 (types, qualities), 03 (sound, descriptive vs coined, initials).

1. Category audit: list every name in the category and its pattern; write the first hypothesis "we are not going there". `[0c6615eb4029]`
2. Product audit: the factual list of what is different. Buyer audit: why they buy, what they expect, the ultimate benefit up the ladder in their words (regularity becomes "feeling lighter"). `[0c6615eb4029]` `[6286b8c570e9]`
3. Answer the 4 questions: how do we define winning, what do we have to win, what do we need to win, what do we need to say. `[14751ff10cd0]`
4. Decide the naming brief's type mix on purpose from the 6 types (founder, descriptive, fabricated, metaphor, acronym, magic spell) and the budget: a small budget leans descriptive or metaphor (R60); a founder name only if the founder will stay the face (R69); initials never before fame (R66). `[449e6bdd1311]` `[b17d31320962]`
5. Generate in 3 briefs, not 1: full product story; the same with 1 altered or added detail; an unrelated domain (aviation, geology, sport). Mine roots, mythology, the periodic table and any cross-category archive. Suspend judgement; accept half-baked ideas. Agency scale: about 2,000 raw candidates over 2 cycles in 2 to 2.5 weeks. Small brand: scale the count down but keep the large-generation-before-selection ratio; run the 20-minute solo routine (pen and paper first; AI for questions about the subject, not for names) and a 30-minute read of unrelated material for a transferable metaphor. `[8d9104bffa0d]` `[4e009c4e7883]` `[3b6889a898c9]` `[d9c1184d1dd6]` `[3cd4209d8e57]`
6. Optional: bulk-generate 200 to 300 more candidates with an AI assistant as raw material only `[verify UI]`. `[bcf903029405]`
7. Score the long list with "no sevens" on: category-relative unexpectedness, processing fluency (pronounceable, partly understandable), sound (syllable count, initial letter), and multi-market legibility. Keep at least 1 candidate that splits the room. `[99647fecb304]` `[7bd3e22840b8]` `[9d81ed21b342]`
8. Legal and domain screen every survivor: trademark registers per selling country, domain and handle availability, common-law conflicts `[web check]`. Narrow to 10 to 15. `[4e009c4e7883]` `[87d34d6ea872]`
9. Language screen: pronunciation and connotation in every selling language; for China, dialect readings and early registration. `[web check]`. `[9e4834e83109]`
10. Run checklist 5.2 on the 10 to 15.
11. Build believability mock-ups for the top 2 to 3: a PDP header, an ad in its real placement, a pack, a search result. Mock-ups must not imply real coverage, endorsements or claims (override 1). Present in context, not as a spreadsheet. `[b7494c09d18d]`
12. On sign-off, deliver nomenclature, a positioning line and a short brand story with the name; if the name is benefit-led, write where the category word lives (subtitle, tags, metadata). `[a714872495ee]` `[6286b8c570e9]`
13. Track at 90 to 120 days: recall, correct category association, spelling and search errors. `[d08af5a4ebfa]`
Rollback: a finalist that fails the legal screen after mock-ups is dropped without appeal; keep the next 2 finalists warm until launch.

### P7. Name screen for a product, SKU or collection name (short form)

Goal: a name that survives search, speech and the shelf. Preconditions: brand name settled. Sources: 03, 05, 06. Pass 1 adaptation for the search step.

1. Does the name begin the positioning (benefit or job visible: Head & Shoulders, DieHard)? If not, does a subtitle carry the category word? `[526980d48d67]` `[6286b8c570e9]`
2. Shopping-list test: given only the brand plus this name, does a shopper know exactly what arrives? `[c4a8fdae883c]`
3. Bartender test: spoken aloud, is it ambiguous with another tier or SKU? If so, give the tier its own sayable name. `[03327dab7ce5]`
4. Sound test: syllables; does any abbreviation actually shorten it? `[7bd3e22840b8]`
5. Generic risk: could the public shorten it to a category word (Miller Lite)? `[5fffd494c3af]`
6. Protectable and positive in every market; domain or handle if it will have its own page `[web check]`. `[87d34d6ea872]`
7. Modular: does it fit the parent's naming pattern so the next SKU can follow it (R101)? `[c2dd2664000b]`

### P8. Rename decision and launch

Goal: a yes or no on renaming, and a launch plan if yes. Preconditions: current name's friction data (spelling errors, search misses, recall), legal status, company stage, equity audit. Sources: 06, 03, 05, 09.

1. Legal trigger check: is the name being challenged or blocking a market? If yes, the decision is made. `[fa435f935bc2]`
2. Friction check: hard to spell, hard to find, hard to recall, or a regional or dated meaning that keeps the brand in the wrong bracket (Eastern Airlines). `[needs brand data: search-term misspellings, branded search share, support mentions]`. `[fa435f935bc2]` `[86ea8f99ebef]`
3. Container check: can the name hold the new position (Volkswagen could not hold luxury)? `[e75b50392fca]`
4. Equity audit: what recognition does the name and mark already carry; what must be preserved (source 09 kept its logo). `[a913f3dfc742]` `[4469bf1ed068]`
5. Stage check: early-stage brands rename cheaply; a brand with deep equity needs a compelling reason. `[fa435f935bc2]`
6. Trigger classification from source 05: name change, revitalise the brand, revitalise the identity, integrate a system, merger. Scope the project to the trigger. `[f83b39ad5c0e]`
7. If yes: run P6, then launch with an explicit story ("we were here, now we're going this way, here is the benefit to you"), reassure customers the product is unchanged, and budget 6 to 9 months of extra resources for redirects, listings, packaging, assets and announcements. Position the new name against the future, not the past. `[fa435f935bc2]` `[defb93a85270]`
8. Track at 90 to 120 days (P6 step 13).
Rollback: if the friction case fails step 2, keep the name and fix the positioning line instead.

### P9. House name vs new name for a new product (line extension gate)

Goal: a decision on whether a new product carries the brand name, an endorsed sub-name or a new name, and whether to launch it at all. Preconditions: the shopping-list test on the current name; expected volume, competitive intensity, ad budget, significance, distribution; sales of the hero SKU. Sources: 03, 04, 05, 12. Conflict C1 applies; see section 7.

1. Shopping-list test today: given only the brand name, can a customer name exactly 1 product? If yes, the name has a position worth protecting. `[c4a8fdae883c]`
2. Teeter-totter check: is the new product the same job-to-be-done as what the name means today (a new flavour or format of the same job), or a different job (a supplement brand's skincare)? Same job: the name can stretch (source 04's halo; source 12's parent kit). Different job: expect the parent meaning to weaken. `[1aaf6ab34b2e]` `[17301f63a26b]`
3. Reverse extension first: can the goal be met by promoting a new use occasion for the same product and pack? `[3ca345f68121]`
4. Score the 5 rules of the road (volume, competition, ad support, significance, distribution) and weigh them together. `[e192263b85cc]`
5. Source 04's stage gate: size of prize, MOQ, margin, lead time, channel strategy, and an anchor customer with a committed launch window; do not press "go" with a manufacturer before it. Allow about 1 founder veto a year for a mission-grounding low-volume SKU. Hand the margin and MOQ arithmetic to 18-COG and 20-FIN. `[e175eacb2b24]`
6. Hero SKU check: has the hero reached the brand's own revenue bar before attention is diverted (source 04's bar was $10M, his category only `[needs brand data: the brand's own bar]`)? `[c842ee26e172]`
7. Architecture choice: monolithic (same name), endorsed (sub-name plus parent), or new name. Small brand default: monolithic unless the audience or price tier needs distance (R82). `[936a15cb7c7e]` `[a18c1c43a8c2]`
8. If the house name is used for a different job anyway, write the monitoring plan: reorder curve for 6 or more months (R81) and the shopping-list test repeated at 6 and 12 months. `[3c603945dca9]`
9. If a new name is used, budget real support for it; an unsupported new name underperforms a known name for a low-involvement purchase. `[4e20426232bb]`
Rollback: an extension whose reorders stall after the launch flash is withdrawn or renamed before it erodes the parent further.

### P10. Identity system build (marks, colour, type, photography, packaging, touchpoints)

Goal: the identity spec (9.4). Preconditions: the P5 brief and values; the decisive touchpoint named (R99); selling markets; equity audit of existing assets. Sources: 12 (sequence), 09 (stylescapes, type, colour, photo, site), 05 (cognition, mark criteria, architecture), 01 (claims, for tests only).

1. Equity audit: list every existing asset and decide keep, refine or replace, on equity, not taste (R87). `[a913f3dfc742]`
2. Reference gathering: collect visual references broadly (Pinterest, Behance, Cosmos named by source 12 `[verify UI]`); include packaging and display references for the decisive touchpoint. `[0060a896ab51]`
3. Build 3 genuinely distinct directions (mood boards or wide stylescapes across touchpoints), each with a written rationale. Present; score on team resonance and fit to the values; ask which elements to borrow across; merge into 1 locked direction. `[0060a896ab51]` `[3d381bacc1a4]`
4. Mark: decide the feeling; rule out category clichés; sketch in volume; filter each candidate for cultural reading per market `[web check]`; choose a mark type the recognition budget can afford (pictorial, wordmark or letterform for an unknown brand; no abstract mark or mascot on a small budget). `[c10449bf351d]` `[5b189a6b6181]` `[7b87514c30ba]`
5. Vectorise the chosen mark; clean proportions until it reads at favicon and label size with shape and colour alone (R91). Clear the 9 functional criteria (R93). Define the signature variants (horizontal, vertical, mark alone). `[01da2ffeccbe]` `[df0d1cef5653]` `[751a21990d7c]`
6. Typography by job: header, body, technical or spec copy, and any decorative face used selectively. Test in a specimen, then on 2 real sample pages with images and buttons. `[acd8f5a64996]`
7. Colour: 1 anchor colour tied to the brand theme plus a small accent set; review swatches across several sessions on both print proofs and screen. Add contrast checks `[web check: WCAG]` since no source gives a threshold. `[9b48715e763f]`
8. Photography rules: write 3 to 5 explicit constraints with reference images (light, tone, scene, people). Add the ecomOS constraint: colour-accurate real product photos for packaging, PDP hero and any accuracy-critical image; generated images may be used for mood only (override 6). `[8a3a065898f8]`
9. Texture, illustration and any secondary "alter-ego" layer: name it and keep it contained (R102). `[a913f3dfc742]`
10. Assemble the asset kit before applying it anywhere. `[01da2ffeccbe]`
11. First proof on the decisive touchpoint: for a physical product, the label and outer pack; for a site-first brand, sitemap then 2 placeholder pages. If it feels off, revisit the direction, not the layout. Test the pack at shelf or thumbnail distance for flavour, claim and colour legibility (source 04's rim and callouts). `[b3388c024bae]` `[c46421294324]` `[72056cea16a3]`
12. Parent and product split: write what the parent owns (values, type, palette, seal) and what each product owns (variant name, accent). `[c2dd2664000b]`
13. Optional sensory checks (P14) for scent, sound or weight decisions; these are claims tests, not requirements.
14. Run checklist 5.3. Deliver 9.4, then P12.
Rollback: keep the pre-rebrand asset kit intact and versioned until the new kit passes checklist 5.3 and the first proof.

### P11. Rebrand of a business that already sells (Double Diamond)

Goal: sequence a full rebrand with owners and artifacts. Preconditions: business goals in writing; several weeks for research. Source: 09, with 05 and 03 for keep-vs-change.

1. Discover: assemble CEO, marketing lead, design lead and an outside facilitator; write business goals; gather traffic, sales and survey data and run video interviews (method in 02-AVT); build personas by behaviour and required treatment, concentrating on segments the team does not know; map each persona's journey and its hurdles; run the 4 attribute brainstorms; build the XY map with out-of-category brands. `[a85cb5eecad5]` `[a04096752c25]` `[84c08bf1872c]`
2. Define: synthesise into a few named themes; decide what to discontinue; write 3 "How might we" challenges. `[ee667d0641e8]`
3. Develop: P10 steps 2 to 12, with the website as the forcing touchpoint if the brand is site-first. Draft voice collaboratively in a shared document over several passes. `[3cac34e1c33d]`
4. Deliver: guidelines (P12), site, packaging, content-capture capability, next product; change materials where the promise requires it (foam to molded pulp); roll out gradually; budget disproportionate time for the last 10%. `[1d643039b4fd]`
5. Translate the single strongest research insight (the moment customers say they connect) into 1 channel decision; label any ecommerce-only translation as an inference. `[a9b87b90a092]`
Rollback: since the logo and name are audited first (step 1 of P10), most rebrands can revert visuals while keeping the strategy work.

### P12. Brand guidelines and the brand voice sheet

Goal: a guideline document a new designer, writer or agent can work from without re-deciding basics (9.5) and a voice sheet the brand brain can load (9.6). Preconditions: P5 and P10 complete. Sources: 09 (4-part brand book), 05 (one-voice asset list, disclosure, crisis), 12 (values as filters), 02 and 03 (execution matches position). Source 05's guidelines chapter is missing from the excerpt, so the structure below is source 09's plus this playbook's sequencing.

1. Strategy page: positioning statement, promise, big idea, values, worldview, tension, enemy, who it is not for, the marketing vector and spectrum (if premium). `[c2131b88c294]`
2. Logo usage: signature variants, clear space, minimum size (the favicon test), what not to do, the equity note on why the mark was kept or changed. `[a913f3dfc742]`
3. Visual language: type by job with sizes, the anchor colour and accents with print and screen values and contrast notes, photography constraints with reference images, texture and illustration rules, the contained alter-ego layer if any, packaging rules for the parent and per-SKU elements. `[acd8f5a64996]` `[9b48715e763f]` `[8a3a065898f8]`
4. Language rules: nomenclature for every product and tier, taglines and descriptors, key messages (1 big idea, at most 3), vocabulary to use and avoid, boilerplate, elevator pitch, and ready messaging samples for PDP, ad, email and support. `[304f64fb3d93]` `[a5504e4a6a39]`
5. Brand expressions: the identity applied across surfaces as thought starters, labelled as not final. `[a913f3dfc742]`
6. Voice sheet (9.6): 3 to 5 voice poles (professional not corporate, friendly not fake, plus the brand's own), reading level rule (override 4), sentence-length and word-choice rules, banned words and jargon, spec-availability rule for research-heavy buyers, humour and tension limits, 6 to 10 before-and-after rewrites from real brand copy, and the override clause that this sheet beats any playbook default. `[3cac34e1c33d]` `[6aa0c57779c2]`
7. Claims register: the provable claims the brand may make, with their source in the brand record, and the claims it may not make (override 1).
8. Governance: who approves, how disclosure works for gifted and affiliate posts (over-disclose; disclose where the reader meets the content), do not delete negative comments, who declares a crisis and the first 3 statements prepared in advance. `[6c5906e5113f]` `[a9088311cadc]` `[15f1c9517cfd]`
9. Market variants: fixed vs adaptable elements per selling market. `[8462323ed8e5]`
10. Run checklist 5.4.
Rollback: guidelines are versioned; a change to any rule cites the decision that caused it.

### P13. Identity process for a small brand with no agency

Goal: a complete positioning, name, identity and guidelines set built by 1 or 2 people. This is the pass 1 adaptation of sources 05 (section 10 of its mini playbook), 06 (procedure B), 12 and 09, sequenced by this playbook. None of the sources tested it at small scale; source 12 is a 1-person freelance case and the closest evidence.

1. Week 1: P1 steps 1 to 13 using reviews, support tickets and search terms in place of interviews; a proxy ladder; 2 XY axis pairs. Write the promise and positioning statement. Get 1 outside person to challenge it (R147).
2. Week 1 to 2: P5 in a single working document: 4 questions, 3 to 5 values, purpose, mission, vision, big idea, worldview, tension, enemy, not-for, 3 How-might-we lines. Skip the facilitator; expect less challenge and compensate with the outside reader.
3. Week 2 to 3: P6 compressed (source 06 procedure B): 3 lenses instead of 3 teams, the 20-minute solo routine, the 30-minute outside read, "no sevens" scoring, trademark and domain checks before any finalist is shown, 2 to 3 believability mock-ups. Budget: source 06's agency fee is $75k to $150k; a small brand spends time plus a trademark search and legal opinion `[web check: cost of a trademark search and filing per selling country]`.
4. Week 3 to 5: P10 with a wordmark, letterform or simple pictorial mark; 3 mood boards; type by job with a free or licensed pair; 1 anchor colour and 2 to 3 accents; photography rules that lean on real product photos; first proof on the decisive touchpoint. Run the small-size test on day 1 of design; it costs nothing and is the highest-leverage check in source 05.
5. Week 5 to 6: P12 as a 6 to 10 page document plus the voice sheet and claims register; disclosure and crisis lines even at small scale.
6. Architecture: monolithic until a second real line needs distance (R82).
7. Skip: abstract marks, mascots, dynamic marks, sonic identity, multi-market adaptation (until a second market is real).
8. Persist: hold the position for years; track branded search and correct category association quarterly as the cheap proxy for awareness tracking (R144).
Rollback: every step produces a versioned file; nothing is printed or shipped until the first proof passes checklist 5.3.

### P14. Sensory congruence test (claims test from source 01)

Goal: decide whether to add a scent insert, a sound, a texture or a weight change to packaging or media. Preconditions: the candidate element and the current visual. Source: 01's "Pete's" method (20 subjects, 9-point scale, commissioned study; treat as a claim).

1. Present the visual alone to a small panel and record pleasantness 1 to 9. `[598a56fddd0e]`
2. Present the sensory element alone; record.
3. Present them together; record. Also test a deliberately mismatched pairing.
4. Adopt only a congruent pairing that scores above either element alone; drop any pairing that scores below either alone. `[20fbba1a4005]`
5. For a sound: separately measure liking of the visual alone vs visual plus sound; a sound that suppresses the visual is retired (the Nokia case). `[e519920226cf]`
6. Report the result as a panel read, not a finding; sample sizes this small do not support a claim on a client page.
Rollback: the visual alone is the default.

### P15. Audience-building and content system for brand

Goal: an owned audience and a content system that builds brand goodwill, with the ask kept honest. Preconditions: a chosen platform and format; the voice sheet; a permission channel. Sources: 02, 07, 08, 11, 04. Hand cadence, hooks and platform tactics to 13-ORG.

1. Remarkable test: write the exact sentence a customer would say to a friend about the product. If none exists, design a visible artifact, ritual or story that gives one; if that is impossible, plan paid acquisition and do not expect organic spread. `[800ade0c28a2]` `[141441a7be8f]`
2. Pick 1 platform and 1 format the founder or brand can sustain; check fit, not audience size. `[64a076c5bf54]` `[6ff737f56ea5]`
3. Set the give and ask rule for the brand: source 08's default is no CTA in organic, ask in paid and link in bio; a store with one-touch purchases may keep a light CTA (conflict C8). Record the choice and the metric that will judge it (paid performance before and after organic ramps) `[needs brand data]`. `[dd681a3febd1]`
4. Calendar: 3 to 4 niche pieces per 1 broad piece; adjust as a pendulum on view-to-buyer data. `[c4306d7bb6d7]`
5. Capture: 1 low-friction capture tool; weekly recent-past mining; occasional far-past lessons; rare manufactured pieces. Multiply each idea across formats. `[322c29135bc2]` `[9fae35015ed8]`
6. Founder plan: 1 to 3 themes; track customers arriving via founder content; write the handover date or the decision to stay the face. `[d5e25e56fca4]`
7. Permission: move every engaged viewer toward email or SMS; measure whether people would notice if the brand stopped showing up. `[b39a993e6adc]`
8. Judge by revenue and owned-audience growth, not views; allow some early awareness value. `[35873b25b23b]`
9. Show up for years; apply the accountant rule before changing anything (R141).
Rollback: if paid metrics do not move after the organic ramp, revisit step 3 before cutting the channel.

### P16. Roll out a position when the brand cannot launch at full scale

Goal: establish the position somewhere before spending everywhere. Source: 03, with 04 as a modern example.

1. Choose 1 rollout axis: geographic, demographic, chronologic (1 cohort ridden forward) or distribution (1 channel first). `[d1ef31a9421a]`
2. Overspend in that market or segment rather than underspending broadly. `[67d6adbf5558]`
3. Confirm the position is established (P1 step 2 re-run, or branded search share) before the next market.
4. Repeat the identical claim; do not re-invent the message per market. `[74102b158e33]`
5. Schedule the next channels on a calendar (source 04: Target, Walmart, then CVS and Walgreens by month). `[fa2b890e7de4]`
Rollback: a market where the position has not landed in the planned window gets more spend or a P2 test, not a new message.

## 5. Diagnostic checklists

Written so a worker can run each one without the sources. Each row: what to check, how, good, bad, fix, source.

### 5.1 Positioning statement review

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Category in the customer's words | Compare the category word to reviews and search terms | Same word customers use | Internal taxonomy or a coined category with no anchor | Rename the category or anchor it to the nearest known one ("the X without Y") | 03 `[d6bb004cc9ea]` `[92e5149e81d9]` |
| Ladder rung stated | The statement says whether the brand is first, an against position, or a new ladder | Rung is named with evidence (interviews or proxy) | Statement reads as if the brand were the leader when it is not | Re-run P1 step 2; adopt the against position | 03 `[ff2d9fce9f88]` `[6c5720ed9b21]` |
| One claim | Count the claims in the statement and the hero | 1 | 2 or more, or a "big, small, cheap, expensive" everybody claim | Cut to the one the brand can own and deliver | 03, 05 `[079c0cc5fa06]` `[a5504e4a6a39]` |
| Not head-on | Compare the claim to the leader's exact claim | Different rung or corner | Same claim as the leader | Go around, under or over (P3) | 03 `[78e52b831776]` |
| Open corner on the XY map | Plot every alternative on 2 axis pairs | Edge with few neighbours on at least 1 pair | Crowded middle on both | Change axes or move to an extreme the brand can deliver | 02, 09 `[cdddb1268ba4]` `[84c08bf1872c]` |
| Worldview, not demographic | Read blank 1 of the promise | A belief | An age, income or location | Rewrite from customer language | 02 `[cdc515a379b0]` `[3a3aa51fd789]` |
| Who it is not for | The statement or brief names the excluded group | Named | "Everyone" or silent | Add the not-for line | 03, 02, 04 `[32142fdf5893]` `[f97dfa662068]` `[1956336eab48]` |
| Not too narrow | Estimate whether total capture of the target sustains the business | Yes | No (Rolls-Royce thinking) | Widen by 1 step or pick a larger adjacent worldview | 03, 07 `[15fe2dcc077a]` `[0bc28a1a4edf]` |
| Deliverable in operations | List the operational facts behind the claim | Each fact exists or has an owner and date | Claim depends on something not yet true | Change operations first or change the claim | 03, 05 `[6355cdae1a6b]` `[9ff53840ee86]` |
| Claims proven | Check each factual word against the brand record | All traceable | A "first", "only", spec or origin claim with no proof | Remove or `[web check]` before use (override 1) | ecomOS; 04 `[341ada6f7913]` |
| Affiliation or dominion frame | Read the tone against customer language | Matches how customers talk | Brand talks winning, customers talk belonging (or the reverse) | Rewrite; run 2 variants for 2 segments if both exist | 02 `[bbfb0fef7597]` |
| Tension not fear | Read the hero aloud | A resolvable pull | A scare or manufactured scarcity | Remove the scare; make any deadline true | 02 `[e1cc02e44a65]` |
| Commodity-swap | Ask whether a switched customer would notice | Yes | No | Commit to a specific promise the competitor does not make | 02 `[dfa417998535]` |
| Money and patience | User has answered questions 4 and 5 | Budget and years stated | Unknown | Shrink the map (P16) or do not advertise the position yet | 03 `[67d6adbf5558]` |
| Execution matches | Read hero, PDP and lead ad against the statement | A stranger could infer the strategy | Clever creative hides the claim | Simplify until the ad restates the strategy | 03 `[bac208e763af]` |
| Reading level | Run a readability check | Below tenth grade | Above | Shorten sentences, simpler words, digits | ecomOS override 4; 05 `[6aa0c57779c2]` |

### 5.2 Name screen

Run on every finalist before it is shown as a finalist.

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Meaningful | Does it carry the benefit, the job or a surprising idea? | Yes | Empty, or only the category word | Climb the benefit ladder; keep the category word in secondary copy | 05, 06, 03 `[87d34d6ea872]` `[6286b8c570e9]` `[526980d48d67]` |
| Distinctive in the category | Compare to the category audit list | Breaks the category pattern | Matches "Fiber One, Fiber Plus" | Regenerate; do not use consensus as tiebreaker | 06 `[0c6615eb4029]` `[0db63ae1d97c]` |
| Tension zone | Poll 5 to 10 people with "no sevens" | At least some strong dislike and strong like | Uniform mild approval | Keep the polarising candidate on the list for the believability gate | 06 `[9d81ed21b342]` `[99647fecb304]` |
| Believable in under 1 second | Show in a PDP header or ad mock-up | "This could exist" | Reads as invented or as another kind of company | Rework or drop | 06 `[b7494c09d18d]` |
| Sound | Count syllables; read aloud; check the initial letter | Short, sayable; abbreviation only if it truly shortens | An abbreviation with no phonetic gain; hard to say | Use the shortest sayable full word | 03 `[7bd3e22840b8]` `[868f7e43ad95]` |
| Not initials | Is it an acronym? | No, or the brand is already famous | Yes, brand unknown | Use a word | 03, 05 `[dca1b04ea88b]` `[449e6bdd1311]` |
| Descriptive vs coined matches budget | Which type is it; what launch budget exists | Descriptive or metaphor on a small budget; coined only if first with a new product and funded | Coined name, small budget, crowded category | Pick a benefit-led real word (conflict C2 rule) | 03, 05, 06 `[b17d31320962]` `[9e3ddfa5cf56]` |
| Future-oriented and modular | Would it still fit in 5 years and on the next 3 SKUs? | Yes | Locks the brand to 1 product, place or era | Prefer the parent-level word; product words go in the SKU name | 05, 03, 12 `[87d34d6ea872]` `[dc9410d03a81]` `[c2dd2664000b]` |
| Generic risk | Could the public shorten it to a category word? | No | Yes (Miller Lite) | Change the descriptor or protect the mark differently | 03 `[5fffd494c3af]` |
| Protectable: trademark | Search registers in every selling country `[web check]` | Clear in the relevant classes | Conflict or a near-identical mark | Drop; do not present | 05, 06 `[87d34d6ea872]` `[4e009c4e7883]` |
| Protectable: domain and handles | Check the .com or the market's main TLD and the main social handles `[web check]` | Available or purchasable within budget | Taken by an active brand | Drop or budget the purchase | 05, 06 |
| Positive in every market | Pronunciation and connotation per selling language; dialects for China `[web check]` | No negative reading | A slur, a joke or a wrong-culture reading | Drop | 05, 06 `[9e4834e83109]` |
| Founder name only if founder stays | If it is a founder name, has the founder committed to remain the face? | Yes | No, brand meant to outlive founder | Use a non-founder name | 04, 05 `[7927ac1ccf6e]` `[449e6bdd1311]` |
| Visual | Set it in the candidate typeface at favicon and pack size | Reads | Awkward letterforms or too long | Adjust or drop | 05 `[87d34d6ea872]` |
| Shopping-list and bartender | Say the brand name alone; order it aloud | 1 clear product; no tier ambiguity | Diffuse or ambiguous | Separate names per tier | 03 `[c4a8fdae883c]` `[03327dab7ce5]` |
| Search anchor | If benefit-led, where does the category word live? | Subtitle, tags or metadata carry it | Nowhere | Add it | 06 `[6286b8c570e9]` |
| No invented claim in the name | Does the name itself assert a fact ("Organic", "No. 1")? | The fact is in the brand record | It is not | Drop the claim word (override 1) | ecomOS |

### 5.3 Identity system audit

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Strategy written before visuals | A brief with values exists and predates the mood boards | Yes | Visuals first | Stop; run P5 | 05, 12, 09 `[c4d91190801b]` `[843d2f160b77]` |
| Small-size test | Shrink the mark to favicon and app-icon size | Shape and colour alone identify it | Only the wordmark carries recognition | Simplify the mark; strengthen the shape | 05, 12 `[751a21990d7c]` `[01da2ffeccbe]` |
| 9 functional criteria | Score the mark on bold, recognisable, consistent, persona, protectable, enduring, cross-media, black and white, colour | All 9 | Any fail | Revise before aesthetics are argued | 05 `[df0d1cef5653]` |
| Mark type vs budget | Classify the mark | Pictorial, wordmark or letterform for an unknown brand | Abstract mark or mascot with no teaching budget | Replace with a mark that carries meaning | 05 `[7b87514c30ba]` `[1956b7a59e66]` |
| Cultural reading | Check each symbol and colour per selling market `[web check]` | Matches the intended story | Wrong-culture or cliché reading | Drop the symbol | 12, 05, 01 `[c10449bf351d]` `[8462323ed8e5]` `[b43f8160f55f]` |
| Category cliché | Compare the hero visuals to competitors | Distinct | Same tropes as the category (mountains for a Himalayan brand; 60 identical car ads) | New mental postcard | 12, 03, 01 `[ea573c35f69c]` `[8311a6869eb4]` |
| Palette structure | Count colours and roles | 1 anchor plus a few accents, validated on print and screen | Flat palette of equals, or screen-only approval | Re-review across media; add contrast checks | 09 `[9b48715e763f]` |
| Type by job | List each typeface and its job | Header, body, technical, decorative each assigned; tested on real pages | Chosen from a specimen only; decorative face overused | Re-test in context; restrict the decorative face | 09 `[acd8f5a64996]` |
| Photography rules | A written list with reference images exists | 3 to 5 constraints; real product photos where accuracy matters | Loose inspiration folder; grading that shifts product colour; generated product images on the PDP | Write the rules; reshoot accuracy-critical images (override 6) | 09 `[8a3a065898f8]` |
| Touchpoint coherence | Put logo, PDP, packaging, email and ad side by side | One company | Several companies | Reconcile to the asset kit | 05 `[e1cc915bc7d7]` |
| Flexibility | Mock the next SKU and the next channel with the kit | The kit stretches without breaking recognition | Every new SKU needs new design | Define parent vs product ownership | 05, 12 `[d658546a61ae]` `[c2dd2664000b]` |
| Decisive touchpoint gets the best execution | Name the touchpoint that decides the purchase | Best execution is there | Effort spread evenly | Reallocate | 12, 05 `[90bb50a21f09]` `[c383852eb750]` |
| Packaging at shelf or thumbnail distance | View at 2 metres or at 150 px | Flavour, key claim and colour code read instantly | Reads only close up | Add colour coding and callouts in the space you control (about 65%) | 04 `[72056cea16a3]` |
| Smashable (claim) | Cover the logo; show a fragment | Still identifiable (established brands) | Not identifiable; brand relies on the logo alone | Build 1 owned cue over time; not a requirement for a new brand | 01 `[b7da48474acd]` |
| Sensory additions tested | Any scent, sound or weight change ran P14 | Congruent pairing scored above either alone | Untested, or incongruent | Drop or test | 01 `[598a56fddd0e]` `[e519920226cf]` |
| Equity kept | List assets replaced and why | Replaced only where they blocked the position | Working assets replaced for taste | Restore | 09, 03 `[a913f3dfc742]` `[a3b068db34cd]` |

### 5.4 Brand guideline completeness

| Section | Present and usable? | If missing | Source |
|---|---|---|---|
| Positioning statement, promise, big idea | Yes, 1 page | Run P1 and P5 | 02, 05 `[25d09eedd419]` `[5e39aa1931b9]` |
| Values (3 to 5) and the 3 How-might-we lines | Each value can reject a real proposal | Rewrite until it can | 12, 09 `[843d2f160b77]` `[ee667d0641e8]` |
| Worldview, tension, enemy, who it is not for | Written as beliefs and behaviours, not people | Add | 02, 03, 04 `[33a9a29e4bd2]` `[e1cc02e44a65]` `[1956336eab48]` |
| Marketing vector and spectrum of ad variance (premium brands) | Media buyers and creators both cite it | Write it (P4 step 5) | 10 `[c2131b88c294]` |
| Promotional intensity rule | Stated in advance with a maximum depth and share of days | Add | 10 `[c2131b88c294]` |
| Logo usage: variants, clear space, minimum size, misuse, equity note | Yes | Add | 09 `[a913f3dfc742]` |
| Visual language: type by job, colour values for print and screen, contrast note, photography constraints with references, texture, alter-ego layer | Yes | Add | 09 `[acd8f5a64996]` `[9b48715e763f]` `[8a3a065898f8]` |
| Real-photo rule for accuracy-critical images | Stated | Add (override 6) | ecomOS; 09 |
| Packaging: parent elements vs per-SKU elements; untouchable regulated area | Yes | Add | 12, 04 `[c2dd2664000b]` `[72056cea16a3]` |
| Language rules: nomenclature, taglines, descriptors, key messages (max 3), vocabulary, boilerplate, elevator pitch | Yes | Add | 05 `[304f64fb3d93]` `[a5504e4a6a39]` |
| Ready messaging samples for PDP, ad, email, support | At least 1 each | Add | 09 `[a913f3dfc742]` |
| Voice sheet with poles, reading level, banned words, spec rule, rewrites, override clause | Yes | Build 9.6 | 09, 05, ecomOS `[3cac34e1c33d]` `[6aa0c57779c2]` |
| Claims register (allowed and forbidden claims with sources) | Yes | Add (override 1) | ecomOS; 05 `[9ff53840ee86]` |
| Brand expressions across surfaces, labelled as thought starters | Yes | Add | 09 `[a913f3dfc742]` |
| Architecture rule: when a sub-brand is allowed | Stated | Add (R82) | 05, 03 `[a18c1c43a8c2]` `[e192263b85cc]` |
| Market variants: fixed vs adaptable elements | Yes if more than 1 market | Add | 05 `[8462323ed8e5]` |
| Disclosure rules for gifted, affiliate and founder content | Yes | Add `[web check: rules per country]` | 05 `[6c5906e5113f]` |
| Crisis: who declares, first 3 statements, do not delete negative comments | Yes | Add | 05 `[a9088311cadc]` |
| Governance: approvers, version log, what triggers a change | Yes | Add | 09, 05 |
| Reading level | Guidelines themselves below tenth grade | Rewrite | ecomOS override 4 |

### 5.5 PDP and ad brand-consistency check

Run on any PDP, landing hero or ad before it ships. Layout belongs to 07-LPG and hooks to 10-MCR; this checklist is only the brand layer.

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Position inferable | Show the asset to someone unfamiliar for 5 seconds; ask what the brand stands for and what it reminds them of | Matches the positioning statement and the intended semiotic reading | Generic, dated, scam-adjacent, or a different claim | Simplify until the execution is the strategy; fix typefaces, photography and layout against the category's trust codes | 03, 02 `[bac208e763af]` `[b1ae1eab635d]` |
| Promise present | Find the X, Y or Z of the 3-sentence promise | At least 1 present and consistent | None | Rewrite the headline | 02 `[25d09eedd419]` |
| One big idea, up to 3 messages | Count messages | 1 plus up to 3 | More | Cut | 05 `[a5504e4a6a39]` |
| Voice sheet compliance | Read against the poles, banned words, reading level | Compliant; specs still available | Jargon, buzzwords, corporate tone, above tenth grade | Rewrite; keep specs in a lower section | 09, 05, ecomOS `[3cac34e1c33d]` |
| Claims match the brand record | Check every factual claim | All in the claims register | Any invented or unproven claim | Remove (override 1) | ecomOS |
| Vector compliance (premium) | Compare tone and offer to the vector and spectrum | Inside the spectrum; promo within the intensity rule | Off-brand concept or a deeper discount than allowed | Reject the concept or the promo | 10 `[c2131b88c294]` |
| Visual kit compliance | Logo variant, type, colour, photo rules | From the kit; real product photo where accuracy matters | Off-kit; stylised or generated product image on an accuracy-critical slot | Replace | 09, ecomOS `[8a3a065898f8]` |
| Not a category cliché | Compare to competitor creative | Distinct | Interchangeable | New visual or angle | 01, 03 `[8311a6869eb4]` `[ea573c35f69c]` |
| No competitor marks, text or products | Scan for any competitor asset | None | Present | Remove (override 5) | ecomOS |
| Comparative claims reviewed | Any named-competitor fact | Verified and legally reviewed | Not | `[web check]` before shipping | 03 `[a57fe56ea376]` |
| Sexual or shock hook | Is the hook sexual or shocking? | No, or brand recall was tested by variant | Yes, untested | Test recall or drop (claim) | 01 `[43f966448348]` |
| Tension not fear; scarcity true | Read the urgency lines | Real deadline or stock; resolvable pull | Fake scarcity or a scare | Remove | 02, ecomOS `[e1cc02e44a65]` |
| Affiliation or dominion match | Compare tone to the segment frame | Matches | Mismatch | Rewrite for the frame | 02 `[bbfb0fef7597]` |
| Co-brand or adjacency | Any second brand present | Load-bearing and on-brand association | Passive wallpaper or an association the brand does not want | Rework or remove (claim on recall suppression) | 01, 08 `[3bdf718b5a61]` `[357f0df4609a]` |
| Disclosure | Gifted, affiliate or paid | Disclosed where the reader meets it | Hidden in bio | Add | 05 `[6c5906e5113f]` |
| Same story as packaging and email | Compare the claim and look across the 3 | Same | Drift | Reconcile to the guidelines | 05 `[e1cc915bc7d7]` |

### 5.6 Premium signal audit

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Triad present | Read PDP, home and top ad for exclusivity narrative, aspirational identity, lifestyle story | All 3 | Features and price only | Write the missing leg | 10 `[6d7746b8892c]` |
| Exclusivity is narrative | Look for the angle | A competitor-untouched, provable angle | "Selling out", "limited stock" or discount urgency as the whole pitch | Reframe (R34) | 10, 04 `[9e9810f99d99]` `[3cdbc042d560]` |
| Segment triggers mapped | A per-segment map exists, split by awareness stage | Yes | One assumed trigger | Run P4 step 1 `[needs brand data]` | 10 `[9e9810f99d99]` |
| Price vs band | Compare price to the category band and the stated position | Inside the band with premium signals elsewhere, or above it with a valid story and first-mover claim | 2 to 3 times the band with no story, or a price that contradicts the XY position | Re-decide (P4 step 3) | 04, 03, 02 `[563e8d7206aa]` `[7f129dfe890c]` `[070a742b6c8b]` |
| Ten-times question answered | For any premium tier | A different story or scarcity | "More of the same" | Redesign the tier | 02 `[b48af12fdcd2]` |
| Promo cadence | Last 6 to 12 months of the promo calendar `[needs brand data]` | Occasional, inside the intensity rule | Frequent deep blanket discounts (source 10's illustration: repeated 40 to 60% off) | Reset against the vector; hand structure to 03-OFF | 10, 02 `[c2131b88c294]` `[19792f53199d]` |
| Sellout handling | Product type and stock history | Drops sell out by design; daily-use products do not stock out | A daily-use product repeatedly out of stock and marketed as a flex | Fix demand planning (18-COG); stop the flex | 04, 01 `[3cdbc042d560]` `[9ee51a3f9c3d]` |
| Format changed only 1 to 2% | Compare the container to the category norm | Familiar format, different liquid or design | Reinvented container in an established category | Return to the known format | 04 `[43695ce04547]` |
| Pack signals | Weight, texture, finish, callouts | Match the premium claim (claim: weight and touch signal quality) | Thin or cheap-feeling pack under a premium claim | Test with P14 or a pack proof | 01, 04 `[501ed81d0942]` `[72056cea16a3]` |
| Creative cast | Who appears in premium video | Real practitioners and community; founder if founder-led | Stock models or paid-model-only | Recast | 10, 01 `[32c97afcbe0f]` `[47ec35b97f3d]` |
| Scorecard | What the dashboard tracks | Hook rate, hold rate, CTR, cohort retention next to ROAS | ROAS and purchases only | Add the equity metrics `[needs brand data: baselines]` | 10 `[b16d4573aa7e]` |
| Trust through action | Refund, breach and delay behaviour | Matches the premium promise | Premium price with commodity service | Fix operations (R48) | 02, 05 `[e4fcc6c178a1]` `[9ff53840ee86]` |
| Borrowed authority real | Any award, list or certification cited | Independent and current `[web check]` | Self-made or expired | Remove (override 1) | 03, 05 `[2e309f07feea]` `[2abe90be27a4]` |

### 5.7 Line extension and architecture check (used inside P9)

| Check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Shopping-list test today | Brand name alone | 1 product | Diffuse | Stop extending; split architecture | 03 `[c4a8fdae883c]` |
| Same job or different job | Compare the new product's job to what the name means | Same job (flavour, format) | Different job | New or endorsed name | 03 `[1aaf6ab34b2e]` |
| Reverse extension considered | Could a new use occasion meet the goal? | Considered | Not | Try it first | 03 `[3ca345f68121]` |
| 5 rules of the road weighed | Volume, competition, ad support, significance, distribution | Weighed together with a written call | Skipped | Run P9 step 4 | 03 `[e192263b85cc]` |
| Stage gate | Size of prize, MOQ, margin, lead time, channel, anchor customer | All answered | Any missing | Do not press "go" | 04 `[e175eacb2b24]` |
| Hero SKU bar | Hero revenue vs the brand's own bar `[needs brand data]` | Reached | Not | Delay | 04 `[c842ee26e172]` |
| Reorder curve plan | Sell-in vs sell-through tracked 6+ months | Planned | Not | Add | 03 `[3c603945dca9]` |
| Parent vs product ownership written | The kit says what each owns | Yes | No | Write it | 12 `[c2dd2664000b]` |

## 6. Thresholds and benchmarks

One table for the folder. Confidence: "3 sources" means 3 mini playbooks state it independently; "single operator" means 1 practitioner's own practice or case; "unsourced" means the number is stated with no method. No number in this table is a validated ecommerce benchmark.

| Value | Condition | Source | Confidence |
|---|---|---|---|
| About 7 brands held per category in the mind; often 1 or 2 in a low-interest category | Ladder mapping | 03, citing George Miller | 1 source, borrowed from psychology; unsourced method for the brand count |
| 1 big idea, at most 3 key messages | Any page, pitch or press material | 05, adapted from Vincent Covello's risk work | 1 source; borrowed from another discipline; 03 and 11 agree on "one idea" |
| 3-sentence promise | Positioning statement | 02 | 1 source; template, not a measured threshold |
| 2 axes per XY map; re-run with other pairs | Positioning | 02, 09 | 2 sources agree on the method; axis choice is subjective |
| 6 positioning questions, answered in writing | Start of any program | 03 | 1 source; 12's 4 questions overlap |
| 3 to 5 non-negotiable core values | Brand brief | 12 | Single operator |
| 4 attribute lenses; 3 "How might we" challenges | Brand brief | 09 | Single operator |
| 9 (or 10) brand ideals | Judging any identity decision | 05 | 1 source; qualitative, no cutoff |
| 3 distinct creative directions before custom design | Identity build | 12, 09 | 2 single operators agree; both say it is habit, not an optimum |
| 2 placeholder sample pages before full site build | Site as forcing touchpoint | 09 | Single operator |
| 1 anchor colour plus a small accent set | Palette | 09 | Single operator; no contrast threshold given |
| 4 written photography constraints | Photo brief | 09 | Single operator; brand-specific |
| 9 functional mark criteria | Logo approval | 05 | 1 source |
| Shape, then colour, then words | Small-size recognition | 05 | 1 source; perception claim, no study cited |
| 7 naming qualities; 6 naming types; 5 tagline types | Naming | 05 | 1 source |
| Clients stall at 50 to 100 names; agency target about 2,000 raw candidates | Naming generation | 06 | Single operator |
| 2 generation cycles over 2 to 2.5 weeks | Agency naming | 06 | Single operator |
| 10 to 15 finalists after legal pruning | Naming | 06 | Single operator |
| Group brainstorming degrades past 4 to 10 people | Ideation | 06 | Single operator; author calls the study "sloppy and crude" |
| 20-minute solo naming session; 30-minute outside read; about 30% hit rate for a new angle | Naming | 06 | Single operator; hit rate is an estimate |
| 6 languages tested for BlackBerry | Multi-market name test | 06 | Single case |
| Naming fee $75k to $150k; up to $200k for large programs | Agency engagement, 2026-era | 06 | Single operator `[web check]` |
| Post-launch name tracking at 90 to 120 days | Naming and rename | 06 | Single operator |
| Rename executed in about 6 weeks (Kodium to Windsurf); 6 to 9 months of extra resources | Rename | 06 | Single case; single operator estimate |
| Initial-company awareness 49% vs name-company 68% | Argument against initials | 03's own survey | 1 dated study, unsourced method |
| Common English initial letters S, C, P, A, T; rarest X, Z, Y, Q, K | Name sound | 03 | 1 source; rough guide |
| Reorder curve watched 6 or more months after an extension; about $35 of stock per supermarket books $1M of first orders | Extension launch flash | 03 | 1 source; 1980 arithmetic |
| Price 2 to 3 times the category norm generally fails with the same shopper | Price band | 04 | Single operator |
| Change only 1 to 2% of a known format | Entering an established category | 04 | Single operator |
| About 35% of a regulated pack is untouchable | Packaging design space | 04 | Single operator estimate |
| Pack redesign reported to triple sales on the same liquid, 2 doors | Shelf legibility | 04 | Single case, self-reported, unverified |
| 3 can redesigns in about 300 days | Iterating pack on sell-through | 04 | Single case |
| Hero SKU at $10M revenue before the next flavour | Extension gate | 04 | Single operator, his category only |
| 1 SKU, 1 flavour for about a year before retailers asked for more | Launch focus | 04 | Single case |
| Retailer margin 45 to 50%; target gross margin 50%+; trade spend 20 to 30%; distributor 15 to 25% | Retail (out of scope here; see 18-COG, 20-FIN) | 04 | Single operator rules of thumb |
| Volume-tier creators about 99% of DTC revenue; elite athlete with 8,000 followers sold none; 400,000-follower creator did $20k on 1 swipe-up | Influencer tiers | 04 | Single operator, self-reported |
| Repeated 40 to 60% off damages premium identity | Promo intensity | 10 | Single operator's illustration, not a measured line |
| 15 to 30 second lifestyle mini-documentary | Premium video format | 10 | Single operator |
| Premium brands make buyers "want to pay 10 times the price"; Festool $220 vs about $25 | Premium multiple | 10, 07 | 2 opinions; illustrative |
| Hook rate, hold rate, CTR, cohort retention tracked next to ROAS | Premium measurement | 10 | 1 source; no target values |
| 1,000 true fans; famous to 1,500 people; 4 then 20 clients for a niche agency | Smallest viable market sizing | 02, 07 | 2 statements by the same author; 1 borrowed essay, 1 hypothetical |
| About 3 people at TED or about 15 in a theatre trigger a standing ovation | Seeding | 02 | 1 source; illustrative |
| 12% of about 21,000 Harry Potter reviews were 1 or 2 stars | Bimodal audiences are normal | 02 | 1 cited figure |
| JCPenney sales down more than 50% after ending coupons | Worldview mismatch | 02 | Single case |
| USHG prices up about 20% with no tipping | Naming who a change is for | 02 | Single case `[web check]` |
| Daily blog for 5 years before readership; 800 straight days of vlogging; 1.1^100 is about 13,800 | Persistence | 07, 11 | 2 single-operator anecdotes plus arithmetic |
| 40 million views and about $200 of sales | Vanity reach | 07 | Anecdote |
| No CTA in organic; ask in paid and link in bio | Give and ask | 08 | Single operator; conflict C8 |
| 3 to 4 niche pieces per 1 broad piece | Content calendar | 08 | Single operator; self-described pendulum |
| Promise, Proof, Path in the first 30 seconds; platform reads the first 3 seconds | Educational video open | 08 | Single operator; 35-video self-study |
| About $5,000 a month agency for cadence; 3 videos a week; 350 pieces a week at maturity | Content operations | 08 | Single operator; examples, not targets |
| 20% retention or CTR gain claimed to give about 100 times views | Quality power law | 08, attributed to MrBeast | Unsourced |
| 3 tasks a day; say no to 97% | Founder focus | 11 | Single operator |
| 1 platform, 1 format | Audience building | 11, 07 | 2 single operators agree |
| Several weeks of strategy; about 4 months to first deliverables; last 10% takes the most time | Rebrand timeline | 09 | Single case |
| Vampire Effect recall: men 9.8% vs about 20%; women 10.85% vs 22.3% (400 subjects) | Sexual creative | 01 | 1 cited study, not independently verified |
| Silk Cut 98% logo-free recognition | Smashable cues | 01 | 1 cited study, unnamed |
| Tiffany-blue box heart rate up about 20% (600 women) | Colour | 01 | Author's own test |
| Congruent sensory pairs score above either alone; incongruent below either alone (20 subjects, 9-point scale) | Sensory test | 01 | Author's commissioned study |
| Andrex about 2:1 over Kleenex on equal spend | Mascot as somatic marker | 01, citing Robert Heath | 1 secondhand account |
| Over 50% of point-of-sale decisions unconscious; about 90% of buying unconscious | Do not quote | 01 | Unsourced; the 90% is the author's synthesis and has been publicly disputed `[web check]` |
| 8 of 10 new products fail within 3 months (US) | Test before scaling | 01 | Loosely cited `[web check]` |
| Coke on screen about 60% of American Idol; Ford recall fell below baseline at $26M a year | Narrative integration | 01 | Author's SST study, about 400 subjects |
| 65 men in the brand-vs-religion scan; 14 religious leaders interviewed for the 10 traits | Religion-like brand traits | 01 | Small samples; no sampling method |

Moved to Appendix A: the Avis profit figures, the Protein 21, Pall Mall and Pringle's share-drop cases, the Rolls-Royce unit count, and the Mailgram and Long Island Trust tracking percentages. These are single 1960s to 1980s ad-agency case numbers, already backing rules elsewhere (R7, R76, R2, R11); kept as history, not a usable benchmark.

## 7. Where sources disagree

Each conflict: what each side says, when each is right, what the agent should do. Nothing here is averaged into a rule neither side stated.

**C1. Line extension never (03) vs hero SKU stretching (04, 12, 05, 09).** Source 03 says line extension "seldom works": one name cannot mean 2 different products (teeter-totter), and it lists Protein 21, Pall Mall, Scott, Xerox and Bayer as proof, while conceding GE and Vaseline Intensive Care as exceptions. Source 04 runs 13 SKUs under 1 brand in under 2 years with a deliberate halo (can, sachet, gel cross-selling) and gates each on an anchor customer and the hero's revenue. Source 12 designs the first product as a component of a parent kit meant to carry a full range. Source 05 lists "modular" as a naming quality and endorsed architecture as a normal option. Source 09 treats catalogue trimming as part of a rebrand. When each is right: 03 is right when the new product is a different job-to-be-done (a supplement brand's skincare line, a coffee brand's apparel drop); its cases are all category jumps. 04, 12 and 05 are right when the new SKU is the same job in a new flavour, format or occasion for the same customer. What the agent should do: run P9. Same job: stretch under the master brand with the parent-vs-product split and the source 04 gate. Different job: run the 5 rules of the road and default to an endorsed or new name, with the reorder curve monitored for 6 or more months. Never present either side's era numbers as a forecast. `[1aaf6ab34b2e]` `[17301f63a26b]` `[c2dd2664000b]` `[e192263b85cc]`

**C2. Abstract or benefit-led name (06) vs descriptive keyword name (03, 05, common SEO practice).** Source 06 argues comfortable, descriptive names ("Ready Mop", "Fiber Plus", "Natural Farms") only confirm what the category already means and carry no differentiation; it pushes toward surprising, benefit-adjacent names (Swiffer, Impossible, Azure). Source 03 says descriptive names beat coined ones for most launches because they carry meaning at zero teaching cost and block me-toos; coined names are justified only for a first-in-mind new product. Source 05 lists both types with their trade-offs and warns fabricated names need education spend. When each is right: 06 is right at the brand level for a funded launch in a category full of descriptive names; 03 and 05 are right for product, SKU and collection names, for small budgets, and for search-driven commodity categories. What the agent should do: at brand level, generate across both types, keep at least 1 tension-zone candidate, and choose by budget and category audit (P6 step 4). At product and collection level, default descriptive (P7). Whatever the brand name, keep the category word visible in the subtitle, tags and metadata (source 06's own resolution). Hand search-title rules to 15-SEO. `[6286b8c570e9]` `[b17d31320962]` `[449e6bdd1311]`

**C3. Logo-first identity (05, 12, 09) vs smashable cues and mascots (01, 02).** Sources 05, 12 and 09 build the identity around a mark that clears functional criteria, reads at small size and is protected; 09 kept its logo for its equity. Source 01 argues logo-free cues can outperform the logo once a code exists, that "smashable" fragments mark the strongest brands, and that an odd mascot builds a somatic marker cheaply; it also contradicts itself by praising Apple's and Nike's symbols. Source 02 says logos matter less than designers claim: pick a workable one and keep it. When each is right: 05, 12 and 09 are right for any new or low-awareness brand, which has no code to be free of (source 01 says this itself in its condition). 01's smashable test is right as an aspiration for an established brand and as an audit of whether recognition rests on the logo alone. 05 is right that mascots need a redraw budget and a voice. What the agent should do: build the mark first under R91 to R93; run the smashable check as a claim-based audit only for established brands; propose a mascot only with a redraw budget and a P14-style test; never claim brain-scan support on a client page. `[751a21990d7c]` `[b7da48474acd]` `[177aa8d4c957]` `[1956b7a59e66]`

**C4. Measure brand marketing (10, 03, 06, 08) vs refuse to measure (02).** Source 02 states Wunderman's binary: direct marketing measures everything; brand marketing must be patient and refuse measurement, and if you cannot afford patience, do not buy brand ads. Source 10 tracks hook rate, hold rate, CTR and cohort retention as brand-equity signals; source 03 tracked unaided awareness and per-attribute scores over 12 to 15 months; source 06 runs a 90 to 120 day tracking study after a name launch; source 08 checks paid performance before and after organic ramps. When each is right: 02 is right that brand spend must not be killed for lacking a CAC in the first quarter and that internal boredom is not a signal. The others are right that position movement can be measured with the right instrument over the right window. What the agent should do: classify every line as direct or brand (R143); for brand lines, set the measurement in advance as awareness, attribute scores, branded search share, correct category association and cohort retention on a 90-day to 15-month window, and forbid ROAS-only kills of premium concepts (R39). Hand instrument design to 06-MEA. `[4a787df73c0a]` `[b16d4573aa7e]` `[fcfff9855adc]` `[d08af5a4ebfa]`

**C5. Discounting (03-OFF neighbour, 03's low-price creneau, 02's JCPenney case) vs premium protection (10, 02, 04, 07).** Source 10 says repeated deep discounts (its illustration: 40 to 60% off) damage premium identity; source 02 says "cheap is another way to say scared" and that lowering price does not build trust; source 04 keeps price inside the band but refuses to compete on it; source 07's Festool sells at about 10 times a commodity. On the other side, source 03 lists low price as a valid creneau for unproven new products, source 02's JCPenney case shows that removing coupons from bargain-hunting true fans cut sales by more than 50%, and the 03-OFF playbook designs discount-led offers. When each is right: premium protection is right for a brand actively building or holding a premium position; discounting is right where the brand's worldview segment shops as a sport (Bargain Bill) or where the category has trained buyers to expect it. What the agent should do: decide the position first (P1, P4 step 3), then write the promotional intensity rule into the vector before any promo calendar is drawn; a premium brand's discounts are occasional and structural (bundles, thresholds) and are designed in 03-OFF within that rule; a value brand's discounts are part of its story and are not treated as a breach. Fixed-offer brands such as Peach Bucket get presentation fixes, not new discounts (03-OFF rule). `[c2131b88c294]` `[19792f53199d]` `[7f129dfe890c]` `[3a3aa51fd789]`

**C6. Audience comes last (11) vs voice of customer (01, 02, 03, 06, 07, 09, 12).** Source 11 says build from your own taste in the creation phase, that the audience "only knows what's come before", and that surveys and focus groups should not drive conception (Rick Rubin, Steve Jobs, the Henry Ford line). Every other source starts from the customer: 03 maps the ladder from prospects; 02 fills the promise with customer language; 06 runs a buyer audit; 09 spent weeks on interviews before any exercise; 12 profiles the audience first; 07 watches who lights up; 01 weights revealed behaviour. When each is right: 11's own cards scope it to how an identity, voice or creative concept is originated, and say it is not a licence to skip research, pricing tests or post-launch data. 01's point that stated preference misleads is a caution about survey wording, not a licence to ignore customers. What the agent should do: research before positioning (P1, P5, P11 Discover) using revealed behaviour and customer language; allow taste-led originality in the creative direction step (P10 step 3) and the naming tension zone (R64); then test in market. Never use "the audience comes last" to defend an untested claim. `[d0a254b5a856]` `[3a3aa51fd789]` `[0c6615eb4029]` `[b6e70f8909c7]`

**C7. Authenticity (05, 11, 01) vs consistency (07, 02, 03, 05).** Source 11 makes weirdness the root of authenticity; source 05 lists authenticity as a brand ideal; source 01 says real people beat polished models. Source 07 says "authenticity is for amateurs, consistency is for professionals": customers want the version they were promised, not the bad day. Source 02 says perform emotional labour instead of striving for authenticity; source 03 holds the same position for years; source 05 defines authenticity as self-knowledge and keeping promises, which is closer to consistency than to self-expression. When each is right: authenticity as "a distinctive point of view and real people" is right for differentiation and casting; consistency is right for service, voice and delivery. What the agent should do: encode the distinctive point of view once, in the brief and voice sheet, then deliver it consistently; a founder's mood never changes the promise; "authentic" never excuses an off-voice post or an unproven claim. `[e1a3cf352d92]` `[a5326e07ad57]` `[59457b9fbb09]` `[7b89da87c95e]`

**C8. Give-only content (08) vs a CTA on every post (common practice; 10; 02; 04).** Source 08 strips every direct CTA from organic content and moves the ask to paid ads and the link in bio, saying CTAs "kill reach"; its own card notes stores with one-touch purchases may not see the same payoff and lose direct attribution. Source 10 lets conversion ads be "more aggressive" inside the vector; source 02 designs tension and relief at every step, including asks; source 04's founder content is tracked by customers it brings in. When each is right: 08 is right for a longer consideration cycle and a business that runs paid alongside organic; the others are right where the post is the shop window and purchase is one tap away. What the agent should do: record the give-and-ask rule per brand in the guidelines (P15 step 3), default to soft asks in organic (link in bio, a product mention without hard sell), keep hard CTAs in paid, and judge the choice by paid performance before and after the organic ramp. Hand cadence and mechanics to 13-ORG. `[dd681a3febd1]` `[c2131b88c294]` `[25f6ebc5c073]`

**C9. Quit sooner (07's Dip) vs persist (02, 07's own accountant rule, 03, 11, 05).** Source 07 says "most people quit too late, they don't quit too soon" and to not start what you cannot finish. The same source, and 02, 03, 11 and 05, say to hold a position for years, change creative only when the accountant is tired of it, and expect a "dip" between your boredom and the audience's absorption. When each is right: 07's Dip rule is scoped to under-resourced or unprepared projects and to quitting at the low-commitment point before starting or early in; the persistence rules apply to a resourced position that has been established and is being held. What the agent should do: run the Dip check before a new brand initiative (P1 step 9, P5 step 1); once a position is launched with the budget and years answered, do not change it on internal fatigue; the only mid-course exits are a failed P2 test, a legal problem, or the runway running out. `[0f5eadcb74ad]` `[440b65714a23]` `[74102b158e33]`

**C10. Sellout as a signal: good (01, 10) vs bad (04).** Source 01 treats seasonal withdrawal and invitation-only access as anticipation builders; source 10 cites drop-based releases as exclusivity built into the operating model. Source 04 calls a stockout on a daily-use product "terrible": it breaks the habit, no one is loyal through it, and a retailer will replace the brand. When each is right: drops and seasonal scarcity are right for apparel, collabs and limited editions with true limits; the daily-use rule is right for consumables and replenishment products. What the agent should do: classify the product; permit scarcity only where it is true (override 1) and where the product is not a habit; for consumables, treat any stockout as an operations failure and never as marketing. `[9ee51a3f9c3d]` `[32c97afcbe0f]` `[3cdbc042d560]`

**C11. Hits vs the smallest viable market (02 with itself).** Source 02 argues for depth over reach and then says someone will be the hit machine and "if you can find a playbook, go for it". What the agent should do: default to the smallest viable market for every brand in ecomOS; treat a hit-machine plan as a user decision that needs a named playbook and budget, and flag it as the exception. `[b5df5fe9a17d]` `[b3bfbcca02fe]`

**C12. Narrow the position (03, 02, 07) vs not too narrow (03, 07).** Source 03 demands sacrifice and warns of "Rolls-Royce thinking" in the same book without a formula for width; source 07 gives the 2 bounds (too narrow to sustain, too broad to be anything but a commodity). What the agent should do: state both bounds in the positioning statement review (5.1) and size the target with the brand's own numbers `[needs brand data: revenue needed and the target's plausible size]`; when in doubt, start narrow and widen by 1 step (R19's one-step rule, P16's rollout). `[15fe2dcc077a]` `[0bc28a1a4edf]`

**C13. Founder as the face (04, 10, 05) vs remove the founder and never name the brand after them (04).** Source 04 uses the founder as the early face, tracks it, plans to remove himself, refused his own name, and still calls Kith's founder-forever model valid. Source 10 makes founder documentaries the storytelling beacon; source 05 lists founder names as a type with real protection advantages. What the agent should do: ask the user for the founder's horizon (input table); if the brand must outlive the founder's visibility, do not use a founder name and write the handover date; if the founder will stay the face, a founder name and founder-led content are allowed and the personal brand follows the same guidelines. `[7927ac1ccf6e]` `[d5e25e56fca4]` `[449e6bdd1311]`

**C14. Revealed behaviour only (01) vs survey-based positioning research (03, 06).** Source 01 says surveys mislead and brain measures predict better; its own study has a vendor stake and small samples. Source 03 built its bank cases on semantic-differential surveys and awareness tracking; source 06 tests names in 6 languages with panels. What the agent should do: use both, with the roles separated: surveys and panels for vocabulary, attribute scores and awareness; order data, repeat rate and search terms for what people do; never resolve a conflict between them by quoting a neuroscience figure. `[b6e70f8909c7]` `[fcfff9855adc]` `[99647fecb304]`

**C15. Stylised photography (09) vs product accuracy (ecomOS).** Source 09's photo rules ask for warm tones and subtle film grain and note the risk to colour accuracy. ecomOS override 6 wins: mood imagery may be graded; accuracy-critical images use colour-accurate real product photos. `[8a3a065898f8]`

## 8. Common mistakes

Merged from all sources and deduplicated, each with the fix.

1. Starting visuals before strategy is written; approval turns into a taste fight. Fix: P5 before P10 (05, 12, 09). `[c4d91190801b]`
2. Conflating the logo with the brand. Fix: R89; audit the whole system, not the mark (05, 12, 09, 02). `[1c1a35e393b7]`
3. Trying to change what is already in the prospect's mind. Fix: work with the ladder and the worldview (03, 07). `[079c0cc5fa06]`
4. Attacking the leader head-on. Fix: against position, creneau or repositioning (03, 02). `[78e52b831776]`
5. Confusing a factory gap with a mind gap. Fix: R9, P9 (03, 04). `[47ce0c7f290e]`
6. Appealing to everyone. Fix: the not-for line and the smallest viable market (03, 02, 07, 04). `[32142fdf5893]`
7. Picking a grandiose, unresourceable change, or reverse-engineering a "change" story with buzzwords to defend an existing product. Fix: R127 (02). `[8ed5982aa5df]`
8. Imposing the founder's or team's worldview on customers who hold a different one (JCPenney). Fix: customer language before decisions (02). `[3a3aa51fd789]`
9. Running "we're better than X" comparative ads instead of changing what the prospect believes about X. Fix: P3 (03). `[a57fe56ea376]`
10. Making a claim, a "first" or a spec comparison the brand cannot prove. Fix: override 1; the claims register (ecomOS; 04's admitted unknown competitor numbers). `[8d0d1d8f914c]`
11. Letting a placeholder name become permanent; believing "I'll know it when I hear it" or "we can't afford to test". Fix: P6 (06, 05). `[24a1ee273847]` `[87d34d6ea872]`
12. Choosing a safe consensus name because it tested as comprehensible. Fix: tension-zone shortlisting; comprehension is not differentiation (06). `[0db63ae1d97c]`
13. Choosing initials before fame, or a coined name on a small budget in a crowded category. Fix: R66, R60 (03, 05). `[dca1b04ea88b]`
14. Stopping name generation at 50 to 100 candidates, or killing ideas in the room. Fix: P6 step 5 (06). `[3b6889a898c9]`
15. Skipping trademark, domain and language checks until after creative and stakeholder investment. Fix: screen before finalists (05, 06). `[4e009c4e7883]`
16. Naming a brand after a founder who plans to step back. Fix: C13 (04). `[7927ac1ccf6e]`
17. Line-extending a strong name onto a different job and mistaking the launch flash for demand. Fix: P9, the reorder curve (03). `[3c603945dca9]`
18. Assuming a famous name gives a new product a free ride. Fix: R80 (03). `[46df3117bf9a]`
19. Adding SKUs before the hero has proved itself. Fix: the source 04 gate (04). `[c842ee26e172]`
20. Replacing a logo or asset that already carries equity. Fix: equity audit first (09, 05, 03). `[a913f3dfc742]`
21. Abandoning a working position for an aspirational or fresher one (Avis "going to be number 1"; Mailgram's "next-day"). Fix: R141 (03). `[a3b068db34cd]`
22. Changing creative because the team is bored, not the audience. Fix: the accountant rule (02, 07). `[440b65714a23]`
23. Underspending across many markets instead of overspending in one. Fix: P16 (03). `[67d6adbf5558]`
24. Choosing an abstract mark or a mascot on a small budget, or a mascot with no redraw plan. Fix: R92, R109 (05). `[7b87514c30ba]`
25. Relying on the wordmark alone for recognition; failing the small-size test. Fix: R91 (05, 12). `[751a21990d7c]`
26. Using category-cliché symbols or symbols with the wrong cultural reading. Fix: R94 (12, 03, 05, 01). `[c10449bf351d]`
27. Choosing type from a specimen alone; overusing a decorative face; approving colour on one medium. Fix: R96, R97 (09). `[acd8f5a64996]`
28. Photography grading that misrepresents the product; generated product images where accuracy matters. Fix: override 6, R98 (09, ecomOS). `[8a3a065898f8]`
29. Spreading identity effort evenly instead of on the decisive touchpoint. Fix: R99 (12, 05). `[90bb50a21f09]`
30. Designing a pack that looks good online and fails at shelf or thumbnail distance. Fix: R41 (04). `[72056cea16a3]`
31. Treating coherence as rigid standards that block creativity, or letting "flexibility" become inconsistency. Fix: R102, R101 (05). `[e1cc915bc7d7]`
32. Simplifying voice by deleting the specs research-heavy buyers need. Fix: R103 (09, 05). `[3cac34e1c33d]`
33. Treating exclusivity as a stock-out; marketing a consumable's stockout as a flex. Fix: R34, C10 (10, 04). `[9e9810f99d99]`
34. Running frequent deep discounts against a premium position; killing premium concepts on ROAS alone. Fix: the intensity rule, R39 (10, 02). `[c2131b88c294]`
35. Assuming every segment shares the same exclusivity trigger. Fix: R35 (10). `[9e9810f99d99]`
36. Lowering price to earn trust on a high-ticket item. Fix: R33 (02). `[e8ed1256772e]`
37. Buying a sponsorship or placement without narrative integration, or appearing next to an association the brand does not want. Fix: R122, R131 (01, 08). `[0fdfce48d0e0]`
38. Using sexual or shock creative without testing brand recall. Fix: R120 (01). `[43f966448348]`
39. Adding a sound or scent without testing it against the visual alone. Fix: P14 (01). `[e519920226cf]`
40. Transplanting a ritual, number or colour across cultures unchanged; overt single-faith symbolism. Fix: R94, R108, R123 (01, 05). `[b43f8160f55f]`
41. Trusting stated preference over revealed behaviour when they conflict, or quoting the "90% unconscious" figure. Fix: R111, R112 (01). `[b6e70f8909c7]`
42. Chasing views and followers that do not convert; assuming all publicity is good. Fix: R129, R131 (07, 08). `[35873b25b23b]`
43. Hard CTAs in every organic post, or no path to purchase at all. Fix: C8 (08). `[dd681a3febd1]`
44. Dabbling across platforms and formats. Fix: R134 (11, 07). `[64a076c5bf54]`
45. Building a referral program with no incentive, no tension and no status story (HugDug). Fix: R53 (02). `[9db7234804f8]`
46. Copying a famous tactic without its cohort dynamics (a gala, a viral stunt). Fix: R140 (02). `[2b7413eac695]`
47. Skipping to "spread the word" before steps 1 to 3. Fix: R126 (02, 07). `[1a1c714f09a8]`
48. Starting a demanding brand initiative without the runway for its hardest stretch. Fix: R148 (07). `[0f5eadcb74ad]`
49. Letting a bad day or a founder's mood change the promised experience. Fix: R142 (07). `[e1a3cf352d92]`
50. Deleting negative comments; hiding a commercial relationship in a bio; writing the crisis plan after the crisis. Fix: R110 (05). `[6c5906e5113f]`
51. Measuring a rebrand by strategy documents rather than shipped artifacts, and underestimating the last 10%. Fix: R107 (09). `[1d643039b4fd]`
52. Copying a competitor's name, mark, text or product "for reference". Fix: override 5 (ecomOS).

## 9. Deliverables

Each deliverable states what the agent produces and the format. All are written below tenth-grade reading level, cite the brand record for every claim, and carry `[needs brand data]` and `[web check]` tags where inputs are missing.

### 9.1 Positioning statement and map
- 1-sentence positioning statement: category in the customer's words, target by worldview, the single claim, the leader or creneau it stands against or in.
- The 3-sentence promise (R20).
- The ladder: rungs 1 to 7 with the evidence source (interviews or proxy) and the brand's rung.
- 2 XY maps (2 axis pairs) as simple tables or an SVG, every alternative plotted, the crowded pool marked, the chosen corner marked.
- The 6 answers (own, want, outgun, money, years, execution) in 1 line each.
- The not-for line and the affiliation or dominion frame.
- Checklist 5.1 result with any open `[web check]`.
Format: Markdown, 1 to 2 pages, saved under `brands/<brand>/`.

### 9.2 Brand brief
- Business goals; the 4 strategy answers; purpose, mission, vision; 3 to 5 values with 1 example each of a proposal the value would reject; big idea; promise; worldview; tension; enemy (as belief, habit or verifiable behaviour); who it is not for; the 3 How-might-we lines; Story of Self, Us, Now; ideals score with notes.
- Premium brands: the marketing vector, the spectrum of ad variance, the promotional intensity rule, the price-band decision and its reason.
Format: Markdown, 2 to 4 pages.

### 9.3 Naming shortlist with screens
- The category audit (names and their pattern), the product audit, the buyer audit, the 4 answers.
- The long list count and the 3 lenses used.
- 10 to 15 finalists (fewer for a small brand), each with: type, "no sevens" scores on unexpectedness, fluency, sound and market legibility; trademark status per selling country `[web check]`; domain and handle status `[web check]`; language readings `[web check]`; checklist 5.2 result.
- 2 to 3 believability mock-ups (PDP header, ad in placement, pack, search result), labelled as mock-ups with no implied endorsement or claim.
- For the recommended name: nomenclature, positioning line, short brand story, where the category word lives, and the 90 to 120 day tracking plan.
- For a rename: the P8 decision record and launch story.
Format: Markdown table plus image files.

### 9.4 Identity spec
- Equity audit (keep, refine, replace, with reasons).
- The 3 directions with rationales and the merged, locked direction.
- Mark: files in vector, signature variants, small-size proof, the 9-criteria score, the cultural-reading check per market.
- Type by job with sizes; anchor colour and accents with print and screen values and contrast notes; photography constraints with references and the real-photo rule; texture and any contained secondary layer.
- Parent vs product ownership table for packaging and SKUs.
- First-proof images on the decisive touchpoint and the shelf-or-thumbnail legibility result.
- Checklist 5.3 result.
Format: Markdown plus asset folder.

### 9.5 Brand guidelines
- The P12 structure: strategy page; logo usage; visual language; language rules with samples; brand expressions; architecture rule; market variants; disclosure and crisis lines; governance and version log; claims register.
- Checklist 5.4 result.
Format: Markdown (6 to 10 pages for a small brand) plus the asset kit; a PDF export if the user asks.

### 9.6 Brand voice sheet for the brand brain
- 3 to 5 voice poles with a 1-line definition each.
- Reading-level rule, sentence-length rule, digit rule, no em dashes, banned words and jargon, allowed technical terms and where specs live.
- Humour, tension and urgency limits; the give-and-ask rule for organic.
- 6 to 10 before-and-after rewrites from real brand copy.
- The claims register or a pointer to it.
- The override clause: this sheet beats any playbook default; the brand record beats this sheet on facts.
Format: Markdown, 1 to 2 pages, saved so the brand brain can load it with the brand record.

### 9.7 Brand-consistency audit report (PDP, ad, email or pack)
- Checklist 5.5 rows with pass, fail, fix and owner; the 5-second stranger read; a list of any claims removed and why.
Format: Markdown table.

### 9.8 Premium signal audit report
- Checklist 5.6 rows with pass, fail and fix; promo cadence summary from the data layer; the equity metrics baseline where available.
Format: Markdown table.

### 9.9 Full-funnel touchpoint audit
- Walk the funnel touchpoint by touchpoint: search result, PDP, cart, checkout, shipping email, unboxing, support.
- Mark each touchpoint functional or experiential; flag any touchpoint with no connection to the brand promise.
- Uses R155. Not covered by 9.7, which is the PDP and ad layer only.
Format: Markdown table.

## 10. What needs live data or a web check

**Needs brand data**
- Unprompted category ladder from real prospects, or the proxy (on-site search terms, review mentions, branded search share). (P1, R3)
- Customer language: reviews, support tickets, UGC, search terms, to fill the promise, worldview and voice. (R11, R20, R27, P5)
- Provable claims list and forbidden claims. (override 1, P12 step 7)
- Product facts and what is provably different. (P6 step 2, R8)
- Price points, category price band, margin. (R31, P4 step 3)
- Promo calendar history: depth, frequency, share of days on promotion. (checklist 5.6)
- Sales by SKU, hero SKU revenue vs the brand's own bar, repeat rate, cohort retention. (R79, P9 step 6, R39, R144)
- Reorder curve after any extension, 6 or more months. (R81)
- Revenue needed and the plausible size of the target, for the narrow-vs-too-narrow bounds. (C12)
- Budget and years available to hold the position; research budget for P2. (P1 step 9, P2)
- Selling countries and languages. (R70, R94, R108)
- Founder's horizon as the face; customers arriving via founder content. (C13, R132)
- Which touchpoint decides the purchase. (R99)
- Paid performance before and after an organic ramp; view-to-buyer split by content type. (P15 steps 3 and 4)
- Baselines for hook rate, hold rate, CTR and cohort retention. (P4 step 7)
- Repeat rate for customers exposed to a ritual-style onboarding vs not; PDP video vs static conversion; brand recall by creative variant. (R114, R115, R120; all claims tests)
- Existing content archive and founder footage. (R133)
- Search-term misspellings and branded search share, for a rename case. (P8 step 2)

**Web check**
- Trademark registers per selling country for every finalist; domain and social handle availability. (R70, checklist 5.2)
- Pronunciation and connotation per selling language; Chinese dialect readings and early registration. (R70, P6 step 9)
- Cultural readings of symbols, colours and numbers per market. (R94, R108, R116)
- Competitor set, claimed positions and price points for the ladder and XY map. (P1 steps 4 and 5)
- Legal review of any comparative or named-competitor claim per selling country. (R13, P3 step 3)
- Disclosure rules for gifted, affiliate and founder content per country. (R110)
- Any borrowed authority (award, list, certification) is independent and current. (R17, checklist 5.6)
- WCAG contrast ratios for the palette, since no source gives a threshold. (R96)
- Cost of a trademark search and filing per country for a small brand. (P13 step 3)
- Post-2008 critiques of source 01's methods and the "90 percent unconscious" figure before any of its numbers are repeated. (group G)
- Dated cases before they are quoted to a client: Uber surge pricing and USHG's no-tipping policy (02); Gatorade's 2025 revenue and competitor sodium levels (04); Packard, Chanel and Nespresso campaign dates (10); Nvidia, Michael Jordan and the iPhone button story (11); Mode's packaging shipment (09); guest identities in 06, 08, 10 and 11.
- Current AI assistant capabilities for bulk name generation `[verify UI]`. (R72)
- Reference-gathering and vector tools named in 12 (Pinterest, Behance, Cosmos, Illustrator) `[verify UI]`.

## 11. Freshness and stale-risk notes

| Area | Risk | Re-verify |
|---|---|---|
| Neuroscience claims (group G) | Source 01 is 2008, small samples, vendor stake, no peer review; its own 2012 election forecast failed; the "90%" figure is disputed. Nokia, Cingular and MySpace-era examples no longer exist as described | Before any claim leaves the playbook for a client page: `[web check]` the critique literature; treat every rule in group G as a hypothesis to test with brand data, every time |
| 1960s to 1980s positioning cases (03) | Every share, dollar and awareness figure is 40+ years old, pre-internet, 3-network US; comparative-ad law history is era-specific; some named brands no longer exist | Never quote the numbers as current; the mechanisms (ladder, creneau, teeter-totter, 6 questions) are timeless and need no re-check |
| 2010s cases (02) | Uber surge, USHG no-tipping, RapCaviar, Facebook's early loop and the "60% of advertisers measure" figure may have changed | `[web check]` each before use; yearly |
| Trademark and domain tooling | Registers, classes, fees and search tools change; AI-assisted clearance tools appear and disappear; domain markets shift | `[web check]` per naming project; never reuse a clearance older than 90 days |
| AI naming tools | Source 06's assistant use and "Predict" scoring reflect a 2026-era snapshot; assistant capabilities change monthly | `[verify UI]` per project; keep the judgement framework (5.2) in-house so tool changes do not change the screen |
| Naming fees and timelines (06) | $75k to $150k and 2 to 2.5 week cycles are 1 agency's 2026 numbers | `[web check]` before any budget decision |
| Design tools and reference sites (12, 09) | Illustrator, Pinterest, Behance, Cosmos, Notion features change | `[verify UI]` per project |
| Platform names and rules (05, 08, 11) | Twitter is X; character limits, YouTube guidance, app-store categories and disclosure rules have all changed since 2013 | `[web check]` before citing; hand platform mechanics to 13-ORG |
| Retail and CPG numbers (04) | Margins, trade spend, distributor cuts and the $10M hero bar are 1 founder's 2025 to 2026 figures in 1 category | Out of scope here; 18-COG and 20-FIN own them |
| Premium creative format (10) | 15 to 30 second mini-documentaries and hook and hold metric definitions depend on platform reporting | `[verify UI: metric definitions on the ad platform]`; 10-MCR owns formats |
| Consumer-law and disclosure rules | Comparative claims, gifted-post disclosure and "first" or "only" claims are regulated differently per country | `[web check]` per selling country per campaign; yearly refresh in the guidelines |
| Sources' own identities | Presenters in 06, 08, 10 and 11 are unnamed or inferred | `[web check]` before attributing a quote to a named person |
| Brand records | Voice sheet, claims register and guidelines override this playbook and must be re-read on every task | Every run |

24 Sep 2026: ecommerce specificity pass applied from ECOM_REVIEW.md; priority block added, 14 rules reworded, 8 levers added, about 580 words moved to Appendix A.

## 12. Source index

Each mini playbook: number, title, type, credibility and bias, what it contributed most.

| No. | Title | Type | Credibility and bias | Contributed most |
|---|---|---|---|---|
| 01 | Buyology (Martin Lindstrom, 2008) | Book | Low as evidence, useful as a hypothesis list. A branding consultant, not a neuroscientist, reporting his own commissioned $7M fMRI and SST study (2,081 subjects across 5 countries, but 20, 12, 10 and 65 subjects in the key sub-studies), with no peer-reviewed publication, endnotes to news articles, and a direct financial stake through his neuromarketing firm BUYOLOGY INC. Its "90% unconscious" figure and small-N method have been publicly disputed. Its 2012 forecast failed. Never mentions ecommerce; all PDP and unboxing mappings are pass 1 adaptations | Group G claims: sensory congruence, smashable cues, rituals, somatic markers, mirror neurons, the Vampire Effect, co-brand recall suppression, the sonic-asset warning, stated vs revealed preference. P14 |
| 02 | This Is Marketing (Seth Godin, 2018) | Book | Medium as a framework, low as evidence. Influential practitioner synthesis with no controlled experiments; numbers are illustrations or single named cases; several cases are dated (Uber, USHG). No ecommerce content; all store mappings are pass 1 adaptations. Same author as 07 | Smallest viable market, worldview segmentation, the 3-sentence promise, the XY grid, affiliation vs dominion, tension not fear, price as signal, permission assets, brand vs direct measurement, the accountant rule, Story of Self, Us, Now |
| 03 | Positioning: The Battle for Your Mind (Ries and Trout, 1981) | Book | Medium for mechanisms, low for numbers. Two agency principals selling their own doctrine through their own case work (Avis, Mailgram, 2 banks) and unverified pop-business anecdote; absolute claims ("second is nowhere", "line extension seldom works") are contradicted by durable exceptions the book itself concedes. Every figure is 40+ years old and pre-internet. No ecommerce; mappings are pass 1 adaptations | The ladder, first in mind, the against position, cherchez le creneau, factory vs mind creneau, the everybody trap, repositioning vs comparative ads, naming rules (descriptive vs coined, sound, initials, generic risk), the teeter-totter, the shopping-list and bartender tests, the 5 rules of the road, the 6 questions, holding a position, rollouts |
| 04 | Premium Isn't About Price, It's About Positioning (podcast, CPG founder) | Transcript | Low. One second-time founder (Cadence, formerly Daring) with entirely self-reported numbers, 2 paid sponsor reads (one with a host investment disclosure), an admitted "I just lied" tactic with a manufacturer, and competitor figures he admits he does not know. Heavily physical-retail; most of its retail content belongs in 18-COG and 20-FIN | Premium inside the price band, change 1 to 2% of the format, state who it is not for, pack for the shelf, SKU stage gate and hero bar, founder as early face then removed, do not name after the founder, document from day one, influencer tiers and brand-fit veto, non-competitive collabs, stockouts as failure |
| 05 | Designing Brand Identity (Alina Wheeler, 4th ed., 2013), excerpt | Book excerpt | Medium for vocabulary, thin for process. A trade reference by a brand strategist with dozens of named agency contributors; no experiments or sales data; Part 1 only, so the research, brand brief, design execution, touchpoint and guidelines chapters are missing; platform specifics are a decade stale. The small-brand mapping in its mini playbook is a pass 1 adaptation | Brand vs identity, the 3 brand jobs, 9 ideals, shape-colour-form, mark types and the recognition budget, 9 functional criteria, 7 naming qualities and 6 types, tagline types, 1 idea and 3 messages, brand architecture, coherence and flexibility, cross-cultural adaptation, disclosure and crisis checklists |
| 06 | We named a billion dollar startup with the guy that named BlackBerry, Febreze and Swiffer (podcast) | Transcript | Medium for process, low for numbers. A naming-agency founder (unnamed in the transcript; portfolio matches Lexicon's David Placek) presenting his own case portfolio, an internal study he calls "sloppy and crude", a proprietary tool no one else can use, and 2026-era fees; hosts run a business podcast. A stray 21-OPS routing note sits in the raw export | The naming process (audits, 4 questions, 3 lenses, 2,000 candidates, tension zone, no sevens, believability mock-ups, legal pruning, 90 to 120 day tracking), the rename procedure, sound symbolism claims, AI for generation and judgement in-house |
| 07 | Marketing Godfather: How To Build An Audience That Buys (Seth Godin interview) | Transcript | Low as evidence, consistent with 02. Anecdotes and hypotheticals (the orthodontist agency), transcription errors in names, an unreliable Birkin price, sponsor reads excluded. Same author as 02, so it does not count as an independent second source | The remarkable test, visible-artifact test, vanity reach, consistency over authenticity, the Dip, decision vs outcome, practical empathy, copy a proven model |
| 08 | Building a brand, but it's on easy mode instead (workshop talk) | Transcript | Low. Unnamed presenter matching Alex Hormozi; self-reported analytics; a lead-gen and course orientation; a contestable "you can't be cancelled" opinion; several garbled names. Its give-and-ask rule is framed for longer consideration cycles | Give vs ask separation, brand as behaviour-changing association with 3 axes, adjacency, Promise Proof Path, niche-to-broad ratio, framework from own outliers, agency then in-house |
| 09 | Building a Brand: Redesigning a Business Start to Finish (Mode rebrand) | Transcript | Medium for process, none for outcomes. One first-party, Shopify-sponsored case (2025) with a Shopify Capital pitch excluded; no revenue or lift numbers; every number is one company's choice | The Double Diamond rebrand sequence, XY map with out-of-category brands, 3 stylescapes, type by job, anchor colour, written photography rules, jargon-free voice, personas by behaviour, sitemap plus 2 sample pages, the 4-part brand book, delivery artifacts, the last 10% |
| 10 | The Psychology of Premium Branding (talk) | Transcript | Low. Unnamed presenter closing with a "book a call" agency pitch; claims 50+ stores scaled with no names; one client case (Slate Swim) self-reported; brand histories retold without sources; one example is a scripted TV scene (Mad Men) | The premium triad, exclusivity as narrative, psychology mapping by segment and awareness stage, the marketing vector and spectrum, promo intensity decided in advance, mini-documentary creative with real practitioners, equity metrics next to ROAS |
| 11 | The psychology of building a brand everyone loves (talk) | Transcript | Low. Unnamed narrator matching creator Matt Gray; top-of-funnel for a paid personal-brand offer; borrowed celebrity anecdotes with `[web check]` on each; no ecommerce content by its own header | Consistency compounding, obsession over craft, "audience comes last" scoped to creation, weirdness as edge, radical simplicity, one platform one format, deep not wide |
| 12 | How to Design a Brand Identity, From Start to Finish (freelance case) | Transcript | Medium for sequence, none for outcomes. One freelance designer's single project (a chili oil brand), sponsor read for Contra excluded; numbers (3 to 5 values, 3 directions) are stated as habit | Strategy before visuals with 4 questions, values as filters, 3 distinct directions, semiotic filtering of symbols, sketch volume, vectorise and systemise before applying, packaging as first proof, parent-brand scaling, the decisive touchpoint, branding as ongoing perception |

**Neighbour folders and what lives there.**
- 01-PRD-product-research: what to sell and product-market signals; source 10 routes pricing elasticity there.
- 02-AVT-avatars: interview scripts, surveys, persona research; sources 09, 10 and 12 route audience research there.
- 03-OFF-offers: bundles, discounts, guarantees, thresholds; owns discount structure inside this playbook's promotional intensity rule (C5); its own "category of one" is a different framework from source 10's phrase.
- 06-MEA-measurement: attribution, LTV and incrementality; owns the instruments for R143 and R144.
- 07-LPG-landing-pages: page layout and wireframes; source 09 routes site design there.
- 09-CRO-testing: A/B design and significance for any positioning, colour or creative test.
- 10-MCR-paid-social-creative: hooks, formats, hook and hold benchmarks; source 10's video format and source 08's Promise Proof Path detail live there.
- 11-ADC-ad-copy-deployment: ad copy from the brand voice sheet.
- 13-ORG-organic-and-content: posting cadence, platform tactics, the give-and-ask mechanics from source 08 and the content system from source 11.
- 14-EML-email-lifecycle: the permission asset from R128.
- 15-SEO-search: title and collection naming for search, which interacts with C2.
- 17-CXP-post-purchase: unboxing, rituals and retention programs built from group G claims.
- 18-COG-sourcing and 20-FIN-finance-and-accounting: MOQ, packaging cost, retail margins, demand planning from source 04.
- 21-OPS-team-and-management: hiring, agencies, facilitators and freelance platforms from sources 04, 08 and 12.
- 24-DEP-ad-deployment: account work; Meta stays read-only.

## Appendix A. General background

Content here was demoted from section 3 or section 6 by the 24 Sep 2026 ecommerce specificity pass (ECOM_REVIEW.md, section 5). It is history, case detail or a claim not actionable enough for the working rules, kept for reference and traceability, not as something an agent should run.

### A.1 R123: brand-vs-religion 10-trait checklist

From R123, Group G (brand psychology claims).

Claim: strong brands show brain patterns "almost identical" to religious icons in one 65-man study, and the author lists 10 traits (belonging, clear vision, power over enemies, sensory appeal, storytelling, grandeur, evangelism, symbols, mystery, rituals) as an audit for aspiring premium brands. Condition: an established or aspiring premium brand; not a checklist a new, low-trust brand should force. Avoid overt single-faith symbolism (Lego's advent calendar backlash). Source 01 only; the trait list came from 14 interviews with no sampling method. `[992d9678d728]` `[2f826d11d900]` `[f951cfe57e4e]` `[6118970e983c]`

### A.2 R121: sonic-asset and Nokia ring-tone test

From R121, Group G (brand psychology claims).

Claim: a signature sound can go negative through overexposure and drag the visual brand down with it; test the visual alone against visual plus sound before adopting any sonic asset. Condition: notification sounds, jingles, unboxing sounds. Source 01's Nokia ring-tone case (3 of 4 tested pairings gained; Nokia's suppressed liking). `[3c9b9d4f6d00]` `[2c808611a9bb]` `[e519920226cf]` `[774df5ca9ac9]`

### A.3 Case detail moved from R66, R80 and R83

From R66 (Group D, naming): Source 03's own Business Week survey found 49% awareness for initial companies vs 68% for name companies, a 1 dated study.

From R80 (Group E, brand architecture): Source 03's Alka-Seltzer Plus case: it cannibalised Alka-Seltzer; Life Savers gum failed while the same company's Bubble Yum, a new name, outsold Life Savers candy.

From R83 (Group E, brand architecture): Source 03's P&G case: P&G launched Tide, not "Ivory Detergent"; an era claim that P&G did about 2 times Colgate's business and 5 times its profit.

### A.4 Section 6 case numbers: 1960s to 1980s ad-agency figures

From section 6, Thresholds and benchmarks. Already backing rules elsewhere (R7, R76, R2, R11); kept as history, not a usable benchmark.

- Mailgram: 23% to 47% awareness (winning frame) vs 27% to 25% (losing frame), 6 cities, 13 weeks. Source 03, single case, authors' own data.
- Long Island Trust: last to first on 2 attributes in 15 months; United Jersey unaided awareness "almost tripled" in about 1 year, earnings up a reported 26%. Source 03, single cases, authors' own accounts.
- Avis profits $1.2M, $2.6M, $5M in 3 years after the number 2 line. Source 03, single case, 1960s.
- Protein 21 share 13% to 2%; Pall Mall 14.4% to 3.8%; Pringle's 18% to 10%. Source 03, single cases, authors' accounts, 1960s to 1970s.
- Rolls-Royce about 1,000 US cars a year, about 0.01% of the market. Source 03, 1 dated figure.

### A.5 R135 to R138: video and PR craft rules

From Group H (audience building and content for brand). Already routed to 13-ORG and 10-MCR; little left specific to store brand strategy.

**R135.** Open educational content with Promise, Proof, Path in the first 30 seconds; give every short cut its own hook. Condition: educational video for brand; entertainer content differs. Source 08 (from his own top 35 videos). Hand hook benchmarks to 10-MCR and 13-ORG. `[f608ae070ae4]` `[21b075fbec0d]`

**R136.** Build a named framework from your own outlier data: list what every top example does, keep only what nearly all share, and package it with alliteration or an acronym. Condition: a signature methodology or content system. Source 08 (35 videos gave Promise, Proof, Path; 20 low-churn gyms gave 5 shared actions). The result is a hypothesis, not a proven cause. `[6d2e83617810]` `[389836501590]`

**R137.** Obsess over the craft, not the metrics; build from your own taste in the creation phase, then let the market test it. Condition: originating a brand's identity, voice or creative concept; not a licence to skip research, pricing tests or post-launch data. Source 11 ("the audience comes last", scoped by its own cards to the creation phase; lean into your weirdness). Conflict C6. `[bfb0f531453b]` `[d0a254b5a856]` `[59457b9fbb09]`

**R138.** Aim to be famous to the smallest viable audience, and reframe PR as telling your story to the right people rather than chasing ink. Condition: PR and reach strategy. Source 02 ("everyone is famous to 1,500 people"). Source 07 agrees (an agency serving only pediatric orthodontists needs 4 proven clients, then 20; hypothetical). `[b75dfff1cc41]` `[0bc28a1a4edf]`

