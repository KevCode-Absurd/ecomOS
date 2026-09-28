# Data layer

Two generators live here.

**v2, `generate.py` (from S2.3, 28 Sep 2026).** Takes a brand folder: reads `app/brain/<brand>/assumptions.json` and nothing else from the brain, and writes `brands/<brand>/`: `data.sqlite` with every row-level table (git-ignored, rebuilt from the seed), `aggregates/*.json` (daily, monthly, channel, product, cohort, wholesale and calibration rollups, committed), `assumptions.json` (the brain fields used), `manifest.json` (per field: value, brain or fallback, rule; plus every placeholder rate), `tables.json` and `README.md` (every table, rows, the connector it is shaped like, how the tables tie together).

    python3 app/data/generate.py --brand bombas                    scale 1.0, the public revenue band (about 11 million orders)
    python3 app/data/generate.py --brand bombas --scale 0.1        fast dev build
    python3 app/data/generate.py --brand bombas --as-of 2026-09-27 fixed window end (default: yesterday, America/New_York)

24 months of days ending on the last full day. Deterministic from seed, scale, as_of and the assumptions file. Orders are the one truth: sessions, Meta, Google, Klaviyo, payouts, returns, tickets and reviews are all derived from orders, with deliberate attribution overlap. Needs numpy. Tests: `python3 -m unittest tests.test_generate_v2`.

**v1, `generate_v1.py` (Phase A, Tallgrass Goods).** Reads `sample-brand/brand.json` and writes `sample-brand/` as JSON and CSV plus `tables.json`. `server.py`, `metrics.py` and `tests/test_app_metrics.py` still read `sample-brand/` until the server is pointed at a v2 brand folder. `python3 app/data/generate_v1.py --check` confirms the files on disk match a fresh run. Standard library only.

`tables.py` loads any v1 table by name (`load_table("orders")`). The live decision log the server appends to is `app/data/decisions.json`; neither generator touches it.
