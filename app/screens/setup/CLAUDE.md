# setup: the onboarding flow

The entry point of the app (first row in `app/screens/INDEX.md`, first in the shell nav). Source: `PRODUCT-PLAN.md` section 5.1, `app/contracts/brand-brain.md` sections 5.1 and 7, `app/contracts/finance-inputs.md`.

Read `app/CLAUDE.md`, `app/contracts/` and this folder. Nothing else.

## The 5 steps

| Step | Reads | Writes |
|---|---|---|
| 1. Website | `app/brain/<brand>/BRAIN.md` sections table (mock crawl, no network) | `website` in `app/brain/<brand>/connections.json` |
| 2. Documents | `documents/manifest.json` | one manifest line (local mode: the file itself is not stored) |
| 3. Sources | `app/brain/sources.registry.json`, rooms from `questions.bank.json` | `choices[category]` = connect, skip or declined, in `connections.json` |
| 4. Brand numbers | `app/contracts/finance-inputs.md` fields and metrics | one row in `app/data/brands/<brand>/finance_inputs.json`; the open row before it gets `effective_to` the day before |
| 5. First audit | `keeper.gaps` and `keeper.ask` with connected and declined sources | answers become founder records through `store.Brain.put` (tier `approved` for claims and decisions) |

## Rules

- Mock mode only. Nothing connects, nothing is fetched, nothing leaves the machine.
- Not comfortable on a category declines every source in it, so the keeper asks plainly and never offers that category again.
- One source per category at most.
- Finance: no overlapping ranges. A new value must start after the newest row for the same field and key.
- Bombas is the demo brand. The page says facts are public and every number is simulated.

## Api

`api.py`, routes in its docstring. `?brand=` picks the brand (default `bombas`). `BRAIN_ROOT`, `DATA_ROOT`, `CONTRACTS` are module constants; tests point them at a temp copy. Tests: `tests/test_screen_setup.py`.

## Server note

`app/server.py` `SAFE_SLUG` accepts `setup` as the one folder without a number prefix. `app/web/shell.js` lists it under "Start here".
