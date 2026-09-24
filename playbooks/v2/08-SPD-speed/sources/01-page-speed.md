# Page speed (Shopify speed optimization video compilation)

source_id: 1sDLOi4dG3ZYPrmTdOL6BbCrjMwr-hLrw  |  folder: /08-SPD-speed  |  cards: 129  |  words: 59,341  |  type: transcript (about 19 YouTube video transcripts joined into one document, auto-captioned, no timestamps)

credibility: One presenter across all videos: "Christian" (also "Chris"), a freelance Shopify developer who says he has worked on Shopify for 8, 10 or 12 years depending on the video. He sells a Shopify speed optimization course, paid code snippets (a "speed boost" snippet that delays app scripts, a cookie banner lazy-load snippet), a done-for-you speed service (site name transcribed as shopioso.com, tropioso.com and shops.com) and a paid community ("Shopify Success Circle"). He gives affiliate links and a 35% discount code for 2 apps he recommends (Tiny SEO Speed and Image Optimizer, SEOAnt). Evidence is his own live demos on demo stores, single-store PageSpeed and Lighthouse runs, and recorded reviews of client and community-member stores. No controlled tests, no conversion data, no revenue data. Two claims cite unnamed "studies" (8-second attention span). Treat numbers as one practitioner's working rules and single-store examples.

date signals: Shopify Horizon theme is at version 1.0.1 and launched with "10 more free themes with the summer editions this year" [web check: Horizon release date, likely 2025]. Dawn-based themes at version 15.3.0 (captioned "153.0" and "1.5.3.0"); source says Shopify "stopped releasing updates [to Dawn] earlier this year". Mentions the "new code editor" in Shopify admin, which now flags script tags missing defer or async. Mentions Shopify Sidekick, ChatGPT, Gemini and Nano Banana for AI lifestyle images, and the Cursor code editor. One older video uses the Shopify admin "speed score" (average of home, collection and product pages); a newer one shows the admin web performance view ("visual stability poor", "loading speed poor"). Core Web Vitals named: LCP and CLS only; "blocking time" is discussed; INP and FID are never named. Videos span several years, so UI steps differ between them.

## 1. What this source is for

It helps an operator speed up a Shopify storefront without a speed app, by editing the theme. It covers: app triage and residual code cleanup, deferring and delaying app scripts (including the content_for_header override), image sizing, format and compression, lazy loading versus preloading, fonts, non-critical CSS, finding and fixing CLS and LCP, testing method, theme choice (Dawn versus Horizon), and a full audit sequence. It also contains 1 long SEO video (keywords, titles, alt text, sitemap, SEOAnt app) and 1 product page layout review, which belong mostly to neighbour folders 15-SEO-search and 09-CRO-testing but are kept here so nothing is lost.

## 2. Principles

1. **Speed is judged by the slowest real shopper, not your desk.** Condition: always, and most for mobile traffic from ads. Shoppers use older phones on 3G or patchy mobile data; a store that looks fine on office Wi-Fi can show them a blank or half-loaded page. Evidence: presenter's own behaviour (he leaves if a site does not load in 2 to 3 seconds) and client experience; "studies say" adult attention span is about 8 seconds; many leave after 3 to 4 seconds; first impression forms in 0.05 seconds (50 ms) after load. None of these are sourced. [37d2f02ad647] [74187c8d7e19]
2. **Whether you need a high score depends on your traffic mix.** Condition: if you depend on or want Google organic traffic, the PageSpeed Insights score matters and you should fix the flagged items. If you drive all traffic with a large ad budget, a low score matters less; big brands with low scores still sell a lot. The shopper-experience case (bounce from ads) applies either way. If you have visits but no sales, speed is a candidate cause to test, not a proven one. [37d2f02ad647] [needs brand data: share of paid versus organic sessions]
3. **Load what is in view first, everything else later ("restaurant" order).** Condition: every page type. Serve drinks, then first course, then second course, then dessert; do not cook the whole menu and bring it at once. On a page: main styling, hero, logo and above-the-fold images first; app widgets, chat, rewards, pop-ups later. On a product page the product image and buy box come first. This is a heuristic; verify with Lighthouse or PageSpeed Insights. [ad877c2f348c] [5f44ccb5ead1]
4. **The 2 root causes of slow Shopify stores are layout stability (CLS, LCP) and apps.** Condition: presenter's experience over 10 years. Even a simple Dawn store with little customization gets issues, which he attributes mostly to apps. A large CLS or a large LCP alone blocks a good score. He ranks CLS as the most impactful, LCP second. On one example store he says fixing only these 2 would move the score "well over 50, maybe even 60". Qualitative ranking, not a Google weight. [7678b95c31ff] [f00068c50316] [37d2f02ad647]
5. **Every app must earn its place in money or user experience.** Condition: every installed app, sales-channel app and external script. Apps fetch assets from third-party servers, often before the main page elements, and some servers are slow. Apps also want their widget on screen as fast as possible so you keep paying. Keep an app only if you can state how it makes money (sizing chart for sized products, reviews for social proof). Prefer apps with many good reviews. Do not use an app for something the theme already does (announcement bar, discount code in cart). If unsure, uninstall; you can reinstall later. [8dbbb42b9c2e] [d675d594782b] [474204ae609c] [56315833a352] [needs brand data: installed app list and the revenue role of each]
6. **Uninstalling an app does not clean the theme.** Condition: after any uninstall, trial install or removed tracking. Apps can leave script tags, JS files, CSS files and rendered snippets that keep calling external servers on every page view. [3c6bd0cce957] [68699dfd59de] [fde546149035]
7. **"Unused JavaScript" means unused at test time, not useless.** Condition: when PageSpeed flags "reduce unused JavaScript". The script is not needed in the first seconds. The fix is to remove leftovers, then delay, defer or conditionally load what remains, not to edit app code line by line (you often cannot; app files live on app servers). [68699dfd59de] [adc3ea59042a] [9714159dd4aa]
8. **Most app widgets do not need to show at first paint.** Condition: widget not above the fold and not part of the buying flow (loyalty, chat, cookie banner, social feed, SMS pop-up). Delay their scripts to first user interaction. Exception: widgets that genuinely must show at load (for example review stars above the fold, per card caveat) and tracking pixels. [4e05290f17d5] [9714159dd4aa] [474204ae609c]
9. **Tracking pixels stay in the initial load (source rule, disputed).** The source says never defer tracking pixels (Facebook, Google) or measurement tools (Hotjar) because deferring can corrupt collected data. Two cards carry an editorial correction: this is not a universal rule; use Shopify's supported pixel integration (Web Pixels API and standard events) and verify each integration. See section 9. [15d23b16ff3c] [adc3ea59042a] [56315833a352] [ef51a42e0e16] [20821a7ae674]
10. **Images are among the heaviest assets and the part you control most.** Condition: always check images, and first if the theme is old, custom or agency-built, the catalog is large, mobile share is high, or the store is simple with few apps and still slow. Shopify helps (CDN, width variants, automatic WebP, light compression) but not enough. [21698bb77d52] [d84575512652] [needs brand data: mobile traffic share, theme age and who built it]
11. **Image count is not the problem; size and delivery timing are.** Condition: correct sizes served per screen and below-the-fold images lazy loaded. Then you can have "as many images as you want". [8e4f0dac7e97]
12. **Never lazy load what is in view; tell the browser it is important.** Condition: hero banner, first slide, logo, main product image, first card of a grid, anything visible without scrolling. LCP is the time to display the largest element in the viewport, usually the hero. Lazy loading, fade or slide effects, preloader bars and placeholders on that element all raise LCP. Use loading="eager", a preload link and high fetch priority instead. Source says Google penalizes lazy loading above the fold. [7a213481a9d2] [d56347d58c66] [b4735bb55b51] [51db910ccfc8]
13. **CLS is unexpected movement without user input.** Condition: during load and during scroll. A change after the user clicks is not CLS. If Google reports CLS, it is real, not a measurement error. Most CLS the presenter sees is either a CSS issue or an app widget that needs reserved space; apps are the main source in his experience. CLS also shows in Search Console Core Web Vitals and affects search performance. [d16d1fcdd349] [24893ea78676] [ba43a0aaa747] [f00068c50316]
14. **There is no quick fix, no magic app and no trustworthy shortcut.** Condition: when offered speed apps, caching scripts or speed specialists. Source says speed apps only work for returning users, if at all; some specialists use tricks that raise Google scores while real users still wait; Shopify already caches, so caching scripts add nothing. Expect many small changes across pages and templates. Opinion from experience. [5f44ccb5ead1] [cdc61c33e699] [23a3f294b81c]
15. **A simpler theme beats a feature-rich one unless the features pay.** Condition: new store or redesign. Premium themes ship libraries and options you will not use, and effects libraries delay display. Buy premium only when you know a feature will make money; not on a hunch or a video. [637495534f7f]
16. **Stores slow down as they mature.** Condition: ongoing. Source's illustration: a fresh store at 60 to 80 drops to 40 with apps, and to 20, 10 or lower with customization. LCP and CLS can be reintroduced by new sections, apps or careless development. Re-audit periodically. [474204ae609c] [d56347d58c66]
17. **Single speed tests are noisy; average several and wait between them.** Condition: every before and after comparison. Test servers can serve a cached older version, so an immediate retest can hide a real change. [079f8ea11444] [c33439a2c9b9] [9b3008487ad5]
18. **Passing Core Web Vitals does not mean a good score.** Condition: when the home page says "vitals passed". Check home, collection and product pages, since each loads different apps. [5e79bed9130e]
19. **Fix the page your ads land on first.** Condition: paid traffic. Ads usually send shoppers to the product page, which often has a large LCP even when the home page scores fine. Desktop is often already fine; focus on mobile. Do not over-invest in a home page that gets no traffic, but keep product page to home page cohesive. [1b9747314efd] [74187c8d7e19] [needs brand data: which pages ads land on]

## 3. Procedures

