"""f01: Cloudflare Rocket Loader rewrites all 31 Next.js script tags to an unknown type, so the browser's
preload scanner cannot see them. rocket-loader.min.js (loaded with defer at the end of the body) then
preloads them, runs them one by one after the window load event, and re-fetches any preload the load
event cut off. Fix: serve the scripts as Next.js emits them (plain defer scripts) and drop Rocket Loader.
In production this is the Rocket Loader switch in the Cloudflare dashboard (Speed > Optimization).
"""
from common import fresh, put_text, get_text, HOME

NAME, PARENT = "arm-a-f01", None
RL_TYPE = ' type="2ac945fd2ac69580976d0ac0-text/javascript"'
RL_TAG = '<script src="/cdn-cgi/scripts/7d0fa10a/cloudflare-static/rocket-loader.min.js" data-cf-settings="2ac945fd2ac69580976d0ac0-|49" defer></script>'


def main():
    v = fresh(NAME, PARENT)
    doc = get_text(v, HOME)
    n = doc.count(RL_TYPE)
    assert n == 31 and RL_TAG in doc, n
    doc = doc.replace(RL_TYPE, "").replace(RL_TAG, "")
    put_text(v, HOME, doc, "text/html; charset=utf-8")
    print("removed rocket loader type from", n, "script tags")


if __name__ == "__main__":
    main()
