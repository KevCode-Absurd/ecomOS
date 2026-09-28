"""The brain in one page for a new team member: what the brand is, what it never does, who it speaks to, how it
speaks, the numbers that must stay right, who keeps what, what is connected, and what is still open.

Built from the same modules the screen uses, as markdown to copy, download or print: the brand card (T0), the
positioning and proof points, the audience profiles (defaults first), the voice sheet lines, the red lines with
reasons, the locked lines and facts, the section owners, the connected sources, the top open questions, the last 5
decisions, the competitors on file, and where each thing lives on the screen. No model writes it; every line names
its record or block. It is the page a new hire, an agency lead or a reviewer reads on day one.
"""
from __future__ import annotations


def _lines(items, fmt, n=None, none="none on file"):
    items = list(items)[:n] if n else list(items)
    return [f"- {fmt(x)}" for x in items] if items else [f"- {none}"]


def build(brain, parts: dict) -> dict:
    name = next((r.get("value") for r in brain.records("identity") if r.get("field") == "name" and isinstance(r.get("value"), str)), brain.brand.replace("_", " ").title())
    out = [f"# {name}: the brain in one page", "", f"For a new team member, {brain.today.isoformat()}. Brain version {brain.version()}. Built from the records; every line names where it lives. Read this, then the brain screen.", ""]
    out += ["## What the brand is", "", parts.get("t0") or "unavailable", ""]
    frame, proof = parts.get("frame"), parts.get("proof_points")
    out += ["## Positioning", ""]
    out.append(f"- Frame ({frame['tier'].replace('_', ' ')}): {frame['text']}" if frame else "- no positioning frame on file (profile block)")
    if proof:
        out.append(f"- Proof points: {proof}")
    out.append("")
    au = parts.get("audiences") or {}
    order = sorted(au.get("profiles") or [], key=lambda p: (0 if p.get("default_for") else 1, 0 if p.get("approved") else 1, -(p.get("share") or 0)))
    out += ["## Who we speak to (audience profiles; defaults first)", ""] + _lines(order, lambda p: ("default for " + ", ".join(p["default_for"]) + ": " if p.get("default_for") else "") + f"{p['name']} ({round((p.get('share') or 0) * 100)} percent): {p.get('job')}" + (" [approved]" if p.get("approved") else " [evidence only]"), 6) + [""]
    vs = parts.get("voice") or {}
    out += ["## How we speak (voice sheet)", ""] + _lines([f for f in vs.get("fields") or [] if f.get("text")], lambda f: f"{f['label']}: {f['text']}", None, "voice sheet not filled yet (voice block)") + [""]
    rl = parts.get("redlines") or {}
    out += ["## What we never do (red lines)", ""] + _lines(rl.get("lines") or [], lambda x: f"{x['label']}: {x['text']}" + (f" (because {x['why']})" if x.get("why") else " (no reason on file)"), 15) + [""]
    lk = parts.get("locks") or {}
    out += ["## Lines and numbers no one rewrites", ""] + _lines(lk.get("lines") or [], lambda x: f"{x['label']}: {x['text']}", 8) + _lines(lk.get("facts") or [], lambda x: f"{x['label']}: " + (", ".join(f"{k} {v}" for k, v in x['value'].items() if isinstance(v, (str, int, float))) if isinstance(x.get('value'), dict) else str(x.get('value'))) + f" ({x['record']})", 8) + [""]
    ow = parts.get("owners") or {}
    assigned = [r for r in ow.get("rows") or [] if r.get("assigned")]
    out += ["## Who keeps what", ""] + _lines(assigned, lambda r: f"{r['label']}: {r['owner']}, every {r['cadence_days']} days" + (f", last {r['last']}" if r.get("last") else ""), None, "no section has an owner yet (owners block)") + [""]
    con = parts.get("connectors") or {}
    connected = [c for c in con.get("categories") or [] if c.get("connected")]
    out += ["## What is connected", ""] + _lines(connected, lambda c: f"{c['label']}: {', '.join(c['connected']) if isinstance(c.get('connected'), list) else c['connected']}", None, "no source connected; every number is simulated or public") + [""]
    comp = parts.get("competitors") or []
    out += ["## Who we are measured against", ""] + _lines(sorted(comp), lambda p: p, 20, "no competitor page on file") + [""]
    qs = parts.get("questions") or []
    out += ["## What is still open (top questions)", ""] + _lines(qs, lambda q: f"{q['question']}" + (f" ({q['hint']})" if q.get("hint") else ""), 5, "no open question") + [""]
    dec = parts.get("decisions") or []
    out += ["## The last decisions", ""] + _lines(dec, lambda d: f"{d.get('date') or ''}: {d.get('text') or d.get('title')}", 5, "no decision logged") + [""]
    out += ["## Where things live", "", "- The plan: the top of the brain screen; every action has an owner, steps and an artefact.", "- Ask the brain: the box under the plan; a plain question, a sourced answer.", "- Review first: the scanner in the claims block; every draft goes through it before a person reads it.",
            "- The brain file for an agent: the package block; one markdown per capability.", "- Files in: drop notes or a brand book; records propose themselves for your tick.", "- Exports and what changed: the permissions block.", ""]
    text = "\n".join(out)
    return {"text": text, "tokens": parts["tokens"](text), "sections": [ln[3:] for ln in out if ln.startswith("## ")], "name": name, "version": brain.version(),
            "note": "One page from the records: read it on day one, then the screen. Copy, download or print; nothing here is written by a model."}
