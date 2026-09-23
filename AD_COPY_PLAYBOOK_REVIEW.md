# Ad-copy comparison: observations and review instructions

Nine completed GPT-6 Luna responses, three briefs, three conditions, three variants each. This is an exploratory copy test, not conversion evidence or a statistically stable latency comparison.

| Condition | Mean input tokens | Mean output tokens, including reasoning | Mean generation seconds | Total estimated USD for three calls |
|---|---:|---:|---:|---:|
| Generic | 417.7 | 1167.7 | 13.70 | 0.001908125 |
| Playbook | 1676.7 | 1244.0 | 15.09 | 0.002494750 |
| Playbook + two cards | 2317.0 | 1141.7 | 15.38 | 0.002581375 |

Completed-generation estimate: **$0.00698425**, using conservative rates without cache discounts. The ledger rounds each settlement upward to microdollars, giving $0.006988. Four initial HTTP 400 formatting rejections retain $0.08 in conservative reservations; these are **not confirmed charges**. This round therefore has $0.086988 committed in its $1 ledger. Existing global and visual-test ledgers remain enforced. No reservations were cleared.

Official pricing reference consulted: https://developers.openai.com/api/docs/models/gpt-6-luna . The estimator uses $0.125/M input (conservative versus ordinary $0.10/M input) and $0.50/M output. Actual invoice reconciliation is not available here.

## What this run measures

Generic versus playbook measures the changed instruction package. Playbook versus playbook plus cards measures the addition of two manually selected full cards. All cells use the same saved public brand facts, task, output schema, length constraints, model and medium reasoning setting. There are no web or image tools. Website facts were not freshly verified. This does not test automatic source selection, website extraction, or agent execution.

Recorded retrieval timing is only an in-memory ID lookup after loading the catalog. It excludes human selection and cold start and must not be presented as end-to-end retrieval latency. Full exact prompts and outputs are preserved. The JSON-mode rejection was fixed identically across conditions and original rejected inputs remain saved as manifest.json; the executed inputs are manifest-corrected.json.

## Concrete observations from reading all outputs

- The generic value variants repeat essentially the same inclusions, price and policies with different openings. Distinct concept labels are not sufficient evidence of distinct concepts.
- The playbook and cards value variants divide attention more clearly among kit contents, installation support and purchase terms. Whether those are useful ads is for the owner to judge.
- Installation variants remain similar even with the playbook. We should test a concept-allocation plan before drafting, rather than simply instructing the writer to be diverse.
- Installation with cards includes “six childproofing items,” which risks implying a verified total piece count. The fact sheet should explicitly distinguish six product categories from item quantities; generated copy needs a corresponding check.
- Copy repeatedly enumerates the full kit. A better brief could choose the single supported detail relevant to each concept instead of requiring the writer to infer how much product identification is enough.
- Qualifying language appears in every standalone ad. Some qualification is appropriate for this product; improvement should focus on concise natural wording, not removal of material limitations.
- Many CTAs are low-energy formulations such as “review the kit” or “see if it suits your home.” Owner feedback should determine whether that matches the intended voice and offer.

These are editorial observations, not a numerical quality score. No condition is declared a winner. Do not promote the playbook based solely on completion or modest changes in wording.

## Owner review

Open AD_COPY_PLAYBOOK_COMPARISON.html. Options A/B/C are shuffled separately for each brief. Before revealing the key, record:

1. Preferred option, or tie/none.
2. Specific variant you would use.
3. What you would edit and why.
4. Any unsupported, unclear or off-brand wording.

Review installation, value and reassurance separately. Then reveal the condition key and costs. The next edit should target the observed issue and owner preference rather than add more cards by default. Original outputs and playbook version 1.1 remain unchanged for reproducibility.
