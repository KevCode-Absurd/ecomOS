"""Page-id discovery for the Meta Ad Library lane: the brand's own page and a competitor proposal.

A new brand never runs a keyword search. The own page id comes from, in order:
  1. a facebook.com link on the brand's site (JSON-LD sameAs first, then header and footer links),
     kept only when the page name or handle matches the brand;
  2. the known-ids cache (`fixtures/adlib/known_pages.json`, ids found by hand on 28 Sep) and any
     page_id already in the brand's brain records;
  3. one public Ad Library page search, keeping only an exact case-insensitive name match;
  4. otherwise unresolved: the founder pastes the id.
On 28 Sep a plain fetch of the page search returned a JavaScript challenge (403), so step 3 is
unavailable without a browser and says so rather than guessing.

Competitors are proposed from the brain (competitors records, Reddit recommended-instead records, the
competitor_frame founder record, identity category), ranked, up to 15, each with its reasons and the
record ids behind them. They are written to config `meta_ad_library.proposed_pages`. Only pages under
`pages` (role self or competitor) are pulled; `--confirm "Name,Name"` moves proposals into `pages`.

    python3 -m app.brain.extract.adlib_pages --brand bombas [--site FILE_OR_URL] [--live] [--confirm "A,B"]

Offline by default: the site is read from a saved file and the page search from saved responses.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures" / "adlib"
PEERS = HERE / "adlib_peers.json"
SEARCH = ("https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country={country}"
          "&q={q}&search_type=page")
UA = "Mozilla/5.0 (compatible; ecomOS brand setup; public pages only)"
MAX_PROPOSALS = 15

# Trailing words a page name may carry without being a different brand ("Darn Tough Vermont Socks").
SUFFIX = {"socks", "sock", "vermont", "official", "us", "usa", "inc", "co", "company", "brand", "apparel",
          "clothing", "hq", "shop", "store", "online"}
# First path parts of facebook.com links that are never a brand page.
NOT_PAGES = {"sharer", "sharer.php", "share", "share.php", "tr", "privacy", "policies", "policy.php", "plugins",
             "dialog", "ads", "help", "legal", "login", "login.php", "events", "groups", "watch", "hashtag",
             "business", "l.php", "photo.php", "story.php", "permalink.php", "gaming", "marketplace", "terms.php"}
FB_LINK = re.compile(r"https?://(?:www\.|m\.|web\.|business\.)?facebook\.com/([^\s\"'<>?#]+)(\?[^\s\"'<>#]*)?", re.I)
SAME_AS = re.compile(r"<script[^>]+application/ld\+json[^>]*>(.*?)</script>", re.S | re.I)


# ---------- names ----------

def norm(s: str | None) -> str:
    s = (s or "").lower().replace("&", " and ")
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())


def key(s: str | None) -> str:
    """Brand key: normalised name without trailing suffix words or a leading 'the'."""
    w = norm(s).split()
    if len(w) > 1 and w[0] == "the":
        w = w[1:]
    while len(w) > 1 and w[-1] in SUFFIX:
        w = w[:-1]
    return " ".join(w)


def exact(a: str | None, b: str | None) -> bool:
    """The page search rule: same name, case and spacing aside. 'Stance Auto' is not 'Stance'."""
    return bool(norm(a)) and norm(a) == norm(b)


def same_brand(a: str | None, b: str | None) -> bool:
    return bool(key(a)) and key(a) == key(b)


def handle_matches(handle: str, brand: str) -> bool:
    h = re.sub(r"[^a-z0-9]", "", handle.lower())
    for b in {key(brand).replace(" ", ""), norm(brand).replace(" ", "")}:
        if b and (h == b or (h.startswith(b) and h[len(b):] in SUFFIX)):
            return True
    return False


# ---------- known ids ----------

def load_known(path: Path | None = None, brain_records: list[dict] | None = None) -> dict:
    """{'pages': [{name, page_id, handles, aliases, source}], 'never': {page_id}} from the cache and brain records."""
    data = json.loads(Path(path or FIXTURES / "known_pages.json").read_text(encoding="utf-8"))
    pages = [dict(p, source=f"known_pages.json ({data.get('captured_at', '')})") for p in data.get("pages", [])]
    never = {str(n["page_id"]) for n in data.get("never", [])}
    for r in brain_records or []:
        v = r.get("value")
        if not isinstance(v, dict) or not v.get("page_id"):
            continue
        if r.get("field") == "lookalike_page" or "impostor" in str(v.get("verdict", "")):
            never.add(str(v["page_id"]))
            continue
        name = v.get("name") or v.get("page")
        if name:
            pages.append({"name": name, "page_id": str(v["page_id"]), "source": r.get("id", "brain")})
    return {"pages": [p for p in pages if str(p["page_id"]) not in never], "never": never}


def known_lookup(known: dict, name: str | None = None, handle: str | None = None, page_id: str | None = None):
    for p in known["pages"]:
        names = [p["name"], *p.get("aliases", [])]
        if page_id and str(p["page_id"]) == str(page_id):
            return p
        if handle and handle.lower() in [h.lower() for h in p.get("handles", [])]:
            return p
        if name and any(same_brand(name, n) for n in names):
            return p
    return None


# ---------- the site ----------

def site_links(pages_html: list[str]) -> list[dict]:
    """facebook.com links on the site, JSON-LD sameAs first. Each: {url, where, page_id?, name?, handle?}."""
    found, seen = [], set()

    def add(url: str, where: str):
        m = FB_LINK.search(html.unescape(url).replace("\\/", "/"))
        if not m:
            return
        path = [p for p in m.group(1).split("/") if p]
        query = urllib.parse.parse_qs((m.group(2) or "?")[1:])
        if not path or path[0].lower() in NOT_PAGES:
            return
        link = {"url": m.group(0), "where": where}
        if path[0] == "profile.php":
            if not query.get("id"):
                return
            link["page_id"] = query["id"][0]
        elif path[0].lower() in {"pages", "people", "pg"} and len(path) >= 2:
            link["name"] = urllib.parse.unquote(path[1]).replace("-", " ")
            ids = [p for p in path[2:] if p.isdigit()]
            if ids:
                link["page_id"] = ids[0]
            elif path[0].lower() == "pg":
                link["handle"] = path[1]
        elif path[0].isdigit():
            link["page_id"] = path[0]
        else:
            tail = re.search(r"-(\d{6,})$", path[0])  # facebook.com/Name-123456789
            link["handle"] = path[0]
            if tail:
                link["page_id"] = tail.group(1)
        k = (link.get("page_id"), (link.get("handle") or "").lower(), link.get("name"))
        if k not in seen:
            seen.add(k)
            found.append(link)

    for text in pages_html:
        for block in SAME_AS.findall(text):
            try:
                data = json.loads(block)
            except ValueError:
                continue
            for obj in data if isinstance(data, list) else [data]:
                same = obj.get("sameAs", []) if isinstance(obj, dict) else []
                for u in [same] if isinstance(same, str) else same:
                    add(u, "json-ld sameAs")
    for text in pages_html:
        for m in FB_LINK.finditer(html.unescape(text).replace("\\/", "/")):
            add(m.group(0), "site link")
    return found


def from_site(brand: str, pages_html: list[str], known: dict, fetch_page=None) -> dict | None:
    """First site link whose name or handle matches the brand and resolves to an id."""
    for link in site_links(pages_html):
        pid, name, handle = link.get("page_id"), link.get("name"), link.get("handle")
        if pid and str(pid) in known["never"]:
            continue
        hit = known_lookup(known, page_id=pid) if pid else None
        confirmed_name = (hit or {}).get("name") or name
        name_ok = (confirmed_name and same_brand(confirmed_name, brand)) or (handle and handle_matches(handle, brand))
        if not name_ok:
            continue
        if not pid and handle:
            hit = known_lookup(known, handle=handle) or known_lookup(known, name=brand)
            pid = hit and hit["page_id"]
            if not pid and fetch_page:
                pid = page_id_from_profile(fetch_page, link["url"])
        if pid:
            return {"page_id": str(pid), "found_by": f"site ({link['where']})", "link": link["url"],
                    "page_name": confirmed_name or handle}
    return None


def page_id_from_profile(fetch_page, url: str) -> str | None:
    """Live only: a public page's HTML may carry its numeric id. Returns None on a challenge or login wall."""
    status, text = fetch_page(url)
    if status != 200 or blocked(text):
        return None
    m = re.search(r'"(?:pageID|page_id|delegate_page_id)"\s*:\s*"?(\d{6,})', text) or re.search(r"fb://page/\?id=(\d+)", text)
    return m.group(1) if m else None


