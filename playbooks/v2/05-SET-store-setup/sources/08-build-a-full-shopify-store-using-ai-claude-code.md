# How to Build a Full Shopify Store using AI (Claude Code)

source_id: 1jz7Ogw0tf0m2Z44y_eerkueDY3b1aPTT  |  folder: 05-SET-store-setup  |  cards: 12  |  words: 9,901  |  type: YouTube video transcript (tutorial, sponsored)

credibility: Unnamed YouTuber/course-style presenter. This is a sponsored walkthrough: the presenter has "partnered with Shopify" for an affiliate deal (3-day free trial, then $1/month for 3 months) and repeatedly points viewers to "the guide linked in the description" for exact copy-paste commands and prompts, which is a lead magnet not included in this source. Evidence is a single self-made demo store (a fictional "Metics Fashion Store" selling t-shirts) built live on camera, with no sales data, no conversion numbers and no client results. Treat this as one operator's opinionated workflow, not a benchmarked method. `[web check: presenter identity and channel, if attribution matters]`.

date signals: References Shopify's Horizon theme as the current default theme, Claude Code installed via `irm https://claude.ai/install.ps1 | iex`, Claude Pro at "$20 a month," Shopify CLI installed via `npm install -g @shopify/cli@latest`, and a "$1 per month for three months" Shopify trial deal. All of these are point-in-time and change often. `[web check: current Shopify default theme, Claude Code install command, Claude Pro price, Shopify trial offer]`.

## 1. What this source is for

Shows a non-developer how to stand up a complete Shopify store end to end using Claude Code as the build agent: install the local toolchain, connect Claude Code to a live Shopify theme via the Shopify CLI, brief Claude with product data and a visual-inspiration folder, build the homepage section by section with plain-English review cycles, then finish back-office settings (payments, shipping, tax, policies, domain) and publish. It is a full-pipeline setup guide, not a copywriting or ad-creative guide.

## 2. Principles

1. Give the AI real inputs before asking it to design anything. The store's products, and a folder of visual references (screenshots, logo, product photos, lifestyle images), should exist before the agent starts building, because the agent designs the homepage and product pages around what already exists in the store and in that folder. Condition: applies to any AI-assisted theme build, not just this one. Evidence: the presenter adds all products and collections, and assembles the inspiration folder, before opening Claude Code at all. [5a0b9ad6456f] [66e36f527ce2]
2. Let the agent interview you before it builds anything. A single "build me a store" instruction is presented as the wrong way to start; the source's method has Claude read the theme and inspiration folder first, then ask about visual direction, homepage sections, and fonts, then propose a plan, before writing any section. Condition: applies to the first build session on a fresh theme. Evidence: presenter's own comparison ("it's honestly a lot like working with a real designer") is opinion, not a tested claim. [13e82e14fdd0]
3. Build and review one homepage section at a time, not the whole page at once. Each section is generated, previewed locally, approved or corrected in plain English, and only then does the next section start. Condition: applies while the homepage is still being designed; once sections exist, batch prompts for small fixes are fine (see mistake below). Evidence: presenter's own workflow across hero, category, featured products, reviews/story. [4d8bf77b16e5]
4. Preview privately before publishing. A local dev server (or, as alternatives the agent may offer, an unpublished preview theme or static mockups) lets you and the agent see changes without exposing them to customers. Condition: applies for the entire build, until you are ready to push to the live theme. Evidence: presenter picks the local dev server specifically and describes it as "only you can see it." [e27f52047618]
5. Manual editing in the Shopify theme editor still works after an AI build. Building with Claude Code does not lock the theme into code-only edits; the presenter uses the normal drag/click theme editor afterward to tweak text, reorder sections, and check mobile. Condition: applies once the AI-built theme is uploaded to Shopify (even before publishing). Evidence: presenter demonstrates this directly. [d23a4cb7706c]
6. Policy pages must exist in Shopify admin before footer links to them will appear, even if the theme already has a footer. Condition: applies whenever a build includes a footer with policy links. Evidence: Claude itself told the presenter this ("policy links will only appear once you create policies in the Shopify admin settings"), reported inside the transcript. [dd3f3bb627c7]
7. Default to free shipping with a minimum order value for most stores, rather than paid shipping tiers. Condition: this is the presenter's general recommendation ("I'd recommend for most stores just offering free shipping"), not a rule tied to margin data. [a3ff8ef93a56]
8. A default `.myshopify.com` domain is fine for testing but is treated as a professionalism liability long-term; buy or connect a real domain before treating the store as final. Condition: applies before public launch/marketing spend, per the presenter's judgment only. [4ad69ffecb22]

