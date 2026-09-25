---
name: research-customers/social
owner: BRAND
version: 1
invoke_when: the source is public social platforms or forums, not the brand's own data
inputs: avatar's likely platforms, public web access
outputs: language bank additions, sub-avatar candidate notes
---
# Run social and forum listening

## Purpose
Public forums surface language, objections and sub-avatars in the customer's own words that a brand's own review file, which only hears from people who already bought, would miss entirely.

## Steps
1. Identify where this avatar actually talks in public: a subreddit, a Quora thread topic, Instagram comment sections on relevant posts, public Facebook groups.
2. Search those places using the avatar's own phrasing (from prior quote sets), not marketing terms.
3. Pull exact language, named objections, and any sub-avatar pattern (a distinct sub-group with a different job) that surfaces.
4. Record the source URL and date for every finding used.
5. Discard anything found in a private or closed group; only public, publicly-indexed content is used.
6. Flag any objection here that did not appear in the brand's own reviews or tickets; that gap is itself a signal (customers with this objection may not be buying at all).

## Checks
- Every finding carries a public URL and a date.
- Nothing from a private group, DM, or paywalled forum is used.
- Language additions are exact quotes, not paraphrases, since the language bank exists to reuse real words.

## Output
`{language_bank_additions: [...], sub_avatar_candidates: [...]}`

## Example
r/SkincareAddiction thread, dated 2 Sep 2026: "wish more brands made this in a travel size for humid weather" flagged as a sub-avatar candidate (frequent traveler) with 3 similar comments in the same thread.
