# Apify by screen: what licensed scraping adds to each part of ecomOS

Date: 28 Sep 2026. Source: three surveys of the Apify Store on this date, public pages only. Prices are the pay-per-result rate shown on each actor page and move often. Signal is the actor's user count and rating: **proven** means thousands of users and a 4+ rating, **usable** means hundreds of users or a strong rating on a small base, **unproven** means under about 50 users, and **none** means no maintained actor exists.

## Why this matters

The brain and the screens are built on the brand's own data plus public sources. Apify turns the public sources that block us (Amazon, Reddit, the Ad Library at scale) and dozens we had no lane for (Google Trends, SERPs, AI answer engines, Instagram, TikTok, YouTube, Trustpilot, Google Maps, PageSpeed, BuiltWith, Alibaba, Walmart, Google Shopping) into read-only pulls priced per result. Everything lands the same way: an actor's items go through an adapter into brain records or data tables, the ladders and audits rerun, the screens change nothing.

Rules from the brain contract still apply: read-only actors only, usernames dropped, competitor material is signals never copied, Reddit never a testimonial, every record traceable to actor and run id, every run capped by the budget ledger.

## Cost picture per brand

At the caps in `config/apify.json`, a full monthly refresh on the tier 1 lanes below costs about $15 to $40 per brand. The Apify Starter plan at $39 a month covers 1 to 2 brands; scale plans are per usage. The free plan's $5 credit covers a first Bombas pull of reviews and Reddit but not the rest.

## The map

### Brand brain, onboarding (setup, 05-brand-brain)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| apify/website-content-crawler | the site crawl as clean text and markdown per page, replacing our own crawler for policies, FAQ, PDPs, about pages | identity, products, offers, policies, claims, voice, site_map | $0.20 to $5 per 1,000 pages | proven, the most used actor on the store |
| builtwith/builtwith-official-technology-scraper | the tech stack of the store: platform, apps, scripts, ESP, analytics | stack | $2 per 1,000 domains | usable, 5.0 |
| axesso_data/amazon-reviews-scraper plus junglee/amazon-crawler | Amazon reviews at volume and listing content per ASIN | language_bank, objections, objection_ladders, avatars, products, marketplaces | $0.90 per 1,000 reviews, $3 per 1,000 listings | proven |
| trudax/reddit-scraper-lite | brand mentions and category threads | language_bank, objections, avatars, competitors, positioning, seo_facts, content | $3.40 per 1,000 items | proven, 4.57 |
| casper11515/trustpilot-reviews-scraper | Trustpilot past the 200-review page cap | language_bank, objections, avatars | $0.45 per 1,000 | usable, 3,000 users |
| curious_coder/facebook-ads-library-scraper | the brand's own ads and the competitor set | competitors, offers, learnings, story_bank | $0.75 per 1,000 ads | proven, 4.77 |
| lukaskrivka/article-extractor-smart plus a news search | press and interviews as clean text | story_bank, identity, economics | usage priced | proven, 4.83 |

### Today (00) and the loop

No actor. Today reads the audits. Every lane above makes its findings better grounded.

### Products and research (01)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| apify/google-trends-scraper | interest over time, related and rising queries, by region | trend_series, seo_facts | $0.30 per 1,000 | proven, 14,000 users |
| junglee/amazon-bestsellers | best sellers and movers by category, position and price | candidate_pipeline, competitor_scan | $3.20 per 1,000 | proven, 4.25 |
| junglee/amazon-crawler | keyword search results with price, rating, review count, BSR, offers | candidate_pipeline, price bands | $3 per 1,000 | proven |
| clockworks/tiktok-trends-scraper | trending hashtags and products by industry with view counts | video_commerce_signals | $1.70 per 1,000 | usable, 4.78 |
| automation-lab/tiktok-shop-scraper | TikTok Shop products: price, sold count, seller | video_commerce_signals | $0.005 per product | unproven |
| dami_studio/aliexpress-products-scraper | AliExpress search: price, orders, rating | candidate_pipeline, sourcing | $0.12 per 1,000 | unproven |
| gio21/1688-product-scraper | 1688 factory listings: price, MOQ, sold | sourcing | $5 per 1,000 | usable, 5.0 |
| hypebridge/temu-scraper | Temu price and sales volume | competitor_scan | $0.004 per item | unproven |
| devcake/etsy-search-scraper | Etsy listings: price, shop, favourites | competitor_scan for craft categories | $2 per 1,000 | usable, new |