# ---------- the page search ----------

def blocked(text: str) -> bool:
    return bool(re.search(r"__rd_verify|/login/\?|id=\"login_form\"|checkpoint", text or ""))


def search_rows(text: str) -> list[dict]:
    """Page rows {page_id, name} from a page search response (JSON, or JSON embedded in HTML)."""
    rows = []

    def walk(o):
        if isinstance(o, dict):
            pid, name = o.get("page_id") or o.get("pageID"), o.get("name") or o.get("page_name")
            if pid and name:
                rows.append({"page_id": str(pid), "name": str(name)})
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    try:
        walk(json.loads(text))
    except ValueError:
        for blob in re.findall(r"\{[^{}]*\"page_id\"[^{}]*\}", text or ""):
            try:
                walk(json.loads(blob))
            except ValueError:
                continue
    return rows


def search_page(name: str, fetch, known: dict, country: str = "US") -> dict:
    """One page search; keep only an exact name match. {status, page_id?, rejected, why}."""
    url = SEARCH.format(country=country, q=urllib.parse.quote(name))
    status, text = fetch(url, name)
    if status is None:
        return {"status": "not_run", "url": url, "why": "no saved response and not live"}
    if status != 200 or blocked(text):
        return {"status": "unavailable", "url": url, "http": status,
                "why": "page search answered with a challenge or login wall; the founder pastes the id"}
    rows = [r for r in search_rows(text) if r["page_id"] not in known["never"]]
    keep = {r["page_id"]: r for r in rows if exact(r["name"], name)}
    rejected = sorted({r["name"].strip() for r in rows if r["page_id"] not in keep})
    if len(keep) == 1:
        (pid, row), = keep.items()
        return {"status": "found", "url": url, "page_id": pid, "page_name": row["name"].strip(), "rejected": rejected}
    why = "no exact name match" if not keep else f"{len(keep)} pages share the exact name; the founder picks"
    return {"status": "none", "url": url, "rejected": rejected, "why": why, "candidates": list(keep)}


