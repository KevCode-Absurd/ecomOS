# SEO: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | done |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | done |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | done |
| 0.4 | `audit.py`: 13 rules SEO-R01 to SEO-R13 in the audit contract shape | done |

## Room jobs and the JTBD table (room "SEO", agent ORG)

| Job | Question | Capabilities | Rule(s) in audit.py | Round 0 state |
|---|---|---|---|---|
| decide whether SEO is worth the spend this quarter | does this category have enough demand and margin to justify SEO work at all | ORG-C17 | none yet | candidate |
| know what buyers are asking before a page is written | what keywords and buyer questions should this page answer | ORG-C18 | none yet | candidate (brain seo_facts has 2 Reddit questions) |
| make sure the site structure carries the content plan | does the collection tree, URL type and menu support the money pages we need | SITE-C07 | none yet | candidate |
| find what is technically broken, including for AI crawlers | what indexing, canonical, redirect or crawl error needs fixing, and can AI crawlers reach our pages | ORG-C20 | SEO-R07, SEO-R12 | unavailable: crawl_snapshot, robots_txt_snapshot |
| know which product pages miss the SEO basics | which product pages have thin titles, no content stack or bad image SEO | ORG-C21 | SEO-R02 | live on search_console, fires on the home page |
| know which collection pages give no buying help | which collection pages have no FAQ, no reviews and no grid logic | ORG-C22 | none yet | candidate |
| confirm structured data validates | which product, review, FAQ or breadcrumb schema is missing or breaking | ORG-C23 | SEO-R06 | unavailable: schema_validation_log |
| sequence the refresh backlog first | which pages are falling and need fixing first, ranked by revenue at risk | ORG-C26 | SEO-R05, SEO-R08 | unavailable: ga4_orders_join, page dates, product_feed_status |
| build buyer-intent content for a money page | which cluster or comparison page should we write next, and ahead of which season | ORG-C24, ORG-C25 | none yet | candidate |
| keep money pages linked | which money pages get no internal links, and which content pages are orphaned | ORG-C27 | SEO-R03, SEO-R04 | R03 live (quiet), R04 unavailable: crawl_snapshot |
| know if outreach and local presence earn real links | are backlink, PR and local listing efforts landing links and reviews | ORG-C28, ORG-C29 | SEO-R09, SEO-R10 | unavailable: backlink_index, gbp_reviews |
| confirm tracking is not the reason numbers look wrong | is GA4, Search Console and Tag Manager tracking what they should | MONEY-C20 | SEO-R11 | live on GA4 daily totals (quiet) |
| get a revenue-first read on organic this month | is organic growing, and where is a drop coming from | ORG-C32 | SEO-R01 | live on sessions (quiet) |
| screen a vendor pitch before signing | does this vendor's stat hold up against our own analytics | ORG-C33 | SEO-R13 | unavailable: vendor_claims |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- does this category have enough demand and margin to justify SEO work at all  (ORG-C17)
- what keywords and buyer questions should this page answer  (ORG-C18)
- does the collection tree, URL type and menu support the money pages we need  (SITE-C07)
- what indexing, canonical, redirect or crawl error needs fixing, and can AI crawlers even reach our pages  (ORG-C20)
- which product pages have thin titles, no real content stack or bad image SEO  (ORG-C21)
- which collection pages have no FAQ, no reviews and no grid logic  (ORG-C22)
- which product, review, FAQ or breadcrumb schema is missing or breaking  (ORG-C23)
- which pages are falling and need fixing first, ranked by revenue at risk  (ORG-C26)
- which cluster or comparison page should we write next, and ahead of which season  (ORG-C24, ORG-C25)
- which money pages get no internal links, and which content pages are orphaned  (ORG-C27)
- are backlink, PR and local-listing efforts landing links and reviews that move rankings  (ORG-C28, ORG-C29)
- is GA4, Search Console and Tag Manager tracking what they should  (MONEY-C20)
- is organic growing, and where exactly is a drop coming from  (ORG-C32)
- does this vendor's own stat hold up against our own analytics  (ORG-C33)

### Metrics specified

