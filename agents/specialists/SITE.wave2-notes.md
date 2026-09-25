# SITE wave 2 notes

## Sources used, by type

- Job descriptions / day-in-the-life: Shopify developer (ByRadiant, SAP BW), CRO manager (Vettio, BuiltIn), e-commerce manager (Shopify, Digital Waffle).
- Agency service menus / pricing: Shopify Plus agency cost (Chargeflow, LiquidLemon), CRO agency pricing (WebFX, We Are Tenet).
- SaaS / tool feature lists: page builders PageFly, GemPages, Replo, Shogun, Instant, Fudge (Fudge.ai comparison); on-site search Algolia, Searchspring, Klevu/Athos Commerce; accessibility UserWay, accessiBe (with the FTC action against accessiBe's overlay claims); visual regression Percy, Chromatic; uptime/transaction monitoring Pingdom, UptimeRobot; AI QA agents QA Wolf, mabl, Testim; Shopify SimGym (AI shopper simulation, Research Preview).
- Freelance marketplaces: Fiverr Shopify development category, Upwork vs. Fiverr skill breadth.
- AI agent products: Shopify's AI agents blog (SimGym, agentic storefronts), Wiz AI theme editing, agentic checkout direction.
- India-specific: RTO reduction plays (Growwwtech, Shipmozo, HillTeck), GST/COD/Shopify India setup (ByBTraction, Vellumarc).

## What wave 1 missed most

Wave 1's 60 capabilities cover the full setup-to-CRO lifecycle deeply but read as if the site is built once and then optimized. What the job-description and tool research surfaces is the ongoing engineering discipline around that: git-based theme version control and CI (most shops still duplicate themes in admin), custom API integrations and webhooks to ERP/WMS/3PL, and continuous automated regression testing with self-healing and video replay, which is now a mature product category (QA Wolf, mabl) wave 1 did not touch. Real-time uptime and transaction monitoring with alerting is also missing; wave 1's hygiene item is a scheduled sweep, not an always-on watch. The single biggest category gap is checkout payment methods and address validation: nothing in wave 1 set up Shop Pay, PayPal, Apple Pay, BNPL or USPS address validation, or measured failed deliveries and chargebacks. Where the brand sells COD in India, the same gap includes return-to-origin (RTO), market option, reads null for US, one of the largest margin leaks for COD-heavy Indian stores, and the checkout-side levers (PIN serviceability, OTP, COD fee, WhatsApp confirmation, branded tracking) are genuinely site-side work there too. Smaller misses: platform release-note tracking (Shopify Editions twice a year), a design-token system to stop page-builder pages drifting from the native theme, and a staging environment distinct from a CI staging theme.

## What is possible but not sold yet

Four records mark real gaps no vendor currently fills at this granularity: sequencing PDP images from the brand's own zoom and click-map data instead of a generic A/B guess; capping an exit-intent or cart-abandonment discount in real time to a margin floor computed from the brand's own landed cost, so the number flexes by cart instead of being one flat guess; an on-site visual search matched only against the brand's own real product photos (never a competitor's or a generated redraw); and watching a competitor's public price to keep an on-site anchor-price comparison claim honest and current rather than a stale one-time write. Agentic checkout (a third-party AI assistant completing a purchase on a shopper's behalf) is marked web_only rather than possible, since Shopify's own direction and OpenAI-style instant checkout already point at it, even though almost no store has tested it yet.
