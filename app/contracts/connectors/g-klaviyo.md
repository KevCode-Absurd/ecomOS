# Connector census: Klaviyo

Filled by a field-census session from the platform's official documentation. Every line carries the doc url it came from. Nothing from memory. Researched Sep 2026 against revision `2026-07-15` (the newest non-`.pre` GA revision at research time; check https://developers.klaviyo.com/en/docs/changelog_ before build).

## Access
- auth: private API key (Custom, Read-Only or Full Access) sent as a bearer token, or OAuth for marketplace apps. Read-only scopes cannot be added after a key is created. https://developers.klaviyo.com/en/docs/authenticate_
- read-only scopes used by this connector: `profiles:read`, `lists:read`, `segments:read`, `flows:read`, `campaigns:read`, `metrics:read`, `events:read`, `subscriptions:read`, `tags:read`. Klaviyo's own reporting docs say reporting needs at minimum `campaigns:read`, `flows:read`, `forms:read`, `segments:read`. https://developers.klaviyo.com/en/docs/authenticate_
- every request also carries a `revision` header, an ISO date e.g. `revision: 2026-07-15`. A revision is stable for about 1 year, deprecated for about 1 year, then retired (can start returning 410). Changelog: https://developers.klaviyo.com/en/docs/changelog_ ; versioning policy: https://developers.klaviyo.com/en/docs/api_versioning_and_deprecation_policy
- rate limits: tiered burst (1s window) / steady (1m window) per endpoint. Table: XS 1/s·15/m, S 3/s·60/m, M 10/s·150/m, L 75/s·700/m, XL 350/s·3500/m. https://developers.klaviyo.com/en/docs/rate_limits_and_error_handling. Confirmed per-endpoint tiers: Get Lists = L (page showed 75/s·750/m, which does not match the L row exactly — re-verify live before relying on the exact steady number, https://developers.klaviyo.com/en/reference/get_lists); Query Metric Aggregates and the flow-message endpoints = S, 3/s·60/m (https://developers.klaviyo.com/en/reference/query_metric_aggregates, https://developers.klaviyo.com/en/reference/get_flow_action_messages). Response headers `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`; on 429, `Retry-After` instead. `additional-fields`/`include` params get stricter limits. https://developers.klaviyo.com/en/docs/rate_limits_and_error_handling
- history available: Metric Aggregates queries are capped at a 1-year date range per request, so history is paged by moving the filter window, not a retention limit. https://developers.klaviyo.com/en/docs/using_the_query_metric_aggregates_endpoint. Event timestamps are only accepted from 1990 through now+1 year on write. https://developers.klaviyo.com/en/reference/events_api_overview. No overall stated retention ceiling ("we keep N months of history") was found on developers.klaviyo.com in this pass — treat as unconfirmed, do not assert unlimited retention.
- doc index: https://developers.klaviyo.com/en/reference/api_overview and https://developers.klaviyo.com/en/docs

## Objects and grain
| Object | Grain | Doc |
|---|---|---|
| Profile | one customer/contact record | https://developers.klaviyo.com/en/reference/get_profiles |
| List | one named, static subscriber collection | https://developers.klaviyo.com/en/reference/get_lists |
| Segment | one dynamically computed audience definition; membership evaluated live against `definition`, not stored | https://developers.klaviyo.com/en/reference/get_segments |
| Flow | one automation (a full multi-step workflow, e.g. Welcome Series) | https://developers.klaviyo.com/en/reference/get_flows |
| Flow Action | one step inside a flow (an email send, a delay, a conditional split) | https://developers.klaviyo.com/en/reference/get_flow_actions |
| Flow Message | one message asset (one email/SMS/push variant) attached to a flow action; one action can have several (A/B variants) | https://developers.klaviyo.com/en/reference/get_flow_action_messages |
| Campaign | one campaign send (one-time or A/B, single channel: email, SMS or push) | https://developers.klaviyo.com/en/reference/get_campaigns |
| Campaign Message | one message variant inside a campaign (a campaign has 1+ messages; A/B tests have several) | https://developers.klaviyo.com/en/reference/get_campaign_messages |
| Metric | one event-type definition (e.g. "Placed Order"), not an individual occurrence | https://developers.klaviyo.com/en/reference/get_metrics |
| Metric Aggregate | one time-bucket x dimension-combination row from a `POST /api/metric-aggregates/` query (e.g. revenue for one flow in one month) | https://developers.klaviyo.com/en/reference/query_metric_aggregates |
| Event | one individual occurrence of a metric for one profile | https://developers.klaviyo.com/en/reference/get_events |

