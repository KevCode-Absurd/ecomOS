# WooCommerce Tutorial for Beginners 2026.docx

source_id: 1N7_C41dloQEP_i1ovlcx9YLjlibrEIwZ  |  folder: /05-SET-store-setup  |  cards: 34  |  words: 17,620  |  type: video tutorial transcript (YouTube course)
credibility: Presenter is "Daryl Wilson," a YouTube creator walking through a live build. He sells nothing of his own in this transcript except an affiliate link and coupon code for Hostinger hosting in the video description (see section 9). His evidence is a single screen-recorded demo store, not client data or a study. He repeatedly flags his own opinions as opinions ("I definitely recommend," "I hate to say this," "I'm a big fan of Poppins") rather than presenting them as universal rules. No stats, benchmarks or A/B results are cited anywhere in the source.
date signals: Filename says 2026. Presenter says "during the creation of this video, Elementor recently launched their Atomic Elements" and recommends deactivating them because they are new and "not really website ready yet" — this dates the recording close to Elementor's Atomic Elements launch. All WordPress, WooCommerce, Elementor, Blocksy, Hostinger, Stripe and PayPal click paths are tagged `[verify UI]` throughout since these products change their admin UI often.

## 1. What this source is for

A single, ordered walkthrough for taking a WooCommerce store from nothing (no domain) to a store that can complete a real payment: buy hosting and a domain, install WordPress, install a theme and starter site, learn the page builder, build products (simple and variable), configure store settings, taxes, shipping, and payment gateways, and run one end-to-end test order before going live. It is a beginner's first-build checklist, not a conversion or growth strategy document.

## 2. Principles

1. Build order matters: domain/hosting and WordPress first, because everything else (theme, products, payments, shipping, tax) attaches to that foundation. Condition: applies to a from-scratch build. Evidence: the source's own sequencing and its explicit checklist card. [b6ce2533321d]
2. Set the store address before configuring tax or shipping, because address is what tax and shipping calculations key off of. Condition: any store selling in jurisdictions with sales tax. Evidence: source states this directly and repeats it as a caveat. [0e315f3cac6e] [810ad7d0f208]
3. Configure payment gateways in Test mode and place a full test order before switching to Live. Condition: before accepting real payments. Evidence: source's own worked demo runs exactly this sequence, and calls it out as a checklist item, not just a step. [e2b93597ab6b] [e56e3a1335af]
4. A product variation without a price is not purchasable. Condition: variable products only. Evidence: stated as a direct warning after the source is caught by it in its own demo ("You must have a price. If you do not have a price, this product will not be able to be added to the cart"). [8e91f90d5c53] [bb9a3685b87f] [4c504a8098d0]
5. Distinguish Upsell (shown on the current product page) from Cross-sell (offered at cart/checkout) and place products deliberately in each slot rather than treating them as interchangeable. Condition: any store using WooCommerce's built-in upsell/cross-sell fields. Evidence: source demonstrates both with a worked example (t-shirt + cap) but gives no measured lift — treat as mechanism, not proven result. [a086335acf29]
6. Match tax "Calculate tax based on" to whether your state is origin-based or destination-based, not to a default setting. Condition: US-based sellers. Evidence: source names specific example states and points to taxjar.com as the reference; explicitly says this is an example list, not authoritative. [810ad7d0f208] [web check: current origin-based state list and rates]
7. Use "Per class" (not "Per order") shipping-class calculation when you have heavy/oversized items mixed with normal items, because "Per order" only charges the single most expensive class once and undercharges a mixed cart. Condition: any catalog with a shipping class assigned to some products. Evidence: source states the mechanism directly, no case data. [da4f0f4ea515] [32e02e8dd4c4]
8. Delete or deactivate host-installed default plugins before importing a theme starter site, because leftover plugins can conflict with the demo import. Condition: fresh WordPress install from a host's one-click installer. Evidence: source's stated reason, not measured. [7eaa358a211d] [f94cf50f4191]
9. Treat the product's "short description" as the most important text on the page because it is what the shopper reads first, and reserve the long description for spec-style detail (origin, technical details). Condition: any WooCommerce simple or variable product. Evidence: source's stated claim; in the source's own demo the short description was filled with copy-pasted long-description text, so the demo does not actually model good short-description copy — treat the principle, not the demo text, as the takeaway. [7b57303f41ec]
10. Do not redirect to the cart page on add-to-cart when the store has multiple products, because it interrupts browsing. Condition: multi-product catalogs; source allows a single-product store may reasonably differ. Evidence: source's own practitioner preference, not tested. [e05ffae1f1e7]
11. Set default customer location to "Shop country" rather than "Geolocate," because many customers use VPNs and geolocation becomes unreliable. Condition: general storefront settings. Evidence: source's stated reasoning, not measured; flagged in the source itself as worth testing against your own buyer mix. [0e315f3cac6e]

