"""Join part files into one idea bank file. Usage: merge_idea_parts.py OUT.json PART1.json PART2.json ..."""
import json, sys
out, parts = sys.argv[1], sys.argv[2:]
ideas = []
for p in parts:
    ideas.extend(json.load(open(p, encoding="utf-8")))
json.dump(ideas, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(out, len(ideas), "ideas")
