"""Query the idea bank from the command line.

Examples:
  python3 scripts/ideas.py --summary
  python3 scripts/ideas.py --bottleneck site_speed --store hero_sku india_mobile custom_platform --top 15
  python3 scripts/ideas.py --query "font" --json
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intelligence import ideas as I

ap = argparse.ArgumentParser()
ap.add_argument("--bottleneck", nargs="*", default=None)
ap.add_argument("--store", nargs="*", default=None, help="store tags, see ideas/README.md")
ap.add_argument("--domain", nargs="*", default=None)
ap.add_argument("--query", default=None)
ap.add_argument("--exclude", nargs="*", default=None, help="idea ids already tried or rejected")
ap.add_argument("--top", type=int, default=20)
ap.add_argument("--json", action="store_true")
ap.add_argument("--summary", action="store_true")
a = ap.parse_args()

bank = I.load()
if a.summary:
    print(json.dumps(I.summary(bank), indent=1)); sys.exit()
bn = set(a.bottleneck) if a.bottleneck else None
sel = I.filter_ideas(bank, bn, set(a.store) if a.store else None, set(a.domain) if a.domain else None, a.query, set(a.exclude) if a.exclude else None)
sel = I.rank(sel, bn)[: a.top]
if a.json:
    print(json.dumps([dict(it, score=I.score(it, bn)) for it in sel], indent=1, ensure_ascii=False)); sys.exit()
print(f"{len(sel)} ideas shown of {len(bank)} in bank\n")
for it in sel:
    e = it["expected_effect"]
    print(f"{it['id']}  score {I.score(it, bn):>5}  [{it['effort']['size']}/{it['cost']}/{it['risk']['level']}]  {it['title']}")
    print(f"      signal: {it['signal']['check']}")
    print(f"      effect: {e['metric']} {e['direction']}, {e['size']} ({e['basis']}); rules {', '.join(it['sources']['rules'][:4])}")
