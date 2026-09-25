# Intelligence layer review

Date: 24 Sep 2026. Reviewer: lead review session (Claude). Method: 8 read-only subagent runs (3 code maps, 1 evidence review, 2 card samples, 1 outside-methods research, 1 retrieval audit), plus my own reading of the handoff, the retrieval docs and the playbook contract. Every finding below has at least 1 citation I opened myself. No code, data or playbook was changed. No paid call was made. The 158 tests pass under Python 3.11 with numpy and tiktoken installed.

Scope: the intelligence layer (sources, cards, labels, search, packing, playbooks, prompts). Kevin also asked how the whole ecomOS should be built and organised, so sections 10 and 11 cover that. The Meta gallery is out of scope.

## 1. Verdict

Right path, with changes. The idea is sound: curated expert knowledge plus each brand's own data should let a model do better ecommerce work. But the build so far is a search library with no user. No app, agent or workflow calls it, and Kevin has rated 0 outputs. The evidence collected so far does not show that stuffing 16 cards into a prompt helps. It shows the opposite on cost and speed, and a wash on quality. Keep the cards as a lookup store, distil the top tasks into short playbooks, add a brand record, route by task, and put Kevin's blind judgement at the centre of measurement.

## 2. How it works today

### Build path (done once, with Codex)

```
Google Drive (293 files, 24 folders)
   |  snapshot_drive.py: DOCX parsed, 37 other files kept as supporting
   v
256 source documents  (data/source-catalog.json)
   |  build_library.py: chunks of ~55,000 chars, 1,200-char overlap -> 630 jobs
   |  deepseek-flash + prompts/cards-v3.md, 120-280 words per card, no verify step
   v
7,611 cards  (data/library-v3/cards.json)
   |  title, summary, use_when, steps, caveats, tags + id, source, folder, section
   +--> search.sqlite   FTS5 (porter) on title, summary, tags, body
   +--> vectors.json    text-embedding-3-small 512d on title+summary+use_when+tags
   +--> metadata.json   deepseek labels: type, roles, durability, tasks (7,610 inferred, 1 reviewed)
```

### Request path (live code, no consumer yet)

```
task text (+ optional brand_context)
   |  scripts/search_knowledge.py -> intelligence/knowledge_search.py
   |  FTS5 OR-query, top 150   +   cosine over vectors, top 150 (skipped with --keyword-only)
   |  RRF 1/(61+rank) + 0.025*exact-word coverage + 0.008*task-label fit
   |  floor 0.55*top, exact-word abstention, title dedup, whole cards only
   v
compact context: up to 16 cards / 8,000 tokens (typical run: 16 cards, ~4,600 tokens)
   |
   v
[nothing]  no app, agent, or workflow reads it; only tests and finished experiment scripts
```

### Playbooks (separate track)

`playbooks/domain_specs.py` holds hand-written steps for 23 domains x 3 workflows. `scripts/build_playbooks.py` attached 3 BM25-picked cards plus 3 "foundation" cards plus 3 mixed cards to each, with no model call. That made the 69 v1 drafts. Ad-copy v1.1 to v1.4 were hand-edited in scripts and tested with AI judges. v1.2 is the best tested. Cards are pinned by id and copied into the playbook file. `scripts/read_playbook.py` is the only loader. Its only callers are tests (`tests/test_playbooks.py:9`). Nothing routes to v1.2 automatically; the loader defaults to `playbooks/v1` (`scripts/read_playbook.py:26`).

### Live versus leftover

