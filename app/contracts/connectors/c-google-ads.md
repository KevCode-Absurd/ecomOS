# Connector census: Google Ads API

Filled by a field-census session from the platform's official documentation. Every line carries the doc url it came from. Nothing from memory.

## Access
- auth: OAuth scope `https://www.googleapis.com/auth/adwords` — there is no separate read-only scope; read-only use means only issuing `search`/`searchStream` (GAQL) calls and never `mutate`. https://developers.google.com/google-ads/api/docs/oauth/single-user-authentication
- developer token access tiers (govern daily operation caps, not auth): Test 15,000 ops/day (test accounts only); Explorer 2,880 ops/day production, 15,000 test, blocks account creation/user mgmt/planning/billing; Basic 15,000 ops/day both, needs brand verification; Standard unlimited ops/day, includes a "Reporting" permissible-use category restricted to read-only/search operations. https://developers.google.com/google-ads/api/docs/access-levels
- rate limits: mutate operations capped at 10,000 per request (`TOO_MANY_MUTATE_OPERATIONS` beyond that — not relevant to a read-only integration but documents the request ceiling), gRPC response cap 64 MB, conversion uploads capped at 2,000/request, Keyword Planning ideas limited to 1 QPS (2 QPS for ad-group-theme generation), plus an hourly system rate limit separate from the daily operations cap. https://developers.google.com/google-ads/api/docs/best-practices/quotas
- history available: granular date segments (`segments.date`, `segments.week`, etc.) are queryable only 37 months back — older requests return `DateRangeError`. Aggregated segments (`segments.month`, `.quarter`, `.year`) and other account data retain 11 years. The 37-month cutoff took effect June 2026, so it is in force today (28 Sep 2026). https://developers.google.com/google-ads/api/docs/reporting/zero-metrics
- doc index: https://developers.google.com/google-ads/api/fields/latest/overview

## Objects and grain
| Object | Grain | Doc |
|---|---|---|
| campaign | campaign x date (x segments selected) | https://developers.google.com/google-ads/api/fields/v25/campaign |
| ad_group | ad group x date | https://developers.google.com/google-ads/api/fields/v25/ad_group |
| ad_group_ad (ad) | ad x date | https://developers.google.com/google-ads/api/fields/v25/ad_group_ad |
| ad_group_criterion / keyword_view | keyword criterion x date | https://developers.google.com/google-ads/api/fields/v25/ad_group_criterion , https://developers.google.com/google-ads/api/fields/v25/keyword_view |
| search_term_view | search term x ad group (x date). Excludes Performance Max data — use campaign_search_term_view for PMax | https://developers.google.com/google-ads/api/fields/v25/search_term_view |
| shopping_performance_view | product segment combination x date (singleton resource per customer, rows come from segments.product_*) | https://developers.google.com/google-ads/api/fields/v25/shopping_performance_view |
| asset_group (Performance Max) | asset group x date | https://developers.google.com/google-ads/api/fields/v25/asset_group |
| asset_group_asset | asset x asset group x date | https://developers.google.com/google-ads/api/fields/v25/asset_group_asset |
| metrics, segments | not standalone FROM-able resources; field sets joined onto the resources above | https://developers.google.com/google-ads/api/fields/latest/overview |

