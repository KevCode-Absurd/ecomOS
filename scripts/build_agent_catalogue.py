"""Merge agent capability files into the catalogue and render the readable index, the skills index and the page.

Inputs:  agents/specialists/*.json (capability arrays), agents/loop/LOOP.json (cross-cutting), agents/loop/*.md and agents/specialists/*.md
Outputs: agents/catalogue.json, agents/CATALOGUE.md, agents/SKILLS.md, reviews/agents/ecomos-agent-catalogue.html
Usage:   python3 scripts/build_agent_catalogue.py
"""
import glob, html, json, os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "agents")
AGENTS = [  # code, file, layer, name
    ("ORCH", "loop/ORCHESTRATOR.md", "loop", "Orchestrator"), ("DIAG", "loop/DIAGNOSE.md", "loop", "Diagnose"),
    ("PROP", "loop/PROPOSE.md", "loop", "Propose"), ("REG", "loop/REGISTRAR.md", "loop", "Registrar"),
    ("QA", "loop/QA-GATE.md", "loop", "QA Gate"), ("BRN", "loop/BRAIN-KEEPER.md", "loop", "Brand Brain Keeper"),
    ("SCT", "loop/REFERENCE-SCOUT.md", "loop", "Reference Scout"),
    ("SITE", "specialists/SITE.md", "specialist", "Site"), ("CREA", "specialists/CREA.md", "specialist", "Paid creative and copy"),
    ("MEDIA", "specialists/MEDIA.md", "specialist", "Media buyer"), ("LIFE", "specialists/LIFE.md", "specialist", "Lifecycle"),
    ("ORG", "specialists/ORG.md", "specialist", "Organic and search"), ("PROD", "specialists/PROD.md", "specialist", "Product and supply"),
    ("MONEY", "specialists/MONEY.md", "specialist", "Money and ops"), ("BRAND", "specialists/BRAND.md", "specialist", "Brand strategist"),
]
CODE2NAME = {c: n for c, _, _, n in AGENTS}
LOOP_OWNER = {"Orchestrator": "ORCH", "Diagnose": "DIAG", "Propose": "PROP", "Registrar": "REG", "QA Gate": "QA", "Brand Brain Keeper": "BRN", "Reference Scout": "SCT"}


def loop_caps_from_md(code, path):
    """Parse the capability index table in a loop agent file."""
    caps = []
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"## Capability index\n(.*?)(\n## |\Z)", txt, re.S)
    if not m:
        return caps
    for line in m.group(1).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and re.match(r"^[A-Z]+-C\d+$", cells[0]):
            caps.append({"id": cells[0], "agent": code, "name": cells[1], "trigger": cells[2], "autonomy": cells[3],
                         "folders": [], "what": "", "encompasses": [], "inputs": [], "outputs": [], "tools": [], "skills": [],
                         "external_write": {"needed": False, "surface": None}, "sources": {"web": [], "bank": []},
                         "found_in": "design", "founder_sees": ""})
    return caps


def load():
    caps = []
    for code, rel, layer, name in AGENTS:
        p = os.path.join(A, rel)
        if layer == "loop" and os.path.exists(p):
            caps += loop_caps_from_md(code, p)
        jp = os.path.join(A, rel.replace(".md", ".json"))
        if layer == "specialist" and os.path.exists(jp):
            for c in json.load(open(jp, encoding="utf-8")):
                c["agent"] = code
                caps.append(c)
    lp = os.path.join(A, "loop", "LOOP.json")
    if os.path.exists(lp):
        for c in json.load(open(lp, encoding="utf-8")):
            c["agent"] = LOOP_OWNER.get(c.get("owner_agent", ""), "ORCH")
            caps.append(c)
    # wave 2: role-first research. New records append; extensions merge into their base record.
    base = {c["id"]: c for c in caps}
    wave2 = [(code, os.path.join(A, rel.replace(".md", ".wave2.json"))) for code, rel, layer, name in AGENTS if layer == "specialist"]
    wave2.append(("LOOP", os.path.join(A, "loop", "LOOP.wave2.json")))
    for code, wp in wave2:
        if not os.path.exists(wp):
            continue
        for c in json.load(open(wp, encoding="utf-8")):
            c["agent"] = LOOP_OWNER.get(c.get("owner_agent", ""), "ORCH") if code == "LOOP" else code
            ext = c.get("extends")
            if ext and ext in base:
                b = base[ext]
                for k in ("encompasses", "inputs", "outputs", "tools", "skills"):
                    b[k] = list(dict.fromkeys((b.get(k) or []) + (c.get(k) or [])))
                b.setdefault("sources", {}).setdefault("web", []).extend((c.get("sources") or {}).get("web", []))
                b["found_in"] = "web+bank" if b.get("found_in") in ("bank_only", "web+bank") else b.get("found_in")
                b.setdefault("extensions", []).append({"name": c.get("name"), "what": c.get("what"), "human_role": c.get("human_role")})
            elif c["id"] not in base:
                base[c["id"]] = c; caps.append(c)
    seen = set(); out = []
    for c in caps:
        if c["id"] in seen:
            continue
        seen.add(c["id"]); out.append(c)
    return apply_review(out)


