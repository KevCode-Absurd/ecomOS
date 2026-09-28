"""Download reference media at pull time into app/inspiration/media/<brand>/<origin>/ (git-ignored).

Meta's media links are signed and expire within days, so files are fetched when the ad is
pulled. Own-brand ads: every image and video. Competitor ads: the image and the video
thumbnail; the video itself stays a remote url with its expiry. A file that cannot be
fetched is skipped; a reference with nothing fetched reads media kind none.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import re
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEDIA_ROOT = HERE / "media"
MAX_BYTES = 60_000_000
TIMEOUT_S = 60
EXT = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif", "video/mp4": ".mp4"}


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (name or "").lower()).strip("_") or "unknown"


def url_expiry(url: str | None) -> str | None:
    """Expiry of a signed Meta CDN url from its oe= parameter (hex unix seconds), else None."""
    if not url:
        return None
    oe = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get("oe")
    if not oe:
        return None
    try:
        return dt.datetime.fromtimestamp(int(oe[0], 16), dt.timezone.utc).date().isoformat()
    except ValueError:
        return None


def _urllib_fetch(url: str, timeout: float):
    req = urllib.request.Request(url, headers={"User-Agent": "ecomOS-inspiration/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.headers.get("Content-Type", ""), resp.read(MAX_BYTES + 1)


class Downloader:
    """fetch(url, folder, stem) -> relative path or None. `fetch_fn` is injectable for tests."""

    def __init__(self, root: Path | str | None = None, fetch_fn=None, rel_to: Path | str | None = None):
        self.root = Path(root) if root else MEDIA_ROOT
        self.rel_to = Path(rel_to) if rel_to else HERE.parents[1]
        self._fetch = fetch_fn or _urllib_fetch
        self.errors: list[str] = []

    def fetch(self, url: str | None, brand: str, origin: str, stem: str) -> str | None:
        if not url or not url.startswith(("http://", "https://")):
            return None
        try:
            ctype, body = self._fetch(url, TIMEOUT_S)
        except Exception as exc:  # expired link, 403, timeout: the reference keeps no file
            self.errors.append(f"{stem}: {type(exc).__name__}")
            return None
        if not body or len(body) > MAX_BYTES:
            self.errors.append(f"{stem}: empty or over {MAX_BYTES} bytes")
            return None
        ctype = (ctype or "").split(";")[0].strip().lower()
        ext = EXT.get(ctype) or Path(urllib.parse.urlparse(url).path).suffix.lower()
        if ext not in EXT.values():
            self.errors.append(f"{stem}: content type {ctype or 'unknown'} not kept")
            return None
        folder = self.root / slug(brand) / slug(origin)
        folder.mkdir(parents=True, exist_ok=True)
        name = f"{stem}-{hashlib.sha1(url.encode()).hexdigest()[:8]}{ext}"
        (folder / name).write_bytes(body)
        try:
            return (folder / name).resolve().relative_to(self.rel_to.resolve()).as_posix()
        except ValueError:
            return (folder / name).as_posix()


def _video_urls(video: dict) -> tuple[str | None, str | None]:
    url = video.get("video_hd_url") or video.get("video_sd_url") or video.get("url")
    thumb = video.get("video_preview_image_url") or video.get("thumbnail_url")
    return url, thumb


def collect(item: dict, rights: str, brand: str, origin: str, stem: str, dl: Downloader | None,
            note: str | None = None) -> dict:
    """The media block for one ad. dl None means no download (mock mode): kind none with a note."""
    snap = item.get("snapshot") or {}
    images = [i.get("original_image_url") or i.get("resized_image_url") for i in snap.get("images") or []]
    for card in snap.get("cards") or []:
        images.append(card.get("original_image_url") or card.get("resized_image_url"))
    images = [u for u in images if u]
    videos = [_video_urls(v) for v in snap.get("videos") or []]
    for card in snap.get("cards") or []:
        if card.get("video_hd_url") or card.get("video_sd_url"):
            videos.append(_video_urls(card))
    remote = videos[0][0] if videos else (images[0] if images else None)
    block = {"kind": "none", "path": None, "thumbnail": None, "remote_url": None, "expires": None,
             "rights": rights, "files": [], "note": note}
    if dl is None:
        return block
    block["remote_url"] = remote
    block["expires"] = url_expiry(remote)
    files: list[str] = []
    for i, url in enumerate(images):
        p = dl.fetch(url, brand, origin, f"{stem}-img{i}")
        if p:
            files.append(p)
            block["path"] = block["path"] or p
    for i, (vurl, thumb) in enumerate(videos):
        t = dl.fetch(thumb, brand, origin, f"{stem}-thumb{i}")
        if t:
            files.append(t)
            block["thumbnail"] = block["thumbnail"] or t
        if rights == "own_brand":
            v = dl.fetch(vurl, brand, origin, f"{stem}-vid{i}")
            if v:
                files.append(v)
                block["path"] = v if i == 0 else block["path"]
    block["files"] = files
    if videos and (block["thumbnail"] or (rights == "own_brand" and block["path"])):
        block["kind"] = "video"
    elif block["path"]:
        block["kind"] = "image"
    else:
        block["note"] = "media could not be fetched at pull time" if (images or videos) else "the ad carried no media"
    return block
