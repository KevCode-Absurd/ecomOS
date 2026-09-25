"""Create the app/ skeleton: one folder per screen, each with its own CLAUDE.md and a seeded FEATURES.md backlog.

Idempotent: never overwrites a file that already exists, so screen folders can be edited freely after scaffolding.
Usage: python3 scripts/scaffold_app.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "app")
ROOMS = json.load(open(os.path.join(ROOT, "agents", "rooms", "rooms.json"), encoding="utf-8"))
BYROOM = {r["room"]: r for r in ROOMS}

# journey order for a normal US DTC brand; (folder slug, room name, one-line purpose)
SCREENS = [
    ("00-today", "Today", "the break in the pipeline, the top 10, pending decisions, ask anything"),
    ("01-market-research", "Products and research", "demand, competition, price bands, product candidates, review mining"),
    ("02-customers-avatars", "Brand and customers", "who buys and why, avatars with evidence, language bank, brand health"),
    ("03-competitors", "Competitors and market", "competitor ads, sites, prices and launches as signals, positioning map"),
    ("04-offers-pricing", "Offers and pricing", "offer economics, discount policy, free shipping threshold, bundles, guarantees"),
    ("05-brand-brain", "Brand brain", "facts, claims tiers, decisions, open questions, freshness"),
    ("06-store-health", "Store health", "setup checklist, uptime, checkout, apps and scripts, payment methods, reversed orders"),
    ("07-landing-pages-cro", "Landing pages and CRO", "page quality, message match, tests from hypothesis to read"),
    ("08-site-speed", "Site and speed", "measured fix chain, filmstrip, developer briefs"),
    ("09-creative", "Creative", "winners and losers by angle, hook and format, fatigue, production pipeline"),
    ("10-copy", "Copy", "copy sets, claim checks, message match, voice compliance"),
    ("11-paid-social", "Paid social", "pacing, structure, kill and scale, tests, anomalies, change lists"),
    ("12-google-ads", "Google Ads", "search, shopping, PMax, feed quality, search terms"),
    ("13-affiliate-marketplace-ads", "Affiliate, marketplace and retail media", "affiliates, Amazon and Walmart ads, retail media, billing reconciliation"),
    ("14-email-messaging", "Email and messaging", "flows, campaigns, SMS, deliverability, list growth, revenue by flow from orders"),
    ("15-customers-cx", "Customers and CX", "cohorts, repeat, LTV, support reasons, returns, chargebacks, reviews"),
    ("16-organic-content", "Organic and content", "calendar, posts and videos with results, creator seeding, community"),
    ("17-seo", "SEO", "rankings, pages, crawl health, links, content refresh, organic revenue from orders"),
    ("18-answer-engines", "Answer engines", "how AI assistants describe and recommend the brand, facts page, corrections"),
    ("19-supply-inventory", "Supply and inventory", "stock cover, reorder points, landed cost, suppliers, carriers, failed deliveries"),
    ("20-marketplaces", "Marketplaces and quick commerce", "Amazon, Walmart, Target Plus, TikTok Shop: listing health, Buy Box, reviews, settlements"),
    ("21-finance-cash", "Finance and cash", "P&L by channel, contribution margin, cash forecast, MER, payouts, sales tax"),
    ("22-measurement", "Measurement and data health", "metric contract with freshness, tracking audit, attribution reconciliation"),
    ("23-team-ops", "Team and ops", "queues, capacity, vendors and agencies, SOP coverage"),
    ("24-security", "Security", "weekly scan findings, bot traffic, fraud, access review, backups"),
    ("25-experiments", "Experiments and memory", "registry: running, reads due, results, learnings, priors"),
    ("26-reports", "Reviews and reports", "weekly business review, monthly report, agency portfolio"),
    ("27-wild-bets-pr", "Wild bets and PR", "bets pipeline with stage gates, PR, partnerships, events"),
]


def write_once(path, text):
    if os.path.exists(path):
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)
    return True


def screen_claude(slug, room, purpose):
    r = BYROOM[room]
    return f"""# Screen: {room}

