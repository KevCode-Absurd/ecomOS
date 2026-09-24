# Blind A/B test 2: Meta ad copy for Gehna, with and without the playbook

Date: 24 Sep 2026. Second run of the playbook test. The first run (`reviews/speed-test/`) was on site speed, where both arms found the same technical facts. This run is on a judgement domain: ad copy.

## What changed from run 1

- Same 2-stage pipeline in both arms (audit, then plan), so the test isolates the playbook and not the pipeline.
- Same brand data for both arms. In run 1 only the playbook arm had backend data; here both arms get the same ad account cache and brand record. Only the playbook differs.
- 3 judges instead of 2, reading order randomised per judge, each judge must verify 3 factual claims per report against the raw data before scoring.

## Arms

Both arms: one Fable agent each, no model override. Both read the same inputs: `data/meta-gallery/brand.json` (voice, approved claims), `data/meta-gallery/cache/gallery.json` (472 ads, 333 with copy, daily spend, purchases, value, impressions and clicks per ad from 23 Sep 2025 to 24 Sep 2026), and the live site gehnaindia.com. Both can use the public web. Neither calls the Meta connector; the cache is the shared, fixed evidence. Neither reads the gallery's own pattern analysis (`data/meta-gallery/playbook.json`, `notes.json`, `tests.json`, `packs.json`, `variants/`), so each arm does its own analysis.

- Arm A (general): general knowledge plus the web. Must not open `playbooks/`, `data/library-v3/`, `intelligence/` or the knowledge notes.
- Arm B (playbook): the same, plus `playbooks/v2/11-ADC-ad-copy-deployment/PLAYBOOK.md` (read in full, section 3.0 first), `playbooks/v2/24-DEP-ad-deployment/PLAYBOOK.md` for test design, and free keyword search over the card library (`scripts/search_knowledge.py --keyword-only`).

## Task (identical brief to both)

Stage 1, audit: what copy the account runs today, which angles, hooks and products carry the spend and the purchase value, what the site promises, which claims are in use and whether they are approved, and where the gaps are. Save every extracted table as JSON or CSV in the arm's raw folder so a judge can check it.

Stage 2, plan: 12 Meta ad sets (primary text, headline, description) across 3 objectives: new buyers, site visitors and cart abandoners, past customers. Each ad carries its angle, product or collection, proof used, and a claim check that traces every claim to the approved list or a page on the site. Then a 4-week test plan: structure, budget split as a share of current spend, kill and scale thresholds set from the account's own baselines, what to measure, and a "decisions for the owner" block.

## Judging

3 Fable judges, blind. Reports are copied to `blind/report-1.md` and `blind/report-2.md` under a random mapping kept in the scratchpad until the verdict is written. Each judge: verify 3 numbers or claims per report against the raw folders and brand.json, then score 1 to 10 on (1) would the owner run these ads as written, (2) editing effort to make them usable, (3) claim accuracy, (4) specificity to Gehna and to ecommerce, (5) test plan quality, and name a winner with reasons. Kevin's own pick is the deciding signal.

## Rules for every agent

Meta is read-only and not called. No credentials. Competitor ads are signals, never copied. No invented claims, prices, offers or numbers. Short sentences, digits, no em dashes, no inflated words. Arithmetic in code, not prose. Missing metrics show as unavailable, not 0.
