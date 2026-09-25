# Data layer

`sample-brand/brand.json` is the only hand-written file. `generate.py` (round 0) produces every table from it with a fixed seed, shaped like the connector exports listed in `contracts/data-sources.md`. Screens read tables through `server.py`, never files directly. Real brands fill the same tables from `app/connectors/` in read-only mode.