| Part | Status | How I know |
|---|---|---|
| `knowledge_search.py`, `knowledge_metadata.py`, `library.build_index`, `budget.py` | Live | Imported by `scripts/search_knowledge.py`, `library_embeddings.py`, tests |
| `creative_retrieval.py` | Live but used only by the finished Peach Bucket writing V2 script and 2 tests | grep of importers |
| `cli.py`, `store.py`, `context.py`, `conditions.py`, `costs.py` | Leftover from the earlier card schema (claim, action, applies_when) | Reached only through `cli.py` and 2 test files |
| `units.py`, `segmentation.py`, `parsing.py`, `capsules.py` | One-off ingestion helpers | Called only by stage scripts |
| `prompts/extract.md`, `verify.md` | Dead | 0 references in .py files |
| `prompts/extract-v2.md`, `extract-cro-v1.md` | Earlier CRO pipeline only | Used by `calibrate_v2.py`, `ingest_cro.py` |
| 69 v1 playbooks, feedback template, operating contract routing table | On paper | No code reads `feedback-template.json` except `scripts/package_handoff.py` |
| ~80 scripts in `scripts/` | Most are finished experiment runners | See `CLAUDE_HANDOFF.md` section 7 |

## 3. Issues

Severity: high means it blocks the goal, medium means it degrades results or costs money later, low means tidy-up.

