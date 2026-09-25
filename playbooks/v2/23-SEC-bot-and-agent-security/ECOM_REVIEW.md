# Ecommerce specificity review: 23-SEC bot and agent security

Reviewed against `playbooks/v2/TEMPLATE.md`. Scope: PLAYBOOK.md section 3 (139 decision rules), plus sections 0, 2, 4, 6, 7, 9 for context. No files edited.

## 1. Score

**Score: 3/5.**

The top layer (sections 0, 2, 3B, 3C, 3G, 3I) is genuinely store-built: it names Shopify Payments, Flow, AVS, CVV, chargeback thresholds, card testing, checkout scripts, and per-store inputs like platform, gateway and processor. But 79% of the underlying cards come from a 2019 university web security course that itself has "no ecommerce fraud content at all," and it shows: most decision rules are cookie, CSRF, XSS, TLS and DNS mechanics with no store framing. The playbook is honest about this split (sections 0 and 12 flag it), which earns it a 3 and not lower, but a store operator reading section 3 top to bottom spends more time in generic appsec than in ecommerce fraud and bot content.

**Rule count by category (139 rules, section 3):**
- (a) Store-specific: 38 rules (27%). Mostly 3B (threat model), 3C (shared responsibility, PCI), 3G (payment controls, all 11), 3I (bot and agent management, 10 of 15), plus incident-response rules naming shipping addresses and payment routes.
- (b) Generic but correctly applied to a store: 34 rules (24%). The condition or example ties it to checkout, cart, staff roles or Shopify, though the principle is general web security.
- (c) Generic with no store framing: 67 rules (48%). Cookie attributes, TLS, CAA, DNS, postMessage, password hashing, injection fixes: correct, none store-specific. Concentrated in 3D, 3E, 3F, 3H, 3J.
- (d) Out of scope (B2B, SaaS, publisher, enterprise-only): 0 rules. Nothing is wrong for a store; the gap is framing, not relevance.

## 2. Prioritisation check

Rule 9 gives a 5-step merchant-side order (admin 2FA, fraud analysis automation, dynamic 3DS, AVS/CVV, organisational controls) but it is one sentence, has no store-type branching, and is not a standalone block an agent can load. No section gives a ranked list conditioned by store type (hero SKU vs catalogue, AOV, subscription, marketplace, luxury, India vs US). Draft below.

### 3.0 Ecommerce priority order (draft)

1. Admin 2FA and passkeys, every staff account, no exceptions. Cheapest, highest-leverage control; rule 9 ranks it first for hosted platforms. [82] [83] [P12]
2. Confirm PCI DSS scope and SAQ type with the acquirer in writing first. A wrong scope assumption undercuts every payment control after it. [30] [P2]
3. Keep card data out of every non-checkout channel (notes, email, chat, sheets). Zero cost, closes the most common human-error exposure. [29] [P2]
4. Wire order-risk fraud analysis to automation: auto-capture low, queue high, notify medium, human path on any cancel. The daily fraud-loss lever once PCI and 2FA are set. [74] [75] [P14]
5. Detect and respond to card-testing bursts. The leading edge of the whole CNP fraud chain; hits stores of any size, any day, not only at peak. [10] [76] [P15]
6. Review AVS, CVV and dynamic 3DS against the brand's own decline data before changing settings. Trades fraud loss for lost sales if wrong; needs steps 4 and 5's data first. Luxury or high-AOV stores should enable 3DS sooner, since each blocked fraud order is worth more. `[general practice]` [71] [72] [73] [P13]
7. Monitor the processor's real chargeback numbers, not the source's illustrative 0.9% and 1%. A hard operating ceiling; miss it and card acceptance can stop. [77] [P15]
8. Inventory every script on the checkout page for skimming risk. Every tag on the payment step is a security surface now, not just a marketing choice. [16] [133] [P22]
9. Least-privilege staff access, same-day offboarding. Agency and seasonal turnover is high in ecommerce; stale access compounds every other control. [86] [P17]
10. App and dependency hygiene, quarterly and after any checkout or payment app install. The largest attack surface specific to a hosted-platform store. [116] [P18]
11. Establish a bot and agent traffic baseline before setting any policy. Ranks higher for catalogue, drop-heavy or marketplace-heavy stores than a single-hero-SKU, low-traffic store, since bot cost scales with catalogue size and launch frequency. `[general practice]` [101] [104] [P16]
12. Backup and restore test with a ransomware-safe copy. Lowest frequency, worst if skipped; do after the fraud and access work above, not instead of it. [125] [P19]

The playbook gives almost no real store-type segmentation: only self-hosted vs Shopify, drops vs steady catalogue in rule 14, and EU/UK/California exposure in rule 130. Subscription vs one-off, mobile-first India vs US, and marketplace-heavy conditions are not in any source; every such condition above is marked `[general practice]`.

## 3. Rule rewrites (15, condition/sources/cards unchanged)

