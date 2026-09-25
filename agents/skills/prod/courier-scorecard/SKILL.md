---
name: prod/courier-scorecard
owner: PROD
version: 1
invoke_when: the monthly courier scorecard is due, or shipping cost per order has drifted above benchmark or a
  contract renewal nears
inputs: the courier scorecard history, RTO/first-attempt-delivery/TAT data per courier per zone, public rate
  benchmarks for comparable India couriers
outputs: an updated scorecard, a volume reallocation recommendation, and a renegotiation draft where warranted
---
# Score couriers and draft a renegotiation

## Purpose
Courier volume should shift to whoever is actually performing better, on real and sustained evidence, not on one
bad week. And a renegotiation ask lands better with a real, cited benchmark behind it than with a bare complaint
about cost.

## Steps
1. Update the running scorecard per courier per zone: RTO rate, first-attempt delivery rate, delivery TAT, using
   the same measurement window for every courier being compared.
2. Compare zone performance across couriers and shift volume to the better performer only where the gap is real
   and sustained across more than one measurement period, not a single good or bad week.
3. Watch the brand's own shipping cost per order against public rate benchmarks for comparable India couriers, on
   a set cadence.
4. When cost drifts meaningfully above benchmark, or a contract renewal is approaching, draft a renegotiation ask
   with the specific, dated benchmark evidence attached.

## Checks
- A volume shift is only recommended on a sustained gap across more than one period.
- Every renegotiation ask cites a real, dated public rate card, not a vague sense that cost feels high.

## Output
{scorecard{}, volume_shift, benchmark_read, renegotiation_draft}

## Example
Courier A: 96% first-attempt in Zone North, sustained 3 months. Courier B: 89%, also sustained. Recommendation:
shift 15% of Zone North volume from B to A. Cost-per-order benchmark: brand paying 8% above the current published
average for comparable weight/zone couriers: renegotiation draft cites the specific rate card and date.
