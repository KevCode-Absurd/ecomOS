"""Find likely duplicate ideas across the bank by title and hypothesis overlap. Read-only; prints pairs.

Usage: python3 scripts/idea_dupes.py [--threshold 0.6] [--same-domain]
"""
import argparse, os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intelligence import ideas as I

STOP = set("a an the and or of to for in on at by with from into over under is are be as not no every each one per your our its their this that than then when before after if it do does use run set add keep make put get let".split())

def toks(s):
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP and len(w) > 2}

def jacc(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0

ap = argparse.ArgumentParser()
ap.add_argument("--threshold", type=float, default=0.6)
ap.add_argument("--same-domain", action="store_true")
ap.add_argument("--json", action="store_true")
a = ap.parse_args()
bank = I.load()
T = [(it["id"], it["domain"], toks(it["title"]), toks(it["title"] + " " + it["hypothesis"])) for it in bank]
pairs = []
for i in range(len(T)):
    for j in range(i + 1, len(T)):
        if not a.same_domain and T[i][1] == T[j][1]:
            continue
        s = jacc(T[i][2], T[j][2])
        if s >= a.threshold:
            pairs.append((round(s, 2), round(jacc(T[i][3], T[j][3]), 2), T[i][0], T[j][0]))
pairs.sort(reverse=True)
if a.json:
    print(json.dumps(pairs)); sys.exit()
print(f"{len(bank)} ideas, {len(pairs)} pairs at title overlap >= {a.threshold}")
byid = {it["id"]: it for it in bank}
for s, s2, x, y in pairs[:80]:
    print(f"{s:.2f} {s2:.2f}  {x} | {byid[x]['title']}\n            {y} | {byid[y]['title']}")
