# app/data status

## S2.3c, 28 Sep 2026: generator fixes from the S2.5 review

1. Landed: all 14 fixes in `brands/bombas/REVIEW.md` ("Fixes applied (S2.3c)" has one line per fix, with before and after). 13 of them are in `generate.py`; fix 13 (margin unavailable when no cost rows are in force) is in `app/metrics.py`.
2. Products now use the 25 finance SKU keys (`BMB-...`), so `cogs_landed` joins 25 of 25 and gross margin by month computes (Sep to Dec 2024 read unavailable).
3. Rebuilt at scale 1.0, seed 7, 2024-09-28 to 2026-09-27: 8.8M orders, 44.7M rows, 8.9 GB `data.sqlite` (git-ignored); aggregates, manifest, tables and README refreshed.
4. Calibration hit, last 12 months: $458.3M against the $457M point (+0.28 percent); site 73.5, wholesale 12.0, stores 6.5, marketplaces 8.0 (largest gap 0.5 points); paid split on target within 0.01 points; AOV $73.01; repeat 0.349.
5. New fixtures: `marketplace_sales` (brain marketplace share), `paid_other_spend` (YouTube creators, TikTok, Pinterest, other); new aggregates `marketplace_monthly`, `paid_media_monthly`.
6. Assumed (marked in `manifest.json`): `site_sessions_monthly` 15,000,000 (brain question stays open); 30 percent of returns open a ticket; marketplaces split Amazon 80, TikTok Shop 20; Google CPAs carry one scale (0.79) so Meta to Google is 60 to 20; list prices for the 25 SKUs.
7. Tests: `tests/test_generate_v2.py` (22) and `tests/test_app_metrics.py` (28) pass; 4 new generator tests and 2 new margin tests. Two screen tests updated to the new catalog (offers R03 now quiet, market research 19 lines).
8. Full suite: 528 tests, 7 failures, all pre-existing and reproduced on a clean checkout: meta_gallery access_token, setup connect_skip_declined and state_has_every_step, brand_brain x3, affiliate Amazon sample.
9. Left: gross margin near 74 percent against the 62 target (S2.4 costs or list prices need a look); year 2 repeat at 28 percent of year 1 (band 40 to 60); YoY growth 25.6 to 41.7 percent on this seed.
10. Left: `brands/bombas/review/build_review.py` still reads the old BB- keys and the review charts were not redrawn.
