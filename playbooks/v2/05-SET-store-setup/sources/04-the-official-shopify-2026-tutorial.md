# The OFFICIAL Shopify 2026 Tutorial

source_id: 1eB2j_ZeImlVA2JjtLr8-WzRNTiMG-oct  |  folder: /05-SET-store-setup  |  cards: 53  |  words: 18,496  |  type: video tutorial (transcript)

credibility: Published by Shopify's own "Learn with Shopify" channel, hosted by Kylie Maher. Shopify sells the platform, the paid plans (Basic, Grow, Advanced, Plus) and the apps it repeatedly promotes inside its own admin (Shopify Payments, Shopify Messaging, Shopify Flow, Shopify Fulfillment Network, Sidekick). Evidence is a mix of: the presenter's own live demo store (a fictional "matcha" brand, used only as an example), a handful of unsourced industry stats (cart abandonment ~70%, 1-second delay costs ~7% conversion, SMS open rate 98%, "72% of brands" from a cited Forbes report on email), and Shopify's own documented mechanics (settings paths, plan names, template flows). It is vendor content: expect it to favor Shopify's built-in tools over third-party alternatives, per ecomOS's own note on this source. Third-party apps are named only where Shopify has no built-in equivalent (shipping insurance apps, SMS apps, review apps, trust-badge apps, heat-map apps, pop-up apps, referral apps).

date signals: Title says "2026." Modified 2026-09-19. Features referenced (Sidekick AI assistant, Shop Pay, the Horizon theme, GA4-only Google Analytics setup, Basic/Grow/Advanced/Plus plan names, "Facebook and Instagram by Meta" sales channel app) are current Shopify features as of this recording, but the source itself warns that admin screens change; every click path below needs a live check.

## 1. What this source is for

This is chapters 1-2 (plus parts of chapters 3-4) of a 4-part beginner tutorial that walks a brand-new merchant from creating a Shopify account through products, collections, theme, navigation, domain, payments, shipping, tax, fulfillment, returns, pre-launch testing and going live. For the 05-SET domain, its job is the exact click paths, gating order and verification steps needed to take a store from nothing to a legally and technically working, publicly visible store. Later chapters (3-4) shift into marketing hub, email, organic social, product-page and checkout conversion optimization, speed and A/B testing; the source's own scope note routes that material to other folders (06-MEA, 07-LPG, 08-SPD, 13-ORG, 14-EML, 15-SEO), so it is indexed here (section 10) but not elaborated in sections 2-8.

## 2. Principles

1. **Identity first, everything else inherits it.** Legal business name and address, entered right after account creation, feed the defaults used later by payments, tax and shipping screens. Condition: applies to every new store, before touching payments or shipping. Evidence: source states skipping this step means re-entering the same data later and risks mismatches during Shopify Payments verification. [5a93770b958e]

2. **Exact legal-identity match avoids payout holds.** Names, addresses and business details entered into Shopify Payments must match government ID and registration documents exactly (example given: "Robert," not "Rob"). Condition: applies whenever activating Shopify Payments as an individual or a business. Evidence: source calls mismatch "the number one reason people get held up in verification." [d81e9a676d16] [ae4e374138b3]

3. **A country lives in exactly one shipping zone at a time.** To give a country its own rate, it must first be removed from whatever zone (e.g. international) currently holds it. Condition: applies whenever carving a country out of a broader zone. Evidence: stated directly as a platform constraint. [b1cd95fe8167] [70512e56f11a]

4. **Product weight alone understates shipping cost.** Calculated and weight-based rates need the packaging's own empty weight added on top of product weight, or rates run light on every order. Condition: applies to any store using calculated or weight-based shipping. Evidence: source frames this as a direct, compounding margin leak as order volume grows. [96efb19e76e2] [e3d04df66513]

5. **Order of setup matters because later steps depend on earlier ones.** Recommended order: account identity → payments (exact identity) → tax (physical presence) → shipping zones and package weights → domain and business email → tracking and legal pages → test-mode verification → remove password. Condition: this is the source's stated sequence to avoid launch-day breakage, not a claim that no other order works. Evidence: shipping rates depend on weight data set during product entry; tax regions depend on physical-presence data; the test order is presented as verifying all the prior steps together. [a14524485a10]

6. **A saved setting is not proof it works.** Every configured step (payments, shipping, tax, domain, tracking, legal pages) should be closed out with an action a customer would actually take: a test order, a rate quote, a live click on a footer link, checking the analytics platform's real-time view. Condition: applies before removing the store password. Evidence: source treats the test order as the single aggregated proof that the whole setup functions end to end. [d6854b97be2c] [3a6ca3eb1bff] [9921264a1167]

7. **Test mode and the password gate must both come off before real traffic arrives, and not before.** Un-gating is presented as the last step, gated on the test order passing, not an early or optional one. Condition: applies at the moment of going live. Evidence: source explicitly warns against leaving either on after launch. [3a6ca3eb1bff] [94700fd0e277]

8. **Tax configuration should track physical presence, not desired convenience.** The basic rule given is to register and collect tax where the business has a location, inventory or employees. Condition: this is Shopify's configuration mechanism, not a legal nexus ruling. Evidence: source explicitly disclaims itself as non-legal-advice and tells the merchant to consult a tax professional. [9f3db093361a] [9ab062ef593f]

9. **Fewer, better products beat a full catalog at launch.** The source's stated preference is a small number of solid product listings over hundreds of thin ones. Condition: applies to a brand-new store choosing what to list first. Evidence: presenter's stated opinion, not a benchmark. [12b76f909fb9]

## 3. Procedures

