# Calibration (brain fields the generator reads)

The sample brand is Bombas, built from public information only, with simulated performance data that every page labels as simulated. The generator shapes the simulated tables to the brand's public profile so screens look right at the right scale. This file lists the brain fields the generator reads, what each one drives, and the rule when a field is missing.

Input: `app/brain/bombas/assumptions.json`, written by session S1.3m. It does not exist yet. The generator reads fields by the ids below; if S1.3m names them differently, update this file, not the generator.

## Rules for every field

- The generator reads only `assumptions.json`. It never reads `app/brain/bombas/raw/` or any extract directly. A number the brain has not settled is not a number the generator can use.
- Every field carries a value, a unit, a confidence (`stated`, `derived`, `estimated`), the source ids behind it and an `as_of` date. The generator copies these into the generation manifest.
- The generator is deterministic from a seed plus the assumptions file. Same inputs, same tables.
- The generation manifest (`app/data/bombas/manifest.json`) records, per field: the value used, whether it came from the brain or from a fallback, and the fallback rule applied. Screens read it and show "calibrated to N of 6 brain fields" on the sample brand banner.
- A fallback is a stated placeholder for a shape or a scale, never a fact about Bombas. Nothing in a fallback may be shown as a brand fact.
- Brand facts, results and founder decisions live in the brain and the experiment registry, never in generated tables.

## Fields

| Field | Unit | What the generator uses it for |
|---|---|---|
| revenue_band | usd per year, low and high | the scale anchor: total net revenue for the 13 simulated months, and from it order count once AOV is known |
| aov | usd | average order value; sets the line-item mix and unit count per order in `orders` |
| repeat_rate | percent, 90 day | share of first-time customers who order again within 90 days; shapes `customers` and the cohort curves |
| channel_mix | percent by channel | share of orders by acquisition channel; drives `sessions`, `ad_rows`, `google_rows`, `flows` volumes and `orders.utm` |
| seasonality | index by month, 12 values | the month curve applied to orders, sessions and spend; Q4 peak and gifting weeks |
| giving_units | units per year, and the rule (one bought, one given) | the giving tiles and the giving column in `orders`; also the unit count reported on the brand page |

## Rule when a field is missing

| Field | Rule |
|---|---|
| revenue_band | Required. The generator stops and writes nothing. Everything scales off it and a made-up scale would look like a fact. The manifest records `revenue_band: missing` and the screens show the empty state. |
| aov | Fallback from the catalog: the median variant price in `products`, times 1.4 units per order. Manifest marks `aov: fallback (catalog)`. |
| repeat_rate | Fallback 25 percent at 90 days, a generic basics-apparel shape. Manifest marks `repeat_rate: fallback (generic)`. |
| channel_mix | Fallback split: paid social 35, paid search 20, organic search 15, direct 15, email and SMS 10, other 5. Manifest marks `channel_mix: fallback (generic)`. |
| seasonality | Fallback US retail curve: index 1.0 in Feb to Sep, 0.9 in Jan, 1.2 in Oct, 1.6 in Nov, 1.8 in Dec. Manifest marks `seasonality: fallback (us_retail)`. |
| giving_units | No fallback. Giving tiles and the giving column read unavailable. A giving number is a brand fact and is never invented. |

A partial field (a band with one end, a channel mix that does not sum to 100) is treated as missing and the manifest says why.

## Derived numbers the generator computes

These are not brain fields. They are computed from the fields above and the catalog, and the manifest records the arithmetic.

| Number | From |
|---|---|
| orders per month | revenue band midpoint over AOV, spread by the seasonality curve, with weekly texture (weekend lift) from a fixed pattern |
| first-time and returning split | repeat rate, applied to cohorts by month of first order |
| sessions per day | orders per day over a fixed conversion rate per channel; the rates are placeholders and the manifest says so |
| ad spend per day | paid channel orders times a placeholder CPA per channel; the manifest says so |
| flow and campaign volumes | email and SMS share of the channel mix and the customer count with consent |
| finance inputs | a simulated `finance_inputs` set at the revenue band, per `finance-inputs.md`, all rows `confidence: simulated` |

Placeholder rates (conversion by channel, CPA by channel, return rate, chargeback rate) are fixed constants in the generator, listed in its docstring and copied into the manifest. They are shapes, not Bombas facts. S2.3c applied the S2.5 review fixes (`data/brands/bombas/REVIEW.md`): return 6 percent, chargeback 0.15 percent, tickets 5 percent of orders (8 in December), mobile 70 percent. Numbers the founder asked us to assume where the brain has none (for now `site_sessions_monthly`, 15,000,000) sit in the generator's `ASSUMED` block and read `origin: assumed` in the manifest; the brain's open question stays open.

The brain's `channel_mix` now carries a marketplace share, and `paid_media_split` gives the paid spend split. Orders are the DTC site plus owned stores; wholesale and marketplaces are monthly fixtures at their shares; Meta and Google spend come from their rows and the other paid platforms from a daily fixture.

## What the brain must not be asked for

- Performance numbers (ROAS, CPA, conversion rate). Bombas does not publish them. The generator uses placeholders and says so.
- Costs, fees, cash. These are `finance_inputs`, simulated for the sample brand, never inferred from public sources.
- Anything from a competitor's public ads beyond layout and mood.

## When a real brand connects

Calibration stops. The tables fill from connectors per `data-sources.md`, the manifest is not written, and the simulated label comes off. The brain fields above stay useful as the brand's own claims for the audit, but nothing in a table is generated from them.
