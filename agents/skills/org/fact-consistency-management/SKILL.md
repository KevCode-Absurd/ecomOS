---
name: fact-consistency-management
owner: ORG
version: 1
invoke_when: monthly to build/refresh the facts page, or on a wrong-fact-found event
inputs: AI-visibility probe gaps, approved-tier brand facts, every surface a fact appears on
outputs: facts page blocks, a cross-surface consistency check, a priority correction plan, a recheck date
---
# Brand fact consistency: facts page build and correction

## Purpose
Publish a facts page that answers every gap the probe finds, keep the same fact identical everywhere an engine can read it, and when an AI states something wrong, fix it in the right order: the site first, the likely publisher second, the wider web third.

## Steps
1. Check each probe gap against the current facts page; draft any missing fact block.
2. Write each block atomically: the entity named directly, one fact, a source if external.
3. Check the same fact across site copy, schema, product feed, directory listings and review profiles for consistency.
4. On a wrong fact found, fix the site source first.
5. Identify the likely publisher source and draft correction outreach to them second.
6. If the fact has spread wider, draft a wider correction plan third.
7. Schedule a recheck of the engines to confirm the fix was actually picked up.

## Checks
- Facts are atomic and tier-checked.
- The same fact matches on every surface.
- Correction follows site-then-publisher-then-web order, always.
- A recheck is scheduled.

## Output
{facts_page_blocks[], consistency_check[], correction_plan[], recheck_date}

## Example
An AI answer states the wrong warranty length; the site's own warranty page is corrected first, then outreach goes to the directory listing that likely fed the wrong figure, with a recheck scheduled for 30 days out.
