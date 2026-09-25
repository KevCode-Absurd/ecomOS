# Ecommerce specificity review: 08-SPD-speed

Reviewed against `playbooks/v2/TEMPLATE.md` and the full `PLAYBOOK.md` (1,387 lines, 104 rule numbers, 3 reused, so 107 rule entries in section 3).

## 1. Score

**Score: 4 out of 5.**

The playbook is built around store templates (home, collection, product, cart, checkout), Shopify and WooCommerce mechanics (theme.liquid, content_for_header, App embeds), and revenue framing (ad landing pages first, AOV-based business case, dynamic checkout buttons, peak-sale brownouts). Procedures and checklists in sections 4 and 5 are almost entirely written for a store, down to per-template tables for cart and checkout. What holds it at 4, not 5: over a third of the decision rules restate generic web performance mechanics (Core Web Vitals definitions, defer vs async, font-display swap, minification) without tying them to a store outcome, and no single place ranks levers by store type.

**Section 3 rule count by category (107 total rule entries):**

| Category | Count | Share |
|---|---|---|
| (a) Store-specific | 43 | 40% |
| (b) Generic, correctly applied to a store | 28 | 26% |
| (c) Generic, no store framing | 36 | 34% |
| (d) Out of scope for a store | 0 | 0% |

Method: each rule was classified by whether its condition, examples or wording name a store element (template, PDP, cart, checkout, app, AOV, catalog, peak sale) or would read the same in a rulebook for a SaaS site or a blog. Borderline calls (for example R62, a generic minification rule that names "checkout code" and "category pages" as examples) were counted as (b). No rule was B2B, enterprise-only or otherwise out of scope; this technical domain applies to any storefront, so 0% in (d) is expected.

The (c) rules cluster in 2 places: Group B (measurement method: averaging runs, reading lab vs field, tool cross-checks) and Group E (theme code and fonts: defer/async, font-display swap, critical CSS, minification). These are correct and necessary, but they would not change if you deleted every ecommerce reference from them.

## 2. Prioritization check

**No priority order block exists.** Section 0's table routes an agent by *task* (first audit, image audit, fonts) and section 3's groups run by *topic* (images, apps, fonts, CLS), not ranked by *what matters most for a store*. Nothing says, in one place, "do this before that," except sequencing buried in R2, R4 and conflict 7.4. There is also no branching by store type (single hero SKU vs catalogue, AOV, subscription vs one-off, marketplace-heavy, luxury, mobile-first India vs US); R3 prioritizes pages by traffic and R39/R22 branch on catalogue size, but nothing else.

Draft block:

### 3.0 Ecommerce priority order

1. Fix images on the ad landing page and top PDP first. Most sources call images the biggest weight, and R2 says find the one biggest cause first. R2, R3, R28, R31.
2. Fix LCP or CLS next on that same page, whichever the report shows as bigger. Either can dominate the score on the page a paid shopper lands on. R2, 7.4, P18 to P20.
3. Triage every app and script by revenue role. Third-party count is the strongest predictor of score in the cited 1,533-store dataset, and these scripts also power reviews, loyalty and upsells. R7, R44, R57.
4. Test and fix cart and checkout speed on its own. A delay here loses a shopper who already decided to buy. R25, R98, R99.
5. Retest mobile-first on the connection shoppers actually use. Weight this highest for India and other lower-bandwidth markets, lower for a fast, mostly-desktop US audience. R10, R19.
6. Decide above-the-fold widgets (wallet buttons, review stars, chat) by measured usage, not guesswork. R47, R56.
7. Clean up fonts and non-critical CSS. Safe, moderate gains, low risk to the purchase flow. R62 to R64, R70 to R73.
8. Caching, CDN and hosting last, only after 1 to 7; infrastructure work before content work hides nothing. R4, R91, 7.4. Pull peak-event capacity work forward only in the weeks before a sale. R94, P31.
9. Build the revenue business case once per audit, not once per fix. R9, P6.
10. [general practice] Single hero SKU store: skip catalogue-wide work, put the effort into the PDP. Large catalogue: automate compression on the top revenue SKUs first. R39.
11. [general practice] High-AOV, luxury or considered-purchase stores can carry heavier hero imagery if LCP still passes; low-AOV, high-volume stores should hold to the strict end of R31.
12. [general practice] Subscription stores: add account and login speed, uncovered here. Marketplace-heavy sellers with little on-site traffic: treat this whole playbook as lower priority.

## 3. Rule rewrites (15)

Condition, sources and card ids stay as written; only the wording changes, to name the store element each technique protects or serves.