- `organic_sessions`: Visits that came from unpaid search. GA4 sessions where default channel group = Organic Search
- `organic_revenue`: Store revenue from orders that started with an unpaid search visit. sum(order_value) where first-touch session channel = organic search, joined by session id or converted client id
- `organic_revenue_share`: Share of total store revenue that organic search brought in. organic_revenue / total_store_revenue, same window
- `keyword_coverage`: Share of the buyer-question map that has a live page ranking in the top 20. keywords_with_page_rank_le_20 / keywords_in_map
- `page1_keyword_count`: Number of mapped keywords ranking in the top 10, and the change from last month. count(keywords where rank <= 10), delta vs 30 days ago
- `ctr_by_query_group`: Click-through rate for branded vs non-branded search queries. clicks / impressions, grouped by branded vs non-branded query classification
- `indexed_page_ratio`: Share of submitted sitemap pages that Google has actually indexed. indexed_pages / submitted_pages
- `crawl_error_count`: Pages returning a broken status, a bad redirect or a redirect chain, on the latest crawl. count(pages) where status in (4xx, 5xx) or redirect_hops >= 3
- `orphan_page_count`: Pages with zero internal links pointing to them. count(pages) where internal_inlinks = 0
- `schema_validation_pass_rate`: Share of product and collection pages with valid, error-free schema. pages_with_valid_schema / money_pages_checked
- `content_refresh_backlog_value`: Total revenue-at-risk sitting in pages flagged for refresh, ranked. sum(page_trailing_90d_revenue) for pages where clicks fell 20%+ over 90 days and not refreshed
- `referring_domains_new`: New unique domains linking to the site this month. count(distinct referring_domain) first seen this month
- `link_velocity_by_source`: New links split by tactic: PR, guest post, broken-link, review-site. count(new_links) grouped by outreach_tactic tag
- `gbp_review_rate`: New Google Business Profile reviews this month and the average rating. count(new_reviews), avg(rating)
- `tag_health_score`: Share of key events (page view, add to cart, purchase) firing correctly on the last audit. events_firing_correctly / key_events_checked
- `cwv_pass_rate`: Share of the top page templates passing Core Web Vitals. templates_passing / templates_checked, using field or lab data
- `discontinued_page_handling_rate`: Share of out-of-stock or discontinued product pages that redirect properly instead of 404ing. pages_redirected_or_kept_with_alternatives / discontinued_pages

### Insights specified (rules in code)

- unexplained traffic drop: organic_sessions falls 15% or more week over week with no logged algorithm update or seasonal cause → "organic visits fell {pct}% this week with no known cause logged" (action ORG-C32)
- CTR mismatch: a page's impressions rank in the top 20% and its CTR sits 30% or more below the branded/non-branded benchmark for its position → "{page} gets {impressions} impressions but a CTR of only {ctr}%, well under what position {pos} should get" (action ORG-C21)
- keyword cannibalization: 2 or more pages rank for the same primary keyword within 5 positions of each other → "{n} pages compete for '{keyword}', splitting the ranking signal" (action ORG-C27)
- orphan money page: a page in the keyword map has zero internal inlinks → "{page} targets '{keyword}' but gets no internal links from anywhere on the site" (action ORG-C27)
- stale high-value page: a page in the top 20% of pages by organic_revenue has clicks down 20% or more over 90 days and has not been refreshed in 180 days → "{page} makes {revenue} a month but clicks fell {pct}% and it has not been touched in {days} days" (action ORG-C26)
- broken schema on a money page: a product or collection page's schema fails validation → "{n} product pages have broken {schema_type} schema" (action ORG-C23)
- long redirect chain: a URL has 3 or more redirect hops before landing → "{n} URLs take {hops} redirects to load, slowing crawl and the visitor" (action ORG-C20)
- discontinued page 404ing: an out-of-stock or discontinued product page returns a 404 or soft-404 instead of a redirect to a live alternative → "{n} discontinued product pages 404 instead of pointing buyers somewhere live" (action ORG-C26)
- outreach not landing links: 60 or more outreach pitches sent in 60 days produced zero new referring domains → "no new links from {n} pitches sent in the last {days} days" (action ORG-C28)
- unanswered reviews: a Google Business Profile review has gone unanswered for more than 7 days → "{n} reviews have waited over a week for a reply" (action ORG-C29)
- tag stopped firing: a key GA4 event's daily count drops to zero for 2 or more consecutive days → "the {event} tag stopped firing on {date}" (action MONEY-C20)
- AI crawler blocked on a money page: robots.txt disallows a known AI crawler (GPTBot, PerplexityBot, Google-Extended) on a page in the keyword map → "{n} money pages block {crawler} from reading them" (action ORG-C20)
- vendor claim does not hold up: a vendor-cited stat about the site differs from the brand's own analytics by 20% or more → "the vendor claims {vendor_stat} but our own data shows {actual_stat}" (action ORG-C33)

