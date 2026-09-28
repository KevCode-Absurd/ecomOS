# Connectors

Read-only adapters, one per source, each with a `mock` mode that returns the generated tables and a `live` mode that calls the source. Built when a screen needs one and a real brand has granted access. The interface per connector: `pull(table, window) -> rows`, `status() -> freshness and errors`. No credentials in code; keys stay in `.env` outside this folder. External research sources (Reddit, Amazon reviews, review sites) follow the same shape, with fixtures in the screen's `fixtures/` folder until the live call exists.

Built: `apify.py` and `apify_adapters.py` (Amazon reviews and listings, Meta Ad Library, Reddit through Apify actors), spec in `app/contracts/connectors/apify.md`, fixtures in `fixtures/apify/`, status in `app/brain/STATUS.md` (S1.6).
