"""What changed since this export: the brain now against an earlier export bundle, record by record.

The export button writes one JSON (format "ecomOS brain export v1") with every section's raw records. Dropping that
file back in gives, per section: records added since, records retired or gone, records whose value, tier, status or
visibility moved (with the value before and after, shortened), documents added, and whether the router text
changed. Counts are sums over those lists; the version hashes and the export date frame it. Plain text to copy.
Nothing is written; the export stays as it was. A file that is not an ecomOS export says so.
"""
from __future__ import annotations

import datetime as dt
import json

FORMAT = "ecomOS brain export v1"


def _short(v, n: int = 100) -> str | None:
    if v is None:
        return None
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    return s if len(s) <= n else s[: n - 1] + "…"


def diff(brain, bundle: dict, sections_list) -> dict | tuple[int, dict]:
    if not isinstance(bundle, dict) or bundle.get("format") != FORMAT or not isinstance(bundle.get("sections"), dict):
        return 400, {"error": f"not an ecomOS brain export ({FORMAT}); drop the file the export button wrote"}
    if bundle.get("brand") and bundle.get("brand") != brain.brand:
        return 400, {"error": f"the export is for {bundle.get('brand')}, this screen is on {brain.brand}"}
    old_secs = bundle["sections"]
    per_section = []
    added, gone, changed = [], [], []
    for sec in sections_list:
        old = {r.get("id"): r for r in (old_secs.get(sec) or []) if isinstance(r, dict) and r.get("id")}
        new = {r.get("id"): r for r in brain.raw(sec) if isinstance(r, dict) and r.get("id")}
        if not old and not new:
            continue
        a = [rid for rid in new if rid not in old]
        g = [rid for rid in old if rid not in new or (new[rid].get("status") == "retired" and old[rid].get("status", "active") != "retired")]
        c = []
        for rid, nr in new.items():
            o = old.get(rid)
            if o is None or rid in g:
                continue
            moves = []
            if o.get("value") != nr.get("value"):
                moves.append({"what": "value", "before": _short(o.get("value")), "after": _short(nr.get("value"))})
            for k in ("tier", "status", "visibility"):
                if (o.get(k) or ("active" if k == "status" else None)) != (nr.get(k) or ("active" if k == "status" else None)):
                    moves.append({"what": k, "before": o.get(k), "after": nr.get(k)})
            if moves:
                c.append({"id": rid, "field": nr.get("field"), "moves": moves, "text": _short(nr.get("text") or "", 120)})
        per_section.append({"section": sec, "then": len(old), "now": len([r for r in new.values() if r.get("status", "active") != "retired"]), "added": len(a), "gone": len(g), "changed": len(c),
                            "added_ids": a[:20], "gone_ids": g[:20], "changes": c[:30]})
        added += [{"id": x, "section": sec, "text": _short(new[x].get("text") or new[x].get("value"), 120), "tier": new[x].get("tier")} for x in a]
        gone += [{"id": x, "section": sec, "text": _short(old[x].get("text") or old[x].get("value"), 120), "now": "retired" if x in new else "not in the brain"} for x in g]
        changed += [dict(x, section=sec) for x in c]
    old_docs = {d.get("file") for d in (bundle.get("documents_manifest") or []) if isinstance(d, dict)}
    docs_added = [d.get("file") for d in brain.documents() if d.get("file") not in old_docs]
    router_changed = None
    if isinstance(bundle.get("router_md"), str):
        p = brain.dir / "BRAIN.md"
        try:
            router_changed = (p.read_text(encoding="utf-8") if p.is_file() else "") != bundle["router_md"]
        except OSError:
            router_changed = None
    since = None
    try:
        since = (brain.today - dt.date.fromisoformat(str(bundle.get("exported_at"))[:10])).days
    except (TypeError, ValueError):
        since = None
    counts = {"added": len(added), "gone": len(gone), "changed": len(changed), "documents_added": len(docs_added), "sections_touched": sum(1 for s in per_section if s["added"] or s["gone"] or s["changed"])}
    lines = [f"{brain.brand}: changes since the export of {bundle.get('exported_at') or 'an unknown date'}" + (f" ({since} days ago)" if since is not None else "") + f", version {bundle.get('version')} to {brain.version()}", ""]
    lines.append(f"{counts['added']} records added, {counts['gone']} retired or gone, {counts['changed']} changed, {counts['documents_added']} documents added" + (", router changed" if router_changed else (", router unchanged" if router_changed is False else "")) + ".")
    for s in per_section:
        if s["added"] or s["gone"] or s["changed"]:
            lines.append(f"- {s['section'].replace('_', ' ')}: {s['then']} then, {s['now']} now; +{s['added']}, -{s['gone']}, {s['changed']} changed")
    for x in changed[:15]:
        m = x["moves"][0]
        lines.append(f"  {x['id']}: {m['what']} {m.get('before')} to {m.get('after')}")
    if not (added or gone or changed or docs_added):
        lines.append("Nothing changed since that export.")
    return {"since_days": since, "exported_at": bundle.get("exported_at"), "version_then": bundle.get("version"), "version_now": brain.version(), "same": bundle.get("version") == brain.version(),
            "counts": counts, "sections": per_section, "added": added[:200], "gone": gone[:200], "changed": changed[:200], "documents_added": docs_added, "router_changed": router_changed, "text": "\n".join(lines),
            "note": "Record by record against the export you dropped: ids that appeared, ids retired or gone, values, tiers, statuses and visibility that moved. Nothing is written; keep the export as your own copy."}
