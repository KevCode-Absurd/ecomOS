# Ecommerce specificity review: 05-SET Store setup

Reviewer: automated pass 2 review, per `playbooks/v2/TEMPLATE.md`. Scope: `PLAYBOOK.md` (143 decision rules, 12 sections).

## 1. Score

Score: 4 out of 5.

Reasoning: Most of the playbook is built from store consequences: it ranks product types by fulfilment, ties shipping fields to undercharge risk, sets tax rules by nexus and market, and checks readiness with a real test order and an incognito walkthrough. It loses a point because about one rule in eight is generic hygiene stated the way a SaaS or WordPress tutorial would state it, and the playbook has no ranked view of what matters most, only a task-to-section lookup table.

Section 3 rule count by class (143 rules, R1 to R143):

| Class | Count | Share |
|---|---|---|
| (a) store-specific | 113 | 79% |
| (b) generic but correctly applied to a store | 11 | 8% |
| (c) generic with no store framing | 19 | 13% |
| (d) out of scope for a store | 0 | 0% |

No rule targets another business type, so (d) is zero. The (c) rules cluster in 4 places: domain and DNS mechanics (3.3), WordPress account cleanup (R13), 2FA and un-drilled backups (3.14), and AI-agent workflow hygiene (R131, R138, R139), which read the same for any coding task.

## 2. Prioritisation check

No, it does not rank levers by store type. Section 0's table sorts by task, not stakes, and nothing tells the agent a single-hero-SKU brand needs almost no collection logic while a catalogue brand does. Draft block below, built only from the playbook's own rules and section 7 conflicts.

### 3.0 Ecommerce priority order

1. Platform fit to the business model (R1-R4). A wrong choice cascades into every later rule; stakes are highest for a brand with an existing WordPress site or a hard checkout-control need.
2. Payments live and verified (R64-R72). No order can be taken until this clears, and verification runs hours to days, so start early. Matters most where card and COD both appear, as in mobile-first India (R66, R67).
3. Shipping rate coverage for every target country (R73-R85). One unrated country is unshippable. A single hero SKU can run one flat rate (R74); a mixed-weight catalogue needs class or table rates (R78, R79).
4. Tax setup with human sign-off (R86-R94). Wrong tax is a legal and refund cost found after launch. A marketplace-heavy or multi-country brand carries more of this, since each market in R104 adds its own tax questions.
5. Product data completeness and buyability (R32-R49). A single-hero-SKU brand should put more depth into that one listing (routed to 07-LPG); a catalogue brand needs the tagging and bulk-edit discipline in R44, R45 to not drown.
6. Legal pages and policy content (R56-R63). A thin shipping or return policy raises tickets and disputes (R59), and matters more for a considered or luxury purchase.
7. Checkout configuration and consent (R95-R103). Regional norms differ: mobile-first India leans on COD and a required phone (R66, R96); a US store leans on wallets (R97).
8. Collections and navigation (R50-R55). A catalogue store needs this; a single-hero-SKU brand needs almost none of it.
9. Lean, model-matched app stack (R108-R115). A subscription app only pays off for consumables (R112); over-installing slows every store type (R108).
10. Markets, currency and language (R104-R107). First-order only for a brand selling into several countries or marketplace-heavy; a single-market DTC brand can skip this at launch.
11. Staff roles, 2FA and backups (R116-R120). Necessary hygiene, lower urgency than the money-moving steps above it.
12. Launch gate verification (R123-R128). Always last, regardless of store type; it only confirms work already done. `[general practice]` for the ordering itself; each line's underlying rule is sourced as cited.

## 3. Rule rewrites

Condition, sources and card ids unchanged; only the rule statement is tightened to a store consequence.

1. **R5.** Sign up with an email the business will still control when it changes currency, deletes the store, or needs a critical account action years on, never a contractor's or agency's.
2. **R13.** Clean the fresh WordPress install before any product, collection or theme work, so a leftover plugin cannot break the store import or the storefront later.
3. **R14.** Write the site title and tagline to tell a shopper what they can buy and where you ship, not to rank higher; the first line of positioning, not an SEO field.
4. **R16.** Check domain availability against the product and category you sell, not just the brand name; the domain is the first trust signal a shopper sees before the cart.
5. **R18.** Do not remove the password until the custom domain resolves in a browser; a shopper who lands on a DNS error at launch does not come back.
6. **R19.** Do not take the store live on the default myshopify.com or a host's temporary URL; a shopper checking the address bar mid-checkout reads it as the store not being real.
7. **R21.** Confirm Force HTTPS is on before any product, price or checkout page goes live, since an unencrypted page collecting payment details is the one non-negotiable WooCommerce security step.
8. **R58.** Treat AI-drafted shipping, return, privacy and terms text as a first pass only; a human with legal knowledge signs off before it governs a real order, refund or chargeback.
9. **R61.** Never leave a borrowed page standing in for Terms and Conditions at the checkout agree-box; a shopper who agrees to the wrong terms has no enforceable return contract.
10. **R62.** Have a working contact channel live before the first order; a new store gets support emails from day one about sizing, shipping and order status.
11. **R64.** Turn on 2FA before activating Shopify Payments, since the account it protects can move the store's payout money, not just its content.
12. **R71.** Keep Stripe, PayPal and gateway keys out of files, prompts and chat; a leaked key can move real customer payments or take checkout down.
13. **R119.** Duplicate the theme before every change and confirm host backups exist, so a bad edit or failed launch step can be undone without the storefront going dark.
14. **R120.** Read every AI agent permission prompt during a theme or product build; a blind-approved write can publish an unfinished PDP or checkout change to real shoppers.
15. **R131.** Ask the agent for one storefront change per prompt and verify it live before the next; a bundled request that lands 3 of 4 changes can leave a broken PDP element live to shoppers.