### Customers and avatars (02), Customers and CX (15)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| the review lanes above (Amazon, Trustpilot, Reddit) | the grounding quotes at volume, by star and source | avatars, objections, objection_ladders, language_bank | see above | proven |
| compass/google-maps-reviews-scraper | reviews of the brand's own stores and of retail partners carrying it | language_bank, marketplaces | $0.30 per 1,000 | proven, 58,000 users, 4.85 |
| apify/instagram-comment-scraper, nooesc/social-media-public-comments | comments under the brand's and competitors' posts, cross-platform | language_bank, objections | $1.50 per 1,000 | proven for Instagram, the cross-platform one unverified |
| epctex/appstore-scraper, automation-lab/google-play-scraper | app reviews for brands with an app | language_bank | $0.005 per page, $0.001 per review | usable, 5.0 |
| seemuapps/judgeme-reviews-scraper, piotrv1001/yotpo-reviews-scraper | own-site widget reviews at volume | language_bank, products | $1 to $2.50 per 1,000 | unproven, our own widget reader stays the default |

### Competitors and market (03)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| curious_coder/facebook-ads-library-scraper (alt apify/facebook-ads-scraper with spend and reach) | every competitor's active ads, run length, formats, offers | competitor_ad_capture, competitors | $0.75 or $3.40 per 1,000 | proven |
| jamhimself/shopify-products-scraper | a competitor's whole catalog with prices, variants and compare-at prices from products.json | competitor_price_capture | $4 per 1,000 | unproven, our own products.json reader is simpler |
| apify/website-content-crawler | competitor PDPs, landers, policies as text | positioning, competitor_snapshot | as above | proven |
| ryanclinton/wayback-machine-search | how a competitor page changed over time, classified as pricing, copy, layout | competitor_snapshot | $0.0035 per snapshot | usable |
| automation-lab/google-shopping-scraper | prices by merchant for the same product | competitor_prices | $0.006 per product | usable, 430 users |
| optimus-fulcria/ecommerce-price-monitor | price history and change alerts across Amazon, Walmart, Target | competitor_prices | $0.002 per product | unproven |
| memo23/crunchbase-scraper | funding rounds and investors for competitors | competitors | $8 per 1,000 | usable, 5.0 |
| bebity/linkedin-jobs-scraper, curious_coder/indeed-scraper | who competitors are hiring, which tools they name | competitors, team | $1 and $0.10 per 1,000 | proven |

### Offers and pricing (04)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| the Ad Library lane | every competitor promo with dates, first-order codes, thresholds seen in ads | offers, competitor offers | see above | proven |
| automation-lab/google-shopping-scraper and the price monitor | price positioning by merchant and over time | competitor_prices | see above | usable, unproven |
| jungle_synthesizer/newsletterhunt-archived-newsletter-issue-scraper | archived brand and competitor emails: subject, sender, date, body | offers, calendar, voice | $1 per 1,000 | unproven, coverage depends on the archive |

### Store health (06)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| builtwith/builtwith-official-technology-scraper, automation-lab/tech-stack-detector | apps and scripts inventory without site access | app_inventory, stack | $2 per 1,000, $0.002 per url | usable |
| jancurn/find-broken-links | dead links and broken fragments across the site | site health findings | $0.25 per 1,000 | usable, by an Apify founder |
| dr.skywalker/domain-dns-health-checker, neverempty/domain-lookup | DNS, SSL expiry, HSTS, CSP, SPF, DMARC | security, email_auth | $0.001 and $11 per 1,000 domains | unproven |
| uptime monitors | none with a track record; use an uptime service, not an actor | | | none |

