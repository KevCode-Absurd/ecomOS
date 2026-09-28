# Extractors

One module per source type, same shape: `run(brand, config) -> list[record]` writing records in `app/brain/schema.json` shape plus a `sources.json` listing every url or file read with the date. Public extractors need no login. Private extractors run only after a founder connects the source (see `app/brain/sources.registry.json`).

| Extractor | Reads | Writes to sections | Notes |
|---|---|---|---|
| site crawl | sitemap, `products.json` (Shopify) or the WooCommerce store API, legal pages, FAQ, size guides, CSS variables | identity, products, offers, policies, claims, voice, visual, site_map, stack | respect robots.txt, 1 request per second, cache pages by hash for the diff |
| Meta Ad Library | the brand's page and 3 to 5 competitor pages | competitors, offers (promos seen in ads), learnings (public), story_bank | signals only; keep format, dates, hook type; never copy text beyond a short quote as evidence |
| press, interviews and podcasts | articles, transcripts, filings | identity, story_bank, channels, economics (public band with source) | every number carries its url and date |
| public reviews and forums | retailer reviews, Reddit, Trustpilot | avatars, objections, language_bank | verbatim quotes only, with the url; no invented quotes |
| job postings and stack | careers page, job boards | team, stack, channels | tools and agencies named in postings |
| documents | uploads, Drive, Notion, Slack | any, proposed through the review queue | never required; a document is useful unextracted |
| connectors | Shopify, Meta, Google, GA4, Klaviyo, Gorgias, GSC, Amazon and the rest of the registry | channels, stack, products (hero flags), marketplaces, learnings with metric pointers | numbers stay in the data layer |

Raw output for the Bombas build goes to `app/brain/bombas/raw/<extractor>/`, merged by S1.3m.