## Fields
| Field | Type | Meaning | Object | Doc |
|---|---|---|---|---|
| `id` | string | Klaviyo primary key | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `email`, `phone_number` (E.164), `external_id` | string | identifiers | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `first_name`, `last_name`, `organization`, `title`, `locale`, `image` | string | profile attributes | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `created`, `updated`, `last_event_date` | date-time | timestamps | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `location` | object | address, coordinates, timezone | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `properties` | object | custom key/value | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `subscriptions.email.marketing.consent` | enum (SUBSCRIBED, UNSUBSCRIBED, NEVER_SUBSCRIBED) | email opt-in state, returned when `additional-fields[profile]=subscriptions` is requested | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `subscriptions.email.marketing.consent_timestamp` | date-time | when consent state was set | Profile | https://developers.klaviyo.com/en/docs/collect_email_and_sms_consent_via_api |
| `subscriptions.email.marketing.can_receive_email_marketing` | boolean | implicit-consent eligibility | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `subscriptions.email.marketing.method`, `.method_detail`, `.custom_method_detail` | string | how consent was captured (e.g. TEXT / JOIN) | Profile | https://developers.klaviyo.com/en/docs/collect_email_and_sms_consent_via_api |
| `subscriptions.email.marketing.double_optin` | boolean | true only if the recipient received and confirmed a double opt-in message | Profile | https://developers.klaviyo.com/en/docs/collect_email_and_sms_consent_via_api |
| `subscriptions.email.marketing.suppression` / `.list_suppressions` | array | global and per-list suppression reason + timestamp | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `subscriptions.email.open_tracking.consent`, `.click_tracking.consent` | string | tracking-specific consent | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `subscriptions.sms.marketing.consent`, `.consent_timestamp`, `.can_receive_sms_marketing` | enum/date-time/bool | SMS marketing consent | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `subscriptions.sms.transactional.consent`, `.can_receive_sms_transactional` | enum/bool | SMS transactional consent | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `subscriptions.mobile_push.marketing.can_receive_push_marketing` | boolean | push consent | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `subscriptions.whatsapp.{marketing,transactional,conversational}.consent` | string | WhatsApp consent per use type | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `predictive_analytics.historic_clv`, `.predicted_clv`, `.total_clv` | number | lifetime value fields, require `additional-fields[profile]=predictive_analytics` (lower rate limit) | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `predictive_analytics.historic_number_of_orders`, `.predicted_number_of_orders` | number | order counts | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `predictive_analytics.average_days_between_orders` | number, null if 1 order | purchase cadence | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `predictive_analytics.average_order_value`, `.churn_probability`, `.expected_date_of_next_order`, `.ranked_channel_affinity` | number/date-time/array | predictive fields | Profile | https://developers.klaviyo.com/en/reference/get_profiles |
| `id`, `name`, `created`, `updated` | string/date-time | list identity | List | https://developers.klaviyo.com/en/reference/get_lists |
| `opt_in_process` | enum (double_opt_in, single_opt_in) | governs whether new subscribers to that list must double-confirm | List | https://developers.klaviyo.com/en/reference/get_lists |
| `id`, `name`, `created`, `updated`, `is_active`, `is_processing`, `is_starred` | mixed | segment identity and state | Segment | https://developers.klaviyo.com/en/reference/get_segments |
| `definition.condition_groups` | array | boolean-logic (AND/OR) condition groups: Profile Property, Profile Metric (count/sum of behavior), Marketing Consent, Predictive Analytics, Custom Object, Postal Code Distance, Group Membership conditions. Nested per-condition-type field schema was summarized, not quoted verbatim from the OpenAPI model — pull the raw schema from the reference page's Model tab if exact sub-fields are needed | Segment | https://developers.klaviyo.com/en/reference/get_segments |
| `id`, `name`, `status`, `archived`, `created`, `updated` | mixed | flow identity | Flow | https://developers.klaviyo.com/en/reference/get_flows |
| `trigger_type` | enum (Metric, Added to List, Unconfigured, Date Based, Price Drop, Low Inventory) | what starts the flow | Flow | https://developers.klaviyo.com/en/reference/get_flows |
| `definition.data.name`, `.status`, `.trigger_type`, `.main_action`, `.profile_filter`, `.trigger_filter`, `.branches` | mixed | one flow step's config, including conditional branch paths | Flow Action | https://developers.klaviyo.com/en/reference/get_flow_actions |
| `channel`, `definition.name`, `.subject_line`, `.body`, `.from_email`, `.from_label`, `.reply_to_email`, `.preview_text`, `.template_id`, `.image_id`, `.title`, `.url`, `.action_buttons` | mixed | one message variant's content, fields vary by channel (email/sms/push) | Flow Message | https://developers.klaviyo.com/en/reference/get_flow_action_messages |
| `id`, `name`, `status`, `archived` | mixed | campaign identity; status enum includes Draft, Scheduled, Sending, Sent, Cancelled and cancellation-reason variants | Campaign | https://developers.klaviyo.com/en/reference/get_campaigns |
| `audiences.included`, `.excluded` | array | targeted lists/segments | Campaign | https://developers.klaviyo.com/en/reference/get_campaigns |
| `send_options.use_smart_sending` | boolean | Klaviyo's smart-sending suppression | Campaign | https://developers.klaviyo.com/en/reference/get_campaigns |
| `send_strategy.type` | enum (Static, Smart Send Time, Throttled, Immediate, AB Test, Unsupported) | how the send is scheduled | Campaign | https://developers.klaviyo.com/en/reference/get_campaigns |
| `tracking_options` | object | click/open tracking flags, custom UTM params | Campaign | https://developers.klaviyo.com/en/reference/get_campaigns |
| `created_at`, `updated_at`, `scheduled_at`, `send_time` | date-time | campaign timestamps, `send_time` null if unscheduled | Campaign | https://developers.klaviyo.com/en/reference/get_campaigns |
| `definition` | object | channel-specific content: email has subject/from_email/preview_text; SMS has body/media_url; push (standard) has title/body/action_buttons/kv_pairs/options; push (silent) has kv_pairs only | Campaign Message | https://developers.klaviyo.com/en/reference/get_campaign_messages |
| `send_times` | array | Send Time sub-objects | Campaign Message | https://developers.klaviyo.com/en/reference/get_campaign_messages |
| `id`, `name`, `created`, `updated`, `integration` | mixed | event-type definition and its source integration | Metric | https://developers.klaviyo.com/en/reference/get_metrics |
| `id`, `timestamp` (unix seconds), `datetime` (ISO 8601), `event_properties`, `uuid` | mixed | one event occurrence; `uuid` also usable as a pagination cursor; max 400 properties per event, string property values capped at 100KB, numeric `0`/`null`/`""` treated as unset and excluded from segmentation, timestamp must be 1990 to now+1 year | Event | https://developers.klaviyo.com/en/reference/get_events and https://developers.klaviyo.com/en/reference/events_api_overview |
| `backfill` | boolean, default false | on event create: stores the event for API/metrics/segmentation but does not trigger flows, for historical replay without re-firing automations | Event | https://developers.klaviyo.com/en/reference/events_api_overview |
| `metric_id`, `measurements`, `by`, `filter`, `interval`, `page_size`, `timezone`, `sort`, `page_cursor`, `return_fields` | request body fields | see Attribution and windows below for the query mechanics | Metric Aggregate (query) | https://developers.klaviyo.com/en/reference/query_metric_aggregates |
| `data.dates`, `data.data[].dimensions`, `data.data[].measurements.{count,sum_value,unique}` | response fields | one array of time buckets, and one row per dimension-combination whose measurement arrays are parallel to `dates` | Metric Aggregate (response) | https://developers.klaviyo.com/en/docs/using_the_query_metric_aggregates_endpoint |

