"""The brand book: one printable document from the records, for a person or an agency, with nothing in it that the
brain does not hold.

Sections, in the order a brand book reads: who we are (identity), what we stand for (positioning and proof points),
who we speak to (the audience profiles), how we speak (the voice sheet and the founder's liked lines), our words
(the glossary), the lines we never cross (the red lines with reasons), the lines that never change (locked lines and
facts), what we look like (the palette with hex codes, the fonts, the logo rules), what we say about the basics (the
approved store facts), and where it all lives. Markdown to copy or download, with a print view on the page. Every
section says when it is empty. Web pass idea 14, the human-readable half.
"""
from __future__ import annotations


def _sec(title: str, lines: list[str], empty: str) -> list[str]:
    return [f"## {title}", ""] + (lines if lines else [f"_{empty}_"]) + [""]


def build(brain, parts: dict) -> dict:
    name = parts.get("name") or brain.brand.replace("_", " ").title()
    out = [f"# {name} brand book", "", f"Built from the brand brain on {brain.today.isoformat()}, version {brain.version()}. Nothing here is written by a model; every line has a record behind it.", ""]
    ident = parts.get("identity") or {}
    out += _sec("Who we are", [f"- {k.replace('_', ' ').capitalize()}: {v}" for k, v in ident.items() if v], "identity not filled yet")
    pos = parts.get("positioning") or {}
    out += _sec("What we stand for", ([f"- Frame: {pos['frame']}"] if pos.get("frame") else []) + ([f"- Proof points: {pos['proof_points']}"] if pos.get("proof_points") else []) + ([f"- Category: {pos['category_frame']}"] if pos.get("category_frame") else []), "positioning not set yet")
    au = parts.get("audiences") or []
    out += _sec("Who we speak to", [f"- **{p['name']}** ({round((p.get('share') or 0) * 100)} percent): {p.get('job')}" + (f" Fears: {', '.join(p.get('pains') or [])}." if p.get("pains") else "") + (f" Note: {p['note']}" if p.get("note") else "") for p in au[:8]], "no audience profile yet")
    vs = parts.get("voice") or {}
    voice_lines = [f"- {f['label']}: {f['text']}" for f in vs.get("fields") or [] if f.get("text")]
    ex = vs.get("examples") or []
    if isinstance(ex, dict):
        ex = [dict(e, liked=True) if isinstance(e, dict) else {"text": e, "liked": True} for e in (ex.get("liked") or [])]
    liked = [f"- Liked: \"{(e.get('text') if isinstance(e, dict) else e)}\"" for e in ex if (e.get("liked") if isinstance(e, dict) else True)][:5]
    out += _sec("How we speak", voice_lines + liked, "voice sheet not filled yet")
    gl = parts.get("glossary") or []
    out += _sec("Our words, spelt exactly so", [f"- {t['term']}" + (f" (never {', '.join(t['wrong'])})" if t.get("wrong") else "") + (f": {t['note']}" if t.get("note") else "") for t in gl[:40]], "no glossary term yet")
    rl = parts.get("redlines") or []
    out += _sec("The lines we never cross", [f"- {x['label']}: {x['text']}" + (f" (because {x['why']})" if x.get("why") else "") for x in rl[:30]], "no red line yet")
    lk = parts.get("locks") or {}
    out += _sec("The lines and numbers that never change", [f"- {x['label']}: {x['text']}" for x in lk.get("lines") or []] + [f"- {x['label']}: {x['value'] if not isinstance(x.get('value'), dict) else ', '.join(f'{k} {v}' for k, v in x['value'].items() if isinstance(v, (str, int, float)))}" for x in lk.get("facts") or []], "nothing locked yet")
    vz = parts.get("visual") or {}
    look = [f"- {c['name']}: {c['hex']} ({c['role']})" for c in vz.get("colours") or []] + ([f"- Fonts: {', '.join(f['name'] + ' (' + f['role'] + ')' for f in vz['fonts'])}"] if vz.get("fonts") else [])
    lr = (vz.get("logo_rules") or {}).get("value") or {}
    if lr:
        look.append("- Logo: " + ", ".join(x for x in [f"minimum {lr['min_size_px']} px" if lr.get("min_size_px") else "", f"clear space {lr['clear_space']}" if lr.get("clear_space") else "", ("never " + "; ".join(lr["never"])) if lr.get("never") else "", ("on " + ", ".join(lr["backgrounds"])) if lr.get("backgrounds") else ""] if x))
    out += _sec("What we look like", look, "no palette on file yet")
    fq = parts.get("facts") or []
    out += _sec("What we say about the basics", [f"- **{p['question']}** {p['answer']}" for p in fq if p.get("export")], "no approved store fact yet")
    out += ["## Where it lives", "", "- The brand brain screen holds every record behind this book, with its source, tier and date.", "- The brain file for an agent is the same content as strict and judgement rules, one per capability.", "- Ask the brain a plain question for anything not on this page.", ""]
    text = "\n".join(out)
    return {"text": text, "tokens": parts["tokens"](text), "name": name, "sections": [ln[3:] for ln in out if ln.startswith("## ")], "version": brain.version(),
            "note": "A brand book from the records: copy, download or print. Empty sections say so; fill them on their blocks and rebuild."}
