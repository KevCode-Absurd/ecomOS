"""f09: The app still loads the Universal Analytics gtag (gtag/js?id=UA-41818105-2, 133 KB wire, about 50 ms of
script evaluation on this profile) and sends a config for it. Google's help page says standard UA properties
stopped processing hits on 1 July 2023 (360 properties on 1 July 2024), so this tag collects nothing.
GA4 (G-FT109JXEC7) and Google Ads (AW-982480202) are loaded by GTM and are not touched.
Fix: drop the ga-global-script element and the UA config line. The inline dataLayer and gtag() definition
and gtag('js') stay, so every other gtag() call keeps working.
"""
from common import fresh, put_text, get_text, APP_JS

NAME, PARENT = "arm-a-f09", "arm-a-f08"
EL = '(0,h.jsx)(re(),{id:"ga-global-script",strategy:"lazyOnload",src:"https://www.googletagmanager.com/gtag/js?id=UA-41818105-2"}),'
CFG = "gtag('config', 'UA-41818105-2', {'allow_enhanced_conversions': true});"


def main():
    v = fresh(NAME, PARENT)
    js = get_text(v, APP_JS)
    assert js.count(EL) == 1 and js.count(CFG) == 1
    js = js.replace(EL, "").replace(CFG, "")
    assert "UA-41818105" not in js
    put_text(v, APP_JS, js, "application/javascript")
    print("UA loader and config removed")


if __name__ == "__main__":
    main()