## Fields
| Field | Type | Meaning | Object | Doc |
|---|---|---|---|---|
| campaign.id | INT64 | campaign id | campaign | https://developers.google.com/google-ads/api/fields/v25/campaign |
| campaign.name | STRING | campaign name | campaign | https://developers.google.com/google-ads/api/fields/v25/campaign |
| campaign.status | ENUM | ENABLED/PAUSED/REMOVED/UNKNOWN/UNSPECIFIED | campaign | https://developers.google.com/google-ads/api/fields/v25/campaign |
| campaign.advertising_channel_type | ENUM | Search, Display, Shopping, Performance Max, etc. | campaign | https://developers.google.com/google-ads/api/fields/v25/campaign |
| campaign.bidding_strategy_type | ENUM | bidding strategy in use | campaign | https://developers.google.com/google-ads/api/fields/v25/campaign |
| ad_group_ad.status | ENUM | ENABLED/PAUSED/REMOVED | ad_group_ad | https://developers.google.com/google-ads/api/fields/v25/ad_group_ad |
| ad_group_ad.ad.id | INT64 | ad id | ad_group_ad | https://developers.google.com/google-ads/api/fields/v25/ad_group_ad |
| ad_group_ad.ad.type | ENUM | ad format (RESPONSIVE_SEARCH_AD, EXPANDED_TEXT_AD, PMax formats, etc.) | ad_group_ad | https://developers.google.com/google-ads/api/fields/v25/ad_group_ad |
| ad_group_ad.ad.final_urls | STRING (repeated) | landing page urls | ad_group_ad | https://developers.google.com/google-ads/api/fields/v25/ad_group_ad |
| ad_group_ad.ad.responsive_search_ad.headlines | MESSAGE (repeated) | RSA headline assets | ad_group_ad | https://developers.google.com/google-ads/api/fields/v25/ad_group_ad |
| ad_group_ad.policy_summary.approval_status | ENUM | ad review status | ad_group_ad | https://developers.google.com/google-ads/api/fields/v25/ad_group_ad |
| ad_group_criterion.keyword.text | STRING | keyword text, max 80 chars / 10 words | ad_group_criterion (keyword) | https://developers.google.com/google-ads/api/fields/v25/ad_group_criterion |
| ad_group_criterion.keyword.match_type | ENUM | BROAD/EXACT/PHRASE/UNKNOWN/UNSPECIFIED | ad_group_criterion (keyword) | https://developers.google.com/google-ads/api/fields/v25/ad_group_criterion |
| ad_group_criterion.quality_info.quality_score | INT32 | 1-10 quality score; may be unpopulated if Google lacks enough data | ad_group_criterion (keyword) | https://developers.google.com/google-ads/api/fields/v25/ad_group_criterion |
| ad_group_criterion.quality_info.creative_quality_score | ENUM | ABOVE_AVERAGE/AVERAGE/BELOW_AVERAGE, expected ad CTR component | ad_group_criterion (keyword) | https://developers.google.com/google-ads/api/fields/v25/ad_group_criterion |
| ad_group_criterion.quality_info.post_click_quality_score | ENUM | landing page quality component | ad_group_criterion (keyword) | https://developers.google.com/google-ads/api/fields/v25/ad_group_criterion |
| ad_group_criterion.quality_info.search_predicted_ctr | ENUM | expected CTR component | ad_group_criterion (keyword) | https://developers.google.com/google-ads/api/fields/v25/ad_group_criterion |
| metrics.historical_quality_score | INT64 | quality score at the time of the historical event | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.historical_creative_quality_score / historical_landing_page_quality_score / historical_search_predicted_ctr | ENUM | historical equivalents of the quality_info components | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| search_term_view.search_term | STRING | the actual search query | search_term_view | https://developers.google.com/google-ads/api/fields/v25/search_term_view |
| search_term_view.status | ENUM | ADDED/ADDED_EXCLUDED/EXCLUDED/NONE — whether the term is one of your targeted or excluded keywords | search_term_view | https://developers.google.com/google-ads/api/fields/v25/search_term_view |
| segments.product_item_id / product_title / product_brand / product_category_level1 | STRING/RESOURCE_NAME | product dimensions driving shopping_performance_view rows | shopping_performance_view | https://developers.google.com/google-ads/api/fields/v25/shopping_performance_view |
| asset_group.id | INT64 | asset group id | asset_group | https://developers.google.com/google-ads/api/fields/v25/asset_group |
| asset_group.name | STRING | unique under a campaign | asset_group | https://developers.google.com/google-ads/api/fields/v25/asset_group |
| asset_group.final_urls | STRING (repeated) | PMax landing pages, eligible for URL expansion by default | asset_group | https://developers.google.com/google-ads/api/fields/v25/asset_group |
| asset_group.ad_strength | ENUM | EXCELLENT/GOOD/AVERAGE/POOR/NO_ADS/PENDING | asset_group | https://developers.google.com/google-ads/api/fields/v25/asset_group |
| metrics.impressions | INT64 | impressions | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.clicks | INT64 | clicks | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.cost_micros | INT64 | sum of CPC and CPM cost, in micros | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.conversions | DOUBLE | conversions from actions where include_in_conversions_metric is true | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.conversions_value | DOUBLE | value of the above | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.all_conversions | DOUBLE | conversions from all conversion actions, ignoring include_in_conversions_metric | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.all_conversions_value | DOUBLE | value of the above | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.ctr | DOUBLE | click-through rate | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.average_cpc | DOUBLE | average cost per click | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.search_impression_share | DOUBLE | share of eligible search impressions won. Reported 0.1-1; below 0.1 shown as 0.0999 | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.search_top_impression_share | DOUBLE | share shown anywhere above organic results | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.search_absolute_top_impression_share | DOUBLE | share shown as the very first ad | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.search_budget_lost_impression_share | DOUBLE | share lost to budget. Reported 0-0.9; above 0.9 shown as 0.9001 | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.search_rank_lost_impression_share | DOUBLE | share lost to ad rank | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.search_budget_lost_absolute_top_impression_share / search_rank_lost_absolute_top_impression_share | DOUBLE | absolute-top variants of the two lost-share metrics | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |
| metrics.content_impression_share / content_budget_lost_impression_share / content_rank_lost_impression_share | DOUBLE | Display/Content Network equivalents. No content_top_impression_share or content_absolute_top_impression_share exists — "top impression" is Search-only in this API | metrics | https://developers.google.com/google-ads/api/fields/v25/metrics |