### 3.1 Account and business identity
1. Sign up with an email address the business will keep long-term (not a personal address at risk of being lost). [2f5a7287fedc]
2. Choose the store name carefully: the `myshopify.com` handle generated from it is treated as effectively permanent; the customer-facing display name can be changed later in Settings. [verify UI] [2f5a7287fedc]
3. During onboarding, select sales method (e.g. Online store), business status (new/existing), product types, and business name; set country/region and currency correctly since these drive default tax and payment behavior. [verify UI] [2f5a7287fedc]
4. On the home dashboard, open the Settings icon (bottom-left), select **General**, click the pencil icon, and enter the exact legal business name and address. Do this immediately, before payments, shipping or taxes. [verify UI] [needs brand data: legal business name and registered address] [5a93770b958e]
5. If a setting can't be found, open **Sidekick** (top-right icon in admin) and ask it where the setting lives, rather than hunting menus. [verify UI] [d32ab6d8ae7a]

### 3.2 Add products
1. From the dashboard, click **Add your first product**. [verify UI] [12b76f909fb9]
2. Write a descriptive, specific title (example given: "natural matcha preworkout drink," not a generic name). [needs brand data: product names and positioning] [12b76f909fb9]
3. Fill the description; if blank, ask Sidekick to draft a professional description, then edit it against the real product. [12b76f909fb9]
4. Upload media (images, video, 3D models) via the upload button; Sidekick can generate image variations (lifestyle settings, natural lighting) up to 5 images per chat, then a new chat for more. [verify UI] [12b76f909fb9]
5. Enter price, inventory stock, product weight and location — weight feeds shipping calculations done later. [needs brand data: price, stock, weight] [12b76f909fb9]
6. Review the auto-populated search-engine listing (title, URL, meta description); edit or ask Sidekick to generate one. [12b76f909fb9]
7. Save, then repeat per product.

### 3.3 Build collections
1. In the left sidebar, Products → **Collections** → **Add collection**. [verify UI] [73ad1a753e69]
2. Choose type: manual (add products yourself) or smart (rule-based). [73ad1a753e69]
3. Add title, description, and fill the search-engine listing fields. [73ad1a753e69]
4. For manual: add products directly. For smart: define the membership rules. [73ad1a753e69]
5. Optionally ask Sidekick to build the collection (e.g. "a three-product collection of my flavors, featured on my homepage"), review in **Preview**. [73ad1a753e69]
6. Add a collection photo: upload your own or generate one in the admin. [needs brand data: collection imagery] [73ad1a753e69]

