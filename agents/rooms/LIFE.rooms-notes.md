# LIFE rooms: what they show that common tools do not

Three rooms cover LIFE's 67 capabilities: **Email and messaging**, **Customers and CX**, **Offers and pricing**. Each follows the Meta gallery/speed lab pattern: metrics with a formula and unavailable rule, rule-based insights read as a sentence, buttons mapped to a capability and its catalogue autonomy.

## What is not elsewhere

**Email and messaging.** Revenue by flow is matched to real orders, not counted on send date inside a click-attribution window like Klaviyo, so a founder sees where the ESP's number and reality disagree. Consent and quiet hours are checked once across email, SMS and WhatsApp together. A pre-send check blocks a scarcity claim with no matching inventory or expiry record, and a back-in-stock alert needs a real restock event behind it. WhatsApp COD-to-prepaid conversion is its own metric, which no ESP or WhatsApp dashboard reports.

**Customers and CX.** Lifetime value is gross profit after returns, support and discount cost, not revenue like Shopify's LTV or Triple Whale's cohorts. COD RTO and failed-delivery (NDR) reschedules get their own funnel tied to courier events. Ticket reasons and CSAT (also in Gorgias alone) sit next to returns, RTO and true per-customer profitability together. A DPDP request register with a legal SLA clock, and an AI agent action log checked against its own limits, are gaps no off-the-shelf tool fills, since the data spans every system a brand uses.

**Offers and pricing.** The free shipping threshold recomputes from the brand's own live AOV, margin and shipping cost and flags stale, instead of manual entry into a calculator like Funnelytics. A margin waterfall runs before an offer launches with a founder red line that can block it. Discount dependency is one running score across every offer and channel, not a per-code count. Competitor and MAP tracking ties straight to the brand's margin data, and offer tests are checked for overlap before a founder trusts a result.

## Hardest data to get

WhatsApp Business/BSP feeds (Email), courier NDR/RTO feeds and support cost allocation (CX), competitor/MAP pulls plus product COGS and shipping cost (Offers) have no ecomOS connector yet; orders and refunds are fastest to connect first. DPDP requests and GST credit-note reconciliation sit outside any marketing tool and need a manual log. Until connected, rooms show only the job list and chart frames, per each founder_view_note.

Files: `LIFE.rooms.json` (3 rooms, schema-valid), this file.
