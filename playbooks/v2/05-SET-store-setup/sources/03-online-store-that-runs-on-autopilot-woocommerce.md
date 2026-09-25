# How To Start an Online Store That Runs on Autopilot (WooCommerce Tutorial)

source_id: 1Eo73m6KopdFsRGjBWkSbOtUGiM8oYMA0  |  folder: /05-SET-store-setup  |  cards: 47  |  words: 25,059  |  type: transcript (1 YouTube tutorial video, auto-captioned, no timestamps in the export)

credibility: The presenter is Ferdy Korpershoek, a website-building YouTuber who says he has made websites since 1999 and with WordPress since 2011. He builds a demo furniture store ("SofaSupa") live on screen and narrates every click. He states plainly that he earns affiliate commissions from several tools he demonstrates: Hostinger (web hosting), the Blocksy Pro theme, Elementor Pro, and by implication other linked tools on his own site (ferdy.com). He also mentions making "$411,000" from affiliate marketing on his own channel as a personal example, not a proven method. Evidence throughout is his own demo store, not client data, studies, or controlled tests; several settings (colors, prices, thresholds) are arbitrary choices made on camera to illustrate mechanics, not benchmarks. Treat every dollar figure and UI click path as illustrative, not as ecommerce best practice or current pricing.

date signals: No year is stated in the transcript body, though the source header/title implies a current WordPress tutorial is separately referenced ("WordPress tutorial 2026" mentioned as a companion video). The presenter says he has used Hostinger "for seven years" and has been building sites with WordPress "since 2011." He references a "Stripe account" tutorial as "already five years old" but still calls it relevant. All hosting prices, plugin names, plugin install counts, and admin screen layouts are dated to whenever this video was filmed; WordPress, WooCommerce, Hostinger, Stripe, PayPal, and OmniSend interfaces change often. File modified 2026-09-19.

## 1. What this source is for

It walks an operator through building a WooCommerce store from zero: buying hosting and a domain, installing WordPress and a theme, creating every WooCommerce product type, configuring shipping and tax, connecting payment gateways, handling incoming orders, branding transactional emails, and connecting an email marketing tool (OmniSend) for opt-ins, welcome automation, abandoned-cart recovery, and segmentation. It is a single continuous walkthrough, not a reference manual, so its steps are best read as one build order. Theme customization detail, SEO plugins, and affiliate-marketing strategy also appear here but the library places their canonical home in 04-BRD, 15-SEO and 13-ORG respectively; this source is kept whole because the presenter interleaves them with setup steps.

## 2. Principles

1. **A brand-new WordPress/WooCommerce install should be cleaned before anything is built on it.** Condition: right after installation, before adding products, pages, or shipping rules. Bulk-deactivate and delete unused default plugins, trash default pages and posts, and delete all but one theme, so the dashboard stays scannable and no dead demo content gets indexed. [16eefae8f3dd] [f0ee1de989fe]
2. **The site title should say what buyers search for, not that a website exists.** Condition: naming any new store. A generic phrase like "my website" or "welcome to my site" never matches a buyer's search intent; a concrete phrase describing the product and market does. Source's worked rewrite: from "My WordPress Website" to "Prima Sofas for USA and Canada." [22fe54d9d081]
3. **Product type must match how the item is actually sold and fulfilled, or checkout math breaks.** Condition: creating any WooCommerce product. Simple = one option, tangible; Variable = multiple options (size/color) needing generated variations; Simple+Virtual = a service with no shipping; Simple+Virtual+Downloadable = a digital file delivered automatically and unlimited times; External/Affiliate = a product you promote but do not sell through your own checkout, inventory, or shipping. A wrongly typed product (e.g. a physical item marked downloadable) breaks shipping and tax calculation. [8c5a95292bdc]
4. **Global color and font settings should be set once at the theme level, not per page.** Condition: rebranding an imported template or setting brand colors for the first time. The source's theme (Blocksy) exposes six palette slots used consistently sitewide; changing slot 1 (the primary/accent color) updates every instance at once. This is theme-customization work that the library routes to 04-BRD, but it appears here because it happens during the same build session. [6429dec45a84]
5. **Shipping cost should scale with cart value or weight through zone-based table rates, not one flat fee.** Condition: selling to more than one country or wanting a free-shipping incentive. Configure a shipping zone per country, add tiered price or weight brackets inside it, and add a free-shipping threshold. Bracket edges must not overlap or leave gaps, or some carts will have no available shipping method at checkout. [6d28f39a903a] [cae87027d082]
6. **Tax should be split into standard, reduced, and zero classes, and price display should be consistent end to end.** Condition: enabling WooCommerce taxes for the first time, especially with a mixed catalog (physical goods, books, digital). Assign the correct tax class per product, then choose a single price-display mode (inclusive or exclusive of tax) and apply it consistently across shop, cart, and checkout so the number a buyer first sees matches what they pay. [64c13e521d9a] [120d8c76c9ef]
7. **Legal pages should be drafted fast with AI, then placed in a dedicated footer menu.** Condition: preparing to launch. AI-drafted privacy policy and terms text is a starting point, not legal advice; the source explicitly frames it that way. Put these pages in their own "Legal" menu and assign that menu to the footer location so they are reachable sitewide without cluttering primary navigation. [4a64696a8718] [4ca98aa08031]
8. **Always connect payment gateways in test/sandbox mode before going live.** Condition: enabling Stripe or PayPal for the first time. Place a full sandbox test order, confirm the order status and both buyer and seller emails fire correctly, then switch to live mode and place one small real order to verify before sending traffic. [6a3060c2e498] [5ef2e7c0343a]
9. **Order status changes drive the customer emails; the only manual step left for physical goods is shipping.** Condition: after checkout, payments, shipping, and tax are configured. A paid order starts at Processing; moving it to Completed after the item ships fires the "completed" email. Digital products and services need no manual shipping step at all. [21c0848f9464]
10. **Transactional emails should carry the store's branding, not the plugin default look.** Condition: right after WooCommerce and email automation are connected. Copy the site's accent color into the email style settings, add the logo, and rewrite the heading/body copy in settings; deeper hard-coded strings require copying the WooCommerce email template PHP file into the theme (source warns this file will be overwritten by theme updates unless done in a child theme). [153e99ddf6bc]
11. **An opt-in discount pop-up should be styled to match the site and gated by a trigger, not shown instantly to everyone.** Condition: building an email list via on-site capture. Use a delay (time on site), a scroll percentage, or exit intent as the trigger, and set a re-display frequency (e.g. once per day) so dismissed visitors are not spammed. [05381758c277]
12. **A welcome automation should fire immediately on signup and reuse one unique, single-use, time-limited discount code across the whole sequence.** Condition: any opt-in offering a first-order discount. Generate the code once via the platform's "unique discount code" element, set its expiry once (the platform recalculates it per recipient), and do not touch the expiry setting on later emails in the same sequence. This makes the code trackable to one contact and unusable twice. [996959f153ce] [a0598dd568d9]
13. **Abandoned-cart emails should trigger on a realistic inactivity window, not the fast demo window.** Condition: recovering carts where a shopper added an item but did not check out. The source used one hour in a real setup and only shortened it to one minute for demonstration on camera. [02c225352111]
14. **Segment subscribers by behavior and value, then trigger different offers per segment.** Condition: list large enough to have engagement history. Build segments such as inactive (no opens/purchases in recent weeks or the last ~20 emails), high-value (active openers who also buy), recent buyers, and region, then trigger a workflow when a contact enters a segment (e.g. 15% extra discount to a high-value segment after a delay, 50% off to win back an inactive one). [0b1a8b07620f]
15. **A/B split test one variable at a time, over a long enough send, before declaring a winner.** Condition: optimizing subject lines or content in an existing automation or campaign. Duplicate into two branches, change only one thing (e.g. subject line), split the audience, and let it run long enough to be meaningful; the source explicitly warns that very short tests (his example: two days) are unreliable. [6d3a34466c86]
16. **Revenue attribution from an email platform should be read as directional, not exact.** Condition: judging whether email automation investment is worth it. Compare total store revenue to platform-attributed revenue as a rough split to guide where to invest next (more automation vs. more list-building), not as an exact P&L. [f836216a37bb]
17. **When deciding what to learn next, match the investment to the store's actual bottleneck.** Condition: store is live and functioning. The presenter's own priority order is SEO (to be found) then email marketing (to monetize existing traffic), with affiliate marketing treated as an optional separate income stream, not a core requirement. This is a stated personal opinion, not a universal rule; the source itself says the store's actual weak point should drive the choice. [6303415d3bb8]

