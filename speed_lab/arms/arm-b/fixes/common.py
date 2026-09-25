"""Shared helpers for arm B fix scripts. Each fix script builds variant arm-b-fNN from its parent."""
import os, re, shutil, sys, io
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "speed_lab"))
import lab  # noqa: E402
from lab import Variant, VARIANTS, key  # noqa: E402

HOME = "https://www.gehnaindia.com/"


def fresh(name, parent=None):
    """Start the variant from scratch (so the script is rerunnable), copying the parent's overrides."""
    d = os.path.join(VARIANTS, name)
    if os.path.exists(d):
        shutil.rmtree(d)
    return Variant(name, parent=parent)


def put_text(v, url, text, content_type, compress=True):
    """Override a text response. The replay server only compresses a body whose entry carries
    content-encoding, and Variant.put strips it, so restore it here to keep text compressed on the wire
    exactly like the base response (gzip level 6 in the replay server)."""
    body = text.encode("utf-8") if isinstance(text, str) else text
    v.put(url, body, content_type=content_type)
    if compress:
        v.idx[key(url)]["headers"]["content-encoding"] = "br"
        v.save()


def get_text(v, url):
    body, _ = v.get(url)
    return body.decode("utf-8")


def add_new(v, url, body, content_type, rtype, headers=None):
    """Add a response that is not in the base store, and label its type for the byte roll-ups."""
    v.add(url, body, content_type, headers=headers)
    v.idx[key(url)]["type"] = rtype
    v.save()