## 3. Procedures

### A. Set up the Shopify account
1. Go to the presenter's Shopify deal link (an affiliate link — not a generic signup) `[web check: current Shopify trial terms, they change]`.
2. Enter email, click continue, create a password, click "Create account."
3. Enter payment info to claim the deal (in this source: 3 days free, then $1/month for 3 months, cancel anytime) `[web check: offer terms]`. Click "Subscribe for $1."
4. On the plan page, click "Try Basic" (presenter's recommendation for stores just starting out).
5. Click "Not now," then "I'll do this later" to skip remaining onboarding prompts and land in the Shopify dashboard.

### B. Install the local toolchain (Node.js, Claude Code account, Git, Shopify CLI)
1. Install Node.js: go to nodejs.org, click "Get Node.js," scroll to the pre-built installer for your OS, download and run it. Accept license, keep defaults through the wizard. On the "tools for native modules" screen, leave the box **unchecked** — not needed for this workflow. Click Install, then Finish. `[verify UI]`
2. Create a Claude account: go to claude.ai, enter email, verify via emailed code or link, create account.
3. Subscribe to the **Pro plan** — required because Pro includes Claude Code (the source states this as the reason, not optional for this workflow). Choose yearly or monthly, enter payment info, click Subscribe. `[web check: current Claude plan names/pricing]`
4. Optionally install the Claude desktop app when prompted (explicitly optional — it is a separate chat app, not needed for the CLI workflow).
5. Install Git: go to git-scm.com, click "Install for Windows" (or the OS-appropriate build), run the installer, accept defaults, click Install then Finish. `[verify UI]`
6. Open a terminal — PowerShell on Windows (Windows key, type "PowerShell"), or Terminal on Mac (Cmd+Space, type "Terminal").
7. Install the Shopify CLI. Command as given in the source: `npm install -g @shopify/cli@latest` (the transcript itself renders this once as "npm instal -g @shopify/cli@latest" — almost certainly a transcription artifact of "install," not a different flag; verify the exact current command). `[web check: current Shopify CLI install command]`
8. Verify: run `shopify version`. A version number printing means it installed correctly; other lines of output during install are normal, not errors.
9. Install Claude Code. The source gives the **Windows** command only: `irm https://claude.ai/install.ps1 | iex`. It states a Mac command also exists and is "in the guide," but does not state it in this transcript — that command is a gap in this source. `[web check: current Claude Code install command for Mac and Windows]`
10. Close and reopen the terminal after installation completes ("Installation complete!").
11. Run `claude`, press Enter to go through onboarding: choose a theme (dark shown), choose "Claude account with subscription," authorize in the browser, copy the code, paste it back into the terminal, press Enter to log in, press Enter to trust/lock the workspace.

### C. Add products and collections (before any AI design work)
1. In Shopify admin: Products > Add product.
2. Title and description: write them yourself, or open a separate Claude chat, drag in the product photo, and ask: **"Give me a short and clean product title and description for this product."** Give feedback and iterate if the first result misses; copy the accepted title/description into the product form.
3. Media: upload product photos — your own, AI-generated (e.g. ChatGPT, per the source), or stock (presenter used Pexels).
4. Pricing: set price (worked example: $19.99).
5. Inventory: set a quantity (worked example transcribed as "$100" — read as 100 units; the dollar sign appears to be a transcription error, not a real setting, since Shopify inventory is a unit count `[verify UI]`).
6. Shipping: can be adjusted per product now, but is mainly configured later at the store level (see procedure F).
7. Variants: toggle on if applicable, e.g. "Size" with options Small, Medium, Large, XL (worked example: t-shirts). Variant-level price, inventory and images can be set individually.
8. Category metafields and SEO fields: left at Shopify defaults in this walkthrough — the source calls these not required for a first build.
9. Collections: on the product page, Add collections > Add new collection. Set a title (worked example: "T-Shirts"), set collection type to **manual**, optionally add a collection image, click Done, then Save on the product.
10. Repeat for every product (worked example used 3 products total). Save.

### D. Gather and organize the inspiration folder
1. In Shopify admin, go to Online Store to see the current (empty) theme — in this source, the **Horizon** theme `[web check: current default theme name]`.
2. Browse the Shopify theme store's demo pages (Online Store page > "visit theme store" > pick a theme > "View demo"). Screenshot individual sections you like across as many themes as you want to mix and match: hero, product display, collection page, product page, reviews, story, etc.
3. On your computer, create separate folders for: product photos, store inspiration screenshots, logo (the source recommends a background version plus transparent dark and light versions — presenter made the logo in Canva), and homepage/lifestyle images (stock, AI-generated, or your own photos; presenter used Pexels).
4. Folder structure does not have to match the presenter's; the requirement is that every reference asset is reachable in one place before the agent starts.

### E. Connect Claude Code to the live theme and brief it
1. In the terminal, if Claude Code is open, type `/exit` to return to the plain terminal.
2. Create and enter a fresh project folder: `mkdir my-store-build` then `cd my-store-build`.
3. Copy the store's domain from Shopify admin > Settings (top of page).
4. Run `shopify theme pull --store [your-store-domain] --live`.
5. Complete the browser login prompt for the Shopify account; confirm the device using the code shown in the terminal.
6. Wait for the "theme [name] has been pulled successfully" message — the live theme is now local and editable.
7. The source says to then "paste in the next command" to give Claude general Shopify domain knowledge, and refers to "the guide" for the exact command — **the command itself is not given in this transcript**. This is a real gap; do not invent it.
8. Create the inspiration folder inside the project: `mkdir inspiration`.
9. Open the folder in the OS file browser: `explorer .` (Windows-specific; Mac equivalent not given in source). Copy in everything from the separately organized asset folder from procedure D (product photos, screenshots, logo, homepage images) directly into `inspiration`.
10. Launch Claude Code from inside the project folder: run `claude`. Step through onboarding prompts (press Enter through defaults); when asked about the Claude-in-Chrome extension, the presenter declines ("no, we won't need it") — optional either way.

### F. Brief and build the homepage, section by section
1. Send an initial prompt that gives Claude instructions/guidelines for the build. The source states this exact prompt text lives in "the guide linked in the description," and is **not reproduced in this transcript** — do not invent it; note that a placeholder brand name must be swapped for your real brand name if pulled from that guide.
2. Claude reads the theme and inspiration folder, then asks clarifying questions. In the worked example, it flagged a mismatch — the theme-derived mockups it was given were "loud" (blue/yellow) while the presenter's own logo and product photography were "clean and neutral" — and asked which direction to build in. Answer format: multiple-choice options via arrow keys/Enter.
3. It asks which homepage sections to include (worked example selected in order: Hero, Shop by Category, Featured Products, Customer Reviews, Our Story), then which fonts to use (worked example: kept the existing "Inter" font).
4. It asks how to preview each section as it builds: local dev server, unpublished preview theme, or static mockups. The source recommends the **local dev server** ("private live preview... only you can see it... updates on its own as Claude builds").
5. Approve the plan. Expect a request for your Shopify URL and a confirmation that it will build one section (the hero) first, then pause for review before continuing. Provide the URL and reply approving the first section only, e.g. "go ahead with building the first section."
6. During generation, approve command-permission prompts as they appear; the source recommends "Yes, and don't ask again" for a specific repeated permission, but also separately warns not to approve blindly — read what is about to run. [see mistakes]
7. To view the built section: open a second terminal tab, `cd my-store-build`, paste in the preview command Claude prints, then supply the **store password** (not the Shopify account password) — found in Shopify admin > Online Store > Edit password. Paste the resulting preview link into a browser.
8. Review the section in the live-updating preview. Give plain-English feedback per section, worked examples from the source:
   - Hero: "I think the hero section looks great. I'd like the text, images and sections to have a clean easing animation when they appear on the website. Right now, everything loads in very quickly and doesn't look very polished." After the change, refresh to check; further tune speed/stagger timing if needed.
   - Approve and advance: "This looks great. Go ahead and build the next section in the same style."
   - Category section: "This new section looks great, but the icons don't match the category. Give this section a quality check."
   - Featured Products: explicitly remind the agent the store already has real products — "My store already has three products within it. For the featured products section, make sure you actually use the three real products." (Needed because otherwise the agent may not know to pull real catalog data.)
   - Advance again: "Looks great. Let's move to the final section." (In the worked run, this single step generated **both** the Customer Reviews and Our Story sections together — reviews used placeholder names/text/images to be replaced later.)
9. Once every section exists, run one final polish pass: "All of the sections look great. Do one last pass for quality and make any potential improvements so the store looks as polished and professional as possible."
10. Batch remaining smaller fixes into a single prompt once the homepage itself is accepted — worked example: "There's a few more things I need you to do. First, create polished product pages for my three products. Polish my store's header and make sure it includes my logo. Create a footer at the bottom of my store that includes my policy links. And overall, polish the rest of the store aside from the homepage."
11. Iterate again in plain English on specific results, worked examples: "All changes look good. I think I want to remove the banner at the top... Also for home, catalogue and contact, let's move those into a hamburger menu."

### G. Push to Shopify and finish manually
1. Tell Claude you are ready to publish to the live theme: "I'm ready to publish this to my live theme." It returns a command to run in the preview terminal.
2. In the preview terminal: Ctrl+C to stop the running preview, paste the returned command, press Enter. This uploads the theme to Shopify **without publishing it** — you can still edit manually before going live.
3. In Shopify admin: Online Store > find the uploaded theme > "Edit theme" to open Shopify's native visual editor.
4. Manual edits work exactly like any other Shopify theme: click into a section to edit text/images, drag sections in the left panel to reorder (this changes homepage layout — review after each move), use the "+" between sections to add new ones, undo via the top-right control.
5. Check mobile: click the mobile-phone icon in the editor and review every page/section on mobile as well as desktop before saving. Click Save.

### H. Back-office settings (can be done before or after the visual build)
1. Settings > general: set the store name (worked example: "Metics Fashion Store"). Save.
2. Settings > Payments: complete Shopify Payments setup (described as quick, a few minutes) so the store can actually get paid.
3. Settings > Shipping and delivery: open the shipping profile.
   - Delete unused rate options (worked example: deleted "Express").
   - Edit the standard rate: rename to "Free Shipping," turn on the free-shipping toggle, set a minimum order amount (worked example: $10), set the transit time you will actually honor (worked example: 5-8 business days). Click Done.
   - International zones: configure deliberately, or delete the zone entirely if not shipping internationally (worked example: kept only a US free-shipping zone).
   - Save.
4. Settings > Taxes and duties: confirm the Shopify tax service is active and set the regions to collect tax in (worked example: US only). Consult a tax professional if unsure.
5. Settings > Policies: for each policy with a template (Refund/Return, Privacy, Terms of Service): open it, click "Insert template," scan for and replace placeholders (worked example: replace an "[insert return address]" placeholder with the real address), then Publish.
6. Shipping policy has **no template** — write it yourself or ask an AI, giving it your exact shipping rules and regions; paste the result in and Publish.
7. Legal notice: the source says most businesses don't need to fill this in, but to consult a professional if unsure.
8. Recheck the theme footer after policies are published — footer policy links only appear once the policies exist in admin (see Principle 6).
9. Settings > Domains: connect an existing domain, or "Buy new domain" (worked example: priced a `.com` at about $16/year). `[web check: current Shopify domain pricing]`
10. Return to Online Store > Edit theme, scroll to confirm policy pages now show, then Publish > Publish, then click "Remove password" to open the store to the public. Use "View store" to confirm the published theme matches what was built.

## 4. Rules, thresholds and numbers

| Rule / setting | Number or threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Shopify trial deal | 3 days free, then $1/month for 3 months | Presenter's affiliate link only, cancel anytime | Promotional offer, point-in-time | none (transcript body) |
| Plan recommendation | Shopify "Basic" plan | For stores just starting out | Presenter's opinion | none |
| Claude plan required | Pro, ~$20/month | Pro is required because it includes Claude Code | Presenter's claim about product bundling | none |
| Node install option | "Tools for native modules" left unchecked | For this Claude Code + Shopify CLI workflow specifically | Presenter says not needed here | [3982a5a8da7a] |
| CLI install command | `npm install -g @shopify/cli@latest` | Run once, in PowerShell/Terminal | Direct instruction | [3982a5a8da7a] |
| Claude Code install (Windows) | `irm https://claude.ai/install.ps1 \| iex` | Windows only; Mac command not given in source | Direct instruction | [3982a5a8da7a] |
| Worked product price | $19.99 | One example t-shirt | Presenter's demo, not a benchmark | [5a0b9ad6456f] |
| Worked inventory qty | "100" (transcribed as "$100," likely a units count) | One example product | Presenter's demo | [5a0b9ad6456f] |
| Variant set | Size: S / M / L / XL | Apparel example only | Presenter's demo | [5a0b9ad6456f] |
| Free shipping minimum | $10 order minimum | Presenter's example, "for most stores" | Opinion, not margin-based analysis | [a3ff8ef93a56] |
| Transit time | 5-8 business days | Presenter's example; must reflect real fulfillment capability | Opinion/example | [a3ff8ef93a56] |
| Domain price | ~$16/year for a `.com` | One example TLD/registrar at time of recording | Point-in-time pricing, varies | [4ad69ffecb22] |
| Products before build | At least the store's real product count (example: 3) | Needed before Featured Products / PDP generation makes sense | Direct instruction, repeated to the agent | [5a0b9ad6456f], [4d8bf77b16e5] |

## 5. Diagnostics and checks

- Check: did `shopify version` return a number after CLI install? Good: a version string. Bad: no output/error. Fix: reinstall Node/Git first, since Shopify CLI depends on them; re-run the install command. `[3982a5a8da7a]`
- Check: after `shopify theme pull ... --live`, did the terminal show "pulled successfully"? Good: message appears, theme files exist locally. Bad: login/device-confirmation step not completed. Fix: complete the browser login and device-code confirmation, then retry. `[401b6d077401]`
- Check: does the preview link ask for a password you don't have? This is the **store password** (Online Store > Edit password in admin), not your Shopify account password. Mixing these up is the source's explicitly called-out point of confusion. `[e27f52047618]`
- Check: after building the Featured Products section, does it show real catalog products or placeholders? If placeholders, the agent likely wasn't told the store already has real products — explicitly tell it the count and to use them. `[4d8bf77b16e5]`
- Check: does the icon set in a generated section actually match its labeled category? If not, ask for an explicit "quality check" on that section rather than accepting it. `[4d8bf77b16e5]`
- Check: after policies are published, does the footer actually show the policy links? If not yet, confirm the policies exist and are published in Settings > Policies; footer links depend on that. `[dd3f3bb627c7]`
- Check: does the storefront look right on mobile, not just desktop? Use the mobile icon in the theme editor and step through every page before publishing. `[d23a4cb7706c]`

## 6. Tools, settings and named features

- **Node.js** (nodejs.org): background runtime the other tools need; installed once, never interacted with directly. `[verify UI]`
- **Git** (git-scm.com): helper dependency required by the Shopify CLI. `[verify UI]`
- **Shopify CLI** (`@shopify/cli`, npm global package): bridges the local machine and the live Shopify store; used for `theme pull` and later theme push/publish commands. `[verify UI]`
- **Claude Code**: the AI coding agent that reads and edits the pulled theme files, installed via a platform-specific script and run from the terminal (`claude` command) inside the project folder. `[verify UI]`
- **Claude.ai account / Pro plan**: required subscription tier for Claude Code access, per the source. `[web check: current Claude plan structure]`
- **Claude desktop app**: optional separate chat client, not required for the CLI/theme workflow.
- **Claude-in-Chrome extension**: offered during Claude Code onboarding; declined in this walkthrough as unnecessary for this task.
- **Shopify Horizon theme**: the store's starting theme in this source (Shopify's theme at the time of recording). `[web check: current default theme]`
- **Shopify theme store / theme library**: browsed for visual inspiration, not for the theme actually installed.
- **Local dev server**: Shopify CLI's local preview mode, chosen over "unpublished preview theme" and "static mockups" for real-time, private review as Claude builds.
- **Canva**: used to create the store logo (background, transparent dark, transparent light versions).
- **Pexels**: free stock photo source used for homepage lifestyle images in this example.
- **ChatGPT**: named as one option (alongside your own camera or stock photos) for generating product photos — not used for the theme/code work itself in this source.
- **Shopify Payments**: native payment processor, set up in Settings > Payments.
- **Shopify tax service**: native tax calculation, confirmed/region-configured in Settings > Taxes and duties.
- **Shopify Policies templates**: built-in templates for Refund/Return, Privacy, Terms of Service; no template exists for Shipping Policy (write manually or with AI).
- **Shopify Domains**: connect an existing domain or buy a new one directly in Shopify Settings > Domains.