### Landing pages and CRO (07)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| apify/screenshot-url | scheduled full-page captures of own and competitor pages | page_registry, landing_page_snapshot | usage priced | proven, 7,800 users |
| apify/website-content-crawler | page text and structure for message-match and objection-proof checks | page_copy_blocks, ad_page_checkout_trace | as above | proven |
| ryanclinton/wayback-machine-search | what a competitor changed on a lander and when | competitor_snapshot | as above | usable |

### Site and speed (08)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| dev00/google-pagespeed-insights-api | Lighthouse per url: LCP, FCP, CLS, TBT, TTFB, scores, mobile and desktop, no API key | speed_runs (as a second source next to our lab) | $2 per 1,000 | usable, new |
| builtwith and the tech detector | third-party scripts per page | script inventory | as above | usable |

### Creative (09) and Copy (10)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| the Ad Library lane | formats, hooks, run lengths, offers as signals for the creative map | competitor_snapshot, hook_bank inputs | see above | proven |
| coregent/tiktok-ads-library-creative-center-scraper (alt dltik/tiktok-creative-center) | TikTok top ads by industry with reach range, likes, CTA, performance label | competitor_snapshot | $1.80 to $2 per 1,000 | usable |
| automation-lab/google-ads-transparency-center-scraper | a competitor's Google ads: format, landing domain, first and last shown | competitor_snapshot | tiered, cheap | usable, 185 users |
| aiscraperdev/youtube-ads-transparency-scraper | YouTube ad creatives and active days by advertiser | competitor_snapshot | $4 per 1,000 | usable, 5.0 |
| automation-lab/pinterest-ads-library-scraper, s-r/linkedin-ads-library | Pinterest and LinkedIn ad libraries | competitor_snapshot | cheap, $5 per 1,000 | unproven, usable |
| the review and Reddit lanes | the language bank the copy is written from | language_bank, objection_ladders | see above | proven |

### Paid social (11)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| curious_coder/facebook-ads-library-scraper | the brand's own active ads for the coverage grid when the Meta API is not connected, and competitors' | ad_copy_inventory (public part), competitor_snapshot | $0.75 per 1,000 | proven |
| apify/facebook-ads-scraper | the same with spend and reach estimates where Meta shows them | competitor_snapshot | $3.40 per 1,000 | proven, official |

### Google Ads (12)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| apify/google-search-scraper | the SERP for brand and category terms: paid results, organic, People Also Ask, related, AI Overview | google_search_terms context, seo_facts | $1.80 per 1,000 pages | proven, 191,000 users |
| automation-lab/google-ads-transparency-center-scraper | which competitors bid on which formats and where they land | competitor_snapshot | cheap | usable |
| automation-lab/google-shopping-scraper | Shopping results and merchant prices for the feed's products | merchant_center context | as above | usable |

### Affiliate, marketplace and retail media (13)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| automation-lab/amazon-product-search-results-scraper (alt amazonscrapers/amazon-sponsored-products-tracker) | sponsored versus organic placements per keyword, ad share of the page | amazon ads context | $2.40 and $1 per 1,000 | unproven |
| apify/instagram-scraper, clockworks/tiktok-scraper | creator discovery by hashtag and follower band, engagement, sponsored flags | creator_seeding | $1.50 to $2.70 per 1,000 | proven |
| affiliate program directories | none with usage | | | none |

### Email and messaging (14)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| jungle_synthesizer/newsletterhunt-archived-newsletter-issue-scraper | competitor email cadence, subjects, offers where the archive covers them | inspiration, calendar | $1 per 1,000 | unproven |
| competitor sign-up capture | no actor exists; needs our own inbox automation | | | none |