def fixture_fetch(dir_: Path | None = None):
    dir_ = Path(dir_ or FIXTURES)
    index = json.loads((dir_ / "page-search.json").read_text(encoding="utf-8")).get("responses", {})

    def fetch(url, name=None):
        entry = next((v for k, v in index.items() if exact(k, name)), None)
        if not entry:
            return None, ""
        return entry.get("status", 200), (dir_ / entry["file"]).read_text(encoding="utf-8")
    return fetch


def live_fetch(pause: float = 1.0):
    def fetch(url, name=None):
        time.sleep(pause)
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status, r.read(2_000_000).decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, e.read(200_000).decode("utf-8", "replace")
        except (urllib.error.URLError, TimeoutError) as e:
            return 0, str(e)
    return fetch


# ---------- resolution ----------

def resolve(name: str, known: dict, fetch=None, country: str = "US") -> dict:
    """Known ids first (no network), then one page search. Never a keyword search."""
    hit = known_lookup(known, name=name)
    if hit:
        return {"page_id": str(hit["page_id"]), "found_by": f"known ids ({hit['source']})", "page_name": hit["name"]}
    if fetch:
        s = search_page(name, fetch, known, country)
        if s["status"] == "found":
            return {"page_id": s["page_id"], "found_by": "ad library page search (exact name)", "page_name": s["page_name"],
                    "rejected": s["rejected"]}
        return {"page_id": None, "found_by": None, "search": s}
    return {"page_id": None, "found_by": None}


def find_own_page(brand_name: str, site_html: list[str], known: dict, fetch=None, fetch_page=None,
                  country: str = "US") -> dict:
    site = from_site(brand_name, site_html, known, fetch_page)
    if site:
        return {"name": brand_name, **site}
    links = site_links(site_html)
    out = {"name": brand_name, **resolve(brand_name, known, fetch, country)}
    out["site_links"] = [l["url"] for l in links]
    if not out["page_id"]:
        out["next"] = "founder pastes the page id (Ad Library: open the page, copy view_all_page_id)"
    return out


# ---------- competitor proposal ----------

def load_brain(brand: str, root: Path) -> list[dict]:
    """Merged competitors and identity records, plus raw folders for a brand not merged yet. Deduped by id."""
    base = Path(root) / brand
    files = [base / "competitors.json", base / "identity.json", *sorted(base.glob("raw/*/competitors.json")),
             *sorted(base.glob("raw/*/identity.json"))]
    out, seen = [], set()
    for f in files:
        if not f.exists():
            continue
        data = json.loads(f.read_text(encoding="utf-8"))
        for r in data if isinstance(data, list) else data.get("records", []):
            if isinstance(r, dict) and r.get("id") not in seen:
                seen.add(r.get("id"))
                out.append(r)
    return out


