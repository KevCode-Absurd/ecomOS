# ecomOS: notes for Claude Code

Kevin's e-commerce operating system for brands and agencies: research, offers, creative, copy, landing pages, acquisition, retention, operations and measurement. The edge should come from expert ecommerce knowledge plus each brand's own data, voice, references and test history.

Priorities: quality first, cost second, speed third. Deliverables must be ecommerce-specific and usable, not citation-heavy.

## Read first

1. This file.
2. `CLAUDE_HANDOFF.md`: full history from Codex (architecture, phases, decisions, benchmarks, budgets, gaps). `CLAUDE_START_HERE.md` is the short version. `HANDOFF_PROJECT_SNAPSHOT.json` has dated counts, hashes and ledger totals.
3. For the library and copy track: `LIBRARY_WORKFLOW.md`, `KNOWLEDGE_RETRIEVAL.md`, `CREATIVE_RETRIEVAL.md`, `AD_COPY_ITERATION_DECISION.md`, `playbooks/README.md`, `playbooks/OPERATING_CONTRACT.md`, `playbooks/ad-copy-v1.2/`.
4. For the Meta gallery track: `META_GALLERY_STATUS.md`, newest update first.

Older READMEs and reports are history. Check current files before trusting them.

## What exists

Two tracks share this repo.

**1. Intelligence library (built with Codex)**
- `data/library-v3/cards.json`: 7,611 task-sized cards from 256 source documents, 23 topic folders plus 1 mixed folder. This is the canonical library. Do not restart ingestion or regenerate cards.
- Search: `scripts/search_knowledge.py` (engine `intelligence/knowledge_search.py`). Keyword (SQLite FTS, `search.sqlite`) plus semantic (`vectors.json`, text-embedding-3-small, 512 dims), labels in `metadata.json`. Defaults: 8,000 tokens and 16 cards for focused tasks. Use `--keyword-only` to avoid an embedding call.
- Creative routing: `intelligence/creative_retrieval.py`.
- Playbooks: `playbooks/v1` has 23 domains x 3 workflows = 69 drafts. For ad copy, `playbooks/ad-copy-v1.2` is the strongest tested version; v1.3 and v1.4 did not replace it. Do not overwrite manual versions with `scripts/build_playbooks.py`.
- Benchmarks (fictional TrailFold, Peach Bucket, ad-copy rounds) gave mixed results. Retrieval is not a proven win, and AI reviewer scores were unstable. Owner preference and editing effort are the better signal.

**2. Meta gallery for Gehna (built with Claude)**
- `meta_gallery/`: Gehna's Meta ad gallery (ad account 577226564072364). Run `python -m meta_gallery.server`, then open http://127.0.0.1:8765. The page is in `meta_gallery/web/` (app.js, engine.js, overview.js, insights.js, lab.js, studio.js, sales.js, testlab.js, prodads.js, report.js, buyer.js, catalog.js, index.html).
- The same page is published at https://claude.ai/artifact/PYtCXf5norsr9vhSw4ZFVT (shared as "anyone with the link").
- Tabs: overview, action plan with ranked tests to run, brand sales (Metabase, months and days), ad gallery, campaigns, insights, creative studio (paste a reference image to build variants), competitors (7 brands with pills), client report.
- Data in `data/meta-gallery/`: `cache/gallery.json` (1 year of Meta), `sales.json` (monthly plus `daily` from 1 Aug 2026), `competitors.json` and `comp_media.json`, `brand.json`. Meta and Metabase were refreshed to 23 Sep 2026 on 24 Sep.
- Refresh: `python -m meta_gallery.refresh meta ...` (merges a read-only MCP re-pull into a new raw capture) and `python -m meta_gallery.refresh sales FILE` (applies a pull made by `meta_gallery/metabase_pull.js` in a signed-in Metabase tab). Steps are in `META_GALLERY_STATUS.md`, Update 9.

Not built yet: a general brand brain, a general reference library, an experiment registry, hosting with auth, and autonomous execution.

## Rules

- Meta is read-only. No publishing, pausing, budget changes or other ad-account writes. The Meta MCP has write tools; that does not make them allowed.
- Never print, paste or commit credentials. Keys live in `.env` and `secrets/` (both git-ignored). API keys stay on the backend, never in browser JavaScript. Subscriptions are not API keys.
- Metrics: missing or unsupported values show as unavailable, not zero. Period ROAS = total value ÷ total spend. Keep totals separate from breakdowns. Keep ad-level metrics when ads share an image. Flag dynamic or mixed creatives. Do arithmetic in code, not in the model.
- Keep brands apart: Gehna (gallery), Peach Bucket (copy tests, childproofing kit) and TrailFold (fictional benchmark).
- Keep public web research separate from private business data.
- Source cards stay intact; feedback changes playbooks, brand records or applicability rules instead.
- Competitor ads are signals, not proven winners. Use them for layout and mood only; never copy text, logos, products or faces.
- Generated images can redraw products. Where accuracy matters, use the real product photo.
- Writing on pages and in copy: short sentences, simple words, digits, no em dashes, no inflated words, below tenth-grade reading level, concrete before-to-after benefits, no invented claims. Do not mention GPT or .env on client pages.

## Money and paid calls

- `intelligence/budget.py` keeps a spend ledger with reservations. Working stop $160, absolute ceiling $200. Snapshot on 24 Sep 2026: about $42.17 settled and $17.47 reserved. Stage ledgers overlap the global one; do not add them up.
- Never clear a reservation to unblock a run, and never rerun paid experiments just to understand the project.
- Paid or side-effect commands: `scripts/build_library.py --execute`, `scripts/library_embeddings.py`, `scripts/classify_knowledge_labels.py`, benchmark scripts, `meta_gallery.graph_client`. Check before running.

## Tests and commands

- Full suite: `python -m unittest discover -s tests` (158 passing on 24 Sep 2026). It needs Python 3.12: the bundled tiktoken in `.retrieval-runtime/` is a 3.12 build, so the default Python 3.11 gives 12 import errors. Use `C:\Users\kevin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`, or install tiktoken for 3.11. Gallery only: `python -m unittest tests.test_meta_gallery -v`.
- Read a playbook: `python scripts/read_playbook.py --directory playbooks/ad-copy-v1.2 --list`.

## Git and data

- Repo: https://github.com/KevCode-Absurd/ecomOS (private). Kevin pushes; Claude commits with a short note.
- On 24 Sep 2026 Kevin chose to put `data/` in the private repo (commit c403d0d). Older notes that say data is git-ignored are out of date. `.env`, `secrets/` and `backups/` stay out.
- Check `git status` before committing. Do not run a blind `git add .` over other sessions' work. Commit data only after real updates, since big files grow the history. `data/library-v3/vectors.json` is 72 MB; move it to Git LFS if it nears 100 MB.
- Data backups: zips in `backups/`, copied to the "ecomOS backups" Google Drive folder.

## Data sources

- Meta: the Meta Ads MCP connector in Claude (read tools only). The direct Marketing API is not active yet.
- Metabase: https://analyze.gehnaindia.com dashboard 6 (website sales). The connector cannot read the cards yet, so daily data came from a signed-in browser. Production access is coming.

## Next steps (Kevin picks the track)

- Copy track: build a compact Peach Bucket writing brief from Kevin's liked and disliked examples, then write 3 real requests with ad-copy v1.2 and only the cards each decision needs. Judge by whether Kevin would use them and how much editing they need.
- Gallery track: production access for Meta and Metabase, then scheduled refreshes; tie tests to results.
- Later: brand brain, reference library, experiment memory, agent layer.
