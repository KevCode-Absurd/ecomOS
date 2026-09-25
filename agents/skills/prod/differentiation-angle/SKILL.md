---
name: prod/differentiation-angle
owner: PROD
version: 1
invoke_when: a hero product needs its next SKUs planned, or any candidate needs its one owned difference named
inputs: hero SKU performance, competitor scouting sheet, sales history, avatar draft
outputs: differentiation angle, line-extension options, demand-pattern tags, subscription-fit verdict
---
# Differentiation angle

## Purpose
Every candidate and every hero product needs one owned point of difference, not a vague "better quality" claim. This
skill turns a scouted competitor gap into a concrete angle and a small set of SKU options that build on it.

## Steps
1. Read the hero product's real performance (sales, margin, reviews) and note the category's default feature set: 
   what every competitor already does.
2. Name the single thing that differs from that default. It must trace to a specific, cited gap found during
   competitor scouting, never an invented or assumed advantage.
3. Draft 2 to 3 line-extension SKU options that build on the angle rather than duplicating the hero product.
4. Tag each option's demand pattern: evergreen, trending, or seasonal: using sales history or category norms as
   evidence, not a guess.
5. Check whether a subscription model is genuinely earned: look for real repeat_rate_90d/365d data. Absent that
   evidence, tag the SKU a one-time purchase, never assume recurring revenue.

## Checks
- The angle names a specific competitor gap it closes, with a citation.
- Every line-extension option states exactly what it adds over the hero SKU.
- The subscription verdict rests on repeat-purchase data, never founder preference.

## Output
{angle, line_extension_options[{name, adds, demand_tag, evidence}], subscription_fit}

## Example
Angle: "every competitor ships a fixed-size travel kit; ours is the only one with 3 refill sizes." Options: refill
2-pack (evergreen), festive gift box (seasonal, Diwali spike from 2 prior years' data), travel mini (trending, but
subscription not earned: repeat_rate_90d is 4%, below the 15% floor).