## Breakdowns and dimensions
| Breakdown | Allowed with | Not allowed with | Doc |
|---|---|---|---|
| segments.date / week / month / quarter | most resources above | granular (date/week) segments beyond 37 months back (use month/quarter/year instead) | https://developers.google.com/google-ads/api/docs/reporting/zero-metrics |
| segments.device | campaign, ad_group, ad_group_ad, keyword_view, etc. | — | https://developers.google.com/google-ads/api/fields/v25/segments |
| segments.click_type | most performance resources | — | https://developers.google.com/google-ads/api/fields/v25/segments |
| segments.ad_network_type | most performance resources | — | https://developers.google.com/google-ads/api/fields/v25/segments |
| segments.hour, segments.day_of_week | most performance resources | — | https://developers.google.com/google-ads/api/fields/v25/segments |
| segments.geo_target_country / geo_target_region | most performance resources | — | https://developers.google.com/google-ads/api/fields/v25/segments |
| segments.ad_sub_format_type | must always be paired with segments.ad_format_type | never selected alone | https://developers.google.com/google-ads/api/fields/v25/segments |
| segments.keyword.* (keyword text/match type segment) | Search campaigns | excludes Dynamic Search Ads, Shopping campaign and Performance Max data from the result set when selected | https://developers.google.com/google-ads/api/docs/reporting/segmentation |
| any additional segment field, generally | — | each extra segment field can multiply row count "exponentially"; per-resource compatibility must be checked on that resource's own field-reference page (filterable fields/segments/metrics table) | https://developers.google.com/google-ads/api/docs/reporting/segmentation , https://developers.google.com/google-ads/api/fields/v25/campaign |

