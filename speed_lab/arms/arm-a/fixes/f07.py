"""f07: Cloudflare email obfuscation adds email-decode.min.js as a parser-blocking script in the body, just
before __NEXT_DATA__ (Chrome marks it render-blocking). It costs one extra round trip before the parser
can finish and before first paint. Fix: load it with defer. It still runs before DOMContentLoaded and still
turns the 2 protected mailto links back into addresses. In production: turn off Email Address Obfuscation
in Cloudflare and render the address directly, or keep it and accept one round trip.
"""
from common import fresh, put_text, get_text, HOME

NAME, PARENT = "arm-a-f07", "arm-a-f06"
OLD = '<script data-cfasync="false" src="/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js"></script>'
NEW = '<script data-cfasync="false" defer src="/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js"></script>'


def main():
    v = fresh(NAME, PARENT)
    doc = get_text(v, HOME)
    assert doc.count(OLD) == 1
    put_text(v, HOME, doc.replace(OLD, NEW), "text/html; charset=utf-8")
    print("email-decode deferred")


if __name__ == "__main__":
    main()
