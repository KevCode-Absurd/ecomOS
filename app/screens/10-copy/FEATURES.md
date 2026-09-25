# Copy: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- will this line get the ad rejected or make a promise we cannot keep  (LOOP-C12)
- does this ad still say the same thing as the page it lands on  (SITE-C39, SITE-C36)
- which text set is actually ready to test  (CREA-C05)
- is this draft too long, too fancy, or above the reading level we agreed on  (CREA-C26, CREA-C26)
- does this line describe an offer we can actually honor, and is the price framed the way we approved  (LIFE-C36, CREA-C31)
- are we answering the objection that is actually costing us sales, before the smaller ones  (CREA-C24)
- is this send inside the rules and does it match the account's cadence plan  (LIFE-C14, LIFE-C14)
- can I get a starting set of ad copy today without waiting on a full brief  (CREA-C37)
- what do we say to remove payment and delivery hesitation without sounding pushy, or, for a COD brand, to move an order toward prepaid  (CREA-C44)
- is this listing or A+ module making a claim our ads are not allowed to make  (PROD-C34, CREA-C45)
- is this ad's copy written for the page it will actually land on, and is the upload sheet ready to submit  (SITE-C35, CREA-C35, CREA-C20)
- does this name carry the benefit or story on its own  (CREA-C32)

### Metrics specified

- `claim_check_pass_rate`: share of copy sets that clear the claim check the first time. copy sets passed on first check divided by all copy sets checked
- `flagged_claims_open`: how many live ads or pages currently carry an unresolved flagged claim. count of live assets with a claim-check status of flag and no resolution
- `message_match_score`: how much of the ad's promise the landing page still says. matched items (same headline claim, same price or offer, same guarantee line, same top benefit) divided by total items checked, times 100
- `drift_alerts_count`: how many live ads no longer match the page they send to. count of live ads flagged for an image, price, offer or headline mismatch against the current page
- `reading_grade_level`: how hard the last month of shipped copy is to read. median Flesch-Kincaid grade level of copy shipped in the window
- `voice_compliance_rate`: share of drafts that pass the account's own writing rules with no fixes needed. drafts with zero em dashes, zero banned words and reading grade at or below 10, divided by all drafts QA'd
- `em_dash_and_banned_word_catches`: how many rule breaks the QA step is catching before ship. count of em dash or banned-word hits caught in QA before a draft shipped
- `objection_coverage`: share of the top real objections that actually have a live line answering them. top 10 objections by frequency with at least one live tagged ad or page line, divided by 10
- `offer_approval_lag`: how long an offer line waits for a founder decision. median days between an offer copy draft and a recorded founder decision
- `price_framing_consistency`: share of live prices using the framing rule the founder actually approved. live price mentions matching the approved framing rule, divided by all live price mentions
- `sms_email_rule_violations`: how many drafted sends broke a rule before they shipped. count of drafted SMS or email sends missing the opt-out line, over the length limit, or breaking the cadence rule, caught before send
- `product_url_draft_turnaround`: how fast a product page turns into a first-pass ad copy set. median minutes from product URL submitted to a delivered draft set
- `payment_delivery_touchpoint_coverage`: share of checkout and post-purchase moments that carry an approved payment or delivery reassurance line (BNPL, free returns, delivery date); for a COD brand (markets: IN), the same metric covers COD trust or prepaid-nudge line coverage instead. touchpoints on the account's fixed list with an approved line attached, divided by all touchpoints on that list
- `marketplace_claim_alignment`: share of marketplace listing and A+ claims that match the same claim tier used in ads. listing or module claims present in the approved claim tier set, divided by all claims found
- `bulk_upload_sheet_error_rate`: share of rows in the last upload batch that would fail on submission. rows failing a required field or character-limit check, divided by all rows in the batch
- `naming_taxonomy_compliance`: share of new copy assets tagged with the full fixed taxonomy at ship time. assets shipped with all 7 tags present (concept, persona, angle, offer, format, stage, source), divided by all assets shipped

### Insights specified (rules in code)

