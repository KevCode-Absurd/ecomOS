"""Build the founder-facing speed page: plain English, one list of fixes, saved decisions.

Usage: python3 speed_lab/build_founder_page.py
Uses arm A's measured chain (the recommended shipping order). Decisions are stored in the page's db.
"""
import base64, io, json, os
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(ROOT, "results")
OUT = os.path.join(os.path.dirname(ROOT), "reviews", "speed-lab", "gehna-speed-plan.html")

FIXES = [
    {"id": "rocket-loader", "var": "arm-a-f01", "title": "Stop a Cloudflare add-on that delays your page's own code",
     "what": "A setting called Rocket Loader holds back the code that builds your page and runs it one piece at a time. Turning it off lets the page build straight away.",
     "needs": "One switch in your Cloudflare settings. No code change.", "tradeoff": "None seen. On its own this fix makes the page slower until the font fix below ships with it, so the two go live together.", "who": "Developer, under an hour"},
    {"id": "korean-fonts", "var": "arm-a-f02", "title": "Shrink two huge font files",
     "what": "Two font files carry every Korean character even though your site only shows English. Keeping only the letters you use cuts 6 MB to under 100 KB on every visit.",
     "needs": "Replace two font files in the site build.", "tradeoff": "None. The letters your pages use, including the rupee sign, stay in.", "who": "Developer, about half a day"},
    {"id": "tags-later", "var": "arm-a-f03", "title": "Let the page show before the marketing trackers load",
     "what": "Google, Meta, Klaviyo and Clarity trackers load before the page is ready for the visitor. Loading them right after the page is ready makes the page usable much sooner.",
     "needs": "A one-line change per tracker in the site code.", "tradeoff": "A visitor who leaves within about 5 seconds on a slow connection is not counted by the trackers. Your marketing team should agree to this first.", "who": "Developer, about an hour"},
    {"id": "icons", "var": "arm-a-f04", "title": "Send smaller category icons",
     "what": "The small category icons on the homepage are sent at about 10 times the size they are shown. Sending the right size saves 170 KB per visit.",
     "needs": "Set the icon size in the site code.", "tradeoff": "None visible. The icons look the same.", "who": "Developer, under an hour"},
    {"id": "lato-font", "var": "arm-a-f05", "title": "Use the modern format for the second font",
     "what": "Your main text font is sent in an old, uncompressed format. The modern format is about half the size and loads sooner, so the main banner appears faster.",
     "needs": "Replace two font files in the site build.", "tradeoff": "None.", "who": "Developer, about an hour"},
    {"id": "hero-preload", "var": "arm-a-f06", "title": "Load the main banner image first",
     "what": "The big banner is the first thing people look at, but the browser only finds it late. Telling the browser to fetch it first shows it about a quarter of a second sooner.",
     "needs": "One line in the page code.", "tradeoff": "None.", "who": "Developer, under an hour"},
    {"id": "inline-css", "var": "arm-a-f08", "title": "Put the page's styling inside the page",
     "what": "The page waits for two small style files before it can show anything at all. Placing them inside the page removes that wait, so the first thing appears about a quarter of a second sooner.",
     "needs": "A build setting in the site code.", "tradeoff": "None.", "who": "Developer, about an hour"},
    {"id": "old-analytics", "var": "arm-a-f09", "title": "Remove an old Google Analytics tag that no longer works",
     "what": "Google stopped collecting data from the old Universal Analytics in July 2023, but the tag still loads on every visit. Removing it saves 150 KB and changes nothing else.",
     "needs": "Delete one tag in Google Tag Manager.", "tradeoff": "None. Your current Google Analytics keeps working.", "who": "Marketing or developer, minutes"},
]


def med(label):
    m = json.load(open(os.path.join(RES, label + ".json")))["median"]
    return {"load": m["load_ms"], "lcp": m["lcp_ms"], "fcp": m["fcp_ms"], "bytes": m["wire_bytes"]}