| # | Issue | Sev | Evidence | Fix |
|---|---|---|---|---|
| 1 | No consumer and no owner feedback loop. The search engine and playbooks have no caller outside tests and finished experiments. Kevin has never rated an output. | High | `scripts/read_playbook.py` callers: tests only. `data/ecommerce-owner-benchmark-v3/human-owner-review.csv`: 81 rows, 0 filled. `data/ecommerce-benchmark-v1/operator-rating-template.csv`: 0 of 40. `playbooks/feedback-template.json:3` version fixed at `1.0.0-draft`, no reader. | Build 1 thin workflow end to end (task 1 in section 8) and make Kevin's blind pick the gate. |
| 2 | Cards in the prompt have not beaten no cards, and they cost more. | High | TrailFold: Luna 3.41 to 3.24, Terra 3.34 to 3.71, Sol 3.78 to 3.90 (`OWNER_BENCHMARK_READOUT.md:33-37`). Cost and time per task with selected cards: Luna $0.0038 to $0.0090 and 18.5 s to 34.6 s; Sol $0.076 to $0.108 and 47.8 s to 73.2 s (`:72-80`). Writing V2: no cards scored highest for all 3 models. | Stop treating 16 whole cards as the default. Use distilled playbooks with 0 to 4 lookup cards (section 6). |
| 3 | AI judges are unstable, so every quality number so far is inside the noise. | High | Same 20 copy sets rescored: mean move 9.9 points out of 100, max 23 (`data/ad-copy-bridge-v1/scores.json` vs `bridge-v2/scores.json`; `AD_COPY_ITERATION_DECISION.md:16`). Owner-benchmark reviewers agreed on "cards helped" in 14 of 27 cells. | Use Kevin's blind pairwise picks. Use AI only for pass/fail fact and constraint checks. |
| 4 | Retrieval ranks by exact word overlap, not relevance. Stemming mismatch drops good cards. Brand context is ignored in keyword mode. | Medium | Coverage uses unstemmed tokens over title, summary, use_when and tags (`intelligence/knowledge_search.py:59`, `:95-97`; `knowledge_metadata.py:28-31`). Audit of 12 owner tasks: mean precision 0.47; "protect my Shopify store from checkout bots" returned 16 cards, 0 about bots (I reran it: 4,180 tokens); "set up GA4 ecommerce tracking" 2 of 16 right; "optimize product page" 3 of 16, while 57 of 60 PDP-titled cards never entered the top 150. Same ids with and without a "no bundles" brand context. | Stem query and card tokens the same way, weight coverage by rarity, add synonyms (pdp, pmax), cap cards per source at 4, use brand exclusions. Then add a cheap reranker if still needed. |
| 5 | Single-source folders pollute results. | Medium | 23-SEC: 326 of 412 cards from `Site Security (1).docx`, a developer web-security course. 22-AMZ: 256 of 284 from one FBA reseller course. 99-multi: 1,016 cards, 837 with no workflow link (`CLAUDE_HANDOFF.md`, section 8). | Exclude the Site Security cards from operator search by source id. Tag the FBA course as marketplace-reseller. Route 99-multi cards to real folders (they are mixed by source, not by topic). |
| 6 | Within-source repeats and examples turned into rules. | Medium | Card sample: 15 to 25% of big-source cards look mergeable; only exact 6-field copies are dropped at build (`scripts/build_library.py:87`). 6,472 cards say "the source" or "the author" in steps or caveats (my count). Weakest folders 04-BRD and 02-AVT (usable 2.6 of 5), from general marketing books. | Do not regenerate cards. Distil per task instead; the distillation step merges repeats and separates rules from stories. |
| 7 | Stale platform advice with no freshness data. | Medium | `source_date`, `last_verified_at`, `next_review_at` are null on all 7,611 cards (`intelligence/knowledge_metadata.py:66`). GA4 task: 8 of 16 cards name menu paths; `needs_current_check` flagged 15 of 16, so it does not discriminate. Stale-risk highest in 05-SET, 06-MEA, 12-GAD, 16-AEO, 22-AMZ. | Carry the Drive `modifiedTime` onto cards. Add a `ui_path` flag separate from durability. Put a "verify in the current UI" line in playbooks instead of trusting menu paths. |
| 8 | Packing is capped by the 16-card limit, not the token budget, and cards are whole or skipped. | Low | 16-card cap bound first in all 12 audited tasks; packets used 4,180 to 5,173 tokens of 8,000. Oversize cards skipped with `continue` (`knowledge_search.py:115`). | Fine for lookup. Not a fix for relevance. Leave it. |
| 9 | Playbook drift risk. Card ids are content hashes, and the loader never checks the catalog hash. | Low today, medium after any card edit | `intelligence/library.py:27-28`; `scripts/read_playbook.py:18` returns the hash without comparing. Only tests catch it. v1.2 to v1.4 `playbook.json` say "ten fully read cards" while `source-evidence.json` holds 13. | Store card ids plus a content hash check in the loader. Fix the evidence count. |
| 10 | Build pipeline is fragile for maintenance. | Medium | `build_library.py` without `--execute` still rewrites cards.json and search.sqlite (`:114-116`). The recorded prompt hash (f2341d28) differs from the current `prompts/cards-v3.md`, so any re-run misses the cache and pays again. Label caches are per 80-card batch. No tests for `sections()`, `prepare()`, `export()`. | Freeze v3. Do not re-run ingestion. New sources go through a small per-source add script with a true dry run. |
| 11 | Brand facts are not modelled. | Medium | `brand_context` is one free-text string, used only in the embedding query (`knowledge_search.py:82`). The benchmark brand sheets are ad hoc files. | Define a brand record (JSON schema) that every workflow loads: products, prices, approved claims, offer rules, voice examples, exclusions. |
| 12 | Cost tracking works but ledgers overlap and the price table is static. | Low | Global ledger $42.17 settled, $17.47 reserved; stage ledgers sum to the same reservations. `intelligence/costs.py:17-26` dated 2026-09-22 and used only by the dead `cli.py`. | Keep `budget.py`. Delete or archive `costs.py` and `cli.py`. |
| 13 | Metadata fields that carry no information. | Low | `domain` equals the folder for all 7,611 cards (0 mismatches). `section` is the chunk index 0 to 27, not a heading. | Drop `domain` from filters or repurpose it. Do not present `section` as a locator. |
| 14 | Leftover code and 58 root-level status files make the repo hard to navigate. | Low | Section 2 table above; `ls *.md` at root gives 58 files. | Move history to `docs/history/`. Keep 5 live docs at root (section 11). |

## 4. The hypothesis

Kevin's hypothesis: expert context curated with taste lets cheaper, faster models do work that would otherwise need a strong model.

**Proven**
- AI judges move by about 10 points out of 100 on unchanged text. Any result smaller than that is noise.
- Cards raise cost per task by 1.4x to 2.4x and add 7 to 26 seconds, when packed as 16 whole cards.
- Retrieval today returns about half relevant cards on plain owner questions (audit mean precision 0.47).

