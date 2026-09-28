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
| Amazon reviews | `junglee~amazon-reviews-scraper` (default; `axesso_data~amazon-reviews-scraper` needs a one-time full-permission approval in the console) | `productUrls`, `maxReviews`, `filterByRatings` (fiveStar, oneStar), `sort` | `productAsin`, `ratingScore`, `reviewTitle`, `reviewDescription`, `reviewedIn`, `isVerified`, `reviewReaction`, `reviewUrl`, normalised in the extractor | about $3 per 1,000 reviews (axesso about $0.90) |
| Amazon listing | `junglee~amazon-crawler` | `categoryOrProductUrls`, `maxItemsPerStartUrl`, `scrapeProductDetails`, `countryCode` | `title`, `url`, `asin`, `price`, `stars`, `reviewsCount`, `features` (bullets) | about $3 per 1,000 results |
| Meta Ad Library | `curious_coder~facebook-ads-library-scraper` (alt `apify~facebook-ads-scraper` for spend and reach enrichment) | `urls` (page or search urls), `scrapeAdDetails`, `limitPerSource`, `scrapePageAds.activeStatus`, `scrapePageAds.countryCode` | ad id, archive id, page name and id, start and end dates, publisher platform, snapshot (copy, cta, media urls), impressions or reach where present | about $0.75 per 1,000 ads (alt about $3.40) |
| Reddit | `trudax~reddit-scraper-lite` | `startUrls` as search result pages (global and per subreddit with restrict_sr; a subreddit home page returns one community record and nothing else), `maxItems`, `maxComments`, `sort`, `time`, `skipUserPosts` | posts: `id`, `url`, `title`, `upVotes`, `numberOfComments`, `createdAt`; comments: `id`, `url`, `body`, `upVotes`, `createdAt` | about $3.40 per 1,000 items |

Reviewer names and Reddit usernames are in the items; the adapter drops them before anything is written.

## Interface

`app/connectors/apify.py`

- `ApifyClient(token=None, mode="live"|"mock")`: `run(actor, input, max_items, max_usd) -> list[dict]`. Mock mode reads `app/connectors/fixtures/apify/<actor>.json`. Live mode estimates cost from the actor's price and `max_items`, reserves it in `intelligence/budget.py`, refuses when the per-run or weekly cap in `config/apify.json` would be exceeded, runs, settles the actual usage, and logs run id, item count and cost with no token.
- `status()`: token present, plan credit if the API exposes it, last run per lane.

`app/connectors/apify_adapters.py`, one function per lane, `items -> records` in `app/brain/schema.json` shape:

- `amazon_reviews(items, brand, asin, listing)`: one `language_bank` record per review with star, verified, helpful votes, date and the review url as `source.ref`; `objections` for 1 and 2 star themes; `products` issue and praise records per line; `marketplaces` listing record per ASIN (title, bullets, stars, review count, price, third-party seller flag). Tier `evidence`, visibility `public`. Quotes verbatim, trimmed to 300 characters.
- `meta_ad_library(items, brand, page_role)`: `competitors` records per page (active ads, longest run, formats, hook types, offers seen), `offers` for the brand's own codes and promos with dates, `learnings` for formats and run lengths as signals, `content` for organic-looking creator formats. Never store ad text beyond a short quote as evidence. Media (decided 28 Sep 2026): the brain adapter keeps none, but the raw items carry `snapshot.images[].original_image_url` and `snapshot.videos`, and the inspiration puller (card S4.2a) downloads them at pull time because Meta's links are signed and expire within days. Own-brand ads are stored in full. Competitor ads keep the image, a video thumbnail and the video url, tagged by format, hook, layout and mood, in a git-ignored media folder, shown in the inspiration screen for reference only; the generation boundary never receives a competitor file, so the signals-only rule is enforced in code. Tier `evidence`, visibility `public`.
- `reddit(items, brand)`: `language_bank` with upvotes as weight and subreddit in the value, `objections`, `avatars` when a buying situation repeats, `competitors` as recommended-instead counts, `positioning` frames, `seo_facts` questions, `content` topics. No usernames. Every record carries `notes: "reddit language, not for testimonial use"`. Tier `evidence`, visibility `public`.

Page discovery for the Meta Ad Library lane (S6.0c, `app/brain/extract/adlib_pages.py`): a new brand never runs a keyword search. The own page id comes from a facebook.com link on the site (JSON-LD sameAs, header, footer) whose name or handle matches the brand, then the known-ids cache (`fixtures/adlib/known_pages.json` plus any `page_id` in brain records), then one public Ad Library page search that keeps only an exact case-insensitive name ("Stance Auto" is not "Stance"), else the founder pastes the id. It is written to `pages` with role self. Competitors are proposed from the brain (competitor set, named and Ad Library competitor records, Reddit recommended-instead, the founder's `competitor_frame`, the identity category), ranked, up to 15, each with reasons that cite record ids, and written to `proposed_pages`; only `pages` are pulled, and `--confirm "Name,Name"` moves a proposal into `pages` as a competitor. On 28 Sep a plain fetch of the page search returned a JavaScript challenge (403) and shop.bombas.com carried no Facebook link, so for Bombas the id came from the cache.

ASIN discovery for the Amazon lane (S6.0d, `app/brain/extract/amazon_discover.py`): a new brand's ASINs are found cheapest first, stopping once 10 or more have a ratings count. First the Amazon links on the brand's own site (`/dp/`, `/gp/product/`, a `/stores/` link), then one polite public fetch of the brand store page (a sign-in page or robot check is recorded as unavailable with the reason and the next step runs), then `axesso_data~amazon-product-search-scraper` with the brand name as keyword, capped at 50 results and a hard $1 per run through the client caps (a 51st result is refused; the price on file is an unverified $5 per 1,000 upper bound, so 50 results reserve $0.56). `junglee~amazon-crawler` is never used for search: it cost $8.64 for 160 results on 28 Sep. Results are kept only when the manufacturer field matches the brand, else when the title starts with the brand name. It writes `marketplaces` listing records and ranks config `amazon_reviews.asins` by review count (top 10, the rest in `asins_backlog`); the review lane then runs unchanged. Input keys (`input[].keyword`, `domainCode`, `sortBy`, `maxPages`, `category`) and output keys (`asin`, `productDescription`, `manufacturer`, `productRating`, `countReview`, `price`, `availability`, `soldBy`) are pinned by the hand-written fixture and must be checked against the actor's input schema tab before the first live run.

`app/brain/extract/apify_<lane>.py`: `run(brand, config) -> writes app/brain/<brand>/raw/<lane>-apify/<section>.json and sources.json` using the client and adapter, then the merge and the ladder builder run as they do for any raw folder.

## Caps and rules

- Per-brand config `app/brain/<brand>/config/apify.json` holds ASINs, pages, searches, subreddits, per-run item caps, `max_usd_per_run` and `max_usd_per_week`.
- A run never starts without a reservation in the budget ledger; the ledger's working stop and ceiling still apply.
- Read-only. No actor that posts, likes, follows or logs in.
- Amazon and Reddit items feed language and objections; Meta items feed signals. Copy rules from the brain contract apply: never copy text, logos, products or faces; Reddit users are never testimonials.
- Every record carries the actor id and run id in `source.ref` as `apify:<actor>:<runId>:<itemUrl>` so a finding can be traced to the item.

## Maps to

Brain sections per lane as in `config/apify.json`; data tables `reviews_raw`, `marketplace_listings`, `ad_library_captures`, `community_mentions`.
