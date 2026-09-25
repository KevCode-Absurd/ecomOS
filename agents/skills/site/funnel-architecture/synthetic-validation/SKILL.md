---
name: synthetic-validation
owner: site-specialist
version: 1
invoke_when: validating a storefront against a simulated shopper persona before an expensive redesign, or checking readiness for a third-party AI shopping agent
inputs: candidate page or theme version, persona definitions or product feed/structured data, sandbox store
outputs: persona run report, friction points list, design comparison summary, agentic-checkout readiness report
---
# Synthetic shopper and agent validation

## Purpose
Test a storefront against a non-human simulated actor, either a synthetic shopper persona or a third-party AI shopping agent, before trusting it with real traffic or real orders.

## Steps
1. For a redesign: define 3-6 personas matching the brand's real segments (first-time, repeat, price-sensitive, gift buyer).
2. Run each persona through the current site and the candidate redesign in a private, non-indexed sandbox.
3. Record add-to-cart rate, click-path length and the exact step each persona abandoned at; compare two designs head to head.
4. State plainly this is a prediction, not a measured result, and should not replace a real A/B test where real money is at stake.
5. For an AI shopping agent channel: verify the product feed and structured data (price, stock, variant, shipping) are accurate.
6. Check the checkout completes an agent-initiated purchase without a broken step, and confirm order attribution tags it correctly.
7. Flag any blocking step (CAPTCHA, mandatory account) and decide with the founder whether to relax it.

## Checks
- Persona output is always labelled a prediction, never presented as a real result.
- Agentic-checkout readiness stays read-only until real agent-driven orders are seen in order-source data.

## Output
A persona run report with friction points and a design comparison, or an agentic-checkout readiness report with a blocked-step list.

## Example
"Persona 'price-sensitive first-timer' abandoned at the shipping-cost reveal in checkout on both designs; this is a prediction, recommend a real A/B test on shipping-cost disclosure timing."
