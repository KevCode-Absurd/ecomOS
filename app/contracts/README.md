# Contracts

Small, shared, read by every screen session. Change them in their own short session, commit first, then screens pick them up.

| File | What it fixes |
|---|---|
| `metrics.md` | The metric contract: every number a screen may show, with formula, source table, window, unavailable rule. Computed in `server.py`. |
| `data-sources.md` | The tables in `app/data/`, their fields, which connector fills each one for a real brand, and how `generate.py` fakes it. |
| `ui-kit.md` | The components in `web/ui-kit.js` and `charts.js`, with the props each takes. |
| `events.md` | Cross-screen hand-offs: what one screen writes that another reads, always through the data layer. |
| `brand.schema.json` | The brand record a screen may read: identity, market, channels, policies, claims tiers, red lines. |

Seed for all of these: `agents/DATA-LAYER.md` (283 tables the rooms asked for, most-shared first) and the room specs in `agents/rooms/rooms.json`. Round 0 lifts the first 30 tables and the metrics the first screens need. The rest come in as screens need them.