### Organic and content (16)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| apify/instagram-scraper | own and competitor profiles, posts, reels, hashtags with likes, comments, views | post_performance, content, creator_seeding | $1.50 per 1,000 | proven, 407,000 users |
| clockworks/tiktok-scraper | same for TikTok with plays, shares, sponsored flag | post_performance, content | $1.70 per 1,000 | proven, 294,000 users |
| streamers/youtube-scraper | channel and video metrics plus transcripts | post_performance, content, story_bank | $2.40 per 1,000 | proven, 127,000 users |
| thirdwatch/pinterest-scraper | pins with saves and reactions | content | $1.20 per 1,000 | usable |
| harvestapi/linkedin-profile-posts | company page posts and engagement | content | $1.50 per 1,000 | proven |

### SEO (17)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| apify/google-search-scraper | rankings by country and device, PAA, related, snippets, AI Overview presence | rank_tracker, keyword_question_map | $1.80 per 1,000 | proven |
| memo23/google-suggest-scraper | autocomplete expansions by seed and country | keyword_question_map | $0.50 per 1,000 | usable, thin |
| memo23/keyword-metrics | volume, CPC, difficulty, intent | keyword_question_map | $0.50 to $0.95 per 1,000 | unproven |
| santhej/backlink-checker | backlinks with anchor, dofollow, spam score | backlink_index | $2.40 per 1,000 | usable, thin |
| apify/website-content-crawler | the crawl for technical checks | crawl_snapshot | as above | proven |
| Bing SERP | no proven actor | | | none |

### Answer engines (18)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| apify/chatgpt-search-scraper | ChatGPT answers and citations for the fixed prompt set | ai_prompt_runs | $3 per 1,000 | usable, official |
| apify/perplexity-search-scraper | Perplexity answers, sources, related questions | ai_prompt_runs | $9 per 1,000 | usable, 5.0 |
| apify/google-ai-overviews-scraper | AI Overview or AI Mode text and sources | ai_prompt_runs | $1 per 1,000 | usable, 4.75 |
| apify/gemini-search-scraper, apify/microsoft-copilot-search-scraper | Gemini and Copilot answers | ai_prompt_runs | $3 per 1,000 | usable |

All five share one shape (query, text, sources), so one adapter covers the screen's whole probe.

### Supply and inventory (19)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| devcake/alibaba-supplier-scraper | supplier vetting: years, verified, review score, revenue band | supplier_master, supplier_scorecard | $5 per 1,000 | usable, 5.0, 98.8 percent success |
| fetch_cat/alibaba-products-suppliers-scraper | product price tiers, MOQ, trade assurance | landed_cost inputs | $1.10 per 1,000 | unproven |
| automation-lab/importyeti-us-import-records | public US import records: shipments, HS codes, lanes | supplier_master, competitor supply signals | $1.75 per 1,000 | unproven |
| carrier rate quotes | no actor; tracking exists, rates do not | | | none |

### Marketplaces and quick commerce (20)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| junglee/amazon-crawler | own listings: price, rating, review count, offers and seller, so Buy Box and reseller presence show without SP-API | marketplace_listings, buybox_snapshots | $3 per 1,000 | proven |
| automation-lab/amazon-sellers-scraper | reseller storefronts: feedback, member since | reseller watch | $0.005 per seller | unproven |
| harvestlab/amazon-keyword-rank-tracker | organic rank per keyword and ASIN | marketplace rank | $0.01 per keyword | unproven |
| automation-lab/walmart-scraper | Walmart listings: price, seller, fulfilment, stock | marketplace_listings | $2.40 per 1,000 | usable |
| Target | actors exist but 2 to 3 users each and $19 per 1,000 | | | unproven |

### Finance and cash (21), Measurement (22)

No actor. These screens read the brand's own systems. Google Shopping and price monitors feed price integrity in Finance indirectly.

### Team and ops (23)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| bebity/linkedin-jobs-scraper | competitor hiring by role, salary, tools named | competitors, hiring_triggers | $1 per 1,000 | proven, 35,000 users |
| curious_coder/indeed-scraper | the same from Indeed | as above | $0.10 per 1,000 | proven, 4.85 |
| scrapesage/glassdoor-scraper | competitor employee reviews | competitors | $2 per 1,000 | unproven |

