"""F03: load the 7 third-party tags in _app (GTM, CustomerLabs, the UA gtag loader and its config snippet,
Klaviyo, Tagalys, Meta pixel) with next/script strategy "lazyOnload" instead of "afterInteractive".
lazyOnload waits for the window load event and then for browser idle (requestIdleCallback) before it
inserts each tag, so the tags no longer compete with first-party JS and images or hold back the load event.
Only the strategy string changes; every tag still loads on every page view. Parent: arm-b-f02."""
from common import fresh, put_text, get_text

NAME, PARENT = "arm-b-f03", "arm-b-f02"
APP = "https://www.gehnaindia.com/_next/static/chunks/pages/_app-dce0792d73ac490d.js"
IDS = ["gtm-script", "customer-labs-script", "ga-global-script", "ga-pageview-script", "klaviyo-script", "tagalys-script", "fb-pixel-script"]


def main():
    v = fresh(NAME, PARENT)
    js = get_text(v, APP)
    assert js.count('strategy:"afterInteractive"') == 7
    for i in IDS:
        a = js.find(f'id:"{i}"'); assert a > 0, i
        b = js.find('strategy:"afterInteractive"', a)
        assert 0 < b - a < 80, (i, b - a)
        js = js[:b] + 'strategy:"lazyOnload"' + js[b + len('strategy:"afterInteractive"'):]
    assert js.count('strategy:"afterInteractive"') == 0 and js.count('strategy:"lazyOnload"') == 7
    put_text(v, APP, js, "text/javascript")
    print("built", NAME)


if __name__ == "__main__":
    main()
