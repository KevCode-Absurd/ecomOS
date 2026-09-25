---
name: money/pricing-waterfall
owner: MONEY
version: 1
invoke_when: a product needs pricing from a profit target, or a promo needs a break-even check
inputs: landed cost, fee schedule, return rate, net-profit target, promo terms
outputs: price waterfall or promo cost model with a break-even result
---
# Price or promo from a profit target

## Purpose
Price bottom-up from a real profit target, never top-down from a keystone guess, and never let a promo go live without knowing its true break-even.

## Steps
1. Read the brand's stated net-profit target for the SKU or line.
2. For a price: solve the waterfall from landed cost through fees, shipping, returns and marketing cost to the shelf price that hits the target.
3. For a promo: model the real cost shape of the specific mechanic (percent-off, BOGO, gift-with-purchase, flash sale), not a flat assumption.
4. Run a break-even go/no-go check, or a margin stress-test for a new price.
5. Once live, stress-test the price against 60 to 90 days of real sell-through.

## Checks
- The profit target always comes from the brand record.
- Every waterfall line between cost and price is shown, none skipped or merged.

## Output
The full waterfall or promo cost model, the recommended price or the break-even volume, and the stress-test result once available.

## Example
A proposed BOGO on a 40 percent margin SKU breaks even only above a 22 percent lift in units; the gate returns no-go until a lift test confirms that volume is realistic.
