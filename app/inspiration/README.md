# Inspiration layer

Outside references shown next to a brand's own work. Contract: `app/contracts/inspiration.md`. Sources: `registry.json`.

## Puller A: Meta Ad Library (S4.2a)

`python3 -m app.inspiration.pull_a --brand bombas [--mode mock|live] [--out app/inspiration] [--date YYYY-MM-DD]` runs the Ad Library lane through the existing `ApifyClient` (same actor, per-run and weekly caps, same budget ledger) over the pages in `app/brain/<brand>/config/apify.json`, by page id only; a page with no id is skipped and listed, and items from any other page are dropped. Every ad becomes a creative reference in `<brand>/creative.json`, and an ad with a promo also becomes an offers reference in `<brand>/offers.json`. `tag.py` tags each ad by format, hook, layout, mood, offer and topic terms with rules in code and keeps a quote of at most 140 characters; the rest of the ad text is never stored. `relevance.py` scores each reference with the 9 contract rules over `Brain(<brand>)` records: every reason names the brain field, the record id, the matched value and a template sentence; the score is the capped sum and a reference under 0.3 is stored with `shown: false`. Live mode downloads media at pull time into `media/<brand>/<origin>/` (git-ignored): own ads in full (images and videos), competitor ads as image plus video thumbnail, with the video kept as a remote url and its expiry read from the signed link. A reference whose media cannot be fetched reads kind none. Mock mode reads the connector fixture plus `fixtures/meta_ad_library_pages/extra_items.json`, makes no network call, and skips downloads (kind none, with a note). `rights.py` is the generation boundary: `assert_generation_input(reference)` passes own_brand and raises `RightsError` for reference_only, and every future generation, copy or brief call goes through it. `--purge "<origin brand>"` removes every reference and media file about that brand, for takedowns. Validate a file with `python3 -m app.inspiration.validate <file>` against `reference.schema.json`. Tests: `python3 -m unittest tests.test_inspiration_pull_a`.

## S4.2a status

1. Built: schema and validator, tagger, relevance (9 rules), rights boundary, media downloader, puller with purge.
2. `bombas/creative.json` (8) and `bombas/offers.json` (5) come from the mock run on 28 Sep 2026: fixture data, not scraped, media kind none.
3. Live mode is tested only with a fake transport and fake downloads; no paid Apify call was made. A small live run is a later decision.
4. Brain gaps the rules work around: no `economics.red_line` (margin room falls back to the contribution margin, 27.5 percent), no price median (geometric midpoint of the ladder), no BFCM or holiday windows in `calendar`, and `competitor_frame` is a category, so the frame check reads `competitors.competitor_set`.
5. Allbirds has no page id in the config, so it is skipped until the founder pastes one.
6. Next: S4.3 renders these in the `inspiration-block`; a live pull needs a card and fits the $4 per-run cap (estimate $2.08 for 12 pages at 150 ads).
