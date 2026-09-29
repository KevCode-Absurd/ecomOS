"""Writes app/handoff/ECOMOS-HANDOFF-APPENDIX.md from the third jobs list (app/jtbd/v3)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "jtbd"))
import build_v3 as b

screens, enablers, problems = b.load()
assert not problems, problems
top30, pool = b.start_now(screens)
rows = b.enabler_use(screens, enablers)
FOCUS = ["00-today", "09-creative", "11-paid-social", "07-landing-pages-cro", "15-customers-cx"]
N = sum(len(d["jobs"]) for d in screens)
L = ["# ecomOS hand-off, appendix: our own answers", "",
     "Paste this only after you have finished steps 1 to 3 of the main brief. Then compare: where do we agree, where did you find something we missed, and where do you think we are wrong?", "",
     f"Our third list has {len(screens)} screens, {N} tactical jobs, {len(rows)} enablers and {pool} start-now jobs. Scores use 4 x money + 2 x satisfaction + 2 x speed + 2 x ease, out of 50.", "",
     f"## A. Start now: our top {len(top30)}", "",
     f"Ready on onboarding day and a first output in hours or days, picked from {pool} such jobs, at most 3 per screen.", "",
     "| # | Job | Screen | Score | Effort |", "|---|---|---|---|---|"]
for i, j in enumerate(top30, 1):
    L.append(f"| {i} | {j['job']} | {j['title']} | {j['total']} | {j['effort']} |")
L += ["", "## B. Enablers, ranked by the total score of the jobs they power", "",
      "| # | Enabler | What it does | Jobs | Start now | Screens |", "|---|---|---|---|---|---|"]
for i, r in enumerate(rows[:40], 1):
    what = r.get("what", "").split(". ")[0].rstrip(".")
    L.append(f"| {i} | {r['name']} | {what} | {r['n']} | {r['now']} | {len(r['screens_used'])} |")
rest = rows[40:]
L += ["", f"The other {len(rest)} enablers, each used by fewer jobs: " + ", ".join(r["name"] for r in rest) + ".", "",
      "Note: the awareness heat map powers jobs on 10 screens but only 1 can start now, because the tagging rules must be written first. The AI video stack needs a paid video tool, so it sits low on readiness, not on value.", "",
      "## C. Our top jobs for every screen", ""]
for d in screens:
    L += [f"### {d['screen'][:2]} {d['title']}", ""]
    for t in d["top_jobs"]:
        L.append(f"- **{t['id']}.** {t['job']} *Metric: {t['metric']}.*")
    L.append("")
L += ["## D. Our tactical jobs for the 5 focus screens", "", "Titles only, grouped under the top job they serve, highest score first. S = start now.", ""]
for d in screens:
    if d["screen"] not in FOCUS:
        continue
    L += [f"### {d['screen'][:2]} {d['title']}", ""]
    for t in d["top_jobs"]:
        L.append(f"**{t['id']}.** {t['job']}")
        L.append("")
        for j in sorted((j for j in d["jobs"] if j["top"] == t["id"]), key=lambda j: -j["total"]):
            s = ", S" if j["start_now"] else ""
            L.append(f"- {j['id']} ({j['total']}{s}) {j['job']} *Enablers: {', '.join(r for r in j['enablers'])}.*")
        L.append("")
out = os.path.join(os.path.dirname(__file__), "ECOMOS-HANDOFF-APPENDIX.md")
open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
print(out)