def propose(brand_name: str, records: list[dict], peers: dict | None = None, limit: int = MAX_PROPOSALS) -> list[dict]:
    """Ranked competitor names with reasons citing record ids. Scores: founder set 5, named record 4,
    seen in the Ad Library 3, Reddit recommended-instead 2 plus 0.5 a mention, category peer 1."""
    peers = peers if peers is not None else json.loads(PEERS.read_text(encoding="utf-8"))
    cands: dict[str, dict] = {}
    never = {str(r["value"].get("page_id")) for r in records
             if r.get("field") == "lookalike_page" and isinstance(r.get("value"), dict)}

    def add(name, score, why, rid, page_id=None):
        k = key(name)
        if not k or same_brand(name, brand_name) or (page_id and str(page_id) in never):
            return
        c = cands.setdefault(k, {"name": name, "score": 0.0, "reasons": [], "names": set()})
        c["names"].add(name)
        if page_id and not c.get("page_id"):
            c["page_id"], c["name"] = str(page_id), name  # a page name with a known id reads best
        c["score"] += score
        c["reasons"].append({"why": why, "record": rid})

    for r in records:
        rid, field, v = r.get("id"), r.get("field"), r.get("value")
        if (r.get("section") or str(rid).split(".")[1:2] and str(rid).split(".")[1]) != "competitors":
            continue
        if field == "competitor_set" and isinstance(v, list):
            for n in v:
                add(n, 5, "in the brain's competitor set", rid)
        elif field == "competitor_frame" or field == "lookalike_page":
            continue
        elif isinstance(v, dict) and v.get("competitor") is not None:
            n = v.get("recommended_instead") or 0
            add(v["competitor"], 2 + 0.5 * n, f"Reddit threads recommend it instead {n} time{'' if n == 1 else 's'}"
                f" ({v.get('upvotes', 0)} upvotes, r/{', r/'.join(v.get('subreddits', []))})", rid)
        elif isinstance(v, dict) and v.get("page") and field == "competitor":
            add(v["page"], 3, f"runs {v.get('active_ads', 0)} active Meta ads (Ad Library)", rid, v.get("page_id"))
        elif isinstance(v, dict) and v.get("name"):
            add(v["name"], 4, "named competitor record", rid, v.get("page_id"))

    # Category peers: the founder's frame first, then words in the identity category.
    frame = next((r for r in records if r.get("field") == "competitor_frame"), None)
    category = next((r for r in records if str(r.get("id", "")).endswith("identity.category")), None)
    if frame and isinstance(frame.get("value"), str):
        for n in peers.get("frames", {}).get(frame["value"], []):
            add(n, 1, f"category peer for the founder's frame '{frame['value']}'", frame["id"])
    if category and isinstance(category.get("value"), str):
        words = set(norm(category["value"]).split())
        for word, names in peers.get("category_words", {}).items():
            if word in words:
                for n in names:
                    add(n, 1, f"category peer: identity says '{category['value']}'", category["id"])

    ranked = sorted(cands.values(), key=lambda c: (-c["score"], c["name"].lower()))[:limit]
    return [{"name": c["name"], "page_id": c.get("page_id"), "score": round(c["score"], 2),
             "also_called": sorted(c["names"] - {c["name"]}), "reasons": c["reasons"]} for c in ranked]


# ---------- config ----------

