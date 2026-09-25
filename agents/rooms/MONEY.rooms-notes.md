# MONEY rooms: what they show that common tools do not

Four rooms, from the MONEY capability catalogue (79 capabilities, each mapped to an action): Finance and cash, Measurement and data health, Team and ops, Security. Each follows the Meta gallery pattern: metrics with a formula and freshness rule, rule-based insights with a plain sentence, one visual per key question, an action next to every card.

## What is not shown elsewhere

**Finance and cash.** Triple Whale computes SKU-level margin on its Advanced tier but sends OPEX and a full P&L back to a spreadsheet; Shopify's native reports show revenue and cost, not contribution margin or a cash forecast. This room puts the P&L ladder (CM1 to CM3 to net profit), a 13-week cash forecast, a promo break-even gate, and live financing simulation against that forecast in one place. Payout tracking exists in A2X and Link My Books (COD tracking in CODReconcile and Shiplystic, for India-selling brands); missing is a drafted, SLA-cited escalation email per source once a remittance is overdue.

**Measurement and data health.** GA4 audit tools and attribution tools (Triple Whale's Moby MMM, Northbeam) each do their own piece, but none write one metric contract with a single formula, owner and freshness stamp, and none catch two dashboards defining a metric differently (one platform's own MER is spend÷revenue, the opposite of the usual convention). This room adds a daily pass/warn/fail trust check before anyone reads yesterday's numbers, and reconciles order counts, bot spikes and attribution gaps together.

**Team and ops.** Hiring triggers, SOP coverage, vendor SLA scoring and SaaS renewal live in memory or a spreadsheet today. No ATS watches the metric that should open a search; no spend tool drafts the renegotiation email.

**Security.** Scanners, Cloudflare's bot dashboard and backup providers each report their own signal. None age a finding against a fix window with an owner, prove a backup restores, or correlate a login anomaly across Shopify admin, ad accounts, the ESP and the payment processor at once.

## Hardest data to get

Landed cost per SKU with a backup document per line (supplier and freight invoices, not just Shopify). A metric contract and UTM convention, since both need a decision, not a pull. Payout and deposit reports across gateway and marketplace sources (courier-level COD reports too, for an India-selling brand; access varies by courier). Vendor SLA text and invoice lines to check against it. Admin login geography and device logs across four platforms in comparable form. A vendor risk questionnaire and DPA history, which most brands have never tracked.
