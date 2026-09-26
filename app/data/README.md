# Data layer

`sample-brand/brand.json` is the only hand-written file. `generate.py` produces every table from it with a fixed seed, shaped like the connector exports listed in `contracts/data-sources.md`, and writes `sample-brand/tables.json` as the manifest. `tables.py` loads any table by name (`load_table("orders")`) and returns typed rows for JSON and CSV alike. Screens read tables through `server.py`, never files directly. Real brands fill the same tables from `app/connectors/` in read-only mode.

`sample-brand/README.md` lists every table, its row count, the connector it is shaped like, the headline numbers and the 4 planted stories. `python generate.py --check` confirms the files on disk match a fresh run.

The live decision log the server appends to is `app/data/decisions.json`. The generator never touches it; `sample-brand/decisions.json` holds 2 seed examples only.
