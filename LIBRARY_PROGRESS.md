# Ecommerce intelligence progress

Snapshot: 2026-09-22T18:28:05.820951+00:00

Generated cards: **7611**.
Conservatively estimated settled API usage: **$18.470**. Pending/uncertain reservations: **$2.715**.
These are pipeline ledger estimates, not provider invoices. The overall USD 200 ceiling includes earlier work; the current working stop remains USD 160.

| Folder | Sections completed | Cards |
|---|---:|---:|
| 09-CRO-testing | 14/14 | 177 |
| 01-PRD-product-research | 16/16 | 170 |
| 02-AVT-avatars | 17/17 | 216 |
| 03-OFF-offers | 23/23 | 270 |
| 04-BRD-brand | 39/39 | 524 |
| 05-SET-store-setup | 34/34 | 432 |
| 06-MEA-measurement | 11/11 | 117 |
| 07-LPG-landing-pages | 34/34 | 400 |
| 08-SPD-speed | 16/16 | 226 |
| 10-MCR-paid-social-creative | 27/27 | 319 |
| 11-ADC-ad-copy-deployment | 70/70 | 756 |
| 12-GAD-google-ads | 17/17 | 221 |
| 13-ORG-organic-and-content | 13/13 | 149 |
| 14-EML-email-lifecycle | 43/43 | 578 |
| 15-SEO-search | 37/37 | 420 |
| 16-AEO-answer-and-generative-engines | 19/19 | 173 |
| 17-CXP-post-purchase | 9/9 | 112 |
| 18-COG-sourcing | 8/8 | 82 |
| 19-WLD-wild-bets | 4/4 | 96 |
| 20-FIN-finance-and-accounting | 20/20 | 203 |
| 21-OPS-team-and-management | 25/25 | 258 |
| 22-AMZ-amazon-marketplace | 20/20 | 284 |
| 23-SEC-bot-and-agent-security | 33/33 | 412 |
| 99-multi | 81/81 | 1016 |

## What is available

- Text-only cards in `data/library-v3/cards.json` and per-folder Markdown in `data/library-v3/markdown/`.
- Keyword plus semantic search, with complete cards packed to a measured token budget.
- Folder completion is listed above. The next stage after ingestion is task-based retrieval and agent integration.
- Three same-model CRO comparisons completed. They demonstrate retrieval and context use, not proven superiority or business uplift.
- Sample corrections clarified lead-generation applicability and source-specific testing thresholds. The revised low-traffic answer retained the heuristic caveat.
- Hosting, a production agent service and GitHub push are not completed.

Use `python scripts/library_status.py` to refresh this report. A folder is fully searchable semantically after its vector refresh finishes.
