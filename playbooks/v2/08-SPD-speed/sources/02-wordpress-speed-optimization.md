# WordPress Speed Optimization: Improve Your Website Performance and Make It Faster (Step-By-Step)

source_id: 1xw38NANCmS8DmKTMRPULxChkXGSPApKH  |  folder: /08-SPD-speed  |  cards: 17  |  words: 6521  |  type: transcript (YouTube tutorial)
credibility: Presenter named Elijah. Channel and employer are not named in the text. He builds with the Oxygen site builder and hosts on a cheap Cloudways plan; both are named but the source curator marked them as promotional context to skip. Evidence is 1 live demo on 1 image-heavy landing page, with before and after scores from PageSpeed Insights, GTmetrix and Gift of Speed plus a visual slow-4G test. No client data, no studies.
date signals: No year given. Names AVIF as having "really good browser support" now and WebP as "popular a while ago". PageSpeed Insights section called "Render-blocking requests". WordPress tools named: Oxygen, WP Codebox, Asset CleanUp, Breeze (Cloudways cache plugin), ShortPixel, Imagify. The file was added to the library in Sep 2026.

## 1. What this source is for

Use it to run a hands-on speed pass on a WordPress (and WooCommerce) landing page or storefront page without buying a speed plugin. It gives a 7-step order: image loading attribute, image width and height, image format and size, unloading unused scripts and styles, removing WordPress defaults, local fonts, then caching and compression. It also gives a way to judge results by how the page looks loading on a slow connection, not only by scores.

## 2. Principles

1. **Perceived performance on slow connections is the main measure, not tool scores.** Condition: applies when judging whether a page is fast enough for real shoppers. The source says PageSpeed Insights, GTmetrix and Gift of Speed scores "are not the best way to determine if the performance is good enough". Evidence: the demo page looked like "a mess" on slow 4G (slow start, layout jumps, images loading in chunks) and that is what the fixes targeted. This is the presenter's opinion; his fixes also raised every score. [29d73beaf348] [21b1708d102a]
2. **Fix fundamentals before caching, compression and a CDN.** Condition: when planning the order of a speed project. The source calls caching and compression "essentially just a band-aid if you don't take care of some of the core issues". Evidence: the demo reached GTmetrix 98% performance, LCP 1 second and CLS 0 with no gzip, no cache and no CDN turned on. The source also says "your mileage may vary depending on your site builder and hosting". [1b50d0611dc3] [55f9847e6f0a]
3. **Do not game scores with a plugin trick.** Condition: always. The source explicitly is "not a tutorial on one specific performance plugin to game PageSpeed Insights and GTmetrix scores". It favors fundamentals because they also improve the real loading experience. [1b50d0611dc3]
4. **Images above the fold load eagerly; images below the fold load lazily.** Condition: applies to `<img>` elements only. It does not apply to CSS background images. Set `eager` explicitly even though it is the browser default, so a later optimization plugin cannot lazy-load it by accident. Evidence: the demo logo was set to lazy by default, which the presenter calls wrong for any above-fold image. [eeb9c51fe0da] [08e530e7d0b2]
5. **Explicit width and height stop image layout shift.** Condition: images and videos that are in the normal page flow. Absolutely positioned images likely do not affect CLS, but the presenter adds dimensions anyway as good practice. Evidence: CLS moved from red to green after the loading attribute and dimension changes; desktop score reached the 90s after these 2 changes. [f597983f8e66]
6. **Resize images to 2x their rendered size, not to the rendered size and not the original.** Condition: content images. Reason: high-density (retina) screens need more pixels. It does not apply to background images that must cover a section; those keep their size and only change format. [b783c30c2217] [f50e2bf2a5c4] [08e530e7d0b2]
7. **AVIF is the preferred image format; WebP is an acceptable alternative.** Condition: when converting images. Source's basis: AVIF compresses better while keeping quality, supports transparency like PNG, and has good browser support. WebP is more efficient than PNG or JPG and has good support. [f50e2bf2a5c4]
8. **Unload assets a page does not use.** Condition: when a page loads scripts or styles for features it does not have (jQuery nobody uses, WooCommerce cart files on a page with no cart). Keep global assets that are needed everywhere. Be conservative. [701c087d0917] [44c02380f01e] [0d00d9d01688]
9. **Serve Google Fonts locally as WOFF2.** Condition: when fonts load from Google's servers. The source says "you can get some performance gains" this way; no number given for the font step alone. [731928d47c17]
10. **Scores fluctuate between runs; average several runs.** Condition: when gathering data for a report or comparison. Evidence: PSI dropped slightly on the final run after more fixes, while GTmetrix hit 100%. [21b1708d102a]
11. **Use the image pass to add alt text.** Condition: every meaningful image gets descriptive alt text; decorative images get an empty alt. Presenter says alt text helps accessibility and "makes your scores look a little bit nicer" in PSI. [876fb6014fe1]

