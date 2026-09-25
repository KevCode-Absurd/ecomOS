---
name: avatar-segmentation
owner: BRAND
version: 1
invoke_when: a price tier, buyer/user split, B2B line, or subscription pattern changes the underlying job for part of the customer base
inputs: current avatar record, brand brain pricing/channel/B2B/subscription facts
outputs: split-needed flag, new segment avatar record(s)
---
# Avatar segmentation

## Purpose
Not every price tier or channel needs its own avatar; most just need the same avatar buying a different SKU. This skill draws the line at whether the actual job differs, which is the only reason to fork a record.

## Steps
1. Check the trigger: a new price tier (does the premium buyer want something functionally different, or just more of the same), a gift-buyer versus the end-user (a common split where the buyer's job, e.g. "find a safe gift," differs sharply from the user's job), a B2B line (the buyer is optimizing for a business outcome, a different job entirely), or subscription churn (the ongoing-relationship job differs from the first-purchase job).
2. If the job genuinely differs, create a separate avatar record for that segment, running `avatar-record-builder` fresh for it rather than copying the parent record with edits.
3. Reuse shared quotes and language bank entries where they genuinely apply to both, but write a distinct job statement, forces and objection map for the segment.

## Checks
- A split happens only when the underlying job differs, never just because the SKU, price or channel differs.
- Each split record stands on its own evidence.

## Output
`{split_needed_flag: bool, new_segment_records: [...]}`

## Example
Gehna's gift-buyer segment (buying for a wedding guest) has a job about not embarrassing the giver, distinct from the wearer's job about looking good in photos; split into two records sharing the same product line.