### Visuals specified

- keyword rank movement (line chart): count of page-1 keywords over time
- crawl health treemap (treemap): pages sized by traffic, colored by health status (healthy, warning, broken)
- content refresh priority table (sortable table): pages ranked by revenue at risk, with the reason flagged
- internal link graph snippet (node graph): money pages and their inlink count, orphans highlighted
- organic revenue vs total revenue (stacked area chart): organic revenue against total store revenue over time
- backlink velocity by tactic (stacked bar chart): new referring domains per month, split by outreach tactic

### Not in the usual tools

- computes organic revenue from the store's own order ledger, not from GA4's own attribution model
- sequences the refresh backlog by revenue at risk from the store's own order data, ahead of writing anything new
- checks AI-crawler-specific access rules (GPTBot, PerplexityBot, Google-Extended) in the same audit as classic crawl health
- flags a discontinued or out-of-stock page that 404s instead of redirecting, tied to the store's own product feed
- screens a vendor's own pitch numbers against the brand's own analytics before the founder signs anything

### Data this screen needs

- `gsc_performance`: date, page, query, clicks, impressions, ctr, position (Search Console API export)
- `ga4_orders_join`: session_id, channel_group, landing_page, order_id, order_value (GA4 export joined to store orders)
- `keyword_question_map`: keyword, buyer_question, target_page, priority, season (ORG-C18 output)
- `rank_tracker`: keyword, page, rank, date (rank tracking tool export)
- `crawl_snapshot`: url, status_code, redirect_hops, canonical, internal_inlinks, indexable, rendered_with_js (JS-rendered site crawl (Screaming Frog-style))
- `schema_validation_log`: page, schema_type, valid, errors, checked_at (structured-data validator)
- `robots_txt_snapshot`: user_agent, disallow_paths, checked_at (robots.txt fetch)
- `backlink_index`: referring_domain, target_url, first_seen, outreach_tactic (backlink index pull (Ahrefs/Semrush-class tool))
- `gbp_reviews`: review_id, rating, text, date, replied (Google Business Profile export)
- `ga4_tag_audit`: event_name, expected_daily_count, actual_daily_count, checked_at (GA4/GTM tag audit script)
- `product_feed_status`: sku, status, redirect_target, page_url (merchant feed + Shopify export)
- `us_holiday_calendar`: holiday, date, category_relevance, shipping_cutoff (shared with Organic room's holiday layer)
- `festive_calendar_india`: festival, date, category_relevance, shipping_cutoff (shared with Organic room's festive layer)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | skeleton, api, 3 tiles, 2 insights, 1 chart, audit with 13 rules | 2026-09-28 | S3.19 |

## Round 0 status

1. Shell, api.py (summary, findings), 3 tiles (organic visits, organic share of visits, non-branded CTR), 2 insights (SEO-R02, SEO-R01), 1 chart (organic sessions vs Search Console clicks, 12 weeks), query table, landing pages; all simulated Bombas data.
2. audit.py covers all 13 room rules; 4 read written tables (R01, R02, R03, R11), 9 read unavailable with the connector named.
3. SEO-R02 fires on Bombas: home page, query 'bombas', CTR 35 percent at position 1.1 against a 54 percent branded curve, $83,897 at stake in 28 days, high, confidence 0.7.
4. The branded curve (2x non-branded) is a rule constant; part of that stake may go to Bombas' own brand search ads, so read it as a ceiling.
5. Search Console has no metric in metrics.md yet; audit.py reads it with one GROUP BY. Propose ctr_by_query_group and cwv_pass_rate in a contract session (lcp_ms reads unavailable: speed_runs has no device or measured_at field).
6. Tests: tests/test_screen_seo.py, 11 passing; screen suite only fails the known test_screen_today tolerance. Screenshot round0.png at 1280 wide.