## 3. Procedures

### A. Domain, hosting and WordPress install
1. Buy a domain and hosting plan. The source used Hostinger via an affiliate link with coupon code "daryl10" for an extra 10% off. `[web check: current pricing, plans and any affiliate terms]` — see section 9, this is an affiliate promotion.
2. Choose a plan: source recommends the "Business" plan (up to 50 hosted websites, NVMe storage) over "Premium" (up to 3 websites, SSD only), with "Cloud Startup" as a later upgrade path. `[verify UI]` `[web check: plan names/limits change]`
3. Choose a term: longer terms (source example: 48 months) give the biggest discount (source's example: about $200 for 4 years); a 12-month plan (source's example: about $50/year) still qualifies for a free domain and suits beginners unsure they'll continue. `[web check: current pricing]`
4. Create the hosting account (email + password), enter billing address, submit payment (card, PayPal or Google Pay supported per source).
5. Answer the host's onboarding questions (who the site is for, create website, WordPress login credentials — write these down), enter the free domain name, check availability, enter owner details, select target-audience country/region, then let the host auto-install WordPress. `[verify UI: host onboarding flow changes often]`
6. Verify both the hosting account email and the domain email (two separate verification emails). Source: failing to verify within 30 days gets the account refunded and closed. `[web check: current Hostinger policy]`
7. Log into the live WordPress site either via `yourdomain.com/wp-admin` with WordPress credentials, or through the host's control panel (Hostinger's "hPanel" > Websites > "WP admin," no credentials needed). `[verify UI]`

### B. Initial WordPress cleanup
1. Plugins: deactivate and delete all host-pre-installed plugins except the caching plugin (source kept LiteSpeed Cache) — reinstall others later if needed. Reason: they can conflict with demo/starter-site imports. `[verify UI]` [f94cf50f4191] [7eaa358a211d]
2. Users > Profile: set a color scheme (source picked "midnight"), confirm/change contact email, set a new password if needed, scroll down and click "Update profile." `[verify UI]`
3. Settings > Discussion: uncheck all comment-allow boxes and all "email me whenever" boxes to block comment spam on a non-blog storefront. Save changes. `[verify UI]`

