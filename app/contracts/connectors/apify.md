# Connector: Apify (licensed scraping for Amazon reviews, Meta Ad Library, Reddit)

Date: 28 Sep 2026. Status: contract for session S1.6. Research from the Apify Store on 28 Sep 2026; actor names, fields and prices change, so the adapter reads the actor's live input schema before a run and the test fixtures pin the output shape we depend on.

## Why

Three sources the brain needs at volume block datacenter traffic or forbid bulk scraping: Amazon reviews, the Meta Ad Library at scale, and Reddit. Apify actors run those pulls under Apify's own infrastructure and terms, priced per result. We call them read-only, cap the spend, and turn the items into brain records. Nothing else in the brain changes: the same sections fill, the ladders rebuild.

## Access

- Token: environment variable `APIFY_TOKEN`. Local: `.env` (git-ignored, see `.env.example`). Cloud sessions: the environment's settings, as an API credential or environment variable named `APIFY_TOKEN`. Never in code, logs, fixtures or chat.
- Auth: header `Authorization: Bearer <token>` (docs: https://docs.apify.com/api/v2).
- Endpoint: `POST https://api.apify.com/v2/acts/{username~actor}/run-sync-get-dataset-items` with the actor input as JSON; returns the dataset items; 408 after 300 s, in which case fall back to `POST /v2/acts/{id}/runs` then poll `GET /v2/actor-runs/{runId}` and `GET /v2/datasets/{datasetId}/items` (docs: https://docs.apify.com/api/v2/act-run-sync-get-dataset-items-post).
- Free plan: $5 platform credit a month, hard stop. Paid plans lift it. Per-run cost is per event or per result, quoted by each actor.

## Actors (verify the input schema tab before the first live run)

| Lane | Actor | Input keys we send | Output keys we read | Price seen 28 Sep 2026 |
|---|---|---|---|---|
| Amazon reviews | `axesso_data~amazon-reviews-scraper` | `asin`, `domainCode`, `sortBy`, `maxPages`, `filterByStar`, `reviewerType` | `rating`, `title`, `text`, `date`, `verified`, `numberOfHelpful`, `reviewId` | about $0.90 per 1,000 reviews |
| Amazon listing | `junglee~amazon-crawler` | `categoryOrProductUrls`, `maxItemsPerStartUrl`, `scrapeProductDetails`, `countryCode` | `title`, `url`, `asin`, `price`, `stars`, `reviewsCount`, `features` (bullets) | about $3 per 1,000 results |
| Meta Ad Library | `curious_coder~facebook-ads-library-scraper` (alt `apify~facebook-ads-scraper` for spend and reach enrichment) | `urls` (page or search urls), `scrapeAdDetails`, `limitPerSource`, `scrapePageAds.activeStatus`, `scrapePageAds.countryCode` | ad id, archive id, page name and id, start and end dates, publisher platform, snapshot (copy, cta, media urls), impressions or reach where present | about $0.75 per 1,000 ads (alt about $3.40) |
| Reddit | `trudax~reddit-scraper-lite` | `startUrls` or `searches`, `maxItems`, `maxComments`, `sort`, `time`, `skipUserPosts` | posts: `id`, `url`, `title`, `upVotes`, `numberOfComments`, `createdAt`; comments: `id`, `url`, `body`, `upVotes`, `createdAt` | about $3.40 per 1,000 items |

Reviewer names and Reddit usernames are in the items; the adapter drops them before anything is written.

## Interface

`app/connectors/apify.py`

- `ApifyClient(token=None, mode="live"|"mock")`: `run(actor, input, max_items, max_usd) -> list[dict]`. Mock mode reads `app/connectors/fixtures/apify/<actor>.json`. Live mode estimates cost from the actor's price and `max_items`, reserves it in `intelligence/budget.py`, refuses when the per-run or weekly cap in `sources.config.json` would be exceeded, runs, settles the actual usage, and logs run id, item count and cost with no token.
- `status()`: token present, plan credit if the API exposes it, last run per lane.

`app/connectors/apify_adapters.py`, one function per lane, `items -> records` in `app/brain/schema.json` shape:

- `amazon_reviews(items, brand, asin, listing)`: one `language_bank` record per review with star, verified, helpful votes, date and the review url as `source.ref`; `objections` for 1 and 2 star themes; `products` issue and praise records per line; `marketplaces` listing record per ASIN (title, bullets, stars, review count, price, third-party seller flag). Tier `evidence`, visibility `public`. Quotes verbatim, trimmed to 300 characters.
- `meta_ad_library(items, brand, page_role)`: `competitors` records per page (active ads, longest run, formats, hook types, offers seen), `offers` for the brand's own codes and promos with dates, `learnings` for formats and run lengths as signals, `content` for organic-looking creator formats. Never store ad text beyond a short quote as evidence, never media. Tier `evidence`, visibility `public`.
- `reddit(items, brand)`: `language_bank` with upvotes as weight and subreddit in the value, `objections`, `avatars` when a buying situation repeats, `competitors` as recommended-instead counts, `positioning` frames, `seo_facts` questions, `content` topics. No usernames. Every record carries `notes: "reddit language, not for testimonial use"`. Tier `evidence`, visibility `public`.

`app/brain/extract/apify_<lane>.py`: `run(brand, config) -> writes app/brain/<brand>/raw/<lane>-apify/<section>.json and sources.json` using the client and adapter, then the merge and the ladder builder run as they do for any raw folder.

## Caps and rules

- Per-brand config `app/brain/<brand>/sources.config.json` holds ASINs, pages, searches, subreddits, per-run item caps, `max_usd_per_run` and `max_usd_per_week`.
- A run never starts without a reservation in the budget ledger; the ledger's working stop and ceiling still apply.
- Read-only. No actor that posts, likes, follows or logs in.
- Amazon and Reddit items feed language and objections; Meta items feed signals. Copy rules from the brain contract apply: never copy text, logos, products or faces; Reddit users are never testimonials.
- Every record carries the actor id and run id in `source.ref` as `apify:<actor>:<runId>:<itemUrl>` so a finding can be traced to the item.

## Maps to

Brain sections per lane as in `sources.config.json`; data tables `reviews_raw`, `marketplace_listings`, `ad_library_captures`, `community_mentions`.
