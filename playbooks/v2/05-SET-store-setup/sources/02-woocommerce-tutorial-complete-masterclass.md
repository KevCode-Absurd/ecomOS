# WooCommerce Tutorial 2026: Complete MasterClass for Beginners

source_id: 1L4m4We7PTUdjH3Mk7VxqSxAc_U4D-yFT | folder: /05-SET-store-setup | cards: 72 | words: 44,012 | type: video transcript (full course)

credibility: Presenter is Tim Nishad, who describes himself as a professional web developer who has "completed so many freelance WordPress projects" for clients; no client names, case studies or measured results are given anywhere in the transcript. He runs (or is affiliated with) a site transcribed inconsistently as "jimfaddigital.com" / "jimfutorial.com" / "Jim Fah Digital" (the transcript never spells it the same way twice, so treat the exact domain as unverified [web check: presenter's actual site domain]). Evidence throughout is a single live demo build (a fictional pet-food store, "Canine Crunch" / "Bark and Bite" products) narrated step by step — this is a walkthrough, not a benchmarked or client-tested result. The course is commercially entangled with multiple affiliate relationships (see Section 9): a Hostinger hosting link with a coupon code, and two paid Elementor template marketplaces. None of the numbers, plan names or discounts should be treated as durable facts.

date signals: Course is titled "2026" and was exported from a doc modified 2026-09-19. Presenter states the Elementor version he used (3.33.6) was already superseded at recording time by 4.0.1, which he calls unstable and instructs viewers to roll back to match him — meaning even the presenter treats his own tooling as time-bound. Hosting and template-marketplace pricing are explicitly flagged by the presenter as changing often ("prices might be slightly different depending on the day you're watching"). Treat all UI paths, plugin names and prices in this file as needing a live check before use.

## 1. What this source is for

Takes an operator from zero to a fully functional (though not yet fully designed) WooCommerce store: buying hosting and a domain, installing WordPress, cleaning up the default install, installing a lightweight theme plus Elementor as the design layer, and then configuring every WooCommerce setting that makes a store actually sell — selling/shipping locations, tax classes and rates, shipping zones and classes, Stripe/PayPal payment gateways, account and checkout behavior, transactional emails, store identity, and the "coming soon to live" launch switch. It also walks through creating all four WooCommerce product types (simple, variable, virtual/downloadable, external/affiliate), coupons, and a full buyer-side and admin-side purchase test. The back half of the course (roughly the second half of the transcript) shifts into detailed Elementor visual design of the homepage, contact page, blog and footer — that design work is out of scope for this folder per the source's own routing note ("Elementor page builder design, CSS injection, and landing page layouts -> 07-LPG") and is only summarized here, not detailed.

## 2. Principles

1. Clean the WordPress install before adding store plugins. Condition: applies immediately after WordPress installs, before any theme or WooCommerce work. Evidence: presenter deactivates then deletes every default plugin and clears default dashboard widgets before doing anything else, framing it as basic hygiene. [95ada3c41602] [b44de1f18767]
2. Set permalinks to "Post name" before creating any pages or products. Condition: general, applies to any WordPress/WooCommerce build. Evidence: presenter calls this "highly, highly" recommended, contrasting it against Plain (random numbers/characters) and Day-and-name (shows a date) structures, for readability and search ranking. [95ada3c41602] [284bc4b17ed7]
3. Use a lightweight theme for structure and a page builder (Elementor) for design, not a heavy pre-built theme. Condition: applies when the operator wants full design control rather than a fast templated look. Evidence: presenter's own stated tradeoff — "themes... has so many limitation... but if you use page builders... you can take control of every inch." [e91f80fe1721]
4. Restrict selling/shipping locations to markets you can actually serve, and disable shipping entirely for pure digital catalogs. Condition: set before adding products, since it changes what tax/shipping options later apply. Evidence: presenter's own settings walkthrough of "Sell to specific countries" and "ship to all countries you sell to," with an explicit carve-out for virtual-only stores. [ca2329868be7]
5. Choose tax-inclusive vs tax-exclusive pricing deliberately, understanding the customer's final price is the same either way — only the display differs. Condition: set once, before entering product prices, since switching later means rechecking every price. Evidence: presenter's worked $100/$5-tax example shown both ways. [f294546e4437]
6. Source real tax rates from a reference (TaxJar cited) rather than guessing, and build per-state rows with priority to resolve overlaps. Condition: applies to any US multi-state (or multi-jurisdiction) store. Evidence: presenter's own worked example where a California-specific row (priority 1, 7.25%) beats a whole-US fallback row (priority 2, 5%) for a California customer. [efa4821ff9f1] [7275017fd366] [8e81d2277f77]
7. Match flat-rate shipping structure to product economics: per-order pricing for small/light repeat-purchase goods, per-item (quantity-based) pricing for bulky or heavy goods. Condition: decided per shipping method, not store-wide. Evidence: presenter's own reasoning — "you cannot charge one single shipping cost for 10 beds," versus pet-food packets where per-order makes sense. [5c049a84968e] [d3912129e9a7]
8. Install dedicated Stripe and PayPal plugins rather than relying on WooCommerce's own defaults, and always run the connection test before trusting a gateway. Condition: applies whenever on-site (not off-site-redirect) card/PayPal payment is wanted. Evidence: presenter names the exact plugins used ("Payment Plugins for Stripe WooCommerce," "Payment Plugins for PayPal WooCommerce") and demonstrates the test-mode connection check before describing the live-mode switch. [b0fd0a5facf8] [02c7c501d001] [780a428b8702]
9. Enable guest checkout as the recommended default, while still offering account creation at checkout. Condition: general ecommerce checkout setting, trades off data capture against completion friction. Evidence: presenter explicitly labels guest checkout "recommended" and checks all three related boxes (guest checkout, login during checkout, account creation during checkout). [fab5bea4ff25]
10. Build attributes globally (Products > Attributes) before building any variable product, never as one-off product-level attributes. Condition: applies whenever more than one product might share an attribute (e.g. weight, size, color). Evidence: presenter states directly that product-level attributes are "only available for this specific product," while global ones are reusable — and walks through creating "Weight" and "Toy" as global attributes before touching the product. [13e3297ba233] [a8a1945fe798] [a065c6dfec57]
11. A store stays in "Coming soon" while it is being built and only switches to "Live" after products, settings and a full purchase test are done. Condition: applies to the WooCommerce Site Visibility toggle specifically. Evidence: presenter frames flipping to Live as the deliberate last step, done "after you done setting up... doing all the e-commerce settings... uploading all the products." [c4521eb76468]
12. Run a full end-to-end purchase test (multiple product types, a coupon, a real payment attempt, and admin order processing) before trusting the setup. Condition: before launch and after any change to payments, tax, shipping or emails. Evidence: presenter performs exactly this test live — adding a simple product, an ebook and a variable-product variation to cart, applying a coupon, placing the order, then switching to the admin view to update order status. [fa39013559f5]
13. Transactional emails are per-event and many need to be manually enabled — a disabled email simply never sends. Condition: whenever store owners expect a specific notification (e.g. cancelled-order) to fire. Evidence: presenter opens each Manage screen individually and toggles Enable on ones he wants active, noting most default template options are otherwise dormant. [6346d90f2e59]
14. Pin a page builder (or any actively-updated plugin) to a known stable version if a just-released major version is reported unstable, and build the whole project on that version. Condition: applies when a tool has recently shipped a new major version. Evidence: presenter's own choice to roll Elementor back from 4.0.1 to 3.33.6 for the entire course. This is a single presenter's judgment call at one point in time, not a durable claim about any specific version — [web check: current Elementor stable version before following this]. [fe4eafe0a577]

## 3. Procedures

### A. Hosting, domain and WordPress install (AFFILIATE — see Section 9)
1. Go to the presenter's affiliate link (transcribed as jimfaddigital.com/besthost) to reach a discounted Hostinger page. [web check: current Hostinger pricing/plans] [affiliate: yes, presenter's own link plus a coupon code]
2. Choose a hosting plan. Options seen: Premium (3 websites) and Business or "Business Plus AI" (up to 50 websites, free domain year 1, free SSL, Hostinger's own "Kodi AI" website builder, 50GB NVMe storage + CDN, daily backups). Presenter recommends Business Plus AI for the extra headroom, but says budget-limited buyers can start on Premium and upgrade later.
3. Choose a billing term: 48 months, 24 months, 12 months or 1 month. Presenter says never pick 1 month — it is the most expensive per-month option (cited as $30.99/month) — and that 48 months gives the deepest discount if affordable. [web check: current terms/pricing]
4. Apply the presenter's coupon code (transcribed "JFD10") for an additional 10% off, if using the affiliate path. [affiliate]
5. Create a Hostinger account: email + strong password > register > fill name/country/phone > pay (card, PayPal, Google Pay, crypto or local options) > submit.
6. Skip or close the post-purchase onboarding wizard (presenter notes it changes often) and go straight to the Hostinger admin panel.
7. In the Hostinger panel, do 3 things in order:
   a. Verify email — open the Hostinger verification email in your inbox and click "verify email."
   b. Claim the free domain — Domains > Claim Domain > pick an extension (presenter recommends .com "because websites look more professional and legit") > type the desired name > Check availability > Claim domain > fill country + Personal/Business > Next > contact details > Finish Registration > Continue > skip the "buy hosting" prompt (already purchased) > verify email again (domain-specific) > Continue to home. [verify UI]
   c. Install WordPress — Websites > Start Over > "who is this website for" (myself/business) > Next > "create or migrate a website" > Create a Website > select WordPress > create a free account (email + password) > Next > Create Blank Site > select the domain just claimed > Next > "where is your target audience located" (pick the region nearest your actual visitors) > Next > wait several minutes for install without closing the browser. [verify UI]
8. Open WP admin: Hostinger panel > Websites > Dashboard (next to the domain) > WordPress Overview > confirm "Force HTTPS" is toggled ON (this is the course's only explicit SSL/security step) > click "WordPress Admin." [verify UI]

### B. WordPress dashboard cleanup and core settings
1. Close the welcome popup; close default dashboard widgets, or use Screen Options to deselect every panel at once, for a clean dashboard. [b44de1f18767]
2. Plugins screen: select all default (host-bundled) plugins > Bulk actions > Deactivate > Apply. Then select all again > Bulk actions > Delete > Apply > OK. Deactivate before deleting to avoid orphaned settings. [95ada3c41602] [b44de1f18767]
   - Caveat from cards, not stated by presenter: verify no default plugin is actually required by your host or theme before bulk-deleting, and take a backup first (Hostinger's daily backups, confirmed running, are the safety net named here — see Section 9 for what the course does NOT cover on backups).
3. Users > Profile: set admin color scheme (cosmetic, admin-only — presenter keeps default), language (kept default English), first/last name, a required Nickname, and "Display name publicly as" (choose the variation that will show as the author name on blog posts). Optionally set a new password (WordPress suggests a strong one, or type your own). Click Update Profile.
4. Settings > General:
   - Site Title: the store/brand name shown publicly.
   - Tagline: write something specific and market-facing, e.g. presenter's example "best pet food online store in California" — naming category and geography, not generic filler. [f7075c8cc183]
   - Membership: check "Anyone can register" — needed so customers can create accounts.
   - New User Default Role: set to Subscriber, never Administrator/Editor/Author. [f66e3a492886]
   - Site Language, Timezone (set to your real location), Date format, Time format, Week Starts On — set to your preference; presenter kept English / Monday.
   - Save Changes.
5. Settings > Permalinks: change from whatever default (Plain / Day and name / etc.) to "Post name." Save Changes. [95ada3c41602] [284bc4b17ed7]
6. Understand backend (wp-admin, admin-only) vs frontend (public site) distinction. View frontend via "Visit Site" (hover the site title, top left). Access wp-admin at `yourdomain.com/wp-admin` at any time. [verify UI — the transcript itself garbles this path as "wpen admin," a transcription artifact, not a real WordPress path]

### C. Theme and page builder installation
1. Appearance > Themes: note the default stock WordPress themes (2023/2024/2025-style) are available but give limited design control compared to a page builder. [e91f80fe1721]
2. Appearance > Add Theme > search for and install a lightweight WooCommerce-friendly theme (transcript renders the name unclearly, sounds like "Woodify" — [verify UI: exact theme name/publisher, transcription is not reliable here]) > Activate. Purpose: provides shop sidebar/widget areas and WooCommerce customization options as a base, while Elementor does the actual visual design.
3. Get a free Elementor account (elementor.com > Get Started > sign in with Google/Apple/email > complete onboarding). Course uses the FREE Elementor plan throughout, not Pro.
4. Plugins > Add New > search "Elementor" > install "Elementor Website Builder" (10M+ installs cited) > Activate.
5. Install supporting plugins (Plugins > Add New > search each > Install), all used later:
   - "ElementsKit" — adds extra Elementor widgets [verify UI: exact publisher, transcript renders it as "Roxnor," likely a transcription error for the real publisher]
   - "Metform" — adds form-building widgets to Elementor, same publisher note as above [verify UI]
   - WooCommerce — by Automattic
   - A wishlist plugin (transcribed "MC Wishlist" / "more convert wish list for WooCommerce") — adds wishlist functionality [verify UI: exact plugin name]
   - "Variation Swatches for WooCommerce" — by Imran Ahmed
   - "Classic Widgets" — official WordPress.org plugin, needed for customizing shop/cart/blog widgets
6. Activation order matters: bulk-activate everything except WooCommerce and the wishlist plugin first (select all > Bulk actions > Activate > Apply). Then activate WooCommerce manually — this triggers WooCommerce's own setup wizard; the course skips it ("No, not ready now" / similar dismiss option — [verify UI: exact wizard-skip label]) and configures everything manually instead. Only after WooCommerce is active can the wishlist plugin (which depends on it) be activated. [e91f80fe1721]
7. Result: WooCommerce auto-creates Cart, Checkout, My Account, Shop and Wishlist pages (all empty at this point), and new sidebar menu items appear (Metform, Wishlist, WooCommerce, Products, Payments, Analytics, Marketing, Elements Kit, Elementor).
8. Version-pin the page builder if needed: presenter's own build used Elementor 3.33.6 and rolled back from the newly-released 4.0.1, which he judged unstable. Rollback path: Elementor logo (in the editor) > Exit to WordPress (open in new tab) > WP admin > hover Elementor > Tools > Version Control > Rollback to a previous version > select the target version > Reinstall > Continue > refresh the editor tab. [verify UI] [fe4eafe0a577]

### D. WooCommerce Settings > General
1. Store address: address line (optional), city, country/state, postcode — this feeds tax and shipping logic even if you have no physical storefront.
2. Selling location — pick one: "Sell to all countries," "Sell to specific countries" (whitelist), or "Sell to all countries except..." (blacklist). Course picks "specific countries" = United States only.
3. Shipping location — pick one: "Ship to all countries you sell to" (default, matches your selling whitelist), "Ship to all countries," "Ship to specific countries only," or "Disable shipping and shipping calculations" (use this last option only for a fully virtual/digital catalog — no shipping needed). [ca2329868be7]
4. Tax & Coupons: toggle ON "Enable taxes" if products are taxable (adds a new Tax settings tab); toggle ON "Enable coupons" if discount codes will be used.
5. Currency: pick the store's currency (course: USD).
6. Save Changes.

### E. WooCommerce Settings > Products
1. Shop page: which page displays the product grid (default: auto-created Shop page).
2. Placeholder image: upload an image to the Media Library, open it, copy its File URL, and paste that URL into the Placeholder Image field — shown whenever a product image is missing or fails to load. [2808b33010fc]
3. Measurements: pick a weight unit (kg/g/lbs/oz — course picks grams) and a dimension unit (m/cm/mm/inches — course picks inches). Set this before creating products; units are store-wide, so changing later means converting every product's data. [6a90a7b59c5c]
4. Enable Reviews (lets customers leave written feedback) and, separately, Enable Product Rating (adds the star-rating UI on top of reviews).
5. Save Changes.

### F. WooCommerce Settings > Tax
1. "Prices entered with tax": choose Yes (inclusive — you type the tax-included price, e.g. $105 for a $100 item + 5% tax) or No (exclusive — you type $100, and 5% is added visibly at checkout). The customer's final total is the same either way; only the displayed shop-page price differs. Course picks No (exclusive). [f294546e4437]
2. "Calculate tax based on": course keeps the default, customer shipping address (matters for origin- vs destination-based US states — see card 8e81d2277f77 for the origin/destination distinction, which the transcript itself does not spell out explicitly beyond naming "shop base address" vs "customer shipping address" as the two options).
3. Additional tax classes: default classes are Standard, Reduced rate, Zero rate. Course creates a new custom class by typing a name (example: "ABC rate") into the additional-classes field and saving — it then appears as its own editable tab.
4. In a tax-class tab, click "Insert row" to add a rate rule. Each row needs: Country code (e.g. US), State code (e.g. CA, NY — leave blank for a whole-country rule), Postcode/City (left blank in the demo), Rate (must be entered to 4 decimal places — e.g. 7.2500 for 7.25%, 4.0000 for 4%, 5.0000 for 5%), Tax name (free text, e.g. "tax"), Priority (lower number = higher priority — used to resolve overlapping rules), and a Shipping toggle (whether this state/country also taxes the shipping cost — decide per jurisdiction). [efa4821ff9f1] [7275017fd366]
5. Source real rates before entering them: presenter's method is "Google 'USA tax rates TaxJar'" > open the Sales Tax by State page > read each state's rate off the map. Rates cited in the transcript at recording time: California 7.25%, New York 4%, Washington 6.5%, Texas 6.25% (plus a "Newark" 4% figure the transcript does not clearly attribute to a state). [web check: current state/local sales tax rates — these change and vary by locality; a state's headline rate is not always the full combined local rate]
6. Conflict resolution example given: a California-specific row at priority 1 (7.25%) and a whole-US fallback row at priority 2 (5.0000, state blank) both match a California customer — priority 1 wins, so they pay 7.25%, not 5% and not a combination of both. [8e81d2277f77] [7275017fd366]
7. Save Changes. Tie a tax class to a specific product later on that product's General tab (Tax status = Taxable, Tax class = the class you built).

### G. WooCommerce Settings > Shipping
1. Shipping > Zones > Add zone: name the zone (e.g. "Whole USA") and set its Zone region (e.g. search and select "United States" to cover the whole country as one zone, or a single state like "California, United States" for a narrower zone). [2331d72754]
2. Add a shipping method to the zone: Free shipping or Flat rate.
   - Flat rate: set Name, Tax status (course picks None — no tax on shipping), and Cost. A plain numeric cost (e.g. 10.00) is charged PER ORDER regardless of quantity. [5c049a84968e]
   - Quantity-based cost formula: enter `[qty] * 10` in the Cost field (square brackets around qty, space, asterisk, space, per-item dollar amount) to charge per item instead of per order — 1 item = $10, 2 = $20, 10 = $100. [d3912129e9a7] [5c049a84968e]
   - Decision rule given: use quantity-based pricing for bulky/heavy goods (a bed cannot ship 10-for-the-price-of-1); use flat per-order pricing for small repeat-purchase goods (pet-food packets), since customers buying more of a light item shouldn't pay proportionally more shipping.
3. Shipping Classes (Shipping > Classes > Add shipping class): name it for the customer-facing consequence (e.g. "Premium shipping"), give it a unique slug (e.g. "AB-packages"), and a description (e.g. "for heavy packages"). Back in the zone's Flat rate method, a per-class cost field appears (e.g. Premium shipping = $20) alongside a "No shipping class" fallback cost (must be filled in, e.g. $10) that applies to any product without an assigned class. [e7fc88f9231f]
4. Multiple zones can stack: the course adds a second, narrower zone ("California") with a Free Shipping method gated by a Requirement — "Minimum order amount" set to $400, so only California customers spending $400+ get free shipping. [2331d72754]
5. The transcript does not fully explain zone-priority mechanics when a customer could match more than one zone beyond "each zone's rules are separate" — treat multi-zone overlap behavior as under-specified in this source and verify in current WooCommerce documentation before relying on it. [gap]

### H. WooCommerce Settings > Payments
1. Native offline options: Direct bank transfer, Check payments, Cash on delivery (COD). Course enables COD, calling it "a really popular payment method."
2. Stripe and PayPal require dedicated plugins, not WooCommerce defaults: install "Payment Plugins for Stripe WooCommerce" and "Payment Plugins for PayPal WooCommerce" (both published by "Payment Plugins" — other similarly-named plugins exist, so match the publisher). [b0fd0a5facf8] [02c7c501d001]
3. Back in Payments, enable "Credit Cards — Stripe by Payment Plugins" and "PayPal Gateway by Payment Plugins."
4. Connect Stripe: Manage > API settings > log into the Stripe dashboard > Developers > API keys > copy Publishable key and Secret key > paste both into WooCommerce (replacing any placeholder) > click Connection test — should read "Connection test to Stripe was successful" (this happens in Stripe's TEST mode). For live payments: in Stripe, click "Switch to live mode," complete Stripe's live verification, then repeat the paste with LIVE keys, making sure the WooCommerce mode selector is also set to Live before saving. [780a428b8702] [needs brand data: a real Stripe account and live API keys]
5. Connect PayPal: Manage > API settings > for live payments select "Production" (not Sandbox) and either paste the Production Client ID + Secret manually, or click "Connect to PayPal" and log in to auto-link — status should read "Connected." [needs brand data: a real PayPal business account]
6. Result: the demo store ends up with 3 payment methods — Stripe (card), PayPal, and Cash on Delivery.

### I. WooCommerce Settings > Accounts & Privacy
1. Enable "Guest checkout" — presenter calls this recommended, since it lets customers buy without creating an account. [fab5bea4ff25]
2. Enable "Allow customers to log in during checkout."
3. Enable "Allow customers to create an account during checkout" AND the matching toggle on the My Account page — presenter calls both "important."
4. Leave the rest at default. Save Changes.

### J. WooCommerce Settings > Emails
1. Review each email event: New order, Cancelled order, Failed order, On hold, Processing, Completed, Refunded, plus customer-facing counterparts. Some go to the store owner (admin events), others to the buyer (customer events). [6346d90f2e59]
2. For each one you want active: open Manage > toggle Enable > (optionally) edit the recipient address, subject line, heading and "additional content" text > Save. A disabled notification simply never sends — nothing else fails silently, it just doesn't fire.
3. A two-step example given: order cancellation first notifies the admin; only after the admin confirms does the customer-facing cancellation email go out.
4. Global email template styling (color palette) can be adjusted so all transactional emails match store branding.
5. Save Changes.

### K. WooCommerce Settings > Site Visibility, Store Details, Advanced
1. Site Visibility: new installs default to "Coming soon" (dashboard also flags "store coming soon"). Switch to "Live" and Save Changes only once tax, shipping, payments, products and a full purchase test are all done — this is a deliberate last step, not an early one. [c4521eb76468]
2. Store details (a "point of sale"-style settings tab): set the real Store name (replacing any placeholder like "My E-commerce Website"), and if there's a physical location, its address, phone and email. A refund/return policy can be pasted in as text here. [ce82c02fc4c6]
3. Advanced > Page setup: confirm Cart, Checkout and My Account pages are the auto-generated WooCommerce ones (course keeps defaults) or swap in custom pages if built separately.
4. Advanced > Terms and conditions page selector: if no real Terms and Conditions page exists yet, temporarily point this at an existing page (e.g. Privacy Policy) as a placeholder, and swap in the real page once written — do not leave a borrowed policy assigned permanently. [ce82c02fc4c6]

### L. Creating products (Products > Add New)
1. **Simple physical product** (course example: "Canine Crunch"):
   - Title, auto-generated permalink slug (editable), rich-text Description.
   - Product Data = Simple. General tab: Regular price and Sale price, entered with 2 decimals (e.g. 42.00 / 39.00) — sale price displays as the live price with the original struck through.
   - Tax status = Taxable; Tax class = the custom class built earlier (e.g. "ABC rate") so the product inherits the location-based rate table.
   - Inventory tab: SKU — course convention is lowercase title, spaces to hyphens, plus a running number (e.g. `canine-crunch-01`, so a second similar product could be `-02`). Toggle Stock management to show an exact quantity (e.g. "10 in stock").
   - Shipping tab: Weight and Length/Width/Height of the outer shipping package (not the bare product) in the units chosen earlier. Assign a Shipping class or leave "No shipping class" for the default rate.
   - Linked Products tab: Upsells (shown as "you may be interested in" suggestions) and Cross-sells (shown as "you may also like" suggestions) — can't be set on the very first product since no others exist yet. [b5fc3d2b7b4c]
   - Attributes tab: used for search-filtering and, separately, for building variations (see below).
   - Product image (featured thumbnail) and Product gallery images — set via the Media Library; bulk-upload multiple images at once via drag-and-drop (SVGs need SVG uploads enabled on the site first — see the SVG note in Section 8).
   - Categories (add inline, e.g. "Dog") and Tags (freeform, e.g. "crunchy food," "vegan food"); optional Brand field.
   - Short description (separate from the long Description, shown right under title/price).
   - Publish. [f81c2abfc7fb]
2. **Variable product** (course example: "Bark and Bite"):
   - Create global attributes FIRST at Products > Attributes (not on the product page): e.g. "Weight" (type: Button) with terms 200g/400g/600g, and "Toy" (type: Radio) with terms "With toy"/"Without toy." [13e3297ba233]
   - On the product: Product Data = Variable product (price field disappears at product level — set per variation instead). Set Tax class and SKU as with a simple product; skip weight/dimensions here (set per variation instead).
   - Attributes tab: "Add existing" > select each global attribute > select all its values (or "Select all") > Save attributes, for each attribute.
   - Variations tab: "Generate variations" auto-creates every combination (course example: 3 weights x 2 toy options = 6 variations).
   - Open each variation row and set: variation image, unique SKU, Regular price, Weight (matching the attribute value), Shipping class and Tax class (both default to the product-level setting unless overridden per variation). [a8a1945fe798] [a065c6dfec57]
   - Course's own example prices (illustrative only — the presenter's own with/without-toy pricing pattern was inconsistent, flagged in Section 9): 200g+toy $37 / 200g+no-toy $40 / 400g+toy $49 / 400g+no-toy $52 / 600g+toy $60 / 600g+no-toy $68.
   - Every variation you want purchasable must have a price — a variation with no price silently fails at add-to-cart (per the card layer's caveat; not stated aloud in the transcript but implied by "you don't have to select the tax class and shipping class... but you have to" enter a price).
   - Front end: shows "Select options" instead of "Add to cart" until options are chosen, and a price range (e.g. "$37 – $68") on the shop grid.
3. **Virtual / downloadable product** (course example: "Pet Food Guide" ebook):
   - Product Data = Simple, then check "Virtual" (removes the Shipping tab entirely — nothing to ship) and "Downloadable."
   - Regular/Sale price as normal (course: $10 / $9).
   - Downloadable files: "Add file" > paste a URL or "Choose file" from the Media Library (course attaches a PDF) > Insert file URL.
   - Download limit (course: unlimited) and Download expiry (course: none/never) — set numeric limits if piracy or access control matters.
   - Skip stock management (unlimited digital good); still set a SKU (e.g. "ebook-01").
   - Publish. Front end: no stock UI; after purchase, a Download button appears on the order confirmation / My Account > Downloads screen. [5c8864617956]
4. **External / affiliate product** (course example: an Amazon "Cat Food" listing):
   - Product Data = External/Affiliate product.
   - Product URL = the affiliate tracking link.
   - Button text = custom CTA replacing "Add to cart" (course: "Buy from Amazon").
   - Price = the partner's displayed price, for comparison only (no purchase happens on your own site, so tax status/class don't apply).
   - Category/tag, short description, product image, publish as normal. [5c9382dfb092]
   - Note: presenter's own workflow was to right-click-save the product image from the affiliate listing (e.g. Amazon) for reuse — check the partner program's own terms on image and price display before doing this; it is a separate question from the ecomOS rule against copying a competitor's ad creative, since here the "competitor" is the actual affiliate merchant whose product you are promoting under their program.

### M. Coupons (Marketing > Coupons)
1. Add coupon: Coupon code (the customer-facing code, e.g. "JFD20") and an internal Description.
2. Discount type: Percentage discount (e.g. 20 = 20% off) vs Fixed cart discount / Fixed product discount (a flat dollar amount regardless of price).
3. Optional Coupon expiry date.
4. Usage restrictions: Minimum spend (course example: $200) and Maximum spend (course example: $500 — rationale given: "20% of $500 is already a lot," i.e. cap the coupon's dollar cost on large carts). Can also restrict/exclude by specific products, categories, or allowed customer emails.
5. Usage limits: "Usage limit per coupon" = total redemptions across all customers (course leaves unlimited); "Usage limit per user" = max redemptions by one customer (course sets 10).
6. Publish to activate. [ba99780859ec]

### N. End-to-end purchase test and order management
1. As a buyer: add a simple product, a downloadable product and a chosen variable-product variation to the cart; adjust quantities from the mini-cart or full Cart page (shows Subtotal, flat-rate shipping line, tax line, Estimated total).
2. Checkout: enter contact info, shipping address, pick a shipping method, pick a payment method (COD, Stripe, or PayPal), optionally add an order note.
3. Apply a coupon code in the order summary and confirm the discount recalculates the total live.
4. Place the order > Thank-you page shows order details and, for any digital product, a Download button.
5. As admin: WooCommerce > Orders > open the order > review line items and customer info > set Status (Pending payment, On hold, Processing, Completed, Cancelled, Refunded, Failed, Draft). Workflow given: ship the physical item first, THEN mark Completed and click Update — this triggers the customer-facing "completed" email if that notification is enabled.
6. Customer-side My Account tour: Wishlist, Orders (history), Downloads, Addresses, Payment methods, Account details, Logout — the account itself was auto-created during checkout (from the Accounts & Privacy setting above), with no separate signup step required. [fa39013559f5]

### O. Pages, navigation and store-wide identity (structural items only — Elementor visual design is out of scope, see Section 9)
1. Create a Home page (Pages > Add New > title "Home" > Publish, initially empty) and assign it as the site's static homepage: Settings > Reading > "Your homepage displays" > A static page > select Home > Save Changes. [ef53f8ba81ec]
2. Create a Contact page the same way (Add New Page > "Contact" > Publish), then design it in Elementor (design steps out of scope here).
3. Create a Blogs page as an empty placeholder, publish it, then assign it under Settings > Reading as the site's Posts page so it auto-populates with every published post. [bd3c16bb41d2]
4. Write blog posts via Posts > Add Post (trash the default "Hello World" post first): rich-text body, Featured Image (becomes the post thumbnail everywhere), Category, Tags, Publish. [260535321f21]
5. Site identity: Appearance > Customize > Site Identity — upload a logo (Skip Cropping to keep full image, then resize with the slider), optional retina/mobile logo variants, Site Title, Tagline, and a Site Icon (favicon). [75fc4536479b]
6. Navigation: Appearance > Menus — create a primary/header menu (add Home, Shop, Blog, Contact, reorder as needed) and one or more footer menus (a "quick links" menu, plus a legal/utility menu for Privacy Policy / Terms / Disclaimer, using "#" as a placeholder link until those pages exist — remember to fill them in later). Populate footer widget columns (Appearance > Widgets) with a logo block, a short description, the footer menus, and contact details. [7c9f9bf805cf] [2f2305cf3b06]
7. Global theme settings via Appearance > Customize > Layout and Colors: site-wide background color, content width, header background color, footer column count and copyright text (dynamic tags like current-year and site-title are supported), and a scroll-to-top button (device visibility, position, color). Also WooCommerce-specific customizer panels: Site Notice (replace or clear the default "this is a demo store" text before launch), Product Catalog (products-per-page, course: 12), Product Images (thumbnail size/cropping — keep all product images the same width and height so cards align), Shop Archive (card content, hover effect, sale-tag style, add-to-cart button style), Product Single (content background, gallery layout, section order). [ca6a6504a47c] [fd779a1ad349]
8. A page-header/banner-with-breadcrumbs template part can be turned on (Customize > Layout > Page Header, naming varies by theme) so non-homepage pages (shop, blog, cart, contact) get a consistent branded title band instead of starting abruptly. [6eacc38f274b]

### P. Final verification pass
1. Run a structured end-to-end check across the whole storefront before calling it done: top navigation links, Shop page (grid, sidebar search, price filter, category/attribute filters), a Product page (gallery, variation selector, description, related products, add-to-cart), Blog listing and single post, Contact page (details, form, map), search, and the My Account dashboard (wishlist, orders, mini-cart). [f93901f8f848]
2. This is a visual/functional sweep, not a substitute for the payment test in Section N — actually place a test order separately (per the card layer's caveat; the source's final "quick tour" segment is presented as a design walkthrough, and the actual purchase test happens earlier in the transcript, not as the literal final step).

## 4. Rules, thresholds and numbers

| Rule / setting | Number or threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Tax rate entry format | 4 decimal places (e.g. 7.2500) | Any WooCommerce tax rate row | WooCommerce's rate field expects this format | efa4821ff9f1 |
| California sales tax (example, dated) | 7.25% | Presenter's TaxJar lookup at recording time | [web check] | efa4821ff9f1 |
| New York sales tax (example, dated) | 4% | Presenter's TaxJar lookup at recording time | [web check] | efa4821ff9f1 |
| Washington sales tax (example, dated) | 6.5% | Presenter's TaxJar lookup at recording time | [web check] | 7275017fd366 |
| Texas sales tax (example, dated) | 6.25% | Presenter's TaxJar lookup at recording time | [web check] | (transcript only) |
| Tax priority resolution | lower number = higher priority | Overlapping tax rows (e.g. state-specific vs country-wide) | Presenter's CA(priority 1)/US(priority 2) example | 7275017fd366 |
| Flat-rate shipping, per-order | $10.00 example | Default flat-rate cost, no formula | Presenter's example | 5c049a84968e |
| Flat-rate shipping, per-item | `[qty] * $10` example | Bulky/heavy goods | Presenter's example | d3912129e9a7 |
| Shipping class example prices | $10 default / $20 "Premium" | Products needing heavier/special packaging | Presenter's example, not a carrier-sourced number | e7fc88f9231f |
| Free-shipping minimum order (example) | $400 | California-only zone in the demo | Presenter's own setup, not a benchmark | 2331d72754 |
| Coupon minimum spend (example) | $200 | Usage restriction example | Presenter's example | ba99780859ec |
| Coupon maximum spend (example) | $500 | Caps discount cost on large carts | Presenter's stated reasoning ("20% of $500 is already a lot") | ba99780859ec |
| Coupon usage limit per user (example) | 10 | Prevents unlimited repeat use by one buyer | Presenter's example | ba99780859ec |
| Products per page (shop grid) | 12 | Course's own catalog-display choice | Presenter's example, not a conversion-tested number | fd779a1ad349 |
| SKU convention | lowercase-title-hyphenated + running number (e.g. canine-crunch-01) | Any product needing a unique identifier | Presenter's own scheme, not a WooCommerce requirement | f81c2abfc7fb |
| Hosting term recommendation | 48 months for deepest discount; never 1 month | Choosing a Hostinger billing term | Presenter's stated math (1-month cited at $30.99/mo) | [web check] |
| Elementor version pinned | 3.33.6 (stable) vs 4.0.1 (new, called unstable) | Recording-time only | Presenter's own judgment call | fe4eafe0a577 |

## 5. Diagnostics and checks

- **Check:** did permalinks actually apply? **How:** open a product page and a category/shop page after saving Settings > Permalinks. **Good:** URL reads `domain.com/shop`-style. **Bad:** URL still shows numbers or `?p=`. **Fix:** some hosts need a `.htaccess`/rewrite refresh; re-save permalinks or contact host support. [95ada3c41602]
- **Check:** is HTTPS actually enforced? **How:** look for "Force HTTPS" toggled ON in the Hostinger WordPress Overview panel, and confirm the padlock shows on the live domain. **Bad:** checkout pages loading without HTTPS. **Fix:** enable Force HTTPS before launch; this is the course's only explicit SSL check (see Section 9 for what it does not cover). [2946d83f30cb] [95ada3c41602]
- **Check:** does a tax rule apply correctly by state? **How:** add a product with the relevant tax class to cart and check out with a test address in each state you care about. **Good:** tax line matches the rate table. **Bad:** wrong rate or no tax charged. **Fix:** re-check state code, priority number and whether a broader rule is silently outranking the specific one. [7275017fd366]
- **Check:** does quantity-based shipping scale correctly? **How:** test a 2-item and a 10-item cart against the `[qty] * X` formula. **Good:** shipping cost multiplies as expected. **Bad:** flat cost regardless of quantity. **Fix:** confirm the formula syntax is in the Cost field exactly (brackets, spacing, asterisk) — verify current syntax in your WooCommerce version. [d3912129e9a7]
- **Check:** is a payment gateway actually connected? **How:** run the built-in "Connection test" after pasting Stripe API keys; check PayPal's status reads "Connected." **Bad:** test fails or reads "not connected." **Fix:** re-copy keys (check test vs live mode match), or re-run "Connect to PayPal." Place one small live test transaction and refund it before fully trusting a gateway. [780a428b8702]
- **Check:** does every variation of a variable product actually sell? **How:** open the front-end product page and try adding each option combination to cart. **Bad:** a combination shows "Select options" indefinitely or add-to-cart silently does nothing. **Fix:** confirm every variation row has a price set — a priceless variation is not purchasable. [a8a1945fe798]
- **Check:** are transactional emails firing? **How:** place a real or test order and watch for the admin "new order" email; trigger a cancellation to confirm the two-step admin-then-customer email flow. **Bad:** expected email never arrives. **Fix:** confirm the specific event's Enable toggle is on in WooCommerce > Settings > Emails; if enabled but still not arriving, the issue is host/SMTP deliverability, not the WooCommerce template (per the card layer's caveat — the transcript itself does not diagnose deliverability). [6346d90f2e59]
- **Check:** is the store still hidden or accidentally live? **How:** look at the WooCommerce dashboard banner ("store coming soon" vs "store is live") and Settings > Site Visibility. **Fix:** don't flip to Live until tax, shipping, payments, products and a purchase test are all verified. [c4521eb76468]
- **Check:** are product images consistent enough for the shop grid to look aligned? **How:** eyeball the shop page grid after uploading several products. **Bad:** cards of visibly different heights/crops. **Fix:** upload all product images at the same width and height (presenter's stated rule, not a hard WooCommerce requirement). [fd779a1ad349]

## 6. Tools, settings and named features

- **Hostinger** — hosting provider used throughout; course is built on Hostinger's own admin panel (not just the WordPress onboarding wizard) so steps stay findable even as onboarding UI changes. [verify UI] [affiliate: presenter's own link + coupon]
- **WordPress** — core CMS; used dashboard: Posts, Media, Pages, Comments, Appearance, Plugins, Users, Settings.
- **WooCommerce** (by Automattic) — turns the WordPress site into an ecommerce store; the central plugin for products, orders, tax, shipping, payments, coupons and customer accounts.
- **Elementor** (free tier) — visual page builder used for all front-end design (homepage, contact page, blog styling, footer). Free tier covers containers, headings, images, text editor, video, buttons; Pro-only widgets (search, posts, portfolio, gallery, loop, carousel) are not used. [4c3e5a5a5303]
- **ElementsKit** — third-party plugin adding extra Elementor widgets, including the countdown-timer widget used on the homepage promo box. [verify UI: exact plugin/publisher name]
- **Metform** — third-party plugin adding the contact-form widget used on the Contact page.
- **Wishlist plugin** (transcribed "MC Wishlist"/"More Convert") — adds a wishlist feature alongside WooCommerce. [verify UI: exact plugin name]
- **Variation Swatches for WooCommerce** (by Imran Ahmed) — enables visual swatch-style selection for product variations.
- **Classic Widgets** — official WordPress.org plugin restoring the classic widgets screen, used for shop/cart/blog page widget customization.
- **Payment Plugins for Stripe WooCommerce** and **Payment Plugins for PayPal WooCommerce** (both by "Payment Plugins") — dedicated gateway plugins, used instead of WooCommerce's own default payment options. [b0fd0a5facf8]
- **TaxJar** — referenced only as a lookup source ("Sales tax by state" page), not installed as a plugin/service in this course; used purely to source example rate numbers to type manually into WooCommerce. [web check: whether an automated tax service like TaxJar's actual integration would be more reliable than manual entry — not addressed by this source]
- **Google Maps widget** (via Elementor) — embeds a location-focused map on the Contact page.
- **kitninja.com** and **kitpapa.com** — paid Elementor template marketplaces, promoted as time-saving alternatives to building the design manually; both are explicit affiliate/sponsored mentions with time-limited pricing cited (see Section 9). [affiliate]

## 7. Examples and case results

- Example only (not a case study): a fictional pet-food store built live in the video, with products "Canine Crunch" (simple), "Bark and Bite" (variable, weight x toy-option), "Pet Food Guide" (virtual/downloadable ebook), and a "Cat Food" Amazon affiliate listing.
- Example purchase: cart containing multiple product types, a 20%-off coupon applied, final total shown as $190.72 — this is one specific demo cart, not a benchmark number.
- Example tax table: California 7.25% (priority 1) beating a whole-US 5% fallback (priority 2) for a California buyer — illustrates the mechanic, not a claim about correct real-world rates today.
- Example shipping zone: "Whole USA" zone with $10 flat-rate (or `[qty]*10`), plus a narrower "California" zone offering free shipping above a $400 minimum order — again a worked mechanic, not a recommended threshold.
- Example variation pricing: 200g without-toy priced higher ($40) than 200g with-toy ($37) — the presenter's own inconsistency, explicitly noted in Section 9 as a data-entry mistake in his own demo, not an intentional pricing strategy.

## 8. Mistakes the source warns about

- Deleting active plugins without deactivating first can leave orphaned settings or errors — deactivate, then delete. [b44de1f18767]
- Leaving the "New user default role" above Subscriber is a stated security risk — self-registered customers could gain content-editing or publishing rights. [f66e3a492886]
- Getting tax-rule priority backwards (thinking a higher number wins) silently charges the wrong rate to customers. [7275017fd366]
- Assuming a flat shipping cost scales with quantity when it does not (the default is per-order, not per-item) — this can quietly erode margin on bulky-goods orders shipped in bulk. [5c049a84968e]
- Pasting Stripe/PayPal keys while the plugin is in the wrong mode (test keys while set to live, or vice versa) breaks the connection test silently rather than obviously. [780a428b8702]
- Publishing a variation with no price — it looks like a normal option in the UI but is not actually purchasable (add-to-cart fails). [a8a1945fe798]
- Building product attributes at the product level instead of globally, which forces re-entering them for every new product and produces inconsistent filters later. [13e3297ba233]
- Assuming a coupon with a high percentage and no maximum-spend cap is safe — large carts can make the discount very expensive; a maximum-spend ceiling exists specifically to prevent this. [ba99780859ec]
- Leaving a borrowed policy page (e.g. Privacy Policy) permanently assigned as "Terms and Conditions" instead of swapping in a real one once written. [ce82c02fc4c6]
- SVG icon uploads: a batch upload can silently show only one icon in the media library — the fix is to publish the page first (so design work isn't lost), refresh the editor, then reopen the SVG uploader, where the rest now appear. Also, SVG uploads must be explicitly enabled on the site before any will show at all. [a2c806b07d12] [gap: the transcript promises to show "how to enable this" for SVG uploads but the actual enabling step is not captured in the exported text]
- Dragging a widget/container to reorder it for one screen size (e.g. mobile) also changes its order on desktop — the fix is the Advanced > Order property, which reorders only for the active breakpoint. [dd4deb9d6b86] [a518d6e71675]
- Flipping the store to "Live" before payments, shipping and a full purchase test are verified. [c4521eb76468]

## 9. Caveats, conflicts and what is missing

- **Affiliate relationships throughout.** The Hostinger hosting link (with a "JFD10"-style coupon) and both template marketplaces (kitninja.com, kitpapa.com) are explicit affiliate or sponsored mentions with time-limited pricing quoted live in the video (a "New Year lifetime access" offer at $59 for kitninja's Buy All package, $49 for kitpapa). None of this pricing should be trusted as current — [web check] before repeating any number from this source to a client or in a cost estimate.
- **The presenter's own pricing/plan inconsistency is a live example of an unstable claim.** The 12-month vs 48-month Hostinger math (e.g. "$2.99/month" vs "$4.49/month," with a coupon dropping these to "$2.69" and "$4.04") is exactly the kind of number the presenter himself flags as changing "depending on the day you're watching this video."
- **Elementor version-pinning is dated by construction.** The course explicitly builds on Elementor 3.33.6 because 4.0.1 was "just launched" and judged unstable at recording time. Neither version number should be assumed current — [web check] the actual current stable release before following any Elementor UI path in this file.
- **Gap: security, backups and performance are essentially unaddressed**, despite the course's own intro promising a "100% secure" website. Beyond enabling Force HTTPS and noting that the recommended Hostinger plan includes daily backups, the source gives no security hardening steps (no mention of two-factor auth, login-attempt limiting, security plugins, malware scanning), no explicit backup verification or restore walkthrough, and no performance/caching/speed optimization content (no caching plugin, no image optimization, no CDN configuration beyond noting the hosting plan includes one, no page-speed testing). If a task needs these, this source cannot supply them — check other 05-SET or 08-SPD sources.
- **Gap: exact WooCommerce shortcode text is never shown verbatim.** The homepage's "best selling products" and "latest products" sections, and the cart/checkout shortcode swap, are all described as "copy this line from [an external page]" without the actual shortcode string being spoken or captured in the transcript. Look up current shortcode names/arguments directly in WooCommerce's own documentation rather than relying on this source. [b3b806623b72] [942b47045992]
- **Gap: multi-zone shipping priority is under-specified.** The course adds a country-wide zone and a narrower state zone but does not explain how WooCommerce resolves a customer matching both beyond "each zone's rules are separate" — verify current WooCommerce zone-matching behavior (typically first-matching zone in the configured order) before relying on stacked zones for real logic.
- **Internal inconsistency, presenter's own build:** the "Bark and Bite" variable product prices without-toy higher than with-toy at the same weight (200g: no-toy $40 vs with-toy $37) — the presenter does not catch or explain this on camera; it reads as a data-entry mistake in the demo, not an intentional pricing lesson. Do not copy this pattern.
- **No conflict found with general ecommerce advice** on the core mechanics covered (permalinks, guest checkout, global attributes for variable products, tax-priority resolution, launch-gating on a purchase test) — these align with standard WooCommerce practice as documented by WooCommerce itself. The one point worth flagging for an ecomOS reader specifically: the source's tagline advice ("best pet food online store in California" as an SEO-facing tagline) is presented as a ranking aid ("high chance... shown on Google search result"), which overstates a tagline's actual SEO weight — a site tagline is a minor, weakly-weighted signal at best, not a mechanism that reliably produces search visibility. Treat this as positioning copy advice, not an SEO tactic.
- **Design work explicitly out of scope for this file.** Roughly the back half of the transcript (banner/hero construction, category badges, countdown promo box, responsive breakpoint fixes, custom CSS polish, footer widget layout, contact-page banner and form styling) is genuine Elementor/CSS design work. Per this source's own routing note, that belongs in folder 07-LPG, not 05-SET, and is only summarized at a structural level here (Section 3.O) rather than detailed step-by-step. A pass-2 writer building the 07-LPG folder playbook should pull the full detail from cards bc76ce991561 through b49ee328a79a (and neighboring design-tagged cards) rather than from this file.

## 10. Card index

95ada3c41602 - Optimize WordPress permalinks and strip default plugins after install
8e81d2277f77 - Set origin-based vs destination-based tax correctly per state
d3912129e9a7 - Charge flat-rate shipping per item instead of per order
b0fd0a5facf8 - Install Stripe and PayPal via dedicated third-party plugins, not defaults
13e3297ba233 - Create global product attributes before building variable products
a8a1945fe798 - Build a Variable Product with Global Attributes
02c7c501d001 - Install Payment Gateways for Stripe and PayPal
ca2329868be7 - Set Store Address, Selling and Shipping Locations
2808b33010fc - Set a Catalog Placeholder Image
f294546e4437 - Choose Tax-Inclusive or Tax-Exclusive Product Pricing
efa4821ff9f1 - Build Location-Based Tax Rates with State Rows
6a90a7b59c5c - Set Weight and Dimension Units Before Adding Products
f66e3a492886 - Enable Customer Registration with Subscriber Role
284bc4b17ed7 - Set Post Name Permalinks for Clean Product and Page URLs
f7075c8cc183 - Configure Site Title and Tagline as Positioning Statements
e91f80fe1721 - Choose a Lightweight Ecommerce Theme and Build with a Page Builder
b44de1f18767 - Back Up and Clean a Fresh WordPress Install
2946d83f30cb - Verify Hosting, Domain and SSL Before Building
c39aeb8d4ca9 - Build Store Front-End Structure That Mirrors Top Ecommerce Sites
7275017fd366 - Set State and Country Tax Rates with Priority Rules
2331d72754 - Use Shipping Zones to Localize Fulfillment Offers
5c049a84968e - Choose Per-Order or Per-Item Flat Rate Shipping
e7fc88f9231f - Create Shipping Classes for Heavy or Premium Packaging
780a428b8702 - Enable Cod and Verify Stripe and PayPal Setup
fab5bea4ff25 - Configure Accounts and Checkout Login Options
6346d90f2e59 - Turn On Transactional Email Notifications Per Event
c4521eb76468 - Keep the Store in Coming Soon Until Catalogs and Pages Are Ready
ce82c02fc4c6 - Fill Store Details and Page Assignments in Settings
f81c2abfc7fb - Create a Simple Physical Product With Pricing, SKU and Stock
a065c6dfec57 - Build Variable Products from Global Attributes
5c8864617956 - Create Virtual Downloadable Products for Digital Goods
5c9382dfb092 - List Affiliate Products as External Products
b5fc3d2b7b4c - Use Upsells and Cross-Sells to Raise Cart Value
ba99780859ec - Configure Coupon Type, Restrictions and Usage Limits
fa39013559f5 - Run an End-to-End Purchase and Order Management Test
ef53f8ba81ec - Set a Static Homepage Before Building the Storefront
4c3e5a5a5303 - Know Free Page Builder Versus Pro Widget Boundaries
bc76ce991561 - Build a WooCommerce Homepage Banner in Elementor with Containers
fe4eafe0a577 - Roll Back Elementor to a Stable Version Before Building
72d6fb10ee6e - Speed Up Store Builds with Elementor Global Colors and Global Fonts
0309c3888f8b - Use Position Absolute + Offsets to Place Decorative Store Images Precisely
b3b806623b72 - Embed Best-Selling and Latest WooCommerce Products via Shortcode
720823a4c0fe - Import a Prebuilt Elementor Template (e.g. Reviews Section) Instead of Building From Scratch
1bfcc5f7fc8c - Build a Countdown-Timer Promo Box for Offers and Drops
ad984b949f14 - Build a Category Showcase Section with Floating Badges
dd4deb9d6b86 - Make Elementor Store Sections Responsive Without Breaking Desktop
6be8fc577f9e - Set a Global Page Background and Full-Width Layout Once Per Page
a518d6e71675 - Use Negatives Margins and Order to Control Store Section Spacing
d9f957bcecd9 - Create Global Font and Colour Shortcuts Inside Widget Settings
5855ce9236b4 - Plan for a Blog Section by Deferring Styling Until Posts Exist
a2c806b07d12 - Fix the SVG Icon Upload 'Only One Image Shows' Bug
7a6cc2f3beca - Renaming and the Structure Panel Keep Complex Store Builds Sane
0276c07ed18a - Choose the Right Text Widget for Store Copy
5ae0eb8572ab - Building a responsive homepage in Elementor (tablet/mobile pass)
bd3c16bb41d2 - Adding more pages before theme customization
6aa4c928e9d4 - Designing a contact page banner and contact-detail cards
7911dd7fa53e - Building a contact form with MetForm in Elementor
7dd589d507f4 - Embedding a store location map widget
260535321f21 - Writing and publishing store blog posts
c04ae9410ddd - Configuring the blog post widget on the homepage
75fc4536479b - Setting site identity: logo, title, tagline and favicon
ca6a6504a47c - Setting global theme layout, colors and scroll-to-top
fd779a1ad349 - Configuring WooCommerce catalog and product display settings
7c9f9bf805cf - Creating header and footer nav menus in WordPress
2f2305cf3b06 - Building footer widget columns with logo, menus and contact info
ff8c51053abf - Catching left-over homepage sections and finishing the pass
27ee48400f7c - Build a multi-column footer with navigation menus and contact details
b49ee328a79a - Apply a curated custom-CSS set to polish theme design elements
942b47045992 - Replace default cart and checkout widgets with WooCommerce shortcodes
6eacc38f274b - Enable and style a page header banner with breadcrumbs
6721dd6120a4 - Change the blog author display name store-wide
f93901f8f848 - Verify storefront pages end-to-end after setup
