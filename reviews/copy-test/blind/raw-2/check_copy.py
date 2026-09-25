"""Check every ad in copy-plan.md (and report.md if present): first-line length, headline and
description length, word count, emoji count, and Flesch reading ease computed in code.
Run from the repo root: python3 reviews/copy-test/blind/raw-2/check_copy.py
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(ROOT, "..", "copy-plan.md")
text = open(src, encoding="utf-8").read()
EMOJI = re.compile(r"[\U0001F300-\U0001FAFF☀-➿⭐⭕⌚-⏿️]")

def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w: return 0
    if len(w) <= 3: return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))

def flesch(s):
    s2 = re.sub(r"\[confirm before launch[^\]]*\]", "", s)
    s2 = re.sub(r"\[date, confirm before launch\]", "date", s2)
    s2 = EMOJI.sub("", s2)
    words = [w for w in re.findall(r"[A-Za-z0-9₹%+,'.-]+", s2) if re.search(r"[A-Za-z0-9]", w)]
    sents = [x for x in re.split(r"[.!?]+(?:\s|$)|\n\n", s2) if re.search(r"[A-Za-z]", x)]
    W, S = len(words), max(1, len(sents))
    SY = sum(syllables(w) for w in words)
    fre = 206.835 - 1.015 * (W / S) - 84.6 * (SY / W if W else 0)
    grade = 0.39 * (W / S) + 11.8 * (SY / W if W else 0) - 15.59
    return round(fre, 1), round(grade, 1), W, S

ads = re.split(r"\n#### ", text)[1:]
out = []
for block in ads:
    name = block.split("\n", 1)[0].strip()
    m = re.search(r"- Primary text:\n\n(.*?)\n\n- Headline: (.*?)\n- Description: (.*?)\n", block, re.S)
    if not m: continue
    body, head, desc = m.group(1), m.group(2).strip(), m.group(3).strip()
    paras = [p.strip() for p in body.split("\n\n") if p.strip()]
    first = re.sub(r"\s*\[confirm before launch[^\]]*\]", "", paras[0])
    clean_body = re.sub(r"\s*\[confirm before launch[^\]]*\]", "", body)
    fre, grade, W, S = flesch(clean_body)
    rec = {
        "ad": name,
        "first_line": first,
        "first_line_chars": len(first),
        "first_line_ok_under_125": len(first) < 125,
        "headline": head, "headline_chars": len(head), "headline_ok_under_40": len(head) < 40,
        "description": desc, "description_chars": len(desc), "description_ok_under_30": len(desc) <= 30,
        "primary_words": W, "primary_ok_under_300_words": W < 300,
        "emoji_in_primary": len(EMOJI.findall(clean_body)), "emoji_in_headline": len(EMOJI.findall(head)),
        "flesch_reading_ease": fre, "flesch_kincaid_grade": grade, "sentences": S,
        "confirm_tags": len(re.findall(r"confirm before launch", block)),
    }
    out.append(rec)
json.dump(out, open(os.path.join(ROOT, "copy_checks.json"), "w"), indent=1, ensure_ascii=False)
for r in out:
    flags = []
    if not r["first_line_ok_under_125"]: flags.append("FIRST LINE")
    if not r["headline_ok_under_40"]: flags.append("HEADLINE")
    if not r["description_ok_under_30"]: flags.append("DESCRIPTION")
    if not r["primary_ok_under_300_words"]: flags.append("WORDS")
    if r["emoji_in_primary"] > 4 or r["emoji_in_headline"] > 1: flags.append("EMOJI")
    if r["flesch_kincaid_grade"] >= 10: flags.append("GRADE")
    print(f"{r['ad'][:40]:40} first {r['first_line_chars']:3} head {r['headline_chars']:2} desc {r['description_chars']:2} words {r['primary_words']:3} emoji {r['emoji_in_primary']}/{r['emoji_in_headline']} FRE {r['flesch_reading_ease']:5} grade {r['flesch_kincaid_grade']:4} confirm {r['confirm_tags']} {' '.join(flags)}")
print(len(out), "ads checked")