- claim_flagged_before_launch: a claim check on a copy set returns any line matching a banned or unverified claim pattern: an unproven superlative, a named competitor comparison, or a guarantee that does not match the brand's actual policy → "{n} lines in this set are flagged: {list}. None can ship until cleared." (action LOOP-C12)
- message_match_drift: a live ad's offer, price or headline term no longer appears in any of its landing destination's current copy blocks → "{ad_name} promises {term}, but the page it sends to no longer says it." (action SITE-C39)
- reading_level_creeping_up: the median reading grade level of shipped copy over the trailing 30 days is above grade 10 → "The last 30 days of copy reads at grade {grade}, above the grade-10 limit." (action CREA-C26)
- top_objection_has_no_line: an objection ranked in the top 5 by frequency in the trailing 90 days has zero live ad or page line tagged to it → "{objection} is the number {rank} reason buyers hesitate, and no live line answers it." (action CREA-C24)
- offer_approval_stalled: an offer copy draft has waited more than 5 business days without a recorded founder decision → "{offer_name} has waited {days} days for a yes or no." (action LIFE-C36)
- price_framing_inconsistent: more than 20% of live price mentions do not match the account's approved framing rule → "{pct}% of live prices are not framed the way you approved." (action CREA-C31)
- sms_email_violation_caught: a drafted SMS or email send is missing the opt-out line, exceeds the approved length, or breaks the account's cadence rule, caught before it ships → "{n} drafted sends this week broke a rule before they shipped: {list}." (action LIFE-C14)
- marketplace_claim_mismatch: a marketplace listing or A+ module claim is not present in the account's approved claim tier set used in ads → "{listing} claims {term}, which is not in your approved claim list." (action PROD-C34)
- bulk_upload_will_fail: a prepped upload sheet has a row missing a required field or over a platform character limit, caught before submission → "{n} rows in this batch will fail on upload: {reason}." (action CREA-C35)
- naming_taxonomy_gap: a shipped copy asset is missing one or more of the 7 fixed tags → "{n} assets shipped without full tagging this month." (action CREA-C20)
- payment_delivery_trust_message_missing: a checkout or post-purchase touchpoint on the account's fixed list has no approved payment or delivery reassurance line (BNPL, free returns, real delivery date) attached; for a COD brand (markets: IN), the same check looks for a prepaid-nudge or RTO-trust line instead → "{touchpoint} has no payment or delivery-trust line." (action CREA-C44)
- product_url_draft_slow: the last 5 product-URL-to-draft runs took more than twice the trailing 30-day median turnaround → "The last {n} product-page drafts took {minutes} minutes, {pct}% slower than usual." (action CREA-C37)
- destination_routing_conflict: two or more live ads target the same keyword or audience but route to different destinations selling the same product → "{n} live ads route the same audience to different pages for the same product." (action SITE-C35)
- voice_rule_catches_rising: more than 10% of drafts this week were caught with an em dash or a banned inflated word before shipping → "{pct}% of this week's drafts needed an em dash or banned-word fix before they shipped." (action CREA-C26)

### Visuals specified

- claim check ledger (table): every claim check run, its status, the reviewer and the resolution
- message match panel per live ad (side-by-side text panel with matched terms highlighted): the ad's headline, offer and price terms next to the landing page's current hero and offer block, with matches and gaps marked
- objection coverage matrix (matrix, objections by channel): the top objections ranked by frequency down the side, ad, page, email and SMS across the top, checked where a live line exists
- reading level trend line (line chart with a ceiling line): median reading grade level of shipped copy over time against the grade-10 limit
- offer approval funnel (funnel or stage chart): offer drafts moving from drafted to submitted to founder decision, with days spent in each stage
- price framing split (bar chart): share of live prices by framing type against the approved rule
- bulk upload QA checklist (pass or fail row list per batch): every row in the last upload batch with its validation result before submission

### Not in the usual tools

- Checks every claim against this brand's own claim tiers and current platform policy before it ships
- Scores message match by checking the ad's actual offer, price and headline terms against this brand's own current page copy blocks
- Ranks real customer objections from this account's own support tickets and reviews, then checks whether a live line actually answers each one
- Catches an SMS or email draft breaking the opt-out, length or the account's own cadence rule before it ships, not after
- Flags a marketplace listing claim that is not in the same approved claim tier used in this brand's ads
- Tracks reading grade level and rule catches over time as a trend against this account's own writing rules

### Data this screen needs

- `claim_tiers`: claim_id, tier, wording, proof_ref, approved_by, platform_notes (brand brain (not built yet))
- `claim_checks`: copy_set_id, claim_id, status, reviewer, checked_at (new claim check tool (CREA-C14))
- `page_copy_blocks`: page_url, block, text, last_scraped_at (new page-copy capture, scrape or CMS pull)
- `ad_copy_inventory`: ad_id, headline, primary_text, cta, offer_terms, price_terms, destination_url (existing Meta gallery ad creative data)
- `message_match_log`: ad_id, checked_at, matched_terms, unmatched_terms, score (new message match compute (CREA-C27, CREA-C53))
- `copy_qa_log`: draft_id, reading_grade, em_dash_count, banned_word_hits, passed_at (new QA scorer (CREA-C34))
- `objection_log`: objection, source, frequency_90d, rank (voice-of-customer pipeline (not yet built))
- `objection_coverage`: objection, channel, asset_id, live (copy inventory tagged by objection (CREA-C24))
- `offer_approval_log`: offer_id, drafted_at, submitted_at, decision, decided_at, decided_by (new offer-lever tool (CREA-C13))
- `price_framing_log`: asset_id, price_shown, framing_type, approved_rule (copy scan (CREA-C31))
- `lifecycle_send_qa`: send_id, channel, opt_out_present, length_ok, cadence_ok, checked_at (new lifecycle QA (CREA-C29, CREA-C30))
- `url_draft_log`: product_url, submitted_at, delivered_at, asset_ids (new URL-to-draft tool (CREA-C37))
- `payment_delivery_touchpoint_coverage`: touchpoint, has_line, line_id, cod_or_rto_line_id (markets: IN, null for a US brand) (new payment and delivery reassurance messaging log (CREA-C44))
- `marketplace_copy`: listing_id, marketplace, claims, matches_claim_tier (new marketplace copy log (CREA-C28, CREA-C45))
- `bulk_upload_batches`: batch_id, rows, errors, submitted_at (new upload sheet tool (CREA-C35))
- `naming_tags`: asset_id, concept, persona, angle, offer, format, stage, source (naming and tagging standard (CREA-C20))

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
