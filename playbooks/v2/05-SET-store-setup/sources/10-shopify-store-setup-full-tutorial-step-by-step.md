# Shopify Store Setup Full Tutorial 2026: Step by Step

source_id: 1ljIAr2ylUWZvpnQdDsCM3ObyPshKXZE4  |  folder: /05-SET-store-setup  |  cards: 20  |  words: 7,646  |  type: video tutorial transcript
credibility: Spoken YouTube walkthrough by an unnamed creator narrating a live Shopify build. No client data, no test results, no company named. Evidence is entirely the presenter's own opinion and repeated assertions ("clarity always performs better," "white backgrounds convert better") stated as fact but not backed by studies or numbers. The presenter says every tool and link used is in the video description, which is a strong signal of affiliate links on the domain registrar, theme, and app recommendations named below; treat those recommendations as possibly commercially motivated. `[web check: does this creator disclose affiliate relationships]`
date signals: Title says "2026." Trial offer described as 3 days free then 3 months at $1/month (~96% off) `[web check: current Shopify trial and pricing]`. Paid themes cited at $200-$400 `[web check: current Shopify theme store pricing]`. Names Shopify's AI writing assistant (sparkle icon), AI section recommendations in the theme editor, and free themes Dawn, Horizon and Trade, all consistent with the Shopify admin as it stood in 2025-2026. Source metadata shows the document was last modified 2026-09-19. Admin menu labels, plan names and AI features are exactly the kind of thing Shopify changes without notice; re-verify before following any UI path literally.
note: the exported text includes curator scope notes for two folders (05-SET and 07-LPG) ahead of the actual transcript, because this one video covers both backend setup and storefront design. Those notes are curation metadata, not the presenter's words; the actual transcript starts at "If you're watching this right now..." This mini playbook draws on the transcript and the 20 cards built from it.

## 1. What this source is for

A single continuous walkthrough for taking a brand-new Shopify account from signup to a public, password-removed store. It covers plan selection, domain, theme install and customization, branding (logo, colors, fonts), navigation, homepage sections, adding the first product and collections, policies, payments, shipping, taxes, a lean app stack, and a pre-launch checklist. It is a sequencing guide for a first-time solo builder, not a strategy or optimization source: use it to know what order to do things in and what to check before going live.

## 2. Principles

1. Reduce admin overwhelm to three areas first: Products (add and manage items), Online Store (design, theme, pages, navigation) and Settings (payments, shipping, taxes, store config). Condition: true for orienting a brand-new store; do not use it as a reason to ignore Orders, Discounts or Analytics once live. Evidence: source's own framing that these three "cover almost everything that matters." [d082e7bbfa8a]
2. A store is technically live but password-protected at signup, so setup is optimization of an existing shell, not a build from zero. Condition: always true for new Shopify signups per the source. [d082e7bbfa8a]
3. Domain quality affects trust before a visitor reads any product content. Condition: applies wherever the URL is visible (ads, email, packaging, social bio). Evidence: source's example of a long messy `.myshopify.com` URL creating hesitation on an ad click. [8936916fd085]
4. Most beginners do not need a paid theme. Condition: unless the business specifically needs a paid theme's built-in features. Evidence: source claims free themes now offer clean layouts, mobile optimization and fast load speed, and that speed is critical because slow stores lose mobile visitors. [6d9a16a8c9c4]
5. Simplicity beats decoration across fonts, colors, and menus. Condition: theme typography, color contrast, and navigation depth. Evidence: source repeats that decorative fonts and long menus hurt because customers who struggle to read or choose will leave; no data cited, opinion only. [ba017a5df345][f4d27950fb54][2c5b09996536]
6. A default installed theme still looks generic; stopping there is a named mistake. Condition: right after publishing a theme, before any customization. [6d9a16a8c9c4][ba017a5df345]
7. Templates (legal policies, AI-drafted product/hero copy) are starting points, never final text. Condition: every use of Shopify's policy templates or an AI drafting prompt. Evidence: source explicitly warns "never copy blindly," and that a policy or description must match the real business or it creates the exact disputes/trust problems it exists to prevent. [f1706731ed68][f330630b1382]
8. Perceived-value pricing (compare-at) only works when the discount is real. Condition: setting a "compare at" price alongside the sale price. Evidence: source calls overstated discounts a credibility risk, without giving a specific ratio limit. [6aec7830e90b]
9. Testimonials and an FAQ can go live before the store has real customers. Condition: pre-launch. Evidence: source explicitly allows honest feedback from friends/early testers as placeholder social proof, not fabricated reviews. [c0d455504772]
10. One payment method is a common beginner mistake; add a fallback. Condition: before removing password protection. Evidence: source frames Shopify Payments plus PayPal as reducing friction and helping international buyers who prefer a familiar option. [6d507ac44e12]
11. Start shipping simple, then expand. Condition: initial launch. Evidence: source says shipping worldwide "sounds attractive" but adds complexity, and recommends flat rate over dynamic/carrier-calculated rates for beginners because it is easier to manage. [6d62360a1568]
12. Tax automation requires you to establish your own obligations first. Condition: before or immediately after enabling Shopify's automatic tax collection. Evidence: source explicitly defers to local law/US state nexus rules/EU VAT thresholds and recommends a tax professional when unsure. [25d24521b0ed]
13. Fewer apps protect site speed, and site speed affects conversion. Condition: at launch. Evidence: source's rule of thumb is 3 apps (review, email, tracking), expand only when the business needs more. [f07ede1e5f57]
14. A pre-launch checklist catches small errors that become large post-launch problems. Condition: the step immediately before removing password protection. [728fa86b4907]
15. Launching imperfect and collecting feedback beats endless pre-launch polishing. Condition: after the checklist passes. Evidence: source's explicit closing framing, "the goal isn't perfection... it's progress." [f7d6a3b222e4]