**Weak evidence**
- A playbook beat a generic prompt by 10 to 20 points in every ad-copy round, on 3 to 6 briefs of 1 brand, judged by AI. The gap is about the size of the judge noise, but it is the only consistent signal in the repo.
- Cards helped Terra on TrailFold (+0.37 of 4 on 9 tasks) and did nothing or hurt for Luna and DeepSeek.

**Untested**
- Cheap model plus knowledge versus strong model without knowledge. No experiment was designed for it. Every cell that can be compared across arms has the strong model without cards ahead (Luna with cards 3.24 at $0.009 versus Sol without cards 3.78 at $0.076).
- Kevin's own judgement. 0 ratings exist.
- Any task other than static ad copy and fictional-brand diagnostics.

**What would prove it**
The experiment in section 7. It needs Kevin's blind picks on real tasks, a cheap model with a distilled playbook against a strong model with nothing, and about 30 pairs to detect a 75/25 preference.

My read: the hypothesis is plausible for procedural tasks (setup checklists, flows, test design) where the knowledge is the answer. It is less likely for taste tasks (copy, creative angles) where strong models already know the general rules and the missing piece is brand facts, not expert principles. The repo's own copy tests point the same way: the playbook (a compact rule set plus brand facts) helped, the extra cards did not.

## 5. Options compared

Costs assume 2,000 tokens of brief, 1,500 of output, Sonnet 5 prices ($2 in, $10 out, $0.20 cache read per million). Cheap-model figures use Haiku 4.5 or Luna. Numbers from the methods research are marked (r); repo measurements (m); my arithmetic (a).

| Option | Quality | Cost per request | Speed | Build effort | Risk for a one-owner business |
|---|---|---|---|---|---|
| A. Today: 16 whole cards per request | Mixed to negative on quality (m) | $0.035 Sonnet, $0.004 Luna (a) | Adds 7 to 26 s (m) | 0 | Already built. Retrieval precision 0.47 (m). |
| B. Distilled task playbooks, cards for lookup only | Playbook beat generic in every copy round (m). ACE reports +8.6 to +10.6% on agent and finance tasks (r). | $0.024 to $0.029 (a) | Faster: 3k rule tokens, no selection step | 1 to 2 days per task incl. Kevin's edits; 5 tasks first | Rules can drop caveats. Keep a link from each rule to its cards. |
| C. Topic pack in a cached prefix | Long context beat RAG on average in Self-Route (r), but "context rot" grows with size (r) | 95k pack: $0.019 per cache read, $0.24 cold write; 20k pack pays only at 4+ requests per 5 min (a, r) | Fast on hit, slow cold | 1 to 2 days | Poor fit for bursty solo use. Good only for small packs in batch sessions. |
| D. Better retrieval: stemming, IDF coverage, source cap, reranker | Fixes the audit failures. Contextual retrieval plus reranker cut retrieval failures 67% in Anthropic's test (r). | +$0.001 to $0.002 for a reranker (r) | +0.2 to 1 s | 2 to 4 days incl. a 30-query labelled set | Low. But does not fix "cards do not help" on its own. |
| E. Route by task: cheap model for diagnostics and summaries, strong for copy and strategy | RouteLLM kept 95% quality at 14% strong-model use (r, academic) | $0.004 to $0.038 mix | Faster on average | 1 day for rules | Misroutes. Start with rules, not a trained router. |
| F. Fine-tune a small model | RAG beats fine-tuning on facts (r) | Not advised | Fast inference | 5+ days | OpenAI is winding down self-serve fine-tuning (r). Style only. |
| G. Mix: B + E + brand record now, D next, C only for batch sessions | Best expected | $0.005 to $0.03 by task | Fast | About 3 weeks of Opus sessions | Moderate. Depends on Kevin's review time. |

Recommendation: G.

## 6. Recommendation

