---
name: creator-seeding-and-discovery
owner: ORG
version: 1
invoke_when: monthly for the seeding batch, continuously for discovery scanning
inputs: gifting inventory, claims tiers, past creator performance, founder seeding budget/scope
outputs: scored discovery candidates with personalized outreach drafts, seeding briefs, delivery tracking
---
# Creator discovery, seeding and UGC briefs

## Purpose
Keep the organic (unpaid or product-only) creator pipeline running: find creators already talking about the category who have not mentioned the brand, and manage gifting through to delivered content, distinct from any paid influencer deal.

## Steps
1. Scan public Instagram, YouTube and Pinterest posts for creators discussing the category or named competitors without mentioning this brand.
2. Score each on category fit, audience size, engagement rate and visual-world match.
3. Draft a personalized outreach note referencing their actual content; batch every candidate for founder approval, never send without it.
4. For approved creators, build the seeding brief: SKU, quantity, what to show, deadline, usage-rights ask, disclosure requirement.
5. Track shipment and delivered content per creator; flag anyone who received product and missed the deadline.
6. Hand delivered content to org/ugc-repurposing with its rights status attached.

## Checks
- No template outreach; every note references real content.
- Usage rights asked for before shipment, every time.
- Non-delivery is tracked and flagged, not dropped silently.

## Output
{discovery_candidates[], seeding_briefs[], delivery_status[]}

## Example
Creator @city_parent_diaries posted about strollers generally without naming any brand; outreach references their specific pothole-test post and offers stroller-v2 for an honest review, disclosure required.