## 3. Procedures

### 3.1 Buy hosting, claim a free domain, and install WordPress
[359dabdafbc0] [verify UI] [web check: current Hostinger plans, prices and promo terms]
1. Go to the hosting provider's site and open its plan comparison page. The source compares three Hostinger tiers: Premium (up to 25 websites, 25 GB SSD storage), Business (up to 50 websites, 50-55 GB NVMe storage, up to 5 mailboxes per site, daily backups, free CDN), and a third "Cloud Startup" tier not detailed in the transcript.
2. Pick a plan and a commitment length; the source's example: Business plan at $3.99/month over 48 months = $192.52 total, or $172.37 with a 10% promo/affiliate discount code; or $4.49/month over 12 months = $53.89/year. [web check: current prices, these are dated]
3. Register with email/password, fill in billing details; adding company details may remove VAT for some countries. Choose a payment method (card, PayPal, or local options shown based on your country).
4. In onboarding, choose: website for yourself or your business → create a new website → WordPress → set admin email/password → create a blank website (skip AI-generated or theme-preview options if you want a clean base).
5. Claim the included free domain: choose an extension (.com or local), fill in registrant details, confirm via the verification email sent to your inbox.
6. When asked for target audience location, pick the server region closest to your buyers (the source notes CDN still keeps load times fast globally, but choose the closest region to your focused market anyway).
7. Wait for WordPress to install (a few minutes) and for the real domain to activate; typically about 10 minutes, rarely up to 24 hours. The site is reachable on a temporary domain in the meantime.
8. Log into the WordPress dashboard ("backend") via the hosting panel's "WP Admin" link; confirm the connection shows secure (HTTPS).