**Keep**
- `data/library-v3/cards.json` as the lookup store. Do not regenerate it. It cost real money and the structure is fine for lookup.
- `intelligence/knowledge_search.py` and the FTS index, as the lookup engine, with the fixes in issue 4.
- `intelligence/budget.py` and the ledger discipline.
- `playbooks/ad-copy-v1.2` as the first distilled playbook. It is the one asset with a consistent signal.
- The rules in `CLAUDE.md`: Meta read-only, brands apart, arithmetic in code, no invented claims.
- The 158 tests.

**Change**
- Make the playbook the unit of knowledge, not the card. For each of the top 5 tasks, distil the relevant folder into 2,000 to 4,000 tokens of rules, conditions and checks, with card ids linked to each rule for lookup. Kevin edits each one once. This is the Agent Skills pattern and the ACE pattern, and it matches the only positive result in the repo.
- Add a brand record. One JSON file per brand with products, prices, approved claims, offer rules, proof available, voice examples, exclusions. Every workflow loads it first. This is the start of the brand brain, and it is where most copy failures in the repo came from (fixed-offer violations, "six items" claims).
- Route by task class with rules. Setup, flows, checklists and diagnostics go to a cheap model with a playbook. Copy, creative angles and strategy go to a strong model with the brand record and a playbook.
- Fix retrieval for lookup: stem both sides, weight coverage by rarity, synonyms, 4 cards per source, brand exclusions. Add a labelled set of 30 owner questions to test against.
- Curate the corpus by exclusion, not regeneration: exclude the Site Security course from operator search, tag the FBA course as reseller, route 99-multi cards to folders.
- Add freshness: carry Drive modifiedTime onto cards, add a `ui_path` flag, and put "verify the current UI" into playbooks.
- Measure with Kevin's blind pairwise picks and a ship / light edit / rewrite label. AI checks only for facts and constraints.

**Stop**
- Broad AI-scored tournaments across models and conditions. They cost money and settle nothing.
- Regenerating or re-ingesting cards. The prompt hash has drifted and every re-run pays again.
- Building or promoting the 69 v1 playbooks. Five good ones beat 69 drafts.
- Adding new topic folders before the first 5 workflows are in use.
- Fine-tuning, and caching whole topic folders as prompt prefixes.
- Tuning ranking heuristics by hand without a labelled query set.

**Why**
The goal is better, cheaper, faster work. Today's design pays for 16 cards on every request, half of them off target, and no one consumes the result. A playbook is smaller, faster, and was the only thing that moved the score. The brand record fixes the errors that cards cannot. Routing gets the cheap-model saving without betting quality on it. Kevin's picks are the only judge that matters for a one-owner business.

## 7. Experiment plan

**Question.** Does a cheap model with a distilled playbook and the brand record match a strong model with only the brand record, as judged by Kevin?

**Tasks.** 10 real requests, written by Kevin in his own words, for 1 brand (Peach Bucket or Gehna; not both). Suggested split: 3 static ad copy sets, 3 diagnostic questions ("ROAS dropped this week, what do I check"), 2 flow or setup tasks (welcome flow, GA4 events), 2 short plans (a creative test plan, a bundle price test).

**Knowledge.** 2 distilled playbooks written for this test: ad copy (start from v1.2) and paid-media diagnostics. Each 2,000 to 4,000 tokens, with linked card ids. Flow and plan tasks use 4 lookup cards from the fixed search engine, no playbook, to test lookup alone.

**Conditions.**
- A: strong model (Sonnet 5 or GPT-5.6 Terra), brand record only, no cards, no playbook.
- B: cheap model (Haiku 4.5 or GPT-5.6 Luna), brand record plus playbook or 4 cards.
- C: cheap model, brand record only. Control, so we know whether the knowledge did anything.

Same brand record, same brief, same output format for all 3. 1 generation each. 30 outputs.

**How Kevin judges.** Blind, order randomised, labels hidden. For each task: pick the better of A versus B, then B versus C. Label each output ship as-is, light edit, or rewrite. Note editing minutes for the one he would use. Record hard failures (wrong price, unsupported claim, fixed-offer break) as pass/fail, checked in code where possible. About 45 minutes of his time.

