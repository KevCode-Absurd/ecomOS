# Extractors

One module per source type, same shape: `run(brand, config) -> list[record]` writing records in `app/brain/schema.json` shape plus a `sources.json` listing every url or file read with the date. Public extractors need no login. Private extractors run only after a founder connects the source (see `app/brain/sources.registry.json`).

| Extractor | Reads | Writes to sections | Notes |
|---|---|---|---|
| site crawl | sitemap, `products.json` (Shopify) or the WooCommerce store API, legal pages, FAQ, size guides, CSS variables | identity, products, offers, policies, claims, voice, visual, site_map, stack | respect robots.txt, 1 request per second, cache pages by hash for the diff |
| Meta Ad Library | the brand's page and 3 to 5 competitor pages | competitors, offers (promos seen in ads), learnings (public), story_bank | signals only; keep format, dates, hook type; never copy text beyond a short quote as evidence |
| press, interviews and podcasts | articles, transcripts, filings | identity, story_bank, channels, economics (public band with source) | every number carries its url and date |
| own-site reviews | the brand's review widget pages or JSON (Judge.me, Yotpo, Okendo, Stamped, Loox) | avatars, objections, language_bank, products | default for every brand; pull 5-star and 1-star first, then the middle; keep star, product, date, verified flag, url |
| Amazon listings and reviews (public sample) | listing pages for the brand's ASINs: title, bullets, A+ content, rating split, review count, visible top reviews | marketplaces, products, objections, language_bank | default for every brand that sells on Amazon; low volume through a sub-agent; no review API and no bulk scraping, so volume comes from the brand's Seller Central export (a document) or a licensed provider |
| retailer and forum reviews | Nordstrom, Dick's, Target, Walmart product pages, Reddit, Trustpilot | avatars, objections, language_bank | verbatim quotes only, with the url; no invented quotes; Trustpilot skews to complaints, say so in the record |
| objection ladders (derived) | every review record in the brain, 5-star and 1-star first | objection_ladders, then avatars, offers, copy, marketplaces | built after the review extractors; see the ladder shape in the contract section 6.2 |
| job postings and stack | careers page, job boards | team, stack, channels | tools and agencies named in postings |
| documents | uploads, Drive, Notion, Slack | any, proposed through the review queue | never required; a document is useful unextracted |
| connectors | Shopify, Meta, Google, GA4, Klaviyo, Gorgias, GSC, Amazon and the rest of the registry | channels, stack, products (hero flags), marketplaces, learnings with metric pointers | numbers stay in the data layer |

## Default extractors for any new brand

Run in this order on day one, before any question is asked: site crawl, own-site reviews, Amazon listings and reviews (when the brand has ASINs), retailer and forum reviews, Meta Ad Library, press and interviews, job postings and stack, then the objection ladders. The list lives in `app/brain/extract/defaults.json` so onboarding and the keeper read the same thing.

Raw output for the Bombas build goes to `app/brain/bombas/raw/<extractor>/`, merged by S1.3m.
