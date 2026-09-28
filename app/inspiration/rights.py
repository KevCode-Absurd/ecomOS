"""The generation boundary. Every generation, copy or brief call that takes a reference as
input goes through assert_generation_input first (app/contracts/inspiration.md section 4).

Own-brand references pass. Competitor and leader references are reference_only: they are
shown to people for layout, mood, format and cadence, and are refused here.
"""
from __future__ import annotations

from pathlib import Path

MEDIA_ROOT = Path(__file__).resolve().parent / "media"


class RightsError(PermissionError):
    """A reference_only reference or file reached the generation boundary."""


def assert_generation_input(reference: dict) -> dict:
    """Return the reference when it may feed generation; raise RightsError otherwise."""
    media = reference.get("media") or {}
    origin = reference.get("origin") or {}
    rights, role = media.get("rights"), origin.get("role")
    if rights != "own_brand" or role != "own":
        raise RightsError(f"{reference.get('id')}: rights {rights!r}, origin {origin.get('brand')!r} ({role}); "
                          "reference_only media is never passed to generation, copy or a brief")
    return reference


def generation_files(reference: dict) -> list[str]:
    """Local media files of a reference that may feed generation. Raises for reference_only."""
    assert_generation_input(reference)
    media = reference["media"]
    files = list(media.get("files") or [])
    for key in ("path", "thumbnail"):
        if media.get(key) and media[key] not in files:
            files.append(media[key])
    return files


def assert_generation_path(path: str | Path, references: list[dict]) -> Path:
    """A local file may feed generation only when an own-brand reference lists it."""
    p = Path(path)
    for ref in references:
        media = ref.get("media") or {}
        listed = set(media.get("files") or []) | {media.get("path"), media.get("thumbnail")}
        if str(p) in listed or p.as_posix() in listed:
            assert_generation_input(ref)
            return p
    raise RightsError(f"{p}: no own-brand reference lists this file; it cannot feed generation")