1. **R15**: Average 3 runs on the pages that carry money (ad landing page, top PDP, checkout), not a random sample.
2. **R17**: Fix against lab data now; field data proves real shoppers, not a lab phone, saw the gain, in about 28 days.
3. **R18**: Report LCP, INP and CLS in every client deliverable, since these are the numbers that move both ranking and the funnel; drop FID and TTI.
4. **R19**: Run the slow-connection test on the page a paid ad sends shoppers to, at the connection speed common in the store's real markets, since this is where a hidden hero or a jump costs a sale.
5. **R26**: Change 1 setting at a time and re-test cart, add-to-cart and tracking before the next change; a broken checkout or a dropped pixel costs more than the speed gain.
6. **R33**: Compress product photos to just before a shopper would notice quality loss on the item they are about to buy, not to the smallest file the tool allows.
7. **R38**: Set width and height on every PDP, grid and cart-thumbnail image; these are the images that jump and shift a tap toward or away from Add to Cart.
8. **R46**: Add defer first, but test the exact buying step each script powers (reviews, upsells, chat) before and after, not just whether the page loads.
9. **R50**: Remove jQuery unless the cart drawer or checkout needs it; if kept, self-host it so a CDN outage cannot take down Add to Cart.
10. **R63**: Delay CSS for the cart drawer, size-chart modal and filter panel; never delay CSS a shopper sees before scrolling.
11. **R65**: On WooCommerce, unload cart, checkout and block styles from every page with no cart or checkout on it; these are the files most often left loading everywhere.
12. **R70**: Set font-display: swap on every font, especially price, CTA and headline weights, so a slow connection never hides the price or the Buy button text.
13. **R74**: Treat any CLS Google reports as real; on a store it usually means a tap landed wrong because a review badge, price or Add to Cart button moved after render.
14. **R83**: A high TBT on a product page means Add to Cart or the variant picker will feel unresponsive after tap; confirm the fix with a tap test, not just the score.
15. **R104**: Roll back the single change that broke something, not the whole batch, and keep a tested rollback path ready before touching anything during a peak sale window.

## 4. Missing store levers (up to 8)

| Lever | Where it would go | Source material in this folder |
|---|---|---|
| In-app browser rendering for ad traffic (Instagram, TikTok, Facebook browsers render differently from mobile Safari/Chrome, where most paid social clicks land) | New rule near R3, Group D | No source, `[general practice]` |
| Currency conversion and geolocation redirects on international stores (can block first paint) | Group D, near R43 | No source, `[general practice]` |
| Predictive or instant site-search latency (autocomplete lag) | New row in 5.8, near R84 | Mentioned once, only as a peak-event "brownout" risk: source 06 [88659194131b]. Buried, not covered as an everyday INP issue. |
| Account, login and order-history speed for subscription and repeat-purchase stores | Group N, after R99 | No source, `[general practice]` |
| Post-purchase upsell and thank-you page speed | Group L or N | No source, `[general practice]` |
| Shipping cost or delivery-date calculators on cart and checkout | Group N, near R98 | No source, `[general practice]` |
| Marketplace-heavy sellers, most revenue off-platform (changes whether this playbook is worth running) | Section 0 or 3.0 | No source, `[general practice]` |
| Luxury or considered-purchase trade-off: heavier, more numerous images are part of the sell, so strict compression can hurt perceived quality | Section 3.0, R29 to R31 | No source, `[general practice]` |

## 5. Demotions to an appendix "General background"

- The Core Web Vitals reference rows in section 6 ("Diagnostic metrics" and the FID/TTI/Speed Index rows): definitions and retirement history with no store framing, about 250 words. Keep only the bands section 5 points to.
- R18's explanation of which metrics are retired and why: correct, pure platform history, about 60 words.
- The tool-feature descriptions inside R21 (GTmetrix's Top Issues tab, WebPageTest's filmstrip, Pingdom's waterfall): about 80 words of tool documentation, not a store decision.
- Source 06's uncited statistics not tied to a store action ("marketers prioritizing speed: 3% top priority"): about 40 words, already flagged low-confidence.
- The AMP discussion (R6's aside, the AMP row in section 6, and section 10's web-check entry): dated history the playbook already flags for a web check, about 100 words.

Total: roughly 500 to 550 words movable without losing any actionable rule.

## 6. Deliverables check (section 9)

The 10 deliverables are things a store team would use: a speed audit keyed to templates, an image audit table, an app/script inventory with revenue roles, a developer brief, a host brief, a peak-readiness note, and client copy with the no-GPT, no-.env rule applied. Nothing reads like a generic "performance report." Only gap: "Business case" is a plain label for a conversion-times-AOV model; rename it "Speed revenue model." No replacements needed.

## 7. Single highest-value change

Add the "3.0 Ecommerce priority order" block drafted above. The playbook already has excellent store-level material: per-template procedures, an app-triage method tied to revenue role, a business-case formula. It lacks the one thing that turns deep technical knowledge into a ranked plan for a specific store: an ordered list of levers, conditioned on store type, readable in 30 seconds before opening any procedure. Without it, an agent infers priority from scattered hints in R2, R3, R4 and conflict 7.4; with it, the playbook goes from "everything you could check" to "what to fix this week for this store," the same gap the playbook's own 24 Sep test log (section 11b) found matters more than the diagnosis itself.
