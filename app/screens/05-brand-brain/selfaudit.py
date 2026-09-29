"""The brain audits itself: what in the brain is wrong about the brain, with the fix beside each line.

Four checks, none needing a model:
1. The brain-level audit (`app/brain/audit.py`): records past expiry, open conflicts, empty sections rooms need,
   documents in the manifest never extracted, BRAIN.md rows and version drifted from the records, links in BRAIN.md
   that point at missing files. Each is a proposal with a before, an after and a reason; here it gains a fix.
2. Duplicates: two active records in one section that say the same thing (same normalised text, or same scalar value
   under the same field), and since round 9 near twins: texts that share 3 words in 4 without being the same (negations count, words common to
   most of a section do not, the language bank is exact only). The
   stronger record (merge.strength: source rank, confidence, capture date) is kept, the other is proposed for
   retirement, with both texts shown so a person can unpick a pair that is two facts. Retire never deletes.
3. Read coverage: which sections screens read (the store's read log) against which sections hold records. A section
   nobody reads is held for no one; a section read often and thin is where a pull pays. Unavailable until a read is
   logged.
4. Documents: manifest entries whose file is no longer on disk.
Rules BRN-R24 (router drifted or broken) and BRN-R25 (duplicate records) put the fixes on the master list.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRAIN_DIR = HERE.parents[1] / "brain"
REPO = HERE.parents[2]
if str(BRAIN_DIR) not in sys.path:
    sys.path.insert(0, str(BRAIN_DIR))
import merge  # noqa: E402
import router  # noqa: E402
from store import SECTIONS  # noqa: E402

_aspec = importlib.util.spec_from_file_location("brain_level_audit", BRAIN_DIR / "audit.py")
brain_audit = importlib.util.module_from_spec(_aspec)
_aspec.loader.exec_module(brain_audit)

SKIP_DUP = {"freshness", "changes", "sources"}
FIX = {
    "stale": {"who": "agent", "text": "re-pull the record from its source, or confirm it in the review queue; retire it if no longer true", "route": "health"},
    "conflict": {"who": "person", "text": "settle it in the conflicts block; the site wins by default", "route": "conflicts"},
    "empty": {"who": "agent", "text": "connect the source that fills it, else the question goes to the founder round", "route": "questions"},
    "unread": {"who": "agent", "text": "run the extractor on the file; the records it proposes land in the review queue", "route": "files"},
    "drifted": {"who": "agent", "text": "regenerate BRAIN.md from the records; the founder notes block is kept", "route": "selfaudit/regenerate"},
    "broken_link": {"who": "person", "text": "create the file or point the row at one that exists", "route": None},
}


def _norm(v) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(v).lower()).strip()


def duplicates(brain) -> list[dict]:
    """Pairs of active records in one section that say the same thing. O(n): a dict keyed by the normalised text or value."""
    out = []
    for sec in SECTIONS:
        if sec in SKIP_DUP:
            continue
        seen: dict[tuple, dict] = {}
        for r in brain.records(sec):
            text = r.get("text") if isinstance(r.get("text"), str) else None
            val = r.get("value")
            keys = []
            if text and len(_norm(text)) >= 20:
                keys.append(("text", _norm(text)))
            if val is not None and not isinstance(val, (dict, list, bool)) and r.get("field"):
                keys.append(("value", r["field"], _norm(val)))
            for k in keys:
                if k in seen and seen[k]["id"] != r["id"]:
                    a, b = seen[k], r
                    keep, drop = (a, b) if merge.strength(a) >= merge.strength(b) else (b, a)
                    if any(d["retire"] == drop["id"] and d["keep"] == keep["id"] for d in out):
                        continue
                    out.append({"section": sec, "keep": keep["id"], "retire": drop["id"], "keep_tier": keep["tier"], "retire_tier": drop["tier"],
                                "keep_source": (keep.get("source") or {}).get("type"), "retire_source": (drop.get("source") or {}).get("type"),
                                "text": (keep.get("text") or str(keep.get("value")))[:140], "match": "same text" if k[0] == "text" else f"same value on {k[1]}"})
                else:
                    seen.setdefault(k, r)
    out.extend(near_duplicates(brain, {(d["keep"], d["retire"]) for d in out}))
    return out


STOP = {"the", "and", "for", "with", "that", "this", "from", "are", "was", "were", "has", "have", "its", "our", "you", "your", "but", "can", "all", "any", "one", "per", "into", "than", "then", "they", "them", "their", "will", "each", "more", "most", "also", "when", "what", "which", "about"}
NEAR_MIN_TOKENS = 6
NEAR_SIMILARITY = 0.75
NEAR_SKIP = {"language_bank"}  # quotes are meant to sound alike; only exact twins count there
NEAR_BOILERPLATE = 0.3  # a word in more than 3 records in 10 of a section is boilerplate (a shared prefix), not a shared fact


def _tokens(text: str) -> frozenset:
    return frozenset(w for w in _norm(text).split() if len(w) >= 3 and w not in STOP)


def near_duplicates(brain, seen_pairs: set | None = None) -> list[dict]:
    """Pairs of active records in one section whose texts share 3 words in 4 (Jaccard on word sets, 6 words or more),
    without being the same text. The stronger record is kept, as for exact twins. O(n squared) per section on word
    sets, which is fine at a few hundred records a section."""
    seen_pairs = seen_pairs or set()
    out = []
    for sec in SECTIONS:
        if sec in SKIP_DUP:
            continue
        if sec in NEAR_SKIP:
            continue
        recs = [(r, _tokens(r.get("text") or "")) for r in brain.records(sec) if isinstance(r.get("text"), str)]
        if len(recs) >= 10:
            df: dict[str, int] = {}
            for _, t in recs:
                for w in t:
                    df[w] = df.get(w, 0) + 1
            boiler = {w for w, n in df.items() if n / len(recs) > NEAR_BOILERPLATE}
            recs = [(r, t - boiler) for r, t in recs]
        recs = [(r, t) for r, t in recs if len(t) >= NEAR_MIN_TOKENS]
        for i in range(len(recs)):
            ra, ta = recs[i]
            for j in range(i + 1, len(recs)):
                rb, tb = recs[j]
                inter = len(ta & tb)
                if inter < NEAR_MIN_TOKENS:
                    continue
                sim = inter / len(ta | tb)
                if sim < NEAR_SIMILARITY or _norm(ra["text"]) == _norm(rb["text"]):
                    continue
                na, nb = set(re.findall(r"\d+(?:\.\d+)?", ra["text"])), set(re.findall(r"\d+(?:\.\d+)?", rb["text"]))
                if (na or nb) and na != nb:
                    continue  # the same words around different numbers are two facts, not a twin
                keep, drop = (ra, rb) if merge.strength(ra) >= merge.strength(rb) else (rb, ra)
                if (keep["id"], drop["id"]) in seen_pairs or (drop["id"], keep["id"]) in seen_pairs:
                    continue
                seen_pairs.add((keep["id"], drop["id"]))
                out.append({"section": sec, "keep": keep["id"], "retire": drop["id"], "keep_tier": keep["tier"], "retire_tier": drop["tier"],
                            "keep_source": (keep.get("source") or {}).get("type"), "retire_source": (drop.get("source") or {}).get("type"),
                            "text": (keep.get("text") or "")[:140], "other_text": (drop.get("text") or "")[:140], "near": True, "similarity": round(sim, 2),
                            "match": f"near twin, {round(sim * 100)} percent of words shared"})
    out.sort(key=lambda d: (-d["similarity"], d["section"], d["keep"]))
    return out


def read_coverage(brain) -> dict:
    reads = brain.reads()
    stats = brain.section_stats()
    if not reads:
        return {"available": False, "reason": "no read is logged yet; screens log a read when they load a section with a reader name", "sections": [], "unread": [], "hot_thin": []}
    by_sec: dict[str, list] = {}
    for r in reads:
        by_sec.setdefault(r.get("section"), []).append(r)
    rows = []
    for sec in SECTIONS:
        rs = by_sec.get(sec, [])
        readers = sorted({x.get("reader") for x in rs if x.get("reader")})
        rows.append({"section": sec, "records": stats.get(sec, {}).get("count", 0), "reads": len(rs), "readers": readers[:6], "last_read": rs[-1].get("at") if rs else None})
    unread = [r for r in rows if r["records"] and not r["reads"]]
    hot_thin = [r for r in rows if r["reads"] >= 3 and r["records"] <= 2]
    return {"available": True, "sections": rows, "unread": unread, "hot_thin": hot_thin, "total_reads": len(reads)}


def missing_files(brain) -> list[dict]:
    out = []
    for d in brain.documents():
        f = d.get("file")
        if f and not (brain.dir / "documents" / f).exists() and not (brain.dir / f).exists():
            out.append({"file": f, "added_at": d.get("added_at"), "fix": "put the file back under documents/, or remove the manifest row"})
    return out


def run(brain, repo: Path = REPO) -> dict:
    props = []
    for p in brain_audit.audit(brain, repo):
        fix = FIX.get(p["kind"]) or {"who": "person", "text": "review it", "route": None}
        props.append(dict(p, fix=fix))
    dups = duplicates(brain)
    cov = read_coverage(brain)
    files = missing_files(brain)
    by_kind: dict[str, int] = {}
    for p in props:
        by_kind[p["kind"]] = by_kind.get(p["kind"], 0) + 1
    router_ok = not any(p["kind"] in ("drifted", "broken_link") for p in props)
    return {"proposals": props, "duplicates": dups, "reads": cov, "missing_files": files,
            "counts": {"proposals": len(props), "by_kind": by_kind, "duplicates": len(dups), "missing_files": len(files), "unread_sections": len(cov["unread"]) if cov["available"] else None,
                       "total": len(props) + len(dups) + len(files)},
            "router": {"ok": router_ok, "file": "BRAIN.md", "exists": (brain.dir / "BRAIN.md").exists()},
            "note": "The brain checked against itself: expiry, conflicts, empty sections, unread files, the router against the records, links, duplicates, read coverage and files on disk. No model, no paid call. Every line ends in a fix; retire never deletes."}


def regenerate(brain) -> dict:
    """Rewrite BRAIN.md from the records, keeping the founder notes block. Returns the drift count before and after."""
    before = [p for p in brain_audit.drift(brain)]
    path = router.write(brain.brand, brain.root, brain.today)
    after = [p for p in brain_audit.drift(brain)]
    return {"ok": True, "file": str(path.relative_to(brain.root)), "drift_before": len(before), "drift_after": len(after), "tokens": router.tokens(path.read_text(encoding="utf-8"))}