## Breakdowns and dimensions
| Breakdown | Allowed with | Not allowed with | Doc |
|---|---|---|---|
| `$attributed_flow` | `by` on a Metric Aggregate query, e.g. paired with `sum_value` for attributed revenue per flow | which metrics support which `by` dimensions is not documented — Klaviyo's own developer community calls this ambiguous; do not assume a dimension is valid for every metric without testing | https://developers.klaviyo.com/en/reference/query_metric_aggregates ; ambiguity flagged at https://community.klaviyo.com/developer-group-64/query-metric-aggregates-endpoint-and-supported-attributes-are-ambiguous-12856 |
| `$attributed_message` | groups by the specific flow message or campaign message credited | same caveat as above | https://developers.klaviyo.com/en/reference/query_metric_aggregates |
| `$attributed_channel` | groups by attributed channel (email/sms/push) | same caveat | https://developers.klaviyo.com/en/reference/query_metric_aggregates |
| `$attributed_variation` | groups by the A/B variation credited | same caveat | https://developers.klaviyo.com/en/reference/query_metric_aggregates |
| `$flow`, `$flow_channel`, `$message`, `$message_send_cohort`, `$campaign_channel`, `$variation`, `$variation_send_cohort`, `$usage_amount`, `$value_currency` | other built-in `by` dimensions | same caveat | https://developers.klaviyo.com/en/reference/query_metric_aggregates |
| custom (non-`$`) dimensions: Bot Click, Bounce Type, Campaign Name, Client Canonical, Client Name, Client Type, Email Domain, Failure Source, Failure Type, From Number, From Phone Region, Inbox Provider, List, Message Format, Message Name, Message Type, Method, Segment Count, Subject, To Number, To Phone Region, URL, form_id | available on some metrics only | same undocumented-mapping caveat | https://developers.klaviyo.com/en/reference/query_metric_aggregates |
| the `filter` array | must include a datetime range; only 1 additional filter allowed beyond the date range; max 1 year date range per query | more than 1 extra filter, or a range over 1 year | https://developers.klaviyo.com/en/docs/using_the_query_metric_aggregates_endpoint |
| `interval` | `hour`, `day`, `week`, `month`, default `day` | — | https://developers.klaviyo.com/en/reference/query_metric_aggregates |