### C. Theme and starter site (Blocksy + Elementor)
1. Appearance > Themes > Add Theme, search for the theme (source's audio transcribes it as "Bloxy"; the card set corrects this to "Blocksy," a real WordPress theme name — verify which is intended when reproducing this step). Install, then Activate. `[verify UI]`
2. Install and activate the theme's companion plugin ("Blocksy Companion" per the card set) when prompted; this unlocks the Starter Sites importer and extra theme options. [caaa3a73071e]
3. In the theme dashboard, open Starter Sites. Under "All plans," filter to "Free." Set builder = Elementor.
4. Pick a template (source's worked example: "Garter Robe") and click Import.
5. Choose page builder = Elementor when prompted (source is explicit: do not use the native Gutenberg builder here — this is presenter opinion, not a rule to force on an existing builder stack).
6. Keep the import checkboxes selected: theme options, widgets, content, and confirm it's a clean install.
7. Keep the plugin checklist selected on the next screen (typically: the page builder, a contact-form plugin, and WooCommerce). Click Install and wait about a minute.
8. Click "View site" to confirm the import: expect a hero landing section, trust badges (free delivery, 30-day returns, secure payment), dummy products, category blocks (source's demo: jackets/sweaters/accessories), a popular-products section, and a shop page with a filterable sidebar. All of this is demo content to be replaced before launch. [7eaa358a211d]
9. Disable Elementor's Atomic Editor for a beginner build: Elementor > Settings > Atomic Editor tab > Deactivate > confirm "I've understood" > Deactivate. Source frames this as developer-only and not beginner friendly at time of recording. `[verify UI]`

### D. Elementor basics (crash course as given by the source)
1. Create a new page (+ New > Page), give it a title, Publish, then "Edit with Elementor."
2. In Page Settings, set Page layout = "Elementor Full" so only the builder controls the page (removes the theme's page-title bar).
3. If the sticky header or transparent header collides with the builder: open the theme Customizer > Header > Global Header, toggle off "Sticky functionality" and/or "Transparent" as needed, then Publish and refresh the Elementor editor. Re-enable sticky header after the build if you want persistent nav for shoppers — the source disabled it purely for editing convenience, not as a storefront recommendation. `[verify UI]` [d6530675b1ba]
4. Add a row: click "+", choose Flexbox (source recommends flexbox over Grid as easier and more common), pick a column layout (e.g., two columns).
5. Add elements by drag-and-drop from the left panel (Basic elements: heading, image, text editor, button, social icons, etc.). Every element has three tabs: Content (the text/media/link), Style (typography, color, size), Advanced (padding/margins, motion/entrance effects).
6. To place items side by side (e.g., two buttons), wrap them in their own container first — plain elements stack vertically with no control otherwise. On the container: set Direction = Horizontal (or Vertical, or Reversed) and use Justify content (center / start / end / space-between / space-around / space-evenly) to arrange children. Adjust per-column Width when one column should be narrower (e.g., image narrower than text). `[verify UI]` [ee48af6266ec]
7. For a full-height hero, set Minimum height = 100 (unit VH) on the section, not the inner container — the Elementor interface itself labels this as the way to get a full-height container.
8. Right-click any element/container to Duplicate or Delete. To keep styling consistent, style one element fully, right-click > Copy, then right-click matching elements > Paste style (works between same element type).
9. Button links: type the destination page's name into the link field; Elementor auto-resolves the URL (source example: typing "products" links to the shop page).
10. Background image editing: right-click the background/container > Edit container > Style > Image: turn off any custom position (select Default), set Display size = Cover, then pick a focal position (e.g., center-center) so subjects aren't cropped. Set text color to white (or a contrasting color) if placed over a dark image.
11. For a fast page draft, try Elementor AI: click Elementor AI, click Generate, enter a prompt (source example: "three column row"). Treat the output as a rough draft only — the source's own AI attempt asked for 3 columns and produced 4, requiring manual cleanup and replacement of placeholder images/names. `[733d55d477a7]`

### E. Mobile/tablet responsive pass
1. In the Elementor top bar, switch device preview between Desktop, Tablet Portrait, and Mobile Portrait. Any setting changed while a device view is active is scoped only to that device (shown by a small screen icon next to the control).
2. Re-apply flexbox settings per device as needed (e.g., set Justify content = center for tablet/mobile where desktop used left/space-between).
3. Swap background images per device: right-click background > Edit container > Style > Image > select the device tab (e.g., Portrait) > choose a different image for that breakpoint.
4. Add a background overlay (darker color, increased opacity) scoped to the device where light imagery makes overlaid text unreadable.
5. Resize typography per device under the Style tab's Typography control when text reads too small/large on a given breakpoint.
6. Hide elements that don't fit small screens: open the element's Advanced tab > Responsive > toggle hide on Tablet and/or Mobile. This control exists at the element, column, and section level. Caution: hiding removes that content entirely for that device's shoppers — do not hide a required CTA or price. [fc132ec61c87] [b252b45ac9b9]
7. Note: WooCommerce's own product-grid displays are automatically responsive per the source; hand-built sections and the footer still need a manual pass.
8. Preview each breakpoint, then Publish.

### F. Pages and navigation
1. Pages > Add Page (or +New > Page), title it, Publish, then design with Elementor (or Elementor AI for a fast draft).
2. Appearance > Menus: under Pages, click "View all," select the new page, click "Add to menu."
3. Drag the item into position; drop it under a parent item to create a hover dropdown.
4. For off-site links (source example: a Facebook group URL), use the "Custom Links" box: paste the URL, add a label, click "Add to menu," position it, then Save menu.
5. Visit the live site to confirm the dropdown opens on hover and the custom link resolves correctly. `[verify UI]` [c27224e22301]

### G. Simple product creation
1. Products > Add New. Enter the product title (source example: "black t-shirt").
2. Fill the long description (spec/technical content shown below the product) and separately the short description field (the source calls this the most important text, shown first to the shopper — note the source's own demo copy-pasted the same content into both fields, which does not model good practice for the short description). [e41eaf5bbcdc] [7b57303f41ec]
3. Product data: choose Simple product. Optionally mark Virtual and/or Downloadable and attach files.
4. Enter Regular price (source example: $100) and, for a sale, the Sale price (source example: $50) with a Sale schedule date range (source example: the 6th through the 31st).
5. Inventory: enter SKU if used; enable stock management; set stock Quantity (source example: 10); choose backorder behavior (source example: allow, but notify the customer); set a Low stock threshold (source example: 3) to get warned before selling out.
6. Shipping: enter weight and dimensions (source example values: weight 1, length 20, width 28, height 24 — units are set separately under WooCommerce > Settings > Products, `[needs brand data: your actual product weights/dimensions and unit system]`). Missing these breaks weight- or class-based shipping calculation.
7. Upsells / Cross-sells: add an Upsell product to show on this same product page (source example: a cap alongside the shirt) and a Cross-sell to offer at cart/checkout.
8. Set the featured Product image and Gallery images, assign a Product category (create new if needed, source example: "Daryl shirts"), and optionally tags/brand.
9. Publish, then View product to confirm price/sale badge, stock count, images, description, additional-info tab, and the "You may also like" upsell block all render. [7b57303f41ec]

### H. Variable product creation
1. Products > Add New (or the +New > Product shortcut). Set Product data = Variable product.
2. Attributes tab: add an attribute (source example: "Size"), enter each value; source describes entering multiple values in one field separated by the pipe character (typed via Shift + the key above Enter on a US keyboard) — e.g. `10 | 11 | 12`. Tick "Use for variations" (values won't become selectable options without this). Click Save attributes.
3. Add a second attribute if needed (source example: "Color" with values gray, red, beige). Save attributes.
4. Variations tab: click "Generate variations" (source also says "Generate all variations") to create one row per combination (source example: Size 10 Gray, Size 10 Red, Size 10 Beige, Size 11 Gray, etc.).
5. Edit each variation individually: assign its image, set its own Price (source examples: gray $50, red $50, beige $80 — a variation with no price cannot be added to the cart, this is stated as a hard rule), and optionally its weight/SKU/stock.
6. Set the overall product's short description and main Product image, then set Default form values (source example: default size 11, default color gray) so the default selection matches the shown default image.
7. Publish. Confirm the storefront shows the price range across variations (source example: "$50–$80"), and that selecting a different size/color combination swaps both image and price. [8e91f90d5c53] [bb9a3685b87f] [4c504a8098d0]

### I. Product categories cleanup
1. Products > Categories: delete imported categories you don't need.
2. The default category cannot be deleted; rename/repurpose it into a real category (source example: renamed to "Daryl's Gear") rather than leaving it as unused "Uncategorized." [61bbf15291749004213a6531 → 61bbf1529174]

### J. Store-wide General settings
1. WooCommerce > Settings > General: enter the store address first (drives tax/shipping).
2. Selling locations: choose "Sell to specific countries" and pick only the countries you serve (source example: United States and Canada) — source calls this the most commonly used setting in its experience.
3. Shipping location: set to match the countries you sell to, not "ship to all countries."
4. Default customer location: choose "Shop country" rather than "Geolocate" (VPN users make geolocation unreliable, per source).
5. Skip address autocomplete unless you're willing to add the third-party plugin it requires.
6. Enable taxes and enable coupons; check the remaining default boxes; set store Currency (source example: USD). Save changes. [0e315f3cac6e]

### K. Products settings
1. WooCommerce > Settings > Products: review "Add to cart behavior" — source advises against redirecting to the cart page when you sell multiple products, since it interrupts browsing.
2. Set Measurements (pounds/ounces for US, kilograms/grams for Europe per source) and Dimension units (inches, cm, etc. — match your market).
3. Reviews: decide whether to enable reviews at all, and whether to require a verified purchase; enable star ratings independently if wanted. Source's own store leaves verified-purchase-only unchecked — a policy choice, not a rule.
4. Save. Optionally visit Inventory settings (stock management) and Downloadable products settings if selling digital goods. [e05ffae1f1e7] [be71d70a5e08]

### L. Tax setup (manual rates)
1. WooCommerce > Settings > Tax: leave "Prices entered with tax" unchecked (source says this is what most stores do — prices display without tax).
2. Set "Calculate tax based on": use Shop base address if your state is origin-based (source examples: Arizona, California, Ohio, Pennsylvania, Tennessee); use Customer shipping address for other (destination-based) states. Source points to taxjar.com as its reference and calls its own list an example, not authoritative. `[web check: current origin/destination state list]`
3. Shipping tax class: leave based on cart items unless you charge one flat rate everywhere, in which case select Standard.
4. Set rounding preference and rename reduced/zero rate labels as needed. Leave "Display prices in the shop excluding tax" on (source: most stores do this). Save.
5. Standard rates: click Insert row. Enter country code (source example: US), state code (source example: CA), postcode (source example: 91311), rate (source example: 7.25 for California), a tax name (source example: "California"), priority (only matters with multiple competing rates), whether the rate compounds, and whether shipping is taxable in that state (source cites taxjar.com listing states including Arkansas, Kentucky, Minnesota, Mississippi as taxing shipping, and estimates "about half" of US states do). `[web check: current state tax rates and shipping-taxability list]` [810ad7d0f208]
6. Reduced rates: Insert row for a special category (source example: 0% named "Digital" for digital goods in California). Then on the affected product: Product data > General > Tax status = Taxable, Tax class = your reduced class (e.g. "Reduced rate"). Update. [e551ef1a9cb2]

### M. Tax setup (automated — WooCommerce Tax / TaxJar)
1. Plugins > Add new, search "WooCommerce Tax," install and activate (published by WooCommerce/Automattic, powered by TaxJar per source).
2. Click Connect; create/authorize a free WordPress.com account when prompted (uses the WordPress.com API).
3. Return to WooCommerce > Settings > Tax, enable automated taxes, Save. Rates are then pulled from the connected tax service. `[web check: current plugin name, connection flow, and whether it remains free]` [cdf8caa5f07e]

### N. Shipping zones and methods
1. WooCommerce > Shipping > Add shipping zone. Name it (source example: "United States").
2. Zone regions: leave "Everywhere" if the zone's countries already match where you sell and ship everywhere within them; otherwise restrict to specific states/regions.
3. Add Shipping method > Free shipping: set the requirement — no requirement, valid coupon, minimum order amount, or a combination. Source example: minimum order amount of $100. Save.
4. Add Shipping method > Flat rate: set a default rate (source example: $5). Save.
5. Add Shipping method > Local pickup: source example fee $0, mark "not taxable." Save. [83e072152c92]

### O. Shipping classes (per-item heavy/oversized pricing)
1. WooCommerce > Shipping > Shipping classes > Add ("Heavy" / "heavy packages" per source example). Create.
2. Edit the zone's Flat rate method: keep the default rate (source example: $5) and add a per-class cost row for the Heavy class (source example: $10).
3. Set Calculation type = "Per class" (charges the class rate per matching item in the cart) rather than "Per order" (only applies the single most expensive class once, undercharging a mixed cart). Save.
4. On each relevant product: Product data > Shipping tab > Shipping class = Heavy. Update.
5. Test with a cart containing a normal item, a heavy item, and both together to confirm rates combine as intended. [da4f0f4ea515] [32e02e8dd4c4]

### P. Payment gateways
1. Plugins > Add new: search and install "Payment Plugins for Stripe WooCommerce" (source explicitly avoids the official Stripe WooCommerce plugin, saying it "malfunctions a lot" in the presenter's own experience; describes the third-party plugin as an official Stripe partner with high ratings — this is the source's opinion, re-evaluate current plugin quality before choosing). Activate.
2. Also install and activate "Payment Plugins for PayPal WooCommerce" when prompted. Activate.
3. Stripe: create a free Stripe.com account (source: no setup cost, no credit check, no monthly fee, only a per-transaction fee, standard across the industry). `[web check: current Stripe fees/terms]` In the plugin settings, click "Connect Stripe account" > log in > select the business account > Connect. Leave in Test mode; Save changes.
4. PayPal: create a PayPal Business account — source states a Personal account will not sync with the site. `[web check: current PayPal business account requirements/fees]` In the plugin settings, click "Connect to PayPal" > log in > connect. Save. [e2b93597ab6b] [840926e7dab9]

### Q. End-to-end test order
1. Add a product to cart, view cart: confirm the flat rate (source example: $5) and Local pickup both appear as options.
2. Increase quantity to cross the free-shipping threshold (source example: $100), click Update; confirm free shipping becomes selectable. Proceed to checkout.
3. Fill billing details; confirm the country dropdown lists only your configured selling countries (source example: US and Canada). Uncheck "ship to a different address" unless testing a separate shipping address.
4. Confirm the correct tax line applies per your origin/destination configuration.
5. With Stripe in Test mode, enter the test card number as digits "4242" repeated across the card field, any future expiry date and any CVC. Place order.
6. Confirm the order appears under WooCommerce > Orders with correct totals, line items, billing and shipping address, and that it also shows on the customer's My Account page. [e56e3a1335af]

### R. Order fulfillment and refunds
1. WooCommerce > Orders: open an order to see status, details, billing/shipping address.
2. Change status to Completed and click Update — this notifies the customer the order has shipped. Default status after purchase is "Processing" (auto-fulfillment is described as configurable but not detailed in this source).
3. To refund: scroll to the bottom of the order screen, click Refund, enter the amount, confirm. Test orders show $0 refunded since no real funds moved. [694b2885835d]
4. Point customers to the auto-created My Account page (view past orders/totals, update address, update payment method, log in/out). Optional: add a third-party social-login plugin.

### S. Email deliverability
1. Recognize that on a fresh WooCommerce install, order emails to customers often fail to send by default — fix this before launch, not after complaints.
2. Configure SMTP settings using a plugin (source refers to "a free plugin" and a separate video walkthrough but does not name the plugin in this source — source is thin on this specific how). `[needs further source: SMTP plugin name and setup steps]`
3. WooCommerce > Settings > Emails: review recipients — new-order notifications go to the store owner; processing/on-hold and similar statuses go to customers. Leave default subject lines/headings (source recommendation for simplicity).
4. For branded email templates, source recommends a free drag-and-drop email-builder plugin since the built-in email body isn't directly editable — again unnamed in this source. `[needs further source: which plugin]` [9a06652f2c2b]

## 4. Rules, thresholds and numbers

| Rule | Number / threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Free shipping minimum | $100 order value (example) | Illustrative only, not a benchmark — set from your own margins/AOV | Worked demo value | 32e02e8dd4c4 |
| Flat rate shipping | $5 default (example) | Illustrative | Worked demo value | 83e072152c92 |
| Heavy shipping class surcharge | $10 per item (example), Per class calculation | Applies to products tagged with a shipping class | Worked demo value | da4f0f4ea515 |
| Low stock threshold | 3 units (example) | Any tracked-inventory simple product | Worked demo value | 7b57303f41ec |
| Sample sale price | $100 → $50, scheduled 6th–31st (example) | Illustrative sale-schedule mechanic | Worked demo value | 7b57303f41ec |
| Variable product price spread | $50–$80 across variations (example) | Different colors/sizes can carry different prices | Worked demo value | 4c504a8098d0 |
| California sales tax rate | 7.25% (example) | California only, as of recording | Cited to taxjar.com | 810ad7d0f208 `[web check]` |
| Origin-based state examples | Arizona, California, Ohio, Pennsylvania, Tennessee | Charge tax at shop base address | Cited to taxjar.com, source calls it illustrative | 810ad7d0f208 `[web check]` |
| States taxing shipping (examples) | Arkansas, Kentucky, Minnesota, Mississippi; "about half" of US states overall | Determines whether "tax on shipping" box is checked | Cited to taxjar.com | 810ad7d0f208 `[web check]` |
| Digital-goods reduced tax rate | 0% (California example) | Assign via a Reduced rate tax class on the product | Worked demo value | e551ef1a9cb2 |
| Email verification window | 30 days | Hosting-account specific (source: Hostinger); miss it and account is refunded/closed | Stated host policy | procedure A `[web check]` |
| WooCommerce install base | "More than 7 million active installs" | Presented as the reason it's the default plugin choice | Presenter claim | procedure G intro `[web check]` |
| Hosting discount example | ~$200 for a 48-month term; ~$50/year on a 12-month term | Illustrative, Hostinger-specific | Presenter's own purchase | procedure A `[web check]` |
| Test card number | "4242" repeated | Stripe Test mode only | Standard Stripe test card convention, stated by source | e56e3a1335af |

## 5. Diagnostics and checks

- Product not addable to cart → check every variation has a price set; a blank price silently blocks purchase. [8e91f90d5c53]
- Shipping calculating wrong for a product → check weight/dimensions were entered on that product, and check whether a Shipping Class was meant to apply. [e41eaf5bbcdc] [da4f0f4ea515]
- Mixed cart of heavy + normal items undercharging shipping → check Calculation type on the flat-rate method; "Per order" only charges the highest class once, switch to "Per class." [da4f0f4ea515]
- Tax looks wrong at checkout → check the store address is correct, then check whether "Calculate tax based on" matches your state's origin/destination rule. [810ad7d0f208]
- Customers not receiving order emails → check SMTP is configured; source states fresh WooCommerce installs often fail to send by default. [9a06652f2c2b]
- Menu item not showing → confirm the page was added via Appearance > Menus > (Pages > View all > select > Add to menu), not just published. [c27224e22301]
- Elementor editor colliding with the header while building → check whether sticky/transparent header is on in the theme Customizer and disable temporarily. [d6530675b1ba]
- Layout looks broken on tablet/mobile → step through each device preview individually; per-device settings do not inherit automatically, and hidden elements must be checked for anything essential (CTA, price). [b252b45ac9b9]
- PayPal connect not syncing → confirm the PayPal account is a Business account, not Personal. [840926e7dab9]
- Before going Live on payments → run the full test order in section Q and confirm order, tax, shipping and confirmation email all behave correctly.

## 6. Tools, settings and named features

- **Hostinger** — hosting/domain provider used in the demo, promoted via an affiliate link and a "daryl10" discount code. `[web check: current pricing/plans]` Flagged explicitly as an affiliate hosting recommendation — see section 9.
- **Blocksy theme** (transcript audio: "Bloxy") + **Blocksy Companion plugin** — WordPress theme and its companion plugin that unlocks Starter Sites. `[verify UI]`
- **Elementor** page builder, including the **Atomic Editor** (new at recording time, source recommends deactivating for beginners) and **Elementor AI** (source rates its output "not the best," useful only as a rough draft). `[verify UI]`
- **WooCommerce** — core shopping-cart plugin (source states 7M+ active installs). `[web check]`
- **WooCommerce Tax** plugin (by WooCommerce/Automattic, powered by TaxJar) — automated tax rates, requires a free WordPress.com account to connect.
- **Payment Plugins for Stripe WooCommerce** and **Payment Plugins for PayPal WooCommerce** — third-party gateway plugins the source prefers over the official Stripe WooCommerce plugin, which it says "malfunctions a lot" in its own experience.
- **Stripe.com** and **PayPal.com (Business account)** — payment processors; source states both are free to set up with only per-transaction fees. `[web check: current fees]`
- Unnamed **SMTP plugin** and unnamed **drag-and-drop email builder plugin** — referenced but not identified in this source; the source points to a separate video instead. `[needs further source]`
- **taxjar.com** — cited as the reference for origin/destination state rules and shipping-taxability by state. `[web check]`

## 7. Examples and case results

All numbers below are from the source's own single worked demo store, not from real sales data or a controlled test — treat every figure as an example, never as a benchmark.

- Black t-shirt: regular price $100, sale price $50, sale window "6th to 31st," stock 10, low-stock alert at 3, shipping dimensions 1 (weight) / 20 / 28 / 24 (L/W/H, units not specified in-source). [7b57303f41ec]
- Daryl's shoes (variable product): attributes Size (10, 11, 12) and Color (gray, red, beige); variation prices $50 (gray), $50 (red), $80 (beige); default form values size 11 / gray to match the default product image; storefront price range displayed as "$50–$80"; a demo customer added 4 shoes to cart across variations. [4c504a8098d0] [bb9a3685b87f]
- Shipping: United States zone, free shipping over $100, flat rate $5 otherwise, local pickup free; Heavy shipping class costs $10 per item on top, using "Per class" calculation. [83e072152c92] [da4f0f4ea515]
- Tax: California example, standard rate 7.25%, one reduced rate of 0% for a "digital" product category. [810ad7d0f208] [e551ef1a9cb2]
- Test checkout: 3 shirts (crossing the $100 free-shipping threshold), Stripe test card "4242" repeated, order placed and confirmed under WooCommerce > Orders showing a $164 total in the customer's My Account transaction history. [e56e3a1335af] [694b2885835d]
- Elementor AI: prompted for a "three column row," returned four columns — source deleted one section rather than trusting the AI output. [733d55d477a7]

## 8. Mistakes the source warns about

- Leaving a product variation without a price — it silently becomes unpurchasable. [8e91f90d5c53] [bb9a3685b87f]
- Redirecting add-to-cart straight to the cart page on a multi-product store — pulls shoppers out of browsing every time. [e05ffae1f1e7]
- Leaving host-installed default plugins active before importing a theme starter site — can conflict with the demo import. [7eaa358a211d]
- Missing the hosting account's email-verification window (source: 30 days) — account gets refunded and closed. `[web check]`
- Using "Per order" instead of "Per class" for shipping-class calculation on mixed carts — undercharges shipping on carts with multiple heavy items. [da4f0f4ea515]
- Guessing the tax "Calculate tax based on" setting instead of checking whether your state is origin- or destination-based — produces the wrong tax basis. [810ad7d0f208]
- Using a Personal PayPal account for the store integration — it will not sync. [840926e7dab9]
- Assuming a fresh WooCommerce install will send order emails correctly by default — it often does not; SMTP needs configuring before launch. [9a06652f2c2b]
- Shipping an AI-drafted page (Elementor AI) without checking it — the source's own attempt needed manual correction. [733d55d477a7]
- Hiding page elements on mobile/tablet without checking whether that content (a CTA, a price) is actually needed by that audience. [fc132ec61c87] [b252b45ac9b9]
- Not testing every generated product variation before publishing — some can be left without images, prices or correct stock.

## 9. Caveats, conflicts and what is missing

- **Affiliate hosting recommendation, flagged per instructions:** the source promotes Hostinger through an affiliate link and a personal discount code ("daryl10"), and frames the "Business" plan as the clear recommendation. This is a monetized recommendation, not a neutral comparison against other hosts — the source itself is aware other hosting options exist but does not evaluate them. `[web check: current hosting market, pricing and alternatives before recommending Hostinger to a brand]`
- **Guest checkout — ambiguous statement, do not resolve it silently.** The transcript says, verbatim in substance: "This is essentially if you want to enable guest checkout. I think that's a terrible idea, and these default options are standard for most e-commerce stores." Read literally, "that" most naturally refers to the immediately preceding phrase ("enable guest checkout"), meaning the source may be calling *enabling* guest checkout a terrible idea. However, the underlying card in this source's card set (be71d70a5e08) paraphrases it the opposite way — as the source calling *disabling* guest checkout "a terrible idea," which would align with common ecommerce advice that forced account creation increases checkout abandonment. **This mini playbook cannot resolve which the source meant** and flags it as a genuine ambiguity rather than picking a side. Whichever reading is correct, note the conflict against common advice: most ecommerce guidance recommends allowing guest checkout to reduce friction, so if the literal reading (opposing guest checkout) is correct, that is a direct conflict with mainstream CRO advice, and should be treated as this presenter's personal opinion, not adopted as a rule, until re-checked against the source video directly.
- **Theme name discrepancy:** the transcript audio consistently says "Bloxy," while the source's own card set (and the real WordPress theme) call it "Blocksy." Likely a transcription/mishearing artifact. Verify which theme is actually shown on screen before reproducing this step for a brand. `[verify UI]`
- **Official vs third-party Stripe plugin:** source's claim that the official Stripe WooCommerce plugin "malfunctions a lot" is a single presenter's experience, not a documented defect list. Re-evaluate current plugin quality and Stripe's own recommended integration path before choosing a plugin for a real brand.
- **SMTP and email-builder plugins are named nowhere in this source** — the source explicitly defers to "a separate video" it made elsewhere. Treat email deliverability setup as a gap this source does not close; a brand needs a named, verified plugin before this step can be executed as written. [9a06652f2c2b]
- **No case data or measured outcomes anywhere.** Every number (prices, thresholds, stock levels) comes from one demo store built for the recording, not from a live business. Do not treat any of them as benchmarks.
- **Product weight/dimension units are never stated** in the simple-product walkthrough (values of 1/20/28/24 are given with no unit); the unit system is set separately in Products settings (pounds/ounces vs kilograms/grams, inches vs cm) and must be checked against the brand's actual catalog. `[needs brand data: product weights, dimensions and unit system]`
- **UI volatility:** every click path in this source (WordPress, WooCommerce, Elementor, Blocksy, Hostinger's onboarding flow, Stripe/PayPal plugin settings) is explicitly liable to change; the source itself notes Elementor had just shipped a new editor (Atomic Elements) during recording, and that host onboarding screens "change frequently." Every procedure section above is `[verify UI]` before use.
- The source is thin on: auto-fulfillment configuration (mentioned as "an option" but not shown), any SEO setup, any analytics/conversion tracking setup, and any multi-currency or international-tax handling beyond the US origin/destination basics.

## 10. Card index

- b6ce2533321d — WooCommerce Setup Order: From Blank to Sellable Store
- caaa3a73071e — Installing and Importing a Blocksy + Elementor Starter Site
- e41eaf5bbcdc — Creating a Simple Product in WooCommerce
- 8e91f90d5c53 — Creating a Variable Product with Attributes and Generated Variations
- e2b93597ab6b — Connecting Stripe and PayPal via Payment Plugins
- 32e02e8dd4c4 — Shipping Zones, Flat Rate vs Free-Over-Threshold, and Shipping Classes
- 0a6c2884d19a — Automated Sales Tax with WooCommerce Tax
- fc132ec61c87 — Elementor Responsive Controls for Product and Landing Pages
- 9237bdf8aa5b — Pre-Launch Store Configuration Checklist (Topic Map)
- f94cf50f4191 — WooCommerce baseline store configuration order
- 7b57303f41ec — Simple product configuration in WooCommerce
- bb9a3685b87f — Variable product setup for size and color options
- a086335acf29 — Upsell vs cross-sell placement in WooCommerce
- ee48af6266ec — Elementor container and flexbox layout for ecommerce pages
- 7eaa358a211d — Starter-site import and why to remove conflicting plugins
- d6530675b1ba — Header settings that block page building and product imagery
- b252b45ac9b9 — Responsive optimization pass across desktop, tablet and mobile
- 733d55d477a7 — Elementor element editing, copy-paste style and AI page drafts
- c27224e22301 — Creating pages, menus and dropdown navigation for a store
- 792085abd57c — WooCommerce admin surfaces for running the store after launch
- 4c504a8098d0 — Create variable products with size/color attributes and variation images
- 0e315f3cac6e — Configure selling locations, shipping locations and customer location sensibly
- e05ffae1f1e7 — Decide add-to-cart redirect behavior and product review permissions
- 810ad7d0f208 — Set tax calculation basis correctly by origin vs destination state
- e551ef1a9cb2 — Use reduced tax rates for special product classes
- cdf8caa5f07e — Automate tax rates with the WooCommerce Tax plugin
- 83e072152c92 — Build shipping zones with free shipping, flat rate and local pickup
- da4f0f4ea515 — Charge per-product shipping with shipping classes and per-class calculation
- 840926e7dab9 — Connect Stripe and PayPal payment gateways
- e56e3a1335af — Run a test order to verify shipping, tax and checkout end to end
- 694b2885835d — Manage and fulfill orders, issue refunds, and understand the customer My Account page
- 61bbf1529174 — Organize product categories and handle undeletable defaults
- 9a06652f2c2b — Check email deliverability and customize transactional emails
- be71d70a5e08 — Tune coupon and review settings for a workable default configuration
