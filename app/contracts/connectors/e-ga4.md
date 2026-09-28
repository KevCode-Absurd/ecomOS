# Connector census: GA4 Data API

Filled by a field-census session from the platform's official documentation. Every line carries the doc url it came from. Nothing from memory.

## Access
- auth: OAuth scope `https://www.googleapis.com/auth/analytics.readonly` (read-only). Auth via Application Default Credentials (user account) or a service account; REST calls send `Authorization: Bearer <token>`. Property-level access is granted manually in the GA4 UI, not through the API. https://developers.google.com/analytics/devguides/reporting/data/v1/quickstart
- property id: numeric GA4 property id in the request path as `properties/GA_PROPERTY_ID`, found in GA Admin > Property Settings; the old Universal Analytics "UA-" id is not supported. https://developers.google.com/analytics/devguides/reporting/data/v1/property-id
- rate limits, standard property: 200,000 tokens/property/day; 40,000 tokens/property/hour; 14,000 tokens/project+property/hour; 10 concurrent requests/property; 10 server errors/project+property/hour. Realtime and Funnel reports each have their own bucket with the same numeric limits. Daily quota resets at midnight Pacific Time. https://developers.google.com/analytics/devguides/reporting/data/v1/quotas
- rate limits, 360 property: 2,000,000 tokens/property/day; 400,000 tokens/property/hour; 140,000 tokens/project+property/hour; 50 concurrent requests/property; 50 server errors/project+property/hour. https://developers.google.com/analytics/devguides/reporting/data/v1/quotas
- thresholded-request allowance: 120 potentially-thresholded requests/property/hour (queries that touch demographic or interest dimensions). https://developers.google.com/analytics/devguides/reporting/data/v1/quotas
- token cost drivers: more dimensions, wider date ranges, higher-cardinality dimensions and higher event volume raise the token cost of a request; changing the `limit` (row count) does not meaningfully change token cost. Exceeding concurrency returns HTTP 429; back off, do not brute-retry. Pass `returnPropertyQuota: true` to get consumption back in `PropertyQuota`. https://developers.google.com/analytics/blog/2023/data-api-quota-management
- history available: not a fixed lookback window like other platforms. Standard aggregated reports (`runReport`, `runPivotReport`) are unaffected by the retention setting below; only Explorations and `runFunnelReport` are bounded by it. See "data retention settings" under Limits and gotchas. https://support.google.com/analytics/answer/7667196
- doc index: https://developers.google.com/analytics/devguides/reporting/data/v1/basics

## Objects and grain
| Object | Grain | Doc |
|---|---|---|
| Property (event stream) | GA4 has no separate session table; every report is a table over event data. `sessions` is itself a metric counting `session_start` events. | https://developers.google.com/analytics/devguides/reporting/data/v1/basics ; https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| runReport | Flat report, one row per requested dimension combination, recommended default method. | https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport |
| runPivotReport | Cross-tabulated report; a dimension is only returned if it is placed inside a `pivots` definition. | https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runPivotReport |
| runRealtimeReport | Events from the last 30 minutes (60 for 360 properties), data visible seconds after it is sent; narrower dimension/metric set and its own quota bucket. | https://developers.google.com/analytics/devguides/reporting/data/v1/realtime-basics |
| runFunnelReport (v1alpha) | Multi-step funnel over event sequences with an optional single breakdown dimension; alpha, can break without notice. | https://developers.google.com/analytics/devguides/reporting/data/v1/funnels |
| batchRunReports / batchRunPivotReports | Multiple runReport/runPivotReport requests in one call. | https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/batchRunReports |

## Fields

