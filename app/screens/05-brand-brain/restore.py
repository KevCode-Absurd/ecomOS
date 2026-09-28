"""Restore from an export: put an earlier export's records back for the sections you choose, as founder-approved
records, with everything logged and nothing deleted.

The export bundle (the JSON the export button writes, sent whole or in 24 KB parts like the diff) holds every
section's raw records. Restore takes the sections named, and for each record in the export writes it back through
the store (a changed value moves the current one into history; a record the brain no longer holds is re-added), and
retires the records the brain has that the export does not, so the section reads as it did. The founder chooses the
sections; the diff (5.6) shows what will move before the restore runs. A restore of a section is one logged change
with the counts. Nothing is deleted: history and retired records stay.
"""
from __future__ import annotations

FORMAT = "ecomOS brain export v1"


def plan(brain, bundle: dict, sections: list[str], all_sections) -> dict | tuple[int, dict]:
    if not isinstance(bundle, dict) or bundle.get("format") != FORMAT or not isinstance(bundle.get("sections"), dict):
        return 400, {"error": f"not an ecomOS brain export ({FORMAT})"}
    if bundle.get("brand") and bundle.get("brand") != brain.brand:
        return 400, {"error": f"the export is for {bundle.get('brand')}, this screen is on {brain.brand}"}
    secs = [s for s in sections if s in all_sections and s in bundle["sections"] and s not in ("changes", "freshness")]
    if not secs:
        return 400, {"error": "name at least one section the export holds (changes and freshness are never restored)"}
    out = []
    for sec in secs:
        old = {r["id"]: r for r in bundle["sections"].get(sec) or [] if isinstance(r, dict) and r.get("id")}
        now = {r["id"]: r for r in brain.raw(sec) if isinstance(r, dict) and r.get("id")}
        re_add = [rid for rid in old if rid not in now]
        change = [rid for rid in old if rid in now and (now[rid].get("value") != old[rid].get("value") or now[rid].get("status", "active") != old[rid].get("status", "active") or now[rid].get("tier") != old[rid].get("tier"))]
        retire = [rid for rid in now if rid not in old and now[rid].get("status", "active") != "retired"]
        out.append({"section": sec, "in_export": len(old), "now": len(now), "re_add": re_add, "change": change, "retire": retire})
    return {"sections": out, "counts": {"re_add": sum(len(x["re_add"]) for x in out), "change": sum(len(x["change"]) for x in out), "retire": sum(len(x["retire"]) for x in out)}}


def apply(brain, bundle: dict, sections: list[str], all_sections) -> dict | tuple[int, dict]:
    p = plan(brain, bundle, sections, all_sections)
    if isinstance(p, tuple):
        return p
    done, errors = [], []
    for sec_plan in p["sections"]:
        sec = sec_plan["section"]
        old = {r["id"]: r for r in bundle["sections"].get(sec) or [] if isinstance(r, dict) and r.get("id")}
        for rid in sec_plan["re_add"] + sec_plan["change"]:
            rec = dict(old[rid])
            rec.pop("age_days", None)
            rec.pop("expired", None)
            rec.pop("date", None)
            src = dict(rec.get("source") or {})
            src["restored_from"] = {"export": bundle.get("exported_at"), "version": bundle.get("version")}
            rec["source"] = src
            errs = brain.put(rec)
            if errs:
                errors.append({"id": rid, "error": "; ".join(errs)})
            else:
                done.append(rid)
        for rid in sec_plan["retire"]:
            if brain.retire(rid):
                done.append(rid)
    return {"ok": not errors, "sections": [x["section"] for x in p["sections"]], "counts": dict(p["counts"], written=len(done), errors=len(errors)), "errors": errors[:20], "plan": p["sections"]}
