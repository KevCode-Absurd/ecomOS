# Playbooks v2 build progress

Started 24 Sep 2026. Method in `TEMPLATE.md`. Source list per folder in `_batch_plan.json`. Pass 1 runs one agent per source (256 runs); the batch grouping in that file is only a size guide. From 24 Sep, pass 1 runs on Sonnet (extraction into a fixed format); pass 2 merges stay on the stronger model.

Pass 1 = mini playbook per source. Pass 2 = folder playbook. Status: todo, running, done, reviewed.

| Folder | Sources | Words | Cards | Sources to run | Pass 1 | Pass 2 |
|---|---|---|---|---|---|---|
| /01-PRD-product-research | 10 | 79,296 | 170 | 2 | todo | todo |
| /02-AVT-avatars | 9 | 114,876 | 216 | 2 | todo | todo |
| /03-OFF-offers | 10 | 140,348 | 270 | 3 | todo | todo |
| /04-BRD-brand | 12 | 255,010 | 524 | 5 | todo | todo |
| /05-SET-store-setup | 11 | 241,346 | 432 | 5 | todo | todo |
| /06-MEA-measurement | 7 | 46,106 | 117 | 1 | todo | todo |
| /07-LPG-landing-pages | 26 | 190,737 | 400 | 4 | todo | todo |
| /08-SPD-speed | 9 | 89,794 | 226 | 2 | running | todo |
| /09-CRO-testing | 7 | 78,699 | 177 | 2 | running | todo |
| /10-MCR-paid-social-creative | 19 | 129,229 | 319 | 3 | todo | todo |
| /11-ADC-ad-copy-deployment | 9 | 271,689 | 402 | 4 | todo | todo |
| /12-GAD-google-ads | 10 | 205,137 | 362 | 4 | todo | todo |
| /13-ORG-organic-and-content | 10 | 76,393 | 149 | 2 | todo | todo |
| /14-EML-email-lifecycle | 13 | 327,983 | 578 | 5 | todo | todo |
| /15-SEO-search | 16 | 231,986 | 420 | 5 | todo | todo |
| /16-AEO-answer-and-generative-engines | 9 | 89,821 | 173 | 2 | todo | todo |
| /17-CXP-post-purchase | 7 | 51,360 | 112 | 1 | todo | todo |
| /18-COG-sourcing | 4 | 47,810 | 82 | 1 | todo | todo |
| /19-WLD-wild-bets | 3 | 22,413 | 96 | 1 | todo | todo |
| /20-FIN-finance-and-accounting | 6 | 132,584 | 203 | 3 | todo | todo |
| /21-OPS-team-and-management | 7 | 154,983 | 258 | 3 | todo | todo |
| /22-AMZ-amazon-marketplace | 4 | 173,534 | 284 | 2 | todo | todo |
| /23-SEC-bot-and-agent-security | 6 | 288,805 | 412 | 2 | todo | todo |
| /24-DEP-ad-deployment | 10 | 110,382 | 213 | 3 | todo | todo |
| /99-multi | 22 | 549,961 | 1016 | 9 | todo | todo |

Totals: 256 sources, 4,100,282 words, 7,611 cards, 76 pass 1 batches, 25 folder playbooks.

Pilot: 08-SPD and 09-CRO first, to prove the format before the fan-out.