## 4. Missing store levers

1. **Fraud and chargeback prevention** (order risk scoring, AVS or CVV checks, 3D Secure or SCA for EU cards). Goes in 3.8 and checklist 5.4. No source in this folder, `[general practice]`.
2. **Subscriptions and bundles as a deliberate lever**, not just an app pick. Goes in 3.5 or a new 3.13 rule tying the choice to store type. Source: 01, card `a517b976f014` names good and poor fits (supplements, food vs electronics), but it appears only once as an app pick in R112.
3. **Loyalty or rewards program decision**, tied to repeat rate. Goes in 3.13. Source: 01, cards `3f5560597133` and `13d14684d9ef` (Stamped.io for loyalty); buried as "evaluate each," with no rule on when it pays off.
4. **B2B or wholesale setup** (price list, minimum order quantity, net terms, a separate checkout). Goes in a new 3.11 rule. Source is thin: 01, card `d96aa7966303` only turns on a company field for B2B. Mostly `[general practice]`.
5. **Marketplace or multichannel listing** (Amazon, TikTok Shop, Google Shopping as your own channel). Goes in 3.13 next to R115. Source found is only WooCommerce's External or Affiliate product type (02, card `5c9382dfb092`), which links out to someone else's listing. Mostly `[general practice]`.
6. **Store migration or replatforming** (moving an existing catalogue, order history, accounts and SEO redirects to the new store). Goes in a new procedure before 4.1. No source in this folder, `[general practice]`.
7. **COD-specific risk controls** for high-COD markets (fake-order screening, phone verification, a prepaid discount nudge, return-to-origin tracking). Goes in 3.8 next to R67. Source: 02 enables COD with no risk framing. Mostly `[general practice]`.
8. **3PL vetting and cross-channel inventory sync** (fulfilment partner choice, split-shipment cost, stock sync so channels do not oversell each other). Goes in 3.9 next to R82. Source: 01, card `c7fe3611980d` verifies an integration end to end, but gives no vetting or sync rule. Mostly `[general practice]`.

## 5. Demotions

Move to an appendix "General background," being generic account, hosting or AI-agent hygiene rather than store-specific rules:

- The mechanical WordPress cleanup checklist in procedure 4.14 step 5 (deactivate plugins, trash pages, set permalinks). Keep R13's own rewrite above; move only the generic click list. About 150 words.
- **R16, R18, R19, R21** (domain naming taste, propagation waiting, avoiding a default URL, Force HTTPS). About 200 words. Keep R17 and R20; they carry store-specific consequences (checkout continuity, ESP DNS reuse).
- **R117, R118, R120** in 3.14 (2FA as a general control, WordPress role hygiene, reading AI permission prompts). About 200 words. Keep R116 (Orders access exposes sales figures) and R119 in the base layer with its store-framed rewrite above.
- **R138, R139** in 3.17 (distrusting the agent's own report, Sidekick vs Claude Code comparison). About 100 words. Keep R129, R130, R132-R137 and R131 with its store-framed rewrite above.

Total: roughly 650 words move to the appendix, none deleted.

## 6. Deliverables check

All 5 deliverables in section 9 are things a store team would actually open and use: a platform decision spec, a product import sheet matched to the platform's own importer columns, a combined shipping and tax matrix, a launch checklist with 4 named sign-offs, and an app stack list with a vetting record. None reads as a generic project document, so no replacement is needed. One naming suggestion: rename "9.1 Platform setup spec" to "9.1 Store build brief," matching the operator-facing tone of the other 4.

## 7. The single highest-value change

Add the "3.0 Ecommerce priority order" block drafted in section 2, right after section 0's task table. Today the playbook treats all 143 rules as equally weighted and sorts them only by which admin task loads which section; it never says which of those tasks actually decides whether the store sells anything, or how that changes for a single-hero-SKU brand versus a catalogue, a subscription brand versus a one-off, or mobile-first India versus the US. A generic prompt would happily spend an afternoon on collection filters for a single-SKU store, or skip tax nuance for a marketplace-heavy brand, because nothing says these levers carry different weight by store type. A ranked, conditioned priority block turns 143 correct but flat rules into a sequence an agent can run under time pressure, which a generic prompt cannot give it.
