"""Shared helpers for arm A fix scripts."""
import os, sys, re, io, shutil
LAB = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, LAB)
from lab import Variant, VARIANTS, read, key  # noqa: E402

HOME = "https://www.gehnaindia.com/"
ORIGIN = "https://www.gehnaindia.com"
CSS_MAIN = ORIGIN + "/_next/static/css/f45806cc85ed262f.css"
APP_JS = ORIGIN + "/_next/static/chunks/pages/_app-dce0792d73ac490d.js"


def fresh(name, parent=None):
    """Rebuild a variant from scratch so each fix script is rerunnable."""
    d = os.path.join(VARIANTS, name)
    if os.path.isdir(d):
        shutil.rmtree(d)
    return Variant(name, parent=parent)


def set_encoding(v, url, enc="gzip"):
    """Mark a text override as compressible so the replay server gzips it like the base did.
    Variant.put() strips content-encoding; the base HTML, CSS and JS were stored as br and served gzip."""
    k = key(url)
    v.idx[k]["headers"]["content-encoding"] = enc
    v.save()


def put_text(v, url, text, ctype):
    v.put(url, text.encode("utf-8"), content_type=ctype)
    set_encoding(v, url)


def get_text(v, url):
    body, _ = v.get(url)
    return body.decode("utf-8")
