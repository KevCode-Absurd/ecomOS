"""F02: turn off Cloudflare Rocket Loader in what the browser receives. Rocket Loader rewrites every Next.js
<script defer> tag to type="<hash>-text/javascript", then re-inserts the 31 scripts itself and runs them one
by one. The fix restores the tags Next.js emits (plain defer scripts) and drops the rocket-loader.min.js tag.
Same as switching Rocket Loader off in Cloudflare (Speed > Optimization > Content Optimization).
Parent: arm-b-f01."""
from common import fresh, put_text, get_text, HOME

NAME, PARENT = "arm-b-f02", "arm-b-f01"
PREFIX = "2ac945fd2ac69580976d0ac0"
RL_TAG = f'<script src="/cdn-cgi/scripts/7d0fa10a/cloudflare-static/rocket-loader.min.js" data-cf-settings="{PREFIX}-|49" defer></script>'


def main():
    v = fresh(NAME, PARENT)
    html = get_text(v, HOME)
    n = html.count(f' type="{PREFIX}-text/javascript"')
    assert n == 31, n
    html = html.replace(f' type="{PREFIX}-text/javascript"', "")
    assert html.count(RL_TAG) == 1
    html = html.replace(RL_TAG, "")
    assert PREFIX not in html
    put_text(v, HOME, html, "text/html; charset=utf-8")
    print("built", NAME, "scripts restored:", n)


if __name__ == "__main__":
    main()
