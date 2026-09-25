# Ecommerce review: 99-multi playbook

Reviewed: PLAYBOOK.md (34,920 words, 22 sources, 1,016 cards) against TEMPLATE.md format rules.

## 1. Ecommerce specificity score: 4 out of 5

This playbook is built almost entirely from store metrics: true gross margin after fulfillment cost, MER and AMER split by new versus returning customer, LTGP to CAC bands by category, and a Black Friday pacing model with real numbers. The only borrowed content is section 3.E (Cialdini's persuasion mechanisms), and it is labeled as adapted and given store applications in every rule, so it earns its place. The score is not a 5 because 7 rules in 3.G (PE mechanics, secondary sales, treasury allocation, equity instrument grants) read like general finance advice for any private company, not a store, and the playbook has no single ranked list that tells the agent what to fix first for a given store.

Section 3 decision rules by class (112 rules total, A1 to I5):

| Class | Count | Share |
|---|---|---|
| (a) store-specific | 82 | 73% |
| (b) generic, correctly applied to a store | 23 | 21% |
| (c) generic, no store framing | 0 | 0% |
| (d) out of scope for a store | 7 | 6% |

(b) is mostly section 3.E (all 10 persuasion rules, since the source itself has no ecommerce content) plus a handful of general business principles (one bottleneck at a time, product beats marketing, hire finance early) that carry ecommerce examples. (d) is entirely in 3.G: G6 (LBO mechanics), G7 (secondary sale), G8 (sell-side process), G10 (personal exit-timing opinion), G11 (founder presence in buyer meetings), G14 (treasury allocation to Bitcoin), G15 (equity-grant instruments). These apply the same way to a SaaS company or a law firm and do not change based on the brand being a store.

## 2. Prioritization check: no priority block exists. Draft below.

The playbook has a task-to-section load table (section 0) and 4 revenue-stage bands (3.C), but nothing ranks levers against each other for a given store type. Section 7's 20 conflicts are the best source for conditions by store type, so the draft below points to them.

**3.0 Ecommerce priority order**

1. Data integrity gate: fix tracking and exclusions before any other read. Always first, any store type. -> A1, B2
2. True gross margin per SKU, COGS tagged. Every other number is wrong without it. -> A4, A5
3. CAC against first-purchase GP, then LTGP:CAC in the category window. The window itself depends on store type: near-zero for furniture and one-off considered purchases, 180 to 365 days for subscription and consumables. -> A6, A8, A9, 7.12
4. Brand archetype and 3-layer read (ads, funnel, backend) to name the one constraint. -> B4, B7
5. Payback period and cash conversion cycle. Binds harder for high-AOV, inventory-heavy or considered-purchase stores than for low-AOV consumables. -> A10, A12, A13
6. Next-dollar channel allocation. For marketplace-heavy stores this weighs retail and Amazon sequencing higher; for DTC-only it weighs Meta and Google mix higher. -> D1, D4, D7
7. Creative volume as the real spend ceiling for media-led stores. A single-hero-SKU store hits its angle ceiling faster than a catalogue store that can rotate SKUs. -> B9, B10, D12
8. Offer architecture: hero-SKU gating versus bundles. Gating fits a single coveted hero SKU; bundles and AOV thresholds fit a catalogue. -> 7.7
9. Retention timing: build flows and a subscription option from day one for consumables; run a dedicated retention phase after acquisition is proven for one-off or considered purchases. -> C6, 7.12
10. Persuasion honesty gate on any new offer or page: luxury and considered-purchase stores default to no discount or urgency language; mass-market impulse stores can use real scarcity. -> 3.E, 7.9
11. Seasonal peak plan. Binding for any store with a Q4-weighted calendar; less binding for flat-demand subscription stores. -> 3.F
12. Local payment method and checkout friction for a mobile-first, non-US market. `[general practice]`, this folder has no source on it; see missing lever 3 below.

## 3. Rule rewrites (up to 15)

Condition, sources and card ids unchanged in every case below; only the rule statement is tightened to name what the agent does on a store.

- **E1**: "On every small on-page ask (email capture, a size or fit question), show the real reason next to it. Never fake the reason."
- **E2**: "Give a real free sample, guide or gift-with-purchase before asking for the order or the email. Never dress up a lowball discount as a gift."
- **E3**: "Set the welcome discount as a first-purchase incentive only, not a recurring reflex, and disclose subscription terms plainly so the value holds once the discount ends."
- **E4**: "Show proof from a similar customer (same body type, same use case) on the ambiguous steps of the funnel, not a generic count. Every number must trace to a real order."
- **E5**: "Use real customers and creators who resemble the buyer in ads and on the PDP. Never use an actor or a staged persona as a customer."
- **E6**: "Only put a named, checkable, relevant credential near a claim on a PDP or ad. Drop titles the shopper cannot verify."
- **E7**: "Only show a stock count, deadline or restock message that is true right now. Kill any countdown that resets or any '3 left' not backed by inventory."
- **E8**: "Show the premium tier or item first on a pricing page or upsell so the rest looks fairly priced. Never fake a 'was' price to fake this effect."
- **B1**: "On a store, fix the one binding growth constraint (traffic, funnel or backend) before touching the other two."
- **B8**: "Before calling a store a product-market-fit failure, run real spend across several personas and angles for a meaningful window, and check price against the target before blaming the product."
- **B13**: "Judge a store's acquisition health on a weekly or monthly window. A same-day email send can flip blended ROAS without saying anything about the store's ad account."
- **G3**: "Bring in a CFO or fractional finance lead once the store passes about $1M in revenue, not the year before a sale."
- **G12**: "Name a backup for ads, fulfilment, finance and customer service so no single person's absence stops orders shipping or ads running."
- **G13**: "Kill a structurally dead product line or SKU fast to protect cash; do not confuse a temporarily slow SKU with a dead one."
- **I5**: "A strong product with average marketing can still sell on a store. The reverse rarely works. Follow the SKU the data picks, even if it raises COGS."

## 4. Missing store levers (up to 8)

1. **Marketplace and payment commission as its own true-gross-margin line.** Belongs in 4.1 step 1, next to shipping and pick-and-pack. Source: thin. Card cb72f5171b60 in `07-he-built-a-725-million-company-in-255-days.md` names "payment and marketplace fees" once, no depth.
2. **Reverse logistics cost (return shipping, restocking, inspection) as a lever, not just a refund-rate haircut.** Belongs in A2 and A5. Source: thin. `01-scale-an-ecommerce-brand-profitably-part1.md` gives fashion refund rates but no processing cost per return. `[general practice]` for the processing-cost part.
3. **Mobile-first and non-US checkout friction (regional wallets, cash on delivery, low-bandwidth PDP).** Belongs in a new rule under 3.D or the international part of C4. No source in this folder; grep for "India" and "COD" found only one line in `04-ecommerce-masterclass-build-scale-win.md` saying to skip India until multi-billion-dollar scale, with no operational detail. `[general practice]`
4. **Loyalty and membership program design and ROI**, beyond routing its landing page to warm traffic. Belongs in a new 3.D or 3.C rule. Source: thin. Card 7c106a91e81a in `17-alo-yoga-teardown-creative-offers-landers-acquisition.md` covers only page routing.
5. **Customer service cost per order inside the unit-economics model.** Belongs in 4.1 or the 6-lever cash model (A13). Source: thin. Card 2c4a21f43820 in `05-how-a-t-shirt-brand-outsmarted-the-industry.md` describes a service "wow budget" but not a cost-per-order or headcount lever.
6. **How the MER and AMER model changes when a large share of revenue is marketplace, not DTC.** Belongs in 3.A or 3.D. No source in this folder. `[general practice]`
7. **Warranty, damage and product-liability reserve as a cost or risk line.** Belongs near G-family or the 20-FIN handoff. No source in this folder. `[general practice]`
8. **Currency and FX exposure beyond the localized-checkout choice already covered.** Belongs in C4. Source: thin, `01-scale-an-ecommerce-brand-profitably-part2.md` and `04-ecommerce-masterclass-build-scale-win.md` mention currency only in the context of payment-processing rates, not hedging. `[general practice]`

## 5. Demotions to an appendix "General background"

- **E1 to E10 (3.E), the raw experiment narratives.** Keep each rule's store constraint in the main body; move the underlying study description (the guard-uniform compliance jump, Pallak's household energy study, the ABC Poseidon broadcast-rights auction, the doomsday-cult pattern, the bystander and lost-wallet studies) to the appendix. None of it is about a store. Roughly 700 to 900 words.
- **G6, G7, G8, G10, G11, G14, G15.** LBO mechanics, secondary-sale process, sell-side process design, a founder's personal exit-timing opinion, founder-presence-in-buyer-meetings tactics, treasury allocation to Bitcoin, and equity-grant instrument mechanics. These are general private-company finance and M&A content that would read the same for a non-store business. Roughly 800 to 900 words. Keep a one-line pointer to 20-FIN so the founder decision memo (4.8, 9.7) still knows this exists.

