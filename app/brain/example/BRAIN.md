# example: brand card (T0)
Identity: unknown yet
Diagnosis: unknown yet
Red lines: none recorded
Top claims: none approved yet
Current promos:
- [site_backed, 2026-09-28, 0 days old] example.offers.current_promos: One promo is running: buy 4 get 1 free on packs.
Freshness: all records in date

## Sections

| Section | Records | Last update | Gist |
|---|---|---|---|
| [offers](offers.json) | 3 | 2026-09-28 | Free shipping on orders over $50. |
| [avatars](avatars.json) | 2 | 2026-09-28 | The Gifter buys packs as presents around holidays and wants the... |
| [learnings](learnings.json) | 2 | 2026-09-28 | Dad socks UGC 03 had the lowest CPA in Q2. Numbers live in the... |

No records yet: identity, diagnosis, story_bank, voice, visual, products, policies, claims, objections, language_bank, competitors, positioning, channels, calendar, economics, operations, marketplaces, stack, site_map, content, seo_facts, team, decisions, open_questions, changes, freshness, plans.

## Routing

| For this work | Read |
|---|---|
| Writing ad copy | `claims`, `voice`, `avatars`, `language_bank`, then skill `agents/skills/CREA/ad-copy/SKILL.md` |
| Pricing a promo | `offers`, `economics`, then `finance_inputs` in the data layer and capability MONEY-C04 |
| A creative brief | `products`, `offers`, `avatars`, `objections`, `voice`, `learnings`, `competitors` |
| Site or landing page work | `site_map`, `policies`, `claims`, `visual` |
| Email and retention | `calendar`, `offers`, `voice`, `learnings` |
| Anything numeric | the metric contract at `/api/metrics`, never this file |
| Checking a claim for copy | records with tier `approved` or `site_backed` only; the QA gate enforces it |

## Links

- Documents: [documents/manifest.json](documents/manifest.json), 1 file
- Open questions: [open_questions.json](open_questions.json), 0 open
- Brain version 9e1f10e2f2bb. Generated from records; edit records, not this file.

## Founder notes

<!-- founder-notes:start -->
Write anything here. Regeneration keeps this block as it is.
<!-- founder-notes:end -->