def apply_review(caps):
    """Apply agents/REVIEW.json: merges (drop into keep), reassignments, gap records, autonomy changes."""
    rp = os.path.join(A, "REVIEW.json")
    if not os.path.exists(rp):
        return caps
    rv = json.load(open(rp, encoding="utf-8"))
    by = {c["id"]: c for c in caps}
    dropped = set()
    for m in rv.get("merge", []):
        k = by.get(m["keep"])
        if not k:
            continue
        for d in m.get("drop", []):
            x = by.get(d)
            if not x or d == m["keep"]:
                continue
            for f in ("encompasses", "inputs", "outputs", "tools", "skills"):
                k[f] = list(dict.fromkeys((k.get(f) or []) + (x.get(f) or [])))
            ks = k.setdefault("sources", {}); xs = x.get("sources") or {}
            ks["web"] = list(dict.fromkeys((ks.get("web") or []) + (xs.get("web") or [])))
            ks["bank"] = list(dict.fromkeys((ks.get("bank") or []) + (xs.get("bank") or [])))
            k.setdefault("merged_from", []).append({"id": d, "name": x.get("name"), "agent": x.get("agent"), "reason": m.get("reason")})
            dropped.add(d)
    for r in rv.get("reassign", []):
        if r["id"] in by and r["id"] not in dropped:
            by[r["id"]]["reassigned_from"] = by[r["id"]]["agent"]; by[r["id"]]["agent"] = r["to"]; by[r["id"]]["reassign_reason"] = r.get("reason")
    for a in rv.get("autonomy", []):
        if a["id"] in by and a["id"] not in dropped:
            by[a["id"]]["autonomy_was"] = by[a["id"]].get("autonomy"); by[a["id"]]["autonomy"] = a["to"]; by[a["id"]]["autonomy_reason"] = a.get("reason")
    out = [c for c in caps if c["id"] not in dropped]
    n = collections.Counter()
    for g in rv.get("gaps", []):
        n[g["agent"]] += 1
        out.append({"id": f"{g['agent']}-G{n[g['agent']]:02d}", "agent": g["agent"], "name": g["name"], "what": g.get("what", ""), "trigger": g.get("trigger", "on demand"),
                    "autonomy": g.get("autonomy", "founder_gate"), "folders": [], "encompasses": [], "inputs": [], "outputs": [], "tools": [], "skills": [],
                    "external_write": {"needed": False, "surface": None}, "sources": {"web": [], "bank": []}, "found_in": "review", "founder_sees": ""})
    return out


def md_to_html(md):
    """Small converter: headings, tables, lists, paragraphs, bold, code, front matter."""
    out = []; lines = md.splitlines(); i = 0
    if lines and lines[0].strip() == "---":
        j = lines.index("---", 1) if "---" in lines[1:] else 0
        fm = lines[1:j]; i = j + 1
        out.append("<dl class='fm'>" + "".join(f"<dt>{html.escape(l.split(':',1)[0])}</dt><dd>{html.escape(l.split(':',1)[1].strip())}</dd>" for l in fm if ":" in l) + "</dl>")
    def inline(s):
        s = html.escape(s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
        return s
    while i < len(lines):
        l = lines[i]
        if l.startswith("#"):
            n = len(l) - len(l.lstrip("#")); out.append(f"<h{min(n+2,6)}>{inline(l.lstrip('#').strip())}</h{min(n+2,6)}>"); i += 1
        elif l.strip().startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            rows = [r for r in rows if not all(re.match(r"^:?-+:?$", c) for c in r)]
            if rows:
                t = "<div class='tw'><table><tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr>"
                t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:]) + "</table></div>"
                out.append(t)
        elif re.match(r"^\s*(-|\d+\.)\s", l):
            items = []
            ordered = bool(re.match(r"^\s*\d+\.", l))
            while i < len(lines) and re.match(r"^\s*(-|\d+\.)\s", lines[i]):
                items.append(re.sub(r"^\s*(-|\d+\.)\s", "", lines[i])); i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
        elif l.strip().startswith("```"):
            buf = []; i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1; out.append("<pre>" + html.escape("\n".join(buf)) + "</pre>")
        elif l.strip() == "":
            i += 1
        else:
            buf = []
            while i < len(lines) and lines[i].strip() and not lines[i].startswith("#") and not lines[i].strip().startswith("|") and not re.match(r"^\s*(-|\d+\.)\s", lines[i]) and not lines[i].strip().startswith("```"):
                buf.append(lines[i]); i += 1
            out.append(f"<p>{inline(' '.join(buf))}</p>")
    return "\n".join(out)


