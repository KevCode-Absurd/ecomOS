# 05-SET Store setup playbook

version: 2.0-draft  |  date: 2026-09-24  |  sources: 11  |  cards: 432  |  built from: sources/*.md

## 0. How to use this playbook

**Ecommerce first.** This playbook is for building and running an ecommerce store, not a generic website or app. Section 3.0 is the priority ranking: load it before the rule groups below, since it says which levers decide whether the store can sell anything at all. Store-type conditions (hero SKU vs catalogue, low vs high AOV, subscription vs one-off, marketplace-heavy, luxury or considered purchase, mobile-first India vs US) decide which rules in sections 3 and 4 apply and how much weight each carries; check the condition on a rule before running it.

**Who runs it.** The store setup and platform operations agent. It builds a new Shopify or WooCommerce store from an empty account to a launched, sellable storefront, and it runs the platform-side operations after launch: products, collections, policies, payments, shipping, taxes, checkout settings, markets, apps, staff access, and the launch gate.

**What the sources are.** All 11 mini playbooks are YouTube walkthroughs or Shopify's own content. 9 of 11 carry affiliate links (Hostinger hosting, Shopify trial deals, Elementor, Blocksy Pro, theme marketplaces, apps) or sell the presenter's own program (source 06 sells a white-label ecommerce course and tools; source 11 sells a product page framework). Source 04 is Shopify's own channel and favours Shopify-built tools. No source gives measured results. Every number in this playbook is a demo value or a presenter's claim unless marked otherwise. Section 12 rates each source.

**Which sections to load for which task.**

| Task | Load |
|---|---|
| Choose the platform for a new brand | 1, 3.1, 7 |
| Build a new store end to end | 2, 3 (all), 4 (your platform's track), 5.1, 9 |
| Add or import products | 3.5, 4.5 or 4.14, 5.2, 9.2 |
| Configure shipping or taxes | 3.9, 3.10, 4.8, 4.9 or 4.17, 4.18, 5.3, 9.3 |
| Turn payments live | 3.8, 4.7 or 4.16, 5.4 |
| Audit apps, staff and security | 3.13, 3.14, 5.5 |
| Launch or relaunch a store | 3.16, 4.12 or 4.20, 5.1, 5.6, 9.4 |
| AI-assisted theme or template work | 3.17, 4.13, 7.4, 7.5 |
| Sell into a new country | 3.12, 4.10, 3.9, 3.10 |

**What the agent must fetch before acting.**

- From the brand record: legal business name and registered address, product catalog with prices, costs, weights, package dimensions, SKUs, stock counts, target countries, return window, shipping promises, brand assets (logo, favicon, palette, fonts), support email, tax registrations. Section 2 lists all of it.
- From the data layer: nothing is required for a first build. For post-launch checks, the order feed and the analytics funnel (section 5.6).
- From the web: current plan names and prices, trial terms, app prices, gateway availability by country, tax rates and nexus rules, current admin UI labels. Section 10 lists every `[web check]`.

**ecomOS rules that override every source.**

1. No invented claims. Product copy, policy text and testimonials must match what the brand can prove. Pre-launch testimonials are allowed only if they are real and labelled (source 10).
2. Legal pages and tax settings need a human check before publish. The agent drafts, a human signs off. Every source that covers tax says the same.
3. Credentials never go in files, prompts, chat, or theme code. Stripe keys, PayPal secrets, store passwords, recovery codes and API tokens stay in the brand's secret store. When a procedure needs a key, the human pastes it in the platform UI.
4. Platform writes need explicit approval. Publishing a theme, removing the password, switching a gateway from test to live, changing tax settings, changing prices in bulk, or deleting zones are approval gates. Meta is read only under the repo rule; the sales channel connection in 3.15 is a Shopify-side step and still needs approval.
5. Tags: `[verify UI]` on every admin path, `[web check]` on every price, plan or tool claim, `[needs brand data]` on every brand-specific value.

## 1. Scope and outcomes

**Covers.** Platform choice between Shopify and WooCommerce. Account signup, plan choice, business identity. Domain purchase or connection and DNS. Theme selection, trial, duplication and the safe editing workflow. Product data: types, variants, options, media, inventory, SKUs, weights, pricing fields. Collections and navigation menus. Static pages and legal policies. Payments: Shopify Payments, Stripe, PayPal, offline methods, test mode to live, identity matching. Shipping: zones, rates, profiles, classes, free shipping thresholds, package weights, local delivery and pickup. Taxes: presence and nexus, inclusive vs exclusive display, classes and rates. Checkout settings, guest checkout, customer accounts, consent. Markets, currencies and languages. Apps and plugins: what to install, how to vet, the app embed step. Staff permissions, 2FA, collaborator access, backups and security basics. Handoff of analytics and pixel installation. Launch: test orders, pre-launch audit, password removal, first-week checks. AI-assisted setup with Shopify CLI and Claude Code, and custom Liquid sections.

**Does not cover, routed out.** The sources mix in a lot of neighbouring material. This playbook keeps a one-line pointer and routes the detail:

| Routed material | From sources | To folder |
|---|---|---|
| Homepage section order, hero banners, product page layout, cart drawer vs page, PDP objection research, Elementor and block editor page building, responsive passes, section color schemes, custom Liquid PDP sections beyond the mechanical click path | 01 (3.10 to 3.17), 02 (Elementor half), 03 (3.5, 3.27), 04 (chapters 3 and 4), 05 (D, E), 06 (page mirroring, PDP sections), 07 (C to G, N, O), 09 (B, C, D, G to K), 10 (E, F, G, L), 11 (3.4 to 3.8 page content) | 07-LPG |
| Welcome flows, abandoned cart, segmentation, OmniSend, Klaviyo, Shopify Messaging, email A/B tests | 01 (3.18.5), 03 (3.19 to 3.26), 04 (marketing hub), 10 (email app) | 14-EML |
| SEO fields beyond the baseline, blog strategy, taglines as ranking aids, Search Console | 01 (3.22), 02 (tagline), 03 (SEO plugin), 04 (3.14.7, launch SEO) | 15-SEO |
| Logo generation, palettes, fonts, brand boards, brand reference guides | 03 (3.5), 04 (3.4.4 to 3.4.7), 06 (branding pipeline), 10 (E) | 04-BRD |
| Product validation, competitor scoring, research tools | 06 (validator) | 01-PRD |
| Supplier scouting, dropship vs private label sequencing, packaging briefs | 06 (sourcing) | 18-COG |
| Pixel events, GA4 property setup, UTM rules, attribution models, conversion funnel reading | 04 (3.14, marketing hub), 01 (3.31) | 06-MEA |
| Security hardening beyond 2FA and roles: login limits, malware scans, WAF, backup restore drills | Gaps flagged in 02, 05, 07 | 23-SEC |
| Site speed, image compression, app weight | 01 (3.21), 04 (speed) | 08-SPD |
| Organic social launch posts, hashtag cadence | 04 (3.16.3) | 13-ORG |
| Discounts and coupons strategy (kept here only as configuration mechanics) | 01 (3.19), 02 (M), 07 (M) | 10-OFF or 14-EML as the offer owner decides |

**Business measures it moves.** A store that can take an order (checkout completes, payment captures, order reaches fulfilment). Zero unshippable destinations among target countries. Zero tax surprises after launch. No placeholder text on legal pages. Time from account creation to first real order. Post-launch support tickets about shipping and policies (a thin policy raises them, source 01).

## 2. Inputs the agent needs

| Input | From where | Required | Why |
|---|---|---|---|
| Platform decision or constraints (existing WordPress site, budget, technical staff) | user | required | Drives the whole track (3.1) |
| Owner email the business controls long term | user | required | Only the owner can change currency, delete the store, own the account (01, 04) |
| Legal business name, registered address, business number or EIN or VAT, owner ID details for payments | brand record | required | Feeds payments verification, tax defaults, shipping origin (04, 01) |
| Store name and myshopify handle preference | user | required | The handle is treated as permanent (04) |
| Target countries to sell to and ship to | brand record | required | Every one needs a shipping rate or it is unshippable (01, 02, 05) |
| Base currency and unit system | brand record | required | Cannot be changed without owner, prices do not auto convert (01, 03) |
| Product list: title, description, images (one ratio), type, vendor, tags, category, price, compare-at, cost, SKU or barcode, stock, weight, package dimensions, variants | brand record | required | Section 3.5, product import sheet (9.2) |
| Collection list and navigation structure | brand record or user | required | Collections type is permanent once saved on Shopify (01) |
| Warehouse or fulfilment locations, fulfilment app | brand record | required | Locations drive zones and inventory (01, 04) |
| Shipping rules: flat rates, free shipping threshold, transit times, package empty weights, carriers | brand record | required | Threshold is a margin decision (07, 10); package weight prevents undercharge (04) |
| Tax registrations and jurisdictions, inclusive or exclusive pricing rule, tax on shipping rule | brand record plus human tax advisor | required | All sources defer tax rules to a professional |
| Return window, who pays return shipping, restocking fee, final sale items | brand record | required | Return rules and policy (04, 01) |
| Support email and phone, contact page | brand record | required | Expect tickets from day one (01) |
| Brand assets: transparent PNG logo, square favicon, 4 to 5 hex colors, 1 to 2 library fonts | brand record via 04-BRD | required | Prepare before opening the theme editor (01) |
| Domain choice and registrar preference | user | required | Conflict 7.2 |
| Payment gateways available in the brand's country, PayPal Business account, Stripe account | brand record plus web | required | Availability varies by country (01, 10) |
| Plan tier, current prices, trial terms | web | required | All plan numbers are dated |
| App stack budget and existing tools (ESP, reviews, support) | brand record | optional | Avoid duplicate abandoned cart emails (01) |
| Staff list with roles | brand record | optional | Custom roles, orders access (01) |
| Existing Meta pixel, GA4 property | brand record via 06-MEA | optional | Handoff in 3.15 |
| Framework or spec for custom product templates | brand record | optional | AI template generation (11) |
| Inspiration screenshots for AI theme build | user or 07-LPG | optional | Claude Code brief (08) |
## 3. Decision rules

Each rule: the rule, when it applies, when it does not, supporting mini playbooks by number, conflicts, card ids. "Sources: 01, 04" means mini playbooks 01 and 04. Rules marked (opinion) rest on one presenter's judgment with no data.

### 3.0 Ecommerce priority order

Ranked by what decides whether the store can sell anything at all, not by which admin screen it lives on. Conditions by store type are given where they change the stakes.

1. **Platform fit to the business model (R1-R4).** A wrong choice cascades into every later rule; stakes are highest for a brand with an existing WordPress site or a hard checkout-control need.
2. **Payments live and verified (R64-R72).** No order can be taken until this clears, and verification runs hours to days, so start early. Matters most where card and COD both appear, as in mobile-first India (R66, R67).
3. **Shipping rate coverage for every target country (R73-R85).** One unrated country is unshippable. A single hero SKU can run one flat rate (R74); a mixed-weight catalogue needs class or table rates (R78, R79).
4. **Tax setup with human sign-off (R86-R94).** Wrong tax is a legal and refund cost found after launch. A marketplace-heavy or multi-country brand carries more of this, since each market in R104 adds its own tax questions.
5. **Product data completeness and buyability (R32-R49).** A single-hero-SKU brand should put more depth into that one listing (routed to 07-LPG); a catalogue brand needs the tagging and bulk-edit discipline in R44, R45 to not drown.
6. **Legal pages and policy content (R56-R63).** A thin shipping or return policy raises tickets and disputes (R59), and matters more for a considered or luxury purchase.
7. **Checkout configuration and consent (R95-R103).** Regional norms differ: mobile-first India leans on COD and a required phone (R66, R96); a US store leans on wallets (R97).
8. **Collections and navigation (R50-R55).** A catalogue store needs this; a single-hero-SKU brand needs almost none of it.
9. **Lean, model-matched app stack (R108-R115).** A subscription app only pays off for consumables (R112); over-installing slows every store type (R108).
10. **Markets, currency and language (R104-R107).** First-order only for a brand selling into several countries or marketplace-heavy; a single-market DTC brand can skip this at launch.
11. **Staff roles, 2FA and backups (R116-R120).** Necessary hygiene, lower urgency than the money-moving steps above it.
12. **Launch gate verification (R123-R128).** Always last, regardless of store type; it only confirms work already done. `[general practice]` for the ordering itself; each line's underlying rule is sourced as cited.

Load this block first; the groups below are the detail.

### 3.1 Platform choice: Shopify vs WooCommerce

**R1. Choose Shopify when the brand wants a hosted platform with payments, tax service, checkout and theme editor built in, and has no in-house WordPress skills.** Applies to new brands, solo founders, agencies building for clients who will self-manage. Does not apply when the brand already runs a WordPress site it must keep, or needs full control over every page element. Trade-offs the sources give: checkout customization is locked below Shopify Plus (01); plan fees plus a per-sale card rate of about 1.5% Basic, 1.3% Grow, 1.1% Advanced `[web check]` (01); currency per market needs Shopify Payments (01); apps inject code and slow the store (01, 04). Sources: 01, 04, 08, 09, 10. [8c79cd592233] [6f0629590ba6] [a14524485a10] [d082e7bbfa8a]

**R2. Choose WooCommerce when the brand needs full design control, owns hosting, or must run on WordPress.** Applies when a page builder (Elementor or block editor) and plugin choice matter more than a managed stack. Trade-offs the sources give: you buy and maintain hosting (all 4 WooCommerce sources use Hostinger through affiliate links; see 7.6); payments need dedicated plugins, not defaults (02, 05, 07); order emails often fail on a fresh install until SMTP is set (05); security, backups and speed are not covered by any WooCommerce source beyond "Force HTTPS" and "the host has daily backups" (02, 05, 07); plugin versions drift and can be unstable at a new major release (02). Sources: 02, 03, 05, 07. [e91f80fe1721] [b6ce2533321d] [9a06652f2c2b] [fe4eafe0a577]

**R3. Do not choose a platform on hosting price.** All hosting numbers in the sources are affiliate promotions tied to 12 to 48 month terms ($2.99 to $4.49 a month, one-month term cited at $30.99) `[web check]`. Compare total cost of ownership: Shopify plan plus card rate plus apps, against hosting plus paid plugins plus developer time. No source gives this comparison; source 11 admits it does not cost its AI workflow either. Sources: 02, 03, 05, 07, 11. [359dabdafbc0] [2946d83f30cb]

**R4. On either platform, plan the store to live with the brand for years.** Theme and platform are multi-year choices. Source 01 says to plan a theme around catalog size 4 to 5 years out. Applies before shortlisting themes. (opinion, but all sources treat migration as costly). Sources: 01, 10. [0875899454b9] [d936f750ed9d] [6d9a16a8c9c4]

**R144. When replatforming, migrate the product catalogue, order history, customer accounts and SEO redirects to the new store before pointing the domain at it.** Applies to a brand replacing an existing website or platform, not a first-time launch. `[general practice]` No library source; verify against brand data before use.

### 3.2 Account, plan and business identity

**R5. Sign up with an email the business will still control when it changes currency, deletes the store, or needs a critical account action years on, never a contractor's or agency's.** Applies whenever someone other than the owner helps. Only the owner can change currency, delete the store and take other critical actions. Choose an address the business will keep long term. Sources: 01, 04. [63c65895f090] [2f5a7287fedc]

**R6. Enter the exact legal business name and registered address before touching payments, tax or shipping.** These feed the defaults every later screen uses. Skipping means re-entry and mismatch risk in payments verification. Applies to every new store. Sources: 04, 01, 09, 10. [5a93770b958e] [e6e96ea93d37] [86354ef8e01e] [728fa86b4907]

**R7. Treat the myshopify.com handle as permanent. Choose it with care.** The customer-facing store name can change later; the handle is what support and apps reference. Source 01 adds that the default domain stays important internally. Applies to Shopify only. Sources: 04, 01. [2f5a7287fedc] [b30915400ab6]

**R8. Start on the cheapest plan (Basic) for a store with no revenue, upgrade when volume or seats justify it.** 4 Shopify sources say this (opinion). Upgrade triggers the sources give: more staff seats (Basic about 1 to 2, Grow up to 5, Advanced up to 15 `[web check]`), lower card rate at volume, shipping insurance included on Grow and above `[web check]`, per-market theme customization possibly gated above Basic `[web check]`. Only Plus allows full checkout customization at about $2,000 to $2,300 a month `[web check]`. Sources: 01, 08, 09, 10. [8c79cd592233] [61a98d182026] [01109f418218] [4a154ed3a11d]

**R9. If the account is old or migrated, audit the actual feature set in Settings rather than trusting the plan name.** Source 01 reports legacy accounts with inconsistent entitlements. Applies to inherited or client accounts. Sources: 01. [8c79cd592233]

**R10. Read trial terms live, and if a promo trial is used, add payment details within the promo window.** The sources describe "7 or 14 days", "3 days then $1 a month for 3 months" and "must add payment within 3 days" in the same breath, and the offers are affiliate deals. Do not quote any trial term without a `[web check]`. Sources: 01, 08, 09, 10. [4a154ed3a11d]

**R11. Set store currency, backup region and unit system once, before entering prices.** Changing currency later does not convert prices (03). Units are store-wide and changing them means converting every product (02). The registered region sets the default currency and market. Sources: 01, 02, 03, 05, 09. [e6e96ea93d37] [04228274dbbb] [6a90a7b59c5c] [0e315f3cac6e] [86354ef8e01e]

**R12. Use an order ID prefix or suffix if you do not want customers to infer order volume.** Optional. Keep the checkout confirmation step on. Sources: 01. [04689a1d2d66] [d57d8a18c963]

**R13. Clean the fresh WordPress install before any product, collection or theme work, so a leftover plugin cannot break the store import or the storefront later.** Deactivate then delete every host-bundled plugin (keep the caching plugin if the host supplies one, source 05), trash default pages and posts, delete all but one theme, set permalinks to Post name, set the new user default role to Subscriber, set timezone, disable comments on a non-blog storefront. Applies right after install, before importing any starter site (leftover plugins can conflict with the import, 05). Take a backup first (02 card caveat). Sources: 02, 03, 05, 07. [95ada3c41602] [b44de1f18767] [16eefae8f3dd] [f0ee1de989fe] [284bc4b17ed7] [f66e3a492886] [7eaa358a211d] [f94cf50f4191]

**R14. On WordPress, write the site title and tagline to tell a shopper what they can buy and where you ship, not to rank higher; the first line of positioning, not an SEO field.** Positioning copy, not an SEO tactic (02 overstates the ranking effect; see 15-SEO). Sources: 02, 03. [f7075c8cc183] [22fe54d9d081]

**R15. Keep WooCommerce in Coming soon (and Shopify password-protected) until the launch gate in 3.16 passes.** Every source that covers launch says this. Sources: 01, 02, 03, 04, 07, 09, 10. [c4521eb76468] [b8f482b2f3d9] [978ff56aaae8] [3a6ca3eb1bff] [86354ef8e01e] [f7d6a3b222e4]

### 3.3 Domain and DNS

Moved to Appendix A: R16, domain naming taste.

**R17. Buy through the platform for the simplest connection; connect an existing domain when the brand already owns one or wants registrar independence.** Shopify-bought domains auto-connect with no DNS work (04, 09, 10). External domains need about 3 DNS records (type, name, value) copied into the registrar, or a nameserver change (01, 10). Sources note GoDaddy first-year promos ($0.01) with higher renewals, and Shopify at about $16 a year `[web check]`. No source discusses portability if the store later migrates; that trade-off is in 7.2. Sources: 01, 04, 08, 09, 10. [b30915400ab6] [4f9700a6e477] [f1fa31262a90] [7ad023a56f5a] [4ad69ffecb22]

Moved to Appendix A: R18, domain propagation waiting.

Moved to Appendix A: R19, avoiding a default URL.

**R20. Reuse the DNS record workflow for sender-domain verification and branded customer-account domains.** Klaviyo or Omnisend sender verification and the Shopify customer accounts domain use the same registrar record steps. Domain authentication can take up to 48 hours (04). Sources: 01, 04. [b30915400ab6] [abc432db1669] [5ceb388ec702]

Moved to Appendix A: R21, Force HTTPS as general hygiene.

### 3.4 Theme selection and safe editing

**R22. Prepare brand assets before opening the theme editor.** Transparent PNG logo, square favicon (PNG, transparent, about 200 to 300 px wide per 04), 4 to 5 hex colors with light and dark values, 1 to 2 fonts from the platform library, product and lifestyle photos, About copy. Detail on making them lives in 04-BRD. Sources: 01, 04, 10. [285d3b5212e7] [1513317a812c] [ea68a79d73c2] [ba017a5df345]

**R23. List required sections and features before browsing themes.** Filter by industry, catalog size (roughly 11 to 100 vs 500 plus) and features (swatches, before and after slider, mega menu, RTL). A section missing from the theme cannot be added later without custom work or the AI section generator. Sources: 01. [36f8551b5974] [e5fb740fbeed] [0875899454b9]

**R24. Vet a theme on its demo store, its product pages, its mobile view and its developer, not the homepage screenshot.** Any feature in any demo preset is available across the theme. Sources: 01, 04, 09. [35eac0a86ba9] [36f8551b5974] [ea68a79d73c2]

**R25. Free vs paid theme: start free unless a required feature is paid-only.** Source 10 and 09 say most beginners do not need a paid theme; Horizon is named as a safe default with first access to new features (opinion). Source 01 prefers paid themes ($100 to $400 one time `[web check]`) for quality and features (opinion). Merged rule: decide on the section list from R23. Conflict recorded in 7.7. Sources: 01, 09, 10, 04. [36f8551b5974] [6d9a16a8c9c4] [ea68a79d73c2]

**R26. Use "Try theme" to install a full trial and build on it before buying; buying preserves the work.** Applies to paid Shopify themes. Sources: 01, 09. [e0fbc88d7b20]

**R27. Duplicate the theme before any major edit, update, code change or AI session. Never edit the live theme directly.** Sources 01, 06 and 11 state this as the single most important safety step. Source 08 pulls the live theme and pushes back to the same store without a duplicate (kept unpublished until review). Strictest condition wins: always duplicate first, work on the copy, publish the copy, then duplicate the now-live theme for the next round. Conflict in 7.4. Sources: 01, 06, 11, 08. [851254972d2b] [cb2126cc048b] [de00dc0259ba] [35ef5d4ea699] [401b6d077401]

**R28. Do not use the one-click AI whole-store theme generator as the final storefront.** Treat it as a rough idea at most (01, opinion; 09 tried it and reverted to Horizon). Design detail is 07-LPG. Sources: 01, 09, 04. [d936f750ed9d] [ea68a79d73c2]

**R29. Set brand colors once in Settings > Brand and connect theme fields to them as dynamic sources.** A later change cascades. Theme-level custom CSS beats editing theme files. Sources: 01, 03. [8de64df0eaa7] [cfa8eb8e67cf] [6429dec45a84]

**R30. Remove the default theme's demo content and default text before launch.** Demo products, demo categories, "this is a demo store" notices, "Powered by Shopify", the "My Store" footer name (set in Settings > General, not the editor). Sources: 02, 05, 07, 09. [fd779a1ad349] [37e739ed2006] [7eaa358a211d]

**R31. On WordPress, choose the page builder once at starter-site import and pin plugin versions if a new major release is reported unstable.** Source 07 says the Elementor vs block editor choice locks the editor for later pages. Source 02 rolled Elementor back from 4.0.1 to 3.33.6 (dated, `[web check]`). Source 05 deactivated Elementor's new Atomic Editor for beginners. Sources: 02, 05, 07. [b6dd763aa701] [fe4eafe0a577] [caaa3a73071e]

### 3.5 Products

**R32. Pick the product type that matches how the item is sold and fulfilled.** WooCommerce: Simple, Variable, Simple plus Virtual (service, no shipping), Simple plus Virtual plus Downloadable (file), External or Affiliate (checkout on the partner's site; your tax, shipping and coupons never apply), Grouped. A physical item marked downloadable breaks shipping and tax. Shopify: a product with the weight toggle off is treated as digital and skips shipping. Sources: 03, 02, 07, 01. [8c5a95292bdc] [5c8864617956] [5c9382dfb092] [2b411bc7b12e] [530b3d95d941] [e08f40db23df]

**R33. On Shopify, turn the physical product weight toggle on and enter a weight for every shippable product, even when rates are flat.** Off means digital and no shipping at checkout; some warehouses require a weight (01). Source 09 says leave weight and volume blank on flat rates because they do nothing (opinion). Strictest wins: toggle on, weight entered. Conflict in 7.9. Sources: 01, 04, 09. [530b3d95d941] [e08f40db23df] [12b76f909fb9] [9cf73ec552f2]

**R34. Enter the outer package weight and dimensions, not the bare product, in the units chosen in R11.** Calculated and weight-based rates run light without the packaging weight (04). Applies to any store on calculated, weight or class-based rates, and to any brand that may switch later. Sources: 02, 04, 05, 07, 10. [96efb19e76e2] [e3d04df66513] [f81c2abfc7fb] [cbae7d9daa4d]

**R35. Fewer complete products beat a full catalog of thin ones at launch.** Source 04 (opinion). Source 06 launched one SKU. Applies to a new store choosing what to list first. Sources: 04, 06. [12b76f909fb9] [9ffaac57744e]

**R36. Every product carries: specific title, short description above the buy area, long description for detail, media in one consistent ratio, type, vendor, tags, category, price, compare-at only when the discount is real, cost per item, SKU or barcode, tracked stock, weight, SEO title and meta.** The short description is what the shopper reads first (05). Do not copy supplier descriptions (10). Photos at least 1000 by 1000 px (10, opinion); first image is the card image (09). Retitling later means fixing the URL handle (01). Sources: 01, 05, 09, 10, 04. [c673b25c3ccd] [59de72e661ee] [c7f6802299ac] [7b57303f41ec] [900e6376b2c2] [6aec7830e90b] [f330630b1382]

**R37. Compare-at price must be a real former price, and sales must end.** Overstated discounts cost credibility (10). A WooCommerce sale price with no end date never reverts (03). Sources: 03, 05, 09, 10. [b5dc14ff91f1] [5094ffe65549] [6aec7830e90b] [7b57303f41ec]

**R38. Enter cost per item (cost of goods only) so margin reports work later.** Sources: 01. [c7f6802299ac]

**R39. Turn inventory tracking on and give every product a SKU or barcode.** A warehouse needs one to match what was ordered (01). Track quantity even when dropshipping (10). SKU convention from the sources: lowercase title, hyphens, running number or variant suffix (`canine-crunch-01`, `kova-echo-white`). Use a real UPC or GTIN only if the brand owns one (07). Sources: 01, 02, 07, 10. [23e7b8e73e4c] [f81c2abfc7fb] [cbae7d9daa4d] [6aec7830e90b]

**R40. Decide "continue selling when out of stock" and backorders on fulfilment ability.** On only when the brand can source after the sale (dropship). Off for fixed physical stock so the item shows sold out at zero. Allow backorders only with a fast restock path. Set a low stock threshold (demo values 2, 3, 10). Sources: 09, 03, 05, 07. [aa3eb044920e] [b5dc14ff91f1] [7b57303f41ec] [cbae7d9daa4d]

**R41. Inventory is a number, not stock.** Setting 10,000 units stops "sold out" but the supplier or fulfilment app must hold the goods. Confirm separately. Sources: 06. [d7c81282140d] [9b0648a9c684]

**R42. Build variant options from global attributes on WooCommerce; use Add options on Shopify.** Global attributes are reusable and feed filters; product-level ones are not (02, 03). Generate variations, then edit every row. A variation with no price cannot be added to the cart (02, 05, 07). Assign an image per variant so selection swaps the photo. Set default form values to match the default image (05, 03). Sources: 01, 02, 03, 05, 07, 09. [0df57c8635cd] [13e3297ba233] [a8a1945fe798] [51f236113f57] [8e91f90d5c53] [6131e524a00d] [b65346a1a919]

**R43. Verify color swatches; auto-detected colors are close but not exact.** Add hex values or a label image for patterns. Variant image grouping usually needs a paid theme or an alt-text convention. Sources: 01, 03. [4cb4b173c437] [08b36113927c] [51f236113f57]

**R44. Tags are internal organizing properties. Decide the collections first, then tag to match, and copy-paste tag text.** A typo silently breaks a smart collection and fragments filters ("bras" vs "browse", "legging" vs "leggings"). Sources: 01, 10. [12b8ef266d4c] [b9eb3390c92d] [aa204dc3c45e]

**R45. Use bulk edit or import for large catalogs; duplicate a configured product to speed up similar ones, then scrub every field.** Bulk edit has limits; a dedicated app may be needed beyond a point (01). Sources: 01, 07. [f119acb5c204] [37e739ed2006]

**R46. Set upsells on the product page and cross-sells in the cart deliberately, after the target products exist.** Mechanism only; no source measures lift. Sources: 02, 03, 05, 07. [b5fc3d2b7b4c] [dc9a53011770] [a086335acf29] [487c7ec1c105]

**R47. Set a catalog placeholder image on WooCommerce and keep all product images the same width and height.** Cards misalign otherwise; theme crops to force a shape. Sources: 02, 01, 07. [2808b33010fc] [fd779a1ad349] [88cfe2d43556] [37e739ed2006]

**R48. Digital products: set download limit and expiry deliberately, skip stock, still set a SKU, test the download after purchase.** Demo values: unlimited or 365 days. Sources: 02, 03. [5c8864617956] [8c4b61afe68a]

**R49. Gift cards on Shopify are digital by default and auto-fulfil; a physical card is a manual add-on.** Sources: 01. [74d169e9b59c] [04689a1d2d66]

### 3.6 Collections and navigation

**R50. Decide manual vs smart collection with future growth in mind. On Shopify the type cannot be changed after save.** Manual collections are not fed automatically; every new product must be added by hand (09). Smart collections depend on consistent tags (10). Default to tag-based smart collections for a growing catalog (01, opinion with a platform basis). Sources: 01, 04, 09, 10. [f46060533ad6] [343ec6b3bbe4] [aa204dc3c45e] [73ad1a753e69]

**R51. Smart collection conditions: choose "any" to pool sub-groups into a parent, "all" to intersect.** Other bases: price (gift guide under $50), inventory level (clearance), category, vendor, weight. A product can sit in many collections. Sources: 01. [646e5b63a24f] [528c1525c249] [8a469102152c]

**R52. Delete or rename default collections and categories.** Shopify's "Home page" collection can be deleted (09). WooCommerce's default category cannot; rename it to a real one (05). Sources: 09, 05, 07. [343ec6b3bbe4] [61bbf1529174] [774893c987c2]

**R53. Build menus around how shoppers think, not internal names; support more than one path to the same products.** Nest up to 3 levels for a mega menu. Products reachable in 2 to 3 clicks (04, heuristic). Keep the menu short; pick drawer, dropdown or mega menu by catalog size (10, opinion). Remove default links that add no shopping path. Sources: 01, 04, 07, 09, 10. [1eaac2268d09] [53605e79474b] [62bc837b1167] [613ebaa5552e] [2c5b09996536] [c27224e22301]

**R54. Build footer menus in the backend first (a Legal or Helpful Links menu for policies, a Quick Links menu for About, Contact, Support), then point footer blocks at them.** Unpublished pages have no URL to link (01). WordPress: assign the Legal menu to the footer location (03). Sources: 01, 03, 02. [7ac89fa59ccf] [5b24de26c78a] [4ca98aa08031] [7c9f9bf805cf]

**R55. Install the free Search and Discovery app on Shopify for filters, search and recommendations, and uninstall paid apps that did the same jobs.** Filters need the underlying fields filled on every product. Sources: 01, 04. [236052ce217f] [d21ee63adb13] [b9eb3390c92d] [2feda79ef81c]

### 3.7 Pages and legal policies

**R56. Create the About, Contact, shipping policy, return and refund policy, privacy policy and terms pages before launch, and before linking them anywhere.** A footer or theme link to a missing policy does not render; Shopify's footer policy links appear only once policies exist (08). Sources: 01, 04, 08, 09, 10. [fe40994519f8] [64e08ffbebfb] [dd3f3bb627c7] [f1706731ed68] [ab549d0194fc]

**R57. Insert the platform template, then edit every placeholder and every clause to match real practice, then publish. Never publish a template unmodified.** All 5 Shopify sources say this; source 08 found an unedited "[insert return address]". Shopify has no shipping policy template; write it from the real shipping rules (08, 09). Sources: 01, 04, 08, 09, 10. [fe40994519f8] [ecbee7e2499a] [dd3f3bb627c7] [f1706731ed68]

**R58. Treat AI-drafted shipping, return, privacy and terms text as a first pass only; a human with legal knowledge signs off before it governs a real order, refund or chargeback.** Source 03's prompt pattern ("I sell [category] in [countries]. Which legal pages do I need? Create the content and tell me what info you need from my company.") is a usable starting point. Source 01 recommends legal review for the EU, UK and UAE. ecomOS rule: mandatory human check. Sources: 03, 01, 09, 10. [4a64696a8718] [fe40994519f8] [f1706731ed68]

**R59. Write real shipping terms: delivery windows, handling time, conditions, and for US or Canada bound cross-border orders a visible note that import duties may apply.** A thin shipping policy raises ticket volume (01) and disputes (10). The shipping policy text does not set checkout rates; those live in Shipping settings (01). Sources: 01, 10, 04. [fe40994519f8] [c7fe3611980d] [f1706731ed68] [9ab062ef593f]

**R60. Configure return rules (window, who pays return shipping, restocking fee, final sale items) and enable self-serve returns after the policy is published.** Sources: 01, 04. [fe40994519f8] [ecbee7e2499a] [abc432db1669]

**R61. On WooCommerce, never leave a borrowed page (for example Privacy) standing in for Terms and Conditions at the checkout agree-box; a shopper who agrees to the wrong terms has no enforceable return contract.** Swap in the real page and link both to the checkout "read and agree" box. Sources: 02, 03. [ce82c02fc4c6] [5ef2e7c0343a]

**R62. Have a working contact channel live before the first order; a new store gets support emails from day one about sizing, shipping and order status.** Expect emails on day one; slow replies damage reputation (01). Sources: 01, 10. [62f0dece472c]

**R63. Gaps to fill from other folders: cookie consent, GDPR and CCPA data handling, accessibility.** No source covers them (10 flags the gap). Route to 23-SEC and 07-LPG. Human check required.

### 3.8 Payments

**R64. Turn on 2FA before activating Shopify Payments, since the account it protects can move the store's payout money, not just its content.** Save recovery codes in the secret store, not a notes app. Sources: 04. [0949813570ce]

**R65. Names, addresses and IDs in payments setup must match government ID and registration documents exactly ("Robert", not "Rob").** Stated top cause of verification holds. Choose Individual (no business number, includes sole proprietors) or Business (registered number). Confirm the payout bank account accepts the regional deposit type (ACH US, EFT Canada, SWIFT Europe Asia Africa, BECS Australia). Review takes hours to days; keep building meanwhile. Sources: 04, 09, 01. [d81e9a676d16] [ae4e374138b3] [86354ef8e01e] [6303d6cb8521]

**R66. Use Shopify Payments as primary where available, add PayPal alongside it regardless, and use Stripe when Shopify Payments is not available in the country.** Shopify Payments needs a registered business (01) and is the only gateway the sources know that gives per-market currency and the Buy it now wallet button (01). One payment method is a named beginner mistake (10). Check availability by country first `[web check]`. Sources: 01, 04, 10, 09. [6303d6cb8521] [36508e46b0c9] [fd255645fcbc] [cb2ff7113ded] [6d507ac44e12]

**R67. Add well-known regional methods for important markets: Klarna (UK), Tabby (UAE and KSA), Cash on Delivery where it is expected.** Names transcribed from audio; `[web check]`. Sources: 01, 02. [6303d6cb8521] [780a428b8702]

**R68. Set payment capture to automatic at checkout unless the brand reviews orders before charging.** Keep Shop Pay, Apple Pay and Google Pay on. Sources: 04. [cb2ff7113ded]

**R69. On WooCommerce, install dedicated gateway plugins and match the publisher.** Sources 02, 05 and 07 use "Payment Plugins for Stripe WooCommerce" and "Payment Plugins for PayPal WooCommerce" (publisher "Payment Plugins"); source 03 uses the official "WooCommerce Stripe Payment Gateway" and "WooCommerce PayPal Payments". Source 05 says the official Stripe plugin "malfunctions a lot" (one presenter's experience). Conflict in 7.8. Either way: PayPal must be a Business account (05); set the statement descriptor to the company name (03, 07). Sources: 02, 03, 05, 07. [b0fd0a5facf8] [02c7c501d001] [6a3060c2e498] [e2b93597ab6b] [840926e7dab9] [bb0bfd9cf533]

**R70. Connect every gateway in test or sandbox mode, place a full test order, then switch to live and place one small real order and refund it.** Keys pasted in the wrong mode fail silently (02). Source 07 re-checks that the connection test reads "Live" before saving. A gateway can also deactivate later if verification data is incomplete, which blocks all checkouts (01). Sources: 01, 02, 03, 04, 05, 07, 10. [780a428b8702] [6a3060c2e498] [5ef2e7c0343a] [e2b93597ab6b] [94700fd0e277] [bb0bfd9cf533] [728fa86b4907] [c7fe3611980d]

**R71. Keep Stripe, PayPal and gateway keys out of files, prompts and chat; a leaked key can move real customer payments or take checkout down.** Stripe publishable and secret keys, PayPal client ID and secret, and test card numbers are entered by a human in the platform UI. The agent never stores or echoes them. ecomOS rule; supported by source 11's note that the AI cannot complete store authentication for you. [cf190b41088d]

**R72. Test mode off and password off are the last two steps, and not before the test order passes.** Both left on block real sales. Sources: 04, 03, 07, 10. [3a6ca3eb1bff] [94700fd0e277] [6a3060c2e498] [8408a99f2223]

**R145. Turn on order risk scoring and address or card verification (AVS, CVV) at the gateway, and require 3D Secure or SCA for cards from markets that mandate it (for example the EU).** Applies to any store taking card payments; stakes rise with average order value. `[general practice]` No library source; verify against brand data before use.

**R146. In a high-COD market, screen orders for fake-order patterns, verify the phone number, and offer a prepaid discount to pull volume off COD.** Applies where cash on delivery is a significant share of orders, most often mobile-first India (see R66, R67). Source 02 enables COD with no risk framing; the risk controls themselves are `[general practice]`. No library source for the controls; verify against brand data before use. [780a428b8702]

### 3.9 Shipping

**R73. Every country the brand sells to needs an explicit rate, or the platform marks products unshippable there.** WooCommerce: set selling locations to specific countries and shipping locations to match (02, 05). Sources: 01, 02, 05, 03. [4b035d79d6ee] [ca2329868be7] [0e315f3cac6e] [cae87027d082]

**R74. Start simple: domestic zone first, flat rate, one profile; add international zones and profiles as needed.** Shipping worldwide by default adds complexity (10). Delete rate options you will not honor (08 deleted Express). Sources: 10, 08, 09, 01. [6d62360a1568] [a3ff8ef93a56] [c2dc1a7de78b] [4b035d79d6ee]

**R75. Review or replace the platform's default zones and rates before launch.** Shopify pre-creates domestic and international zones with weight-based rates and a $50 plus free threshold (09 says delete them; 04 says inspect and edit). WooCommerce onboarding may leave a default free shipping method (03). Either way the defaults must match real costs before launch. Sources: 04, 09, 03. [0475c2317d11] [c2dc1a7de78b] [6d28f39a903a]

**R76. Prefer flat rates with a free shipping threshold; the threshold is a margin and AOV decision, not a copied number.** Flat rates are easier to estimate and reduce checkout abandonment (01, opinion). Demo thresholds: €50, €100, $75, $100, $200, $300, $400, $10; none is a benchmark. Set it from the brand's margin and typical basket (07). Show the threshold on the storefront (03, 10). Sources: 01, 03, 05, 07, 08, 10. [4b035d79d6ee] [e0349a2e584a] [01aafe27763f] [6d62360a1568] [a3ff8ef93a56] [cb975a996a4d] `[needs brand data: margin, AOV]`

**R77. Order free shipping above flat rate inside a WooCommerce zone so qualifying carts get it; decide whether the minimum applies before or after coupons.** Sources: 07. [01aafe27763f]

**R78. Use per-item or table rates when shipping cost scales with quantity, weight or value; use per-order flat rates for small light goods.** WooCommerce cost field `[qty] * 10` charges per item (02). Table-rate plugins give value or weight brackets; brackets must not gap or overlap or some carts get no method (03). Sources: 02, 03. [5c049a84968e] [d3912129e9a7] [6d28f39a903a] [cae87027d082]

**R79. Use shipping classes for heavy or premium items, fill the "no class" fallback cost, and set calculation to per class, not per order, when carts mix classes.** Per order charges only the most expensive class once and undercharges (05). Sources: 02, 05. [e7fc88f9231f] [da4f0f4ea515] [32e02e8dd4c4]

**R80. On Shopify a country lives in exactly one zone; remove it from the international zone before giving it its own rate, via Markets.** Sources: 04. [b1cd95fe8167] [70512e56f11a]

**R81. Set default package dimensions and empty weight, and assign packages per product when packaging differs.** Undercharge compounds with volume (04). Sources: 04. [e3d04df66513] [96efb19e76e2]

**R82. Assign each zone a fulfilment location; add every warehouse as a location and hold per-location inventory.** Sources: 01. [68a2525c5b79] [4b035d79d6ee]

**R83. Add a delivery time estimate to every rate label and state times wherever shipping is mentioned.** Only promise what fulfilment can honor (08 demo: 5 to 8 business days). Sources: 01, 08, 10. [4b035d79d6ee] [a3ff8ef93a56] [6d62360a1568]

**R84. Configure local delivery, pickup and label purchase only where the business model needs them; check insurance terms per plan.** Insurance: up to $200 per eligible label on Grow and above with Shopify Payments; purchasable up to $5,000 on Basic `[web check]`. Sources: 04, 05, 07. [5c69503ff6eb] [61a98d182026] [83e072152c92]

**R85. Test carts at every bracket edge and every zone, from at least one address per zone, before launch.** Sources: 03, 04, 05, 07. [6d28f39a903a] [3a6ca3eb1bff] [e56e3a1335af] [e0349a2e584a]

**R147. Vet a 3PL on integration reliability, split-shipment cost and stock-sync speed, and sync inventory across every sales channel so two channels cannot both sell the last unit.** Applies to any brand using a fulfilment partner or selling on more than one channel. Source 01 verifies an integration end to end but gives no vetting or sync rule; the vetting and sync steps are `[general practice]`. No library source for them; verify against brand data before use. [c7fe3611980d]

### 3.10 Taxes

**R86. Establish the brand's own obligations first (registered locations, inventory, employees, US nexus, EU VAT thresholds), then configure. A tax professional signs off.** Every source that covers tax defers to a professional and disclaims legal advice. ecomOS rule: human check mandatory. Sources: 01, 03, 04, 09, 10. [9f3db093361a] [9ab062ef593f] [25d24521b0ed] [e86ad9540ade] [64c13e521d9a]

**R87. Set the store address before tax and shipping; both key off it.** Sources: 02, 05, 04. [ca2329868be7] [0e315f3cac6e] [810ad7d0f208] [5a93770b958e]

**R88. On Shopify, enable the built-in tax service and add each region where tax is collected, with the tax ID; set up duties for international markets and say so in the shipping policy.** Sources: 04, 08, 09, 10. [9ab062ef593f] [a3ff8ef93a56] [25d24521b0ed]

**R89. Choose inclusive or exclusive pricing once, before entering prices, and display it consistently across shop, cart and checkout.** The final total is the same; only display differs (02). Inclusive is required in Japan and common in the EU (04); dynamic inclusive pricing per market shows $100 in the UK and $90.91 plus tax in the US (04). Source 01 prefers baking B2C tax into the price everywhere (opinion); sources 02 and 05 chose exclusive ("most stores"); source 03 chose inclusive everywhere for a hybrid B2B and B2C store. Conflict in 7.3. Sources: 01, 02, 03, 04, 05. [f294546e4437] [120d8c76c9ef] [a16dd21fbfc9] [9ab062ef593f] [e86ad9540ade] [810ad7d0f208]

**R90. On WooCommerce, use Standard, Reduced and Zero classes (plus custom), assign the class per product, and enter rates as one row per jurisdiction to 4 decimals with priority where rows overlap.** Lower priority number wins (CA 7.2500 at priority 1 beats a US 5.0000 fallback at priority 2). Do not approximate many states with one row. Source rates like CA 7.25%, NY 4%, WA 6.5%, TX 6.25%, NV 6.85% are dated `[web check]`. Sources: 02, 03, 05. [efa4821ff9f1] [7275017fd366] [8e81d2277f77] [64c13e521d9a] [291aa05299b3] [e551ef1a9cb2]

**R91. Set "calculate tax based on" to the shop address for origin-based states and the customer shipping address for destination-based states.** Source 05 lists AZ, CA, OH, PA, TN as origin-based examples `[web check]`. Sources: 05, 02. [810ad7d0f208] [8e81d2277f77]

**R92. Decide tax on shipping per jurisdiction.** Roughly half of US states tax shipping (05, from taxjar.com, `[web check]`); source 03 turns it on when selling to companies. Sources: 02, 03, 04, 05. [efa4821ff9f1] [9ab062ef593f] [810ad7d0f208]

**R93. Consider an automated tax service (WooCommerce Tax by Automattic, powered by TaxJar, needs a WordPress.com account) instead of manual rows when selling to many jurisdictions.** Source 03 flags its "WooCommerce Tax" mention as a possible affiliate recommendation `[web check]`. Sources: 05, 03. [cdf8caa5f07e] [0a6c2884d19a]

**R94. Test one product per tax class to at least 2 states or countries, and re-open tax settings whenever a new market or shipping destination is added.** A post-launch surprise of unintended tax is a named common mistake (01). Sources: 01, 03, 04. [c7fe3611980d] [64c13e521d9a] [9f3db093361a]

### 3.11 Checkout and customer accounts

**R95. Keep guest checkout on. Do not force account creation before checkout.** Sources 01, 02 and 04 state it; the card for source 05 says the presenter called disabling guest checkout "a terrible idea" while its transcript reading is ambiguous. Offer login and account creation during checkout as well (02). Conflict logged in 7.1. Sources: 01, 02, 04, 05. [47c8ccf3f338] [fab5bea4ff25] [8f9f02d8611d] [be71d70a5e08]

**R96. Contact method email only, phone required at the shipping step, last name only required, company field only for B2B, extra address lines optional.** Order confirmation reaches the customer by SMS only if a phone was given, so email must be required (01). Hide company and second address line on WooCommerce unless needed (03). Sources: 01, 03, 04. [47c8ccf3f338] [d96aa7966303] [1259e2e7f080] [5ef2e7c0343a] [8f9f02d8611d]

**R97. Separate transactional consent from marketing consent. Turn on the marketing checkbox for email and SMS. Pre-select only where legal, per country.** Giving an email for fulfilment is not marketing consent. Pre-selected gives more subscribers with lower engagement (01, rule of thumb: pre-select for a new business, unchecked for an established one). Parts of Europe and the UK forbid pre-selection `[web check]`. Sources: 01, 04, 10. [ed38e3fd032c] [cb2ff7113ded] [f7d6a3b222e4]

**R98. Expect checkout customization to be locked below Plus; brand the checkout with logo, colors and one-page layout; apps can still show or hide payment methods by country.** Sources: 01. [6f0629590ba6] [b7733d8e8e98] [77c72b3e8b08]

**R99. Use the newer passwordless customer accounts, enable self-serve returns and store credit where wanted, and skip legacy accounts unless a marketplace model needs formal signup.** Sources: 01, 04. [abc432db1669] [ecbee7e2499a]

**R100. Set a per-order quantity cap when stock is scarce or inventory depth should not be visible.** Demo value 10. Sources: 01. [f6e33255728a]

**R101. Turn on one abandoned checkout email, not two.** Native Shopify if there is no ESP; the ESP flow if Klaviyo or Omnisend runs. Same rule for branded order confirmation vs the native one (03). Flow content is 14-EML. Sources: 01, 03, 04. [67507a55b77b] [bccbebbbfe5d] [87e84f54a8e0]

**R102. On WooCommerce, do not redirect to the cart on add-to-cart in a multi-product store, and set default customer location to Shop country rather than Geolocate.** Both are source 05 opinions with reasons (browsing interruption; VPN users). Sources: 05. [e05ffae1f1e7] [0e315f3cac6e]

**R103. Enable coupons in settings before building any discount; cap coupons with a per-user limit and a maximum spend where the discount is a percentage.** Shopify cannot natively cap the amount saved on a percentage discount; an app is needed at high AOV (01). Use a code when attribution matters, automatic otherwise (01). Mechanics only; offer strategy is elsewhere. Sources: 01, 02, 07. [bd76d7f8a46b] [447fe9aa14c2] [ba99780859ec] [85bfef85b9bf] [60a02cc9a78e]

**R148. For B2B or wholesale, turn on the company field, build a separate price list or minimum order quantity, and route payment to net terms or a separate checkout.** Applies only where the brand sells to other businesses alongside or instead of consumers. Source 01 only turns on the company field for B2B; the price list, MOQ and net-terms steps are `[general practice]`. No library source for them; verify against brand data before use. [d96aa7966303]

### 3.12 Markets, currencies and languages

**R104. Group countries into markets by shared tax and regulatory treatment, not geography.** Example: Italy and Germany together, Switzerland excluded as non-EU. The registered country becomes the default market. Sources: 01, 04. [8597c5d851d5] [b1cd95fe8167]

**R105. Per-market currency needs Shopify Payments; without it, checkout always reverts to the base currency, so pick a widely understood base (USD or EUR).** Rounding rule such as .95 gives natural prices. Use a per-market catalog to exclude products or override prices (for example to absorb duties). Sources: 01, 04. [36508e46b0c9] [8597c5d851d5] [6474521ce75a] [9ab062ef593f]

**R106. Add languages with Translate and Adapt (free tier 2 languages `[web check]`), auto-translate as a baseline, then human review, and assign the language to its market.** Sources: 01. [018a6b7b5f0e]

**R107. Per-market theme customization may need a plan above Basic; verify.** Sources: 01. [01109f418218]

### 3.13 Apps and plugins

**R108. Launch with a lean stack: reviews, email, tracking. Add one app at a time when a need appears.** Apps inject code and slow the store (01, 04, 10). Uninstall unused apps and re-check speed after each install. Sources: 10, 01, 04. [f07ede1e5f57] [cb7f3ba4e5c9] [60e0c0a3ad53]

**R109. Vet every app before install: 4 plus stars (ideally 4.5 plus), 100 plus reviews, recent complaint patterns, developer track record, Built for Shopify badge, the app's own demo store, and a support response test.** A low review count is acceptable for a niche need (01). Sources: 04, 01. [60e0c0a3ad53] [3f5560597133]

**R110. Installing an app is not enough; enable its App embed and blocks in the theme editor or nothing shows.** Sources: 01. [3f5560597133] [00e6bb4974e0]

**R111. Reviews app: pick one with automated post-purchase requests; sources name Judge.me (free plan plus about $15 a month `[web check]`), Loox (photo reviews), Stamped (loyalty), Yotpo.** If past customers exist, request reviews before showing widgets so the store does not launch at zero. Sources: 01, 04, 10. [13d14684d9ef] [00e6bb4974e0] [fd106fda6cf6] [88e1f0388bb2] [f07ede1e5f57]

**R112. Prefer native Shopify apps where they cover the job: Search and Discovery, Bundles, Subscriptions, Inbox, Flow, Translate and Adapt.** Subscriptions only where the niche fits (consumables, not electronics). Source 04 is vendor content and favours these; cross-check alternatives before recommending a stack. Sources: 01, 04. [a517b976f014] [d21ee63adb13] [275ea2cf320b] [0cbef48284c3]

**R113. On WooCommerce, install the minimum plugin set and activate in order: page builder and helpers, then WooCommerce, then plugins that depend on WooCommerce (wishlist, swatches).** Named sets: Elementor plus ElementsKit plus Metform plus Variation Swatches plus Classic Widgets (02); Blocksy Companion plus swatches (03, 05); table-rate shipping (03); SMTP plugin, unnamed (05). Sources: 02, 03, 05. [e91f80fe1721] [caaa3a73071e] [51f236113f57] [9a06652f2c2b]

**R114. On WooCommerce, configure SMTP before launch or order emails may not send, and enable each transactional email event you want.** A disabled event never fires. Brand the emails, and edit template PHP only in a child theme. Sources: 05, 02, 03. [9a06652f2c2b] [6346d90f2e59] [153e99ddf6bc]

**R115. Connect sales channel apps (Facebook and Instagram by Meta, TikTok) only with owner approval; the prerequisites are an established Facebook account, admin on the business manager, page and Instagram professional account.** Meta is read only under ecomOS rules; the Shopify-side connection is a platform write and an approval gate. Sources: 04. [08b80874b674]

**R149. Choose subscriptions or bundles as a deliberate lever tied to the product, not just an app pick: subscriptions fit consumables that run out (supplements, food), not one-time or durable goods like electronics.** Applies when repeat purchase or basket-building is a real lever for the catalogue. Sources: 01. [a517b976f014]

**R150. Add a loyalty or rewards program when repeat purchase rate matters to the brand's margin, not as a default app install.** It pays off more for a consumable or frequently repurchased catalogue than for a one-time purchase. Source 01 names Stamped for loyalty but only as "evaluate each," with no rule on when it pays off; the payoff condition is `[general practice]`. Sources: 01. [3f5560597133] [13d14684d9ef]

**R151. List on a marketplace or another channel (Amazon, TikTok Shop, Google Shopping) as a deliberate multichannel decision, and treat inventory sync across channels as a launch requirement, not an afterthought.** Applies to a brand with production or stock capacity beyond its own store's demand. Source 02's only related feature is the External or Affiliate product type, which links out to someone else's listing rather than syncing your own; the multichannel rule itself is `[general practice]`. No further library source; verify against brand data before use. [5c9382dfb092]

### 3.14 Staff, permissions, security and backups

**R116. Give staff custom roles with exact permissions; be deliberate about Orders access because it exposes sales figures.** Use collaborator access (code plus myshopify domain) for developers and agencies instead of a paid seat. Sources: 01. [b03f3e640118]

Moved to Appendix A: R117, 2FA as a general control.

Moved to Appendix A: R118, WordPress role hygiene.

**R119. Duplicate the theme before every change and confirm host backups exist, so a bad edit or failed launch step can be undone without the storefront going dark.** Use a versioned backup app if more restore depth is needed. No source shows a restore drill. Route hardening (login limits, malware scanning, WAF) to 23-SEC. Sources: 01, 02, 11. [851254972d2b] [b44de1f18767] [de00dc0259ba]

Moved to Appendix A: R120, reading AI agent permission prompts.

### 3.15 Analytics and pixel handoff

**R121. Install tracking through the platform's native integration, then verify with a real-time view during a test session, on the checkout step too, and re-verify after any theme change or app install.** GA4 through the Google and YouTube app; Search Console added separately. Event setup, pixels and attribution live in 06-MEA. Sources: 04, 10. [9921264a1167] [b915be273681] [f07ede1e5f57]

**R122. Read analytics over a multi-month window; cohort reports need about a year of orders.** One day's conversion rate is not an average. Funnel reading is 06-MEA and 07-LPG. Sources: 01. [63acdbeb3fff] [d90fa94f0b55] [a6c3105bd9d3]

### 3.16 Launch gate

**R123. Follow the setup order: identity, payments, tax, shipping and package weights, domain and email, tracking and legal pages, test order, remove password.** Later steps depend on earlier ones. Sources: 04, 05, 09, 10. [a14524485a10] [b6ce2533321d] [86354ef8e01e] [728fa86b4907]

**R124. A saved setting is not proof. Close every step with the action a customer would take.** Test order, rate quote, footer link click, real-time analytics view, incognito visit. Sources: 04, 06, 07. [d6854b97be2c] [220bda0dd2e7] [978ff56aaae8]

**R125. Run test mode orders, then real orders through the real gateway and real fulfilment, especially with a warehouse integration, many SKUs or bundles.** Test at least one address per zone, one product per tax class, and on a real phone. Confirm the confirmation email arrives. Sources: 01, 04, 03, 05, 10. [c7fe3611980d] [94700fd0e277] [3a6ca3eb1bff] [6a3060c2e498] [e56e3a1335af] [728fa86b4907]

**R126. Verify on the live, logged-out storefront in an incognito window, not the editor preview.** Click every interactive element; AI-built accordions can render and not open. Sources: 06, 07, 10. [220bda0dd2e7] [e5db2ba0cf5e] [a8e85e602df8] [978ff56aaae8]

**R127. Remove the password (or set WooCommerce to Live) only after the checklist in 5.1 passes, then browse the domain as a first-time visitor.** Confirm the intended theme shows as live. Optional early access: share the password with a waitlist first (01, one client example). Sources: 01, 02, 04, 07, 09, 10. [c7fe3611980d] [c4521eb76468] [b915be273681] [978ff56aaae8] [f7d6a3b222e4] [a5598af5de1a]

**R128. Launch imperfect after the checklist passes, then collect feedback.** Source 10 (opinion). Sources: 10. [f7d6a3b222e4]

### 3.17 AI-assisted setup

**R129. Give the AI real inputs before it builds: products and collections in the store, an inspiration folder with logo, product photos, screenshots, and a spec or framework if one exists.** The agent designs around what exists; remind it of the real product count or it uses placeholders. Sources: 08, 11, 06. [5a0b9ad6456f] [66e36f527ce2] [100fb168dda1]

**R130. Let the agent read the theme and interview you (direction, sections, fonts, preview method) and propose a plan before writing any section.** Sources: 08. [13e82e14fdd0]

**R131. Ask the agent for one storefront change per prompt and verify it live before the next; a bundled request that lands 3 of 4 changes can leave a broken PDP element live to shoppers.** Source 11's 4-part request landed 3 of 4. Re-issue the missing piece alone. Sources: 08, 11. [4d8bf77b16e5] [9e2078f63db9] [5c660bd33ab3]

**R132. Preview privately on a local dev server or an unpublished theme; the preview password is the store password, not the account password.** Sources: 08. [e27f52047618]

**R133. Pull and push through the Shopify CLI on a duplicated theme only; the human runs `shopify auth login` and reads every permission prompt; push uploads unpublished, then review in the theme editor, then publish.** Source 08's `shopify theme pull --store DOMAIN --live` pulls the live theme; the strict rule (R27) is to duplicate first. Conflict in 7.4. Sources: 08, 11. [401b6d077401] [cf190b41088d] [de00dc0259ba] [d23a4cb7706c] [35ef5d4ea699]

**R134. Custom Liquid sections go in via Edit Code on the duplicate; assign the product template and select the product in the section settings, or it renders empty; update by pasting over the existing file, never a second file.** Sources: 06. [cb2126cc048b] [8818e8f9c5b2] [3d2c297be211] [54bad54781d1] [c7884fec6d58] [a8e85e602df8]

**R135. AI output is a draft: prune duplicate sections, resize icons, click every interactive element, check images are not oversized, run a mobile pass the sources skip.** Source 01 rates the native AI section generator as unpredictable and not first choice for beginners. Sources: 06, 11, 01, 05. [100fb168dda1] [91ef75dc529d] [82e21838aca5] [3dca4354b6dc] [733d55d477a7]

**R136. Clone a competitor's layout or interaction pattern only; never its text, logo, product or faces.** ecomOS rule, matched by source 11. Sources: 11. [91ef75dc529d]

**R137. Reusing one template across many SKUs or brands trades uniqueness for speed; differentiate copy and imagery or the store reads generic.** Conflict in 7.5. Sources: 06, 01. [309fee9d852d] [1b74e6a6d37e]

Moved to Appendix A: R138, distrusting the agent's own report.

Moved to Appendix A: R139, Sidekick vs Claude Code comparison.

### 3.18 Post-launch platform operations

**R140. Order flow: keep auto-fulfil off for physical goods (gift cards excepted), move Processing to Completed after shipping on WooCommerce, let the tracking number trigger the shipping email on Shopify, split multi-item orders when one item is backordered.** Sources: 01, 03, 02, 04, 05. [04689a1d2d66] [98bfe80fc295] [21c0848f9464] [fa39013559f5] [eb0639f2f194] [694b2885835d]

**R141. Edit fixed notification templates sparingly and send a test after any edit.** Sources: 01, 03. [1259e2e7f080] [153e99ddf6bc]

**R142. Classify support tickets in the first weeks: product questions mean a thin product page; shipping questions mean a thin shipping policy. Do not patch either by editing notification emails.** Sources: 01. [e2fd26e10b51] [62f0dece472c]

**R143. Re-run the shipping and tax checks whenever a product, zone, market, app or theme changes.** Sources: 04, 01. [9f3db093361a] [cb7f3ba4e5c9]
## 4. Procedures (implementation)

Two tracks. Procedures 4.2 to 4.13 are Shopify. Procedures 4.14 to 4.20 are WooCommerce. 4.1 and 4.21 are shared. Every admin path is `[verify UI]`; the tag is stated once per procedure header and applies to every step in it. Rollback means how to undo the step if a check fails.

### 4.1 Choose the platform (shared)

Goal: a written platform decision with the trade-offs the brand accepted.
Preconditions: inputs from section 2 (existing site, budget, staff skills, target countries, checkout needs).
Steps:
1. Score the brand on R1 to R4: existing WordPress site (yes pushes WooCommerce), need for custom checkout (only Plus on Shopify), need for per-market currency (Shopify Payments availability in the brand's country `[web check]`), in-house WordPress skills, willingness to maintain hosting, plugins, SMTP, backups and security.
2. Price both stacks for 12 months: Shopify plan plus card rate plus the 3 launch apps; hosting plus paid plugins (table-rate shipping, tax service, swatches, SMTP, security) plus developer hours. All numbers `[web check]`.
3. Record the decision in the store build brief (9.1) with the 3 trade-offs the brand accepted.
Check: the user has approved the platform in writing.
Rollback: none; this is a decision record.

### 4.2 Shopify: account, plan, identity and security

Goal: an owner-controlled account with legal identity set, the right plan, and 2FA on. `[verify UI]`
Preconditions: owner email, legal business name and address, plan decision, current trial terms `[web check]`.
Steps:
1. Sign up at Shopify with the owner's long-term business email (R5). Set a strong password and store it in the brand's secret store. Do not use an affiliate link unless the user chose to (all Shopify sources link one).
2. Answer or skip the onboarding questions. Pick the store name; the myshopify handle it creates is permanent (R7).
3. Choose the plan (R8). If a promo trial applies, add payment details inside the promo window (R10).
4. Settings > General: enter the legal business name, registered address, store email (a branded address the team reads), phone, currency, backup region, unit system, order ID prefix (R6, R11, R12). Save.
5. Settings > General > Brand: upload rectangular logo, square logo (reuse the favicon), 4 to 5 hex colors, slogan, social links (R22).
6. Profile > Security > turn on two-step authentication. Save recovery codes in the secret store, never a notes app (R64, R117).
7. Settings > Users: add staff by email with custom roles; decide Orders access; use collaborator access for agencies and developers (R116).
8. If the account is inherited, audit Settings for actual features (R9).
Checks: Settings > General shows the exact legal name and address; 2FA shows on; the owner email is the business's.
Rollback: store name and address can be edited; the handle cannot. Roles can be edited or removed.

### 4.3 Shopify: domain and business email

Goal: a custom primary domain that resolves, plus a branded mailbox. `[verify UI]`
Preconditions: domain decision (7.2), registrar login held by the brand (never pasted to the agent).
Steps:
1. Settings > Domains. Either Buy new domain (search, buy, it auto-connects) or Connect existing (enter the domain).
2. For an external domain, follow the on-screen records: usually about 3 DNS records (type, name, value) added at the registrar under Manage DNS, or a nameserver change (R17). The human enters them at the registrar.
3. Wait. "Pending" for a few hours is normal; up to 24 hours is possible (R18).
4. Set the custom domain as primary.
5. Create a branded mailbox at the mail provider; send and receive a test (04).
6. Later, reuse the same DNS steps for ESP sender authentication and a branded customer accounts domain (R20).
Checks: the domain loads the password page in an incognito window; Settings > Domains reads Connected; the test email round-trips.
Rollback: revert the primary domain to myshopify.com; remove the DNS records at the registrar.

### 4.4 Shopify: theme selection, trial, duplicate and brand settings

Goal: a theme that has every required section, installed as a safe working copy, with brand colors and fonts connected. `[verify UI]`
Preconditions: brand assets (R22), section list (R23), decision free vs paid (7.7).
Steps:
1. Online Store > Themes. Note the installed default (Horizon in the sources `[web check]`).
2. Visit theme store. Filter by Industry, Catalog size, Features. Open each shortlisted demo; check product pages and the mobile preview; vet the developer (R24).
3. For a paid theme, click Try theme and build on the trial; Buy later keeps the work (R26). For a free theme, Add to theme library.
4. Three-dot menu > Duplicate. Rename the copy with a date. Work only on the copy (R27).
5. Edit theme on the copy. Theme settings > Colors: connect each field to the saved brand colors via the dynamic source icon (R29). Typography: choose 1 to 2 library fonts. Logo and favicon: upload.
6. Remove demo content, "Powered by Shopify" and any "My Store" text (R30; the footer store name is set in Settings > General).
7. Password page: keep password protection on; optionally customize the coming soon page.
8. Hand section building (hero, homepage order, PDP layout) to 07-LPG. Do not use the AI whole-store generator as the final storefront (R28).
Checks: the copy exists in the theme library; the live theme is untouched; brand colors cascade when one is changed in Settings > Brand.
Rollback: delete the copy; the live theme was never edited.

### 4.5 Shopify: products, variants and bulk edit

Goal: every product complete per R36 and buyable. `[verify UI]`
Preconditions: product import sheet (9.2), images in one ratio, SKUs, weights, costs, stock.
Steps, per product (Products > Add product):
1. Title. Save once to generate the URL handle; if you rename later, fix the handle (R36).
2. Short description above the buy area; long detail lower (routed to 07-LPG for structure). Do not paste supplier copy.
3. Media: upload all images in one batch, one ratio, clearest image first.
4. Category (most specific suggestion; review auto-detected values such as color), Type (specific, for example "legging"), Vendor (own brand or third-party brand), Tags (copy-paste from the collection plan, R44), Collections.
5. Pricing: Price, Compare-at only if real (R37), Cost per item (R38). Charge tax checkbox per the tax decision (4.9).
6. Inventory: Track quantity on; SKU or barcode; quantity per location; "continue selling when out of stock" per R40.
7. Shipping: physical product toggle on; weight; customs info for international (R33); package assignment if packages differ (R81).
8. Variants: Add options (Size, Color); per-variant price, quantity, image; check swatch colors (R42, R43).
9. Search engine listing: title, meta description, handle.
10. Status Active. Save.
Bulk: Products > select > Bulk edit; expose columns (price, tracking, tags, type, metafields); drag values down; copy-paste tags. For a large catalog, use import (R45). Beyond bulk edit limits, a bulk-edit app.
Checks: open the live product in incognito; add to cart; reach checkout; variant selection swaps image and price; no "Sold out" unless intended (06). Run checklist 5.2.
Rollback: set status to Draft; bulk edit can be reversed by re-editing; keep the import sheet as the source of truth.

### 4.6 Shopify: collections, filters, menus and footer

Goal: navigable catalog with correct collection types and working menus. `[verify UI]`
Preconditions: collection plan with type (manual or smart) decided per R50; tags applied.
Steps:
1. Products > Collections. Delete the default "Home page" collection if unused (R52).
2. Add collection: title, description, image, SEO fields. Choose Manual or Automated. Automated: conditions (tag, type, category, vendor, price, inventory) and "any" or "all" (R51). The type is permanent after save.
3. Install Search and Discovery (free). Filters: keep Availability and Price if useful; add filters from category metafields, standard fields or custom metafields (Settings > Custom data > Products > Add definition; "List of values" when a product can hold several values). Order filters in the app (R55).
4. Content > Menus: edit Main menu; add items linking to collections, products, pages or URLs; drag right to nest, up to 3 levels; "#" for a non-clickable parent (R53).
5. Create footer menus (Legal or Helpful Links; Quick Links) after policies and pages are published (R54, 4.11).
6. In the theme copy, set Header > Navigation to the main menu; add footer Link list blocks pointing at the footer menus.
Checks: every menu item resolves in preview and on a phone; a filter showing only one value means the field is not filled on other products (fix in bulk edit); a smart collection missing a product means a tag typo.
Rollback: menus and filters are editable; a wrongly typed collection must be recreated.

### 4.7 Shopify: payments, test mode to live

Goal: Shopify Payments verified, PayPal added, alternatives where needed, test mode used then turned off. `[verify UI]`
Preconditions: 2FA on (4.2); legal identity documents held by the owner; gateway availability by country `[web check]`.
Steps:
1. Settings > Payments > Activate Shopify Payments. Choose Individual or Business (R65). The owner enters legal names exactly as on ID, dates of birth, ID numbers, addresses, and uploads the ID document. Confirm the payout bank account matches the regional deposit type. Submit; review takes hours to days.
2. Payment capture: Automatically at checkout unless orders are reviewed first (R68). Manage payment methods: keep Shop Pay, Apple Pay, Google Pay on.
3. Additional payment methods: add PayPal (log in, grant permissions). Add regional methods for key markets (R66, R67). If Shopify Payments is unavailable, add Stripe as the card gateway.
4. Shopify Payments > Manage > enable Test mode. Place a full order from the storefront (eye icon) with an official test card number (ask Sidekick or the docs; never a real card in test mode). Verify tax, shipping rate, policy links, confirmation email, and the order in admin. Process it through fulfilment (R125).
5. Turn Test mode off. After launch, place one small real order and refund it (R70).
6. Before launch, re-open Settings > Payments and confirm the gateway is active, not paused for missing verification (01).
Checks: checklist 5.4.
Rollback: turn test mode back on; disable an alternative method. Never leave test mode on after launch (R72).

### 4.8 Shopify: locations, shipping zones, rates, packages and profiles

Goal: a rate for every target country, correct package weights, and no default rate left unreviewed. `[verify UI]`
Preconditions: shipping and tax matrix (9.3): countries, rates, threshold, transit times, locations, package weights.
Steps:
1. Settings > Locations: add each warehouse with address (R82). Assign inventory per location on products or via Products > Inventory.
2. Settings > Shipping and delivery. Open the general profile. Inspect the pre-created domestic and international zones and their weight-based rates and $50 plus free threshold. Edit them to the matrix or delete them (R75).
3. Per zone: set the fulfilment location; Add rate: flat rate with a price and a condition (order value or weight), plus a free shipping rate above the threshold (R76). Name rates with the delivery estimate (R83). Delete rates you will not honor.
4. To give a country its own zone: remove it from the international zone (Edit zone, uncheck, Save), then Create market for it and add its rates (R80).
5. Packages: Add package with type, outside dimensions and empty weight; set as default; assign per product where packaging differs (R81).
6. Additional profiles only when product groups ship differently (R74).
7. Local delivery and pickup only if the model needs them (R84).
Checks: quote a multi-item order at addresses in every zone, just below and above the threshold; a country with no rate shows as unshippable, so add one; a low quote signals a missing package weight. Checklist 5.3.
Rollback: zones and rates are editable; keep the matrix as the source of truth.

### 4.9 Shopify: taxes and duties

Goal: tax collected only where the brand is registered, displayed the way the brand decided, signed off by a human. `[verify UI]`
Preconditions: tax registrations and IDs from the brand's advisor; inclusive vs exclusive decision (7.3).
Steps:
1. Settings > Taxes and duties. Confirm the base country.
2. Sales tax: Collect in a new region for each registered jurisdiction; enter the tax ID; Collect (R88).
3. Duties and import taxes: Set up for the international markets served; state in the shipping policy that duties are handled at checkout, or add the arrival-duties note for US and Canada if not (R59).
4. Shipping taxability per region (Advanced options in the US).
5. Global setting "Include sales tax in product price and shipping rate" only where required or expected (Japan, EU) or where the brand chose inclusive (R89). For international, adjust per-market pricing under Markets.
6. Check the "charge tax" box state on products and the tax class on shipping rates.
Checks: test order per tax class and per region; a human tax advisor reviews the settings before launch; re-check after any new market (R94).
Rollback: stop collecting in a region; remove the inclusive setting. Charging tax by mistake after launch is a named common error (01).

### 4.10 Shopify: markets, currencies and languages

Goal: markets grouped by tax treatment with local currency, catalog and language. `[verify UI]`
Preconditions: Shopify Payments active (for currency), target countries, translation review capacity.
Steps:
1. Markets (sidebar or Settings). The registered country is the default market. Create market > name > add countries grouped by shared tax and regulatory treatment (R104). Nest sub-markets if useful.
2. Currency per market with a rounding rule (for example .95) or fixed per-market prices. Without Shopify Payments, set a widely understood base currency and accept that checkout reverts to it (R105).
3. Catalog per market to exclude products (gift cards) or override prices (absorb duties).
4. Languages: install Translate and Adapt; Settings > Languages > Add language; Auto translate; human review side by side; assign to the market (R106).
5. Per-market theme customization (hero swap for one country) only if the plan allows (R107).
Checks: view the storefront with a VPN or the country selector; prices, currency, language and shipping rates match the market; checkout currency behaves as expected.
Rollback: deactivate the market; remove the language.

### 4.11 Shopify: policies, return rules, checkout, customer accounts, apps

Goal: legal pages published and linked, checkout fields and consent set, lean app stack installed and embedded. `[verify UI]`
Preconditions: policy drafts approved by a human; return rules; ESP decision; app budget.
Steps:
1. Settings > Policies: for Refund and return, Privacy, Terms of service, Contact information: Insert template, replace every bracket and placeholder, edit clauses to real practice, Publish (R57). Shipping policy: no template; write from the shipping matrix (R59). Legal notice as required.
2. Online Store > Pages: About, Contact (with the support email), size guide if needed. Publish.
3. Return rules: window, return shipping, restocking fee, final sale. Settings > Customer accounts: choose the newer passwordless accounts, enable self-serve returns and store credit as wanted (R60, R99).
4. Settings > Checkout: contact method email; phone required at shipping; last name only; company only for B2B; no forced account; marketing consent checkboxes for email and SMS with pre-selection per country rules (R95 to R97). Optional per-order quantity limit (R100).
5. Checkout > Customize: logo, colors, one-page checkout (R98).
6. Marketing > Automations: turn on Recover abandoned checkout only if no ESP will run it (R101).
7. Apps: install the reviews app, the email app and the tracking integration; vet each per R109; open Edit theme > App embeds and enable each (R110). Search and Discovery from 4.6. Bundles and Subscriptions only where the niche fits (R112).
8. Sales channels (Meta, TikTok) only with owner approval (R115).
9. Footer menus (4.6 step 5) now that policies exist; confirm the theme footer shows policy links (R56).
Checks: click every footer policy link in incognito; read the first paragraph of each policy for placeholders; the human sign-off for legal pages is recorded in the launch checklist (9.4). Checklist 5.5 for apps.
Rollback: unpublish a policy (links stop resolving); uninstall an app and disable its embed.

### 4.12 Shopify: launch gate and password removal

Goal: a store that passes checklist 5.1, then goes public. `[verify UI]`
Preconditions: 4.2 to 4.11 done; tracking installed and verified by 06-MEA (R121).
Steps:
1. Ask Sidekick (or run checklist 5.2) to scan products for missing descriptions, prices, images.
2. Run test mode orders (4.7 step 4) at one address per zone and one product per tax class; repeat on a real phone (R125).
3. Place real orders through the real gateway and, if a warehouse app is connected, confirm the order reaches the warehouse and tracking flows back (01).
4. Confirm Settings > Payments shows an active gateway, Settings > Domains shows Connected, Settings > Taxes matches intent, every target country has a rate.
5. Walk the site in incognito: every menu item, every policy link, every interactive element (R126).
6. Get the owner's written approval to launch (ecomOS approval gate).
7. Online Store > Preferences > remove password protection. Confirm the intended theme is live (Online Store > Themes).
8. Open the domain in a new incognito tab as a first-time visitor: homepage, product, add to cart, checkout start (R127).
9. Optional: share the password with a waitlist a few hours before removal (01).
Checks: checklist 5.1 signed; 5.6 scheduled for the first week.
Rollback: re-enable password protection; the store is hidden again within seconds.

### 4.13 Shopify: AI-assisted theme work with Shopify CLI and Claude Code, and custom Liquid sections

Goal: theme code changes made by an AI agent on a duplicate theme, previewed privately, reviewed, then published. `[verify UI]` `[web check: install commands, plan requirements]`
Preconditions: products and collections exist (R129); inspiration folder assembled; owner approval for theme publish; a Claude plan that includes Claude Code (sources say Pro `[web check]`).
Steps:
1. Install Node.js (leave "tools for native modules" unchecked), Git, and the Shopify CLI: `npm install -g @shopify/cli@latest` (08; source 11 chose npm over Homebrew after Homebrew failed once). Verify with `shopify version`.
2. Install Claude Code (Windows: `irm https://claude.ai/install.ps1 | iex`; the Mac command is not given in the sources `[web check]`) or the Anthropic VS Code extension (check the publisher is Anthropic, 11).
3. In Shopify admin, duplicate the live theme (4.4 step 4) or ask the agent to duplicate it and confirm the copy in Online Store > Themes (R27, R133).
4. Create a project folder. Authenticate: the human runs `shopify auth login` (or the login prompt from `shopify theme pull`) in the terminal and picks the account (R71, R133).
5. Pull the duplicate theme, not the live one. The sources only give `shopify theme pull --store <store-domain> --live` (08); the flag that targets a specific theme by ID is not stated in any source `[web check: current Shopify CLI flag to pull a named or ID-selected theme]`. Do not pass `--live`, see 7.4. Confirm "pulled successfully" and the files locally. Source 11's route is to ask the agent to list themes, confirm which is live, then ask it to pull the duplicate by name.
6. Add an `inspiration` folder with product photos, logo versions, screenshots, and any framework document (R129). Never place credentials in the folder or the prompt.
7. Start the agent in the project folder. Ask it to read the theme and the folder, interview you (direction, sections, fonts, preview method) and propose a plan before building (R130). The exact kickoff prompt used by source 08 is not in the source; write your own from R129 to R131.
8. Preview on the local dev server using the preview command the agent prints (source 08 does not state the command itself `[web check: current Shopify CLI dev preview command]`); enter the store password (Online Store > Preferences), not the account password (R132).
9. Build one section or one change per prompt. Review in the preview. Give feedback in plain English. Remind the agent of the real product count for product sections (R131). Read each permission prompt (R120).
10. Push unpublished using the push command the agent prints after you say you are ready to publish (source 08 states only that it uploads without publishing; the exact flags are not in the sources `[web check: current Shopify CLI push flags and how to target the duplicate]`). Open Edit theme on the duplicate, check text, order and mobile (08).
11. Custom Liquid section path (06): Online Store > Themes > duplicate > Edit code > Sections > Add a new section named `<brand>_<product>.liquid`; paste the code; Save. Customize theme > create a product template > hide default sections > Add section > pick the custom file > in section settings select the product > assign the template to the product (R134). To update, paste over the same file.
12. QA on the live, logged-out URL: click every accordion and tab; check image sizes; run a mobile pass (R135).
13. With owner approval, Publish the duplicate. The old theme moves to unpublished. For the next round, duplicate the now-live theme (R133).
Checks: theme list shows the duplicate and the untouched live theme before any edit; every requested change verified on the storefront, not from the agent's report (R138).
Rollback: publish the previous theme from the library; delete the section file; reassign the product to the default template.

### 4.14 WooCommerce: hosting, domain, WordPress install and cleanup

Goal: a clean WordPress install on the brand's domain with HTTPS. `[verify UI]` `[web check: hosting plans and prices]`
Preconditions: hosting choice made without affiliate bias (7.6); owner holds the hosting account.
Steps:
1. Buy hosting on a 12 to 48 month term (sources say never 1 month; 12 months minimum, 07). Register with the owner's email; add company details for VAT where relevant.
2. Verify the account email and, after claiming the domain, the domain email (R21).
3. Claim or connect the domain (.com preferred). Install WordPress through the host: create a blank site, set the admin username and password (secret store), pick the server region nearest the buyers.
4. Wait for install and propagation (about 10 minutes typical, up to 24 hours). Confirm Force HTTPS is on in the host panel.
5. Log in at `yourdomain.com/wp-admin`. Cleanup per R13. Moved to Appendix A: WordPress fresh-install cleanup click list.
Checks: padlock on the live domain; one theme installed; permalinks produce `domain.com/shop` style URLs (re-save permalinks if not).
Rollback: host daily backup restore (confirm it exists); reinstall WordPress from the host panel.

### 4.15 WooCommerce: theme, page builder, plugins and core WooCommerce settings

Goal: WooCommerce installed with the base plugin set and General, Products, Accounts and Emails settings done. `[verify UI]`
Preconditions: 4.14 done; builder choice made (block editor vs Elementor, R31).
Steps:
1. Appearance > Themes > Add: install a lightweight WooCommerce-friendly theme (sources use Blocksy with Blocksy Companion, or Astra with Starter Templates). Activate. Delete the other theme.
2. Starter site import (optional): filter Free and ecommerce, choose the builder at the prompt (07 stresses this choice locks the editor), import with WooCommerce checked. Or install WooCommerce directly: Plugins > Add New > WooCommerce > Activate; skip or run the wizard (country sets currency).
3. Install remaining plugins per R113, then activate in order: builder and helpers, then WooCommerce, then WooCommerce-dependent plugins. Pin a builder version if the new major is unstable (R31).
4. WooCommerce > Settings > General: store address; Selling locations = specific countries; Shipping locations = ship to all countries you sell to (or Disable shipping for a digital-only catalog); Default customer location = Shop country (05); Enable taxes; Enable coupons; Currency, symbol position, separators, 2 decimals (R11, R73, R102).
5. Settings > Products: Shop page; Placeholder image (upload to Media, paste the file URL); weight and dimension units before any product (R11, R47); Add to cart behaviour: no redirect to cart for multi-product stores (R102); Reviews on, verified purchase per policy; Product rating on.
6. Settings > Accounts and Privacy: Guest checkout on; Allow log in during checkout; Allow account creation during checkout and on My Account (R95).
7. Settings > Emails: for each event you want (New order, Cancelled, Failed, On hold, Processing, Completed, Refunded, customer emails): Manage > Enable > recipient, subject, heading, additional content. Set From name and address. Brand color and logo (R114). Install and configure an SMTP plugin (unnamed in the sources `[web check]`) so emails actually send.
8. Settings > Advanced: confirm Cart, Checkout, My Account pages; set the Terms and Conditions page to the real page once written (R61).
9. Settings > Site visibility stays Coming soon (R15). Store details: real store name, address, phone, email.
10. Appearance > Customize > WooCommerce: clear the "demo store" site notice; products per page; product image dimensions (equal width and height); Site Identity: logo (skip cropping), favicon.
Checks: Cart, Checkout, My Account, Shop pages exist; a test email arrives from the SMTP sender; coming soon banner shows on the front end.
Rollback: deactivate a plugin; restore from the host backup.

### 4.16 WooCommerce: payments, test mode to live

Goal: Stripe, PayPal and any offline method connected, tested in sandbox, then live. `[verify UI]` `[web check: plugin names and current maintenance]`
Preconditions: Stripe account and PayPal Business account owned by the brand; plugin choice (7.8).
Steps:
1. Plugins > Add New: install the chosen Stripe plugin and PayPal plugin, matching the publisher exactly (R69). Activate.
2. WooCommerce > Settings > Payments: enable the Stripe card gateway and the PayPal gateway; enable Cash on delivery, bank transfer or cheque only where expected (02). Drag to order the methods (card above PayPal, 03).
3. Stripe: Manage > connect the account through the on-screen flow, or paste the test publishable and secret keys (human pastes; never in files, R71). Set the statement descriptor to the company name. Enable test mode; confirm webhooks show enabled. Run the Connection test. Decide where Apple Pay and Google Pay buttons show (product page vs checkout only).
4. PayPal: Manage > Connect to PayPal with the Business account; status Connected. Sandbox first if offered.
5. Place a full sandbox order with the provider's test card (Stripe's 4242 test card in test mode only). Confirm the order in WooCommerce > Orders, the customer email and the admin email (R70).
6. Switch to live: paste live keys or uncheck Test mode, set the mode selector to Live, run the Connection test again and confirm it reads Live, Save (07). PayPal: Production, not Sandbox.
7. After launch, one small real order, then refund it from the order screen.
Checks: checklist 5.4; a failed connection test after pasting keys means the mode and keys do not match.
Rollback: set the gateway back to test mode or disable it in Payments.

### 4.17 WooCommerce: shipping zones, methods, classes and table rates

Goal: every selling country in a zone with a method that matches the shipping matrix, no bracket gaps. `[verify UI]`
Preconditions: shipping and tax matrix (9.3); product weights and package dimensions entered; table-rate plugin installed if brackets are needed (03).
Steps:
1. WooCommerce > Settings > Shipping > Zones. Remove any leftover default method from onboarding (03).
2. Add zone: name and region (country, or a state for a narrower zone). Zones match in order; verify current zone matching before stacking overlapping zones (02 gap).
3. Add method Free shipping with requirement Minimum order amount (or coupon, or both); decide "apply minimum before coupon" (R76, R77). Drag it above Flat rate.
4. Add method Flat rate: name, tax status, cost. Per-order cost is a plain number; per-item is `[qty] * <amount>` (R78).
5. Shipping classes: Shipping > Classes > add (for example Heavy). In the zone's Flat rate, fill the per-class cost and the "No shipping class" fallback; set Calculation type = Per class (R79). Assign the class on each heavy product.
6. Table rates (optional): add the table-rate method per zone; build price or weight brackets that leave no gap and no overlap; set the free threshold; enable the "left for free shipping" notice (R78).
7. Local pickup only if offered.
8. Repeat per country with that country's rates and threshold.
Checks: carts just below and above every bracket edge and the threshold, a normal item, a heavy item, and both together; a cart with no shipping option means a bracket gap. Checklist 5.3.
Rollback: disable a method; delete a zone.

### 4.18 WooCommerce: taxes, manual or automated

Goal: tax rows or an automated service that match the brand's registrations, with display consistent from shop to checkout. `[verify UI]` `[web check: rates, origin-based state list, plugin status]`
Preconditions: store address set; obligations confirmed by a human advisor (R86); inclusive vs exclusive decision (7.3).
Steps:
1. Settings > General: Enable taxes. Settings > Tax appears.
2. Prices entered with tax: Yes (inclusive) or No (exclusive), per the decision. Display prices in shop and in cart and checkout: the same mode everywhere (R89).
3. Calculate tax based on: shop base address for origin-based states, customer shipping address otherwise (R91). Shipping tax class: based on cart items unless one flat rate everywhere.
4. Tax classes: Standard, Reduced rate, Zero rate; add custom classes by typing a name.
5. Manual rates: in each class tab, Insert row per jurisdiction: country code, state code (blank for whole country), postcode or city if needed, rate to 4 decimals (7.2500), name, priority (lower wins), compound, shipping taxable (R90, R92). Source real rates from a reference `[web check]`; never one blanket row for many states.
6. Automated alternative: install WooCommerce Tax (Automattic, powered by TaxJar), connect a WordPress.com account, enable automated taxes in Settings > Tax (R93).
7. On each product: Tax status Taxable and the right Tax class; digital goods often a 0% reduced class (05).
Checks: test order per tax class to at least 2 jurisdictions; the shop price matches the checkout price mode; a human advisor signs off before Live.
Rollback: disable taxes in General; delete rows; deactivate the tax plugin.

### 4.19 WooCommerce: products, categories and coupons

Goal: each product type set up correctly and every variation priced. `[verify UI]`
Preconditions: product import sheet (9.2); global attributes list; categories plan.
Steps:
1. Products > Categories: delete demo categories; rename the undeletable default to a real category; set slugs lowercase; nest with Parent (R52). Products > All: trash demo products and empty trash (R30).
2. Products > Attributes: create each global attribute (Size, Color) with type (label, button, radio, color for swatches) and terms in display order (R42).
3. Products > Add New, Simple physical: title, long description, short description; General: Regular price (2 decimals), Sale price with schedule end date (R37); Tax status and class; Inventory: SKU per convention, Manage stock, quantity, backorders per R40, low stock threshold, Sold individually if one per order; Shipping: package weight and dimensions, shipping class; Linked products: upsells and cross-sells once other products exist (R46); Attributes for filtering; featured image and gallery; category, tags, brand; Publish.
4. Variable: Product data = Variable; Attributes > Add existing global attributes, select the values this product has, "Used for variations"; Variations > Generate variations; open every row: image, SKU, price (mandatory or the variation cannot be bought), stock, weight, shipping and tax class; Default form values matching the default image; Publish (R42).
5. Virtual (service): Simple plus Virtual; price; purchase note with the booking link; Sold individually. Downloadable: plus Downloadable; add the file; download limit and expiry (R48).
6. External or affiliate: Product data = External; product URL; button text; price for display only (R32).
7. Duplicate a configured product for similar items and scrub every field (R45).
8. Coupons: Marketing > Coupons: code, type (percentage or fixed), expiry, minimum and maximum spend, exclude sale items, prevent stacking, usage limit per coupon and per user (welcome codes: 1 per user) (R103).
Checks: front end shows "Select options" then price range for variables; each combination adds to cart; the download button appears after a test purchase; the coupon applies once and is blocked on the second try. Checklist 5.2.
Rollback: set the product to Draft; trash and restore from Trash.

### 4.20 WooCommerce: pages, menus, legal pages and going live

Goal: static pages, legal pages, menus and the Live switch. `[verify UI]`
Preconditions: policy drafts approved by a human; 4.15 to 4.19 done.
Steps:
1. Pages > Add: Home (assign as static homepage in Settings > Reading), Shop (auto), Blog (Posts page), About, Contact (form plugin, support email), Privacy Policy, Terms and Conditions, Shipping, Refunds. Publish. Page design is 07-LPG.
2. Legal text: draft with the source 03 prompt pattern, fill in legal name, address, category, countries; human legal review; paste and publish (R58).
3. Settings > Advanced: point Terms and Conditions to the real page; Customize > WooCommerce > Checkout: hide company and address line 2 if not needed, phone optional or required per fulfilment, select the Privacy and Terms pages for the agree box (R61, R96).
4. Appearance > Menus (or Customize > Menus): primary menu (Shop, categories, About, Contact); footer menus: Legal (policies) and Quick links; assign to locations; replace any "#" placeholders once pages exist (R54).
5. Run the end-to-end test (02 N, 05 Q): as a buyer add a simple, a variable and a digital product, apply a coupon, choose shipping, pay by each method in sandbox, confirm the thank-you page, download button, order in admin, My Account. As admin, move the order Processing to Completed and confirm the customer email.
6. Final sweep (02 P): navigation, shop grid and filters, product page, blog, contact form, search, My Account.
7. Owner approval. WooCommerce > Settings > Site visibility > Live > Save.
8. Incognito check of product pages and checkout (R127).
Checks: checklist 5.1.
Rollback: Site visibility back to Coming soon.

### 4.21 Post-launch platform operations (shared)

Goal: orders flow, notifications fire, refunds work, settings stay correct.
Preconditions: store live; support inbox monitored.
Steps:
1. Shopify: Orders > review, print packing slip and label, ship; the tracking number triggers the shipping confirmation; bulk print and mark fulfilled at volume; fulfil in-stock items now if one item is backordered (R140). WooCommerce: WooCommerce > Orders > ship, then set Completed and Update; use Cancelled or Refunded as needed.
2. Refunds: Shopify order > Refund; WooCommerce order > Refund at the bottom of the order.
3. Notifications: edit templates lightly; send a test after any change (R141). WooCommerce email PHP edits only in a child theme.
4. Weekly in the first month: run checklist 5.6; classify tickets (R142); re-check speed after any app or theme change; re-open tax and shipping after any new market (R143).
5. Every platform write after launch (price bulk edits, deleting zones, changing tax, publishing a theme, removing a payment method) goes through owner approval.
Checks: confirmation and shipping emails arrive on a real order; refunds show in the gateway; no order stuck in Processing past the ship time.
Rollback: republish the previous theme; re-enable a payment method; restore a deleted zone from the matrix.
## 5. Diagnostic checklists

Written for a worker. Each row: what to check | how | good | bad | fix | source. Record the result and the date in the launch checklist (9.4).

### 5.1 Pre-launch audit (the gate before password removal or Live)

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Owner controls the account | Settings > Users, or WP Users | Owner email is the business's; 2FA on | Contractor email owns it | Transfer ownership before launch | 01, 04 |
| Legal name and address | Settings > General; WC > General | Exact legal name and registered address | Nickname, missing address | Correct, then re-check payments | 04 |
| Store currency and units | Settings > General; WC > General and Products | Match the target market | Wrong currency | Fix before entering more prices | 09, 10, 03 |
| Domain | Open the domain in incognito | Store loads on the custom domain; status Connected | Pending for more than a day, or loads myshopify | Check DNS records; wait; do not launch | 04, 10 |
| Payments active | Settings > Payments; WC > Payments | Gateway active, verification complete, test mode off | Paused for verification, test mode on | Complete verification; turn test mode off after the test order | 01, 04, 07 |
| Test order passed | Checklist 5.4 | Order, tax, shipping, email all correct | Any miss | Fix and repeat | 04, 10, 05 |
| Rate for every target country | Quote an order per zone | Rate shows for each | "Not shippable" | Add the rate | 01, 04 |
| Tax matches intent | Test order per class and region; advisor sign-off recorded | Tax as intended, human sign-off dated | Tax charged where not registered, or missing | Fix Settings > Taxes; advisor review | 01, 04, 10 |
| Policies published and real | Open each footer link in incognito, read the first paragraph | Real business name, no brackets, shipping and return terms real | Placeholder text, missing shipping policy | Edit and publish; human sign-off dated | 08, 09, 10 |
| Footer policy links present | View the footer on the live theme | All 5 links resolve | Missing links | Create the policy; rebuild the footer menu | 08, 01 |
| Navigation | Click every menu item, submenu and collection, on a phone too | Every link resolves to a populated page | Empty or broken | Fix link, tag or collection | 09, 10 |
| Products complete | Checklist 5.2 | All pass | Missing price, image, weight | Fix in bulk edit | 04, 10 |
| Contact channel live | Send a test to the support email or form | Reply path works | Bounces | Fix mailbox | 01 |
| Notifications | Test order emails; WC SMTP test | Confirmation and shipping emails arrive | Nothing arrives | SMTP on WC; check notification settings | 05, 01 |
| Tracking fires | Real-time view during a test session, including checkout | Events show | No events | Reinstall via native integration; hand to 06-MEA | 04 |
| Duties disclosure | Read the shipping policy for US and Canada cross-border | Arrival duties note present, or duties at checkout set | Nothing said | Add the note or set duties | 01, 04 |
| Demo content gone | Browse products, collections, footer, site notice | Only real content | "My Store", demo products, demo notice | Remove | 07, 09, 02 |
| Mobile pass | Real phone: scroll, tap every button, add to cart, checkout | Clean | Cramped nav, unreadable text | Fix in 07-LPG | 10, 04 |
| Live theme is the intended one | Online Store > Themes | Intended theme marked live | Old theme live | Publish the right one | 10, 11 |
| Owner approval | Written approval on file | Yes | No | Do not remove the password | ecomOS |

### 5.2 Product data completeness

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Title specific, handle matches | Product list; open URL | Descriptive title; handle matches | Generic title; stale handle after rename | Edit title and handle | 01, 04 |
| Short description present | Product form | Above the buy area, benefit-led, not supplier copy | Empty or pasted from supplier | Rewrite | 05, 10 |
| Images | Product media | One ratio across the catalog, first image clearest, at least 1000 px | Mixed ratios, blurry, oversized files | Re-upload at consistent size | 01, 10, 06 |
| Price and compare-at | Product form | Compare-at only when the discount is real; sale has an end date | Fake or permanent strikethrough | Remove or schedule | 10, 03, 09 |
| Cost per item | Product form | Filled | Empty | Fill from the import sheet | 01 |
| SKU or barcode | Inventory section | Present and unique per variant | Missing or duplicated | Apply the convention | 01, 02, 07 |
| Inventory tracking | Inventory section | Tracking on; continue-selling per fulfilment ability; low stock threshold set | Untracked; continue-selling on with fixed stock | Fix | 01, 09, 10 |
| Weight and package | Shipping section | Physical toggle on; package weight and dimensions in store units | Toggle off (treated as digital); bare product weight | Fix; assign package | 01, 04, 02 |
| Variants | Storefront | Every variation has a price, image, stock; selection swaps image and price; default matches image | Priceless variation; "Select options" never resolves | Edit each row | 02, 05, 07 |
| Type, vendor, tags, category | Product form | Specific type; tags copied from the plan; category precise | Typos, inconsistent case | Bulk edit | 01 |
| Tax status and class | Product form | Matches the tax decision | Taxable digital item at standard rate | Assign class | 02, 05 |
| SEO listing | Search engine listing preview | Title and meta filled | Blank | Fill | 01, 10 |
| Buyable | Incognito: add to cart, reach checkout | Works, no "sold out" | Sold out, button dead | Inventory non-zero; status active; template assigned | 06 |
| Filters populated | Storefront filters | Every product carries the filter field | Filter shows one value | Bulk edit the field | 01 |

### 5.3 Shipping and tax configuration check

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Selling and shipping locations | WC > General; Shopify Markets | Only served countries | All countries by default | Restrict | 02, 05 |
| Default zones reviewed | Shipping settings | Defaults edited or deleted to match the matrix | Weight-based defaults and a $50 threshold left as shipped | Replace | 09, 04 |
| One zone per country | Shopify zones | Country appears in one zone | Country in two zones or none | Remove from the broad zone, then add | 04 |
| Rates per zone | Quote from an address per zone | Correct flat rate and free threshold | No option, wrong rate | Add or edit rate | 01, 03 |
| Threshold boundaries | Carts just below and above the threshold | Paid below, free at or above | Free too early or never | Fix minimum and method order | 07, 03 |
| Bracket gaps | Carts at every bracket edge | Every value falls in exactly one bracket | No shipping option | Re-edit brackets | 03 |
| Class calculation | Cart with a normal item, a heavy item, both | Charges combine as intended | Highest class charged once | Per class, not per order | 05 |
| Package weight | Quote before and after setting package weight | Quote rises by the packaging weight | Same quote (weight unset) | Set default package | 04 |
| Rate labels | Checkout | Delivery estimate on each rate | Bare "Standard" | Add estimate | 01, 09 |
| Free threshold visible | Announcement bar or cart | Shoppers see "spend X more" | Hidden | Add the bar or notice | 03, 10 |
| Tax regions | Taxes settings | Only registered jurisdictions collect | Extra or missing region | Fix; advisor review | 04, 01 |
| Tax basis | WC > Tax | Origin or destination matches the state rule | Guessed | Look up and set | 05 |
| Tax rows | WC > Tax class tabs | One row per jurisdiction, 4 decimals, priority set | One blanket row | Rebuild rows or automate | 02, 03 |
| Tax on shipping | Per region | Set per jurisdiction rule | Default left | Decide and set | 05, 04 |
| Display mode | Shop page vs checkout | Same inclusive or exclusive mode | Shop shows one, checkout another | Align display settings | 03, 02 |
| Per-class test | One order per class to 2 regions | Tax line matches | Wrong rate | Reassign class or row | 03 |
| Duties | International test order | Duties at checkout, or arrival note in policy | Silent | Set duties or add note | 04, 01 |
| Human sign-off | Launch checklist | Advisor initials and date | Missing | Do not launch | ecomOS |

### 5.4 Payments go-live check

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| 2FA | Profile > Security | On | Off | Turn on before Shopify Payments | 04 |
| Identity match | Payments setup | Names, addresses, IDs match documents exactly | Nickname or old address | Correct; expect a re-review | 04 |
| Payout account | Payments setup | Right deposit type for the region | Wrong type | Change bank details | 04 |
| Gateway status | Settings > Payments; WC > Payments | Active, verified | Paused, incomplete verification | Complete it; a gateway can deactivate silently | 01, 04 |
| Second method | Checkout | Card plus PayPal (plus regional) | One method | Add PayPal or Stripe | 10, 01 |
| PayPal account type | PayPal dashboard | Business | Personal | Upgrade | 05 |
| Mode and keys match | WC gateway settings; Connection test | Test passes in test mode; Live reads Live | Test fails | Re-paste matching keys; check mode selector | 02, 07 |
| Statement descriptor | Gateway settings | Company name | Default | Set | 03, 07 |
| Sandbox order | Full checkout with the test card | Order, customer email, admin email, order in admin | Any miss | Fix, repeat | 03, 04, 05 |
| Wallets | Checkout | Shop Pay, Apple Pay, Google Pay as intended | Missing | Manage payment methods | 04 |
| Test mode off | Payments settings, after the test order | Off | On at launch | Turn off | 04, 03, 07 |
| Real order and refund | Small live order, refund from the order screen | Funds move and return | Fails | Investigate before traffic | 03, 05 |
| Credentials | Files, prompts, chat | None present | A key in a file or prompt | Rotate the key; remove | ecomOS |

### 5.5 App and permissions audit

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| App count | Apps list | Launch set: reviews, email, tracking, plus native free apps | 10 apps at launch | Uninstall unused | 10, 01 |
| Vetting record | App stack list (9.5) | Rating 4 plus, 100 plus reviews, developer checked, support tested, Built for Shopify where present | No record | Vet or remove | 04, 01 |
| App embeds enabled | Edit theme > App embeds | Each installed app's embed on | Installed but invisible | Enable | 01 |
| Duplicate jobs | Compare features | One reviews app, one abandoned checkout flow, one search app | Two apps doing the same job | Consolidate | 01 |
| Speed after install | Speed metrics before and after | No regression | Regression | Remove the app or its embed | 01 |
| Plugin versions (WC) | Plugins list | Current or deliberately pinned | Unstable new major | Roll back or update | 02 |
| Unused plugins and themes (WC) | Plugins, Themes | None inactive | Inactive leftovers | Delete | 03, 05 |
| Staff roles | Settings > Users; WP Users | Custom roles; Orders access deliberate; Subscriber default | Blanket admin; Administrator default | Fix roles | 01, 02 |
| Collaborator access | Settings > Users | Agencies via collaborator code, time-bound | Agency holds owner login | Revoke; reissue | 01 |
| Sales channels | Settings > Sales channels | Only approved channels connected | Unapproved Meta or TikTok connection | Remove; log approval | 04, ecomOS |
| Backups | Theme library; host panel | Dated theme duplicate; host backups confirmed | None | Duplicate; enable backups | 01, 02, 11 |
| Recovery codes | Secret store | Stored | In a notes app or chat | Move; regenerate | 04 |

### 5.6 Post-launch first-week check

| What to check | How | Good | Bad | Fix | Source |
|---|---|---|---|---|---|
| Password and test mode | Storefront in incognito; payments settings | Public; test mode off | Still gated or in test | Fix now | 04, 10 |
| First real orders | Orders list | Payment captured; order reached fulfilment; tracking back | Stuck in Processing; no tracking | Fulfil; check the warehouse app | 01, 03 |
| Confirmation and shipping emails | Ask a real customer or place your own order | Both arrive | Missing | SMTP (WC); notification settings | 05, 01 |
| Tax surprise | First orders' tax lines | As intended | Tax charged unexpectedly | Fix taxes; refund the difference | 01 |
| Unshippable destinations | Support tickets, checkout errors | None | Customers blocked | Add rates | 01 |
| Ticket mix | Classify tickets | Mostly order status | Product questions (thin PDP) or shipping questions (thin policy) | Fix the page or policy, not the emails | 01 |
| Tracking data | Analytics real-time and daily reports | Sessions and purchases recorded | Gaps | 06-MEA re-verify | 04 |
| Speed | Built-in speed metrics | Stable | Drop after an app install | Remove the app | 01 |
| Domain and email | Send and receive; open the domain | Working | Bounces, DNS drift | Fix records | 04 |
| Review requests | Reviews app log | Requests sending on the set delay | None sent | Enable automation | 01 |
| Inventory drift | Compare platform stock to real stock | Match | Oversold | Turn off continue-selling; correct counts | 09, 06 |
| Analytics reading | Time window set to the launch period, no conclusions from one day | Multi-day view | Judging on day one | Wait for a longer window | 01 |

## 6. Thresholds and benchmarks

Confidence: how many sources agree. "Demo" marks a number a presenter typed on camera to show a mechanic; it is not a recommendation. Every price and plan number is `[web check]`.

| Value | Condition | Sources | Confidence | Note |
|---|---|---|---|---|
| Card rate 1.5% Basic, 1.3% Grow, 1.1% Advanced | Shopify plan choice | 01 | 1 source | `[web check]` |
| Staff seats about 1 to 2 Basic, 5 Grow, 15 Advanced | Seat limit triggers upgrade | 01 | 1 source | `[web check]` |
| Shopify Plus about $2,000 to $2,300 a month | Only plan with full checkout customization | 01 | 1 source | `[web check]` |
| Trial: 3 days free then $1 a month for 3 months; also "7 or 14 days" | Affiliate promo terms | 01, 08, 09, 10 | 4 sources, internally inconsistent | `[web check]`; promo, not price |
| Payment details within 3 days of signup | Keep the promo trial | 09, 10 | 2 sources | `[web check]` |
| Paid theme $100 to $400 (01) or $200 to $400 (10) one time | Theme choice | 01, 10 | 2 sources | `[web check]` |
| Favicon PNG, transparent, about 200 to 300 px wide | Branding upload | 04 | 1 source | Stated spec |
| Product images at least 1000 by 1000 px | Product media | 10 | 1 source | Opinion |
| 3 to 5 real product images per product | Product media | 04 | 1 source | Opinion |
| Brand palette 4 to 5 hex colors, light and dark | Pre-build assets | 01 | 1 source | Working habit |
| Menu nesting up to 3 levels | Mega menu | 01 | 1 source | Theme-typical |
| Products reachable in 2 to 3 clicks | Navigation | 04 | 1 source | Heuristic |
| Mobile products per row 2 | Product cards | 01 | 1 source | Opinion |
| Shopify default free shipping threshold $50 plus, weight-based | Shipped default zone | 09 | 1 source | Delete or edit before launch |
| Free shipping thresholds: €50 (01), €100 (01), $75 (10), $100 (05, 07), $200 (03), $300 (03), $400 (02), $10 (08) | Free shipping over a minimum | 01, 02, 03, 05, 07, 08, 10 | 7 sources agree on the mechanic; none on a number | Demo; set from margin and AOV |
| Flat rates: €8.80, €10, $20 (01); $5 (05); $6 and $15 express (09); $10 (02, 07); $6.99 to $14.99 brackets (03) | Flat or table rates | 01, 02, 03, 05, 07, 09 | 6 sources | Demo |
| Handling buffer about $5 | Added to shipping | 10 | 1 source | Demo |
| Transit time 5 to 8 business days | Rate label | 08 | 1 source | Demo; must reflect real fulfilment |
| Shipping insurance up to $200 per label on Grow and above with Shopify Payments; purchasable up to $5,000 on Basic | Insurance | 04 | 1 source | `[web check]` |
| Local delivery radius 100 miles or km | Local delivery | 04 | 1 source | Demo |
| Tax rate entry 4 decimals (7.2500) | WooCommerce rate rows | 02, 03 | 2 sources | Platform format |
| Priority: lower number wins | Overlapping WooCommerce rows | 02 | 1 source | Platform behaviour |
| CA 7.25%, NY 4%, WA 6.5%, TX 6.25%, NV 6.85% | US state rates at recording | 02, 03, 05 | 3 sources | `[web check]`; dated |
| Origin-based states: AZ, CA, OH, PA, TN | Tax basis | 05 | 1 source | `[web check]`; example list |
| About half of US states tax shipping | Tax on shipping | 05 | 1 source | `[web check]` |
| Demo tax classes: US standard 20%, reduced 10%, digital 0%, Canada 30% | Class mechanic | 03 | 1 source | Demo, not real rates |
| Dynamic inclusive pricing: $100 in the UK vs $90.91 plus tax in the US | Markets pricing | 04 | 1 source | Worked example |
| Payments verification hours to days | After submitting Shopify Payments | 04 | 1 source | Typical range |
| Domain propagation: a few hours typical, up to 24 hours; hosting domain about 10 minutes | After connecting | 03, 07, 10 | 3 sources | Provider dependent |
| Sender domain authentication up to 48 hours | ESP DNS | 04 | 1 source | Stated |
| Domain about $16 a year (.com) | Buying through Shopify | 07, 08, 09 | 3 sources | `[web check]` |
| GoDaddy $0.01 first year | Registrar promo | 01 | 1 source | `[web check]`; promo |
| Hosting $2.99 to $4.49 a month on 12 to 48 months; 1 month $30.99 | Hostinger terms | 02, 03, 05, 07 | 4 sources, all affiliate | `[web check]` |
| Hosting term 12 to 48 months, never 1 month | Term choice | 02, 07 | 2 sources | Opinion |
| Hosting email verification within 30 days | Account kept | 05 | 1 source | `[web check]` |
| Launch app count 3 (reviews, email, tracking) | App stack | 10 | 1 source | Rule of thumb |
| App vetting 4 plus stars, ideally 4.5, 100 plus reviews | Before install | 04 | 1 source | Heuristic |
| Judge.me about $15 a month paid tier, 15-day trial | Reviews app | 01 | 1 source | `[web check]` |
| Review request delay 14 days domestic, 5 days other | Judge.me default at recording | 01 | 1 source | `[web check]` |
| Translate and Adapt free tier 2 languages | Languages | 01 | 1 source | `[web check]` |
| Per-order quantity cap 10 | Checkout limit | 01 | 1 source | Demo |
| Low stock threshold 2, 3, 10 | Inventory alerts | 03, 05, 07 | 3 sources | Demo |
| Inventory 10,000 to avoid "sold out" on a dropship SKU | Inventory field | 06 | 1 source | Demo; not stock |
| Coupon: per user 1; min spend $200 and max spend $500; 10% welcome | Coupon limits | 02, 07 | 2 sources | Demo |
| Cohort report needs about 1 year of orders | Analytics | 01 | 1 source | Rule of thumb |
| Funnel example 10% add to cart, 5.32% reach checkout, 2.63% purchase | One demo store | 01 | 1 source | Demo, not a benchmark |
| Cart abandonment about 70%; 7% conversion loss per second of delay; two-thirds of orders on mobile; SMS 98% open | Cited industry stats | 04 | 1 source | Unsourced; do not quote to clients |
| Claude Code usage warning at 90%, about 1 hour reset | AI session limits | 11 | 1 source | `[web check]`; one instance |
| AI section build 1.5 to 2.5 minutes; full template a couple of minutes | AI theme work | 11 | 1 source | One instance |
| Bundled prompt: 3 of 4 changes landed | AI prompting | 11 | 1 source | One instance |
| Claude Pro about $20 a month required for Claude Code | AI toolchain | 08, 11 | 2 sources | `[web check]` |

## 7. Where sources disagree

### 7.1 Guest checkout on or off
- Sources 01, 02 and 04 say keep guest checkout on; forced account creation is a named mistake. Source 02 labels guest checkout "recommended".
- Source 05's transcript says "enable guest checkout. I think that's a terrible idea", which read literally opposes guest checkout. Its card (be71d70a5e08) records the presenter calling *disabling* guest checkout a terrible idea, which matches the other sources. The mini playbook flagged the transcript as ambiguous.
- When each is right: forced accounts only make sense for a marketplace or membership model (01 on legacy accounts).
- What the agent should do: keep guest checkout on, offer account creation during checkout, use passwordless accounts. Treat source 05 as agreeing via its card and note the transcript ambiguity if anyone cites it the other way.

### 7.2 Domain through the platform vs an independent registrar
- Sources 04, 09 and 10 favour buying through Shopify: auto-connect, no DNS work, about $16 a year `[web check]`. Source 10 notes registrars can be cheaper in year 1 and dearer at renewal.
- Source 01 shows both paths and buys at GoDaddy in the demo. No source discusses portability if the brand migrates platforms; source 10's mini playbook flags this as the missing trade-off.
- When each is right: platform purchase for a solo founder who values speed; registrar for a brand that already owns domains, wants one registrar for all of them, or plans to keep platform options open.
- What the agent should do: ask the brand which it wants (section 2 input). Default to the registrar the brand already uses; otherwise buy through the platform. Either way the brand, not the agent or agency, holds the registrar login.

### 7.3 Tax baked into the price vs itemised at checkout
- Source 01 prefers folding B2C tax into the price and remitting it (opinion), while admitting Europe requires formal configuration.
- Sources 02 and 05 chose exclusive display ("most stores do this").
- Source 03 chose inclusive everywhere for a hybrid B2B and B2C store so the first price seen equals the price paid.
- Source 04 says inclusive is required in Japan and common in the EU, and shows dynamic inclusive pricing per market.
- When each is right: inclusive where law or local expectation demands it (EU, UK, JP); exclusive in the US where itemised sales tax is expected; per-market dynamic pricing when selling to both.
- What the agent should do: decide per market with the brand's tax advisor, never from a presenter's preference. Keep display consistent from shop to checkout. Record the decision in the shipping and tax matrix. Human sign-off before launch.

### 7.4 Pull and push to the live theme vs duplicate first
- Source 08 runs `shopify theme pull --store DOMAIN --live`, edits locally, pushes back unpublished, reviews, then publishes. No duplicate or staging theme.
- Sources 01, 06 and 11 duplicate the theme before any edit; source 11 calls it the single most important safety step and re-duplicates the now-live theme each round.
- When each is right: source 08's flow keeps the push unpublished, so risk is lower than editing live in the theme editor, but a push with the wrong flag or a publish of a half-reviewed theme has no restore point.
- What the agent should do: always duplicate first and pull the duplicate by theme ID (4.13). Never pass `--live` on pull or push. Publishing needs owner approval.

### 7.5 Template reuse across products and brands
- Source 06 builds one section-based PDP and reuses the structure across SKUs and even brands ("swap out the logo"), and admits it can feel generic.
- Source 01 says use one default template for what is common, extra templates only where layout differs, and metafields where only content differs.
- Source 11 generates a full template from a framework document and prunes it.
- When each is right: structural reuse is efficient; copy and imagery must differ per product. A white-label clone of another brand's page is out of bounds under the ecomOS rule against copying competitor text, products or faces.
- What the agent should do: reuse templates and metafields per source 01; require distinct copy, images and claims per product; refuse "swap the logo" clones of a competitor's page.

### 7.6 Hosting choices with affiliate bias
- Sources 02, 03, 05 and 07 all recommend Hostinger's Business plan on a 48-month term through their own affiliate links and coupons. Source 03 also earns on Blocksy Pro and Elementor Pro; source 02 promotes two paid template marketplaces.
- No source compares hosts, uptime, support or backup restore. Prices quoted differ between sources and the presenters say they change daily.
- What the agent should do: treat every hosting number as a promo `[web check]`; compare at least 2 hosts on price after year 1, backups with a restore test, staging, SSL, and support; never buy 48 months for an unproven store without the owner's explicit choice; record the affiliate context in the setup spec.

### 7.7 Free vs paid theme
- Source 01 prefers paid themes for quality and section variety (opinion). Sources 09 and 10 say most beginners do not need a paid theme; Horizon is a safe default. Source 04 (Shopify) shows a free theme.
- What the agent should do: build the required section list first (R23). Pay only when a required section or feature is paid-only. Use Try theme to verify before buying.

### 7.8 Official vs third-party Stripe plugin on WooCommerce
- Sources 02, 05 and 07 install "Payment Plugins for Stripe WooCommerce"; source 05 says the official plugin "malfunctions a lot" (one presenter's experience).
- Source 03 installs the official "WooCommerce Stripe Payment Gateway" and it worked in the demo.
- What the agent should do: `[web check]` current ratings, maintenance and Stripe's recommended integration; pick one, match the publisher exactly, and run the sandbox and live tests either way.

### 7.9 Fill weight fields on a flat-rate store
- Source 09 leaves weight and volume blank on flat rates because they do nothing. Source 01 says leave the physical toggle on and enter a weight or the item is treated as digital and some warehouses need it. Source 04 wants package weights for calculated rates.
- What the agent should do: toggle on and enter weights and package dimensions always. It costs one field per product and protects against a later switch to calculated rates or a warehouse integration.

### 7.10 Marketing consent pre-selected
- Source 01: pre-select for a new business, unchecked for an established one, and per country where pre-selection is illegal. Source 04 and 10: enable the checkbox to start list building. No source pre-selects in the EU or UK.
- What the agent should do: checkbox on; pre-selected only where legal and only with the brand's consent language reviewed by a human `[web check: consent rules per country]`.

### 7.11 Default shipping zones: delete or edit
- Source 09 says delete Shopify's default zone before building your own. Source 04 says inspect the pre-created zones and add or edit rates.
- What the agent should do: either, as long as no default rate survives unreviewed. Deleting is simpler when the matrix is complete.

### 7.12 Flat rate vs table rate
- Sources 01, 09 and 10 recommend flat rates with a free threshold for simplicity and lower abandonment. Sources 02 and 03 build per-item and bracket rates because bulky goods do not ship 10 for the price of 1.
- What the agent should do: flat plus free threshold for small light goods; per-item, class or bracket rates when cost scales with quantity or weight. Test bracket edges.

### 7.13 Trial and pricing claims
- Source 01 states two trial structures in one passage; sources 08, 09 and 10 state a third via affiliate links. All differ from Shopify's standard pricing.
- What the agent should do: never quote a trial or plan price without a same-day `[web check]`; use no affiliate link unless the owner chooses one.

### 7.14 Sidekick vs Claude Code for theme work
- Source 11 says Sidekick only generates sections. Sources 01 and 04 use Sidekick for settings lookup, drafts, collections and data questions, and source 01 notes Sidekick's editor changes can propagate through shared settings.
- What the agent should do: use the native assistant for lookup and drafts; use CLI plus an agent on a duplicate theme for code; `[web check]` current capabilities before repeating either claim.

### 7.15 Product count at launch
- Source 04 prefers a few solid listings; source 01 builds a full activewear catalog with collections and filters; source 06 launches one SKU.
- What the agent should do: launch with every product that passes checklist 5.2, however many that is. Do not pad the catalog with thin listings.

## 8. Common mistakes

Merged and deduplicated. Each with the fix.

1. Signing up with a contractor's email. Fix: owner email, transfer ownership if already wrong. (01, 04)
2. Skipping the legal name and address step, then failing payments verification. Fix: fill Settings > General first; match documents exactly. (04)
3. Nickname instead of legal name in payments. Fix: exact match; expect a re-review. (04)
4. Choosing a myshopify handle carelessly. Fix: it is permanent; choose with care. (04)
5. Quoting trial or plan prices from a video. Fix: `[web check]`. (01, 08, 09, 10)
6. Launching on the default domain or a pending domain. Fix: custom primary domain that resolves. (08, 09, 10)
7. Editing the live theme, or pulling `--live` with no duplicate. Fix: duplicate first, always. (01, 06, 11, 08)
8. Picking a theme without checking it has the niche-critical section. Fix: section list first, demo check, Try theme. (01)
9. Trusting the AI whole-store generator or an AI page draft as final. Fix: draft only; prune, click, mobile pass. (01, 05, 06, 11)
10. Leaving demo products, categories, "demo store" notices, "Powered by" and "My Store" text. Fix: remove before launch. (02, 07, 09)
11. Mixed image ratios and oversized files. Fix: one ratio, consistent size. (01, 06, 07)
12. Physical product weight toggle off. Fix: toggle on; enter package weight. (01)
13. Package weight unset on calculated rates. Fix: default package with empty weight. (04)
14. Wrong product type (physical marked downloadable). Fix: match type to fulfilment. (03)
15. Variation without a price. Fix: price every row. (02, 05, 07)
16. Product-level attributes instead of global ones. Fix: global attributes first. (02, 03)
17. Tag typos and case drift. Fix: copy-paste tags; bulk edit. (01)
18. Wrong collection type saved (permanent). Fix: recreate the collection. (01)
19. Manual collections left unfed. Fix: add each new product, or use smart collections. (09)
20. Sale price with no end date; fake compare-at. Fix: schedule sales; real former prices only. (03, 10)
21. Continue-selling on with fixed stock; silent backorders. Fix: off unless fulfilment can source. (09, 03)
22. Large inventory number treated as real stock. Fix: confirm supplier stock. (06)
23. Copying supplier descriptions. Fix: write benefit-led copy. (10)
24. Retitling without fixing the URL handle. Fix: update the handle. (01)
25. Publishing policy templates with placeholders or borrowed pages as Terms. Fix: edit every clause; real page; human sign-off. (02, 08, 09, 10)
26. Skipping the shipping policy because there is no template. Fix: write it from the matrix. (08, 09, 10)
27. Linking policies before they are published. Fix: publish first; links appear after. (01, 08)
28. Missing duties disclosure for US and Canada cross-border. Fix: note in policy or duties at checkout. (01, 04)
29. Forcing account creation before checkout. Fix: guest checkout on. (01, 02, 04, 05 card)
30. Requiring both email and phone at contact, or extra fields. Fix: email contact, phone at shipping. (01, 04)
31. Treating fulfilment email as marketing consent; pre-selecting where illegal. Fix: separate checkbox; per-country rules. (01)
32. Two abandoned checkout emails or two order confirmations firing. Fix: one owner per email. (01, 03)
33. Pasting gateway keys in the wrong mode. Fix: match mode and keys; connection test. (02)
34. Forgetting to switch test to live, or leaving test mode on at launch. Fix: R72. (03, 04, 07, 10)
35. Personal PayPal account. Fix: Business account. (05)
36. One payment method only. Fix: add PayPal or a regional method. (10)
37. Gateway silently deactivated for missing verification. Fix: re-check Settings > Payments before launch; real test order. (01)
38. Simulated test order treated as enough. Fix: real order through the real gateway and warehouse. (01)
39. Default shipping zone and rates left in place. Fix: edit or delete to the matrix. (09, 04)
40. Adding a country to a new zone while it sits in another. Fix: remove first. (04)
41. Flat cost assumed to scale with quantity. Fix: `[qty] *` or brackets. (02)
42. Bracket gaps or overlaps. Fix: test every edge. (03)
43. Per order instead of per class on mixed carts. Fix: per class. (05)
44. Free shipping threshold copied from a video. Fix: margin and AOV based. (07, 10)
45. Threshold hidden from shoppers. Fix: announcement bar or cart notice. (03, 10)
46. Shipping worldwide by default. Fix: domestic first, then zones. (10)
47. Guessing tax basis or nexus; one blanket rate for many states; tax priority backwards. Fix: advisor, per-row rates, lower priority wins. (02, 03, 05, 10)
48. Shop price inclusive and checkout exclusive. Fix: one display mode. (03)
49. Tax charged where not intended, discovered after launch. Fix: check before launch; re-check per market. (01, 04)
50. WooCommerce emails not sending. Fix: SMTP before launch. (05)
51. Editing email PHP in the parent theme. Fix: child theme. (03)
52. Installing an app without enabling its embed. Fix: App embeds tab. (01)
53. Installing many apps at once; leaving dormant apps. Fix: 3 at launch; uninstall unused; re-check speed. (01, 04, 10)
54. Choosing apps by marketing claims. Fix: reviews, demo store, support test. (01, 04)
55. Deleting plugins without deactivating; leaving default plugins before a starter import; default role above Subscriber. Fix: R13. (02, 05)
56. Wrong page builder chosen at import. Fix: choose once, deliberately. (07)
57. Bundling several AI changes in one prompt. Fix: one change per prompt; verify each. (11)
58. Blind-approving AI permission prompts. Fix: read each. (08, 11)
59. Store password confused with account password for the preview. Fix: Online Store > Preferences. (08)
60. Custom section with no product selected, or a second file for an update. Fix: select the product; paste over the same file. (06)
61. Trusting the editor preview or the agent's report. Fix: incognito, click everything. (06, 07, 11)
62. Skipping the mobile pass. Fix: real phone before launch. (04, 05, 07, 10)
63. Removing the password before the checklist passes, or never removing it. Fix: 5.1 then remove; launch imperfect after that. (04, 09, 10)
64. Reading one day's analytics or a young cohort report. Fix: multi-month window; a year for cohorts. (01)
65. Patching thin product pages or policies by editing notification emails. Fix: fix the page or policy. (01)
66. Credentials in files or prompts. Fix: secret store; rotate if exposed. (ecomOS)

## 9. Deliverables

### 9.1 Store build brief
Format: one Markdown file per brand at `brands/<brand>/setup/platform-spec.md`. Sections: platform decision and 3 accepted trade-offs (4.1); account owner and email; plan tier and price `[web check]` with date; legal identity block (name, address, business number, payments account type); domain, registrar, DNS records added, primary domain date; theme name, version, duplicate naming rule, paid or free with reason; base currency, backup region, units, order prefix; markets list with currency, rounding, language; staff roles; approval log (who approved each platform write and when). Every value tagged `[needs brand data]` until filled.

### 9.2 Product import sheet spec
Format: CSV or sheet matching the platform importer, one row per variant. Columns: handle, title, short description, long description, vendor, type, category, tags (from the collection plan), status, option1 name and value, option2, option3, SKU, barcode, price, compare-at price, cost per item, charge tax, tax class, track quantity, quantity per location, continue selling when out of stock, low stock threshold, weight, weight unit, package length, width, height, shipping class or package, image URLs in order, image alt text, SEO title, SEO description, collections, upsells, cross-sells, product type flags for WooCommerce (simple, variable, virtual, downloadable, external), download file and expiry, external URL and button text. Validation rules: no variant without a price; one image ratio; unique SKUs; tags exactly matching the collection plan; weight present on every physical row. Checklist 5.2 runs against this sheet.

### 9.3 Shipping and tax matrix
Format: one sheet with two tabs. Shipping tab: zone name, countries or states, fulfilment location, rate name with delivery estimate, rate type (flat, per item, bracket, carrier), price, conditions (value or weight range), free shipping threshold and whether it applies before coupons, shipping classes and per-class costs, package name with dimensions and empty weight, local delivery and pickup settings, tax on shipping. Tax tab: jurisdiction, registered (yes or no), tax ID, rate or "platform service", class, basis (origin or destination), inclusive or exclusive display, duties handling, advisor sign-off name and date. Every rate `[needs brand data]`; every rate reference `[web check]`. Checklist 5.3 runs against it.

### 9.4 Launch checklist with sign-offs
Format: checklist 5.1 as a table with 3 extra columns: result, checked by, date. Plus 4 named sign-offs: legal pages (human with legal knowledge), tax settings (tax advisor), payments live (owner), password removal or Live switch (owner). No launch without all 4.

### 9.5 App stack list
Format: table per brand. Columns: app or plugin name, publisher, job (reviews, email, tracking, search, shipping, tax, SMTP, swatches, security), rating and review count at vetting `[web check]`, Built for Shopify badge, demo store checked, support test result, price and plan `[web check]`, install date, embed enabled, duplicate-job check, removal date if uninstalled, affiliate context of the source that named it. Checklist 5.5 runs against it.

## 10. What needs live data or a web check

### `[needs brand data]`
- Legal business name, registered address, business number or EIN or VAT, owner ID details, payout bank details (entered by the owner, never stored by the agent).
- Owner email, store name, myshopify handle, domain and registrar preference.
- Product catalog per 9.2: titles, copy, images, prices, compare-at, costs, SKUs, stock, weights, package dimensions, variants, tags, categories.
- Collection plan and navigation structure; footer menus.
- Target countries; fulfilment locations; warehouse app.
- Shipping rules per 9.3: rates, free threshold from margin and AOV, transit times, package empty weights, carriers, classes.
- Tax registrations, jurisdictions, inclusive or exclusive decision, tax on shipping rule, advisor.
- Return window, return shipping payer, restocking fee, final sale list.
- Support email and phone; contact page content; About page story.
- Brand assets: logo versions, favicon, palette, fonts (from 04-BRD).
- Policy text: shipping, returns, privacy, terms, contact, legal notice; consent language per country.
- ESP in use (to avoid duplicate abandoned checkout emails); reviews app choice; existing pixel and GA4 property.
- Staff list and roles; agencies needing collaborator access.
- Markets: currencies, rounding rule, per-market prices, languages, translation reviewers.
- AI-assisted build: inspiration folder, framework document, section choices, Claude plan.
- Mobile QA coverage; cost comparison of AI theme work vs developer or app.

### `[web check]`
- Shopify plan names, prices, card rates, seat limits, Plus price; trial terms; legacy account entitlements.
- Theme store filters, current default theme (Horizon, Dawn, Trade named), paid theme prices, Try theme behaviour.
- Shopify domain price; registrar prices and renewals; current DNS connection flow for external domains.
- Shopify Payments availability by country; test card numbers; verification times; deposit types; wallet options; regional gateways (Klarna, Tabby, COD) and their names.
- Shipping label availability and insurance terms per plan; carrier-calculated rate availability.
- Tax rates per jurisdiction; origin vs destination state list; states taxing shipping; nexus and EU VAT thresholds; WooCommerce Tax plugin status and cost; TaxJar references.
- Markets availability on Basic; per-market theme customization gating; Translate and Adapt free tier.
- App prices and ratings: Judge.me, Loox, Stamped, Yotpo, Klaviyo, Omnisend, Gorgias, Tidio, label apps; Built for Shopify badge presence.
- WooCommerce and WordPress UI labels; WooCommerce zone matching order; shortcode names; Elementor stable version; Blocksy and Astra starter site flows; SMTP and email builder plugin names; Payment Plugins vs official Stripe and PayPal plugin status; PayPal Business requirements; Stripe fees.
- Hostinger plans, prices, term discounts, verification window; at least one alternative host.
- Shopify CLI install command; Claude Code install commands for Windows and Mac; Claude plan that includes Claude Code and its price; usage limits; Sidekick capabilities; AI section generator behaviour.
- Consent pre-selection rules per country; cookie consent and accessibility requirements (gap in all sources).
- Any industry statistic from source 04 before it appears in client material.

## 11. Freshness and stale-risk notes

| Area | Why it goes stale | Re-verify |
|---|---|---|
| Shopify admin paths and labels (Settings, Markets in sidebar vs Settings, Checkout, Customer accounts, Policies, Preferences) | Source 01 records a mid-recording "Winter Edition" update; sources say screens change without notice | Before every build; every quarter for the playbook |
| Shopify plans, prices, card rates, seats, trial offers | Promo trials and tier names change; all quoted through affiliate links | Same day as any quote |
| Shopify features flagged "new" or "rolling out": passwordless accounts, return rules, quantity limits, per-market theme edits, ChatGPT listing, AI section generator, Sidekick scope | Rollout is staged by country and plan | Before relying on any of them |
| WooCommerce settings screens, zone matching, tax rows, email toggles | Plugin releases; source 02 pinned Elementor 3.33.6 against an unstable 4.0.1; source 05 saw Atomic Editor land mid-recording | Before every build; check plugin changelogs |
| WordPress plugins named (Payment Plugins, WooCommerce Stripe, PayPal Payments, WooCommerce Tax, Flexible Shipping, Variation Swatches, Blocksy Companion, Astra Starter Templates, ElementsKit, Metform, Classic Widgets) | Ownership, maintenance and ratings change; some names are transcribed from audio | Before install; check publisher and last update |
| Hosting plans and prices | Daily promos; affiliate coupons | Same day as any quote; compare 2 hosts |
| Tax rates, nexus rules, EU VAT thresholds, states taxing shipping | Law changes | Before launch; each new market; annually with the advisor |
| Payment gateway availability and regional methods | Country rollouts | Before launch; each new market |
| App prices and features (Judge.me, Loox, Klaviyo, Omnisend, label apps) | Pricing tiers move | Before install; annually |
| AI tooling: Shopify CLI commands, Claude Code install, plan requirements, usage limits, Sidekick capabilities, VS Code extension | Monthly release cycle; source 11 says "typing is so 2025" | Before every AI session |
| Industry statistics in source 04 | Unsourced | Do not reuse without a current source |
| Theme names (Horizon, Dawn, Trade) and default theme | Shopify rotates defaults | Before theme selection |

Rules least likely to go stale: R5 (owner email), R6 (identity first), R27 (duplicate first), R32 (product type discipline), R42 (price every variation), R57 (edit templates), R70 (test then live), R73 (rate per country), R86 (obligations first), R95 (guest checkout on), R124 (saved is not proven), R131 (one change at a time).

24 Sep 2026: ecommerce specificity pass applied from ECOM_REVIEW.md; priority block added, 15 rules reworded, 8 levers added, about 380 words moved to Appendix A.

## 12. Source index

| No. | Title | Type | Credibility and bias | Contributed most |
|---|---|---|---|---|
| 01 | Shopify for Beginners: Everything From Setup to Your First Sale | Course transcript, 124 cards, 79k words | Unnamed practitioner with client work; opinions flagged as opinions; Shopify affiliate link and a lead-magnet guide; features dated to a specific Shopify release window. Rating: high on click paths, medium on advice, no data | The deepest Shopify walkthrough: settings, products, collections, filters, theme trial and duplicate, checkout fields and consent, markets, languages, gateways by region, shipping zones, tax preference, pre-launch real orders, notifications, support, analytics |
| 02 | WooCommerce Tutorial 2026: Complete MasterClass | Course transcript, 72 cards, 44k words | Freelance developer Tim Nishad; Hostinger affiliate with coupon; two paid template marketplaces; Elementor version pinned; no results. Rating: medium on WooCommerce mechanics, low on numbers | WooCommerce General, Products, Tax rows with priority, shipping per item formula and classes, Payment Plugins for Stripe and PayPal with connection test, Accounts and emails, all 4 product types, coupons, end-to-end test, site visibility |
| 03 | How To Start an Online Store That Runs on Autopilot (WooCommerce) | Tutorial transcript, 47 cards, 25k words | Ferdy Korpershoek; declares affiliate income on Hostinger, Blocksy Pro, Elementor Pro; probable affiliate on TaxJar and OmniSend; demo values only. Rating: medium on mechanics, low on numbers, email half routed to 14-EML | Product type discipline, table-rate brackets without gaps, tax classes and consistent inclusive display, AI-drafted legal pages with a Legal footer menu, test mode first then live, email branding in a child theme, currency does not convert prices |
| 04 | The OFFICIAL Shopify 2026 Tutorial | Shopify vendor tutorial, 53 cards, 18k words | Shopify's Learn with Shopify channel; favours Shopify-built tools; several unsourced stats; explicit tax disclaimer. Rating: high on platform mechanics, biased on tool choice, low on stats | Identity first, exact legal match, 2FA before payments, one zone per country, package weights, setup order, test mode order as the launch gate, returns and self-serve, tax by presence, tracking verification, app vetting bar, sales channel prerequisites |
| 05 | WooCommerce Tutorial for Beginners 2026 | Tutorial transcript, 34 cards, 18k words | Daryl Wilson; Hostinger affiliate with coupon; opinions flagged; guest checkout line ambiguous in transcript, resolved by its card. Rating: medium on mechanics, low on numbers | Origin vs destination tax basis, per-class shipping calculation, automated tax plugin, SMTP gap, Shop country default location, no cart redirect, Blocksy and Elementor import, test card checkout |
| 06 | Claude and Shopify Built $750k/m AI Powered Ecom Brand | Promotional tutorial, 27 cards, 15k words | Sells the presenter's white-label program and tools; revenue claim is a third-party tool's estimate of another brand; no independent evidence. Rating: low on claims, medium on the narrow Liquid section click path | Custom Liquid section via Edit Code on a duplicate, template assignment, select the product in section settings, inventory is not stock, incognito QA and clicking every element, paste over the same file, branded PDP vs unbranded product warning |
| 07 | How to Create an Ecommerce Website with WordPress 2026 | Tutorial transcript, 25 cards, 11k words | Dale (Creator Pro); Hostinger affiliate with coupon; no tax or legal coverage. Rating: medium on WooCommerce mechanics, low on numbers | Builder choice at import, test to live re-verification reading "Live", free shipping above flat rate ordering and coupon interaction, welcome coupon per-user limit, category slugs and parents, product duplication, coming soon to live with incognito check |
| 08 | How to Build a Full Shopify Store using AI (Claude Code) | Sponsored tutorial, 12 cards, 10k words | Shopify affiliate deal; kickoff prompt and Shopify-knowledge command withheld in an external guide; pulls the live theme with no duplicate. Rating: medium on toolchain steps, low on safety practice | Toolchain install, `shopify theme pull`, inspiration folder, interview then section-by-section build, local dev server and store password, push unpublished then edit in the theme editor, policies must exist for footer links, back-office steps |
| 09 | Shopify Tutorial for Beginners 2026: Full Store Setup Guide | Tutorial transcript, 8 cards, 8k words | Simon; Shopify affiliate trial link; opinions; curator skip notes on the trial link and the ChatGPT shipping policy aside. Rating: medium on click paths, low on advice | Delete default shipping zone, weight fields only when rates use them (conflict 7.9), continue selling by fulfilment ability, manual collections are unfed, policies with no shipping template, backend launch order |
| 10 | Shopify Store Setup Full Tutorial 2026: Step by Step | Tutorial transcript, 20 cards, 8k words | Unnamed; "every tool and link is in the description"; conversion claims stated as fact without data. Rating: medium on sequencing, low on claims | Domain naming filters and Shopify vs registrar trade-off, free theme default, template text never final, two payment methods, shipping simple then expand, tax obligations first, 3 apps at launch, Test Order Protocol, pre-launch checklist, launch imperfect |
| 11 | Claude Just Changed Shopify Forever | Tutorial transcript, 10 cards, 5k words | Academy owner selling a product page framework; single demo; capability claims shown once. Rating: medium on the safe AI workflow, low on capability guarantees | Duplicate before any AI edit and re-duplicate each round, human runs `shopify auth login`, list themes to confirm the connection, one change per prompt, verify each part, usage limits, clone competitor patterns not content, publish flow |

**Neighbour folders and what lives there**

- 01-PRD: product validation and competitor scoring (source 06's validator).
- 04-BRD: logo, palette, fonts, brand board, brand reference guide (sources 03, 04, 06, 10).
- 06-MEA: pixels, GA4 events, UTM rules, attribution, funnel reports (sources 01, 04).
- 07-LPG: homepage and PDP layout, page builders, hero and section design, cart drawer vs page, responsive passes, checkout UX beyond settings (all sources' design halves).
- 08-SPD: speed, image compression, app weight (sources 01, 04).
- 13-ORG: organic social launch content (source 04).
- 14-EML: welcome, abandoned cart, segmentation, ESP setup, Shopify Messaging (sources 01, 03, 04, 10).
- 15-SEO: SEO beyond the baseline fields, blogs, Search Console (sources 01, 02, 03, 04).
- 18-COG: sourcing, dropship vs private label, packaging (source 06).
- 23-SEC: security hardening, backups and restore drills, cookie consent and data handling (gaps in 02, 05, 07, 10).

## Appendix A. General background

Moved here by the 24 Sep 2026 ecommerce specificity pass. This is generic account, hosting or AI-agent hygiene that reads the same for any web project, not a store-specific rule. Kept for completeness; the rule id stays live at its original spot as a pointer.

**R16 (from 3.3 Domain and DNS).** Check domain availability when the brand name is chosen, before it is final. Prefer .com. Keep it to 1 or 2 words, no hyphens or numbers, easy to spell (opinion, 10). Consider buying other extensions defensively (01). Do not overthink it (10). Sources: 01, 02, 10. [b30915400ab6] [8936916fd085]

**R18 (from 3.3 Domain and DNS).** Set the custom domain as primary, wait for propagation, and test it in a browser before removing the password. "Pending" for a few hours is normal (10); up to 24 hours is possible (03, 07). "Connected" in admin is not proof; the URL must resolve (04). Sources: 04, 10, 03, 07. [4f9700a6e477] [d6854b97be2c] [7ad023a56f5a] [359dabdafbc0]

**R19 (from 3.3 Domain and DNS).** Do not launch on the default myshopify.com or a host's temporary domain. Treated as a professionalism and trust liability by 3 sources (opinion). Sources: 08, 09, 10. [4ad69ffecb22] [8936916fd085]

**R21 (from 3.3 Domain and DNS).** On WordPress hosting, verify the account email and the domain email, and confirm Force HTTPS is on. Source 05 says an unverified Hostinger account is refunded and closed after 30 days `[web check]`. HTTPS is the only security step the WooCommerce sources give; the rest routes to 23-SEC. Sources: 02, 05, 03. [2946d83f30cb] [359dabdafbc0]

**WordPress fresh-install cleanup click list (from procedure 4.14 step 5).** Screen Options off; Plugins > select all > Deactivate > then Delete (keep the host's caching plugin if present); Pages and Posts > trash and empty; Appearance > Themes > delete all but one; Settings > General: title, tagline, timezone, Anyone can register on, default role Subscriber; Settings > Permalinks > Post name; Settings > Discussion > disable comments if no blog; Users > Profile: display name. This is the mechanical click path behind R13; R13's own store-framed rewrite stays in section 3.2.

**R117 (from 3.14 Staff, permissions, security and backups).** Two-step authentication on the owner account before payments; recovery codes in the secret store. Sources: 04. [0949813570ce]

**R118 (from 3.14 Staff, permissions, security and backups).** On WordPress, new user default role is Subscriber, never Editor or Administrator; delete unused plugins and themes; keep Force HTTPS on. Sources: 02, 03, 05. [f66e3a492886] [16eefae8f3dd] [2946d83f30cb]

**R120 (from 3.14 Staff, permissions, security and backups).** When an AI agent runs commands, read each permission prompt; do not blind-approve. Sources: 08, 11. [13e82e14fdd0] [cf190b41088d]

**R138 (from 3.17 AI-assisted setup).** Expect usage limits in long sessions (one presenter hit a 90% warning and waited about an hour `[web check]`); do not treat the agent's success report as proof, verify on the storefront. Sources: 11. [af0b1c693102] [2068dc8e74a9]

**R139 (from 3.17 AI-assisted setup).** Sidekick vs Claude Code: source 11 says Sidekick only generates sections while Claude Code builds blocks and templates; source 04 and 01 use Sidekick for finding settings, drafts and data questions. Verify current capabilities before repeating the comparison `[web check]`. Sources: 04, 01, 11. [d32ab6d8ae7a] [e431785d2758] [2068dc8e74a9]