## 3. Procedures

All admin paths are Shopify's UI as narrated in this 2026 video and are tagged `[verify UI]` since Shopify admin layouts change. Steps are given in the order the source performs them.

**A. Account creation and plan** [4a154ed3a11d]
1. Go to Shopify's official website, enter an email, click "start free trial," create a password, complete signup.
2. Shopify redirects to a promotional offer: as described, 3 months at $1/month after an initial 3-day free trial (~96% off) `[web check: verify this offer still exists and its terms]`.
3. Either activate the discounted plan immediately, or first complete the short business setup questions (source says ~20 seconds), then land on the dashboard.
4. If the discount offer is skipped during signup, the source says it can still be claimed from the lower-left corner of the dashboard, but only before the initial 3-day free trial expires. `[web check]`
5. Pick the Basic plan for a first store (source's claim: it covers launch, payments and a functional store); upgrade later as needed. `[web check: current plan names/tiers, e.g. Basic, Grow, Advanced, Plus]`

**B. Dashboard orientation** [d082e7bbfa8a]
1. Note the main menu: Orders, Products, Customers, Marketing, Discounts, Content, Markets, Analytics. `[verify UI]`
2. Focus first on Products, Online Store, and Settings (see Principle 1).

**C. Domain** [8936916fd085][7ad023a56f5a]
1. Ideate names with AI: prompt example "generate 20 brandable domain names for a fitness apparel store."
2. Apply filters: 1-2 words max; no hyphens or numbers; no unusual/hard-to-spell names; brandable over generic (source contrasts generic descriptors with names like Gymshark, Allbirds, Glossier as its bar for "brandable" — these are the source's illustrations, not verified performance data).
3. To buy new through Shopify: Settings > Domains > buy new domain > search name > purchase if available. Connects automatically, no manual DNS. `[verify UI]`
4. To connect an existing domain (e.g. bought at GoDaddy): Settings > Domains > connect existing domain. Shopify supplies DNS records; copy them into the registrar's DNS settings; save. `[verify UI]`
5. Expect propagation to take a few hours; "pending" status during that window is normal, not a failure.
6. Trade-off noted: third-party registrars (source names GoDaddy) may have lower first-year price but higher renewals `[web check: current registrar and Shopify domain pricing]`; buying through Shopify is called the smoother beginner path.
7. Confirm domain shows "Connected" before publishing.

**D. Theme selection and install** [6d9a16a8c9c4]
1. Online Store > Themes > scroll to explore free themes. `[verify UI]`
2. Named free themes: Dawn (minimal/versatile — fashion, beauty, general stores), Horizon (modern/bold — stronger visual impact), Trade (built for large catalogs). `[web check: are these still Shopify's current free theme names]`
3. Click the theme, select "view demo," preview before installing.
4. If it fits, click "add to theme library," then "publish." Storefront updates within seconds.
5. Paid themes cited at $200-$400 with extra built-in features `[web check]`; most beginners don't need one per the source.
6. Theme choice is reversible; don't over-analyze.

**E. Theme customization: brand foundation** [ba017a5df345]
1. Open "Edit theme." Left panel = sections, right panel = live preview.
2. Start with header structure/alignment even without a final logo.
3. Theme settings > Colors: set the primary brand color, keep background white for now (source's opinion: white backgrounds convert better because products stand out).
4. Typography settings: choose simple, readable fonts. Named examples: Montserrat, Source Sans Pro. Avoid decorative fonts.
5. Optionally use AI section recommendations in the theme editor: describe the brand in a few sentences to get layout suggestions.
6. Logo: generate with an AI image tool (example prompt: "create a minimalist logo for a skincare brand called Pure Glow. It's modern, luxury, and bold") or a free logo tool; text-based logos work well.
7. Remove the logo's background with a free tool named as an example: remove.bg. Download a transparent PNG before uploading, to avoid a messy white/colored box behind the logo (named beginner mistake).
8. Upload the logo via header/theme settings; adjust size to balanced (not oversized or tiny).
9. Optional cohesive palette: ask AI for "a modern color palette for a fitness brand" to get primary/secondary/accent hex codes; paste primary hex into the color field; keep contrast high for legibility.

**F. Header, menu style, announcement bar** [f4d27950fb54]
1. In theme editor, click header; choose logo position (left or center).
2. Choose menu style by catalog size: drawer menu for heavy mobile traffic, dropdown for smaller catalogs, mega menu for large catalogs with many categories.
3. Keep the menu short (source: too many items create confusion).
4. Enable the announcement bar with a benefit-led message. Examples given: "free shipping on orders over $50," "limited time launch sale." `[needs brand data: real shipping threshold and any live promotion]`
5. Refresh preview; re-check in mobile view.

**G. Hero banner** [c479568fefa4]
1. Get an image direction from AI: example prompt "produce a hero banner image that matches this brand."
2. Use Shopify's built-in free image library: click hero section > select image > explore free images > search niche keywords. Use high-resolution images only.
3. Write a benefit/outcome headline, not a product name. Example given: "confidence starts with skin."
4. Add one short supporting subtext sentence.
5. Add a CTA button (examples: "Shop now," "Explore collection"). Never leave the banner without a button.
6. Set the homepage hero heading to an H1 tag for SEO structure.
7. Preview on mobile; if the headline blends into the image, add a subtle overlay for contrast.

**H. About page and policies** [f1706731ed68]
1. Online Store > Pages > add page > About Us. Keep it simple: why the brand started, who it serves, what makes it different. `[needs brand data: founder story, positioning]`
2. Settings > Policies > create from template for Privacy Policy, Terms of Service, Shipping Policy, Refund Policy. `[verify UI]`
3. Read every generated policy and edit it to match the real business; do not publish unedited defaults.
4. Write real shipping terms (delivery windows, handling time, conditions); the source calls skipping this detail a common cause of disputes and refunds. `[needs brand data: actual delivery times and carriers]`
5. Decide the refund window (in days) and who pays return shipping. `[needs brand data: real return policy terms]`
6. Optional AI drafting prompts given as examples: "write a simple shipping policy for this brand," "write a simple refund policy for this brand" — then replace every placeholder with real terms.
7. Shopify places saved policies in the footer automatically.

**I. First product** [f330630b1382][6aec7830e90b]
1. Products > Add product.
2. Write a simple, specific title.
3. Do not copy supplier descriptions (source: this reads as generic and lowers trust).
4. Write to benefits, not just features, in short scannable paragraphs.
5. Optional: click the sparkle icon in the description box for Shopify's AI writing assistant to draft copy, then edit to match brand voice. `[verify UI]`
6. Set Price and Compare at price. Worked example: price $49, compare-at $79 (displays crossed out for perceived value). Keep the gap realistic.
7. Inventory: enable "Track quantity," enter available stock to avoid overselling. Dropshippers may disable tracking, but the source still recommends tracking to prevent order issues.
8. Configure physical package dimensions so shipping calculations have accurate inputs.
9. If the product has options (size, color), click "add options," create variants (example: small, medium, large).
10. Add product tags for grouping/search, and for smart-collection rules later.
11. Upload photos at least 1000x1000 pixels; zoom in to check for blur; replace anything low quality. Order images so the first is the clearest.
12. Scroll to the search engine listing preview; set page title with the main keyword and a concise meta description.

**J. Collections** [aa204dc3c45e]
1. Products > Collections > Create collection; name it clearly.
2. Choose manual (hand-pick products) or automatic/smart (rule-based grouping; saves time as the store grows — but depends on consistent product tags).
3. Add a collection image and short description.
4. Homepage > theme editor > add a section that features the collection; select the correct category.
5. Preview to confirm products are visible in the storefront, not just the backend.

**K. Navigation** [2c5b09996536]
1. Online Store > Navigation > open main menu. `[verify UI]`
2. Remove default links that add no shopping path (home, catalog, contact, as named defaults).
3. Add menu item > name it > link > choose Collections > select the matching collection > save. Repeat for main categories.
4. Limit total links.
5. Switch to mobile preview; check spacing, dropdown behavior, crowding.
6. Click every link, submenu, and collection to confirm no broken paths.
7. Confirm policy/support pages are reachable from the footer.

**L. Homepage section order** [c0d455504772]
1. Homepage in theme editor > Add section.
2. Add testimonials (even a few short quotes; pre-launch friend/tester feedback is acceptable if honestly labeled).
3. Add an FAQ (shipping times, returns, sizing).
4. Confirm the top-to-bottom order: hero > collections > featured products > trust elements (testimonials, FAQ).
5. Re-check the same order/spacing in mobile view.

**M. Payments** [6d507ac44e12]
1. In admin, find Shopify Payments > choose a provider > complete setup (connects payouts to a bank account; enables major cards without third-party integration). `[verify UI]`
2. Add at least one alternative method: enable PayPal (often already linked to the account email, or click activate PayPal > log in > grant permissions, ~1 minute per the source).
3. Check what gateways are available in your specific region/country before assuming Shopify Payments and PayPal both work everywhere. `[web check: gateway availability by region]`

**N. Shipping** [6d62360a1568]
1. Settings > Shipping and delivery > open primary zone > define countries actually shipped to (domestic-only vs. worldwide). `[verify UI]` `[needs brand data: actual fulfillment countries/carriers]`
2. Choose pricing model: flat rate (single fixed charge, source recommends for beginners) vs. dynamic/carrier-calculated (real-time by weight and carrier).
3. Consider a free-shipping threshold. Worked example: free over $75, argued to lift average order value by encouraging add-to-cart behavior. `[needs brand data: real margin-based threshold]`
4. For international shipping, create separate zones with higher flat rates or calculated rates.
5. Add a handling buffer where relevant. Worked example given: about $5.
6. State delivery times clearly everywhere shipping is mentioned.

**O. Taxes** [25d24521b0ed]
1. Settings > Taxes and duties. `[verify UI]`
2. Verify your own obligations under local law before relying on automation. `[needs brand data: business registration location, nexus/VAT status]`
3. Enable automatic tax collection; review the rates configured for your region.
4. US: review state nexus rules to determine sales-tax collection duty.
5. EU: check VAT requirements and registration thresholds.
6. Consult a tax professional if unsure; source calls mistakes here potentially expensive.

**P. Contact page** 
1. Online Store > Pages > add page > "Contact us." Add a business email; most themes include a contact form by default. `[needs brand data: real support email]`

**Q. Apps** [f07ede1e5f57]
1. Apps > Shopify App Store > search only for essential tools. `[verify UI]`
2. Source's rule: 3 apps at launch — a review app, an email app, a tracking/analytics app (analytics app is not named specifically in the source; thin on which one).
3. Review app options named: Judge.me (strong free plan, per source) vs. Loox (focused on photo-based reviews). `[web check: current pricing/features of both]`
4. Enable automatic post-purchase review request emails.
5. Install a tracking/analytics app to see traffic sources, top products, and drop-off points.
6. Avoid installing many apps at once; each one adds page weight and can hurt site speed and conversion.

**R. Pre-launch checklist** [728fa86b4907]
1. Settings > Store details: confirm business name, email, and store currency match the target market. `[verify UI]` `[needs brand data: legal business name, support email, target market currency]`
2. Settings > Domains: confirm status is "Connected," not "pending."
3. Payments: enable test mode, place a test order, complete the full checkout, confirm the order confirmation email actually arrives, then disable test mode. (Named in the source as "The Test Order Protocol.")
4. Review the store on an actual phone: scroll, tap every button, add to cart, complete checkout.
5. Open every footer policy page; read the first paragraph; confirm the real business name appears and no placeholder text remains.
6. Click every menu item, submenu, and collection to confirm nothing is broken.

**S. Launch** [f7d6a3b222e4]
1. Online Store > click "remove password." Store becomes publicly accessible with no restriction. `[verify UI]`
2. Online Store > Themes: confirm the current theme shows as "live"; if not, publish and confirm.
3. Enable the email and SMS marketing opt-in checkboxes at the checkout/sign-in step to capture consent directly. `[needs brand data: which consent language and opt-in mechanics your jurisdiction requires]`
4. Open a new browser tab, type the live domain manually, and browse as a first-time visitor: homepage, product page, add to cart, checkout.
5. Start distributing the link (social bio, direct messages) and collect feedback rather than continuing to polish.

## 4. Rules, thresholds and numbers

| Rule / figure | Number or threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Free trial then promo | 3-day free trial, then 3 months at $1/month (~96% off) | Must claim before the 3-day trial ends | Presenter's on-screen walkthrough `[web check]` | 4a154ed3a11d |
| Business setup questions | ~20 seconds | During signup flow | Presenter's estimate | 4a154ed3a11d |
| Domain length | 1-2 words max | Choosing a domain | Presenter's rule of thumb, no data | 8936916fd085 |
| Domain propagation | "a few hours" | After connecting/buying a domain | Presenter's estimate | 7ad023a56f5a |
| Paid theme price | $200-$400 | Considering a premium theme | Presenter's figure `[web check]` | 6d9a16a8c9c4 |
| Product image minimum | 1000 x 1000 px | Uploading product photos | Presenter's minimum, not a platform requirement | 6aec7830e90b |
| Compare-at example | $49 price / $79 compare-at | Illustrating perceived-value pricing | Presenter's worked example, not a ratio rule | 6aec7830e90b |
| Free shipping threshold example | Free over $75 (also "$50" used in an announcement-bar example) | Illustrating AOV-lifting threshold | Presenter's examples, not benchmarks | 6d62360a1568 / f4d27950fb54 |
| Handling buffer example | ~$5 | Adding a shipping handling fee | Presenter's example | 6d62360a1568 |
| PayPal activation time | ~1 minute | Enabling PayPal if not already linked | Presenter's estimate | 6d507ac44e12 |
| Lean app count | 3 apps (review, email, tracking) | At initial launch | Presenter's rule of thumb | f07ede1e5f57 |

## 5. Diagnostics and checks

- Store details check: business name, email, and currency correct in Settings > Store details. Bad = wrong currency, which the source says causes checkout confusion and abandonment. Fix: correct currency to match target market. [728fa86b4907]
- Domain check: Settings > Domains should read "Connected." Bad = "pending" for longer than a few hours; action = wait for DNS propagation, don't launch on a broken domain. [728fa86b4907]
- Payment check ("Test Order Protocol"): enable test mode, place a test order, confirm the order confirmation email arrives, then disable test mode. Bad = no confirmation email or failed test transaction; fix before removing password. [728fa86b4907]
- Mobile check: open the live/preview store on an actual phone, scroll, tap every button, add to cart, complete checkout. Bad = cramped nav, text blending into images, awkward tap targets; fix before launch. [728fa86b4907][f4d27950fb54][c479568fefa4]
- Policy check: open every footer policy page, read the first paragraph. Bad = placeholder text or wrong business name; fix by re-editing the template. [728fa86b4907]
- Navigation check: click every menu item, submenu, and collection link. Bad = broken or empty destination; fix the link or remove it. [728fa86b4907][2c5b09996536]
- Theme-live check: Online Store > Themes should show the intended theme as "live." Bad = an old/default theme still marked live; fix by publishing the correct one. [f7d6a3b222e4]

## 6. Tools, settings and named features

- Shopify plans: Basic, Grow, Advanced, Plus named as the tier list. `[web check: current tier names/prices]`
- ChatGPT (or "any AI image tool" for logos): used for domain-name ideation, logo generation, color-palette hex generation, hero-image direction, and drafting shipping/refund policy text. Not a Shopify-native tool.
- remove.bg: named specifically for stripping logo backgrounds to a transparent PNG. `[verify UI: tool interface may change]`
- Shopify's AI writing assistant (sparkle icon in the product description box): drafts product descriptions from a short input. `[verify UI]`
- AI section recommendations (inside the theme editor): generates layout suggestions from a brand description. `[verify UI]`
- Free themes: Dawn, Horizon, Trade. `[web check: still current]`
- Fonts named as "simple, readable": Montserrat, Source Sans Pro.
- Shopify's built-in free stock image library (inside the hero/section image picker). `[verify UI]`
- Shopify Payments (native gateway) and PayPal (alternate gateway).
- GoDaddy: named as an example third-party domain registrar alternative to buying through Shopify.
- Review apps: Judge.me (source's pick for strongest free plan) and Loox (photo-based reviews). `[web check: current pricing/plans]`
- Tracking/analytics app: referenced generically ("search for an analytics or tracking app"), no specific product named — source is thin here.
- Affiliate note: the presenter states "every tool and link that I use is in the description below," which is a standard affiliate-link disclosure pattern for domain registrars, themes, and apps named in the video. Treat every named tool (GoDaddy, Judge.me, Loox, remove.bg, any AI tool) as a possible affiliate recommendation, not a neutral endorsement. `[web check: verify current independent reviews/pricing before recommending to a brand]`

## 7. Examples and case results

All of the following are the presenter's illustrative examples during a live demo, not case studies or verified outcomes:
- Domain ideation prompt: "generate 20 brandable domain names for a fitness apparel store." [8936916fd085]
- Logo prompt: "create a minimalist logo for a skincare brand called Pure Glow. It's modern, luxury, and bold." [ba017a5df345]
- Color palette prompt: "create a modern color palette for a fitness brand" (yields primary/secondary/accent hex codes). [ba017a5df345]
- Hero image prompt: "produce a hero banner image that matches this brand." [c479568fefa4]
- Hero headline: "confidence starts with skin" (used as an example of benefit-first copy for a skincare brand). [c479568fefa4]
- Announcement bar copy: "free shipping on orders over $50" and "limited time launch sale." [f4d27950fb54]
- Compare-at pricing: product priced at $49, compare-at shown at $79. [6aec7830e90b]
- Free shipping threshold: "free shipping on orders over $75." [6d62360a1568]
- Handling buffer: "about $5." [6d62360a1568]
- Trial pricing: 3-day free trial, then 3 months at $1/month, described as ~96% off, for a total of $3 across 90 days. [4a154ed3a11d] `[web check]`
- "over six million online stores" cited as Shopify's scale/adoption claim, used to argue platform stability — not sourced. `[web check]`

## 8. Mistakes the source warns about

- Overthinking the domain name in search of something flawless and unused instead of clean and easy to spell. [8936916fd085]
- Stopping at the default installed theme without customizing colors, fonts, and logo. [6d9a16a8c9c4][ba017a5df345]
- Uploading a logo with a messy (non-transparent) background. [ba017a5df345]
- Using decorative fonts that hurt readability. [ba017a5df345]
- Putting too many items in the main menu, creating decision fatigue. [f4d27950fb54][2c5b09996536]
- Leaving a hero banner without a CTA button. [c479568fefa4]
- Copying legal policy templates without customizing them to the real business. [f1706731ed68]
- Ignoring shipping-policy details, leading to disputes and unnecessary refunds. [f1706731ed68]
- Copying supplier product descriptions verbatim. [f330630b1382]
- Overstating the compare-at discount, which reduces credibility. [6aec7830e90b]
- Activating only one payment method, limiting flexibility and reducing buyer trust. [6d507ac44e12]
- Shipping worldwide by default instead of starting with a simpler domestic zone. [6d62360a1568]
- Guessing at tax obligations instead of verifying nexus/VAT rules. [25d24521b0ed]
- Installing many apps at once, adding page weight and hurting site speed. [f07ede1e5f57]
- Skipping the test-order/test-mode step before launch. [728fa86b4907]
- Launching with the wrong store currency. [728fa86b4907]
- Stopping right before removing the password after building, tweaking, and adjusting indefinitely. [f7d6a3b222e4]

## 9. Caveats, conflicts and what is missing

- Affiliate risk: every named third-party tool (GoDaddy, Judge.me, Loox, remove.bg, unnamed AI tools) may be an affiliate recommendation given the presenter's own disclosure that "every tool and link" is in the description. Do not present these as independently vetted picks. `[web check]`
- Conflicts with common ecommerce advice: buying the domain directly through Shopify (source's preferred path, for simplicity) trades off against the common independent advice to keep domain registration with a neutral registrar for portability if the store ever migrates platforms. The source does not mention this trade-off at all, only pricing and DNS convenience.
- The tracking/analytics app step is thin on specifics: the source says "search for an analytics or tracking app and install the one that fits your needs" without naming one, unlike its specific picks for reviews (Judge.me, Loox). Treat this as a gap, not a recommendation.
- No mention of cookie consent banners, GDPR/CCPA data handling, or accessibility (WCAG) requirements anywhere in the setup flow, despite covering EU VAT for taxes. This is a gap for any brand selling into the EU/UK or California.
- No mention of abandoned-cart flows, post-purchase email sequences, or SMS platform setup beyond the single opt-in checkbox at checkout; that is explicitly out of this source's scope and redirected by the curator to 14-EML.
- No mention of multi-currency display/conversion beyond setting one store currency, and no mention of Shopify Markets despite it appearing in the dashboard menu list.
- Compare-at pricing and free-shipping-threshold guidance are stated as universal conversion truths with no supporting data; treat both as common practice, not proven for every brand or margin structure. `[needs brand data: real margin and AOV history before setting a threshold]`
- The $1/3-month trial, the theme price range, the Judge.me/Loox comparison, and the "over six million stores" statistic are all time-sensitive claims that should be checked live before quoting to a client. `[web check]`
- Tax and payment-gateway availability explicitly varies by country and is left to the operator to verify; the source gives no region-specific detail beyond "US nexus" and "EU VAT."

## 10. Card index

- 4a154ed3a11d — Claim the $1/month trial link before the 3-day window closes
- d082e7bbfa8a — Know which three Shopify admin areas actually run the store
- 8936916fd085 — Choose a clean, brandable domain instead of an over-thought one
- 7ad023a56f5a — Buy the domain inside Shopify vs. connecting an existing third-party domain
- 6d9a16a8c9c4 — Pick and publish a lightweight free Shopify theme before customizing
- ba017a5df345 — Turn a default theme into a brand with global settings and a transparent logo
- f4d27950fb54 — Structure header, menu style and announcement bar for product count
- c479568fefa4 — Build a hero banner that communicates one clear benefit
- f1706731ed68 — Generate policies from Shopify templates and customize every detail
- f330630b1382 — Write a product page by describing the product, then generating and rewriting the copy
- 6aec7830e90b — Use compare-at pricing, variants and 1000px+ images on the product page
- aa204dc3c45e — Choose manual vs. automatic collections and surface them on the homepage
- 2c5b09996536 — Prune and rebuild the main menu around collections, then test it on mobile
- c0d455504772 — Order the homepage: hero, collections, featured products, then trust blocks
- 6d507ac44e12 — Activate Shopify Payments plus at least one alternative gateway
- 6d62360a1568 — Define shipping zones, rates and a free-shipping threshold
- 25d24521b0ed — Configure taxes by verifying your own obligations first
- f07ede1e5f57 — Install three apps, not ten — reviews, email, tracking
- 728fa86b4907 — Run the pre-launch checklist: store details, domain, test order, mobile, policies, links
- f7d6a3b222e4 — Remove password protection and verify the live store as a customer