## 7. Examples and case results

- Example only, one demo store: "Metics Fashion Store," a t-shirt store, built live during the recording. Products: t-shirts with Size variants (S/M/L/XL), 3 products total, one priced at $19.99 with inventory example "100."
- Example homepage build order: Hero -> Shop by Category -> Featured Products -> Customer Reviews + Our Story (built together in the "final" pass) -> header/footer/PDP polish pass -> banner removal + hamburger-menu nav change.
- Example shipping config: Free Shipping, $10 minimum order, 5-8 business day transit, US-only (deleted international zone).
- Example domain: `meticsfashionstore.com` quoted at about $16/year.
- No conversion rates, traffic, revenue or before/after sales numbers are given anywhere in the source. This is a build-process demo, not a performance case study.

## 8. Mistakes the source warns about

- Do not confuse the Shopify **account** password with the **store** password used for the private preview link; they are found in different places and are not interchangeable. `[e27f52047618]`
- Do not approve every AI command-permission prompt blindly; read what is about to run even while using "don't ask again" for routine repeats. `[13e82e14fdd0]`
- Do not skip adding real products/collections before asking the agent to build the homepage or product pages — the Featured Products section and PDPs are built around what already exists in the catalog; the source has to explicitly remind the agent of the real product count mid-build. `[5a0b9ad6456f]`, `[4d8bf77b16e5]`
- Do not jump straight to "build the whole store" in one prompt; the source frames the interview-then-section-by-section approach as what prevents mismatched output (their claim, not measured). `[13e82e14fdd0]`
- Do not forget that footer policy links stay invisible until the policies are actually created and published in Shopify admin, even after the footer itself exists. `[dd3f3bb627c7]`
- Do not publish templated legal/policy pages without reading them for placeholder text (worked example: an unedited "insert return address" placeholder). `[dd3f3bb627c7]`
- Do not treat the reordering of homepage sections in the visual editor as risk-free; each reorder changes the whole homepage layout and should be reviewed immediately after. `[d23a4cb7706c]`

