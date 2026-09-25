"""F07: stop loading the dead Universal Analytics tag. _app loads gtag/js?id=UA-41818105-2 (133 KB on the wire)
and sends gtag('config', 'UA-41818105-2'), which also pulls google-analytics.com/analytics.js (21 KB).
Standard Universal Analytics properties stopped processing hits on 1 July 2023 (web_log.md #1), so these
bytes feed nothing. The fix removes the UA loader element and the UA config call. It keeps the inline
snippet that defines window.dataLayer and window.gtag, because the app calls window.gtag("set","user_data",...)
and GTM (which loads the live GA4 G-FT109JXEC7 and Ads AW-982480202 tags) reads the same dataLayer.
Parent: arm-b-f06."""
from common import fresh, put_text, get_text

NAME, PARENT = "arm-b-f07", "arm-b-f06"
APP = "https://www.gehnaindia.com/_next/static/chunks/pages/_app-dce0792d73ac490d.js"
LOADER = '(0,h.jsx)(re(),{id:"ga-global-script",strategy:"lazyOnload",src:"https://www.googletagmanager.com/gtag/js?id=UA-41818105-2"}),'
CONFIG = "gtag('config', 'UA-41818105-2', {'allow_enhanced_conversions': true});"


def main():
    v = fresh(NAME, PARENT)
    js = get_text(v, APP)
    assert js.count(LOADER) == 1 and js.count(CONFIG) == 1
    js = js.replace(LOADER, "").replace(CONFIG, "")
    assert "UA-41818105" not in js
    put_text(v, APP, js, "text/javascript")
    print("built", NAME)


if __name__ == "__main__":
    main()
