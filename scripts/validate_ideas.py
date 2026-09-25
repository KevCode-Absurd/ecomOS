"""Validate an idea bank file against ideas/schema.json and the playbook it came from.

Usage: python3 scripts/validate_ideas.py ideas/v1/08-SPD-speed.json [--playbook playbooks/v2/08-SPD-speed/PLAYBOOK.md]
No third-party packages. Exit 1 on any failure.
"""
import json, re, sys, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = json.load(open(os.path.join(ROOT, "ideas", "schema.json"), encoding="utf-8"))
PROPS = SCHEMA["items"]["properties"]
REQUIRED = SCHEMA["items"]["required"]


def enum_of(prop):
    return prop.get("enum")


def check_str(v, spec, path, errs):
    if not isinstance(v, str):
        errs.append(f"{path}: not a string"); return
    if "minLength" in spec and len(v) < spec["minLength"]: errs.append(f"{path}: shorter than {spec['minLength']}")
    if "maxLength" in spec and len(v) > spec["maxLength"]: errs.append(f"{path}: longer than {spec['maxLength']} ({len(v)})")
    if "pattern" in spec and not re.search(spec["pattern"], v): errs.append(f"{path}: does not match {spec['pattern']}: {v!r}")
    if "enum" in spec and v not in spec["enum"]: errs.append(f"{path}: {v!r} not in enum")
    if "—" in v: errs.append(f"{path}: em dash")


def check(v, spec, path, errs):
    t = spec.get("type")
    if "enum" in spec and t is None:
        if v not in spec["enum"]: errs.append(f"{path}: {v!r} not in enum")
        return
    if t == "string": check_str(v, spec, path, errs)
    elif t == "boolean":
        if not isinstance(v, bool): errs.append(f"{path}: not a boolean")
    elif t == "array":
        if not isinstance(v, list): errs.append(f"{path}: not a list"); return
        if "minItems" in spec and len(v) < spec["minItems"]: errs.append(f"{path}: fewer than {spec['minItems']} items")
        if "maxItems" in spec and len(v) > spec["maxItems"]: errs.append(f"{path}: more than {spec['maxItems']} items")
        for i, x in enumerate(v): check(x, spec["items"], f"{path}[{i}]", errs)
    elif t == "object":
        if not isinstance(v, dict): errs.append(f"{path}: not an object"); return
        for k in spec.get("required", []):
            if k not in v: errs.append(f"{path}.{k}: missing")
        for k, x in v.items():
            if k not in spec["properties"]: errs.append(f"{path}.{k}: unknown field")
            else: check(x, spec["properties"][k], f"{path}.{k}", errs)


def main():
    args = sys.argv[1:]
    pb = None
    if "--playbook" in args:
        i = args.index("--playbook"); pb = args[i + 1]; del args[i:i + 2]
    path = args[0]
    ideas = json.load(open(path, encoding="utf-8"))
    errs, warns = [], []
    if not isinstance(ideas, list): sys.exit("top level must be a list")
    folder = os.path.basename(path).replace(".json", "")
    if pb is None:
        pb = os.path.join(ROOT, "playbooks", "v2", folder, "PLAYBOOK.md")
    pbtext = open(pb, encoding="utf-8").read() if os.path.exists(pb) else ""
    pb_rules = set(re.findall(r"^\*\*((?:R|P|F|C)\d+[a-z]?)\.", pbtext, re.M)) | set(re.findall(r"^### ((?:P|F|C)\d+[a-z]?)\.", pbtext, re.M)) | set(re.findall(r"\b((?:C|F)\d+)\b", pbtext))
    cards = json.load(open(os.path.join(ROOT, "data", "library-v3", "cards.json"), encoding="utf-8"))["cards"]
    card_ids = [c["id"] for c in cards]
    ids, titles = set(), {}
    for n, it in enumerate(ideas):
        p = f"[{n}]"
        if not isinstance(it, dict): errs.append(f"{p}: not an object"); continue
        for k in REQUIRED:
            if k not in it: errs.append(f"{p}.{k}: missing")
        for k, v in it.items():
            if k not in PROPS: errs.append(f"{p}.{k}: unknown field")
            else: check(v, PROPS[k], f"{p}.{k}", errs)
        iid = it.get("id", "")
        if iid in ids: errs.append(f"{p}: duplicate id {iid}")
        ids.add(iid)
        t = re.sub(r"[^a-z0-9 ]", "", it.get("title", "").lower()).strip()
        if t in titles: errs.append(f"{p}: duplicate title of {titles[t]}: {it.get('title')!r}")
        titles[t] = iid
        src = it.get("sources", {})
        for c in src.get("cards", []):
            if not any(x.startswith(c) for x in card_ids): errs.append(f"{p} {iid}: card {c} not in cards.json")
        for r in src.get("rules", []):
            if pb_rules and r not in pb_rules: warns.append(f"{p} {iid}: rule {r} not found in playbook")
        if it.get("general_practice") and it.get("expected_effect", {}).get("basis") != "general_practice" and not src.get("cards"):
            warns.append(f"{p} {iid}: general_practice with no cards but basis {it['expected_effect'].get('basis')}")
        for k in ("hypothesis", "title"):
            txt = it.get(k, "")
            if re.search(r"(?<!Chat)GPT(?!Bot|-\d)", txt) or ".env" in txt: errs.append(f"{p}.{k}: forbidden mention")
    raw = open(path, encoding="utf-8").read()
    if "—" in raw: errs.append(f"file contains {raw.count(chr(0x2014))} em dashes")
    from collections import Counter
    bn = Counter(b for it in ideas if isinstance(it, dict) for b in it.get("bottleneck", [])[:1])
    print(f"{folder}: {len(ideas)} ideas; primary bottlenecks {dict(bn)}; general_practice {sum(1 for it in ideas if isinstance(it, dict) and it.get('general_practice'))}; cards cited {len(set(c for it in ideas if isinstance(it, dict) for c in it.get('sources', {}).get('cards', [])))}")
    for w in warns[:30]: print("WARN", w)
    if len(warns) > 30: print(f"WARN ... {len(warns) - 30} more")
    for e in errs[:60]: print("FAIL", e)
    if len(errs) > 60: print(f"FAIL ... {len(errs) - 60} more")
    print("PASS" if not errs else f"FAILED with {len(errs)} errors")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
