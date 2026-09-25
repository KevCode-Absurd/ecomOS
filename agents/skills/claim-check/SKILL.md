---
name: claim-check
owner: shared (QA Gate runs it; specialists self-apply)
version: 1
invoke_when: any customer-facing text is produced (copy, page, email, listing, reply)
inputs: the text; brand record claims in 3 tiers; prices; policies; forbidden words
outputs: pass or list of failing sentences with the tier and a fix
---
# Claim check

## Purpose
Every factual statement traces to an approved or site-backed claim. Nothing forbidden, nothing invented.

## Steps
1. Split the text into sentences. Mark each sentence that states a fact about product, price, delivery, policy, guarantee, result, origin, material or certification.
2. For each fact sentence, find the matching claim in the tiers. Record the tier and the source.
3. A sentence with no match is "untraced". A sentence matching a forbidden claim is "forbidden".
4. Check numbers against the record (prices, days, percentages). A number not in the record fails.
5. Check forbidden words and superlatives without a fact behind them.
6. Return the list.

## Checks before returning
- Every fact sentence has a verdict.
- Fixes rewrite the sentence with an approved claim or remove it; they never invent a new claim.

## Output
{pass, failures[{sentence, verdict, tier, source, fix}]}