## 3. Procedures

### 3.1 Test perceived performance (before and after every stage)
1. Open Chrome DevTools, Network tab. [verify UI]
2. Change the throttling dropdown from "No throttling" to "Slow 4G" (presenter's default) or "3G". Pick the one most common for your visitors. Fast 4G exists but use a slower option for performance testing. [verify UI] [needs brand data: visitor connection mix]
3. Tick "Disable cache" so assets are not served from browser memory. [verify UI]
4. Reload. Watch time until anything appears, layout jumps, and images revealing in chunks ("scanning effect").
5. Repeat after each stage so you can attribute the gain. [29d73beaf348] [1b50d0611dc3]

### 3.2 Set the image loading attribute
1. List images visible on first load: hero, any decorative image behind it, logo.
2. Add attribute `loading` = `eager` to each. In Oxygen: element Settings (gear) > Properties panel > add attribute. [verify UI]
3. Add `loading` = `lazy` to every image below the fold, including a repeated footer logo.
4. To speed up: right-click the settings gear > Copy settings, then Paste settings on the next image. [verify UI]
5. After pasting, re-add any alt text the paste overwrote. Decorative images get an empty `alt`.
6. Background images cannot use this attribute; handle them in 3.4. [eeb9c51fe0da] [876fb6014fe1] [08e530e7d0b2]

### 3.3 Add width and height to stop CLS
1. On the live page, right-click the image > Inspect.
2. In the image tag, hover the `src` URL. Read the rendered size (example: logo 256x106).
3. In the builder, add attribute `width` = rendered width and `height` = rendered height. No "px" unit.
4. Repeat for every image. Priority is images not absolutely positioned (example: 398x597 main image). Examples from the demo: background 1440x810, a set of logos 198x64 (copy and paste settings across the set), shoes image 800x1000.
5. Save and retest in PageSpeed Insights. Check CLS is green. [f597983f8e66]

### 3.4 Resize and convert image files (free manual method)
1. Inspect the image and hover the `src`. Read rendered size, intrinsic size and file size. Demo: rendered 398x597, intrinsic 1770x2560 (transcript says "1,77"), 161 KB.
2. If intrinsic is far larger than rendered, there is waste.
3. Open the image URL in a new tab and copy the image.
4. Open Photopea (browser editor, no account needed) and paste. [verify UI]
5. File > Export as > More > AVIF. [verify UI]
6. Set width to 2x rendered width (demo: 796). Height follows the aspect ratio (demo: 1194).
7. Leave quality at 50%. Presenter says the difference is "pretty much imperceptible" in his tests.
8. Check the preview file size (demo: about 10 KB), save, and replace the image on the page (arrived at about 11 KB vs 157 KB original).
9. Add alt text while replacing.
10. For background images that must cover a section: do not resize; convert to AVIF only.
11. Alternatives: ShortPixel or Imagify automate this but "typically that's going to cost some money". The WordPress media library can resize (Edit image > Scale) but does not give AVIF or WebP savings. [verify UI] [f50e2bf2a5c4] [b783c30c2217] [08e530e7d0b2]
12. Re-run the slow-4G test. Expected pattern from the demo: main image appears at once; background image arrives later but appears all at once.

### 3.5 Find unneeded assets
1. In PageSpeed Insights, open "Render-blocking requests". [verify UI]
2. For the full list, open the GTmetrix waterfall chart. It shows everything that loaded. [verify UI]
3. Mark items the page does not use. Demo finds: jQuery (site does not use it), WooCommerce CSS, add-to-cart script (no cart on the page), builder entrance animations, fonts loading from Google.
4. Split into global (needed everywhere) and page-specific (safe to unload here). [701c087d0917]

### 3.6 Remove default WordPress bloat (site-wide)
1. Open theme or builder performance settings. Demo: Oxygen > Settings > Performance. [verify UI]
2. Tick what you do not use: Gutenberg block CSS (only if you do not use Gutenberg), disable emojis, disable dashicons for logged-out users, remove and disable pingbacks.
3. Skip any toggle tied to a feature you use.
4. Save and recheck the waterfall. [83d6ff4a133c]

### 3.7 Dequeue jQuery for logged-out visitors
1. Confirm in the waterfall that jQuery and jQuery Migrate load on the public page.
2. Create a snippet (demo uses WP Codebox) with a filter on `wp_enqueue_scripts` that dequeues and deregisters jQuery. This removes jQuery, jQuery Migrate and dependencies. The source does not print the code.
3. Add conditions: location = front end AND user logged-in status = not logged in. Logged-in users need jQuery for the WordPress admin bar. [verify UI]
4. Enable and recheck the waterfall.
5. Only do this if the theme and plugins do not need jQuery on the front end. [0d00d9d01688]

### 3.8 Unload WooCommerce assets on one page with Asset CleanUp
1. Install Asset CleanUp (free, WordPress repository). [verify UI]
2. Pages > open the landing page. A new metabox lists loaded files by source. Demo: WooCommerce group with 13 files.
3. Unload what the page does not use. Demo unloaded: brand styles, sourcebuster, add-to-cart, block styles CSS, jQuery block UI and the rest of WooCommerce. Kept: WooCommerce "coming soon" CSS, because it is small and he was not sure it was unneeded.
4. Save. The unload applies only to that page.
5. Write down what you unloaded. If you later add a WooCommerce feature such as a mini cart, re-enable those files. [44c02380f01e]

### 3.9 Load Google Fonts locally
1. Find the fonts on fonts.google.com (demo: Inter, Libre Baskerville).
2. Get WOFF2 files. Downloads from Google come as TTF. Tools: Font Squirrel Webfont Generator (failed on some fonts for the presenter, possibly variable fonts) or Google Web Fonts Helper (recommended; pick styles and weights, download WOFF2). [verify UI]
3. Upload as custom fonts in the builder or theme. Demo: Oxygen logo > Preferences > Custom Fonts > add font, add each WOFF2 file, set weight (example 900) and style (italic or normal). If the theme has no upload, use a custom-font plugin from the repository. [verify UI]
4. Name them clearly, for example "Inter Local".
5. Switch body and heading font variables to the local versions. With variables, one change updates the whole site.
6. Rerun GTmetrix and check the Google font requests are gone. [731928d47c17]

### 3.10 Check and enable caching and compression
1. DevTools > Network. Tick "Preserve log". No throttle needed. Reload. [verify UI]
2. Select the first (document) request. Read response headers.
3. Caching on: a cache header such as `x-cache: hit`. Do not rely on `cache-control` (demo showed `no-cache, must-revalidate`).
4. Compression on: `content-encoding: gzip` (or your host's method).
5. Turn on compression and caching at the host. Demo: server settings on Cloudways plus the Breeze plugin. [verify UI]
6. Re-verify in an incognito window with "Disable cache" unticked. [55f9847e6f0a]
7. Optional: add a CDN "as a bonus". [1b50d0611dc3]

### 3.11 Final before and after comparison
1. Incognito window, slow 4G, "Disable cache" ticked.
2. Load an unoptimized copy of the page. Note shifts and slow images.
3. Load the optimized page. Compare how soon it is usable and whether layout holds.
4. Remember global fixes (local fonts, removed bloat) also apply to the copy, so the gap shows only page-level work.
5. Untick "Disable cache" and reload for the typical repeat-visit case. Demo: looked fully loaded in 782 ms, transferring 547 bytes. On 3G with cache, disk-cached assets hid most remaining issues. [15b41de4c239]

### 3.12 Checklist (source's own summary)
1. Lazy-load below-fold images; do not lazy-load above-fold images.
2. Fixed width and height on above-fold images.
3. Optimize and resize images; AVIF or WebP.
4. Unload unneeded scripts and styles, including jQuery if unused.
5. Remove WordPress bloat (emojis, Gutenberg block CSS).
6. Load Google Fonts locally.
7. Enable caching and compression.
8. Bonus: CDN. [514d616ab421]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Throttle for perceived-speed tests | Slow 4G (or 3G) | choose the slowest common visitor connection | presenter's practice | [29d73beaf348] |
| Export size for content images | 2x rendered size (398x597 > 796x1194) | not for cover background images | retina screens | [b783c30c2217] |
| AVIF export quality | 50% | presenter's tests found it imperceptible | own tests | [f50e2bf2a5c4] |
| Image file savings (example) | 161 KB to about 10 to 11 KB | 1 image in demo | case result | [f50e2bf2a5c4] |
| width/height attribute unit | no unit, number only | HTML attributes | demo | [f597983f8e66] |
| Font file format | WOFF2 | local web fonts in WordPress | demo | [731928d47c17] |
| Cache check header | `x-cache: hit` (example) | header name depends on host | demo | [55f9847e6f0a] |
| Compression check header | `content-encoding: gzip` | or host's method | demo | [55f9847e6f0a] |
| Score noise | run several times and average | reports and comparisons | PSI moved down on a rerun | [21b1708d102a] |
| WooCommerce files on landing page | 13 files in 1 group | demo site | case | [44c02380f01e] |

## 5. Diagnostics and checks

| check | how | good | bad | next |
|---|---|---|---|---|
| Real loading feel | DevTools, slow 4G, cache disabled, reload | main content appears fast, no jumps, images pop in whole | long blank wait, layout jumps, images scan in chunks | work through 3.2 to 3.9 |
| Above-fold images lazy? | inspect `loading` attribute on hero and logo | `eager` | `lazy` (demo logo was lazy by default) | set eager |
| CLS | PSI CLS metric | green (demo reached 0) | red | add width and height (3.3); note other shift sources exist |
| Oversized image | hover `src`: rendered vs intrinsic size and KB | intrinsic about 2x rendered | intrinsic many times rendered (demo 1770x2560 for 398x597) | 3.4 |
| Unused assets | GTmetrix waterfall | only what the page uses | jQuery, WooCommerce cart files, block CSS on a page that does not use them | 3.6 to 3.8 |
| External font calls | waterfall | fonts from own domain | requests to Google Fonts | 3.9 |
| Caching and compression | response headers of document request | `x-cache: hit`, `content-encoding: gzip` | missing | enable at host (3.10) |
| Score trust | rerun each tool several times; compare PSI, GTmetrix, Gift of Speed | stable across runs and tools | single run, single tool | average; weight the slow-4G test higher |

## 6. Tools, settings and named features

- Chrome DevTools Network tab: throttling dropdown (No throttling, Fast 4G, Slow 4G, 3G), Disable cache, Preserve log, response headers, Inspect to read rendered and intrinsic image size. [verify UI]
- PageSpeed Insights: scores, CLS, "Render-blocking requests" list. [verify UI]
- GTmetrix: performance and structure scores, LCP, CLS, waterfall chart. [verify UI]
- Gift of Speed: third speed score used for cross-checking. [verify UI]
- Photopea: free browser image editor, no login; Export as AVIF with size and quality controls. [verify UI]
- ShortPixel, Imagify: paid automated image optimization (not demoed).
- WordPress media library: Edit image > Scale for resizing. [verify UI]
- Oxygen builder: attribute panel, copy and paste settings, Settings > Performance toggles, Preferences > Custom Fonts, font variables. [verify UI]
- WP Codebox: snippet manager with a condition builder (location, logged-in status). [verify UI]
- Asset CleanUp: free plugin, per-page metabox to unload files by plugin group. [verify UI]
- Font Squirrel Webfont Generator and Google Web Fonts Helper: TTF to WOFF2. [verify UI]
- Breeze: Cloudways cache management plugin. [verify UI]
- CDN: named as a bonus, no product named.

## 7. Examples and case results

All from 1 demo page; examples only, not promises.
- Start state: image-heavy Oxygen landing page on a cheap Cloudways plan, no gzip, no cache, no CDN. Scores were poor (numbers not read out).
- After loading attribute plus width and height: CLS green; desktop PSI "into the 90s".
- After image, asset and font work (still no cache or compression): GTmetrix 98% performance, 97% structure, LCP 1 second, CLS 0. PSI 95 mobile and 99 desktop performance, 100 on other categories (a figure of "71 overall" is also mentioned as the starting point of that run). Gift of Speed 99/100.
- After enabling gzip and cache: PSI slightly lower on one run; GTmetrix 100%; Gift of Speed 99.
- Cached repeat view: looked fully loaded in 782 ms with 547 bytes transferred.
- 1 image: 161 KB to about 11 KB.

## 8. Mistakes the source warns about

- Chasing a perfect PSI score instead of the real experience on slow connections. [29d73beaf348]
- Relying on caching, compression or a CDN before fixing heavy images and extra assets. [1b50d0611dc3]
- Leaving above-fold images (including the logo) set to lazy. [eeb9c51fe0da]
- Exporting images at the raw rendered size (soft on retina) or keeping huge originals. [b783c30c2217]
- Overwriting alt text when pasting element settings. [876fb6014fe1]
- Removing jQuery for logged-in users (breaks the admin bar). [0d00d9d01688]
- Forgetting what you unloaded, then adding a cart feature that needs those files. [44c02380f01e]
- Reading `cache-control` as proof of caching. [55f9847e6f0a]
- Trusting 1 test run; scores move between runs. [21b1708d102a]
- Treating a cache-disabled test as the typical user; it is the worst case. [15b41de4c239]

## 9. Caveats, conflicts and what is missing

- Scope is 1 landing page with no live cart, not a full WooCommerce catalog. Product pages, cart and checkout are not covered.
- The jQuery snippet code is described but not shown. Hook name `wp_enqueue_scripts` is from the transcript; verify against WordPress docs. [0d00d9d01688]
- The 2x rule is a practical rule of thumb from the presenter, not a standard. [b783c30c2217]
- The 50% quality setting is based on the presenter's eye only.
- Width and height fix only image-caused shift. Ads, injected content and web fonts can still shift layout; the source does not cover those (card caveat). [f597983f8e66]
- No numbers for the font step or the bloat-removal step alone.
- The source does not cover field data (Chrome UX Report), INP, third-party apps, or video.
- Oxygen and Cloudways are the presenter's own stack; the principles are said to be builder-neutral but the UI steps are not.
- Conflict to keep for the folder: this source ranks slow-4G visual tests above tool scores. Other speed sources in this folder may lean on PSI or Core Web Vitals thresholds as targets.

## 10. Card index

- [29d73beaf348] Measure Perceived Performance With Slow-4G Throttling
- [eeb9c51fe0da] Set loading=eager Above the Fold and lazy Below
- [f597983f8e66] Fix CLS With Explicit Width and Height Attributes
- [f50e2bf2a5c4] Convert and Resize Images With AVIF at 2x Rendered Size
- [701c087d0917] Audit Loaded Assets With a Waterfall Chart
- [0d00d9d01688] Dequeue jQuery for Logged-Out Front-End Users
- [44c02380f01e] Unload Unused WooCommerce Assets Per Page With Asset CleanUp
- [83d6ff4a133c] Unload Default WordPress Bloat for Logged-Out Users
- [731928d47c17] Self-Host Google Fonts as WOFF2 to Cut External Requests
- [55f9847e6f0a] Verify Caching and Compression via Response Headers
- [1b50d0611dc3] Sequence WordPress Speed Work: Fundamentals Before Caching
- [21b1708d102a] Interpret Waffling Speed Test Scores and Average Runs
- [514d616ab421] Apply the WordPress Speed Optimization Checklist
- [15b41de4c239] Compare Optimized vs Unoptimized Page Under Throttling
- [08e530e7d0b2] Do Not Lazy-Load Background Images; Optimize Them Instead
- [b783c30c2217] Resize Images to 2x Rendered Size for Retina
- [876fb6014fe1] Add Alt Text and Preserve It When Copying Image Settings