def render_catalogue_md(caps):
    by = collections.defaultdict(list)
    for c in caps:
        by[c["agent"]].append(c)
    L = ["# ecomOS capability catalogue", "", f"{len(caps)} capabilities across {len(by)} agents. Generated by `scripts/build_agent_catalogue.py`. Edit the agent files, not this one.", ""]
    counts = collections.Counter(c.get("autonomy", "") for c in caps)
    L.append("| Autonomy | Count |\n|---|---|\n" + "\n".join(f"| {k} | {v} |" for k, v in counts.most_common()) + "\n")
    for code, rel, layer, name in AGENTS:
        rows = by.get(code, [])
        if not rows:
            continue
        L.append(f"## {name} ({code}), {len(rows)} capabilities\n")
        L.append("| id | name | trigger | autonomy | write | found in |\n|---|---|---|---|---|---|")
        for c in rows:
            w = c.get("external_write") or {}
            L.append(f"| {c['id']} | {c['name']} | {c.get('trigger','')} | {c.get('autonomy','')} | {(w.get('surface') or '') if w.get('needed') else ''} | {c.get('found_in','')} |")
        L.append("")
    return "\n".join(L)


def render_skills_md(caps):
    sk = collections.defaultdict(set)
    for c in caps:
        for s in c.get("skills", []) or []:
            sk[s].add(c["agent"])
    shared = sorted(os.listdir(os.path.join(A, "skills"))) if os.path.isdir(os.path.join(A, "skills")) else []
    L = ["# ecomOS skills index", "", f"{len(sk)} skills referenced by capabilities. Shared skills have a SKILL.md in `agents/skills/`. Agent skills are outlined in each agent file.", "",
         "| Skill | Called by | Shared file |\n|---|---|---|"]
    for s in sorted(sk):
        L.append(f"| {s} | {', '.join(sorted(sk[s]))} | {'yes' if s in shared else ''} |")
    return "\n".join(L)


def render_page(caps):
    agents_html = []
    for code, rel, layer, name in AGENTS:
        p = os.path.join(A, rel)
        body = md_to_html(open(p, encoding="utf-8").read()) if os.path.exists(p) else "<p>Not written yet.</p>"
        n = sum(1 for c in caps if c["agent"] == code)
        agents_html.append(f"<details class='agent' id='ag-{code}'><summary><span class='code'>{code}</span><b>{html.escape(name)}</b><span class='muted'>{layer} · {n} capabilities</span></summary><div class='body'>{body}</div></details>")
    data = json.dumps(caps, ensure_ascii=False).replace("</", "<\\/")
    tpl = open(os.path.join(ROOT, "scripts", "agent_catalogue_page.html"), encoding="utf-8").read()
    return tpl.replace("/*DATA*/", data).replace("<!--AGENTS-->", "\n".join(agents_html)).replace("<!--AGENTNAMES-->", json.dumps(CODE2NAME))


if __name__ == "__main__":
    caps = load()
    json.dump(caps, open(os.path.join(A, "catalogue.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(os.path.join(A, "CATALOGUE.md"), "w", encoding="utf-8").write(render_catalogue_md(caps))
    open(os.path.join(A, "SKILLS.md"), "w", encoding="utf-8").write(render_skills_md(caps))
    os.makedirs(os.path.join(ROOT, "reviews", "agents"), exist_ok=True)
    out = os.path.join(ROOT, "reviews", "agents", "ecomos-agent-catalogue.html")
    open(out, "w", encoding="utf-8").write(render_page(caps))
    print(len(caps), "capabilities;", out, os.path.getsize(out) // 1024, "KB")
