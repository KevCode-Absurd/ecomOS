"""f03: The app injects its tags with next/script strategy "afterInteractive": GTM (which then pulls gtag
for G- and AW-, Clarity, Google Ads, Merchant Center), the old UA gtag, Klaviyo (10 files), Meta pixel and
CustomerLabs. After f02 they start right after hydration and keep the window load event open to 13.8 s.
Fix: switch those six Script tags to strategy "lazyOnload" (Next.js runs them after the load event, in
requestIdleCallback). A two-line stub in <head> defines window.dataLayer and window.gtag first, so
gtag() events fired before the tags arrive are queued in dataLayer instead of being dropped.
"""
from common import fresh, put_text, get_text, HOME, APP_JS

NAME, PARENT = "arm-a-f03", "arm-a-f02"
IDS = ["gtm-script", "customer-labs-script", "ga-global-script", "ga-pageview-script", "klaviyo-script", "fb-pixel-script"]
STUB = '<script>window.dataLayer=window.dataLayer||[];window.gtag=window.gtag||function(){dataLayer.push(arguments)};</script>'
ANCHOR = '<meta name="next-head-count" content="17"/>'


def main():
    v = fresh(NAME, PARENT)
    js = get_text(v, APP_JS)
    for i in IDS:
        old_a = f'id:"{i}",strategy:"afterInteractive"'
        old_b = f'id:"{i}",type:"text/javascript",strategy:"afterInteractive"'
        if old_a in js:
            js = js.replace(old_a, f'id:"{i}",strategy:"lazyOnload"')
        elif old_b in js:
            js = js.replace(old_b, f'id:"{i}",type:"text/javascript",strategy:"lazyOnload"')
        else:
            raise SystemExit(f"not found: {i}")
    put_text(v, APP_JS, js, "application/javascript")
    doc = get_text(v, HOME)
    assert ANCHOR in doc and STUB not in doc
    doc = doc.replace(ANCHOR, ANCHOR + STUB)
    put_text(v, HOME, doc, "text/html; charset=utf-8")
    print("lazyOnload:", ", ".join(IDS), "| remaining afterInteractive:", js.count('strategy:"afterInteractive"'))


if __name__ == "__main__":
    main()
