# Creative: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- which ads should I copy the pattern of and which should I kill  (CREA-C16, CREA-C42)
- is this ad fatigued or just underfunded  (CREA-C15)
- what angle should the next batch of creative argue, and for whom  (BRAND-C14, BRAND-C11, CREA-C03)
- what exactly are we building, for whom, and why  (CREA-C06)
- which hook actually stops the scroll  (CREA-C04)
- how many usable statics came out of this brief, and does the product shown match what ships  (CREA-C07, CREA-C12)
- does this script hit hook, mechanism, proof, objection and CTA, and stay an argument, not a biography  (CREA-C08, CREA-C09)
- which creators are worth briefing again, and are we cleared to run their post as a paid ad  (CREA-C10, CREA-C38, CREA-C51)
- can we get a working cold-open video today instead of in two weeks  (CREA-C36)
- does this concept fit the platform and the market, or does it need a redo  (CREA-C11, CREA-C19, CREA-C22)
- how much manual resizing, subtitling and cutting can we skip  (CREA-C39, CREA-C40, CREA-C41)
- are we making enough of the right creative, on time, on budget, and tagged right  (MEDIA-C15, CREA-C18, CREA-C20, CREA-C21, CREA-C18, CREA-C54)
- will this feed or overlay break on some SKUs, or does an asset carry a license risk  (CREA-C52, CREA-C43, CREA-C49, CREA-C52)
- what are competitors testing that we are not, and can I get approved creative into Ads Manager as a draft without touching a live setting  (LOOP-C13, CREA-C46, CREA-C47, CREA-C48)

### Metrics specified

- `hook_rate`: how many people stop scrolling in the first 3 seconds of a video ad. 3-second video plays divided by impressions
- `hold_rate`: of the people who stopped, how many kept watching. ThruPlays divided by 3-second plays
- `audience_reach_growth`: whether the ad set still has new people to show the ad to. reach in the last 7 days divided by reach in the 7 days before it, minus 1
- `days_to_fatigue_by_format`: how many days a format usually lasts before it starts losing steam. median days from first spend to the day CTR first drops 25% and stays down, grouped by format
- `winner_breakdown_coverage`: share of this month's clear winners and losers that actually have a written reason on file. ads in the top or bottom spend quartile with a saved breakdown, divided by all ads in that quartile
- `brief_to_launch_days`: how long it takes from a written brief to the ad actually spending. median of (first spend date minus brief date) for ads matched to a brief_id
- `concepts_per_brief`: how many usable variants one brief produces in the studio. count of saved studio variants divided by count of briefs in the same period
- `new_ad_hit_rate`: share of newly launched ads that actually earn a Scale verdict. ads launched in the window that reach a Scale verdict within 14 days of first spend, divided by all ads launched in the window
- `cost_per_produced_asset`: what a finished asset actually costs, all in. sum of AI credits, freelancer or agency invoices and stock license fees for the month, divided by finished assets that reached a live ad that month
- `pipeline_volume_vs_plan`: are we on pace to make as much creative as the plan calls for. assets shipped to a live ad this month divided by the month's planned asset count
- `dpa_feed_health`: share of catalogue products whose price and badge overlay actually render correctly. SKUs with no flagged overlay issue divided by all active SKUs in the feed
- `rights_expiry_risk`: how many live ads are about to lose their license or authorization. count of live ads whose stock, music, font license or creator whitelisting record expires within 30 days
- `resize_and_caption_coverage`: share of approved masters that have every required size, caption and alt text ready. approved masters with all required placement specs generated, captioned and alt-texted, divided by all approved masters
- `predictive_score_agreement`: whether the pre-spend score actually predicted the real result. scored ads whose predicted bucket (strong, mixed, weak) matches their actual 14-day verdict bucket, divided by all scored ads with 14 days of spend
- `competitor_format_angle_gap_count`: how many formats or angles competitors run at volume that we have not tested recently. count of format-or-angle combinations run by 3 or more competitors on over 20% of their active ads, with zero matching live ads from this account in the trailing 90 days
- `approved_draft_backlog`: how many approved creatives are waiting to become a real draft ad. count of approved creatives with no matching Ads Manager draft ID after 3 business days
- `production_cost_share_of_media_spend`: how much of the ad budget is going into making the ads versus running them. monthly production cost divided by monthly media spend

### Insights specified (rules in code)

