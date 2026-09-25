---
name: money/financing-comparison
owner: MONEY
version: 1
invoke_when: cash is running low or a hard-to-source launch needs funding
inputs: cash forecast, current financing terms, reference cost-of-capital rates, slow-month sales history
outputs: financing option comparison with a repayment stress-test
---
# Compare financing options against the cash forecast

## Purpose
A financing decision made against the actual 13-week forecast, at the real cost of capital, not the advertised rate.

## Steps
1. Pull the current cash forecast and the lowest-cash flag if one exists.
2. Compare a line of credit, inventory financing and revenue-based financing against reference cost-of-capital rates for each.
3. For a hard-to-source or hard-to-fund launch, widen the search to crowdfunding, private capital and manufacturer referrals, and look for a cheap way to prototype before any commitment.
4. Stress-test the repayment schedule of the leading option against the brand's own slowest historical month, not a generic haircut.

## Checks
- Every option is shown at its real annualized cost of capital.
- The stress test uses the brand's own sales history, not an assumed decline.

## Output
A comparison table of options with real cost of capital, and a repayment stress-test result for the leading option.

## Example
A revenue-based advance's headline '8 percent fee' works out to a 34 percent annualized cost once the repayment period is short; the comparison states the annualized figure next to the headline one.