## Attribution and windows
- Attribution models (on `conversion_action.attribution_model_settings.attribution_model`, ENUM): `EXTERNAL`, `GOOGLE_ADS_LAST_CLICK`, `GOOGLE_SEARCH_ATTRIBUTION_DATA_DRIVEN`, `GOOGLE_SEARCH_ATTRIBUTION_FIRST_CLICK`, `GOOGLE_SEARCH_ATTRIBUTION_LINEAR`, `GOOGLE_SEARCH_ATTRIBUTION_POSITION_BASED`, `GOOGLE_SEARCH_ATTRIBUTION_TIME_DECAY`, `UNKNOWN`, `UNSPECIFIED`. https://developers.google.com/google-ads/api/fields/v25/conversion_action
- `conversion_action.click_through_lookback_window_days` (INT64): max days between an interaction and a conversion event that still counts. https://developers.google.com/google-ads/api/fields/v25/conversion_action
- `conversion_action.view_through_lookback_window_days` (INT64): max days between an impression and a view-through conversion (no click). https://developers.google.com/google-ads/api/fields/v25/conversion_action
- UNCONFIRMED: the exact allowed numeric day ranges for the two lookback window fields above (a commonly cited [1,30]/[1,60] split by conversion-action type could not be verified against a fetched official doc page). Verify against the live `ConversionAction` field reference before relying on a specific number.
- Conversion value fields: `metrics.conversions_value`, `metrics.all_conversions_value`, and the "by conversion date" variants `metrics.conversions_value_by_conversion_date` / `metrics.all_conversions_value_by_conversion_date` / `metrics.conversions_by_conversion_date` (bucket by the conversion event's own date rather than the interaction/click date). `metrics.value_per_conversion` = conversions_value / conversions; `metrics.value_per_all_conversions` = all_conversions_value / all_conversions. `conversion_action.value_settings.default_value` is used when an incoming conversion event has an invalid, disallowed or missing value. https://developers.google.com/google-ads/api/fields/v25/metrics , https://developers.google.com/google-ads/api/fields/v25/conversion_action

## Limits and gotchas
- Search terms report privacy threshold: "Some search terms that do not have enough query activity are omitted from the search terms report to maintain our standards on data privacy." Clicks from these hidden terms still count in the campaign total but are excluded from `search_term_view` rows, so campaign-level clicks will exceed the sum of search-term rows — do not use this view for reconciliation. No numeric threshold is published. https://developers.google.com/google-ads/api/docs/campaigns/ai-max-for-search-campaigns/ai-max-reporting (background: https://support.google.com/google-ads/answer/11127882, grouped-theme surfacing via Search Terms Insights: https://support.google.com/google-ads/answer/11386930)
- Performance Max transparency: PMax campaigns "don't have standard AdGroup and AdGroupAd entities... querying resources such as ad_group or ad_group_ad won't return any data for your Performance Max campaigns" — no ad-group or ad-level reporting, and no keyword-level resource (asset targeting is signal-based). Reporting surface instead: `campaign` + `performance_max_placement_view` (placements), `asset_group` (ad strength, performance by channel), `asset_group_asset` (per-asset performance), `asset_group_top_combination_view` (top asset combinations), `asset_group_product_group_view` / `shopping_performance_view` / `shopping_product` (retail), `location_view` (campaign criterion/location), and `campaign_search_term_view` for PMax search terms (`search_term_view` explicitly excludes PMax data). https://developers.google.com/google-ads/api/docs/performance-max/reporting
- Pagination: `GoogleAdsService.Search`/`SearchStream` pages at up to 10,000 rows; `page_size` defaults to 10,000 and (v17+) any other value returns `PAGE_SIZE_NOT_SUPPORTED`; page with `page_token` from the previous response's `next_page_token` (omitted on the final page). https://developers.google.com/google-ads/api/docs/reporting/paging
- Zero-metric rows are excluded by default: "rows where all selected metrics equal zero are automatically excluded from results" — filter explicitly (e.g. `WHERE metrics.impressions > 0`) to control this. https://developers.google.com/google-ads/api/docs/reporting/zero-metrics
- Removed/ended entities are not auto-filtered by the API the way the UI filters them: "the UI implicitly filters out removed entities, whereas the API does not" — add `WHERE campaign.status != 'REMOVED'` (and equivalent for ad group/ad/criterion) to match UI defaults. https://developers.google.com/google-ads/api/docs/reporting/uireports
- Date range: granular date segments only queryable 37 months back; use `segments.month`/`.quarter`/`.year` for older aggregated history. https://developers.google.com/google-ads/api/docs/reporting/zero-metrics
- `click_view` (replacement for the legacy Click Performance Report): "Queries including ClickView must have a filter limiting the results to one day and can be requested for dates back to 90 days before the time of the request." https://developers.google.com/google-ads/api/fields/v25/click_view
- Row explosion: "For each additional segment field included in your report query, the number of rows can increase exponentially." https://developers.google.com/google-ads/api/docs/reporting/segmentation
- Rate/response limits: mutate operations capped at 10,000/request, gRPC response cap 64 MB, conversion uploads capped at 2,000/request. https://developers.google.com/google-ads/api/docs/best-practices/quotas

## Sample row
Constructed illustrative example only — field names, GAQL paths and data types match the documented definitions above; the numeric values are invented, not real account data.
```json
{
  "campaign.id": "20123456789",
  "campaign.name": "Search - Brand - US",
  "segments.date": "2026-09-15",
  "metrics.impressions": "48213",
  "metrics.clicks": "2190",
  "metrics.cost_micros": "1875430000",
  "metrics.conversions": "63.0",
  "metrics.conversions_value": "5482.75",
  "metrics.search_impression_share": "0.7834"
}
```

## Maps to ecomOS tables
| Table in contracts/data-sources.md | Fields used |
|---|---|
| `google_rows` (Google Ads daily by campaign and search term) | campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, segments.date, search_term_view.search_term, search_term_view.status, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions, metrics.conversions_value, metrics.all_conversions, metrics.all_conversions_value, metrics.ctr, metrics.average_cpc, metrics.search_impression_share, metrics.search_top_impression_share, metrics.search_absolute_top_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share, ad_group_criterion.quality_info.quality_score, asset_group.ad_strength (for PMax rows, via asset_group instead of ad_group_ad) |
