# Connector census: Meta Marketing API (Insights + Ad Creative)

Filled by a field-census session from the platform's official documentation. Every line carries the doc url it came from. Nothing from memory. Read-only endpoints only: `ads_read`, never `ads_management`.

Items marked **UNVERIFIED** or **PARTIALLY VERIFIED** could not be confirmed against a directly-fetched official page in this session (a doc 404'd, or the detail came from a search snippet of an official page rather than a fetch of it). Do not build against those without re-checking.

## Access
- auth: OAuth permission `ads_read` for read-only ad report access. `ads_management` also exists but is write-capable and out of scope (ecomOS rule: Meta is read-only). (https://developers.facebook.com/docs/marketing-api/get-started/authorization)
- access tiers: Limited/dev access is "heavily rate-limited per ad account. For development only." Full/standard access is "lightly rate limited per ad account" and requires the app to have made at least 500 Marketing API calls in the last 15 days with an error rate under 15% in the last 500 calls. (https://developers.facebook.com/docs/marketing-api/get-started/authorization, https://developers.facebook.com/docs/marketing-api/insights/best-practices/)
- rate limits: Business Use Case (BUC) limit for `ads_insights`, per ad account per hour: Full access tier = 190,000 + 400 x number of active ads, minus 0.001 x user errors; Dev tier = 600 + 400 x number of active ads. Check the `X-Business-Use-Case` response header for `call_count`, `total_cputime`, `total_time`, `estimated_time_to_regain_access`. (https://developers.facebook.com/docs/marketing-api/overview/rate-limiting/)
  - Insights-specific throttle: response header `x-fb-ads-insights-throttle` returns JSON `{app_id_util_pct, acc_id_util_pct, ads_api_access_tier}` so a caller can see percent of capacity used before it is throttled. (https://developers.facebook.com/docs/marketing-api/insights/best-practices/)
- history available: 37 months maximum lookback for totals ("the start date of the time range cannot be beyond 37 months from the current date"). Breakdown-level data is narrower for several metric families as of the Jan 12 2026 change (see Limits and gotchas). (https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights/, https://developers.facebook.com/blog/post/2025/10/16/ads-insights-api-metric-availability-updates/)
- doc index: https://developers.facebook.com/docs/marketing-api/insights/

## Objects and grain
| Object | Grain | Doc |
|---|---|---|
| Account insights | `/{ad-account-id}/insights`, `level=account`, one row per `time_increment` (1-90 days, or `monthly`) | https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights/ |
| Campaign insights | `/{campaign-id}/insights` or account insights with `level=campaign`, daily via `time_increment=1` | https://developers.facebook.com/docs/marketing-api/insights/ |
| Ad set insights | `/{ad-set-id}/insights` or account insights with `level=adset`, daily via `time_increment=1` | https://developers.facebook.com/docs/marketing-api/insights/ |
| Ad insights | `/{ad-id}/insights` or account insights with `level=ad`, daily via `time_increment=1` | https://developers.facebook.com/docs/marketing-api/insights/ |
| Ad creative | `/{ad-creative-id}` node, one row per creative object | https://developers.facebook.com/docs/marketing-api/reference/ad-creative |

`level` enum values: `ad`, `adset`, `campaign`, `account`. `time_increment`: integer 1-90 (days), or `monthly`, or `all_days`. (https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights/) The claim that `all_days` is the default when `time_increment` is omitted is **UNVERIFIED** (third-party source, not confirmed on an official page).

## Fields
| Field | Type | Meaning | Object | Doc |
|---|---|---|---|---|
| `spend` | numeric string | estimated total spend on the campaign/ad set/ad during its schedule | Insights | https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights/ |
| `impressions` | numeric string | number of times ads were on screen | Insights | same |
| `reach` | numeric string | number of Accounts Center accounts that saw the ad at least once | Insights | same |
| `frequency` | numeric string | average number of times each person saw the ad | Insights | same |
| `clicks` | numeric string | number of clicks on the ads | Insights | same |
| `inline_link_clicks` | numeric string | clicks on links to select destinations/experiences; fixed 1-day-click attribution window regardless of the report's attribution setting | Insights | same |
| `cpm` | numeric string | average cost per 1,000 impressions | Insights | same |
| `cpc` | numeric string | average cost per click | Insights | same |
| `ctr` | numeric string | percentage of impressions that produced a click | Insights | same |
| `actions` | list of `AdsActionStats` | total actions attributed to the ad, one entry per `action_type` (or other `action_breakdowns`), each carrying per-attribution-window values | Insights | same; object shape: https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/ |
| `action_values` | list of `AdsActionStats` | total value of conversions attributed to the ad, same per-action-type/window shape as `actions` | Insights | https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights/ |
| `cost_per_action_type` | list of `AdsActionStats` | average cost per relevant action, keyed by `action_type` | Insights | same |
| `purchase_roas` | list of `AdsActionStats` | total ROAS from purchases, keyed by `action_type` | Insights | same |
| `video_p25_watched_actions` ... `video_p100_watched_actions` | list of `AdsActionStats` | count of plays that reached 25/50/75/95/100% of video length, including skips to that point | Insights | same |
| `video_thruplay_watched_actions` | list of `AdsActionStats` (assumed, same family) | **UNVERIFIED**: not confirmed against a directly fetched official page in this session | Insights | not confirmed |
| `fields` (request param) | list of string | which fields to return; default is `impressions` and `spend` if omitted | Insights request | https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights/ |
| `filtering` (request param) | list of `Filter` | filter objects applied to the report | Insights request | same |
| `sort` (request param) | list of string | field name plus `ascending`/`descending` | Insights request | same |
| `date_preset` (request param) | enum, default `last_30d` | relative time range | Insights request | same |
| `time_range` (request param) | object `{since, until}` | explicit date range, `YYYY-MM-DD` | Insights request | same |
| `body` | string | ad body text; not supported for video post creatives | Ad Creative | https://developers.facebook.com/docs/marketing-api/reference/ad-creative |
| `title` | string | title for a link ad not belonging to a page | Ad Creative | same |
| `call_to_action_type` | enum | CTA button text/header, e.g. `OPEN_LINK`, `LIKE_PAGE`, `SHOP_NOW`, `INSTALL_APP`, `BOOK_NOW` (80+ values); must align with the campaign objective | Ad Creative | same |
| `image_hash` | string | hash referencing an image in the ad account's image library; do not send alongside `image_url` | Ad Creative | same |
| `video_id` | numeric string | Facebook object ID for the creative's video | Ad Creative | same |
| `thumbnail_url` | string | thumbnail image URL, with optional `thumbnail_width`/`thumbnail_height` | Ad Creative | same |
| `object_story_spec` | object (`AdCreativeObjectStorySpec`) | builds an unpublished page post to turn into an ad; carries `link_data`/`photo_data`/`video_data`/`text_data`/`template_data` plus a page id | Ad Creative | same |
| `asset_feed_spec` | object (`AdAssetFeedSpec`) | Dynamic Creative: an asset feed of multiple images/text/other assets used to auto-generate ad variations | Ad Creative | same |

## Breakdowns and dimensions
Full `breakdowns` enum confirmed on the doc: `action_device`, `action_canvas_component_name`, `action_carousel_card_id`, `action_carousel_card_name`, `action_destination`, `action_reaction`, `action_target_id`, `action_type`, `action_video_sound`, `action_video_type`, `ad_format_asset`, `age`, `app_id`, `body_asset`, `call_to_action_asset`, `country`, `description_asset`, `device_platform`, `dma`, `frequency_value`, `gender`, `hourly_stats_aggregated_by_advertiser_time_zone`, `hourly_stats_aggregated_by_audience_time_zone`, `image_asset`, `impression_device`, `is_conversion_id_modeled`, `link_url_asset`, `place_page_id`, `platform_position`, `product_id`, `publisher_platform`, `region`, `skan_campaign_id`, `skan_conversion_id`, `title_asset`, `user_segment_key`, `video_asset`. (https://developers.facebook.com/docs/marketing-api/insights/breakdowns/)

Separate `action_breakdowns` parameter for how `actions`/`action_values` are split: `action_type`, `action_target_id`, `action_destination`, `action_device`, `action_canvas_component_name`, `action_carousel_card_id`, `action_carousel_card_name`, `action_reaction`, `action_video_type`, `action_video_sound`. If omitted, `action_type` is implied. Only certain permutations of `action_breakdowns` are storable together. (https://developers.facebook.com/docs/marketing-api/insights/action-breakdowns/)

| Breakdown | Allowed with | Not allowed with | Doc |
|---|---|---|---|
| `page_place_id` | — | account-level insights (cannot be queried together) | https://developers.facebook.com/docs/marketing-api/insights/breakdowns/ |
| `hourly_stats_aggregated_by_advertiser_time_zone`, `hourly_stats_aggregated_by_audience_time_zone` | — | any `video_*` fields; any field prefixed `unique_*`; `reach`; `frequency` | same |
| `video_avg_time_watched_actions` (field) | — | `region` breakdown | same |
| Type 1 breakdowns: `region`, `dma`, `hourly_stats_aggregated_by_audience_time_zone`, `hourly_stats_aggregated_by_advertiser_time_zone` | on-Meta action metrics | off-Meta (offsite) action metrics | same |
| Type 2 breakdowns: `action_device`, `action_destination`, `action_target_id`, `product_id`, `action_carousel_card_id`/`action_carousel_card_name`, `action_canvas_component_name` | on-Meta action metrics | restricted for off-Meta action metrics | same |

## Attribution and windows
`action_attribution_windows` enum: `1d_view`, `7d_view`, `28d_view`, `1d_click`, `7d_click`, `28d_click`, `1d_ev`, `dda`, `default`, `7d_view_first_conversion`, `28d_view_first_conversion`, `7d_view_all_conversions`, `28d_view_all_conversions`, `skan_view`, `skan_click`, `skan_click_second_postback`, `skan_view_second_postback`, `skan_click_third_postback`, `skan_view_third_postback`. Default value `default` expands to `["7d_click", "1d_view"]`. (https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights/)

The `AdsActionStats` object (used by `actions`, `action_values`, `cost_per_action_type`, `purchase_roas`) carries `action_type`, an unwindowed `value` (default-window metric), plus per-window fields `1d_click`, `7d_click`, `28d_click`, `1d_view`, `7d_view`, `28d_view`, `dda`, `incrementality`, `inline`, and `_all_conversions`/`_first_conversion` variants per window. (https://developers.facebook.com/docs/marketing-api/reference/ads-action-stats/)

Example `action_type` values seen: `offsite_conversion.fb_pixel_purchase`, `offsite_conversion.fb_pixel_add_to_cart`, `offsite_conversion.fb_pixel_initiate_checkout`, `offsite_conversion.fb_pixel_view_content`, `link_click`, `landing_page_view`, grouped/omni types `omni_purchase`, `page_engagement`, `post_engagement`, `video_view`. The exact spellings `omni_add_to_cart`, `omni_initiate_checkout`, `omni_view_content` are **PARTIALLY VERIFIED**: the `omni_` prefix pattern and `omni_purchase` itself are confirmed on the ads-action-stats doc, the other three names are inferred from the pattern plus non-primary sources, not from a directly fetched, quoted official page.

**2026 change, effective Jan 12 2026** (https://developers.facebook.com/blog/post/2025/10/16/ads-insights-api-metric-availability-updates/):
- `7d_view` and `28d_view` attribution windows will no longer be returned (calls requesting them get empty data for those values going forward).
- `1d_click`, `7d_click`, `28d_click`, `1d_ev` (1-day engaged view) and `1d_view` continue to be available, in addition to default values based on the advertiser's own attribution settings.
- No official confirmation found that `28d_click` itself is deprecated — treat it as still supported per the parameter's current enum list.

## Limits and gotchas
- **37-month cap**: total-field values stay available for up to 37 months; the start date of any time range cannot be more than 37 months back. (https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights/, https://developers.facebook.com/blog/post/2025/10/16/ads-insights-api-metric-availability-updates/)
- **Reach with breakdowns narrowed**: as of June 10 2025, `reach` is no longer returned for standard queries that combine `breakdowns` with a `start_date` more than 13 months old. (https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights/)
- **2026 breakdown narrowing** (effective Jan 12 2026, same blog as above): unique-count fields (`unique_actions`, `cost_per_unique_action_type`) with any breakdowns limited to 13 months; hourly breakdowns limited to 13 months; frequency breakdowns limited to 6 months; MMM (marketing mix modeling) breakdowns restricted to asynchronous report jobs only.
- **Sync vs async**: try synchronous requests first; they can time out on large pulls. For large volumes, POST to create an async report run, poll for completion, then GET the rows. Workflow: POST `<AD_OBJECT>/insights` returns a `report_run_id` (`AdReportRun`); poll until `async_status` = "Job Completed" and `async_percent_completion` = 100; then GET `<AD_REPORT_RUN_ID>/insights` for rows. Do not store `report_run_id` long term — it expires after 30 days. This async field/example detail is **PARTIALLY VERIFIED**: the direct fetch of `https://developers.facebook.com/docs/marketing-api/reference/ad-report-run/` returned 404 in this session; the detail came from a search-engine snippet of Meta's own docs, not a confirmed direct fetch. Re-verify before relying on exact field names. (workflow description: https://developers.facebook.com/docs/marketing-api/insights/best-practices/)
- **Batching**: use batch requests for multiple sync calls to avoid rate-limit and timeout issues. (https://developers.facebook.com/docs/marketing-api/insights/best-practices/)
- **Pagination**: standard Graph API cursor pagination, `paging.cursors.{before,after}`. (https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights/, https://developers.facebook.com/docs/marketing-api/insights/)
- **Access tier gates rate limit**, not just permissions: dev/limited tier is unusable for a live advertiser at volume; full/standard access needs a 15-day history of at least 500 calls with under 15% error rate. (https://developers.facebook.com/docs/marketing-api/get-started/authorization, https://developers.facebook.com/docs/marketing-api/insights/best-practices/)
- **Dynamic/flexible creative flag**: any creative using `asset_feed_spec` is a Dynamic Creative generating multiple variations from one asset feed; per ecomOS rule, flag these and mixed creatives rather than treating each generated variation as a distinct fixed ad. (https://developers.facebook.com/docs/marketing-api/reference/ad-creative)
- Two fields referenced in `PRODUCT-PLAN.md#4.2` (`video_thruplay_watched_actions`, and the exact `omni_*` action-type spellings beyond `omni_purchase`) are **UNVERIFIED/PARTIALLY VERIFIED** above; re-check against a live account or a successful direct doc fetch before depending on them.

## Sample row
Illustrative only, built from confirmed field names and shapes (not a live pull; no numbers here represent real Meta data):
```json
{
  "date_start": "2026-09-24",
  "date_stop": "2026-09-24",
  "account_id": "123456789012345",
  "campaign_id": "987654321098765",
  "adset_id": "876543210987654",
  "ad_id": "765432109876543",
  "spend": "142.37",
  "impressions": "18420",
  "reach": "15230",
  "frequency": "1.209",
  "clicks": "312",
  "inline_link_clicks": "198",
  "cpm": "7.73",
  "cpc": "0.4563",
  "ctr": "1.694",
  "actions": [
    { "action_type": "landing_page_view", "value": "150" },
    { "action_type": "omni_add_to_cart", "value": "40", "1d_view": "8", "7d_click": "32" },
    { "action_type": "omni_purchase", "value": "9", "1d_view": "1", "7d_click": "8" }
  ],
  "action_values": [
    { "action_type": "omni_purchase", "value": "612.00", "1d_view": "68.00", "7d_click": "544.00" }
  ],
  "cost_per_action_type": [
    { "action_type": "omni_purchase", "value": "15.82" }
  ],
  "purchase_roas": [
    { "action_type": "omni_purchase", "value": "4.30" }
  ],
  "video_p25_watched_actions": [
    { "action_type": "video_view", "value": "2100" }
  ],
  "video_p100_watched_actions": [
    { "action_type": "video_view", "value": "410" }
  ]
}
```

## Maps to ecomOS tables
| Table in contracts/data-sources.md | Fields used |
|---|---|
| `ad_rows` | campaign id, ad set id, ad id, creative id (from `object_story_spec`/`asset_feed_spec` on the linked Ad Creative), `spend`, `impressions`, `reach`, `clicks`, `action_type=omni_purchase` from `actions` (purchases), matching `action_values` entry (purchase_value); daily grain via `level=ad`, `time_increment=1` |
