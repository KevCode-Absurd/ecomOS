"""Site crawl extractor: any store url into brand brain records.

Usage:
  python3 -m app.brain.extract.site --brand bombas --url https://shop.bombas.com
  python3 -m app.brain.extract.site --brand bombas --url https://shop.bombas.com \
      --fixture app/brain/extract/fixtures/site/bombas --out /tmp/brain

Writes <out>/<brand>/raw/a-site/<section>.json (identity, products, offers,
policies, claims, voice, visual, site_map, stack) plus sources.json. Works on
Shopify (/products.json), WooCommerce (Store API) and custom stores (product
pages from the sitemap, read through JSON-LD).

Polite by design: one host, 1 request per second, a descriptive user agent,
robots.txt honoured, 20 html pages by default. Public pages only, no
credentials, no writes outside --out. Quotes are short evidence, never whole
copy. Images are never stored: the logo is read for its colours only.

--save-fixture DIR records the live crawl as slim offline responses (inline
scripts dropped, product feed trimmed, css cut to :root and @font-face).
No third-party packages.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

USER_AGENT = "ecomOS-site-extractor/0.1 (public brand onboarding crawl; 1 request per second; honours robots.txt)"
SECTIONS = ["identity", "products", "offers", "policies", "claims", "voice", "visual", "site_map", "stack"]
TTL_DAYS = {"identity": 180, "voice": 60, "visual": 90, "products": 7, "offers": 1, "policies": 30,
            "claims": 30, "stack": 14, "site_map": 7}
MAX_TEXT = 300
MAX_QUOTE = 200
EM_DASH = "—"


# ---------------------------------------------------------------- helpers

def slug(s: str) -> str:
    s = html.unescape(s).lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def clean(s: str) -> str:
    s = html.unescape(s or "").replace(EM_DASH, " - ").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def cap(s: str, n: int = MAX_TEXT) -> str:
    s = clean(s)
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(" ", 1)[0].rstrip(",;:")
    return cut


def _fit(value):
    """Keep every string inside a value under the text cap."""
    if isinstance(value, str):
        return cap(value)
    if isinstance(value, list):
        return [_fit(v) for v in value]
    if isinstance(value, dict):
        return {k: _fit(v) for k, v in value.items()}
    return value


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9“\"(])", clean(text))
    return [p.strip() for p in parts if len(p.strip()) > 3]


def quote_at(text: str, start: int, end: int) -> str:
    """A verbatim quote around a match: its sentence, clipped to MAX_QUOTE."""
    lo = max(text.rfind(". ", 0, start) + 2, text.rfind("! ", 0, start) + 2, text.rfind("? ", 0, start) + 2, 0)
    hi_candidates = [i for i in (text.find(". ", end), text.find("! ", end), text.find("? ", end)) if i != -1]
    hi = min(hi_candidates) + 1 if hi_candidates else len(text)
    if end - start > MAX_QUOTE:
        lo, hi = start, start + MAX_QUOTE
    if hi - lo > MAX_QUOTE:
        room = MAX_QUOTE - (end - start)
        lo = max(lo, start - room // 2)
        hi = min(hi, lo + MAX_QUOTE)
        lo = max(lo, hi - MAX_QUOTE)
    q = text[lo:hi]
    # trim ragged word edges without breaking the verbatim substring
    if lo > 0 and not text[lo - 1].isspace() and " " in q[:25]:
        q = q[q.index(" ") + 1:]
    if hi < len(text) and text[hi:hi + 1].isalnum() and " " in q[-25:]:
        q = q[:q.rindex(" ")]
    return q.strip()


def find(pattern: str, text: str, flags=re.I):
    return re.search(pattern, text or "", flags)


MONTHS = {m: i for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august",
                                        "september", "october", "november", "december"], 1)}


def parse_date(s: str) -> str | None:
    m = re.search(r"([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})", s)
    if m and m.group(1).lower() in MONTHS:
        return f"{int(m.group(3)):04d}-{MONTHS[m.group(1).lower()]:02d}-{int(m.group(2)):02d}"
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    return m.group(0) if m else None


def money(s: str) -> float | None:
    try:
        return float(s.replace(",", ""))
    except (ValueError, AttributeError):
        return None


def num(v: float):
    return int(v) if float(v).is_integer() else round(v, 2)


# ---------------------------------------------------------------- robots

class Robots:
    """robots.txt for our agent: longest matching rule wins, * and $ supported."""

    def __init__(self, text: str = ""):
        self.rules: list[tuple[bool, str]] = []
        self.sitemaps: list[str] = []
        self.delay = 0.0
        groups, agents, in_rules = {}, [], False
        for raw in text.splitlines():
            line = raw.split("#", 1)[0].strip()
            if ":" not in line:
                continue
            key, val = [x.strip() for x in line.split(":", 1)]
            key = key.lower()
            if key == "sitemap":
                self.sitemaps.append(val)
            elif key == "user-agent":
                if in_rules:
                    agents, in_rules = [], False
                agents.append(val.lower())
            elif key in ("allow", "disallow", "crawl-delay"):
                in_rules = True
                for a in agents:
                    groups.setdefault(a, []).append((key, val))
        mine = groups.get("ecomos-site-extractor") or groups.get("*", [])
        for key, val in mine:
            if key == "crawl-delay":
                try:
                    self.delay = min(float(val), 10.0)
                except ValueError:
                    pass
            elif val:
                self.rules.append((key == "allow", val))

    @staticmethod
    def _rx(path: str):
        body = re.escape(path).replace(r"\*", ".*")
        if body.endswith(r"\$"):
            body = body[:-2] + "$"
        return re.compile("^" + body)

    def allowed(self, url: str) -> bool:
        p = urllib.parse.urlsplit(url)
        path = (p.path or "/") + (("?" + p.query) if p.query else "")
        best, verdict = -1, True
        for allow, rule in self.rules:
            if self._rx(rule).match(path) and (len(rule) > best or (len(rule) == best and allow)):
                best, verdict = len(rule), allow
        return verdict

    def disallowed(self) -> list[str]:
        return [r for a, r in self.rules if not a]


# ---------------------------------------------------------------- fetching

class Budget(Exception):
    pass


class Fetcher:
    """Live fetcher: one host, one request per second, caps per kind."""

    CAPS = {"page": 20, "sitemap": 4, "feed": 1, "css": 2, "logo": 1, "robots": 1}

    def __init__(self, base: str, max_pages: int = 20, save_to: Path | None = None, today: str | None = None):
        self.base = base.rstrip("/")
        self.host = urllib.parse.urlsplit(self.base).netloc
        self.caps = dict(self.CAPS, page=max_pages)
        self.used = Counter()
        self.sources: list[dict] = []
        self.robots = Robots("")
        self.last = 0.0
        self.save_to = save_to
        self.today = today or dt.date.today().isoformat()
        self.index: dict = {"captured_at": self.today, "base": self.base, "responses": {}}

    def url(self, path: str) -> str:
        return urllib.parse.urljoin(self.base + "/", path)

    def get(self, url: str, kind: str = "page") -> tuple[int, str, bytes]:
        url = urllib.parse.urljoin(self.base + "/", url)
        if urllib.parse.urlsplit(url).netloc != self.host:
            raise Budget(f"off host: {url}")
        if self.used[kind] >= self.caps.get(kind, 0):
            raise Budget(f"{kind} cap reached")
        if kind != "robots" and not self.robots.allowed(url):
            self.sources.append({"url": url, "date": self.today, "note": "skipped, disallowed by robots.txt"})
            return 0, "", b""
        self.used[kind] += 1
        status, ctype, body = self._fetch(url)
        entry = {"url": url, "date": self.today, "status": status}
        if status != 200:
            entry["note"] = f"HTTP {status}; not used as evidence"
        self.sources.append(entry)
        if self.save_to is not None and status == 200 and kind != "logo":
            self._save(url, kind, ctype, body)
        return status, ctype, body

    def _fetch(self, url: str):
        wait = max(1.0, self.robots.delay) - (time.monotonic() - self.last)
        if wait > 0:
            time.sleep(wait)
        self.last = time.monotonic()
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.headers.get("Content-Type", ""), r.read(20_000_000)
        except urllib.error.HTTPError as e:
            return e.code, "", b""
        except (urllib.error.URLError, TimeoutError, OSError):
            return -1, "", b""

    def _save(self, url: str, kind: str, ctype: str, body: bytes):
        name = f"{len(self.index['responses']) + 1:02d}-{kind}-{slug(urllib.parse.urlsplit(url).path)[:40] or 'root'}"
        name += {"page": ".html", "css": ".css", "feed": ".json", "sitemap": ".xml", "robots": ".txt"}.get(kind, ".bin")
        self.save_to.mkdir(parents=True, exist_ok=True)
        (self.save_to / name).write_bytes(slim(kind, body))
        self.index["responses"][url] = {"file": name, "kind": kind, "status": 200, "content_type": ctype.split(";")[0]}
        (self.save_to / "index.json").write_text(json.dumps(self.index, indent=1) + "\n", encoding="utf-8")


class FixtureFetcher(Fetcher):
    """Offline fetcher: answers from a saved index.json, same caps and robots."""

    def __init__(self, fixture: Path, base: str, max_pages: int = 20):
        self.fixture = Path(fixture)
        self.saved = json.loads((self.fixture / "index.json").read_text(encoding="utf-8"))
        super().__init__(base, max_pages, today=self.saved.get("captured_at"))

    def _fetch(self, url: str):
        hit = self.saved["responses"].get(url)
        if not hit:
            return 404, "", b""
        return hit.get("status", 200), hit.get("content_type", ""), (self.fixture / hit["file"]).read_bytes()


def _one_per_price(variants: list) -> list:
    seen, out = set(), []
    for v in variants:
        if v.get("price") not in seen:
            seen.add(v.get("price"))
            out.append(v)
    return out


def slim(kind: str, body: bytes) -> bytes:
    """Shrink a response for the fixture without losing what the extractor reads."""
    text = body.decode("utf-8", "replace")
    if kind == "page":
        text = re.sub(r"(?is)<script\b(?![^>]*ld\+json)([^>]*)>.*?</script>", r"<script\1></script>", text)
        text = re.sub(r"(?is)<style\b[^>]*>(?:(?!</style>).)*</style>",
                      lambda m: m.group(0) if (":root" in m.group(0) or "@font-face" in m.group(0)) else "", text)
        text = re.sub(r"(?is)<svg\b.*?</svg>", "", text)
        text = re.sub(r"(?is)<!--.*?-->", "", text)
        text = re.sub(r"\s*\n\s*", "\n", text)
    elif kind == "css":
        keep = re.findall(r":root\s*\{[^}]*\}", text) + re.findall(r"@font-face\s*\{[^}]*\}", text)
        text = "\n".join(keep)
    elif kind == "feed":
        data = json.loads(text)
        if isinstance(data, dict) and "products" in data:
            data = {"products": [{
                "id": p.get("id"), "title": p.get("title"), "handle": p.get("handle"),
                "product_type": p.get("product_type"), "vendor": p.get("vendor"), "tags": p.get("tags"),
                "created_at": p.get("created_at"), "body_html": clean(re.sub(r"<[^>]+>", " ", p.get("body_html") or ""))[:240],
                "variants": [{"title": v.get("title"), "price": v.get("price"), "compare_at_price": v.get("compare_at_price"),
                              "available": v.get("available")} for v in _one_per_price(p.get("variants", []))],
            } for p in data["products"]]}
        text = json.dumps(data, separators=(",", ":"))
    return text.encode("utf-8")


# ---------------------------------------------------------------- html

class Page(HTMLParser):
    """Reads a page for text, meta tags, links, stylesheets, scripts and JSON-LD."""

    SKIP = {"script", "style", "noscript", "svg", "template", "head"}

    def __init__(self, url: str, raw: str):
        super().__init__(convert_charrefs=True)
        self.url, self.title, self.meta = url, "", {}
        self.links, self.css, self.scripts, self.ldjson, self.icons, self.logos = [], [], [], [], [], []
        self.styles, self._body, self._stack, self._buf = [], [], [], None
        self._ld = False
        try:
            self.feed(raw)
        except Exception:  # broken html still yields what was read
            pass
        self.body = clean(" ".join(self._body))
        self.description = clean(self.meta.get("description") or self.meta.get("og:description") or "")
        parts = [clean(self.title), self.description, self.body]
        self.text = clean(". ".join(p.rstrip(".") for p in parts if p) + ".") if any(parts) else ""

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "meta":
            key = (a.get("name") or a.get("property") or "").lower()
            if key and a.get("content") and key not in self.meta:
                self.meta[key] = a["content"]
        elif tag == "a" and a.get("href"):
            self.links.append(urllib.parse.urljoin(self.url, a["href"]))
        elif tag == "link":
            rel = a.get("rel", "").lower()
            if "stylesheet" in rel and a.get("href"):
                self.css.append(urllib.parse.urljoin(self.url, a["href"]))
            if "icon" in rel and a.get("href"):
                self.icons.append(urllib.parse.urljoin(self.url, a["href"]))
        elif tag == "img":
            blob = " ".join([a.get("class", ""), a.get("alt", ""), a.get("src", ""), a.get("id", "")]).lower()
            if "logo" in blob and a.get("src"):
                self.logos.append(urllib.parse.urljoin(self.url, a["src"]))
        elif tag == "script":
            if a.get("src"):
                self.scripts.append(a["src"])
            self._ld = "ld+json" in a.get("type", "")
        if tag in ("title", "style") or (tag == "script" and self._ld):
            self._buf = []
        if tag in self.SKIP:
            self._stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "title" and self._buf is not None:
            self.title = self.title or "".join(self._buf)
        elif tag == "style" and self._buf is not None:
            self.styles.append("".join(self._buf))
        elif tag == "script" and self._ld and self._buf is not None:
            try:
                self.ldjson.append(json.loads("".join(self._buf)))
            except ValueError:
                pass
            self._ld = False
        if tag in ("title", "style", "script"):
            self._buf = None
        if tag in self.SKIP and self._stack and self._stack[-1] == tag:
            self._stack.pop()

    def handle_data(self, data):
        if self._buf is not None:
            self._buf.append(data)
        elif not self._stack and data.strip():
            self._body.append(data)

    def ld_items(self):
        out, todo = [], list(self.ldjson)
        while todo:
            x = todo.pop(0)
            if isinstance(x, list):
                todo.extend(x)
            elif isinstance(x, dict):
                out.append(x)
                todo.extend(x.get("@graph", []) if isinstance(x.get("@graph"), list) else [])
        return out


def sitemap_locs(xml: str) -> list[str]:
    return [html.unescape(x.strip()) for x in re.findall(r"<loc>\s*([^<]+?)\s*</loc>", xml)]


def sitemap_kind(url: str) -> str:
    u = url.lower()
    for key, kind in (("agentic", "facts"), ("product_cat", "collection"), ("collection", "collection"),
                      ("categor", "collection"), ("product", "PDP"), ("page", "page"), ("post", "blog"),
                      ("blog", "blog")):
        if key in u:
            return kind
    return "other"


# ---------------------------------------------------------------- crawl

ABOUT_GROUPS = [r"about|our-story|story|mission|who-we-are", r"b-?corp|certified", r"donat|impact",
                r"giving|give-back", r"sustainab", r"guarantee", r"gift"]
POLICY_TYPES = {"shipping": r"shipping|delivery", "returns": r"return|refund|exchange",
                "privacy": r"privacy", "terms": r"terms|conditions"}
SHOPIFY_POLICIES = {"shipping": "/policies/shipping-policy", "returns": "/policies/refund-policy",
                    "privacy": "/policies/privacy-policy", "terms": "/policies/terms-of-service"}
NOISE = re.compile(r"test|sirius|skimm|espn|iheart|campaign|sweeps|webform|washington|faq-covid|\d{3,}")


def handle_of(url: str) -> str:
    return urllib.parse.urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1].lower()


def pick_pages(urls: list[str], patterns: list[str], limit: int) -> list[str]:
    """One page per pattern group: fewest handle words, then sitemap order."""
    chosen = []
    for pat in patterns:
        cands = [u for u in urls if re.search(pat, handle_of(u)) and not NOISE.search(handle_of(u))
                 and "terms" not in handle_of(u) and u not in chosen]
        if cands:
            chosen.append(min(cands, key=lambda u: (handle_of(u).count("-"), urls.index(u))))
        if len(chosen) >= limit:
            break
    return chosen


class Crawl:
    def __init__(self, fetcher: Fetcher, brand: str):
        self.f, self.brand = fetcher, brand
        self.pages: dict[str, Page] = {}
        self.roles: dict[str, set] = {}
        self.platform, self.platform_evidence = "custom", ""
        self.products: list[dict] = []
        self.feed_url = ""
        self.sitemaps: list[tuple[str, str]] = []
        self.sitemap_urls: dict[str, list[str]] = {}
        self.css: list[tuple[str, str]] = []
        self.logo: tuple[str, list] | None = None
        self.notes: list[str] = []

    def page(self, url: str, role: str) -> Page | None:
        url = self.f.url(url)
        if url in self.pages:
            self.roles[url].add(role)
            return self.pages[url]
        try:
            status, _, body = self.f.get(url, "page")
        except Budget as e:
            self.notes.append(str(e))
            return None
        if status != 200:
            return None
        p = Page(url, body.decode("utf-8", "replace"))
        self.pages[url], self.roles[url] = p, {role}
        return p

    def run(self):
        st, _, body = self.f.get("/robots.txt", "robots")
        if st == 200:
            self.f.robots = Robots(body.decode("utf-8", "replace"))
        home = self.page("/", "home")
        raw_home = " ".join([(home.text if home else "")] + (home.scripts + home.css if home else [])).lower()
        if "cdn.shopify.com" in raw_home or "shopify" in raw_home or "/cdn/shop/" in raw_home:
            self.platform, self.platform_evidence = "shopify", "cdn.shopify.com" if "cdn.shopify.com" in raw_home else "/cdn/shop/"
        elif "wp-content" in raw_home or "woocommerce" in raw_home:
            self.platform, self.platform_evidence = "woocommerce", "wp-content" if "wp-content" in raw_home else "woocommerce"
        self._sitemaps()
        self._feed()
        page_urls = self.sitemap_urls.get("page", []) + [u for u in (home.links if home else [])
                                                         if urllib.parse.urlsplit(u).netloc == self.f.host]
        page_urls = list(dict.fromkeys(u.split("#")[0].split("?")[0] for u in page_urls))
        # policies
        for kind, pat in POLICY_TYPES.items():
            if self.platform == "shopify":
                self.page(SHOPIFY_POLICIES[kind], kind)
                continue
            cands = [u for u in page_urls if re.search(pat, handle_of(u)) and not NOISE.search(handle_of(u))]
            if cands:
                self.page(min(cands, key=lambda u: (handle_of(u).count("-"), len(u))), kind)
        # about and story pages
        for u in pick_pages(page_urls, ABOUT_GROUPS, 7):
            self.page(u, "about")
        # collections for claims
        for u in self._collections():
            self.page(u, "collection")
        # product pages when no feed
        if not self.products:
            pdps = self.sitemap_urls.get("PDP", []) + [u for u in page_urls if re.search(r"/products?/", u)]
            for u in list(dict.fromkeys(pdps))[:5]:
                p = self.page(u, "pdp")
                if p:
                    self.products.extend(ld_products(p))
        self._css(home)
        self._logo(home)

    def _sitemaps(self):
        roots = [u for u in self.f.robots.sitemaps if urllib.parse.urlsplit(u).netloc == self.f.host][:1] or ["/sitemap.xml"]
        try:
            st, _, body = self.f.get(roots[0], "sitemap")
        except Budget:
            return
        if st != 200 and self.platform == "woocommerce":
            st, _, body = self.f.get("/wp-sitemap.xml", "sitemap")
        if st != 200:
            return
        xml = body.decode("utf-8", "replace")
        root_url = self.f.url(roots[0])
        if "<sitemapindex" not in xml:
            for u in sitemap_locs(xml):
                self.sitemap_urls.setdefault(self._url_kind(u), []).append(u)
            self.sitemaps.append((root_url, "mixed"))
            return
        children = [(u, sitemap_kind(u)) for u in sitemap_locs(xml)]
        self.sitemaps = children
        want = ["page", "collection"] + ([] if self.platform in ("shopify", "woocommerce") else ["PDP"])
        for kind in want:
            for u, k in children:
                if k == kind:
                    try:
                        st, _, b = self.f.get(u, "sitemap")
                    except Budget:
                        break
                    if st == 200:
                        self.sitemap_urls.setdefault(kind, []).extend(sitemap_locs(b.decode("utf-8", "replace")))
                    break

    @staticmethod
    def _url_kind(u: str) -> str:
        p = urllib.parse.urlsplit(u).path.lower()
        if re.search(r"/products?/", p):
            return "PDP"
        if re.search(r"/collections/|/product-category/|/category/", p):
            return "collection"
        return "page"

    def _feed(self):
        tries = {"shopify": ["shopify"], "woocommerce": ["woo"]}.get(self.platform, ["shopify", "woo"])
        for t in tries:
            path = "/products.json?limit=250" if t == "shopify" else "/wp-json/wc/store/v1/products?per_page=100"
            try:
                st, _, body = self.f.get(path, "feed")
            except Budget:
                self.f.caps["feed"] += 1  # the fallback feed gets its own try
                st, _, body = self.f.get(path, "feed")
            if st != 200:
                continue
            try:
                data = json.loads(body.decode("utf-8", "replace"))
            except ValueError:
                continue
            if t == "shopify" and isinstance(data, dict) and isinstance(data.get("products"), list):
                self.products = [shopify_product(p, self.f.base) for p in data["products"]]
                self.platform = "shopify"
                self.platform_evidence = self.platform_evidence or "/products.json answers"
            elif t == "woo" and isinstance(data, list):
                self.products = [woo_product(p) for p in data]
                self.platform = "woocommerce"
                self.platform_evidence = self.platform_evidence or "WooCommerce Store API answers"
            if self.products:
                self.feed_url = self.f.url(path)
                return

    def _collections(self) -> list[str]:
        urls = [u for u in self.sitemap_urls.get("collection", []) if not re.search(r"related|test|sale", handle_of(u))]
        types = Counter(p["type"].lower() for p in self.products if p["type"])
        words = set()
        for t, _ in types.most_common(2):
            w = slug(t).replace("_", "-")
            words |= {w, w.rstrip("s"), w + "s"}
        out, seen = [], set()
        for u in urls:
            h = handle_of(u)
            toks = h.split("-")
            if words and not (set(toks) & words or h in words):
                continue
            if len(toks) > 3:
                continue
            key = claim_key(h)
            if key in seen:
                continue
            seen.add(key)
            out.append(u)
            if len(out) >= 4:
                break
        return out

    def _css(self, home: Page | None):
        if not home:
            return
        for s in home.styles:
            if ":root" in s or "@font-face" in s:
                self.css.append((home.url, s))
        for u in [c for c in home.css if urllib.parse.urlsplit(c).netloc == self.f.host]:
            try:
                st, _, body = self.f.get(u, "css")
            except Budget:
                break
            if st == 200:
                self.css.append((self.f.url(u).split("?")[0], body.decode("utf-8", "replace")))

    def _logo(self, home: Page | None):
        if not home:
            return
        cands = list(home.logos)
        for item in home.ld_items():
            lg = item.get("logo")
            if isinstance(lg, dict):
                lg = lg.get("url")
            if isinstance(lg, str):
                cands.append(urllib.parse.urljoin(home.url, lg))
        cands += home.icons
        cands = [c for c in cands if urllib.parse.urlsplit(c).netloc == self.f.host]
        if not cands:
            return
        try:
            st, ctype, body = self.f.get(cands[0], "logo")
        except Budget:
            return
        if st == 200:
            colours = logo_colours(body)
            if colours:
                self.logo = (self.f.url(cands[0]), colours)


def claim_key(handle: str) -> str:
    toks = [t for t in handle.split("-") if t not in ("mens", "men", "womens", "women", "kids", "unisex", "boys", "girls")]
    return "_".join(toks) or handle


def strip_tags(s: str) -> str:
    return clean(re.sub(r"<[^>]+>", " ", s or ""))


def shopify_product(p: dict, base: str) -> dict:
    tags = p.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    return {"title": clean(p.get("title", "")), "url": f"{base}/products/{p.get('handle', '')}",
            "type": clean(p.get("product_type") or ""), "tags": tags,
            "prices": [x for x in (money(v.get("price")) for v in p.get("variants", [])) if x is not None],
            "description": strip_tags(p.get("body_html"))[:400]}


def woo_product(p: dict) -> dict:
    pr = p.get("prices") or {}
    minor = int(pr.get("currency_minor_unit", 2) or 0)
    price = money(str(pr.get("price", "")))
    cats = [clean(c.get("name", "")) for c in p.get("categories", [])]
    return {"title": clean(p.get("name", "")), "url": p.get("permalink", ""), "type": cats[0] if cats else "",
            "tags": [clean(t.get("name", "")) for t in p.get("tags", [])] + cats,
            "prices": [price / 10 ** minor] if price is not None else [],
            "description": strip_tags(p.get("short_description") or p.get("description"))[:400]}


def ld_products(page: Page) -> list[dict]:
    out = []
    for item in page.ld_items():
        t = item.get("@type")
        if t == "Product" or (isinstance(t, list) and "Product" in t):
            offers = item.get("offers") or {}
            offers = offers if isinstance(offers, list) else [offers]
            prices = [money(str(o.get("price", o.get("lowPrice", "")))) for o in offers if isinstance(o, dict)]
            out.append({"title": clean(item.get("name", "")), "url": page.url, "type": clean(str(item.get("category", ""))),
                        "tags": [clean(str(item.get("material", "")))] if item.get("material") else [],
                        "prices": [x for x in prices if x is not None],
                        "description": clean(item.get("description", ""))[:400]})
    return out


# ---------------------------------------------------------------- logo colours (read, never stored)

def logo_colours(data: bytes, top: int = 3) -> list[str]:
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        px = png_pixels(data)
    elif b"<svg" in data[:2000]:
        found = re.findall(rb"(?:fill|stroke|stop-color)\s*[:=]\s*[\"']?(#[0-9a-fA-F]{3,6})", data)
        px = [hex_rgb(h.decode()) for h in found]
    else:
        return []
    counts = Counter((r // 16 * 16, g // 16 * 16, b // 16 * 16) for r, g, b in px if (r, g, b) != (-1, -1, -1))
    return ["#%02x%02x%02x" % c for c, _ in counts.most_common(top)]


def hex_rgb(h: str):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def png_pixels(data: bytes) -> list:
    """Minimal PNG reader: 8-bit, non-interlaced, grey, RGB, RGBA or palette. Transparent pixels skipped."""
    pos, idat, plte, trns = 8, b"", b"", b""
    w = h = depth = ctype = interlace = 0
    while pos < len(data):
        ln, typ = struct.unpack(">I4s", data[pos:pos + 8])
        chunk = data[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            w, h, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", chunk)
        elif typ == b"PLTE":
            plte = chunk
        elif typ == b"tRNS":
            trns = chunk
        elif typ == b"IDAT":
            idat += chunk
        pos += 12 + ln
    if depth != 8 or interlace or ctype not in (0, 2, 3, 4, 6):
        return []
    bpp = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    raw, stride, prev, out, i = zlib.decompress(idat), w * bpp, bytearray(w * bpp), [], 0
    for _ in range(h):
        f, line = raw[i], bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        for x in range(stride):
            a = line[x - bpp] if x >= bpp else 0
            b = prev[x]
            c = prev[x - bpp] if x >= bpp else 0
            if f == 1:
                line[x] = (line[x] + a) & 255
            elif f == 2:
                line[x] = (line[x] + b) & 255
            elif f == 3:
                line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        prev = line
        for x in range(0, stride, bpp):
            px = line[x:x + bpp]
            if ctype == 6:
                out.append(tuple(px[:3]) if px[3] > 127 else (-1, -1, -1))
            elif ctype == 2:
                out.append(tuple(px))
            elif ctype == 4:
                out.append((px[0],) * 3 if px[1] > 127 else (-1, -1, -1))
            elif ctype == 0:
                out.append((px[0],) * 3)
            else:
                k = px[0]
                if k < len(trns) and trns[k] <= 127:
                    out.append((-1, -1, -1))
                else:
                    out.append(tuple(plte[k * 3:k * 3 + 3]))
    return out


# ---------------------------------------------------------------- records

class Out:
    def __init__(self, brand: str, date: str, name: str):
        self.brand, self.date, self.name = brand, date, name
        self.recs: dict[str, dict[str, dict]] = {s: {} for s in SECTIONS}

    def add(self, section, field, value, text, url, quotes=(), confidence=0.85, notes=None):
        field = slug(field)[:60]
        if not field or value in (None, "", [], {}):
            return
        ev = [{"quote": cap(q, MAX_QUOTE), "ref": url} for q in quotes if q]
        have = self.recs[section].get(field)
        if have:  # same field again: keep the first value, add evidence
            have.setdefault("evidence", []).extend(e for e in ev if e not in have.get("evidence", []))
            have["evidence"] = have["evidence"][:3]
            return
        expires = (dt.date.fromisoformat(self.date) + dt.timedelta(days=TTL_DAYS[section])).isoformat()
        rec = {"id": f"{self.brand}.{section}.{field}", "brand": self.brand, "section": section, "field": field,
               "value": _fit(value), "text": cap(text),
               "source": {"type": "site", "ref": url, "captured_at": self.date},
               "confidence": confidence, "tier": "site_backed", "visibility": "public", "expires_at": expires}
        if ev:
            rec["evidence"] = ev[:3]
        if notes:
            rec["notes"] = cap(notes)
        self.recs[section][field] = rec


def pages_with(crawl: Crawl, role: str) -> list[Page]:
    return [p for u, p in crawl.pages.items() if role in crawl.roles[u]]


def search_pages(pages: list[Page], pattern: str, flags=re.I):
    for p in pages:
        m = re.search(pattern, p.text, flags)
        if m:
            return p, m
    return None, None


GIVING = (r"one (?:\w+ )?purchased\s*=\s*one (?:\w+ )?donated(?:,? always and forever)?|buy one,? give one"
          r"|for every [^.]{0,40}?(?:sold|purchased|bought)[^.]{0,40}?(?:donate|give)[^.]{0,40}")


def extract_identity(c: Crawl, o: Out):
    home = c.pages.get(c.f.url("/"))
    allp = list(c.pages.values())
    about = pages_with(c, "about")
    name = o.name
    if home and home.meta.get("og:site_name"):
        o.add("identity", "name", name, f"The store calls itself {name}.", home.url, [f"{home.meta['og:site_name']}"], 0.9)
    if home:
        m = find(r"\b(?:is|are) an? ([^.]{3,90}?\b(?:brand|company|store|shop|label|maker|retailer))\b", home.description)
        if m:
            o.add("identity", "category", m.group(1).lower(), f"{name} describes itself as a {m.group(1).lower()}.",
                  home.url, [quote_at(home.description, m.start(), m.end())], 0.9)
    for p in about + ([home] if home else []):
        for s in sentences(p.text):
            if name.lower() in s.lower() and find(r"\b(built|designed|engineered|crafted|made) (for|to)\b", s):
                val = find(r"\b(?:are|is) (.+?)\.?$", s)
                o.add("identity", "one_line_pitch", (val.group(1) if val else s).lower(),
                      f"{name} describes its products this way: {s}", p.url, [s], 0.85)
                o.add("claims", "brand_positioning", "positioning claim: " + (val.group(1) if val else s).lower(),
                      f"{name} positions itself in its own words: {s}", p.url, [s], 0.85)
                break
        if "one_line_pitch" in o.recs["identity"]:
            break
    p, m = search_pages(about + allp, r"\bB[\s-]?Corp(?:oration)?\b")
    if p:
        o.add("identity", "certification_bcorp", True, f"{name} states on its site that it is a certified B Corp.",
              p.url, [quote_at(p.text, m.start(), m.end())], 0.9)
    p, m = search_pages(([home] if home else []) + about + allp, GIVING)
    if p:
        val = clean(m.group(0)).lower().replace("=", "equals")
        val = re.sub(r",? always and forever", "", val)
        o.add("identity", "giving_model", re.sub(r"\s+", " ", val), f"{name} runs a giving model: {clean(m.group(0))}.",
              p.url, [quote_at(p.text, m.start(), m.end())], 0.9)
    p, m = search_pages(about + allp, r"\b(\d[\d,.]*\s*(?:million|billion|thousand|k)?)\s+(?:\w+\s+){0,2}?(?:donated|given away|donations)\b")
    if p:
        o.add("identity", "donation_milestone", f"{clean(m.group(1)).lower()} donated, per a page on the site",
              f"A page on the {name} site marks {clean(m.group(1)).lower()} donated.", p.url,
              [quote_at(p.text, m.start(), m.end())], 0.8)
    p, m = search_pages(allp, r"\b(?:founded|established|since)\s+(?:in\s+)?((?:19|20)\d{2})\b")
    if p:
        o.add("identity", "founded", int(m.group(1)), f"{name} says it was founded in {m.group(1)}.", p.url,
              [quote_at(p.text, m.start(), m.end())], 0.8)
    p, m = search_pages(pages_with(c, "terms") + allp, r"\b([A-Z][\w&']+(?: [A-Z][\w&']+){0,3},? (?:LLC|Inc\.?|Ltd\.?|Limited|GmbH|PBC))(?=[\s,.)])", 0)
    if p:
        o.add("identity", "legal_name", m.group(1).rstrip("."), f"The site names the legal entity as {m.group(1).rstrip('.')}.",
              p.url, [quote_at(p.text, m.start(), m.end())], 0.8)


MATERIALS = ["merino wool", "organic cotton", "pima cotton", "supima cotton", "cotton", "cashmere", "alpaca", "wool",
             "linen", "silk", "bamboo", "hemp", "tencel", "modal", "recycled polyester", "polyester", "nylon",
             "spandex", "elastane", "leather", "suede", "fleece", "compression", "stainless steel", "ceramic",
             "glass", "oak", "walnut", "soy wax", "beeswax"]


def extract_products(c: Crawl, o: Out):
    prods, name = c.products, o.name
    if not prods:
        return
    ref = c.feed_url or prods[0]["url"]
    types = [p["type"] for p in prods if p["type"]]
    counts = Counter(types)
    if types:
        lines = list(dict.fromkeys(types))
        o.add("products", "lines", lines, f"The {name} product feed lists {len(lines)} product types: "
              + ", ".join(t.lower() for t in lines[:8]) + ".", ref, [f'"product_type": "{t}"' for t in lines[:2]], 0.9)
        for t, n in counts.most_common(2):
            ps = [x for p in prods if p["type"] == t for x in p["prices"] if x > 0]
            if ps:
                o.add("products", f"price_ladder_{slug(t)}",
                      {"line": t, "min_usd": num(min(ps)), "max_usd": num(max(ps)), "sample_size": n},
                      f"In a {len(prods)} product sample, {t.lower()} listings priced from {num(min(ps))} to {num(max(ps))} dollars.",
                      ref, [f'"price": "{min(ps):.2f}"', f'"price": "{max(ps):.2f}"'], 0.85)
    else:
        ps = [x for p in prods for x in p["prices"] if x > 0]
        if ps:
            o.add("products", "price_range", {"min_usd": num(min(ps)), "max_usd": num(max(ps)), "sample_size": len(prods)},
                  f"{len(prods)} product pages priced from {num(min(ps))} to {num(max(ps))} dollars.", ref, [], 0.8)
    packs, single, ex = set(), False, None
    for p in prods:
        m = find(r"\b(\d{1,2})\s*[-– ]?\s*(?:pack|pk)\b", p["title"])
        if m:
            packs.add(int(m.group(1)))
            ex = ex or p
        elif not find(r"gift ?card", p["title"]):
            single = True
    if packs:
        ladder = (["single"] if single else []) + [f"{n}-pack" for n in sorted(packs)]
        o.add("products", "pack_sizes", ladder, f"{name} sells " + ", ".join(ladder) + " options.", ref,
              [f'"{ex["title"]}"'], 0.9)
        if len(packs) >= 2:
            o.add("offers", "bundles_pack_ladder", ladder, f"{name} prices products as " + ", ".join(ladder)
                  + ", so buyers step up to bigger packs.", ref, [f'"{ex["title"]}"'], 0.85)
    blob = " ".join((p["title"] + " " + " ".join(p["tags"]) + " " + p["description"]).lower().replace("-", " ") for p in prods)
    mats = []
    for mname in MATERIALS:
        if re.search(r"\b" + mname + r"\b", blob) and not any(mname in m for m in mats):
            mats.append(mname)
    if mats:
        o.add("products", "materials", mats[:8], f"{name} product titles, tags and copy name " + ", ".join(mats[:8]) + ".",
              ref, [], 0.8)
    flags: dict[str, list] = {}
    for p in prods:
        for t in p["tags"]:
            tl = t.lower()
            m = re.match(r"badge:(?:[^:]*:)?([a-z0-9 -]+)$", tl)
            key = m.group(1) if m else ("new" if tl in ("status:new", "new", "new-arrival", "new arrival") else
                                        tl if tl in ("best-seller", "bestseller", "best seller", "selling-fast", "limited") else None)
            if key:
                flags.setdefault(slug(key), []).append((p, t))
    for key, hits in list(flags.items())[:4]:
        p, t = hits[0]
        o.add("products", f"hero_flag_{key}", {"badge": key.replace("_", "-"), "count": len(hits), "example_product": p["title"],
                                               "example_pdp": p["url"]},
              f"{len(hits)} listings carry a {key.replace('_', ' ')} tag, for example {p['title']}.", ref, [t], 0.85)
    cards = [p for p in prods if find(r"gift ?card", p["title"]) or slug(p["type"]).replace("_", "") in ("giftcard", "giftcards")]
    if cards:
        d = sorted({num(x) for p in cards for x in p["prices"]})
        span = (f" from {d[0]} to {d[-1]} dollars." if len(d) > 1 else f" for {d[0]} dollars." if d else ".")
        o.add("products", "gift_card", {"name": cards[0]["title"], "denominations_usd": d},
              f"{name} sells a gift card{span}", ref, [f'"title": "{cards[0]["title"]}"'], 0.9)


def extract_offers_policies(c: Crawl, o: Out):
    name = o.name
    ship = pages_with(c, "shipping")
    rets = pages_with(c, "returns")
    priv = pages_with(c, "privacy")
    terms = pages_with(c, "terms")
    allp = list(c.pages.values())
    # shipping threshold and cost
    p, m = search_pages(ship + allp, r"free[^.$]{0,80}?(?:orders?|purchases?|over|above)[^.$]{0,20}?\$\s?(\d+(?:\.\d{2})?)\s*\+?")
    if not p:
        p, m = search_pages(ship + allp, r"orders? (?:over|above|of) \$\s?(\d+(?:\.\d{2})?)[^.]{0,40}?ship[^.]{0,20}?free")
    thr = None
    if p:
        thr = num(money(m.group(1)))
        o.add("offers", "free_shipping_threshold_usd", thr, f"{name} offers free shipping on orders of {thr} dollars or more.",
              p.url, [quote_at(p.text, m.start(), m.end())], 0.95)
    p, m = search_pages(ship, r"\$\s?(\d+\.\d{2})\s*\(?(flat rate[^)]{0,40}|[^.:]{0,20}orders under \$\s?\d+)")
    if p:
        cond = find(r"orders under \$\s?\d+", m.group(2))
        o.add("offers", "standard_shipping_cost", {"cost_usd": num(money(m.group(1))), "condition": cond.group(0) if cond else "flat rate"},
              f"Standard shipping costs {m.group(1)} dollars" + (f" on {cond.group(0)}." if cond else "."),
              p.url, [quote_at(p.text, m.start(), m.end())], 0.95)
    opts = []
    for p in ship[:1]:
        for chunk in re.split(r"(?<=business days)", p.text):
            m = find(r"((?:[A-Z][a-z]+ )?[A-Z][a-z]+)(?: Shipping)?\s*(?:\(when available\s*\))?\s+-\s+(Free|\$\s?\d+(?:\.\d{2})?)[^:]{0,80}:\s*(\d+)\s*-\s*(\d+) business days", chunk, 0)
            if m:
                nm = re.sub(r"\s+Shipping$", "", clean(m.group(1)).split(". ")[-1])
                cost = 0 if m.group(2).lower() == "free" else num(money(m.group(2).strip("$ ")))
                row = {"name": nm, "cost_usd": cost, "business_days": f"{m.group(3)}-{m.group(4)}"}
                if cost == 0 and thr:
                    row["threshold_usd"] = thr
                opts.append(row)
        if opts:
            o.add("policies", "shipping_options", opts[:6], f"{name} lists {len(opts)} shipping options, from "
                  f"{opts[0]['name'].lower()} in {opts[0]['business_days']} business days to {opts[-1]['name'].lower()} in {opts[-1]['business_days']}.",
                  p.url, [quote_at(p.text, *find(r"business days", p.text).span())], 0.9)
    # returns
    p, m = search_pages(rets, r"within (\d+) days")
    days = None
    if p:
        days = int(m.group(1))
        hol = find(r"within (\d+) days(?:(?!within).){0,80}holiday", p.text[m.end():])
        o.add("policies", "returns_window_days", days, f"{name} accepts returns within {days} days"
              + (f", or {hol.group(1)} days for holiday purchases." if hol else "."), p.url, [quote_at(p.text, m.start(), m.end())], 0.95)
    p, m = search_pages(rets, r"refunds?[^.]{0,80}?(original (?:method of )?payment|store credit)")
    if p:
        val = "original payment method" if "original" in m.group(1).lower() else "store credit"
        o.add("policies", "refund_method", val, f"{name} refunds go to the {val}.", p.url, [quote_at(p.text, m.start(), m.end())], 0.9)
    p, m = search_pages(rets, r"(?:after|outside)[^.]{0,60}(?:refund|return) (?:period|window)[^.]{0,120}(?:replacement|exchange)|exchanges? (?:are|is) (?:available|offered|accepted)[^.]{0,80}")
    if p:
        o.add("policies", "exchanges", "replacement or exchange offered, see quote",
              f"{name} offers replacements or exchanges, per its returns policy.", p.url, [quote_at(p.text, m.start(), m.end())], 0.8)
    guar = None
    p, m = search_pages(rets + allp, r"\b(?:The )?(?:[A-Z]\w+ )?([A-Z][a-z]+) Guarantee is ([^.]{10,200})", 0)
    if p:
        guar = m.group(1)
        o.add("policies", f"{slug(guar)}_guarantee", f"{guar} Guarantee: " + cap(m.group(2), 160),
              f"The {name} {guar} Guarantee is its promise to customers, as stated in its policy.", p.url,
              [quote_at(p.text, m.start(), m.end())], 0.9)
        o.add("claims", "guarantee_promise", "guarantee claim: " + cap(m.group(2), 160),
              f"{name} {guar} Guarantee claim: {cap(m.group(2), 200)}.", p.url, [quote_at(p.text, m.start(), m.end())], 0.9)
    else:
        p, m = search_pages(rets + allp, r"\b(money[- ]back|satisfaction|lifetime|\d+[- ]day) guarantee")
        if p:
            guar = clean(m.group(1)).title()
    if guar:
        o.add("offers", "guarantee", f"{guar} Guarantee" + (f", {days} day return window" if days else ""),
              f"{name} backs purchases with its {guar} Guarantee" + (f" and a {days} day return window." if days else "."),
              p.url, [quote_at(p.text, m.start(), m.end())], 0.9)
    p, m = search_pages(rets + allp, r"[^.]{0,80}(?:will not|won't|does not|do not|not) (?:trigger|count toward|include)[^.]{0,20}donat[^.]{0,80}"
                                      r"|[^.]{0,80}donat[^.]{0,60}(?:will not|won't|does not|do not|not) (?:apply|count)[^.]{0,60}")
    if p:
        o.add("claims", "donation_exclusion", "mission claim limit: some orders do not trigger a donation",
              f"{name} states some orders do not trigger a donation: {cap(m.group(0).strip(), 200)}", p.url,
              [quote_at(p.text, m.start(), m.end())], 0.9)
    # gifting
    gifts = [p for p in allp if "gift" in handle_of(p.url)]
    card = o.recs["products"].get("gift_card")
    if gifts or card:
        parts = []
        if card:
            d = card["value"].get("denominations_usd") or []
            parts.append("gift cards" + (f" from ${d[0]} to ${d[-1]}" if len(d) > 1 else f" at ${d[0]}" if d else ""))
        if gifts:
            parts.append(f"a gifting page ({handle_of(gifts[0].url)})")
        g = gifts[0] if gifts else None
        o.add("offers", "gifting", " plus ".join(parts), f"{name} sells " + " and runs ".join(parts) + ".",
              g.url if g else card["source"]["ref"], [g.description[:MAX_QUOTE]] if g and g.description else [], 0.85)
    p, m = search_pages(allp, r"(\d{1,2})%\s*off (?:your )?first (?:order|purchase)")
    if p:
        o.add("offers", "first_order_discount_pct", int(m.group(1)), f"{name} offers {m.group(1)} percent off a first order.",
              p.url, [quote_at(p.text, m.start(), m.end())], 0.85)
    # privacy and terms
    for kind, pages in (("privacy", priv), ("terms", terms)):
        p, m = search_pages(pages, r"(?:effective date|last updated|last modified|last revised)\s*:?\s*([A-Za-z]+ \d{1,2},? \d{4}|\d{4}-\d{2}-\d{2})")
        if p and parse_date(m.group(1)):
            o.add("policies", f"{kind}_effective_date", parse_date(m.group(1)),
                  f"The {name} {kind} policy on the site is effective {m.group(1)}.", p.url, [m.group(0)], 0.9)
    if priv:
        p = priv[0]
        vocab = ["email address", "first name and last name", "name", "phone number", "address", "ip address",
                 "browser type", "device", "pages of our site that you visit", "payment", "location", "purchase history"]
        low, got, qs = p.text.lower(), [], []
        for v in vocab:
            i = low.find(v)
            if i != -1 and not any(v in g for g in got):
                got.append(v)
                if len(qs) < 2:
                    qs.append(quote_at(p.text, i, i + len(v)))
        if got:
            o.add("policies", "privacy_data_collected", got, f"The {name} privacy policy lists data it collects, including "
                  + ", ".join(got[:5]) + ".", p.url, qs, 0.85)
        cats = []
        for m in re.finditer(r"[“\"]([A-Z][^”\"]{2,60})[”\"]\s*cookies", p.text):
            v = clean(m.group(1))
            if v.lower() not in ("session", "persistent", "first-party", "third-party", name.lower()) and v not in cats:
                cats.append(v)
        if cats:
            m = re.search(r"[“\"]" + re.escape(cats[0]), p.text)
            o.add("policies", "cookie_categories", cats[:8], f"The {name} privacy policy groups cookies into {len(cats)} categories.",
                  p.url, [quote_at(p.text, m.start(), m.end() + 10)], 0.85)
    p, m = search_pages(terms, r"liabilit[^.]{0,300}?exceed[^$]{0,120}?\$\s?([\d,]+(?:\.\d{2})?)")
    if p:
        v = num(money(m.group(1)))
        o.add("policies", "terms_liability_cap", v, f"The {name} terms cap its liability at {v} dollars.", p.url,
              [quote_at(p.text, m.end() - 60, m.end())], 0.8)


CLAIM_WORDS = r"comfort|support|cushion|soft|durab|moisture|breath|wick|organic|recycled|sustainab|stay[- ]up|blister|arch|seamless|warm|cool|odor|last|premium|high-quality|handmade|non-toxic|natural"


def claim_category(s: str) -> str:
    s = s.lower()
    if find(r"guarantee|warranty|refund", s):
        return "guarantee"
    if find(r"better than|unlike|compared|most|best", s):
        return "comparison"
    if find(r"cotton|wool|merino|polyester|nylon|leather|organic|recycled|material|fabric", s):
        return "material"
    return "benefit"


def extract_claims(c: Crawl, o: Out):
    name = o.name
    home = c.pages.get(c.f.url("/"))
    p, m = search_pages(([home] if home else []) + list(c.pages.values()), GIVING)
    if p:
        o.add("claims", "donation_pledge", "mission claim: " + clean(m.group(0)).lower(),
              f"{name} states its giving pledge: {clean(m.group(0))}.", p.url, [quote_at(p.text, m.start(), m.end())], 0.9)
    for p in pages_with(c, "collection"):
        src = p.description or p.body
        for s in sentences(src):
            if find(CLAIM_WORDS, s):
                title = re.split(r"\s[-–|]\s", clean(p.title))[0].lower()
                o.add("claims", f"{claim_key(handle_of(p.url))}_benefit", f"{claim_category(s)} claim",
                      f"{name} {title} copy claims: {s}", p.url, [s], 0.9)
                break
    n = 0
    for pr in c.products:
        if n >= 3:
            break
        for s in sentences(pr["description"]):
            if find(CLAIM_WORDS, s) and len(s) > 25:
                short = "_".join(slug(re.sub(r"\d+\s*-?\s*pack|\(.*?\)", "", pr["title"], flags=re.I)).split("_")[:5])
                o.add("claims", f"{short}_benefit", f"{claim_category(s)} claim",
                      f"{name} {pr['title']} copy claims: {s}", pr["url"], [s], 0.85)
                n += 1
                break


STOP = set("""a an the and or but if of to in on for with at by from as is are was were be been it its this that these those
you your yours we our us i my me they them their he she his her not no so do does did can will just than then there here what
which who whom how all any more most other some such only own same too very s t don now also into out up down over under again
further once about get got has have had having one two per off new shop skip content bombas""".split())


def copy_of(p: Page) -> str:
    return ". ".join(x.rstrip(".") for x in (p.description, p.body) if x) + "."


def syllables(w: str) -> int:
    w = w.lower()
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1:
        n -= 1
    return max(1, n)


def extract_voice(c: Crawl, o: Out):
    name = o.name
    legal = {"privacy", "terms", "shipping", "returns"}
    cands = [p for u, p in c.pages.items() if not (c.roles[u] & legal)]
    cands = sorted(cands, key=lambda p: -len(p.description + " " + p.body))[:5]
    if not cands:
        return
    texts = [(p, [s for s in sentences(copy_of(p)) if len(s.split()) >= 3]) for p in cands]
    sents = [s for _, ss in texts for s in ss]
    if not sents:
        return
    ref = cands[0].url
    words = [w for s in sents for w in re.findall(r"[A-Za-z']+", s)]
    avg = round(len(words) / len(sents), 1)
    grade = round(0.39 * avg + 11.8 * sum(syllables(w) for w in words) / max(1, len(words)) - 15.59, 1)
    urls = [p.url for p in cands]
    o.add("voice", "pages_sampled", urls, f"Voice read from {len(urls)} {name} pages.", ref, [], 0.9)
    o.add("voice", "sentence_length_avg", avg, f"{name} writes sentences of about {avg} words on average across {len(urls)} pages.",
          ref, [], 0.8)
    o.add("voice", "reading_grade", grade, f"{name} copy reads at about grade {grade} on the Flesch-Kincaid scale.", ref, [], 0.7)
    low = [w.lower() for w in words]
    we = sum(low.count(x) for x in ("we", "our", "us", "we're"))
    you = sum(low.count(x) for x in ("you", "your", "you're", "yours"))
    they = low.count(name.lower())
    person = "first person plural" if we >= max(you, they) and we else "second person" if you >= they and you else "third person, brand name"
    o.add("voice", "person", {"dominant": person, "we_our": we, "you_your": you, "brand_name": they},
          f"{name} mostly writes in the {person}: {we} we or our, {you} you or your, {they} uses of its own name.", ref, [], 0.75)
    counts = Counter(w for w in low if len(w) > 3 and w not in STOP and w != name.lower())
    rec = [w for w, n in counts.most_common(10) if n >= 2]
    if rec:
        o.add("voice", "recurring_words", rec, f"Words {name} repeats most across its pages: " + ", ".join(rec[:8]) + ".", ref, [], 0.75)
    seen = Counter()
    where = {}
    everyone = [p for u, p in c.pages.items() if not (c.roles[u] & legal)]
    for p, ss in [(p, [s for s in sentences(copy_of(p)) if len(s.split()) >= 4]) for p in everyone]:
        for s in set(ss):
            seen[s] += 1
            where.setdefault(s, p)
    rep = [s for s, n in seen.most_common() if 2 <= n < max(3, len(everyone)) and len(s) <= 140]
    if rep:
        o.add("voice", "tagline", rep[0], f"{name} repeats this line word for word on {seen[rep[0]]} pages.", where[rep[0]].url, [rep[0]], 0.8)


COLOR = re.compile(r"^(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|hsla?\([^)]*\))$")


def extract_visual(c: Crawl, o: Out):
    name = o.name
    ncol = 0
    for ref, css in c.css:
        for block in re.findall(r":root\s*\{([^}]*)\}", css):
            decls = re.findall(r"--([\w-]+)\s*:\s*([^;]+)", block)
            vars_ = {k: v.strip() for k, v in decls}
            for k, v in decls:
                v = v.strip()
                if COLOR.match(v) and ncol < 24:
                    roles = [r for r, rv in vars_.items() if rv == f"var(--{k})" and r in ("primary", "secondary", "accent", "brand", "background", "foreground")]
                    o.add("visual", f"color_{k}", v.lower(), f"{name} stylesheet defines a colour token {k} as {v.lower()}"
                          + (f" and uses it as the {', '.join(roles)} colour." if roles else "."), ref,
                          [f"--{k}: {v}"] + [f"--{r}: var(--{k})" for r in roles[:1]], 0.9)
                    ncol += 1
                elif "font" in k and not v.startswith("var(") and not re.match(r"^[\d.]+(px|rem|em|%)?$", v):
                    fam = v.split(",")[0].strip("'\" ")
                    fld = "font_" + slug(k.replace("font", "")).strip("_") if k.replace("font", "").strip("-") else "font_main"
                    o.add("visual", fld, fam, f"{name} stylesheet sets the {k} token to the typeface {fam}.", ref, [f"--{k}: {v}"[:MAX_QUOTE]], 0.9)
        faces = list(dict.fromkeys(clean(f).strip("'\"") for f in re.findall(r"@font-face\s*\{[^}]*?font-family\s*:\s*([^;}]+)", css)))
        if faces:
            o.add("visual", "font_faces", faces[:10], f"{name} loads these web fonts: " + ", ".join(faces[:6]) + ".", ref,
                  [f"font-family: {faces[0]}"], 0.85)
    if c.logo:
        url, cols = c.logo
        o.add("visual", "logo_colors", cols, f"The {name} logo is mostly " + ", ".join(cols) + ", measured from its pixels.", url, [], 0.7,
              notes="colours counted in 16-step bins; the image was read once and not stored")


def extract_site_map(c: Crawl, o: Out):
    name, base = o.name, c.f.url("/")
    if base in c.pages:
        o.add("site_map", "home", {"url": base, "type": "home"}, f"The {name} home page is at {base}, on {c.platform}.", base,
              [c.pages[base].title.strip()], 0.95)
    if c.sitemaps:
        o.add("site_map", "sitemap_index", [{"url": u, "type": k} for u, k in c.sitemaps[:10]],
              f"The sitemap lists {len(c.sitemaps)} sub sitemaps.", c.f.url("/sitemap.xml"), [], 0.9)
    for kind, urls in c.sitemap_urls.items():
        label = {"page": "pages", "collection": "collections", "PDP": "products"}.get(kind, kind)
        o.add("site_map", f"{label}_sitemap_count", len(urls), f"The {label} sitemap lists {len(urls)} urls.",
              urls[0] if urls else base, [f"<loc>{urls[0]}</loc>"] if urls else [], 0.9)
    allu = list(dict.fromkeys(c.sitemap_urls.get("page", []) + list(c.pages)))
    legal = [u for u in allu if re.search(r"privacy|terms|policy|policies|accessib|legal|cookie", u.lower())][:10]
    if legal:
        o.add("site_map", "legal_pages", [{"url": u, "type": "legal"} for u in legal],
              f"The site has at least {len(legal)} legal pages.", legal[0], [], 0.9)
    facts = [u for u in allu if re.search(r"about|story|faq|size|guide|sustainab|b-corp|giving|donat|tech|mission|help", handle_of(u))
             and not NOISE.search(handle_of(u))][:12]
    if facts:
        o.add("site_map", "facts_pages", [{"url": u, "type": "facts"} for u in facts],
              f"The site has at least {len(facts)} fact pages a buyer or answer engine would read.", facts[0], [], 0.85)
    dis = c.f.robots.disallowed()
    if dis:
        o.add("site_map", "crawl_access", {"disallowed": dis[:12], "sitemaps": c.f.robots.sitemaps[:3]},
              f"robots.txt disallows {len(dis)} paths, for example " + ", ".join(dis[:4]) + ".", c.f.url("/robots.txt"),
              [f"Disallow: {dis[0]}"], 0.9)
    o.add("site_map", "pages_crawled", [{"url": u, "roles": sorted(c.roles[u])} for u in c.pages],
          f"This crawl read {len(c.pages)} html pages.", base, [], 0.95)


def extract_stack(c: Crawl, o: Out):
    o.add("stack", "platform", c.platform, f"The store runs on {c.platform}, as seen from the crawl. Apps and scripts are left for the stack detector.",
          c.feed_url or c.f.url("/"), [c.platform_evidence] if c.platform_evidence else [], 0.8 if c.platform != "custom" else 0.5,
          notes="stub; the stack detector (S6.0b) fills theme, apps, analytics and consent")


def brand_name(c: Crawl, brand: str) -> str:
    home = c.pages.get(c.f.url("/"))
    if home:
        if home.meta.get("og:site_name"):
            return clean(home.meta["og:site_name"])
        t = re.split(r"\s[|–-]\s", clean(home.title))
        if t and t[-1]:
            return t[-1]
    return brand.replace("-", " ").title()


def run(brand: str, url: str, out: Path, fixture: Path | None = None, max_pages: int = 20,
        save_fixture: Path | None = None) -> dict[str, list]:
    url = url.rstrip("/")
    fetcher = FixtureFetcher(fixture, url, max_pages) if fixture else Fetcher(url, max_pages, save_to=save_fixture)
    crawl = Crawl(fetcher, brand)
    crawl.run()
    o = Out(brand, fetcher.today, brand_name(crawl, brand))
    extract_identity(crawl, o)
    extract_products(crawl, o)
    extract_offers_policies(crawl, o)
    extract_claims(crawl, o)
    extract_voice(crawl, o)
    extract_visual(crawl, o)
    extract_site_map(crawl, o)
    extract_stack(crawl, o)
    folder = Path(out) / brand / "raw" / "a-site"
    folder.mkdir(parents=True, exist_ok=True)
    result = {}
    for s in SECTIONS:
        recs = list(o.recs[s].values())
        (folder / f"{s}.json").write_text(json.dumps(recs, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        result[s] = recs
    sources = list({(x["url"], x.get("note", "")): x for x in fetcher.sources}.values())
    (folder / "sources.json").write_text(json.dumps(sources, indent=1) + "\n", encoding="utf-8")
    result["sources"] = sources
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Crawl a store's public site into brand brain records.")
    ap.add_argument("--brand", required=True, help="brand slug, lowercase")
    ap.add_argument("--url", required=True, help="store url, e.g. https://shop.bombas.com")
    ap.add_argument("--out", default="app/brain", help="brain root; writes <out>/<brand>/raw/a-site/")
    ap.add_argument("--fixture", help="read saved responses from this folder instead of the web")
    ap.add_argument("--max-pages", type=int, default=20, help="html page cap (default 20)")
    ap.add_argument("--save-fixture", help="live mode only: save slim responses here for offline runs")
    a = ap.parse_args(argv)
    if not re.match(r"^[a-z0-9_-]+$", a.brand):
        ap.error("brand must be a lowercase slug")
    res = run(a.brand, a.url, Path(a.out), Path(a.fixture) if a.fixture else None, a.max_pages,
              Path(a.save_fixture) if a.save_fixture else None)
    for s in SECTIONS:
        print(f"{s:10} {len(res[s]):3} records")
    print(f"sources    {len(res['sources']):3} urls")
    return 0


if __name__ == "__main__":
    sys.exit(main())
