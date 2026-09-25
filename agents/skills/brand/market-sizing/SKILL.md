---
name: market-sizing
owner: BRAND
version: 1
invoke_when: a new niche or product idea needs sizing from the brand's own numbers
inputs: AOV, gross margin, contribution margin, repeat rate; candidate niche
outputs: sustaining-buyer-count figure, independent size signal, matrix placement
---
# Market sizing

## Purpose
An idea sounds bigger than it is until it is sized against this brand's actual AOV, margin and repeat rate. This skill does that arithmetic in code, every time, instead of letting an estimate happen in prose.

## Steps
1. Compute how many repeat buyers, at what purchase frequency, would sustain the business or the candidate line at this AOV and contribution margin. Use the metric contract fields directly; a missing field shows as unavailable, never assumed.
2. Search for an independent size signal for the specific niche: category search volume, a relevant subreddit or forum size, marketplace listing count, or a review-count proxy for comparable products. Every signal needs a URL and date.
3. Place the candidate on a matrix of price point against the customer count needed, to see whether this is realistically a volume play or a margin play, stated as a range rather than a false-precise number.

## Checks
- All arithmetic runs in code, never estimated in prose.
- A missing input shows as unavailable, never filled with an assumption.
- A sizing claim always cites the independent signal it is based on; a niche with no findable signal is marked "unproven."

## Output
`{sustaining_buyer_count, size_signal: {value, source, date}, matrix_placement}`

## Example
At AOV $65 and 28% contribution margin, sustaining an $18,000/month line needs approximately 220 repeat buyers per month at a 2x/year frequency; independent signal: category search volume flat over 12 months per Search Console, so treated as a margin play, not a volume play.