## Attribution and windows
Klaviyo does not expose an attribution-window field in the developer API. `POST /api/metric-aggregates/` returns revenue already attributed by Klaviyo's server-side model, groupable by `$attributed_flow` / `$attributed_message` / `$attributed_channel` / `$attributed_variation`, per https://developers.klaviyo.com/en/reference/query_metric_aggregates and the worked example at https://developers.klaviyo.com/en/docs/using_the_query_metric_aggregates_endpoint. The `$`-prefixed dimensions are also named on https://developers.klaviyo.com/en/docs/supported_metrics_and_attributes, which does not state a numeric window.

The actual window and model are documented only on Klaviyo's help center, not developers.klaviyo.com: default is a "cooperative last-touch" model, 5-day window for email clicks and a 24-hour window for SMS, adjustable per account, credit going to whichever message (flow or campaign) got the last qualifying click. https://help.klaviyo.com/hc/en-us/articles/1260804504250. An account on Marketing Analytics/Advanced KDP can switch to a linear multi-touch model instead. https://help.klaviyo.com/hc/en-us/articles/11118357030555. Treat the window as an account-level setting outside API scope: the connector reads whatever `sum_value` the account's configured model already produced, and does not need or have a way to set the window itself.

To query attributed revenue for a flow or a specific message: `POST /api/metric-aggregates/` with `measurements: ["sum_value"]`, `by: ["$attributed_flow"]` (or `$attributed_message` for message-level), a `metric_id` for the relevant metric (e.g. Placed Order), a `filter` with a datetime range plus optionally `not(equals($attributed_flow,""))` to drop unattributed rows, and `interval` set to the reporting grain. See the sample request/response below.