**Read-out.** B beats or ties A in 6 or more of 10: the hypothesis holds for that task class, extend to 30 pairs. B loses to A in 8 or more: the hypothesis fails for that class, route those tasks to the strong model. B beats C in fewer than 6: the knowledge added nothing, fix the playbook before anything else. Report per task class, not one average.

**Dollar cap.** $5 reserved in the global ledger. Expected spend under $2 (30 generations at $0.005 to $0.04). Stop at $5 or at 30 outputs, whichever comes first.

**Stop rule.** Stop the whole track if, after the extension to 30 pairs, B still loses to A in 20 or more and C ties B in 15 or more. That would mean the knowledge is not the lever and the brand record plus a strong model is the product.

## 8. Task list for Opus 5.5

Each task is one session. Effort is the suggested reasoning effort.

1. **Brand record schema and 2 records.** Scope: define `brands/schema.json` and write `brands/peach-bucket.json` and `brands/gehna.json` from existing files (Peach Bucket facts in `CLAUDE_HANDOFF.md` 7.3, Gehna in `data/meta-gallery/brand.json`). Fields: products, prices, costs, approved claims, offer rules, proof available, voice examples, exclusions, attribution settings. Accept: a loader `intelligence/brand_record.py` with 5 tests; no invented facts; unknowns marked unknown. Effort: medium.
2. **Repo tidy.** Scope: move 50+ root status and results files to `docs/history/`, keep `README.md`, `CLAUDE.md`, `CLAUDE_HANDOFF.md`, `KNOWLEDGE_RETRIEVAL.md`, `META_GALLERY_STATUS.md` at root; archive `intelligence/cli.py`, `store.py`, `context.py`, `conditions.py`, `costs.py` and their 2 tests under `archive/`; update `CLAUDE.md` paths. Accept: tests still pass; `git mv` only, no deletions. Effort: low.
3. **Retrieval fixes for lookup.** Scope: in `intelligence/knowledge_search.py` and `knowledge_metadata.py`, stem query and card tokens with the same porter stemmer as FTS; weight coverage by inverse document frequency; add a synonym map (pdp, product page, pmax, performance max, bots, bot); cap 4 cards per source; extend STOP with owner filler words; apply brand exclusions in keyword mode. Accept: a new `evals/owner_queries.json` of 30 plain owner questions with expected card ids or titles (20 from the audit list in this review), and precision at 16 moves from 0.47 to at least 0.70 on it; existing 12 search tests pass. Effort: high.
4. **Corpus curation by exclusion.** Scope: `data/library-v3/exclusions.json` listing source ids to drop from operator search (start with `Site Security (1).docx`), and a `reseller` tag on the FBA course cards via `metadata-overrides.json`; route the 99-multi cards to real folders with a keyword rule plus a manual list for the 40 sampled in this review. Accept: cards.json unchanged; search honours exclusions; a test proves the Site Security cards no longer return for the bots query. Effort: medium.
5. **Distilled playbook: ad copy v2.** Scope: start from `playbooks/ad-copy-v1.2`, fold in the v1.3 and v1.4 checklists as optional checks, link each rule to card ids, add a brand-record slot, cut to under 3,500 tokens. Output as `playbooks/v2/ad-copy/SKILL.md` plus `rules.json`. Accept: Kevin reads and edits it once; loader test passes; token count under 3,500. Effort: medium.
6. **Distilled playbook: paid-media diagnostics.** Scope: read folders 06-MEA, 10-MCR, 11-ADC, 12-GAD, 20-FIN through search and the markdown exports; write a "ROAS dropped, what do I check" playbook with a decision tree, arithmetic done in code (period ROAS, MER, contribution after ads), Meta and Google branches. Accept: under 4,000 tokens; every rule links to at least 1 card id; Kevin edits once. Effort: high.
7. **Workflow runner.** Scope: `intelligence/workflow.py` that takes task, brand id, playbook id, model tier and returns prompt, output, audit record (cards used, tokens, cost, elapsed) and appends to `data/runs/`. Rule-based model routing in `intelligence/routing.py`. No UI yet. Uses `budget.py` reservations. Accept: 1 end-to-end run per playbook on a $0.50 cap; 6 tests; no secrets in outputs. Effort: high.
8. **Owner evaluation kit.** Scope: `scripts/eval_pairs.py` that builds a blind, shuffled review sheet (CSV or a local HTML page) from run outputs, and `scripts/eval_readout.py` that computes wins, ties, ship/edit/rewrite counts and hard-fail counts per task class. Accept: sheet hides model and condition; readout handles missing rows; 4 tests. Effort: medium.
9. **Run the experiment in section 7.** Scope: 10 tasks from Kevin, 30 generations, $5 reservation, sheet handed to Kevin, readout written to `reviews/EXPERIMENT_1_READOUT.md`. Accept: ledger shows the reservation and settlement; every output saved; readout reports per class. Effort: medium. Needs Kevin's 10 tasks and 45 minutes first.
10. **Freshness fields.** Scope: carry Drive `modifiedTime` from `data/snapshots` and `data/inventory` onto `metadata.json` as `source_date`; add a `ui_path` flag by regex (menu arrows, "Settings >", "Admin >", "click"); expose both in the search response instead of the blanket `needs_current_check`. Accept: counts reported; test proves the GA4 query flags fewer than 16 of 16. Effort: low.
11. **Playbook drift guard.** Scope: make `scripts/read_playbook.py` compare `source_catalog_sha256` to the live catalog and warn; fix the evidence count in v1.2 to v1.4 `playbook.json`. Accept: 2 tests. Effort: low.
12. **Per-source add script with a true dry run.** Scope: `scripts/add_source.py` that ingests 1 new DOCX into cards, embeddings and labels under a stated cap, writes nothing without `--execute`, and does not touch other sources' jobs. Accept: dry run leaves `git status` clean; test with a fixture. Effort: medium. Do this only when Kevin has a new source to add.

