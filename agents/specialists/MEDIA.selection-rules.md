# MEDIA wave 4: selection rules and notes

## How the agent picks a workflow

Match platform first, then channel or task, then store tags, then trigger. First
matching row wins; a more specific platform+channel row beats a cross-platform one.

| Signal | Platform | Channel/task | Tags | WF | Skill |
|---|---|---|---|---|---|
| monthly | meta |: | any | W01 | audit-meta |
| monthly | google |: | any | W18 | audit-google |
| tier change | meta | structure | any | W02 | meta-structure |
| concept approved | meta | concept ad set | any | W03 | meta-concept |
| daily | meta |: | any | W04 | read-results/meta, kill-scale/meta |
| Monday | meta+google |: | any | W05 | suggestion-filter |
| LIFE-C32 handoff | meta | retargeting | any | W06 | meta-retargeting |
| weekly | meta | dynamic ads | catalogue | W07 | meta-catalogue |
| pre-budget check | any |: | has stock | W08 | stock-check |
| sale in 3-4 wks | meta+google |: | any | W09 | peak-sale-ramp |
| market launch | meta+google |: | cross-border | W10 | cross-border-setup |
| quarterly | any |: | any | W11 | access-audit |
| ROAS/MER gap, post-recon | meta |: | any | W12 | incrementality-test |
| new/relaunch | tiktok | first launch | any | W13 | tiktok-launch |
| weekly | tiktok | ad group | any | W14 | kill-scale/tiktok |
| post 5-7 days old | tiktok | spark | has creators | W15 | tiktok-spark-loop |
| launch / SKU review | tiktok | shop, GMV Max | catalogue | W16 | tiktok-shop-gmvmax |
| weekly | tiktok | ladder | any | W17 | kill-scale/tiktok, pace-budget/tiktok |
| weekly | google | feed | catalogue | W19 | google-merchant-feed |
| new/gap found | google | architecture | any | W20 | google-architecture |
| weekly | google | shopping, search | catalogue | W21 | google-shopping, -search |
| weekly | google | PMax | catalogue | W22 | google-pmax |
| search/shop stable | google | YouTube, Demand Gen | high AOV, visual | W23 | google-youtube-demandgen |
| weekly | google | bidding | any | W24 | pace-budget/google, kill-scale/google |
| new app / weekly | affiliate |: | has program | W25 | affiliate-program |
| launch / quarterly | amazon, walmart, target (flipkart, IN) | sponsored ads | listed | W26 | marketplace-amazon-flipkart |
| push / new listing | instacart, doordash, gopuff (blinkit, zepto, instamart, IN) | retail media | listed | W27 | marketplace-quick-commerce |
| gates hit | new/unproven |: | saturated | W28 | channel-pilot |
| disapproval / daily | meta, google, tiktok |: | any | W29 | policy-appeals |
| thresholds set | meta, google, tiktok |: | any | W30 | rule-automation |

## Picking a sub-skill

Each step routes through the 4 shared parents (build-campaign, pace-budget,
read-results, kill-scale) or account-ops / partnerships, switching on
**platform** first, then **channel/task**, then **store type**, only where one
platform has several matching children. Never guess between two matches; the
skill satisfying more `select_by` keys wins.

## When nothing matches

The agent does not improvise. It drafts a one-page proposal: the job, the
trigger, the inputs, the output, and the closest existing skill, for a person
to review before it runs on a real account.

## Notes

LIFE-C32, CREA-C38 and PROD-C49 are owned by other agents. They appear in W06,
W15 and W27 because those workflows execute on that specialist's decision or
data; MEDIA never sets an existing-customer budget, issues a creator
authorization, or recomputes quick-commerce margin itself.

Every founder_gate capability (C06, C49, C50, C55, C62, C63, LIFE/CREA
handoffs) stops at shared/founder-question-round before spend, an appeal or a
rule goes live, even on a schedule.

Google and TikTok have no read connector, so every google-* and tiktok-*
build-campaign skill hands a human a checklist or brief. Once one exists, the
read half should move toward agent_does while writes stay gated, per
MEDIA.md's gaps section.