Folder: `app/screens/{slug}/`. Purpose: {purpose}.

Read first, in this order, and nothing else unless a feature needs it:
1. `app/CLAUDE.md` (the app contract: server, data layer, UI kit, rules).
2. `app/contracts/` (metric contract, data sources, UI kit, cross-screen events).
3. This folder: `FEATURES.md` (the backlog and what is done), `screen.js`, `index.html`, `api.py` once they exist.

Spec pointers (read the section, not the whole file): room "{room}" in `agents/rooms/rooms.json`; agent {r['agent']} in `agents/catalogue.json` (filter by agent); workflows and skills for {r['agent']} in `agents/workflows/`. Copy nothing from them into this folder; link by id.

What this screen owns: its own `index.html`, `screen.js`, `screen.css` (optional), `api.py` (endpoints under `/api/{slug}/`), and `fixtures/` (dummy data this screen needs beyond the shared sample brand). It never imports another screen's JS. Anything two screens need lives in `app/contracts/` or `app/data/`.

Working rules for a session in this folder:
- One feature per commit. Update `FEATURES.md` status in the same commit.
- Numbers come from `app/data/` through `api.py`, computed in code. Missing shows as unavailable, never 0.
- Every insight is a rule in code with the sentence it produces. Every action button maps to a capability id and shows its autonomy (agent does, founder gate, human assist).
- US brand by default. Market-only fields (cash on delivery, return to origin) read null and are hidden unless the brand's market enables them.
- Keep this session small: do not read `agents/**` beyond the pointers above, do not read other screens.
"""


def screen_features(slug, room):
    r = BYROOM[room]
    L = [f"# {room}: features", "", "Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.", "",
         "## Round 0: skeleton", "", "| # | Feature | Status |", "|---|---|---|",
         "| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |",
         "| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |",
         "| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |",
         "", "## Candidates from the room spec (pick 10 per round)", "", "### Questions this screen should answer", ""]
    for j in r.get("jobs", []):
        L.append(f"- {j.get('question')}  ({', '.join(j.get('capabilities', []))})")
    L += ["", "### Metrics specified", ""]
    for m in r.get("metrics", []):
        L.append(f"- `{m.get('name')}`: {m.get('plain')}. {m.get('formula')}")
    L += ["", "### Insights specified (rules in code)", ""]
    for i in r.get("insights", []):
        L.append(f"- {i.get('name')}: {i.get('rule')} → \"{i.get('sentence')}\" (action {i.get('action_capability')})")
    L += ["", "### Visuals specified", ""]
    for v in r.get("visuals", []):
        L.append(f"- {v.get('name')} ({v.get('type')}): {v.get('shows')}")
    L += ["", "### Not in the usual tools", ""]
    for n in r.get("not_elsewhere", []):
        L.append(f"- {n.get('claim')}")
    L += ["", "### Data this screen needs", ""]
    for d in r.get("data_needs", []):
        L.append(f"- `{d.get('table')}`: {', '.join((d.get('fields') or [])[:10])} ({d.get('connector_or_script')})")
    L += ["", "## Rounds", "", "| Round | Features picked | Date | Notes |", "|---|---|---|---|", ""]
    return "\n".join(L)


if __name__ == "__main__":
    made = 0
    for slug, room, purpose in SCREENS:
        d = os.path.join(APP, "screens", slug)
        made += write_once(os.path.join(d, "CLAUDE.md"), screen_claude(slug, room, purpose))
        made += write_once(os.path.join(d, "FEATURES.md"), screen_features(slug, room))
        made += write_once(os.path.join(d, "fixtures", ".keep"), "")
    idx = ["# Screens", "", "| Folder | Room | Purpose |", "|---|---|---|"] + [f"| `{s}` | {r} | {p} |" for s, r, p in SCREENS]
    open(os.path.join(APP, "screens", "INDEX.md"), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    print("screens:", len(SCREENS), "files created:", made)