### Security (24)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| domain and DNS checkers | SSL expiry, HSTS, CSP, SPF, DMARC | email_auth, dns_records | cheap | unproven |
| sian.agency/email-breach-checker | breach exposure for brand addresses | security findings | $22.50 per 1,000 | unproven, expensive |
| uptime monitors, dark web watch | no proven actor; use dedicated services | | | none |

### Experiments (25), Reports (26)

No actor.

### Wild bets and PR (27)

| Actor | Adds | Fills | Price | Signal |
|---|---|---|---|---|
| lukaskrivka/article-extractor-smart | any article as clean text | pr_coverage, reputation_monitor_feed | usage priced | proven, 4.83 |
| automation_craft/google-news-scraper | news search with decoded publisher urls | pr_coverage | $0.002 per article | unproven |
| memo23/crunchbase-scraper | funding and investor news | partnership_pipeline | $8 per 1,000 | usable |
| parseforge/producthunt-scraper | daily launches, votes, topics | wild_bets signals | $0.03 per result | usable |
| themineworks/podcast-episode-scraper | episodes with transcripts where available | media_list, story_bank | $1 per 1,000 | unproven |
| piotrv1001/eventbrite-event-scraper | event listings | events_and_popups | $3 per 1,000 | unproven |

## What changes in the product

1. **Default extractors for a new brand** grow from 8 to 14: add the site crawler, BuiltWith, Trustpilot, Google Trends, the Google SERP for the brand's own terms, and the five answer-engine probes. All public, all read-only, all capped. `app/brain/extract/defaults.json` and `sources.registry.json` get the entries; each is one adapter in `apify_adapters.py`.
2. **The inspiration layer gets its sources** without building pullers: Ad Library, TikTok Creative Center, Google Ads Transparency, Instagram, TikTok, YouTube, archived newsletters. Session S4.2 becomes adapters over these actors instead of four custom pullers.
3. **Competitors becomes a live board**: ads, catalog and prices, page changes, hiring, funding, all on a weekly schedule.
4. **Answer engines becomes real** on day one: the five actors share a shape, so one adapter runs the fixed prompt set across engines.
5. **Marketplaces without SP-API**: listings, Buy Box, resellers and reviews from the crawler and reviews actors, so the screen works before the brand connects Seller Central.
6. **Site speed gets a second source** next to our lab: PageSpeed per url, mobile and desktop.
7. **What stays ours**: the site widget review reader, the products.json reader, the speed lab, and anything the brand's own connectors provide. Apify fills gaps, it does not replace connected data.
8. **What Apify cannot do**: competitor email capture, affiliate program directories, carrier rate quotes, uptime, dark web watch, Bing SERP. Those stay fixtures or dedicated services.

## Rollout, in order

| Tier | Lanes | Why first |
|---|---|---|
| 1, this week, session S1.6 and S1.7 | Amazon reviews and listings, Reddit, Ad Library, Trustpilot, Google Trends, Google SERP, the five answer engines, PageSpeed, BuiltWith, Instagram, TikTok, YouTube | proven actors, feed the brain, competitors, SEO, answer engines, speed, organic on day one |
| 2, when the screens need them | Alibaba supplier, Amazon best sellers, Walmart, Google Shopping, Wayback, TikTok Creative Center, Google Ads Transparency, YouTube ads, LinkedIn Jobs, Indeed, Crunchbase, article extractor, Google Maps reviews | usable actors, one adapter each, per screen round |
| 3, only on a brand's request | 1688, Temu, AliExpress, Etsy, TikTok Shop, Pinterest, LinkedIn ads, newsletters, import records, domain checks, Glassdoor, podcasts, events | unproven actors, verify on a live run before trusting fields |

Each lane is one entry in the registry, one adapter, one fixture, one test. The connector, the caps and the ledger are shared.