def shot(label, width=300):
    im = Image.open(os.path.join(RES, label + "-run1.png")).convert("RGB")
    h = int(im.height * width / im.width)
    im = im.resize((width, h), Image.LANCZOS).crop((0, 0, width, min(h, 640)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=66, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


BRIEFS = {
"rocket-loader": "Change: turn off Cloudflare Rocket Loader for www.gehnaindia.com.\nWhere: Cloudflare dashboard > the gehnaindia.com zone > Speed > Optimization > Content Optimization > Rocket Loader: Off.\nWhy: Rocket Loader rewrites all 31 Next.js script tags to type=\"text/rocketscript\" and runs them one at a time after the load event. The browser's preload scanner cannot see them, and when fonts get faster it re-fetches about 20 scripts one by one, so the product carousel appears late.\nShip with: the font subset change (fix 2) in the same release. Rocket Loader off on its own made the page slower in our test (load 15.4 s to 22.4 s) until the fonts were fixed too.\nCheck: view-source of the homepage must show <script src=\"/_next/static/chunks/...\" defer> with no type=\"text/rocketscript\" and no rocket-loader.min.js. On a throttled mobile profile (slow 4G, 4x CPU) the first GraphQL call should move from about 17 s to about 5 s after navigation.\nRollback: switch Rocket Loader back on in the same dashboard setting. Takes effect within minutes.",
"korean-fonts": "Change: replace the two NanumMyeongjo font files (weights 400 and 700, /_next/static/media/14a3fceaeabbcb56-s.p.ttf and ae1a48c074c123e8-s.p.ttf, about 3 MB each) with Latin subsets in WOFF2, and preload the subsets instead of the TTFs.\nHow: with next/font/google use subsets: ['latin'] and display: 'swap' (Next.js then emits WOFF2 subsets and the preload). If the font is local, build the subset with fontTools:\n  pyftsubset NanumMyeongjo-Regular.ttf --unicodes=\"U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+20B9,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD\" --flavor=woff2 --layout-features=\"*\" --output-file=nanum-400-latin.woff2\n  Repeat for the 700 weight. Keep U+20B9 (the rupee sign) in the range.\nAlso: keep a second @font-face per weight for the remaining code points with a unicode-range, so any non-Latin glyph still loads on demand. Our test did this and glyph coverage was unchanged.\nCheck: the two font requests on the homepage drop from about 1.1 MB each on the wire to under 50 KB each. Body text renders in the same face (compare a screenshot). Total page weight falls by about 2 MB.\nRollback: restore the previous font config and redeploy.",
"tags-later": "Change: load the third-party tags after the page load event instead of right after hydration.\nWhere: pages/_app (the file that renders the next/script tags). For these Script elements change strategy=\"afterInteractive\" to strategy=\"lazyOnload\": Google Tag Manager (GTM-PK4C6HK), Klaviyo, the Meta pixel, Clarity, Google Ads, CustomerLabs. Leave any consent script as it is.\nAlso add, as the first inline script in <head>: window.dataLayer = window.dataLayer || []; window.gtag = window.gtag || function(){ dataLayer.push(arguments); };  This queues any gtag() event fired before the tags arrive, so events are delayed rather than lost.\nTrade-off to confirm with marketing: a visitor who leaves within about 5 seconds on a slow connection will not be counted by GA4, Ads, Meta, Klaviyo or Clarity. Test every key event (page view, add to cart, purchase) with consent on and off after the change.\nCheck: on a throttled mobile profile the load event fires at about 6 s instead of about 14 s, and the tag requests start after it. All tag endpoints still fire within a few seconds of load.\nRollback: change the strategies back to afterInteractive and remove the stub.",
"icons": "Change: request smaller files for the 7 category icons in the first screen.\nWhere: the category icon component uses next/image with width={200}. They render at 60 x 60 CSS px. Set width={128} height={128} (or sizes=\"60px\"), so the srcset becomes w=128 1x and w=256 2x instead of w=256 and w=640.\nCheck: on a phone the icon requests should fetch the 256 px files, about 60 KB total for the 7 icons instead of about 229 KB. The icons must look the same at 60 px (compare a screenshot at 2x or 3x device pixel ratio).\nRollback: restore width={200}.",
"lato-font": "Change: serve Lato 400 and 700 as Latin WOFF2 subsets instead of TTF (/_next/static/media/2c00c297d3cdabf8-s.p.ttf and 4291f48c2ea51320-s.p.ttf, about 75 KB each).\nHow: same method as the NanumMyeongjo change. With next/font/google use Lato with subsets: ['latin']; if local, run pyftsubset with the same unicode range and --flavor=woff2, and keep a unicode-range fallback face for the remaining code points.\nCheck: the two Lato requests drop to about 20 KB each and are WOFF2. Text renders in the same face. On a throttled profile the banner (LCP) should show about 200 ms sooner because the preloaded fonts stop competing with the banner image.\nRollback: restore the previous font files and preload links.",
"hero-preload": "Change: preload the first hero banner image so the browser fetches it before the scripts and fonts.\nWhere: the hero slider component. Give the first slide's next/image priority={true}. Next.js then emits, in <head>, <link rel=\"preload\" as=\"image\" fetchpriority=\"high\" imagesrcset=\"...\" imagesizes=\"...\"> for it. Only the first slide gets priority; the other slides stay lazy.\nCheck: view-source shows the preload link before the font preloads. On a throttled mobile profile LCP improves by about 130 ms; the banner request starts within the first 100 ms of the load.\nRollback: remove priority from the first slide.",
"inline-css": "Change: inline the two render-blocking stylesheets (the global CSS and the page CSS, about 8 KB gzipped together) into the HTML instead of linking them.\nHow: enable experimental.optimizeCss (Critters) in next.config.js, or inline them in a custom _document. If inlining by hand, keep the page stylesheet in a <style data-n-href=\"/_next/static/css/<hash>.css\"> element, because Next.js uses that element to swap page CSS on client-side navigation. Remove the matching <link rel=\"preload\" as=\"style\"> and <link rel=\"stylesheet\"> tags.\nCheck: first contentful paint on a throttled mobile profile improves by about 200 ms (740 ms to about 520 ms). Client-side navigation to a product page must still be styled correctly. The banner can get about 100 ms later because scripts start sooner; that is expected and the net effect is positive.\nRollback: disable the setting or restore the link tags.",
"old-analytics": "Change: remove the Universal Analytics tag.\nWhere: in pages/_app, delete the next/script element with id=\"ga-global-script\" that loads https://www.googletagmanager.com/gtag/js?id=UA-41818105-2, and the line gtag('config', 'UA-41818105-2', {...}). Keep the inline dataLayer and gtag() definition and gtag('js', new Date()), since other calls use them. If the UA tag is also configured inside Google Tag Manager, pause it there too.\nWhy: Google stopped processing hits for standard Universal Analytics properties on 1 July 2023. The tag still costs about 133 KB per visit and about 50 ms of script time on a slow phone. GA4 (G-FT109JXEC7) and Google Ads (AW-982480202) are not affected.\nCheck: no request to gtag/js?id=UA-41818105-2 on any page. GA4 real-time report still shows visits.\nRollback: restore the two lines."
}
for f in FIXES:
    f["brief"] = BRIEFS[f["id"]]

base = med("baseline")
steps = [dict(f, m=med(f["var"]), shot=shot(f["var"])) for f in FIXES]
final = steps[-1]["m"]
data = {"base": base, "base_shot": shot("baseline"), "steps": steps}


def s(x): return f"{x/1000:.1f} seconds"
def mb(x): return f"{x/1048576:.1f} MB"


page = f'''<title>Gehna Speed Plan</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&display=swap">
<style>
:root{{--bg:#F7F5F0;--panel:#FFFFFF;--ink:#1E1C19;--muted:#6B665D;--line:#DDD8CD;--accent:#8E6A1C;--accent-ink:#FFFFFF;--good:#2F6B3A;--goodbg:#E6F0E7;--warn:#9A5A0A;--warnbg:#F6EBD9;--code:#EFECE4;
--display:'Sora',system-ui,sans-serif;--body:'Source Sans 3',system-ui,sans-serif}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#17161A;--panel:#211F24;--ink:#EDEAE3;--muted:#A49E92;--line:#3A373F;--accent:#D8AE52;--accent-ink:#1E1C19;--good:#7CC48A;--goodbg:#1F2E22;--warn:#E0A552;--warnbg:#332A1C;--code:#2B2930;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#17161A;--panel:#211F24;--ink:#EDEAE3;--muted:#A49E92;--line:#3A373F;--accent:#D8AE52;--accent-ink:#1E1C19;--good:#7CC48A;--goodbg:#1F2E22;--warn:#E0A552;--warnbg:#332A1C;--code:#2B2930;color-scheme:dark}}
body{{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:17px;line-height:1.55;padding-inline:16px;padding-block:0 60px}}
main{{max-width:860px;margin:0 auto}}
h1{{font-family:var(--display);font-size:clamp(26px,4vw,36px);font-weight:700;letter-spacing:-.015em;margin:30px 0 8px;text-wrap:balance}}
h2{{font-family:var(--display);font-size:21px;margin:34px 0 10px;text-wrap:balance}}
p{{max-width:66ch;margin:0 0 10px}} .muted{{color:var(--muted)}}
.now{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px;margin:16px 0 6px}}
.tile{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px}}
.tile .l{{font:600 12px var(--display);letter-spacing:.05em;text-transform:uppercase;color:var(--muted)}}
.tile .v{{font:700 26px var(--display);margin-top:2px;letter-spacing:-.01em;font-variant-numeric:tabular-nums}}
.tile .v.after{{color:var(--good)}}
.tile .s{{font-size:13px;color:var(--muted)}}
.tile .bar{{height:8px;background:var(--code);border-radius:4px;overflow:hidden;margin-top:8px}} .tile .bar i{{display:block;height:100%;background:var(--accent);border-radius:4px;transition:width .35s}}
.ctl{{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 4px}}
.ctl button,.card button{{font:600 14px var(--display);padding:9px 14px;border-radius:999px;border:1px solid var(--line);background:var(--panel);color:var(--ink);cursor:pointer}}
.ctl button.primary{{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}}
.list{{display:grid;gap:12px;margin:14px 0}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 18px;display:grid;grid-template-columns:44px 1fr;gap:12px}}
.card.on{{border-color:var(--accent)}}
.card .n{{font:700 20px var(--display);color:var(--accent);line-height:1.1}}
.card h3{{font-family:var(--display);font-size:18px;margin:0 0 6px;text-wrap:balance}}
.card .what{{margin:0 0 8px}}
.card dl{{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;margin:0 0 10px;font-size:15px}}
.card dt{{font-weight:600;color:var(--muted)}} .card dd{{margin:0}}
.card .gain{{display:inline-block;background:var(--goodbg);color:var(--good);border-radius:6px;padding:4px 8px;font:600 14px var(--display);margin-bottom:8px}}
.card .gain.none{{background:var(--code);color:var(--muted)}}
.card .warn{{display:inline-block;background:var(--warnbg);color:var(--warn);border-radius:6px;padding:4px 8px;font-size:14px;margin-bottom:8px}}
.card .row{{display:flex;gap:8px;flex-wrap:wrap;align-items:center}}
.card button.approve{{border-color:var(--good);color:var(--good)}} .card button.approve.sel{{background:var(--good);color:#fff}}
.card button.hold{{border-color:var(--warn);color:var(--warn)}} .card button.hold.sel{{background:var(--warn);color:#fff}}
.card input{{font:15px var(--body);padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);min-width:220px;flex:1}}
.card .saved{{font-size:13px;color:var(--muted)}}
.card button.dev{{border-color:var(--accent);color:var(--accent)}} .card button.dev.sel{{background:var(--accent);color:var(--accent-ink)}}
.modal[hidden]{{display:none}}
.modal{{position:fixed;inset:0;background:rgba(20,18,14,.55);display:flex;align-items:center;justify-content:center;padding:16px;z-index:20}}
.mbox{{background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:12px;max-width:760px;width:100%;max-height:90vh;overflow:auto;padding:16px 18px}}
.mhead{{display:flex;justify-content:space-between;align-items:center;gap:10px}} .mhead h3{{font-family:var(--display);font-size:18px;margin:0}}
.mhead button,#mcopy{{font:600 14px var(--display);padding:8px 14px;border-radius:999px;border:1px solid var(--line);background:var(--panel);color:var(--ink);cursor:pointer}}
#mcopy{{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}}
#mbody{{white-space:pre-wrap;font:14px/1.5 var(--body);background:var(--code);padding:12px;border-radius:8px;margin:10px 0}}
.modal .row{{display:flex;gap:10px;align-items:center;flex-wrap:wrap}}
.shots{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:14px 0}}
.shots figure{{margin:0;min-width:0}} .shots img{{width:100%;border:1px solid var(--line);border-radius:8px;display:block}} .shots figcaption{{font-size:13px;color:var(--muted);margin-top:4px}}
.box{{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:10px;padding:14px 18px;max-width:72ch}}
.small{{font-size:14px;color:var(--muted);max-width:72ch}}
button:focus-visible,input:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
@media (max-width:560px){{.card{{grid-template-columns:32px 1fr}} .shots{{grid-template-columns:1fr}}}}
@media (prefers-reduced-motion: reduce){{.tile .bar i{{transition:none}}}}
</style>
<main>
<h1>Your homepage on a slow phone connection, and 8 ways to make it faster</h1>
<p class="muted">We copied your homepage exactly as it is today and loaded it the way a shopper on a weak 4G signal would. Then we tried 8 changes, one at a time, and measured each one. Nothing here changes what the page shows or sells. Press "Show the next fix" to see what each change does, then approve the ones you want your developer to ship.</p>

<div class="now" id="tiles"></div>
<div class="ctl"><button class="primary" id="next">Show the next fix</button><button id="back">Go back one</button><button id="all">Show all 8</button><button id="reset">Start over</button></div>
<div class="shots"><figure><img src="{data["base_shot"]}" alt="Homepage today, above the fold"><figcaption>Today</figcaption></figure><figure><img id="afterimg" src="{data["base_shot"]}" alt="Homepage after the fixes shown"><figcaption id="aftercap">No fix shown yet</figcaption></figure></div>
<p class="small">The top banner rotates on its own, so the two pictures can show different slides. That is the page working as usual, not a change.</p>

<h2>The fixes, in the order to ship them</h2>
<div class="list" id="list"></div>

<h2>What we cannot fix from outside</h2>
<div class="box"><p>After the page arrives, its code keeps the phone busy for about 2.4 seconds building the page. None of the 8 fixes change that. It needs your developers to rework the app itself, which is a bigger project. Worth doing after the 8 fixes above are live.</p></div>

<h2>What happens next</h2>
<p>"Let the agent do it" asks ecomOS to prepare the change on a copy of the site for you to review; nothing changes on the live site until you say so. "Send to developer" opens the exact instructions to copy and send. Fixes 1 and 2 go live together. Fix 3 waits for your marketing team's yes. The rest can ship any time.</p>
<p class="small">How we measured: a Pixel 5 phone profile on a slow 4G connection, 3 loads per version, the middle result. "Fully loaded" is when everything on the page has arrived. "Banner shows" is when the big top image is on screen. Real visits will be slower than these numbers because they also include your server and network, but the savings carry over.</p>
</main>
<div id="modal" class="modal" hidden><div class="mbox" role="dialog" aria-modal="true" aria-labelledby="mtitle"><div class="mhead"><h3 id="mtitle">Instructions</h3><button id="mclose" aria-label="Close">Close</button></div><p class="small">Copy this and send it to your developer as it is. It says what to change, where, how to check it worked, and how to undo it.</p><pre id="mbody"></pre><div class="row"><button id="mcopy" class="primary">Copy instructions</button><span class="saved" id="mcopied"></span></div></div></div>
<script>
const D = {json.dumps(data)};
let n = 0; let db = null; const decisions = {{}};
const sec = x => (x/1000).toFixed(1) + ' s';
const mb = x => (x/1048576).toFixed(1) + ' MB';
const TILES = [['load','Fully loaded',sec],['lcp','Banner shows',sec],['fcp','First thing on screen',sec],['bytes','Downloaded per visit',mb]];
function cur(){{ return n===0 ? D.base : D.steps[n-1].m; }}
function renderTiles(){{
  const c = cur(); let h='';
  for(const [k,l,f] of TILES){{ const d = c[k]-D.base[k]; const pct = Math.round(-d/D.base[k]*100); const w=Math.max(3,Math.round(c[k]/D.base[k]*100));
    h += `<div class="tile"><div class="l">${{l}}</div><div class="v ${{n>0&&d<0?'after':''}}">${{f(c[k])}}</div><div class="s">${{n===0?'today':(d<0?pct+'% faster than today':(d>0?'slightly slower than today':'same as today'))}}</div><div class="bar"><i style="width:${{w}}%"></i></div></div>`; }}
  document.getElementById('tiles').innerHTML=h;
  document.getElementById('afterimg').src = n===0 ? D.base_shot : D.steps[n-1].shot;
  document.getElementById('aftercap').textContent = n===0 ? 'No fix shown yet' : 'With fixes 1 to '+n;
  document.getElementById('next').disabled = n>=D.steps.length; document.getElementById('back').disabled = n===0;
}}
function renderList(){{
  const el=document.getElementById('list'); el.innerHTML='';
  D.steps.forEach((s,i)=>{{
    const prev = i===0 ? D.base : D.steps[i-1].m;
    const dl = s.m.load-prev.load, dlcp = s.m.lcp-prev.lcp, dfcp = s.m.fcp-prev.fcp, db_ = s.m.bytes-prev.bytes;
    const gains=[]; if(dl<-150) gains.push('page fully loads '+(-dl/1000).toFixed(1)+' s sooner'); if(dlcp<-80) gains.push('banner shows '+Math.round(-dlcp)+' ms sooner'); if(dfcp<-80) gains.push('first paint '+Math.round(-dfcp)+' ms sooner'); if(db_<-50000) gains.push(mb(-db_)+' less to download');
    const gain = gains.length ? `<span class="gain">On its own: ${{gains.join(', ')}}</span>` : `<span class="gain none">Small on its own, part of the set</span>`;
    const warn = s.tradeoff.startsWith('None') ? '' : `<span class="warn">Trade-off: ${{s.tradeoff}}</span>`;
    const dec = decisions[s.id] || {{}};
    const card=document.createElement('div'); card.className='card'+(i<n?' on':''); card.innerHTML=`<div class="n">${{i+1}}</div><div>
      <h3>${{s.title}}</h3><p class="what">${{s.what}}</p>${{gain}} ${{warn}}
      <dl><dt>Needs</dt><dd>${{s.needs}}</dd><dt>Who and how long</dt><dd>${{s.who}}</dd>${{warn?'':'<dt>Trade-off</dt><dd>'+s.tradeoff+'</dd>'}}</dl>
      <div class="row"><button class="approve ${{dec.decision==='agent'?'sel':''}}" data-id="${{s.id}}" data-d="agent">Let the agent do it</button><button class="dev ${{dec.decision==='developer'?'sel':''}}" data-id="${{s.id}}" data-d="developer">Send to developer</button><button class="hold ${{dec.decision==='hold'?'sel':''}}" data-id="${{s.id}}" data-d="hold">Not now</button></div>
      <div class="row" style="margin-top:6px"><input id="r-${{s.id}}" placeholder="A short reason or note (optional)" value="${{(dec.reason||'').replace(/"/g,'&quot;')}}"><span class="saved" id="s-${{s.id}}">${{dec.at?('saved: '+({{agent:'agent will do it',developer:'sent to developer',hold:'not now'}}[dec.decision]||dec.decision)+', '+new Date(dec.at).toLocaleDateString()):''}}</span></div></div>`;
    el.appendChild(card);
  }});
  el.querySelectorAll('button[data-id]').forEach(b=>b.addEventListener('click',()=>{{ if(b.dataset.d==='developer') openBrief(b.dataset.id); save(b.dataset.id,b.dataset.d); }}));
}}
function openBrief(id){{
  const s=D.steps.find(x=>x.id===id); const i=D.steps.indexOf(s)+1;
  const text = 'Gehna homepage speed fix '+i+' of 8: '+s.title+'\\n\\n'+s.brief+'\\n\\nMeasured on a copy of the live homepage, 25 Sep 2026, Pixel 5 profile on slow 4G. Questions: reply to this message.';
  document.getElementById('mtitle').textContent = 'Fix '+i+': '+s.title;
  document.getElementById('mbody').textContent = text;
  document.getElementById('mcopied').textContent='';
  document.getElementById('modal').hidden=false; document.body.style.overflow='hidden';
  document.getElementById('mcopy').focus();
}}
function closeBrief(){{ document.getElementById('modal').hidden=true; document.body.style.overflow=''; }}
document.getElementById('mclose').onclick=closeBrief;
document.getElementById('modal').addEventListener('click',e=>{{ if(e.target.id==='modal') closeBrief(); }});
document.addEventListener('keydown',e=>{{ if(e.key==='Escape') closeBrief(); }});
document.getElementById('mcopy').onclick=async()=>{{
  const t=document.getElementById('mbody').textContent; const st=document.getElementById('mcopied');
  try{{ await navigator.clipboard.writeText(t); st.textContent='Copied. Paste it into a message to your developer.'; }}
  catch(e){{ const r=document.createRange(); r.selectNodeContents(document.getElementById('mbody')); const sel=getSelection(); sel.removeAllRanges(); sel.addRange(r); st.textContent='Select all is done. Press Ctrl+C or Cmd+C to copy.'; }}
}};
async function save(id,decision){{
  const reason=(document.getElementById('r-'+id).value||'').slice(0,300); const body={{decision,reason,at:new Date().toISOString(),fix:id}};
  decisions[id]=body; renderList();
  const st=document.getElementById('s-'+id);
  if(!db){{ try{{localStorage.setItem('gehna-speed-decisions',JSON.stringify(decisions));}}catch(e){{}} st.textContent='saved on this device only'; return; }}
  try{{ await db.doc('decisions/'+id).set(body); st.textContent='saved'; }}catch(e){{ st.textContent='could not save ('+(e&&e.code||'error')+')'; }}
}}
document.getElementById('next').onclick=()=>{{n=Math.min(n+1,D.steps.length);renderTiles();renderList();}};
document.getElementById('back').onclick=()=>{{n=Math.max(0,n-1);renderTiles();renderList();}};
document.getElementById('all').onclick=()=>{{n=D.steps.length;renderTiles();renderList();}};
document.getElementById('reset').onclick=()=>{{n=0;renderTiles();renderList();}};
try{{ Object.assign(decisions, JSON.parse(localStorage.getItem('gehna-speed-decisions')||'{{}}')); }}catch(e){{}}
renderTiles(); renderList();
(async()=>{{ try{{ db = await (window.claude && window.claude.use ? window.claude.use('db') : Promise.resolve(null)); }}catch(e){{ db=null; }}
  if(!db) return;
  db.collection('decisions').onSnapshot(snap=>{{ snap.docs.forEach(d=>{{ if(d.exists) decisions[d.id]=d.data(); }}); renderList(); }}, ()=>{{}});
}})();
</script>
'''
open(OUT, "w", encoding="utf-8").write(page)
print(OUT, len(page) // 1024, "KB; final", final)
