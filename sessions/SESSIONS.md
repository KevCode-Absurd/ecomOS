# Sessions: how ecomOS gets built without bloated context windows

Date: 28 Sep 2026. Machine copy: `sessions/sessions.json`. Card for any session: `python3 scripts/session.py <id>`.

## The rules

1. **One session, one deliverable, one folder.** A session reads at most 3 named files plus its own folder, writes the files on its card, commits, pushes, and ends. Nothing else is in scope.
2. **The card is the brief.** `python3 scripts/session.py S1.2a` prints the first line to type, the reads with token estimates, the writes and the done-when. The first line is fixed. Do not improvise a longer one.
3. **Budgets are real.** Build sessions start under about 25k tokens, bulk sessions under 12k, contract and review sessions under 40k. The card prints the estimate. If the reads exceed the budget, the session is too big: split it before starting.
4. **The big files are never opened.** `agents/catalogue.json` is about 300k tokens, `agents/rooms/rooms.json` about 180k, `agents/DATA-LAYER.md` 11k, `app/data/generate.py` 22k. Query them: `scripts/session.py --room "Paid social"`, `--capability MEDIA-C04`, `--capabilities MEDIA`, `--contract 3,5`, `--sample bombas offers`. A session that needs a slice gets the slice.
5. **Reading many things is a sub-agent's job.** When a session must survey files, docs or the web, it spawns an agent that returns at most 500 words, or records in the schema, never pages. The parent keeps its context for building.
6. **Memory is files and git, never the transcript.** Each stage folder keeps a `STATUS.md` under 30 lines: what is done, what is next, what was parked and why. The last act of every session is updating it. The next session reads `STATUS.md`, not the history. The commit message carries the reason for a decision.
7. **`/clear` after every commit.** One deliverable per conversation. Ask for the numbered item, never "improve X".
8. **Tests are the done check.** A session ends by running its tests and printing the counts. A session without a test writes one.
9. **Parallel groups run in worktrees.** Sessions in the same parallel group (S1.3, S2.1) run at the same time in separate worktrees. They share nothing but the contract. Contract changes are their own session and land first.
10. **Model by session type.** Contracts, schemas, reviews and ranking: Fable. Building: Opus. Bulk and parallel work (extractors, field census, overlays): Sonnet. Tagging inside pipelines at runtime: Haiku.
11. **Nothing paid without a card that says so.** Extractors use public pages and sub-agent web reads. No embedding calls, no benchmark reruns.

## Why this keeps context small

The heavy knowledge lives in files with a query script in front of it. A session is a card: 3 files, a folder, a first line. The brain contract is 7.7k tokens but a session reads 2 of its sections (1.8k). The product plan is 9k tokens and no build session reads it at all. `STATUS.md` replaces the history. Sub-agents do the reading. The result: a build session starts around 5k to 8k tokens and spends the rest of its window on the work.

## Stage 1: brand brain

| Id | Session | Model | Budget | Needs |
|---|---|---|---|---|
| S1.2a | Brain store, package builder and BRAIN.md router | opus | 22,000 | none |
| S1.2b | brain_sections overlay for every capability | sonnet | 12,000 | S1.2a |
| S1.3a | Bombas extractor: site crawl | sonnet | 15,000 | S1.2a |
| S1.3b | Bombas extractor: Meta Ad Library | opus | 15,000 | S1.2a |
| S1.3c | Bombas extractor: press, interviews and podcasts | sonnet | 15,000 | S1.2a |
| S1.3d | Bombas extractor: public reviews and forums | sonnet | 15,000 | S1.2a |
| S1.3e | Bombas extractor: job postings and stack | sonnet | 15,000 | S1.2a |
| S1.3m | Bombas merge and first publish | opus | 30,000 | S1.3a, S1.3b, S1.3c, S1.3d, S1.3e |
| S1.4 | Brain review with Kevin | fable | 20,000 | S1.3m |
| S1.5 | Keeper: gaps, the ask, the weekly audit | opus | 25,000 | S1.2a |

Order: S1.2a first (everything reads the store). Then S1.2b and S1.5 in parallel with the S1.3 group. S1.3m after the group. S1.4 with Kevin.

## Stage 2: data layer

| Id | Session | Model | Budget | Needs |
|---|---|---|---|---|
| S2.1a | Field census: Meta Marketing API insights and creatives | sonnet | 10,000 | none |
| S2.1b | Field census: Meta Ad Library, datasets and catalog | sonnet | 10,000 | none |
| S2.1c | Field census: Google Ads API | sonnet | 10,000 | none |
| S2.1d | Field census: Google Merchant Center | sonnet | 10,000 | none |
| S2.1e | Field census: GA4 Data API | sonnet | 10,000 | none |
| S2.1f | Field census: Shopify Admin API | sonnet | 10,000 | none |
| S2.1g | Field census: Klaviyo API | sonnet | 10,000 | none |
| S2.1h | Field census: Gorgias API | sonnet | 10,000 | none |
| S2.1i | Field census: Google Search Console | sonnet | 10,000 | none |
| S2.1j | Field census: Amazon SP-API and Ads API | sonnet | 10,000 | none |
| S2.1k | Field census: WooCommerce REST API | sonnet | 10,000 | none |
| S2.1l | Field census: Mailchimp API | sonnet | 10,000 | none |
| S2.2 | Data sources v2 contract | fable | 40,000 | S2.1a, S2.1c, S2.1e, S2.1f, S2.1g |
| S2.3 | Generator v2 for Bombas | opus | 50,000 | S2.2, S1.3m |
| S2.4 | Brand-supplied numbers and margin metrics | opus | 25,000 | S2.2 |
| S2.5 | Data review with Kevin | fable | 20,000 | S2.3, S2.4 |

Order: the S2.1 group can start today, in parallel, nothing depends on the brain. S2.2 once the 5 core census files exist. S2.3 needs the Bombas brain for calibration.

## Stage 3 on: screens, inspiration, the loop

| Id | Session | Model | Budget | Needs |
|---|---|---|---|---|
| S3.0 | Setup screen round 0 | opus | 20,000 | S1.5, S2.4 |
| S3.1 | Audit contract | fable | 25,000 | none |
| S3.x | Any screen, round 0 then rounds of 10 | opus builds, fable ranks | 20,000 | S3.1 |

Screens follow `app/BUILD-PLAN.md`: round 0 (shell, api, 3 tiles, 2 insights, 1 chart, audit stub), then rounds of 10. Each screen session reads `app/CLAUDE.md`, `app/contracts/` and its folder, and pulls its room spec with `--room`. Stage 4 (inspiration) and stage 5 (the loop) get their cards in a contract session once stage 3 has 5 screens running; the pattern is the same.

## What a session looks like, start to end

```
python3 scripts/session.py S1.3a        # read the card
<paste the first line into a fresh session>
... the session reads its 3 files, spawns a sub-agent for the web pass,
    writes records, runs python3 app/brain/validate.py on its folder ...
git add <its files> && git commit -m "<what and why>" && git push
<update STATUS.md in the same commit>
/clear
```
