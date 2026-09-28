# bombas: brand card (T0)
Identity: Bombas runs a giving model where one pair purchased equals one pair donated.
Diagnosis: Comfort basics brand, 457 million dollars. Three pressure points to test: durability complaints undercut the premium price, the price objection sits on Amazon, competitors own buy-it-for-life.
Red lines: none recorded
Top claims:
- [site_backed, 2026-09-28, 0 days old] bombas.claims.ankle_socks_benefit: Bombas ankle socks are described as moisture-wicking with a blister tab, a cushioned footbed and its Honeycomb Arch Support System.
- [site_backed, 2026-09-28, 0 days old] bombas.claims.calf_socks_benefit: Bombas calf socks are described with extra-long staple cotton, stay-up technology, an invisitoe, a y-stitched heel and the Honeycomb Arch Support System.
- [site_backed, 2026-09-28, 0 days old] bombas.claims.donation_exclusion: Bombas states that a replacement or exchange item does not trigger an additional donation.
- [site_backed, 2026-09-28, 0 days old] bombas.claims.donation_pledge: Bombas states that for every item purchased it donates one item, always and forever.
- [site_backed, 2026-09-28, 0 days old] bombas.claims.guarantee_promise: Bombas Happiness Guarantee claims it will do everything it can to make a purchase right if the customer is not happy.
Current promos: none recorded
Freshness: all records in date

## Sections

| Section | Records | Last update | Gist |
|---|---|---|---|
| [identity](identity.json) | 11 | 2026-09-28 | Bombas runs a giving model where one pair purchased... |
| [diagnosis](diagnosis.json) | 9 | 2026-09-28 | Comfort basics brand, 457 million dollars. Three... |
| [story_bank](story_bank.json) | 23 | 2026-09-28 | Bombas pitched on Shark Tank in the Season 6 premiere,... |
| [voice](voice.json) | 3 | 2026-09-28 | Bombas repeats the same donation tagline word for word... |
| [visual](visual.json) | 16 | 2026-09-28 | Bombas main stylesheet defines a black color token named... |
| [products](products.json) | 30 | 2026-09-28 | Bombas sells a digital gift card in denominations from... |
| [offers](offers.json) | 10 | 2026-09-28 | Bombas offers free standard shipping on US orders of 75... |
| [policies](policies.json) | 10 | 2026-09-28 | Bombas accepts returns for a refund within 30 days of... |
| [claims](claims.json) | 6 | 2026-09-28 | Bombas ankle socks are described as moisture-wicking... |
| [avatars](avatars.json) | 13 | 2026-09-28 | Cold Weather Wool Sock Loyalist: warm, durable socks for... |
| [objections](objections.json) | 42 | 2026-09-28 | Compression socks are too hard to pull on, sit too high... |
| [objection_ladders](objection_ladders.json) | 7 | 2026-09-28 | Comfort and feel: 24 complaint and 103 praise quotes.... |
| [language_bank](language_bank.json) | 335 | 2026-09-28 | Reviewers say 'it is literally just a men's shirt'... |
| [competitors](competitors.json) | 15 | 2026-09-28 | Competitors should be sock and fashion apparel brands... |
| [positioning](positioning.json) | 10 | 2026-09-28 | Premium everyday basics. Socks and slippers are 93... |
| [channels](channels.json) | 13 | 2026-09-28 | Bombas announced it would begin selling socks in more... |
| [calendar](calendar.json) | 8 | 2026-09-28 | Bombas launched ribbed seamless bralettes around March... |
| [economics](economics.json) | 21 | 2026-09-28 | Average order value 73 dollars stands. |
| [operations](operations.json) | 6 | 2026-09-28 | Bombas' distribution runs through a network of... |
| [marketplaces](marketplaces.json) | 36 | 2026-09-28 | Verified Bombas ASINs on Amazon from a search pull: 29... |
| [stack](stack.json) | 17 | 2026-09-28 | Bombas uses OneTrust for cookie and privacy consent... |
| [site_map](site_map.json) | 6 | 2026-09-28 | The live storefront's home page is at... |
| [content](content.json) | 3 | 2026-09-28 | Comrad Socks runs 7 creator-style ads (first person,... |
| [seo_facts](seo_facts.json) | 2 | 2026-09-28 | Question asked on r/BuyItForLife: What's something you... |
| [team](team.json) | 8 | 2026-09-28 | Bombas has an open Vice President, Distribution role... |
| [decisions](decisions.json) | 2 | 2026-09-28 | S1.4 follow-up: no more Amazon reviews; pull the Ad... |
| [learnings](learnings.json) | 12 | 2026-09-28 | On 2026-09-28 Bombas runs 23 active US Meta ads: 11... |
| [open_questions](open_questions.json) | 5 | undated | What proof answers "will it do the job it claims, like... |
| [freshness](freshness.json) | 27 | 2026-09-28 | avatars: 13 records, last updated 2026-09-28, 0 stale, 0... |

No records yet: changes, plans.

## Routing

| For this work | Read |
|---|---|
| Writing ad copy | `claims`, `voice`, `avatars`, `language_bank`, then skill `agents/skills/CREA/ad-copy/SKILL.md` |
| Pricing a promo | `offers`, `economics`, then `finance_inputs` in the data layer and capability MONEY-C04 |
| A creative brief | `products`, `offers`, `avatars`, `objections`, `voice`, `learnings`, `competitors` |
| Site or landing page work | `site_map`, `policies`, `claims`, `visual` |
| Email and retention | `calendar`, `offers`, `voice`, `learnings` |
| Anything numeric | the metric contract at `/api/metrics`, never this file |
| Answering an objection | `objection_ladders`, then `claims` |
| Checking a claim for copy | records with tier `approved` or `site_backed` only; the QA gate enforces it |

## Links

- Documents: [documents/manifest.json](documents/manifest.json), 0 files
- Open questions: [open_questions.json](open_questions.json), 5 open
- Brain version b927d0021906. Generated from records; edit records, not this file.

## Founder notes

<!-- founder-notes:start -->
Write anything here. Regeneration keeps this block as it is.
<!-- founder-notes:end -->