### 3.2 Clean the fresh install and set core settings
[f0ee1de989fe] [16eefae8f3dd] [verify UI]
1. Dismiss the dashboard welcome notice; open Screen Options and turn off widget panels you don't use.
2. Go to Plugins → select all → Bulk Actions → Deactivate → Apply; select all again → Bulk Actions → Delete → Apply. This removes preinstalled tools (e.g. a caching plugin) you may not need yet; add a caching plugin back later if required.
3. Go to Pages → select all → Move to Trash → Apply → open Trash → Empty Trash. Repeat for the single default Post.
4. Go to Appearance → Themes; for every inactive theme open Theme Details → Delete, leaving exactly one theme.
5. Edit your user profile: set first name, last name, and nickname; choose the public display name (this becomes the "Howdy [name]" label and the blog post byline); optionally link the same email to a free Gravatar account for a profile photo.
6. Go to Settings → General: set site language, timezone (choose your city, e.g. Amsterdam), date format, time format, and first day of week; save.
7. On the same screen, replace the Site Title with a concrete, search-matched phrase (see Principle 2) and write a one-line Tagline stating a concrete promise (source's example: "we deliver in the USA and Canada").

### 3.3 Install a theme and import a starter site (or skip to manual WooCommerce)
[fc3e397bfa08] [35896aa4b3ce] [verify UI]
1. Go to Appearance → Themes → Add New, search for the theme by name (source uses the free "Blocksy" theme), install, activate, and install its companion plugin when prompted.
2. Delete the previously active default theme (e.g. the current year's default WP theme) so only one theme remains.
3. Open the theme's starter-sites screen, filter to Free plans, then filter category to e-commerce; preview each candidate and close the ones you reject.
4. Import the chosen template. Choose the page-builder variant offered (source supports Gutenberg and Elementor, and notes the Elementor variant is missing some front-end effects such as hover zoom); pick Gutenberg for the full feature set.
5. If WooCommerce is not yet installed, the import installs it automatically; otherwise the option is greyed out. Finish the import and view the imported site; inspect a demo product page (breadcrumb, title, price, short description, add-to-cart, related products) to confirm the template works.
6. If you prefer to build without a template: go to Plugins → Add New, search "WooCommerce," install and activate it directly (see 3.4).

### 3.4 Install WooCommerce manually and run the setup wizard
[35896aa4b3ce] [verify UI]
1. Plugins → Add New → search "WooCommerce" → Install Now → Activate.
2. Check "set up my store" to enter the onboarding wizard (or run it later from WooCommerce settings).
3. Choose "I'm just starting my business" or the applicable alternative; continue.
4. Select your industry and the store's physical location; the country selection sets the default store currency (choosing United States sets USD).
5. Enter an email address, continue, and skip optional steps you can configure later.
6. Confirm the front end now shows Cart, Checkout, My Account, and Shop pages. Note: WooCommerce places the storefront in "coming soon" mode by default; you must explicitly turn this off before real traffic can buy (WooCommerce → Settings → General, or the "Store coming soon" bar shown on the front end).
7. Clean up the leftover WooCommerce setup panel from the dashboard via Screen Options.

### 3.5 Brand the theme: colors, logo, favicon, menu
[6429dec45a84] [ed8a244d941c] [2228f1a54227] [verify UI]
1. Open Appearance → Customize; find the theme's global color settings (source's theme exposes 6 palette slots).
2. Paste your primary brand color into slot 1; watch it propagate sitewide. Fill remaining slots with tints/shades of the same family so hover states stay coherent.
3. Upload a logo, preferably SVG for sharpness and small file size (source's example logo was about 4 KB); set logo height (source used ~35 px); fill in alt text and description.
4. Set the site icon (favicon) under Site Identity: a square image with transparent background.
5. Open Customize → Menus → Main Menu: delete redundant entries (e.g. a "Home" link, since the logo already links home); drag items to reorder; drag an item right to nest it as a sub-item.
6. Pick a menu hover style (source preferred a simple color-change hover over animated variants); reduce inner spacing between items (source used ~30 px); set link font color to a darker palette slot and hover color to the accent slot.
7. In header settings: choose an icon set, optionally add a header background color, reduce header height, enable "sticky" if you want the header to remain visible while scrolling (test on mobile first, since sticky headers eat vertical space on phones), and mark this header as the sitewide global header.
8. Open Customize → General → Layout: set container width to about 1120 px (source calls this a reliable general default). Open WooCommerce → Single Product in the customizer and switch to the narrow single-product width.
9. If a section background looks mismatched after import, use a browser color-picker extension to sample the surrounding correct color, open the block in the block editor, go to Styles → Background, and paste the sampled hex (or leave the section transparent, which the source found looked better in their case). [f0f548d0227a]
10. Set typography and the shop archive layout: pick fonts at fonts.google.com (filter by category, e.g. sans-serif); use one font for headings and a different one for body text. In the Customizer's typography settings, set the base (body) font (source used "Open Sans") and the heading font (source used "Nunito Sans"); apply the heading font to the menu as well and adjust capitalization, letter spacing (source used ~0.05), and size. On the WooCommerce product archive settings, reduce or remove the large page-title area so products sit higher on the page; toggle whether price and "add to cart" show on archive cards; drag to reorder archive card elements (image, title, price, rating, taxonomies); set image corner radius (source used 1em, about 16px); match price/taxonomy/button colors to the brand palette; add custom CSS (e.g. rounded buttons) under Additional CSS. [955efb44177f] [verify UI]

### 3.6 Create a Simple product
[b5dc14ff91f1] [verify UI]
1. Products → Add New; enter the product name and publish to see the bare product page, then edit it further.
2. Add a long description (shows below the fold) and a short description (shows next to the price).
3. Under Product data, keep type "Simple"; leave Virtual and Downloadable unchecked for a physical item.
4. Set the regular price; if running a promotion, set a sale price and sale end date so the regular price returns automatically (source's example: Santorini couch, regular $1,999, sale $1,399, ending last day of the month).
5. Under Inventory: set a SKU; enable stock management and enter quantity; choose a back-order policy (disallow = safest; allow with notification; allow silently, which only works if you can restock fast); set a low-stock notification threshold (source used 2); optionally enable "sold individually" to cap one unit per order.
6. Under Advanced: set a purchase note (e.g. a scheduling link, for service-adjacent products).
7. Upload a featured image (used as the archive thumbnail) and gallery images; copy the product title into each image's alt text and description.
8. Assign a category (parent or sub-category, e.g. Furniture → Sofas) and tags (material, color, style) for breadcrumb and filtering.

### 3.7 Build a Variable product with attributes and swatches
[51f236113f57] [verify UI]
1. Install a variation-swatches plugin (source uses the Brainstorm Force one) via Plugins → Add New.
2. Go to Products → Attributes; create one global attribute per option type (e.g. "Size" as type Label, "Color" as type Color), each with a shape (e.g. circle) and pixel size (source used 36 px).
3. Populate each attribute's terms: for Size add XS, S, M, L, XL, 2XL, 3XL (reorder them; new terms can appear in reverse order); for Color add each color name and its swatch hex (paste exact hex if matching brand colors).
4. Create a new product; set Product data type to "Variable"; under Attributes, add each global attribute and tick only the values this specific product has (e.g. XS, M, L, XL and black, white, navy, not every term).
5. Click "Generate variations." The count equals the product of selected values (source's example: 4 sizes x 3 colors = 12 variations).
6. Use bulk actions on the variations list to toggle stock management across all, set a base regular price (source used $19.99), then override outliers individually (e.g. XL at $24.99, which makes the product page show a price range).
7. Override stock per variation where demand differs (source's example: XS black = 3 units, L black = 10 units).
8. Assign a featured image and gallery, then open each variation individually and assign its own image so selecting a color swaps the displayed photo; this is a one-time setup per variation.
9. Optionally set default form values (e.g. large + navy pre-selected) and, in the swatches plugin's global styling, adjust border width and swatch alignment (source added custom CSS to center swatches on the product page, found via the presenter's own tutorial site).

### 3.8 Create a Service product (virtual, non-shippable)
[8c5a95292bdc] [verify UI]
1. Products → Add New; name it (source's example: "coaching call, 60 minutes").
2. Upload a product image.
3. Under Product data keep type "Simple" but check "Virtual" so no shipping is charged.
4. Set the regular price (source's example: $2.99 for one hour).
5. Add a short description; under Advanced, add a purchase note with a scheduling link (e.g. a Calendly URL) so the buyer knows the next step.
6. Under Inventory, enable "sold individually" if the offer should be capped at one unit per order (e.g. exactly one hour, not multiple).

### 3.9 Create a Downloadable digital product
[8c4b61afe68a] [verify UI]
1. Products → Add New; name the digital item (source's example: "ebook affiliate marketing for beginners").
2. Upload a product image.
3. Under Product data, keep type "Simple," check both Virtual and Downloadable.
4. Set the regular price (source used $14.99).
5. In the Downloadable Files section, add the file: upload it to the media library and paste its URL into the field, or select an existing media item.
6. Set the download expiry: leave blank for never-expiring, or set a day limit (source's example: 365 days) if you want to cap access.
7. Add short/long descriptions, assign a category (e.g. "eBooks"), and publish.
8. Optionally enable "sold individually" so one buyer cannot purchase the same download twice in one order.
9. Test the full purchase flow to confirm the download link is delivered after payment.

### 3.10 List an External/Affiliate product [dropshipping assumption: this is not dropshipping — you never take the order or the payment; the buyer completes checkout on the partner's own site and you earn a referral commission]
[2b411bc7b12e] [a33f88e1cb66] [verify UI]
1. Copy your affiliate link for the partner product.
2. Products → Add New; name it after the partner's product; upload a product image (source recommends first fixing odd aspect ratios in an image editor, e.g. expanding canvas to a square such as 1000x1000 px, so it doesn't display cropped on the shop archive).
3. Change Product data type to "External/Affiliate." This removes inventory and shipping fields entirely.
4. Paste the affiliate link into the Product URL field; set button text to match the destination's call to action (e.g. "Buy now," "More information," "See plans").
5. Enter a price context (source's example: "from $5 per month," shown as a starting price, not a fixed one).
6. Add a short/long description and a category (e.g. "Tools"); publish.
7. Open the live product and click the button to confirm the affiliate link and any tracking parameters survive the round trip.
Note: because this product type leaves your own checkout, your own payment, tax, shipping, and coupon rules never apply to it.

### 3.11 Add upsells and cross-sells
[dc9a53011770] [verify UI]
1. Open a product → Product data → Linked Products.
2. Add one or more products to the "Upsells" field; these display on that product's page (theme-dependent, often labeled "you may also like").
3. Add one or more products to the "Cross-sells" field; these display in the cart below the line items, and only when the triggering product is in the cart.
4. Update and verify on the live product page (upsells) and cart page (cross-sells); removing the triggering product from the cart also removes its cross-sells.

### 3.12 Set currency and store locale
[04228274dbbb] [verify UI]
1. WooCommerce → Settings → General.
2. Set the store's country first, since it determines the default currency.
3. Choose the currency symbol and its position (before/after the amount).
4. Set the thousand and decimal separators to match your market's convention, and the number of decimal places (source used two).
5. Save, then check a product page, cart, and variable-product price range to confirm correct display everywhere.
Note: changing currency after publishing does not convert existing prices; each must be updated manually.

### 3.13 Restrict selling locations and set up flexible table-rate shipping
[6d28f39a903a] [cae87027d082] [cb975a996a4d] [verify UI]
1. WooCommerce → Settings → General → Selling Locations: choose "Sell to specific countries" (or "all except") and list your target countries (source's example: United States and Canada).
2. WooCommerce → Settings → Shipping → Shipping zones: remove any default free-shipping method left over from onboarding.
3. Install a table-rate plugin (source uses "Flexible Shipping" and refers to it via the vendor name Octolize; the transcript describes it as having "more than a hundred thousand installations"). [web check: current plugin name and install count]
4. Add a shipping zone per country you sell to; inside it, add a flexible/table-rate shipping method; name the carrier (source used "UPS" for the US, "FedEx" for Canada, as labels only, not integrations).
5. Set a free-shipping minimum order value (source's US example: $200; Canada example: $300).
6. Build price-based bracket rules under the free-shipping minimum. Source's illustrative US brackets: $0-$99.99 = $6.99 (also shown as "$0-$90.99" at one point, likely a rounding slip in narration), $20-$49.99 = $8.99, $50-$99.99 = $12.99, $100-$199.99 = $14.99.
7. Check brackets for gaps or overlaps before saving; a cart's value must land in exactly one bracket or checkout will show no shipping option.
8. Optionally switch the rule basis to weight instead of price; set product weight/dimensions on each product, and set the store's weight/dimension units under WooCommerce → Settings → Products.
9. Optionally enable a "left for free shipping" progress-bar notice in the plugin so shoppers see how much more to add.
10. Repeat the whole zone setup for each additional country, using that country's own rates and free-shipping threshold.
11. Test multiple example carts near each bracket boundary and near the free-shipping threshold, in each destination country, to confirm the correct rate always appears.

### 3.14 Configure tax classes, rates, and price display
[64c13e521d9a] [291aa05299b3] [a16dd21fbfc9] [120d8c76c9ef] [verify UI] [web check: current tax rates and rules for your jurisdiction]
1. Ensure the store address is filled in under WooCommerce → Settings → General.
2. Enable taxes on that same screen; a "Tax" tab appears.
3. Understand the three built-in classes: Standard (most physical goods), Reduced (source's example: books), Zero (source's example: digital products in the US). Add custom classes if needed (source demoed adding a "cool rates" class, then removed it).
4. In Tax → Standard Rates, add one row per country/state you must charge in: set Country Code (e.g. US), State Code where relevant (e.g. CA, NV), and the rate to four decimal places (source's example rate: 7.2500%, sourced from a tax-lookup service the presenter calls "TaxJar" — this looks like an affiliate link on the presenter's own site) [affiliate recommendation]. Repeat per state; do not try to approximate multiple states with one blanket row.
5. Set Reduced and Zero rates per country the same way (source's illustrative examples: US standard 20%, US reduced 10%, US digital 0%, Canada standard 30% — these are demo numbers, not real tax advice).
6. Decide whether to charge tax on shipping (source: turn it on if you sell to companies).
7. On each product's General tab, assign the correct Tax Class (standard/reduced/zero) — this is what actually determines the rate applied at cart and checkout, more than the store-wide default.
8. Choose price-display settings: whether you enter prices inclusive or exclusive of tax, and whether the shop, cart, and checkout each display inclusive or exclusive. The source's stated preferred setup for a hybrid B2B/B2C store: enter prices inclusive of tax, and display inclusive of tax at every stage (shop, cart, checkout), so the number a shopper first sees matches what they pay — modeled on how the presenter says Coolblue's site behaves.
9. Alternative: leave everything manual and accept the workload, or install a paid automated-tax plugin (source names "WooCommerce Tax") to avoid state-by-state entry. [affiliate/product recommendation, unverified pricing] [web check]
10. Place a test order for one product of each tax class (standard, reduced, zero) and to at least two different states/countries, and confirm the tax line matches expectations each time.

### 3.15 Generate and publish legal pages
[4a64696a8718] [4ca98aa08031] [verify UI]
1. Prompt an AI assistant with your product category and countries sold to; ask which legal pages you need and have it draft the content, and ask what company details it needs from you (source's prompt pattern: "I sell [category] in [countries]. Which legal pages do I need? Create the content, and tell me what info you need from my company.").
2. Supply your legal company name, business address, and product category so drafts are specific.
3. Create a WordPress page per document (source's examples: Privacy Policy, Terms and Conditions) and paste the generated content into each; publish.
4. In the Customizer, create a new menu (source names it "Legal") containing only these page links, separate from the primary navigation.
5. Assign the Legal menu to the footer menu location; edit the footer to remove placeholder info and insert this menu.
6. Load the live site and click through the footer links on desktop and mobile to confirm they resolve correctly.
Note: this AI-drafted text is explicitly framed by the source as a starting draft, not legal advice; have it reviewed against your actual jurisdiction and business model before relying on it.

### 3.16 Connect Stripe and PayPal, test, then go live
[6a3060c2e498] [5ef2e7c0343a] [verify UI] [web check: current plugin names, connection flow]
1. If you don't have a Stripe account yet, create one first (source points to a separate, older tutorial for this step and does not walk through Stripe account creation here).
2. Plugins → Add New → search "WooCommerce Stripe" → install the official "WooCommerce Stripe Payment Gateway" plugin → Activate.
3. Connect your account through the plugin's on-screen connect flow; it redirects back to WooCommerce once linked.
4. Enable Test Mode; create/connect a test account, which generates the required webhook (payment enabled / payout enabled / webhook enabled should all show).
5. Set the statement descriptor (the name shown on the buyer's bank/card statement) to your company name.
6. Place a full sandbox test order using the provider's test card; confirm both the buyer confirmation email and your own new-order notification email arrive, and that the order appears correctly in WooCommerce → Orders.
7. Decide where Apple Pay / Google Pay (express checkout) buttons appear: on product pages (faster impulse purchase but a separate checkout path that can bypass some cart logic) or checkout-page only (cleaner product page). Toggle accordingly and re-test.
8. When ready to go live: WooCommerce → Settings → Payments → Stripe → Manage → Settings; uncheck Test Mode; save. Place one small real order with a real card to verify live mode end to end.
9. Repeat a parallel flow for PayPal: Plugins → Add New → search "WooCommerce PayPal" → install "WooCommerce PayPal Payments" → Activate → complete the account-setup wizard (choose "business," select "physical/virtual products," connect your PayPal business account) → enable it.
10. In WooCommerce → Settings → Payments, drag to set the display order of payment methods at checkout (source put credit card above PayPal).
11. In Customize → WooCommerce → Checkout page, hide fields you don't need (company name, second address line), make phone optional/hidden if not needed, and select your Privacy Policy and Terms pages so the "read and agree" checkbox links to the correct pages.

### 3.17 Handle incoming orders and manage order status
[21c0848f9464] [verify UI]
1. WooCommerce → Orders; open a paid order.
2. Confirm the buyer received the default "processing" confirmation email and you received the admin "new order" notification.
3. For physical goods: once shipped, open the order and change status from Processing to Completed; this fires the completed-order email to the buyer.
4. Use Cancelled or Refunded statuses as needed.
5. Note that digital products and services require no manual shipping step at all; the only manual action across the whole flow is dispatching physical goods.

### 3.18 Brand the transactional emails
[153e99ddf6bc] [verify UI]
1. WooCommerce → Settings → Emails: review the list of customer-facing and admin-facing emails, each with a preview.
2. Copy the site's primary accent color from the Customizer's colors panel and paste it into the email style color field so buttons/accents match.
3. Upload your logo into the email header, set its size (source used 120) and alignment; confirm the site title/store address text that appears lower in the email footer.
4. Edit the visible heading and "additional content" text for key emails (e.g. the processing-order email).
5. For hard-coded template strings not exposed in settings: Appearance → Theme File Editor → WooCommerce → emails → open the relevant PHP template and edit the text directly. The source explicitly warns this file lives in the theme and can be overwritten by a theme update; in practice, do this edit in a child theme instead of the parent theme.
6. Set the "From" name (e.g. "[Your name] from [Store]") and "From" address so replies route correctly.
7. Send a test email or place a real test order to confirm the change renders.

### 3.19 Connect OmniSend and set up email marketing
[349933913a28] [verify UI] [web check: current OmniSend pricing and free-tier limits]
1. Sign up at OmniSend with a business email; verify via the confirmation link sent to that inbox.
2. Enter store details (name, URL), current platform (WooCommerce), prior email provider (or "none"), business address, and time zone.
3. Download the OmniSend WooCommerce connector plugin from the OmniSend dashboard; in WordPress go to Plugins → Add New → Upload Plugin, upload the file, Install → Activate.
4. In WordPress, click "connect your store to OmniSend," log in, and approve the requested permissions.
5. OmniSend attempts to auto-pull your site's branding colors; if it misses, manually set accent/dark/light colors (copy from the Customizer), upload a logo PNG, choose heading fonts, and optionally add social links; save brand assets.
6. If migrating an existing list from another provider, use OmniSend's migration form (source states the vendor claims completion within five business days — a vendor claim, not verified). [affiliate/vendor claim, unverified]
7. Free tier note: source describes a cap around 500 sends/month and 250 contacts, with OmniSend branding shown on forms; source's example paid tier was $11.20/month (stated as "30% off") for up to 500 contacts, scaling automatically past that, including some free SMS credits, AI features, and 24/7 support. [web check: current OmniSend pricing, these figures are dated and possibly promotional]

### 3.20 Build a discount opt-in pop-up
[05381758c277] [verify UI]
1. In OmniSend, go to Forms; choose a template (source used a simple pop-up offering a first-order discount).
2. Edit the heading/copy; add a first-name field (remove its placeholder label so it reads naturally) in addition to email.
3. Match the site's styling: button corner radius, field radius, fonts, and colors; match the success-message styling to the site's existing tone.
4. Set display rules: trigger after a time delay (source's range: 3-10 seconds), after a scroll percentage (source used 30%), or on exit intent; set a re-display frequency (source used once per day) after a visitor dismisses it.
5. Choose display type (pop-up, flyout, landing page, or embed) and device targeting (all devices, or desktop/mobile only).
6. Only include a phone number field if you plan to send SMS; otherwise remove it to reduce friction.
7. Enable the form; because the plugin is connected to the store, this makes it live on-site immediately.

### 3.21 Build a welcome automation with a unique discount code
[996959f153ce] [ec7dfdb364bb] [a0598dd568d9] [verify UI]
1. Copy the opt-in form's name so you can match it to the workflow trigger later.
2. In Automation, choose a welcome-workflow template (source used a 3-email version).
3. Set the trigger to "subscribed via a signup form," and add a trigger filter naming the specific form, so only subscribers from that exact form enter this workflow (prevents cross-contamination between multiple forms).
4. Remove or shorten any default wait node if you want the first email to send immediately.
5. In the first email, add a "unique discount code" element; choose percent (source used 10%) or fixed amount; set the expiry once (source used 7 days); check "reuse unique discount code in this workflow" so the same per-contact code is reused in later emails without regenerating it.
6. Personalize subject line and body with a first-name variable; style the email (button shape/color) to match the site.
7. Finish editing and start the workflow to make it live.
8. Edit the follow-up emails in the sequence (source's example cadence: immediate, then +1 day, then +4 days) to reuse the same discount element and matching styling; delete any unused leftover blocks before publishing each one.
9. Test end to end: sign up with a real or test email/name, receive the code, add a product to cart, apply the code, complete checkout, and confirm in the store's coupon list that the code is single-use with the correct expiry.

### 3.22 Build an abandoned-cart automation
[02c225352111] [verify UI]
1. Create a new workflow; select the abandoned-cart/cart-inactivity trigger.
2. Set the inactivity window to a realistic production value (source's stated production value: one hour; he used one minute only for on-camera demonstration).
3. Write a subject line that creates urgency (source's example: "items in your cart are selling out fast").
4. Insert the dynamic cart-contents block so the email shows the actual product(s) left in cart plus a return link.
5. Activate the workflow.
6. Test: add a product to cart, wait past the inactivity window, confirm the email arrives with the correct product and a working link.
Note: this only works for identifiable visitors (opted in or logged in) whose email address is already captured.

### 3.23 Build a branded order-confirmation workflow
[bccbebbbfe5d] [verify UI]
1. Create a new workflow; select the order-confirmation trigger (search "confirmation" if not obvious).
2. Edit content and button styling to match brand colors.
3. Finish editing, start the workflow.
4. Test with a real or test order; the customer should receive the platform's branded confirmation, while the store owner still separately receives the native WooCommerce order notification.
5. Decide whether to keep both the platform's and WooCommerce's default confirmation active, since both can fire and confuse a buyer if left unmanaged.

### 3.24 Build value/behavior segments and segment-triggered offers
[0b1a8b07620f] [verify UI]
1. Go to Audience Segments; use AI-assisted creation or pre-built templates.
2. Build segments such as: active subscribers, birthdays, inactive subscribers (no opens/purchases across recent weeks or the last ~20 emails), region (e.g. Europe), recent buyers, and high-value subscribers (active openers who also purchase).
3. Create a new workflow from scratch; set trigger to "entered a segment," and choose the segment.
4. Add a delay if appropriate (source's example: 10 days for a high-value segment).
5. Send a segment-specific offer (source's illustrative examples: 15% extra discount for 3 days to customers who spent over $1,000; a "we miss you" 50%-off-for-2-days offer to inactive subscribers). These thresholds and discount levels are the tutorial's own examples, not recommended numbers.
6. Activate the workflow; review segment membership periodically to confirm the criteria still match intent.

### 3.25 Run an A/B split test on an email
[6d3a34466c86] [verify UI]
1. In the workflow or campaign builder, locate the split/A-B test element and drag it into the flow.
2. Duplicate the email into two branches; change exactly one variable (source's example: subject line only, "last chance" vs. the original).
3. Split the list between branches so results are comparable, rather than sending sequentially.
4. Publish and let the test run long enough to be meaningful (source explicitly says a 2-day test is too short).
5. Compare open rate first, then clicks and sales; keep the winner as the new standard for that send.
6. Repeat on other emails in the sequence over time.

### 3.26 Add SMS, push, and tag-gated conditions to a workflow
[50ffde2a6ccb] [b3e79539406d] [verify UI]
1. If you collect phone numbers, add an SMS step alongside email steps.
2. If push notifications are supported and available, add a push step.
3. Use delay/timing controls so channels don't fire simultaneously.
4. Assign tags to contacts based on behavior or source; add a tag-check condition in the workflow so a step only fires for tagged contacts.
5. Test each channel and each tag branch separately (tagged vs. untagged contact) before activating broadly.

### 3.27 Edit homepage/landing content directly in the block editor
[ba8d266e5ef9] [5e220039b763] [verify UI]
1. Open the page for editing; triple-click (or click into) any text block to edit copy directly.
2. For a button: use the style tab for hover behavior (darken/scale) and border/shadow settings for radius; in the details/link panel, type a target product or page name so the editor auto-suggests a match.
3. For a product image block: select it, choose "select image," swap in the intended product photo; update the price text manually if shown as a static block (this can drift out of sync with the actual product price — update both whenever price changes).
4. Dynamic sections (source's example: an "Arrivals" block) are auto-fetched from the store; verify they reflect the intended products rather than trying to edit them by hand.
5. For background images/colors: Style → Background; for text color: Style → Typography.
6. To add a new content area, click the "+" or type "/" to insert a new block.
7. Switch the editor to tablet and mobile preview; fix header/menu/logo/icon styling separately at each breakpoint (source's example: setting a light background, dark menu text with an orange hover color, and a dark close-icon color specifically for the mobile off-canvas menu).
8. Publish, then re-check desktop, tablet, and mobile before considering the page done.

## 4. Rules, thresholds and numbers

| Rule | Number or threshold | Condition | Source's basis | Card |
|---|---|---|---|---|
| Domain activation time | ~10 minutes typical, rarely up to 24 hours | after claiming a free domain via hosting onboarding | presenter's account, provider-specific | 359dabdafb |
| Free-shipping threshold (US example) | $200 | source's demo store, US zone | arbitrary demo value | 6d28f39a9 |
| Free-shipping threshold (Canada example) | $300 | source's demo store, Canada zone | arbitrary demo value | cae87027d |
| Shipping bracket examples | $0-$99.99 = $6.99; $20-$49.99 = $8.99; $50-$99.99 = $12.99; $100-$199.99 = $14.99 | source's demo store, US zone | arbitrary demo values, not margin-based | 6d28f39a9, cae87027d |
| Simple product sale example | regular $1,999, sale $1,399 | demo Santorini couch, ends last day of month | arbitrary demo value | b5dc14ff9 |
| Variable product base/outlier price | base $19.99, XL outlier $24.99 | demo sweater, 4 sizes x 3 colors = 12 variations | arbitrary demo value | 51f236113 |
| Digital product price | $14.99 | demo ebook | arbitrary demo value | 8c4b61afe |
| Service product price | $2.99/hour | demo coaching call | arbitrary demo value | 8c5a95292 |
| Affiliate product price framing | "from $5/month" | demo Elementor Pro listing | partner's own pricing, presenter is an affiliate | 2b411bc7b |
| US tax rate examples (illustrative only) | standard 20%, reduced 10% (books), zero 0% (digital) | demo store, not real tax law | arbitrary demo values | 64c13e521, 120d8c76c |
| Canada tax rate example (illustrative only) | 30% | demo store, not real tax law | arbitrary demo value | 120d8c76c |
| US state rate examples | California 7.2500%, Nevada 6.85% | sourced from a third-party tax lookup service ("TaxJar") at time of filming | presenter's lookup, dated, possibly affiliate-linked | 291aa0529, a16dd21fb |
| Container width | ~1120 px | general layout default, this theme | presenter's heuristic, not a benchmark | 2228f1a54 |
| Logo size example | ~4 KB SVG file, ~35 px display height | demo store logo | presenter's example | 6429dec45 |
| Menu inner spacing example | ~30 px | demo store header | presenter's preference | ed8a244d9 |
| Swatch shape/size | circle, 36 px | demo store attributes | presenter's preference | 51f236113 |
| Download expiry example | blank (never) or 365 days | demo digital product | presenter's choice, both valid | 8c4b61afe |
| Welcome workflow cadence example | immediate, then +1 day, then +4 days | 3-email OmniSend welcome flow | demo automation | 996959f15 |
| Unique discount code example | 10% off, 7-day expiry, single use | demo welcome workflow | presenter's example, not a recommended level | 996959f15, a0598dd56 |
| Abandoned-cart trigger window | 1 hour in production; 1 minute used only for the on-camera demo | cart inactivity trigger | presenter's stated real-world setting vs. demo shortcut | 02c225352 |
| A/B test minimum duration | "2 days is too short" (no specific minimum given) | subject-line/content split test | presenter's opinion | 6d3a34466 |
| High-value segment example threshold | spent over $1,000 -> 15% extra discount for 3 days, after a 10-day delay | demo segment workflow | presenter's example, not a recommended threshold | 0b1a8b076 |
| Win-back segment example | 50% off for 2 days to inactive subscribers | demo segment workflow | presenter's example, not a recommended level | 0b1a8b076 |
| Revenue attribution example | total store revenue $1,991; $900 attributed to OmniSend | one demo test order plus one earlier sale, not a real campaign | presenter's own demo numbers, tiny sample | f836216a37 |
| OmniSend free tier example | ~500 sends/month, ~250 contacts, platform branding shown | at time of filming | vendor's stated tier, dated | 349933913 |
| OmniSend paid tier example | $11.20/month ("30% off"), up to 500 contacts, scales automatically, some free SMS included | at time of filming | vendor's stated tier, dated, presenter may be an affiliate | 349933913 |
| Hosting price examples | $3.99/mo x 48 mo = $192.52 (or $172.37 with a 10% code); $4.49/mo x 12 mo = $53.89/year | Hostinger Business plan, at time of filming | vendor's stated pricing, dated, presenter is an affiliate | 359dabdafb |
| Affiliate income claim | "$411,000" from affiliate marketing on his own channel | presenter's own, stated in passing near the end | personal claim, not verifiable, not a promise | 6303415d3 |

## 5. Diagnostics and checks

- **Fresh install is not clean.** Check: dashboard still shows demo plugins, sample pages, or more than one active theme. Good: only needed plugins active, no demo pages, one theme installed. Fix: rerun 3.2. [16eefae8f3dd]
- **Product type mismatch.** Check: a physical item is marked Downloadable, or a service is charging shipping. Bad: checkout shows a shipping charge on a service, or a digital item asks for a shipping address. Fix: edit the product's type/virtual/downloadable flags per Principle 3. [8c5a95292bdc]
- **Shipping bracket gap or overlap.** Check: place several test carts at values just under and over each bracket boundary and the free-shipping threshold, in each destination country. Bad: a cart value that matches no rule, so checkout shows no shipping method. Fix: re-edit bracket edges so every value falls into exactly one bracket. [6d28f39a903a] [cb975a996a4d]
- **Tax class or display mismatch.** Check: place a test order for one product per tax class (standard, reduced, zero) and to at least two states/countries. Bad: tax line shows an unexpected rate, or the price shown on the shop page does not match the price shown at checkout. Fix: reassign the product's tax class, or make price-display settings (inclusive/exclusive) consistent shop-to-checkout. [64c13e521d9a] [a16dd21fbfc9]
- **Coming-soon mode left on.** Check: the front end still shows a "store coming soon" bar after setup. Bad: real traffic cannot buy. Fix: turn off coming-soon mode in WooCommerce settings before sending traffic. [35896aa4b3ce]
- **Payment gateway still in test mode at launch, or vice versa.** Check: WooCommerce → Settings → Payments → Stripe status. Bad: real customers see a test-only card form, or you accidentally take real payments while still testing. Fix: confirm Test Mode is off only when you intend to go live, and always place one verification order after flipping the switch. [6a3060c2e498] [5ef2e7c0343a]
- **Order stuck in Processing.** Check: WooCommerce → Orders, physical-goods orders older than your normal ship time still show Processing. Bad: customer never receives the "completed" email. Fix: update status to Completed once shipped. [21c0848f9464]
- **Email theme edits lost after a theme update.** Check: after any theme update, re-open the customized WooCommerce email PHP template. Bad: custom copy reverted to default. Fix: keep email template edits in a child theme, not the parent theme. [153e99ddf6bc]
- **Discount code reused or leaked.** Check: the store's coupon list after a code has been used once. Bad: code shows no usage limit or no expiry despite the workflow being configured with one. Fix: confirm the store's own coupon settings actually enforce the single-use/expiry the automation platform generated. [a0598dd568d9]
- **Welcome workflow cross-contamination.** Check: the workflow's trigger filter. Bad: subscribers from an unrelated form entering this workflow. Fix: add/confirm the form-specific trigger filter. [996959f153ce]
- **Abandoned-cart trigger left at demo speed.** Check: the live workflow's inactivity setting. Bad: still set to 1 minute (a demo value) instead of a realistic window (source's real-world value: 1 hour). Fix: reset to a realistic window before going live. [02c225352111]
- **A/B test called too early.** Check: how long the split test has been running and the sample size. Bad: declaring a winner after 2 days or on very few sends. Fix: let it run longer before acting on the result. [6d3a34466c86]
- **Manually edited homepage prices drift from real product prices.** Check: static price text in a hand-edited hero/featured block versus the live product's actual price. Bad: mismatch after a price change. Fix: update both whenever pricing changes, or avoid hardcoding price text in content blocks. [ba8d266e5ef9]
- **Mobile/tablet header broken.** Check: preview the header, menu, logo, and off-canvas menu at tablet and mobile breakpoints specifically. Bad: unreadable menu text, wrong-color close icon, wrong logo variant. Fix: set background, menu colors, and icon colors per breakpoint in the theme's responsive design settings. [5e220039b763]

## 6. Tools, settings and named features

- **Hostinger**: web hosting provider used for the whole demo; plans, free domain, and pricing named are dated and the presenter is an affiliate. [verify UI] [web check] [affiliate recommendation]
- **WordPress**: the core CMS; dashboard = backend, live site = front end.
- **WooCommerce**: the ecommerce plugin; product types (Simple, Variable, Simple+Virtual, Simple+Virtual+Downloadable, External/Affiliate), Orders, Settings (General, Products, Shipping, Tax, Emails, Payments) all referenced throughout. [verify UI]
- **Blocksy theme** (free) plus its companion plugin and paid "Blocksy Pro" tier; used for starter-site import, global colors, header/menu, and layout width settings. Presenter is an affiliate for the Pro tier. [verify UI] [affiliate recommendation]
- **Variation swatches plugin** (source names the one from "Brainstorm Force"): renders visual size/color swatches on variable products instead of dropdowns. [verify UI]
- **Table-rate shipping plugin** (source refers to "Flexible Shipping," vendor "Octolize"; transcript is unclear on the exact name): tiered price/weight-based shipping rules and free-shipping thresholds per zone. [verify UI] [web check: exact current plugin name]
- **Stripe** via the official "WooCommerce Stripe Payment Gateway" plugin: card payments, Apple Pay/Google Pay express checkout, test mode and webhook setup. [verify UI]
- **PayPal** via "WooCommerce PayPal Payments": secondary payment method, connected via a business PayPal account. [verify UI]
- **TaxJar** (or a similarly named tax-lookup service): used only to look up current per-state US tax percentages to enter manually; likely an affiliate link on the presenter's own site. [web check] [affiliate recommendation]
- **"WooCommerce Tax"** (named paid add-on): automated tax calculation as an alternative to manual state-by-state entry. [web check: current pricing/availability] [affiliate recommendation, unverified]
- **Gravatar**: free service linking a profile email to a public avatar image; presenter jokes it costs "$50/month" before clarifying it's free — a joke, not a real price. [verify UI]
- **Chrome color-picker extension**: used to sample an existing background color as a hex value for matching mismatched sections. [verify UI]
- **Google Fonts (fonts.google.com)**: font selection for typography (source used "Open Sans" for body, "Nunito Sans" for headings, as one example pairing).
- **An AI assistant (referred to generically as "ChatGPT")**: used to draft a site title, legal-page content, and to answer "which legal pages do I need."
- **OmniSend**: email marketing/automation platform connected via its WooCommerce plugin; used for opt-in forms, branding sync, welcome workflows, abandoned-cart workflows, order-confirmation workflows, segments, A/B split testing, SMS/push steps, tags, and revenue attribution. Presenter states he personally switched to it from a prior tool ("Confluent," likely a mis-transcription). [verify UI] [affiliate recommendation, likely]
- **Calendly**: referenced as the scheduling link destination in a service product's purchase note. [verify UI]
- **A rank-tracking/SEO plugin** (transcript renders the name unintelligibly, something like "Shure Red" / "sure rank" — likely a mis-transcription of a real plugin name): recommended as the presenter's top follow-up priority after store setup. [web check: unclear which plugin this is; do not guess a specific name from this transcript]

## 7. Examples and case results

All figures below are from the presenter's own single demo store built live on camera, not from a real business, client data, or a controlled test. Treat every number as illustrative of the mechanism, never as a benchmark.

- **Hosting cost example**: Business plan quoted at $3.99/month over 48 months ($192.52 total, or $172.37 with a 10% promo code) or $4.49/month over 12 months ($53.89/year). [359dabdafbc0] [web check: current pricing]
- **Site title rewrite example**: "My WordPress Website" -> "Prima Sofas for USA and Canada," modeled after competitor titles found by searching "buy PS5 online." [22fe54d9d081]
- **Simple product example**: "Santorini couch," regular price $1,999, sale price $1,399 through the end of the month. [b5dc14ff91f1]
- **Variable product example**: a long-sleeve sweater with 4 sizes (XS, M, L, XL) and 3 colors (black, white, navy) = 12 generated variations; base price $19.99, XL priced up to $24.99; stock set individually per variation (e.g. XS black = 3 units, L black = 10 units). [51f236113f57]
- **Downloadable product example**: an ebook, "affiliate marketing for beginners," priced $14.99, delivered via a media-library file URL with no expiry set. [8c4b61afe68a]
- **Service product example**: a "coaching call, 60 minutes," priced $2.99/hour, sold individually, purchase note pointing to a Calendly link. [8c5a95292bdc]
- **Affiliate product example**: Elementor Pro, listed at "from $5/month," using the presenter's own affiliate link; he states explicitly that this is how he personally earns from these tutorials. [2b411bc7b12e]
- **Shipping example**: US zone with UPS-labeled flat/tiered rates ($6.99 to $14.99 across price brackets) and free shipping above $200; Canada zone with FedEx-labeled rates and free shipping above $300. [6d28f39a903a] [cae87027d082]
- **Tax example**: US standard rate demoed at 20%, reduced (books) at 10%, zero (digital) at 0%; Canada demoed at 30%; California state rate looked up at 7.2500%, Nevada at 6.85% — all illustrative, not real current tax figures. [64c13e521d9a] [291aa05299b3]
- **Welcome automation example**: a 3-email sequence (immediate, +1 day, +4 days) with a reused 10%-off, 7-day-expiry, single-use coupon code generated per subscriber, tested with a fake signup ("George") through to a completed $900 order. [996959f153ce]
- **Abandoned-cart example**: production window stated as 1 hour, shortened to 1 minute only for the live demo, with the resulting email showing the actual abandoned product back to the shopper. [02c225352111]
- **Revenue attribution example**: after the demo store's automations ran, the OmniSend dashboard showed total store revenue of $1,991, with $900 of that attributed to OmniSend-driven automations and campaigns — a single small demo sample, not a benchmark for expected email-attributed revenue share. [f836216a37bb]
- **Affiliate earnings aside**: the presenter states he has made "$411,000" through affiliate marketing on his own YouTube channel; this is a personal, unverified claim used to justify recommending affiliate marketing as a follow-up topic, not a result tied to the WooCommerce store built in this tutorial. [6303415d3bb8]

## 8. Mistakes the source warns about

1. Leaving a fresh install uncleaned (extra plugins, demo pages, more than one theme) before building on top of it. [16eefae8f3dd]
2. Using a generic site title ("my website," "welcome to my site") instead of one matching buyer search intent. [22fe54d9d081]
3. Assigning the wrong WooCommerce product type to an item (e.g. a physical product marked Downloadable), which breaks shipping and tax calculation. [8c5a95292bdc]
4. Running a sale price with no end date, so the discount never automatically reverts. [b5dc14ff91f1]
5. Allowing silent back-orders without a fast, reliable restocking process, which creates unhappy customers. [b5dc14ff91f1]
6. Leaving overlapping or gapped shipping brackets, which can leave some cart values with no available shipping method at checkout. [6d28f39a903a] [cae87027d082]
7. Mixing shop-inclusive and checkout-exclusive tax price display, which produces a confusing mismatch between the price a shopper first sees and what they pay. [120d8c76c9ef]
8. Manually approximating multiple states' tax with one blanket rate instead of a per-state row. [291aa05299b3]
9. Treating AI-drafted legal-page content as final legal advice instead of a first draft. [4a64696a8718]
10. Editing a theme's core WooCommerce email PHP template directly in the parent theme, which a future theme update can silently overwrite (source explicitly recommends a child theme instead). [153e99ddf6bc]
11. Leaving Test Mode on (or off) unintentionally when a payment gateway should be in the opposite state. [6a3060c2e498]
12. Forgetting to disable "coming soon" mode before sending real traffic. [35896aa4b3ce]
13. Not exposing the free-shipping threshold to customers, missing the incentive effect of "spend $X more for free shipping." [6d28f39a903a]
14. Re-setting a per-recipient unique discount code's expiry on every individual email in a workflow instead of once at the workflow level (it recalculates automatically per recipient). [996959f153ce]
15. Leaving an abandoned-cart trigger at a demo-speed window (e.g. 1 minute) in a live, real-world workflow. [02c225352111]
16. Declaring an A/B test winner after too short a run (source's example: 2 days) or too small a sample. [6d3a34466c86]
17. Letting both a platform's branded order-confirmation email and WooCommerce's own default confirmation fire without deciding which one the customer should actually see, risking a confusing duplicate. [bccbebbbfe5d]
18. Hardcoding a price into a manually edited content block, then letting it drift out of sync when the real product price changes. [ba8d266e5ef9]
19. Only checking the desktop view and skipping tablet/mobile preview before publishing header, menu, or off-canvas menu changes. [5e220039b763]
20. Treating platform-attributed email revenue as an exact, guaranteed figure rather than a directional signal. [f836216a37bb]

## 9. Caveats, conflicts and what is missing

- **Heavy affiliate-monetization overlap.** The presenter states outright that he earns commissions on Hostinger, Blocksy Pro, and Elementor Pro, and demonstrates OmniSend and a third-party tax-lookup service ("TaxJar") in ways that plausibly carry his own affiliate links too, though he does not say so for those two. Treat every recommended paid tool and every price quoted as commercially motivated, not neutral, and re-check pricing and terms independently. [affiliate recommendation] [web check]
- **No dropshipping or print-on-demand automation is covered anywhere in this source.** The only "you don't hold the product" path shown is the External/Affiliate product type, and that is affiliate referral (checkout happens entirely on the partner's site, you never touch the order, payment, or fulfillment), not dropshipping (where you would take the order and payment yourself and have a third party ship on your behalf). There is no AliExpress/Oberlo-style plugin, no supplier order-routing, and no print-on-demand integration mentioned at all. An agent looking for dropshipping/POD automation should treat this source as silent on that topic, not as evidence it isn't needed.
- **All setup uses manual fulfillment for physical goods.** The only automation for physical products is order-status emails; actually shipping the item is explicitly left as the one manual human step in the whole flow. [21c0848f9464]
- **Scope bleeds into neighbor folders.** A large share of this source (theme colors, fonts, logo, menu styling, homepage block editing, mobile responsiveness) is theme/branding work that this library's own folder map assigns to 04-BRD, not 05-SET; the email opt-in, welcome, abandoned-cart, segmentation, and A/B-testing content belongs to 14-EML; and the closing SEO/affiliate-marketing recommendation belongs to 15-SEO/13-ORG. This mini playbook keeps that material because the presenter interleaves it into one continuous build, but a folder-level (Pass 2) playbook should decide where each piece actually lives so it isn't duplicated.
- **All dollar amounts, percentages, and thresholds are demo values, not benchmarks.** Every shipping bracket, tax rate, discount percentage, free-shipping threshold, and workflow delay shown is something the presenter typed on camera to illustrate the mechanism. None are presented as, or should be treated as, recommended settings for a real store.
- **Tax content is mechanism only, not tax advice.** The source shows how to enter rates and classes in WooCommerce; it does not establish nexus, does not give current real rates, and explicitly is not a substitute for a tax professional. [64c13e521d9a] [291aa05299b3]
- **UI paths will drift.** WordPress, WooCommerce, Hostinger, Stripe, PayPal, and OmniSend all change their admin screens over time; nearly every click path in Section 3 should be re-verified against the current interface before an agent follows it literally.
- **Transcript garbles a few plugin/tool names.** The shipping plugin name and vendor, the prior email tool the presenter switched from ("Confluent"), and the final recommended SEO/rank-tracking plugin name are all unclear or likely mis-transcribed; do not assert a specific product name for these without a web check.
- **No controlled comparison anywhere.** Every claim of what "works better" (e.g. narrow product-page width, 1120 px container, specific menu spacing, specific email trigger timing) is presented as the presenter's personal preference or convention, not as a tested result against an alternative.
- **Conflicts with common ecommerce advice**: none found that contradict standard practice; the source's approach (test-mode-first payments, tax nexus caveat, legal-page disclaimer, product-type discipline, shipping-bracket testing, single-use discount codes, gradual A/B test patience) is broadly consistent with common WooCommerce/ecommerce guidance elsewhere in this library. The main risk is not bad advice but staleness: hosting/plugin/pricing specifics will be out of date by the time this is used, and every UI path needs a live check.

## 10. Card index

- `16eefae8f3dd2f05d73eb0d6` Clean a Fresh WordPress/WooCommerce Install
- `8c5a95292bdc4ce09575e115` Pick the Right WooCommerce Product Type for Each Item
- `6a3060c2e498268447474f82` Connect Stripe and PayPal with Test Mode First
- `6d28f39a903a0079e1c6efa5` Set Up Flexible Table-Rate Shipping by Order Value
- `64c13e521d9aceea6d8c2589` Configure Standard, Reduced and Zero Tax Rates
- `291aa05299b310b2ee926f8d` Manually Configure US State Tax Rates in WooCommerce
- `4a64696a871835d9a4f609ce` Create Legal Pages and Place Them in a Footer Menu
- `359dabdafbc0f3a53d618b20` Set Up Free Hosting, Domain and WordPress for a WooCommerce Store
- `f0ee1de989fefb5e6a0f8bd6` Clean a Fresh WordPress Install Before Building the Store
- `22fe54d9d0816ff0fb8b0273` Write a Site Title That Matches What Buyers Search
- `fc3e397bfa083bfeb674bc7c` Install a Free Store Theme and Import a Starter Site
- `35896aa4b3cec7005bc233bf` Install WooCommerce Manually and Complete the Setup Wizard
- `6429dec45a847409b07c32df` Apply Global Brand Colors and a Logo Through the Customizer
- `ed8a244d941cd4740fb015b1` Shape the Header and Main Menu for Store Navigation
- `2228f1a54227ecde4705ff92` Standardise Layout Widths for Store and Product Pages
- `b5dc14ff91f1a92f2c8a7707` Create a Simple Product with Price, Sale Price, Stock and Categories
- `51f236113f57a26fc8758473` Build Variable Products with Attributes, Swatches and Generated Variations
- `8c4b61afe68aac3fdd48a7bc` Create a Downloadable Digital Product with Unlimited Delivery
- `2b411bc7b12e0d6ddb153cf6` List an Affiliate/External Product Without Shipping or Inventory
- `04228274dbbb2839f01e240e` Configure Currency and Store Locale in WooCommerce
- `f0f548d0227a073cb2c123f4` Use the Contrast Trick to Fix Mismatched Block Backgrounds
- `a16dd21fbfc90bf8978d92b3` Set Up Manual US State Tax Rates with Inclusive/Exclusive Display
- `cb975a996a4d4989c8d5b6ad` Set Shipping Cost Brackets and a Free-Shipping Threshold in WooCommerce
- `a33f88e1cb66df7c3e1c20f1` Create WooCommerce Affiliate Products with External/Affiliate Product Type
- `dc9a530117706a528ae01263` Add WooCommerce Upsells (Product Page) vs Cross-Sells (Cart)
- `955efb44177f2412cce4e10f` Customize Shop Look with Fonts, Spacing and Archive Layout
- `cae87027d08212d1be0245a9` Sell to Specific Countries and Set Flexible Table-Rate Shipping by Price Tiers
- `120d8c76c9efd89d773ddd99` Configure Tax Rates by Country, State and Product Class
- `4ca98aa0803179300b1acbb0` Generate Legal Pages Content and Add Them to the Footer Menu
- `5ef2e7c0343a6ccdb3823f9b` Enable Card, PayPal and Wallet Payments (Stripe + PayPal) and Test the Flow
- `21c0848f9464b0f87c8f9734` Handle Incoming Orders and Manage WooCommerce Order Statuses
- `153e99ddf6bcb8f6d5246d28` Brand Transactional Order Emails (Colors, Logo, Copy)
- `349933913a28683f133a4c0c` Connect OmniSend to WooCommerce and Brand the Account
- `05381758c27738a20f12373e` Build a Discount Opt-In Pop-Up to Grow the Email List
- `996959f153ce88d543f7f0c4` Set Up a Welcome Automation with a Unique Per-Person Discount Code
- `ec7dfdb364bb2f5fc3bf6f7c` Welcome Email Series with Unique Per-Subscriber Coupon Codes
- `6d3a34466c8608794dc8eaca` Split Testing Email Subject Lines and Content to Lift Revenue
- `02c225352111465f7a5a410b` Abandoned Cart Email Triggered by Cart Inactivity
- `0b1a8b07620f37efa6469eec` Behavioral and Value-Based Subscriber Segments Feeding Targeted Automations
- `bccbebbbfe5d58aa1fc55635` Custom Branded Order Confirmation Email Replacing the Default
- `f836216a37bb843c5f2b8b40` Revenue Attribution: Separating Platform-Driven Sales from Total Store Revenue
- `a0598dd568d92cd2ba952649` Swap Shared Discount Codes for Unique, Single-Use, Time-Limited Codes
- `ba8d266e5ef955ec253ec398` Editing Homepage Content, Product Blocks and Prices in the Site Editor
- `5e220039b763f35826f77dba` Making the Header, Menu and Off-Canvas Mobile View Responsive
- `50ffde2a6ccb535180be1e48` Optional Channels: Texts and Push Notifications Alongside Email
- `b3e79539406dce7531266a77` Using Tags to Conditionally Gate Automation Emails
- `6303415d3bb8a2f424ff65aa` Prioritizing Your Next Store Improvements: SEO and Email First