## Limits and gotchas
- Metric Aggregate queries: 1-year max date range, only 1 additional filter beyond the date range, `by`-dimension support is undocumented per metric (verify empirically). https://developers.klaviyo.com/en/docs/using_the_query_metric_aggregates_endpoint, ambiguity noted at https://community.klaviyo.com/developer-group-64/query-metric-aggregates-endpoint-and-supported-attributes-are-ambiguous-12856
- Pagination is cursor-based via `page[cursor]`; list responses carry `links.self`/`next`/`prev`, pass the returned cursor through rather than building an offset. https://developers.klaviyo.com/en/reference/api_overview. Events also expose `uuid` as a cursor. https://developers.klaviyo.com/en/reference/get_events. A forum post (not an official doc, flag as unverified) suggests cursors expire after roughly 3 days: https://community.klaviyo.com/developer-group-64/how-long-is-a-page-cursor-available-for-usage-when-requesting-filtered-events-from-the-klaviyo-api-6355
- Predictive analytics fields on Profiles need `additional-fields[profile]=predictive_analytics` and carry a lower rate limit; subscription fields need `additional-fields[profile]=subscriptions`. https://developers.klaviyo.com/en/reference/get_profiles
- List's stated max page size (10, per the fetched page) does not match the profiles endpoint's default/max of 20/100 — re-verify the exact number live before hardcoding, since this was extracted via an HTML-to-text tool that can mis-render a table cell. https://developers.klaviyo.com/en/reference/get_lists vs https://developers.klaviyo.com/en/reference/get_profiles
- No dedicated Conversations/SMS-channel-object reference page was found in this pass, though the 2026-07-15 changelog says the Conversations API went multi-channel (SMS/WhatsApp). Needs a follow-up fetch if SMS conversation objects (as opposed to profile-level SMS consent) matter for this connector. https://developers.klaviyo.com/en/docs/changelog_
- No stated overall retention ceiling for events/metric history was found on developers.klaviyo.com — do not assert unlimited retention in the product; label as unconfirmed.
- Revisions are stable ~1 year then deprecated ~1 year then retired (can 410); Klaviyo recommends re-checking/upgrading every 12-18 months. https://developers.klaviyo.com/en/docs/api_versioning_and_deprecation_policy

## Sample row
Request — `POST /api/metric-aggregates/`, revenue by flow, monthly (verbatim from the docs' own example):
```json
{
  "data": {
    "type": "metric-aggregate",
    "attributes": {
      "measurements": ["sum_value"],
      "by": ["$attributed_flow"],
      "filter": [
        "greater-or-equal(datetime,2022-01-01T00:00:00)",
        "less-than(datetime,2023-01-01T00:00:00)",
        "not(equals($attributed_flow,\"\"))"
      ],
      "metric_id": "PhqdJM",
      "interval": "month",
      "timezone": "US/Eastern"
    }
  }
}
```
Response (verbatim): `dimensions: ["R9VbBr"]` is the flow id (since `by` is `$attributed_flow`), and `measurements.sum_value` is attributed revenue per month for that flow, parallel to `dates`.
```json
{
  "data": {
    "type": "metric-aggregate",
    "id": "<ephemeral id>",
    "attributes": {
      "dates": [
        "2021-12-01T05:00:00+00:00",
        "2022-01-01T05:00:00+00:00"
      ],
      "data": [
        {
          "dimensions": ["R9VbBr"],
          "measurements": {
            "sum_value": [0.0, 17829.0]
          }
        }
      ]
    },
    "links": {"self": "<uri>"}
  }
}
```
Source: https://developers.klaviyo.com/en/docs/using_the_query_metric_aggregates_endpoint

## Maps to ecomOS tables
| Table in contracts/data-sources.md | Fields used |
|---|---|
| `flows` | Flow `id`/`name`/`status`/`trigger_type`, Flow Message `channel`/content fields, Metric Aggregate `sum_value` grouped by `$attributed_flow` and `$attributed_message` for attributed revenue per flow/message, `count`/`unique` for sends and unique recipients per the relevant metric (e.g. Received Email, Placed Order) |
| `campaign_sends` | Campaign `id`/`name`/`status`/`send_time`, Campaign Message `definition` (subject/body per channel), Metric Aggregate `sum_value`/`count` grouped by `$attributed_channel` and `$attributed_message` for a campaign's opens, clicks, unsubscribes and attributed revenue; Event-level `unsubscribed`/`bounced` metrics for unsubscribe/bounce counts; `order ids matched` comes from Event `event_properties` on the Placed Order metric filtered by `$attributed_message`/`$attributed_flow` |
