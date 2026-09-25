"""F08: make Cloudflare's email-decode.min.js non-blocking. It sits as a parser-blocking <script> in the body
(Chrome marks it render-blocking status "blocking" in the baseline) before __NEXT_DATA__. The fix moves it
into <head> with defer, ahead of the Next.js defer scripts, so it still runs before hydration (defer scripts
run in document order after parsing) and still decodes the one obfuscated e-mail link, but the parser no
longer stops for its round trip. Email Obfuscation stays on. Parent: arm-b-f07."""
from common import fresh, put_text, get_text, HOME

NAME, PARENT = "arm-b-f08", "arm-b-f07"
TAG = '<script data-cfasync="false" src="/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js"></script>'
FIRST_NEXT = '<script defer="" nomodule="" src="/_next/static/chunks/polyfills-42372ed130431b0a.js"></script>'


def main():
    v = fresh(NAME, PARENT)
    html = get_text(v, HOME)
    assert html.count(TAG) == 1 and html.count(FIRST_NEXT) == 1
    html = html.replace(TAG, "")
    html = html.replace(FIRST_NEXT, '<script defer data-cfasync="false" src="/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js"></script>' + FIRST_NEXT)
    put_text(v, HOME, html, "text/html; charset=utf-8")
    print("built", NAME)


if __name__ == "__main__":
    main()
