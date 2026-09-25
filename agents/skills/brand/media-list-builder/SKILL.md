---
name: media-list-builder
owner: BRAND
version: 1
invoke_when: a specific story or launch needs a targeted, verified media list
inputs: pitch angle, target media tier
outputs: verified, beat-matched media list
---
# Media list builder

## Purpose
A generic media database list wastes outreach on journalists who no longer cover that beat. This skill builds a small, verified list matched to the specific angle, not a purchased mailing list.

## Steps
1. Search public journalist and outlet information (recent articles, bylines, outlet beat pages) for people whose current coverage matches this specific pitch angle.
2. Verify each match against the journalist's recent bylines (last 3-6 months), not an old media database entry that may be stale.
3. Note each contact's outlet, beat, and the specific recent piece that shows the match, so the pitch can reference it.

## Checks
- Every listed contact's beat match is checked against recent, real bylines, never assumed from an old database record.
- The list is sized to quality, not volume; a focused list of 8-15 real matches beats a generic list of 100.

## Output
`{verified_beat_matched_media_list: [{name, outlet, beat, recent_piece, url, date}]}`

## Example
Contact matched on a piece published 3 weeks ago about sustainable Indian fashion brands, directly relevant to this brand's durability angle, with the piece URL attached for pitch reference.
