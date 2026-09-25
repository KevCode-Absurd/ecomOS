---
name: prod/amazon-launch-sequence
owner: PROD
version: 1
invoke_when: a brand is considering an Amazon launch, or a listing is going live and needs Brand Registry and
  launch protection
inputs: business entity and GST details, bank/payout details, identity verification documents, trademark status,
  the stock and PPC plan for launch
outputs: a verified account, a sequenced Brand Registry checklist, and a protected launch plan
---
# Sequence an Amazon account, Brand Registry and launch

## Purpose
Account setup, trademark filing, Brand Registry enrolment and launch-week execution have a strict order: doing
them out of order (enrolling Brand Registry before the trademark is filed, for instance) causes rejections and
weeks of delay. This skill enforces the correct sequence.

## Steps
1. Get the Amazon seller account, business entity, payout details and identity verification right the first time
: a rejected or later-flagged account costs far more time than a careful first submission.
2. Sequence trademark filing before listing creation; Brand Registry cannot be enrolled without a filed trademark,
   so this step must complete first.
3. Once the trademark is filed and the listing (built via PROD-W22) is live, enrol Brand Registry.
4. Turn on the Storefront and Subscribe & Save benefits Brand Registry unlocks, confirming both are actually live,
   not just eligible.
5. Concentrate real demand into the first launch weeks by aligning stock arrival and PPC campaign start to the same
   date, and build a pre-launch audience where the platform's rules allow it.
6. Protect a novel product against copycats from day one: watermark product images, and file for design protection
   where the product is genuinely novel.

## Checks
- No step in the sequence is attempted before its prerequisite is confirmed complete.
- Stock and PPC go live on the same date, never staggered by more than a day.

## Output
{account_status, trademark_status, brand_registry_status, launch_plan, protection_checklist}

## Example
Account verified on first submission (2 weeks). Trademark filed before listing creation. Listing built and live.
Brand Registry enrolled once both prerequisites confirmed. Launch week: stock arrived and PPC campaign started the
same day; a pre-launch waitlist built the prior 2 weeks.