### Metrics (session/engagement)
| Field | Type | Meaning | Object | Doc |
|---|---|---|---|---|
| sessions | integer | Sessions that began on the site or app (event: session_start). | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| totalUsers | integer | Distinct users who logged at least one event. | user | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| newUsers | integer | Users interacting for the first time (event: first_open or first_visit). | user | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| activeUsers | integer | Distinct users who visited the site or app. | user | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| engagedSessions | integer | Sessions lasting over 10s, or with a key event, or 2+ screen views. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| engagementRate | float (fraction) | engagedSessions / sessions. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| averageSessionDuration | seconds | Average session duration. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| bounceRate | float (fraction) | (sessions − engagedSessions) / sessions. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| userEngagementDuration | seconds | Total time the site/app was in the foreground. | user | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| screenPageViews | integer | screen_view + page_view events. | event | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| screenPageViewsPerSession | float | screenPageViews / sessions. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| eventCount | integer | Count of events. | event | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| keyEvents | integer | Count of key events (GA4's 2024 rename of "conversions"). | event | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| sessionKeyEventRate | float (fraction) | Percent of sessions with any key event. Replaces the old "session conversion rate" naming. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| userKeyEventRate | float (fraction) | Percent of users who triggered any key event. Replaces the old "user conversion rate" naming. | user | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |

### Metrics (ecommerce and item-scoped)
| Field | Type | Meaning | Object | Doc |
|---|---|---|---|---|
| addToCarts | integer | Times users added items to cart. | event | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| checkouts | integer | begin_checkout events. | event | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| ecommercePurchases | integer | purchase events; excludes in_app_purchase and subscription events. | event | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| purchaseRevenue | currency | Purchase, ecommerce_purchase, in_app_purchase and app store subscription revenue, minus refunds. | transaction | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| grossPurchaseRevenue | currency | Same event set as purchaseRevenue, before refunds are subtracted. | transaction | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| totalRevenue | currency | Purchase + subscription + ad revenue, minus refunds. | transaction | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| refundAmount | currency | Total refunded transaction revenue (refund + app_store_refund events). | transaction | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| taxAmount | currency | Tax amount from the `tax` event parameter. | transaction | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| shippingAmount | currency | Shipping amount from the `shipping` event parameter. | transaction | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| transactions | integer | Count of transaction events (in_app_purchase, ecommerce_purchase, purchase, subscription renew/convert, refund). | transaction | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| transactionsPerPurchaser | float | Average transactions per purchaser. | user | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| totalPurchasers | integer | Users who logged a purchase event in the period. | user | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| firstTimePurchasers | integer | Users completing their first purchase event. | user | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| firstTimePurchaserRate | float (fraction) | First-time purchasers / active users. | user | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| averagePurchaseRevenue | currency | Average purchase revenue in the transaction group. | transaction | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| averagePurchaseRevenuePerUser | currency | Purchase revenue per active user (any event). | user | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| averagePurchaseRevenuePerPayingUser | currency | Purchase revenue per active user that logged a purchase (ARPPU). | user | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| cartToViewRate | float (fraction) | Users who added a product to cart / users who viewed the same product. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| purchaseToViewRate | float (fraction) | Users who purchased a product / users who viewed the same product. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemViewEvents | integer | view_item events. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemsViewed | integer | Item quantity in view_item events. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemsAddedToCart | integer | Item quantity in add_to_cart events. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemsCheckedOut | integer | Item quantity in begin_checkout events. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemsPurchased | integer | Item quantity in purchase events. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemRevenue | currency | price × quantity for an item, minus refunds; excludes tax and shipping. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| grossItemRevenue | currency | price × quantity for an item, before refunds. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemRefundAmount | currency | Refunded transaction revenue, items only. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemsClickedInList | integer | Item quantity in select_item events. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemsViewedInList | integer | Item quantity in view_item_list events. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemsViewedInPromotion | integer | Item quantity in view_promotion events. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| promotionViews / promotionClicks | integer | view_promotion / select_promotion events. | event | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |

Per-metric type (integer/float/currency/seconds) is not published as a static column in the schema table; it is returned at request time in `metricHeaders[].type` (enum `MetricType`: TYPE_INTEGER, TYPE_FLOAT, TYPE_CURRENCY, TYPE_SECONDS, etc.), or via `properties.getMetadata`. The types above are read off the schema descriptions and the `MetricType` enum and should be re-checked against a live `getMetadata` call before the connector goes live. https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/MetricType

### Dimensions
| Field | Type | Meaning | Object | Doc |
|---|---|---|---|---|
| date | string (YYYYMMDD) | Date of the event. | event | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| sessionSource | string | Source that initiated the session. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| sessionMedium | string | Medium that initiated the session. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| sessionSourceMedium | string | sessionSource + sessionMedium combined. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| sessionCampaignName | string | Marketing campaign name for the session. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| sessionCampaignId | string | Marketing campaign id for the session. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| sessionDefaultChannelGroup | string (enum) | Session's default channel group; see the channel taxonomy below. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| defaultChannelGroup | string (enum) | Default channel group attributed to the key event (event-level). | event | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| firstUserDefaultChannelGroup | string (enum) | Default channel group that first acquired the user. | user | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| firstUserPrimaryChannelGroup / primaryChannelGroup / sessionPrimaryChannelGroup | string | Primary channel group (custom channel groups feature) for the user, key event, or session. | user/event/session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| landingPage | string | Page path of the first pageview in a session. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| landingPagePlusQueryString | string | Landing page path plus query string. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| deviceCategory | string (enum) | Desktop, Tablet or Mobile. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| country | string | Country of the user activity. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| countryId | string (ISO 3166-1 alpha-2) | Geographic id of the country, derived from IP. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| region | string | Geographic region, derived from IP. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| city | string | City, derived from IP. | session | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| newVsReturning | string (new / returning) | New = 0 previous sessions; returning = 1+. | user | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemName | string | Item name. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemId | string | Item id. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemCategory ... itemCategory5 | string | Hierarchical product classification (e.g. Apparel/Mens/Summer/Shirts/T-shirts). | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemBrand | string | Brand name of the item. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemVariant | string | Item variant. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemAffiliation | string | Store or affiliation selling the item. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemListId / itemListName / itemListPosition | string/int | The list an item was shown or clicked in, and its position. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| itemPromotionId / itemPromotionName / itemPromotionCreativeName / itemPromotionCreativeSlot | string | Item promotion attributes. | item | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| orderCoupon | string | Coupon code applied at the order level. | transaction | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| transactionId | string | Ecommerce transaction id. | transaction | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |
| currencyCode | string (ISO 4217) | Local currency of the ecommerce event. | transaction | https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema |

A large family of platform-specific session dimensions also exists (sessionGoogleAds*, sessionManualSource/Medium/CampaignName/CampaignId/AdContent/Term/MarketingTactic/SourceMedium/SourcePlatform/CreativeFormat for UTM-tagged traffic, sessionCm360*, sessionDv360*, sessionSa360*). Out of scope for the base ecommerce contract; pull from the same schema page if a screen needs UTM-level detail. https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema

## Breakdowns and dimensions

GA4 has no fixed, published breakdown compatibility matrix. Compatibility is checked at request time with `properties.checkCompatibility` (send candidate `dimensions` and `metrics`, get back `dimensionCompatibilities[]` / `metricCompatibilities[]` each marked COMPATIBLE or INCOMPATIBLE), or read from the `category` field on `DimensionMetadata`/`MetricMetadata` returned by `properties.getMetadata` — fields in the same category (e.g. Ecommerce, Session, Item, Page/Screen) combine; item-scoped fields (itemRevenue, itemsViewed, itemName, ...) commonly fail to combine with session- or user-scoped fields outside their category, and this must be verified per pair with `checkCompatibility` rather than assumed.

| Breakdown | Allowed with | Not allowed with | Doc |
|---|---|---|---|
| Any dimension/metric pair | Query `checkCompatibility` per candidate pair before building a report | Item-scoped fields combined with unrelated session/user-scoped fields (verify per pair; no static list published) | https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/checkCompatibility |

sessionDefaultChannelGroup / defaultChannelGroup channel taxonomy (source/medium and campaign-name rules), the authoritative full list beyond the abbreviated set named on the schema page: Direct, Organic Search, Paid Search, Paid Social, Organic Social, Email, Affiliates, Referral, Display, Paid Shopping, Organic Shopping, Paid Video, Organic Video, Audio, SMS, Mobile Push Notifications, AI Assistant, Unassigned. https://support.google.com/analytics/answer/9756891

## Attribution and windows

GA4's Data API does not expose configurable attribution "windows" the way Meta or Google Ads do. `sessionDefaultChannelGroup`/`sessionSource`/`sessionMedium` are last-non-direct-click at the session level, derived from the `session_start` event's own source/medium parameters, not a lookback window over prior touches. `firstUserDefaultChannelGroup` is first-touch, assigned once at the user's first session. Ecommerce metrics (purchaseRevenue, transactions, itemRevenue, ...) are counted directly off the triggering event (purchase, add_to_cart, begin_checkout, ...) with no attribution model applied — they are not "attributed" conversions in the Meta/Google Ads sense, they are literal event counts and event-parameter sums. Key events (`keyEvents`, `sessionKeyEventRate`, `userKeyEventRate`) replace the old "conversions" naming (2024 rename); confirm exact current terminology against a live property before wiring a screen, since GA4 has renamed this concept before. https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema

## Limits and gotchas

- **Sampling.** `runReport` can return sampled data for large or complex queries; UI and API can use different thresholds, causing UI-vs-API discrepancies. Standard properties sample above roughly 10 million events used by a query; GA4 360 goes up to 1 billion (100 million default), and `reportTasks.create` can request `samplingLevel: UNSAMPLED` on 360 properties. Detect sampling via `samplingMetadatas` in the response's `ResponseMetaData`. https://developers.google.com/analytics/devguides/reporting/data/v1/reporting-data-expectations ; https://support.google.com/analytics/answer/13331292
- **Unique-count approximation.** Active Users and Sessions use HyperLogLog++ approximation in both UI and API, independent of the sampling flag. https://developers.google.com/analytics/devguides/reporting/data/v1/reporting-data-expectations
- **Data thresholding (privacy).** Rows with a small number of users can be dropped, mainly on demographic, interest or high-cardinality dimensions (e.g. search query). Thresholds are system-defined and not adjustable. Detect via `subjectToThresholding` in `ResponseMetaData`. Exact suppressed-row display (blank vs. dropped) is not documented — treat as open and test against a live property. https://developers.google.com/analytics/devguides/reporting/data/v1/reporting-data-expectations ; https://support.google.com/analytics/answer/9383630
- **"(other)" row.** High-cardinality dimensions (over roughly 500 unique values/day) roll long-tail values into an `(other)` row; filters cannot see inside it since it is applied post-aggregation. Detect via `dataLossFromOtherRow`. https://developers.google.com/analytics/devguides/reporting/data/v1/reporting-data-expectations
- **Reporting identity.** Blended vs. device-based identity settings change user counts and apply to both UI and API; a source of cross-tool mismatch to flag on any screen showing GA4 user counts. https://developers.google.com/analytics/devguides/reporting/data/v1/reporting-data-expectations
- **Event data retention.** Configurable to 2 or 14 months on standard properties (26/38/50 on 360). Does not affect standard `runReport`/`runPivotReport` aggregated reports; it only bounds Explorations and `runFunnelReport`, which query event-level data beyond the pre-aggregated tables. https://support.google.com/analytics/answer/7667196
- **Row limits and pagination.** `runReport`/`runPivotReport`/`runRealtimeReport` cap at 250,000 rows per request regardless of the requested limit; default row count if `limit` is unset is 10,000. Pagination is `limit` (page size) plus `offset` (start position), not cursor-based. https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport
- **Date ranges.** Multiple, including overlapping, date ranges are supported in one `runReport` request; no documented maximum span or count of ranges. https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runReport
- **Realtime window.** Fixed at up to 30 minutes historical on standard properties, 60 minutes on 360; not a configurable date range like `runReport`. Its own quota bucket, same numeric limits as Core. https://developers.google.com/analytics/devguides/reporting/data/v1/realtime-basics
- **Funnel reports are v1alpha.** "You should expect to encounter breaking changes before this feature is publicly released." Breakdown is limited to a single `breakdownDimension` per request, defaulting to the top 5 distinct values (overridable via `FunnelBreakdown.limit`). Can be sampled (`SamplingMetadata` in the response). No documented maximum step count or elapsed-time-between-steps limit; the 5-step docs example is illustrative, not a stated cap — confirm against a live property before building a contract that depends on a specific step ceiling. Its own quota bucket, same numeric limits as Core. https://developers.google.com/analytics/devguides/reporting/data/v1/funnels
- **Quota exhaustion.** Exceeding concurrent requests per property returns HTTP 429; back off rather than retry immediately. Pass `returnPropertyQuota: true` to read remaining quota per bucket in the response. https://developers.google.com/analytics/devguides/reporting/data/v1/quotas
- **Metric type is not static.** Whether a metric is an integer, float, currency or seconds value is only available at request time (`metricHeaders[].type`) or via `properties.getMetadata`, not as a fixed column on the public schema page; re-verify before hard-coding formatting rules. https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/MetricType

## Sample row

Representative shape for a `runReport` request grouping by date, source/medium, channel group and landing page, with session and ecommerce metrics — field names are exact API names from the Fields tables above; values are illustrative, not pulled from a live property.

```json
{
  "date": "20260927",
  "sessionSource": "google",
  "sessionMedium": "cpc",
  "sessionDefaultChannelGroup": "Paid Search",
  "landingPage": "/products/summer-tee",
  "deviceCategory": "mobile",
  "newVsReturning": "new",
  "sessions": 412,
  "engagedSessions": 265,
  "engagementRate": 0.6432,
  "addToCarts": 58,
  "checkouts": 21,
  "ecommercePurchases": 14,
  "transactions": 14,
  "purchaseRevenue": 1189.42,
  "cartToViewRate": 0.187,
  "purchaseToViewRate": 0.045
}
```

## Maps to ecomOS tables

| Table in contracts/data-sources.md | Fields used |
|---|---|
| `sessions` (date, source, medium, campaign, landing_page, device, product_view, add_to_cart, checkout, purchase) | date, sessionSource, sessionMedium, sessionCampaignName, sessionDefaultChannelGroup, landingPage, deviceCategory, itemViewEvents/itemsViewed, addToCarts, checkouts, ecommercePurchases, transactions, purchaseRevenue |
| `orders` (utm on order rows, channel reconciliation against Shopify) | sessionDefaultChannelGroup, sessionSource, sessionMedium, sessionCampaignName, transactionId, purchaseRevenue, taxAmount, shippingAmount — reconciled against Shopify's own order/session join, not assumed equal (GA4 counts events, Shopify counts orders) |
| `products` (funnel by sku, for the measurement and landing-page screens) | itemId, itemName, itemCategory..itemCategory5, itemBrand, itemsViewed, itemsAddedToCart, itemsCheckedOut, itemsPurchased, itemRevenue, cartToViewRate, purchaseToViewRate |