### 3.4 Theme and store design
1. Admin → **Online store** → **Themes**. [verify UI] [ea68a79d73c2]
2. Either type a store description into the theme-generation box and click **Generate theme**, or browse the theme store, filter to free themes, and **Try theme** (source's example pick: Horizon). [verify UI] [ea68a79d73c2]
3. Open **Edit theme** for the theme editor (toggles, sliders, color boxes, dropdowns; most changes preview live). [verify UI] [ea68a79d73c2]
4. Ask Sidekick for a design brief: "professional, clean, organized... color palettes with hex codes, font recommendations, layout tips." [ea68a79d73c2]
5. Theme settings → **Colors**: apply the Sidekick-suggested palette (review before publish) or set values manually. [verify UI] [ea68a79d73c2]
6. **Typography**: set fonts for headings, body text, subheadings, accents. [verify UI] [ea68a79d73c2]
7. **Logo and favicon**: upload logo (plus an inverse version for dark backgrounds) and favicon. Favicon spec given: high-quality PNG, transparent background, ~200-300 px wide for desktop. [ea68a79d73c2]
8. Edit page sections in the live preview (click a section, e.g. hero banner, to swap its image; use the plus icon to add a section such as a contact form or carousel). [verify UI] [ea68a79d73c2]
9. Check every change in the editor's mobile/phone preview (top-right phone icon) — source cites roughly two-thirds of online retail orders as coming through mobile. [verify UI] [ea68a79d73c2]
10. Use the top navigation dropdown to edit other page types (products, collections, blogs) with the same process. [ea68a79d73c2]
11. Do a final image pass: keep quality high, mix AI-generated banners/graphics with authentic real-product photos.

### 3.5 Navigation menus
1. Admin → **Content** → **Menus**. [verify UI] [62bc837b1167]
2. Open a preset menu (main menu, catalog, contact) to edit its name and linked destination. [62bc837b1167]
3. **Add menu item**, choosing a collection, product, page, or external URL as the destination. [62bc837b1167]
4. Drag with the vertical-dots handle to reorder; drag one item slightly right under another to nest it as a dropdown submenu. [verify UI] [62bc837b1167]
5. Organize by customer logic (category, e.g. men's/women's/accessories, or product type, e.g. shirts/pants/shoes), not internal naming. [needs brand data: category structure] [62bc837b1167]
6. Save, then preview via the eye icon on the Online store row, and test every path including on a phone. [verify UI] [62bc837b1167]

### 3.6 Domain and business email
1. Admin → **Settings** → **Domains**. [verify UI] [4f9700a6e477]
2. **Connect existing** (enter your domain) or **Buy new domain** (search the store name for suggestions, purchase, enter payment info). [verify UI] [4f9700a6e477] [f1fa31262a90]
3. A domain bought through Shopify connects automatically with no manual DNS work; an externally purchased domain follows DNS instructions (A/CNAME records, or nameserver change) that the source does not detail in full. [web check: current Shopify domain connection flow for external registrars] [f1fa31262a90]
4. Test the domain by visiting it in a browser before removing the store password. [4f9700a6e477]
5. In domain settings, set the store's **primary domain** to the custom one, not the `myshopify.com` address. [verify UI] [4f9700a6e477]
6. Set up a matching branded business email through a mail provider; test sending and receiving before publishing it anywhere customer-facing. [needs brand data: chosen mail provider and address] [f1fa31262a90]

### 3.7 Payments
1. **Gate: enable two-step authentication first.** Profile → **Security** → **Turn on two-step** → enter password → choose method (authenticator app such as Google Authenticator or Duo, SMS, security key, or Shopify's built-in mobile prompt) → follow on-screen steps → save recovery codes somewhere secure (explicitly not a notes app). Shopify Payments cannot be activated without this. [verify UI] [0949813570ce]
2. Settings → **Payments** → follow the account-setup prompt. [verify UI] [d81e9a676d16]
3. Choose business type: **Individual** if there's no business number yet (including sole proprietors — there is no separate sole-proprietor option), or **Business** if there is a registration number (LLC, corporation, partnership). [ae4e374138b3]
4. Individual: enter legal name exactly as on ID, date of birth, SSN/ITIN/TIN, email, phone, home address, plus a verification document (passport or driver's license). [needs brand data: owner's legal identity documents] [ae4e374138b3]
5. Business: enter registered business name, business number/EIN/VAT number, business phone and address, then add an account representative (owner or signing authority) with their own legal name, date of birth, ID number and residential address. [needs brand data: business registration details] [ae4e374138b3]
6. Confirm the payout bank account can receive the correct deposit type for the region: ACH transfer (US), EFT (Canada), SWIFT (Europe/Asia/Africa), BECS (Australia). [ae4e374138b3]
7. Save and wait for review (typically a few hours, sometimes a few days); keep building other parts of the store while waiting. [ae4e374138b3]
8. If unsure whether Shopify Payments is available in a country, or how to classify a registered-but-not-incorporated business, ask Sidekick. [web check: Shopify Payments country availability] [0949813570ce] [ae4e374138b3]
9. Set payment capture: Settings → Payments → payment capture method → **Automatically at checkout** (captures funds the instant an order is placed); manual capture can be switched on later for order review before charging. [verify UI] [cb2ff7113ded]
10. Confirm accelerated wallets (Shop Pay, Apple Pay, Google Pay) show at checkout; manage via **Manage** next to Shopify Payments → **Manage payment methods**, toggling wallets on/off. [verify UI] [cb2ff7113ded]
11. Settings → **Checkout**: set the customer contact method (email or SMS), enable the "track your order with Shop" link, and enable the marketing-consent checkbox to start list-building from day one. [verify UI] [cb2ff7113ded]
12. Optionally add more payment methods (PayPal, third-party processors) from **Additional payment methods**; multiple methods can run alongside Shopify Payments. [cb2ff7113ded]

### 3.8 Shipping
1. Settings → **Shipping and delivery**; Shopify pre-creates domestic and international zones with weight-based rates filled in. [verify UI] [0475c2317d11]
2. Under the domestic zone, inspect existing rates or **Add rate** (flat amount or free), or let Shopify calculate rates automatically from origin, destination, weight and size. [needs brand data: actual product weights and desired margin] [0475c2317d11]
3. To ship to a specific country with its own rate: International section → three-dot menu → **Edit zone** → uncheck the target country → **Done** → **Save** (frees the country from that zone). Then **Shipping** → "start shipping to more places" / **Go to markets** → **Create market** → name it, add a condition, check the country → **Done** → **Save**. Then **Add rate** and choose flat rate, carrier-calculated, or free shipping; set price/conditions → **Done** → **Save**. Repeat per country. [verify UI] [b1cd95fe8167]
4. Package weights: Settings → Shipping and delivery → **Packages** → **Add package** → choose type → enter outside dimensions and empty packaging weight → name it (e.g. "small box," "standard mailer") → check **Set as default** if all products ship the same way. [verify UI] [e3d04df66513]
5. If different products use different packaging, assign packages at the product level: Products → select product → shipping section → choose the matching package → save; also re-check the product's own weight there. [e3d04df66513]
6. Local delivery: **Setup** under local delivery → choose location → define delivery area (radius, e.g. 100 miles/km, or specific postal codes) → optional minimum order amount and delivery fee → save. [verify UI] [needs brand data: delivery radius and fee] [5c69503ff6eb]
7. Store pickup: **Setup** under store pickup → select location → set pickup times → add special instructions → save. [verify UI] [5c69503ff6eb]
8. Shipping labels: buy directly in the Shopify admin (uses Shopify's pre-negotiated carrier discount) where available, or install a labels app (source names AfterShip Shipping Plus Labels or ReadyToShip Shipping Labels) where not. [verify UI] [web check: label purchasing availability by country] [5c69503ff6eb]
9. Label charges post to the Shopify account balance (not deducted from the customer's payment), invoiced when the account's billing threshold is hit, or bundled into the next monthly subscription bill otherwise. Check status: Settings → **Billing** → **Bills**. [verify UI] [5c69503ff6eb]
10. Shipping insurance: on Grow/Advanced/Plus with Shopify Payments, up to $200 of insurance is included per eligible label (read exclusions for fragile/high-value items); on Basic, insurance is not automatically included but can be purchased for orders up to $5,000. From Canada or Europe: use carrier insurance directly, a third-party app, or self-insure. [web check: current plan-linked insurance terms] [61a98d182026]
11. Before moving to test orders, re-check that zones, rates and packages are all saved. [61a98d182026]

### 3.9 Fulfillment
1. Orders tab: for each approved order, review customer details, pull items from inventory, prep packaging. [verify UI] [eb0639f2f194]
2. Click **Print packing slip** (goes inside the box), then print the shipping label. [verify UI] [eb0639f2f194]
3. Ship by drop-off or scheduled pickup; the customer's "shipped" email with tracking sends automatically, and Shopify normally marks the order fulfilled. [eb0639f2f194]
4. Multi-item orders: if one item is on back order, fulfill and ship the in-stock items now, and fulfill the remainder later. [eb0639f2f194]
5. At volume: batch-pack (e.g. two at a time, marked in progress), then Orders → select-all checkbox → bulk print packing slips and labels → mark all fulfilled in one action. [verify UI] [eb0639f2f194]
6. Customize the "order shipped" email template: ask Sidekick where to edit it, add logo, set accent color, preview, save. [eb0639f2f194]

### 3.10 Returns and refund policy
1. Settings → **Policies** → **Return and refund policy**; if none exists, insert Shopify's template. [verify UI] [ecbee7e2499a]
2. Edit the template to match actual practices, then **Publish**. [ecbee7e2499a]
3. Settings → **Customer accounts** → toggle on **self-serve returns**. [verify UI] [ecbee7e2499a]
4. In return rules, set the return window (days), whether return shipping is charged, any restocking fee, and which items are final sale. [needs brand data: return window, restocking fee, final-sale list] [ecbee7e2499a]
5. Save, then confirm the policy is reachable from the storefront and visible at checkout. [ecbee7e2499a]

### 3.11 Taxes
1. Settings → **Taxes and duties** → select the store's base country. [verify UI] [9ab062ef593f]
2. Under sales tax, **Collect in a new region**, select the state/province, enter a sales tax ID if held, **Collect sales tax**. [verify UI] [needs brand data: registered tax jurisdictions and IDs] [9ab062ef593f] [9f3db093361a]
3. **Duties and import taxes** → **Set up** → select applicable markets → save; update the shipping policy to state that duties/taxes are handled at checkout (no pay-on-delivery surprise). [verify UI] [9ab062ef593f]
4. Check shipping taxability per region: open the country/state in Taxes and duties, find shipping tax options (US: **Advanced options** to set whether shipping is taxable — this varies by jurisdiction). [verify UI] [9ab062ef593f]
5. Enable tax-inclusive pricing only where required or expected (e.g. required in Japan, common in the EU): global settings → **Include sales tax in product price and shipping rate**. [verify UI] [9ab062ef593f]
6. For international selling, use dynamic tax-inclusive pricing under **Markets**: select a market, adjust pricing settings so displayed price matches local expectation (example: a $100 product shows as $100 tax-included in the UK, but $90.91 plus tax at US checkout). [verify UI] [9ab062ef593f]
7. Keep records of tax registrations and consult a local tax professional; the source explicitly does not establish a universal nexus rule. [9f3db093361a] [9ab062ef593f]

### 3.12 Verification: test-mode orders
1. Shopify Payments section → **Manage** → toggle **test mode** (or check "use test mode"). [verify UI] [94700fd0e277]
2. Click the eye icon next to Online store to view the storefront as a customer. [verify UI] [94700fd0e277]
3. Add a product to cart and complete a purchase using an official Shopify test card number (ask Sidekick for the current numbers — never a real card). [web check: current Shopify test card numbers] [94700fd0e277]
4. Verify: tax calculates correctly per configured region, shipping rates display correctly, payment options work, and policy links (e.g. return policy) are visible at checkout. [94700fd0e277] [3a6ca3eb1bff]
5. Test at least one address per shipping zone to catch rate/tax gaps a single address would miss. [3a6ca3eb1bff]
6. Run the downstream workflow too: process the test order through receiving and fulfillment. [94700fd0e277]
7. Repeat the entire walkthrough on a phone. [94700fd0e277]
8. Ask Sidekick for a checklist of what to review while test mode is active; when satisfied, turn test mode off. [94700fd0e277]

### 3.13 Pre-launch page and content audit
1. Ask Sidekick to scan the product list for missing descriptions, prices or images, and to verify contact/shipping/return policies are set up correctly. [ab549d0194fc]
2. Confirm essential pages exist: contact page, shipping policy, return policy, privacy policy, terms of service. [64e08ffbebfb] [ab549d0194fc]
3. Generate first drafts with Sidekick where needed (e.g. "draft a return policy for a clothing business with a 30-day return window"), then customize to actual practice. [ab549d0194fc]
4. Do a final walkthrough as a first-time visitor: navigate, add to cart, complete checkout in test mode, confirm shipping rates and payment options, on desktop and phone. [ab549d0194fc]

### 3.14 Tracking install
1. Install analytics/pixel tracking through the Shopify admin or the platform's own app. [verify UI] [9921264a1167]
2. Use a debug/test session to confirm page-view (and configured add-to-cart/checkout) events actually register — do not assume the script loaded. [9921264a1167]
3. Confirm tracking is present on the checkout step, not just the storefront (a script that only covers storefront pages misses purchases). [web check: current checkout-extensibility tracking support for your plan] [9921264a1167]
4. Confirm data appears in the platform's real-time view during the test session. [9921264a1167]
5. Re-verify after any theme change or new app install, since these can drop tracking snippets. [9921264a1167]
6. Google Analytics: Shopify admin search bar → "Google and YouTube" app → install → **Connect Google account** → sign in → for Analytics-only, use the "set up Google Analytics 4" banner → **Get started** → select or create a GA4 property → **Connect**. [verify UI] [b915be273681]
7. Google Search Console: go to search.google.com/search-console separately, add the store URL, verify ownership per Google's prompts. [verify UI] [b915be273681]

### 3.15 Apps: connecting sales channels and vetting the app store
1. Before installing any app: check its rating (4+ stars, ideally 4.5+) and review count (100+ is a reliability signal); read recent reviews for complaint patterns; check the developer's other apps/track record; look for the **Built for Shopify** badge. Install apps one at a time as an actual need arises. [60e0c0a3ad53]
2. Browse via Settings → **Apps** → **Shopify App Store**, filter by rating/price/category, or ask Sidekick for recommendations. [verify UI] [60e0c0a3ad53]
3. To connect Meta/TikTok ads: Settings → **Sales channels** → search and install the official Facebook and Instagram (by Meta) or TikTok app. Prerequisites: an established (not brand-new) Facebook account, owner/admin permission on the business manager, Facebook page and Instagram account, and an Instagram professional account. [verify UI] [08b80874b674]
4. Log into Facebook first, then in admin click **Facebook and Instagram** → **Get started**; add business assets (page, Instagram account), add data sharing (existing pixel if any), add business details (contact email, return window), accept the seller agreement, grant catalog access, submit for review. [verify UI] [needs brand data: business contact email and return window] [08b80874b674]
5. Once approved, ads run through Meta Ads Manager (feed/stories/reels); expect traffic within 24-48 hours, then check attribution from the Shopify marketing dashboard. This card sits on the boundary with acquisition; the source itself defers deep ad setup to a separate tutorial. [08b80874b674]

### 3.16 Launch
1. Admin → **Sales channels** → **Online store** → **Preferences** → deselect **password protection**. The store becomes publicly visible immediately. [verify UI] [b915be273681]
2. Send a short, personal launch email to friends/family/contacts featuring the best product/collection with a clear "shop now" button (draft with Sidekick, add a personal touch); send via **Apps** → **Messaging** → **Create campaign** → choose template → paste copy → add images → send a test email first, then send for real. [verify UI] [b915be273681]
3. Post a 3-post social sequence: teaser (curiosity) → behind-the-scenes (story) → clear launch announcement with the store link. Consider a $20-50 boost on the launch post to extend reach past current followers, especially on Instagram/Facebook. [web check: current ad boost minimums/costs] [b915be273681]
4. Set SEO groundwork at launch: ask Sidekick to audit the store for SEO issues, improve meta descriptions, and optimize the homepage, about page and product listings; write descriptive alt text on product images (not generic filenames) rather than keyword-stuffing. [b915be273681]

## 4. Rules, thresholds and numbers

| Rule / number | Value | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Two-step authentication | required before Shopify Payments can activate | any store activating Shopify Payments | stated platform requirement | 0949813570ce |
| Legal-identity match | exact match to government ID (e.g. "Robert" not "Rob") | Shopify Payments individual or business setup | stated top cause of verification holds | d81e9a676d16, ae4e374138b3 |
| Payments verification time | a few hours typically, up to a few days | after submitting Shopify Payments application | presenter's stated typical range | ae4e374138b3 |
| Payout deposit types | ACH (US), EFT (Canada), SWIFT (Europe/Asia/Africa), BECS (Australia) | confirming bank account before payments go live | stated by region | ae4e374138b3 |
| Shipping insurance included | up to $200 per eligible label | Shopify Payments on Grow, Advanced or Plus plan [web check: current plan terms] | stated as a plan feature at time of recording | 61a98d182026 |
| Shipping insurance purchasable | up to $5,000 per order | Basic plan, buying insurance separately [web check] | stated as a plan feature at time of recording | 61a98d182026 |
| Free-shipping-into-price example | $35 all-in vs $30 + $5 shipping | example only, not a rule | presenter's example, framed as a conversion tactic | 0475c2317d11 |
| Local delivery radius example | 100 miles/km | example only | presenter's example | 5c69503ff6eb |
| Cart-abandonment automation exclusion window | 14 days | excludes anyone already emailed for abandoned checkout/browse in that window | stated default Shopify Messaging behavior | 87e84f54a8e0 |
| Free Shopify Messaging email allowance | up to 10,000 emails/month | across campaigns + automations; abandoned-checkout emails always free and don't count | stated platform allowance at time of recording [web check] | 5ceb388ec702 |
| SMS pricing | separate, per message | when adding SMS to Shopify Messaging | stated platform behavior | 5ceb388ec702 |
| SMS open rate | 98%, read within minutes | cited to justify SMS urgency use cases | presenter's cited figure, not store data | 88e1f0388bb2 |
| Email effectiveness stat | 72% of brands rate email most effective | context for prioritizing email | cited from a named Forbes report | (no dedicated card; contextual claim in text) |
| Domain email sender verification | instant (quick verify) vs up to 48 hours (domain authentication/DNS) | choosing sender verification method | stated processing time | 5ceb388ec702 |
| Dynamic tax-inclusive pricing example | $100 shows as $100 (UK, tax-included) vs $90.91 + tax (US) | Markets-based dynamic pricing example | worked example from source | 9ab062ef593f |
| Funnel drop-off example | 100 sessions → 5 add-to-cart → 95 leave | conversion-rate-breakdown report example | presenter's worked example, not a benchmark | a0544e91dab6 |
| Product-page share of conversion killers | 60-70% (presenter's framing) | product-page-first optimization | unsourced presenter claim | 41414136b4ab |
| Product images recommended | at least 3-5 real images, multiple angles | any product page | presenter's stated minimum | 41414136b4ab |
| Vessi example | 4 images incl. 1 lifestyle + 1 360° video per product | worked example, footwear brand | named case example | 41414136b4ab |
| Click-depth rule | products reachable in 2-3 clicks from homepage | navigation structure | presenter's heuristic, not a universal law | 613ebaa5552e |
| Hashtag guidance | 5-10 targeted, not 30 random | organic social posts (out of 05-SET scope) | presenter's heuristic | c2a9e36b5b45 |
| Organic posting cadence | 3-4 times/week | organic social (out of 05-SET scope) | presenter's recommendation, not validated | c2a9e36b5b45 |
| Launch social boost budget | $20-$50 | extending launch post reach on Instagram/Facebook | presenter's suggestion [web check: current ad minimums] | b915be273681 |
| Bounce-rate speed flag | above 60% | signal of a likely site-speed problem (08-SPD territory) | presenter's heuristic | 14f8bc81657f |
| Speed-to-conversion estimate | ~7% conversion loss per 1-second delay; $10,000/month store example loses ~$700 | illustrative arithmetic on a cited study figure | cited studies, presenter's own math example | 14f8bc81657f |
| Image size target | under 200 KB per image; JPEG for photos, PNG for transparency | site-speed optimization (08-SPD territory) | presenter's stated targets | 14f8bc81657f |
| Favicon spec | PNG, transparent background, ~200-300 px wide (desktop) | theme/branding setup | stated spec | ea68a79d73c2 |
| Mobile order share | roughly two-thirds of online retail orders | justification for mobile-first QA throughout setup | presenter's cited figure | ea68a79d73c2 |
| Cart abandonment rate | ~70% industry average | context for checkout-friction work (07-LPG territory) | presenter's cited industry figure | 8f9f02d8611d |
| A/B test minimum duration | at least 2 weeks | before drawing conclusions from a test (07-LPG territory) | presenter's rule of thumb | 8f76661ea3a5 |
| VIP segment examples | 2+ orders, or spend over $200; VIP10 = 10% off orders over $50 | worked example for a retention campaign (14-EML/13-ORG territory) | presenter's example, not a benchmark | 1cb48ec66159 |
| App vetting bar | 4+ stars (ideally 4.5+), 100+ reviews | before installing any Shopify app | presenter's heuristic | 60e0c0a3ad53 |

## 5. Diagnostics and checks

- **Domain live check.** Visit the custom domain in a browser; it must resolve to the store, not just show as "connected" in admin, before removing the password. [4f9700a6e477] [d6854b97be2c]
- **Payments verification check.** If a payout is held, the first thing to re-check is name/address/ID exact match against government documents. [d81e9a676d16] [ae4e374138b3]
- **Shipping-rate accuracy check.** Quote a multi-item test order before and after changing package weights and compare totals; a lower-than-expected quote signals missing or wrong default package weight. [96efb19e76e2] [e3d04df66513]
- **Tax-region completeness check.** After adding a new shipping destination or market, re-open Taxes and duties for that region — a location you now sell into may need tax registration you haven't added. [9f3db093361a]
- **Tracking check.** Don't trust that a script tag exists in the theme; confirm the analytics platform's real-time view shows the test session, and specifically test the checkout step, not just the storefront. [9921264a1167]
- **Full-setup check (the test order).** Toggle Shopify Payments test mode, view the store as a customer, place an order with an official Shopify test card, and confirm: correct tax total, correct shipping rate for the address used, visible policy links, and successful order processing through fulfillment. Repeat on mobile. This is presented as the single gate before removing the password. [94700fd0e277] [3a6ca3eb1bff]
- **Legal-page completeness check.** Ask Sidekick to verify all contact, shipping and return policies are set up correctly, and to scan the product list for missing descriptions, prices or images, before the final walkthrough. [ab549d0194fc]
- **Site-speed signal (08-SPD boundary).** Bounce rate over time above 60% flags a likely speed problem; confirm with Google PageSpeed Insights on specific pages. [14f8bc81657f]
- **Funnel leak location (07-LPG boundary).** Analytics → Reports → Behavior → conversion rate breakdown shows sessions, cart-adds, checkout-starts, completions; the largest proportional drop tells you whether to fix product pages or checkout first. [a0544e91dab6]

## 6. Tools, settings and named features

- **Sidekick** — Shopify's built-in AI assistant (top-right icon in admin, also has voice input); used throughout for finding settings, drafting descriptions/policies/emails, generating images, building collections/segments/discounts, auditing apps, navigation and SEO, and explaining attribution models. Saved chat history sits at the bottom of the left nav. [verify UI] [d32ab6d8ae7a]
- **Shopify Payments** — native payment processor; gated behind two-step authentication; supports individual and business account types. [d81e9a676d16]
- **Shop Pay / Apple Pay / Google Pay** — accelerated checkout wallets, toggled in payment settings. [cb2ff7113ded] [8f9f02d8611d]
- **Horizon theme** — named example of a current free theme with speed-oriented architecture and built-in predictive search. [verify UI] [ea68a79d73c2] [2feda79ef81c]
- **Search and Discovery app** (free, Shopify-made) — enables custom search suggestions, predictive search and synonyms if the theme lacks it. [verify UI] [2feda79ef81c]
- **Breadcrumbs Uncomplicated** — named free app for adding breadcrumb navigation if the theme lacks it. [613ebaa5552e]
- **Shopify Flow** — automation builder for custom trigger/condition/action logic (e.g. WhatsApp abandoned-cart recovery, welcome/win-back flows). [0cbef48284c3] [87e84f54a8e0]
- **Shopify Messaging** — built-in email/SMS tool (10,000 free emails/month allowance); called "Shopify email" in older material. [5ceb388ec702]
- **Shopify Fulfillment Network** — named as one fulfillment option alongside self-fulfillment or a third-party app. [eb0639f2f194]
- **AfterShip Shipping Plus Labels / ReadyToShip Shipping Labels** — named third-party label apps for regions without native Shopify label purchase. [web check: current availability] [5c69503ff6eb]
- **Klaviyo** — named as the step-up email/SMS/WhatsApp/push platform once past ~10,000 emails/month; steeper learning curve. [88e1f0388bb2]
- **Postscript, Attentive** — named SMS marketing apps. [88e1f0388bb2]
- **Judge.me, Loox, Yotpo** — named review/social-proof apps. [88e1f0388bb2] [41414136b4ab]
- **Privy, Justuno** — named pop-up/conversion apps (Privy = all-in-one incl. email/SMS; Justuno = pop-ups only, pairs with an existing email platform). [88e1f0388bb2]
- **Referral Candy** — named referral/affiliate app. [88e1f0388bb2]
- **Essential Trust Badges and Icons, Conversion Bear Trust Badges, Super Trust Badges and Icons** — named trust-badge apps (07-LPG territory). [a23f9e5da162]
- **Lucky Orange, Hotjar** — named heat-map apps (07-LPG territory). [8f76661ea3a5]
- **TinyPNG, Squoosh** — named free image-compression tools (08-SPD territory). [14f8bc81657f]
- **Google PageSpeed Insights** — free page-speed testing tool. [14f8bc81657f]
- **Google Analytics (GA4) / Google Search Console** — installed via the "Google and YouTube" Shopify app (Analytics) and directly at search.google.com/search-console (Search Console). [verify UI] [b915be273681]
- **Facebook and Instagram by Meta app / TikTok app** — Shopify sales-channel apps required to connect ad accounts. [08b80874b674]
- **Built for Shopify badge** — Shopify's own quality signal for app-store vetting. [60e0c0a3ad53]

## 7. Examples and case results

- Presenter's own demo: a fictional matcha energy-drink brand, used to illustrate product entry, a 3-flavor collection, shipping weights (0.5 lb single / 3 lb three-pack / 7 lb eight-pack), a VIP campaign, and a click-depth analysis result (2 clicks to product via Catalog → flavor). All figures are this one example, not benchmarks. [12b76f909fb9] [73ad1a753e69] [0475c2317d11] [1cb48ec66159] [613ebaa5552e]
- Vessi (footwear brand), named case: 4 product images per listing, one lifestyle shot in a puddle, one 360° video — cited as a model for "enough, not excessive" product visuals. [41414136b4ab]
- Worked tax example: a $100 product displays as $100 tax-included in the UK (dynamic tax-inclusive pricing) versus $90.91 plus tax at US checkout. [9ab062ef593f]
- Worked funnel example: 100 sessions, 5 cart-adds, 95 no-adds — illustrates reading the conversion-rate-breakdown report to find the biggest leak (07-LPG territory). [a0544e91dab6]
- Worked speed-cost example: a $10,000/month store loses roughly $700/month from one extra second of load time, based on the cited "7% per second" study figure — illustrative math, not the store's own measured result. [14f8bc81657f]

## 8. Mistakes the source warns about

- Entering a nickname or shortened name instead of the exact legal ID name in Shopify Payments — the stated top cause of verification holds. [d81e9a676d16] [ae4e374138b3]
- Skipping the legal business name/address step at account creation, forcing re-entry (and mismatch risk) later in payments and tax screens. [5a93770b958e]
- Leaving default package weight unset or wrong when using calculated shipping — undercharges compound as order volume grows, quietly eating margin. [96efb19e76e2] [e3d04df66513]
- Trying to add a country to a new shipping zone while it is still in another zone — it must be removed first. [b1cd95fe8167]
- Removing the store password before running a test-mode order that confirms checkout, tax, shipping and policy links. [3a6ca3eb1bff] [d6854b97be2c]
- Leaving test mode or the password gate on after real customers are expected — both block real sales. [3a6ca3eb1bff]
- Publishing Shopify's generated policy templates without editing the placeholder language to match actual practice. [64e08ffbebfb] [ab549d0194fc]
- Assuming a saved setting means it works, instead of verifying with a live action (test order, rate quote, footer-link click, analytics real-time check). [d6854b97be2c] [9921264a1167]
- Installing many apps without vetting rating, review count, developer track record or the Built for Shopify badge, or leaving unused/dormant apps installed — a stated speed and cost drain (08-SPD territory). [60e0c0a3ad53] [14f8bc81657f]
- Forcing account creation before checkout instead of keeping guest checkout on (07-LPG territory). [8f9f02d8611d]
- Asking for more checkout form fields than needed (both email and phone, optional address lines made mandatory) (07-LPG territory). [8f9f02d8611d]
- Revealing shipping costs only at the final checkout step instead of earlier in the funnel (07-LPG territory). [8f9f02d8611d]
- Changing more than one variable at a time in an A/B test, which makes it impossible to attribute the result (07-LPG territory). [8f76661ea3a5]
- Sending a blanket discount to the entire list instead of segmenting, which gives margin away to customers who would have paid full price — the source's own reasoning, not a measured result (14-EML territory). [241fe26f97c1] [1cb48ec66159]

## 9. Caveats, conflicts and what is missing

- **Vendor bias.** This is Shopify's own tutorial channel. Every recommended tool is a Shopify-built feature (Sidekick, Shopify Payments, Shopify Messaging, Shopify Flow, Shopify Fulfillment Network) unless Shopify has no built-in equivalent, in which case a small number of named third-party apps appear (label apps, SMS apps, review apps, trust-badge apps, heat-map apps, pop-up apps, referral apps, image compressors). Do not read the absence of a competing tool as evidence Shopify's option is best; it reflects what the source is incentivized to show. Cross-check third-party alternatives elsewhere before recommending a stack to a client.
- **Unsourced statistics.** Several numbers are presented without a data source and should be treated as industry folklore, not fact: ~70% cart abandonment, ~7% conversion loss per second of load delay (with the $10,000/month example built on top of it), 60-70% of conversion killers being product-page issues, 98% SMS open rate, two-thirds of orders on mobile. The only cited external source in the transcript is a named Forbes report for the "72% of brands rate email most effective" line. [web check: current figures if any of these are used in a client-facing claim]
- **Scope boundary with other folders.** The source's own header explicitly routes several topics elsewhere even though all 53 cards are currently filed under this source's folder: product-page design and checkout UX (→ 07-LPG), site speed and app-load optimization (→ 08-SPD), email flows and automations (→ 14-EML), organic social cadence and content pillars (→ 13-ORG), attribution models in the marketing hub (→ 06-MEA), and SEO briefs (→ 15-SEO). Sections 2-8 above stayed inside the 05-SET (account, product/collection/theme/nav setup, domain, payments, shipping, tax, checkout gating, fulfillment, returns, tracking, legal pages, launch) scope; the remaining cards (attribution, UTM automatch, campaign activities, marketing-hub automations, Shopify Messaging campaign building, segmentation, Meta/TikTok ad account connection details, organic social calendar, app selection for growth, funnel diagnostics, product-page fixes, navigation/search UX, site speed, checkout trust/A/B testing, VIP campaigns, weekly routine, and general Sidekick workflow) are indexed in section 10 for the pass-2 merge to route correctly.
- **Thin on "how" in places.** The source names the default-package-weight setting and the risk of getting it wrong, but gives no method for calculating the right empty-box weight beyond "weigh your actual packaging." Domain connection for an externally purchased (non-Shopify) domain is mentioned but the DNS steps are not walked through. The Shopify Payments billing threshold for shipping labels is stated to depend on "account activity and store history" with no number or formula given.
- **No conflict with other sources found within this document** — it is internally consistent, though it repeatedly hedges its own click paths ("verify the current interface") given how often Shopify's admin changes. Compare against other 05-SET sources for the same steps once more mini playbooks exist; no cross-source comparison was possible from this document alone.
- **Legal/tax disclaimer stated explicitly.** The source is clear that its tax section is configuration guidance only, not legal or tax advice, and tells the merchant to keep records and use a professional. Do not treat the "physical presence" framing as a complete nexus rule for any given jurisdiction. [web check: current nexus rules per jurisdiction before advising a client]

## 10. Card index

- [2f5a7287fedc] Initializing a Shopify account and choosing a store name
- [d81e9a676d16] Setting up Shopify Payments with exact legal identity match
- [9f3db093361a] Defining physical presence for tax collection
- [70512e56f11a] Building shipping zones for domestic and international delivery
- [96efb19e76e2] Setting default package weights so calculated rates do not undercharge
- [f1fa31262a90] Connecting a custom domain and a business email address
- [3a6ca3eb1bff] Testing checkout, tax and policy links with test mode transactions
- [9921264a1167] Installing tracking and verifying it fires before launch
- [64e08ffbebfb] Publishing required legal and policy pages before removing the password
- [a14524485a10] Doing store setup in the right order to avoid launch breakage
- [d6854b97be2c] Verifying each setup step actually worked
- [5a93770b958e] Configure Shopify Legal Business Name and Address Before Anything Else
- [12b76f909fb9] Add First Products with Descriptive Titles, Weight and Dimensions
- [73ad1a753e69] Organize Products into Manual or Smart Collections for Findability
- [ea68a79d73c2] Choose and Customize a Shopify Theme, Then Restyle It
- [62bc837b1167] Set Up Navigation Menus with Nested Submenus
- [4f9700a6e477] Connect or Buy a Domain and Set It as Primary
- [0949813570ce] Enable Two-Step Authentication Before Activating Shopify Payments
- [ae4e374138b3] Activate Shopify Payments with Exact Legal Names to Avoid Verification Holds
- [cb2ff7113ded] Set Payment Capture, Wallets and Customer Contact Defaults
- [0475c2317d11] Build Shipping Zones and Rates Without Undercharging
- [b1cd95fe8167] Add a New Shipping Zone to a Specific Country
- [e3d04df66513] Set Default Package Weights and Dimensions to Prevent Shipping Undercharges
- [5c69503ff6eb] Configure Local Delivery, Store Pickup and Shipping Labels with Billing Thresholds
- [61a98d182026] Review Shipping Insurance Coverage Before High-Value Shipments
- [eb0639f2f194] Set Up a Repeatable Fulfillment Workflow with Bulk Processing
- [ecbee7e2499a] Publish Return and Refund Policies and Enable Self-Serve Returns
- [9ab062ef593f] Configure Sales Tax Based on Physical Presence and Set Duties for International Markets
- [94700fd0e277] Run Test Orders in Shopify Payments Test Mode Before Launch
- [ab549d0194fc] Run a Pre-Launch Audit of Products, Policies and Navigation
- [b915be273681] Remove Password Protection to Go Live and Announce Launch
- [8493c303ca6d] Use Campaigns and UTM Automatch Rules to Attribute Marketing in Shopify (out of 05-SET scope → 06-MEA)
- [1e109800dd1b] Choose a Shopify attribution model by marketing goal (out of 05-SET scope → 06-MEA)
- [d458f58e2ffa] Set up campaign tracking activities and a morning marketing report (out of 05-SET scope → 06-MEA)
- [0cbef48284c3] Set up marketing automations for welcome, cart recovery and lifecycle messages (out of 05-SET scope → 14-EML)
- [5ceb388ec702] Use Shopify Messaging campaigns within the free email allowance (out of 05-SET scope → 14-EML)
- [241fe26f97c1] Build targeted customer segments for email and offers (out of 05-SET scope → 14-EML)
- [08b80874b674] Connect Meta (Facebook/Instagram) and TikTok to Shopify before running ads (boundary with acquisition; kept in section 3.15 as an app-connection setup step)
- [c2a9e36b5b45] Run an organic social content mix with clear paths to purchase (out of 05-SET scope → 13-ORG)
- [60e0c0a3ad53] Vet Shopify apps before installing (kept in section 3.15; general app-store hygiene)
- [88e1f0388bb2] Match app choices to the marketing job you need done (out of 05-SET scope → 14-EML/13-ORG)
- [a0544e91dab6] Find your largest funnel drop-off with the conversion rate breakdown report (out of 05-SET scope → 07-LPG)
- [41414136b4ab] Fix product pages: visuals, descriptions, trust signals and CTA (out of 05-SET scope → 07-LPG)
- [613ebaa5552e] Reduce navigation friction with click depth, clear categories and mega menus (out of 05-SET scope → 07-LPG)
- [2feda79ef81c] Improve site search with predictive text and synonyms (out of 05-SET scope → 07-LPG)
- [14f8bc81657f] Diagnose and reduce site speed problems (out of 05-SET scope → 08-SPD)
- [8f9f02d8611d] Cut checkout friction: payment options, forms and cost transparency (out of 05-SET scope → 07-LPG)
- [a23f9e5da162] Build checkout trust with badges and concrete delivery dates (out of 05-SET scope → 07-LPG)
- [87e84f54a8e0] Set up abandoned cart and abandonment recovery flows (out of 05-SET scope → 14-EML)
- [1cb48ec66159] Run a VIP campaign using top products, a segment and an exclusive code (out of 05-SET scope → 14-EML)
- [8f76661ea3a5] Test one variable at a time and watch real behavior with heat maps (out of 05-SET scope → 07-LPG)
- [caa00f2a301f] Keep a weekly marketing routine of one email, your post goal, one data-driven change (out of 05-SET scope → 14-EML)
- [d32ab6d8ae7a] Use Sidekick across setup, analysis and creative tasks (cross-cutting; kept as a principle/tool note in sections 2 and 6)
