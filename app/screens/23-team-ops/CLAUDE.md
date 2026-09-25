# Screen: Team and ops

Folder: `app/screens/23-team-ops/`. Purpose: queues, capacity, vendors and agencies, SOP coverage.

Read first, in this order, and nothing else unless a feature needs it:
1. `app/CLAUDE.md` (the app contract: server, data layer, UI kit, rules).
2. `app/contracts/` (metric contract, data sources, UI kit, cross-screen events).
3. This folder: `FEATURES.md` (the backlog and what is done), `screen.js`, `index.html`, `api.py` once they exist.

Spec pointers (read the section, not the whole file): room "Team and ops" in `agents/rooms/rooms.json`; agent MONEY in `agents/catalogue.json` (filter by agent); workflows and skills for MONEY in `agents/workflows/`. Copy nothing from them into this folder; link by id.

What this screen owns: its own `index.html`, `screen.js`, `screen.css` (optional), `api.py` (endpoints under `/api/23-team-ops/`), and `fixtures/` (dummy data this screen needs beyond the shared sample brand). It never imports another screen's JS. Anything two screens need lives in `app/contracts/` or `app/data/`.

Working rules for a session in this folder:
- One feature per commit. Update `FEATURES.md` status in the same commit.
- Numbers come from `app/data/` through `api.py`, computed in code. Missing shows as unavailable, never 0.
- Every insight is a rule in code with the sentence it produces. Every action button maps to a capability id and shows its autonomy (agent does, founder gate, human assist).
- US brand by default. Market-only fields (cash on delivery, return to origin) read null and are hidden unless the brand's market enables them.
- Keep this session small: do not read `agents/**` beyond the pointers above, do not read other screens.
