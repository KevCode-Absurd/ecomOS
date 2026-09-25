# Organic and content: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- did we post what we planned and is the next holiday slot covered  (ORG-C02)
- how much of what worked needed the founder's face, and are we over that budget  (ORG-C03)
- what do we say, to whom, and in which language variant  (ORG-C04)
- which post should become a format the team can run without the founder  (ORG-C05)
- what do we need to film this batch and when do we raise production stakes  (ORG-C06)
- what should we post about next, and what are named competitors doing  (ORG-C07)
- is this draft ready for a human rewrite, and does it clear the claims and safety gate  (CREA-C21, LOOP-C12)
- which messages need a human right now, and does this post's funnel actually capture a lead  (ORG-C09, ORG-C10)
- what UGC is sitting unused, and what is about to retire without being reused anywhere  (ORG-C11, ORG-C13)
- does every live post's link work, match, and carry the right product tag  (ORG-C12)
- who should get product for content, and did we get usage rights back  (ORG-C14)
- which content made money, and which viral post reached strangers who never bought  (ORG-C16)
- are our videos titled, thumbnailed and chaptered to be found in YouTube search  (ORG-C38)
- is the community active, and do active members actually buy  (LIFE-C53)

### Metrics specified

- `posting_floor_adherence`: Share of this week's planned posts that actually went out. posts_published_this_week / posts_planned_at_floor_this_week
- `holiday_slot_coverage`: Share of US holidays and retail moments in the next 30 days that already have a script assigned. holiday_slots_with_script / holiday_slots_in_next_30_days
- `festival_slot_coverage`: Share of India festivals in the next 30 days that already have a script assigned. festival_slots_with_script / festival_slots_in_next_30_days
- `founder_camera_share`: Share of published posts that feature the founder on camera. founder_posts / total_posts, trailing 30 days
- `revenue_from_tagged_content`: Orders that came from a specific post, tracked by its own link tag or promo code. sum(order_value) where session utm_content or promo code matches a post id, within its view-through window
- `content_pillar_revenue_share`: Share of tagged content revenue coming from each pillar. revenue_from_tagged_content grouped by pillar / total tagged revenue
- `link_destination_pass_rate`: Share of live posts whose link opens a working page that matches the post. posts_with_verified_live_matching_link / posts_checked
- `shoppable_tag_coverage`: Share of eligible posts with correct product tags attached. posts_with_correct_product_tag / posts_eligible_for_tagging
- `comment_response_time_median`: Typical time to the first reply on a comment or DM that needs one. median(first_reply_time - message_time) for messages flagged as needing a reply
- `dm_to_owned_contact_rate`: Share of DM conversations that end with an email, SMS opt-in or phone number captured (or a WhatsApp opt-in, market option for India, EU or LATAM). dm_threads_with_captured_contact / dm_threads_total
- `ugc_pipeline_depth`: Verified reviews and UGC assets ready to post, by SKU. count(verified_ugc_assets) where posted = false, grouped by sku
- `asset_reuse_rate`: Share of assets past their reuse checkpoint that got reused on at least one other surface. assets_reused_before_shelf_life_end / assets_past_reuse_checkpoint
- `creator_seeding_active_count`: Creators currently seeded with product this month, and total product cost sent. count(distinct creator) and sum(product_cost) where seeding_status = active
- `creator_content_yield`: Content pieces delivered per 10 creators seeded. 10 * count(content_delivered) / count(distinct creator seeded)
- `claims_gate_hold_count`: Posts the safety gate held before publish this month, and the most common rule triggered. count(posts) where gate_result = held, grouped by rule
- `stranger_blind_share`: Share of the top 10 posts by reach that name no product and give no next step. count(top_10_reach_posts where no_named_sku and no_cta) / 10
- `broad_low_value_hit_share`: Share of top-quartile-reach posts whose matched orders fall below the brand's set floor. count(top_quartile_reach posts where matched_orders < floor) / count(top_quartile_reach posts)
- `youtube_search_traffic_share`: Share of channel views coming from YouTube search rather than suggested or browse. search_views / total_views
- `community_active_member_rate`: Share of community members who sent at least one message in the last 30 days. active_members_30d / total_members
- `community_to_order_rate`: Share of community members who also placed an order in the same window, matched by phone or email. members_with_matching_order / total_members

### Insights specified (rules in code)

