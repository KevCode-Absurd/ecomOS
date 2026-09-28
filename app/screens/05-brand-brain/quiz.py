"""Ten questions for a new hire or a new agent, with the answer key from the records, and a checker for pasted answers.

The questions are the facts anyone working on the brand must know: the returns window, the free shipping threshold,
the first order code, the guarantee line, the giving model, a line we never say, the default audience, the
positioning frame, a locked line, the product lines. Each question exists only when the brain holds the answer; the
key names the record. `check` takes pasted answers (one per line, in order) and scores each in code: a number
compared as a number, a code compared exactly, a phrase by word overlap; a wrong answer shows the right one with its
record. Used two ways: a person reads the key on day one; an agent's answers are pasted in to see what it got wrong,
and a miss can be recorded as a correction (7.5).
"""
from __future__ import annotations

import re

STOP = set("the a an and or of to in on for with is are was were be it its this that you your we our at from by as".split())


def _rec(brain, section, field):
    rows = [r for r in brain.records(section) if r.get("field") == field]
    rows.sort(key=lambda r: ({"approved": 0, "site_backed": 1}.get(r["tier"], 2), r["id"]))
    return rows[0] if rows else None


def _words(s) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9$%.]+", str(s or "").lower()) if w not in STOP and len(w) > 2}


def questions(brain, parts: dict) -> dict:
    qs = []

    def add(key, q, answer, record, kind, hint=None):
        if answer is None or answer == "" or answer == []:
            return
        qs.append({"n": len(qs) + 1, "key": key, "question": q, "answer": answer if isinstance(answer, str) else (", ".join(str(x) for x in answer) if isinstance(answer, list) else str(answer)), "record": record, "kind": kind, "hint": hint})

    r = _rec(brain, "policies", "returns_window_days")
    if r and isinstance(r.get("value"), (int, float)):
        add("returns", "How many days does a customer have to return an order?", str(int(r["value"])), r["id"], "number")
    r = _rec(brain, "offers", "free_shipping_threshold_usd")
    if r and isinstance(r.get("value"), (int, float)):
        add("free_shipping", "Above what order value is standard shipping free?", f"${r['value']:g}", r["id"], "number")
    r = _rec(brain, "offers", "first_order_code")
    if r and isinstance(r.get("value"), dict) and r["value"].get("code"):
        add("code", "What is the first order code, and how much is it worth?", f"{r['value']['code']}, {r['value'].get('discount_pct')} percent", r["id"], "code")
    r = _rec(brain, "policies", "happiness_guarantee") or _rec(brain, "offers", "guarantee")
    if r:
        add("guarantee", "What does the guarantee promise, in one line?", r.get("text") or str(r.get("value")), r["id"], "phrase")
    r = _rec(brain, "identity", "giving_model")
    if r:
        add("giving", "What does a purchase give, and to whom?", r.get("text") or str(r.get("value")), r["id"], "phrase")
    rl = [x for x in (parts.get("redlines") or []) if x["kind"] == "never_say"]
    if rl:
        add("never_say", "Name a phrase we never say about the product.", [x["text"] for x in rl[:5]], rl[0]["record"], "any_of", "any one of them counts")
    au = parts.get("audiences") or {}
    d = (au.get("defaults") or {}).get("ads")
    if d:
        name = next((p["name"] for p in au.get("profiles") or [] if p["id"] == d), None)
        add("audience", "Who is the default audience for ads?", name, d, "phrase")
    fr = next((x for x in brain.records("positioning") if x["id"].endswith(".positioning.frame")), None)
    if fr:
        add("frame", "What is the positioning frame, in your words?", fr.get("text") or str(fr.get("value")), fr["id"], "phrase", "the key words count, not the wording")
    lk = [x for x in (parts.get("locks") or {}).get("lines") or []]
    if lk:
        add("locked", "Quote a line that is locked word for word.", [x["text"] for x in lk[:5]], lk[0].get("record"), "any_of", "any one of them, exactly")
    r = _rec(brain, "products", "lines")
    if r and isinstance(r.get("value"), list):
        add("lines", "Name the product lines.", [str(x) for x in r["value"]], r["id"], "list", "at least half of them")
    return {"questions": qs, "counts": {"questions": len(qs)}, "text": "\n".join(f"{q['n']}. {q['question']}" for q in qs), "key": "\n".join(f"{q['n']}. {q['answer']} ({q['record']})" for q in qs),
            "note": "Only questions the brain can answer; the key names the record. Paste answers one per line, in order, to score them; a miss can be recorded as a correction."}


def _num(s):
    m = re.search(r"-?\d+(?:\.\d+)?", str(s or "").replace(",", ""))
    return float(m.group(0)) if m else None


def check(brain, qs: list[dict], answers: list[str]) -> dict:
    rows = []
    for q in qs:
        i = q["n"] - 1
        given = answers[i].strip() if i < len(answers) else ""
        ok, why = False, "no answer"
        if given:
            if q["kind"] == "number":
                ok = _num(given) is not None and _num(q["answer"]) is not None and abs(_num(given) - _num(q["answer"])) < 0.01
                why = "the number matches" if ok else f"the brain says {q['answer']}"
            elif q["kind"] == "code":
                code = q["answer"].split(",")[0].strip().upper()
                ok = code in given.upper()
                why = "the code matches" if ok else f"the code is {code}"
            elif q["kind"] == "any_of":
                opts = [o.strip().lower() for o in q["answer"].split(", ")]
                ok = any(o and o in given.lower() for o in opts) or any(len(_words(o) & _words(given)) >= max(2, len(_words(o)) // 2) for o in opts if _words(o))
                why = "one of the lines" if ok else "none of the lines on record"
            elif q["kind"] == "list":
                opts = [o.strip().lower() for o in q["answer"].split(", ")]
                hit = sum(1 for o in opts if o and o in given.lower())
                ok = hit >= max(1, (len(opts) + 1) // 2)
                why = f"{hit} of {len(opts)} named"
            else:
                aw, gw = _words(q["answer"]), _words(given)
                share = len(aw & gw) / len(aw) if aw else 0
                ok = share >= 0.4
                why = f"{round(share * 100)} percent of the key words" + ("" if ok else f"; the brain says: {q['answer'][:100]}")
        rows.append({"n": q["n"], "question": q["question"], "given": given, "ok": ok, "why": why, "answer": q["answer"], "record": q["record"]})
    score = sum(1 for r in rows if r["ok"])
    return {"rows": rows, "score": score, "of": len(rows), "pct": round(100 * score / len(rows)) if rows else None, "misses": [r for r in rows if not r["ok"]],
            "note": "Scored in code: numbers as numbers, codes exactly, lines by word overlap. Record a miss as a correction and every agent reads it."}