## 9. Caveats, conflicts and what is missing

- This source is a sponsored tutorial with an affiliate offer baked into step 1; the "special deal" numbers ($1/month for 3 months) are promotional and not a general Shopify price. `[web check: real current Shopify pricing]`
- Two concrete artifacts the source repeatedly relies on are **not actually included in this transcript**: (1) the exact command to give Claude "knowledge of how Shopify works" after the theme pull, and (2) the exact initial kickoff prompt used to start the interview-then-build flow. Both are pushed to an external "guide... linked in the description," which is outside this source. Any playbook built from this source alone must flag these as unresolved gaps rather than inventing prompt text.
- The Mac-specific Claude Code install command is likewise referenced but never stated (only the Windows PowerShell command is given verbatim).
- No security guidance is given about approving AI-run terminal commands beyond "read what it's about to run" — no allowlist, no sandboxing advice, no mention of testing on a duplicate/staging theme before pulling `--live` directly. This is a gap relative to more cautious dev practice (pulling a live theme, editing locally, and pushing straight back onto the same live theme, is a real production system, not a staging clone).
- The $10 free-shipping minimum and 5-8 day transit time are stated as the presenter's personal example ("for most stores"), not derived from margin, carrier cost or customer data — a brand should not copy these without checking its own numbers. `[needs brand data: shipping cost per order, carrier transit times, margin per SKU]`
- No claims are made about conversion lift, SEO, or sales performance of the AI-built theme versus a manually built or paid-theme store. Nothing here should be read as evidence that AI-built themes convert as well as (or better than) alternatives.
- The workflow directly modifies the **live** theme's pulled copy and later uploads back into the same store (unpublished, then published) — there is no branch/staging-theme step described, unlike common Shopify dev practice of using a duplicate theme for changes. This is worth flagging as a conflict with more conservative theme-development advice, though the source does keep changes unpublished until final review.
- Brand-specific facts needed to actually execute this (not given by the source, since it is a generic template): `[needs brand data: real product catalog, pricing, inventory counts, shipping rates and destinations, tax nexus, return address, actual homepage section choices, brand name/logo, domain choice]`.

## 10. Card index

- [3982a5a8da7a] Install Node, Git and Shopify CLI before AI-assisted theme work
- [401b6d077401] Pull the live theme locally so the AI can edit real code
- [5a0b9ad6456f] Add products and collections before generating the store
- [66e36f527ce2] Organise a local asset folder as the AI's design brief
- [13e82e14fdd0] Prompt the AI to interview you before it builds
- [4d8bf77b16e5] Build the homepage section by section in plain English
- [e27f52047618] Preview changes privately on a local dev server
- [5fa9ccc816ec] Use easing and scroll animations to soften load friction
- [d23a4cb7706c] Push the AI-built theme, then keep editing it in Shopify
- [a3ff8ef93a56] Configure shipping zones, free-shipping thresholds and taxes
- [dd3f3bb627c7] Generate policy pages from templates and AI, then publish
- [4ad69ffecb22] Connect a custom domain and go live