- posting floor missed: posts_published this week < posts_planned at floor → "{n} of {planned} planned posts did not go out this week" (action ORG-C02)
- holiday gap: a US holiday or retail moment is within 14 days and has zero assigned script → "{holiday} is in {d} days and has no script yet" (action ORG-C02)
- festival gap: an India festival is within 14 days and has zero assigned script → "{festival} is in {d} days and has no script yet" (action ORG-C02)
- stranger-blind viral post: a post is in the top 3 by reach in the last 30 days and carries no named SKU or CTA tag → "{title} got {reach} views but named no product and gave no next step" (action ORG-C16)
- broad low-value hit: a post is in the top reach quartile and its matched orders fall below the set floor → "{title} reached {n} people but sold {k} pieces, below the {floor} floor" (action ORG-C16)
- unused UGC: a verified review or photo asset has sat unposted for more than 21 days → "{n} verified reviews are unused for over {d} days" (action ORG-C11)
- asset expiring unused: an asset's shelf-life end date is within 7 days and its reuse count is 0 → "{n} assets retire this week without being reused anywhere" (action ORG-C13)
- claims gate catching a real pattern: the same claims rule triggers 3 or more times in a month → "{n} posts were held this month for {top_rule}, more than any other rule" (action LOOP-C12)
- creator seeding, no yield: a creator was seeded more than 21 days ago and has delivered zero content → "{n} of {seeded} creators sent product but delivered nothing in 3 weeks" (action ORG-C14)
- DM funnel leak: the share of DM threads ending with no captured contact exceeds 70% → "{pct}% of DM conversations end without an email, SMS opt-in or phone number (or a WhatsApp opt-in, market option for India, EU or LATAM)" (action ORG-C10)
- dead or mismatched link: a live post's link fails the check or does not match the intended page → "{n} live posts point to a page that is down or does not match" (action ORG-C12)
- comment response lag: a comment or DM needing a reply has waited more than 24 hours → "{n} messages have waited over {h} hours for a reply" (action ORG-C09)
- community going quiet: active member rate falls 10 percentage points or more month over month → "community activity fell {pct} points this month" (action LIFE-C53)
- YouTube search share falling: search-traffic share this period is lower than the prior period → "{pct}% of views now come from search, down from {prev}%" (action ORG-C38)
- founder over budget: founder_camera_share exceeds the target set when the on-camera plan was made → "{pct}% of posts need the founder on camera, above the {target}% plan" (action ORG-C03)

### Visuals specified

- calendar heatmap (calendar grid): planned vs published posts per day, with holiday flags (festival flags for an India calendar)
- SKU by hook revenue grid (heatmap table): matched revenue for each SKU by hook type
- comment to order funnel (stepped funnel chart): comments to DMs to owned contacts to orders
- creator seeding scorecard (table with bars): creators seeded, cost sent, content delivered, yield
- asset lifecycle timeline (gantt-style bar per asset): shelf-life window and reuse events across PDP, email, DM and post-purchase
- community health line (line chart with overlay): weekly active member rate with matched-order rate overlaid

### Not in the usual tools

- ties each post to the order it produced, by SKU and hook, using the post's own link tag or promo code
- runs a fixed claims and safety gate against the brand's own claim tiers before a post can publish
- tracks creator seeding cost, fulfillment and content yield against the same tagged asset library the calendar draws from
- flags a stranger-blind viral post and a broad-reach, low-order hit by a fixed rule tied to the store's own orders
- tracks an asset's shelf life and reuse across PDP, email, DM and post-purchase flow before retiring it
- reads the owned Discord, SMS or WhatsApp community's active-member rate against matched store orders

### Data this screen needs

- `content_calendar`: brand, date, platform, pillar, status, holiday_tag, language_variant (calendar tool export or ORG-C02 output)
- `post_performance`: post_id, platform, date, reach, views, engagement, follower_share_of_views, sku_tag, hook_tag, cta_tag (platform insights API (Instagram, TikTok, YouTube))
- `utm_promo_orders`: order_id, order_value, utm_content, promo_code, session_time, order_time (store analytics joined to orders)
- `ugc_assets`: asset_id, sku, source, verified, posted, intake_date (review platform export + manual intake)
- `asset_library`: asset_id, surfaces_used, shelf_life_end, reuse_count, retired (asset tagging tool)
- `creator_seeding`: creator_id, platform, product_cost, seeded_date, content_delivered, rights_confirmed, fraud_flag (seeding tracker (spreadsheet or CRM))
- `inbox_log`: message_id, platform, type, received_at, first_reply_at, needs_reply, auto_sent (unified inbox tool export)
- `dm_funnel`: thread_id, entry_post_id, captured_contact, contact_type, lead_magnet (DM automation tool + CRM)
- `claims_gate_log`: post_id, rule_triggered, result, checked_at (ORG-C15 gate script)
- `link_check_log`: post_id, url, status_code, matches_intent, checked_at (automated crawler)
- `youtube_studio_export`: video_id, title, views, search_views, suggested_views, avg_view_duration, date (YouTube Studio API)
- `community_roster`: member_id, platform, phone_or_email, joined_at, last_active_at, message_count (Discord export or SMS platform export (WhatsApp Business API export, market option for India, EU or LATAM))

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