### 3.1 Testing protocol (run before and after every change)
1. Duplicate the live theme and test on its preview link. The preview link runs a bit slower than live, so compare preview to preview. [c33439a2c9b9]
2. Pick reference pages: home, a product page and a collection page (the 3 pages Shopify's admin score uses). For ad traffic, the product page matters most. [c33439a2c9b9] [9b3008487ad5]
3. Run Google PageSpeed Insights 3 times per page (the composite-score video says 3 to 4), leaving time between runs. Record each result in a text file or note. Average them. Example of variance given: 48, 51, 54 on the same page. [079f8ea11444] [9b3008487ad5]
4. Check both the mobile and the desktop tab. Mobile is usually the problem, but CLS can be zero on mobile and large on desktop. [f00068c50316]
5. Make one batch of changes. Wait about 1 minute (other videos say "a couple of minutes") before retesting, or you get the old score. [c33439a2c9b9] [d1007a68a9e0] [079f8ea11444]
6. Run 3 more tests, average, and compare averages, not single readings. Treat differences of a few points cautiously. [c33439a2c9b9]
7. Lighthouse in Chrome: right-click > Inspect > Lighthouse tab > Analyze page load. Scroll to the details to find render-blocking resources. [verify UI] [1dffb0dd47d1]
8. PageSpeed Insights historical (field) graphs cover the past 28 days, so a fix today takes up to 28 days to show there. Use lab results meanwhile. [0d2d3621b19d]
9. The Shopify admin score updates about every 12 to 24 hours and needs store traffic to update (presenter's observation). [verify UI] [9b3008487ad5] [web check: whether Shopify admin still shows a composite speed score or only the web performance report]
10. Search Console lags fixes by a couple of days (critical CSS video) or about 28 days for field CLS to reach zero (CLS client case). [ba43a0aaa747] [80a761efcb18]
11. Expect to spend most audit time waiting for tests. Be patient. Results that swing a lot usually mean many apps are loading. [079f8ea11444]
12. If Google's list runs out of actionable items, run the page on GTmetrix "or somewhere else". [9b3008487ad5]

### 3.2 See the store the way a slow-connection shopper does
1. Open the store on your phone on mobile data away from strong Wi-Fi (for example on a bus). [74187c8d7e19]
2. Or in Chrome DevTools: Network tab > tick Disable cache > Throttling: Fast 3G or Slow 3G > reload. [verify UI] [d16d1fcdd349] [1b9747314efd]
3. If 3G is still too fast to see movement, add a custom throttling profile (source used about 20 kilobits per second). If throttling seems not to apply, switch to another profile and back, then reload. [verify UI] [a5d2c3aee970]
4. Stop the page load when the suspect element appears, then inspect it mid-load. [a5d2c3aee970]
5. Optional: a third-party site that records a GIF of your page loading (not named). It may not register the same CLS Google reports. [a5d2c3aee970]
6. Optional: DevTools Performance tab > run a recording to get a loading profile and timeline. [verify UI] [d16d1fcdd349]
7. Mobile friendliness check: Chrome Inspect > device toolbar > pick a device (source used iPhone 12 Pro); Safari Develop > Enter Responsive Design Mode. Pass if text stays on screen, images are not shrunk or distorted, and everything is reachable. [verify UI] [58bc1e28be27]

### 3.3 App triage
1. List every installed app, sales-channel app and external script. For each, write the concrete revenue mechanism. [8dbbb42b9c2e] [474204ae609c]
2. No clear value to you or the customer: uninstall. Purely visual or no longer used: uninstall. [d675d594782b] [adc3ea59042a]
3. Before installing a new app, check reviews (many and good) and whether the theme already has the feature. [8dbbb42b9c2e]
4. Theme > Customize > App embeds: turn off every embed you do not actively use, then Save. After uninstalling, the embed should disappear; if it is still there and unused, turn it off. [verify UI] [d675d594782b] [4e05290f17d5]
5. Clean residual code (3.4 and 3.5). [3c6bd0cce957]
6. Re-test (3.1). [d675d594782b]

### 3.4 Remove residual app code inside Shopify's code editor
1. Online Store > Themes > Edit code. [verify UI] [8dbbb42b9c2e]
2. Use the search in the left panel. Search the app's brand name (example: "loox", captioned "locks"/"logs"). Also search its app store listing name when it differs (example: brand "Hexom", listing "free shipping bar"). [8dbbb42b9c2e] [3c6bd0cce957]
3. Check theme.liquid, head.liquid and footer.liquid at minimum. A Chrome extension named "Shopify Theme File Search" searches all theme files at once. [3c6bd0cce957] [fde546149035] [68699dfd59de]
4. Remove the leftover script tag, or comment it out: select it and press Cmd+/ (Ctrl+/) to wrap it in a Liquid comment. [8dbbb42b9c2e]
5. Also scroll through theme.liquid for script and pixel tags you do not recognize. Also remove old tracking pixels, unused custom fonts and style tags from plugins you stopped using. [8dbbb42b9c2e] [68699dfd59de]
6. To tell if a script belongs to an installed app: check Apps in admin, including apps listed as sales channels. If still unsure, ask whoever managed the store; it may be an external service not in the Shopify app store. [68699dfd59de]
7. Only remove code for apps you have actually uninstalled. Back up or duplicate the theme first. Save, check the store works, re-test after each removal so you can attribute changes. [3c6bd0cce957] [58c5589c135f]

### 3.5 Deep search in a downloaded theme
1. Online Store > Themes > (theme menu) > Download theme file. Shopify emails a link. Download and unzip. [verify UI] [10d064e032f8] [58c5589c135f]
2. Open the folder in a code editor (source uses Cursor, free, with built-in AI help for non-coders): File > Open Folder. [10d064e032f8]
3. Use global search for each app name, listing name, old pixel or provider name (example searches: "hexom", "logs", "Google"). A match can sit in a JSON file. [10d064e032f8] [58c5589c135f]
4. Note the file name and line (example: a pixel at line 72). [58c5589c135f]
5. Back in Shopify Edit code, open that file, go to that line, remove only the target tag, save, and verify the store. [58c5589c135f]
6. Re-download if you changed the theme since; the download is a snapshot. [10d064e032f8]

### 3.6 Add defer or async to scripts in theme.liquid
1. Run Lighthouse and note scripts under render-blocking resources. [1dffb0dd47d1]
2. Open theme.liquid (holds most scripts). Find script tags with neither defer nor async. The new Shopify code editor flags these. [verify UI] [1dffb0dd47d1] [1d1dca3e3cfb]
3. Find out what each script does and which app it belongs to (inspect the front end; example: a script traced to the "ILO Banner" cookie banner widget). Do not touch a script whose function you do not know. [07b358e531fb] [1d1dca3e3cfb]
4. Add defer first. Either `defer` or `defer="defer"` works. [1d1dca3e3cfb]
5. Save, load the store, and test the exact feature the script powers. If it works, keep defer. [1dffb0dd47d1]
6. If it breaks, replace defer with async and test again. If async also breaks it, leave the script as it was; it must block. [1dffb0dd47d1] [9714159dd4aa]
7. Re-run Lighthouse and confirm the render-blocking entry is gone. Example: 78 to 80 after one defer; 81 after removing a jQuery script. Expect small gains per script. [1dffb0dd47d1] [1d1dca3e3cfb]
8. Leave unknown scripts from speed or caching services alone unless testing proves they do nothing (example: a "Website Speedy" script; commenting it out left speed about the same, so he left it). [cdc61c33e699]

Definitions as the source gives them: defer = the script downloads and runs after the document has loaded; async = the script downloads at the same time as the document without blocking it. Source says defer is better ("more powerful") than async. Some apps break with either, because they need their script immediately, or because they want their widget visible at once. [1dffb0dd47d1] [07b358e531fb] [1d1dca3e3cfb]

### 3.7 Self-host a library you must keep
1. Prefer removing jQuery; source calls it old technology and says use vanilla JavaScript. [fdbc70a82f75]
2. If you must keep a CDN library: open its CDN URL in a new tab, save the file. [fdbc70a82f75]
3. Upload it to the theme assets folder in the code editor. [verify UI] [fdbc70a82f75]
4. Copy an existing script line that uses the asset_url filter (as Horizon does) and replace only the file name. [fdbc70a82f75]
5. Hover the link in the code editor; the tooltip should say assets should be served from the Shopify CDN for better performance. [verify UI] [fdbc70a82f75]

### 3.8 Understand how apps reach the page (3 routes)
1. **Async load function (via content_for_header).** In DevTools, expand the head, open the unnamed empty script tags until you find the "asyncLoad" function (usually the last one). It lists the URLs of every app script Shopify injects (example: several Trustpilot scripts). These load at the same time as the theme. [2a89f4e58923] [b7d4c6046a25]
2. **Hardcoded script tag.** Some apps ask you to paste a script into theme.liquid (example: a cookie banner). You can defer these yourself. [b1f2c1da412b] [1d1dca3e3cfb]
3. **App embed toggle.** Theme > Customize > App embeds. When on, Shopify adds the app's scripts directly to the head, not through the async function, which is why they load early. [verify UI] [b711b4ded0ce]
4. Diagnostic demo only: in theme.liquid, commenting out `{{ content_for_header }}` removes all Shopify-injected scripts (example: 80 to 100). Never do this on a live theme; the editor flags it as an error and apps and platform features break. [b7d4c6046a25]

### 3.9 Delay all app scripts until the shopper interacts (content_for_header override)
1. Back up the theme. Work on a duplicate. [d1007a68a9e0] [c33439a2c9b9]
2. Edit code > theme.liquid > search "content_for_header". [verify UI] [d1007a68a9e0]
3. Wrap the tag in a Liquid comment (`{% comment %}` ... `{% endcomment %}`). [4e05290f17d5] [d1007a68a9e0]
4. Paste the delaying code directly under it (the author sells this as "Shopio speed boost"; copy everything between its start and end markers). Or create a snippet and render it in the same spot. [d1007a68a9e0] [c33439a2c9b9]
5. The code stops the async function from injecting app scripts during load, then injects them on the first human interaction (scroll, click, mouse move and similar). You can write your own: "look at this async function and create something that will delay the injection". The source does not publish the code. [d1007a68a9e0] [4e05290f17d5]
6. Save. Wait a couple of minutes. Re-test 3 times. [d1007a68a9e0]
7. Verify: DevTools Console, refresh, move the mouse over the page. A message appears ("Shopio scripts have loaded") and widgets such as the Trustpilot badge appear only after that. [d1007a68a9e0]
8. Test every app's full function afterwards: reviews, upsells, loyalty, forms, tracking events. [6427c0d96eec]
9. Also turn off unused app embeds before testing. [4e05290f17d5]
10. Condition: works best when apps are the bottleneck. If the store has large CLS or LCP, fix those first; the snippet removes blocking time, not layout problems. [4e05290f17d5] [b7d4c6046a25]

### 3.10 Remove one app script from content_for_header and re-inject it yourself
Use when a script flagged as unused is not in theme.liquid (so you cannot add defer). Source describes the method; no code is given. [9714159dd4aa] [56315833a352]
1. Inspect the page head, open the async function, copy the URL of the app script you want to delay. [9714159dd4aa]
2. In theme.liquid, capture content_for_header with Liquid, assign a modified content_for_header with that URL removed, and output the modified version instead of the original. [9714159dd4aa] [56315833a352]
3. Confirm the URL is gone from the async function. The app should now stop working on the front end. If it does not stop, it is also injected via an app embed; toggle that embed off. [9714159dd4aa]
4. Create a snippet (source example name: lazy-scripts.liquid) with a small vanilla JavaScript function that creates a script tag with that src on user interaction (click, scroll or other input). Source asked ChatGPT to write it. Render the snippet in theme.liquid. [56315833a352]
5. Verify the app fires as soon as you click or scroll, and re-test speed. [56315833a352]

### 3.11 Lazy-load a hardcoded app script (cookie banner example)
1. Find the banner's script tag in theme.liquid (in the example it already had defer). Confirm in the speed report that the banner causes CLS or blocking. [b1f2c1da412b]
2. Comment out the original tag. The banner stops showing. [b1f2c1da412b]
3. Paste the lazy-load function above the closing `</head>` tag. Put the script URL in its list (replace the "add your script link here" placeholder). [b1f2c1da412b]
4. The function creates the script tag when the user clicks, scrolls, touches (touchstart), moves the mouse or presses a key (keydown). [b1f2c1da412b]
5. Verify: refresh, do not touch the page, banner absent; move the mouse, banner appears; Console shows a custom interaction script message. Example result: CLS gone, score about 48-50 to 57. [b1f2c1da412b]
6. Card caveat (not in transcript): delaying a consent banner can have legal consequences; confirm with your consent rules. [b1f2c1da412b] [867a3ac29ede]

### 3.12 Lazy-load an app embed widget (chat widget example)
1. Leave the app embed on for now. Refresh the store, open DevTools Elements, search the app name (example: "vanchat"). [b711b4ded0ce]
2. Find its JS element. Right-click > Edit as HTML. Copy the script URL. Add it to the lazy-load function's script list (add a comma after the previous entry). [b711b4ded0ce]
3. Find its CSS element the same way. Paste the CSS URL into the function's CSS area. Save. [b711b4ded0ce]
4. Theme > Customize > App embeds: toggle the app off and save. The function now injects its files on interaction. [verify UI] [b711b4ded0ce]
5. Verify the widget appears only after hover or scroll and works fully. Example: blocking time dropped sharply, score 57 to about 65, over 60 on retest. [b711b4ded0ce] [6427c0d96eec]
6. Repeat for any app that does not need to be on screen at once. Re-check after app updates, since URLs can change. [b711b4ded0ce]

### 3.13 Shopify dynamic payment button script
1. Check whether shoppers use the dynamic checkout (wallet) buttons under add to cart. [needs brand data: dynamic checkout button usage] [98a7bf9f5fb4]
2. If not, disable them; source calls the script demanding and says it slows the store noticeably. [verify UI] [98a7bf9f5fb4]
3. If you keep them: in theme.liquid add another line removing that script from content_for_header (same method as 3.10), and add a case to your interaction script to inject it on first interaction. [98a7bf9f5fb4]
4. Test on a copy theme so customers see no errors. Trade-off not measured: buttons appear only after interaction. [98a7bf9f5fb4]

### 3.14 Load app assets only on the templates that use them
1. For each flagged script, check if its widget is visible on that page. Example: Yotpo and Recharge widgets exist only on collection and product pages, so they need not load on the home page; Swell (rewards) only on the rewards page; the Swiper carousel plugin can load later when no carousel is visible at first. [adc3ea59042a]
2. Load those assets conditionally on the templates that need them. This also removes that app's "reduce unused CSS" warning on other pages. Source gives no code. [adc3ea59042a]
3. Keep Facebook and Google pixel scripts and Hotjar in the initial load (source rule; see 9). [adc3ea59042a] [81ac749043da]
4. Look for duplicate injections (example: Facebook loaded twice, likely once hand-added to theme.liquid and once by the app; PostScript also duplicated). Remove the duplicate. [adc3ea59042a] [81ac749043da]
5. App code you cannot minify or that lacks text compression (example: an asset served from Amazon): contact the app's support, or drop the app if you do not really use it. [81ac749043da]

### 3.15 Image pipeline before upload (recommended order)
Order: resize, crop, convert format, compress, rename, alt text, upload, order gallery, verify on site. Other orders create rework. [08bb3d69ec5b] [dc287d5fb7e6]
1. **Resize.** Long edge to about 2,000 px (3,000 is the "overkill" ceiling). macOS Preview batch method: put same-orientation images in one folder, select all, open in Preview, Edit > Select All, Tools > Adjust Size, set the larger dimension (example 4,000) to 2,000, OK. Do not mix portrait and landscape in one batch. Windows tools exist but are not shown. [verify UI] [08bb3d69ec5b] [cfa3fe76f953]
2. **Crop one by one**, never in bulk, because product position differs per shot. Preview: markup toolbar > selection tool, hold Shift for a square, adjust, click crop. [verify UI] [08bb3d69ec5b]
3. **Convert.** File > Export lets you change format (example: iPhone format to JPEG) and set compression in one step, but you only see file size, not quality. [verify UI] [08bb3d69ec5b]
4. **Compress with a visual preview.** Squoosh: drop the image, drag the quality slider from the default 75 and compare side by side; stop when artifacts show. Alternative: Photopea > Image > Size (2,000 px) > File > Export as JPEG at about 70%. Then optionally TinyJPEG (tinyjpeg.com) or compressjpeg.com. Photoshop also works. [cfa3fe76f953] [621e302f651f] [cce38d9369f2]
5. **Rename** (3.20). **Write alt text** (3.20). [88d406704603] [fe083ee96b08]
6. **Upload** once to the media library and reuse (3.19). [23917da7d97a]
7. **Order the gallery** (3.21) and assign variant images. [b29f3cc2d36f] [c4e17c272dd9]
8. **Verify on the live site** (3.17). [dc287d5fb7e6]
9. Large catalog or images already uploaded: use a bulk compression app instead of one-by-one work. Source uses Tiny SEO Speed and Image Optimizer, set to compress automatically on upload; its report showed individual images losing more than 80%. SEOAnt has a bulk "optimize" for published product images and collections. Keep the manual pipeline for hero and launch images. Measure before and after, because the app adds its own scripts. [3bbbee3c2099] [64042fc21a8b]
10. Do the same for video: compress video files; oversized video is as damaging as oversized images. [3dd6497a4d63] [621e302f651f]

### 3.16 Find and fix heavy images already on the store
1. Content > Files: scroll for large files (examples 3 MB, 5 MB). App compressors often touch only product images, so check section and home page images here. [verify UI] [3a99be49f292]
2. Find which section uses each heavy image. Download it. [3a99be49f292]
3. Compress it on a free compression site (example cut about 70%). If still over budget (example: 1.7 MB), resize in Shopify's image editor (Resize, example width 1,500; aspect ratio is kept; it saves a copy), download again, compress again (example: about 400 KB). [verify UI] [3a99be49f292]
4. Re-upload and place it back in the section. Keep the original if you may need higher resolution later. [3a99be49f292]
5. Quick in-theme fix for a hero: Customize > click the section > on the image click Edit > Resize > enter new width > Apply > Save. Refresh and inspect: it looks the same but is lighter. Shopify's editor has no compression control, so compress separately for the real gain. [verify UI] [7558889b0856] [cfa3fe76f953]

### 3.17 Inspect rendered versus intrinsic size
1. On the live page right-click the image > Inspect. Read the intrinsic size of the file versus the box it renders in. You can dock the DevTools panel to the side. [036e673a5a05] [c9fcbc1b5513]
2. In the Network tab, reload to see the delivered file size. [21698bb77d52]
3. Flag big gaps (example: 5,000 px image in a 700 px box, 6 MB file). [036e673a5a05]
4. Target width = box width plus 100 to 300 px (example: 1,000 px for a 700 px box). Exactly box size can look blurry; far larger wastes weight. [7558889b0856] [c9fcbc1b5513]
5. Decide per image: oversized dimensions, resize; still heavy after resize, compress; right size but heavy, compress only; small and right size, leave it. [08b2e0e2f95d]
6. Re-check visually after each change. Apply to hero, section images and repeated blocks, not only product images. [036e673a5a05]

### 3.18 Check whether the theme serves responsive widths
1. Edit code > open a section or snippet that renders an image (hero, image with text, product grid). [verify UI] [c5fb935a9b7d]
2. Bad pattern: a single img src using the image URL filter with "master". Every device downloads the original (a 5,000 px upload goes to a phone). [c5fb935a9b7d]
3. Good pattern: several width options (example: default 1,600 px, with 800 px under 800 px width, 1,200 px under 1,200 px). [c5fb935a9b7d]
4. Check all image sections on old, custom or agency themes; sections added later often skip the pattern. Fix or have them fixed. [c5fb935a9b7d] [d84575512652]
5. How to see Shopify's width variants: an image URL ends with a width parameter (example 493 or 450) from the theme's image filter; removing it opens the original. Newer themes resize automatically (example: a 5,000 px upload shown at 1,300 px intrinsic). [21698bb77d52]

### 3.19 Upload, media library and variants
1. Upload entry points, all landing in one media library: Content > Files (Upload files), product page (Upload new or Select existing), collection cover image, blog images, theme customizer section image pickers. [verify UI] [c4e17c272dd9]
2. Upload each image once and select it everywhere. Uploading the same file name twice creates a second file with a gibberish-suffixed URL, which hurts SEO and multiplies edits. [23917da7d97a]
3. To update an image everywhere, use Replace image in the media library: URL stays, file swaps. Check each placement after, since a new crop may not fit a hero. [verify UI] [23917da7d97a]
4. Variant images: in the product editor, click the image or plus icon on each variant row, select or upload the matching image, Done, Save. Clicking colour swatches should then switch the gallery. Give every variant a real image. [verify UI] [c4e17c272dd9]
5. Fix a messy grid of mixed ratios: open the image in the media editor > Crop and transform > choose ratio (square preset) > drag to keep the whole product > Apply > Resize (example 3,000 to 1,920) > Apply > Save; refresh the collection page. Better: crop to ratio before upload. [verify UI] [c371cc94a060]

### 3.20 File names and alt text
1. File name formula: main keyword + product descriptor + unique detail + angle. Examples: leather-wallet-men-brown-front, leather-wallet-men-brown-back, leather-wallet-men-stitched-detail; sports-backpack-men-black-front. Never upload camera or supplier names. [88d406704603] [3c75d10544c6]
2. Generate names with a ChatGPT prompt: give main keyword, descriptor and a comma list of per-image details. Match names to files by hand; the model produced more names than images in the demo. [88d406704603]
3. Alt text: describe what is in the image in natural language, include product, visible attributes and angle. Examples: "Men wearing a black sports backpack outdoors", "Closeup of padded shoulder straps on a black sports backpack", "Side view of black men's sports backpack". [fe083ee96b08] [465183671efc]
4. No ads in alt text ("leather wallet man black buy cheap" is wrong), though source ranks it above no alt text. [fe083ee96b08]
5. Generate per-angle alt text with an AI prompt: product name, visible characteristics (example: black, water resistant) and the angle list (front view, back view, front detail, top detail, lifestyle on shoulder). Check each output against the image. [fa20f325b789] [465183671efc]
6. Paste into the image editor's alt text field on the product, or via Content > Files. Save. Inspect the live image element to confirm the alt attribute is there. [verify UI] [465183671efc]
7. SEO video variant: alt text = target keyword + product + attribute + angle (example: "summer fragrance bath bomb purple frontal"), then rename the file to match. Do the same for section images in Content > Files. [66c68817418b]
8. Why: alt text serves visually impaired shoppers, shows when an image fails to load, and helps Google decide whether to show the image in search. The file name only helps Google categorize; it is never shown to users. Source says this is not a speed factor. [fe083ee96b08] [465183671efc]

### 3.21 Product image set and order (merchandising, neighbour 09-CRO)
1. 3 to 5 images minimum (1 works, 2 is better). Each answers a question: main image, alternate angle, detail shot of a feature, lifestyle (in use or held). Video at the end is good too. [17019c2bec17]
2. More images for higher-priced or complex products (kit contents, several scenarios) to justify price. Stop when no image answers a new question; watch excessive mobile scrolling. [17019c2bec17]
3. Order: main, alternate angle, details, lifestyle; or main, alternate, lifestyle, details so the shopper imagines owning it first. Source presents both. [b29f3cc2d36f] [17019c2bec17] [c4e17c272dd9]
4. No supplier lifestyle images: generate with AI (Gemini, Nano Banana). Check accuracy against the product. [b29f3cc2d36f]
5. Aspect ratios: square for general grids; 4:5 for fashion. [c371cc94a060]

### 3.22 Lazy load below the fold
1. Add loading="lazy" to every image not visible at first load. [51db910ccfc8] [0f413fcac223]
2. Add preload="none" to videos so they do not interrupt other downloads. [0f413fcac223] [70af8654d12d]
3. Carousel: lazy load slides 2, 3 and on; never slide 1. [70af8654d12d] [7a213481a9d2]
4. Optional lazysizes plugin ("bulletproof"): set src to an empty pixel, data-src to the real URL, add the lazyload class; the plugin swaps in the real src when needed. Grey placeholders show first (example: a side drawer). Source opinion: slightly better than native loading="lazy". Never on in-view images. [3c9bddfb47c1]
5. Lazy load non-essential app widgets too (3.9 to 3.12). [b4735bb55b51]
6. Verify in the Network panel: in-view images download at once; others only on scroll. [51db910ccfc8]

### 3.23 Fix LCP
1. Identify the largest element in the viewport: usually the hero or the first slide; on a product page the main product image. [7a213481a9d2] [1b9747314efd]
2. Test the page ads land on (usually the product page) with throttling (3.2). Watch whether the main image shows. In the reviewed store the image file had already downloaded but was hidden until a slideshow plugin's JavaScript loaded. [1b9747314efd]
3. Remove loading="lazy", "lazyload"/lazysizes classes or similar from that image. Set loading="eager". [7a213481a9d2]
4. Remove fade-in, slide-in and other entrance effects. Effects need an effects library to download first. Remove any preloader bar or placeholder shown instead of the image. Keep the main image out of the delayed carousel path; show it as a plain image. [7a213481a9d2] [d56347d58c66] [1b9747314efd] [b4735bb55b51]
5. Compress that image as much as possible. [7a213481a9d2]
6. Add preload tags in the head for visible images, fonts and asset URLs, with fetch priority set to high. For product pages, add Liquid logic in theme.liquid that preloads the right image per product. Preload only in-view, critical assets; too many preloads recreate the contention. [d56347d58c66] [1b9747314efd] [b4735bb55b51]
7. Also check blocking time; it affects LCP too. [7a213481a9d2]
8. First-item-eager logic for loops (collection list example, as described; exact syntax not shown, adapt to your theme): [b093ed3b4d75] [481d00497deb]
   - In the section's for loop over blocks, if forloop.index equals 1, assign a variable lazy = false, else lazy = true.
   - Pass it into the card snippet where it is rendered (a line like lazy: lazy).
   - In the card snippet, replace the hardcoded loading="lazy" with: if lazy is false, output loading="eager", else loading="lazy".
   - Inspect: card 1 eager, the rest lazy. Re-test.
9. If a theme's hero section lazy-loads its first image by default, add custom logic to exempt it. [51db910ccfc8]

### 3.24 Find the CLS source
1. PageSpeed Insights: open the screenshot filmstrip and compare frames for an element that appears and pushes content. GIF motion in frames is expected; the signal is a new element. Check the desktop tab too. [f00068c50316]
2. PageSpeed outlines the shifting element. Copy its ID or classes, open the page, Inspect, Cmd/Ctrl+F, paste, press Return to reach the HTML tag. [24893ea78676] [f00068c50316]
3. If the ID looks like an app prefix, search that name in the Shopify App Store (example: "hexom" led to a free shipping bar app that injected an announcement bar after load). [f00068c50316]
4. Lighthouse > View Original Trace: watch the timeline from first paint for elements that appear late (examples: top menu or header, Afterpay widget, product thumbnails). Zoom the page out and re-run to catch below-the-fold shifts. Lighthouse shows fewer issues than PageSpeed Insights; fix Lighthouse first, then PageSpeed's list. [verify UI] [80a761efcb18] [cabcd2d4c66e] [ba43a0aaa747]
5. Throttle and watch (3.2); stop the load mid-way to inspect. [a5d2c3aee970]
6. Search Console > Core Web Vitals shows how CLS affects search. [verify UI] [24893ea78676]
7. Admin dashboard "visual stability: poor" points to CLS; "loading speed: poor" to LCP (click through to analytics). [verify UI] [f00068c50316]

### 3.25 Fix CLS
1. **Images without dimensions:** add width and height attributes to image tags so the browser reserves the box. Works only if CSS keeps the aspect ratio. [d16d1fcdd349]
2. **Late app widgets:** measure the widget's rendered size and add a CSS rule fixing its container width and height. Verify on the breakpoints you care about (fixed size can clip responsive widgets). Test the widget on a duplicate theme. [24893ea78676] [ba43a0aaa747]
3. **Contradicting CSS:** if 2 stylesheets set different heights for one element, remove one rule instead of stacking overrides. [24893ea78676] [80a761efcb18]
4. **App-only simple elements:** replace an app announcement bar with the theme's own. [f00068c50316]
5. **Font swap:** style the fallback font to match the custom font's size and line height so the swap does not resize text. [14bc6ce5b8a6] [cce38d9369f2]
6. **Late body styles (client case):** a "page width 70%" style placed in the body tag re-wrote base CSS after first render and shrank the page. Test removing it; then move that style to the end of the head. It also loaded faster. If the rule is meant for desktop only, wrap it in a media query so it applies only above 767 px (mobile goes full width, no white side bands). Better still, use the theme's layout width setting. Confirm the intended design with the client first. [dbf103b05b0a] [3b3894441e6c]
7. **Body jump:** adding style display:block to the body tag stopped the hero from rendering low and jumping up (presenter used to add this on Dawn). One store's fix. [dbf103b05b0a] [f21b8466aa36]
8. **Lazy-loaded theme CSS without complete critical CSS:** if theme.css loads after the DOM, elements show unstyled for about 1 second then jump. Inline correct critical CSS for the visible part of each template. Generate it with an online critical CSS generator (feed the full theme CSS and the page URL); make separate files for visually different templates (collection with banner versus without). Serve it inline from theme.liquid via a snippet. If the theme has no critical CSS at all, create a snippet of CLS-preventing rules and render it only on the template you are fixing (use conditions). Then test repeatedly with Lighthouse original trace; for any element still moving (example: font-size change), add a rule reserving its final size. [cabcd2d4c66e]
9. **Cookie banner:** delay it (3.11). [b1f2c1da412b]
10. Re-test; aim for the CLS target in section 4. [80a761efcb18]

### 3.26 Fonts
1. Inventory custom font weights and styles actually used. Keep at most about 3 variations; 5 or 10 because of one occurrence is "not a great idea". [1eacf61a57a2]
2. Edit code > search "@font-face". For each rule without it, add `font-display: swap;` (example: just under font-family). Check every weight and italic. [027af5f63b68] [3ef856fab3ae]
3. Test on throttled 3G: a standard browser font shows first, then the custom font swaps in. Without swap the whole document can wait for the font. [027af5f63b68]
4. Match fallback metrics to limit CLS (3.25 step 5). [14bc6ce5b8a6]
5. No real design reason for custom fonts: use Shopify's built-in theme fonts. [1eacf61a57a2]

### 3.27 Delay non-critical CSS
1. Identify stylesheets that style only elements not visible at load (modals, below-fold sections). [08d397da7d0d] [b73d08e8603c]
2. Rewrite them as `<link rel="stylesheet" href="..." media="print" onload="this.media='all'">`. [08d397da7d0d]
3. Never apply it to CSS for in-view elements; that causes unstyled content, CLS and LCP. Keep critical CSS loading normally. [b73d08e8603c] [cce38d9369f2]
4. Check the swap happens (rendered page and Network panel). A failed onload leaves the sheet applied to print only. [e9b7f4c3107e]

### 3.28 Theme choice, migration and benchmark
1. New store or beginner: start on Dawn or Horizon, not a complex premium theme. Free saves about $300. [637495534f7f]
2. The 23 free themes are 2 codebases: 13 Dawn-based and 10 Horizon-based (Horizon ones carry a "new" badge in the theme store). They differ only in settings, JSON data, images and colours; versions match within each family. Switching between variants of one base changes design, not performance. [943bdc967b80]
3. Structure: Debut was "Shopify 1.0" (all settings in one settings_data.json); Dawn is a 2.0 theme (JSON templates per page); Horizon adds a blocks folder of global blocks usable in any block-accepting section, with nested sub-blocks (example: accordion). Dawn sections only accept their own blocks. Customizer copy-paste and renaming of sections apply to all themes. [d68b270990ab]
4. Existing Dawn store with lots of work: keep Dawn for now; move to Horizon at the next redesign. New store: build on Horizon. Developers and designers: learn Horizon. Presenter expects Dawn to be sunset eventually but not soon; wait for Horizon to mature past early bugs. [21280154cb29]
5. Old, slow theme on an established store: apply all fixes in this playbook, accepting that some get technical. If you can, rebuild on Dawn or Horizon; every section must be rebuilt, but optimizing an old theme can cost more than migrating. Plan it with a redesign. [02c570556e30]
6. Benchmark method: 2 themes on one store with identical content (hero banner and a few products), all app embeds off in both, PageSpeed on each published theme, record mobile and desktop plus LCP and blocking-time details. [caf6d4c08b6d]

### 3.29 Order of operations (the source gives 3 versions)
- **7-step framework:** 1 reduce apps; 2 remove residual code; 3 images; 4 fonts; 5 prioritize scripts (defer/async); 6 delay non-visible CSS; 7 lazy load apps and their assets on interaction. The 7-tips video adds that step 7 may need a specialist. [cce38d9369f2] [15d23b16ff3c]
- **Top-5 video:** 1 remove apps and residual code; 2 defer or lazy load scripts; 3 images; 4 fonts; 5 choose the right theme. [8dbbb42b9c2e] [637495534f7f]
- **Client case work order:** defer scripts in theme.liquid; lazy load app scripts (override plus per-app); find and fix CLS; fix LCP (first in-view eager). Retest 3 times per stage. [dca8734ae894]
- The LCP/CLS video and the "needs a good score" card say fix LCP and CLS first because they dominate the score, and the app snippet is "not as effective" while CLS or LCP is large. [37d2f02ad647] [4e05290f17d5]
- SEOAnt video order: compress images, then speed up the store, then on-page SEO. [64042fc21a8b]

### 3.30 Full store audit (as the presenter does it)
1. Test home, collection and product pages (3.1). Do not trust "vitals passed". [5e79bed9130e] [81ac749043da]
2. Read the JavaScript execution delay (example: 2.7 s, mostly apps). Inventory apps; no new installs yet. [81ac749043da]
3. For each script: needed at load? Social widget, PostScript and similar can load later or go. Keep pixels and Hotjar. Remove duplicates. Review jQuery and remove if possible. [81ac749043da] [adc3ea59042a]
4. Fix images flagged "too large for mobile". Lazy load only below the fold. [81ac749043da]
5. Fix render-blocking CSS, including app widget CSS; keep the real critical CSS. [81ac749043da]
6. Minify what you can; contact app support about uncompressed or unminified assets, or drop the app. [81ac749043da]
7. Expect new issues to appear in Google's top list as you clear old ones. Fix all templates of a page type, not only the one Shopify links to (extra gain in presenter's tests). [9b3008487ad5] [5e79bed9130e]

### 3.31 Mobile product page layout (from a store review; neighbour 09-CRO)
1. Pull a scroll heatmap (Hotjar). Example depth: everyone sees the header and first image, then 93%, 91%, 80% and so on; only 20% reached add to cart. [bf8e6e41254e]
2. Shrink the mobile logo (tried 120, 110, 100 px), remove big gaps, shrink or single-line header text. [bf8e6e41254e]
3. Move variants and quantity directly under reviews. Test the benefit row below versus above the buy button. [bf8e6e41254e]
4. Button: a bit thinner, full width; test "Add to bag" versus "Add to cart" instead of "Yes I want mine". Show the review badge on mobile if desktop has it. [bf8e6e41254e]
5. Promo copy: replace "20 to 50% off with free shipping today only" with 1 clear offer (for example "50% off with free shipping"). [00a97db32711]
6. Other review notes: use real product photos, not supplier images with text (a dropshipping tell); keep one image style (all white background or all in use); make the gift product relevant to the main product; align reviews left. [transcript only; no card]

### 3.32 SEO procedures in this source (neighbour 15-SEO-search; kept for completeness)
1. Keywords: 1 main + 2 secondary per page. Google Keyword Planner (needs a Google Ads account; Tools > Planning; enter seed, country, language; Get results). Read volume, competition, CPC. Prefer buying intent ("homemade soap for sale", "near me") over informational ("how to make"). Use "Start with a website" on a competitor URL. Cross-check with Google Trends plus the Glimpse Chrome extension, Google autocomplete, or paid Ahrefs or Semrush (show intent directly). [verify UI] [a8d01f5b91b6]
2. Store listing: Online Store > Preferences > Search engine listing. Main keyword in the title (limit 70 characters; example used 63), supporting keywords and a call to action in the description. Draft with ChatGPT, then fit brand voice. [verify UI] [198c9b1e5856]
3. One H1 per page. On Dawn, the home page H1 is the logo, collection H1 is the collection title, product H1 is the product title. Check custom sections for extra H1s. [cdf20f6157c3]
4. Product titles: rewrite vague names ("sweet honey bomb") into keyword titles: ChatGPT for candidates from specs, validate in Keyword Planner, ChatGPT for title options with the main keyword, then reduce title font size in the customizer if needed. [1ba6eb3b6a8f]
5. Descriptions: at least 100 words, 300 to 400 ideal, keywords included, human-sounding. Collection descriptions 100 to 400 words; can move below the product grid. [b5556041696c]
6. Meta description about 160 characters, written for clicks more than keywords; keep a good auto-excerpt on large catalogs. [bc59ae3525fa]
7. URL handle: paste the title, drop grammar and special characters, keep "create URL redirect" ticked so old links do not 404. Same for collections, pages and blog posts. [verify UI] [0894dbc180a6]
8. Internal links from pages and posts to products and each other speed up crawling. [512774f2b241]
9. Rich snippets (FAQ, product with price, rating, reviews, availability, article) need custom code or an app. [91fbb9ca7dd1]
10. Blog at least 2 posts a month, ideally 4 (1 a week), researched in Keyword Planner. [73c6764d7c45]
11. Backlinks from authoritative sites, partners, influencers. [d0b33b41e18d]
12. Settings > Domains: set the custom domain as primary, then submit yourstore.com/sitemap.xml in Search Console > Indexing > Sitemaps; resubmit if you change primary domain later. [verify UI] [e42e8ace0dab] [3ef1ab6d1697]
13. Fill brand information (logo, colours) in the brand settings (found via Sidekick); Facebook, Google and other channels pull it. [verify UI] [e482e075913e]
14. SEOAnt app (affiliate): speed score, SEO summary, bulk image optimize, "instant page" speed feature free, per-page score (80% with 2 target keywords, 91 after adding an H2, 94 after images in description and keyword in meta), search appearance snippet toggles plus a test, broken link finder, backlink tracking, keyword research, "analyze my keywords", competitor tracking. [verify UI] [d075713968d8] [9f00d339ffcc] [64042fc21a8b]

## 4. Rules, thresholds and numbers

| Rule | Number or threshold | Condition | Source's basis | Card |
|---|---|---|---|---|
| Shopper patience | leaves if not loaded in 2 to 3 s; many leave after 3 to 4 s; 10 s+ store has "no chance" | mobile, from ads | presenter's own behaviour; unsourced "studies" | 37d2f02ad647, 74187c8d7e19 |
| Attention span | about 8 s | adults | "studies say", unsourced | 74187c8d7e19 |
| First impression | 0.05 s (50 ms) after load | all visitors | stated, unsourced | (transcript only) |
| Load target | under 3 s | whole store | "Google says" per presenter | (transcript only) |
| Low-score alarm | Google score 20 or lower | mobile | presenter: many customers struggle or fail to load | 74187c8d7e19 |
| Case target | mobile score over 50 | client work | presenter's goal; "33 is not bad, over 50 is better" | dca8734ae894 |
| LCP + CLS fix alone | score "well over 50, maybe 60" | one example store | presenter estimate | f00068c50316, 37d2f02ad647 |
| LCP | "should be under 4" (seconds) | product page | presenter; store was about 5 s | 1b9747314efd |
| CLS | under 0.25; ideally 0.1 or 0 | all pages | presenter | 80a761efcb18 |
| Page weight | 2 to 3 MB total ("the entire store"); SEO video says a page "can have like 2 MB", maybe a bit more | whole page | presenter practice | 621e302f651f, 3a99be49f292 |
| Image file ceiling | 500 KB recommended max (video 1) | Shopify images | presenter | 21698bb77d52 |
| Image file ceiling | 500 to 600 KB, never over 600 KB; better 100 to 200 KB | before upload | presenter | cfa3fe76f953 |
| Image file ceiling | reduce anything over 500 KB | checklist | presenter | 0c4e0163aff8, dc287d5fb7e6 |
| Image file ceiling | under 1 MB; "1 MB is too much"; ideally a few hundred KB | section and hero images | presenter | 3a99be49f292 |
| Image file ceiling | full HD JPEG under 1 MB covers any screen | mobile-majority traffic | presenter | cce38d9369f2, 70af8654d12d |
| Max dimension | never above 2,000 to 3,000 px; 3,000 is overkill; 2,000 enough for zoom and retina | uploads | presenter demo | cfa3fe76f953 |
| Full-width hero | up to about 3,000 px (a 3,840 px 4K screen may use more) | full-bleed hero only | presenter | cfa3fe76f953 |
| Zoomable product image | 1,920 x 1,920 at 46 KB looked fine | product zoom | example store | cfa3fe76f953 |
| Resize target | display box + 100 to 300 px | section images | presenter rule of thumb | 7558889b0856, c9fcbc1b5513 |
| Squoosh quality | default 75; 40 gave 172 KB from 2.7 MB; 20 to 30 still acceptable | photos | presenter's eye | cfa3fe76f953 |
| JPEG export quality | about 70% (lower if it holds) | Photopea export | presenter | 621e302f651f |
| Compression savings | free sites 50 to 70%; compressjpeg.com 50 to 60%+; app over 80%; a second pass only 8% | examples | demos | 3a99be49f292, cce38d9369f2, 3bbbee3c2099, 621e302f651f |
| Shopify built-in compression | 9.8 MB upload delivered at 6.1 MB | test store | presenter demo | 21698bb77d52 |
| Formats | JPEG default; PNG only for transparency; no GIF; MP4 in video tag for motion; do not upload WebP | all images | presenter | 02dbd594ff18, 3dd6497a4d63 |
| Product images | 3 to 5 minimum (1 ok, 2 better) | per product | heuristic | 17019c2bec17 |
| Aspect ratio | square; 4:5 for fashion | product grid | common practice per presenter | c371cc94a060 |
| Custom font variations | about 3 max | custom fonts | presenter | 1eacf61a57a2 |
| Speed tests | 3 runs averaged (3 to 4 in one video) | every comparison | practice | c33439a2c9b9, 9b3008487ad5 |
| Wait before retest | about 1 minute; "a couple of minutes" | after a change | caching lag | c33439a2c9b9, d1007a68a9e0 |
| PSI field data window | 28 days | historical graphs | Google tool behaviour as stated | 0d2d3621b19d |
| Shopify admin score refresh | 12 to 24 h, needs traffic | admin score | presenter observation | 9b3008487ad5 |
| Search Console CLS recovery | about 28 days in one case; "a couple of days" in another | after fix | cases | 80a761efcb18, ba43a0aaa747 |
| App delay snippet gain | "10 to 20%"; "10 to 15%"; "15 to 20% or more" | apps are the bottleneck | presenter claims, differ by video | b7d4c6046a25, dca8734ae894, 0d2d3621b19d |
| Apps' cost | about 20% of initial score (Stamped, Smile, Rebuy, Instafeed) | demo store | presenter demo | (transcript only) |
| Score decay | 60 to 80 new, 40 with apps, 20 or 10 or lower with customization | over time | illustrative | 474204ae609c |
| Premium theme cost | about $300 | theme choice | presenter | 637495534f7f |
| Free themes | 23 = 13 Dawn + 10 Horizon; Dawn 15.3.0, Horizon 1.0.1 | at recording | theme store | 943bdc967b80 |
| Desktop-only style breakpoint | min-width 767 px | client CSS fix | one store | dbf103b05b0a, 3b3894441e6c |
| Custom throttle | about 20 kbps | CLS hunting | presenter | a5d2c3aee970 |
| Mobile logo | 100 to 120 px | PDP review | opinion | bf8e6e41254e |
| Scroll depth | only 20% reached add to cart | one store | Hotjar | bf8e6e41254e |
| SEO title | 70 character limit (63 used) | store listing | Shopify field | 198c9b1e5856 |
| Meta description | about 160 characters | product, post | presenter | bc59ae3525fa |
| Description length | 100 words min; 300 to 400 ideal; collections 100 to 400 | product, collection | presenter | b5556041696c |
| Keywords per page | 1 main + 2 secondary | every page | presenter | a8d01f5b91b6 |
| Blog cadence | 2 per month minimum, 4 ideal | content | presenter | 73c6764d7c45 |
| SEOAnt description images | 1 to 4 pictures | per app scoring | app rule | d075713968d8 |

## 5. Diagnostics and checks

| Check | How | Good | Bad | Next |
|---|---|---|---|---|
| Baseline score | PSI 3 runs per page type, averaged, mobile and desktop | stable average; mobile over 50 | 20 or lower; large swings | run 3.3 onward; swings suggest many apps [c33439a2c9b9] [74187c8d7e19] |
| Vitals vs score | PSI on home, collection, product | vitals pass and score decent on all 3 | "vitals passed" but 18/38 | audit all 3 pages [5e79bed9130e] |
| Blocking JS | PSI "reduce JavaScript execution" and "unused JavaScript"; Lighthouse render-blocking list | few app scripts at load | seconds of JS (example 2.7 s) from apps | 3.6 to 3.14 [81ac749043da] |
| App scripts at load | DevTools head > asyncLoad function; theme.liquid scripts; App embeds | only needed scripts; pixels once | many app URLs; duplicates | delay, remove, dedupe [2a89f4e58923] [adc3ea59042a] |
| Residual code | search app names in theme files / downloaded theme | no hits for removed apps | leftover tags | remove after backup [3c6bd0cce957] [10d064e032f8] |
| Scripts without defer/async | theme.liquid scan; editor warning | all non-critical have defer or async | bare script tags | 3.6 [1d1dca3e3cfb] |
| Delay snippet working | Console message on mouse enter; widget appears after interaction | message and widget after hover | widget shows at load, or never | check comment/paste; test app [d1007a68a9e0] |
| Image weight | Content > Files sizes; Network tab | under the ceiling you chose (section 4) | multi-MB files | 3.16 [3a99be49f292] |
| Image dimensions | Inspect intrinsic vs box | box + 100 to 300 px | 5,000 px in 700 px box | resize then compress [036e673a5a05] |
| Responsive widths | read section code | srcset with several widths | img src with master | fix section [c5fb935a9b7d] |
| Format | file extensions | JPEG photos; PNG only transparent; MP4 motion | PNG photos; GIFs | re-export [02dbd594ff18] |
| Hero loading | Inspect hero/first slide/first card | loading="eager", preloaded, no effect | loading="lazy", lazyload class, fade-in, preloader | 3.23 [7a213481a9d2] |
| LCP on ad landing page | throttled load of PDP | main image shows at once | image downloaded but hidden by carousel JS | 3.23 steps 4 and 6 [1b9747314efd] |
| CLS source | PSI filmstrip; Lighthouse original trace; throttled reload; desktop tab | no element moves without input | header, widget, thumbnails, banner push content | 3.25 [f00068c50316] [80a761efcb18] |
| Font swap | search @font-face; throttled reload | swap on every rule; fallback sized to match | invisible text; text resizes on swap | 3.26 [027af5f63b68] [14bc6ce5b8a6] |
| Non-critical CSS | review stylesheets; Network panel | below-fold CSS on media=print swap | everything render-blocking; or visible CSS delayed | 3.27 [b73d08e8603c] |
| Critical CSS | Lighthouse trace first second | styled from first paint | unstyled flash then jump | recompile critical CSS [cabcd2d4c66e] |
| App still works | exercise each delayed app fully | widget, forms, events all work | anything broken | revert that app [6427c0d96eec] |
| Tracking intact | test page view, variant, add to cart, test purchase; check missing and duplicate events | all events once | missing or doubled | revert or fix per integration [ef51a42e0e16] [needs brand data: pixel and consent setup] |
| Mobile friendly | device toolbar | text in screen, images right | overflow, distortion | fix layout [58bc1e28be27] |
| Buy button reach | Hotjar scroll heatmap | most visitors reach add to cart | 20% reach it | 3.31 [bf8e6e41254e] [needs brand data: scroll heatmap] |
| Shopify admin score | admin speed/web performance view after 12 to 24 h | improving | not updated yet | wait; fix all templates [9b3008487ad5] |

## 6. Tools, settings and named features

- **Google PageSpeed Insights:** main score, field data (28 days), filmstrip screenshots, CLS element outline, mobile and desktop tabs. [0d2d3621b19d] [f00068c50316]
- **Chrome Lighthouse** (DevTools > Lighthouse): render-blocking list, View Original Trace for CLS timeline. [verify UI] [1dffb0dd47d1] [80a761efcb18]
- **Chrome DevTools:** Elements (find asyncLoad, Edit as HTML), Network (Disable cache, Fast/Slow 3G, custom profiles), Console (snippet messages), Performance tab, Coverage tab (PSI suggests it for unused JS; presenter calls line-by-line cleanup simplistic), device toolbar. [verify UI] [a5d2c3aee970] [2a89f4e58923]
- **Safari:** Develop > Enter Responsive Design Mode. [verify UI] [58bc1e28be27]
- **GTmetrix:** extra test when Google's list is exhausted. [9b3008487ad5]
- **Unnamed GIF-capture site** for page-load recordings; **unnamed online critical CSS generator**. [a5d2c3aee970] [cabcd2d4c66e]
- **Google Search Console:** Core Web Vitals report; Indexing > Sitemaps. [verify UI] [24893ea78676] [e42e8ace0dab]
- **Shopify admin:** Online Store > Themes > Edit code (search, new editor warnings), Download theme file, Customize > App embeds, Content > Files, image editor (Crop and transform, Resize, alt text; no compression control), Replace image, Preferences > Search engine listing, Settings > Domains, speed score / web performance view, Sidekick, dynamic checkout buttons. [verify UI] [8dbbb42b9c2e] [c371cc94a060] [9b3008487ad5]
- **Liquid:** content_for_header, asset_url, image URL filters (width parameter, "master"), for loop index, comment tags, capture/assign. [b7d4c6046a25] [fdbc70a82f75] [b093ed3b4d75]
- **HTML/CSS attributes:** defer, async, loading="lazy", loading="eager", preload="none" (video), link rel="preload" with high fetch priority, width and height on img, font-display: swap, media="print" onload="this.media='all'", media queries. [0f413fcac223] [d56347d58c66] [08d397da7d0d]
- **lazysizes** plugin (data-src, lazyload class). [3c9bddfb47c1]
- **Shopify Theme File Search** Chrome extension; **Cursor** code editor (free, AI). [3c6bd0cce957] [10d064e032f8]
- **Image tools:** macOS Preview, Squoosh, Photopea, Photoshop, TinyJPEG/tinyjpeg.com, compressjpeg.com, Canva (warned: PNG export is heavy), Tiny SEO Speed and Image Optimizer app (affiliate), SEOAnt (affiliate), ChatGPT for names and alt text, Gemini and Nano Banana for lifestyle images. [verify UI] [cfa3fe76f953] [621e302f651f] [3bbbee3c2099]
- **Author's paid snippets:** "Shopio speed boost" (content_for_header delay), cookie banner lazy-load function. Not published in the source. [d1007a68a9e0] [b1f2c1da412b]
- **Apps named as examples:** Loox, Yotpo, Stamped, Judge-type reviews via Trustpilot, Smile, Rebuy, Instafeed, Recharge, Swell, PostScript, Hotjar, Klaviyo (kept as an embed that makes money), Hexom free shipping bar, ILO cookie banner, VanChat, Afterpay widget, Swiper, jQuery, Website Speedy. [adc3ea59042a] [f00068c50316] [b711b4ded0ce]
- **Themes:** Debut, Dawn, Horizon. [d68b270990ab]
- **SEO tools:** Google Keyword Planner, Google Trends, Glimpse extension, Google autocomplete, Ahrefs, Semrush. [a8d01f5b91b6]

## 7. Examples and case results (examples, not promises)

1. **Shopify delivery test:** 9.8 MB upload delivered at 6.1 MB (6,130 KB). Presenter's ceiling is 500 KB. [21698bb77d52]
2. **Visual comparisons:** 2.7 MB vs 136 KB compressed looked the same; 5,712 x 3,213 at 2.5 MB vs 1,920 x 1,080 at 38 KB looked the same on a 3,000 px wide screen; 8 MB hero vs 234 KB compressed looked the same; 400 KB vs 100 KB looked the same. [cfa3fe76f953] [621e302f651f]
3. **PNG cost:** same photo re-exported as PNG with no edits went from 2.7 MB to 8 MB. [02dbd594ff18]
4. **Box waste:** a 600 x 600 box fed a 5,000 px image serves about 3 MB where about 60 KB would do. [cfa3fe76f953]
5. **Hero resize in Shopify:** 5,712 px wide hero resized to 2,000 in the editor dropped to about 1 MB; presenter says compression could reach about 100 KB. (He reads the new intrinsic width as 2,700, which conflicts with the 2,000 he typed.) Section image: 6 MB, 5,000 px in a 700 px box, resized to 1,000 px, about 1 MB. [7558889b0856] [08b2e0e2f95d]
6. **Files library:** 5 MB image, compressed to 1.7 MB, resized to 1,500 px (1.6 MB), compressed again to about 400 KB. [3a99be49f292]
7. **Photopea:** 2,000 px, JPEG 70% gave about 200 KB; TinyJPEG then removed only 8% more. [621e302f651f]
8. **Lighthouse script demo:** 78 to 80 after one defer; 81 after removing jQuery; 100 with content_for_header commented out (diagnostic only); 97 with the delay snippet; back to 80 when reverted. [1dffb0dd47d1] [b7d4c6046a25]
9. **Delay snippet, LCP/CLS video:** about 40 to 50 rose to 85, and reverted when removed. [4e05290f17d5]
10. **App lazy-load video (simple Dawn store):** 37 to 38 baseline; snippet 48 to 50; cookie banner delayed, CLS gone, 57; chat widget delayed, about 65, over 60 on retest. [d1007a68a9e0] [b1f2c1da412b] [b711b4ded0ce]
11. **Client store to over 50:** mobile 33 to 58, desktop to 93. Changes: defer on the cookie banner script, delay snippet (scores bounced: "19", then 38, then over 40; CLS about "170 something" before), display:block on body, moved the 70% page-width style to the end of the head with a 767 px media query, first collection card eager. Several changes together, so no single step gets the credit. [dca8734ae894] [481d00497deb] [867a3ac29ede]
12. **Horizon vs Dawn:** Horizon 71 mobile, 77 desktop; Dawn 56 mobile, 78 desktop; LCP from an oversized hero in both. Presenter later restates Horizon as "71 and 74". [caf6d4c08b6d]
13. **Community store PDP:** LCP about 5 s from a carousel plugin hiding a downloaded image; presenter expects about 43 to 50 (or 50 to 60 with preload) after fixes; Hotjar showed 20% reach add to cart. [1b9747314efd] [bf8e6e41254e]
14. **CLS client:** PSI showed "141" on a product page (unit unclear); late header menu, Afterpay widget and thumbnails. Another case: CLS 0.73 (12 June), 0.66 (18 June), then 0.13, 0.1 and 0 after about 28 days. [80a761efcb18]
15. **Critical CSS store:** organic visits dropped, owner blamed CLS; recompiled critical CSS plus reserve rules turned PSI green; Search Console lagged days. [cabcd2d4c66e]
16. **Audit store:** vitals passed but home 18, collection 38, product lower, about 20 overall; 2.7 s JS from apps; Facebook loaded twice; social widget, PostScript, jQuery flagged. [5e79bed9130e] [81ac749043da]
17. **Code widget demo:** Stamped, Smile, Rebuy, Instafeed cost about 20% of the initial score; snippet "restored" it on a basic store. [transcript only]
18. **SEO examples:** "homemade soap" 1,000 to 10,000 monthly searches, high competition, CPC about $0.20 to $1.54 (captioned "$154"); SEOAnt page score 80 to 91 to 94. [a8d01f5b91b6] [d075713968d8]

## 8. Mistakes the source warns about

- Keeping apps that do not clearly make money; using an app for an announcement bar or other simple theme feature. [8dbbb42b9c2e] [f00068c50316]
- Assuming uninstalling an app removes its code. [3c6bd0cce957]
- Commenting out content_for_header on a live theme. [b7d4c6046a25]
- Adding defer or async to a script without knowing what it does; not testing the app after. [07b358e531fb] [6427c0d96eec]
- Loading jQuery or libraries from an outside CDN. [fdbc70a82f75]
- Believing "Shopify optimizes images automatically". [21698bb77d52]
- Believing higher resolution always looks better; uploading DSLR originals. [cfa3fe76f953] [cce38d9369f2]
- Believing PNG is better than JPEG; exporting banners as PNG from Canva. [02dbd594ff18]
- Believing more images always means a slower site. [8e4f0dac7e97]
- Converting and uploading WebP yourself (non-supporting browsers would show nothing, per source). [21698bb77d52]
- Using animated GIFs. [5148a60eef22] [68ca7da1a081]
- Batch cropping. [08bb3d69ec5b]
- Uploading the same image twice instead of reusing and using Replace. [23917da7d97a]
- Mixed aspect ratios in one grid. [c371cc94a060]
- Random camera file names; ad copy in alt text; no alt text. [88d406704603] [fe083ee96b08]
- Lazy loading the hero, logo, first slide, main product image or first card. [7a213481a9d2] [b093ed3b4d75]
- Fade-in or slide-in effects, preloaders or placeholders on in-view images. [d56347d58c66]
- Making everything eager, or preloading too many assets. [481d00497deb] [b4735bb55b51]
- Images without width and height; unreserved widget space; contradicting CSS; late inline styles in the body. [d16d1fcdd349] [24893ea78676] [dbf103b05b0a]
- Missing font-display: swap; 5 to 10 font variations; swapping without matching fallback size. [1eacf61a57a2] [14bc6ce5b8a6]
- Applying the media=print trick to CSS for visible elements. [b73d08e8603c]
- Testing only on fast Wi-Fi; testing only mobile or only desktop; testing only the home page. [74187c8d7e19] [f00068c50316] [5e79bed9130e]
- Trusting a single test run, or retesting immediately after a change. [079f8ea11444]
- Thinking CLS reported by Google is a measurement error. [24893ea78676]
- Buying speed apps or specialists that game the score; adding caching scripts. [5f44ccb5ead1] [cdc61c33e699]
- Buying a feature-heavy premium theme on a hunch; rushing a Dawn to Horizon migration. [637495534f7f] [21280154cb29]
- Fixing only the one template Shopify links to. [9b3008487ad5]
- Deferring tracking pixels (source's view; see 9). [cce38d9369f2]
- Supplier images with text overlays; confusing multi-level promo copy; buy button far down on mobile. [bf8e6e41254e] [00a97db32711]
- SEO: several H1s per page; spec-only descriptions; changing URL handles without the redirect ticked; submitting the sitemap before setting the primary domain. [cdf20f6157c3] [b5556041696c] [0894dbc180a6] [3ef1ab6d1697]

## 9. Caveats, conflicts and what is missing

**Conflicts inside the source**
- **Image file ceilings differ by video:** 500 KB max; 500 to 600 KB (never over 600); prefer 100 to 200 KB; under 1 MB; full HD JPEG under 1 MB is enough. Do not average these. The strictest stated is 500 KB with 100 to 200 KB preferred (image-guide video); the loosest is under 1 MB (7-step and 7-tips videos). [21698bb77d52] [cfa3fe76f953] [3a99be49f292] [cce38d9369f2]
- **Page weight:** "entire store around 2 or 3 MB" vs "a web page can have like 2 MB, maybe a bit bigger". [621e302f651f] [3a99be49f292]
- **Delay-snippet gain:** 10 to 20%, 10 to 15%, 15 to 20%; plus warnings that it helps little when CLS/LCP or other issues dominate. [b7d4c6046a25] [dca8734ae894] [4e05290f17d5]
- **Order of work:** 3 sequences (section 3.29). The 7-step list puts app lazy loading last; the client case does it second; the LCP/CLS video says fix LCP and CLS first.
- **Gallery order:** details before lifestyle, or lifestyle before details. [b29f3cc2d36f] [17019c2bec17]
- **Horizon desktop score:** 77 then restated as 74 (card uses 74). [caf6d4c08b6d]
- **Hero resize demo:** typed 2,000 px, then read 2,700 px intrinsic. [7558889b0856]
- **defer vs async wording:** most videos say async loads alongside and defer after the document; one line in the client-case video garbles this. Source always prefers defer.

**Conflict between source and card editors**
- **Pixels:** the source says tracking pixels (Facebook, Google) must not be deferred and should stay in the initial load. Cards [ef51a42e0e16] and [20821a7ae674] add an editorial correction: this is not a universal requirement; use Shopify's supported pixel integration (Web Pixels API, standard events, https://shopify.dev/docs/api/pixels) and test consent, page view, variant, add to cart and a test purchase for missing and duplicate events. An agent should follow the tested behaviour of each integration, not a blanket rule. [web check: current Shopify Web Pixels guidance] Pixel setup itself belongs to 06-MEA.
- **Cookie banner:** card [b1f2c1da412b] adds a compliance caveat the transcript does not raise. Card [867a3ac29ede] says a "different property" was added; the transcript says "a differenter property", which in context is **defer** on the cookie banner script. Treat it as the defer fix.

**Card errors spotted against the transcript**
- [fde546149035] names Yotpo as the uninstall example; in that video the example is the Loox review app ("logs"). The Yotpo leftover example is from the unused-JavaScript video [68699dfd59de].
- [f00068c50316] says the free shipping bar CLS was worse on desktop; transcript says the desktop reading was "a little bit higher" for the same element.

**Claims to verify on the live web**
- [web check: current Google Core Web Vitals thresholds for LCP, CLS and INP] The source's "LCP under 4" and "CLS under 0.25" are the presenter's numbers. INP is never mentioned.
- [web check: whether Shopify still serves WebP/AVIF automatically and whether uploading WebP is still a problem]
- [web check: whether Shopify admin still has a composite speed score and how its web performance report is calculated]
- [web check: current state of Dawn updates and Horizon version]
- [web check: whether speed-optimization apps "only work for returning users"] This is the presenter's opinion.
- [web check: "8-second attention span" and 50 ms first-impression figures] Unsourced.
- [web check: behaviour of media=print onload trick and lazysizes in current browsers]

**Bias and evidence limits**
- The presenter sells the delay snippets, a course and a service, and has affiliate links to Tiny SEO and SEOAnt. His strongest numeric claims promote those products.
- All scores are single stores and few runs; several changes are often made together.
- No revenue or conversion data. "Optimized stores got more sales" is his observation.

**What is missing (the source skips the how)**
- No published code for the content_for_header delay snippet, the cookie banner function or the lazy-scripts snippet; only the method.
- No exact Liquid for capture/replace of content_for_header or for conditional app loading per template.
- No exact srcset Liquid, preload tag markup or fetchpriority syntax beyond names.
- No video tag attributes for GIF replacement (autoplay, muted, loop, playsinline). [5148a60eef22]
- No INP, TTFB, server response, third-party connection or cache-header guidance.
- No field-data (real user) method beyond PSI's 28-day graphs; no CrUX or RUM setup.
- No rollback steps beyond "back up or duplicate the theme".
- No guidance on consent mode or legal limits of delaying consent banners.
- No names for the critical CSS generator, GIF-capture site or the free compression site in some demos.
- Checkout, cart drawer and Shopify Markets speed are not covered.
- [needs brand data: theme name, version and customization history] [needs brand data: installed apps and which widgets must show at load] [needs brand data: mobile share and ad landing pages] [needs brand data: baseline PSI averages per template]

**Neighbour folders:** SEO steps (3.32) belong to 15-SEO-search; PDP layout, promo copy and image order (3.21, 3.31) to 09-CRO-testing and 07-LPG-landing-pages; pixel and CAPI setup to 06-MEA-measurement; theme selection and media library setup overlap 05-SET-store-setup.

## 10. Card index

- 3c6bd0cce957 | Remove residual Shopify app code from theme files
- ff5edde57340 | Format and size images and videos for faster load
- 0f413fcac223 | Lazy load below-fold media, preload the hero
- ef51a42e0e16 | Reduce storefront script blocking while preserving purchase tracking
- 08d397da7d0d | Load non-critical CSS asynchronously with the media=print trick
- 3ef856fab3ae | Set font-display: swap to prevent invisible text
- 23a3f294b81c | Approach speed work as rendering mechanics, not app shortcuts
- 21698bb77d52 | Shopify image pipeline audit: what Shopify does and doesn't optimize
- c5fb935a9b7d | Check whether your theme serves responsive image widths
- 02dbd594ff18 | Choose JPEG, PNG, WebP or MP4 by image role
- cfa3fe76f953 | Size and compress product images before upload
- 08bb3d69ec5b | Batch resize in Preview, crop individually, then convert format
- 3bbbee3c2099 | Automate image compression for large catalogs
- c371cc94a060 | Fix messy product grids with Shopify's crop and resize tools
- 17019c2bec17 | Plan a product image set: 3-5 images that each answer a question
- 88d406704603 | Name image files with keyword-first descriptive filenames
- fe083ee96b08 | Write alt text that describes the image, not a sales pitch
- c4e17c272dd9 | Upload product images and assign variant images so color swatches switch the gallery
- 23917da7d97a | Reuse one media-library file per image and use Replace to update everywhere
- d84575512652 | Diagnose whether images are a plausible cause of your speed problem
- 8e4f0dac7e97 | Lazy-load images so catalog size doesn't dictate load weight
- 20821a7ae674 | Reduce storefront script blocking while preserving purchase tracking
- e9b7f4c3107e | Load non-critical CSS asynchronously
- 3263b4728b85 | Prevent invisible-text flash with font-display: swap
- 5148a60eef22 | Replace animated GIFs with MP4 video in a video tag
- 465183671efc | Write descriptive alt text that serves accessibility and image SEO
- fa20f325b789 | Match alt text to image angle for multi-image product galleries
- 7558889b0856 | Resize images to just above their display box
- 0c4e0163aff8 | Compress images to keep files small, especially for mobile shoppers
- cf9d029b70aa | Pick the right image format and swap GIFs for MP4
- 3c75d10544c6 | Name image files descriptively before upload
- b29f3cc2d36f | Order gallery images to answer customer questions
- dc287d5fb7e6 | Run a final image checklist before finishing a store
- 036e673a5a05 | Inspect rendered image dimensions to find wasted bandwidth
- 08b2e0e2f95d | Decide whether an image is worth resizing, compressing, or both
- 8dbbb42b9c2e | App Portfolio Triage: Only Keep Apps That Clearly Make Money
- ad877c2f348c | Use the Restaurant Analogy to Prioritize Above-the-Fold Loading
- 1dffb0dd47d1 | Defer Script Tags in theme.liquid, Then Fall Back to Async
- fdbc70a82f75 | Self-Host Third-Party Libraries in the Shopify Assets Folder
- b7d4c6046a25 | Understand How Shopify Injects App Scripts via content_for_header
- 621e302f651f | Compress and Resize Product and Hero Images Before Upload
- c9fcbc1b5513 | Set Image Upload Dimensions Slightly Above the Container Size
- 3dd6497a4d63 | Match Image Format to Use: JPEG Default, PNG for Transparency, MP4 Over GIF
- b4735bb55b51 | Preload Above-the-Fold Media and Lazy Load Everything Below
- 1eacf61a57a2 | Trim Custom Font Variations and Enable font-display: swap
- 637495534f7f | Choose a Simpler Theme Over a Feature-Rich One Unless Features Pay
- 02c570556e30 | Weigh Migrating an Old Theme vs. Rebuilding on Dawn or Horizon
- 943bdc967b80 | Recognize That Most Free Shopify Themes Are the Same Codebase
- d68b270990ab | Understand Horizon's Global Blocks vs. Dawn's Section-Scoped Blocks
- caf6d4c08b6d | Benchmark Theme Speed With an Apples-to-Apples Comparison
- 21280154cb29 | Keep Dawn for Now; Build New Stores on Horizon
- f00068c50316 | Diagnose CLS by Reading Google's Rendering Screenshots
- 7a213481a9d2 | Fix LCP by Un-lazy-loading and De-animating the Hero Image
- 37d2f02ad647 | Decide Whether Your Store Actually Needs a Good Speed Score
- 10d064e032f8 | Search a Downloaded Theme Folder for Residual App and Pixel Code
- 58c5589c135f | Audit Shopify theme files for leftover app code with a code editor
- 3a99be49f292 | Find and compress oversized non-product images in Shopify Files
- 68ca7da1a081 | Choose JPEG vs PNG vs GIF for store imagery
- 51db910ccfc8 | Lazy-load below-the-fold images but never the hero image
- 027af5f63b68 | Add font-display: swap to custom fonts to avoid render blocking
- 07b358e531fb | Add async or defer to third-party scripts after checking their purpose
- 4e05290f17d5 | Defer all app scripts until user interaction to cut blocking time
- d675d594782b | Prune unused apps and app embeds to reduce third-party load
- a8d01f5b91b6 | Plan a three-keyword SEO scheme per page with Google Keyword Planner
- 198c9b1e5856 | Optimize the store-level SEO title and meta description
- 1ba6eb3b6a8f | Rename generic product titles into keyword-rich H1 titles
- b5556041696c | Write substantive 100-400 word product and collection descriptions
- 66c68817418b | Write alt text and rename image files for SEO and accessibility
- 0894dbc180a6 | Set SEO-friendly URL handles with automatic redirects
- cdf20f6157c3 | Ensure each page has exactly one H1 tag
- bc59ae3525fa | Write 160-character meta descriptions for click-through
- 512774f2b241 | Use internal linking to speed up crawling and discovery
- 58bc1e28be27 | Verify mobile friendliness before treating SEO as complete
- 0d2d3621b19d | Use PageSpeed Insights for a baseline and install speed snippets
- 91fbb9ca7dd1 | Add rich snippets to earn larger search listings
- 73c6764d7c45 | Publish keyword-researched content at least twice a month
- d0b33b41e18d | Earn backlinks from authoritative sites and partners
- e42e8ace0dab | Set a primary domain and submit your sitemap to Search Console
- 3ef1ab6d1697 | Submit Sitemap and Set Primary Domain Before Google Indexing
- e482e075913e | Brand Asset Completeness for Sales Channel Syndication
- d075713968d8 | Use an SEO App Dashboard to Drive Pages Toward 100% Score
- 64042fc21a8b | Automate Image Compression Instead of One-by-One Optimization
- 9f00d339ffcc | Reclaim Stale Keywords and Add Rich Snippets via an SEO App
- 7678b95c31ff | Two Root Causes of Slow Shopify Stores: Layout Stability and Apps
- 2a89f4e58923 | Find App Scripts Injected via the async Function in Your Theme Head
- d1007a68a9e0 | Delay All App Scripts to Human Interaction via content_for_header
- b1f2c1da412b | Lazy-Load a Cookie Banner Script to Eliminate Its CLS and Blocking
- b711b4ded0ce | Lazy-Load App-Embed Widgets by Copying Their JS and CSS URLs
- 1d1dca3e3cfb | Audit theme.liquid for Scripts Missing defer or async
- 079f8ea11444 | Retest Speed Three Times and Average to Defeat Caching Lag
- a5d2c3aee970 | Find Layout Shift Sources by Throttling Network to Slow 3G
- dbf103b05b0a | Fix Theme-Level Layout Shift Caused by Body and Inline Styles
- b093ed3b4d75 | Mark the First Visible Item Eager, Keep the Rest Lazy
- 6427c0d96eec | Verify Each Lazy-Loaded App Still Works After Changing Loading
- cdc61c33e699 | Don't Trust Third-Party Caching Scripts on Shopify
- dca8734ae894 | Follow the Speed Work Order: Defer, Lazy-Load Apps, Fix CLS, Fix LCP
- 1b9747314efd | LCP diagnosis: the largest-in-viewport element and its delay source
- 481d00497deb | Handling loading="eager" vs loading="lazy" in collection and card loops
- d56347d58c66 | Splitting above-the-fold assets from lazy-loaded assets
- d16d1fcdd349 | CLS from images without dimensions: reserve space with width and height
- 24893ea78676 | Stopping app-widget CLS by reserving the widget container
- 14bc6ce5b8a6 | Matching fallback font metrics to the custom font to prevent font-swap CLS
- 68699dfd59de | Removing residual code from uninstalled apps and old tracking
- 9714159dd4aa | Deferring or lazy-loading app scripts so they don't block core content
- 98a7bf9f5fb4 | Lazy-loading Shopify's dynamic payment button script
- 3b3894441e6c | CSS that rewrites base styles from the body tag
- f21b8466aa36 | Fixing layout shift from the body tag with display:block
- 867a3ac29ede | Cookie banner modification via a theme property
- cce38d9369f2 | The seven-step Shopify speed framework and its order of operations
- 474204ae609c | Choosing app and functionality by value to protect speed
- c33439a2c9b9 | Testing protocol: three runs, averaged, on a duplicate theme
- 74187c8d7e19 | Simulating the real shopper's device and connection instead of your desk
- bf8e6e41254e | Product page mobile layout: get the add-to-cart within the visible band
- 00a97db32711 | Clarifying the promo message so shoppers can act on it
- 9b3008487ad5 | Diagnose Shopify's Composite Speed Score
- 80a761efcb18 | Set a CLS Target and Find Shifts in Lighthouse Trace
- cabcd2d4c66e | Recompile Critical CSS for Lazy-Loaded Theme CSS
- ba43a0aaa747 | Reserve Space for Widgets That Inject Late
- 56315833a352 | Defer or Lazy-Trigger App Scripts to Shield Core Assets
- adc3ea59042a | Assess Whether Each Blocking Script Is Visible or Pixels
- fde546149035 | Clean Residual Scripts After Uninstalling Apps
- 70af8654d12d | Right-Size Images and Pick the Correct Format
- 3c9bddfb47c1 | Use lazy-sizes for Bulletproof Image Lazy Loading
- ea1d2a527d10 | Font Loading: Add font-display: swap
- 15d23b16ff3c | Defer and Async Scripts to Prioritize Core Assets
- b73d08e8603c | Delay Non-Visible CSS with media-onload-Print
- 5f44ccb5ead1 | Evaluate Speed-Apps and Optimization Vendors Skeptically
- 5e79bed9130e | Check Page Vitals Before Trusting Them
- 81ac749043da | Reproduce the Original Page-Speed Audit Method