def write_config(path: Path, own: dict | None, proposals: list[dict], known: dict, fetch=None,
                 confirm: list[str] | None = None, country: str = "US") -> dict:
    """Own id into pages (role self), unconfirmed proposals into proposed_pages, confirmed names into pages.
    Writes only when something changed, so a second run leaves the file byte for byte the same."""
    path = Path(path)
    before = path.read_text(encoding="utf-8")
    cfg = json.loads(before)
    mal = cfg.setdefault("meta_ad_library", {})
    pages = mal.setdefault("pages", [])

    if own and own.get("page_id"):
        me = next((p for p in pages if p.get("role") == "self"), None)
        if not me:
            pages.insert(0, {"name": own["name"], "role": "self", "page_id": own["page_id"], "found_by": own["found_by"]})
        elif not me.get("page_id"):
            me.update(page_id=own["page_id"], found_by=own["found_by"])

    for p in pages:  # fill ids for configured pages that had none (Allbirds on 28 Sep)
        if not p.get("page_id"):
            got = resolve(p["name"], known, fetch, country)
            if got["page_id"]:
                p.update(page_id=got["page_id"], found_by=got["found_by"])

    previous = {key(p["name"]): p for p in mal.get("proposed_pages", [])}
    proposed = []
    for c in proposals:
        if any(same_brand(c["name"], p["name"]) for p in pages):
            continue
        entry = {"name": c["name"], "role": "proposed", "page_id": c.get("page_id"), "found_by": None,
                 "score": c["score"], "reasons": c["reasons"]}
        if entry["page_id"]:
            entry["found_by"] = "brain record"
        else:
            old = previous.get(key(c["name"]), {})
            got = resolve(c["name"], known, fetch, country) if not old.get("page_id") else \
                {"page_id": old["page_id"], "found_by": old.get("found_by")}
            entry.update(page_id=got["page_id"], found_by=got["found_by"])
            if not got["page_id"]:
                entry["next"] = "founder pastes the page id"
        proposed.append(entry)

    moved, missing = [], []
    for name in confirm or []:
        hit = next((e for e in proposed if same_brand(e["name"], name)), None)
        if not hit:
            if not any(same_brand(p["name"], name) for p in pages):
                missing.append(name)
            continue
        proposed.remove(hit)
        page = {"name": hit["name"], "role": "competitor"}
        if hit.get("page_id"):
            page.update(page_id=hit["page_id"], found_by=hit["found_by"])
        pages.append(page)
        moved.append(hit["name"])

    mal["proposed_pages"] = proposed
    after = json.dumps(cfg, indent=1, ensure_ascii=False) + "\n"
    if after != before:
        path.write_text(after, encoding="utf-8")
    return {"changed": after != before, "confirmed": moved, "not_found": missing, "proposed": len(proposed),
            "pages": len(pages)}


# ---------- run ----------

def read_site(site: str | None, live: bool) -> list[str]:
    if not site:
        return []
    if re.match(r"https?://", site):
        if not live:
            raise SystemExit("a site url needs --live; pass a saved html file for offline runs")
        status, text = live_fetch(0)(site)
        return [text] if status == 200 else []
    p = Path(site)
    return [f.read_text(encoding="utf-8", errors="replace") for f in (sorted(p.glob("*.html")) if p.is_dir() else [p])]


def run(brand: str, brand_name: str | None = None, *, site: str | None = None, root: Path | None = None,
        config_path: Path | None = None, live: bool = False, confirm: list[str] | None = None,
        search_fixtures: Path | None = None, known_path: Path | None = None) -> dict:
    root = Path(root or ROOT / "app" / "brain")
    config_path = Path(config_path or root / brand / "config" / "apify.json")
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    mal = cfg.get("meta_ad_library", {})
    country = mal.get("country", "US")
    brand_name = brand_name or next((p["name"] for p in mal.get("pages", []) if p.get("role") == "self"), None) \
        or cfg.get("reddit", {}).get("brand_name") or brand.title()
    records = load_brain(brand, root)
    known = load_known(known_path, records)
    fetch = live_fetch() if live else fixture_fetch(search_fixtures)
    own = find_own_page(brand_name, read_site(site, live), known, fetch, live_fetch() if live else None, country)
    proposals = propose(brand_name, records)
    result = write_config(config_path, own, proposals, known, fetch, confirm, country)
    return {"own": own, "proposals": proposals, **result}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--brand", required=True)
    ap.add_argument("--name", help="brand name as on Facebook; default: the self page in config")
    ap.add_argument("--site", help="saved html file or folder, or a url with --live")
    ap.add_argument("--out", default=str(ROOT / "app" / "brain"), help="brain root")
    ap.add_argument("--live", action="store_true", help="allow one fetch of the site and one page search per name")
    ap.add_argument("--confirm", help='comma list of proposed names to move into pages, e.g. "Darn Tough,Stance"')
    a = ap.parse_args(argv)
    confirm = [n.strip() for n in (a.confirm or "").split(",") if n.strip()]
    res = run(a.brand, a.name, site=a.site, root=Path(a.out), live=a.live, confirm=confirm)
    own = res["own"]
    print(f"own page: {own['name']} -> {own.get('page_id') or 'unresolved'} ({own.get('found_by') or own.get('next')})")
    for i, p in enumerate(res["proposals"], 1):
        print(f"{i:2}. {p['name']:<24} score {p['score']:<5} id {p.get('page_id') or '-':<18} "
              f"{'; '.join(r['why'] for r in p['reasons'][:2])}")
    print(f"config {'updated' if res['changed'] else 'unchanged'}: {res['pages']} pages, {res['proposed']} proposed;"
          f" confirmed {res['confirmed'] or 'none'}" + (f"; not found {res['not_found']}" if res["not_found"] else ""))


if __name__ == "__main__":
    main()
