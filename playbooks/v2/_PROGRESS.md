# Playbooks v2 build progress

Started 24 Sep 2026. Method in `TEMPLATE.md`. Source list per folder in `_source_manifest.json` (one row per source, status todo or done). Pass 1 runs one agent per source; pass 2 runs one merge agent per folder.

Pass 1 = mini playbook per source (Sonnet from 24 Sep). Pass 2 = folder playbook (Fable). Status: todo, running, done.

| Folder | Sources | Source words | Cards | Pass 1 | Mini playbook words | Pass 2 | Folder playbook words |
|---|---|---|---|---|---|---|---|
| /01-PRD-product-research | 10 | 79,296 | 170 | done | 41,313 | done | 22,765 |
| /02-AVT-avatars | 9 | 114,876 | 216 | done | 39,115 | done | 26,061 |
| /03-OFF-offers | 10 | 140,348 | 270 | done | 72,025 | done | 29,627 |
| /04-BRD-brand | 12 | 255,010 | 524 | done | 86,235 | done | 31,219 |
| /05-SET-store-setup | 11 | 241,346 | 432 | done | 79,049 | done | 23,519 |
| /06-MEA-measurement | 7 | 46,106 | 117 | done | 32,609 | done | 24,264 |
| /07-LPG-landing-pages | 26 | 190,737 | 400 | done | 140,426 | done | 35,221 |
| /08-SPD-speed | 9 | 89,794 | 226 | done | 33,838 | done | 29,052 |
| /09-CRO-testing | 7 | 78,699 | 177 | done | 39,217 | done | 31,718 |
| /10-MCR-paid-social-creative | 19 | 129,229 | 319 | done | 98,987 | done | 38,746 |
| /11-ADC-ad-copy-deployment | 9 | 271,689 | 402 | done | 79,699 | done | 26,854 |
| /12-GAD-google-ads | 10 | 205,137 | 362 | done | 80,897 | done | 31,564 |
| /13-ORG-organic-and-content | 10 | 76,393 | 149 | done | 49,309 | done | 31,742 |
| /14-EML-email-lifecycle | 13 | 327,983 | 578 | done | 96,790 | done | 29,857 |
| /15-SEO-search | 16 | 231,986 | 420 | done | 90,077 | done | 27,688 |
| /16-AEO-answer-and-generative-engines | 9 | 89,821 | 173 | done | 44,492 | done | 25,761 |
| /17-CXP-post-purchase | 7 | 51,360 | 112 | done | 35,875 | done | 26,308 |
| /18-COG-sourcing | 4 | 47,810 | 82 | done | 15,770 | done | 19,801 |
| /19-WLD-wild-bets | 3 | 22,413 | 96 | done | 19,706 | done | 28,251 |
| /20-FIN-finance-and-accounting | 6 | 132,584 | 203 | done | 42,154 | done | 30,565 |
| /21-OPS-team-and-management | 7 | 154,983 | 258 | done | 34,865 | done | 20,806 |
| /22-AMZ-amazon-marketplace | 4 | 173,534 | 284 | done | 38,070 | done | 19,570 |
| /23-SEC-bot-and-agent-security | 6 | 288,805 | 412 | done | 64,745 | done | 20,266 |
| /24-DEP-ad-deployment | 10 | 110,382 | 213 | done | 60,852 | done | 22,536 |
| /99-multi | 22 | 549,961 | 1016 | done | 162,751 | done | 34,920 |

Totals: 256 sources, 4,100,282 source words, 7,611 cards. Mini playbook words: 1,578,866. Folder playbooks done: 25 of 25, 688,681 words. Build finished 24 Sep 2026.

## Notes

- Three sources were too long for one pass 1 agent and were split into equal text parts, one agent per part, with a short index file under the source's own number: /23-SEC 01 Site Security (273k words, 5 parts), /22-AMZ 01 Amazon FBA 12 hour course (155k words, 3 parts), /99-multi 01 Scale an eCommerce Brand Profitably (124k words, 2 parts). The parts stay as the mini playbook; the folder merge reads them directly. No re-compression pass.
- /23-SEC 01 turned out to be a transcript of a university web security course (about 2019), not an ecommerce document. The folder's ecommerce fraud content comes from sources 02 to 06.
- /01-PRD sources 02 and 10 are different videos, not two cuts of one talk; the folder playbook keeps them separate.
- /99-multi 13 bundles two unrelated pieces (a Bloom Nutrition summary and a full Oodie founder podcast); the mini playbook flags both for routing.
- Fable merge tokens (subagent tokens reported per folder): about 7.8M for the 25 folders, about 310k per folder; the multi folder was the largest at 638k. SEO and operations were cut off by a rate limit before reporting usage and are estimated at 300k each.
- A rate limit on 24 Sep cut 5 agents off mid-run. The SEO and operations folder playbooks and both multi 01 parts had finished writing and were kept; a QA agent checked both playbooks (all sections, rules, procedures and card ids valid; 12 truncated card ids in SEO were expanded from cards.json); a check agent verified and extended the multi 01 part 2 tail slice; the security merge was relaunched.
- Two folder playbooks (10-MCR, 03-OFF) were briefly committed as partial drafts by a mid-write sweep and then overwritten by the finished file in a later commit. The committed versions are the finished ones.
- The /99-multi playbook carries a 166-row routing table mapping its domain findings to the folder that owns them, for a later overlay pass.
- 08-SPD was updated on 24 Sep 2026 from the first blind A/B test (`reviews/speed-test/`): P1 steps 12 and 13, R59 to R61, checklist rows, and a test learnings log in section 11b.
- Wave 2 (24 Sep 2026): every folder playbook received an ecommerce specificity pass (priority block 3.0, reworded rules, new store levers, Appendix A for demoted material). Ranking and per-folder reviews are in `_ECOM_RANKING.md` and `<folder>/ECOM_REVIEW.md`. Playbook word counts grew by 1,500 to 3,500 each; the pass 2 column above is the pre-wave-2 size.
- Not done yet: agent overlays (`overlays/<agent>.md`), brand overlays (`brands/<brand>/overlays/<folder>.md`), spot-checks beyond 08-SPD.