Order: 1, 2, 3 and 4 can run in parallel. 5 and 6 need 1. 7 needs 1, 3, 5. 8 is independent. 9 needs 7 and 8. 10, 11, 12 fit anywhere.

## 9. Questions for Kevin

1. Which brand is the first real user: Peach Bucket (copy track, small data) or Gehna (gallery, 1 year of Meta and Metabase data)? The experiment and the first playbooks should target 1 brand.
2. Will you give 45 minutes for the blind review in the experiment, and 1 editing pass on each of the first 2 playbooks? The plan depends on it.
3. Is the "owner asks a question and gets an answer" interface the first product, or is "produce a deliverable" (ad copy, flow, plan) first? Section 8 assumes deliverables first, since that is where the evidence is.
4. Is the Site Security developer course meant for ecommerce operators, or was it added for a future security agent? I recommend excluding it from operator search either way.
5. Do you want the 99-multi folder re-sorted into topic folders, or is the mixed folder deliberate?

## 10. The wider system: how to build the 5 layers

Kevin's picture has 5 layers: data layer with a warehouse and CAPI enrichment, brand brain, intelligence layer, inspiration layer, execution layer. The picture is right. The order matters for a one-owner business.

**Build a thin slice first, not a layer at a time.** A warehouse with all sources connected is the most expensive layer and pays off only when something consumes it. The Gehna gallery already proves the pattern: a narrow data pull (Meta plus Metabase for 1 brand), a brand file, and 2 or 3 deliverables (action plan, client report). Copy that pattern.

Suggested order, each step usable on its own:

