# bombas: brand card (T0)
Identity: Bombas is B Corp certified.
Diagnosis: unknown yet
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
| [identity](identity.json) | 11 | 2026-09-28 | Bombas is B Corp certified. |
| [story_bank](story_bank.json) | 23 | 2026-09-28 | Bombas pitched on Shark Tank in the Season 6 premiere, which first... |
| [voice](voice.json) | 3 | 2026-09-28 | Bombas repeats the same donation tagline word for word across its... |
| [visual](visual.json) | 16 | 2026-09-28 | Bombas main stylesheet defines a black color token named black as... |
| [products](products.json) | 20 | 2026-09-28 | Bombas sells a digital gift card in denominations from 25 to 300... |
| [offers](offers.json) | 7 | 2026-09-28 | Bombas offers free standard shipping on US orders of 75 dollars or... |
| [policies](policies.json) | 10 | 2026-09-28 | Bombas accepts returns for a refund within 30 days of purchase, or... |
| [claims](claims.json) | 6 | 2026-09-28 | Bombas ankle socks are described as moisture-wicking with a... |
| [avatars](avatars.json) | 11 | 2026-09-28 | Cold Weather Wool Sock Loyalist: warm, durable socks for cold... |
| [objections](objections.json) | 14 | 2026-09-28 | Compression socks are too hard to pull on, sit too high or too... |
| [objection_ladders](objection_ladders.json) | 7 | 2026-09-28 | Comfort and feel: 18 complaint and 50 praise quotes. Top rung... |
| [language_bank](language_bank.json) | 36 | 2026-09-28 | Reviewers say 'it is literally just a men's shirt' (complaint). |
| [competitors](competitors.json) | 7 | 2026-09-28 | Meta competitor set confirmed from the Ad Library: Stance, Darn... |
| [channels](channels.json) | 13 | 2026-09-28 | Bombas announced it would begin selling socks in more than 190... |
| [calendar](calendar.json) | 8 | 2026-09-28 | Bombas launched ribbed seamless bralettes around March 1, 2023, in... |
| [economics](economics.json) | 12 | 2026-09-28 | Bombas exceeded 100 million dollars in revenue in 2018 and was... |
| [operations](operations.json) | 6 | 2026-09-28 | Bombas' distribution runs through a network of third-party... |
| [marketplaces](marketplaces.json) | 9 | 2026-09-28 | Amazon ASIN B07MTXGV9R (Bombas Women's Originals Ankle Socks,... |
| [stack](stack.json) | 17 | 2026-09-28 | Bombas uses OneTrust for cookie and privacy consent management. |
| [site_map](site_map.json) | 6 | 2026-09-28 | The live storefront's home page is at https://shop.bombas.com/,... |
| [team](team.json) | 8 | 2026-09-28 | Bombas has an open Vice President, Distribution role reporting... |
| [learnings](learnings.json) | 8 | 2026-09-28 | On 2026-09-28 Bombas runs 23 active US Meta ads: 11 image, 8... |
| [open_questions](open_questions.json) | 12 | undated | What is the average order value on the US site? |
| [freshness](freshness.json) | 22 | 2026-09-28 | avatars: 11 records, last updated 2026-09-28, 0 stale, 0 open... |

No records yet: diagnosis, positioning, content, seo_facts, decisions, changes, plans.

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
- Open questions: [open_questions.json](open_questions.json), 12 open
- Brain version 80e0a411b82c. Generated from records; edit records, not this file.

## Founder notes

<!-- founder-notes:start -->
Write anything here. Regeneration keeps this block as it is.
<!-- founder-notes:end -->
