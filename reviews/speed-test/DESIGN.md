# Speed audit A/B test: playbook vs no playbook

Date: 24 Sep 2026. Brand: Gehna (gehnaindia.com, Shopify). Domain: 08-SPD-speed.

## Question
Does an agent with the folder playbook produce a better site speed audit and fix plan than an agent with a general prompt and the same tools?

## Arms
| | Agent A (control) | Agent B (playbook) |
|---|---|---|
| Model | Fable 5.1 | Fable 5.1 |
| Web access | yes (fetch, search, curl, headless Chromium) | same |
| Playbook | none | `playbooks/v2/08-SPD-speed/PLAYBOOK.md` |
| Backend data | none | Metabase read tools, `data/meta-gallery/brand.json` |
| Stages | 1 agent: audit plus top 10 fixes | 2 agents: audit, then execution plan; combined report |
| Output | `agent-a-report.md` | `agent-b-audit.md`, `agent-b-tasks.md`, `agent-b-report.md` |

Both arms get the same brand brief (homepage URL, Shopify store, Indian fine jewellery, mobile-heavy audience) and the same deliverable spec: an audit a non-technical owner can read, the top 10 fixes ranked by impact, an estimate of the gain per fix with the basis for the estimate, and exactly how to do each fix.

## Measurement instrument
Google PageSpeed Insights free quota was exhausted on the day, so both arms measure with the same local instrument: headless Chromium via Playwright (navigation timing, resource count and bytes, LCP element, layout shift entries, long tasks) plus curl for TTFB and headers. Both arms are told this.

## Judging
Reports are copied to `blind/report-1.md` and `blind/report-2.md` in random order with arm names removed. Two judge agents score each report 1 to 5 on: accuracy of findings, depth, actionability (could a Shopify store owner or developer execute it), ecommerce and Shopify specificity, credibility of the impact estimates, readability, and errors or invented claims. Each judge names the better report and why. The orchestrator (this session) adds its own read, then reveals the mapping.

## Rules
No paid calls. Meta read only. No credentials. Public web research is kept separate from private Metabase data in the reports. Competitor content is not copied.

## Changes for the next run (from the 24 Sep result)
- Give the control arm the same 2-stage pipeline (audit, then plan) so the test isolates the playbook, not the pipeline.
- Add a third judge and randomise reading order across all 3; 2 judges split 1 point each way.
- Have judges verify 2 or 3 factual claims against the raw evidence instead of judging from the report text alone.
- Run the next round on a judgement-heavy domain (03-OFF or 11-ADC), where decision rules should matter more than measurement.
- Playbook updated: 08-SPD P1 steps 12 and 13, R59 to R61, checklist rows, section 11b log.
