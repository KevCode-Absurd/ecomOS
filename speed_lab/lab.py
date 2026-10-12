"""Helpers shared by the recorder, server and variant builders."""
import hashlib, json, os, shutil
from urllib.parse import urlsplit, urlunsplit

ROOT = os.path.dirname(os.path.abspath(__file__))
STORE = os.environ.get("SPEED_LAB_STORE") or os.path.join(ROOT, "store")  # set SPEED_LAB_STORE to record or serve another capture
VARIANTS = os.path.join(ROOT, "variants")
ACTIVE = os.path.join(ROOT, "ACTIVE_VARIANT")


def norm(url: str) -> str:
    s = urlsplit(url)
    return urlunsplit((s.scheme.lower(), s.netloc.lower(), s.path or "/", s.query, ""))


def key(url: str) -> str:
    return hashlib.sha1(norm(url).encode()).hexdigest()


def load_index(path=STORE) -> dict:
    p = os.path.join(path, "index.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def save_index(idx: dict, path=STORE):
    json.dump(idx, open(os.path.join(path, "index.json"), "w", encoding="utf-8"), indent=0)


def read(url: str, path=STORE) -> tuple[bytes, dict] | None:
    """Return (body, entry) for a stored url, or None."""
    idx = load_index(path)
    k = key(url)
    if k not in idx:
        return None
    e = idx[k]
    body = open(os.path.join(path, e["file"]), "rb").read() if e.get("file") else b""
    return body, e


class Variant:
    """A variant is a directory of overrides on top of the base store.

    v = Variant("arm-a-step1"); v.put(url, body, content_type="font/woff2"); v.drop(url); v.add(url, body, ...)
    Overrides win over the base store. A dropped url is served as 404.
    """

    def __init__(self, name: str, parent: str | None = None):
        self.name = name
        self.dir = os.path.join(VARIANTS, name)
        os.makedirs(self.dir, exist_ok=True)
        self.idx = load_index(self.dir)
        if parent and not self.idx:
            pdir = os.path.join(VARIANTS, parent)
            for k, e in load_index(pdir).items():
                if e.get("file"):
                    shutil.copy(os.path.join(pdir, e["file"]), os.path.join(self.dir, e["file"]))
                self.idx[k] = dict(e)
            self.save()

    def save(self):
        save_index(self.idx, self.dir)

    def get(self, url: str):
        r = read(url, self.dir)
        return r if r else read(url)

    def put(self, url: str, body: bytes, content_type: str | None = None, headers: dict | None = None, status: int = 200):
        base = self.get(url)
        h = dict(base[1]["headers"]) if base else {}
        if headers:
            h.update(headers)
        if content_type:
            h["content-type"] = content_type
        h.pop("content-encoding", None)
        h.pop("content-length", None)
        k = key(url)
        fn = k + ".bin"
        open(os.path.join(self.dir, fn), "wb").write(body)
        self.idx[k] = {"url": norm(url), "status": status, "headers": h, "file": fn, "size": len(body), "type": (base[1].get("type") if base else "other")}
        self.save()

    def drop(self, url: str):
        k = key(url)
        self.idx[k] = {"url": norm(url), "status": 404, "headers": {"content-type": "text/plain"}, "file": None, "size": 0, "type": "dropped"}
        self.save()

    def add(self, url: str, body: bytes, content_type: str, headers: dict | None = None):
        self.put(url, body, content_type=content_type, headers=headers)


def set_active(name: str | None):
    if name is None:
        if os.path.exists(ACTIVE):
            os.remove(ACTIVE)
    else:
        open(ACTIVE, "w").write(name)


def get_active() -> str | None:
    return open(ACTIVE).read().strip() if os.path.exists(ACTIVE) else None
