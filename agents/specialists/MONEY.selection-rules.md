# MONEY wave 4: selection rules and notes

## How a workflow is picked

MONEY matches a trigger (schedule, event, or founder question) to one workflow below. A trigger naming a source (gateway, marketplace, ad invoices, chargebacks, or a COD courier for India-selling brands) or a surface (GA4, Meta CAPI, Google Ads, server events) routes into that workflow's matching `reconcile` or `audit-tracking` child skill.

| Trigger or bottleneck | Source / surface | Workflow | Skill(s) |
|---|---|---|---|
| Month close, settlement ends | gateway/marketplace/ad-invoices/chargebacks/cod-courier (India) | W01 | reconcile/*, pnl-close-checklist |
| Weekly margin, quarterly loyalty redesign | sku/basket/channel/customer | W02 | margin, margin/customer-profitability |
| New SKU, cost change, promo proposed | - | W03 | pricing-waterfall |
| Weekly cash plan, financing question | - | W04 | cash-forecast-13wk, financing-comparison |
| Raise, loan, insurance renewal, loss | - | W05 | capital-and-investor-reporting, insurance-cover-and-claims |
| Weekly CAC/LTV/forecast, monthly budget | cac-ltv/revenue-forecast/opex/subscription | W06 | growth-economics-stack, mmm-stack-evaluate |
| Monthly, before filing, new SKU/B2B | tax-code/nexus/filing-prep/facilitator-credit/credit-memo (India: hsn/eway-bill) | W07 | gst-tax-compliance |
| Bill in, invoice due, payroll, card cycle | payable/receivable/payroll/expense | W08 | cash-ops-cycle |
| Payout cycle, tier change, creator deal | affiliate/creator | W09 | partner-commercial-terms |
| Monthly, new account, site change | ga4/meta-capi/google-ads/server-events | W10 | audit-tracking/* |
| Monthly, ROAS vs MER disagree | order-count/model-gap/holdout | W11 | utm-link-hygiene, attribution-model-reconcile, mmm-stack-evaluate |
| Building attribution, new channel | - | W12 | attribution-survey-build |
| Daily scoreboard, monthly maintenance | - | W13 | dashboard-build |
| Quarterly review, hire trigger fires | trigger/scorecard/interview/offer | W14 | hiring-scorecard-to-offer |
| New hire, repeated procedure, exit | sop/handbook/offboarding | W15 | sop-and-hr-docs |
| Quarterly | rhythm/facilitation | W16 | mgmt-rhythm-and-facilitation |
| Monthly, RFP warranted | - | W17 | vendor-rfp-evaluation |
| Quarterly, contract, renewal, new engagement | tooling/renewal/risk/contract/freelancer | W18 | vendor-saas-contract-governance |
| Monthly CS review, CCPA/CPRA request in (DPDP for India) | capacity-plan/data-subject-request | W19 | cs-capacity-and-dpdp |
| Weekly | - | W20 | security-scan-weekly |
| Monthly | - | W21 | security-audit-monthly |
| Quarterly | access/privacy/email-auth/credentials/training | W22 | security-audit-quarterly |
| Annually, payment-flow change | - | W23 | pci-saq-scope |
| Continuous, reviewed daily | - | W24 | account-takeover-correlate |

(Workflow ids are MONEY-W01 to MONEY-W24; skill ids all sit under `money/`.)

Store tags narrow steps, not the workflow choice: india_mobile or GST-registered always runs W07's e-way bill and HSN steps (these read null for a US-only brand, which runs W07's Avalara/TaxJar nexus and filing steps instead); subscription always adds W06's subscription-economics module; marketplace-heavy always runs the marketplace child of reconcile in W01, even with no chargebacks or, for an India-selling brand, no COD that week.

## When nothing matches

MONEY never improvises a fix or a number outside these 24 workflows. It drafts a workflow proposal instead: a name, the capability it covers, a first-pass step list, and the inputs it needs, then routes it to a person for review before running it once. It never invents a script, a metric definition, or a security control on the spot.

## Method notes

Capabilities came from `MONEY.caps2.txt`, 76 ids across finance, measurement, ops and security, including several tagged under other agent codes (MEDIA, LIFE, PROD) that this wave's routing placed with MONEY. All 76 appear in exactly one workflow, none dropped or duplicated. Workflows group by job, not by capability count: the month-end close (W01) carries 8 capabilities because a bookkeeper closes reconciliation, disputes and fixed assets in one sitting; hiring, PCI scope and account-takeover correlation stayed one capability each since splitting them would not reflect a separate real task.

Both required nested families are built: `money/reconcile` splits by source (gateway, marketplace, ad-platform-invoices, chargebacks, and cod-courier as the India option) and `money/audit-tracking` splits by surface (GA4, Meta pixel and CAPI, Google Ads, server events), each dispatching on a `select_by` switch instead of five copies. Ten shared skills are referenced by id from workflow steps and were never re-authored here, per the brief.

One judgment call for Kevin: MEDIA-C51 (affiliate commissions) and MEDIA-C56 (MMM stack evaluation) sit with MONEY here because the decision they drive is margin and cost, not creative or targeting. If the Media buyer specialist also claims them, that overlap needs one owner set in the catalogue review.
