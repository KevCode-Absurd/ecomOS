# ecomOS app: the contract every screen session reads

This folder is the product: one local server, one shared data layer, one UI kit, and one folder per screen. It is built the way the Meta gallery was built: a skeleton first, then features in rounds, each screen improving on its own. Read this file, then `contracts/`, then the screen folder you are working in. Nothing else.

## Layout

```
app/
  CLAUDE.md          this contract (keep under 120 lines)
  BUILD-PLAN.md      how we build, in what order, with which sessions
  server.py          one local server: static files from screens/ and web/, JSON API from data/ (to build in round 0)
  web/               the shell: nav across screens, ui-kit.css, ui-kit.js, charts.js (to build in round 0)
  contracts/         shared and small: metrics, data sources, UI kit, events between screens, brand schema
  data/
    sample-brand/    the fictional brand used to build every screen (brand.json plus generated tables)
    generate.py      deterministic dummy-data generator from brand.json (to build in round 0)
  screens/
    <nn>-<slug>/     CLAUDE.md, FEATURES.md, index.html, screen.js, api.py, fixtures/
```

## Rules that hold in every screen

- **One screen, one folder, one session.** A session works in one screen folder. It reads `app/CLAUDE.md`, `app/contracts/` and its own folder. It never reads other screens or the whole `agents/` tree. Spec pointers in the screen's CLAUDE.md say exactly which room, agent and workflows apply.
- **Shared things go through contracts.** A table two screens need is defined in `contracts/data-sources.md` and produced by `data/generate.py`. A number two screens show is defined once in `contracts/metrics.md` and computed in `server.py`, not in a screen. A screen that needs something another screen produces reads it from the data layer, never from the other screen's code. Cross-screen hand-offs are listed in `contracts/events.md`.
- **Numbers are computed in code.** Every metric has a formula, a source table, a window and an unavailable rule. Missing shows as unavailable, never 0. Period ratios come from totals.
- **Insights are rules.** A rule in code, the sentence it produces, the capability it maps to. No insight needs a model's judgement to render.
- **Every action is a capability.** Buttons carry a capability id from `agents/catalogue.json` and its autonomy: agent does, founder gate, human assist. Until the agent layer exists, a button opens a stub that shows what would happen and logs the decision to `data/decisions.json`.
- **US brand by default.** Dollars, sales tax, US holidays, US marketplaces and carriers. Market-only fields (cash on delivery, return to origin) exist in the schema, read null and stay hidden unless `brand.json` sets `market` to a market that uses them.
- **Reversed orders are three legs**: returns (received and sent back), return to origin (never received, a subset of cash on delivery, null for US), chargebacks and disputes.
- **Dummy data is honest dummy data.** The sample brand is fictional and says so on every page. Generated numbers are deterministic from a seed and shaped like real connector output (Shopify orders, GA4 sessions, Meta ad-level rows, Klaviyo flows, Gorgias tickets, reviews). When a real brand connects, the same tables fill from connectors and nothing in a screen changes.
- **Writing.** Short sentences, digits, plain words, no jargon, no em dashes. Never mention GPT or .env on a page.
- **No paid calls, no credentials in code, no writes to any external system.** Connectors are read-only adapters with a mock mode.

## The UI kit (built once in round 0, used by every screen)

Tiles with unavailable state, insight cards with rule and sentence, the 3-button decision row (Let the agent do it, Send to a person, Not now), tables with tabular numbers, a chart helper (bar, line, step, cohort grid, funnel), the filmstrip player, the founder note. Screens compose these. A screen that needs a new component adds it to `web/ui-kit.js` in its own commit and notes it in `contracts/ui-kit.md`.

## Session protocol

1. Start in the screen folder. Read the 3 things above. Run `python3 app/server.py` and open the screen.
2. Round 0 for a new screen: shell, `api.py`, 3 tiles, 2 insights, 1 chart. Commit.
3. Feature rounds: the founder asks for 10 candidates. The session ranks candidates from `FEATURES.md` (seeded from the room spec), from the capability catalogue for this screen's agent, and from one web pass on what the common tools show. Ranking: revenue impact, usefulness to a founder deciding alone, buildable on dummy data. The founder picks. One feature per commit, `FEATURES.md` updated in the same commit.
4. `/clear` between features. The conversation is not the memory; `FEATURES.md` and git are.
5. Contract changes (a new shared table, a new metric, a new kit component) happen in a separate short session at `app/` level, then screens pick them up.