## 6. Deliverables check (section 9)

Section 9's outputs are things a store team or founder would actually use: a growth-model sheet with a new-customer profit contribution dashboard (9.1), a bottleneck memo naming one constraint and its owner folder (9.2), a channel mix plan with a next-dollar call (9.4), and a Black Friday plan with a pacing sheet and offer ladder (9.5) are all concrete and ready to run from. Two are weaker fits. 9.7, the founder decision memo, inherits the out-of-scope M&A content from 3.G; rename it "Capital and ownership memo" and strip the pure M&A-process steps (buyer count, banker selection) down to a pointer, since a store operator agent should flag the decision, not draft the deal process. 9.8, the routing list, is an internal bookkeeping artifact for the agent's own folder handoffs, not something a store team reads; label it as internal, not a deliverable, so it is not confused with the other 7.

## 7. The single highest-value change

Add the ranked "3.0 Ecommerce priority order" drafted above. Right now the playbook is a strong, well-sourced reference: any one of its 112 rules could be produced by a generic prompt asked the right narrow question. A generic prompt cannot tell the agent, for this specific store (single hero SKU or catalogue, subscription or one-off, marketplace-heavy or DTC), which of those rules to reach for first, second and third. That ranked, conditioned order is the real edge this playbook should sell, and it is the one piece of sections 3 to 9 that does not yet exist.