1. **Rule 1**: name the store cases: cart price and quantity, applied discount codes, referral credit, and role claims on account and admin endpoints are all re-checked server-side.
2. **Rule 17**: name the actual scripts at risk: review widgets, chat, retention popups and ad pixels on account and checkout pages, not just "a script."
3. **Rule 43**: the session carries the shopper's cart and saved address, so a stolen or reused cookie exposes checkout, not just a login state.
4. **Rule 50**: flag the store trap: a marketing email link that adds to cart, applies a discount, or removes a saved item must never be a bare GET.
5. **Rule 54**: name checkout, address-book and payment-method-update endpoints as the ones that must reject a foreign Origin outright.
6. **Rule 61/62**: name the store's own render points: product reviews, Q&A, wishlist names and vendor bios, the fields shoppers see rendered back to them.
7. **Rule 64**: name product search, filters and discount-code lookup as the store's own highest-traffic injection surfaces.
8. **Rule 88**: separate staff accounts (strict, MFA-backed) from guest and customer checkout accounts (frictionless, still breach-checked).
9. **Rule 91**: size the threshold against the store's own peak: a drop or flash sale spikes legitimate checkout attempts, so set the limit from that peak, not average traffic.
10. **Rule 92**: name guest checkout email lookup and loyalty account login as the two flows most likely to leak which emails are customers.
11. **Rule 93**: name the triggers: changing a shipping address, adding a payment method, or editing payout details for a seller or affiliate account.
12. **Rule 95**: name gift card balance checks and promo code fields as common brute-force targets, kept behind the rate limit, not on browsing.
13. **Rule 118**: name theme code and checkout-page apps specifically, since they run on the highest-value page in the store.
14. **Rule 121**: name fulfilment and support staff machines, since they handle live order and payment-route data daily.
15. **Rule 134**: tie it to the store's own retargeting and ad pixels, the most common source of unjustified fingerprinting on a storefront.

## 4. Missing store levers (up to 8)

1. **Return and refund fraud (wardrobing, serial returners).** Goes in 3B and 5.3. No source in this folder, `[general practice]`.
2. **Promo and discount code abuse** (scraping, stacking, leaked influencer codes). Goes in 3G near rule 76. Adjacent only: gift card validation failures appear as a bot signal [edbeaf87d1ad] in `05-ecommerce-security-threats-and-modern-best-practices.md`; discount codes are not covered. `[general practice]`.
3. **Counterfeit and lookalike storefronts, brand abuse.** Belongs in 3B. Source has it: card `[f7fc93724150]`, "Protect against counterfeit sites and brand abuse," in `06-ecommerce-security-importance-issues-and-protection.md`. It is in that source's mistake list and card index but never reached PLAYBOOK.md: a dropped card, not a missing source.
4. **Friendly fraud and chargeback representment** (evidence packet, dispute win rate). Extends rule 81 and deliverable 3. No source in this folder, `[general practice]`.
5. **Cash-on-delivery (COD) fraud and fake orders**, common for mobile-first India stores. Goes in 3B and 3G. No source in this folder, `[general practice]`.
6. **Subscription and recurring-billing fraud, and dunning.** Goes in 3G. Barely touched: subscriptions appear only as a trigger to re-run the four-pillars audit [a1aa08fcea08]. `[general practice]`.
7. **Loyalty and rewards account takeover, points draining.** Extends 3H and 3I. Lightly present: source 01p2's hotlinking rule covers a loyalty badge at a guessable URL, and source 05 mentions loyalty account passwords [aef2c2727587], but no detection or response procedure exists. Buried, not missing.
8. **Reseller and scalper bot detection**, distinct from the hoarding-to-abandon signal in rule 14. Goes in 3I near rule 114. No source in this folder, `[general practice]`.

## 5. Demotions to an appendix "General background"

- **Rules 35 to 42** (mixed content, HSTS ratchet, CAA, Certificate Transparency, HPKP, DoH): pure TLS and PKI mechanics, no store framing. About 550 words.
- **Rules 57 to 60** (postMessage targetOrigin, JSONP, CORS, Cache-Control): general web-app plumbing for a developer, not a store decision. About 350 words.
- **Historical case list in section 10's web-check block** (GitHub OAuth HEAD bypass, event-stream, Mirai, DigiNotar, Blizzard and Transmission rebinding, Great Cannon, the Japan `alert()` arrest, Heartbleed year dispute): background for citing externally, not a store rule. About 90 words.
- **CAPTCHA break-rate history and the Chrome dynamic-pinning removal fact in section 6**: correct trivia, no store decision attached. About 100 words.
- **Underground cybercrime specialization background** from `01-site-security-part1.md`: the source itself says it has no matching card and is scene-setting only.

## 6. Deliverables check (section 9)

Six of the 7 deliverables are things a store team would use: the fraud settings spec, the app inventory, the access matrix (ecommerce roles: fulfilment, content, marketing, agency), the incident runbook (skimming and ATO waves, not generic breach categories), and the quarterly calendar (names pre-peak Flow review). The threat model (deliverable 1) is weakest: it reads as a security-team document rather than something a merchandising or ops lead would open, even though P1 correctly weights it by drop calendar and EU/UK exposure.

Proposed changes: rename deliverable 1 to "Store threat model, weighted by peak calendar and region" to surface its existing store framing. Add an eighth deliverable, "Card testing and bot incident postmortem," pulling the after-action write-up out of P15 and P16 instead of folding it into the fraud settings spec.

## 7. Single highest-value change

The playbook's problem is not wrong content, it is weight: 48% of its decision rules are correct, well-sourced, generic web security with no ecommerce framing, inherited wholesale from a 2019 course that itself has zero ecommerce fraud content. The single change that would most raise its value over a generic security prompt is to publish the "3.0 Ecommerce priority order" block above as a real, load-bearing section, and use it to gate what an agent reads: for most store tasks, load 3B, 3C, 3G and 3I first, and pull the generic mechanics in 3D, 3E, 3F, 3H and 3J only when a specific gap (self-hosted transport, a custom login, in-house code) needs them. That reordering turns a 139-rule flat list, half of which reads the same for a bank or a blog, into a playbook that leads with what only a store operator needs.