1. **Brand record** (task 1). Cheap, and every other layer needs it. This is the seed of the brand brain.
2. **Intelligence as playbooks plus lookup** (tasks 3 to 7). 5 workflows, 1 brand, Kevin's judgement as the gate.
3. **Execution as draft mode** (task 7 grows into it). Every workflow produces a draft and an audit record. No writes to Meta, Shopify or Klaviyo until a human clicks. Keep the Meta read-only rule.
4. **Data layer for 1 brand.** Extend the gallery's Meta and Metabase pulls into a small normalised store (daily spend, revenue, orders, COGS, margin by day and campaign) with a data-integrity check (missing days, duplicate rows, currency). Then the diagnostics playbook can read numbers instead of asking for them. A full warehouse and CAPI gross-profit events come after this works for 1 brand.
5. **Inspiration layer.** Start with the 3,000 to 4,000 statics Kevin already has. Store each with a structured description (format, hook type, product placement, colour, text density, offer shown) written once by a vision model, plus performance where known. Match by those fields and by embedding. Competitor ads stay signals, never copied. Video, landing pages and email come after statics show use.
6. **Experiment memory.** A table of hypothesis, brand, asset versions, dates, budget, result, decision. Fill it from the runs in task 7 and from the gallery's test list. This is what stops repeating tests.
7. **Client-facing interface.** After 2 brands run on the same code. Hosting, auth and tenant separation are a real project on their own.

What not to do first: a general warehouse for every source, a general video pipeline, a trained router, or autonomous execution.

## 11. How to organise the project in Claude Code

Treat the repo as 1 product with 5 layers, and give each layer 1 folder, 1 short doc and 1 owner note.

```
ecomOS/
  CLAUDE.md                  rules, layer map, current step (keep under 150 lines)
  README.md                  what this is, how to run tests
  docs/
    ROADMAP.md               the 7 steps above, with the current one marked
    DECISIONS.md             dated decisions, 3 lines each (replaces 58 status files)
    history/                 all old reports and status files, untouched
  brands/                    brand records (schema + 1 file per brand)
  intelligence/              search, playbooks loader, workflow runner, routing, budget
  playbooks/v2/<task>/       SKILL.md + rules.json per distilled task; v1 archived
  data/                      library-v3 (frozen), runs/, brand data pulls
  data_layer/                per-brand pulls and integrity checks (grow from meta_gallery)
  inspiration/               asset store and descriptions (later)
  meta_gallery/              as is, until data_layer absorbs the pulls
  evals/                     owner_queries.json, review sheets, readouts
  scripts/                   only live commands; experiment runners move to docs/history or archive/
  tests/
  .claude/agents/            the 5 review agents, plus 1 builder agent per layer later
  .claude/skills/            house style for client pages and copy, as a skill
```

Working habits that fit this repo and 1 owner:
- One session per task from section 8. The task text is the session brief. Commit at the end with the task number in the message.
- `CLAUDE.md` says what the current step is and what is frozen. Old reports never override it.
- Every paid step reserves in `budget.py` first and states its cap in the task.
- Kevin's review time is the scarce resource. Batch it: 1 blind review sheet per week, 45 minutes.
- Add a `DECISIONS.md` line each time a version is kept or dropped, so the next session does not re-argue it.
- Keep the review agents in `.claude/agents/` and re-run the retrieval auditor after task 3 as the acceptance check.

## Appendix: numbers behind the tables

- Card sample, folders 01 to 12 (96 cards, seed 7) and 13 to 99 (140 cards, seed 11), graded 1 to 5: strongest 09-CRO 4.3, 20-FIN 4.2, 12-GAD 4.2; weakest 23-SEC 2.4, 04-BRD 2.6, 02-AVT 2.6, 13-ORG 2.6. Stale-risk highest 05-SET 4.4, 06-MEA 4.3, 16-AEO 4.2. 8 cards per folder, so direction only.
- Whole-file counts: 7,611 cards, 256 sources, cards per source min 3, median 16, max 326. 13 exact duplicate title groups (29 cards). Median card length 216 words. 0 empty step lists.
- Retrieval audit, 12 owner tasks, keyword-only, 16 cards each: precision 0.13 to 0.88, mean 0.47; tokens 4,180 to 5,173; the 16-card cap bound first every time; top 5 unchanged at a 2,500-token budget.
- Ledger: $42.17 settled and $17.47 reserved of a $160 working stop; experiments about $24.8 settled.
- Judge drift: 20 unchanged copy sets moved 9.9 points on average between review batches, max 23.