- worn_out_vs_undertested: an ad's CTR is down 25% or more and ROAS is down 30% or more over the last 7 days versus the prior 21, AND its ad set's reach in the last 7 days grew less than 10% versus the 7 days before: call it worn out. If reach still grew 10% or more while CTR or ROAS fell, call it a targeting or sequencing problem, not fatigue. → "{ad_name} looks worn out. CTR is down {ctr_pct}% and its audience has stopped growing." (action CREA-C15)
- hidden_gem_hook: an ad's hook_rate is in the top quartile of the account's trailing 90 days, but its verdict is Watch or Cut → "{ad_name}'s hook stops {hook_pct}% of viewers, above your best quarter of ads, but it is not converting. Try the same hook with a different offer." (action CREA-C04)
- loser_with_no_breakdown: an ad in the bottom spend quartile has spent at least one target CPA, its ROAS is under half the target, and it has been live 14 days or more with no saved breakdown → "{ad_name} spent {spend} at {roas}x with no breakdown on file. Write one before the next batch is commissioned." (action CREA-C16)
- brief_less_spend: an ad is currently spending and has no brief_id recorded in the brief log → "{n} live ads have no brief on file, including {ad_name}." (action CREA-C06)
- pipeline_behind_plan: assets shipped this month are under 70% of the planned count with 5 or fewer days left in the month → "{shipped} of {planned} planned assets have shipped with {days} days left this month." (action CREA-C18)
- cost_per_asset_drifting_up: this month's cost per produced asset is more than 1.3 times the trailing 3-month average → "Cost per finished asset is {cost}, {pct}% above your 3-month average." (action CREA-C54)
- rights_expiring_soon: a live ad's stock, music, font license or creator whitelisting record expires within 14 days → "{n} live ads use a license or authorization expiring within 14 days." (action CREA-C49)
- dpa_template_broken: overlay QA flags an issue on more than 2% of active catalogue SKUs → "{pct}% of SKUs in the feed show a broken price or badge overlay." (action CREA-C52)
- asset_qa_gap: an approved master creative is missing a required placement size, a burned-in caption, or alt text more than 3 days after approval → "{n} approved creatives are missing a size, caption or alt text more than 3 days after approval." (action CREA-C39)
- predictive_score_miscalibrated: the predictive score's bucket matched the actual 14-day verdict on fewer than half of the last 20 scored ads → "The pre-spend score matched the real result on only {pct}% of the last {n} ads. Treat it as a rough filter, not a green light." (action CREA-C42)
- competitor_volume_gap: 3 or more competitors run a format or angle on over 20% of their active ads, and this account has zero live ads in that format or angle in the trailing 90 days → "{n} competitors run {format_or_angle} on over a fifth of their active ads. You have none live in the last 90 days. This is a signal, not proof it will work here." (action LOOP-C13)
- draft_backlog_piling_up: an approved creative has waited more than 3 business days without a matching Ads Manager draft ID → "{n} approved creatives have waited over 3 days to become a draft ad." (action CREA-C48)
- hit_rate_falling: the new-ad hit rate for launches in the last 30 days is 20 percentage points or more below the trailing 90-day hit rate, with at least 5 launches in each window → "Only {pct}% of last month's new ads hit Scale, versus {pct2}% over the last quarter." (action MEDIA-C15)

### Visuals specified

- winners and losers grid (sortable card grid with thumbnails): every ad ranked by spend with verdict, ROAS, hook rate and a link to its breakdown
- fatigue diagnosis chart (line chart, 3 lines plus an annotation): daily spend, rolling 7-day ROAS and link CTR, with the reach-growth line and the worn-out-or-not verdict marked
- hook bank leaderboard (ranked list with thumbnails or waveform for audio hooks): every hook in the bank, its grade, and which ads it has been tested in
- production pipeline funnel (funnel chart): briefs written, concepts made, assets shipped, ads launched, ads that hit Scale, in one month
- cost per asset over time (line chart with a budget line): monthly cost per finished asset against the planned budget per asset
- rights and authorization calendar (timeline): every licensed asset, stock clip and whitelisting window with its expiry date against currently live ads
- competitor format and angle heatmap (matrix, own volume vs competitor volume): each format and angle combination, this account's live count against competitor count

### Not in the usual tools

- Root-causes fatigue as a worn-out audience versus an under-tested budget, by checking whether the ad set's own reach has actually stopped growing
- Ties a written why-it-worked or why-it-failed hypothesis to this account's own numbers and its brief, for every winner and loser
- Tracks real production cost per finished asset against the month's budget line and plan
- Flags stock, music, font and creator-whitelisting rights expiring on currently live ads before a takedown risk lands
- Closes the loop on the pre-spend predictive score by checking it against this account's own real 14-day verdict
- Flags a broken price or badge overlay at the SKU level on the rendered creative itself, before a DPA campaign goes live at scale

### Data this screen needs

- `meta_ad_and_video_daily`: brand, ad_id, date, spend, impressions, purchases, purchase_value, video_3s_plays, thruplays, reach (existing meta_gallery.refresh meta plus meta_gallery.snapshot)
- `ad_creative_breakdowns`: ad_id, verdict, summary, why, structure, keep, test_next, watch_out, brief_id, model (existing meta_gallery lab.js plus breakdowns.json)
- `briefs`: brief_id, date, persona, angle, offer, destination, awareness_stage, format, owner, status (new creative brief tool (CREA-C06))
- `hook_bank`: hook_id, format, text_or_script, audio_type, on_screen_copy, visual_type, grade, tested_ad_ids (new hook bank tool (CREA-C04))
- `studio_variants`: variant_id, source_ad_id, ref_role, prompt, image, created_at (existing meta_gallery creative studio, /api/variants)
- `production_cost_log`: date, asset_id, cost_type, amount_inr, month_budget_line (new manual or finance import (CREA-C54))
- `pipeline_plan`: month, planned_assets, planned_budget, hit_rate_target (new plan set from the account's own trailing hit rate (CREA-C18))
- `rights_and_authorizations`: asset_id, type, license_or_consent_ref, expires_at, ad_ids_using (new rights log (CREA-C49, CREA-C38))
- `dpa_overlay_qa`: sku, feed_id, overlay_ok, issue, checked_at (new catalogue overlay QA script (CREA-C52))
- `asset_placement_coverage`: master_creative_id, placement_spec, generated, captioned, alt_text (new export and QA log (CREA-C39, CREA-C40, CREA-C41))
- `predictive_scores`: ad_or_draft_id, score, flagged_elements, scored_at, later_verdict (new predictive scoring tool (CREA-C42) plus existing verdict engine)
- `competitor_snapshot`: brand, ad_id, format, angle_tags, days_live, versions (existing competitors.json and comp_media.json, Ad Library search)
- `draft_upload_log`: creative_id, approved_at, staged_at, ads_manager_draft_id (new browser-agent draft log (CREA-C48))

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
