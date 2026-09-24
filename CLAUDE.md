# ecomOS: notes for Claude Code

This repo is Kevin's e-commerce operating system. Read this first, then the status file for the area you work on.

## Where things are

- `meta_gallery/`: the Meta ad gallery for Gehna (ad account 577226564072364). Local server: `python -m meta_gallery.server` then open http://127.0.0.1:8765. The web page is in `meta_gallery/web/` (app.js, engine.js, overview.js, insights.js, lab.js, studio.js, sales.js, testlab.js, index.html). The same page is published as a claude.ai artifact: https://claude.ai/artifact/PYtCXf5norsr9vhSw4ZFVT
- `META_GALLERY_STATUS.md`: full history of the gallery, newest update first. Read it before changing the gallery.
- `data/meta-gallery/`: gallery data. `cache/gallery.json` (Meta, 1 year), `sales.json` (Metabase monthly plus `daily` from 1 Aug 2026), `competitors.json` and `comp_media.json` (Ad Library snapshot with images), `brand.json`.
- `intelligence/`, `playbooks/`, `prompts/`, `scripts/`: the knowledge library and playbooks. Other `*_STATUS.md` files describe each area.
- Tests: `python -m unittest tests.test_meta_gallery -v` (49 passing on 24 Sep 2026).

## Rules

- Meta access is read-only. No publishing, campaign edits, budget changes or other ad-account writes.
- Never print tokens or commit credentials. Keys live in `.env` (git-ignored) and stay on the backend, never in browser JavaScript.
- Missing or unsupported metrics show as unavailable, not zero. Period ROAS = total value ÷ total spend. Keep aggregate totals separate from breakdowns. Keep ad-level metrics when ads share an image. Flag dynamic or mixed creatives.
- Writing on the page: short sentences, simple words, digits, no em dashes, no inflated words. Do not mention GPT or .env on the page.
- Competitor images are for layout and mood only. Never copy their text, logos, products or faces.

## Data sources

- Meta: the Meta Ads MCP connector (read tools only). The direct Marketing API is not active yet.
- Metabase: https://analyze.gehnaindia.com dashboard 6 (website sales). The Metabase connector cannot read the cards yet; daily data was pulled from a signed-in browser. Production access is coming.

## Open items

- Metabase and Meta production access, then scheduled refreshes.
- Back up `backups/` zips to the "ecomOS backups" Google Drive folder.
